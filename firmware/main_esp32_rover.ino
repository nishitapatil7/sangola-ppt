/* ==============================================================================
   PROJECT: AURA-X AI-POWERED EXPLORATION ROVER
   MODULE:  Main Rover Controller Firmware (ESP32 Dual-Core)
   FRAMEWORK: FreeRTOS + Arduino ESP32 Core
   DATE:    October 2026
   AUTHOR:  AURA-X Robotics Engineering Cohort
   
   ARCHITECTURE ENFORCEMENT:
   - Core 1: Motor PWM & Time-Critical Safety Supervisor (High Priority)
   - Core 0: LoRa SPI Packet Radio & Telemetry Serialization
   - Local firmware retains absolute physical veto over actuation.
   - Command lease timer (1.0s) safely halts rover on packet loss.
   - Ultrasonic echo line must be level-shifted (1k/2k divider) to 3.3V!
   ============================================================================== */

#include <Arduino.h>
#include <SPI.h>

// -----------------------------------------------------------------------------
// PIN ALLOCATION & HARDWARE DEFINITIONS (Carefully chosen to avoid strapping pins)
// -----------------------------------------------------------------------------
// Motor Driver Pins (DRV8833 / L298N)
#define PIN_MOTOR_L_PWM    25  // Left Motor Speed PWM
#define PIN_MOTOR_L_DIR    26  // Left Motor Direction
#define PIN_MOTOR_R_PWM    27  // Right Motor Speed PWM
#define PIN_MOTOR_R_DIR    14  // Right Motor Direction
#define PIN_DRIVER_ENABLE  13  // Hardware Driver Enable Line (Veto cut)

// Ultrasonic Sensor (HC-SR04)
#define PIN_US_TRIG        32  // Trigger Output (3.3V to HC-SR04 Trig)
#define PIN_US_ECHO        35  // Echo Input (Input-only pin; MUST BE LEVEL SHIFTED to 3.3V!)

// Physical Emergency Stop Button
#define PIN_HARDWARE_ESTOP 34  // Active LOW hardware cutoff button (Input-only, external pullup)

// LoRa SPI Interface (Semtech SX1278 / RA-02 433MHz)
#define LORA_SCK           18
#define LORA_MISO          19
#define LORA_MOSI          23
#define LORA_CS            5
#define LORA_RST           17
#define LORA_DIO0          4

// Battery ADC Voltage Monitor
#define PIN_BATT_SENSE     36  // VP (Analog Input via 10k/10k divider)

// -----------------------------------------------------------------------------
// OPERATIONAL CONSTANTS & SAFETY ENVELOPES
// -----------------------------------------------------------------------------
#define SAFETY_STOP_DISTANCE_CM   28.0f // Obstacle veto boundary
#define COMMAND_LEASE_TIMEOUT_MS  1000  // Maximum lease before auto-halt
#define LORA_NODE_ID_ROVER        0x01
#define LORA_NODE_ID_BASE         0xFE
#define PROTOCOL_VERSION          1

// Finite State Machine Enums
enum RoverMode {
    MODE_INIT = 0,
    MODE_MANUAL_DRIVE,
    MODE_AUTO_AVOIDANCE,
    MODE_AI_MISSION,
    MODE_SAFE_STOP
};

// Structured LoRa Command Packet Format (Table 7 in Report)
struct __attribute__((packed)) LoRaCommandPacket {
    uint8_t  version;
    uint8_t  msg_type;      // 0x01: CMD, 0x02: STOP, 0x03: HEARTBEAT
    uint8_t  node_id;
    uint16_t seq_id;
    uint8_t  action_code;   // 1: FWD, 2: REV, 3: LEFT, 4: RIGHT, 5: STOP
    uint8_t  speed;         // 0-255 PWM
    uint16_t lease_ms;      // Validity duration
    uint16_t checksum;
};

// Structured Telemetry Packet Format
struct __attribute__((packed)) LoRaTelemetryPacket {
    uint8_t  version;
    uint8_t  msg_type;      // 0x10: TELEMETRY
    uint8_t  node_id;
    uint16_t seq_id;
    uint8_t  current_mode;
    uint16_t battery_mv;
    uint16_t clearance_mm;
    int16_t  pitch_cd;      // Centi-degrees
    int16_t  roll_cd;
    uint16_t yaw_deg;
    uint8_t  fault_code;
    uint16_t checksum;
};

// -----------------------------------------------------------------------------
// SHARED SYSTEM STATE (Protected by Mutex)
// -----------------------------------------------------------------------------
SemaphoreHandle_t xStateMutex;

volatile RoverMode current_mode = MODE_INIT;
volatile float g_front_clearance_cm = 100.0f;
volatile uint32_t g_last_valid_command_time = 0;
volatile uint16_t g_active_lease_ms = 0;
volatile int16_t g_target_pwm_left = 0;
volatile int16_t g_target_pwm_right = 0;
volatile bool g_estop_tripped = false;
volatile uint16_t g_packet_seq_counter = 0;

// -----------------------------------------------------------------------------
// HARDWARE ISR: PHYSICAL EMERGENCY STOP
// -----------------------------------------------------------------------------
void IRAM_ATTR isr_emergency_stop() {
    // Hardware cutoff: disable motor driver pin immediately in ISR!
    digitalWrite(PIN_DRIVER_ENABLE, LOW);
    digitalWrite(PIN_MOTOR_L_PWM, LOW);
    digitalWrite(PIN_MOTOR_R_PWM, LOW);
    g_estop_tripped = true;
    current_mode = MODE_SAFE_STOP;
}

// -----------------------------------------------------------------------------
// SENSOR UTILITY: ULTRASONIC PING
// -----------------------------------------------------------------------------
float read_ultrasonic_clearance() {
    digitalWrite(PIN_US_TRIG, LOW);
    delayMicroseconds(2);
    digitalWrite(PIN_US_TRIG, HIGH);
    delayMicroseconds(10);
    digitalWrite(PIN_US_TRIG, LOW);
    
    // Measure echo pulse (timeout 18ms approx 300cm)
    unsigned long duration = pulseIn(PIN_US_ECHO, HIGH, 18000);
    if (duration == 0) return 999.0f; // No echo / out of range
    
    // Speed of sound: 343 m/s = 0.0343 cm/us -> distance = duration * 0.0343 / 2
    return (duration * 0.0343f) / 2.0f;
}

// -----------------------------------------------------------------------------
// FREERTOS TASK 1: MOTOR CONTROL & LEASE MONITOR (CORE 1 - 50Hz)
// -----------------------------------------------------------------------------
void Task_MotorControl(void *pvParameters) {
    TickType_t xLastWakeTime = xTaskGetTickCount();
    const TickType_t xFrequency = pdMS_TO_TICKS(20); // 50Hz control loop

    for (;;) {
        uint32_t now = millis();

        xSemaphoreTake(xStateMutex, portMAX_DELAY);

        // 1. Check Hardware E-Stop Condition
        if (g_estop_tripped || digitalRead(PIN_HARDWARE_ESTOP) == LOW) {
            digitalWrite(PIN_DRIVER_ENABLE, LOW);
            g_target_pwm_left = 0;
            g_target_pwm_right = 0;
            current_mode = MODE_SAFE_STOP;
        }
        // 2. Command Freshness Lease Check (Table 15)
        else if (current_mode == MODE_MANUAL_DRIVE) {
            if ((now - g_last_valid_command_time) > g_active_lease_ms) {
                // Lease expired! Auto-halt motors to prevent runaway robot
                g_target_pwm_left = 0;
                g_target_pwm_right = 0;
            }
        }
        // 3. Ultrasonic Distance Veto Guard
        if (g_front_clearance_cm < SAFETY_STOP_DISTANCE_CM) {
            if (g_target_pwm_left > 0 && g_target_pwm_right > 0) {
                // VETO forward movement!
                g_target_pwm_left = 0;
                g_target_pwm_right = 0;
            }
        }

        // Apply PWM and Direction to Motors
        if (g_target_pwm_left >= 0) {
            digitalWrite(PIN_MOTOR_L_DIR, HIGH);
            analogWrite(PIN_MOTOR_L_PWM, g_target_pwm_left);
        } else {
            digitalWrite(PIN_MOTOR_L_DIR, LOW);
            analogWrite(PIN_MOTOR_L_PWM, abs(g_target_pwm_left));
        }

        if (g_target_pwm_right >= 0) {
            digitalWrite(PIN_MOTOR_R_DIR, HIGH);
            analogWrite(PIN_MOTOR_R_PWM, g_target_pwm_right);
        } else {
            digitalWrite(PIN_MOTOR_R_DIR, LOW);
            analogWrite(PIN_MOTOR_R_PWM, abs(g_target_pwm_right));
        }

        xSemaphoreGive(xStateMutex);
        vTaskDelayUntil(&xLastWakeTime, xFrequency);
    }
}

// -----------------------------------------------------------------------------
// FREERTOS TASK 2: SAFETY SUPERVISOR & SENSORS (CORE 1 - 25Hz)
// -----------------------------------------------------------------------------
void Task_SafetySupervisor(void *pvParameters) {
    TickType_t xLastWakeTime = xTaskGetTickCount();
    const TickType_t xFrequency = pdMS_TO_TICKS(40); // 25Hz sensor polling

    for (;;) {
        float distance = read_ultrasonic_clearance();
        
        xSemaphoreTake(xStateMutex, portMAX_DELAY);
        g_front_clearance_cm = distance;

        // Reactive Obstacle Avoidance Loop (Section 8)
        if (current_mode == MODE_AUTO_AVOIDANCE && !g_estop_tripped) {
            if (distance < SAFETY_STOP_DISTANCE_CM) {
                // Stop and pivot clear
                g_target_pwm_left = -120;
                g_target_pwm_right = 120;
            } else {
                // Advance forward at regulated survey speed
                g_target_pwm_left = 150;
                g_target_pwm_right = 150;
            }
        }
        xSemaphoreGive(xStateMutex);

        vTaskDelayUntil(&xLastWakeTime, xFrequency);
    }
}

// -----------------------------------------------------------------------------
// FREERTOS TASK 3: LORA RADIO PACKET LINK (CORE 0 - 20Hz)
// -----------------------------------------------------------------------------
void Task_LoRaLink(void *pvParameters) {
    for (;;) {
        // Serial / SPI LoRa Packet Ingestion
        if (Serial.available() >= sizeof(LoRaCommandPacket)) {
            LoRaCommandPacket cmd;
            Serial.readBytes((char*)&cmd, sizeof(LoRaCommandPacket));

            // Validate Protocol Version & Target Node ID
            if (cmd.version == PROTOCOL_VERSION && (cmd.node_id == LORA_NODE_ID_ROVER || cmd.node_id == 0xFF)) {
                xSemaphoreTake(xStateMutex, portMAX_DELAY);
                
                g_last_valid_command_time = millis();
                g_active_lease_ms = cmd.lease_ms > 0 ? cmd.lease_ms : COMMAND_LEASE_TIMEOUT_MS;

                // Handle Command Action Primitives (Allowlist Enforcement)
                switch (cmd.action_code) {
                    case 1: // MOVE_FORWARD
                        if (g_front_clearance_cm >= SAFETY_STOP_DISTANCE_CM) {
                            g_target_pwm_left = cmd.speed;
                            g_target_pwm_right = cmd.speed;
                        }
                        break;
                    case 2: // MOVE_BACKWARD
                        g_target_pwm_left = -cmd.speed;
                        g_target_pwm_right = -cmd.speed;
                        break;
                    case 3: // TURN_LEFT
                        g_target_pwm_left = -cmd.speed;
                        g_target_pwm_right = cmd.speed;
                        break;
                    case 4: // TURN_RIGHT
                        g_target_pwm_left = cmd.speed;
                        g_target_pwm_right = -cmd.speed;
                        break;
                    case 5: // STOP
                    default:
                        g_target_pwm_left = 0;
                        g_target_pwm_right = 0;
                        break;
                }

                xSemaphoreGive(xStateMutex);
            }
        }
        vTaskDelay(pdMS_TO_TICKS(50));
    }
}

// -----------------------------------------------------------------------------
// FREERTOS TASK 4: TELEMETRY BROADCASTER (CORE 0 - 1.5Hz)
// -----------------------------------------------------------------------------
void Task_Telemetry(void *pvParameters) {
    for (;;) {
        LoRaTelemetryPacket telem;
        telem.version = PROTOCOL_VERSION;
        telem.msg_type = 0x10;
        telem.node_id = LORA_NODE_ID_ROVER;

        xSemaphoreTake(xStateMutex, portMAX_DELAY);
        telem.seq_id = ++g_packet_seq_counter;
        telem.current_mode = (uint8_t)current_mode;
        telem.clearance_mm = (uint16_t)(g_front_clearance_cm * 10.0f);
        
        // Read battery voltage through calibrated divider
        int raw_adc = analogRead(PIN_BATT_SENSE);
        telem.battery_mv = (uint16_t)((raw_adc / 4095.0f) * 3.3f * 2.5f * 1000.0f); // Calibrated
        
        telem.pitch_cd = 120;  // Placeholder for MPU-9250 centi-degrees
        telem.roll_cd  = -50;
        telem.yaw_deg  = 142;
        telem.fault_code = g_estop_tripped ? 0x01 : 0x00;
        xSemaphoreGive(xStateMutex);

        // Send telemetry packet over LoRa serial bridge
        Serial.write((uint8_t*)&telem, sizeof(LoRaTelemetryPacket));

        vTaskDelay(pdMS_TO_TICKS(667)); // ~1.5 Hz broadcast rate
    }
}

// -----------------------------------------------------------------------------
// ARDUINO SETUP & SYSTEM BRING-UP
// -----------------------------------------------------------------------------
void setup() {
    Serial.begin(115200);

    // Motor driver pin configurations
    pinMode(PIN_MOTOR_L_PWM, OUTPUT);
    pinMode(PIN_MOTOR_L_DIR, OUTPUT);
    pinMode(PIN_MOTOR_R_PWM, OUTPUT);
    pinMode(PIN_MOTOR_R_DIR, OUTPUT);
    pinMode(PIN_DRIVER_ENABLE, OUTPUT);
    digitalWrite(PIN_DRIVER_ENABLE, HIGH); // Enable driver logic

    // Ultrasonic sensor pins
    pinMode(PIN_US_TRIG, OUTPUT);
    pinMode(PIN_US_ECHO, INPUT);

    // Hardware Emergency Stop with interrupt
    pinMode(PIN_HARDWARE_ESTOP, INPUT_PULLUP);
    attachInterrupt(digitalPinToInterrupt(PIN_HARDWARE_ESTOP), isr_emergency_stop, FALLING);

    // Battery sense pin
    pinMode(PIN_BATT_SENSE, INPUT);

    // Create RTOS Mutex
    xStateMutex = xSemaphoreCreateMutex();

    // Transition to Standby
    current_mode = MODE_MANUAL_DRIVE;

    // Pin RTOS Tasks to Cores
    // Core 1 (High priority time-critical motor & safety loops)
    xTaskCreatePinnedToCore(Task_MotorControl, "MotorCtrl", 2048, NULL, 3, NULL, 1);
    xTaskCreatePinnedToCore(Task_SafetySupervisor, "SafetySup", 2048, NULL, 2, NULL, 1);

    // Core 0 (Communications and Telemetry)
    xTaskCreatePinnedToCore(Task_LoRaLink, "LoRaLink", 3072, NULL, 1, NULL, 0);
    xTaskCreatePinnedToCore(Task_Telemetry, "Telemetry", 2048, NULL, 1, NULL, 0);
}

void loop() {
    // Arduino loop remains empty; FreeRTOS scheduler handles all tasks
    vTaskDelay(portMAX_DELAY);
}

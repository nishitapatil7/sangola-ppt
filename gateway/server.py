import os
import time
import json
import random
import asyncio
from typing import Optional, List
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, StreamingResponse
from pydantic import BaseModel

app = FastAPI(title="AURA-X Ground Mission Control Gateway", version="1.0.0")

# Mount static files
app.mount("/static", StaticFiles(directory="gateway/static"), name="static")

# Rover State Representation based on Reference Report
class RoverState:
    def __init__(self):
        self.mode = "MANUAL_DRIVE"  # INIT, MANUAL_DRIVE, AUTO_AVOIDANCE, AI_MISSION, SAFE_STOP
        self.battery_voltage = 7.82  # 2S Li-ion nominal 7.4V, charged 8.4V
        self.front_clearance_cm = 65.4
        self.pitch_deg = 1.2
        self.roll_deg = -0.5
        self.yaw_deg = 142.0
        self.lora_rssi_dbm = -74
        self.lora_snr_db = 9.2
        self.lora_packets_rx = 1420
        self.lora_packets_lost = 12
        self.wifi_connected = True
        self.ai_available = True
        self.command_lease_ms = 1000
        self.lease_remaining_ms = 0
        self.last_command_time = time.time()
        self.e_stop_active = False
        self.left_motor_pwm = 0
        self.right_motor_pwm = 0
        self.events: List[dict] = [
            {"time": "00:00:01", "type": "BOOT", "msg": "ESP32 dual-core boot verified. Logic rail: 3.31V."},
            {"time": "00:00:02", "type": "RF_INIT", "msg": "LoRa SX1278 (433MHz) online. Sync word: 0x12."},
            {"time": "00:00:03", "type": "SENSORS", "msg": "HC-SR04 ultrasonic echo valid (divider protected). MPU-9250 calibrated."},
            {"time": "00:00:05", "type": "LINK", "msg": "Wi-Fi camera stream active (802.11 b/g/n @ 2.4GHz)."},
            {"time": "00:00:06", "type": "STATUS", "msg": "Ready for operator command or autonomous mission."}
        ]

    def log_event(self, event_type: str, message: str):
        ts = time.strftime("%H:%M:%S")
        self.events.insert(0, {"time": ts, "type": event_type, "msg": message})
        if len(self.events) > 50:
            self.events.pop()

    def update_simulation(self):
        # Battery slowly discharges
        if self.battery_voltage > 6.8:
            self.battery_voltage -= 0.00005
        
        # In AUTO_AVOIDANCE or AI_MISSION, fluctuate distance and steer
        if self.mode in ["AUTO_AVOIDANCE", "AI_MISSION"] and not self.e_stop_active:
            # Simulate forward movement
            self.front_clearance_cm -= random.uniform(1.0, 3.5)
            if self.front_clearance_cm < 28.0:
                self.log_event("SAFETY_GUARD", f"Obstacle at {self.front_clearance_cm:.1f} cm! Firmware vetoed forward motion.")
                self.left_motor_pwm = -120
                self.right_motor_pwm = 120
                self.front_clearance_cm = random.uniform(55.0, 85.0)
                self.yaw_deg = (self.yaw_deg + 45) % 360
                self.log_event("REACTIVE_NAV", f"Autonomous pivot executed. New heading: {self.yaw_deg:.0f}°.")
            else:
                self.left_motor_pwm = 150
                self.right_motor_pwm = 150
        elif self.mode == "SAFE_STOP" or self.e_stop_active:
            self.left_motor_pwm = 0
            self.right_motor_pwm = 0

        # Command lease timeout check
        if self.mode == "MANUAL_DRIVE":
            elapsed = (time.time() - self.last_command_time) * 1000
            self.lease_remaining_ms = max(0, int(self.command_lease_ms - elapsed))
            if self.lease_remaining_ms == 0 and (self.left_motor_pwm != 0 or self.right_motor_pwm != 0):
                self.left_motor_pwm = 0
                self.right_motor_pwm = 0
                self.log_event("LEASE_EXPIRED", "Drive command lease expired (1.0s). Motors halted safely.")

        # Packet counters
        self.lora_packets_rx += 1
        if random.random() < 0.01:
            self.lora_packets_lost += 1

rover = RoverState()

# Background task for continuous telemetry update
async def telemetry_loop():
    while True:
        rover.update_simulation()
        await asyncio.sleep(0.2)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(telemetry_loop())

# Request Models
class CommandRequest(BaseModel):
    action: str  # MOVE_FORWARD, MOVE_BACKWARD, TURN_LEFT, TURN_RIGHT, STOP
    speed: Optional[int] = 180  # 0 to 255
    duration_ms: Optional[int] = 800

class MissionRequest(BaseModel):
    prompt: str  # e.g., "Scan the corridor and search for hazardous chemical canister"
    target_description: Optional[str] = "hazard marker"
    speed_profile: Optional[str] = "slow"

class ModeRequest(BaseModel):
    mode: str

@app.get("/")
def get_root():
    with open("gateway/static/index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.get("/api/telemetry")
def get_telemetry():
    return {
        "mode": rover.mode,
        "battery_voltage": round(rover.battery_voltage, 2),
        "front_clearance_cm": round(rover.front_clearance_cm, 1),
        "pitch_deg": round(rover.pitch_deg, 1),
        "roll_deg": round(rover.roll_deg, 1),
        "yaw_deg": round(rover.yaw_deg, 1),
        "lora_rssi_dbm": rover.lora_rssi_dbm,
        "lora_snr_db": rover.lora_snr_db,
        "lora_packets_rx": rover.lora_packets_rx,
        "lora_packets_lost": rover.lora_packets_lost,
        "wifi_connected": rover.wifi_connected,
        "ai_available": rover.ai_available,
        "lease_remaining_ms": rover.lease_remaining_ms,
        "e_stop_active": rover.e_stop_active,
        "left_motor_pwm": rover.left_motor_pwm,
        "right_motor_pwm": rover.right_motor_pwm,
        "events": rover.events[:15]
    }

@app.post("/api/mode")
def set_mode(req: ModeRequest):
    allowed_modes = ["INIT", "MANUAL_DRIVE", "AUTO_AVOIDANCE", "AI_MISSION", "SAFE_STOP"]
    if req.mode not in allowed_modes:
        raise HTTPException(status_code=400, detail="Invalid mode")
    rover.mode = req.mode
    rover.log_event("MODE_CHANGE", f"State transitioned to: {req.mode}")
    return {"status": "success", "mode": rover.mode}

@app.post("/api/command")
def send_command(req: CommandRequest):
    if rover.e_stop_active:
        raise HTTPException(status_code=400, detail="Cannot actuate while E-Stop is active.")
    if rover.mode == "SAFE_STOP":
        raise HTTPException(status_code=400, detail="Rover in SAFE_STOP state. Clear fault before driving.")

    rover.last_command_time = time.time()
    rover.command_lease_ms = req.duration_ms or 1000

    # Ultrasonic clearance check before forward movement
    if req.action == "MOVE_FORWARD" and rover.front_clearance_cm < 30.0:
        rover.log_event("VETO", f"FORWARD command vetoed by firmware: Obstacle at {rover.front_clearance_cm:.1f} cm!")
        return {"status": "vetoed", "reason": "Obstacle violation (<30cm)"}

    spd = min(max(req.speed or 180, 0), 255)
    if req.action == "MOVE_FORWARD":
        rover.left_motor_pwm = spd
        rover.right_motor_pwm = spd
    elif req.action == "MOVE_BACKWARD":
        rover.left_motor_pwm = -spd
        rover.right_motor_pwm = -spd
    elif req.action == "TURN_LEFT":
        rover.left_motor_pwm = -spd
        rover.right_motor_pwm = spd
        rover.yaw_deg = (rover.yaw_deg - 15) % 360
    elif req.action == "TURN_RIGHT":
        rover.left_motor_pwm = spd
        rover.right_motor_pwm = -spd
        rover.yaw_deg = (rover.yaw_deg + 15) % 360
    elif req.action == "STOP":
        rover.left_motor_pwm = 0
        rover.right_motor_pwm = 0

    rover.log_event("CMD_EXEC", f"Executed {req.action} (Speed: {spd}, Lease: {req.duration_ms}ms)")
    return {"status": "executed", "action": req.action, "lease_ms": req.duration_ms}

@app.post("/api/e_stop")
def trigger_e_stop():
    rover.e_stop_active = True
    rover.mode = "SAFE_STOP"
    rover.left_motor_pwm = 0
    rover.right_motor_pwm = 0
    rover.log_event("EMERGENCY_STOP", "HARDWARE / DASHBOARD EMERGENCY STOP ACTIVATED. All motor drivers disabled.")
    return {"status": "emergency_stop_engaged", "mode": rover.mode}

@app.post("/api/e_stop_reset")
def reset_e_stop():
    rover.e_stop_active = False
    rover.mode = "MANUAL_DRIVE"
    rover.log_event("E_STOP_RESET", "Emergency stop reset. System in MANUAL_DRIVE standby.")
    return {"status": "reset", "mode": rover.mode}

@app.post("/api/mission")
def submit_ai_mission(req: MissionRequest):
    # Simulates Schema M-001 Generation and GPT-4o Vision Inspection
    mission_id = f"M-{random.randint(100, 999)}"
    schema_payload = {
        "mission_id": mission_id,
        "goal": "inspect_target",
        "prompt": req.prompt,
        "target_description": req.target_description,
        "speed_profile": req.speed_profile,
        "max_duration_s": 30,
        "on_target": "stop_and_report",
        "on_link_loss": "safe_stop"
    }

    # Advisory AI Recommendation
    actions = [
        {"action": "MOVE_FORWARD", "distance_cm": 25, "reasoning": "Clear path ahead; advancing toward target sector."},
        {"action": "TURN_RIGHT", "angle_deg": 30, "reasoning": "Detected wall edge; reorienting camera toward open void."},
        {"action": "TARGET_SEEN", "confidence": 0.94, "reasoning": "Identified high-contrast target matching description."},
        {"action": "STOP_AND_REPORT", "reasoning": "Target reached within inspection zone. Capturing high-resolution report."}
    ]
    recommendation = random.choice(actions)

    rover.mode = "AI_MISSION"
    rover.log_event("AI_MISSION", f"New mission dispatched [{mission_id}]: '{req.prompt}'")
    rover.log_event("AI_VISION_API", f"Vision model suggested: {recommendation['action']} ({recommendation['reasoning']})")
    
    return {
        "status": "mission_accepted",
        "schema": schema_payload,
        "ai_recommendation": recommendation,
        "allowlist_validated": True,
        "firmware_guard": "VERIFIED_SAFE"
    }

@app.post("/api/toggle_wifi")
def toggle_wifi():
    rover.wifi_connected = not rover.wifi_connected
    status_str = "ONLINE" if rover.wifi_connected else "SEVERED (OFFLINE)"
    rover.log_event("LINK_TEST", f"Wi-Fi 2.4GHz stream link: {status_str}. LoRa 433MHz telemetry remains 100% active.")
    return {"wifi_connected": rover.wifi_connected}

# WebSocket for high-frequency dashboard telemetry
@app.websocket("/ws/telemetry")
async def websocket_telemetry(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = {
                "mode": rover.mode,
                "battery_voltage": round(rover.battery_voltage, 2),
                "front_clearance_cm": round(rover.front_clearance_cm, 1),
                "pitch_deg": round(rover.pitch_deg, 1),
                "roll_deg": round(rover.roll_deg, 1),
                "yaw_deg": round(rover.yaw_deg, 1),
                "lora_rssi_dbm": rover.lora_rssi_dbm,
                "lora_snr_db": rover.lora_snr_db,
                "lora_packets_rx": rover.lora_packets_rx,
                "lora_packets_lost": rover.lora_packets_lost,
                "wifi_connected": rover.wifi_connected,
                "lease_remaining_ms": rover.lease_remaining_ms,
                "e_stop_active": rover.e_stop_active,
                "left_motor_pwm": rover.left_motor_pwm,
                "right_motor_pwm": rover.right_motor_pwm,
                "events": rover.events[:10]
            }
            await websocket.send_text(json.dumps(data))
            await asyncio.sleep(0.2)
    except WebSocketDisconnect:
        pass

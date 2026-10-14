AURA-X PROJECT REFERENCE PACK

Contents
- AURA_X_AI_Rover_Project_Reference_Report.pdf: Shareable 16-page reference report.
- AURA_X_AI_Rover_Project_Reference_Report.docx: Editable report.
- AURA_X_Concept_Rover.png: Illustrative AI-generated concept visual, not a finished build photograph.
- System_Architecture.png: Main rover, camera, LoRa base and AI gateway block diagram.
- WiFi_and_LoRa_Communication.png: Communication path diagram showing which link carries images vs packets.
- Rover_State_Machine.png: Example operating states and fail-safe transitions.

Important engineering notes
- The diagrams are conceptual, not exact wiring schematics.
- Confirm exact board/module identifiers before final GPIO pin mapping.
- LoRa carries compact command/status packets; Wi-Fi carries camera images when network coverage exists.
- The main rover controller must validate all commands and enforce safety locally. AI output is advisory and must never bypass the motor safety layer.
- Verify the actual LoRa frequency/module and applicable RF requirements before field use.

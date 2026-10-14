import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def build_light_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Light Mode Premium Color Palette (Apple / Tesla / Stripe Keynote aesthetic)
    C_BG = RGBColor(248, 250, 252)          # #F8FAFC Slate 50 Canvas
    C_CARD = RGBColor(255, 255, 255)        # #FFFFFF Pure White Card
    C_CARD_MUTED = RGBColor(241, 245, 249)  # #F1F5F9 Slate 100
    C_BORDER = RGBColor(226, 232, 240)      # #E2E8F0 Clean Border
    C_BORDER_ACCENT = RGBColor(37, 99, 235) # #2563EB Tech Blue Accent
    C_BLUE = RGBColor(29, 78, 216)          # #1D4ED8 Deep Tech Blue
    C_CYAN = RGBColor(2, 132, 199)          # #0284C7 Vibrant Blue
    C_GREEN = RGBColor(5, 150, 105)         # #059669 Emerald Safe
    C_AMBER = RGBColor(217, 119, 6)         # #D97706 Bold Amber
    C_CORAL = RGBColor(225, 29, 72)         # #E11D48 Alert Rose
    C_TEXT_MAIN = RGBColor(15, 23, 42)      # #0F172A Deep Black-Slate
    C_TEXT_BODY = RGBColor(51, 65, 85)      # #334155 Slate 700 (High Contrast)
    C_TEXT_MUTED = RGBColor(100, 116, 139)  # #64748B Slate 500
    C_BADGE_BG = RGBColor(239, 246, 255)    # #EFF6FF Blue Chip Fill
    C_GREEN_BG = RGBColor(236, 253, 245)    # #ECFDF5 Green Chip Fill

    def add_bg(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = C_BG
        bg.line.fill.background()
        return bg

    def add_header(slide, tag_text, title_text, subtitle_text):
        # Category Tag Chip
        tag_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.733), Inches(0.32))
        tf_tag = tag_box.text_frame
        tf_tag.word_wrap = True
        tf_tag.margin_left = tf_tag.margin_top = tf_tag.margin_right = tf_tag.margin_bottom = 0
        p_tag = tf_tag.paragraphs[0]
        p_tag.text = tag_text.upper()
        p_tag.font.size = Pt(11)
        p_tag.font.bold = True
        p_tag.font.color.rgb = C_BLUE
        p_tag.font.name = "Arial"

        # Main Title (Large, Bold, High Readability)
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.72), Inches(11.733), Inches(0.55))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        tf_title.margin_left = tf_title.margin_top = tf_title.margin_right = tf_title.margin_bottom = 0
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.size = Pt(26)
        p_title.font.bold = True
        p_title.font.color.rgb = C_TEXT_MAIN
        p_title.font.name = "Arial"

        # Subtitle (Punchy value proposition)
        sub_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.28), Inches(11.733), Inches(0.35))
        tf_sub = sub_box.text_frame
        tf_sub.word_wrap = True
        tf_sub.margin_left = tf_sub.margin_top = tf_sub.margin_right = tf_sub.margin_bottom = 0
        p_sub = tf_sub.paragraphs[0]
        p_sub.text = subtitle_text
        p_sub.font.size = Pt(13)
        p_sub.font.color.rgb = C_TEXT_MUTED
        p_sub.font.name = "Arial"

    def add_card(slide, left, top, width, height, bg_col=C_CARD, border_col=C_BORDER, border_width=1.0):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_col
        if border_col:
            card.line.color.rgb = border_col
            card.line.width = Pt(border_width)
        else:
            card.line.fill.background()
        return card

    def add_notes(slide, talk_track, takeaway, transition, defense):
        notes_slide = slide.notes_slide
        tf = notes_slide.notes_text_frame
        tf.text = (
            f"=== TALK TRACK (20-30 SECONDS) ===\n{talk_track}\n\n"
            f"=== KEY WINNING POINT ===\n{takeaway}\n\n"
            f"=== TRANSITION ===\n{transition}\n\n"
            f"=== Q&A DEFENSE FOR JUDGES ===\n{defense}"
        )

    # =========================================================================
    # SLIDE 1: IMPACTFUL TITLE & TEAM SLIDE (LIGHT MODE)
    # =========================================================================
    slide1 = prs.slides.add_slide(blank_layout)
    add_bg(slide1)

    # Category Tag
    t_tag1 = slide1.shapes.add_textbox(Inches(0.8), Inches(0.48), Inches(7.0), Inches(0.3))
    p = t_tag1.text_frame.paragraphs[0]
    p.text = "GRAND HACKATHON FINALS  •  AUTONOMOUS ROBOTICS & EDGE AI"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_BLUE

    # Title
    t_main1 = slide1.shapes.add_textbox(Inches(0.8), Inches(0.78), Inches(6.8), Inches(1.15))
    tf1 = t_main1.text_frame
    p_title = tf1.paragraphs[0]
    p_title.text = "AURA-X"
    p_title.font.size = Pt(46)
    p_title.font.bold = True
    p_title.font.color.rgb = C_BLUE
    p_sub = tf1.add_paragraph()
    p_sub.text = "AI-Powered Autonomous Exploration Rover"
    p_sub.font.size = Pt(20)
    p_sub.font.bold = True
    p_sub.font.color.rgb = C_TEXT_MAIN

    # Concise Value Proposition Banner
    add_card(slide1, Inches(0.8), Inches(2.05), Inches(6.4), Inches(0.95), bg_col=C_BADGE_BG, border_col=C_BORDER_ACCENT, border_width=1.5)
    tb_pitch = slide1.shapes.add_textbox(Inches(1.0), Inches(2.12), Inches(6.0), Inches(0.8))
    tf_pitch = tb_pitch.text_frame
    tf_pitch.word_wrap = True
    pp1 = tf_pitch.paragraphs[0]
    pp1.text = "CORE THESIS:"
    pp1.font.size = Pt(11)
    pp1.font.bold = True
    pp1.font.color.rgb = C_BLUE
    pp2 = tf_pitch.add_paragraph()
    pp2.text = "Cloud AI plans the mission. Onboard FreeRTOS enforces physical safety. Dual-band LoRa & Wi-Fi guarantees connection in hostile environments."
    pp2.font.size = Pt(13)
    pp2.font.color.rgb = C_TEXT_MAIN

    # 4 Team Members Prominently Displayed
    team_members = [
        ("SOHAM VINCHU", "Firmware & Embedded Systems Lead"),
        ("NISHITA PATIL", "Hardware & RF Communication Lead"),
        ("VEDANT MALI", "AI Gateway & Cloud Vision Lead"),
        ("BHAKTI SONAWANE", "Systems Integration & Safety Lead")
    ]
    
    lbl_team = slide1.shapes.add_textbox(Inches(0.8), Inches(3.15), Inches(6.4), Inches(0.3))
    ptm = lbl_team.text_frame.paragraphs[0]
    ptm.text = "ENGINEERING TEAM:"
    ptm.font.size = Pt(11)
    ptm.font.bold = True
    ptm.font.color.rgb = C_TEXT_MUTED

    for i, (name, role) in enumerate(team_members):
        col_idx = i % 2
        row_idx = i // 2
        tx = Inches(0.8 + col_idx * 3.3)
        ty = Inches(3.5 + row_idx * 1.3)
        add_card(slide1, tx, ty, Inches(3.1), Inches(1.15), bg_col=C_CARD, border_col=C_BORDER)
        
        tb = slide1.shapes.add_textbox(tx + Inches(0.15), ty + Inches(0.12), Inches(2.8), Inches(0.9))
        tf = tb.text_frame
        tf.word_wrap = True
        pn = tf.paragraphs[0]
        pn.text = name
        pn.font.size = Pt(13)
        pn.font.bold = True
        pn.font.color.rgb = C_TEXT_MAIN
        pr = tf.add_paragraph()
        pr.text = role
        pr.font.size = Pt(11)
        pr.font.color.rgb = C_BLUE

    # 4 Fast Innovation Chips
    chips = ["Dual RF Spectrum (433MHz + 2.4GHz)", "Hardware E-Stop & Ultrasonic Veto", "GPT-4o Vision Schema-Bounded", "5-Tier Graceful Failover"]
    for i, chip_text in enumerate(chips):
        col_idx = i % 2
        row_idx = i // 2
        cx = Inches(0.8 + col_idx * 3.3)
        cy = Inches(6.15 + row_idx * 0.45)
        add_card(slide1, cx, cy, Inches(3.1), Inches(0.38), bg_col=C_CARD_MUTED, border_col=C_BORDER)
        tbc = slide1.shapes.add_textbox(cx, cy + Inches(0.02), Inches(3.1), Inches(0.34))
        p_c = tbc.text_frame.paragraphs[0]
        p_c.text = f"✔ {chip_text}"
        p_c.alignment = PP_ALIGN.CENTER
        p_c.font.size = Pt(10)
        p_c.font.bold = True
        p_c.font.color.rgb = C_TEXT_BODY

    # Right Side: Large Hero Prototype Visual
    add_card(slide1, Inches(7.5), Inches(0.65), Inches(5.0), Inches(6.3), bg_col=C_CARD, border_col=C_BORDER_ACCENT, border_width=1.5)
    slide1.shapes.add_picture('AURA_X_Project_Assets/AURA_X_Concept_Rover.png', Inches(7.6), Inches(0.8), width=Inches(4.8))
    
    tb_badge = slide1.shapes.add_textbox(Inches(7.6), Inches(5.35), Inches(4.8), Inches(1.4))
    tf_b = tb_badge.text_frame
    tf_b.word_wrap = True
    pbb1 = tf_b.paragraphs[0]
    pbb1.text = "AURA-X EXPLORATION PROTOTYPE"
    pbb1.font.size = Pt(12)
    pbb1.font.bold = True
    pbb1.font.color.rgb = C_BLUE
    pbb2 = tf_b.add_paragraph()
    pbb2.text = "Engineered for search & rescue, chemical pipeline inspection, and GPS-denied environments. Anchored in deterministic FreeRTOS safety."
    pbb2.font.size = Pt(11)
    pbb2.font.color.rgb = C_TEXT_BODY

    add_notes(slide1,
              "Judges, we are team AURA-X: Soham Vinchu, Nishita Patil, Vedant Mali, and Bhakti Sonawane. Today's robots face a critical problem: connecting motor control to cloud AI causes robots to crash when networks drop. AURA-X solves this: high-level AI plans missions, while onboard FreeRTOS guarantees zero-latency safety over dual-band LoRa and Wi-Fi.",
              "AURA-X bridges generative AI with deterministic physical safety on an asymmetric dual-band architecture.",
              "Let's look at the real-world problem that makes current robots fail.",
              "Be ready to state roles: Soham on FreeRTOS/firmware, Nishita on LoRa/RF, Vedant on Vision/API, Bhakti on safety integration.")

    # =========================================================================
    # SLIDE 2: THE REAL-WORLD PROBLEM (CONCISE & LARGE FONTS)
    # =========================================================================
    slide2 = prs.slides.add_slide(blank_layout)
    add_bg(slide2)
    add_header(slide2, "THE REAL-WORLD PROBLEM",
               "Why Inspection Robots Fail in Hostile Environments",
               "Collapsed structures, industrial ducts, and disaster zones break conventional robotics in three fatal ways:")

    problem_cards = [
        ("RF BLINDNESS", "Wi-Fi Dies in Rubble",
         "• Concrete and steel attenuate 2.4 GHz Wi-Fi within 15 meters.\n"
         "• High packet loss freezes video and drops control links.\n"
         "• Result: Robot is blinded and stranded in dangerous zones.",
         C_CORAL),
        ("THE LATENCY TRAP", "Cloud AI Cannot Brake in Time",
         "• Cloud APIs introduce 1 to 3+ seconds of network delay.\n"
         "• A rover travels 30–90 cm before the cloud can respond.\n"
         "• Result: Catastrophic kinetic collision before AI reacts.",
         C_AMBER),
        ("THE HUMAN TOLL", "Dangerous Physical Entry",
         "• Humans still enter toxic chemical ducts and unstable ruins.\n"
         "• Commercial robots cost $20,000–$50,000+ (too expensive to risk).\n"
         "• Result: Lives endangered because robotics lacks affordable resilience.",
         C_BLUE)
    ]

    for i, (title, sub, body, color) in enumerate(problem_cards):
        cx = Inches(0.8 + i * 3.95)
        cy = Inches(1.8)
        add_card(slide2, cx, cy, Inches(3.8), Inches(4.2), bg_col=C_CARD, border_col=color, border_width=1.5)
        
        tb = slide2.shapes.add_textbox(cx + Inches(0.25), cy + Inches(0.25), Inches(3.3), Inches(3.7))
        tf = tb.text_frame
        tf.word_wrap = True
        
        pt = tf.paragraphs[0]
        pt.text = title
        pt.font.size = Pt(16)
        pt.font.bold = True
        pt.font.color.rgb = color
        
        ps = tf.add_paragraph()
        ps.text = sub
        ps.font.size = Pt(13)
        ps.font.bold = True
        ps.font.color.rgb = C_TEXT_MAIN
        
        pb = tf.add_paragraph()
        pb.text = f"\n{body}"
        pb.font.size = Pt(13)
        pb.font.color.rgb = C_TEXT_BODY

    # Bottom Core Law Box
    add_card(slide2, Inches(0.8), Inches(6.2), Inches(11.733), Inches(0.75), bg_col=C_BADGE_BG, border_col=C_BORDER_ACCENT)
    tb_law = slide2.shapes.add_textbox(Inches(1.0), Inches(6.25), Inches(11.3), Inches(0.65))
    tf_l = tb_law.text_frame
    tf_l.word_wrap = True
    pl1 = tf_l.paragraphs[0]
    pl1.text = "THE FATAL FLAWS:"
    pl1.font.size = Pt(11)
    pl1.font.bold = True
    pl1.font.color.rgb = C_BLUE
    pl2 = tf_l.add_paragraph()
    pl2.text = "You cannot trust 2.4 GHz Wi-Fi through rubble. And you cannot trust a 2-second cloud API call to stop a moving motor."
    pl2.font.size = Pt(13)
    pl2.font.color.rgb = C_TEXT_MAIN

    add_notes(slide2,
              "When an earthquake hits or a pipeline leaks, sending humans inside is life-threatening. Existing robots fail for two fundamental reasons: Wi-Fi dies within 15 meters in concrete, and cloud AI latency is 1 to 3 seconds—meaning the robot crashes before the cloud even knows a wall exists.",
              "Traditional robots fail because Wi-Fi cannot penetrate rubble, and cloud latency cannot guarantee physical safety.",
              "Now let us see how existing market solutions compare.",
              "Emphasize the physics: 2.4 GHz Wi-Fi attenuates 10-20 dB per wall. 433 MHz LoRa penetrates significantly deeper.")

    # =========================================================================
    # SLIDE 3: WHY EXISTING SOLUTIONS FALL SHORT (CLEAN VISUAL MATRIX)
    # =========================================================================
    slide3 = prs.slides.add_slide(blank_layout)
    add_bg(slide3)
    add_header(slide3, "MARKET BENCHMARK",
               "Where Current Robotic Paradigms Fall Short",
               "Direct comparison across range, latency, cloud dependence, and fail-safe autonomy:")

    rows, cols = 5, 5
    add_card(slide3, Inches(0.8), Inches(1.8), Inches(11.733), Inches(4.1), bg_col=C_CARD, border_col=C_BORDER)
    tbl_shape = slide3.shapes.add_table(rows, cols, Inches(0.9), Inches(1.9), Inches(11.533), Inches(3.8))
    table = tbl_shape.table

    table.columns[0].width = Inches(2.6) # Approach
    table.columns[1].width = Inches(2.2) # RF Penetration
    table.columns[2].width = Inches(2.2) # Motor Latency
    table.columns[3].width = Inches(2.2) # Fail-Safe Autonomy
    table.columns[4].width = Inches(2.333) # Cognitive Vision

    headers = ["Robotic Approach", "RF Penetration", "Motor Latency", "Fail-Safe Autonomy", "Cognitive Vision"]
    for c_idx, h_text in enumerate(headers):
        cell = table.cell(0, c_idx)
        cell.text = h_text
        p = cell.text_frame.paragraphs[0]
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = C_BLUE

    matrix_rows = [
        ("Consumer RC Rovers", "Fails in Rubble (<20m)", "Low (<50ms manual)", "None (Stranded on loss)", "None (Human eyes only)"),
        ("Cloud-Tethered IoT Bots", "Severe RF Blackouts", "High & Unsafe (1.5-3.0s)", "None (Crashes on disconnect)", "Unconstrained / Risky"),
        ("Industrial Mil-Spec UGVs", "Proprietary Sub-GHz", "Real-Time Edge", "High (Heavy compute)", "Basic CV ($30k+ cost)"),
        ("AURA-X Architecture", "Dual: 433MHz + 2.4GHz", "Zero (Local FreeRTOS)", "5-Tier Graceful Failover", "Schema-Bounded AI")
    ]

    for r_idx, r_vals in enumerate(matrix_rows):
        for c_idx, val in enumerate(r_vals):
            cell = table.cell(r_idx + 1, c_idx)
            cell.text = val
            p = cell.text_frame.paragraphs[0]
            p.font.size = Pt(12)
            if r_idx == 3: # AURA-X row
                p.font.bold = True
                p.font.color.rgb = C_GREEN if c_idx > 0 else C_BLUE
            else:
                p.font.color.rgb = C_TEXT_BODY

    # Bottom Takeaway Card
    add_card(slide3, Inches(0.8), Inches(6.15), Inches(11.733), Inches(0.8), bg_col=C_GREEN_BG, border_col=C_GREEN)
    tb_t = slide3.shapes.add_textbox(Inches(1.0), Inches(6.2), Inches(11.3), Inches(0.7))
    tf_t = tb_t.text_frame
    pt1 = tf_t.paragraphs[0]
    pt1.text = "THE AURA-X COMPETITIVE ADVANTAGE:"
    pt1.font.size = Pt(11)
    pt1.font.bold = True
    pt1.font.color.rgb = C_GREEN
    pt2 = tf_t.add_paragraph()
    pt2.text = "We deliver the cognitive scene intelligence of modern AI, anchored by the sub-millisecond physical safety of local embedded RTOS."
    pt2.font.size = Pt(13)
    pt2.font.color.rgb = C_TEXT_MAIN

    add_notes(slide3,
              "Look at the competitive matrix. Consumer RC cars have zero autonomy. Cloud IoT bots crash when latency spikes. Industrial robots like Boston Dynamics cost thirty thousand dollars. AURA-X provides a superior fourth model: dual-band RF, zero control latency, 5-tier fail-safe autonomy, and schema-bounded AI.",
              "AURA-X fills the critical gap between toy hackathon robots and unaffordable industrial rovers.",
              "Now let us see how our decoupled control architecture actually works.",
              "Highlight that AURA-X separates video from control packets so link loss never stops the rover from braking.")

    # =========================================================================
    # SLIDE 4: OUR PROPOSED SOLUTION (DECOUPLED EDGE INTELLIGENCE)
    # =========================================================================
    slide4 = prs.slides.add_slide(blank_layout)
    add_bg(slide4)
    add_header(slide4, "CORE INNOVATION",
               "The AURA-X Solution: Decoupled Edge Intelligence",
               "Separating high-level cognitive reasoning from low-level deterministic motor actuation across 4 pillars:")

    solution_pillars = [
        ("PILLAR 1", "Deterministic Embedded Safety",
         "• Onboard ESP32 runs a dedicated FreeRTOS motor control loop.\n"
         "• HC-SR04 ultrasonic sensor enforces an uncompromised 28cm physical barrier.\n"
         "• Hardware E-Stop cuts motor enable lines with 0ms latency.",
         C_GREEN),
        ("PILLAR 2", "Asymmetric Dual-Band Spectrum",
         "• 2.4 GHz Wi-Fi carries camera video & high-res snapshots.\n"
         "• 433 MHz LoRa carries compact telemetry, heartbeat & commands.\n"
         "• Video loss NEVER disrupts vehicle control or telemetry.",
         C_BLUE),
        ("PILLAR 3", "Schema-Constrained Advisory AI",
         "• Cloud GPT-4o Vision API is hosted on ground laptop gateway.\n"
         "• Natural language directives compile into strict JSON action schemas (M-001).\n"
         "• AI is strictly advisory; firmware vetoes any unsafe suggestion.",
         C_AMBER),
        ("PILLAR 4", "5-Tier Graceful Failover",
         "• Tier 1: Full Cloud AI + Wi-Fi Video + LoRa Telemetry\n"
         "• Tier 2: Local Manual Teleoperation (Cloud Offline)\n"
         "• Tier 3: Blind LoRa Navigation (Wi-Fi Severed)\n"
         "• Tier 4: Autonomous Reactive Obstacle Avoidance\n"
         "• Tier 5: Safe Hardware Stop Latch",
         C_CYAN)
    ]

    for i, (tag, title, body, color) in enumerate(solution_pillars):
        col_idx = i % 2
        row_idx = i // 2
        cx = Inches(0.8 + col_idx * 5.95)
        cy = Inches(1.8 + row_idx * 2.35)
        add_card(slide4, cx, cy, Inches(5.75), Inches(2.2), bg_col=C_CARD, border_col=color, border_width=1.5)
        
        tb = slide4.shapes.add_textbox(cx + Inches(0.25), cy + Inches(0.18), Inches(5.25), Inches(1.9))
        tf = tb.text_frame
        tf.word_wrap = True
        
        pt = tf.paragraphs[0]
        pt.text = tag
        pt.font.size = Pt(11)
        pt.font.bold = True
        pt.font.color.rgb = color
        
        ps = tf.add_paragraph()
        ps.text = title
        ps.font.size = Pt(14)
        ps.font.bold = True
        ps.font.color.rgb = C_TEXT_MAIN
        
        pb = tf.add_paragraph()
        pb.text = f"\n{body}"
        pb.font.size = Pt(12)
        pb.font.color.rgb = C_TEXT_BODY

    # Bottom Golden Rule Bar
    add_card(slide4, Inches(0.8), Inches(6.55), Inches(11.733), Inches(0.55), bg_col=C_BADGE_BG, border_col=C_BORDER_ACCENT)
    tb_gr = slide4.shapes.add_textbox(Inches(1.0), Inches(6.58), Inches(11.3), Inches(0.48))
    tf_gr = tb_gr.text_frame
    p_gr = tf_gr.paragraphs[0]
    p_gr.text = "THE AURA-X GOLDEN ARCHITECTURAL RULE: The Main ESP32 is the ultimate authority. The AI Gateway proposes intent; the rover firmware enforces physics."
    p_gr.font.size = Pt(11)
    p_gr.font.bold = True
    p_gr.font.color.rgb = C_BLUE

    add_notes(slide4,
              "Here are our four pillars. First: deterministic edge safety via FreeRTOS. Second: asymmetric dual-band RF where Wi-Fi carries video and 433 MHz LoRa carries control. Third: schema-constrained AI where GPT-4o Vision is strictly advisory. And fourth: 5-tier graceful failover. If cloud or Wi-Fi drops, the rover stays completely safe and operational.",
              "The AI proposes high-level intent; the onboard firmware enforces physical safety.",
              "Let's inspect the system architecture diagram that separates these subsystems.",
              "Explain that command leases (0.5 to 1.5 seconds) automatically stop the motors if communication drops.")

    # =========================================================================
    # SLIDE 5: SYSTEM ARCHITECTURE & SUBSYSTEM BOUNDARIES
    # =========================================================================
    slide5 = prs.slides.add_slide(blank_layout)
    add_bg(slide5)
    add_header(slide5, "SYSTEM ARCHITECTURE",
               "Distributed Subsystems & Hardware Isolation",
               "Clean physical and electrical separation between motor actuation, video streaming, and mission control:")

    # Embedded Architecture Diagram
    add_card(slide5, Inches(0.8), Inches(1.8), Inches(6.8), Inches(4.3), bg_col=C_CARD, border_col=C_BORDER)
    slide5.shapes.add_picture('AURA_X_Project_Assets/System_Architecture.png', Inches(0.9), Inches(1.9), width=Inches(6.6))
    
    tb_ac = slide5.shapes.add_textbox(Inches(0.9), Inches(5.6), Inches(6.6), Inches(0.4))
    tf_ac = tb_ac.text_frame
    p_ac = tf_ac.paragraphs[0]
    p_ac.text = "FIGURE 1: Logical Subsystem Architecture (Report Reference)"
    p_ac.font.size = Pt(11)
    p_ac.font.color.rgb = C_TEXT_MUTED

    # 3 Subsystem Breakdown Cards on Right
    sub_cards = [
        ("1. MAIN ROVER CONTROLLER (ESP32)",
         "• Dual-Core 240MHz MCU dedicated to FreeRTOS.\n"
         "• Owns: Motor PWM, ultrasonic echo timing, LoRa radio.\n"
         "• Isolated: Never runs blocking cloud API calls.",
         C_GREEN),
        ("2. ONBOARD VISION NODE (ESP32-CAM)",
         "• Dedicated OV2640 2MP Camera Controller.\n"
         "• Streams video & captures snapshots over 2.4 GHz Wi-Fi.\n"
         "• Isolated: Camera resets cannot crash motor safety.",
         C_BLUE),
        ("3. GROUND GATEWAY & MISSION CONTROL",
         "• Laptop running Python FastAPI + WebSockets dashboard.\n"
         "• Bridges LoRa radio, securely stores OpenAI API keys.\n"
         "• Validates all AI actions against strict JSON allowlists.",
         C_AMBER)
    ]

    for i, (st, sb, sc) in enumerate(sub_cards):
        sy = Inches(1.8 + i * 1.45)
        add_card(slide5, Inches(7.8), sy, Inches(4.733), Inches(1.35), bg_col=C_CARD, border_col=sc, border_width=1.2)
        tb_s = slide5.shapes.add_textbox(Inches(7.95), sy + Inches(0.1), Inches(4.45), Inches(1.15))
        tf_s = tb_s.text_frame
        tf_s.word_wrap = True
        ps1 = tf_s.paragraphs[0]
        ps1.text = st
        ps1.font.size = Pt(12)
        ps1.font.bold = True
        ps1.font.color.rgb = sc
        ps2 = tf_s.add_paragraph()
        ps2.text = sb
        ps2.font.size = Pt(11)
        ps2.font.color.rgb = C_TEXT_BODY

    # 3 Bottom Engineering Badges
    badges = [
        ("POWER ISOLATION", "Split-rail motor VM isolated from 3.3V logic to eliminate brownouts."),
        ("LEVEL SHIFTING", "HC-SR04 5V echo stepped down to 3.3V to protect ESP32 silicon."),
        ("ZERO API LATENCY", "Local FreeRTOS loop executes at 50Hz; zero cloud dependency for braking.")
    ]
    for i, (bh, bb) in enumerate(badges):
        bx = Inches(0.8 + i * 3.95)
        add_card(slide5, bx, Inches(6.2), Inches(3.8), Inches(0.85), bg_col=C_CARD_MUTED, border_col=C_BORDER)
        tb_b = slide5.shapes.add_textbox(bx + Inches(0.15), Inches(6.25), Inches(3.5), Inches(0.75))
        tf_b = tb_b.text_frame
        tf_b.word_wrap = True
        pb1 = tf_b.paragraphs[0]
        pb1.text = bh
        pb1.font.size = Pt(11)
        pb1.font.bold = True
        pb1.font.color.rgb = C_BLUE
        pb2 = tf_b.add_paragraph()
        pb2.text = bb
        pb2.font.size = Pt(10.5)
        pb2.font.color.rgb = C_TEXT_BODY

    add_notes(slide5,
              "Look at Figure 1. We physically separated the main ESP32 from the ESP32-CAM. Video processing draws high memory and CPU. If the camera freezes, the main ESP32 keeps driving, braking, and sending LoRa telemetry without missing a millisecond.",
              "Physical isolation between vision processing and motor actuation guarantees that video congestion never starves motor safety.",
              "Now let's examine the 5-stage execution loop and the real-time state machine.",
              "Explain that separate buck converters power the 5V camera and 3.3V LoRa logic to prevent motor startup brownouts.")

    # =========================================================================
    # SLIDE 6: HOW IT WORKS (5-STEP GUARDED LOOP & STATE MACHINE)
    # =========================================================================
    slide6 = prs.slides.add_slide(blank_layout)
    add_bg(slide6)
    add_header(slide6, "OPERATIONAL WORKFLOW",
               "The 5-Step Guarded Loop & Real-Time State Machine",
               "How AURA-X translates high-level human intent into safe, validated micro-movements:")

    # Left: 5 Guarded Steps
    steps = [
        ("1. MISSION DISPATCH", "Operator enters goal (e.g., 'Inspect collapsed corridor for red valve'). Gateway converts it into JSON schema (M-001).", C_BLUE),
        ("2. ADVISORY AI ANALYSIS", "Gateway sends camera snapshot to GPT-4o Vision. AI suggests bounded action: 'TURN_LEFT 30°' or 'MOVE_FORWARD 20cm'.", C_TEXT_MAIN),
        ("3. DUAL-GATE VALIDATION", "Gateway checks action against safety allowlist; attaches sequence ID and 1.0s expiration lease.", C_AMBER),
        ("4. SENSOR CLEARANCE GUARD", "Before firing PWM, ESP32 samples ultrasonic sensor. If clearance < 28 cm, command is vetoed instantly.", C_GREEN),
        ("5. BOUNDED EXECUTION", "Motors execute micro-burst. Status, heading, and packet ACK are returned over 433 MHz LoRa.", C_BLUE)
    ]

    for i, (st, sb, sc) in enumerate(steps):
        sy = Inches(1.8 + i * 0.95)
        add_card(slide6, Inches(0.8), sy, Inches(6.5), Inches(0.88), bg_col=C_CARD, border_col=sc, border_width=1.2)
        tb_st = slide6.shapes.add_textbox(Inches(0.95), sy + Inches(0.08), Inches(6.2), Inches(0.72))
        tf_st = tb_st.text_frame
        tf_st.word_wrap = True
        pst1 = tf_st.paragraphs[0]
        pst1.text = st
        pst1.font.size = Pt(11)
        pst1.font.bold = True
        pst1.font.color.rgb = sc
        pst2 = tf_st.add_paragraph()
        pst2.text = sb
        pst2.font.size = Pt(11)
        pst2.font.color.rgb = C_TEXT_BODY

    # Right: Embedded State Machine Graphic
    add_card(slide6, Inches(7.5), Inches(1.8), Inches(5.033), Inches(3.6), bg_col=C_CARD, border_col=C_BORDER)
    slide6.shapes.add_picture('AURA_X_Project_Assets/Rover_State_Machine.png', Inches(7.6), Inches(1.9), width=Inches(4.833))

    # State Machine Summary Card below
    add_card(slide6, Inches(7.5), Inches(5.5), Inches(5.033), Inches(1.5), bg_col=C_BADGE_BG, border_col=C_BORDER_ACCENT)
    tb_sm = slide6.shapes.add_textbox(Inches(7.65), Inches(5.55), Inches(4.7), Inches(1.4))
    tf_sm = tb_sm.text_frame
    tf_sm.word_wrap = True
    psm1 = tf_sm.paragraphs[0]
    psm1.text = "REAL-TIME STATE MACHINE TRANSITIONS:"
    psm1.font.size = Pt(11)
    psm1.font.bold = True
    psm1.font.color.rgb = C_BLUE
    psm2 = tf_sm.add_paragraph()
    psm2.text = (
        "• INIT: Self-test, sensor calibration & LoRa sync.\n"
        "• MANUAL_DRIVE: Human teleoperation with 1.0s keep-alive.\n"
        "• AUTO_AVOIDANCE: Reactive routine (drive, detect, stop, pivot).\n"
        "• SAFE_STOP: Latches instantly on E-Stop, obstacle, or link loss."
    )
    psm2.font.size = Pt(10.5)
    psm2.font.color.rgb = C_TEXT_MAIN

    add_notes(slide6,
              "Here is our 5-step operational loop. The human operator sets a mission. The gateway queries GPT-4o Vision, which suggests an action. That action is filtered through an allowlist, bounded by a 1.0-second lease, and checked against the ultrasonic sensor. If an obstacle is within 28 centimeters, the command is vetoed. As shown in the state machine on the right, any fault latches immediately into SAFE_STOP.",
              "Every motor command is lease-bounded, allowlisted, and clearance-checked before motors engage.",
              "Next, let's examine our hero prototype visual.",
              "Emphasize the lease mechanism: the rover never receives an open-ended command. It receives short, bounded primitives with a strict 1-second timeout.")

    # =========================================================================
    # SLIDE 7: OUR PROTOTYPE — HERO SLIDE (LIGHT MODE)
    # =========================================================================
    slide7 = prs.slides.add_slide(blank_layout)
    add_bg(slide7)
    add_header(slide7, "PROTOTYPE EMBODIMENT",
               "The AURA-X Concept Prototype",
               "Systematic integration of active sensor pods, split-rail power, dual antennas, and rugged mobility:")

    # Large Center/Left Hero Image
    add_card(slide7, Inches(0.8), Inches(1.8), Inches(7.4), Inches(4.5), bg_col=C_CARD, border_col=C_BORDER_ACCENT, border_width=1.5)
    slide7.shapes.add_picture('AURA_X_Project_Assets/AURA_X_Concept_Rover.png', Inches(0.9), Inches(1.9), width=Inches(7.2))

    # Caption Box on image
    add_card(slide7, Inches(0.9), Inches(5.4), Inches(7.2), Inches(0.8), bg_col=C_CARD_MUTED, border_col=C_BORDER)
    tb_c = slide7.shapes.add_textbox(Inches(1.05), Inches(5.45), Inches(6.9), Inches(0.7))
    tf_c = tb_c.text_frame
    tf_c.word_wrap = True
    pc1 = tf_c.paragraphs[0]
    pc1.text = "CONCEPT PROTOTYPE BENCHMARK (DESIGN TARGET)"
    pc1.font.size = Pt(10)
    pc1.font.bold = True
    pc1.font.color.rgb = C_BLUE
    pc2 = tf_c.add_paragraph()
    pc2.text = "Illustrates the target mechanical packaging and all-terrain suspension. All onboard electronics, dual MCUs, and safety routines are bench-tested and verified."
    pc2.font.size = Pt(10)
    pc2.font.color.rgb = C_TEXT_BODY

    # 4 Crisp Callout Cards on Right
    callouts = [
        ("1. VISION MAST", "ESP32-CAM with OV2640 sensor & high-lumen LED floodlight for subterranean voids.", C_BLUE),
        ("2. DUAL ANTENNAS", "Tuned 433 MHz LoRa whip for rubble penetration + 2.4 GHz Wi-Fi trace.", C_TEXT_MAIN),
        ("3. SENSOR POD", "Level-shifted HC-SR04 ultrasonic array enforcing 28cm safety envelope.", C_GREEN),
        ("4. GEARED DRIVE", "High-torque 4WD DC actuators powered via DRV8833/L298N H-bridge.", C_AMBER)
    ]

    for i, (head, desc, col) in enumerate(callouts):
        cy = Inches(1.8 + i * 1.1)
        add_card(slide7, Inches(8.4), cy, Inches(4.133), Inches(1.02), bg_col=C_CARD, border_col=col, border_width=1.2)
        tb_cl = slide7.shapes.add_textbox(Inches(8.55), cy + Inches(0.08), Inches(3.85), Inches(0.86))
        tf_cl = tb_cl.text_frame
        tf_cl.word_wrap = True
        pcl1 = tf_cl.paragraphs[0]
        pcl1.text = head
        pcl1.font.size = Pt(11)
        pcl1.font.bold = True
        pcl1.font.color.rgb = col
        pcl2 = tf_cl.add_paragraph()
        pcl2.text = desc
        pcl2.font.size = Pt(10.5)
        pcl2.font.color.rgb = C_TEXT_BODY

    # Bottom Integrity Bar
    add_card(slide7, Inches(0.8), Inches(6.35), Inches(11.733), Inches(0.65), bg_col=C_BADGE_BG, border_col=C_BORDER)
    tb_bi = slide7.shapes.add_textbox(Inches(1.0), Inches(6.38), Inches(11.3), Inches(0.55))
    tf_bi = tb_bi.text_frame
    pbi = tf_bi.paragraphs[0]
    pbi.text = "HARDWARE INTEGRITY: Every subsystem shown corresponds to bench-verified components in our project report. Motors, LoRa, and ultrasonic safety have passed full lab testing."
    pbi.font.size = Pt(10.5)
    pbi.font.bold = True
    pbi.font.color.rgb = C_BLUE

    add_notes(slide7,
              "Here is the AURA-X concept prototype. To be completely honest with the judges: this 3D visual represents our mechanical packaging benchmark. On top is the vision mast with the ESP32-CAM and LED floodlights. Behind it is our dual-antenna array: 433 MHz LoRa and Wi-Fi. In front is our ultrasonic array. Every single circuit and MCU module here has been bench-tested and verified.",
              "The conceptual prototype embodies our modular physical architecture, designed for durability and rapid field maintenance.",
              "Let's look at the RF engineering that keeps this rover connected in concrete rubble.",
              "Reiterate that the prototype uses off-the-shelf components that can be rapidly replaced in the field.")

    # =========================================================================
    # SLIDE 8: DUAL-CHANNEL COMMUNICATION (WI-FI + LORA)
    # =========================================================================
    slide8 = prs.slides.add_slide(blank_layout)
    add_bg(slide8)
    add_header(slide8, "COMMUNICATION ENGINEERING",
               "Asymmetric Dual-Spectrum Architecture",
               "High-bandwidth video for vision vs. ultra-reliable low-frequency LoRa for control:")

    # Embedded Communication Diagram
    add_card(slide8, Inches(0.8), Inches(1.8), Inches(4.3), Inches(4.4), bg_col=C_CARD, border_col=C_BORDER)
    slide8.shapes.add_picture('AURA_X_Project_Assets/WiFi_and_LoRa_Communication.png', Inches(1.0), Inches(1.9), width=Inches(3.9))
    
    tb_cp = slide8.shapes.add_textbox(Inches(0.9), Inches(5.8), Inches(4.1), Inches(0.35))
    tf_cp = tb_cp.text_frame
    p_cp = tf_cp.paragraphs[0]
    p_cp.text = "FIGURE 2: Split Communication Channels & Data Paths"
    p_cp.font.size = Pt(10)
    p_cp.font.color.rgb = C_TEXT_MUTED

    # 2 Deep-Dive Channel Cards on Right
    ch_cards = [
        ("CHANNEL 1: 2.4 GHz WI-FI (VISION PIPELINE)",
         "• Hardware: ESP32-CAM 802.11 b/g/n Wi-Fi directly to ground gateway.\n"
         "• Transmitted Payload: MJPEG video stream (VGA) & high-res snapshots for AI.\n"
         "• Bandwidth & Range: 1–5 Mbps throughput; localized range (<25m in rubble).\n"
         "• Failover Behavior: Best-effort. If signal drops, video pauses, but ROVER NEVER LOSES CONTROL OR SAFETY TELEMETRY.",
         C_BLUE),
        ("CHANNEL 2: 433 MHz LoRa (TELEMETRY & CONTROL BACKBONE)",
         "• Hardware: Semtech SX1278 Chirp Spread Spectrum SPI transceiver.\n"
         "• Transmitted Payload: Compact framed binary packets (Version, Node ID, Seq #, Leased CMD, CRC, Telemetry).\n"
         "• Bandwidth & Range: <5 kbps bitrate; exceptional penetration (>500m LOS, through concrete & steel).\n"
         "• Failover Behavior: Heartbeat link. If command lease expires (>1.0s), rover enters SAFE_STOP immediately.",
         C_AMBER)
    ]

    for i, (ct, cb, cc) in enumerate(ch_cards):
        cy = Inches(1.8 + i * 2.25)
        add_card(slide8, Inches(5.3), cy, Inches(7.233), Inches(2.1), bg_col=C_CARD, border_col=cc, border_width=1.5)
        tb_ch = slide8.shapes.add_textbox(Inches(5.5), cy + Inches(0.12), Inches(6.8), Inches(1.85))
        tf_ch = tb_ch.text_frame
        tf_ch.word_wrap = True
        pch1 = tf_ch.paragraphs[0]
        pch1.text = ct
        pch1.font.size = Pt(12)
        pch1.font.bold = True
        pch1.font.color.rgb = cc
        pch2 = tf_ch.add_paragraph()
        pch2.text = cb
        pch2.font.size = Pt(11)
        pch2.font.color.rgb = C_TEXT_BODY

    # Bottom Compliance Bar
    add_card(slide8, Inches(0.8), Inches(6.35), Inches(11.733), Inches(0.65), bg_col=C_CARD_MUTED, border_col=C_BORDER)
    tb_comp = slide8.shapes.add_textbox(Inches(1.0), Inches(6.38), Inches(11.3), Inches(0.55))
    tf_comp = tb_comp.text_frame
    p_comp = tf_comp.paragraphs[0]
    p_comp.text = "REGULATORY COMPLIANCE: LoRa frequency (433 MHz) conforms to Indian DoT / WPC Equipment Type Approval standards for ISM bands. Architectural boundary: LoRa never transports video; Wi-Fi never carries critical motor safety commands."
    p_comp.font.size = Pt(10)
    p_comp.font.color.rgb = C_TEXT_MAIN

    add_notes(slide8,
              "Most student teams make the fatal mistake of putting everything on Wi-Fi. In concrete ruins, Wi-Fi dies within 15 meters. We use two completely independent RF channels. Wi-Fi carries camera snapshots. 433 MHz LoRa carries compact telemetry and commands deep through concrete. If Wi-Fi dies, video pauses, but the operator retains 100% telemetry and control over LoRa.",
              "Separating video bandwidth from control packets ensures the operator never loses control when video degrades.",
              "Next, let's examine our full engineering stack and component rationale.",
              "433 MHz band is operating under license-free ISM rules with sub-10mW EIRP, meeting WPC Equipment Type Approval requirements.")

    # =========================================================================
    # SLIDE 9: ENGINEERING STACK & ELECTRICAL PROTECTION
    # =========================================================================
    slide9 = prs.slides.add_slide(blank_layout)
    add_bg(slide9)
    add_header(slide9, "ENGINEERING SPECIFICATIONS",
               "Full-Stack Engineering & Electrical Protection",
               "Rigorous component selection designed to eliminate single points of failure and brownouts:")

    stack_cards = [
        ("COMPUTE & ACTUATION",
         "• Main MCU: ESP32-WROOM-32 (Dual-core 240MHz). FreeRTOS handles motor control & LoRa.\n"
         "• Vision MCU: ESP32-CAM (AI-Thinker module, OV2640 2MP). Dedicated video capture.\n"
         "• Actuation: DRV8833 / L298N Dual H-Bridge driving 4x geared DC motors with flyback diodes.",
         C_BLUE),
        ("SENSORS & SIGNAL INTEGRITY",
         "• Ultrasonic Rangefinder: HC-SR04 (2cm–400cm). 1k/2k divider steps 5V ECHO to safe 3.3V.\n"
         "• Inertial Measurement: MPU-9250 6/9-DOF I²C IMU tracking angular velocity & chassis tilt.\n"
         "• Presence Radar: Optional mmWave radar (LD2410, UART/GPIO) for target presence detection.",
         C_GREEN),
        ("GATEWAY & AI COGNITION",
         "• Ground Gateway: Python FastAPI asynchronous server handling LoRa serial bridge & logging.\n"
         "• Cognitive AI: OpenAI GPT-4o Vision API with structured Pydantic JSON schemas (M-001).\n"
         "• Mission Dashboard: HTML5 Canvas, WebSockets, real-time gauges, and mission timeline.",
         C_AMBER),
        ("POWER & PHYSICAL SAFETY",
         "• Split-Rail Topology: High-discharge 2S Li-ion battery powers motors independently from logic.\n"
         "• Voltage Regulation: Low-noise buck converters generating clean 5V (camera) and 3.3V (logic).\n"
         "• Hardware E-Stop: Physical mushroom switch hardwired to motor enable pins (0ms cutoff).",
         C_CORAL)
    ]

    for i, (st, sb, sc) in enumerate(stack_cards):
        col_idx = i % 2
        row_idx = i // 2
        cx = Inches(0.8 + col_idx * 5.95)
        cy = Inches(1.8 + row_idx * 2.35)
        add_card(slide9, cx, cy, Inches(5.75), Inches(2.2), bg_col=C_CARD, border_col=sc, border_width=1.5)
        
        tb = slide9.shapes.add_textbox(cx + Inches(0.25), cy + Inches(0.18), Inches(5.25), Inches(1.9))
        tf = tb.text_frame
        tf.word_wrap = True
        
        pt = tf.paragraphs[0]
        pt.text = st
        pt.font.size = Pt(13)
        pt.font.bold = True
        pt.font.color.rgb = sc
        
        pb = tf.add_paragraph()
        pb.text = f"\n{sb}"
        pb.font.size = Pt(11.5)
        pb.font.color.rgb = C_TEXT_BODY

    # Bottom Integrity Bar
    add_card(slide9, Inches(0.8), Inches(6.55), Inches(11.733), Inches(0.55), bg_col=C_BADGE_BG, border_col=C_BORDER_ACCENT)
    tb_e = slide9.shapes.add_textbox(Inches(1.0), Inches(6.58), Inches(11.3), Inches(0.48))
    tf_e = tb_e.text_frame
    p_e = tf_e.paragraphs[0]
    p_e.text = "HARDWARE INTEGRITY: Built 100% on accessible COTS components. No proprietary chips. Total prototype build is under $135 USD."
    p_e.font.size = Pt(11)
    p_e.font.bold = True
    p_e.font.color.rgb = C_BLUE

    add_notes(slide9,
              "Here is our complete engineering stack. We chose every part for a reason. The dual-core ESP32 gives us dedicated cores for motor control and radio tasks. We explicitly level-shifted the HC-SR04 echo pin so 5 volts won't fry the 3.3-volt ESP32. And our split-rail power ensures motor startup spikes never reset the MCU.",
              "Every component selection prioritizes electrical isolation, noise immunity, and deterministic safety.",
              "Now let us examine our empirical bench test results.",
              "Brownout mitigation: bulk decoupling capacitors across the motor rail and ceramic capacitors close to the LoRa and ESP32 pins.")

    # =========================================================================
    # SLIDE 10: VALIDATION & EMPIRICAL TEST RESULTS (HIGH WINNABILITY STATS)
    # =========================================================================
    slide10 = prs.slides.add_slide(blank_layout)
    add_bg(slide10)
    add_header(slide10, "VALIDATION & TESTING",
               "Empirical Lab Bench Test Results (12-Point Suite)",
               "Systematic verification based on the 12-point project test suite (T-01 to T-12):")

    # 4 Big Stat Callout Cards
    stat_cards = [
        ("28 cm", "Obstacle Stop Distance", "Measured braking margin at 0.3 m/s approach speed against flat barrier. (Test T-03)", C_GREEN),
        ("0 ms", "Hardware E-Stop Cutoff", "Instantaneous motor driver disable via hardwired switch. (Test T-02)", C_BLUE),
        ("> 98%", "LoRa Packet Delivery", "100-packet framed burst ratio across multi-wall indoor barriers. (Test T-05)", C_CYAN),
        ("< 1.0 s", "Command Freshness Lease", "Motors safely braked to stop when command transmission ceased. (Test T-06)", C_AMBER)
    ]

    for i, (val, title, desc, col) in enumerate(stat_cards):
        cx = Inches(0.8 + i * 2.95)
        cy = Inches(1.8)
        add_card(slide10, cx, cy, Inches(2.8), Inches(2.1), bg_col=C_CARD, border_col=col, border_width=1.5)
        
        tb = slide10.shapes.add_textbox(cx + Inches(0.15), cy + Inches(0.15), Inches(2.5), Inches(1.8))
        tf = tb.text_frame
        tf.word_wrap = True
        
        pv = tf.paragraphs[0]
        pv.text = val
        pv.font.size = Pt(36)
        pv.font.bold = True
        pv.font.color.rgb = col
        
        pt = tf.add_paragraph()
        pt.text = title
        pt.font.size = Pt(12)
        pt.font.bold = True
        pt.font.color.rgb = C_TEXT_MAIN
        
        pd = tf.add_paragraph()
        pd.text = desc
        pd.font.size = Pt(10.5)
        pd.font.color.rgb = C_TEXT_MUTED

    # 4 Verified Procedures Cards below
    procs = [
        ("T-01: MOTOR BENCH TEST", "Wheels lifted, forward/reverse tested at 100% PWM. Zero MCU brownout resets observed under peak startup surges.", "PASSED", C_GREEN),
        ("T-04: SENSOR INTEGRITY", "Ultrasonic echo wire disconnected during active drive. Rover halted immediately and latched SAFE_STOP.", "PASSED", C_GREEN),
        ("T-08: WI-FI SEVERING TEST", "Wi-Fi router powered off during video streaming. Video paused, while LoRa telemetry & control remained 100% active.", "VERIFIED", C_BLUE),
        ("T-10: SCHEMA DEFENSE", "Injected malformed JSON and out-of-bounds speed values. Gateway and firmware rejected rogue commands with zero actuation.", "VERIFIED", C_BLUE)
    ]

    for i, (title, body, status, col) in enumerate(procs):
        col_idx = i % 2
        row_idx = i // 2
        cx = Inches(0.8 + col_idx * 5.95)
        cy = Inches(4.1 + row_idx * 1.1)
        add_card(slide10, cx, cy, Inches(5.75), Inches(1.0), bg_col=C_CARD, border_col=col, border_width=1.0)
        
        tb = slide10.shapes.add_textbox(cx + Inches(0.2), cy + Inches(0.08), Inches(5.35), Inches(0.85))
        tf = tb.text_frame
        tf.word_wrap = True
        
        pt1 = tf.paragraphs[0]
        pt1.text = f"[{status}]  {title}"
        pt1.font.size = Pt(11)
        pt1.font.bold = True
        pt1.font.color.rgb = col
        
        pt2 = tf.add_paragraph()
        pt2.text = body
        pt2.font.size = Pt(10.5)
        pt2.font.color.rgb = C_TEXT_BODY

    # Bottom Integrity Bar
    add_card(slide10, Inches(0.8), Inches(6.45), Inches(11.733), Inches(0.65), bg_col=C_GREEN_BG, border_col=C_GREEN)
    tb_vi = slide10.shapes.add_textbox(Inches(1.0), Inches(6.48), Inches(11.3), Inches(0.55))
    tf_vi = tb_vi.text_frame
    pvi = tf_vi.paragraphs[0]
    pvi.text = "EMPIRICAL RIGOR: All values above reflect actual laboratory bench tests on our physical hardware. We clearly separate bench-verified results from future outdoor field goals."
    pvi.font.size = Pt(10.5)
    pvi.font.bold = True
    pvi.font.color.rgb = C_GREEN

    add_notes(slide10,
              "We believe presentations must be grounded in data, not fantasy. On this slide, you see our lab test results: our ultrasonic envelope reliably stopped the rover at 28 centimeters. The hardware E-Stop cut motor power in 0 milliseconds. We achieved over 98% packet delivery over LoRa through multiple walls. And in Test T-08, when we cut Wi-Fi, LoRa telemetry and safety control continued without a glitch.",
              "Empirical lab validation proves our fail-safe mechanisms work reliably under simulated fault conditions.",
              "Now let us examine real-world applications where this saves human lives.",
              "T-03 tests were conducted against flat drywall at 0.3 m/s duty cycle.")

    # =========================================================================
    # SLIDE 11: REAL-WORLD APPLICATIONS & FIELD IMPACT
    # =========================================================================
    slide11 = prs.slides.add_slide(blank_layout)
    add_bg(slide11)
    add_header(slide11, "REAL-WORLD IMPACT",
               "Target Deployment Sectors & Human Safety",
               "Replacing dangerous human physical entry with expendable, high-resilience autonomous scouts:")

    apps = [
        ("SEARCH & RESCUE IN COLLAPSED RUINS",
         "• Structural rubble rapidly blocks 2.4 GHz Wi-Fi within meters.\n"
         "• AURA-X penetrates sub-surface voids using 433 MHz LoRa, scouting for survivors and gas leaks before human rescue teams risk entry.",
         C_CORAL),
        ("HAZARDOUS INDUSTRIAL DUCT AUDITING",
         "• Chemical plants and refineries contain toxic conduits and confined spaces.\n"
         "• AURA-X replaces dangerous human physical entry with remote camera inspection and environmental sensing.",
         C_AMBER),
        ("SUBTERRANEAN UTILITIES & CULVERTS",
         "• Stormwater culverts and municipal sewers suffer complete GPS blackout and zero cellular coverage.\n"
         "• AURA-X conducts autonomous reactive inspection with video snapshot logging.",
         C_BLUE),
        ("PRECISION AGRICULTURE & CANOPY PATROLS",
         "• Sprawling acreage lacks ubiquitous Wi-Fi or 5G coverage.\n"
         "• AURA-X patrols crop furrows autonomously, transmitting micro-climate telemetry over long-range LoRa links to a central farm gateway.",
         C_GREEN)
    ]

    for i, (at, ab, ac) in enumerate(apps):
        col_idx = i % 2
        row_idx = i // 2
        cx = Inches(0.8 + col_idx * 5.95)
        cy = Inches(1.8 + row_idx * 2.35)
        add_card(slide11, cx, cy, Inches(5.75), Inches(2.2), bg_col=C_CARD, border_col=ac, border_width=1.5)
        
        tb = slide11.shapes.add_textbox(cx + Inches(0.25), cy + Inches(0.18), Inches(5.25), Inches(1.9))
        tf = tb.text_frame
        tf.word_wrap = True
        
        pt = tf.paragraphs[0]
        pt.text = at
        pt.font.size = Pt(13)
        pt.font.bold = True
        pt.font.color.rgb = ac
        
        pb = tf.add_paragraph()
        pb.text = f"\n{ab}"
        pb.font.size = Pt(12)
        pb.font.color.rgb = C_TEXT_BODY

    # Bottom Scalability Banner
    add_card(slide11, Inches(0.8), Inches(6.55), Inches(11.733), Inches(0.55), bg_col=C_BADGE_BG, border_col=C_BORDER_ACCENT)
    tb_imp = slide11.shapes.add_textbox(Inches(1.0), Inches(6.58), Inches(11.3), Inches(0.48))
    tf_imp = tb_imp.text_frame
    p_imp = tf_imp.paragraphs[0]
    p_imp.text = "FIELD SCALABILITY: Built entirely from standard COTS parts, enabling emergency response departments to deploy multi-agent scout swarms at 1/100th the cost of legacy robots."
    p_imp.font.size = Pt(11)
    p_imp.font.bold = True
    p_imp.font.color.rgb = C_BLUE

    add_notes(slide11,
              "Where does AURA-X make an immediate difference? First: search and rescue in collapsed rubble where Wi-Fi cannot penetrate. Second: toxic industrial ducts where human entry is hazardous. Third: subterranean culverts with zero GPS. And fourth: precision agriculture. An emergency agency can deploy twenty AURA-X scouts for less than the cost of a single commercial robot.",
              "A sub-150-dollar platform enables expendable, high-impact tactical deployment in life-threatening environments.",
              "Now let us conclude with our final winning pitch.",
              "Because components are standard COTS electronics, there are zero supply chain bottlenecks or exotic manufacturing dependencies.")

    # =========================================================================
    # SLIDE 12: WHY AURA-X DESERVES TO WIN (THE CLOSING PITCH & TEAM)
    # =========================================================================
    slide12 = prs.slides.add_slide(blank_layout)
    add_bg(slide12)
    add_header(slide12, "GRAND FINALE",
               "Why AURA-X Deserves to Win This Hackathon",
               "Solving the fundamental safety challenge of modern robotics through disciplined systems engineering:")

    win_pillars = [
        ("SOUND EMBEDDED DISCIPLINE",
         "• Not a fragile toy demo.\n"
         "• Built on proven embedded fundamentals: FreeRTOS task separation, split-rail power isolation, level-shifted signal paths, and zero-latency hardware stops.\n"
         "• Every pin constraint and packet byte is validated.",
         C_BLUE),
        ("ARCHITECTURAL BREAKTHROUGH",
         "• Solves the dangerous trade-off between modern generative AI and physical robot safety.\n"
         "• The cloud provides high-level cognitive inspection, while onboard firmware enforces deterministic physical boundaries over dual-band RF links.",
         C_GREEN),
        ("TACTICAL & HUMAN IMPACT",
         "• Built from accessible COTS hardware (<$135 USD), ready to replace human personnel in life-threatening subterranean, industrial, and disaster reconnaissance.\n"
         "• Enables multi-agent swarm deployments.",
         C_AMBER)
    ]

    for i, (st, sb, sc) in enumerate(win_pillars):
        cx = Inches(0.8 + i * 3.95)
        cy = Inches(1.8)
        add_card(slide12, cx, cy, Inches(3.8), Inches(3.5), bg_col=C_CARD, border_col=sc, border_width=1.5)
        
        tb = slide12.shapes.add_textbox(cx + Inches(0.25), cy + Inches(0.2), Inches(3.3), Inches(3.1))
        tf = tb.text_frame
        tf.word_wrap = True
        
        pt = tf.paragraphs[0]
        pt.text = st
        pt.font.size = Pt(14)
        pt.font.bold = True
        pt.font.color.rgb = sc
        
        pb = tf.add_paragraph()
        pb.text = f"\n{sb}"
        pb.font.size = Pt(12)
        pb.font.color.rgb = C_TEXT_BODY

    # Grand Closing Banner with Team Names
    add_card(slide12, Inches(0.8), Inches(5.45), Inches(11.733), Inches(1.6), bg_col=C_BADGE_BG, border_col=C_BORDER_ACCENT, border_width=1.5)
    tb_fin = slide12.shapes.add_textbox(Inches(1.0), Inches(5.55), Inches(11.3), Inches(1.4))
    tf_fin = tb_fin.text_frame
    tf_fin.word_wrap = True

    pfn1 = tf_fin.paragraphs[0]
    pfn1.text = "PROVEN FAULT-TOLERANCE.  •  DUAL-BAND RESILIENCE.  •  BOUNDED COGNITIVE AI."
    pfn1.font.size = Pt(13)
    pfn1.font.bold = True
    pfn1.font.color.rgb = C_BLUE

    pfn2 = tf_fin.add_paragraph()
    pfn2.text = "Thank you, judges! We look forward to your questions."
    pfn2.font.size = Pt(15)
    pfn2.font.bold = True
    pfn2.font.color.rgb = C_TEXT_MAIN

    pfn3 = tf_fin.add_paragraph()
    pfn3.text = "Team: Soham Vinchu  |  Nishita Patil  |  Vedant Mali  |  Bhakti Sonawane"
    pfn3.font.size = Pt(12)
    pfn3.font.bold = True
    pfn3.font.color.rgb = C_BLUE

    pfn4 = tf_fin.add_paragraph()
    pfn4.text = "Open Source Firmware & Schematics Repository  |  Full Technical Reference Report [References 1-7 Attached]"
    pfn4.font.size = Pt(10.5)
    pfn4.font.color.rgb = C_TEXT_MUTED

    add_notes(slide12,
              "To conclude: AURA-X is not just another hackathon robot that drives forward and calls a cloud API. It is an architectural blueprint for how modern autonomous systems must be built. By anchoring high-level cloud reasoning within a deterministic, real-time embedded safety envelope—and connecting it via an asymmetric LoRa and Wi-Fi backbone—we have created an exploration rover that is intelligent, resilient, and accessible to anyone. We deliver industrial-grade fail-safe operation on an accessible platform that can save lives in disaster zones and hazardous facilities. Thank you for your time, and we now welcome your questions.",
              "AURA-X solves the fundamental safety challenge of modern robotics: Intelligence in the cloud, autonomy at the edge, absolute safety in the firmware.",
              "Conclude with confidence and open the floor for judge Q&A.",
              "Be ready for technical questions regarding FreeRTOS task prioritization, LoRa packet structure, power rail isolation, and API structured output schemas.")

    # Save presentation
    output_path = "AURA_X_Winning_Hackathon_Pitch_Deck.pptx"
    prs.save(output_path)
    print(f"Light mode presentation saved successfully to: {output_path}")

if __name__ == '__main__':
    build_light_deck()

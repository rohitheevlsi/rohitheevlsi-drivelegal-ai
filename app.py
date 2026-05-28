# ─────────────────────────────────────────────────────────────────────────────
# DriveLegal AI | Main App | Road Safety Hackathon 2026
# Run: streamlit run app.py
# ─────────────────────────────────────────────────────────────────────────────
import streamlit as st
from datetime import date, timedelta
import pandas as pd

# ── Page config (must be first Streamlit call) ────────────────────────────────
st.set_page_config(
    page_title="DriveLegal AI — India's Traffic Law Assistant",
    page_icon="🚦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Local imports ─────────────────────────────────────────────────────────────
from ui.styles import MAIN_CSS, LETTER_CSS
from ui.components import (
    hero, stat_row, section_header, result_box,
    emergency_sidebar, violation_select, state_select,
    language_select, display_fine_result, display_penalty_status,
    render_dashboard_cards, render_back_button,
)
from utils.calculators import (
    calculate_bac, calculate_fine, get_penalty_status,
    check_document, get_speed_limits, ROAD_TYPE_LABELS,
)
from ai.client import (
    chat, validate_challan_with_image, validate_challan_text,
    generate_dispute_letter, answer_legal_query,
    compare_states, explain_rights, stream_ai_response,
)
from laws_data import TRAFFIC_LAWS_DB, SYSTEM_PROMPT

# ── Inject CSS ────────────────────────────────────────────────────────────────
st.markdown(MAIN_CSS, unsafe_allow_html=True)

# ── Initialize Navigation State ───────────────────────────────────────────────
if "active_tool" not in st.session_state:
    st.session_state.active_tool = None

# ── Sidebar ───────────────────────────────────────────────────────────────────
emergency_sidebar()

# ── Main Content Layout ───────────────────────────────────────────────────────
if st.session_state.active_tool is None:
    # ── Render Dashboard Home ──
    hero()
    stat_row()
    render_dashboard_cards()

else:
    # ── Render Active Tool View ──
    render_back_button()
    
    # -------------------------------------------------------------------------
    # TOOL: AI Legal Chat
    # -------------------------------------------------------------------------
    if st.session_state.active_tool == "chat":
        section_header("💬", "AI Traffic Law Assistant")
        st.markdown("Ask anything about Indian traffic laws, challans, rights, fines, or procedures.")

        col1, col2 = st.columns([2, 1])
        with col1:
            lang = language_select(key="chat_lang")
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            st.button(
                "Clear Conversation 🗑️",
                key="chat_clear",
                on_click=lambda: st.session_state.update(chat_history=[], api_messages=[]),
                use_container_width=True
            )

        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
        if "api_messages" not in st.session_state:
            st.session_state.api_messages = []

        # Render message history
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        # Handle new user input
        if user_input := st.chat_input("Ask anything about Indian traffic laws, fines, or procedures..."):
            # Append user message
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            
            # Formulate message with language override instruction
            user_msg = user_input
            if lang != "English":
                user_msg += f" (Please respond in {lang})"
            st.session_state.api_messages.append({"role": "user", "content": user_msg})

            # Display user message immediately
            with st.chat_message("user"):
                st.markdown(user_input)

            # Display assistant message box and stream output
            with st.chat_message("assistant"):
                prompt = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.api_messages])
                
                response_placeholder = st.empty()
                full_response = ""
                
                # Stream content from client generator
                for chunk in stream_ai_response(prompt, system_prompt=SYSTEM_PROMPT):
                    full_response += chunk
                    response_placeholder.markdown(full_response + " 🚦")
                
                # Render clean final message
                response_placeholder.markdown(full_response)

            st.session_state.chat_history.append({"role": "assistant", "content": full_response})
            st.session_state.api_messages.append({"role": "assistant", "content": full_response})
            st.rerun()

    # -------------------------------------------------------------------------
    # TOOL: Challan Validator
    # -------------------------------------------------------------------------
    elif st.session_state.active_tool == "challan":
        section_header("📋", "Challan Validator")
        st.markdown("Upload your challan photo **or** describe it — we verify if the fine is legally correct.")

        col1, col2 = st.columns(2)
        with col1:
            challan_state = state_select("State where challan was issued", key="chk_state")
            challan_violation = st.text_input("Violation on challan", placeholder="e.g. No Helmet", key="chk_viol")
            challan_fine = st.number_input("Fine amount on challan (₹)", min_value=0, step=100, key="chk_fine")
        with col2:
            uploaded = st.file_uploader("Upload challan image (optional)", type=["jpg","jpeg","png","webp"], key="chk_img")
            if uploaded:
                st.image(uploaded, caption="Uploaded Challan", use_container_width=True)

        if st.button("🔍 Validate Challan", key="chk_btn", use_container_width=True):
            if not challan_violation.strip():
                st.warning("Please enter the violation type.")
            elif challan_fine == 0:
                st.warning("Please enter the fine amount.")
            else:
                with st.spinner("Analysing challan with AI…"):
                    if uploaded:
                        img_bytes = uploaded.read()
                        mime = f"image/{uploaded.name.split('.')[-1].lower().replace('jpg','jpeg')}"
                        result = validate_challan_with_image(
                            img_bytes, mime, challan_state, challan_violation, int(challan_fine)
                        )
                    else:
                        result = validate_challan_text(challan_state, challan_violation, int(challan_fine))

                kind = "success" if "VALID ✅" in result else ("danger" if "OVERCHARGED ❌" in result else "warning")
                result_box(result.replace("\n", "<br>"), kind)

    # -------------------------------------------------------------------------
    # TOOL: Dispute Letter Generator
    # -------------------------------------------------------------------------
    elif st.session_state.active_tool == "dispute":
        section_header("✉️", "Dispute Letter Generator")
        st.markdown("Generate a **print-ready formal letter** to dispute a challan. Fill in your details below.")

        c1, c2 = st.columns(2)
        with c1:
            dl_name       = st.text_input("Your Full Name", key="dl_name")
            dl_address    = st.text_area("Your Address", height=80, key="dl_addr")
            dl_vehicle    = st.text_input("Vehicle Number", placeholder="TN01AB1234", key="dl_veh")
            dl_challan    = st.text_input("Challan / Notice Number", key="dl_chno")
        with c2:
            dl_date       = st.date_input("Date of Offence", key="dl_date")
            dl_state      = state_select("State", key="dl_state")
            dl_violation  = st.text_input("Violation Alleged", key="dl_viol")
            dl_fine_paid  = st.number_input("Fine Charged (₹)", min_value=0, step=100, key="dl_fine")
            dl_legal_fine = st.number_input("Correct Legal Fine (₹)", min_value=0, step=100, key="dl_lfine")

        dl_grounds = st.text_area(
            "Grounds for Dispute",
            placeholder="e.g. Fine amount exceeds MV Act 2019 limit. Speed gun calibration certificate not shown.",
            height=80, key="dl_grounds"
        )

        if st.button("✉️ Generate Dispute Letter", key="dl_btn", use_container_width=True):
            missing = [f for f, v in {
                "Name": dl_name, "Address": dl_address, "Vehicle No": dl_vehicle,
                "Challan No": dl_challan, "Violation": dl_violation, "Grounds": dl_grounds,
            }.items() if not str(v).strip()]
            if missing:
                st.warning(f"Please fill in: {', '.join(missing)}")
            else:
                with st.spinner("Drafting your legal letter…"):
                    letter = generate_dispute_letter(
                        dl_name, dl_address, dl_vehicle, dl_challan,
                        str(dl_date), dl_violation, int(dl_fine_paid),
                        int(dl_legal_fine), dl_grounds, dl_state,
                    )
                st.success("✅ Letter generated! Copy and print on plain paper.")
                st.markdown(LETTER_CSS, unsafe_allow_html=True)
                st.markdown(f'<div class="letter-container">{letter}</div>', unsafe_allow_html=True)
                st.download_button("⬇️ Download as .txt", letter, file_name="dispute_letter.txt", mime="text/plain", use_container_width=True)

    # -------------------------------------------------------------------------
    # TOOL: Fine Calculator
    # -------------------------------------------------------------------------
    elif st.session_state.active_tool == "fine":
        section_header("💰", "Fine Calculator")
        st.markdown("Calculate the exact legal fine for any violation in any Indian state.")

        col1, col2 = st.columns(2)
        with col1:
            fc_violation = violation_select("Select Violation", key="fc_viol")
            fc_state     = state_select("State", key="fc_state")
        with col2:
            fc_repeat = st.radio("Offence Type", ["First Offence", "Repeat Offence"], key="fc_rep", horizontal=True)

        if st.button("💰 Calculate Fine", key="fc_btn", use_container_width=True):
            is_repeat = fc_repeat == "Repeat Offence"
            fine_info = calculate_fine(fc_violation, is_repeat, fc_state)
            display_fine_result(fine_info)

        st.divider()
        section_header("📊", "All Violations Quick Reference")
        laws = TRAFFIC_LAWS_DB["national_mv_act_2019"]
        rows = []
        for k, v in laws.items():
            rows.append({
                "Violation": v["violation"],
                "Section": v["section"],
                "First Fine (₹)": f"₹{v['fine_first']:,}",
                "Repeat Fine (₹)": f"₹{v['fine_repeat']:,}",
                "Penalty Points": v.get("licence_points", 0),
            })
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    # -------------------------------------------------------------------------
    # TOOL: BAC Calculator
    # -------------------------------------------------------------------------
    elif st.session_state.active_tool == "bac":
        section_header("🍺", "BAC Calculator")
        st.markdown(
            "Estimate your Blood Alcohol Content using the Widmark formula. "
            "**India's legal BAC limit is 30 mg/100ml.** This is for awareness only — never drink and drive."
        )

        col1, col2, col3 = st.columns(3)
        with col1:
            bac_weight  = st.number_input("Body Weight (kg)", 30, 200, 70, key="bac_wt")
            bac_gender  = st.radio("Gender", ["Male", "Female"], key="bac_gen", horizontal=True)
        with col2:
            bac_drinks  = st.number_input("Number of Drinks", 0.0, 30.0, 2.0, 0.5, key="bac_dr")
            bac_ml      = st.number_input("ml per drink", 10, 500, 30, key="bac_ml")
        with col3:
            bac_abv     = st.number_input("Alcohol % (ABV)", 1.0, 90.0, 40.0, 0.5, key="bac_abv")
            bac_hours   = st.number_input("Hours since first drink", 0.0, 24.0, 1.0, 0.5, key="bac_hrs")

        if st.button("🧪 Calculate BAC", key="bac_btn", use_container_width=True):
            try:
                result = calculate_bac(bac_weight, bac_gender, bac_drinks, bac_hours, bac_ml, bac_abv)
                col1, col2, col3 = st.columns(3)
                col1.metric("BAC (%)", f"{result.bac_percent:.4f}%")
                col2.metric("BAC (mg/100ml)", f"{result.bac_mg_per_100ml:.1f} mg")
                col3.metric("India Limit", "30 mg/100ml")

                kind = "danger" if result.is_over_limit else "success"
                msg  = f"🚨 **OVER LIMIT** — Do NOT drive. Wait at least **{result.hours_to_legal} hours**." if result.is_over_limit else "✅ Below India's legal limit. Still, if you feel impaired — don't drive."
                result_box(f"<b>Risk Level:</b> {result.risk_level}<br>{msg}", kind)
                st.warning(result.disclaimer)

                if result.is_over_limit:
                    st.error("🚨 **Legal consequence if caught:** ₹10,000 fine or 6 months jail + licence suspension (Section 185, MV Act 2019)")
            except ValueError as e:
                st.error(str(e))

    # -------------------------------------------------------------------------
    # TOOL: Licence Penalty Points Tracker
    # -------------------------------------------------------------------------
    elif st.session_state.active_tool == "points":
        section_header("📍", "Licence Penalty Points Tracker")
        st.markdown(
            "Under MV Act 2019, penalty points accumulate on your licence. "
            "Reaching **12 points** means automatic suspension."
        )

        laws = TRAFFIC_LAWS_DB["national_mv_act_2019"]

        if "selected_violations" not in st.session_state:
            st.session_state.selected_violations = []

        selected = st.multiselect(
            "Select violations committed",
            options=[(v["violation"], v.get("licence_points", 0)) for v in laws.values() if v.get("licence_points", 0) > 0],
            format_func=lambda x: f"{x[0]} ({x[1]} pts)",
            key="pp_sel"
        )

        manual = st.number_input("Or enter total points manually", 0, 30, 0, key="pp_manual")

        total = sum(x[1] for x in selected) + manual

        if st.button("📊 Check My Status", key="pp_btn", use_container_width=True):
            status = get_penalty_status(total)
            display_penalty_status(status)

        st.divider()
        section_header("📋", "Penalty Points Reference Table")
        rows = [
            {"Violation": v["violation"], "Points": v.get("licence_points", 0), "Section": v["section"]}
            for v in laws.values() if v.get("licence_points", 0) > 0
        ]
        df = pd.DataFrame(rows).sort_values("Points", ascending=False)
        st.dataframe(df, use_container_width=True, hide_index=True)

    # -------------------------------------------------------------------------
    # TOOL: Document Expiry Checker
    # -------------------------------------------------------------------------
    elif st.session_state.active_tool == "doc":
        section_header("📄", "Document Expiry Checker")
        st.markdown("Check if your vehicle documents are valid and see the fine if caught expired.")

        DOC_OPTIONS = {
            "Driving Licence (DL)":         "driving_licence",
            "Vehicle Registration (RC)":    "vehicle_registration_rc",
            "Insurance":                    "insurance",
            "PUC Certificate":              "puc_certificate",
            "Fitness Certificate (FC)":     "fitness_certificate",
        }

        st.markdown("Enter expiry dates for your documents:")
        results = []
        cols = st.columns(2)
        items = list(DOC_OPTIONS.items())
        for i, (label, key) in enumerate(items):
            with cols[i % 2]:
                exp = st.date_input(label, value=date.today() + timedelta(days=180), key=f"doc_{key}")
                results.append((key, exp))

        if st.button("🔍 Check All Documents", key="doc_btn", use_container_width=True):
            all_ok = True
            for key, exp in results:
                try:
                    status = check_document(key, exp)
                    icon = "✅" if not status.is_expired else ("⏳" if status.in_grace else "🚨")
                    with st.expander(f"{icon} {status.doc_name}", expanded=status.is_expired):
                        st.markdown(status.advice)
                        if status.is_expired:
                            st.error(f"Fine if caught: ₹{status.fine_if_caught:,} under {status.section}")
                            all_ok = False
                except Exception as e:
                    st.error(f"Error checking {key}: {e}")
            if all_ok:
                st.success("✅ All your documents are valid!")

    # -------------------------------------------------------------------------
    # TOOL: State Rules Comparator
    # -------------------------------------------------------------------------
    elif st.session_state.active_tool == "compare":
        section_header("🗺️", "State Rules Comparator")
        st.markdown("Compare traffic rules and fines between any two Indian states.")

        col1, col2 = st.columns(2)
        states = sorted(TRAFFIC_LAWS_DB["states"].keys())
        with col1:
            sc_state1 = st.selectbox("State 1", states, index=states.index("Tamil Nadu"), key="sc_s1")
        with col2:
            sc_state2 = st.selectbox("State 2", states, index=states.index("Delhi"), key="sc_s2")

        sc_violation = st.text_input("Violation to compare", value="drunk driving", key="sc_viol")

        if st.button("⚖️ Compare States", key="sc_btn", use_container_width=True):
            if sc_state1 == sc_state2:
                st.warning("Please select two different states.")
            else:
                with st.spinner("Comparing states…"):
                    result = compare_states(sc_state1, sc_state2, sc_violation)
                result_box(result.replace("\n", "<br>"), "info")

        st.divider()
        section_header("🗂️", "State-wise Quick Facts")
        selected_state = st.selectbox("Select a state for detailed info", states, key="sc_detail")
        state_data = TRAFFIC_LAWS_DB["states"].get(selected_state, {})
        if state_data:
            col1, col2 = st.columns(2)
            col1.metric("Traffic Helpline", state_data.get("traffic_helpline", "103"))
            col2.metric("Emergency", state_data.get("emergency", "112"))
            if state_data.get("notes"):
                st.info(f"📌 {state_data['notes']}")
            if state_data.get("unique_rule"):
                st.warning(f"🔔 **Unique Rule:** {state_data['unique_rule']}")
            if state_data.get("dispute_office"):
                st.markdown(f"**Dispute Office:** {state_data['dispute_office']}")

    # -------------------------------------------------------------------------
    # TOOL: AI Rights Advisor
    # -------------------------------------------------------------------------
    elif st.session_state.active_tool == "rights":
        section_header("⚖️", "Know Your Rights When Stopped by Police")

        rights = TRAFFIC_LAWS_DB["rights_if_stopped"]
        col1, col2 = st.columns(2)
        yes_rights = [r for r in rights if r["positive"]]
        no_rights  = [r for r in rights if not r["positive"]]

        with col1:
            st.markdown("### ✅ Your Rights")
            for r in yes_rights:
                with st.expander(f"✅ {r['right']}"):
                    st.markdown(r["detail"])

        with col2:
            st.markdown("### ❌ What Officers CANNOT Do")
            for r in no_rights:
                with st.expander(f"❌ {r['right']}"):
                    st.markdown(r["detail"])

        st.divider()
        section_header("🤖", "AI Rights Advisor")
        st.markdown("Describe your situation and get personalised legal rights guidance.")

        scenario = st.text_area(
            "Describe your situation",
            placeholder="e.g. Officer stopped me at night, demanded ₹2000 cash, refused to give challan receipt.",
            height=100, key="rights_scenario"
        )
        rights_lang = language_select(key="rights_lang")

        if st.button("⚖️ Get Rights Advice", key="rights_btn", use_container_width=True):
            if not scenario.strip():
                st.warning("Please describe your situation.")
            else:
                with st.spinner("Analysing your rights…"):
                    query = scenario
                    if rights_lang != "English":
                        query += f" Please respond in {rights_lang}."
                    reply = explain_rights(query)
                result_box(reply.replace("\n", "<br>"), "info")

        st.divider()
        section_header("📋", "Dispute Process — Step by Step")
        for step in TRAFFIC_LAWS_DB["dispute_process"]["steps"]:
            st.markdown(f"- {step}")
        col1, col2 = st.columns(2)
        col1.markdown(f"**Time limit:** {TRAFFIC_LAWS_DB['dispute_process']['time_limit']}")
        col2.markdown(f"**Online portal:** [{TRAFFIC_LAWS_DB['dispute_process']['online_portal']}]({TRAFFIC_LAWS_DB['dispute_process']['online_portal']})")

        st.markdown("**Common grounds for dispute:**")
        for g in TRAFFIC_LAWS_DB["dispute_process"]["common_grounds"]:
            st.markdown(f"- {g}")

    # -------------------------------------------------------------------------
    # TOOL: Speed Limits Guide
    # -------------------------------------------------------------------------
    elif st.session_state.active_tool == "speed":
        section_header("🚗", "Speed Limits Guide")
        st.markdown("Official speed limits under MV Act 2019 by road type and vehicle category.")

        road_type = st.selectbox(
            "Select Road Type",
            list(ROAD_TYPE_LABELS.keys()),
            format_func=lambda x: ROAD_TYPE_LABELS[x],
            key="sl_road"
        )

        limits = get_speed_limits(road_type)
        if "error" not in limits:
            col1, col2, col3 = st.columns(3)
            col1.metric("🚗 Car / Jeep / Van", f"{limits['car_jeep']} km/h")
            col2.metric("🚌 Bus / Truck", f"{limits['bus_truck']} km/h")
            col3.metric("🏍️ Two Wheeler", f"{limits['two_wheeler']} km/h")
            if limits.get("note"):
                st.info(f"ℹ️ {limits['note']}")

        st.divider()
        section_header("📊", "All Road Types — Speed Limit Table")
        rows = []
        for rt, label in ROAD_TYPE_LABELS.items():
            l = get_speed_limits(rt)
            rows.append({
                "Road Type": label,
                "Car / Jeep (km/h)": l.get("car_jeep", "—"),
                "Bus / Truck (km/h)": l.get("bus_truck", "—"),
                "Two Wheeler (km/h)": l.get("two_wheeler", "—"),
                "Note": l.get("note", ""),
            })
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

        st.divider()
        section_header("⚡", "Overspeeding Fine Calculator")
        col1, col2 = st.columns(2)
        with col1:
            os_veh = st.selectbox("Vehicle Type", ["Light Motor Vehicle", "Medium Passenger", "Heavy Vehicle"], key="os_veh")
        with col2:
            os_repeat = st.radio("Offence", ["First", "Repeat"], horizontal=True, key="os_rep")

        viol_map = {
            "Light Motor Vehicle": "overspeeding_light",
            "Medium Passenger": "overspeeding_medium",
            "Heavy Vehicle": "overspeeding_heavy",
        }
        os_state = state_select("State", key="os_state")

        if st.button("💰 Get Overspeeding Fine", key="os_btn", use_container_width=True):
            fine_info = calculate_fine(viol_map[os_veh], os_repeat == "Repeat", os_state)
            display_fine_result(fine_info)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<center><small>🚦 DriveLegal AI · Road Safety Hackathon 2026 · IIT Madras × MoRTH · "
    "Built with ❤️ for safer Indian roads · "
    "Data: Motor Vehicles (Amendment) Act 2019 · "
    "For legal advice, consult a qualified advocate.</small></center>",
    unsafe_allow_html=True,
)

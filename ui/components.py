# ─────────────────────────────────────────────────────────────────────────────
# DriveLegal AI | UI Components
# Reusable Streamlit display helpers
# ─────────────────────────────────────────────────────────────────────────────
import streamlit as st
from laws_data import TRAFFIC_LAWS_DB


def hero():
    """Render top hero banner."""
    st.markdown("""
    <div class="hero-banner">
      <h1>🚦 DriveLegal AI</h1>
      <p>India's AI-powered traffic law assistant — Road Safety Hackathon 2026 · IIT Madras × MoRTH</p>
    </div>
    """, unsafe_allow_html=True)


def stat_row():
    """Display headline stats."""
    st.markdown("""
    <div class="stat-row">
      <div class="stat-card"><div class="num">30+</div><div class="lbl">Violations Covered</div></div>
      <div class="stat-card"><div class="num">18</div><div class="lbl">Indian States</div></div>
      <div class="stat-card"><div class="num">10+</div><div class="lbl">Regional Languages</div></div>
      <div class="stat-card"><div class="num">MV 2019</div><div class="lbl">Latest Act</div></div>
      <div class="stat-card"><div class="num">₹0</div><div class="lbl">Cost to Citizens</div></div>
    </div>
    """, unsafe_allow_html=True)


def section_header(icon: str, title: str):
    st.markdown(f'<div class="section-header">{icon} {title}</div>', unsafe_allow_html=True)


def result_box(content: str, kind: str = ""):
    """Render a styled result box. kind: success | warning | danger | info | ''"""
    st.markdown(f'<div class="result-box {kind}">{content}</div>', unsafe_allow_html=True)


def emergency_sidebar():
    """Sidebar with emergency contacts inside a clean expander."""
    with st.sidebar:
        st.markdown("<h2 style='text-align: center; color: #FF6B35; font-family: Outfit;'>🚦 DriveLegal AI</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-size: 0.85rem; color: rgba(255,255,255,0.6);'>Road Safety Legal Shield</p>", unsafe_allow_html=True)
        
        st.divider()

        # Let's add the active tool info or sidebar navigation here if needed
        # (It will be managed in app.py, but let's provide a fallback)
        if "active_tool" in st.session_state and st.session_state.active_tool:
            tool_labels = {
                "chat": "💬 AI Legal Chat",
                "challan": "📋 Challan Validator",
                "dispute": "✉️ Dispute Generator",
                "fine": "💰 Fine Calculator",
                "bac": "🍺 BAC Calculator",
                "points": "📍 Licence Points",
                "doc": "📄 Document Checker",
                "compare": "🗺️ State Comparator",
                "rights": "⚖️ AI Rights Advisor",
                "speed": "🚗 Speed Limits Guide"
            }
            active_lbl = tool_labels.get(st.session_state.active_tool, "Dashboard")
            st.info(f"📍 Active: **{active_lbl}**")
            if st.button("⬅️ Dashboard Home", key="sidebar_back", use_container_width=True):
                st.session_state.active_tool = None
                st.rerun()
            st.divider()
        
        with st.expander("🚨 Emergency Contacts", expanded=False):
            contacts = TRAFFIC_LAWS_DB["emergency_contacts"]
            contact_display = {
                "🆘 National": contacts["national_emergency"],
                "🚔 Police": contacts["police"],
                "🚑 Ambulance": contacts["ambulance"],
                "🔥 Fire": contacts["fire"],
                "🛣️ Road Accident": contacts["road_accident_helpline"],
                "👩 Women Helpline": contacts["women_helpline"],
                "⚖️ Legal Aid": contacts["legal_aid"],
                "🛡️ Anti-Corruption": contacts["anti_corruption"],
                "💻 Cyber Crime": contacts["cyber_crime"],
            }
            for label, number in contact_display.items():
                st.markdown(f"**{label}:** `{number}`")

        with st.expander("🔗 Useful Quick Links", expanded=False):
            st.markdown("- [Pay Challan Online](https://vahan.parivahan.gov.in/challan)")
            st.markdown("- [Check E-Challan](https://echallan.parivahan.gov.in)")
            st.markdown("- [MoRTH Website](https://morth.nic.in)")
            st.markdown("- [Free Legal Aid (DLSA)](https://nalsa.gov.in)")

        st.divider()
        st.markdown(
            "<div style='text-align: center;'><small style='color: rgba(245,246,250,0.45);'>DriveLegal AI is for awareness only. "
            "For legal advice, consult an advocate. "
            "IIT Madras × MoRTH · 2026</small></div>",
            unsafe_allow_html=True,
        )


def render_dashboard_cards():
    """Render a premium grid of tool launch cards."""
    # Let's use 3 main columns or sections
    st.markdown("<h3 style='margin-top: 1.5rem; font-family: Outfit; font-weight:700;'>🤖 AI Legal Powerhouse</h3>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        with st.container(border=True):
            st.markdown('<div class="card-icon">💬</div>', unsafe_allow_html=True)
            st.markdown('<div class="card-title">AI Legal Chat</div>', unsafe_allow_html=True)
            st.markdown('<div class="card-desc">Chat about traffic law, checkpoints, or fines in 10+ languages.</div>', unsafe_allow_html=True)
            st.button("Open Chat 🚦", key="btn_chat", on_click=lambda: select_tool("chat"), use_container_width=True)
    with c2:
        with st.container(border=True):
            st.markdown('<div class="card-icon">📋</div>', unsafe_allow_html=True)
            st.markdown('<div class="card-title">Challan Validator</div>', unsafe_allow_html=True)
            st.markdown('<div class="card-desc">Verify if a fine amount is legally correct by text or image.</div>', unsafe_allow_html=True)
            st.button("Validate 🔍", key="btn_challan", on_click=lambda: select_tool("challan"), use_container_width=True)
    with c3:
        with st.container(border=True):
            st.markdown('<div class="card-icon">✉️</div>', unsafe_allow_html=True)
            st.markdown('<div class="card-title">Dispute Letter</div>', unsafe_allow_html=True)
            st.markdown('<div class="card-desc">Draft a formal, print-ready dispute letter to contest a challan.</div>', unsafe_allow_html=True)
            st.button("Generate 📝", key="btn_dispute", on_click=lambda: select_tool("dispute"), use_container_width=True)
    with c4:
        with st.container(border=True):
            st.markdown('<div class="card-icon">⚖️</div>', unsafe_allow_html=True)
            st.markdown('<div class="card-title">Rights Advisor</div>', unsafe_allow_html=True)
            st.markdown('<div class="card-desc">Describe a checkpoint situation to get instant rights guidance.</div>', unsafe_allow_html=True)
            st.button("Check Rights 🛡️", key="btn_rights", on_click=lambda: select_tool("rights"), use_container_width=True)

    st.markdown("<h3 style='margin-top: 2rem; font-family: Outfit; font-weight:700;'>🧮 Smart Calculators & Trackers</h3>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        with st.container(border=True):
            st.markdown('<div class="card-icon">💰</div>', unsafe_allow_html=True)
            st.markdown('<div class="card-title">Fine Calculator</div>', unsafe_allow_html=True)
            st.markdown('<div class="card-desc">Calculate exact legal fines for any violation across all states.</div>', unsafe_allow_html=True)
            st.button("Calculate Fine 💸", key="btn_fine", on_click=lambda: select_tool("fine"), use_container_width=True)
    with c2:
        with st.container(border=True):
            st.markdown('<div class="card-icon">🍺</div>', unsafe_allow_html=True)
            st.markdown('<div class="card-title">BAC Calculator</div>', unsafe_allow_html=True)
            st.markdown('<div class="card-desc">Estimate your Blood Alcohol Content using the Widmark formula.</div>', unsafe_allow_html=True)
            st.button("Estimate BAC 🧪", key="btn_bac", on_click=lambda: select_tool("bac"), use_container_width=True)
    with c3:
        with st.container(border=True):
            st.markdown('<div class="card-icon">📍</div>', unsafe_allow_html=True)
            st.markdown('<div class="card-title">Penalty Tracker</div>', unsafe_allow_html=True)
            st.markdown('<div class="card-desc">Track demerit points on your licence and suspension risk.</div>', unsafe_allow_html=True)
            st.button("Check Points 📊", key="btn_points", on_click=lambda: select_tool("points"), use_container_width=True)

    st.markdown("<h3 style='margin-top: 2rem; font-family: Outfit; font-weight:700;'>📚 Safety Guides & Verification</h3>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        with st.container(border=True):
            st.markdown('<div class="card-icon">📄</div>', unsafe_allow_html=True)
            st.markdown('<div class="card-title">Document Expiry</div>', unsafe_allow_html=True)
            st.markdown('<div class="card-desc">Log expiry dates for DL, RC, PUC to check validity and fines.</div>', unsafe_allow_html=True)
            st.button("Check Expiry ⏰", key="btn_doc", on_click=lambda: select_tool("doc"), use_container_width=True)
    with c2:
        with st.container(border=True):
            st.markdown('<div class="card-icon">🗺️</div>', unsafe_allow_html=True)
            st.markdown('<div class="card-title">State Comparator</div>', unsafe_allow_html=True)
            st.markdown('<div class="card-desc">Compare traffic regulations and fine differences side-by-side.</div>', unsafe_allow_html=True)
            st.button("Compare States 🗺️", key="btn_compare", on_click=lambda: select_tool("compare"), use_container_width=True)
    with c3:
        with st.container(border=True):
            st.markdown('<div class="card-icon">🚗</div>', unsafe_allow_html=True)
            st.markdown('<div class="card-title">Speed Limits Guide</div>', unsafe_allow_html=True)
            st.markdown('<div class="card-desc">Verify road speed limits and calculate overspeeding fines.</div>', unsafe_allow_html=True)
            st.button("View Limits ⚡", key="btn_speed", on_click=lambda: select_tool("speed"), use_container_width=True)


def select_tool(tool_name):
    """Callback to switch the active tool page."""
    st.session_state.active_tool = tool_name


def render_back_button():
    """Render a premium Back to Dashboard row."""
    col1, col2 = st.columns([1, 5])
    with col1:
        st.button("⬅️ Back Home", key="back_to_dashboard_btn", on_click=lambda: select_tool(None))


def violation_select(label: str = "Select Violation", key: str = "viol") -> str:
    """Dropdown for all violations in national_mv_act_2019."""
    laws = TRAFFIC_LAWS_DB["national_mv_act_2019"]
    options = {v["violation"]: k for k, v in laws.items()}
    chosen_label = st.selectbox(label, list(options.keys()), key=key)
    return options[chosen_label]


def state_select(label: str = "Select State", key: str = "state") -> str:
    states = sorted(TRAFFIC_LAWS_DB["states"].keys())
    return st.selectbox(label, states, key=key)


def language_select(key: str = "lang") -> str:
    languages = [
        "English", "Tamil", "Hindi", "Telugu", "Kannada",
        "Bengali", "Marathi", "Gujarati", "Malayalam", "Punjabi", "Odia",
    ]
    return st.selectbox("🌐 Response Language", languages, key=key)


def display_fine_result(fine_info: dict):
    """Nicely display output from calculate_fine()."""
    if "error" in fine_info:
        st.error(fine_info["error"])
        return
    col1, col2, col3 = st.columns(3)
    col1.metric("💰 Fine Amount", f"₹{fine_info['effective_fine']:,}")
    col2.metric("⚠️ Penalty Points", fine_info["licence_points"])
    col3.metric("Repeat Offence", "Yes" if fine_info["is_repeat"] else "No")
    st.markdown(f"""
    **Violation:** {fine_info['violation']}  
    **Legal Section:** `{fine_info['section']}` — {fine_info['act']}  
    **Punishment:** {fine_info['punishment']}
    """)
    if fine_info.get("state_note"):
        st.info(f"🗺️ **{fine_info['state']} specific:** {fine_info['state_note']}")


def display_penalty_status(status):
    """Display penalty point status with colour-coded metric."""
    color_map = {"green": "normal", "amber": "inverse", "orange": "inverse", "red": "off"}
    delta_color = color_map.get(status.color, "normal")
    col1, col2 = st.columns(2)
    col1.metric("🎯 Total Points", status.total_points, delta_color=delta_color)
    col2.metric("📍 Status", status.status)
    if status.points_to_suspension > 0:
        st.progress(min(status.total_points / 12, 1.0), text=f"{status.points_to_suspension} points away from suspension")
    else:
        st.error("⛔ Licence SUSPENDED — Appear before licensing authority immediately.")
    st.info(status.message)


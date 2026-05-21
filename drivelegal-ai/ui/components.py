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
    """Sidebar with emergency contacts."""
    with st.sidebar:
        st.markdown("## 🚨 Emergency Contacts")
        contacts = TRAFFIC_LAWS_DB["emergency_contacts"]
        contact_display = {
            "🆘 National Emergency": contacts["national_emergency"],
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

        st.divider()
        st.markdown("### 🔗 Useful Links")
        st.markdown("- [Pay Challan Online](https://vahan.parivahan.gov.in/challan)")
        st.markdown("- [Check E-Challan](https://echallan.parivahan.gov.in)")
        st.markdown("- [MoRTH Website](https://morth.nic.in)")
        st.markdown("- [Free Legal Aid (DLSA)](https://nalsa.gov.in)")

        st.divider()
        st.markdown(
            "<small>DriveLegal AI is for awareness only. "
            "For legal advice, consult a qualified advocate. "
            "Built for Road Safety Hackathon 2026.</small>",
            unsafe_allow_html=True,
        )


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
    return st.selectbox("🌐 Language", languages, key=key)


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

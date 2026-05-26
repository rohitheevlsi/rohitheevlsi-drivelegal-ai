# ─────────────────────────────────────────────────────────────────────────────
# DriveLegal AI | UI Styles
# All CSS injected via st.markdown — keeps app.py clean
# ─────────────────────────────────────────────────────────────────────────────

MAIN_CSS = """
<style>
/* ── Load Premium Typography ── */
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');

/* ── Custom Theme Variables (Harmonious & Sleek Dark Mode) ── */
:root {
  --primary:    #FF6B35;
  --secondary:  #0a0b1c;
  --accent:     #12132e;
  --success:    #00E676;
  --warning:    #FFD600;
  --danger:     #FF1744;
  --info:       #00E5FF;
  --text-light: #F5F6FA;
  --card-bg:    rgba(255, 255, 255, 0.03);
  --glass-bg:   rgba(10, 11, 28, 0.45);
  --border:     rgba(255, 107, 53, 0.15);
  --glow:       rgba(255, 107, 53, 0.4);
}

/* ── Global Styles ── */
* { 
  font-family: 'Plus Jakarta Sans', sans-serif; 
}
h1, h2, h3, .section-header, .hero-banner h1 {
  font-family: 'Outfit', sans-serif !important;
}

.stApp {
  background: radial-gradient(circle at 10% 20%, rgba(26, 20, 68, 0.25) 0%, rgba(13, 13, 30, 0.95) 90%),
              linear-gradient(135deg, #06060c 0%, #0d0f28 50%, #04040a 100%) !important;
  color: var(--text-light) !important;
}

.main .block-container { 
  padding-top: 1.5rem; 
  max-width: 1100px; 
}

/* ── Animated Traffic Light Glow (Aesthetic Hackathon WOW Factor) ── */
@keyframes traffic-glow {
  0%, 100% { filter: drop-shadow(0 0 8px rgba(255, 23, 68, 0.4)); }
  33% { filter: drop-shadow(0 0 12px rgba(255, 214, 0, 0.5)); }
  66% { filter: drop-shadow(0 0 8px rgba(0, 230, 118, 0.4)); }
}
.hero-banner h1 {
  animation: traffic-glow 6s infinite alternate;
}

/* ── Hero Banner (Premium Gradient Glassmorphism) ── */
.hero-banner {
  background: linear-gradient(135deg, rgba(255, 107, 53, 0.12) 0%, rgba(230, 57, 70, 0.05) 50%, rgba(10, 11, 28, 0.6) 100%);
  -webkit-backdrop-filter: blur(12px);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 107, 53, 0.25);
  border-radius: 20px;
  padding: 3rem 2rem;
  text-align: center;
  margin-bottom: 2rem;
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.35), inset 0 1px 1px rgba(255, 255, 255, 0.05);
  position: relative;
  overflow: hidden;
}
.hero-banner::after {
  content: '';
  position: absolute;
  top: -50%; left: -50%; width: 200%; height: 200%;
  background: radial-gradient(circle, rgba(255,107,53,0.06) 0%, transparent 60%);
  pointer-events: none;
}
.hero-banner h1 { 
  background: linear-gradient(135deg, #FFF 30%, #FF9E79 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  font-size: 2.8rem; 
  font-weight: 800; 
  margin: 0; 
  letter-spacing: -0.5px; 
}
.hero-banner p { 
  color: rgba(245, 246, 250, 0.75); 
  font-size: 1.1rem; 
  margin: 0.8rem 0 0; 
  font-weight: 300;
  letter-spacing: 0.5px;
}

/* ── Premium Stat Cards (Rise on Hover & Subtle Glow) ── */
.stat-row { 
  display: flex; 
  gap: 1.2rem; 
  margin-bottom: 2rem; 
  flex-wrap: wrap; 
}
.stat-card {
  flex: 1; 
  min-width: 160px;
  background: var(--card-bg);
  -webkit-backdrop-filter: blur(10px);
  backdrop-filter: blur(10px);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 1.2rem;
  text-align: center;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  box-shadow: 0 4px 15px rgba(0,0,0,0.15);
}
.stat-card:hover {
  transform: translateY(-5px);
  border-color: rgba(255, 107, 53, 0.4);
  box-shadow: 0 10px 25px rgba(255, 107, 53, 0.15), inset 0 1px 0 rgba(255,255,255,0.03);
}
.stat-card .num { 
  font-family: 'Outfit', sans-serif;
  font-size: 2.2rem; 
  font-weight: 700; 
  color: #FF7F50; 
  background: linear-gradient(135deg, #FF9E79 0%, #FF6B35 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
.stat-card .lbl { 
  font-size: 0.8rem; 
  color: rgba(245, 246, 250, 0.55); 
  margin-top: 4px; 
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* ── Elegant Section Headers (Glossy Gradient Accent) ── */
.section-header {
  background: linear-gradient(90deg, rgba(255, 107, 53, 0.22) 0%, rgba(230, 57, 70, 0.05) 70%, transparent 100%);
  border-left: 4px solid var(--primary);
  border-radius: 4px 12px 12px 4px;
  padding: 0.8rem 1.2rem;
  margin-top: 1.5rem;
  margin-bottom: 1.2rem;
  font-weight: 600;
  font-size: 1.15rem;
  color: #fff;
  letter-spacing: 0.5px;
  box-shadow: inset 1px 0 0 rgba(255,255,255,0.05);
}

/* ── Premium Glass Result Boxes ── */
.result-box {
  background: rgba(255, 255, 255, 0.02);
  -webkit-backdrop-filter: blur(10px);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 16px;
  padding: 1.5rem;
  margin: 1.2rem 0;
  color: var(--text-light);
  line-height: 1.7;
  font-size: 0.95rem;
  box-shadow: 0 8px 24px rgba(0,0,0,0.2);
  transition: all 0.3s ease;
}
.result-box:hover {
  border-color: rgba(255, 255, 255, 0.15);
  box-shadow: 0 12px 30px rgba(0,0,0,0.25);
}
.result-box.success { 
  border-color: rgba(0, 230, 118, 0.3); 
  background: rgba(0, 230, 118, 0.04); 
  box-shadow: 0 4px 20px rgba(0, 230, 118, 0.05);
}
.result-box.warning { 
  border-color: rgba(255, 214, 0, 0.3); 
  background: rgba(255, 214, 0, 0.03); 
  box-shadow: 0 4px 20px rgba(255, 214, 0, 0.04);
}
.result-box.danger  { 
  border-color: rgba(255, 23, 68, 0.3); 
  background: rgba(255, 23, 68, 0.04); 
  box-shadow: 0 4px 20px rgba(255, 23, 68, 0.05);
}
.result-box.info    { 
  border-color: rgba(0, 229, 255, 0.3); 
  background: rgba(0, 229, 255, 0.03); 
  box-shadow: 0 4px 20px rgba(0, 229, 255, 0.04);
}

/* ── Advanced Futuristic Chat Interface ── */
.chat-user {
  background: linear-gradient(135deg, #FF6B35 0%, #FF3D00 100%);
  color: #fff;
  padding: 0.85rem 1.2rem;
  border-radius: 18px 18px 4px 18px;
  margin: 0.8rem 0 0.8rem 15%;
  line-height: 1.6;
  font-size: 0.95rem;
  box-shadow: 0 4px 15px rgba(255, 61, 0, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.1);
}
.chat-bot {
  background: rgba(255, 255, 255, 0.03);
  -webkit-backdrop-filter: blur(10px);
  backdrop-filter: blur(10px);
  border: 1px solid var(--border);
  color: var(--text-light);
  padding: 0.85rem 1.2rem;
  border-radius: 18px 18px 18px 4px;
  margin: 0.8rem 15% 0.8rem 0;
  line-height: 1.6;
  font-size: 0.95rem;
  box-shadow: 0 4px 15px rgba(0,0,0,0.15);
}

/* ── Streamlit UI Widget Overrides (Futuristic Styling) ── */
/* Primary Buttons with a beautiful hover glow */
.stButton > button {
  background: linear-gradient(135deg, #FF6B35 0%, #E63946 50%, #7000FF 100%) !important;
  color: #fff !important;
  border: none !important;
  border-radius: 10px !important;
  font-family: 'Outfit', sans-serif !important;
  font-weight: 600 !important;
  padding: 0.6rem 1.8rem !important;
  letter-spacing: 0.5px !important;
  box-shadow: 0 4px 15px rgba(255, 107, 53, 0.25) !important;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
  width: auto !important;
}
.stButton > button:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 8px 25px rgba(255, 107, 53, 0.45) !important;
  opacity: 1 !important;
}
.stButton > button:active {
  transform: translateY(1px) !important;
}

/* Beautiful Inputs & Textareas */
.stSelectbox > div > div,
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stTextArea > div > div > textarea,
.stDateInput > div > div > input {
  background: rgba(255, 255, 255, 0.04) !important;
  color: var(--text-light) !important;
  border: 1px solid var(--border) !important;
  border-radius: 10px !important;
  transition: all 0.3s ease !important;
  padding: 0.4rem 0.8rem !important;
}
.stSelectbox > div > div:focus-within,
.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
  border-color: rgba(255, 107, 53, 0.5) !important;
  background: rgba(255, 255, 255, 0.06) !important;
  box-shadow: 0 0 10px rgba(255, 107, 53, 0.15) !important;
}

/* Stunning Navigation Tabs */
.stTabs [data-baseweb="tab"] {
  color: rgba(245, 246, 250, 0.45) !important;
  font-family: 'Outfit', sans-serif !important;
  font-weight: 500 !important;
  font-size: 0.95rem !important;
  transition: all 0.25s ease !important;
  padding: 0.6rem 1rem !important;
}
.stTabs [aria-selected="true"] {
  color: #FF7F50 !important;
  font-weight: 600 !important;
  border-bottom: 2px solid #FF6B35 !important;
}
.stTabs [data-baseweb="tab"]:hover {
  color: rgba(255, 127, 80, 0.85) !important;
}

/* Elegant Metric Display override */
div[data-testid="stMetric"] {
  background: rgba(255, 255, 255, 0.02) !important;
  -webkit-backdrop-filter: blur(10px) !important;
  backdrop-filter: blur(10px) !important;
  border: 1px solid rgba(255, 107, 53, 0.12) !important;
  border-radius: 16px !important;
  padding: 1rem 1.2rem !important;
  box-shadow: 0 4px 15px rgba(0,0,0,0.1) !important;
}
div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
  font-family: 'Outfit', sans-serif !important;
  color: #fff !important;
  font-size: 1.8rem !important;
}

/* ── Modern Premium Sidebar ── */
section[data-testid="stSidebar"] {
  background: #090a16 !important;
  border-right: 1px solid rgba(255, 107, 53, 0.12) !important;
}
section[data-testid="stSidebar"] * { 
  color: rgba(245, 246, 250, 0.85) !important; 
}
section[data-testid="stSidebar"] .stDivider {
  border-color: rgba(255, 107, 53, 0.1) !important;
}

/* ── Customized Scrollbar ── */
::-webkit-scrollbar { width: 8px; height: 8px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { 
  background: linear-gradient(180deg, #FF6B35, #E63946); 
  border-radius: 4px; 
}
::-webkit-scrollbar-thumb:hover { 
  background: linear-gradient(180deg, #FF9E79, #FF6B35); 
}

/* ── Alert boxes ── */
.stAlert {
  background-color: rgba(10, 11, 28, 0.6) !important;
  border: 1px solid rgba(255, 107, 53, 0.15) !important;
  border-radius: 14px !important;
}
</style>
"""

LETTER_CSS = """
<style>
/* ── Premium Printable Legal Document ── */
.letter-container {
  background: #ffffff;
  color: #1a1a1a;
  font-family: 'Times New Roman', Times, serif;
  padding: 3.5rem 3rem;
  border-radius: 6px;
  line-height: 1.8;
  font-size: 15px;
  white-space: pre-wrap;
  border: 1px solid #e0e0e0;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4), inset 0 0 40px rgba(0, 0, 0, 0.02);
  margin-top: 1.5rem;
  position: relative;
}
.letter-container::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0; height: 4px;
  background: linear-gradient(90deg, #FF6B35, #E63946);
  border-radius: 6px 6px 0 0;
}
</style>
"""

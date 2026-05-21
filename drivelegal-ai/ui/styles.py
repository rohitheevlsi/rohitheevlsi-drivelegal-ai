# ─────────────────────────────────────────────────────────────────────────────
# DriveLegal AI | UI Styles
# All CSS injected via st.markdown — keeps app.py clean
# ─────────────────────────────────────────────────────────────────────────────

MAIN_CSS = """
<style>
/* ── Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* ── Root variables ── */
:root {
  --primary:    #FF6B35;
  --secondary:  #1A1A2E;
  --accent:     #16213E;
  --success:    #28A745;
  --warning:    #FFC107;
  --danger:     #DC3545;
  --info:       #17A2B8;
  --text-light: #F8F9FA;
  --card-bg:    rgba(255,255,255,0.05);
  --border:     rgba(255,107,53,0.2);
}

/* ── Global ── */
* { font-family: 'Inter', sans-serif; }
.stApp { background: linear-gradient(135deg, #0D0D1A 0%, #1A1A2E 50%, #16213E 100%); }
.main .block-container { padding-top: 1rem; max-width: 1100px; }

/* ── Hero banner ── */
.hero-banner {
  background: linear-gradient(135deg, #FF6B35 0%, #E63946 40%, #1A1A2E 100%);
  border-radius: 16px;
  padding: 2.5rem 2rem;
  text-align: center;
  margin-bottom: 1.5rem;
  box-shadow: 0 8px 32px rgba(255,107,53,0.3);
}
.hero-banner h1 { color: #fff; font-size: 2.4rem; font-weight: 700; margin: 0; letter-spacing: -0.5px; }
.hero-banner p  { color: rgba(255,255,255,0.85); font-size: 1rem; margin: 0.5rem 0 0; }

/* ── Stat cards ── */
.stat-row { display: flex; gap: 1rem; margin-bottom: 1.5rem; flex-wrap: wrap; }
.stat-card {
  flex: 1; min-width: 140px;
  background: var(--card-bg);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 1rem;
  text-align: center;
}
.stat-card .num  { font-size: 1.8rem; font-weight: 700; color: var(--primary); }
.stat-card .lbl  { font-size: 0.75rem; color: rgba(255,255,255,0.6); margin-top: 2px; }

/* ── Section headers ── */
.section-header {
  background: linear-gradient(90deg, var(--primary), transparent);
  border-radius: 8px;
  padding: 0.6rem 1rem;
  margin-bottom: 1rem;
  font-weight: 600;
  font-size: 1rem;
  color: #fff;
}

/* ── Result boxes ── */
.result-box {
  background: var(--card-bg);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 1.2rem;
  margin: 0.8rem 0;
  color: var(--text-light);
  line-height: 1.7;
}
.result-box.success { border-color: var(--success); background: rgba(40,167,69,0.1); }
.result-box.warning { border-color: var(--warning); background: rgba(255,193,7,0.1); }
.result-box.danger  { border-color: var(--danger);  background: rgba(220,53,69,0.1); }
.result-box.info    { border-color: var(--info);    background: rgba(23,162,184,0.1); }

/* ── Chat bubbles ── */
.chat-user {
  background: linear-gradient(135deg, var(--primary), #E63946);
  color: #fff;
  padding: 0.75rem 1rem;
  border-radius: 16px 16px 4px 16px;
  margin: 0.5rem 0 0.5rem 20%;
  line-height: 1.6;
}
.chat-bot {
  background: var(--card-bg);
  border: 1px solid var(--border);
  color: var(--text-light);
  padding: 0.75rem 1rem;
  border-radius: 16px 16px 16px 4px;
  margin: 0.5rem 20% 0.5rem 0;
  line-height: 1.6;
}

/* ── Streamlit overrides ── */
.stButton > button {
  background: linear-gradient(135deg, var(--primary), #E63946) !important;
  color: #fff !important;
  border: none !important;
  border-radius: 8px !important;
  font-weight: 600 !important;
  padding: 0.5rem 1.5rem !important;
  transition: opacity 0.2s;
}
.stButton > button:hover { opacity: 0.9; }

.stSelectbox > div > div,
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stTextArea > div > div > textarea {
  background: rgba(255,255,255,0.07) !important;
  color: var(--text-light) !important;
  border: 1px solid var(--border) !important;
  border-radius: 8px !important;
}
.stTabs [data-baseweb="tab"] {
  color: rgba(255,255,255,0.6) !important;
  font-weight: 500;
}
.stTabs [aria-selected="true"] {
  color: var(--primary) !important;
  border-bottom-color: var(--primary) !important;
}
div[data-testid="stMetric"] {
  background: var(--card-bg);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 0.8rem;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
  background: var(--secondary) !important;
  border-right: 1px solid var(--border);
}
section[data-testid="stSidebar"] * { color: var(--text-light) !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--primary); border-radius: 3px; }

/* ── Spinner / progress ── */
.stProgress > div > div { background: var(--primary) !important; }

/* ── Alerts ── */
.stAlert { border-radius: 10px !important; }
</style>
"""

LETTER_CSS = """
<style>
.letter-container {
  background: #fff;
  color: #111;
  font-family: 'Times New Roman', serif;
  padding: 3rem;
  border-radius: 4px;
  line-height: 1.8;
  font-size: 15px;
  white-space: pre-wrap;
  border: 1px solid #ddd;
  margin-top: 1rem;
}
</style>
"""

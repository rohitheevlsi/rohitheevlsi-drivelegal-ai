# 🚦 DriveLegal AI
### India's AI-Powered Traffic Law Assistant
**Road Safety Hackathon 2026 · CoERS, IIT Madras × MoRTH**

[![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-FF6B35?logo=streamlit)](https://streamlit.io)
[![Claude AI](https://img.shields.io/badge/Powered%20by-Claude%20AI-blueviolet)](https://anthropic.com)
[![MV Act 2019](https://img.shields.io/badge/Data-MV%20Act%202019-green)](https://morth.nic.in)
[![Tests](https://img.shields.io/badge/Tests-26%20passing-brightgreen)](#testing)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 🎯 Problem Statement

Every year, millions of Indian drivers receive traffic challans — many of which are **overcharged, incorrectly issued, or legally disputable**. Most citizens:
- Don't know the exact legal fine amounts under MV Act 2019
- Don't know their constitutional rights when stopped by police
- Can't afford a lawyer to draft a dispute letter
- Are unaware of state-specific variations in traffic rules

**DriveLegal AI solves all of this in one free, multilingual app.**

---

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| 💬 **AI Chat** | Ask any traffic law question in 10+ Indian languages |
| 📋 **Challan Validator** | Upload challan photo — AI verifies if fine is legal |
| ✉️ **Dispute Letter Generator** | Auto-generates print-ready formal dispute letter |
| 💰 **Fine Calculator** | Exact legal fines for 30+ violations across 18 states |
| 🍺 **BAC Calculator** | Widmark-formula blood alcohol estimate with legal context |
| 📍 **Penalty Points Tracker** | Track licence demerit points, suspension threshold |
| 📄 **Document Checker** | Expiry alerts for DL, RC, Insurance, PUC, FC |
| 🗺️ **State Comparator** | Side-by-side rules comparison across any 2 states |
| ⚖️ **Know Your Rights** | What officers can/cannot do. Rights at checkpoints. |
| 🚗 **Speed Limits Guide** | Complete speed limit table by road type & vehicle |

---

## 🏗️ Project Structure

```
drivelegal-ai/
├── app.py                  # Main Streamlit app (tabs, layout, session state)
├── laws_data.py            # Traffic laws database (MV Act 2019 + 18 states)
├── ai/
│   ├── __init__.py
│   └── client.py           # Anthropic API calls with retry & error handling
├── ui/
│   ├── __init__.py
│   ├── styles.py           # All CSS (extracted from app for cleanliness)
│   └── components.py       # Reusable Streamlit UI components
├── utils/
│   ├── __init__.py
│   └── calculators.py      # BAC, fine, penalty points, doc checker (pure Python)
├── tests/
│   ├── __init__.py
│   └── test_calculators.py # 26 unit tests for all calculators
├── .streamlit/
│   ├── config.toml         # Dark theme, server config
│   └── secrets.toml        # API key (local dev only — DO NOT COMMIT)
├── requirements.txt
└── README.md
```

---

## 🚀 Quick Start

### 1. Clone & install
```bash
git clone https://github.com/rohitheevlsi/drivelegal-ai.git
cd drivelegal-ai
pip install -r requirements.txt
```

### 2. Add your API key
Edit `.streamlit/secrets.toml`:
```toml
ANTHROPIC_API_KEY = "sk-ant-your-key-here"
```
Get a free key at [console.anthropic.com](https://console.anthropic.com)

### 3. Run
```bash
streamlit run app.py
```
Open [http://localhost:8501](http://localhost:8501)

---

## ☁️ Deploy to Streamlit Cloud (Free — 10 minutes)

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io) → New app
3. Select your repo → `app.py`
4. **Settings → Secrets** → paste:
   ```toml
   ANTHROPIC_API_KEY = "sk-ant-your-key-here"
   ```
5. Click **Deploy** → get a public URL instantly

---

## 🧪 Testing

```bash
python -m pytest tests/ -v
```

**26 tests covering:**
- BAC calculator (Widmark formula accuracy, boundary conditions, edge cases)
- Fine calculator (state overrides, repeat offences, unknown violations)
- Penalty points (all thresholds, suspension logic)
- Document checker (grace periods, expiry detection, fine lookup)
- Speed limits (road type hierarchy, error handling)

All 26 tests pass ✅

---

## 🗄️ Data Sources

- **Motor Vehicles (Amendment) Act 2019** — Central legislation
- **State Transport Notifications** — 18 state-specific rules (Tamil Nadu, Delhi, Maharashtra, Karnataka, Gujarat, Kerala, Goa, and more)
- **CMVR (Central Motor Vehicles Rules)** — Technical standards
- **MoRTH circulars** — Updated fine schedules

Data is embedded in `laws_data.py` — no external database required, works offline for all non-AI features.

---

## 🌐 Multilingual Support

The AI Chat and Rights Advisor respond in:
English · Tamil · Hindi · Telugu · Kannada · Bengali · Marathi · Gujarati · Malayalam · Punjabi · Odia

---

## 🤖 AI Architecture

```
User Query
    │
    ▼
laws_data.py (system prompt + full MV Act 2019 DB)
    │
    ▼
ai/client.py (exponential backoff, error handling)
    │
    ▼
Anthropic Claude API (claude-opus-4-5)
    │
    ▼
Streamlit UI (streamed response)
```

Image analysis (challan validator) uses Claude's vision capability with base64-encoded uploads.

---

## 💡 Impact

- **30+ crore vehicle owners** in India can use this
- **No lawyer needed** — AI generates legally correct dispute letters
- **Stops corruption** — citizens know exact fine amounts, can reject overcharging
- **Saves lives** — BAC calculator discourages drunk driving
- **Accessible** — works on any device, 10+ languages, completely free

---

## 👨‍💻 Team

Built for **Road Safety Hackathon 2026** organised by CoERS, IIT Madras & MoRTH.

---

## 📜 License

MIT License — free to use, modify, and distribute.

---

## ⚠️ Disclaimer

DriveLegal AI is for awareness and educational purposes only. Fine amounts and rules are based on MV Act 2019 and may vary. For specific legal advice, consult a qualified advocate. BAC estimates are approximate — never drive after consuming alcohol.

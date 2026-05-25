---
title: DriveLegal AI
emoji: 🚦
colorFrom: red
colorTo: orange
sdk: streamlit
sdk_version: 1.35.0
app_file: app.py
pinned: false
---
# 🚦 DriveLegal AI
### India's AI-Powered Traffic Law Assistant
**Road Safety Hackathon 2026 · Track 1: DriveLegal · CoERS, IIT Madras × MoRTH**

[![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-FF6B35?logo=streamlit)](https://streamlit.io)
[![Claude AI](https://img.shields.io/badge/Powered%20by-Claude%20AI-blueviolet)](https://anthropic.com)
[![MV Act 2019](https://img.shields.io/badge/Data-MV%20Act%202019-green)](https://morth.nic.in)
[![Tests](https://img.shields.io/badge/Tests-26%20passing-brightgreen)](#testing)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Live Demo](https://img.shields.io/badge/Live-Demo-00B4D8)](https://drivelegal-ai.streamlit.app)

> **One free app that gives every Indian driver the legal superpower of a lawyer.**

---

## 🎯 The Problem

Every year, millions of Indian drivers receive traffic challans — many overcharged, incorrectly issued, or legally disputable. Citizens face four critical gaps:

| Gap | Reality |
|-----|---------|
| **Legal Ignorance** | Most drivers don't know exact fine amounts under MV Act 2019 |
| **State Confusion** | Fine amounts vary significantly across 18+ states |
| **No Recourse** | Can't afford a lawyer to draft a dispute letter |
| **Language Barrier** | Rules exist only in English/Hindi — rural India is left out |

India records **1.7 lakh road fatalities annually** — 84% caused by driver negligence. Legal awareness is road safety.

---

## ✨ Features (10 Tools in One App)

| # | Feature | What It Does |
|---|---------|--------------|
| 💬 | **AI Chat** | Ask any traffic law question in 10+ Indian languages |
| 📋 | **Challan Validator** | Upload challan photo — AI verifies if fine is legal |
| ✉️ | **Dispute Letter Generator** | Auto-generates print-ready formal dispute letter |
| 💰 | **Fine Calculator** | Exact legal fines for 30+ violations across 18 states |
| 🍺 | **BAC Calculator** | Widmark-formula blood alcohol estimate with legal context |
| 📍 | **Penalty Points Tracker** | Track licence demerit points, suspension threshold |
| 📄 | **Document Checker** | Expiry alerts for DL, RC, Insurance, PUC, FC |
| 🗺️ | **State Comparator** | Side-by-side rules comparison across any 2 states |
| ⚖️ | **Know Your Rights** | What officers can/cannot do at checkpoints |
| 🚗 | **Speed Limits Guide** | Complete speed limit table by road type & vehicle |

---

## 🏗️ Architecture

```
User Query (Any Device, Any Language)
         │
         ▼
  Streamlit UI (app.py)
         │
    ┌────┴────┐
    │         │
    ▼         ▼
laws_data.py   calculators.py
(MV Act 2019   (BAC, fines,
 18 states)     penalty pts)
    │
    ▼
ai/client.py
(exponential backoff,
 error handling)
    │
    ▼
Anthropic Claude API
(claude-opus-4-5 · Vision + Text)
    │
    ▼
Streamed Response → UI
```

**Key design decisions:**
- **Zero external database** — all 18-state data embedded in `laws_data.py`
- **Offline-first** — all calculators work without internet
- **Production-grade** — exponential backoff, retry logic, error handling
- **Vision-capable** — challan image analysis via base64 + Claude vision

---

## 🚀 Quick Start

### 1. Clone & install
```bash
git clone https://github.com/rohitheevlsi/rohitheevlsi-drivelegal-ai.git
cd rohitheevlsi-drivelegal-ai
pip install -r requirements.txt
```

### 2. Add your API key
Create `.streamlit/secrets.toml`:
```toml
ANTHROPIC_API_KEY = "sk-ant-your-key-here"
```
Get a free key at [console.anthropic.com](https://console.anthropic.com)

### 3. Run
```bash
streamlit run app.py
```
Open http://localhost:8501

---

## ☁️ Deploy to Streamlit Cloud (Free · 10 minutes)

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io) → **New app**
3. Select your repo → `app.py`
4. **Settings → Secrets** → paste:
```toml
ANTHROPIC_API_KEY = "sk-ant-your-key-here"
```
5. Click **Deploy** → instant public URL

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

| Source | Coverage |
|--------|----------|
| Motor Vehicles (Amendment) Act 2019 | Central legislation, all fine schedules |
| State Transport Notifications | 18 states: TN, Delhi, MH, KA, GJ, KL, Goa + more |
| CMVR (Central Motor Vehicles Rules) | Technical standards |
| MoRTH circulars | Updated fine schedules |

Data embedded in `laws_data.py` — no external database required. Works offline for all non-AI features.

---

## 🌐 Multilingual Support

AI Chat and Rights Advisor respond in:

**English · Tamil · Hindi · Telugu · Kannada · Bengali · Marathi · Gujarati · Malayalam · Punjabi · Odia**

---

## 📦 Software Packages Used

| Package | Version | Purpose |
|---------|---------|---------|
| streamlit | ≥1.32 | Web UI framework |
| anthropic | ≥0.25 | Claude AI API client |
| Pillow | ≥10.0 | Image processing for challan upload |
| pytest | ≥8.0 | Unit testing |

All dependencies in `requirements.txt`.

---

## 💡 Impact

- **30+ crore vehicle owners** in India can use this today
- **No lawyer needed** — AI generates legally correct dispute letters
- **Stops corruption** — citizens know exact fine amounts, can reject overcharging
- **Saves lives** — BAC calculator discourages drunk driving
- **Accessible** — works on any device, 10+ languages, completely free
- **Aligned with** Digital India · AI for All · Vision Zero 2030 · MoRTH Road Safety Goals

---

## 🗺️ Roadmap

| Phase | Status | Highlights |
|-------|--------|-----------|
| Hackathon MVP | ✅ Done | 10 features, 18 states, 26 tests |
| Post-Hackathon | ⚡ Next | WhatsApp bot, GPS state detection, UMANG integration |
| National Scale | 🎯 Vision | RTO API, DigiLocker, court e-filing, AI outcome predictor |

---

## 👨‍💻 About

Built for **Road Safety Hackathon 2026** organised by CoERS, IIT Madras & MoRTH.

---

## 📜 License

MIT License — free to use, modify, and distribute.

---

## ⚠️ Disclaimer

DriveLegal AI is for awareness and educational purposes only. Fine amounts and rules are based on MV Act 2019 and may vary by state and notification date. For specific legal advice, consult a qualified advocate. BAC estimates are approximate — never drive after consuming alcohol.

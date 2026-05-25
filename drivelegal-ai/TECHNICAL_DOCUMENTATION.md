# DriveLegal AI — Technical Documentation
### Road Safety Hackathon 2026 · Track 1: DriveLegal
**CoERS, IIT Madras × MoRTH**

---

## 1. Project Overview

DriveLegal AI is a free, multilingual AI-powered web application that helps Indian citizens understand traffic laws, validate challans, dispute wrongful fines, and know their legal rights. It is built on the Motor Vehicles (Amendment) Act 2019 and covers 18 Indian states.

The application directly addresses **Track 1 — DriveLegal: Simplifying Traffic Laws**, by:
- Creating a location-specific database of traffic laws (18 states)
- Integrating national, state, and local regulations into a single interface
- Using AI to improve legal compliance and citizen awareness

---

## 2. Software Packages & Dependencies

| Package | Version | License | Purpose |
|---------|---------|---------|---------|
| `streamlit` | ≥1.32.0 | Apache 2.0 | Web UI framework — multi-tab layout, session state, file uploader |
| `anthropic` | ≥0.25.0 | MIT | Official Claude AI Python SDK — text and vision inference |
| `Pillow` | ≥10.0.0 | HPND | Image preprocessing for challan photo upload (base64 encoding) |
| `pytest` | ≥8.0.0 | MIT | Unit testing framework — 26 tests across 5 modules |

**Full requirements.txt:**
```
streamlit>=1.32.0
anthropic>=0.25.0
Pillow>=10.0.0
pytest>=8.0.0
```

**Runtime:** Python 3.10+
**Deployment:** Streamlit Community Cloud (free tier)
**External APIs:** Anthropic Claude API (claude-opus-4-5)

---

## 3. Architecture

### 3.1 File Structure
```
rohitheevlsi-drivelegal-ai/
├── app.py              # Main Streamlit entry point (tabs, layout, session state)
├── laws_data.py        # Traffic law database (MV Act 2019 + 18 states)
├── client.py           # Anthropic API wrapper (retry logic, streaming)
├── calculators.py      # Pure Python calculators (BAC, fines, penalty pts)
├── components.py       # Reusable Streamlit UI components
├── styles.py           # CSS (dark theme, card layout)
├── config.toml         # Streamlit server configuration
├── requirements.txt    # Python dependencies
├── test_calculators.py # 26 unit tests
└── __init__.py
```

### 3.2 Data Flow
```
User Input
    │
    ├─ Text query → laws_data.py (system prompt context) → Claude API → Streamed response
    │
    ├─ Image upload (challan) → PIL base64 encode → Claude Vision API → Validation result
    │
    └─ Calculator input → calculators.py (pure Python) → Result (no API needed)
```

### 3.3 Key Design Decisions

**Zero-database architecture:** All 18-state traffic law data is embedded directly in `laws_data.py` as Python dictionaries. This enables offline operation for all non-AI features, eliminates database setup complexity, and makes deployment trivial.

**Offline-first calculators:** The BAC calculator (Widmark formula), fine calculator, penalty point tracker, document checker, and speed limit guide all run entirely in Python without any API calls. This ensures the app is useful even with no internet connection.

**Production-grade API client:** `client.py` implements exponential backoff retry logic, graceful error handling, and response streaming. This handles API rate limits and transient errors without crashing the user session.

**Vision-capable challan validation:** Challan photos are preprocessed using PIL, encoded to base64, and sent to Claude's vision endpoint. The AI cross-references the photo against the legal fine schedule in `laws_data.py` and identifies discrepancies.

---

## 4. Feature Implementation Details

### 4.1 AI Chat (Multilingual)
- System prompt includes full MV Act 2019 fine schedule and state-specific rules
- Language detection: user types in any of 11 languages; Claude responds in the same language
- Implemented as a streaming chat with session state for conversation history

### 4.2 Challan Validator
- User uploads photo (JPG/PNG)
- PIL converts to RGB, encodes to base64
- Sent to `claude-opus-4-5` vision endpoint
- Claude identifies: violation type, claimed amount, legal amount, discrepancy flag

### 4.3 Dispute Letter Generator
- Takes: violation type, location, date, officer name (optional), disputed amount
- Claude generates a formal letter citing specific MV Act sections
- Output is formatted for direct printing

### 4.4 Fine Calculator
- `calculators.py: calculate_fine(state, violation, repeat=False)`
- State lookup → base fine → state multiplier → repeat offence surcharge
- Returns: base amount, state amount, applicable section, notes

### 4.5 BAC Calculator
- Implements Widmark formula: BAC = (alcohol_grams) / (weight_kg × r × 10) − (0.015 × hours)
- r = 0.68 for male, 0.55 for female
- Legal limit context: 0.03% for commercial, 0.03% for private (MV Act 2019)

### 4.6 Penalty Points Tracker
- Maps violations to demerit points per CMVR schedule
- Tracks cumulative total; warns at 12 (caution), 15 (review), 18 (suspension)

### 4.7 Document Checker
- Takes expiry dates for DL, RC, Insurance, PUC, FC
- Calculates days remaining; applies 30-day warning threshold
- Maps expired documents to applicable fine under MV Act 2019

### 4.8 State Comparator
- Pulls data for two selected states from `laws_data.py`
- Renders side-by-side comparison table for any violation category

### 4.9 Know Your Rights
- Pre-loaded rights advisory (no AI needed for static content)
- Covers: what documents officers can demand, right to receipt, right against illegal detention

### 4.10 Speed Limits Guide
- Complete table: road type × vehicle category
- Sources: CMVR Rule 112, state notifications

---

## 5. Testing

**Framework:** pytest
**Test file:** `test_calculators.py`
**Total tests:** 26 (all passing ✅)

| Module | Tests | What's Covered |
|--------|-------|----------------|
| BAC Calculator | 8 | Widmark formula accuracy, gender factor, edge cases (0 drinks, very high intake) |
| Fine Calculator | 6 | Base fine lookup, state override, repeat offence multiplier, unknown violation |
| Penalty Points | 5 | All threshold levels, cumulative logic, suspension trigger |
| Document Checker | 5 | Grace period detection, expired state, fine mapping, multi-doc expiry |
| Speed Limits | 2 | Road type hierarchy, invalid input handling |

**Run tests:**
```bash
python -m pytest test_calculators.py -v
```

---

## 6. Data Sources & Legal Basis

| Data | Source | Notes |
|------|--------|-------|
| Central fine schedule | Motor Vehicles (Amendment) Act 2019 | Sections 177–210 |
| State multipliers | State Transport Department notifications | 18 states verified |
| Speed limits | CMVR Rule 112 | Updated per 2023 amendment |
| Demerit points | CMVR Schedule XIV | Draft rules reference |
| BAC limits | MV Act 2019 Section 185 | 30mg/100ml blood |

---

## 7. Technical Assumptions

1. **Fine data currency:** State-specific fine amounts are based on notifications available as of early 2026. MoRTH may update schedules; a production deployment would sync from an official API.
2. **BAC formula:** The Widmark formula provides a population-average estimate. Individual metabolism varies. The app explicitly disclaims this.
3. **Language detection:** The app relies on Claude to detect and respond in the user's language. Accuracy is high for the 11 supported languages but may vary for mixed-language inputs.
4. **Image quality:** Challan validation accuracy depends on photo quality. Blurry or partially visible challans may not be validated correctly.
5. **Offline mode:** AI-dependent features (Chat, Challan Validator, Dispute Letter) require an active internet connection. All calculator features work offline.

---

## 8. Deployment

**Platform:** Streamlit Community Cloud
**URL:** https://drivelegal-ai.streamlit.app
**Cost:** Free
**Setup time:** ~10 minutes

Steps:
1. Push repo to GitHub (public)
2. Go to share.streamlit.io → New app
3. Select repo, set main file to `app.py`
4. Add `ANTHROPIC_API_KEY` in Settings → Secrets
5. Deploy

---

## 9. Future Roadmap

**Phase 2 (Post-Hackathon):**
- WhatsApp chatbot via Twilio/Meta Business API
- GPS-based automatic state detection
- Real-time sync with MoRTH official fine database
- Android APK via Kivy/BeeWare
- UMANG super-app integration

**Phase 3 (National Scale):**
- RTO database API integration for RC/DL verification
- DigiLocker integration for document storage
- Court e-filing module for formal disputes
- AI-powered court outcome predictor based on case history

---

*Documentation prepared for Road Safety Hackathon 2026 submission.*
*Final submission deadline: 31 May 2026*

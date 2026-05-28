# ─────────────────────────────────────────────────────────────────────────────
# DriveLegal AI | Utilities
# Pure-Python helpers: BAC calc, fine calc, penalty points, doc checker
# ─────────────────────────────────────────────────────────────────────────────
from __future__ import annotations
from dataclasses import dataclass
from datetime import date, timedelta


# ── BAC Calculator ───────────────────────────────────────────────────────────

WIDMARK_FACTORS = {"Male": 0.68, "Female": 0.55}
INDIA_BAC_LIMIT_MG = 30          # mg per 100 ml blood
ELIMINATION_RATE = 0.015          # % BAC per hour (average)


@dataclass
class BACResult:
    bac_percent: float            # e.g. 0.05 = 0.05%
    bac_mg_per_100ml: float       # e.g. 50 mg/100ml
    is_over_limit: bool
    hours_to_legal: float         # hours until BAC drops below India limit
    risk_level: str               # "Safe" / "Borderline" / "Over Limit" / "Dangerous"
    disclaimer: str


def calculate_bac(
    weight_kg: float,
    gender: str,          # "Male" or "Female"
    drinks: float,        # standard drinks consumed
    hours_since_start: float,
    ml_per_drink: float = 30,
    abv_percent: float = 40.0,
) -> BACResult:
    """
    Widmark formula BAC estimate.
    bac = (alcohol_grams / (weight_kg * r)) - (elimination_rate * hours)
    """
    if weight_kg <= 0 or drinks < 0 or hours_since_start < 0:
        raise ValueError("Weight, drinks, and hours must be non-negative.")

    r = WIDMARK_FACTORS.get(gender, 0.68)
    alcohol_ml = drinks * ml_per_drink * (abv_percent / 100)
    alcohol_grams = alcohol_ml * 0.789          # ethanol density

    bac_raw = (alcohol_grams / (weight_kg * r * 10)) - (ELIMINATION_RATE * hours_since_start)
    bac_percent = max(0.0, round(bac_raw, 4))
    bac_mg = round(bac_percent * 1000, 2)       # % → mg/100ml  (0.03% = 30 mg)

    is_over = bac_mg > INDIA_BAC_LIMIT_MG

    if bac_mg > INDIA_BAC_LIMIT_MG:
        excess = bac_percent - (INDIA_BAC_LIMIT_MG / 1000)
        hours_to_legal = round(excess / ELIMINATION_RATE, 1)
    else:
        hours_to_legal = 0.0

    if bac_mg == 0:
        risk = "Safe"
    elif bac_mg <= 20:
        risk = "Low (likely safe)"
    elif bac_mg <= 30:
        risk = "Borderline — do not drive"
    elif bac_mg <= 60:
        risk = "Over Limit 🚨"
    else:
        risk = "Dangerously High 🚨🚨"

    disclaimer = (
        "⚠️ DISCLAIMER: This is a rough Widmark-formula estimate. "
        "Actual BAC varies with food, metabolism, medications, liver health, and more. "
        "If you've consumed alcohol, DO NOT DRIVE. Call a cab or wait. "
        "This tool is for awareness only — not a substitute for a breathalyser."
    )
    return BACResult(bac_percent, bac_mg, is_over, hours_to_legal, risk, disclaimer)


# ── Fine Calculator ───────────────────────────────────────────────────────────

from laws_data import TRAFFIC_LAWS_DB


def calculate_fine(violation_key: str, is_repeat: bool, state: str) -> dict:
    """
    Return fine details for a given violation + state.
    State-specific overrides applied where available.
    """
    laws = TRAFFIC_LAWS_DB["national_mv_act_2019"]
    if violation_key not in laws:
        return {"error": f"Violation '{violation_key}' not found in database."}

    law = laws[violation_key]
    base_fine = law["fine_repeat"] if is_repeat else law["fine_first"]

    # State override
    state_data = TRAFFIC_LAWS_DB["states"].get(state, {})
    state_rules = state_data.get("specific_rules", {})
    # Map violation_key to state rule key (best effort)
    state_key_map = {
        "drunk_driving": "drunk_driving", "no_helmet": "no_helmet",
        "mobile_driving": "mobile", "red_light": "red_light",
        "overspeeding_light": "overspeeding", "parking_violation": "parking",
    }
    mapped_key = state_key_map.get(violation_key)
    state_fine = None
    state_note = None
    if mapped_key and mapped_key in state_rules:
        state_fine = state_rules[mapped_key].get("fine")
        state_note = state_rules[mapped_key].get("note")

    multiplier = state_data.get("fine_multiplier", 1.0)
    effective_fine = state_fine if state_fine else int(base_fine * multiplier)

    return {
        "violation": law["violation"],
        "section": law["section"],
        "act": law["act"],
        "base_fine": base_fine,
        "effective_fine": effective_fine,
        "state": state,
        "state_note": state_note,
        "punishment": law["punishment"],
        "licence_points": law.get("licence_points", 0),
        "is_repeat": is_repeat,
        "multiplier": multiplier,
    }


# ── Penalty Points Tracker ────────────────────────────────────────────────────

@dataclass
class PenaltyStatus:
    total_points: int
    status: str
    color: str
    message: str
    points_to_suspension: int


def get_penalty_status(total_points: int) -> PenaltyStatus:
    pp = TRAFFIC_LAWS_DB["penalty_points"]
    threshold = pp["suspension_threshold"]
    levels = pp["levels"]

    if total_points <= 4:
        lvl = levels["0-4"]
    elif total_points <= 8:
        lvl = levels["5-8"]
    elif total_points <= 11:
        lvl = levels["9-11"]
    else:
        lvl = levels["12+"]

    pts_to_suspension = max(0, threshold - total_points)
    return PenaltyStatus(total_points, lvl["status"], lvl["color"], lvl["message"], pts_to_suspension)


# ── Document Expiry Checker ───────────────────────────────────────────────────

DOC_VALIDITY = TRAFFIC_LAWS_DB["document_validity"]

DOC_GRACE_DAYS = {
    "driving_licence": 30,
    "vehicle_registration_rc": 0,
    "insurance": 0,
    "puc_certificate": 0,
    "fitness_certificate": 0,
}


@dataclass
class DocStatus:
    doc_name: str
    expiry_date: date
    days_remaining: int
    is_expired: bool
    in_grace: bool
    fine_if_caught: int
    section: str
    advice: str


def check_document(doc_key: str, expiry_date: date) -> DocStatus:
    if doc_key not in DOC_VALIDITY:
        raise ValueError(f"Unknown document type: {doc_key}")

    doc = DOC_VALIDITY[doc_key]
    today = date.today()
    days_remaining = (expiry_date - today).days
    grace = DOC_GRACE_DAYS.get(doc_key, 0)

    is_expired = days_remaining < 0
    in_grace = is_expired and abs(days_remaining) <= grace

    if not is_expired:
        if days_remaining <= 30:
            advice = f"⚠️ Expiring soon! Renew within {days_remaining} days."
        else:
            advice = f"✅ Valid for {days_remaining} more days."
    elif in_grace:
        advice = f"⏳ Expired {abs(days_remaining)} days ago. Still within {grace}-day grace period — renew immediately."
    else:
        advice = f"🚨 EXPIRED {abs(days_remaining)} days ago. Renew immediately — fine: ₹{doc['fine_expired']} under {doc['section']}."

    return DocStatus(
        doc_name=doc_key.replace("_", " ").title(),
        expiry_date=expiry_date,
        days_remaining=days_remaining,
        is_expired=is_expired,
        in_grace=in_grace,
        fine_if_caught=doc["fine_expired"],
        section=doc["section"],
        advice=advice,
    )


# ── Speed Limit Lookup ────────────────────────────────────────────────────────

ROAD_TYPE_LABELS = {
    "expressway": "Expressway / Highway (120 zone)",
    "national_highway": "National Highway",
    "state_highway": "State Highway",
    "city_road": "City / Urban Road",
    "residential": "Residential Area",
    "mountain_ghat": "Mountain / Ghat Road",
}


def get_speed_limits(road_type: str) -> dict:
    limits = TRAFFIC_LAWS_DB["speed_limits"]
    if road_type not in limits:
        return {"error": f"Road type '{road_type}' not found."}
    return {**limits[road_type], "road_type": ROAD_TYPE_LABELS.get(road_type, road_type)}

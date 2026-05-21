# ─────────────────────────────────────────────────────────────────────────────
# DriveLegal AI | Tests
# Run: python -m pytest tests/ -v
# ─────────────────────────────────────────────────────────────────────────────
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from datetime import date, timedelta
from utils.calculators import (
    calculate_bac, BACResult,
    calculate_fine,
    get_penalty_status,
    check_document,
    get_speed_limits,
)


# ── BAC Calculator Tests ──────────────────────────────────────────────────────

class TestBACCalculator:

    def test_zero_drinks_is_safe(self):
        result = calculate_bac(70, "Male", 0, 0)
        assert result.bac_percent == 0.0
        assert not result.is_over_limit
        assert result.hours_to_legal == 0.0

    def test_over_limit_detected(self):
        # 5 drinks, 70kg male, 0 hours elapsed → well over limit
        result = calculate_bac(70, "Male", 5, 0)
        assert result.is_over_limit
        assert result.bac_mg_per_100ml > 30

    def test_female_higher_bac(self):
        # Women have lower Widmark r-factor → higher BAC for same intake
        male = calculate_bac(70, "Male", 3, 0)
        female = calculate_bac(70, "Female", 3, 0)
        assert female.bac_percent > male.bac_percent

    def test_time_reduces_bac(self):
        early = calculate_bac(70, "Male", 2, 0)
        later = calculate_bac(70, "Male", 2, 4)
        assert later.bac_percent <= early.bac_percent

    def test_bac_never_negative(self):
        result = calculate_bac(70, "Male", 1, 48)  # 48 hours later
        assert result.bac_percent >= 0.0

    def test_invalid_weight_raises(self):
        with pytest.raises(ValueError):
            calculate_bac(-1, "Male", 2, 0)

    def test_hours_to_legal_positive_when_over(self):
        result = calculate_bac(60, "Female", 4, 0)
        if result.is_over_limit:
            assert result.hours_to_legal > 0

    def test_india_bac_limit_boundary(self):
        # 30 mg/100ml = 0.03% BAC
        result = calculate_bac(80, "Male", 1, 1)
        # Just check it returns a proper dataclass
        assert isinstance(result, BACResult)
        assert result.disclaimer != ""


# ── Fine Calculator Tests ─────────────────────────────────────────────────────

class TestFineCalculator:

    def test_known_violation_returns_dict(self):
        result = calculate_fine("no_helmet", False, "Tamil Nadu")
        assert "effective_fine" in result
        assert result["effective_fine"] > 0

    def test_repeat_fine_gte_first(self):
        first = calculate_fine("drunk_driving", False, "Maharashtra")
        repeat = calculate_fine("drunk_driving", True, "Maharashtra")
        assert repeat["effective_fine"] >= first["effective_fine"]

    def test_unknown_violation_returns_error(self):
        result = calculate_fine("flying_car", False, "Delhi")
        assert "error" in result

    def test_section_present(self):
        result = calculate_fine("mobile_driving", False, "Karnataka")
        assert "section" in result
        assert result["section"] != ""

    def test_state_override_gujarat_drunk_driving(self):
        result = calculate_fine("drunk_driving", False, "Gujarat")
        # Gujarat has much higher DUI fine
        assert result["effective_fine"] >= 10000

    def test_licence_points_present(self):
        result = calculate_fine("dangerous_driving", False, "Kerala")
        assert "licence_points" in result
        assert result["licence_points"] >= 0

    def test_delhi_multiplier(self):
        base = calculate_fine("red_light", False, "Maharashtra")
        delhi = calculate_fine("red_light", False, "Delhi")
        # Delhi has 1.5x multiplier or state-specific override
        assert delhi["effective_fine"] >= base["effective_fine"]


# ── Penalty Points Tests ──────────────────────────────────────────────────────

class TestPenaltyPoints:

    def test_zero_points_safe(self):
        status = get_penalty_status(0)
        assert status.status == "Safe Driver"

    def test_twelve_points_suspended(self):
        status = get_penalty_status(12)
        assert "SUSPENDED" in status.status

    def test_high_points_warning(self):
        status = get_penalty_status(9)
        assert "High Risk" in status.status

    def test_points_to_suspension_calculated(self):
        status = get_penalty_status(8)
        assert status.points_to_suspension == 4

    def test_over_suspension_threshold(self):
        status = get_penalty_status(15)
        assert status.points_to_suspension == 0

    def test_caution_zone(self):
        status = get_penalty_status(6)
        assert "Caution" in status.status


# ── Document Checker Tests ────────────────────────────────────────────────────

class TestDocumentChecker:

    def test_valid_document(self):
        future = date.today() + timedelta(days=60)
        result = check_document("driving_licence", future)
        assert not result.is_expired
        assert result.days_remaining > 0

    def test_expired_document(self):
        past = date.today() - timedelta(days=40)
        result = check_document("driving_licence", past)
        assert result.is_expired

    def test_dl_grace_period(self):
        # DL has 30-day grace period
        just_expired = date.today() - timedelta(days=15)
        result = check_document("driving_licence", just_expired)
        assert result.in_grace

    def test_insurance_no_grace(self):
        just_expired = date.today() - timedelta(days=1)
        result = check_document("insurance", just_expired)
        assert result.is_expired
        assert not result.in_grace   # insurance has 0 grace days

    def test_expiring_soon_advice(self):
        soon = date.today() + timedelta(days=15)
        result = check_document("puc_certificate", soon)
        assert "⚠️" in result.advice

    def test_unknown_doc_raises(self):
        with pytest.raises(ValueError):
            check_document("magic_document", date.today())

    def test_fine_populated(self):
        past = date.today() - timedelta(days=100)
        result = check_document("no_pollution", past) if False else check_document("puc_certificate", past)
        assert result.fine_if_caught > 0


# ── Speed Limit Tests ─────────────────────────────────────────────────────────

class TestSpeedLimits:

    def test_expressway_car_limit(self):
        result = get_speed_limits("expressway")
        assert result["car_jeep"] == 120

    def test_city_road_lower_limit(self):
        city = get_speed_limits("city_road")
        express = get_speed_limits("expressway")
        assert city["car_jeep"] < express["car_jeep"]

    def test_unknown_road_returns_error(self):
        result = get_speed_limits("moon_highway")
        assert "error" in result

    def test_truck_slower_than_car(self):
        result = get_speed_limits("national_highway")
        assert result["bus_truck"] <= result["car_jeep"]

    def test_mountain_strictest(self):
        mountain = get_speed_limits("mountain_ghat")
        city = get_speed_limits("city_road")
        assert mountain["car_jeep"] <= city["car_jeep"]

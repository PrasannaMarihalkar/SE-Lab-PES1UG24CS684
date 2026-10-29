import pytest
from food_delivery import delivery_charge, apply_coupon, estimated_time


# =====================================================================
# Tests for delivery_charge(distance_km, order_value, is_raining)
# =====================================================================

def test_delivery_charge_invalid_distance_zero():
    """Line 5-6: Test non-positive distance raises ValueError."""
    with pytest.raises(ValueError, match="out of delivery range"):
        delivery_charge(0, 100, False)


def test_delivery_charge_invalid_distance_negative():
    """Line 5-6: Test negative distance raises ValueError."""
    with pytest.raises(ValueError, match="out of delivery range"):
        delivery_charge(-1, 250, False)


def test_delivery_charge_invalid_distance_too_large():
    """Line 5-6: Test distance > 15 km raises ValueError."""
    with pytest.raises(ValueError, match="out of delivery range"):
        delivery_charge(15.1, 300, False)


def test_delivery_charge_free_delivery():
    """Line 7-8: Test free delivery when order_value >= 500."""
    # Distance within valid range, rain False
    assert delivery_charge(5, 500, False) == 0
    # Free delivery with rain surcharge (0 + 30)
    assert delivery_charge(10, 600, True) == 30


def test_delivery_charge_tier_up_to_3km():
    """Line 9-10: Test tier 1 (distance <= 3 km) with order < 500."""
    assert delivery_charge(3, 400, False) == 20
    assert delivery_charge(0.5, 100, True) == 50  # 20 + 30


def test_delivery_charge_tier_up_to_8km():
    """Line 11-12: Test tier 2 (3 < distance <= 8 km) with order < 500."""
    assert delivery_charge(8, 499, False) == 40
    assert delivery_charge(5, 200, True) == 70  # 40 + 30


def test_delivery_charge_tier_above_8km():
    """Line 13-14: Test tier 3 (8 < distance <= 15 km) with order < 500."""
    assert delivery_charge(15, 300, False) == 60
    assert delivery_charge(12, 100, True) == 90  # 60 + 30


# =====================================================================
# Tests for apply_coupon(order_value, code, is_first_order)
# =====================================================================

def test_apply_coupon_none():
    """Line 21-22: Test when code is None returns order_value."""
    assert apply_coupon(350, None, False) == 350


def test_apply_coupon_invalid_code():
    """Line 23-24: Test invalid coupon raises ValueError."""
    with pytest.raises(ValueError, match="invalid coupon"):
        apply_coupon(300, "DISCOUNT50", False)


def test_apply_coupon_welcome_not_first_order():
    """Line 25-26: Test WELCOME coupon on repeat order raises ValueError."""
    with pytest.raises(ValueError, match="coupon only for first order"):
        apply_coupon(300, "WELCOME", False)


def test_apply_coupon_below_minimum_order_value():
    """Line 27-28: Test coupon applied to order < 200 returns original value."""
    assert apply_coupon(150, "SAVE50", False) == 150
    assert apply_coupon(199, "WELCOME", True) == 199


def test_apply_coupon_valid_save50():
    """Line 29: Test valid SAVE50 discount applied for order >= 200."""
    assert apply_coupon(200, "SAVE50", False) == 150
    assert apply_coupon(400, "SAVE50", True) == 350


def test_apply_coupon_valid_welcome_first_order():
    """Line 29: Test valid WELCOME discount applied for eligible first order."""
    assert apply_coupon(200, "WELCOME", True) == 100
    assert apply_coupon(500, "WELCOME", True) == 400


# =====================================================================
# Tests for estimated_time(distance_km, is_peak_hour, restaurant_busy)
# =====================================================================

def test_estimated_time_normal():
    """Line 33: Base time without peak hour or busy restaurant."""
    # 15 + 5 * 4 = 35
    assert estimated_time(5, False, False) == 35


def test_estimated_time_peak_hour_only():
    """Line 34-35: Peak hour adds 10 minutes."""
    # 15 + 5 * 4 + 10 = 45
    assert estimated_time(5, True, False) == 45


def test_estimated_time_restaurant_busy_only():
    """Line 36-37: Restaurant busy adds 15 minutes (non-peak)."""
    # 15 + 5 * 4 + 15 = 50
    assert estimated_time(5, False, True) == 50


def test_estimated_time_peak_and_restaurant_busy():
    """Line 38-39: Both peak hour and busy restaurant adds 10 + 15 + 5 = 30."""
    # 15 + 5 * 4 + 10 + 15 + 5 = 65
    assert estimated_time(5, True, True) == 65

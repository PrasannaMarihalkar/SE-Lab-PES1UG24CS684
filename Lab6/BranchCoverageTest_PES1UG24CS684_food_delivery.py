import pytest
from food_delivery import delivery_charge, apply_coupon, estimated_time


# =====================================================================
# Decision / Branch Coverage for delivery_charge(distance_km, order_value, is_raining)
# Decision 1: if distance_km <= 0 or distance_km > 15
#   - distance_km <= 0 (True) -> raises ValueError
#   - distance_km > 15 (True) -> raises ValueError
#   - distance_km in (0, 15] (False for both conditions) -> proceeds
# Decision 2: if order_value >= 500
#   - True -> charge = 0
#   - False -> checks elif distance_km <= 3
# Decision 3: elif distance_km <= 3
#   - True -> charge = 20
#   - False -> checks elif distance_km <= 8
# Decision 4: elif distance_km <= 8
#   - True -> charge = 40
#   - False -> charge = 60
# Decision 5: if is_raining
#   - True -> charge += 30
#   - False -> charge unchanged
# =====================================================================

@pytest.mark.parametrize("distance", [0, -0.1, -10])
def test_delivery_charge_distance_non_positive_branch(distance):
    """Branch: distance_km <= 0 evaluates to True."""
    with pytest.raises(ValueError, match="out of delivery range"):
        delivery_charge(distance, 200, False)


@pytest.mark.parametrize("distance", [15.01, 20, 100])
def test_delivery_charge_distance_above_15_branch(distance):
    """Branch: distance_km > 15 evaluates to True."""
    with pytest.raises(ValueError, match="out of delivery range"):
        delivery_charge(distance, 200, False)


def test_delivery_charge_free_delivery_branch_rain_false():
    """Branch: order_value >= 500 is True, is_raining is False."""
    assert delivery_charge(5, 500, False) == 0


def test_delivery_charge_free_delivery_branch_rain_true():
    """Branch: order_value >= 500 is True, is_raining is True."""
    assert delivery_charge(5, 500, True) == 30


def test_delivery_charge_tier_under_3km_rain_false():
    """Branch: order < 500 (False), distance <= 3 (True), is_raining False."""
    assert delivery_charge(3, 499, False) == 20


def test_delivery_charge_tier_under_3km_rain_true():
    """Branch: order < 500 (False), distance <= 3 (True), is_raining True."""
    assert delivery_charge(0.1, 100, True) == 50


def test_delivery_charge_tier_3_to_8km_rain_false():
    """Branch: order < 500, distance > 3 (False), distance <= 8 (True), rain False."""
    assert delivery_charge(8, 250, False) == 40


def test_delivery_charge_tier_3_to_8km_rain_true():
    """Branch: order < 500, distance > 3, distance <= 8, rain True."""
    assert delivery_charge(3.1, 250, True) == 70


def test_delivery_charge_tier_above_8km_rain_false():
    """Branch: order < 500, distance > 8 (False), rain False."""
    assert delivery_charge(15, 250, False) == 60


def test_delivery_charge_tier_above_8km_rain_true():
    """Branch: order < 500, distance > 8, rain True."""
    assert delivery_charge(8.1, 250, True) == 90


# =====================================================================
# Decision / Branch Coverage for apply_coupon(order_value, code, is_first_order)
# Decision 1: if code is None
#   - True -> return order_value
#   - False -> proceed
# Decision 2: if code not in COUPONS
#   - True -> raises ValueError("invalid coupon")
#   - False -> proceed
# Decision 3: if code == "WELCOME" and not is_first_order
#   - code == "WELCOME" and is_first_order == False -> True (raises ValueError)
#   - code == "WELCOME" and is_first_order == True  -> False
#   - code != "WELCOME" (e.g. "SAVE50")            -> False (short-circuits)
# Decision 4: if order_value < 200
#   - True -> return order_value
#   - False -> return order_value - COUPONS[code]
# =====================================================================

def test_apply_coupon_none_branch():
    """Branch: code is None evaluates to True."""
    assert apply_coupon(300, None, False) == 300
    assert apply_coupon(100, None, True) == 100


def test_apply_coupon_invalid_code_branch():
    """Branch: code not in COUPONS evaluates to True."""
    with pytest.raises(ValueError, match="invalid coupon"):
        apply_coupon(300, "EXPIRED100", True)


def test_apply_coupon_welcome_repeat_order_branch():
    """Branch: code == 'WELCOME' and not is_first_order evaluates to True."""
    with pytest.raises(ValueError, match="coupon only for first order"):
        apply_coupon(400, "WELCOME", is_first_order=False)


def test_apply_coupon_welcome_first_order_eligible_branch():
    """Branch: code == 'WELCOME', is_first_order=True, order_value >= 200."""
    assert apply_coupon(200, "WELCOME", is_first_order=True) == 100
    assert apply_coupon(350, "WELCOME", is_first_order=True) == 250


def test_apply_coupon_welcome_first_order_below_min_value_branch():
    """Branch: code == 'WELCOME', is_first_order=True, order_value < 200 (True)."""
    assert apply_coupon(199, "WELCOME", is_first_order=True) == 199


def test_apply_coupon_save50_eligible_branch():
    """Branch: code == 'SAVE50' (code != 'WELCOME' evaluates to False), order >= 200."""
    assert apply_coupon(200, "SAVE50", is_first_order=False) == 150
    assert apply_coupon(500, "SAVE50", is_first_order=True) == 450


def test_apply_coupon_save50_below_min_value_branch():
    """Branch: code == 'SAVE50', order_value < 200 (True)."""
    assert apply_coupon(150, "SAVE50", is_first_order=False) == 150


# =====================================================================
# Decision / Branch Coverage for estimated_time(distance_km, is_peak_hour, restaurant_busy)
# Decision 1: if is_peak_hour
#   - True -> minutes += 10
#   - False -> skip
# Decision 2: if restaurant_busy
#   - True -> minutes += 15, then check nested Decision 3
#   - False -> skip
# Decision 3 (nested): if is_peak_hour (inside restaurant_busy)
#   - True -> minutes += 5
#   - False -> skip
# Matrix of all 4 combinations:
#   1. (False, False): No peak, not busy
#   2. (True, False): Peak only, not busy
#   3. (False, True): Not peak, restaurant busy (exercises nested False branch)
#   4. (True, True): Peak AND restaurant busy (exercises nested True branch)
# =====================================================================

def test_estimated_time_combination_neither():
    """Peak: False, Busy: False."""
    # 15 + 10 * 4 = 55
    assert estimated_time(10, is_peak_hour=False, restaurant_busy=False) == 55


def test_estimated_time_combination_peak_only():
    """Peak: True, Busy: False."""
    # 15 + 10 * 4 + 10 = 65
    assert estimated_time(10, is_peak_hour=True, restaurant_busy=False) == 65


def test_estimated_time_combination_busy_only():
    """Peak: False, Busy: True (Crucial for nested False branch: restaurant_busy=True and is_peak_hour=False)."""
    # 15 + 10 * 4 + 15 = 70
    assert estimated_time(10, is_peak_hour=False, restaurant_busy=True) == 70


def test_estimated_time_combination_both_peak_and_busy():
    """Peak: True, Busy: True (Nested True branch: restaurant_busy=True and is_peak_hour=True)."""
    # 15 + 10 * 4 + 10 + 15 + 5 = 85
    assert estimated_time(10, is_peak_hour=True, restaurant_busy=True) == 85

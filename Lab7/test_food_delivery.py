import math
import pytest
from hypothesis import given, settings, example, strategies as st
from food_delivery import parse_order, delivery_eta, coupon_discount

# ============================================================================
# A. Tests for parse_order(items_csv)
# ============================================================================

valid_item_name = st.text(
    alphabet=st.characters(categories=["L", "N"], blacklist_characters=":, \t\r\n"),
    min_size=1,
    max_size=20
)
valid_qty = st.integers(min_value=1, max_value=100)

@settings(max_examples=200, deadline=None)
@given(st.dictionaries(keys=valid_item_name, values=valid_qty, min_size=1, max_size=10))
def test_parse_order_valid_generated(order_dict):
    """Hypothesis generates valid order dictionaries serialized as CSV;
    parsing must reconstruct the exact expected dictionary."""
    csv_str = ",".join(f"{k}:{v}" for k, v in order_dict.items())
    result = parse_order(csv_str)
    assert result == order_dict
    assert isinstance(result, dict)


@settings(max_examples=200, deadline=None)
@given(st.dictionaries(keys=valid_item_name, values=valid_qty, min_size=1, max_size=5))
def test_parse_order_whitespace_handling(order_dict):
    """Whitespace around item names and quantities must be properly stripped."""
    csv_str = ",".join(f"  {k}  :  {v}  " for k, v in order_dict.items())
    result = parse_order(csv_str)
    assert result == order_dict


@settings(max_examples=200, deadline=None)
@given(st.text() | st.none())
@example("")
@example(None)
@example("   ")
@example("pizza")
@example("pizza:")
@example(":2")
@example("pizza:abc")
@example("pizza:-1")
@example("pizza:0")
@example("pizza:2:extra")
@example("pizza:2,,burger:1")
@example("pizza:1,pizza:2")
@example("🍕:2")
def test_parse_order_no_crash(s):
    """Any arbitrary text or None must either parse into a valid dict or
    fail cleanly with ValueError (input validation contract). Leaking
    TypeError, IndexError, AttributeError, or other internal errors is a bug."""
    try:
        res = parse_order(s)
        assert isinstance(res, dict)
        for k, v in res.items():
            assert isinstance(k, str) and len(k) > 0
            assert isinstance(v, int) and v > 0
    except ValueError:
        pass


# ============================================================================
# B. Tests for delivery_eta(distance_km)
# ============================================================================

valid_distance_float = st.floats(min_value=0.0, max_value=10000.0, allow_nan=False, allow_infinity=False)
valid_distance_int = st.integers(min_value=0, max_value=10000)

@settings(max_examples=200, deadline=None)
@given(st.one_of(valid_distance_float, valid_distance_int))
def test_delivery_eta_valid_calculation(d):
    """For valid nonnegative finite numeric input, ETA calculation must match
    int(15 + float(d) * 4)."""
    expected = int(15 + float(d) * 4)
    assert delivery_eta(d) == expected


@settings(max_examples=200, deadline=None)
@given(valid_distance_float)
def test_delivery_eta_valid_numeric_string(d):
    """Numeric string representations must be parsed correctly."""
    s = str(d)
    expected = int(15 + float(d) * 4)
    assert delivery_eta(s) == expected


@settings(max_examples=200, deadline=None)
@given(st.text() | st.none())
@example("")
@example("   ")
@example(None)
@example("abc")
@example("-5")
@example("-0.01")
@example("infinity")
@example("nan")
def test_delivery_eta_no_crash(s):
    """Fuzzing delivery_eta with arbitrary text or None must either compute the
    correct ETA or cleanly raise ValueError. Uncontrolled TypeErrors or OverflowErrors
    are bugs."""
    try:
        res = delivery_eta(s)
        assert isinstance(res, int)
        assert res >= 15
    except ValueError:
        pass


@settings(max_examples=100, deadline=None)
@given(st.booleans())
def test_delivery_eta_rejects_booleans(b):
    """Booleans (True/False) should not be silently treated as 1 or 0 km."""
    with pytest.raises(ValueError):
        delivery_eta(b)


@settings(max_examples=100, deadline=None)
@given(st.sampled_from([float("nan"), float("inf"), float("-inf")]))
def test_delivery_eta_rejects_non_finite(x):
    """Non-finite floats (NaN, +inf, -inf) must raise ValueError, not OverflowError."""
    with pytest.raises(ValueError):
        delivery_eta(x)


# ============================================================================
# C. Tests for coupon_discount(code)
# ============================================================================

valid_discount_amount = st.integers(min_value=0, max_value=10000)

@settings(max_examples=200, deadline=None)
@given(valid_discount_amount)
def test_coupon_discount_valid_format(amt):
    """Valid SAVE<amt> coupons must return the exact integer discount."""
    code = f"SAVE{amt}"
    assert coupon_discount(code) == amt


@settings(max_examples=200, deadline=None)
@given(valid_discount_amount, st.sampled_from(["save", "Save", "SAVE", "sAvE"]))
def test_coupon_discount_case_and_whitespace_insensitivity(amt, prefix):
    """Coupon validation must handle mixed/lower case and surrounding whitespace."""
    code = f"  {prefix}{amt}  "
    assert coupon_discount(code) == amt


@settings(max_examples=200, deadline=None)
@given(st.text() | st.none())
@example("")
@example(None)
@example("   ")
@example("SAVE")
@example("SAVE-10")
@example("SAVEabc")
@example("DISCOUNT50")
@example("MYSAVE50EXTRA")
@example("SAVE50SAVE20")
@example("SAVE 50")
def test_coupon_discount_no_crash(s):
    """Any arbitrary string or None passed to coupon_discount must either return
    the correct discount or cleanly raise ValueError. Leaking IndexError,
    AttributeError, or TypeError indicates unhandled edge cases."""
    try:
        res = coupon_discount(s)
        assert isinstance(res, int)
        assert res >= 0
    except ValueError:
        pass

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


@pytest.mark.parametrize("invalid_input", [
    None,
    "",
    "   ",
    "\t\n",
    "pizza",                 # Missing colon
    ":2",                    # Empty item name
    "   :2",                 # Whitespace item name
    "pizza:",                # Missing quantity
    "pizza:   ",             # Whitespace quantity
    "pizza:abc",             # Non-numeric quantity
    "pizza:2.5",             # Float quantity
    "pizza:0",               # Zero quantity
    "pizza:-1",              # Negative quantity
    "pizza:-99",             # Large negative quantity
    "pizza:2:extra",         # Multiple colons
    "pizza:2:3:4",           # Many colons
    "pizza:2,,burger:1",     # Empty CSV entry between commas
    ",pizza:2",              # Leading comma / empty entry
    "pizza:2,",              # Trailing comma / empty entry
    "pizza:1,pizza:2",       # Duplicate item names
    "burger:2, burger:5",    # Duplicate item names with spaces
])
def test_parse_order_explicit_invalid_inputs(invalid_input):
    """Dedicated parametrized test verifying that invalid order inputs cleanly raise ValueError."""
    with pytest.raises(ValueError):
        parse_order(invalid_input)


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


@settings(max_examples=100, deadline=None)
@given(st.integers(min_value=10**400, max_value=10**450))
def test_delivery_eta_rejects_overflowing_integers(huge_int):
    """Extremely large integers that would trigger OverflowError during float conversion
    must be cleanly rejected with ValueError."""
    with pytest.raises(ValueError):
        delivery_eta(huge_int)


@pytest.mark.parametrize("invalid_distance", [
    None,
    True,
    False,
    "",
    "   ",
    "\t\n",
    "abc",
    "4.5km",
    "--5",
    "-1",
    "-0.001",
    "-100",
    float("nan"),
    float("inf"),
    float("-inf"),
    "nan",
    "inf",
    "-infinity",
    10**500,               # Huge integer causing float OverflowError
    -(10**500),            # Huge negative integer causing float OverflowError
    1e308,                 # Huge float causing int arithmetic overflow
])
def test_delivery_eta_explicit_invalid_inputs(invalid_distance):
    """Dedicated parametrized test verifying that all invalid distance values raise ValueError."""
    with pytest.raises(ValueError):
        delivery_eta(invalid_distance)


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


@pytest.mark.parametrize("invalid_code", [
    None,
    "",
    "   ",
    "\t\n",
    "SAVE",                 # SAVE without numeric suffix
    "save",                 # Lowercase without suffix
    "SAVE-10",              # Negative suffix
    "SAVE-0",               # Hyphen prefix
    "SAVEabc",              # Alphabetic suffix
    "SAVETWENTY",           # Word suffix
    "DISCOUNT50",           # Incorrect prefix
    "OFF50",                # Incorrect prefix
    "50SAVE",               # Prefix at end
    "MYSAVE50",             # Prefix embedded in word
    "MYSAVE50EXTRA",        # Embedded SAVE token with extra text
    "SAVE50SAVE20",         # Multiple SAVE tokens
    "SAVE 50",              # Space separator inside code
    "SAVE50.5",             # Float decimal in suffix
    "SAVE!",                # Symbol suffix
])
def test_coupon_discount_explicit_invalid_inputs(invalid_code):
    """Dedicated parametrized test verifying that all invalid coupon codes raise ValueError."""
    with pytest.raises(ValueError):
        coupon_discount(invalid_code)

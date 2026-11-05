import math

def parse_order(items_csv):
    """
    Parses a comma-separated string of item orders in the format 'name:qty'.
    Trims surrounding whitespace, requires non-empty names and positive integer quantities,
    and disallows empty inputs, malformed pairs, and duplicate item names.
    Raises ValueError on invalid user input.
    """
    if not isinstance(items_csv, str):
        raise ValueError("Order CSV must be a string")
    
    items_csv = items_csv.strip()
    if not items_csv:
        raise ValueError("Order CSV cannot be empty")
    
    order = {}
    for item in items_csv.split(','):
        item = item.strip()
        if not item:
            raise ValueError("Empty item entry found in order CSV")
        
        parts = item.split(':')
        if len(parts) != 2:
            raise ValueError(f"Malformed item entry '{item}', expected format 'name:qty'")
        
        name, qty_str = parts[0].strip(), parts[1].strip()
        if not name:
            raise ValueError(f"Item name cannot be empty in '{item}'")
        if name in order:
            raise ValueError(f"Duplicate item name '{name}' found in order")
        
        try:
            qty = int(qty_str)
        except (ValueError, TypeError):
            raise ValueError(f"Quantity for '{name}' must be an integer, got '{qty_str}'")
        
        if qty <= 0:
            raise ValueError(f"Quantity for '{name}' must be a positive integer, got {qty}")
        
        order[name] = qty
        
    return order


def delivery_eta(distance_km):
    """
    Calculates estimated delivery time in minutes given distance in kilometers.
    Preserves original calculation: int(15 + float(distance_km) * 4)
    Rejects None, booleans, non-finite values (inf, nan), malformed strings,
    and negative distances.
    Raises ValueError on invalid input.
    """
    if isinstance(distance_km, bool) or distance_km is None:
        raise ValueError("Distance cannot be None or a boolean")
    
    try:
        dist = float(distance_km)
    except (ValueError, TypeError):
        raise ValueError(f"Invalid distance value: {distance_km}")
    
    if math.isnan(dist) or math.isinf(dist):
        raise ValueError("Distance must be a finite real number")
    
    if dist < 0:
        raise ValueError(f"Distance cannot be negative, got {dist}")
    
    return int(15 + dist * 4)


def coupon_discount(code):
    """
    Calculates discount given a coupon code formatted as SAVE<amount>.
    Accepts uppercase, lowercase, and mixed-case codes with surrounding whitespace.
    Validates that the entire code matches the SAVE prefix followed by a nonnegative integer.
    Rejects missing prefix, non-string input, non-numeric or negative suffixes.
    Raises ValueError on invalid coupon code.
    """
    if not isinstance(code, str):
        raise ValueError("Coupon code must be a string")
    
    code = code.strip().upper()
    if not code.startswith("SAVE"):
        raise ValueError(f"Invalid coupon code '{code}', must start with 'SAVE'")
    
    discount_str = code[4:]
    if not discount_str:
        raise ValueError("Coupon code missing discount amount after 'SAVE'")
    
    if not discount_str.isdigit():
        raise ValueError(f"Coupon discount amount must be a nonnegative integer, got '{discount_str}'")
    
    discount = int(discount_str)
    return discount


def main():
    print("==== Running parse_order ====")
    user_input = input("Enter items as name:qty CSV (e.g. pizza:2,burger:1): ")
    try:
        result = parse_order(user_input)
        print("Order:", result)
    except ValueError as e:
        print(f"Error: {e}")

    print("\n==== Running delivery_eta ====")
    user_input = input("Enter distance in km (e.g. 4.5): ")
    try:
        result = delivery_eta(user_input)
        print("ETA in Minutes:", result)
    except ValueError as e:
        print(f"Error: {e}")

    print("\n==== Running coupon_discount ====")
    user_input = input("Enter a coupon code (e.g. SAVE50): ")
    try:
        result = coupon_discount(user_input)
        print("Discount:", result)
    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()

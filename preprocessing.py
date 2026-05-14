def parse_features(message: str, expected_count: int) -> list:
    """Converts '619, 42, 2, 0.0, 1, 1, 1, 101348.88, 0, 0, 0' into a list of floats"""
    raw = message.replace(",", " ").split()

    if len(raw) == 0:
        raise ValueError("empty message")

    try:
        values = [float(x) for x in raw]
    except ValueError:
        raise ValueError("all values must be numeric")

    if len(values) != expected_count:
        raise ValueError(f"expected {expected_count} values, got {len(values)}")

    return values
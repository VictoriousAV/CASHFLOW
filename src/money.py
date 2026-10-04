"""Money guards — integers only (Phase 2, rule 1)."""


def to_minor(amount) -> int:
    """Coerce user input to int naira minor units. Rejects floats/negatives."""
    if isinstance(amount, bool):
        raise ValueError("amount must be integer")
    if isinstance(amount, float):
        raise ValueError("amount must be integer minor units, not float")
    if isinstance(amount, str):
        amount = amount.replace(",", "").strip()
    value = int(amount)
    if value <= 0:
        raise ValueError("amount must be > 0")
    return value


def assert_int_money(**kwargs) -> None:
    for name, val in kwargs.items():
        if not isinstance(val, int) or isinstance(val, bool) or val < 0:
            raise ValueError(f"{name} must be non-negative int minor units")

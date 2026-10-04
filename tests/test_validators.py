import pytest
from src.validators import parse_date, validate_amount, validate_email


def test_dates():
    assert parse_date("2026-09-20") == "2026-09-20"
    assert parse_date("01/09/2026") == "2026-09-01"
    with pytest.raises(ValueError):
        parse_date("20-13-2026")
    with pytest.raises(ValueError):
        parse_date("2999-01-01")


def test_amount_and_email():
    assert validate_amount("2,500") == 2500
    with pytest.raises(ValueError):
        validate_amount(0)
    assert validate_email("A@b.co") == "a@b.co"
    with pytest.raises(ValueError):
        validate_email("bad")

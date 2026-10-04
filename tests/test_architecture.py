import pytest
from src.money import to_minor, assert_int_money
from src.config import build_forecast_inputs, FORECAST_METHOD
from src.validators import require_user_id


def test_money_rejects_float_and_negative():
    assert to_minor("4,500") == 4500
    with pytest.raises(ValueError):
        to_minor(45.5)
    with pytest.raises(ValueError):
        to_minor(-5)
    with pytest.raises(ValueError):
        to_minor(0)


def test_assert_int_money():
    assert_int_money(balance=10)
    with pytest.raises(ValueError):
        assert_int_money(balance=10.5)


def test_forecast_versioned():
    fi = build_forecast_inputs(48500, 2800.0)
    assert fi["method"] == FORECAST_METHOD == "mean_7d_v1"
    assert fi["balance"] == 48500 and fi["window_days"] == 30


def test_user_scoping_guard():
    with pytest.raises(ValueError):
        require_user_id("")

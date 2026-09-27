from src.forecast import project_balance, forecast_message


def test_project_floor_zero():
    proj = project_balance(5000, 3000, 3)
    assert proj[0] == (0, 5000)
    assert proj[-1][1] == 0


def test_message_none():
    assert "Add some expenses" in forecast_message(0, 0, None)

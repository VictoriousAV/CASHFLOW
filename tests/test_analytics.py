from src.analytics import (calc_balance, calc_avg_daily, calc_days_remaining,
                              calc_budget_usage, calc_savings_progress, summarize_category_totals)


def test_balance():
    assert calc_balance(70000, 21500) == 48500


def test_avg_daily():
    assert calc_avg_daily(21500, 5) == 4300.0
    assert calc_avg_daily(0, 0) == 0.0


def test_days_remaining():
    assert calc_days_remaining(48500, 2800) == 17
    assert calc_days_remaining(1000, 0) is None


def test_budget_and_savings():
    assert round(calc_budget_usage(17000, 20000), 1) == 85.0
    assert calc_savings_progress(75000, 250000) == 30.0


def test_category_totals():
    txns = [{"type": "expense", "category": "Food", "amount": 100},
            {"type": "income", "category": "Other", "amount": 999}]
    assert summarize_category_totals(txns) == {"Food": 100}

from src.analytics import dashboard_summary, week_over_week, generate_insights, daily_series
from src.forecast import versioned_forecast


def test_dashboard_summary():
    txns = [{"type": "income", "amount": 70000, "date": "2026-09-01", "category": "Other"},
            {"type": "expense", "amount": 2500, "date": "2026-09-03", "category": "Transport"}]
    s = dashboard_summary(txns)
    assert s["balance"] == 67500 and s["days_left"] == 27


def test_versioned():
    v = versioned_forecast(48500, 2800.0)
    assert v["inputs"]["method"] == "mean_7d_v1" and v["days_left"] == 17


def test_insights_budget_warning():
    outs = generate_insights({"Food": 17000}, None,
                             [{"category": "Food", "amount": 20000, "spent": 17000}])
    assert any("85%" in o or "budget" in o for o in outs)


def test_daily_and_wow_none():
    assert daily_series([]) == {}
    assert week_over_week([]) is None

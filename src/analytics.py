"""Core money math + pattern analysis — Python computes, LLM only explains (ADR-003)."""
from __future__ import annotations
from collections import defaultdict
from datetime import date


def calc_balance(total_income: int, total_expenses: int) -> int:
    return int(total_income) - int(total_expenses)


def calc_avg_daily(total_expenses: int, spending_days: int) -> float:
    if spending_days <= 0 or total_expenses <= 0:
        return 0.0
    return float(total_expenses) / float(spending_days)


def calc_days_remaining(balance: int, avg_daily: float):
    if avg_daily <= 0 or balance <= 0:
        return None
    return int(balance // avg_daily)


def calc_budget_usage(spent: int, limit: int) -> float:
    if limit <= 0:
        return 0.0
    return float(spent) / float(limit) * 100.0


def calc_savings_progress(saved: int, target: int) -> float:
    if target <= 0:
        return 0.0
    return float(saved) / float(target) * 100.0


def summarize_category_totals(transactions: list[dict]) -> dict:
    totals: dict[str, int] = {}
    for t in transactions:
        if str(t.get("type", "")).lower() != "expense":
            continue
        cat = t.get("category") or "Other"
        totals[cat] = totals.get(cat, 0) + int(t.get("amount", 0))
    return totals


def top_category(totals: dict) -> tuple[str | None, int]:
    if not totals:
        return None, 0
    k = max(totals, key=totals.get)
    return k, totals[k]


def daily_series(transactions: list[dict]) -> dict[str, int]:
    out: dict[str, int] = defaultdict(int)
    for t in transactions:
        if str(t.get("type", "")).lower() != "expense":
            continue
        out[str(t.get("date", ""))] += int(t.get("amount", 0))
    return dict(sorted(out.items()))


def week_over_week(transactions: list[dict]) -> float | None:
    """% change last 7 days vs prior 7 days (by ISO date strings). Needs >=2 days data."""
    days = sorted({str(t.get("date", "")) for t in transactions if t.get("date")})
    if len(days) < 2:
        return None
    last, prev = days[-7:], days[-14:-7]
    def s(ds):
        return sum(int(t.get("amount", 0)) for t in transactions
                   if t.get("date") in ds and str(t.get("type")).lower() == "expense")
    p, l = s(prev), s(last)
    if p <= 0:
        return None if l == 0 else 100.0
    return round((l - p) / p * 100, 1)


def generate_insights(totals: dict, wow: float | None, budgets: list[dict]) -> list[str]:
    out: list[str] = []
    k, v = top_category(totals)
    if k:
        out.append(f"{k} is your largest expense so far (₦{v:,}).")
    if wow is not None:
        out.append(f"Spending {'up' if wow >= 0 else 'down'} {abs(wow)}% vs prior week.")
    spent_by = {b.get("category"): 0 for b in budgets}
    # caller fills spent; budgets carry amount only — usage computed in app
    for b in budgets:
        u = calc_budget_usage(0, 0)  # placeholder keeps helper pure
        _ = u
    for b in budgets:
        if calc_budget_usage(int(b.get("spent", 0)), int(b.get("amount", 0))) >= 85:
            out.append(f"⚠️ {b.get('category')} budget at "
                       f"{calc_budget_usage(int(b.get('spent',0)),int(b.get('amount',0))):.0f}% used.")
    return out


def dashboard_summary(transactions: list[dict]) -> dict:
    inc = sum(int(t.get("amount", 0)) for t in transactions if str(t.get("type")).lower() == "income")
    exp = sum(int(t.get("amount", 0)) for t in transactions if str(t.get("type")).lower() == "expense")
    days = len({t.get("date") for t in transactions if str(t.get("type")).lower() == "expense"})
    avg = calc_avg_daily(exp, days)
    bal = calc_balance(inc, exp)
    totals = summarize_category_totals(transactions)
    return {"income": inc, "expenses": exp, "balance": bal, "avg_daily": avg,
            "days": days, "days_left": calc_days_remaining(bal, avg),
            "totals": totals, "daily": daily_series(transactions),
            "wow": week_over_week(transactions), "today": date.today().isoformat()}

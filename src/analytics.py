"""Core money math — Python computes, LLM only explains (ADR-003)."""
from __future__ import annotations


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

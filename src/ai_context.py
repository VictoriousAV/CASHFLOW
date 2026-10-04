"""Grounded AI context builder (Phase 8) — Python computes, LLM explains."""
from __future__ import annotations


def build_context(balance: int, avg_daily: float, cat_totals: dict,
                  days_left, savings_goal: int = 0, budgets: list | None = None) -> str:
    parts = [f"Current balance: ₦{balance:,}",
             f"Average daily spending: ₦{int(avg_daily):,}",
             f"Estimated remaining days: {days_left} (estimate, not guarantee)",
             f"Savings goal: ₦{int(savings_goal):,}"]
    for k, v in sorted((cat_totals or {}).items(), key=lambda x: -x[1])[:5]:
        parts.append(f"{k} spending: ₦{v:,}")
    for b in budgets or []:
        parts.append(f"Budget {b.get('category')}: spent ₦{b.get('spent',0):,} / limit ₦{b.get('amount',0):,}")
    return "\n".join(parts)


def build_context_json(balance: int, avg_daily: float, cat_totals: dict,
                       days_left, savings_goal: int = 0) -> dict:
    return {"balance": int(balance), "avg_daily": float(avg_daily),
            "days_left": days_left, "savings_goal": int(savings_goal),
            "categories": dict(cat_totals or {})}

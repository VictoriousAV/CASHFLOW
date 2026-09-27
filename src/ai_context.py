"""Grounded AI context builder (full in Phase 8)."""


def build_context(balance: int, avg_daily: float, cat_totals: dict,
                  days_left, savings_goal: int = 0) -> str:
    parts = [f"Current balance: ₦{balance:,}",
             f"Average daily spending: ₦{int(avg_daily):,}"]
    for k, v in sorted(cat_totals.items(), key=lambda x: -x[1])[:5]:
        parts.append(f"{k}: ₦{v:,}")
    parts.append(f"Estimated remaining days: {days_left}")
    parts.append(f"Savings goal: ₦{savings_goal:,}")
    return "\n".join(parts)

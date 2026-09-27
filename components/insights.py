"""Deterministic insights (no LLM)."""


def top_category_insight(totals: dict) -> str:
    if not totals:
        return "Add transactions to unlock insights."
    top = max(totals, key=totals.get)
    return f"{top} is your largest expense so far (₦{totals[top]:,})."

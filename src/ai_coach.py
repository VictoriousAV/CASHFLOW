"""LLM wrapper stub — rule-based fallback keeps demo alive offline."""
from .forecast import forecast_message


def fallback_answer(question: str, balance: int, avg_daily: float, days_left) -> str:
    q = question.lower()
    if "afford" in q:
        return (f"With ₦{balance:,} and ~₦{int(avg_daily):,}/day "
                f"({forecast_message(balance, avg_daily, days_left)}), "
                f"check if the purchase keeps 7+ days buffer.")
    if "where" in q or "most" in q:
        return "Your largest category is shown in the donut chart above."
    return forecast_message(balance, avg_daily, days_left)

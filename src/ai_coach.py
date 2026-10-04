"""AI Coach — grounded answers with guardrails (Phase 8).
Uses LLM API when OPENAI_API_KEY (or compatible) is set; otherwise rule-based fallback.
Never invents transactions; forecasts labeled estimates; not a licensed adviser.
"""
from __future__ import annotations
from .forecast import forecast_message
from .ai_context import build_context
from .secrets import get_secret

SYSTEM_PROMPT = (
    "You are CashFlow AI, a friendly financial decision-support assistant (not a licensed adviser). "
    "Use ONLY the provided calculated context. Never invent transactions. "
    "Explain numbers plainly in ₦, present forecasts as estimates "
    "(Balance ÷ Avg Daily), say when info is unavailable, "
    "and avoid high-risk investment recommendations."
)


def fallback_answer(question: str, balance: int, avg_daily: float, days_left) -> str:
    return _rule_based(question, balance, avg_daily, days_left, {})


def _rule_based(question: str, balance: int, avg_daily: float, days_left, totals: dict) -> str:
    q = (question or "").lower()
    import re
    m = re.search(r"(\d[\d,]*)", q)
    purchase = int(m.group(1).replace(",", "")) if m else None
    if "afford" in q and purchase:
        left = balance - purchase
        verdict = "likely yes, with buffer" if days_left and left > avg_daily * 7 else "risky — it eats your buffer"
        return (f"That ₦{purchase:,} purchase is {verdict}. "
                f"{forecast_message(balance, avg_daily, days_left)} Keep 7+ days buffer.")
    if "afford" in q:
        return (f"{forecast_message(balance, avg_daily, days_left)} "
                f"Tell me the amount to check affordability with a 7-day buffer.")
    if "where" in q or "most" in q or "spend" in q:
        if totals:
            k = max(totals, key=totals.get)
            return f"Most goes to {k} (₦{totals[k]:,}). " + forecast_message(balance, avg_daily, days_left)
        return "Your largest category will appear once you add expenses."
    if "last" in q or "long" in q or "stretch" in q or "make" in q:
        per_day = f"₦{int(30000/14):,}/day" if "30000" in q else f"₦{int(avg_daily):,}/day"
        return (f"{forecast_message(balance, avg_daily, days_left)} "
                f"To stretch: cap food+entertainment, cook more, target {per_day}.")
    if "save" in q:
        return f"Save 10-20% of income first, then spend. {forecast_message(balance, avg_daily, days_left)}"
    return forecast_message(balance, avg_daily, days_left)


def _llm_answer(question: str, context: str) -> str | None:
    key = get_secret("OPENAI_API_KEY") or get_secret("GROQ_API_KEY")
    if not key:
        return None
    try:
        from openai import OpenAI
        client = OpenAI(api_key=key, base_url=get_secret("OPENAI_BASE_URL") or None)
        r = client.chat.completions.create(
            model=get_secret("OPENAI_MODEL", "gpt-4o-mini"),
            messages=[{"role": "system", "content": SYSTEM_PROMPT},
                      {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}],
            max_tokens=300, temperature=0.3, timeout=20)
        return r.choices[0].message.content.strip()
    except Exception:
        return None


def answer(question: str, balance: int, avg_daily: float, days_left,
           totals: dict | None = None, savings_goal: int = 0) -> str:
    totals = totals or {}
    ctx = build_context(balance, avg_daily, totals, days_left, savings_goal)
    llm = _llm_answer(question, ctx)
    if llm:
        if "estimate" not in llm.lower() and days_left is not None:
            llm += " (Estimate only.)"
        return llm
    return _rule_based(question, balance, avg_daily, days_left, totals)

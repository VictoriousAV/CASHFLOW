"""AI Coach — OpenRouter (OpenAI-compatible) with rule-based fallback.

The API key lives only in the server environment (OPENROUTER_API_KEY) and is
never shipped to the browser. Without a key (or on any provider error) the
coach silently falls back to the local rule-based answers.
"""
from __future__ import annotations

import os

from src.ai_coach import SYSTEM_PROMPT, _rule_based
from src.ai_context import build_context

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
DEFAULT_MODEL = "openai/gpt-4o-mini"


def api_key() -> str:
    return os.environ.get("OPENROUTER_API_KEY", "").strip()


def model() -> str:
    return os.environ.get("OPENROUTER_MODEL", "").strip() or DEFAULT_MODEL


def _llm_answer(question: str, context: str) -> str | None:
    key = api_key()
    if not key:
        return None
    try:
        from openai import OpenAI
        client = OpenAI(api_key=key, base_url=OPENROUTER_BASE_URL)
        r = client.chat.completions.create(
            model=model(),
            messages=[{"role": "system", "content": SYSTEM_PROMPT},
                      {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}],
            max_tokens=300, temperature=0.3, timeout=20)
        return (r.choices[0].message.content or "").strip() or None
    except Exception:
        return None


def answer(question: str, balance: float, avg_daily: float, days_left,
           totals: dict | None = None, savings_goal: float = 0) -> tuple[str, str]:
    """Return (answer_text, source) where source is 'openrouter' or 'fallback'."""
    totals = totals or {}
    balance, avg_daily = int(balance or 0), float(avg_daily or 0)
    savings_goal = int(savings_goal or 0)
    ctx = build_context(balance, avg_daily, totals, days_left, savings_goal)
    llm = _llm_answer(question, ctx)
    if llm:
        if "estimate" not in llm.lower() and days_left is not None:
            llm += " (Estimate only.)"
        return llm, "openrouter"
    return _rule_based(question, balance, avg_daily, days_left, totals), "fallback"

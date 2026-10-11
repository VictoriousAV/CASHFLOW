"""CashFlow AI — FastAPI server.

Serves the redesigned web UI and exposes the dynamic API:
  GET  /api/health  → service + AI provider status
  POST /api/coach   → AI coach answer (OpenRouter, rule-based fallback)
"""
from __future__ import annotations

import os
import time
from collections import defaultdict, deque
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel, Field

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

from . import coach

ROOT = Path(__file__).resolve().parent.parent
app = FastAPI(title="CashFlow AI", version="1.0.0")

_hits: dict[str, deque] = defaultdict(deque)


def _int_env(name: str, default: int) -> int:
    try:
        return int(os.environ.get(name, default))
    except (TypeError, ValueError):
        return default


def _client_ip(request: Request) -> str:
    fwd = request.headers.get("x-forwarded-for", "")
    if fwd:
        return fwd.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


def _rate_limited(ip: str) -> tuple[bool, int, int]:
    """Sliding-window limit per visitor IP. Returns (limited, limit, window)."""
    limit = _int_env("COACH_RATE_LIMIT", 2)
    window = _int_env("COACH_RATE_WINDOW", 3600)
    now = time.time()
    q = _hits[ip]
    while q and now - q[0] > window:
        q.popleft()
    if len(q) >= limit:
        return True, limit, window
    q.append(now)
    return False, limit, window


def _limit_message(limit: int, window: int) -> str:
    when = (f"{window // 3600} hour(s)" if window >= 3600 and window % 3600 == 0
            else f"{max(1, round(window / 60))} minutes")
    return (f"You've used your {limit} free AI coach questions for now. "
            f"Upgrade for unlimited questions, or try again in about {when}.")


class CoachRequest(BaseModel):
    question: str = Field(min_length=1, max_length=500)
    balance: float = 0
    avg_daily: float = 0
    days_left: int | None = None
    totals: dict[str, float] = Field(default_factory=dict)
    savings_goal: float = 0


@app.get("/api/health")
def health() -> dict:
    return {"status": "ok",
            "ai": "openrouter" if coach.api_key() else "fallback",
            "model": coach.model()}


@app.post("/api/coach", response_model=None)
def ask(req: CoachRequest, request: Request):
    limited, limit, window = _rate_limited(_client_ip(request))
    if limited:
        return JSONResponse(status_code=429, content={
            "source": "rate_limited",
            "message": _limit_message(limit, window)})
    text, source = coach.answer(
        req.question.strip(), req.balance, req.avg_daily,
        req.days_left, req.totals, req.savings_goal)
    return {"answer": text, "source": source}


@app.get("/")
def index() -> FileResponse:
    return FileResponse(ROOT / "index.html")

"""CashFlow AI — FastAPI server.

Serves the redesigned web UI and exposes the dynamic API:
  GET  /api/health  → service + AI provider status
  POST /api/coach   → AI coach answer (OpenRouter, rule-based fallback)
"""
from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

from . import coach

ROOT = Path(__file__).resolve().parent.parent
app = FastAPI(title="CashFlow AI", version="1.0.0")


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


@app.post("/api/coach")
def ask(req: CoachRequest) -> dict:
    text, source = coach.answer(
        req.question.strip(), req.balance, req.avg_daily,
        req.days_left, req.totals, req.savings_goal)
    return {"answer": text, "source": source}


@app.get("/")
def index() -> FileResponse:
    return FileResponse(ROOT / "index.html")

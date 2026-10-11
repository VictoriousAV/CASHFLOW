"""FastAPI server tests — health, UI serving, coach contract + fallback."""
from fastapi.testclient import TestClient

from server import coach
from server.main import app

client = TestClient(app)


def test_health_reports_ai_mode(monkeypatch):
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    r = client.get("/api/health")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok"
    assert body["ai"] == "fallback"


def test_health_reports_openrouter_when_key_set(monkeypatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "sk-or-test")
    r = client.get("/api/health")
    assert r.json()["ai"] == "openrouter"


def test_index_served():
    r = client.get("/")
    assert r.status_code == 200
    assert "CashFlow AI" in r.text


def test_coach_falls_back_without_key(monkeypatch):
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    r = client.post("/api/coach", json={
        "question": "Can I afford ₦50000 headphones?",
        "balance": 120000, "avg_daily": 4000, "days_left": 30,
        "totals": {"Food": 9000}})
    assert r.status_code == 200
    body = r.json()
    assert body["source"] == "fallback"
    assert "₦" in body["answer"]


def test_coach_uses_llm_when_available(monkeypatch):
    monkeypatch.setattr(coach, "_llm_answer", lambda q, c: "Your balance covers it")
    r = client.post("/api/coach", json={
        "question": "Can I afford ₦50000?", "balance": 120000,
        "avg_daily": 4000, "days_left": 30})
    assert r.status_code == 200
    body = r.json()
    assert body["source"] == "openrouter"
    assert body["answer"].startswith("Your balance covers it")
    assert "estimate" in body["answer"].lower()


def test_coach_requires_question():
    assert client.post("/api/coach", json={"question": ""}).status_code == 422
    assert client.post("/api/coach", json={}).status_code == 422

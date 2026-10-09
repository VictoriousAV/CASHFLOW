"""Groq provider resolution tests (no network — config only)."""
import os
import src.ai_coach as coach
from src.ai_coach import resolve_llm_config, GROQ_BASE_URL, GROQ_DEFAULT_MODEL


def _clean():
    for k in ("OPENAI_API_KEY", "OPENAI_BASE_URL", "OPENAI_MODEL",
              "GROQ_API_KEY", "GROQ_BASE_URL", "GROQ_MODEL", "APP_DB_PATH"):
        os.environ.pop(k, None)


def test_no_key_returns_none():
    _clean()
    assert resolve_llm_config() is None


def test_groq_selected_with_defaults(monkeypatch):
    _clean()
    monkeypatch.setenv("GROQ_API_KEY", "gsk-test")
    cfg = resolve_llm_config()
    assert cfg["provider"] == "groq"
    assert cfg["base_url"] == GROQ_BASE_URL
    assert cfg["model"] == GROQ_DEFAULT_MODEL


def test_openai_takes_priority(monkeypatch):
    _clean()
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
    monkeypatch.setenv("GROQ_API_KEY", "gsk-test")
    assert resolve_llm_config()["provider"] == "openai"


def test_groq_model_override(monkeypatch):
    _clean()
    monkeypatch.setenv("GROQ_API_KEY", "gsk-test")
    monkeypatch.setenv("GROQ_MODEL", "llama-3.1-8b-instant")
    assert resolve_llm_config()["model"] == "llama-3.1-8b-instant"


def test_answer_still_offline_without_key():
    _clean()
    a = coach.answer("Can I afford 5000?", 30000, 2500.0, 12, {"Food": 15000})
    assert "buffer" in a.lower() or "estimate" in a.lower()

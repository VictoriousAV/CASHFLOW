"""Secrets loader — env first, then .streamlit/secrets.toml (never committed)."""
from __future__ import annotations
import os
from pathlib import Path

try:
    import tomllib  # py3.11+
except ImportError:  # pragma: no cover
    tomllib = None


def get_secret(name: str, default: str = "") -> str:
    if os.environ.get(name):
        return os.environ[name]
    try:
        import streamlit as st  # only inside Streamlit runtime
        if hasattr(st, "secrets") and name in st.secrets:
            return str(st.secrets[name])
    except Exception:
        pass
    p = Path(".streamlit/secrets.toml")
    if tomllib and p.exists():
        try:
            return str(tomllib.loads(p.read_text()).get(name, default))
        except Exception:
            pass
    return default


def db_path() -> str:
    return get_secret("APP_DB_PATH", os.environ.get("APP_DB_PATH", "data/cashflow.db"))

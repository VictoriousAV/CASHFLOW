"""SQLite connection + init (stdlib only)."""
from __future__ import annotations
import os
import sqlite3
from pathlib import Path

DB_PATH = os.environ.get("APP_DB_PATH", "data/cashflow.db")
SCHEMA_PATH = Path(__file__).resolve().parent.parent / "data" / "schema.sql"


def get_conn(path: str = DB_PATH) -> sqlite3.Connection:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(path: str = DB_PATH) -> None:
    conn = get_conn(path)
    try:
        conn.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
        conn.commit()
    finally:
        conn.close()

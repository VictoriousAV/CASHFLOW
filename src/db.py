"""SQLite connection + init + scoped helpers (Phase 3)."""
from __future__ import annotations
import sqlite3
from contextlib import contextmanager
from pathlib import Path

from .secrets import db_path

SCHEMA_PATH = Path(__file__).resolve().parent.parent / "data" / "schema.sql"


def get_conn(path: str | None = None) -> sqlite3.Connection:
    p = path or db_path()
    Path(p).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(p)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


@contextmanager
def tx(path: str | None = None):
    """Transactional scope — commits on success, rolls back on error."""
    conn = get_conn(path)
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db(path: str | None = None) -> None:
    conn = get_conn(path)
    try:
        conn.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
        conn.commit()
    finally:
        conn.close()

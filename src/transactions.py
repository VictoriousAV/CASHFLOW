"""Transactions service — scoped CRUD + transactional CSV (Phase 3)."""
from __future__ import annotations
import csv
import uuid
from . import db as dbm
from .auth import utcnow
from .categorize import categorize
from .validators import (validate_amount, parse_date, validate_type,
                         validate_category, require_user_id)

REQUIRED_COLS = {"date", "description", "amount", "type"}


def _norm_row(raw: dict) -> dict:
    desc = str(raw.get("description") or "").strip()
    if not desc:
        raise ValueError("description required")
    return {
        "description": desc,
        "amount": validate_amount(raw.get("amount")),
        "type": validate_type(raw.get("type")),
        "category": validate_category(raw.get("category") or categorize(desc)),
        "date": parse_date(str(raw.get("date") or "")),
        "note": str(raw.get("note") or ""),
    }


def parse_csv_rows(text: str) -> tuple[list[dict], list[str]]:
    """Validate-only pass — returns (rows, errors), inserts nothing."""
    rows: list[dict] = []
    errors: list[str] = []
    reader = csv.DictReader(text.splitlines())
    if reader.fieldnames is None:
        return [], ["Empty CSV"]
    cols = {c.strip().lower() for c in reader.fieldnames}
    if not REQUIRED_COLS.issubset(cols):
        return [], [f"Missing columns. Need: {sorted(REQUIRED_COLS)}"]
    for i, r in enumerate(reader, start=2):
        get = lambda *ks: next((r.get(k) for k in ks if r.get(k) is not None), "")
        try:
            rows.append(_norm_row({
                "description": get("Description", "description"),
                "amount": str(get("Amount", "amount")).replace(",", ""),
                "type": get("Type", "type"),
                "date": get("Date", "date"),
            }))
        except Exception as e:
            errors.append(f"Row {i}: {e}")
    return rows, errors


def create_transaction(user_id: str, raw: dict, path: str | None = None) -> dict:
    require_user_id(user_id)
    clean = _norm_row(raw)
    tid = "t_" + uuid.uuid4().hex[:12]
    with dbm.tx(path) as conn:
        conn.execute(
            "INSERT INTO transactions(txn_id,user_id,description,amount,type,category,date,note,created_at)"
            " VALUES(?,?,?,?,?,?,?,?,?)",
            (tid, user_id, clean["description"], clean["amount"], clean["type"],
             clean["category"], clean["date"], clean["note"], utcnow()))
    return {"txn_id": tid, **clean}


def import_transactions(user_id: str, rows: list[dict], path: str | None = None) -> int:
    """All-or-nothing bulk insert — caller must pass validated rows."""
    require_user_id(user_id)
    clean = [_norm_row(r) for r in rows]  # re-validate inside tx boundary
    with dbm.tx(path) as conn:
        for c in clean:
            conn.execute(
                "INSERT INTO transactions(txn_id,user_id,description,amount,type,category,date,note,created_at)"
                " VALUES(?,?,?,?,?,?,?,?,?)",
                ("t_" + uuid.uuid4().hex[:12], user_id, c["description"], c["amount"],
                 c["type"], c["category"], c["date"], c["note"], utcnow()))
    return len(clean)


def list_transactions(user_id: str, category: str = "", path: str | None = None) -> list[dict]:
    require_user_id(user_id)
    conn = dbm.get_conn(path)
    try:
        if category:
            rows = conn.execute(
                "SELECT * FROM transactions WHERE user_id=? AND category=? ORDER BY date",
                (user_id, category)).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM transactions WHERE user_id=? ORDER BY date",
                (user_id,)).fetchall()
    finally:
        conn.close()
    return [dict(r) for r in rows]


def delete_transaction(user_id: str, txn_id: str, path: str | None = None) -> bool:
    require_user_id(user_id)
    with dbm.tx(path) as conn:
        cur = conn.execute("DELETE FROM transactions WHERE txn_id=? AND user_id=?",
                           (txn_id, user_id))
        return cur.rowcount > 0

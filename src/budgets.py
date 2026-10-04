"""Budgets + goals scoped CRUD (Phase 3; full UI in Phase 7)."""
from __future__ import annotations
import uuid
from . import db as dbm
from .analytics import calc_budget_usage, calc_savings_progress
from .validators import validate_amount, validate_category, require_user_id

budget_usage = calc_budget_usage
savings_progress = calc_savings_progress


def set_budget(user_id: str, category: str, amount: int, path: str | None = None) -> dict:
    require_user_id(user_id)
    category = validate_category(category)
    amount = validate_amount(amount)
    bid = "b_" + uuid.uuid4().hex[:12]
    with dbm.tx(path) as conn:
        conn.execute("DELETE FROM budgets WHERE user_id=? AND category=?", (user_id, category))
        conn.execute("INSERT INTO budgets(budget_id,user_id,category,amount) VALUES(?,?,?,?)",
                     (bid, user_id, category, amount))
    return {"budget_id": bid, "category": category, "amount": amount}


def list_budgets(user_id: str, path: str | None = None) -> list[dict]:
    require_user_id(user_id)
    conn = dbm.get_conn(path)
    try:
        rows = conn.execute("SELECT * FROM budgets WHERE user_id=?", (user_id,)).fetchall()
    finally:
        conn.close()
    return [dict(r) for r in rows]


def set_goal(user_id: str, name: str, target: int, path: str | None = None) -> dict:
    require_user_id(user_id)
    if not name.strip():
        raise ValueError("goal name required")
    target = validate_amount(target)
    gid = "g_" + uuid.uuid4().hex[:12]
    with dbm.tx(path) as conn:
        conn.execute("INSERT INTO goals(goal_id,user_id,name,target_amount) VALUES(?,?,?,?)",
                     (gid, user_id, name.strip(), target))
    return {"goal_id": gid, "name": name.strip(), "target_amount": target}

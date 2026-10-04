"""User service — scoped, bcrypt-backed (Phase 3)."""
from __future__ import annotations
import uuid
from . import db as dbm
from .auth import hash_password, verify_password, utcnow
from .validators import validate_email, require_user_id


def create_user(name: str, email: str, password: str, monthly_income: int = 0,
                path: str | None = None) -> dict:
    email = validate_email(email)
    if not name.strip():
        raise ValueError("name required")
    uid = "u_" + uuid.uuid4().hex[:12]
    with dbm.tx(path) as conn:
        try:
            conn.execute(
                "INSERT INTO users(user_id,name,email,password_hash,monthly_income,created_at)"
                " VALUES(?,?,?,?,?,?)",
                (uid, name.strip(), email, hash_password(password),
                 int(monthly_income), utcnow()))
        except Exception as e:
            if "UNIQUE" in str(e).upper():
                raise ValueError("email already registered")
            raise
    return {"user_id": uid, "name": name.strip(), "email": email}


def authenticate(email: str, password: str, path: str | None = None) -> dict | None:
    email = validate_email(email)
    conn = dbm.get_conn(path)
    try:
        row = conn.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()
    finally:
        conn.close()
    if not row or not verify_password(password, row["password_hash"]):
        return None
    return dict(row)


def get_user(user_id: str, path: str | None = None) -> dict | None:
    require_user_id(user_id)
    conn = dbm.get_conn(path)
    try:
        row = conn.execute("SELECT * FROM users WHERE user_id=?", (user_id,)).fetchone()
    finally:
        conn.close()
    return dict(row) if row else None

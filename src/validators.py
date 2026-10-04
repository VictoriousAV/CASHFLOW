"""Validation helpers — amount, dates, email, category (Phase 2/3)."""
from __future__ import annotations
from datetime import datetime, date
from .config import CATEGORIES
from .money import to_minor

DATE_FORMATS = ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y")


def validate_amount(amount) -> int:
    return to_minor(amount)


def parse_date(value: str) -> str:
    """Accept YYYY-MM-DD + DD/MM/YYYY (CSV), return ISO YYYY-MM-DD. Rejects future."""
    v = (value or "").strip()
    if not v:
        raise ValueError("date is required")
    for fmt in DATE_FORMATS:
        try:
            d = datetime.strptime(v, fmt).date()
            if d > date.today():
                raise ValueError("date cannot be in the future")
            return d.isoformat()
        except ValueError as e:
            if "future" in str(e):
                raise
            continue
    raise ValueError(f"bad date '{value}': use YYYY-MM-DD or DD/MM/YYYY")


def validate_type(value: str) -> str:
    v = str(value or "").strip().lower()
    if v not in ("income", "expense"):
        raise ValueError("type must be income|expense")
    return v


def validate_category(value: str) -> str:
    v = str(value or "Other").strip()
    return v if v in CATEGORIES else "Other"


def validate_email(value: str) -> str:
    v = str(value or "").strip().lower()
    if "@" not in v or "." not in v:
        raise ValueError("bad email")
    return v


def require_user_id(user_id: str) -> str:
    if not user_id or not str(user_id).strip():
        raise ValueError("user_id is required (no cross-user access)")
    return str(user_id)

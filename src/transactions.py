"""Transactions service — CRUD + CSV validation (full in Phase 5)."""
from __future__ import annotations
import csv
from .categorize import categorize

REQUIRED_COLS = {"date", "description", "amount", "type"}


def parse_csv_rows(text: str) -> tuple[list[dict], list[str]]:
    rows: list[dict] = []
    errors: list[str] = []
    reader = csv.DictReader(text.splitlines())
    if reader.fieldnames is None:
        return [], ["Empty CSV"]
    cols = {c.strip().lower() for c in reader.fieldnames}
    if not REQUIRED_COLS.issubset(cols):
        return [], [f"Missing columns. Need: {sorted(REQUIRED_COLS)}"]
    for i, r in enumerate(reader, start=2):
        try:
            desc = (r.get("Description") or r.get("description") or "").strip()
            amt = int(str(r.get("Amount") or r.get("amount") or "0").replace(",", "").strip())
            typ = str(r.get("Type") or r.get("type") or "").strip().lower()
            if not desc or amt <= 0 or typ not in ("income", "expense"):
                raise ValueError("bad row")
            rows.append({
                "description": desc, "amount": amt, "type": typ,
                "date": (r.get("Date") or r.get("date") or "").strip(),
                "category": categorize(desc),
            })
        except Exception:
            errors.append(f"Row {i}: invalid amount/type/description")
    return rows, errors

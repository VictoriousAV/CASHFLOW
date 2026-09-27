"""Rule-based categorizer v1 (Phase 0 stub → full in Phase 4)."""
from __future__ import annotations
import re

KEYWORDS = {
    r"mtn|glo|airtel|9mobile|data|airtime": "Data & Airtime",
    r"uber|bolt|keke|bus|transport|fuel": "Transport",
    r"chicken|kfc|shoprite|food|restaurant|republic": "Food",
    r"school|tuition|books|education|udemy": "Education",
    r"netflix|cinema|game|entertainment|spotify": "Entertainment",
    r"shop|jumia|konga|shopping|boutique": "Shopping",
    r"nepa|phcn|rent|water|bill|dstv": "Bills",
    r"savings|ajo|piggy": "Savings",
    r"hospital|pharmacy|health|drug": "Health",
}

COMPILED = [(re.compile(p, re.I), cat) for p, cat in KEYWORDS.items()]


def categorize(description: str, fallback: str = "Other") -> str:
    desc = (description or "").strip()
    for pattern, cat in COMPILED:
        if pattern.search(desc):
            return cat
    return fallback

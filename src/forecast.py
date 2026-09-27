"""Forecast — estimates only, never guarantees."""
from __future__ import annotations


def project_balance(balance: int, avg_daily: float, days: int = 30) -> list[tuple[int, int]]:
    out: list[tuple[int, int]] = []
    for d in range(days + 1):
        remaining = int(balance - avg_daily * d)
        out.append((d, max(remaining, 0)))
    return out


def forecast_message(balance: int, avg_daily: float, days_left) -> str:
    if days_left is None:
        return "Add some expenses to enable your forecast estimate."
    return (
        f"Your money may last approximately {days_left} days "
        f"at your current spending rate ({int(avg_daily):,}/day). Estimate only."
    )

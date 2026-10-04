"""Forecast — estimates only, never guarantees (versioned inputs per Phase 2)."""
from __future__ import annotations
from .config import build_forecast_inputs


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
        f"at your current spending rate (₦{int(avg_daily):,}/day). Estimate only."
    )


def versioned_forecast(balance: int, avg_daily: float, window_days: int = 30) -> dict:
    inputs = build_forecast_inputs(balance, avg_daily, window_days)
    from .analytics import calc_days_remaining
    days_left = calc_days_remaining(balance, avg_daily)
    return {"inputs": inputs, "days_left": days_left,
            "projection": project_balance(balance, avg_daily, window_days),
            "message": forecast_message(balance, avg_daily, days_left)}

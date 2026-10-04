"""Design tokens + constants — bright high-contrast theme (user-approved)."""
PRIMARY = "#00C853"
PRIMARY_DARK = "#009624"
SECONDARY = "#D4FF00"
BG = "#FFFFFF"
TEXT = "#000000"
MUTED = "#333333"
BORDER = "#000000"
WARNING = "#FF8F00"
DANGER = "#E60000"
INFO = "#0057FF"
RADIUS = 16

CATEGORIES = [
    "Food", "Transport", "Data & Airtime", "Education",
    "Entertainment", "Shopping", "Bills", "Savings",
    "Health", "Other",
]

CATEGORY_COLORS = {
    "Food": "#00C853",
    "Transport": "#0057FF",
    "Data & Airtime": "#9D00FF",
    "Education": "#00B8D4",
    "Entertainment": "#FF8F00",
    "Shopping": "#FF4081",
    "Bills": "#333333",
    "Savings": "#D4FF00",
    "Health": "#E60000",
    "Other": "#9E9E9E",
}

MOCK_USER = {"name": "Daniel", "balance": 48500, "income": 70000,
             "expenses": 21500, "savings": 10000, "avg_daily": 2800, "days_left": 17}

FORECAST_METHOD = "mean_7d_v1"


def build_forecast_inputs(balance: int, avg_daily: float, window_days: int = 30) -> dict:
    from .money import assert_int_money
    assert_int_money(balance=int(balance))
    return {"balance": int(balance), "avg_daily": float(avg_daily),
            "window_days": int(window_days), "method": FORECAST_METHOD}

def format_naira(amount) -> str:
    try:
        return f"₦{int(amount):,}"
    except (ValueError, TypeError):
        return "₦0"

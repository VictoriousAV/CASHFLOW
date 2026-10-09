"""Design tokens — Complete UI color system (user-approved).
Primary #064E3B (hover #043D2F), Secondary #52796F, Gold #D6B779,
bg #FAF8F2, surface #FFFFFF, border #E5E1D8, text #202923, muted #68756D.
"""
PRIMARY = "#064E3B"
PRIMARY_DARK = "#043D2F"
PRIMARY_HOVER = "#043D2F"
SECONDARY = "#52796F"
GOLD = "#D6B779"
BG = "#FAF8F2"
SURFACE = "#FFFFFF"
BORDER = "#E5E1D8"
TEXT = "#202923"
MUTED = "#68756D"
BUTTON = "#064E3B"
BUTTON_TEXT = "#FFFFFF"
WARNING = "#B7791F"
DANGER = "#C0392B"
INFO = "#52796F"
RADIUS = 16
# Back-compat aliases
BG_DEEP = "#F1EEE6"
HEADER = "#064E3B"

CATEGORIES = [
    "Food", "Transport", "Data & Airtime", "Education",
    "Entertainment", "Shopping", "Bills", "Savings",
    "Health", "Other",
]

CATEGORY_COLORS = {
    "Food": "#064E3B",
    "Transport": "#52796F",
    "Data & Airtime": "#1D6FA5",
    "Education": "#7FB069",
    "Entertainment": "#D6B779",
    "Shopping": "#B7791F",
    "Bills": "#68756D",
    "Savings": "#2D6A4F",
    "Health": "#C0392B",
    "Other": "#A9B5AD",
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

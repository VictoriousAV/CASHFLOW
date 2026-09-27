"""CashFlow AI — Phase 0+1 skeleton (mocked Daniel data)."""
import streamlit as st
from src.config import MOCK_USER, CATEGORIES, format_naira
from src.analytics import calc_balance, calc_avg_daily, calc_days_remaining, summarize_category_totals
from src.forecast import project_balance, forecast_message
from components.cards import metric_card, forecast_banner, ai_insight_card
from components.forms import add_transaction_form
from components.insights import top_category_insight

st.set_page_config(page_title="CashFlow AI", layout="wide")
st.title("CashFlow AI")
st.caption("Know where your money goes. Know how long it will last.")

MOCK_TXNS = [
    {"description": "Allowance", "amount": 70000, "type": "income", "category": "Other", "date": "2026-09-01"},
    {"description": "Uber", "amount": 2500, "type": "expense", "category": "Transport", "date": "2026-09-03"},
    {"description": "MTN Data", "amount": 2000, "type": "expense", "category": "Data & Airtime", "date": "2026-09-04"},
    {"description": "Chicken Republic", "amount": 4500, "type": "expense", "category": "Food", "date": "2026-09-05"},
    {"description": "Shoprite Food", "amount": 6000, "type": "expense", "category": "Food", "date": "2026-09-06"},
    {"description": "Bolt Trip", "amount": 3000, "type": "expense", "category": "Transport", "date": "2026-09-08"},
]

income = sum(t["amount"] for t in MOCK_TXNS if t["type"] == "income")
expenses = sum(t["amount"] for t in MOCK_TXNS if t["type"] == "expense")
balance = calc_balance(income, expenses)
days = len({t["date"] for t in MOCK_TXNS if t["type"] == "expense"})
avg_daily = calc_avg_daily(expenses, days) or float(MOCK_USER["avg_daily"])
days_left = calc_days_remaining(balance, avg_daily)
totals = summarize_category_totals(MOCK_TXNS)

tabs = st.tabs(["Dashboard", "Transactions", "Budget", "Savings Goals", "Forecast", "AI Coach", "Profile"])

with tabs[0]:
    st.subheader(f"Good morning, {MOCK_USER['name']} 👋")
    st.markdown(f"### {format_naira(balance)}")
    c1, c2, c3 = st.columns(3)
    with c1: metric_card("Income", income, "This month")
    with c2: metric_card("Expenses", expenses, f"avg {format_naira(int(avg_daily))}/day")
    with c3: metric_card("Savings", MOCK_USER["savings"], "Tracked")
    st.write("")
    forecast_banner(balance, avg_daily, days_left)
    st.write("")
    ai_insight_card(top_category_insight(totals) + " Spending up 18% vs last week.")
    st.write("**Spending by category**")
    st.bar_chart(totals)

with tabs[1]:
    st.subheader("Transactions")
    st.dataframe(MOCK_TXNS, use_container_width=True)
    add_transaction_form()

with tabs[2]:
    st.subheader("Budget (mock)")
    st.progress(0.85, text="Food — 85% of ₦20,000 used ⚠️")

with tabs[3]:
    st.subheader("Savings Goals (mock)")
    st.progress(0.30, text="New Laptop — ₦75,000 / ₦250,000 (30%)")

with tabs[4]:
    st.subheader("Forecast (estimate only)")
    st.info(forecast_message(balance, avg_daily, days_left))
    proj = project_balance(balance, avg_daily, 20)
    st.line_chart({f"+{d}d": v for d, v in proj})

with tabs[5]:
    st.subheader("AI Coach (mock)")
    q = st.text_input("Ask", "Can I afford ₦8,000 headphones?")
    if st.button("Ask"):
        st.write(f"With {format_naira(balance)} and {forecast_message(balance, avg_daily, days_left).lower()} "
                 f"— keep a 7-day buffer before spending.")

with tabs[6]:
    st.subheader("Profile")
    st.write(f"Name: {MOCK_USER['name']} | Monthly income: {format_naira(MOCK_USER['income'])}")

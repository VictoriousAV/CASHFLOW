"""Phase 1 forms stub."""
import streamlit as st
from src.config import CATEGORIES


def add_transaction_form():
    with st.form("add_txn"):
        desc = st.text_input("Description", "Chicken Republic")
        amount = st.number_input("Amount (₦)", min_value=1, value=4500)
        typ = st.selectbox("Type", ["Expense", "Income"])
        cat = st.selectbox("Category", CATEGORIES)
        date = st.date_input("Date")
        submitted = st.form_submit_button("Add")
        if submitted:
            st.success(f"Mock saved: {desc} — ₦{amount:,} ({typ}/{cat})")

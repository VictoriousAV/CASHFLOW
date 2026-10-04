"""CashFlow AI — full MVP (Phases 5-7: Track/Analyze/Predict, DB-backed)."""
import streamlit as st
from src.config import CATEGORIES, CATEGORY_COLORS, format_naira
from src.db import init_db
from src.users import create_user, authenticate, get_user
from src.transactions import (parse_csv_rows, create_transaction, list_transactions,
                              delete_transaction, import_transactions)
from src.analytics import dashboard_summary, generate_insights
from src.forecast import versioned_forecast
from src.budgets import set_budget, list_budgets, set_goal
from src import db as dbm
from src.charts import donut_figure, trend_figure, forecast_figure
from components.cards import metric_card, forecast_banner, ai_insight_card

st.set_page_config(page_title="CashFlow AI", layout="wide")
init_db()

# ---------- Auth (Phase 5) ----------
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if not st.session_state.user_id:
    st.title("CashFlow AI")
    st.caption("Know where your money goes. Know how long it will last.")
    tab1, tab2 = st.tabs(["Login", "Register"])
    with tab1:
        em = st.text_input("Email", key="li_em")
        pw = st.text_input("Password", type="password", key="li_pw")
        if st.button("Login"):
            u = authenticate(em, pw)
            if u:
                st.session_state.user_id = u["user_id"]
                st.rerun()
            else:
                st.error("Invalid credentials")
    with tab2:
        nm = st.text_input("Name", key="rg_nm")
        em2 = st.text_input("Email", key="rg_em")
        pw2 = st.text_input("Password", type="password", key="rg_pw")
        inc = st.number_input("Monthly income (₦, optional)", min_value=0, value=70000)
        if st.button("Create account"):
            try:
                u = create_user(nm, em2, pw2, monthly_income=int(inc))
                st.session_state.user_id = u["user_id"]
                st.rerun()
            except Exception as e:
                st.error(str(e))
    st.stop()

uid = st.session_state.user_id
user = get_user(uid) or {"name": "User"}
if st.sidebar.button("Logout"):
    st.session_state.user_id = None
    st.rerun()

# ---------- Data ----------
txns = list_transactions(uid)
s = dashboard_summary(txns)
budgets = list_budgets(uid)
for b in budgets:
    b["spent"] = sum(t["amount"] for t in txns
                     if t["type"] == "expense" and t["category"] == b["category"])
insights = generate_insights(s["totals"], s["wow"], budgets)
fc = versioned_forecast(s["balance"], s["avg_daily"])

tabs = st.tabs(["Dashboard", "Transactions", "Budget", "Savings Goals", "Forecast", "AI Coach", "Profile"])

with tabs[0]:  # ANALYZE
    st.subheader(f"Good morning, {user.get('name', 'User')} 👋")
    st.markdown(f"### {format_naira(s['balance'])}")
    c1, c2, c3 = st.columns(3)
    with c1: metric_card("Income", s["income"], "This month")
    with c2: metric_card("Expenses", s["expenses"], f"avg {format_naira(int(s['avg_daily']))}/day")
    with c3: metric_card("Savings", sum(t["amount"] for t in txns if t["category"] == "Savings"), "Tracked")
    st.write("")
    forecast_banner(s["balance"], s["avg_daily"], s["days_left"])
    st.write("")
    ai_insight_card(" ".join(insights) if insights else "Add transactions to unlock insights.")
    fig = donut_figure(s["totals"], CATEGORY_COLORS)
    if fig: st.plotly_chart(fig, use_container_width=True)
    else: st.bar_chart(s["totals"])
    tf = trend_figure(s["daily"])
    if tf: st.plotly_chart(tf, use_container_width=True)

with tabs[1]:  # TRACK
    st.subheader("Transactions")
    q = st.text_input("Search")
    fcat = st.selectbox("Category filter", [""] + CATEGORIES)
    view = [t for t in txns if q.lower() in t["description"].lower() and (not fcat or t["category"] == fcat)]
    st.dataframe(view, use_container_width=True)
    with st.form("add"):
        d = st.text_input("Description", "Chicken Republic")
        a = st.number_input("Amount (₦)", min_value=1, value=4500)
        t = st.selectbox("Type", ["Expense", "Income"])
        c = st.selectbox("Category", CATEGORIES)
        dt = st.date_input("Date")
        if st.form_submit_button("Add"):
            try:
                create_transaction(uid, {"description": d, "amount": int(a),
                                         "type": t.lower(), "category": c, "date": str(dt)})
                st.success("Saved"); st.rerun()
            except Exception as e:
                st.error(str(e))
    up = st.file_uploader("Upload CSV (Date,Description,Amount,Type, max 2MB)", type="csv")
    if up:
        if up.size > 2 * 1024 * 1024:
            st.error("CSV too large (2MB limit)")
        else:
            rows, errs = parse_csv_rows(up.read().decode("utf-8", "ignore"))
            for e in errs: st.error(e)
            if rows and st.button(f"Import {len(rows)} rows"):
                import_transactions(uid, rows); st.success("Imported"); st.rerun()
    for t in view[:20]:
        if st.button(f"Delete {t['description']} {format_naira(t['amount'])}", key=t["txn_id"]):
            delete_transaction(uid, t["txn_id"]); st.rerun()

with tabs[2]:  # Budgets
    st.subheader("Budgets")
    with st.form("bud"):
        bc = st.selectbox("Category", CATEGORIES)
        ba = st.number_input("Limit (₦)", min_value=1, value=20000)
        if st.form_submit_button("Set budget"):
            set_budget(uid, bc, int(ba)); st.rerun()
    for b in budgets:
        from src.analytics import calc_budget_usage
        pct = calc_budget_usage(b.get("spent", 0), b["amount"])
        st.progress(min(pct / 100, 1.0), text=f"{b['category']} — {format_naira(b.get('spent',0))} / {format_naira(b['amount'])} ({pct:.0f}%)")

with tabs[3]:  # Goals
    st.subheader("Savings Goals")
    with st.form("goal"):
        gn = st.text_input("Goal name", "New Laptop")
        gt = st.number_input("Target (₦)", min_value=1, value=250000)
        if st.form_submit_button("Create goal"):
            set_goal(uid, gn, int(gt)); st.rerun()
    conn = dbm.get_conn(); rows = conn.execute("SELECT * FROM goals WHERE user_id=?", (uid,)).fetchall(); conn.close()
    for g in rows:
        from src.analytics import calc_savings_progress
        p = calc_savings_progress(g["current_amount"], g["target_amount"])
        st.progress(min(p / 100, 1.0), text=f"{g['name']} — {format_naira(g['current_amount'])} / {format_naira(g['target_amount'])} ({p:.0f}%)")

with tabs[4]:  # PREDICT
    st.subheader("Forecast (estimate only)")
    st.info(fc["message"])
    st.caption(f"method={fc['inputs']['method']} • balance={format_naira(fc['inputs']['balance'])}")
    ff = forecast_figure(fc["projection"])
    if ff: st.plotly_chart(ff, use_container_width=True)
    else: st.line_chart({f"+{d}d": v for d, v in fc["projection"][:21]})

with tabs[5]:  # Phase 8 coach (wired in next step; fallback now)
    st.subheader("AI Coach")
    from src.ai_coach import answer
    qq = st.text_input("Ask", "Can I afford ₦8,000 headphones?")
    if st.button("Ask"):
        st.write(answer(qq, s["balance"], s["avg_daily"], s["days_left"], s["totals"]))

with tabs[6]:
    st.subheader("Profile")
    st.write(f"{user.get('name')} • {user.get('email')} • Income {format_naira(user.get('monthly_income', 0))}")

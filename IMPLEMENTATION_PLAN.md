# CashFlow AI — Implementation Plan

**Source:** `CashFlow_AI_PRD_Product_Bible.md` (v1, 29 sections) + `README.md`  
**Goal MVP:** Track → Analyze → Predict → Explain → Assist  
**Stack:** Streamlit + Python + Pandas + SQLite (→ Postgres) + Plotly + LLM API → Streamlit Cloud  
**Status:** No app code yet. This plan takes us from zero to hackathon demo to production-ready path.

---

## Phase 0 — Project Foundation (0.5 day)

**Objective:** Clean, runnable repo.

1. Confirm repo structure:
```text
/app.py                 # Streamlit entry, navigation
/src/
  config.py             # constants, categories, colors
  db.py                 # sqlite connection + init
  models.py             # dataclasses: User, Transaction, Budget, Goal
  auth.py               # register/login, bcrypt password_hash
  transactions.py       # CRUD + CSV import validation
  categorize.py         # rule-based categorizer v1
  analytics.py          # balance, category totals, avg daily, trends
  forecast.py           # days-remaining, balance projection
  budgets.py            # budget CRUD + usage %
  goals.py              # savings goals + progress %
  ai_context.py         # builds grounded JSON for LLM
  ai_coach.py           # LLM wrapper + system prompt + guardrails
  charts.py             # Plotly donut, line, forecast
/components/
  cards.py, forms.py, insights.py
/data/
  seed_daniel.csv       # ₦70k demo data
  schema.sql
/tests/
  test_analytics.py, test_forecast.py, test_categorize.py, test_csv.py
 requirements.txt
 .streamlit/config.toml # theme
 secrets.toml.example
```
2. `requirements.txt`: `streamlit, pandas, plotly, bcrypt, python-dotenv, openai|anthropic|groq (pick 1), pytest`
3. ADRs to lock:
   - ADR-001: Streamlit monolith for MVP (speed > scale)
   - ADR-002: SQLite via stdlib `sqlite3`, single `cashflow.db`, migrate to Postgres later via SQLAlchemy-ready schema
   - ADR-003: Never let LLM compute money; Python computes, LLM explains
   - ADR-004: Pandas for analysis, not for storage
4. Acceptance: `streamlit run app.py` renders empty dashboard; `pytest` passes.

---

## Phase 1 — Design System (1 day)

**Objective:** Modern, friendly, trustworthy UI per PRD §25.

**1.1 Tokens (`.streamlit/config.toml` + `src/config.py`):**
- Primary deep green `#0E7A5B`, secondary mint `#D9F2E6`, bg off-white `#FAFAF7`, text charcoal `#1F2937`, warning amber `#F59E0B`, danger red `#EF4444`
- Font: Inter/system, H1 28 bold, H2 20, body 15, figures 32 bold tabular-nums
- Radius 16px cards, 12px padding, whitespace > density, one primary metric per row on mobile

**1.2 Components:**
- `MetricCard(title, value₦, sub)` – balance large, income/expenses/savings small
- `ForecastBanner(days_remaining)` – “~17 days” + disclaimer “estimate, not guarantee”
- `AIInsightCard(text)` – 🤖 prefix, max 3 lines + “Ask coach →”
- `CategoryDonut`, `TrendLine`, `ForecastLine` (Plotly, matching palette)
- Forms: Add Transaction (description, amount>0, type, category dropdown, date ≤ today), Add Income, Budget, Goal

**1.3 IA / Navigation (PRD §10-11):**
`Dashboard | Transactions | Budget | Savings Goals | Forecast | AI Coach | Profile`
Top: “Good morning, Daniel 👋” + balance. Then summary row → donut + trend → forecast → AI insight.

**1.4 Deliverable:** Figma-less clickable Streamlit skeleton with mocked Daniel data (₦48,500 balance example). Acceptance: 5-sec comprehension test — where is money going + how long left visible without scroll on desktop.

---

## Phase 2 — Architecture Decisions (0.5 day)

```text
UI (Streamlit pages)
 ↓ calls
Service layer (transactions.py, budgets.py, goals.py, auth.py)
 ↓ calls
Engine layer (analytics.py, forecast.py, categorize.py) ← Pandas
 ↓ reads/writes
Data layer (db.py + SQLite)
 ↓ exports JSON
AI layer (ai_context.py → ai_coach.py → LLM API)
```

Key rules:
- All money as INTEGER kobo/naira minor units internally, format `₦48,500` only at display.
- `user_id` scoping on every query. No cross-user reads.
- CSV import is transactional: validate all rows, then insert, else reject with row errors.
- Forecast inputs versioned: `{balance, avg_daily, window_days, method:"mean_7d_v1"}` stored for explainability.
- Secrets via `st.secrets` / env, never in repo.

---

## Phase 3 — Data Layer (1 day)

**SQLite `schema.sql`:**
```sql
CREATE TABLE users(user_id TEXT PK, name TEXT, email UNIQUE, password_hash TEXT, monthly_income INTEGER, next_income_date TEXT, savings_goal INTEGER, created_at TEXT);
CREATE TABLE transactions(txn_id TEXT PK, user_id TEXT, description TEXT, amount INTEGER, type TEXT CHECK(type IN ('income','expense')), category TEXT, date TEXT, note TEXT, created_at TEXT, FOREIGN KEY(user_id) REFERENCES users);
CREATE TABLE budgets(budget_id TEXT PK, user_id TEXT, category TEXT, amount INTEGER, period TEXT DEFAULT 'monthly');
CREATE TABLE goals(goal_id TEXT PK, user_id TEXT, name TEXT, target_amount INTEGER, current_amount INTEGER DEFAULT 0, deadline TEXT);
CREATE INDEX idx_txn_user_date ON transactions(user_id, date);
```

Auth: bcrypt hash, session_state `user_id`, logout clears. Validation: amount>0, date parse `YYYY-MM-DD` + accept `DD/MM/YYYY` on CSV.

---

## Phase 4 — Financial Engine (1 day, core)

`analytics.py` (Pandas, PRD §17):
- `balance = income - expenses`
- `avg_daily = expenses / distinct_expense_days` (guard div/0 → 0, show “—”)
- `days_remaining = balance / avg_daily if avg_daily>0 else None`
- Category totals, WoW % change, top category, weekly target breach

`categorize.py` v1 rules + keyword map:
```python
KEYWORDS = {"mtn|glo|airtel|data": "Data & Airtime", "uber|bolt|keke|bus": "Transport", "chicken|kfc|shoprite|food": "Food", ...}
# fallback: "Other" + confidence; allow user correction → store override
```
Log corrections for future ML.

`forecast.py`:
- `project(balance, avg_daily, days=30) -> [(day, balance - avg*d)]` floored at 0
- Output strings always: “may last approximately X days at your current rate.”

Tests with Daniel seed: Income 70k, expenses 21.5k → balance 48.5k, avg 2.8k → ~17 days.

---

## Phase 5 — TRACK: Input Features (1 day)

1. Register/Login + onboarding (income, next payday, savings goal optional)
2. Add Transaction form + edit/delete + user correction of category
3. CSV Upload: columns `Date,Description,Amount,Type`, sample:
```csv
Date,Description,Amount,Type
01/09/2026,Allowance,70000,Income
03/09/2026,Uber,2500,Expense
```
Show preview → auto-category → confirm → insert. Reject bad rows with messages.
4. Transactions page: search, filter by category/type/date, sort.

Acceptance: PRD functional req 1-5 pass.

---

## Phase 6 — ANALYZE: Dashboard + Insights (1 day)

Dashboard binds engine → UI:
- Metrics: balance, income, expenses, savings, avg daily, days remaining
- Donut (category share), Line (daily spend trend)
- Insight generator (deterministic, no LLM needed):
  - “Food is your largest expense this month.”
  - “Spending up 18% vs last week.”
  - “⚠️ 85% of food budget used.”

---

## Phase 7 — PREDICT: Forecast, Budget, Goals (1 day)

- Forecast page: big number + table (Today, +5/10/15/20d) + Plotly declining line to zero. Disclaimer footer.
- Budget CRUD per category + progress bars + warnings at 80/100%.
- Goals CRUD + `% = saved/target*100` + suggestion hook (“Cut entertainment ₦2k → goal 4 days earlier”).

Acceptance: PRD req 6-11 pass.

---

## Phase 8 — EXPLAIN + ASSIST: AI Coach (1.5 days)

`ai_context.py` builds:
```text
Current balance: ₦48,500
Average daily spending: ₦2,800
Food: ₦12,000 | Transport: ₦7,500 | Entertainment: ₦4,000
Estimated remaining: 17 days | Savings goal: ₦100,000
```

System prompt must enforce:
- Use only provided data, don’t invent txns, say “I don’t have that” when missing
- Forecasts = estimates, explain formula `Balance ÷ Avg Daily`
- No licensed advice, no high-risk investments, plain language, ₦ formatting
- Affordability check: compare purchase vs balance + days-left impact

UI: chat history, suggested chips (“Where am I spending most?”, “Can I afford ₦8,000 headphones?”, “How to make ₦30k last 2 weeks?”), show data snapshot expander for trust.

Fallback if no API key: rule-based responder using same context (keeps demo alive offline).

---

## Phase 9 — Quality, Security, Performance (0.5 day)

- Tests: analytics edge (0 spend, 0 balance), forecast math, categorizer keywords, CSV malformed, budget 85% trigger, auth scoping.
- Security: parameterized SQL, bcrypt, per-user checks, CSV size limit 2MB, LLM never sees password/hash.
- Perf: dashboard <1.5s on 5k txns (Pandas agg + indexed SQLite); cache with `st.cache_data`.
- A11y/responsive: mobile single-column, clear language, no jargon.

---

## Phase 10 — Seed, Demo, Deploy (0.5 day)

- `seed_daniel.csv` reproduces PRD §22: 70k in, ~40k out across Food 15k/Transport 8k/Data 4k/Entertainment 5k/Education 3k/Other 5k → 30k balance, 2.5k/day → 12 days.
- Demo script (PRD §26): Hook (“You get ₦70k… how long will it last?”) → Add income → Upload → Dashboard → Forecast → AI insight → “Can I spend ₦8k today?” → Closer: “Not just where money went, but what it means for tomorrow.”
- Deploy Streamlit Cloud, set secrets, test cold start. Tag `v0.1-mvp`.

Success metrics to log: users, txns, CSV uploads, AI questions, % who find top category / set budget, forecast views.

---

## Phase 11 — Post-MVP (roadmap)

**Phase 2:** better forecasting (7/14/30-day weighted, payday-aware), alerts, weekly summaries, receipt scan stub.  
**Phase 3:** Postgres + SQLAlchemy, bank API, mobile (Flutter/React Native wrapper), voice, ML time-series after >90 days data, multi-currency, shared budgets.

**Risks:** LLM hallucination → grounded context + tests; irregular income → payday-aware forecast; categorization errors → one-tap correction; privacy → minimal retention + clear disclaimers.

---

## Build Order Checklist

- [ ] 0 Repo + reqs + ADRs
- [ ] 1 Theme + skeleton + mocked dashboard
- [ ] 2 DB schema + auth
- [ ] 3 Engine + tests (analytics/forecast/categorize)
- [ ] 4 Transactions + CSV
- [ ] 5 Dashboard + charts + insights
- [ ] 6 Forecast + budgets + goals
- [ ] 7 AI context + coach + guardrails
- [ ] 8 Polish + tests + seed
- [ ] 9 Deploy + demo rehearsal

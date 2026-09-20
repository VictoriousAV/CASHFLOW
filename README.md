# CashFlow AI
### *Know where your money goes. Know how long it will last.*

CashFlow AI is an AI-powered personal finance platform that helps users track their money, understand their spending, estimate how long their balance may last, and make more informed everyday financial decisions.

> Full product specification: [`CashFlow_AI_PRD_Product_Bible.md`](./CashFlow_AI_PRD_Product_Bible.md)

---

## Problem

People often know their current bank balance but don't know what it means for the rest of the month:

- Where did my money go?
- What am I spending the most on?
- Can my remaining money last until my next income?
- Can I afford a particular purchase?
- How much can I safely save?

Traditional budgeting tools focus on recording history. CashFlow AI combines financial data with analysis and forecasting to answer **what is happening, what may happen next, and what the user can do about it.**

## Target Users

**Primary:** Students, young adults, and early-career professionals with limited or irregular income (allowance, salary, freelance, family support, scholarships).

**Secondary:** Young professionals who want simple spending awareness without complex finance tools.

Example persona: Daniel, 21, university student, ₦70,000/month — money often finishes before next allowance. His core question: *“Will this money last me until my next allowance?”*

## How It Works

```text
Sign Up
  ↓
Add Income
  ↓
Add / Upload Transactions
  ↓
Automatic Categorization
  ↓
Financial Analysis
  ↓
Dashboard
  ↓
Spending Insights
  ↓
Balance Forecast
  ↓
AI Financial Coach
  ↓
Better Everyday Decisions
```

MVP focus in 5 steps: **Track → Analyze → Predict → Explain → Assist**

## Main Features

1. **User Registration** – name, email, password + optional income, next income date, savings goal.
2. **Add Transaction** – description, amount, type (Income/Expense), category, date, note.
3. **CSV Upload** – bulk import `Date, Description, Amount, Type` for fast onboarding.
4. **Automatic Categorization** – Food, Transport, Data & Airtime, Education, Entertainment, Shopping, Bills, Savings, Health, Other.
5. **Financial Dashboard** – balance, income, expenses, savings, average daily spend, estimated days remaining + donut and trend charts.
6. **Spending Analysis** – plain-language insights, e.g. “Food is your largest expense this month.”
7. **Money Duration Forecast (signature feature)** – `Current Balance ÷ Average Daily Spending = Estimated Days Remaining`. Always labeled as an estimate.
8. **Balance Forecast** – projected balance over time with chart.
9. **Budget Management** – per-category limits with usage warnings (e.g. 85% of food budget used).
10. **Savings Goals** – target tracking with progress and suggestions.
11. **AI Financial Coach** – natural-language Q&A grounded in calculated user data, e.g. “Can I afford ₦8,000 headphones?”

## AI Architecture

Financial calculations are **not** left to the LLM. Python computes the facts, the LLM explains them:

```text
USER DATA → Transaction Engine → Financial Calculations
  → Analytics Engine + Forecast Engine → AI Context → AI Financial Coach
```

The AI receives calculated context (balance, avg daily spend, category totals, days remaining) and must use that data, explain clearly, avoid inventing transactions, label forecasts as estimates, and avoid posing as a licensed adviser.

Core calculations:
- `Balance = Total Income - Total Expenses`
- `Average Daily Spending = Total Expenses ÷ Spending Days`
- `Estimated Days Remaining = Current Balance ÷ Average Daily Spending`
- `Budget Usage = Spent ÷ Limit × 100`
- `Savings Progress = Saved ÷ Target × 100`

## Tech Stack

- **Frontend:** Streamlit (MVP)
- **Backend:** Python
- **Data:** Pandas
- **DB:** SQLite (MVP) → PostgreSQL (production)
- **Charts:** Plotly
- **AI:** LLM API for explanations, Q&A, categorization assist
- **Deploy:** Streamlit Community Cloud
- **Version Control:** GitHub

## Project Structure

```text
QUABATORS FOLD/
├── CashFlow_AI_PRD_Product_Bible.md  # Product Bible / PRD (v1)
├── README.md                         # This file
└── .git/                             # Scoped git repo for this project
```

No app code yet — current version is PRD + README only.

## Roadmap

- **Phase 1 – Hackathon MVP:** auth, manual entry, CSV upload, categorization, dashboard, budget, basic forecast, AI Coach
- **Phase 2 – Improved:** better forecasting, alerts, savings goals, weekly reports, receipt scanning
- **Phase 3 – Production:** bank integrations, mobile app, voice assistant, ML forecasting, multi-currency, shared budgeting

## Trust & Safety

Decision-support tool only, not a financial adviser. Forecasts are estimates, never guarantees. Users own their data, can correct categories, and high-risk investment advice is out of scope.

## Success = Answering 3 Questions

1. “Where is my money going?”
2. “How long might my money last?”
3. “What can I do about it?”

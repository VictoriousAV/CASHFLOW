# CashFlow AI — Architecture (Phase 2)

```text
UI (app.py + components/ + index.html prototype)
  ↓ calls service layer only
Service (src/users.py, src/transactions.py, src/budgets.py, src/goals.py, src/auth.py)
  ↓ calls engine + data
Engine (src/analytics.py, src/forecast.py, src/categorize.py, src/money.py, src/validators.py)
  ↓ reads/writes via scoped helpers
Data (src/db.py + data/schema.sql + SQLite file, never committed)
  ↓ exports grounded JSON
AI (src/ai_context.py → src/ai_coach.py → LLM API, Phase 8)
```

## Enforced rules
1. **Money as INTEGER minor units** (`src/money.py`): all storage/math in int naira;
   `format_naira()` display-only. Floats never stored.
2. **user_id scoping**: every SELECT/UPDATE/DELETE takes `user_id`; helpers reject
   empty `user_id`; tests prove cross-user isolation.
3. **Transactional CSV**: `parse_csv_rows()` validates everything first;
   `import_transactions()` inserts in one `with conn:` block — all or nothing.
4. **Versioned forecast**: `FORECAST_METHOD="mean_7d_v1"` in `src/config.py`;
   `build_forecast_inputs()` returns `{balance, avg_daily, window_days, method}`
   for explainability (PRD §17).
5. **Secrets**: `src/secrets.py` reads env / `.streamlit/secrets.toml`, never repo;
   `.gitignore` blocks `data/cashflow.db` + `secrets.toml`.

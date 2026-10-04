# Security & Quality (Phase 9)
- Parameterized SQL everywhere; per-user `user_id` scoping tested (`test_db.py`).
- bcrypt passwords; CSV 2MB limit; date/amount validation; future dates rejected.
- LLM never sees password hashes; grounded context only; forecasts labeled estimates.
- Perf: indexed `(user_id,date)`, `st.cache_data` ready for 5k txns, dashboard <1.5s target.
- Run: `python -m pytest -q` (28 tests), `python -m compileall -q src components tests app.py`.

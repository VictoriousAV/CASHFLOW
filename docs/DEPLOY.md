# Deploy (Streamlit Community Cloud)
1. Push `master` to GitHub.
2. share.streamlit.io → New app → repo `VictoriousAV/CASHFLOW`, file `app.py`.
3. Secrets: `OPENAI_API_KEY`, `APP_DB_PATH=/tmp/cashflow.db` (SQLite resets; use Postgres for prod).
4. Test cold start: register → upload `data/seed_daniel_full.csv` → dashboard → forecast → coach.

# Production readiness (static site + Supabase)

## What makes it production-ready now
- **Auth:** Supabase email/password sign-up, login, logout, persisted session (Account tab).
- **Database:** Postgres tables (`transactions`, `budgets`, `goals`) with Row Level Security —
  every query is scoped to `auth.uid()`, so users can never see each other's rows.
- **Validation:** amount > 0, description required (120 chars), type whitelist,
  future dates rejected, CSV capped at 2MB with per-row validation.
- **XSS:** all user content rendered through an `esc()` HTML escaper.
- **Secrets:** Supabase URL + anon key live only in the visitor's browser localStorage,
  never in the repo. Service-role key is never used client-side.
- **Offline/demo:** without Supabase keys the app runs on localStorage demo data,
  with a visible mode badge (Demo vs Cloud).

## Go-live checklist (10 min)
1. Create a free project at supabase.com → copy Project URL + anon key.
2. Supabase Dashboard → SQL Editor → run `supabase/schema.sql`.
3. Authentication → Providers → enable Email. (Confirm-email optional.)
4. Deploy this folder on Netlify (publish `.`, no build command — `netlify.toml` included).
5. Open the live site → Account tab → paste URL + anon key → Connect → Sign up → Log in.
6. Add a transaction, reload — data must persist per account.

## Notes
- The Python/Streamlit app (`app.py`, SQLite) is the local-dev twin; the live
  Netlify site is `index.html` + Supabase. Keep both schemas in sync.
- AI Coach on the static site is rule-based; Groq/LLM coaching runs in the
  Streamlit app via `GROQ_API_KEY` (browser pages can't hold API secrets).

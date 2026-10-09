-- CashFlow AI — Supabase (Postgres) schema with per-user RLS.
-- Run in Supabase Dashboard → SQL Editor. Auth uses Supabase Auth (email/password).

create table if not exists public.transactions (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade,
  description text not null check (char_length(description) between 1 and 120),
  amount integer not null check (amount > 0),
  type text not null check (type in ('income','expense')),
  category text not null default 'Other',
  date date not null default current_date,
  note text not null default '',
  created_at timestamptz not null default now()
);
create index if not exists idx_txn_user_date on public.transactions(user_id, date);

create table if not exists public.budgets (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade,
  category text not null,
  amount integer not null check (amount > 0),
  period text not null default 'monthly',
  unique(user_id, category)
);

create table if not exists public.goals (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade,
  name text not null,
  target_amount integer not null check (target_amount > 0),
  current_amount integer not null default 0 check (current_amount >= 0),
  deadline date
);

alter table public.transactions enable row level security;
alter table public.budgets enable row level security;
alter table public.goals enable row level security;

-- Users can only touch their own rows.
create policy "own txns" on public.transactions for all using (auth.uid() = user_id) with check (auth.uid() = user_id);
create policy "own budgets" on public.budgets for all using (auth.uid() = user_id) with check (auth.uid() = user_id);
create policy "own goals" on public.goals for all using (auth.uid() = user_id) with check (auth.uid() = user_id);

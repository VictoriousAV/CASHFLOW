CREATE TABLE IF NOT EXISTS users(
  user_id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL,
  password_hash TEXT NOT NULL,
  monthly_income INTEGER DEFAULT 0,
  next_income_date TEXT DEFAULT '',
  savings_goal INTEGER DEFAULT 0,
  created_at TEXT DEFAULT ''
);
CREATE TABLE IF NOT EXISTS transactions(
  txn_id TEXT PRIMARY KEY,
  user_id TEXT NOT NULL,
  description TEXT NOT NULL,
  amount INTEGER NOT NULL CHECK(amount > 0),
  type TEXT NOT NULL CHECK(type IN ('income','expense')),
  category TEXT DEFAULT 'Other',
  date TEXT DEFAULT '',
  note TEXT DEFAULT '',
  created_at TEXT DEFAULT '',
  FOREIGN KEY(user_id) REFERENCES users(user_id)
);
CREATE TABLE IF NOT EXISTS budgets(
  budget_id TEXT PRIMARY KEY,
  user_id TEXT NOT NULL,
  category TEXT NOT NULL,
  amount INTEGER NOT NULL CHECK(amount > 0),
  period TEXT DEFAULT 'monthly',
  FOREIGN KEY(user_id) REFERENCES users(user_id)
);
CREATE TABLE IF NOT EXISTS goals(
  goal_id TEXT PRIMARY KEY,
  user_id TEXT NOT NULL,
  name TEXT NOT NULL,
  target_amount INTEGER NOT NULL CHECK(target_amount > 0),
  current_amount INTEGER DEFAULT 0,
  deadline TEXT DEFAULT '',
  FOREIGN KEY(user_id) REFERENCES users(user_id)
);
CREATE INDEX IF NOT EXISTS idx_txn_user_date ON transactions(user_id, date);

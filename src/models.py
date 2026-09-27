"""Dataclasses mirroring data/schema.sql."""
from dataclasses import dataclass


@dataclass
class User:
    user_id: str
    name: str
    email: str
    password_hash: str = ""
    monthly_income: int = 0
    next_income_date: str = ""
    savings_goal: int = 0
    created_at: str = ""


@dataclass
class Transaction:
    txn_id: str
    user_id: str
    description: str
    amount: int
    type: str  # income | expense
    category: str = "Other"
    date: str = ""
    note: str = ""
    created_at: str = ""


@dataclass
class Budget:
    budget_id: str
    user_id: str
    category: str
    amount: int
    period: str = "monthly"


@dataclass
class Goal:
    goal_id: str
    user_id: str
    name: str
    target_amount: int
    current_amount: int = 0
    deadline: str = ""

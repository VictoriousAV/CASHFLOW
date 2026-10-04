from src.ai_coach import answer, SYSTEM_PROMPT


def test_affordability_mentions_buffer():
    a = answer("Can I afford 8000 headphones?", 30000, 2500.0, 12, {"Food": 15000})
    assert "buffer" in a.lower() or "estimate" in a.lower()


def test_no_invented_txn_numbers():
    a = answer("Where am I spending most?", 10000, 1000.0, 10, {"Food": 5000})
    assert "Food" in a and "₦5,000" in a


def test_empty_data_safe():
    a = answer("hello?", 0, 0.0, None, {})
    assert "Add some expenses" in a


def test_system_prompt_guardrails():
    p = SYSTEM_PROMPT.lower()
    assert "only" in p and "estimate" in p and "not a licensed" in p

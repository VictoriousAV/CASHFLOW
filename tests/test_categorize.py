from src.categorize import categorize


def test_food():
    assert categorize("Chicken Republic") == "Food"


def test_transport():
    assert categorize("Uber Trip") == "Transport"


def test_data():
    assert categorize("MTN Data") == "Data & Airtime"


def test_fallback():
    assert categorize("xyz unknown") == "Other"

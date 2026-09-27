from src.transactions import parse_csv_rows


def test_valid_csv():
    txt = "Date,Description,Amount,Type\n01/09/2026,Allowance,70000,Income\n03/09/2026,Uber,2500,Expense"
    rows, errs = parse_csv_rows(txt)
    assert errs == [] and len(rows) == 2
    assert rows[1]["category"] == "Transport"


def test_missing_cols():
    rows, errs = parse_csv_rows("a,b\n1,2")
    assert rows == [] and errs

"""Phase 3 isolation tests — temp SQLite per test."""
import tempfile, os
import pytest
from src.db import init_db
from src.users import create_user, authenticate
from src.transactions import (create_transaction, list_transactions,
                              delete_transaction, import_transactions, parse_csv_rows)


@pytest.fixture
def dbpath():
    fd, p = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    init_db(p)
    yield p
    try:
        os.remove(p)
    except OSError:
        pass


def test_user_auth(dbpath):
    u = create_user("Daniel", "d@test.co", "secret123", path=dbpath)
    assert authenticate("d@test.co", "secret123", path=dbpath)["user_id"] == u["user_id"]
    assert authenticate("d@test.co", "badpass", path=dbpath) is None
    with pytest.raises(ValueError):
        create_user("X", "d@test.co", "secret123", path=dbpath)


def test_txn_isolation_and_crud(dbpath):
    a = create_user("A", "a@t.co", "secret123", path=dbpath)["user_id"]
    b = create_user("B", "b@t.co", "secret123", path=dbpath)["user_id"]
    t = create_transaction(a, {"description": "Uber", "amount": 2500,
                               "type": "expense", "date": "2026-09-03"}, path=dbpath)
    assert t["category"] == "Transport"
    assert len(list_transactions(a, path=dbpath)) == 1
    assert list_transactions(b, path=dbpath) == []
    assert not delete_transaction(b, t["txn_id"], path=dbpath)  # cross-user blocked
    assert delete_transaction(a, t["txn_id"], path=dbpath)


def test_csv_transactional(dbpath):
    u = create_user("C", "c@t.co", "secret123", path=dbpath)["user_id"]
    rows, errs = parse_csv_rows("Date,Description,Amount,Type\n01/09/2026,Allowance,70000,Income")
    assert errs == [] and import_transactions(u, rows, path=dbpath) == 1
    bad = [{"description": "", "amount": -5, "type": "expense", "date": "bad"}]
    with pytest.raises(ValueError):
        import_transactions(u, bad, path=dbpath)
    assert len(list_transactions(u, path=dbpath)) == 1  # rollback held

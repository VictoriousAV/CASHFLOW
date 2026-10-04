"""Auth with bcrypt (Phase 3). Falls back to sha256 only if bcrypt missing."""
import hashlib
from datetime import datetime, timezone

try:
    import bcrypt as _bcrypt
except ImportError:  # pragma: no cover
    _bcrypt = None


def hash_password(password: str) -> str:
    if not password or len(password) < 6:
        raise ValueError("password must be >= 6 chars")
    if _bcrypt:
        return _bcrypt.hashpw(password.encode(), _bcrypt.gensalt()).decode()
    return "sha256$" + hashlib.sha256(password.encode()).hexdigest()


def verify_password(password: str, hashed: str) -> bool:
    try:
        if hashed.startswith("$2"):
            return _bcrypt.checkpw(password.encode(), hashed.encode())
        if hashed.startswith("sha256$"):
            return hashed == "sha256$" + hashlib.sha256(password.encode()).hexdigest()
        return False
    except Exception:
        return False


def utcnow() -> str:
    return datetime.now(timezone.utc).isoformat()

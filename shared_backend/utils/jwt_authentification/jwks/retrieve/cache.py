import json
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import cast

from django.conf import settings

CACHE_FILE = Path(getattr(settings, "BASE_DIR", "/")) / ".cache" / "jwks.json"


def is_jwks_stale(max_age_hours: int = 24) -> bool:
    """Check if cached JWKS is older than max_age_hours"""
    if not CACHE_FILE.exists():
        return True

    file_age = datetime.now(UTC) - datetime.fromtimestamp(CACHE_FILE.stat().st_mtime, UTC)
    return file_age > timedelta(hours=max_age_hours)


def load_jwks_from_cache() -> dict[str, list[dict[str, str]]] | None:
    """Load JWKS from cache file"""
    try:
        if CACHE_FILE.exists():
            with open(CACHE_FILE, encoding="utf-8") as f:
                return cast(dict[str, list[dict[str, str]]], json.load(f))
    except (json.JSONDecodeError, OSError):
        pass
    return None


def save_jwks_to_cache(jwks: dict[str, list[dict[str, str]]]) -> None:
    """Save JWKS to cache file"""
    try:
        # Create parent directory if it doesn't exist
        CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(jwks, f, indent=2)
    except OSError:
        pass  # Fail silently if can't write cache

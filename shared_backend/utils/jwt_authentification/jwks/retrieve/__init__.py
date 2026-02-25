from .cache import is_jwks_stale, load_jwks_from_cache, save_jwks_to_cache
from .provider import fetch_jwks_from_provider


def get_jwks(force_refresh: bool = False) -> dict[str, list[dict[str, str]]]:
    """
    Fetch JWKS from auth provider or cache.
    - Checks file cache first (unless force_refresh=True)
    - Refetches if cache is older than 24 hours
    """
    # Try to load from cache if not stale and not forcing refresh
    if not force_refresh and not is_jwks_stale(max_age_hours=24):
        cached_jwks = load_jwks_from_cache()
        if cached_jwks:
            return cached_jwks

    jwks = fetch_jwks_from_provider()
    save_jwks_to_cache(jwks)
    return jwks


__all__ = ["get_jwks"]

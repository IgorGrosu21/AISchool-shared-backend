from typing import cast

from django.core.cache import cache

CACHE_KEY_PREFIX = "service_token_"
CACHE_TIMEOUT = 24 * 60 * 60


class TokenStorage:
    _service_id: str

    def __init__(self, service_id: str):
        self._service_id = service_id

    @property
    def cache_key(self) -> str:
        return f"{CACHE_KEY_PREFIX}{self._service_id}"

    def get_token(self) -> str | None:
        return cast(str | None, cache.get(self.cache_key))

    def set_token(self, token: str) -> None:
        cache.set(self.cache_key, token, CACHE_TIMEOUT)

    def clear_cache(self) -> None:
        cache.delete(self.cache_key)

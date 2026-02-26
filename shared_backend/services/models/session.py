import atexit
from typing import Any

import requests
from requests.adapters import HTTPAdapter
from requests.exceptions import ConnectionError, RequestException, Timeout
from urllib3.util.retry import Retry

from shared_backend.utils.exceptions import BadRequest, InternalServerError

RETRY_STRATEGY = Retry(
    total=2,
    backoff_factor=0.3,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["POST"],
)

ADAPTER = HTTPAdapter(
    max_retries=RETRY_STRATEGY,
    pool_connections=10,
    pool_maxsize=20,
)


def _create_session() -> requests.Session:
    session = requests.Session()

    session.mount("http://", ADAPTER)
    session.mount("https://", ADAPTER)

    return session


class Session:
    _instance: requests.Session | None = None
    _headers: dict[str, str | None]
    _headers_with_token: dict[str, str | None]

    def __init__(self):
        self._headers = {"Content-Type": "application/json"}
        self._headers_with_token = {**self._headers, "Authorization": None}
        self._recreate_session()

        atexit.register(self.close)

    def _recreate_session(self) -> None:
        if self._instance is not None:
            try:
                self._instance.close()
            except Exception:
                pass
        self._instance = _create_session()

    def set_auth_token(self, token: str) -> None:
        self._headers_with_token["Authorization"] = f"Bearer {token}"

    def _build_headers(self, use_token: bool, language: str | None = None) -> dict[str, str | None]:
        """Build headers with optional token and language."""
        headers = (self._headers_with_token if use_token else self._headers).copy()
        if language:
            headers["Accept-Language"] = language
        return headers

    def post(
        self,
        url: str,
        data: dict[str, Any] | list[Any],
        use_token: bool = True,
        language: str | None = None,
    ) -> tuple[dict[str, Any] | None, str]:
        headers = self._build_headers(use_token, language)
        if headers.get("Authorization") is None and use_token:
            raise BadRequest("Authorization token is not set")

        if self._instance is None:
            raise InternalServerError("Session is not initialized")

        try:
            response = self._instance.post(url, json=data, headers=headers, timeout=10)
        except (ConnectionError, Timeout):
            self._recreate_session()
            try:
                return self.post(url, data, use_token, language)
            except Exception as retry_e:
                raise InternalServerError(
                    f"Failed to send request to {url} after session refresh: {str(retry_e)}"
                ) from retry_e
        except RequestException as e:
            raise InternalServerError(f"Request failed for {url}: {str(e)}") from e
        except Exception as e:
            raise InternalServerError(f"Failed to send request to {url}: {str(e)}") from e

        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            if e.response.status_code in [401, 403]:
                return None, "unauthorized"
            # Try to parse error response, but handle empty responses
            try:
                error_data = e.response.json() if e.response.content else {}
                return None, str(error_data)
            except (ValueError, AttributeError):
                return None, "error"

        # Handle empty responses (e.g., 204 No Content)
        if response.status_code == 204 or not response.content:
            return {}, "success"

        return response.json(), "success"

    def close(self) -> None:
        if self._instance is not None:
            self._instance.close()
            self._instance = None

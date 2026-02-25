from shared_backend.utils.exceptions import InternalServerError


def fetch_jwks_from_provider() -> dict[str, list[dict[str, str]]]:
    """Fetch JWKS from auth provider."""
    try:
        from shared_backend.services.models import Client

        url = Client.build_url("auth-service", ".well-known/jwks.json")
        return Client.send_request(url, {})
    except Exception as e:
        raise InternalServerError(
            f"Failed to fetch public keys from auth provider: {str(e)}"
        ) from e

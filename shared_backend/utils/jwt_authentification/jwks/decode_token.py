from typing import cast

import jwt
from rest_framework.exceptions import AuthenticationFailed

from .public_key import get_public_key_for_token


def decode_token(token: str, force_refresh: bool = False) -> dict[str, str]:
    """
    Verify JWT token signature and decode it.
    Automatically retries with fresh JWKS if signature verification fails.
    Returns decoded token payload.
    """
    # First attempt: Get public key for token (raises AuthenticationFailed on error)
    public_key = get_public_key_for_token(token, force_refresh)

    try:
        decoded_token = jwt.decode(
            token,
            public_key,
            algorithms=["RS256"],
            options={
                "verify_signature": True,
                "verify_exp": True,
            },
        )
        return cast(dict[str, str], decoded_token)
    except jwt.ExpiredSignatureError as e:
        raise AuthenticationFailed("Token has expired") from e
    except jwt.InvalidTokenError as e:
        # If signature verification fails, try refreshing JWKS and retry
        # This handles the case where keys have been rotated but cache hasn't expired
        error_str = str(e)
        if (
            "Signature verification failed" in error_str or "Invalid token" in error_str
        ) and not force_refresh:
            return decode_token(token, force_refresh=True)
        raise AuthenticationFailed(f"Invalid token: {error_str}") from e

from typing import Any

import jwt
from jwt.algorithms import RSAAlgorithm
from rest_framework.exceptions import AuthenticationFailed

from .retrieve import get_jwks


def get_public_key_for_token(token: str, force_refresh: bool = False) -> Any:
    """
    Get the appropriate RSA public key for a token.
    Returns RSA key object or raises AuthenticationFailed if not found.
    """
    try:
        # Decode header to get key ID (kid)
        unverified_header = jwt.get_unverified_header(token)
        kid = unverified_header.get("kid")

        # Fetch JWKS (cached, or force refresh if requested)
        try:
            jwks: dict[str, list[dict[str, str]]] = get_jwks(force_refresh=force_refresh)
        except ValueError as e:
            raise AuthenticationFailed(str(e)) from e

        if "keys" not in jwks or not jwks["keys"]:
            raise AuthenticationFailed("No public keys found in JWKS")

        # Find key by kid
        key_data = None
        if kid:
            for key in jwks["keys"]:
                if key.get("kid") == kid:
                    key_data = key
                    break

        # Fallback to first key if no kid match
        if not key_data and jwks["keys"]:
            key_data = jwks["keys"][0]

        if not key_data:
            raise AuthenticationFailed("No matching public key found for token")

        # Convert JWK to RSA key (requires cryptography)
        try:
            return RSAAlgorithm.from_jwk(key_data)
        except Exception as e:
            raise AuthenticationFailed(f"Unable to convert JWK to RSA key: {str(e)}") from e

    except AuthenticationFailed:
        raise
    except Exception as e:
        raise AuthenticationFailed(f"Failed to get public key: {str(e)}") from e

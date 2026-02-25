from uuid import UUID

from django.apps import apps
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.request import Request

from shared_backend.api.models import AuthenticateableUser

from .jwks.decode_token import decode_token


class JWTUserAuthentication(BaseAuthentication):
    """
    DRF Base Authentication class for external JWT tokens.
    Verifies JWT tokens using RSA public key from auth service
    and authenticates users or services by id (from 'auth_id' or 'service_id' claim in JWT).
    Subclasses should implement the authenticate method to handle the specific token type.
    """

    token_type: str | None = None
    model: type[AuthenticateableUser] | None = None

    def decode_token(self, token: str) -> dict[str, str]:
        return decode_token(token)

    def serialize_payload(self, payload: dict[str, str]) -> AuthenticateableUser:
        if self.model is None:
            raise ValueError("Model is not set")
        user_claim = self.model.user_claim_key

        try:
            user = self.model.objects.get(**{user_claim: UUID(payload.get(user_claim))})
        except self.model.DoesNotExist:
            user = self.model(**{user_claim: UUID(payload.get(user_claim))})
            user.is_anonymous = True
        return user

    def authenticate(self, request: Request) -> tuple[AuthenticateableUser, str] | None:
        """
        Authenticate the request and return a two-tuple of (auth_id or service_id, token).
        Returns None if no authentication credentials are provided or the token is invalid.
        """
        auth_header: str = request.META.get("HTTP_AUTHORIZATION", "")

        if not auth_header.startswith("Bearer "):
            return None

        token = auth_header.split(" ")[1]
        try:
            # Verify and decode token
            payload = self.decode_token(token)

            token_type = payload.get("type")
            if self.model is None:
                self.model = apps.get_model("api", "User")
            if self.token_type is None:
                self.token_type = self.model.authentication_token_type

            if token_type != self.token_type:
                raise AuthenticationFailed(f"Token is not a {self.token_type} token")

            return (self.serialize_payload(payload), token)

        except AuthenticationFailed:
            raise
        except Exception as e:
            raise AuthenticationFailed(f"Authentication failed: {str(e)}") from e

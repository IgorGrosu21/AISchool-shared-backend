from typing import TYPE_CHECKING

from drf_spectacular.extensions import OpenApiAuthenticationExtension

if TYPE_CHECKING:
    from drf_spectacular.openapi import AutoSchema


class JWTUserAuthSchemeExtension(OpenApiAuthenticationExtension):  # type: ignore[no-untyped-call]
    target_class = "shared_backend.utils.jwt_authentification.JWTUserAuthentication"
    name = "JWTUserAuth"

    def get_security_definition(self, auto_schema: "AutoSchema") -> dict[str, str]:
        return {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "JWT Authorization header using the Bearer scheme.",
        }


class JWTServiceAuthSchemeExtension(OpenApiAuthenticationExtension):  # type: ignore[no-untyped-call]
    target_class = "shared_backend.utils.jwt_authentification.JWTServiceAuthentication"
    name = "JWTServiceAuth"

    def get_security_definition(self, auto_schema: "AutoSchema") -> dict[str, str]:
        return {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "JWT Authorization header using the Bearer scheme.",
        }

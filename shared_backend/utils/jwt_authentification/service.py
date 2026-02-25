from shared_backend.utils.exceptions import NotFound

from .user import JWTUserAuthentication


class JWTServiceAuthentication(JWTUserAuthentication):
    token_type: str = "service"

    def serialize_payload(self, payload: dict[str, str]):  # type: ignore
        from shared_backend.services.models import Client

        service_id: str | None = payload.get("service_id")
        if not service_id:
            raise ValueError("Service ID is not set")
        service = Client.get_service(service_id)
        if not service:
            raise NotFound(detail="service_not_found", attr="service_id")
        return service

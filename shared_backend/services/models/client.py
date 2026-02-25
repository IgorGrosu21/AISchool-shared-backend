from typing import Any

from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView

from shared_backend.api.models import AuthenticateableUser
from shared_backend.utils.exceptions import (
    APIException,
    BadRequest,
    InternalServerError,
    Unauthorized,
)

from .consumer_caller import ConsumerCaller
from .service import Service
from .service_storage import ServiceStorage
from .session import Session
from .token_storage import TokenStorage


class Client:
    _debug: bool

    _id: str
    _secret: str
    _host: str
    _services_config: dict[str, dict[str, str]]

    _session: Session
    _token_storage: TokenStorage
    _service_storage: ServiceStorage
    _consumer_caller: ConsumerCaller

    @classmethod
    def initialize(cls) -> None:
        cls._debug = settings.DEBUG

        cls._id = getattr(settings, "SERVICE_ID", "")
        cls._secret = getattr(settings, "SERVICE_SECRET", "")
        cls._host = getattr(settings, "HOST", "")
        cls._services_config = getattr(settings, "SERVICES_CONFIG", {})

        cls._session = Session(cls._host)
        cls._token_storage = TokenStorage(cls._id)
        cls.initialize_storage()  # may vary in services
        cls._consumer_caller = ConsumerCaller(cls._debug)

        cls.auth()

    @classmethod
    def initialize_storage(cls) -> None:
        cls._service_storage = ServiceStorage(cls._services_config, cls._id, cls._debug)

    @classmethod
    def get_service(cls, service_id: str) -> Service | None:
        return cls._service_storage.get_service(service_id)

    @classmethod
    def call_consumer(
        cls,
        view_class: type[APIView],
        data: dict[str, Any] | list[Any],
        user: AuthenticateableUser,
        language: str | None = None,
    ) -> Response:
        return cls._consumer_caller.call(view_class, data, user, language)

    @classmethod
    def build_url(cls, service_id: str, url: str) -> str:
        return f"{cls._service_storage.get_service_url(service_id)}/services/{url}"

    @classmethod
    def auth(cls) -> str:
        url = cls.build_url("auth-service", "auth/")
        try:
            data = cls.send_request(url, {"id": cls._id, "secret": cls._secret}, use_token=False)
        except Exception as e:
            raise InternalServerError(
                f"Failed to get service token from auth provider: {str(e)}"
            ) from e

        token: str | None = data.get("accessToken")
        if not token:
            raise BadRequest("No access_token in response")

        cls._token_storage.set_token(token)
        cls._session.set_auth_token(token)
        return token

    @classmethod
    def send_request(
        cls,
        url: str,
        data: dict[str, Any] | list[Any],
        use_token: bool = True,
        language: str | None = None,
    ) -> dict[str, Any]:
        if use_token:
            token = cls._token_storage.get_token()
            if not token:
                token = cls.auth()
            else:
                # Ensure session has the token from storage
                cls._session.set_auth_token(token)

        try:
            response_data, response_status = cls._session.post(url, data, use_token, language)
            if response_status == "success" and response_data is not None:
                return response_data

            if response_status == "unauthorized" and use_token:
                token = cls.auth()
                retry_response_data, retry_response_status = cls._session.post(
                    url, data, use_token=True, language=language
                )
                if retry_response_status == "success" and retry_response_data is not None:
                    return retry_response_data
                if retry_response_status == "unauthorized":
                    raise Unauthorized("Unauthorized")
                raise InternalServerError(
                    f"Request failed after token refresh: {retry_response_status}"
                )

            raise BadRequest(f"Request failed: {response_status}")
        except APIException:
            raise
        except Exception as e:
            raise InternalServerError(f"Failed to send request to {url}: {str(e)}") from e

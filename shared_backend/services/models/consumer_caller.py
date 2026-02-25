from typing import Any, cast

from django.test import RequestFactory
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from shared_backend.api.models import AuthenticateableUser


class ConsumerCaller:
    _debug: bool
    _factory: RequestFactory

    def __init__(self, debug: bool):
        self._debug = debug
        self._factory = RequestFactory()

    def call(
        self,
        consumer_view_class: type[APIView],
        data: dict[str, Any] | list[Any],
        user: AuthenticateableUser,
        language: str | None = None,
    ) -> Response:
        django_request = self._factory.post(
            "/",
            data=data,
            content_type="application/json",
            secure=not self._debug,
        )
        view_instance = consumer_view_class()

        original_auth_classes = getattr(view_instance, "authentication_classes", None)
        original_permission_classes = getattr(view_instance, "permission_classes", None)

        try:
            view_instance.authentication_classes = []
            view_instance.permission_classes = [AllowAny]

            # Use dispatch to properly initialize the request with parsers
            drf_request = view_instance.initialize_request(django_request)
            drf_request.user = user  # type: ignore[assignment]
            drf_request.language = language  # type: ignore[attr-defined]

            return cast(Response, view_instance.post(drf_request))  # type: ignore[attr-defined]
        finally:
            if original_auth_classes is not None:
                view_instance.authentication_classes = original_auth_classes
            if original_permission_classes is not None:
                view_instance.permission_classes = original_permission_classes

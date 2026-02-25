from typing import Any, Generic, TypeVar

from django.db.models import Model
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.views import APIView

from shared_backend.services.permissions import CanAccessProducer
from shared_backend.utils.jwt_authentification import JWTServiceAuthentication

T = TypeVar("T", bound=Serializer[Model])


@extend_schema(tags=["service - producers"])
class BaseProducerView(APIView, Generic[T]):
    authentication_classes = [JWTServiceAuthentication]
    permission_classes = [IsAuthenticated, CanAccessProducer]
    serializer_class: type[T] | None = None
    allowed_services: list[str] | str = []

    def process_request(self, request: Request, serializer: T | None = None) -> T | None:
        return serializer

    def get_response_data(
        self, request: Request, serializer: T | None = None
    ) -> dict[str, Any] | None:
        if not serializer:
            return None
        return serializer.data

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer: T | None = None
        if self.serializer_class:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
        serializer = self.process_request(request, serializer)

        status_code: int = status.HTTP_200_OK
        response_data = self.get_response_data(request, serializer)
        if not response_data:
            status_code = status.HTTP_204_NO_CONTENT
        return Response(response_data, status=status_code)

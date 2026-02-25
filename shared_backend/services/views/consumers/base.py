from typing import Any

from drf_spectacular.utils import extend_schema
from rest_framework import status, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from shared_backend.services.models import Client
from shared_backend.utils.exceptions import APIException, InternalServerError


@extend_schema(tags=["service - consumers"])
class BaseConsumerView(views.APIView):
    permission_classes = [IsAuthenticated]
    producer_service_id: str
    producer_url: str
    client = Client

    def validate_request(self, request: Request) -> Response | None:
        return None

    def get_data(self, request: Request) -> dict[str, Any] | list[Any]:
        return {}

    def handle_response(self, request: Request, response: dict[str, Any]) -> Response:
        return Response(response, status=status.HTTP_200_OK)

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        validation_response = self.validate_request(request)
        if validation_response:
            return validation_response

        data = self.get_data(request)
        # Pass request.language to service-to-service calls
        language = getattr(request, "language", None)
        try:
            url = self.client.build_url(self.producer_service_id, self.producer_url + "/")
            response_data = self.client.send_request(url, data, language=language)
            return self.handle_response(request, response_data)
        except APIException:
            # Re-raise custom exceptions so they're handled by the exception handler
            raise
        except Exception as e:
            raise InternalServerError(f"Failed to make a request: {str(e)}") from e

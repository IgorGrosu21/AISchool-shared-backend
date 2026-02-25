from typing import cast

from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import APIView

from shared_backend.services.models import Service


class CanAccessProducer(permissions.BasePermission):
    def has_permission(self, request: Request, view: APIView) -> bool:
        if not hasattr(view, "allowed_services"):
            return False
        allowed_services = getattr(view, "allowed_services", [])
        if allowed_services == "*":
            return True
        service: Service = cast(Service, request.user)
        return service.get_id() in allowed_services

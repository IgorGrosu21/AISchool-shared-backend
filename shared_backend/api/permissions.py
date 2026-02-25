from typing import cast

from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import APIView

from shared_backend.api.models import UserWithProfileType


class CanCreateUser(permissions.BasePermission):
    code = "user_already_exists"
    message = "User already exists."

    def has_permission(self, request: Request, view: APIView) -> bool:
        user = cast(UserWithProfileType, request.user)
        return user.is_anonymous and user.auth_id is not None

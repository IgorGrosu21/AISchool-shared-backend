from typing import Any, cast

from django.apps import apps
from drf_spectacular.utils import extend_schema
from rest_framework import generics, status
from rest_framework.authentication import BaseAuthentication
from rest_framework.request import Request
from rest_framework.response import Response

from shared_backend.api.models import UserWithProfileType
from shared_backend.api.permissions import CanCreateUser
from shared_backend.api.serializers import CreateUserSerializer
from shared_backend.utils.jwt_authentification import JWTUserAuthentication

User = cast(UserWithProfileType, apps.get_model("api", "User"))


@extend_schema(tags=["api - user"])
class CreateUserView(generics.CreateAPIView[UserWithProfileType]):
    authentication_classes = [JWTUserAuthentication]
    permission_classes = [CanCreateUser]
    serializer_class = CreateUserSerializer

    def get_authenticators(self) -> list[BaseAuthentication]:
        auth = JWTUserAuthentication()
        auth.token_type = "access"
        return [auth]

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = CreateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        profile_type = serializer.validated_data["profile_type"]

        user = cast(UserWithProfileType, request.user)
        User.objects.create(auth_id=user.auth_id, profile_type=profile_type)
        return Response({}, status=status.HTTP_201_CREATED)

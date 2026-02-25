from rest_framework import serializers

from shared_backend.api.models import UserWithProfileType


class CreateUserSerializer(serializers.Serializer[UserWithProfileType]):
    profile_type = serializers.CharField(max_length=7)

from django.db import models

from .with_auth_id import UserWithAuthId


class UserWithProfileType(UserWithAuthId):
    PROFILE_TYPES = {
        "student": "Студент",
        "teacher": "Преподаватель",
        "parent": "Родитель",
    }

    profile_type = models.CharField("Тип профиля", max_length=7, choices=PROFILE_TYPES)

    class Meta:
        abstract = True

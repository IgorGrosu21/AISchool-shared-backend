from django.db import models

from .authenticateable import AuthenticateableUser


class UserWithAuthId(AuthenticateableUser):
    auth_id = models.UUIDField("ID аккаунта", unique=True, db_index=True)

    authentication_token_type = "access"
    user_claim_key = "auth_id"

    class Meta:
        abstract = True

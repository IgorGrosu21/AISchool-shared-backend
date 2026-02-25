from .with_uuid import WithUUID


class AuthenticateableUser(WithUUID):
    is_anonymous = False

    authentication_token_type: str
    user_claim_key: str

    @property
    def is_authenticated(self) -> bool:
        return not self.is_anonymous

    class Meta:
        abstract = True

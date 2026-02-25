from .with_profile_type import UserWithProfileType


class UserWithPlans(UserWithProfileType):
    plans: set[str]

    authentication_token_type = "subscriptions"

    class Meta:
        abstract = True

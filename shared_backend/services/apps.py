from django.apps import AppConfig


class ServicesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "services"

    def ready(self) -> None:
        from shared_backend.services.models import Client

        Client.initialize()

        import sys

        if "runserver" not in sys.argv:
            return

        try:
            from shared_backend.utils.jwt_authentification.jwks import get_jwks

            get_jwks(force_refresh=True)

        except Exception as e:
            print(f"Failed to initialize services on startup: {str(e)}")

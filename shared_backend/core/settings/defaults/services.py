from ..helpers import get_env

SERVICES_CONFIG = {
    "auth-service": {
        "secret_hash": get_env("AUTH_SERVICE_SECRET", required=False),
        "dev_url": "http://127.0.0.1:8000",
        "prod_url": "https://aischoolauth.pythonanywhere.com",
    },
    "diary-service": {
        "secret_hash": get_env("DIARY_SERVICE_SECRET", required=False),
        "dev_url": "http://127.0.0.1:8080",
        "prod_url": "https://aischoolapi.pythonanywhere.com",
    },
    "manuals-service": {
        "secret_hash": get_env("MANUALS_SERVICE_SECRET", required=False),
        "dev_url": "http://127.0.0.1:8160",
        "prod_url": "https://aischoolmanuals.pythonanywhere.com",
    },
    "notifications-service": {
        "secret_hash": get_env("NOTIFICATIONS_SERVICE_SECRET", required=False),
        "dev_url": "http://127.0.0.1:8240",
        "prod_url": "https://aischoolnotifications.pythonanywhere.com",
    },
    "subscriptions-service": {
        "secret_hash": get_env("SUBSCRIPTIONS_SERVICE_SECRET", required=False),
        "dev_url": "http://127.0.0.1:8320",
        "prod_url": "https://aischoolsubscriptions.pythonanywhere.com",
    },
}

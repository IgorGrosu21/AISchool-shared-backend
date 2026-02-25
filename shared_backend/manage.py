#!/usr/bin/env python
import os
import sys

PORTS_MAP = {
    "auth": 8000,
    "diary": 8080,
    "manuals": 8160,
    "notifications": 8240,
    "subscriptions": 8320,
}


def main(service_name: str) -> None:
    if not service_name:
        raise RuntimeError("Service name is required")

    """Run administrative tasks."""
    # Set Django settings module
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    if sys.argv[1] == "runserver" and len(sys.argv) == 2:
        sys.argv.append(f"127.0.0.1:{PORTS_MAP[service_name]}")
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    raise RuntimeError("This file is not executable")

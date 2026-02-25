import os
from pathlib import Path

import dotenv


def setup_base_dir(settings_file: Path) -> Path:
    return settings_file.parent.parent


def load_environment(base_dir: Path) -> None:
    env_path = base_dir / ".env"
    if env_path.exists():
        dotenv.load_dotenv(env_path)


def get_env(key: str, required: bool = True) -> str:
    value = os.environ.get(key)
    if not value:
        if required:
            raise ValueError(f"{key} environment variable is required")
        return ""
    return value


def get_env_list(key: str, default: list[str] | None = None) -> list[str]:
    if default is None:
        default = []
    value = os.environ.get(key, "")
    if not value:
        return default
    return [item.strip() for item in value.split(",") if item.strip()]


def get_env_int(key: str, default: int | None = None) -> int | None:
    value = os.environ.get(key)
    if not value:
        return default
    try:
        return int(value)
    except ValueError:
        return default

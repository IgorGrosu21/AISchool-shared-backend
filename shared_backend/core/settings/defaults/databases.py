from pathlib import Path


def setup_databases(base_dir: Path) -> dict[str, dict[str, str | Path]]:
    return {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": base_dir / "db.sqlite3",
        }
    }

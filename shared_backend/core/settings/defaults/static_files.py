from pathlib import Path


def setup_static_files(base_dir: Path) -> dict[str, str | Path]:
    return {
        "STATIC_URL": "static/",
        "STATIC_ROOT": base_dir / "static",
        "MEDIA_URL": "media/",
        "MEDIA_ROOT": base_dir / "media",
        "PUBLIC_URL": "public/",
        "PUBLIC_ROOT": base_dir / "public",
    }

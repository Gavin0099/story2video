import os
import tomllib
from pathlib import Path


def database_path(config: Path | None, override: Path | None) -> Path:
    if override is not None:
        return override
    if configured := os.environ.get("S2V_DB_PATH"):
        return Path(configured)

    if config is None:
        config = Path("story2video.toml")
        if not config.exists():
            return Path("artifacts/story2video.sqlite3")

    with config.open("rb") as file:
        settings = tomllib.load(file)
    storage = settings.get("storage")
    database = storage.get("database") if isinstance(storage, dict) else None
    if not isinstance(database, str) or not database.strip():
        raise ValueError(f"{config}: storage.database must be a non-empty path")
    return config.parent / database

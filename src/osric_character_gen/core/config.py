"""Application settings for the character sheet manager."""

from pathlib import Path

from pydantic_settings import BaseSettings

_PACKAGE_ROOT = Path(__file__).resolve().parent.parent
_DEFAULT_DB_PATH = str(_PACKAGE_ROOT / "data" / "osric_characters.db")


class Settings(BaseSettings):
    """Configuration loaded from environment variables with OSRIC_ prefix."""

    db_path: str = _DEFAULT_DB_PATH
    secret_key_bytes: int = 24
    admin_key_bytes: int = 36
    max_versions_per_character: int = 20

    model_config = {"env_prefix": "OSRIC_"}


settings = Settings()

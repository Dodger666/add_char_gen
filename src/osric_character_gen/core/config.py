"""Application settings for the character sheet manager."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configuration loaded from environment variables with OSRIC_ prefix."""

    db_path: str = "data/osric_characters.db"
    secret_key_bytes: int = 24
    admin_key_bytes: int = 36
    max_versions_per_character: int = 20

    model_config = {"env_prefix": "OSRIC_"}


settings = Settings()

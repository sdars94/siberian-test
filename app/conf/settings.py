from pathlib import Path

from pydantic import PostgresDsn, field_validator
from pydantic_core.core_schema import FieldValidationInfo
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Settings class.

    Subclass of the pydantic settings BaseSettings class.
    """

    PROJECT_NAME: str = "Siberian.pro"
    API_STR: str = "/api"

    BASE_DIR: Path = Path(__file__).resolve().parent.parent

    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "default_password"
    POSTGRES_DB: str = "siberian_db"
    SQLALCHEMY_DATABASE_URI: PostgresDsn | None = None

    @field_validator("SQLALCHEMY_DATABASE_URI", mode="before")
    @classmethod
    def _build_postgres_uri(cls, v, info: FieldValidationInfo):
        """
        Build the PostgreSQL URI based on provided configuration.

        Args:
            v: The field value.
            info (FieldValidationInfo): Information about the validation.

        Returns:
            str: The constructed PostgreSQL URI.
        """
        postgres_user = info.data.get("POSTGRES_USER")
        postgres_password = info.data.get("POSTGRES_PASSWORD")
        postgres_server = info.data.get("POSTGRES_SERVER")
        postgres_db = info.data.get("POSTGRES_DB")

        return (
            f"postgresql+asyncpg://{postgres_user}:{postgres_password}"
            f"@{postgres_server}:5432/{postgres_db}"
        )

    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=f"{BASE_DIR.parent.parent}/.env",
    )


def get_settings() -> Settings:
    """Get Settings instance."""
    return Settings()


settings = get_settings()

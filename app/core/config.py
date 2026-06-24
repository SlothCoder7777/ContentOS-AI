from functools import lru_cache
from typing import Literal

from pydantic import Field, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = Field(default="ContentOS AI")
    app_env: Literal["development", "staging", "production"] = Field(
        default="development"
    )
    debug: bool = Field(default=True)

    api_v1_prefix: str = Field(default="/api/v1")

    database_url: str = Field(default="")

    jwt_secret_key: str = Field(default="")
    jwt_algorithm: str = Field(default="HS256")
    access_token_expire_minutes: int = Field(default=60)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @field_validator("database_url")
    @classmethod
    def normalize_database_url(cls, value: str) -> str:
        if value.startswith("postgresql://"):
            return value.replace("postgresql://", "postgresql+psycopg://", 1)

        return value

    @model_validator(mode="after")
    def validate_required_settings(self) -> "Settings":
        if not self.database_url:
            raise ValueError("DATABASE_URL is missing in .env")

        if not self.jwt_secret_key:
            raise ValueError("JWT_SECRET_KEY is missing in .env")

        if self.jwt_secret_key == "CHANGE_ME_TO_A_LONG_RANDOM_SECRET":
            raise ValueError("JWT_SECRET_KEY must be changed in .env")

        if not self.database_url.startswith("postgresql+psycopg://"):
            raise ValueError(
                "DATABASE_URL must start with postgresql:// or postgresql+psycopg://"
            )

        return self


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

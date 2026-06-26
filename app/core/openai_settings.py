from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class OpenAISettings(BaseSettings):
    api_key: str | None = Field(
        default=None,
        validation_alias="OPENAI_API_KEY",
    )
    model: str = Field(
        default="gpt-5.5",
        validation_alias="OPENAI_MODEL",
    )
    timeout_seconds: float = Field(
        default=30.0,
        validation_alias="OPENAI_TIMEOUT_SECONDS",
    )
    max_retries: int = Field(
        default=2,
        validation_alias="OPENAI_MAX_RETRIES",
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


openai_settings = OpenAISettings()

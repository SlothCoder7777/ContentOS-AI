from functools import cached_property

from openai import OpenAI

from app.core.openai_settings import openai_settings


class OpenAIClientService:
    @cached_property
    def client(self) -> OpenAI:
        if not openai_settings.api_key:
            raise RuntimeError(
                "OPENAI_API_KEY is missing. Add it to your local .env or deployment secrets."
            )

        return OpenAI(
            api_key=openai_settings.api_key,
            timeout=openai_settings.timeout_seconds,
            max_retries=openai_settings.max_retries,
        )

    def is_configured(self) -> bool:
        return bool(openai_settings.api_key)

    def get_model(self) -> str:
        return openai_settings.model


openai_client_service = OpenAIClientService()

from openai import APIError, APITimeoutError, RateLimitError

from app.core.openai_settings import openai_settings
from app.schemas.llm import LLMGenerateRequest, LLMGenerateResponse
from app.services.openai_client_service import openai_client_service


class LLMService:
    def generate_text(
        self,
        request_data: LLMGenerateRequest,
    ) -> LLMGenerateResponse:
        if not openai_client_service.is_configured():
            raise RuntimeError(
                "OpenAI is not configured. Add OPENAI_API_KEY to your environment."
            )

        try:
            response = openai_client_service.client.responses.create(
                model=openai_settings.model,
                instructions=request_data.system_prompt,
                input=request_data.user_prompt,
            )

            return LLMGenerateResponse(
                model=openai_settings.model,
                output_text=response.output_text,
                metadata=request_data.metadata,
            )

        except (APITimeoutError, RateLimitError, APIError) as exc:
            raise RuntimeError(f"OpenAI generation failed: {exc}") from exc


llm_service = LLMService()

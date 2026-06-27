from fastapi import APIRouter, HTTPException, status

from app.core.openai_settings import openai_settings
from app.schemas.llm import LLMGenerateRequest, LLMGenerateResponse
from app.services.llm_service import llm_service
from app.services.openai_client_service import openai_client_service

router = APIRouter(
    prefix="/ai",
    tags=["AI"],
)


@router.get("/status")
def get_ai_status():
    return {
        "provider": "openai",
        "model": openai_settings.model,
        "configured": openai_client_service.is_configured(),
    }


@router.post(
    "/generate",
    response_model=LLMGenerateResponse,
    status_code=status.HTTP_200_OK,
)
def generate_ai_text(
    request_data: LLMGenerateRequest,
) -> LLMGenerateResponse:
    try:
        return llm_service.generate_text(request_data)

    except RuntimeError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc

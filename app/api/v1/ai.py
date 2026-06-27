from fastapi import APIRouter, HTTPException, status

from app.schemas.llm import LLMGenerateRequest, LLMGenerateResponse
from app.services.llm_service import llm_service

router = APIRouter(
    prefix="/ai",
    tags=["AI"],
)


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

from fastapi import APIRouter, status

from app.schemas.ai_influencer import (
    AIInfluencerGenerateRequest,
    AIInfluencerGenerateResponse,
)
from app.services.ai_influencer_service import AIInfluencerService

router = APIRouter(
    prefix="/ai-influencers",
    tags=["AI Influencers"],
)


@router.get("/presets")
def get_ai_influencer_presets():
    return AIInfluencerService().get_presets()


@router.post(
    "/generate",
    response_model=AIInfluencerGenerateResponse,
    status_code=status.HTTP_200_OK,
)
def generate_ai_influencer(
    request_data: AIInfluencerGenerateRequest,
) -> AIInfluencerGenerateResponse:
    return AIInfluencerService().generate(request_data)

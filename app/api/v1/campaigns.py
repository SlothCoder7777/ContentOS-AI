from fastapi import APIRouter, status

from app.schemas.campaign import CampaignGenerateRequest, CampaignGenerateResponse
from app.services.campaign_service import CampaignService

router = APIRouter(
    prefix="/campaigns",
    tags=["Campaigns"],
)


@router.post(
    "/generate",
    response_model=CampaignGenerateResponse,
    status_code=status.HTTP_200_OK,
)
def generate_campaign(
    request_data: CampaignGenerateRequest,
) -> CampaignGenerateResponse:
    return CampaignService().generate(request_data)

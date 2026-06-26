from fastapi import APIRouter, status

from app.schemas.whatsapp_campaign import (
    WhatsAppCampaignGenerateRequest,
    WhatsAppCampaignGenerateResponse,
)
from app.services.whatsapp_campaign_service import WhatsAppCampaignService

router = APIRouter(
    prefix="/whatsapp-campaigns",
    tags=["WhatsApp Campaigns"],
)


@router.post(
    "/generate",
    response_model=WhatsAppCampaignGenerateResponse,
    status_code=status.HTTP_200_OK,
)
def generate_whatsapp_campaign(
    request_data: WhatsAppCampaignGenerateRequest,
) -> WhatsAppCampaignGenerateResponse:
    return WhatsAppCampaignService().generate(request_data)

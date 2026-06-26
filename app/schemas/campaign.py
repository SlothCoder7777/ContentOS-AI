from pydantic import BaseModel, Field


class CampaignGenerateRequest(BaseModel):
    brand_name: str = Field(
        ...,
        min_length=2,
        max_length=120,
    )

    niche: str = Field(
        ...,
        min_length=2,
        max_length=120,
    )

    campaign_goal: str = Field(
        ...,
        min_length=2,
        max_length=200,
    )

    target_audience: str = Field(
        ...,
        min_length=2,
        max_length=200,
    )

    platform: str = Field(
        default="Instagram",
        max_length=80,
    )

    offer_details: str | None = Field(
        default=None,
        max_length=500,
    )

    tone: str = Field(
        default="friendly",
        max_length=80,
    )

    output_count: int = Field(
        default=3,
        ge=1,
        le=5,
    )


class CampaignContentVariation(BaseModel):
    variation: int
    headline: str
    caption: str
    call_to_action: str


class CampaignTrendIdea(BaseModel):
    rank: int
    title: str
    hook: str
    suggested_format: str


class CampaignWhatsAppMessage(BaseModel):
    variation: int
    message: str


class CampaignInfluencerDirection(BaseModel):
    influencer_name: str
    personality: str
    bio: str


class CampaignGenerateResponse(BaseModel):
    brand_name: str
    niche: str
    campaign_goal: str
    platform: str
    tone: str
    strategy_summary: str
    trends: list[CampaignTrendIdea]
    content_variations: list[CampaignContentVariation]
    whatsapp_messages: list[CampaignWhatsAppMessage]
    influencer_direction: CampaignInfluencerDirection

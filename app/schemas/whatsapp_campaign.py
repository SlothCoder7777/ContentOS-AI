from pydantic import BaseModel, Field


class WhatsAppCampaignGenerateRequest(BaseModel):
    brand_name: str = Field(
        ...,
        min_length=2,
        max_length=120,
        description="Business or brand name",
    )

    offer_title: str = Field(
        ...,
        min_length=2,
        max_length=200,
        description="Main campaign offer title",
    )

    offer_details: str = Field(
        ...,
        min_length=2,
        description="Detailed offer description",
    )

    target_audience: str | None = Field(
        default=None,
        max_length=200,
        description="Target audience for the campaign",
    )

    tone: str = Field(
        default="friendly",
        max_length=80,
        description="Campaign tone such as friendly, premium, urgent, festive",
    )

    validity: str | None = Field(
        default=None,
        max_length=120,
        description="Offer validity text",
    )

    call_to_action: str = Field(
        default="Order now",
        max_length=120,
        description="Campaign CTA",
    )

    output_count: int = Field(
        default=3,
        ge=1,
        le=10,
        description="Number of campaign message variations",
    )


class WhatsAppCampaignMessage(BaseModel):
    variation: int
    message: str
    short_message: str
    call_to_action: str


class WhatsAppCampaignGenerateResponse(BaseModel):
    brand_name: str
    offer_title: str
    tone: str
    output_count: int
    messages: list[WhatsAppCampaignMessage]

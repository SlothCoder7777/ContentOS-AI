from pydantic import BaseModel, Field


class AIInfluencerGenerateRequest(BaseModel):
    brand_name: str = Field(
        ...,
        min_length=2,
        max_length=120,
        description="Brand or business name",
    )

    niche: str = Field(
        ...,
        min_length=2,
        max_length=120,
        description="Influencer niche, such as food, travel, tech, fashion",
    )

    target_audience: str = Field(
        ...,
        min_length=2,
        max_length=200,
        description="Audience the AI influencer should appeal to",
    )

    personality: str = Field(
        default="friendly",
        max_length=120,
        description="Influencer personality style",
    )

    platform: str = Field(
        default="Instagram",
        max_length=80,
        description="Primary platform for the influencer",
    )

    language_style: str = Field(
        default="simple and engaging",
        max_length=160,
        description="Preferred language and communication style",
    )


class AIInfluencerContentIdea(BaseModel):
    title: str
    format: str
    hook: str
    caption_direction: str


class AIInfluencerGenerateResponse(BaseModel):
    influencer_name: str
    brand_name: str
    niche: str
    platform: str
    personality: str
    bio: str
    content_pillars: list[str]
    visual_style: dict[str, str]
    content_ideas: list[AIInfluencerContentIdea]

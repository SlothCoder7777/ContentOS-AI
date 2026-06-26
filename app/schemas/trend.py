from pydantic import BaseModel, Field


class TrendDetectRequest(BaseModel):
    niche: str = Field(
        ...,
        min_length=2,
        max_length=120,
        description="Business niche or content category",
    )

    platform: str = Field(
        default="Instagram",
        max_length=80,
        description="Target platform such as Instagram, YouTube, WhatsApp, LinkedIn",
    )

    location: str | None = Field(
        default=None,
        max_length=120,
        description="Optional target location",
    )

    audience: str | None = Field(
        default=None,
        max_length=200,
        description="Optional target audience",
    )

    result_count: int = Field(
        default=5,
        ge=1,
        le=10,
        description="Number of trend ideas to return",
    )


class TrendIdea(BaseModel):
    rank: int
    title: str
    hook: str
    content_angle: str
    suggested_format: str
    hashtags: list[str]


class TrendDetectResponse(BaseModel):
    niche: str
    platform: str
    location: str | None
    audience: str | None
    trends: list[TrendIdea]

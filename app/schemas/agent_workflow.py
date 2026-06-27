from pydantic import BaseModel, Field


class ContentWorkflowRunRequest(BaseModel):
    brand_name: str = Field(
        ...,
        min_length=2,
        max_length=120,
    )

    topic: str = Field(
        ...,
        min_length=2,
        max_length=200,
    )

    platform: str = Field(
        default="Instagram",
        max_length=80,
    )

    content_type: str = Field(
        default="instagram_post",
        max_length=80,
    )

    tone: str = Field(
        default="friendly",
        max_length=80,
    )

    use_ai: bool = Field(
        default=False,
        description="Use OpenAI for the writer node when configured. Falls back safely.",
    )


class ContentWorkflowRunResponse(BaseModel):
    brand_name: str
    topic: str
    platform: str
    content_type: str
    tone: str
    use_ai: bool
    plan: str
    draft: str
    review: str
    workflow_status: str
    generation_engine: str

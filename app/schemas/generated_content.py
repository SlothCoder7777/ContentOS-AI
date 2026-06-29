from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class GeneratedContentCreate(BaseModel):
    project_id: str | None = Field(default=None)
    title: str | None = Field(default=None, max_length=200)

    generation_engine: str = Field(..., min_length=1, max_length=120)
    model: str | None = Field(default=None, max_length=120)

    content_type: str = Field(..., min_length=1, max_length=120)
    platform: str = Field(default="General", max_length=120)
    tone: str = Field(default="engaging", max_length=120)
    brief: str = Field(..., min_length=1)

    brand_context: dict[str, Any] | None = Field(default=None)
    variations: list[dict[str, Any]] = Field(default_factory=list)
    raw_output: str | None = Field(default=None)
    content_metadata: dict[str, Any] | None = Field(default=None)


class GeneratedContentRead(BaseModel):
    id: str
    project_id: str | None
    title: str | None

    generation_engine: str
    model: str | None

    content_type: str
    platform: str
    tone: str
    brief: str

    brand_context: dict[str, Any] | None
    variations: list[dict[str, Any]]
    raw_output: str | None
    content_metadata: dict[str, Any] | None

    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True,
    }


class GeneratedContentListResponse(BaseModel):
    items: list[GeneratedContentRead]
    total: int

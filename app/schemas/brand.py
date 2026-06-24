from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class BrandBase(BaseModel):
    name: str = Field(
        ...,
        min_length=2,
        max_length=120,
        description="Brand name",
    )

    description: str | None = Field(
        default=None,
        description="Short brand description",
    )

    industry: str | None = Field(
        default=None,
        max_length=100,
        description="Brand industry or niche",
    )

    target_audience: str | None = Field(
        default=None,
        description="Target audience description",
    )

    brand_voice: str | None = Field(
        default=None,
        description="Tone and communication style of the brand",
    )

    brand_values: dict[str, Any] | None = Field(
        default=None,
        description="Structured brand values used for AI content generation",
    )

    visual_guidelines: dict[str, Any] | None = Field(
        default=None,
        description="Colors, typography, logo rules, and visual identity notes",
    )


class BrandCreate(BrandBase):
    pass


class BrandUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=120,
    )

    description: str | None = None

    industry: str | None = Field(
        default=None,
        max_length=100,
    )

    target_audience: str | None = None
    brand_voice: str | None = None
    brand_values: dict[str, Any] | None = None
    visual_guidelines: dict[str, Any] | None = None
    is_active: bool | None = None


class BrandRead(BrandBase):
    id: UUID
    owner_id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

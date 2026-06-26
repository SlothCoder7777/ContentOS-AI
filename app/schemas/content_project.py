from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ContentProjectBase(BaseModel):
    title: str = Field(
        ...,
        min_length=2,
        max_length=160,
        description="Content project title",
    )

    content_type: str = Field(
        ...,
        min_length=2,
        max_length=80,
        description="Type of content, such as instagram_post, reel_script, blog, whatsapp_campaign",
    )

    platform: str | None = Field(
        default=None,
        max_length=80,
        description="Target platform, such as Instagram, YouTube, WhatsApp, LinkedIn",
    )

    brief: str | None = Field(
        default=None,
        description="Project brief or content instruction",
    )

    brand_id: UUID | None = Field(
        default=None,
        description="Optional linked brand ID",
    )

    generated_content: dict[str, Any] | None = Field(
        default=None,
        description="Generated AI content output",
    )

    project_metadata: dict[str, Any] | None = Field(
        default=None,
        description="Extra structured project metadata",
    )


class ContentProjectCreate(ContentProjectBase):
    pass


class ContentProjectUpdate(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=2,
        max_length=160,
    )

    content_type: str | None = Field(
        default=None,
        min_length=2,
        max_length=80,
    )

    platform: str | None = Field(
        default=None,
        max_length=80,
    )

    brief: str | None = None

    brand_id: UUID | None = None

    status: str | None = Field(
        default=None,
        max_length=50,
    )

    generated_content: dict[str, Any] | None = None

    project_metadata: dict[str, Any] | None = None


class ContentProjectGenerateRequest(BaseModel):
    prompt_override: str | None = Field(
        default=None,
        description="Optional extra instruction for generation",
    )

    tone: str | None = Field(
        default=None,
        max_length=80,
        description="Desired tone, such as friendly, premium, funny, professional",
    )

    output_count: int = Field(
        default=3,
        ge=1,
        le=10,
        description="Number of content variations to generate",
    )


class ContentProjectRead(ContentProjectBase):
    id: UUID
    owner_id: UUID
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

from typing import Any

from pydantic import BaseModel, Field


class AIContentVariation(BaseModel):
    variation: int = Field(
        ...,
        ge=1,
        description="Variation number of generated content.",
    )

    headline: str = Field(
        ...,
        min_length=1,
        description="Generated headline or hook.",
    )

    caption: str = Field(
        ...,
        min_length=1,
        description="Generated caption, post copy, or message body.",
    )

    call_to_action: str = Field(
        ...,
        min_length=1,
        description="Suggested call to action.",
    )

    hashtags: list[str] = Field(
        default_factory=list,
        description="Suggested hashtags for social platforms.",
    )

    notes: str | None = Field(
        default=None,
        description="Optional generation notes.",
    )


class StructuredAIOutput(BaseModel):
    generation_engine: str = Field(
        ...,
        min_length=1,
        description="Engine used for generation.",
    )

    model: str | None = Field(
        default=None,
        description="AI model used when generation is powered by an LLM.",
    )

    content_type: str = Field(
        ...,
        min_length=1,
        description="Type of content generated.",
    )

    platform: str = Field(
        default="General",
        description="Target platform.",
    )

    tone: str = Field(
        default="engaging",
        description="Tone used for generated content.",
    )

    brief: str = Field(
        ...,
        min_length=1,
        description="Input brief used for generation.",
    )

    brand_context: dict[str, Any] | None = Field(
        default=None,
        description="Optional brand memory context used during generation.",
    )

    variations: list[AIContentVariation] = Field(
        default_factory=list,
        description="Generated content variations.",
    )

    raw_output: str | None = Field(
        default=None,
        description="Raw AI output before parsing, when available.",
    )


class StructuredAIOutputList(BaseModel):
    items: list[StructuredAIOutput] = Field(
        default_factory=list,
        description="List of structured AI outputs.",
    )

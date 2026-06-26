from typing import Any

from pydantic import BaseModel, Field


class LLMGenerateRequest(BaseModel):
    system_prompt: str = Field(
        ...,
        min_length=2,
        description="Developer/system instruction for the model",
    )

    user_prompt: str = Field(
        ...,
        min_length=2,
        description="User prompt sent to the model",
    )

    metadata: dict[str, Any] | None = Field(
        default=None,
        description="Optional internal metadata for tracking generation context",
    )


class LLMGenerateResponse(BaseModel):
    model: str
    output_text: str
    provider: str = "openai"
    metadata: dict[str, Any] | None = None

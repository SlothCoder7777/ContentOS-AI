from uuid import UUID

from pydantic import BaseModel, Field


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: UUID = Field(
        ...,
        description="User ID stored inside JWT subject",
    )

    email: str | None = Field(
        default=None,
        description="Optional email stored inside JWT payload",
    )

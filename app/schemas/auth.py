from pydantic import BaseModel, EmailStr, Field

from app.schemas.user import UserRead


class RegisterRequest(BaseModel):
    email: EmailStr = Field(
        ...,
        description="User email address",
    )

    full_name: str = Field(
        ...,
        min_length=2,
        max_length=120,
        description="User full name",
    )

    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description="User password",
    )


class LoginRequest(BaseModel):
    email: EmailStr = Field(
        ...,
        description="Registered email address",
    )

    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description="User password",
    )


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserRead

from datetime import UTC, datetime, timedelta
from uuid import UUID

from jose import JWTError, jwt
from pydantic import ValidationError

from app.core.config import settings
from app.schemas.token import TokenPayload


def create_access_token(
    subject: UUID | str,
    email: str | None = None,
    expires_delta: timedelta | None = None,
) -> str:
    now = datetime.now(UTC)

    expire = now + (
        expires_delta
        if expires_delta is not None
        else timedelta(minutes=settings.access_token_expire_minutes)
    )

    payload = {
        "sub": str(subject),
        "type": "access",
        "iat": int(now.timestamp()),
        "exp": int(expire.timestamp()),
    }

    if email is not None:
        payload["email"] = email

    return jwt.encode(
        payload,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )


def decode_access_token(token: str) -> TokenPayload | None:
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
        )

        if payload.get("type") != "access":
            return None

        return TokenPayload.model_validate(
            {
                "sub": payload.get("sub"),
                "email": payload.get("email"),
            }
        )

    except (JWTError, ValidationError):
        return None

from fastapi.security import OAuth2PasswordBearer

from app.core.config import settings
from app.utils.jwt_handler import create_access_token, decode_access_token
from app.utils.password import hash_password, verify_password

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.api_v1_prefix}/auth/login",
)

__all__ = [
    "oauth2_scheme",
    "hash_password",
    "verify_password",
    "create_access_token",
    "decode_access_token",
]

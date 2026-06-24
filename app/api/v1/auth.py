from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.auth import AuthResponse, LoginRequest, RegisterRequest
from app.services.auth_service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=AuthResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_user(
    register_data: RegisterRequest,
    db: Annotated[Session, Depends(get_db)],
) -> AuthResponse:
    return AuthService(db).register(register_data)


@router.post(
    "/login",
    response_model=AuthResponse,
)
def login_user(
    login_data: LoginRequest,
    db: Annotated[Session, Depends(get_db)],
) -> AuthResponse:
    return AuthService(db).login(login_data)


@router.post(
    "/token",
    response_model=AuthResponse,
)
def login_for_swagger_authorize(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)],
) -> AuthResponse:
    login_data = LoginRequest(
        email=form_data.username,
        password=form_data.password,
    )

    return AuthService(db).login(login_data)

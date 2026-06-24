from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth import AuthResponse, LoginRequest, RegisterRequest
from app.schemas.user import UserRead
from app.utils.jwt_handler import create_access_token
from app.utils.password import hash_password, verify_password


class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repository = UserRepository(db)

    def register(self, register_data: RegisterRequest) -> AuthResponse:
        existing_user = self.user_repository.get_by_email(register_data.email)

        if existing_user is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this email already exists.",
            )

        hashed_password = hash_password(register_data.password)

        try:
            user = self.user_repository.create(
                email=register_data.email,
                full_name=register_data.full_name,
                hashed_password=hashed_password,
            )

            self.db.commit()
            self.db.refresh(user)

        except IntegrityError as exc:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this email already exists.",
            ) from exc

        except Exception:
            self.db.rollback()
            raise

        access_token = create_access_token(
            subject=user.id,
            email=user.email,
        )

        return AuthResponse(
            access_token=access_token,
            token_type="bearer",
            user=UserRead.model_validate(user),
        )

    def authenticate(self, login_data: LoginRequest) -> User:
        user = self.user_repository.get_by_email(login_data.email)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password.",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not verify_password(login_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password.",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive.",
            )

        return user

    def login(self, login_data: LoginRequest) -> AuthResponse:
        user = self.authenticate(login_data)

        access_token = create_access_token(
            subject=user.id,
            email=user.email,
        )

        return AuthResponse(
            access_token=access_token,
            token_type="bearer",
            user=UserRead.model_validate(user),
        )

from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserRead, UserUpdate


class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repository = UserRepository(db)

    def get_by_id(self, user_id: UUID) -> User:
        user = self.user_repository.get_by_id(user_id)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found.",
            )

        return user

    def get_current_user_profile(self, current_user: User) -> UserRead:
        return UserRead.model_validate(current_user)

    def update_user(
        self,
        *,
        user_id: UUID,
        user_data: UserUpdate,
    ) -> UserRead:
        user = self.get_by_id(user_id)

        try:
            updated_user = self.user_repository.update(
                user=user,
                full_name=user_data.full_name,
                is_active=user_data.is_active,
            )

            self.db.commit()
            self.db.refresh(updated_user)

        except Exception:
            self.db.rollback()
            raise

        return UserRead.model_validate(updated_user)

    def list_users(
        self,
        *,
        skip: int = 0,
        limit: int = 100,
    ) -> list[UserRead]:
        users = self.user_repository.list_users(
            skip=skip,
            limit=limit,
        )

        return [UserRead.model_validate(user) for user in users]

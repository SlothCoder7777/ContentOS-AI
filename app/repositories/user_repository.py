from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: UUID) -> User | None:
        statement = select(User).where(User.id == user_id)
        return self.db.scalar(statement)

    def get_by_email(self, email: str) -> User | None:
        normalized_email = email.lower().strip()
        statement = select(User).where(User.email == normalized_email)
        return self.db.scalar(statement)

    def create(
        self,
        *,
        email: str,
        full_name: str,
        hashed_password: str,
        is_active: bool = True,
        is_superuser: bool = False,
    ) -> User:
        user = User(
            email=email.lower().strip(),
            full_name=full_name.strip(),
            hashed_password=hashed_password,
            is_active=is_active,
            is_superuser=is_superuser,
        )

        self.db.add(user)
        self.db.flush()

        return user

    def update(
        self,
        *,
        user: User,
        full_name: str | None = None,
        is_active: bool | None = None,
    ) -> User:
        if full_name is not None:
            user.full_name = full_name.strip()

        if is_active is not None:
            user.is_active = is_active

        self.db.add(user)
        self.db.flush()

        return user

    def list_users(
        self,
        *,
        skip: int = 0,
        limit: int = 100,
    ) -> list[User]:
        statement = (
            select(User).order_by(User.created_at.desc()).offset(skip).limit(limit)
        )

        return list(self.db.scalars(statement).all())

    def email_exists(self, email: str) -> bool:
        return self.get_by_email(email) is not None

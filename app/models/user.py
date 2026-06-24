from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, String, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TimestampMixin

if TYPE_CHECKING:
    from app.models.brand import Brand


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    email: Mapped[str] = mapped_column(
        String(length=320),
        unique=True,
        nullable=False,
    )

    full_name: Mapped[str] = mapped_column(
        String(length=120),
        nullable=False,
    )

    hashed_password: Mapped[str] = mapped_column(
        String(length=255),
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default=text("true"),
    )

    is_superuser: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default=text("false"),
    )

    brands: Mapped[list["Brand"]] = relationship(
        back_populates="owner",
    )

    def __repr__(self) -> str:
        return f"User(id={self.id!s}, email={self.email!r})"

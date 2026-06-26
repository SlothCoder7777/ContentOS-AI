import uuid
from typing import TYPE_CHECKING, Any

from sqlalchemy import ForeignKey, String, Text, text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TimestampMixin

if TYPE_CHECKING:
    from app.models.brand import Brand
    from app.models.user import User


class ContentProject(Base, TimestampMixin):
    __tablename__ = "content_projects"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    owner_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    brand_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("brands.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    title: Mapped[str] = mapped_column(
        String(length=160),
        nullable=False,
        index=True,
    )

    content_type: Mapped[str] = mapped_column(
        String(length=80),
        nullable=False,
        index=True,
    )

    platform: Mapped[str | None] = mapped_column(
        String(length=80),
        nullable=True,
        index=True,
    )

    brief: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(length=50),
        nullable=False,
        server_default=text("'draft'"),
        index=True,
    )

    generated_content: Mapped[dict[str, Any] | None] = mapped_column(
        JSONB,
        nullable=True,
    )

    project_metadata: Mapped[dict[str, Any] | None] = mapped_column(
        JSONB,
        nullable=True,
    )

    owner: Mapped["User"] = relationship()

    brand: Mapped["Brand | None"] = relationship()

    def __repr__(self) -> str:
        return f"ContentProject(id={self.id!s}, title={self.title!r})"

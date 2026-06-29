import uuid
from datetime import datetime, timezone
from typing import Any

from sqlalchemy import JSON, DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class GeneratedContent(Base):
    __tablename__ = "generated_contents"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        index=True,
    )

    project_id: Mapped[str | None] = mapped_column(
        String(36),
        nullable=True,
        index=True,
    )

    title: Mapped[str | None] = mapped_column(
        String(200),
        nullable=True,
    )

    generation_engine: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
        index=True,
    )

    model: Mapped[str | None] = mapped_column(
        String(120),
        nullable=True,
    )

    content_type: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
        index=True,
    )

    platform: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
        default="General",
        index=True,
    )

    tone: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
        default="engaging",
    )

    brief: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    brand_context: Mapped[dict[str, Any] | None] = mapped_column(
        JSON,
        nullable=True,
    )

    variations: Mapped[list[dict[str, Any]]] = mapped_column(
        JSON,
        nullable=False,
        default=list,
    )

    raw_output: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    content_metadata: Mapped[dict[str, Any] | None] = mapped_column(
        JSON,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

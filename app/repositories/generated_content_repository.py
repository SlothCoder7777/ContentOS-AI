from sqlalchemy import Select, desc, func, select
from sqlalchemy.orm import Session

from app.models.generated_content import GeneratedContent
from app.schemas.generated_content import GeneratedContentCreate


class GeneratedContentRepository:
    def create(
        self,
        db: Session,
        data: GeneratedContentCreate,
    ) -> GeneratedContent:
        generated_content = GeneratedContent(**data.model_dump())

        db.add(generated_content)
        db.commit()
        db.refresh(generated_content)

        return generated_content

    def get_by_id(
        self,
        db: Session,
        generated_content_id: str,
    ) -> GeneratedContent | None:
        statement: Select[tuple[GeneratedContent]] = select(GeneratedContent).where(
            GeneratedContent.id == generated_content_id
        )

        return db.execute(statement).scalar_one_or_none()

    def list_recent(
        self,
        db: Session,
        limit: int = 20,
        offset: int = 0,
    ) -> list[GeneratedContent]:
        statement: Select[tuple[GeneratedContent]] = (
            select(GeneratedContent)
            .order_by(desc(GeneratedContent.created_at))
            .limit(limit)
            .offset(offset)
        )

        return list(db.execute(statement).scalars().all())

    def count(
        self,
        db: Session,
    ) -> int:
        statement = select(func.count()).select_from(GeneratedContent)

        return int(db.execute(statement).scalar_one())


generated_content_repository = GeneratedContentRepository()

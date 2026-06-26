from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.content_project import ContentProject
from app.schemas.content_project import ContentProjectCreate, ContentProjectUpdate


class ContentProjectRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        owner_id: UUID,
        project_data: ContentProjectCreate,
    ) -> ContentProject:
        project = ContentProject(
            owner_id=owner_id,
            **project_data.model_dump(),
        )

        self.db.add(project)
        self.db.commit()
        self.db.refresh(project)

        return project

    def list_by_owner(
        self,
        owner_id: UUID,
        skip: int = 0,
        limit: int = 100,
        status: str | None = None,
    ) -> list[ContentProject]:
        statement = select(ContentProject).where(
            ContentProject.owner_id == owner_id,
        )

        if status:
            statement = statement.where(ContentProject.status == status)

        statement = (
            statement.order_by(ContentProject.created_at.desc())
            .offset(skip)
            .limit(limit)
        )

        return list(self.db.scalars(statement).all())

    def get_by_owner(
        self,
        owner_id: UUID,
        project_id: UUID,
    ) -> ContentProject | None:
        statement = select(ContentProject).where(
            ContentProject.id == project_id,
            ContentProject.owner_id == owner_id,
        )

        return self.db.scalar(statement)

    def update(
        self,
        project: ContentProject,
        project_data: ContentProjectUpdate,
    ) -> ContentProject:
        update_data = project_data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(project, field, value)

        self.db.add(project)
        self.db.commit()
        self.db.refresh(project)

        return project

    def delete(self, project: ContentProject) -> None:
        self.db.delete(project)
        self.db.commit()

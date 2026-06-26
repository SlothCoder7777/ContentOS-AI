from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.content_project import ContentProject
from app.models.user import User
from app.repositories.content_project_repository import ContentProjectRepository
from app.schemas.content_project import (
    ContentProjectCreate,
    ContentProjectGenerateRequest,
    ContentProjectUpdate,
)
from app.services.content_generation_service import ContentGenerationService


class ContentProjectService:
    def __init__(self, db: Session):
        self.repository = ContentProjectRepository(db)
        self.generation_service = ContentGenerationService()

    def create_project(
        self,
        owner: User,
        project_data: ContentProjectCreate,
    ) -> ContentProject:
        return self.repository.create(
            owner_id=owner.id,
            project_data=project_data,
        )

    def list_projects(
        self,
        owner: User,
        skip: int = 0,
        limit: int = 100,
        status_filter: str | None = None,
    ) -> list[ContentProject]:
        return self.repository.list_by_owner(
            owner_id=owner.id,
            skip=skip,
            limit=limit,
            status=status_filter,
        )

    def get_project(
        self,
        owner: User,
        project_id: UUID,
    ) -> ContentProject:
        project = self.repository.get_by_owner(
            owner_id=owner.id,
            project_id=project_id,
        )

        if project is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Content project not found",
            )

        return project

    def update_project(
        self,
        owner: User,
        project_id: UUID,
        project_data: ContentProjectUpdate,
    ) -> ContentProject:
        project = self.get_project(
            owner=owner,
            project_id=project_id,
        )

        return self.repository.update(
            project=project,
            project_data=project_data,
        )

    def generate_project_content(
        self,
        owner: User,
        project_id: UUID,
        request_data: ContentProjectGenerateRequest,
    ) -> ContentProject:
        project = self.get_project(
            owner=owner,
            project_id=project_id,
        )

        generated_content = self.generation_service.generate(
            project=project,
            request_data=request_data,
        )

        update_data = ContentProjectUpdate(
            status="generated",
            generated_content=generated_content,
            project_metadata={
                "generation_engine": generated_content.get("generation_engine"),
                "output_count": request_data.output_count,
                "tone": request_data.tone,
                "use_ai": request_data.use_ai,
            },
        )

        return self.repository.update(
            project=project,
            project_data=update_data,
        )

    def delete_project(
        self,
        owner: User,
        project_id: UUID,
    ) -> None:
        project = self.get_project(
            owner=owner,
            project_id=project_id,
        )

        self.repository.delete(project)

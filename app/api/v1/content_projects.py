from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.models.content_project import ContentProject
from app.models.user import User
from app.schemas.content_project import (
    ContentProjectCreate,
    ContentProjectGenerateRequest,
    ContentProjectRead,
    ContentProjectUpdate,
)
from app.services.content_project_service import ContentProjectService

router = APIRouter(
    prefix="/content-projects",
    tags=["Content Projects"],
)


@router.post(
    "",
    response_model=ContentProjectRead,
    status_code=status.HTTP_201_CREATED,
)
def create_content_project(
    project_data: ContentProjectCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
) -> ContentProject:
    return ContentProjectService(db).create_project(
        owner=current_user,
        project_data=project_data,
    )


@router.get(
    "",
    response_model=list[ContentProjectRead],
)
def list_my_content_projects(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=100),
    status_filter: str | None = Query(default=None, alias="status"),
) -> list[ContentProject]:
    return ContentProjectService(db).list_projects(
        owner=current_user,
        skip=skip,
        limit=limit,
        status_filter=status_filter,
    )


@router.get(
    "/{project_id}",
    response_model=ContentProjectRead,
)
def get_my_content_project(
    project_id: UUID,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
) -> ContentProject:
    return ContentProjectService(db).get_project(
        owner=current_user,
        project_id=project_id,
    )


@router.patch(
    "/{project_id}",
    response_model=ContentProjectRead,
)
def update_my_content_project(
    project_id: UUID,
    project_data: ContentProjectUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
) -> ContentProject:
    return ContentProjectService(db).update_project(
        owner=current_user,
        project_id=project_id,
        project_data=project_data,
    )


@router.post(
    "/{project_id}/generate",
    response_model=ContentProjectRead,
)
def generate_content_for_project(
    project_id: UUID,
    request_data: ContentProjectGenerateRequest,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
) -> ContentProject:
    return ContentProjectService(db).generate_project_content(
        owner=current_user,
        project_id=project_id,
        request_data=request_data,
    )


@router.delete(
    "/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_my_content_project(
    project_id: UUID,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
) -> Response:
    ContentProjectService(db).delete_project(
        owner=current_user,
        project_id=project_id,
    )

    return Response(status_code=status.HTTP_204_NO_CONTENT)

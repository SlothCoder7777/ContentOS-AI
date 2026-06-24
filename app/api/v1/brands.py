from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.brand import BrandCreate, BrandRead, BrandUpdate
from app.services.brand_service import BrandService

router = APIRouter(
    prefix="/brands",
    tags=["Brands"],
)


@router.post(
    "",
    response_model=BrandRead,
    status_code=status.HTTP_201_CREATED,
)
def create_brand(
    brand_data: BrandCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
) -> BrandRead:
    return BrandService(db).create_brand(
        owner=current_user,
        brand_data=brand_data,
    )


@router.get(
    "",
    response_model=list[BrandRead],
)
def list_my_brands(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=100),
    active_only: bool = Query(default=True),
) -> list[BrandRead]:
    return BrandService(db).list_brands_for_owner(
        owner=current_user,
        skip=skip,
        limit=limit,
        active_only=active_only,
    )


@router.get(
    "/{brand_id}",
    response_model=BrandRead,
)
def get_my_brand(
    brand_id: UUID,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
) -> BrandRead:
    return BrandService(db).get_brand_read_for_owner(
        owner=current_user,
        brand_id=brand_id,
    )


@router.patch(
    "/{brand_id}",
    response_model=BrandRead,
)
def update_my_brand(
    brand_id: UUID,
    brand_data: BrandUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
) -> BrandRead:
    return BrandService(db).update_brand(
        owner=current_user,
        brand_id=brand_id,
        brand_data=brand_data,
    )


@router.patch(
    "/{brand_id}/deactivate",
    response_model=BrandRead,
)
def deactivate_my_brand(
    brand_id: UUID,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
) -> BrandRead:
    return BrandService(db).deactivate_brand(
        owner=current_user,
        brand_id=brand_id,
    )


@router.delete(
    "/{brand_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_my_brand(
    brand_id: UUID,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
) -> Response:
    BrandService(db).delete_brand(
        owner=current_user,
        brand_id=brand_id,
    )

    return Response(status_code=status.HTTP_204_NO_CONTENT)

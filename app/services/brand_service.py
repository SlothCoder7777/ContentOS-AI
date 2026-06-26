from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.brand import Brand
from app.models.user import User
from app.repositories.brand_repository import BrandRepository
from app.schemas.brand import BrandCreate, BrandUpdate


class BrandService:
    def __init__(self, db: Session):
        self.repository = BrandRepository(db)

    def create_brand(self, owner: User, brand_data: BrandCreate) -> Brand:
        return self.repository.create(
            owner_id=owner.id,
            brand_data=brand_data,
        )

    def list_brands(
        self,
        owner: User,
        skip: int = 0,
        limit: int = 100,
        active_only: bool = True,
    ) -> list[Brand]:
        return self.repository.list_by_owner(
            owner_id=owner.id,
            skip=skip,
            limit=limit,
            active_only=active_only,
        )

    def get_brand(self, owner: User, brand_id: UUID) -> Brand:
        brand = self.repository.get_by_owner(
            owner_id=owner.id,
            brand_id=brand_id,
        )

        if brand is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Brand not found",
            )

        return brand

    def update_brand(
        self,
        owner: User,
        brand_id: UUID,
        brand_data: BrandUpdate,
    ) -> Brand:
        brand = self.get_brand(
            owner=owner,
            brand_id=brand_id,
        )

        return self.repository.update(
            brand=brand,
            brand_data=brand_data,
        )

    def deactivate_brand(self, owner: User, brand_id: UUID) -> Brand:
        brand = self.get_brand(
            owner=owner,
            brand_id=brand_id,
        )

        return self.repository.deactivate(brand)

    def delete_brand(self, owner: User, brand_id: UUID) -> None:
        brand = self.get_brand(
            owner=owner,
            brand_id=brand_id,
        )

        self.repository.delete(brand)

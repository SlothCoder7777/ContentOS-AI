from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.brand import Brand
from app.models.user import User
from app.repositories.brand_repository import BrandRepository
from app.schemas.brand import BrandCreate, BrandRead, BrandUpdate


class BrandService:
    def __init__(self, db: Session):
        self.db = db
        self.brand_repository = BrandRepository(db)

    def create_brand(
        self,
        *,
        owner: User,
        brand_data: BrandCreate,
    ) -> BrandRead:
        try:
            brand = self.brand_repository.create(
                owner_id=owner.id,
                brand_data=brand_data,
            )

            self.db.commit()
            self.db.refresh(brand)

        except Exception:
            self.db.rollback()
            raise

        return BrandRead.model_validate(brand)

    def get_brand_for_owner(
        self,
        *,
        owner: User,
        brand_id: UUID,
    ) -> Brand:
        brand = self.brand_repository.get_by_owner_and_id(
            owner_id=owner.id,
            brand_id=brand_id,
        )

        if brand is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Brand not found.",
            )

        return brand

    def get_brand_read_for_owner(
        self,
        *,
        owner: User,
        brand_id: UUID,
    ) -> BrandRead:
        brand = self.get_brand_for_owner(
            owner=owner,
            brand_id=brand_id,
        )

        return BrandRead.model_validate(brand)

    def list_brands_for_owner(
        self,
        *,
        owner: User,
        skip: int = 0,
        limit: int = 100,
        active_only: bool = True,
    ) -> list[BrandRead]:
        brands = self.brand_repository.list_by_owner(
            owner_id=owner.id,
            skip=skip,
            limit=limit,
            active_only=active_only,
        )

        return [BrandRead.model_validate(brand) for brand in brands]

    def update_brand(
        self,
        *,
        owner: User,
        brand_id: UUID,
        brand_data: BrandUpdate,
    ) -> BrandRead:
        brand = self.get_brand_for_owner(
            owner=owner,
            brand_id=brand_id,
        )

        try:
            updated_brand = self.brand_repository.update(
                brand=brand,
                brand_data=brand_data,
            )

            self.db.commit()
            self.db.refresh(updated_brand)

        except Exception:
            self.db.rollback()
            raise

        return BrandRead.model_validate(updated_brand)

    def deactivate_brand(
        self,
        *,
        owner: User,
        brand_id: UUID,
    ) -> BrandRead:
        brand = self.get_brand_for_owner(
            owner=owner,
            brand_id=brand_id,
        )

        try:
            deactivated_brand = self.brand_repository.deactivate(
                brand=brand,
            )

            self.db.commit()
            self.db.refresh(deactivated_brand)

        except Exception:
            self.db.rollback()
            raise

        return BrandRead.model_validate(deactivated_brand)

    def delete_brand(
        self,
        *,
        owner: User,
        brand_id: UUID,
    ) -> None:
        brand = self.get_brand_for_owner(
            owner=owner,
            brand_id=brand_id,
        )

        try:
            self.brand_repository.delete(
                brand=brand,
            )

            self.db.commit()

        except Exception:
            self.db.rollback()
            raise

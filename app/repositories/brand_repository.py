from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.brand import Brand
from app.schemas.brand import BrandCreate, BrandUpdate


class BrandRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, owner_id: UUID, brand_data: BrandCreate) -> Brand:
        brand = Brand(
            owner_id=owner_id,
            **brand_data.model_dump(),
        )

        self.db.add(brand)
        self.db.commit()
        self.db.refresh(brand)

        return brand

    def list_by_owner(
        self,
        owner_id: UUID,
        skip: int = 0,
        limit: int = 100,
        active_only: bool = True,
    ) -> list[Brand]:
        statement = select(Brand).where(Brand.owner_id == owner_id)

        if active_only:
            statement = statement.where(Brand.is_active.is_(True))

        statement = (
            statement.order_by(Brand.created_at.desc()).offset(skip).limit(limit)
        )

        return list(self.db.scalars(statement).all())

    def get_by_owner(self, owner_id: UUID, brand_id: UUID) -> Brand | None:
        statement = select(Brand).where(
            Brand.id == brand_id,
            Brand.owner_id == owner_id,
        )

        return self.db.scalar(statement)

    def update(self, brand: Brand, brand_data: BrandUpdate) -> Brand:
        update_data = brand_data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(brand, field, value)

        self.db.add(brand)
        self.db.commit()
        self.db.refresh(brand)

        return brand

    def deactivate(self, brand: Brand) -> Brand:
        brand.is_active = False

        self.db.add(brand)
        self.db.commit()
        self.db.refresh(brand)

        return brand

    def delete(self, brand: Brand) -> None:
        self.db.delete(brand)
        self.db.commit()

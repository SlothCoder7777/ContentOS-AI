from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.brand import Brand
from app.schemas.brand import BrandCreate, BrandUpdate


class BrandRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, brand_id: UUID) -> Brand | None:
        statement = select(Brand).where(Brand.id == brand_id)
        return self.db.scalar(statement)

    def get_by_owner_and_id(
        self,
        *,
        owner_id: UUID,
        brand_id: UUID,
    ) -> Brand | None:
        statement = select(Brand).where(
            Brand.id == brand_id,
            Brand.owner_id == owner_id,
        )

        return self.db.scalar(statement)

    def list_by_owner(
        self,
        *,
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

    def create(
        self,
        *,
        owner_id: UUID,
        brand_data: BrandCreate,
    ) -> Brand:
        brand = Brand(
            owner_id=owner_id,
            name=brand_data.name.strip(),
            description=brand_data.description,
            industry=brand_data.industry,
            target_audience=brand_data.target_audience,
            brand_voice=brand_data.brand_voice,
            brand_values=brand_data.brand_values,
            visual_guidelines=brand_data.visual_guidelines,
        )

        self.db.add(brand)
        self.db.flush()

        return brand

    def update(
        self,
        *,
        brand: Brand,
        brand_data: BrandUpdate,
    ) -> Brand:
        update_data = brand_data.model_dump(exclude_unset=True)

        if "name" in update_data and update_data["name"] is not None:
            update_data["name"] = update_data["name"].strip()

        for field, value in update_data.items():
            setattr(brand, field, value)

        self.db.add(brand)
        self.db.flush()

        return brand

    def delete(
        self,
        *,
        brand: Brand,
    ) -> None:
        self.db.delete(brand)
        self.db.flush()

    def deactivate(
        self,
        *,
        brand: Brand,
    ) -> Brand:
        brand.is_active = False

        self.db.add(brand)
        self.db.flush()

        return brand

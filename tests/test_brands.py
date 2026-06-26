from datetime import datetime, timezone
from uuid import UUID, uuid4

from fastapi.testclient import TestClient

from app.api.v1 import brands as brands_router
from app.main import app

client = TestClient(app)


class FakeUser:
    id = uuid4()
    email = "brand-test@example.com"
    full_name = "Brand Test User"
    is_active = True


def fake_get_current_user():
    return FakeUser()


def fake_get_db():
    return object()


def build_brand(
    brand_id: UUID | None = None,
    owner_id: UUID | None = None,
    name: str = "Kulfi Lounge",
    is_active: bool = True,
):
    now = datetime.now(timezone.utc)

    return {
        "id": brand_id or uuid4(),
        "owner_id": owner_id or FakeUser.id,
        "name": name,
        "description": "Premium kulfi and falooda brand",
        "industry": "Food and Beverage",
        "target_audience": "Dessert lovers",
        "brand_voice": "Friendly and premium",
        "brand_values": {"quality": "high", "taste": "authentic"},
        "visual_guidelines": {"colors": ["pink", "teal", "chocolate"]},
        "is_active": is_active,
        "created_at": now,
        "updated_at": now,
    }


class FakeBrandService:
    def __init__(self, db):
        self.db = db

    def create_brand(self, owner, brand_data):
        return build_brand(
            owner_id=owner.id,
            name=brand_data.name,
        )

    def list_brands(self, owner, skip=0, limit=100, active_only=True):
        return [
            build_brand(owner_id=owner.id),
        ]

    def get_brand(self, owner, brand_id):
        return build_brand(
            brand_id=brand_id,
            owner_id=owner.id,
        )

    def update_brand(self, owner, brand_id, brand_data):
        return build_brand(
            brand_id=brand_id,
            owner_id=owner.id,
            name=brand_data.name or "Kulfi Lounge Updated",
        )

    def deactivate_brand(self, owner, brand_id):
        return build_brand(
            brand_id=brand_id,
            owner_id=owner.id,
            is_active=False,
        )

    def delete_brand(self, owner, brand_id):
        return None


original_brand_service = brands_router.BrandService


def setup_module():
    app.dependency_overrides[brands_router.get_current_user] = fake_get_current_user
    app.dependency_overrides[brands_router.get_db] = fake_get_db
    brands_router.BrandService = FakeBrandService


def teardown_module():
    app.dependency_overrides.clear()
    brands_router.BrandService = original_brand_service


def test_create_brand_endpoint():
    response = client.post(
        "/api/v1/brands",
        json={
            "name": "Kulfi Lounge",
            "description": "Premium kulfi and falooda brand",
            "industry": "Food and Beverage",
            "target_audience": "Dessert lovers",
            "brand_voice": "Friendly and premium",
            "brand_values": {"quality": "high"},
            "visual_guidelines": {"colors": ["pink", "teal"]},
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Kulfi Lounge"
    assert data["is_active"] is True


def test_list_brands_endpoint():
    response = client.get("/api/v1/brands")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert data[0]["name"] == "Kulfi Lounge"


def test_get_brand_endpoint():
    brand_id = uuid4()

    response = client.get(f"/api/v1/brands/{brand_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == str(brand_id)
    assert data["name"] == "Kulfi Lounge"


def test_update_brand_endpoint():
    brand_id = uuid4()

    response = client.patch(
        f"/api/v1/brands/{brand_id}",
        json={
            "name": "Kulfi Lounge Updated",
            "brand_voice": "Modern and playful",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == str(brand_id)
    assert data["name"] == "Kulfi Lounge Updated"


def test_deactivate_brand_endpoint():
    brand_id = uuid4()

    response = client.patch(f"/api/v1/brands/{brand_id}/deactivate")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == str(brand_id)
    assert data["is_active"] is False


def test_delete_brand_endpoint():
    brand_id = uuid4()

    response = client.delete(f"/api/v1/brands/{brand_id}")

    assert response.status_code == 204
    assert response.content == b""

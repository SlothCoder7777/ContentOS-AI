from datetime import datetime, timezone
from uuid import UUID, uuid4

from fastapi.testclient import TestClient

from app.api.v1 import content_projects as content_projects_router
from app.main import app

client = TestClient(app)


class FakeUser:
    id = uuid4()
    email = "content-test@example.com"
    full_name = "Content Test User"
    is_active = True


def fake_get_current_user():
    return FakeUser()


def fake_get_db():
    return object()


def build_project(
    project_id: UUID | None = None,
    owner_id: UUID | None = None,
    title: str = "Instagram Monsoon Campaign",
    status: str = "draft",
    generated_content: dict | None = None,
    project_metadata: dict | None = None,
):
    now = datetime.now(timezone.utc)

    return {
        "id": project_id or uuid4(),
        "owner_id": owner_id or FakeUser.id,
        "brand_id": None,
        "title": title,
        "content_type": "instagram_post",
        "platform": "Instagram",
        "brief": "Create a monsoon dessert campaign",
        "status": status,
        "generated_content": generated_content,
        "project_metadata": project_metadata,
        "created_at": now,
        "updated_at": now,
    }


class FakeContentProjectService:
    def __init__(self, db):
        self.db = db

    def create_project(self, owner, project_data):
        return build_project(
            owner_id=owner.id,
            title=project_data.title,
        )

    def list_projects(self, owner, skip=0, limit=100, status_filter=None):
        return [
            build_project(owner_id=owner.id),
        ]

    def get_project(self, owner, project_id):
        return build_project(
            project_id=project_id,
            owner_id=owner.id,
        )

    def update_project(self, owner, project_id, project_data):
        return build_project(
            project_id=project_id,
            owner_id=owner.id,
            title=project_data.title or "Instagram Monsoon Campaign Updated",
            status=project_data.status or "draft",
        )

    def generate_project_content(self, owner, project_id, request_data):
        return build_project(
            project_id=project_id,
            owner_id=owner.id,
            status="generated",
            generated_content={
                "content_type": "instagram_post",
                "platform": "Instagram",
                "tone": request_data.tone or "engaging",
                "variations": [
                    {
                        "variation": 1,
                        "headline": "Instagram Monsoon Campaign - Idea 1",
                        "caption": "Enjoy monsoon with Kulfi Lounge",
                        "call_to_action": "Try it today",
                    }
                ],
            },
            project_metadata={
                "generation_engine": "local-template-v1",
                "output_count": request_data.output_count,
                "tone": request_data.tone,
                "use_ai": request_data.use_ai,
            },
        )

    def delete_project(self, owner, project_id):
        return None


original_content_project_service = content_projects_router.ContentProjectService


def setup_module():
    app.dependency_overrides[content_projects_router.get_current_user] = (
        fake_get_current_user
    )
    app.dependency_overrides[content_projects_router.get_db] = fake_get_db
    content_projects_router.ContentProjectService = FakeContentProjectService


def teardown_module():
    app.dependency_overrides.clear()
    content_projects_router.ContentProjectService = original_content_project_service


def test_create_content_project_endpoint():
    response = client.post(
        "/api/v1/content-projects",
        json={
            "title": "Instagram Monsoon Campaign",
            "content_type": "instagram_post",
            "platform": "Instagram",
            "brief": "Create a monsoon dessert campaign",
            "generated_content": {"caption": "Enjoy monsoon with Kulfi Lounge"},
            "project_metadata": {"campaign": "monsoon"},
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["title"] == "Instagram Monsoon Campaign"
    assert data["status"] == "draft"


def test_list_content_projects_endpoint():
    response = client.get("/api/v1/content-projects")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert data[0]["title"] == "Instagram Monsoon Campaign"


def test_get_content_project_endpoint():
    project_id = uuid4()

    response = client.get(f"/api/v1/content-projects/{project_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == str(project_id)
    assert data["title"] == "Instagram Monsoon Campaign"


def test_update_content_project_endpoint():
    project_id = uuid4()

    response = client.patch(
        f"/api/v1/content-projects/{project_id}",
        json={
            "title": "Instagram Monsoon Campaign Updated",
            "status": "in_progress",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == str(project_id)
    assert data["title"] == "Instagram Monsoon Campaign Updated"
    assert data["status"] == "in_progress"


def test_generate_content_project_endpoint():
    project_id = uuid4()

    response = client.post(
        f"/api/v1/content-projects/{project_id}/generate",
        json={
            "tone": "friendly",
            "output_count": 1,
            "prompt_override": "Make it suitable for monsoon offer",
            "use_ai": False,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == str(project_id)
    assert data["status"] == "generated"
    assert data["generated_content"]["tone"] == "friendly"
    assert len(data["generated_content"]["variations"]) == 1
    assert data["project_metadata"]["generation_engine"] == "local-template-v1"


def test_delete_content_project_endpoint():
    project_id = uuid4()

    response = client.delete(f"/api/v1/content-projects/{project_id}")

    assert response.status_code == 204
    assert response.content == b""

from fastapi.testclient import TestClient

from app.main import app
from app.schemas.agent_workflow import ContentWorkflowRunRequest
from app.services.agent_workflow_service import AgentWorkflowService

client = TestClient(app)


def test_agent_workflow_service_runs_content_workflow():
    response = AgentWorkflowService().run_content_workflow(
        ContentWorkflowRunRequest(
            brand_name="Kulfi Lounge",
            topic="Mixed Berries Milkshake offer",
            platform="Instagram",
            content_type="instagram_post",
            tone="friendly",
        )
    )

    assert response.brand_name == "Kulfi Lounge"
    assert response.topic == "Mixed Berries Milkshake offer"
    assert response.workflow_status == "reviewed"
    assert "Plan a friendly instagram_post" in response.plan
    assert "Kulfi Lounge presents" in response.draft
    assert "Draft reviewed successfully" in response.review


def test_agent_content_workflow_endpoint_runs_successfully():
    response = client.post(
        "/api/v1/agents/content-workflow/run",
        json={
            "brand_name": "Kulfi Lounge",
            "topic": "Mixed Berries Milkshake offer",
            "platform": "Instagram",
            "content_type": "instagram_post",
            "tone": "friendly",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["brand_name"] == "Kulfi Lounge"
    assert data["topic"] == "Mixed Berries Milkshake offer"
    assert data["workflow_status"] == "reviewed"
    assert "Plan a friendly instagram_post" in data["plan"]
    assert "Kulfi Lounge presents" in data["draft"]
    assert "Draft reviewed successfully" in data["review"]

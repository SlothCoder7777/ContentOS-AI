from types import SimpleNamespace
from typing import Any, cast

from fastapi.testclient import TestClient

from app.main import app
from app.schemas.agent_workflow import ContentWorkflowRunRequest
from app.services.agent_workflow_service import AgentWorkflowService

client = TestClient(app)


class FakeSuccessfulLLMService:
    def generate_text(self, request_data):
        return SimpleNamespace(
            model="gpt-5.5",
            output_text="AI writer draft for Kulfi Lounge campaign.",
            metadata=request_data.metadata,
        )


class FakeFailingLLMService:
    def generate_text(self, request_data):
        raise RuntimeError("OpenAI failed")


def test_agent_workflow_service_runs_local_content_workflow():
    response = AgentWorkflowService().run_content_workflow(
        ContentWorkflowRunRequest(
            brand_name="Kulfi Lounge",
            topic="Mixed Berries Milkshake offer",
            platform="Instagram",
            content_type="instagram_post",
            tone="friendly",
            use_ai=False,
        )
    )

    assert response.brand_name == "Kulfi Lounge"
    assert response.topic == "Mixed Berries Milkshake offer"
    assert response.use_ai is False
    assert response.workflow_status == "reviewed"
    assert response.generation_engine == "local-agent-workflow-v1"
    assert "Plan a friendly instagram_post" in response.plan
    assert "Kulfi Lounge presents" in response.draft
    assert "Draft reviewed successfully" in response.review


def test_agent_workflow_service_uses_mocked_ai_writer():
    service = AgentWorkflowService()
    service.llm_service = cast(Any, FakeSuccessfulLLMService())

    response = service.run_content_workflow(
        ContentWorkflowRunRequest(
            brand_name="Kulfi Lounge",
            topic="Mixed Berries Milkshake offer",
            platform="Instagram",
            content_type="instagram_post",
            tone="friendly",
            use_ai=True,
        )
    )

    assert response.use_ai is True
    assert response.workflow_status == "reviewed"
    assert response.generation_engine == "openai-agent-writer"
    assert response.draft == "AI writer draft for Kulfi Lounge campaign."


def test_agent_workflow_service_falls_back_when_ai_writer_fails():
    service = AgentWorkflowService()
    service.llm_service = cast(Any, FakeFailingLLMService())

    response = service.run_content_workflow(
        ContentWorkflowRunRequest(
            brand_name="Kulfi Lounge",
            topic="Mixed Berries Milkshake offer",
            platform="Instagram",
            content_type="instagram_post",
            tone="friendly",
            use_ai=True,
        )
    )

    assert response.use_ai is True
    assert response.workflow_status == "reviewed"
    assert response.generation_engine == "local-agent-workflow-v1-fallback"
    assert "Kulfi Lounge presents" in response.draft


def test_agent_content_workflow_endpoint_runs_successfully():
    response = client.post(
        "/api/v1/agents/content-workflow/run",
        json={
            "brand_name": "Kulfi Lounge",
            "topic": "Mixed Berries Milkshake offer",
            "platform": "Instagram",
            "content_type": "instagram_post",
            "tone": "friendly",
            "use_ai": False,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["brand_name"] == "Kulfi Lounge"
    assert data["topic"] == "Mixed Berries Milkshake offer"
    assert data["use_ai"] is False
    assert data["workflow_status"] == "reviewed"
    assert data["generation_engine"] == "local-agent-workflow-v1"
    assert "Plan a friendly instagram_post" in data["plan"]
    assert "Kulfi Lounge presents" in data["draft"]
    assert "Draft reviewed successfully" in data["review"]

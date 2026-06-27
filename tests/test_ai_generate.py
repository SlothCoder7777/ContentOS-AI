from fastapi.testclient import TestClient

from app.api.v1 import ai as ai_router
from app.main import app
from app.schemas.llm import LLMGenerateResponse

client = TestClient(app)


class FakeSuccessfulLLMService:
    def generate_text(self, request_data):
        return LLMGenerateResponse(
            model="gpt-5.5",
            output_text="Generated AI response for ContentOS.",
            provider="openai",
            metadata=request_data.metadata,
        )


class FakeFailingLLMService:
    def generate_text(self, request_data):
        raise RuntimeError("OpenAI is not configured")


def test_ai_generate_endpoint_returns_mocked_llm_output(monkeypatch):
    monkeypatch.setattr(
        ai_router,
        "llm_service",
        FakeSuccessfulLLMService(),
    )

    response = client.post(
        "/api/v1/ai/generate",
        json={
            "system_prompt": "You are ContentOS AI.",
            "user_prompt": "Write one short caption.",
            "metadata": {
                "feature": "ai-generate-test",
            },
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["model"] == "gpt-5.5"
    assert data["provider"] == "openai"
    assert data["output_text"] == "Generated AI response for ContentOS."
    assert data["metadata"]["feature"] == "ai-generate-test"


def test_ai_generate_endpoint_returns_503_when_llm_fails(monkeypatch):
    monkeypatch.setattr(
        ai_router,
        "llm_service",
        FakeFailingLLMService(),
    )

    response = client.post(
        "/api/v1/ai/generate",
        json={
            "system_prompt": "You are ContentOS AI.",
            "user_prompt": "Write one short caption.",
        },
    )

    assert response.status_code == 503

    data = response.json()

    assert data["status"] == "error"
    assert "OpenAI is not configured" in data["message"]


def test_ai_generate_endpoint_validates_prompt_fields():
    response = client.post(
        "/api/v1/ai/generate",
        json={
            "system_prompt": "",
            "user_prompt": "",
        },
    )

    assert response.status_code == 422

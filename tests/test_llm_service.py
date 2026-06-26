from types import SimpleNamespace

import pytest

from app.schemas.llm import LLMGenerateRequest
from app.services import llm_service as llm_service_module
from app.services.llm_service import LLMService


class FakeResponsesClient:
    def create(self, model: str, instructions: str, input: str):
        assert model == "gpt-5.5"
        assert instructions == "You are a helpful content assistant."
        assert input == "Write one short caption."

        return SimpleNamespace(output_text="Here is a short AI-generated caption.")


class FakeOpenAIClient:
    responses = FakeResponsesClient()


class FakeConfiguredOpenAIClientService:
    client = FakeOpenAIClient()

    def is_configured(self) -> bool:
        return True


class FakeUnconfiguredOpenAIClientService:
    def is_configured(self) -> bool:
        return False


def test_llm_service_generates_text_with_mocked_openai(monkeypatch):
    monkeypatch.setattr(
        llm_service_module,
        "openai_client_service",
        FakeConfiguredOpenAIClientService(),
    )

    request_data = LLMGenerateRequest(
        system_prompt="You are a helpful content assistant.",
        user_prompt="Write one short caption.",
        metadata={"feature": "test"},
    )

    response = LLMService().generate_text(request_data)

    assert response.model == "gpt-5.5"
    assert response.output_text == "Here is a short AI-generated caption."
    assert response.provider == "openai"
    assert response.metadata == {"feature": "test"}


def test_llm_service_fails_when_openai_is_not_configured(monkeypatch):
    monkeypatch.setattr(
        llm_service_module,
        "openai_client_service",
        FakeUnconfiguredOpenAIClientService(),
    )

    request_data = LLMGenerateRequest(
        system_prompt="You are a helpful content assistant.",
        user_prompt="Write one short caption.",
    )

    with pytest.raises(RuntimeError, match="OpenAI is not configured"):
        LLMService().generate_text(request_data)

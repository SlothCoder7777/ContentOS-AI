from types import SimpleNamespace
from typing import Any, cast

from app.models.content_project import ContentProject
from app.schemas.content_project import ContentProjectGenerateRequest
from app.services.content_generation_service import ContentGenerationService


class FakeSuccessfulLLMService:
    def generate_text(self, request_data):
        return SimpleNamespace(
            model="gpt-5.5",
            output_text="AI generated caption for Kulfi Lounge.",
            metadata=request_data.metadata,
        )


class FakeFailingLLMService:
    def generate_text(self, request_data):
        raise RuntimeError("OpenAI is not configured")


def test_content_generation_without_brand_context():
    project = cast(
        ContentProject,
        SimpleNamespace(
            id="project-1",
            title="Monsoon Dessert Campaign",
            content_type="instagram_post",
            platform="Instagram",
            brief="Promote mixed berry milkshake offer",
            brand=None,
        ),
    )

    request_data = ContentProjectGenerateRequest(
        prompt_override=None,
        tone="friendly",
        output_count=2,
        use_ai=False,
    )

    result = ContentGenerationService().generate(
        project=project,
        request_data=request_data,
    )

    assert result["generation_engine"] == "local-template-v1"
    assert result["content_type"] == "instagram_post"
    assert result["platform"] == "Instagram"
    assert result["tone"] == "friendly"
    assert result["brand_context"] is None
    assert len(result["variations"]) == 2
    assert result["variations"][0]["call_to_action"] == "Follow for more"


def test_content_generation_uses_brand_context():
    brand = SimpleNamespace(
        name="Kulfi Lounge",
        description="Premium kulfi and falooda brand",
        industry="Food and Beverage",
        target_audience="Dessert lovers",
        brand_voice="friendly and premium",
        brand_values={"quality": "high"},
        visual_guidelines={"colors": ["pink", "teal", "chocolate"]},
    )

    project = cast(
        ContentProject,
        SimpleNamespace(
            id="project-2",
            title="Monsoon Dessert Campaign",
            content_type="instagram_post",
            platform="Instagram",
            brief="Promote mixed berry milkshake offer",
            brand=brand,
        ),
    )

    request_data = ContentProjectGenerateRequest(
        prompt_override=None,
        tone=None,
        output_count=1,
        use_ai=False,
    )

    result = ContentGenerationService().generate(
        project=project,
        request_data=request_data,
    )

    assert result["generation_engine"] == "local-template-v1"
    assert result["tone"] == "friendly and premium"
    assert result["brand_context"]["name"] == "Kulfi Lounge"
    assert result["brand_context"]["target_audience"] == "Dessert lovers"
    assert len(result["variations"]) == 1

    variation = result["variations"][0]

    assert "Kulfi Lounge" in variation["headline"]
    assert "Brand: Kulfi Lounge" in variation["caption"]
    assert "Target audience: Dessert lovers" in variation["caption"]


def test_content_generation_prompt_override_has_priority():
    project = cast(
        ContentProject,
        SimpleNamespace(
            id="project-3",
            title="Original Campaign",
            content_type="whatsapp_campaign",
            platform="WhatsApp",
            brief="Original brief",
            brand=None,
        ),
    )

    request_data = ContentProjectGenerateRequest(
        prompt_override="Special weekend offer",
        tone="urgent",
        output_count=1,
        use_ai=False,
    )

    result = ContentGenerationService().generate(
        project=project,
        request_data=request_data,
    )

    assert result["generation_engine"] == "local-template-v1"
    assert result["brief"] == "Special weekend offer"
    assert result["tone"] == "urgent"
    assert result["variations"][0]["call_to_action"] == "Message us now"


def test_content_generation_ai_mode_uses_mocked_llm_successfully():
    project = cast(
        ContentProject,
        SimpleNamespace(
            id="project-4",
            title="AI Campaign",
            content_type="instagram_post",
            platform="Instagram",
            brief="AI generated caption",
            brand=None,
        ),
    )

    request_data = ContentProjectGenerateRequest(
        prompt_override=None,
        tone="friendly",
        output_count=2,
        use_ai=True,
    )

    service = ContentGenerationService()
    service.llm_service = cast(Any, FakeSuccessfulLLMService())

    result = service.generate(
        project=project,
        request_data=request_data,
    )

    assert result["generation_engine"] == "openai"
    assert result["model"] == "gpt-5.5"
    assert result["ai_output"] == "AI generated caption for Kulfi Lounge."
    assert (
        result["variations"][0]["caption"] == "AI generated caption for Kulfi Lounge."
    )


def test_content_generation_ai_mode_falls_back_when_openai_fails():
    project = cast(
        ContentProject,
        SimpleNamespace(
            id="project-5",
            title="AI Campaign",
            content_type="instagram_post",
            platform="Instagram",
            brief="AI generated caption",
            brand=None,
        ),
    )

    request_data = ContentProjectGenerateRequest(
        prompt_override=None,
        tone="friendly",
        output_count=2,
        use_ai=True,
    )

    service = ContentGenerationService()
    service.llm_service = cast(Any, FakeFailingLLMService())

    result = service.generate(
        project=project,
        request_data=request_data,
    )

    assert result["generation_engine"] == "local-template-v1-fallback"
    assert result["content_type"] == "instagram_post"
    assert len(result["variations"]) == 2

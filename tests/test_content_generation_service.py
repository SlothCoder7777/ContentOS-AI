from types import SimpleNamespace
from typing import cast

from app.models.content_project import ContentProject
from app.schemas.content_project import ContentProjectGenerateRequest
from app.services.content_generation_service import ContentGenerationService


def test_content_generation_without_brand_context():
    project = cast(
        ContentProject,
        SimpleNamespace(
            title="Monsoon Dessert Campaign",
            content_type="instagram_post",
            platform="Instagram",
            brief="Promote mixed berry milkshake offer",
            brand=None,
        ),
    )

    request_data = cast(
        ContentProjectGenerateRequest,
        SimpleNamespace(
            prompt_override=None,
            tone="friendly",
            output_count=2,
        ),
    )

    result = ContentGenerationService().generate(
        project=project,
        request_data=request_data,
    )

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
            title="Monsoon Dessert Campaign",
            content_type="instagram_post",
            platform="Instagram",
            brief="Promote mixed berry milkshake offer",
            brand=brand,
        ),
    )

    request_data = cast(
        ContentProjectGenerateRequest,
        SimpleNamespace(
            prompt_override=None,
            tone=None,
            output_count=1,
        ),
    )

    result = ContentGenerationService().generate(
        project=project,
        request_data=request_data,
    )

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
            title="Original Campaign",
            content_type="whatsapp_campaign",
            platform="WhatsApp",
            brief="Original brief",
            brand=None,
        ),
    )

    request_data = cast(
        ContentProjectGenerateRequest,
        SimpleNamespace(
            prompt_override="Special weekend offer",
            tone="urgent",
            output_count=1,
        ),
    )

    result = ContentGenerationService().generate(
        project=project,
        request_data=request_data,
    )

    assert result["brief"] == "Special weekend offer"
    assert result["tone"] == "urgent"
    assert result["variations"][0]["call_to_action"] == "Message us now"

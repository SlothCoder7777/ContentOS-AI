from app.schemas.ai_output import StructuredAIOutput
from app.services.ai_output_parser_service import (
    AIOutputParserService,
    ai_output_parser_service,
)


def test_parse_content_generation_result_with_variations():
    result = {
        "generation_engine": "local-template-v1",
        "content_type": "instagram_post",
        "platform": "Instagram",
        "tone": "friendly",
        "brief": "Promote mixed berries milkshake offer",
        "brand_context": {
            "name": "Kulfi Lounge",
            "target_audience": "Dessert lovers",
        },
        "variations": [
            {
                "variation": 1,
                "headline": "Berry Refreshment is Here",
                "caption": "Enjoy Mixed Berries Milkshake at Rs.90 only.",
                "call_to_action": "Grab it soon",
                "hashtags": ["KulfiLounge", "#BerryMilkshake"],
                "notes": "Good for Instagram.",
            }
        ],
    }

    output = AIOutputParserService().parse_content_generation_result(result)

    assert isinstance(output, StructuredAIOutput)
    assert output.generation_engine == "local-template-v1"
    assert output.content_type == "instagram_post"
    assert output.platform == "Instagram"
    assert output.tone == "friendly"
    assert output.brief == "Promote mixed berries milkshake offer"
    assert output.brand_context is not None
    assert output.brand_context["name"] == "Kulfi Lounge"
    assert len(output.variations) == 1
    assert output.variations[0].headline == "Berry Refreshment is Here"
    assert output.variations[0].hashtags == ["#KulfiLounge", "#BerryMilkshake"]


def test_parse_content_generation_result_with_ai_output_fallback():
    result = {
        "generation_engine": "openai",
        "model": "gpt-5.5",
        "content_type": "instagram_post",
        "platform": "Instagram",
        "tone": "premium",
        "brief": "Promote berry milkshake",
        "ai_output": "AI generated caption for Kulfi Lounge.",
    }

    output = AIOutputParserService().parse_content_generation_result(result)

    assert output.generation_engine == "openai"
    assert output.model == "gpt-5.5"
    assert output.raw_output == "AI generated caption for Kulfi Lounge."
    assert len(output.variations) == 1
    assert output.variations[0].headline == "Promote berry milkshake"
    assert output.variations[0].caption == "AI generated caption for Kulfi Lounge."
    assert output.variations[0].call_to_action == "Try it today"


def test_parse_content_generation_result_handles_missing_optional_fields():
    result = {
        "content_type": "blog_post",
        "brief": "Write about seasonal desserts",
    }

    output = AIOutputParserService().parse_content_generation_result(result)

    assert output.generation_engine == "unknown"
    assert output.content_type == "blog_post"
    assert output.platform == "General"
    assert output.tone == "engaging"
    assert output.brief == "Write about seasonal desserts"
    assert output.brand_context is None
    assert output.variations == []
    assert output.raw_output is None


def test_parse_raw_text_response():
    output = AIOutputParserService().parse_raw_text_response(
        raw_output="Fresh desserts are waiting for you.",
        content_type="whatsapp_campaign",
        platform="WhatsApp",
        tone="urgent",
        brief="Weekend dessert offer",
        generation_engine="openai",
        model="gpt-5.5",
        brand_context={
            "name": "Kulfi Lounge",
        },
    )

    assert output.generation_engine == "openai"
    assert output.model == "gpt-5.5"
    assert output.content_type == "whatsapp_campaign"
    assert output.platform == "WhatsApp"
    assert output.tone == "urgent"
    assert output.brief == "Weekend dessert offer"
    assert output.brand_context is not None
    assert output.brand_context["name"] == "Kulfi Lounge"
    assert output.raw_output == "Fresh desserts are waiting for you."
    assert len(output.variations) == 1
    assert output.variations[0].caption == "Fresh desserts are waiting for you."


def test_global_ai_output_parser_service_instance_exists():
    assert isinstance(ai_output_parser_service, AIOutputParserService)

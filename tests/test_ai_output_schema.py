from app.schemas.ai_output import (
    AIContentVariation,
    StructuredAIOutput,
    StructuredAIOutputList,
)


def test_ai_content_variation_schema():
    variation = AIContentVariation(
        variation=1,
        headline="Try our Mixed Berries Milkshake",
        caption="A refreshing monsoon treat is waiting for you.",
        call_to_action="Visit Kulfi Lounge today",
        hashtags=["#KulfiLounge", "#Milkshake"],
        notes="Good for Instagram.",
    )

    assert variation.variation == 1
    assert variation.headline == "Try our Mixed Berries Milkshake"
    assert variation.caption == "A refreshing monsoon treat is waiting for you."
    assert variation.call_to_action == "Visit Kulfi Lounge today"
    assert "#KulfiLounge" in variation.hashtags
    assert variation.notes == "Good for Instagram."


def test_structured_ai_output_schema():
    output = StructuredAIOutput(
        generation_engine="openai",
        model="gpt-5.5",
        content_type="instagram_post",
        platform="Instagram",
        tone="friendly",
        brief="Promote mixed berries milkshake offer",
        brand_context={
            "name": "Kulfi Lounge",
            "target_audience": "Dessert lovers",
        },
        variations=[
            AIContentVariation(
                variation=1,
                headline="Berry Refreshment is Here",
                caption="Enjoy our Mixed Berries Milkshake at Rs.90 only.",
                call_to_action="Grab it soon",
                hashtags=["#KulfiLounge", "#BerryMilkshake"],
            )
        ],
        raw_output="Raw AI response text",
    )

    assert output.generation_engine == "openai"
    assert output.model == "gpt-5.5"
    assert output.content_type == "instagram_post"
    assert output.platform == "Instagram"
    assert output.tone == "friendly"
    assert output.brand_context["name"] == "Kulfi Lounge"
    assert len(output.variations) == 1
    assert output.variations[0].headline == "Berry Refreshment is Here"
    assert output.raw_output == "Raw AI response text"


def test_structured_ai_output_list_schema():
    output_list = StructuredAIOutputList(
        items=[
            StructuredAIOutput(
                generation_engine="local-template-v1",
                content_type="whatsapp_campaign",
                platform="WhatsApp",
                tone="urgent",
                brief="Weekend offer",
                variations=[
                    AIContentVariation(
                        variation=1,
                        headline="Weekend Offer",
                        caption="Special dessert offer available today.",
                        call_to_action="Message us now",
                    )
                ],
            )
        ]
    )

    assert len(output_list.items) == 1
    assert output_list.items[0].generation_engine == "local-template-v1"
    assert output_list.items[0].variations[0].call_to_action == "Message us now"

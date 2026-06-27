from app.services.prompt_builder_service import PromptBuilderService


def test_build_content_system_prompt():
    prompt = PromptBuilderService().build_content_system_prompt()

    assert "ContentOS AI" in prompt
    assert "content strategist" in prompt
    assert "brand-aware" in prompt


def test_build_content_user_prompt_with_brand_context():
    prompt = PromptBuilderService().build_content_user_prompt(
        title="Monsoon Milkshake Campaign",
        content_type="instagram_post",
        platform="Instagram",
        brief="Promote mixed berries milkshake",
        tone="friendly",
        output_count=3,
        brand_context={
            "name": "Kulfi Lounge",
            "target_audience": "Dessert lovers",
        },
    )

    assert "Monsoon Milkshake Campaign" in prompt
    assert "instagram_post" in prompt
    assert "Instagram" in prompt
    assert "friendly" in prompt
    assert "Kulfi Lounge" in prompt
    assert "Output count: 3" in prompt


def test_build_campaign_system_prompt():
    prompt = PromptBuilderService().build_campaign_system_prompt()

    assert "ContentOS AI" in prompt
    assert "campaign strategist" in prompt
    assert "WhatsApp messages" in prompt


def test_build_campaign_user_prompt():
    prompt = PromptBuilderService().build_campaign_user_prompt(
        brand_name="Kulfi Lounge",
        niche="Food and Beverage",
        campaign_goal="Promote mixed berries milkshake offer",
        target_audience="Dessert lovers",
        platform="Instagram",
        offer_details="Mixed Berries Milkshake at Rs.90 only",
        tone="friendly",
        output_count=2,
    )

    assert "Kulfi Lounge" in prompt
    assert "Food and Beverage" in prompt
    assert "Dessert lovers" in prompt
    assert "Mixed Berries Milkshake at Rs.90 only" in prompt
    assert "Output count: 2" in prompt

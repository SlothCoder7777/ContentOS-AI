from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_week2_public_ai_foundation_endpoints_are_available():
    endpoints = [
        "/api/v1/content-projects/presets",
        "/api/v1/whatsapp-campaigns/generate",
        "/api/v1/trends/presets",
        "/api/v1/trends/detect",
        "/api/v1/ai-influencers/presets",
        "/api/v1/ai-influencers/generate",
        "/api/v1/campaigns/generate",
        "/api/v1/system/routes",
        "/openapi.json",
    ]

    assert endpoints


def test_content_project_presets_smoke():
    response = client.get("/api/v1/content-projects/presets")

    assert response.status_code == 200

    data = response.json()

    assert "content_types" in data
    assert "platforms" in data
    assert "tones" in data


def test_whatsapp_campaign_generator_smoke():
    response = client.post(
        "/api/v1/whatsapp-campaigns/generate",
        json={
            "brand_name": "Kulfi Lounge",
            "offer_title": "Mixed Berries Milkshake at Rs.90 only",
            "offer_details": "Refreshing mixed berries milkshake offer",
            "target_audience": "Dessert lovers",
            "tone": "urgent",
            "validity": "1st July",
            "call_to_action": "Grab it soon",
            "output_count": 2,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["brand_name"] == "Kulfi Lounge"
    assert data["output_count"] == 2
    assert len(data["messages"]) == 2


def test_trend_detection_smoke():
    response = client.post(
        "/api/v1/trends/detect",
        json={
            "niche": "Food and Beverage",
            "platform": "Instagram",
            "location": "Mumbai",
            "audience": "Dessert lovers",
            "result_count": 2,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["niche"] == "Food and Beverage"
    assert len(data["trends"]) == 2


def test_ai_influencer_generator_smoke():
    response = client.post(
        "/api/v1/ai-influencers/generate",
        json={
            "brand_name": "Kulfi Lounge",
            "niche": "Food and Beverage",
            "target_audience": "Dessert lovers",
            "personality": "friendly",
            "platform": "Instagram",
            "language_style": "simple and engaging",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["brand_name"] == "Kulfi Lounge"
    assert data["platform"] == "Instagram"
    assert len(data["content_ideas"]) == 3


def test_unified_campaign_generator_smoke():
    response = client.post(
        "/api/v1/campaigns/generate",
        json={
            "brand_name": "Kulfi Lounge",
            "niche": "Food and Beverage",
            "campaign_goal": "Promote mixed berries milkshake offer",
            "target_audience": "Dessert lovers",
            "platform": "Instagram",
            "offer_details": "Mixed Berries Milkshake at Rs.90 only",
            "tone": "friendly",
            "output_count": 2,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["brand_name"] == "Kulfi Lounge"
    assert len(data["trends"]) == 2
    assert len(data["content_variations"]) == 2
    assert len(data["whatsapp_messages"]) == 2
    assert data["influencer_direction"]["influencer_name"] == "Kulfi Campaign Muse"

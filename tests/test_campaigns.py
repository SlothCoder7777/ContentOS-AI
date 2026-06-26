from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_generate_campaign_endpoint_returns_complete_campaign_package():
    response = client.post(
        "/api/v1/campaigns/generate",
        json={
            "brand_name": "Kulfi Lounge",
            "niche": "Food and Beverage",
            "campaign_goal": "Promote mixed berries milkshake monsoon offer",
            "target_audience": "Dessert lovers and milkshake fans",
            "platform": "Instagram",
            "offer_details": "Mixed Berries Milkshake at Rs.90 only",
            "tone": "friendly",
            "output_count": 3,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["brand_name"] == "Kulfi Lounge"
    assert data["niche"] == "Food and Beverage"
    assert data["platform"] == "Instagram"
    assert data["tone"] == "friendly"

    assert "strategy_summary" in data
    assert len(data["trends"]) == 3
    assert len(data["content_variations"]) == 3
    assert len(data["whatsapp_messages"]) == 3

    assert data["influencer_direction"]["influencer_name"] == "Kulfi Campaign Muse"
    assert "Mixed Berries Milkshake" in data["strategy_summary"]
    assert "Kulfi Lounge" in data["content_variations"][0]["headline"]


def test_generate_campaign_validates_output_count():
    response = client.post(
        "/api/v1/campaigns/generate",
        json={
            "brand_name": "Kulfi Lounge",
            "niche": "Food and Beverage",
            "campaign_goal": "Promote offer",
            "target_audience": "Dessert lovers",
            "output_count": 20,
        },
    )

    assert response.status_code == 422

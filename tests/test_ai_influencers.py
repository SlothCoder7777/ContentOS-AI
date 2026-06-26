from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_ai_influencer_presets_endpoint_returns_supported_options():
    response = client.get("/api/v1/ai-influencers/presets")

    assert response.status_code == 200

    data = response.json()

    assert "niches" in data
    assert "personalities" in data
    assert "platforms" in data
    assert "language_styles" in data

    assert "Food and Beverage" in data["niches"]
    assert "Instagram" in data["platforms"]
    assert "friendly" in data["personalities"]


def test_generate_ai_influencer_endpoint():
    response = client.post(
        "/api/v1/ai-influencers/generate",
        json={
            "brand_name": "Kulfi Lounge",
            "niche": "Food and Beverage",
            "target_audience": "Dessert lovers and milkshake fans",
            "personality": "friendly",
            "platform": "Instagram",
            "language_style": "simple and engaging",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["brand_name"] == "Kulfi Lounge"
    assert data["niche"] == "Food and Beverage"
    assert data["platform"] == "Instagram"
    assert data["personality"] == "friendly"
    assert "Kulfi" in data["influencer_name"]
    assert "bio" in data
    assert len(data["content_pillars"]) == 5
    assert len(data["content_ideas"]) == 3
    assert "visual_style" in data


def test_generate_ai_influencer_validates_required_fields():
    response = client.post(
        "/api/v1/ai-influencers/generate",
        json={
            "brand_name": "K",
            "niche": "F",
            "target_audience": "",
        },
    )

    assert response.status_code == 422

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_trend_presets_endpoint_returns_supported_options():
    response = client.get("/api/v1/trends/presets")

    assert response.status_code == 200

    data = response.json()

    assert "platforms" in data
    assert "popular_niches" in data
    assert "formats" in data
    assert data["default_result_count"] == 5
    assert data["max_result_count"] == 10

    assert "Instagram" in data["platforms"]
    assert "Food and Beverage" in data["popular_niches"]


def test_detect_trends_endpoint_returns_trend_ideas():
    response = client.post(
        "/api/v1/trends/detect",
        json={
            "niche": "Food and Beverage",
            "platform": "Instagram",
            "location": "Mumbai",
            "audience": "Dessert lovers",
            "result_count": 3,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["niche"] == "Food and Beverage"
    assert data["platform"] == "Instagram"
    assert data["location"] == "Mumbai"
    assert data["audience"] == "Dessert lovers"
    assert len(data["trends"]) == 3

    first_trend = data["trends"][0]

    assert first_trend["rank"] == 1
    assert "title" in first_trend
    assert "hook" in first_trend
    assert "content_angle" in first_trend
    assert "suggested_format" in first_trend
    assert "hashtags" in first_trend
    assert "#foodandbeverage" in first_trend["hashtags"]
    assert "#mumbai" in first_trend["hashtags"]


def test_detect_trends_validates_result_count():
    response = client.post(
        "/api/v1/trends/detect",
        json={
            "niche": "Food and Beverage",
            "platform": "Instagram",
            "result_count": 20,
        },
    )

    assert response.status_code == 422

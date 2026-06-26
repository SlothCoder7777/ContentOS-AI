from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_content_project_presets_endpoint_returns_supported_options():
    response = client.get("/api/v1/content-projects/presets")

    assert response.status_code == 200

    data = response.json()

    assert "content_types" in data
    assert "platforms" in data
    assert "tones" in data
    assert data["default_output_count"] == 3
    assert data["max_output_count"] == 10

    content_type_keys = [item["key"] for item in data["content_types"]]

    assert "instagram_post" in content_type_keys
    assert "instagram_reel_script" in content_type_keys
    assert "whatsapp_campaign" in content_type_keys
    assert "blog_post" in content_type_keys
    assert "linkedin_post" in content_type_keys
    assert "youtube_script" in content_type_keys

    assert "Instagram" in data["platforms"]
    assert "WhatsApp" in data["platforms"]
    assert "friendly" in data["tones"]
    assert "professional" in data["tones"]

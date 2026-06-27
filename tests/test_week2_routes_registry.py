from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_system_routes_registry_contains_week2_endpoints():
    response = client.get("/api/v1/system/routes")

    assert response.status_code == 200

    data = response.json()

    paths = [route["path"] for route in data["routes"]]

    assert "/api/v1/content-projects/presets" in paths
    assert "/api/v1/content-projects/{project_id}/generate" in paths
    assert "/api/v1/whatsapp-campaigns/generate" in paths
    assert "/api/v1/trends/presets" in paths
    assert "/api/v1/trends/detect" in paths
    assert "/api/v1/ai-influencers/presets" in paths
    assert "/api/v1/ai-influencers/generate" in paths
    assert "/api/v1/ai/status" in paths
    assert "/api/v1/ai/generate" in paths
    assert "/api/v1/campaigns/generate" in paths


def test_openapi_schema_contains_week2_tags():
    response = client.get("/openapi.json")

    assert response.status_code == 200

    data = response.json()

    tag_names = [tag["name"] for tag in data["tags"]]

    assert "Content Projects" in tag_names
    assert "WhatsApp Campaigns" in tag_names
    assert "Trends" in tag_names
    assert "AI Influencers" in tag_names
    assert "Campaigns" in tag_names

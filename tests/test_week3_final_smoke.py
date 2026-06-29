from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_week3_ai_status_and_health_are_available():
    status_response = client.get("/api/v1/ai/status")
    health_response = client.get("/api/v1/ai/health")

    assert status_response.status_code == 200
    assert health_response.status_code == 200

    status_data = status_response.json()
    health_data = health_response.json()

    assert status_data["provider"] == "openai"
    assert status_data["model"] == "gpt-5.5"
    assert isinstance(status_data["configured"], bool)

    assert health_data["provider"] == "openai"
    assert health_data["model"] == "gpt-5.5"
    assert isinstance(health_data["configured"], bool)
    assert health_data["status"] in {"healthy", "not_configured"}

    assert "api_key" not in status_data
    assert "api_key" not in health_data
    assert "OPENAI_API_KEY" not in status_data
    assert "OPENAI_API_KEY" not in health_data


def test_week3_agent_workflow_endpoint_smoke():
    response = client.post(
        "/api/v1/agents/content-workflow/run",
        json={
            "brand_name": "Kulfi Lounge",
            "topic": "Mixed Berries Milkshake offer",
            "platform": "Instagram",
            "content_type": "instagram_post",
            "tone": "friendly",
            "use_ai": False,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["brand_name"] == "Kulfi Lounge"
    assert data["topic"] == "Mixed Berries Milkshake offer"
    assert data["platform"] == "Instagram"
    assert data["content_type"] == "instagram_post"
    assert data["tone"] == "friendly"
    assert data["use_ai"] is False
    assert data["workflow_status"] == "reviewed"
    assert data["generation_engine"] == "local-agent-workflow-v1"
    assert "Plan a friendly instagram_post" in data["plan"]
    assert "Kulfi Lounge presents" in data["draft"]
    assert "Draft reviewed successfully" in data["review"]


def test_week3_openapi_contains_ai_and_agents_tags():
    response = client.get("/openapi.json")

    assert response.status_code == 200

    data = response.json()
    tag_names = [tag["name"] for tag in data["tags"]]

    assert "AI" in tag_names
    assert "Agents" in tag_names


def test_week3_system_routes_contains_ai_and_agents_routes():
    response = client.get("/api/v1/system/routes")

    assert response.status_code == 200

    data = response.json()
    paths = [route["path"] for route in data["routes"]]

    assert "/api/v1/ai/status" in paths
    assert "/api/v1/ai/health" in paths
    assert "/api/v1/ai/generate" in paths
    assert "/api/v1/agents/content-workflow/run" in paths

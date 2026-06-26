from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_system_environment_endpoint_returns_environment_data():
    response = client.get("/api/v1/system/environment")

    assert response.status_code == 200

    data = response.json()

    assert "environment" in data
    assert "debug" in data
    assert isinstance(data["environment"], str)
    assert isinstance(data["debug"], bool)

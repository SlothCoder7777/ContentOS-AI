from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_system_info_endpoint_returns_backend_metadata():
    response = client.get("/api/v1/system/info")

    assert response.status_code == 200

    data = response.json()

    assert data["service"] == "ContentOS AI Backend"
    assert data["version"] == "1.0.0"
    assert data["api_version"] == "v1"
    assert "environment" in data


def test_system_version_endpoint_returns_version_metadata():
    response = client.get("/api/v1/system/version")

    assert response.status_code == 200

    data = response.json()

    assert data["version"] == "1.0.0"
    assert data["api_version"] == "v1"

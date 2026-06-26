from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_system_routes_endpoint_returns_public_routes():
    response = client.get("/api/v1/system/routes")

    assert response.status_code == 200

    data = response.json()

    assert data["api_version"] == "v1"
    assert "routes" in data
    assert isinstance(data["routes"], list)

    paths = [route["path"] for route in data["routes"]]

    assert "/" in paths
    assert "/docs" in paths
    assert "/api/v1/health" in paths
    assert "/api/v1/health/db" in paths
    assert "/api/v1/system/info" in paths
    assert "/api/v1/system/environment" in paths
    assert "/api/v1/system/version" in paths
    assert "/api/v1/system/routes" in paths

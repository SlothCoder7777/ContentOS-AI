from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_endpoint_returns_healthy_status():
    response = client.get("/api/v1/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"
    assert data["service"] == "ContentOS AI Backend"
    assert data["version"] == "1.0.0"


def test_database_health_endpoint_returns_connected_status():
    response = client.get("/api/v1/health/db")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"
    assert data["database"] == "connected"


def test_wrong_url_returns_custom_error_response():
    response = client.get("/api/v1/wrong-url")

    assert response.status_code == 404

    data = response.json()

    assert data["status"] == "error"
    assert data["message"] == "Not Found"

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root_endpoint_returns_backend_overview():
    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["service"] == "ContentOS AI Backend"
    assert data["status"] == "running"
    assert data["version"] == "1.0.0"
    assert data["docs"] == "/docs"
    assert data["redoc"] == "/redoc"
    assert data["api"] == "/api/v1"
    assert data["health"] == "/api/v1/health"
    assert data["database_health"] == "/api/v1/health/db"
    assert data["system_info"] == "/api/v1/system/info"

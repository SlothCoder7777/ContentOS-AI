from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_backend_root_health_system_and_docs_are_available():
    root_response = client.get("/")
    health_response = client.get("/api/v1/health")
    system_info_response = client.get("/api/v1/system/info")
    system_version_response = client.get("/api/v1/system/version")
    system_routes_response = client.get("/api/v1/system/routes")
    docs_response = client.get("/docs")
    openapi_response = client.get("/openapi.json")

    assert root_response.status_code == 200
    assert health_response.status_code == 200
    assert system_info_response.status_code == 200
    assert system_version_response.status_code == 200
    assert system_routes_response.status_code == 200
    assert docs_response.status_code == 200
    assert openapi_response.status_code == 200

    assert root_response.json()["service"] == "ContentOS AI Backend"
    assert health_response.json()["status"] == "healthy"
    assert system_info_response.json()["service"] == "ContentOS AI Backend"
    assert system_version_response.json()["version"] == "1.0.0"
    assert system_routes_response.json()["api_version"] == "v1"


def test_backend_response_has_production_headers():
    response = client.get("/api/v1/health")

    assert response.status_code == 200

    assert "x-request-id" in response.headers
    assert response.headers["x-content-type-options"] == "nosniff"
    assert response.headers["x-frame-options"] == "DENY"
    assert response.headers["referrer-policy"] == "strict-origin-when-cross-origin"

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_request_id_header_is_added_to_response():
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert "x-request-id" in response.headers
    assert response.headers["x-request-id"]


def test_existing_request_id_header_is_preserved():
    request_id = "test-request-id-123"

    response = client.get(
        "/api/v1/health",
        headers={"X-Request-ID": request_id},
    )

    assert response.status_code == 200
    assert response.headers["x-request-id"] == request_id

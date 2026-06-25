from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_openapi_schema_contains_project_metadata():
    response = client.get("/openapi.json")

    assert response.status_code == 200

    data = response.json()

    assert data["info"]["title"] == "ContentOS AI Backend"
    assert data["info"]["version"] == "1.0.0"
    assert "ContentOS AI Backend" in data["info"]["description"]


def test_swagger_docs_are_available():
    response = client.get("/docs")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_redoc_docs_are_available():
    response = client.get("/redoc")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

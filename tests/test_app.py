from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_fastapi_app_loads_successfully():
    assert app is not None


def test_docs_endpoint_available():
    response = client.get("/docs")
    assert response.status_code == 200

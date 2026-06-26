from app.core.constants import (
    API_PREFIX,
    API_V1_PREFIX,
    API_VERSION,
    APP_NAME,
    APP_VERSION,
    DOCS_URL,
    OPENAPI_URL,
    REDOC_URL,
)


def test_backend_constants_have_expected_values():
    assert APP_NAME == "ContentOS AI Backend"
    assert APP_VERSION == "1.0.0"
    assert API_VERSION == "v1"

    assert API_PREFIX == "/api"
    assert API_V1_PREFIX == "/v1"

    assert DOCS_URL == "/docs"
    assert REDOC_URL == "/redoc"
    assert OPENAPI_URL == "/openapi.json"

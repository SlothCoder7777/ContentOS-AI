from fastapi import FastAPI

from app.api.router import api_router
from app.core.constants import (
    API_PREFIX,
    API_VERSION,
    APP_NAME,
    APP_VERSION,
    DOCS_URL,
    OPENAPI_URL,
    REDOC_URL,
)
from app.core.cors import configure_cors
from app.core.exceptions import register_exception_handlers
from app.core.logging import RequestLoggingMiddleware, configure_logging
from app.core.metadata import API_DESCRIPTION, OPENAPI_TAGS
from app.core.request_id import RequestIDMiddleware
from app.core.security_headers import SecurityHeadersMiddleware

configure_logging()

app = FastAPI(
    title=APP_NAME,
    description=API_DESCRIPTION,
    version=APP_VERSION,
    openapi_tags=OPENAPI_TAGS,
    docs_url=DOCS_URL,
    redoc_url=REDOC_URL,
    openapi_url=OPENAPI_URL,
)

configure_cors(app)
app.add_middleware(RequestIDMiddleware)
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(RequestLoggingMiddleware)
register_exception_handlers(app)


@app.get("/", tags=["Root"])
def root():
    return {
        "service": APP_NAME,
        "status": "running",
        "version": APP_VERSION,
        "docs": DOCS_URL,
        "redoc": REDOC_URL,
        "api": f"{API_PREFIX}/{API_VERSION}",
        "health": f"{API_PREFIX}/{API_VERSION}/health",
        "database_health": f"{API_PREFIX}/{API_VERSION}/health/db",
        "system_info": f"{API_PREFIX}/{API_VERSION}/system/info",
    }


app.include_router(api_router, prefix=API_PREFIX)

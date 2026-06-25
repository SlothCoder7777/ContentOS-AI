from fastapi import FastAPI

from app.api.router import api_router
from app.core.cors import configure_cors
from app.core.exceptions import register_exception_handlers
from app.core.logging import RequestLoggingMiddleware, configure_logging
from app.core.metadata import API_DESCRIPTION, OPENAPI_TAGS
from app.core.request_id import RequestIDMiddleware
from app.core.security_headers import SecurityHeadersMiddleware

configure_logging()

app = FastAPI(
    title="ContentOS AI Backend",
    description=API_DESCRIPTION,
    version="1.0.0",
    openapi_tags=OPENAPI_TAGS,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

configure_cors(app)
app.add_middleware(RequestIDMiddleware)
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(RequestLoggingMiddleware)
register_exception_handlers(app)


@app.get("/", tags=["Root"])
def root():
    return {
        "service": "ContentOS AI Backend",
        "status": "running",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
        "api": "/api/v1",
        "health": "/api/v1/health",
        "database_health": "/api/v1/health/db",
        "system_info": "/api/v1/system/info",
    }


app.include_router(api_router, prefix="/api")

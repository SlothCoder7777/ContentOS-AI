import os

from fastapi import APIRouter

from app.core.constants import API_VERSION, APP_NAME, APP_VERSION

router = APIRouter(
    prefix="/system",
    tags=["System"],
)


@router.get("/info")
def system_info():
    return {
        "service": APP_NAME,
        "version": APP_VERSION,
        "environment": os.getenv("ENVIRONMENT", "development"),
        "api_version": API_VERSION,
    }


@router.get("/environment")
def system_environment():
    environment = os.getenv("ENVIRONMENT", "development")
    debug_value = os.getenv("DEBUG", "False").lower()

    return {
        "environment": environment,
        "debug": debug_value in {"true", "1", "yes", "on"},
    }


@router.get("/version")
def system_version():
    return {
        "service": APP_NAME,
        "version": APP_VERSION,
        "api_version": API_VERSION,
    }


@router.get("/routes")
def system_routes():
    return {
        "api_version": API_VERSION,
        "routes": [
            {
                "method": "GET",
                "path": "/",
                "description": "Root backend overview",
            },
            {
                "method": "GET",
                "path": "/docs",
                "description": "Swagger API documentation",
            },
            {
                "method": "GET",
                "path": "/redoc",
                "description": "ReDoc API documentation",
            },
            {
                "method": "GET",
                "path": "/api/v1/health",
                "description": "Application health check",
            },
            {
                "method": "GET",
                "path": "/api/v1/health/db",
                "description": "Database health check",
            },
            {
                "method": "GET",
                "path": "/api/v1/system/info",
                "description": "System information",
            },
            {
                "method": "GET",
                "path": "/api/v1/system/environment",
                "description": "Environment information",
            },
            {
                "method": "GET",
                "path": "/api/v1/system/version",
                "description": "Backend version information",
            },
            {
                "method": "GET",
                "path": "/api/v1/system/routes",
                "description": "Registered public API routes",
            },
        ],
    }

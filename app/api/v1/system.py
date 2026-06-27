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
                "path": "/openapi.json",
                "description": "OpenAPI schema",
            },
            {
                "method": "POST",
                "path": "/api/v1/auth/register",
                "description": "Register a new user",
            },
            {
                "method": "POST",
                "path": "/api/v1/auth/login",
                "description": "Login and receive JWT token",
            },
            {
                "method": "POST",
                "path": "/api/v1/brands",
                "description": "Create brand profile",
            },
            {
                "method": "GET",
                "path": "/api/v1/brands",
                "description": "List user brand profiles",
            },
            {
                "method": "GET",
                "path": "/api/v1/brands/{brand_id}",
                "description": "Get brand profile by ID",
            },
            {
                "method": "PATCH",
                "path": "/api/v1/brands/{brand_id}",
                "description": "Update brand profile",
            },
            {
                "method": "PATCH",
                "path": "/api/v1/brands/{brand_id}/deactivate",
                "description": "Deactivate brand profile",
            },
            {
                "method": "DELETE",
                "path": "/api/v1/brands/{brand_id}",
                "description": "Delete brand profile",
            },
            {
                "method": "GET",
                "path": "/api/v1/content-projects/presets",
                "description": "Get supported content project presets",
            },
            {
                "method": "POST",
                "path": "/api/v1/content-projects",
                "description": "Create content project",
            },
            {
                "method": "GET",
                "path": "/api/v1/content-projects",
                "description": "List content projects",
            },
            {
                "method": "GET",
                "path": "/api/v1/content-projects/{project_id}",
                "description": "Get content project by ID",
            },
            {
                "method": "PATCH",
                "path": "/api/v1/content-projects/{project_id}",
                "description": "Update content project",
            },
            {
                "method": "POST",
                "path": "/api/v1/content-projects/{project_id}/generate",
                "description": "Generate content for a project",
            },
            {
                "method": "DELETE",
                "path": "/api/v1/content-projects/{project_id}",
                "description": "Delete content project",
            },
            {
                "method": "POST",
                "path": "/api/v1/whatsapp-campaigns/generate",
                "description": "Generate WhatsApp campaign messages",
            },
            {
                "method": "GET",
                "path": "/api/v1/trends/presets",
                "description": "Get trend detection presets",
            },
            {
                "method": "POST",
                "path": "/api/v1/trends/detect",
                "description": "Detect trend ideas for a niche",
            },
            {
                "method": "GET",
                "path": "/api/v1/ai-influencers/presets",
                "description": "Get AI influencer presets",
            },
            {
                "method": "POST",
                "path": "/api/v1/ai-influencers/generate",
                "description": "Generate AI influencer persona",
            },
            {
                "method": "GET",
                "path": "/api/v1/ai/status",
                "description": "Check safe AI provider configuration status",
            },
            {
                "method": "POST",
                "path": "/api/v1/ai/generate",
                "description": "Generate text directly using configured AI provider",
            },
            {
                "method": "POST",
                "path": "/api/v1/campaigns/generate",
                "description": "Generate unified campaign package",
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

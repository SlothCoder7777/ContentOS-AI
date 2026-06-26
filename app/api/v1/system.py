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


@router.get("/version")
def system_version():
    return {
        "version": APP_VERSION,
        "api_version": API_VERSION,
    }

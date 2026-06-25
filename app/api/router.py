from fastapi import APIRouter

from app.api.v1 import auth, brands, health, system, users

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/v1")
api_router.include_router(brands.router, prefix="/v1")
api_router.include_router(users.router, prefix="/v1")
api_router.include_router(health.router, prefix="/v1")
api_router.include_router(system.router, prefix="/v1")

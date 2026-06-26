from fastapi import APIRouter

from app.api.v1 import auth, brands, health, system, users
from app.core.constants import API_V1_PREFIX

api_router = APIRouter()

api_router.include_router(auth.router, prefix=API_V1_PREFIX)
api_router.include_router(brands.router, prefix=API_V1_PREFIX)
api_router.include_router(users.router, prefix=API_V1_PREFIX)
api_router.include_router(health.router, prefix=API_V1_PREFIX)
api_router.include_router(system.router, prefix=API_V1_PREFIX)

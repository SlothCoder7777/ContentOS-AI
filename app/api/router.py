from fastapi import APIRouter

from app.api.v1 import (
    auth,
    brands,
    content_projects,
    health,
    system,
    users,
    whatsapp_campaigns,
)
from app.core.constants import API_V1_PREFIX

api_router = APIRouter()

api_router.include_router(auth.router, prefix=API_V1_PREFIX)
api_router.include_router(brands.router, prefix=API_V1_PREFIX)
api_router.include_router(content_projects.router, prefix=API_V1_PREFIX)
api_router.include_router(whatsapp_campaigns.router, prefix=API_V1_PREFIX)
api_router.include_router(users.router, prefix=API_V1_PREFIX)
api_router.include_router(health.router, prefix=API_V1_PREFIX)
api_router.include_router(system.router, prefix=API_V1_PREFIX)

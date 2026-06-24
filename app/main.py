from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.api.router import api_router
from app.core.config import settings
from app.core.database import get_db

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="ContentOS AI backend API",
)

app.include_router(
    api_router,
    prefix=settings.api_v1_prefix,
)


@app.get("/")
def root():
    return {
        "app": settings.app_name,
        "environment": settings.app_env,
        "status": "running",
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok",
    }


@app.get("/health/db")
def database_health_check(
    db: Session = Depends(get_db),
):
    db.execute(text("SELECT 1"))

    return {
        "database": "connected",
    }

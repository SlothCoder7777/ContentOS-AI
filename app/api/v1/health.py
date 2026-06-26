from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.constants import APP_NAME, APP_VERSION
from app.core.database import get_db

router = APIRouter(
    prefix="/health",
    tags=["Health"],
)


@router.get("")
def health_check():
    return {
        "status": "healthy",
        "service": APP_NAME,
        "version": APP_VERSION,
    }


@router.get("/db")
def database_health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))

        return {
            "status": "healthy",
            "database": "connected",
        }

    except SQLAlchemyError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "status": "unhealthy",
                "database": "disconnected",
                "error": str(exc),
            },
        ) from exc

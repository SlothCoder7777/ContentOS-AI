from fastapi import APIRouter, status

from app.schemas.trend import TrendDetectRequest, TrendDetectResponse
from app.services.trend_service import TrendService

router = APIRouter(
    prefix="/trends",
    tags=["Trends"],
)


@router.get("/presets")
def get_trend_presets():
    return TrendService().get_presets()


@router.post(
    "/detect",
    response_model=TrendDetectResponse,
    status_code=status.HTTP_200_OK,
)
def detect_trends(
    request_data: TrendDetectRequest,
) -> TrendDetectResponse:
    return TrendService().detect_trends(request_data)

from fastapi import APIRouter

from app.models import HealthResponse
from app.services.health import build_health_response
from app.settings import get_settings


router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse, summary="Backend health check")
def get_health() -> HealthResponse:
    return build_health_response(get_settings())

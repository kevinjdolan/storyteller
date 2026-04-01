from fastapi import APIRouter

from app.models import HelloResponse
from app.services.health import build_hello_response
from app.settings import get_settings


router = APIRouter(prefix="/api", tags=["legacy"])


@router.get(
    "/hello",
    response_model=HelloResponse,
    include_in_schema=False,
    summary="Legacy hello check kept for the existing frontend scaffold",
)
def get_hello() -> HelloResponse:
    return build_hello_response(get_settings())

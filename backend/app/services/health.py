from typing import Optional

from app.db.status import get_database_dependency_status
from app.models import HealthResponse, HelloResponse
from app.settings import AppSettings


def build_health_response(
    settings: AppSettings,
    api_version: Optional[str] = None,
) -> HealthResponse:
    return HealthResponse(
        status="ok",
        service=settings.app_name,
        environment=settings.environment,
        version=settings.version,
        api_version=api_version,
        dependencies={
            "database": get_database_dependency_status(settings),
        },
    )


def build_hello_response(settings: AppSettings) -> HelloResponse:
    del settings
    return HelloResponse(message="Hello from FastAPI!")

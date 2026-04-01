from app.models import DependencyStatus
from app.settings import AppSettings


def get_database_dependency_status(settings: AppSettings) -> DependencyStatus:
    return DependencyStatus(
        status="configured",
        detail="A database URL is configured for the application runtime.",
    )

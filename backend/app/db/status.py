from app.models import DependencyStatus
from app.settings import AppSettings


def get_database_dependency_status(settings: AppSettings) -> DependencyStatus:
    if settings.database_url:
        return DependencyStatus(
            status="configured",
            detail="A database URL is configured for the application runtime.",
        )

    return DependencyStatus(
        status="not-configured",
        detail="Database wiring lands in a later prompt; this scaffold only reports configuration state.",
    )

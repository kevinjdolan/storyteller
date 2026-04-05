from app.models import DependencyStatus
from app.settings import AppSettings


def get_object_storage_dependency_status(settings: AppSettings) -> DependencyStatus:
    return DependencyStatus(
        status="configured",
        detail=(
            "A file-backed object storage backend is configured for session, audio, "
            "and export artifacts. Asset access stays mediated through backend routes."
        ),
    )

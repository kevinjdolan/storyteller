from app.models import DependencyStatus
from app.settings import AppSettings


def get_object_storage_dependency_status(settings: AppSettings) -> DependencyStatus:
    missing_fields = [
        name
        for name, value in (
            ("STORYTELLER_GCS_BUCKET_NAME", settings.gcs_bucket_name),
            ("STORYTELLER_GCS_ENDPOINT", settings.gcs_endpoint),
            ("STORYTELLER_GCS_PROJECT_ID", settings.gcs_project_id),
        )
        if not value
    ]

    if missing_fields:
        return DependencyStatus(
            status="not-configured",
            detail=(
                "Object storage wiring lands in a later prompt; missing "
                f"configuration for {', '.join(missing_fields)}."
            ),
        )

    public_url_detail = (
        f" Public URL: {settings.gcs_public_url}."
        if settings.gcs_public_url
        else ""
    )

    return DependencyStatus(
        status="configured",
        detail=(
            "A file-backed GCS emulator is configured for bucket "
            f"'{settings.gcs_bucket_name}' at {settings.gcs_endpoint}."
            f"{public_url_detail}"
        ),
    )

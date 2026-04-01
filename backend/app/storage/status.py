from app.models import DependencyStatus
from app.settings import AppSettings


def get_object_storage_dependency_status(settings: AppSettings) -> DependencyStatus:
    public_url_detail = (
        f" Public URL: {settings.gcs_public_url}."
        if settings.gcs_public_url
        else ""
    )
    bucket_detail = ", ".join(
        (
            settings.gcs_bucket_names.sessions,
            settings.gcs_bucket_names.audio,
            settings.gcs_bucket_names.exports,
        ),
    )

    return DependencyStatus(
        status="configured",
        detail=(
            "A file-backed GCS emulator is configured for buckets "
            f"{bucket_detail} at {settings.gcs_endpoint}."
            f"{public_url_detail}"
        ),
    )

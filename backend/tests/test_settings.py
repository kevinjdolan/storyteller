from app.settings import get_settings


def test_settings_read_database_and_object_storage_environment(
    monkeypatch,
) -> None:
    monkeypatch.setenv(
        "STORYTELLER_DATABASE_URL",
        "postgresql://storyteller:storyteller@postgres:5432/storyteller",
    )
    monkeypatch.setenv("STORYTELLER_GCS_BUCKET_NAME", "storyteller-dev")
    monkeypatch.setenv("STORYTELLER_GCS_ENDPOINT", "http://gcs:4443")
    monkeypatch.setenv("STORYTELLER_GCS_PROJECT_ID", "storyteller-local")
    monkeypatch.setenv("STORYTELLER_GCS_PUBLIC_URL", "http://localhost:8568")
    get_settings.cache_clear()

    settings = get_settings()

    assert settings.database_url == (
        "postgresql://storyteller:storyteller@postgres:5432/storyteller"
    )
    assert settings.gcs_bucket_name == "storyteller-dev"
    assert settings.gcs_endpoint == "http://gcs:4443"
    assert settings.gcs_project_id == "storyteller-local"
    assert settings.gcs_public_url == "http://localhost:8568"
    get_settings.cache_clear()

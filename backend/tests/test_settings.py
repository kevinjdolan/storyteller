from __future__ import annotations

import os
import subprocess
import sys
import textwrap
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.main import create_app
from app.settings import SettingsValidationError, get_settings, load_settings


BACKEND_ROOT = Path(__file__).resolve().parents[1]


def write_secrets_file(tmp_path: Path, body: str) -> Path:
    secrets_file = tmp_path / "secrets.yaml"
    secrets_file.write_text(textwrap.dedent(body).strip() + "\n", encoding="utf-8")
    return secrets_file


def test_settings_read_required_runtime_values_from_environment(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("STORYTELLER_SECRETS_FILE", "")
    monkeypatch.setenv(
        "STORYTELLER_DATABASE_URL",
        "postgresql://storyteller:storyteller@postgres:5432/storyteller",
    )
    monkeypatch.setenv("STORYTELLER_GEMINI_API_KEY", "env-api-key")
    monkeypatch.setenv("STORYTELLER_GCS_ENDPOINT", "http://gcs:4443")
    monkeypatch.setenv("STORYTELLER_GCS_PROJECT_ID", "storyteller-local")
    monkeypatch.setenv("STORYTELLER_GCS_PUBLIC_URL", "http://localhost:8568")
    monkeypatch.setenv("STORYTELLER_GCS_SESSIONS_BUCKET_NAME", "storyteller-sessions")
    monkeypatch.setenv("STORYTELLER_GCS_AUDIO_BUCKET_NAME", "storyteller-audio")
    monkeypatch.setenv("STORYTELLER_GCS_EXPORTS_BUCKET_NAME", "storyteller-exports")
    monkeypatch.setenv("STORYTELLER_FEATURE_ENABLE_API_DOCS", "false")
    get_settings.cache_clear()

    settings = get_settings()

    assert settings.database_url == (
        "postgresql://storyteller:storyteller@postgres:5432/storyteller"
    )
    assert settings.gemini_api_key == "env-api-key"
    assert settings.gcs_endpoint == "http://gcs:4443"
    assert settings.gcs_project_id == "storyteller-local"
    assert settings.gcs_public_url == "http://localhost:8568"
    assert settings.gcs_bucket_names.sessions == "storyteller-sessions"
    assert settings.gcs_bucket_names.audio == "storyteller-audio"
    assert settings.gcs_bucket_names.exports == "storyteller-exports"
    assert settings.feature_flags.enable_api_docs is False
    assert settings.secrets_file is None
    get_settings.cache_clear()


def test_settings_merge_local_secrets_file_when_present(tmp_path: Path) -> None:
    secrets_file = write_secrets_file(
        tmp_path,
        """
        database:
          url: postgresql://storyteller:storyteller@localhost:8567/storyteller
        gemini:
          api_key: secrets-api-key
        gcs:
          endpoint: http://localhost:8568
          project_id: storyteller-local
          public_url: http://localhost:8568
          buckets:
            sessions: storyteller-sessions
            audio: storyteller-audio
            exports: storyteller-exports
        cors:
          allowed_origins:
            - http://localhost:8566
            - http://127.0.0.1:8566
        feature_flags:
          enable_api_docs: true
          enable_audio_generation: true
          enable_debug_inspector: false
        """,
    )

    settings = load_settings(
        {"STORYTELLER_SECRETS_FILE": str(secrets_file)},
        cwd=tmp_path,
    )

    assert settings.database_url == (
        "postgresql://storyteller:storyteller@localhost:8567/storyteller"
    )
    assert settings.gemini_api_key == "secrets-api-key"
    assert settings.cors_allowed_origins == (
        "http://localhost:8566",
        "http://127.0.0.1:8566",
    )
    assert settings.feature_flags.enable_audio_generation is True
    assert settings.secrets_file == secrets_file


def test_environment_values_override_secrets_file(tmp_path: Path) -> None:
    secrets_file = write_secrets_file(
        tmp_path,
        """
        database:
          url: postgresql://storyteller:storyteller@localhost:8567/storyteller
        gemini:
          api_key: secrets-api-key
        gcs:
          endpoint: http://localhost:8568
          project_id: storyteller-local
          buckets:
            sessions: storyteller-sessions
            audio: storyteller-audio
            exports: storyteller-exports
        feature_flags:
          enable_api_docs: true
        """,
    )

    settings = load_settings(
        {
            "STORYTELLER_SECRETS_FILE": str(secrets_file),
            "STORYTELLER_DATABASE_URL": (
                "postgresql://storyteller:storyteller@postgres:5432/storyteller"
            ),
            "STORYTELLER_GEMINI_API_KEY": "env-api-key",
            "STORYTELLER_CORS_ALLOWED_ORIGINS": (
                "http://localhost:8566,http://127.0.0.1:8566,http://frontend:8566"
            ),
            "STORYTELLER_FEATURE_ENABLE_API_DOCS": "false",
        },
        cwd=tmp_path,
    )

    assert settings.database_url == (
        "postgresql://storyteller:storyteller@postgres:5432/storyteller"
    )
    assert settings.gemini_api_key == "env-api-key"
    assert settings.cors_allowed_origins == (
        "http://localhost:8566",
        "http://127.0.0.1:8566",
        "http://frontend:8566",
    )
    assert settings.feature_flags.enable_api_docs is False


def test_legacy_single_bucket_name_populates_all_runtime_buckets() -> None:
    settings = load_settings(
        {
            "STORYTELLER_SECRETS_FILE": "",
            "STORYTELLER_DATABASE_URL": (
                "postgresql://storyteller:storyteller@postgres:5432/storyteller"
            ),
            "STORYTELLER_GEMINI_API_KEY": "env-api-key",
            "STORYTELLER_GCS_ENDPOINT": "http://gcs:4443",
            "STORYTELLER_GCS_PROJECT_ID": "storyteller-local",
            "STORYTELLER_GCS_BUCKET_NAME": "storyteller-dev",
        },
    )

    assert settings.gcs_bucket_names.sessions == "storyteller-dev"
    assert settings.gcs_bucket_names.audio == "storyteller-dev"
    assert settings.gcs_bucket_names.exports == "storyteller-dev"


def test_api_docs_can_be_disabled_with_feature_flag(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("STORYTELLER_SECRETS_FILE", "")
    monkeypatch.setenv(
        "STORYTELLER_DATABASE_URL",
        "postgresql://storyteller:storyteller@postgres:5432/storyteller",
    )
    monkeypatch.setenv("STORYTELLER_GEMINI_API_KEY", "env-api-key")
    monkeypatch.setenv("STORYTELLER_GCS_ENDPOINT", "http://gcs:4443")
    monkeypatch.setenv("STORYTELLER_GCS_PROJECT_ID", "storyteller-local")
    monkeypatch.setenv("STORYTELLER_GCS_SESSIONS_BUCKET_NAME", "storyteller-sessions")
    monkeypatch.setenv("STORYTELLER_GCS_AUDIO_BUCKET_NAME", "storyteller-audio")
    monkeypatch.setenv("STORYTELLER_GCS_EXPORTS_BUCKET_NAME", "storyteller-exports")
    monkeypatch.setenv("STORYTELLER_FEATURE_ENABLE_API_DOCS", "false")
    get_settings.cache_clear()

    with TestClient(create_app()) as client:
        assert client.get("/docs").status_code == 404

    get_settings.cache_clear()


def test_missing_required_settings_raise_readable_validation_errors() -> None:
    with pytest.raises(SettingsValidationError) as exc_info:
        load_settings({"STORYTELLER_SECRETS_FILE": ""})

    message = str(exc_info.value)

    assert "Storyteller configuration is invalid." in message
    assert (
        "- database.url: missing required setting from "
        "STORYTELLER_DATABASE_URL or database.url"
    ) in message
    assert (
        "- gemini.api_key: missing required setting from "
        "STORYTELLER_GEMINI_API_KEY or gemini.api_key"
    ) in message
    assert (
        "- gcs.endpoint: missing required setting from "
        "STORYTELLER_GCS_ENDPOINT or gcs.endpoint"
    ) in message
    assert "STORYTELLER_* environment variables" in message


def test_invalid_secrets_yaml_is_reported_cleanly(tmp_path: Path) -> None:
    secrets_file = tmp_path / "secrets.yaml"
    secrets_file.write_text("database: [oops\n", encoding="utf-8")

    with pytest.raises(SettingsValidationError) as exc_info:
        load_settings(
            {"STORYTELLER_SECRETS_FILE": str(secrets_file)},
            cwd=tmp_path,
        )

    assert "Could not parse secrets file" in str(exc_info.value)


def test_python_module_startup_surfaces_configuration_errors_without_traceback() -> None:
    command_env = os.environ.copy()

    for variable_name in (
        "STORYTELLER_DATABASE_URL",
        "STORYTELLER_GEMINI_API_KEY",
        "STORYTELLER_GCS_ENDPOINT",
        "STORYTELLER_GCS_PROJECT_ID",
        "STORYTELLER_GCS_PUBLIC_URL",
        "STORYTELLER_GCS_SESSIONS_BUCKET_NAME",
        "STORYTELLER_GCS_AUDIO_BUCKET_NAME",
        "STORYTELLER_GCS_EXPORTS_BUCKET_NAME",
        "STORYTELLER_GCS_BUCKET_NAME",
    ):
        command_env.pop(variable_name, None)

    command_env["STORYTELLER_SECRETS_FILE"] = ""

    process = subprocess.run(
        [sys.executable, "-m", "app"],
        cwd=BACKEND_ROOT,
        capture_output=True,
        text=True,
        env=command_env,
        check=False,
    )

    assert process.returncode != 0
    assert "Storyteller configuration is invalid." in process.stderr
    assert "Traceback" not in process.stderr

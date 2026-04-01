from __future__ import annotations

import os
import logging
from functools import lru_cache
from pathlib import Path
from typing import Any, Mapping, Sequence

import yaml
from pydantic import BaseModel, ConfigDict, Field, SecretStr, ValidationError, field_validator


DEFAULT_CORS_ALLOWED_ORIGINS = (
    "http://localhost:8566",
    "http://127.0.0.1:8566",
)
PROJECT_ROOT = Path(__file__).resolve().parents[3]
BACKEND_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SECRETS_FILE_NAME = "secrets.yaml"
FIELD_HINTS = {
    "database.url": "STORYTELLER_DATABASE_URL or database.url",
    "gemini.api_key": "STORYTELLER_GEMINI_API_KEY or gemini.api_key",
    "gcs.endpoint": "STORYTELLER_GCS_ENDPOINT or gcs.endpoint",
    "gcs.project_id": "STORYTELLER_GCS_PROJECT_ID or gcs.project_id",
    "gcs.buckets.sessions": (
        "STORYTELLER_GCS_SESSIONS_BUCKET_NAME or gcs.buckets.sessions"
    ),
    "gcs.buckets.audio": "STORYTELLER_GCS_AUDIO_BUCKET_NAME or gcs.buckets.audio",
    "gcs.buckets.exports": (
        "STORYTELLER_GCS_EXPORTS_BUCKET_NAME or gcs.buckets.exports"
    ),
}


def _stringify_error_path(path: Sequence[Any]) -> str:
    return ".".join(str(item) for item in path if item != "__root__")


def _raise_missing_required_setting(field_path: str) -> None:
    hint = FIELD_HINTS.get(field_path, field_path)
    raise ValueError(f"missing required setting from {hint}")


def _normalize_string(value: str) -> str:
    return value.strip()


def _read_bool(value: Any, default: bool | None = None) -> bool | None:
    if value is None:
        return default

    if isinstance(value, bool):
        return value

    normalized = str(value).strip().lower()

    if normalized in {"1", "true", "yes", "on"}:
        return True

    if normalized in {"0", "false", "no", "off"}:
        return False

    raise ValueError(
        f"expected a boolean value but received {value!r}; use true/false, yes/no, or 1/0",
    )


def _read_int(value: Any, default: int) -> int:
    if value is None or value == "":
        return default

    return int(value)


def _read_string(value: Any, default: str | None = None) -> str | None:
    if value is None:
        return default

    normalized = str(value).strip()
    return normalized or default


def _read_env_bool(environ: Mapping[str, str], name: str) -> bool | None:
    try:
        return _read_bool(environ.get(name))
    except ValueError as exc:
        raise SettingsValidationError((f"{name}: {exc}",)) from None


def _read_env_int(environ: Mapping[str, str], name: str, default: int) -> int | None:
    if environ.get(name) is None:
        return None

    try:
        return _read_int(environ.get(name), default)
    except ValueError as exc:
        raise SettingsValidationError((f"{name}: {exc}",)) from None


def _read_env_string_list(
    environ: Mapping[str, str],
    name: str,
    default: tuple[str, ...],
) -> tuple[str, ...] | None:
    if environ.get(name) is None:
        return None

    try:
        return _read_string_list(environ.get(name), default)
    except ValueError as exc:
        raise SettingsValidationError((f"{name}: {exc}",)) from None


def _read_string_list(
    value: Any,
    default: tuple[str, ...],
) -> tuple[str, ...]:
    if value is None or value == "":
        return default

    if isinstance(value, str):
        items = [item.strip() for item in value.split(",")]
    elif isinstance(value, Sequence):
        items = [str(item).strip() for item in value]
    else:
        raise ValueError(
            "expected a comma-separated string or list of strings for CORS origins",
        )

    normalized = tuple(item for item in items if item)
    return normalized or default


def _normalize_api_prefix(value: str) -> str:
    prefix = value.strip() or "/api/v1"
    return prefix if prefix.startswith("/") else f"/{prefix}"


def _deep_merge(base: dict[str, Any], override: Mapping[str, Any]) -> dict[str, Any]:
    merged = dict(base)

    for key, value in override.items():
        if isinstance(value, Mapping) and isinstance(merged.get(key), Mapping):
            merged[key] = _deep_merge(dict(merged[key]), value)
            continue

        merged[key] = value

    return merged


def _discover_secrets_file(
    environ: Mapping[str, str],
    *,
    cwd: Path | None = None,
) -> Path | None:
    explicit = environ.get("STORYTELLER_SECRETS_FILE")
    search_root = cwd or Path.cwd()

    if explicit is not None:
        explicit = explicit.strip()

        if not explicit:
            return None

        candidate = Path(explicit).expanduser()

        if not candidate.is_absolute():
            candidate = (search_root / candidate).resolve()

        return candidate if candidate.is_file() else None

    candidates = (
        search_root / DEFAULT_SECRETS_FILE_NAME,
        BACKEND_ROOT / DEFAULT_SECRETS_FILE_NAME,
        PROJECT_ROOT / DEFAULT_SECRETS_FILE_NAME,
    )

    for candidate in candidates:
        if candidate.is_file():
            return candidate

    return None


def _load_secrets_file(path: Path | None) -> dict[str, Any]:
    if path is None:
        return {}

    try:
        raw_data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise SettingsValidationError(
            (
                f"Could not read secrets file at {path}: {exc.strerror or exc}",
            ),
        ) from exc
    except yaml.YAMLError as exc:
        raise SettingsValidationError(
            (
                f"Could not parse secrets file at {path}: {exc}",
            ),
        ) from exc

    if raw_data is None:
        return {}

    if not isinstance(raw_data, dict):
        raise SettingsValidationError(
            (
                f"Expected a mapping at the root of {path}, found {type(raw_data).__name__}.",
            ),
        )

    return raw_data


def _build_default_payload(environment: str) -> dict[str, Any]:
    return {
        "app_name": "Storyteller API",
        "environment": environment,
        "version": "0.1.0",
        "host": "0.0.0.0",
        "port": 8565,
        "reload": environment.lower() == "development",
        "api_v1_prefix": "/api/v1",
        "log_level": "INFO",
        "cors": {
            "allowed_origins": DEFAULT_CORS_ALLOWED_ORIGINS,
        },
        "database": {},
        "gemini": {},
        "gcs": {
            "buckets": {},
        },
        "feature_flags": {
            "enable_api_docs": environment.lower() != "production",
            "enable_audio_generation": False,
            "enable_debug_inspector": False,
        },
    }


def _build_environment_payload(environ: Mapping[str, str]) -> dict[str, Any]:
    legacy_bucket = _read_string(environ.get("STORYTELLER_GCS_BUCKET_NAME"))

    return {
        "app_name": _read_string(environ.get("STORYTELLER_APP_NAME")),
        "environment": _read_string(environ.get("STORYTELLER_ENVIRONMENT")),
        "version": _read_string(environ.get("STORYTELLER_VERSION")),
        "host": _read_string(environ.get("STORYTELLER_HOST")),
        "port": _read_env_int(environ, "STORYTELLER_PORT", 8565),
        "reload": _read_env_bool(environ, "STORYTELLER_RELOAD"),
        "api_v1_prefix": _read_string(environ.get("STORYTELLER_API_V1_PREFIX")),
        "log_level": _read_string(environ.get("STORYTELLER_LOG_LEVEL")),
        "cors": {
            "allowed_origins": _read_env_string_list(
                environ,
                "STORYTELLER_CORS_ALLOWED_ORIGINS",
                DEFAULT_CORS_ALLOWED_ORIGINS,
            ),
        },
        "database": {
            "url": _read_string(environ.get("STORYTELLER_DATABASE_URL")),
        },
        "gemini": {
            "api_key": _read_string(environ.get("STORYTELLER_GEMINI_API_KEY")),
            "planning_model": _read_string(
                environ.get("STORYTELLER_GEMINI_PLANNING_MODEL"),
            ),
            "composition_model": _read_string(
                environ.get("STORYTELLER_GEMINI_COMPOSITION_MODEL"),
            ),
            "tts_model": _read_string(environ.get("STORYTELLER_GEMINI_TTS_MODEL")),
        },
        "gcs": {
            "endpoint": _read_string(environ.get("STORYTELLER_GCS_ENDPOINT")),
            "project_id": _read_string(environ.get("STORYTELLER_GCS_PROJECT_ID")),
            "public_url": _read_string(environ.get("STORYTELLER_GCS_PUBLIC_URL")),
            "buckets": {
                "sessions": _read_string(
                    environ.get("STORYTELLER_GCS_SESSIONS_BUCKET_NAME"),
                    legacy_bucket,
                ),
                "audio": _read_string(
                    environ.get("STORYTELLER_GCS_AUDIO_BUCKET_NAME"),
                    legacy_bucket,
                ),
                "exports": _read_string(
                    environ.get("STORYTELLER_GCS_EXPORTS_BUCKET_NAME"),
                    legacy_bucket,
                ),
            },
        },
        "feature_flags": {
            "enable_api_docs": _read_env_bool(
                environ,
                "STORYTELLER_FEATURE_ENABLE_API_DOCS",
            ),
            "enable_audio_generation": _read_env_bool(
                environ,
                "STORYTELLER_FEATURE_ENABLE_AUDIO_GENERATION",
            ),
            "enable_debug_inspector": _read_env_bool(
                environ,
                "STORYTELLER_FEATURE_ENABLE_DEBUG_INSPECTOR",
            ),
        },
    }


def _prune_none_values(value: Any) -> Any:
    if isinstance(value, dict):
        pruned = {
            key: _prune_none_values(item)
            for key, item in value.items()
            if item is not None
        }
        return pruned

    return value


class SettingsValidationError(RuntimeError):
    def __init__(self, issues: Sequence[str]) -> None:
        self.issues = tuple(issues)
        super().__init__(self.format_for_cli())

    @classmethod
    def from_validation_error(cls, exc: ValidationError) -> "SettingsValidationError":
        issues = []

        for error in exc.errors():
            path = _stringify_error_path(error["loc"])
            if error["type"] == "missing" and path in FIELD_HINTS:
                message = f"missing required setting from {FIELD_HINTS[path]}"
            else:
                message = error["msg"]
            issues.append(f"{path}: {message}")

        return cls(issues)

    def format_for_cli(self) -> str:
        issue_list = "\n".join(f"- {issue}" for issue in self.issues)
        return (
            "Storyteller configuration is invalid.\n"
            f"{issue_list}\n"
            "Set the matching STORYTELLER_* environment variables or add the values "
            "to secrets.yaml. See docs/secrets-and-local-config.md for the supported "
            "shape and precedence rules."
        )


class BaseSettingsModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class CorsSettings(BaseSettingsModel):
    allowed_origins: tuple[str, ...] = DEFAULT_CORS_ALLOWED_ORIGINS

    @field_validator("allowed_origins", mode="before")
    @classmethod
    def validate_allowed_origins(cls, value: Any) -> tuple[str, ...]:
        return _read_string_list(value, DEFAULT_CORS_ALLOWED_ORIGINS)


class DatabaseSettings(BaseSettingsModel):
    url: str

    @field_validator("url")
    @classmethod
    def validate_url(cls, value: str) -> str:
        normalized = _normalize_string(value)

        if not normalized:
            _raise_missing_required_setting("database.url")

        return normalized


class GeminiSettings(BaseSettingsModel):
    api_key: SecretStr
    planning_model: str = "gemini-3.1-flash-lite"
    composition_model: str = "gemini-3.1-pro"
    tts_model: str = "gemini-tts"

    @field_validator("api_key", mode="before")
    @classmethod
    def validate_api_key(cls, value: Any) -> Any:
        normalized = _read_string(value)

        if not normalized:
            _raise_missing_required_setting("gemini.api_key")

        return normalized


class StorageBucketsSettings(BaseSettingsModel):
    sessions: str
    audio: str
    exports: str

    @field_validator("sessions", "audio", "exports")
    @classmethod
    def validate_bucket_name(cls, value: str, info: Any) -> str:
        normalized = _normalize_string(value)

        if not normalized:
            _raise_missing_required_setting(f"gcs.buckets.{info.field_name}")

        return normalized


class GCSSettings(BaseSettingsModel):
    endpoint: str
    project_id: str
    public_url: str | None = None
    buckets: StorageBucketsSettings

    @field_validator("endpoint")
    @classmethod
    def validate_endpoint(cls, value: str) -> str:
        normalized = _normalize_string(value)

        if not normalized:
            _raise_missing_required_setting("gcs.endpoint")

        return normalized

    @field_validator("project_id")
    @classmethod
    def validate_project_id(cls, value: str) -> str:
        normalized = _normalize_string(value)

        if not normalized:
            _raise_missing_required_setting("gcs.project_id")

        return normalized

    @field_validator("public_url")
    @classmethod
    def validate_public_url(cls, value: str | None) -> str | None:
        return _read_string(value)


class FeatureFlagsSettings(BaseSettingsModel):
    enable_api_docs: bool = True
    enable_audio_generation: bool = False
    enable_debug_inspector: bool = False


class AppSettings(BaseSettingsModel):
    app_name: str
    environment: str
    version: str
    host: str
    port: int
    reload: bool
    api_v1_prefix: str
    log_level: str
    cors: CorsSettings = Field(default_factory=CorsSettings)
    database: DatabaseSettings
    gemini: GeminiSettings
    gcs: GCSSettings
    feature_flags: FeatureFlagsSettings = Field(default_factory=FeatureFlagsSettings)
    secrets_file: Path | None = None

    @field_validator(
        "app_name",
        "environment",
        "version",
        "host",
    )
    @classmethod
    def validate_strings(cls, value: str) -> str:
        normalized = _normalize_string(value)

        if not normalized:
            raise ValueError("must not be empty")

        return normalized

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, value: str) -> str:
        normalized = _normalize_string(value).upper()

        if not normalized:
            raise ValueError("must not be empty")

        if not isinstance(getattr(logging, normalized, None), int):
            raise ValueError("must be a valid logging level")

        return normalized

    @field_validator("api_v1_prefix")
    @classmethod
    def validate_api_prefix(cls, value: str) -> str:
        return _normalize_api_prefix(value)

    @property
    def cors_allowed_origins(self) -> tuple[str, ...]:
        return self.cors.allowed_origins

    @property
    def database_url(self) -> str:
        return self.database.url

    @property
    def gemini_api_key(self) -> str:
        return self.gemini.api_key.get_secret_value()

    @property
    def gcs_endpoint(self) -> str:
        return self.gcs.endpoint

    @property
    def gcs_project_id(self) -> str:
        return self.gcs.project_id

    @property
    def gcs_public_url(self) -> str:
        return self.gcs.public_url or ""

    @property
    def gcs_bucket_names(self) -> StorageBucketsSettings:
        return self.gcs.buckets

    @property
    def gcs_bucket_name(self) -> str:
        return self.gcs.buckets.sessions


def load_settings(
    environ: Mapping[str, str] | None = None,
    *,
    cwd: Path | None = None,
) -> AppSettings:
    active_environ = os.environ if environ is None else environ
    environment = _read_string(
        active_environ.get("STORYTELLER_ENVIRONMENT"),
        "development",
    )
    default_payload = _build_default_payload(environment)
    secrets_file = _discover_secrets_file(active_environ, cwd=cwd)
    secrets_payload = _load_secrets_file(secrets_file)
    env_payload = _build_environment_payload(active_environ)
    payload = _deep_merge(default_payload, secrets_payload)
    payload = _deep_merge(payload, _prune_none_values(env_payload))

    if payload.get("reload") is None:
        payload["reload"] = payload.get("environment", "development").lower() == "development"

    payload["secrets_file"] = secrets_file

    try:
        return AppSettings.model_validate(payload)
    except ValidationError as exc:
        raise SettingsValidationError.from_validation_error(exc) from None


@lru_cache(maxsize=1)
def get_settings() -> AppSettings:
    return load_settings()

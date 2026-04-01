from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Tuple


DEFAULT_CORS_ALLOWED_ORIGINS = (
    "http://localhost:8566",
    "http://127.0.0.1:8566",
)


def _read_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)

    if value is None:
        return default

    return value.strip().lower() in {"1", "true", "yes", "on"}


def _read_int(name: str, default: int) -> int:
    value = os.getenv(name)

    if value is None:
        return default

    return int(value)


def _read_csv(name: str, default: Tuple[str, ...]) -> Tuple[str, ...]:
    value = os.getenv(name)

    if not value:
        return default

    items = tuple(item.strip() for item in value.split(",") if item.strip())
    return items or default


def _normalize_api_prefix(value: str) -> str:
    prefix = value.strip() or "/api/v1"
    return prefix if prefix.startswith("/") else f"/{prefix}"


@dataclass(frozen=True)
class AppSettings:
    app_name: str
    environment: str
    version: str
    host: str
    port: int
    reload: bool
    api_v1_prefix: str
    cors_allowed_origins: Tuple[str, ...]
    database_url: str
    log_level: str


@lru_cache(maxsize=1)
def get_settings() -> AppSettings:
    environment = os.getenv("STORYTELLER_ENVIRONMENT", "development").strip()

    return AppSettings(
        app_name=os.getenv("STORYTELLER_APP_NAME", "Storyteller API").strip(),
        environment=environment,
        version=os.getenv("STORYTELLER_VERSION", "0.1.0").strip(),
        host=os.getenv("STORYTELLER_HOST", "0.0.0.0").strip(),
        port=_read_int("STORYTELLER_PORT", 8565),
        reload=_read_bool(
            "STORYTELLER_RELOAD",
            environment.lower() == "development",
        ),
        api_v1_prefix=_normalize_api_prefix(
            os.getenv("STORYTELLER_API_V1_PREFIX", "/api/v1"),
        ),
        cors_allowed_origins=_read_csv(
            "STORYTELLER_CORS_ALLOWED_ORIGINS",
            DEFAULT_CORS_ALLOWED_ORIGINS,
        ),
        database_url=os.getenv("STORYTELLER_DATABASE_URL", "").strip(),
        log_level=os.getenv("STORYTELLER_LOG_LEVEL", "INFO").strip().upper(),
    )

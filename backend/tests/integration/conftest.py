from __future__ import annotations

import os
from collections.abc import Callable, Iterator
from pathlib import Path
from uuid import uuid4

import httpx
import pytest
from alembic import command
from alembic.config import Config
from app.db import Base, make_engine
from app.settings import AppSettings, load_settings
from app.storage import ObjectStorageService, build_object_storage_service
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine, make_url
from sqlalchemy.orm import Session, sessionmaker

BACKEND_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_POSTGRES_ADMIN_URL = "postgresql+psycopg://storyteller:storyteller@127.0.0.1:8567/postgres"
DEFAULT_GCS_ENDPOINT = "http://127.0.0.1:8568"
DEFAULT_GCS_PUBLIC_URL = "http://127.0.0.1:8568"
DEFAULT_GCS_PROJECT_ID = "storyteller-local"
DEFAULT_GCS_BUCKET_NAME = "storyteller-sessions"
DEFAULT_GCS_AUDIO_BUCKET_NAME = "storyteller-audio"
DEFAULT_GCS_EXPORTS_BUCKET_NAME = "storyteller-exports"


def _build_alembic_config(database_url: str) -> Config:
    config = Config(str(BACKEND_ROOT / "alembic.ini"))
    config.set_main_option("script_location", str(BACKEND_ROOT / "migrations"))
    config.set_main_option("sqlalchemy.url", database_url)
    return config


def _assert_postgres_available(admin_url: str) -> None:
    engine = create_engine(admin_url, future=True, pool_pre_ping=True)

    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
    except Exception as exc:  # pragma: no cover - exercised only when local services are missing
        raise RuntimeError(
            "Postgres integration service is unavailable. Start the local compose stack with "
            "`./scripts/dev-compose.sh up -d postgres gcs` or run `make backend-integration-test`."
        ) from exc
    finally:
        engine.dispose()


def _assert_gcs_available(endpoint: str) -> None:
    try:
        response = httpx.get(
            f"{endpoint.rstrip('/')}/storage/v1/b",
            timeout=5.0,
        )
        response.raise_for_status()
    except Exception as exc:  # pragma: no cover - exercised only when local services are missing
        raise RuntimeError(
            "Fake GCS integration service is unavailable. Start the local compose stack with "
            "`./scripts/dev-compose.sh up -d postgres gcs` or run `make backend-integration-test`."
        ) from exc


def _build_database_url(admin_url: str, database_name: str) -> str:
    return make_url(admin_url).set(database=database_name).render_as_string(hide_password=False)


def _drop_database(admin_engine: Engine, database_name: str) -> None:
    with admin_engine.connect() as connection:
        connection.execute(
            text(
                """
                SELECT pg_terminate_backend(pid)
                FROM pg_stat_activity
                WHERE datname = :database_name
                  AND pid <> pg_backend_pid()
                """
            ),
            {"database_name": database_name},
        )
        connection.execute(text(f'DROP DATABASE IF EXISTS "{database_name}"'))


def _truncate_application_tables(engine: Engine) -> None:
    table_names = [table.name for table in Base.metadata.sorted_tables]

    if not table_names:
        return

    joined_table_names = ", ".join(f'"{table_name}"' for table_name in table_names)

    with engine.begin() as connection:
        connection.exec_driver_sql(f"TRUNCATE TABLE {joined_table_names} CASCADE")


@pytest.fixture(scope="session")
def postgres_admin_url() -> str:
    admin_url = os.environ.get(
        "STORYTELLER_INTEGRATION_POSTGRES_ADMIN_URL",
        DEFAULT_POSTGRES_ADMIN_URL,
    ).strip()
    _assert_postgres_available(admin_url)
    return admin_url


@pytest.fixture(scope="session")
def gcs_endpoint() -> str:
    endpoint = os.environ.get(
        "STORYTELLER_INTEGRATION_GCS_ENDPOINT",
        DEFAULT_GCS_ENDPOINT,
    ).strip()
    _assert_gcs_available(endpoint)
    return endpoint


@pytest.fixture(scope="session")
def postgres_admin_engine(postgres_admin_url: str) -> Iterator[Engine]:
    engine = create_engine(
        postgres_admin_url,
        isolation_level="AUTOCOMMIT",
        future=True,
        pool_pre_ping=True,
    )

    try:
        yield engine
    finally:
        engine.dispose()


@pytest.fixture(scope="session")
def temporary_database_url_factory(
    postgres_admin_url: str,
    postgres_admin_engine: Engine,
) -> Iterator[Callable[[], str]]:
    created_database_names: list[str] = []

    def create_database() -> str:
        database_name = f"storyteller_it_{uuid4().hex}"

        with postgres_admin_engine.connect() as connection:
            connection.execute(text(f'CREATE DATABASE "{database_name}"'))

        created_database_names.append(database_name)
        return _build_database_url(postgres_admin_url, database_name)

    try:
        yield create_database
    finally:
        for database_name in reversed(created_database_names):
            _drop_database(postgres_admin_engine, database_name)


@pytest.fixture(scope="session")
def integration_database_url(
    temporary_database_url_factory: Callable[[], str],
) -> str:
    database_url = temporary_database_url_factory()
    command.upgrade(_build_alembic_config(database_url), "head")
    return database_url


@pytest.fixture(scope="session")
def postgres_engine(integration_database_url: str) -> Iterator[Engine]:
    engine = make_engine(integration_database_url)

    try:
        yield engine
    finally:
        engine.dispose()


@pytest.fixture
def db_session_factory(postgres_engine: Engine) -> Iterator[sessionmaker[Session]]:
    _truncate_application_tables(postgres_engine)
    factory = sessionmaker(bind=postgres_engine, autoflush=False, expire_on_commit=False)

    try:
        yield factory
    finally:
        _truncate_application_tables(postgres_engine)


@pytest.fixture(scope="session")
def integration_settings(
    integration_database_url: str,
    gcs_endpoint: str,
) -> AppSettings:
    public_url = os.environ.get(
        "STORYTELLER_INTEGRATION_GCS_PUBLIC_URL",
        DEFAULT_GCS_PUBLIC_URL,
    ).strip()
    project_id = os.environ.get(
        "STORYTELLER_INTEGRATION_GCS_PROJECT_ID",
        DEFAULT_GCS_PROJECT_ID,
    ).strip()

    return load_settings(
        {
            "STORYTELLER_SECRETS_FILE": "",
            "STORYTELLER_DATABASE_URL": integration_database_url,
            "STORYTELLER_GEMINI_API_KEY": "test-gemini-key",
            "STORYTELLER_GCS_ENDPOINT": gcs_endpoint,
            "STORYTELLER_GCS_PROJECT_ID": project_id,
            "STORYTELLER_GCS_PUBLIC_URL": public_url,
            "STORYTELLER_GCS_SESSIONS_BUCKET_NAME": os.environ.get(
                "STORYTELLER_INTEGRATION_GCS_SESSIONS_BUCKET_NAME",
                DEFAULT_GCS_BUCKET_NAME,
            ),
            "STORYTELLER_GCS_AUDIO_BUCKET_NAME": os.environ.get(
                "STORYTELLER_INTEGRATION_GCS_AUDIO_BUCKET_NAME",
                DEFAULT_GCS_AUDIO_BUCKET_NAME,
            ),
            "STORYTELLER_GCS_EXPORTS_BUCKET_NAME": os.environ.get(
                "STORYTELLER_INTEGRATION_GCS_EXPORTS_BUCKET_NAME",
                DEFAULT_GCS_EXPORTS_BUCKET_NAME,
            ),
        },
    )


@pytest.fixture
def object_storage(integration_settings: AppSettings) -> Iterator[ObjectStorageService]:
    storage = build_object_storage_service(integration_settings)

    try:
        storage.ensure_runtime_buckets()
        yield storage
    finally:
        storage.close()

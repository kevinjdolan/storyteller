import os
import sys
from collections.abc import Iterator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

BACKEND_ROOT = Path(__file__).resolve().parents[1]
TEST_ENVIRONMENT_DEFAULTS = {
    "STORYTELLER_SECRETS_FILE": "",
    "STORYTELLER_DATABASE_URL": (
        "postgresql+psycopg://storyteller:storyteller@postgres:5432/storyteller"
    ),
    "STORYTELLER_GEMINI_API_KEY": "test-gemini-key",
    "STORYTELLER_GCS_ENDPOINT": "http://gcs:4443",
    "STORYTELLER_GCS_PROJECT_ID": "storyteller-local",
    "STORYTELLER_GCS_PUBLIC_URL": "http://localhost:8568",
    "STORYTELLER_GCS_SESSIONS_BUCKET_NAME": "storyteller-sessions",
    "STORYTELLER_GCS_AUDIO_BUCKET_NAME": "storyteller-audio",
    "STORYTELLER_GCS_EXPORTS_BUCKET_NAME": "storyteller-exports",
}

if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

for name, value in TEST_ENVIRONMENT_DEFAULTS.items():
    os.environ.setdefault(name, value)


def _integration_enabled(config: pytest.Config) -> bool:
    if config.getoption("--run-integration"):
        return True

    return os.environ.get("STORYTELLER_RUN_INTEGRATION_TESTS", "").strip().lower() in {
        "1",
        "true",
        "yes",
        "on",
    }


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--run-integration",
        action="store_true",
        default=False,
        help="run integration tests that require local Postgres and fake GCS services",
    )


def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
    if _integration_enabled(config):
        return

    skip_integration = pytest.mark.skip(
        reason=(
            "integration tests are disabled by default; pass --run-integration or set "
            "STORYTELLER_RUN_INTEGRATION_TESTS=1"
        ),
    )

    for item in items:
        if "integration" in item.keywords:
            item.add_marker(skip_integration)


@pytest.fixture
def client() -> Iterator[TestClient]:
    from app.main import create_app
    from app.settings import get_settings

    get_settings.cache_clear()

    with TestClient(create_app()) as test_client:
        yield test_client

    get_settings.cache_clear()

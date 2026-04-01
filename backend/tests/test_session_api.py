from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Iterator

import pytest
from fastapi.testclient import TestClient
from app.db import Base, StorySession
from app.db.session import get_engine, get_session_factory
from app.main import create_app
from app.models import WorkflowStage, WorkflowStageState
from app.services.sessions import SessionService
from app.settings import get_settings


@pytest.fixture
def session_api_client(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Iterator[TestClient]:
    database_path = tmp_path / "session-api.sqlite3"
    monkeypatch.setenv("STORYTELLER_DATABASE_URL", f"sqlite+pysqlite:///{database_path}")

    get_settings.cache_clear()
    get_engine.cache_clear()
    get_session_factory.cache_clear()

    engine = get_engine()
    Base.metadata.create_all(engine)

    with TestClient(create_app()) as test_client:
        yield test_client

    get_settings.cache_clear()
    get_engine.cache_clear()
    get_session_factory.cache_clear()


def test_list_recent_sessions_endpoint_returns_sessions_with_latest_first(
    session_api_client: TestClient,
) -> None:
    db_session = get_session_factory()()
    try:
        service = SessionService(db_session)
        older = service.create_session(working_title="Older Session")
        newer = service.create_session(working_title="Newer Session")

        older_row = db_session.get(StorySession, older.id)
        newer_row = db_session.get(StorySession, newer.id)
        assert older_row is not None and newer_row is not None

        older_row.updated_at = datetime.now(timezone.utc) - timedelta(days=1)
        newer_row.updated_at = datetime.now(timezone.utc)
        db_session.commit()

        service.update_stage_state(
            newer.id,
            stage=WorkflowStage.GENRE,
            status=WorkflowStageState.COMPLETED,
            detail="Accepted quest fantasy.",
        )
    finally:
        db_session.close()

    response = session_api_client.get("/api/v1/sessions")

    assert response.status_code == 200
    payload = response.json()

    assert [session["display_title"] for session in payload[:2]] == [
        "Newer Session",
        "Older Session",
    ]
    assert payload[0]["overall_status"] == "in_progress"
    assert payload[0]["current_stage"] == "tone"
    assert payload[0]["progress"]["completed_stages"] == 1
    assert payload[1]["overall_status"] == "draft"
    assert payload[1]["progress"]["completed_stages"] == 0


def test_create_session_endpoint_returns_a_fresh_snapshot(
    session_api_client: TestClient,
) -> None:
    response = session_api_client.post(
        "/api/v1/sessions",
        json={"working_title": "  Moonlit Harbor  "},
    )

    assert response.status_code == 201
    payload = response.json()

    assert payload["display_title"] == "Moonlit Harbor"
    assert payload["working_title"] == "Moonlit Harbor"
    assert payload["resume_stage"] == "genre"
    assert payload["overall_status"] == "draft"
    assert payload["progress"] == {
        "total_stages": 10,
        "completed_stages": 0,
        "in_progress_stages": 0,
        "needs_regeneration_stages": 0,
    }

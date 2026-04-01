from __future__ import annotations

from pathlib import Path
from typing import Iterator

import pytest
from app.db import Base, Genre, ToneProfile
from app.db.session import get_engine, get_session_factory
from app.main import create_app
from app.services import SessionService
from app.settings import get_settings
from fastapi.testclient import TestClient


@pytest.fixture
def action_policy_api_client(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> Iterator[TestClient]:
    database_path = tmp_path / "action-policy-api.sqlite3"
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


def test_evaluate_actions_endpoint_returns_structured_policy_decisions(
    action_policy_api_client: TestClient,
) -> None:
    db_session = get_session_factory()()
    try:
        genre = Genre(
            slug="quest-fantasy",
            label="Quest Fantasy",
            description="A soft quest.",
        )
        tone = ToneProfile(
            genre=genre,
            slug="hushed-wonder",
            label="Hushed Wonder",
            description="Quiet and luminous.",
        )
        db_session.add_all([genre, tone])
        db_session.flush()
        session_id = SessionService(db_session).create_session(working_title="Lantern Cove").id
        db_session.commit()
    finally:
        db_session.close()

    response = action_policy_api_client.post(
        f"/api/v1/sessions/{session_id}/actions/evaluate",
        json={
            "actions": [
                {
                    "action": {
                        "schema_version": 1,
                        "action_type": "select_tone",
                        "target_stage": "tone",
                        "confidence": 0.82,
                        "rationale": "The user asked for a hushed tone.",
                        "requires_confirmation": True,
                        "extracted_values": {
                            "tone_profile_slug": "hushed-wonder",
                        },
                    }
                }
            ]
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["session_id"] == session_id
    assert payload["evaluated_actions"][0]["decision"] == "rejected"
    assert payload["evaluated_actions"][0]["prerequisite_action_types"] == ["select_genre"]
    assert payload["evaluated_actions"][0]["reasons"][0]["code"] == (
        "prerequisite_selection_missing"
    )


def test_evaluate_actions_endpoint_returns_404_for_missing_session(
    action_policy_api_client: TestClient,
) -> None:
    response = action_policy_api_client.post(
        "/api/v1/sessions/missing-session/actions/evaluate",
        json={"actions": []},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "session 'missing-session' was not found"}

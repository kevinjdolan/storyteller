from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Iterator

import pytest
from app.db import Base, StorySession
from app.db.session import get_engine, get_session_factory
from app.main import create_app
from app.models import WorkflowStage, WorkflowStageState
from app.services.sessions import SessionService
from app.settings import get_settings
from fastapi.testclient import TestClient


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


def test_get_session_snapshot_endpoint_returns_full_snapshot(
    session_api_client: TestClient,
) -> None:
    create_response = session_api_client.post(
        "/api/v1/sessions",
        json={"working_title": "Moonlit Harbor"},
    )
    created = create_response.json()

    response = session_api_client.get(f"/api/v1/sessions/{created['id']}")

    assert response.status_code == 200
    payload = response.json()

    assert payload["id"] == created["id"]
    assert payload["display_title"] == "Moonlit Harbor"
    assert payload["current_stage"] == "genre"
    assert payload["progress"]["total_stages"] == 10
    assert len(payload["stage_states"]) == 10
    assert payload["stage_states"][0]["stage"] == "genre"
    assert payload["stage_states"][0]["status"] == "draft"
    assert payload["agent_context_summary"].startswith("Session title: Moonlit Harbor")


def test_hydrate_session_endpoint_returns_snapshot_history_and_metadata(
    session_api_client: TestClient,
) -> None:
    create_response = session_api_client.post(
        "/api/v1/sessions",
        json={"working_title": "Moonlit Harbor"},
    )
    created = create_response.json()

    response = session_api_client.get(f"/api/v1/sessions/{created['id']}/hydrate")

    assert response.status_code == 200
    payload = response.json()

    assert payload["snapshot"]["id"] == created["id"]
    assert payload["recent_history"]["session_id"] == created["id"]
    assert payload["recent_history"]["events"][0]["event_type"] == "session.created"
    assert payload["hydration"]["strategy"] == "materialized_only"
    assert payload["hydration"]["latest_sequence_number"] == 1
    assert payload["hydration"]["history_event_count"] == 1


def test_get_session_history_endpoint_returns_durable_timeline(
    session_api_client: TestClient,
) -> None:
    create_response = session_api_client.post(
        "/api/v1/sessions",
        json={"working_title": "History Check"},
    )
    created = create_response.json()

    response = session_api_client.get(f"/api/v1/sessions/{created['id']}/history")

    assert response.status_code == 200
    payload = response.json()

    assert payload["session_id"] == created["id"]
    assert payload["latest_sequence_number"] == 1
    assert payload["events"][0]["event_type"] == "session.created"


def test_record_session_ui_action_endpoint_returns_recorded_event(
    session_api_client: TestClient,
) -> None:
    create_response = session_api_client.post(
        "/api/v1/sessions",
        json={"working_title": "Echo Source"},
    )
    created = create_response.json()

    response = session_api_client.post(
        f"/api/v1/sessions/{created['id']}/ui-actions",
        json={
            "action": "navigate_to_stage",
            "stage": "audio",
            "control_id": "stage-navigator",
            "value_summary": "Audio",
            "origin": "workspace",
        },
    )

    assert response.status_code == 201
    payload = response.json()

    assert payload["event_type"] == "ui.action.recorded"
    assert payload["stage"] == "audio"
    assert payload["payload"]["action"] == "navigate_to_stage"
    assert payload["payload"]["control_id"] == "stage-navigator"
    assert payload["payload"]["value_summary"] == "Audio"
    assert payload["payload"]["origin"] == "workspace"


def test_hydrate_session_endpoint_preserves_chat_navigation_bridge_history(
    session_api_client: TestClient,
) -> None:
    create_response = session_api_client.post(
        "/api/v1/sessions",
        json={"working_title": "Bridge Replay"},
    )
    created = create_response.json()

    parse_response = session_api_client.post(
        f"/api/v1/sessions/{created['id']}/chat/intents",
        json={
            "message": "/next-stage",
            "explicit_command": {
                "command_id": "next_stage",
                "source": "quick_action",
                "proposed_actions": {
                    "schema_version": 1,
                    "actions": [
                        {
                            "schema_version": 1,
                            "action_type": "navigate_to_stage",
                            "target_stage": "tone",
                            "confidence": 1,
                            "rationale": "Explicit command requested navigation to Tone.",
                            "requires_confirmation": False,
                            "extracted_values": {},
                        }
                    ],
                },
            },
        },
    )

    assert parse_response.status_code == 200
    assert parse_response.json()["policy_evaluation"]["evaluated_actions"][0]["decision"] == (
        "accepted"
    )

    ui_action_response = session_api_client.post(
        f"/api/v1/sessions/{created['id']}/ui-actions",
        json={
            "action": "navigate_to_stage",
            "stage": "tone",
            "control_id": "chat-intent",
            "value_summary": "Tone",
            "origin": "chat",
        },
    )

    assert ui_action_response.status_code == 201

    hydration_response = session_api_client.get(f"/api/v1/sessions/{created['id']}/hydrate")

    assert hydration_response.status_code == 200
    payload = hydration_response.json()

    assert [event["event_type"] for event in payload["recent_history"]["events"]] == [
        "session.created",
        "chat.message.recorded",
        "chat.intent.parsed",
        "chat.message.recorded",
        "ui.action.recorded",
    ]
    assert payload["recent_history"]["events"][-1]["payload"] == {
        "schema_version": 1,
        "action": "navigate_to_stage",
        "control_id": "chat-intent",
        "value_summary": "Tone",
        "origin": "chat",
    }
    assert payload["snapshot"]["current_stage"] == "genre"
    assert payload["snapshot"]["resume_stage"] == "genre"
    assert payload["hydration"]["strategy"] == "materialized_only"
    assert payload["hydration"]["latest_sequence_number"] == 5
    assert payload["hydration"]["history_event_count"] == 5


def test_apply_session_context_update_endpoint_returns_updated_snapshot_and_event(
    session_api_client: TestClient,
) -> None:
    db_session = get_session_factory()()
    try:
        snapshot = SessionService(db_session).create_session(working_title="Context Update")
        service = SessionService(db_session)
        for stage in (
            WorkflowStage.GENRE,
            WorkflowStage.TONE,
            WorkflowStage.BRIEF,
            WorkflowStage.PITCHES,
            WorkflowStage.CHARACTERS,
            WorkflowStage.BEATS,
        ):
            service.update_stage_state(
                snapshot.id,
                stage=stage,
                status=WorkflowStageState.COMPLETED,
                detail=f"Accepted {stage.value}.",
            )
    finally:
        db_session.close()

    response = session_api_client.post(
        f"/api/v1/sessions/{snapshot.id}/context-updates",
        json={
            "target_kind": "stage_note",
            "stage": "beats",
            "control_id": "stage-note-editor",
            "origin": "workspace",
            "values": {
                "detail": "Add one calmer beat before the return home.",
            },
        },
    )

    assert response.status_code == 200
    payload = response.json()

    assert payload["event"]["event_type"] == "content.user_edit.recorded"
    assert payload["event"]["payload"]["field_values"] == {
        "detail": "Add one calmer beat before the return home.",
        "control_id": "stage-note-editor",
    }
    assert payload["snapshot"]["stage_states"][5]["detail"] == (
        "Add one calmer beat before the return home."
    )
    assert payload["snapshot"]["stage_states"][7]["status"] == "draft"
    assert (
        "Latest saved UI detail: Beat sheet: Add one calmer beat"
        in payload["snapshot"]["agent_context_summary"]
    )


def test_hydrate_session_endpoint_replays_context_updates_into_resumed_snapshot(
    session_api_client: TestClient,
) -> None:
    db_session = get_session_factory()()
    try:
        service = SessionService(db_session)
        snapshot = service.create_session(working_title="Replay Context")
        for stage in (
            WorkflowStage.GENRE,
            WorkflowStage.TONE,
            WorkflowStage.BRIEF,
            WorkflowStage.PITCHES,
            WorkflowStage.CHARACTERS,
            WorkflowStage.BEATS,
            WorkflowStage.STORY_SETUP,
            WorkflowStage.COMPOSITION,
            WorkflowStage.AUDIO,
        ):
            service.update_stage_state(
                snapshot.id,
                stage=stage,
                status=WorkflowStageState.COMPLETED,
                detail=f"Accepted {stage.value}.",
            )
    finally:
        db_session.close()

    ui_action_response = session_api_client.post(
        f"/api/v1/sessions/{snapshot.id}/ui-actions",
        json={
            "action": "navigate_to_stage",
            "stage": "audio",
            "control_id": "stage-navigator",
            "value_summary": "Audio",
            "origin": "workspace",
        },
    )
    assert ui_action_response.status_code == 201

    context_update_response = session_api_client.post(
        f"/api/v1/sessions/{snapshot.id}/context-updates",
        json={
            "target_kind": "stage_note",
            "stage": "beats",
            "control_id": "stage-note-editor",
            "origin": "workspace",
            "values": {
                "detail": "Soften the midpoint and let the return home land faster.",
            },
        },
    )
    assert context_update_response.status_code == 200

    hydration_response = session_api_client.get(f"/api/v1/sessions/{snapshot.id}/hydrate")

    assert hydration_response.status_code == 200
    payload = hydration_response.json()

    assert [event["event_type"] for event in payload["recent_history"]["events"][-3:]] == [
        "ui.action.recorded",
        "workflow.stage_changed",
        "content.user_edit.recorded",
    ]
    assert payload["snapshot"]["stage_states"][5]["detail"] == (
        "Soften the midpoint and let the return home land faster."
    )
    assert payload["snapshot"]["stage_states"][7]["status"] == "needs_regeneration"
    assert payload["snapshot"]["stage_states"][8]["status"] == "needs_regeneration"
    assert payload["snapshot"]["resume_stage"] == "composition"
    assert payload["snapshot"]["overall_status"] == "needs_regeneration"
    assert payload["hydration"]["history_event_count"] == 13
    assert payload["hydration"]["latest_sequence_number"] == 13


def test_get_session_snapshot_endpoint_returns_404_for_missing_session(
    session_api_client: TestClient,
) -> None:
    response = session_api_client.get("/api/v1/sessions/missing-session")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "session 'missing-session' was not found",
    }


def test_hydrate_session_endpoint_returns_404_for_missing_session(
    session_api_client: TestClient,
) -> None:
    response = session_api_client.get("/api/v1/sessions/missing-session/hydrate")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "session 'missing-session' was not found",
    }


def test_record_session_ui_action_endpoint_returns_404_for_missing_session(
    session_api_client: TestClient,
) -> None:
    response = session_api_client.post(
        "/api/v1/sessions/missing-session/ui-actions",
        json={
            "action": "navigate_to_stage",
            "stage": "audio",
        },
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "session 'missing-session' was not found",
    }


def test_apply_session_context_update_endpoint_returns_422_for_unsupported_stage(
    session_api_client: TestClient,
) -> None:
    create_response = session_api_client.post(
        "/api/v1/sessions",
        json={"working_title": "Unsupported Stage"},
    )
    created = create_response.json()

    response = session_api_client.post(
        f"/api/v1/sessions/{created['id']}/context-updates",
        json={
            "target_kind": "stage_note",
            "stage": "genre",
            "values": {
                "detail": "Quest fantasy should lean quieter.",
            },
        },
    )

    assert response.status_code == 422
    assert "does not support durable note edits" in response.json()["detail"]


def test_apply_session_context_update_endpoint_returns_409_for_invalid_transition(
    session_api_client: TestClient,
) -> None:
    create_response = session_api_client.post(
        "/api/v1/sessions",
        json={"working_title": "Transition Guard"},
    )
    created = create_response.json()

    response = session_api_client.post(
        f"/api/v1/sessions/{created['id']}/context-updates",
        json={
            "target_kind": "stage_note",
            "stage": "story_setup",
            "values": {
                "detail": "Target a shorter read-aloud.",
            },
        },
    )

    assert response.status_code == 409
    assert "cannot set 'story_setup' to 'in_progress' before prerequisites are completed" in (
        response.json()["detail"]
    )


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

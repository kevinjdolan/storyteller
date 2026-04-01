from __future__ import annotations

from pathlib import Path
from typing import Iterator

import pytest
from app.db import Base
from app.db.session import get_engine, get_session_factory
from app.main import create_app
from app.models import IntentParserInvocationResult, IntentParserStructuredOutput
from app.services import SessionEventLogService, SessionService
from app.settings import get_settings
from fastapi.testclient import TestClient


class StubIntentParserAdapter:
    def __init__(self, structured_output: IntentParserStructuredOutput) -> None:
        self.model_id = "gemini-3.1-flash-lite"
        self._structured_output = structured_output

    def parse(self, invocation):
        return IntentParserInvocationResult(
            invocation=invocation,
            structured_output=self._structured_output,
            raw_response={"mock": "response"},
        )

    def close(self) -> None:
        return None


@pytest.fixture
def intent_parser_api_client(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> Iterator[tuple[TestClient, StubIntentParserAdapter]]:
    database_path = tmp_path / "intent-parser-api.sqlite3"
    monkeypatch.setenv("STORYTELLER_DATABASE_URL", f"sqlite+pysqlite:///{database_path}")

    get_settings.cache_clear()
    get_engine.cache_clear()
    get_session_factory.cache_clear()

    engine = get_engine()
    Base.metadata.create_all(engine)
    app = create_app()
    adapter = StubIntentParserAdapter(
        IntentParserStructuredOutput.model_validate(
            {
                "schema_version": 1,
                "status": "parsed",
                "needs_clarification": False,
                "assistant_response": "I can shorten the setup target and make the notes moodier.",
                "proposed_actions": {
                    "schema_version": 1,
                    "actions": [
                        {
                            "action_type": "update_story_setup",
                            "target_stage": "story_setup",
                            "confidence": 0.86,
                            "rationale": "The user asked for a shorter story.",
                            "requires_confirmation": False,
                            "extracted_values": {
                                "target_runtime_minutes": 9,
                                "guidance_notes": "Lean slightly more mysterious.",
                            },
                        }
                    ],
                },
            }
        )
    )
    app.state.intent_parser_adapter = adapter

    with TestClient(app) as test_client:
        yield test_client, adapter

    get_settings.cache_clear()
    get_engine.cache_clear()
    get_session_factory.cache_clear()


def test_parse_chat_intents_endpoint_returns_structured_actions_and_logs_audit_event(
    intent_parser_api_client: tuple[TestClient, StubIntentParserAdapter],
) -> None:
    client, _adapter = intent_parser_api_client
    db_session = get_session_factory()()
    try:
        session_id = SessionService(db_session).create_session(working_title="Lantern Cove").id
    finally:
        db_session.close()

    response = client.post(
        f"/api/v1/sessions/{session_id}/chat/intents",
        json={"message": "make it shorter and moodier"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "parsed"
    assert payload["assistant_response"] == (
        "I can shorten the setup target and make the notes moodier."
    )
    assert payload["proposed_actions"]["actions"][0]["action_type"] == "update_story_setup"
    assert payload["proposed_actions"]["actions"][0]["requires_confirmation"] is False
    assert payload["policy_evaluation"]["evaluated_actions"][0]["decision"] == "rejected"
    assert payload["policy_evaluation"]["evaluated_actions"][0]["reasons"][0]["code"] == (
        "prerequisite_stage_incomplete"
    )

    db_session = get_session_factory()()
    try:
        history = SessionEventLogService(db_session).list_session_history(session_id)
    finally:
        db_session.close()

    assert history.events[-2].event_type == "chat.intent.parsed"
    assert history.events[-2].payload is not None
    assert history.events[-2].payload.model_id == "gemini-3.1-flash-lite"
    assert history.events[-2].payload.result.proposed_actions.actions[0].action_type == (
        "update_story_setup"
    )


def test_parse_chat_intents_endpoint_returns_404_for_missing_session(
    intent_parser_api_client: tuple[TestClient, StubIntentParserAdapter],
) -> None:
    client, _adapter = intent_parser_api_client

    response = client.post(
        "/api/v1/sessions/missing-session/chat/intents",
        json={"message": "make it shorter and moodier"},
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "session 'missing-session' was not found",
    }

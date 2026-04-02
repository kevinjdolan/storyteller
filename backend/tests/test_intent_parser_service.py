from __future__ import annotations

from datetime import datetime, timezone

import pytest
from app.ai import IntentParserTransportError
from app.db import (
    Base,
    CharacterSheet,
    Genre,
    Pitch,
    StoryBrief,
    StorySession,
    ToneProfile,
    make_engine,
)
from app.models import (
    ChatToUIActionType,
    IntentParserStatus,
    IntentParserStructuredOutput,
    SessionActionDecision,
    SessionContextUpdateRequest,
    SessionEventType,
    WorkflowStage,
    WorkflowStageState,
)
from app.services import SessionEventLogService, SessionIntentParserService, SessionService
from sqlalchemy.orm import sessionmaker


def _enable_sqlite_foreign_keys(engine) -> None:
    with engine.begin() as connection:
        connection.exec_driver_sql("PRAGMA foreign_keys=ON")


@pytest.fixture
def db_session():
    engine = make_engine("sqlite+pysqlite:///:memory:")
    _enable_sqlite_foreign_keys(engine)
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)()

    try:
        yield session
    finally:
        session.close()
        engine.dispose()


class StubIntentParserAdapter:
    def __init__(self, structured_output: IntentParserStructuredOutput) -> None:
        self.model_id = "gemini-3.1-flash-lite"
        self._structured_output = structured_output
        self.invocations = []

    def parse(self, invocation):
        from app.models import IntentParserInvocationResult

        self.invocations.append(invocation)
        return IntentParserInvocationResult(
            invocation=invocation,
            structured_output=self._structured_output,
            raw_response={"mock": "response"},
        )

    def close(self) -> None:
        return None


class RaisingIntentParserAdapter:
    model_id = "gemini-3.1-flash-lite"

    def parse(self, invocation):
        raise IntentParserTransportError("network timeout")

    def close(self) -> None:
        return None


def test_intent_parser_service_handles_happy_path_updates_and_audits_events(db_session) -> None:
    session_id = _create_beats_session(db_session)
    adapter = StubIntentParserAdapter(
        IntentParserStructuredOutput.model_validate(
            {
                "schema_version": 1,
                "status": "parsed",
                "needs_clarification": False,
                "assistant_response": (
                    "I can make the beat sheet moodier and shorten the planned runtime."
                ),
                "proposed_actions": {
                    "schema_version": 1,
                    "actions": [
                        {
                            "action_type": "refine_beat_sheet",
                            "target_stage": "beats",
                            "confidence": 0.88,
                            "rationale": "The user asked for a more mysterious story shape.",
                            "requires_confirmation": True,
                            "extracted_values": {
                                "instructions": (
                                    "Make the midpoint and mystery beats feel "
                                    "a little more mysterious."
                                ),
                                "bedtime_goal": (
                                    "Keep the tension gentle and resolve it quickly."
                                ),
                            },
                        },
                        {
                            "action_type": "update_story_setup",
                            "target_stage": "story_setup",
                            "confidence": 0.84,
                            "rationale": "The user asked for a shorter story.",
                            "requires_confirmation": False,
                            "extracted_values": {
                                "target_runtime_minutes": 8,
                                "guidance_notes": "Aim for a slightly shorter read-aloud.",
                            },
                        },
                    ],
                },
            }
        )
    )

    service = SessionIntentParserService(db_session, adapter)
    result = service.parse_user_message(
        session_id,
        message="make it a little more mysterious and shorter",
    )

    assert result.status == IntentParserStatus.PARSED
    assert [action.action_type for action in result.proposed_actions.actions] == [
        ChatToUIActionType.REFINE_BEAT_SHEET,
        ChatToUIActionType.UPDATE_STORY_SETUP,
    ]
    assert result.policy_evaluation is not None
    assert [item.decision for item in result.policy_evaluation.evaluated_actions] == [
        SessionActionDecision.REJECTED,
        SessionActionDecision.REJECTED,
    ]
    assert adapter.invocations
    assert '"current_stage": "beats"' in adapter.invocations[0].rendered_prompt
    assert "Selected tone: Hushed Wonder" in adapter.invocations[0].rendered_prompt

    history = SessionEventLogService(db_session).list_session_history(session_id)

    assert history.events[-3].event_type == SessionEventType.CHAT_MESSAGE_RECORDED
    assert history.events[-2].event_type == SessionEventType.CHAT_INTENT_PARSED
    assert history.events[-2].payload is not None
    assert history.events[-2].payload.result.status == IntentParserStatus.PARSED
    assert history.events[-2].payload.result.proposed_actions.actions[1].action_type == (
        ChatToUIActionType.UPDATE_STORY_SETUP
    )
    assert history.events[-1].event_type == SessionEventType.CHAT_MESSAGE_RECORDED
    assert history.events[-1].payload is not None
    assert history.events[-1].payload.message_role == "assistant"


def test_intent_parser_service_requests_clarification_for_vague_message(db_session) -> None:
    session_id = _create_beats_session(db_session)
    adapter = StubIntentParserAdapter(
        IntentParserStructuredOutput.model_validate(
            {
                "schema_version": 1,
                "status": "needs_clarification",
                "needs_clarification": True,
                "assistant_response": "Do you want the tone, beats, or runtime to change?",
                "clarification_reason": (
                    "The request does not say which part of the session to adjust."
                ),
                "proposed_actions": {
                    "schema_version": 1,
                    "actions": [],
                },
            }
        )
    )

    result = SessionIntentParserService(db_session, adapter).parse_user_message(
        session_id,
        message="make it better",
    )

    assert result.status == IntentParserStatus.NEEDS_CLARIFICATION
    assert result.needs_clarification is True
    assert result.proposed_actions.actions == []
    assert "tone, beats, or runtime" in result.assistant_response


def test_intent_parser_service_falls_back_gracefully_when_adapter_fails(db_session) -> None:
    session_id = _create_beats_session(db_session)
    result = SessionIntentParserService(
        db_session,
        RaisingIntentParserAdapter(),
    ).parse_user_message(
        session_id, message="make it a little more mysterious and shorter"
    )

    assert result.status == IntentParserStatus.FAILED
    assert result.proposed_actions.actions == []
    assert "structured story-studio actions" in result.assistant_response

    history = SessionEventLogService(db_session).list_session_history(session_id)
    assert history.events[-2].event_type == SessionEventType.CHAT_INTENT_PARSED
    assert history.events[-2].payload is not None
    assert history.events[-2].payload.raw_response is None
    assert history.events[-2].payload.result.status == IntentParserStatus.FAILED


def test_intent_parser_service_uses_updated_ui_context_in_prompt_summary(db_session) -> None:
    session_id = _create_beats_session(db_session)
    session_service = SessionService(db_session)
    session_service.apply_context_update(
        session_id,
        payload=SessionContextUpdateRequest.model_validate({
            "target_kind": "stage_note",
            "stage": "beats",
            "control_id": "stage-note-editor",
            "origin": "workspace",
            "values": {
                "detail": "Make the midpoint gentler and add one calmer beat before the finale.",
            },
        }),
    )
    adapter = StubIntentParserAdapter(
        IntentParserStructuredOutput.model_validate(
            {
                "schema_version": 1,
                "status": "needs_clarification",
                "needs_clarification": True,
                "assistant_response": "Do you want me to adjust the beat sheet or story setup?",
                "clarification_reason": "Need the target workflow stage.",
                "proposed_actions": {
                    "schema_version": 1,
                    "actions": [],
                },
            }
        )
    )

    SessionIntentParserService(db_session, adapter).parse_user_message(
        session_id,
        message="make it even softer",
    )

    assert adapter.invocations
    assert "Current beat sheet detail: Make the midpoint gentler" in (
        adapter.invocations[0].rendered_prompt
    )


def test_intent_parser_service_includes_latest_character_options_in_prompt_summary(
    db_session,
) -> None:
    session_id = _create_beats_session(db_session)
    adapter = StubIntentParserAdapter(
        IntentParserStructuredOutput.model_validate(
            {
                "schema_version": 1,
                "status": "needs_clarification",
                "needs_clarification": True,
                "assistant_response": "Which saved character sheet should I refine?",
                "clarification_reason": "Need the specific character sheet target.",
                "proposed_actions": {
                    "schema_version": 1,
                    "actions": [],
                },
            }
        )
    )

    SessionIntentParserService(db_session, adapter).parse_user_message(
        session_id,
        message="Refine the softer character sheet and make her voice warmer.",
    )

    assert adapter.invocations
    assert "Latest character options:" in adapter.invocations[0].rendered_prompt
    assert "Rev 1: Harbor Listener Cast" in adapter.invocations[0].rendered_prompt
    assert "Rev 2: Lantern Keeper Cast" in adapter.invocations[0].rendered_prompt


def _create_beats_session(db_session) -> str:
    genre = Genre(
        slug="quest-fantasy",
        label="Quest Fantasy",
        description="A gentle adventure with emotional repair.",
    )
    tone = ToneProfile(
        genre=genre,
        slug="hushed-wonder",
        label="Hushed Wonder",
        description="Quiet, luminous, and bedtime-safe.",
    )
    db_session.add_all([genre, tone])
    db_session.flush()

    session_service = SessionService(db_session)
    snapshot = session_service.create_session(working_title="Moonlit Harbor")
    story_session = db_session.get(StorySession, snapshot.id)
    assert story_session is not None
    story_session.selected_genre = genre
    story_session.selected_tone_profile = tone
    db_session.flush()

    for stage in (
        WorkflowStage.GENRE,
        WorkflowStage.TONE,
        WorkflowStage.BRIEF,
        WorkflowStage.PITCHES,
        WorkflowStage.CHARACTERS,
    ):
        session_service.update_stage_state(
            snapshot.id,
            stage=stage,
            status=WorkflowStageState.COMPLETED,
        )

    session_service.update_stage_state(
        snapshot.id,
        stage=WorkflowStage.BEATS,
        status=WorkflowStageState.IN_PROGRESS,
        detail="Refining the midpoint tension.",
    )
    db_session.add(
        StoryBrief(
            session_id=snapshot.id,
            revision_number=1,
            raw_brief="A harbor fox follows a moonlit clue across the docks.",
            normalized_summary="A sleepy harbor mystery that resolves gently before bedtime.",
            planning_notes="Keep every surprise reassuring.",
            is_active=True,
            accepted_at=datetime.now(timezone.utc),
        )
    )
    db_session.flush()
    db_session.add(
        Pitch(
            session_id=snapshot.id,
            generation_key="pitch-batch-1",
            pitch_index=1,
            title="Lanterns Over Moon Harbor",
            logline="A harbor child follows a moonlit clue before bedtime.",
            is_selected=True,
            accepted_at=datetime.now(timezone.utc),
        )
    )
    db_session.flush()
    db_session.add_all(
        [
            CharacterSheet(
                session_id=snapshot.id,
                pitch_id=None,
                revision_number=1,
                title="Harbor Listener Cast",
                protagonist_name="Mira",
                summary="A quieter harbor cast with a listening-first lead.",
                is_selected=False,
                character_data={
                    "batch_metadata": {
                        "generation_key": "character-batch-1",
                        "generation_kind": "generated",
                        "candidate_index": 1,
                    }
                },
            ),
            CharacterSheet(
                session_id=snapshot.id,
                pitch_id=None,
                revision_number=2,
                title="Lantern Keeper Cast",
                protagonist_name="Pip",
                summary="A steadier harbor cast with a visible comfort ritual.",
                is_selected=True,
                accepted_at=datetime.now(timezone.utc),
                character_data={
                    "batch_metadata": {
                        "generation_key": "character-batch-1",
                        "generation_kind": "generated",
                        "candidate_index": 2,
                    },
                    "refinement": {
                        "selection_rationale": "Refined from Harbor Listener Cast with a calmer lead voice.",
                        "change_summary": "Keep the same harbor arc but make the comfort ritual clearer.",
                        "change_impact": "minor",
                    },
                },
            ),
        ]
    )
    db_session.commit()
    return snapshot.id

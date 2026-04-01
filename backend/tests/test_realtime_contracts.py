from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

import pytest
from app.models import (
    ChatMessageRealtimeEvent,
    CompositionChunkRealtimeEvent,
    EventActorType,
    RealtimeDeliveryMode,
    SessionRealtimeEvent,
    WorkflowStage,
    WorkflowStageChangedRealtimeEvent,
    build_session_channel_name,
    get_realtime_contract_schema_bundle,
)
from pydantic import TypeAdapter, ValidationError


def test_build_session_channel_name_uses_the_session_scope() -> None:
    assert build_session_channel_name("session-123") == "session:session-123"

    with pytest.raises(ValueError, match="session_id must not be empty"):
        build_session_channel_name("   ")


def test_realtime_event_contract_supports_durable_and_ephemeral_events() -> None:
    durable_event = TypeAdapter(SessionRealtimeEvent).validate_python(
        {
            "event_id": "rt-1",
            "type": "workflow.stage_changed",
            "session_id": "session-123",
            "channel": "session:session-123",
            "actor": {
                "actor_type": "user",
                "actor_id": "local-user",
            },
            "stage": "brief",
            "created_at": datetime(2026, 4, 1, 8, 15, tzinfo=UTC),
            "correlation_id": "mutation-9",
            "delivery": "replay",
            "sequence_number": 14,
            "event_log_entry_id": "event-log-14",
            "payload": {
                "previous_status": "draft",
                "status": "completed",
                "detail": "Accepted the normalized story brief.",
                "invalidated_stages": ["pitches", "characters"],
                "current_stage": "pitches",
                "resume_stage": "pitches",
                "furthest_completed_stage": "brief",
                "overall_status": "in_progress",
            },
        }
    )
    chunk_event = TypeAdapter(SessionRealtimeEvent).validate_python(
        {
            "event_id": "rt-2",
            "type": "composition.chunk",
            "session_id": "session-123",
            "channel": "session:session-123",
            "actor": {
                "actor_type": "system",
                "actor_id": "worker",
            },
            "created_at": datetime(2026, 4, 1, 8, 16, tzinfo=UTC),
            "payload": {
                "job_id": "composition-job-1",
                "segment_id": "segment-2",
                "segment_index": 2,
                "chunk_index": 3,
                "chunk_kind": "delta",
                "text": "Milo listened as the lantern boat hummed.",
                "cumulative_character_count": 144,
                "cumulative_word_count": 27,
            },
        }
    )

    assert isinstance(durable_event, WorkflowStageChangedRealtimeEvent)
    assert durable_event.delivery == RealtimeDeliveryMode.REPLAY
    assert durable_event.sequence_number == 14
    assert durable_event.payload.current_stage == WorkflowStage.PITCHES
    assert isinstance(chunk_event, CompositionChunkRealtimeEvent)
    assert chunk_event.stage == WorkflowStage.COMPOSITION
    assert chunk_event.sequence_number is None
    assert chunk_event.payload.text == "Milo listened as the lantern boat hummed."


def test_realtime_event_contract_rejects_invalid_chunk_payloads() -> None:
    with pytest.raises(ValidationError, match="delta chunks must include text"):
        TypeAdapter(SessionRealtimeEvent).validate_python(
            {
                "event_id": "rt-3",
                "type": "composition.chunk",
                "session_id": "session-123",
                "channel": "session:session-123",
                "actor": {
                    "actor_type": "system",
                    "actor_id": "worker",
                },
                "created_at": datetime(2026, 4, 1, 8, 17, tzinfo=UTC),
                "payload": {
                    "job_id": "composition-job-1",
                    "segment_id": "segment-3",
                    "segment_index": 3,
                    "chunk_index": 0,
                    "chunk_kind": "delta",
                },
            }
        )


def test_realtime_schema_bundle_matches_the_checked_in_schema_file() -> None:
    schema_path = (
        Path(__file__).resolve().parents[2] / "docs" / "realtime-events.schema.json"
    )

    assert json.loads(schema_path.read_text()) == get_realtime_contract_schema_bundle()


def test_realtime_contract_uses_event_actor_types_already_known_to_the_event_log() -> None:
    event = ChatMessageRealtimeEvent.model_validate(
        {
            "event_id": "rt-4",
            "type": "chat.message",
            "session_id": "session-123",
            "channel": "session:session-123",
            "actor": {
                "actor_type": "assistant",
                "actor_id": "story-planner",
            },
            "stage": "pitches",
            "created_at": datetime(2026, 4, 1, 8, 18, tzinfo=UTC),
            "sequence_number": 15,
            "event_log_entry_id": "event-log-15",
            "payload": {
                "message_id": "chat-15",
                "message_role": "assistant",
                "content": "Here are three gentler pitch options.",
                "content_format": "plain_text",
            },
        }
    )

    assert event.actor.actor_type == EventActorType.ASSISTANT

from __future__ import annotations

import pytest
from app.db import Base, EventActorType, StorySession, make_engine
from app.models import (
    AIOutputKind,
    ChatMessageRole,
    SelectionKind,
    SessionEventActor,
    UserEditTargetKind,
    WorkflowStage,
)
from app.services.event_log import SessionEventLogService
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


def test_event_log_service_records_supported_event_categories(db_session) -> None:
    story_session = StorySession(working_title="Durable Timeline")
    db_session.add(story_session)
    db_session.commit()

    event_log = SessionEventLogService(db_session)
    event_log.record_selection(
        story_session.id,
        selection_kind=SelectionKind.GENRE,
        stage=WorkflowStage.GENRE,
        selection_id="genre-1",
        slug="quest-fantasy",
        label="Quest Fantasy",
    )
    event_log.record_ai_output(
        story_session.id,
        output_kind=AIOutputKind.PITCH_BATCH,
        stage=WorkflowStage.PITCHES,
        generation_key="pitch-batch-1",
        candidate_count=3,
        model_id="gemini-3.1-pro",
        summary_text="Three bedtime-safe pitches.",
    )
    event_log.record_user_edit(
        story_session.id,
        target_kind=UserEditTargetKind.STORY_BRIEF,
        stage=WorkflowStage.BRIEF,
        target_id="brief-1",
        revision_number=2,
        changed_fields=("raw_brief", "planning_notes"),
        field_values={
            "raw_brief": "A calmer harbor mystery.",
            "planning_notes": "Keep the midpoint reassuring.",
        },
        summary_text="Updated story brief notes from the workspace.",
    )
    event_log.record_chat_message(
        story_session.id,
        message_role=ChatMessageRole.USER,
        content="Please make the midpoint gentler and shorter.",
        stage=WorkflowStage.BEATS,
    )
    event_log.record_ui_action(
        story_session.id,
        action="updated_target_runtime",
        stage=WorkflowStage.STORY_SETUP,
        control_id="runtime-minutes",
        value_summary="~12 minutes",
    )
    event_log.record_composition_progress(
        story_session.id,
        job_id="composition-job-1",
        status="in_progress",
        progress_percent=62.5,
        current_segment_index=3,
        total_segments=5,
        segment_id="segment-3",
    )
    event_log.record_audio_progress(
        story_session.id,
        job_id="audio-job-1",
        status="queued",
        progress_percent=25.0,
        current_segment_index=1,
        total_segments=4,
        segment_id="audio-segment-1",
        estimated_duration_seconds=720,
        voice_key="gemini-soft-1",
    )
    event_log.append_event(
        story_session.id,
        actor=SessionEventActor(
            actor_type=EventActorType.SERVICE,
            actor_id="timeline-api",
        ),
        event_type="timeline.custom_synced",
        summary="Synced session history for an API consumer.",
        payload={"source": "timeline-api"},
    )
    db_session.commit()

    history = event_log.list_session_history(story_session.id)

    assert history.latest_sequence_number == 8
    assert [event.sequence_number for event in history.events] == list(range(1, 9))
    assert history.events[0].event_type == "selection.recorded"
    assert history.events[0].payload is not None
    assert history.events[0].payload.selection_kind == SelectionKind.GENRE
    assert history.events[1].actor.actor_type == EventActorType.ASSISTANT
    assert history.events[1].payload is not None
    assert history.events[1].payload.output_kind == AIOutputKind.PITCH_BATCH
    assert history.events[2].payload is not None
    assert history.events[2].payload.changed_fields == ["raw_brief", "planning_notes"]
    assert history.events[2].payload.field_values == {
        "raw_brief": "A calmer harbor mystery.",
        "planning_notes": "Keep the midpoint reassuring.",
    }
    assert history.events[2].payload.summary_text == (
        "Updated story brief notes from the workspace."
    )
    assert history.events[3].payload is not None
    assert history.events[3].payload.message_role == ChatMessageRole.USER
    assert history.events[4].summary == "Recorded UI action: updated_target_runtime."
    assert history.events[5].stage == WorkflowStage.COMPOSITION
    assert history.events[5].payload is not None
    assert history.events[5].payload.progress_percent == 62.5
    assert history.events[6].stage == WorkflowStage.AUDIO
    assert history.events[6].payload is not None
    assert history.events[6].payload.voice_key == "gemini-soft-1"
    assert history.events[7].actor.actor_type == EventActorType.SERVICE
    assert history.events[7].payload == {
        "schema_version": 1,
        "source": "timeline-api",
    }


def test_event_log_service_supports_incremental_history_reads(db_session) -> None:
    story_session = StorySession(working_title="History Tail")
    db_session.add(story_session)
    db_session.commit()

    event_log = SessionEventLogService(db_session)
    event_log.record_session_created(
        story_session.id,
        working_title=story_session.working_title,
    )
    event_log.record_ui_action(
        story_session.id,
        action="opened_workspace",
        stage=WorkflowStage.GENRE,
    )
    event_log.record_chat_message(
        story_session.id,
        message_role=ChatMessageRole.ASSISTANT,
        content="I can help you choose a genre.",
        stage=WorkflowStage.GENRE,
    )
    db_session.commit()

    history = event_log.list_session_history(story_session.id, after_sequence_number=1)

    assert history.latest_sequence_number == 3
    assert [event.sequence_number for event in history.events] == [2, 3]

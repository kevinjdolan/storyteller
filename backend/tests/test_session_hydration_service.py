from __future__ import annotations

from datetime import datetime, timezone

import pytest
from app.db import (
    AssetKind,
    AssetStatus,
    Base,
    CompositionJob,
    CompositionJobKind,
    JobStatus,
    SessionAsset,
    make_engine,
)
from app.models import WorkflowStage, WorkflowStageState
from app.services.event_log import SessionEventLogService
from app.services.session_hydration import (
    SessionHydrationNotFoundError,
    SessionHydrationService,
)
from app.services.sessions import SessionService
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


def _complete_stage_prefix(
    session_service: SessionService,
    session_id: str,
    *,
    through: WorkflowStage,
):
    for stage in WorkflowStage:
        if stage == WorkflowStage.FINALIZE:
            break
        session_service.update_stage_state(
            session_id,
            stage=stage,
            status=WorkflowStageState.COMPLETED,
            detail=f"Accepted {stage.value}.",
        )
        if stage == through:
            break


def test_hydrate_session_replays_failed_composition_job_state(db_session) -> None:
    session_service = SessionService(db_session)
    snapshot = session_service.create_session(working_title="Hydration Failure")
    _complete_stage_prefix(
        session_service,
        snapshot.id,
        through=WorkflowStage.STORY_SETUP,
    )
    session_service.update_stage_state(
        snapshot.id,
        stage=WorkflowStage.COMPOSITION,
        status=WorkflowStageState.IN_PROGRESS,
        detail="Writing the second segment.",
    )

    composition_job = CompositionJob(
        session_id=snapshot.id,
        job_kind=CompositionJobKind.DRAFT,
        status=JobStatus.FAILED,
        progress_percent=42.0,
        current_segment_index=2,
        error_message="Gemini draft call timed out after the retry budget.",
        started_at=datetime.now(timezone.utc),
    )
    db_session.add(composition_job)
    db_session.flush()

    SessionEventLogService(db_session).record_composition_progress(
        snapshot.id,
        job_id=composition_job.id,
        status=JobStatus.FAILED,
        progress_percent=42.0,
        current_segment_index=2,
        total_segments=5,
    )
    db_session.commit()

    hydrated = SessionHydrationService(db_session).hydrate_session(snapshot.id)

    assert hydrated.snapshot.active_composition_job is None
    assert hydrated.snapshot.latest_composition_job is not None
    assert hydrated.snapshot.latest_composition_job.status == "failed"
    assert hydrated.snapshot.latest_composition_job.error_message == (
        "Gemini draft call timed out after the retry budget."
    )
    composition_stage = next(
        stage
        for stage in hydrated.snapshot.stage_states
        if stage.stage == WorkflowStage.COMPOSITION
    )
    assert composition_stage.status == WorkflowStageState.NEEDS_REGENERATION
    assert composition_stage.detail == "Gemini draft call timed out after the retry budget."
    assert hydrated.snapshot.resume_stage == WorkflowStage.COMPOSITION
    assert hydrated.snapshot.overall_status == WorkflowStageState.NEEDS_REGENERATION
    assert hydrated.hydration.strategy == "materialized_with_recent_replay"
    assert hydrated.hydration.replayed_event_count == 1
    assert "Composition job: failed at 42.0%" in (
        hydrated.snapshot.agent_context_summary or ""
    )


def test_hydrate_session_returns_completed_workspace_state(db_session) -> None:
    now = datetime.now(timezone.utc)
    session_service = SessionService(db_session)
    snapshot = session_service.create_session(working_title="Hydration Complete")

    for stage in WorkflowStage:
        session_service.update_stage_state(
            snapshot.id,
            stage=stage,
            status=WorkflowStageState.COMPLETED,
            detail=f"Accepted {stage.value}.",
        )

    story_asset = SessionAsset(
        session_id=snapshot.id,
        asset_kind=AssetKind.STORY_DOCX,
        status=AssetStatus.READY,
        storage_bucket="storyteller-exports",
        object_path="sessions/hydration-complete/story.docx",
        mime_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        ready_at=now,
    )
    audio_asset = SessionAsset(
        session_id=snapshot.id,
        asset_kind=AssetKind.FINAL_AUDIO,
        status=AssetStatus.READY,
        storage_bucket="storyteller-exports",
        object_path="sessions/hydration-complete/story.mp3",
        mime_type="audio/mpeg",
        ready_at=now,
    )
    db_session.add_all([story_asset, audio_asset])
    db_session.commit()

    hydrated = SessionHydrationService(db_session).hydrate_session(snapshot.id)

    assert hydrated.snapshot.overall_status == WorkflowStageState.COMPLETED
    assert hydrated.snapshot.resume_stage == WorkflowStage.FINALIZE
    assert hydrated.snapshot.latest_story_asset is not None
    assert hydrated.snapshot.latest_audio_asset is not None
    assert hydrated.snapshot.latest_story_asset.object_path.endswith("story.docx")
    assert hydrated.snapshot.latest_audio_asset.object_path.endswith("story.mp3")
    assert hydrated.hydration.strategy == "materialized_only"
    assert hydrated.hydration.replayed_event_count == 0


def test_hydrate_session_limits_recent_history_window(db_session) -> None:
    session_service = SessionService(db_session)
    snapshot = session_service.create_session(working_title="Hydration Window")

    session_service.record_ui_action(
        snapshot.id,
        action="navigate_to_stage",
        stage=WorkflowStage.TONE,
        control_id="stage-nav",
        value_summary="Tone",
    )
    session_service.record_ui_action(
        snapshot.id,
        action="navigate_to_stage",
        stage=WorkflowStage.BRIEF,
        control_id="stage-nav",
        value_summary="Brief",
    )

    hydrated = SessionHydrationService(db_session).hydrate_session(
        snapshot.id,
        history_limit=2,
    )

    assert [event.sequence_number for event in hydrated.recent_history.events] == [2, 3]
    assert hydrated.recent_history.latest_sequence_number == 3
    assert hydrated.hydration.history_event_count == 2
    assert hydrated.hydration.history_window_truncated is True


def test_hydrate_session_raises_for_missing_session(db_session) -> None:
    with pytest.raises(SessionHydrationNotFoundError):
        SessionHydrationService(db_session).hydrate_session("missing-session")

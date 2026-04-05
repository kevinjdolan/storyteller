from __future__ import annotations

from datetime import datetime, timezone

import pytest
from app.db import (
    AssetKind,
    AssetStatus,
    AudioJob,
    Base,
    BeatSheet,
    CompositionJob,
    CompositionJobKind,
    CompositionSegment,
    CompositionSegmentAcceptanceState,
    ContinuityBible,
    JobStatus,
    NarrationPauseHint,
    NarrationSegment,
    NarrationSourceBoundaryKind,
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


class FakeDraftSnapshotStorage:
    def __init__(self, payloads: dict[tuple[str, str], str]) -> None:
        self._payloads = payloads

    def download_text(self, location) -> str:
        return self._payloads[(location.bucket, location.key)]


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
    assert "Composition job: failed at 42.0%" in (hydrated.snapshot.agent_context_summary or "")


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
        asset_kind=AssetKind.STORY_TEXT,
        status=AssetStatus.READY,
        storage_bucket="storyteller-exports",
        object_path="sessions/hydration-complete/story.md",
        mime_type="text/markdown",
        ready_at=now,
    )
    story_export_asset = SessionAsset(
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
    db_session.add_all([story_asset, story_export_asset, audio_asset])
    db_session.commit()

    hydrated = SessionHydrationService(db_session).hydrate_session(snapshot.id)

    assert hydrated.snapshot.overall_status == WorkflowStageState.COMPLETED
    assert hydrated.snapshot.resume_stage == WorkflowStage.FINALIZE
    assert hydrated.snapshot.latest_story_asset is not None
    assert hydrated.snapshot.latest_story_export_asset is not None
    assert hydrated.snapshot.latest_audio_asset is not None
    assert hydrated.snapshot.latest_story_asset.object_path.endswith("story.md")
    assert hydrated.snapshot.latest_story_export_asset.object_path.endswith("story.docx")
    assert hydrated.snapshot.latest_audio_asset.object_path.endswith("story.mp3")
    assert hydrated.snapshot.latest_story_asset.access is not None
    assert hydrated.snapshot.latest_story_asset.access.download_path.endswith(
        f"/api/v1/sessions/{snapshot.id}/assets/{story_asset.id}/content?disposition=attachment"
    )
    assert hydrated.snapshot.latest_story_export_asset.access is not None
    assert hydrated.snapshot.latest_story_export_asset.access.download_path.endswith(
        f"/api/v1/sessions/{snapshot.id}/assets/{story_export_asset.id}/content?disposition=attachment"
    )
    assert hydrated.snapshot.latest_audio_asset.access is not None
    assert hydrated.snapshot.latest_audio_asset.access.stream_path.endswith(
        f"/api/v1/sessions/{snapshot.id}/assets/{audio_asset.id}/content?disposition=inline"
    )
    assert hydrated.hydration.strategy == "materialized_only"
    assert hydrated.hydration.replayed_event_count == 0


def test_hydrate_session_includes_selected_continuity_bible(db_session) -> None:
    session_service = SessionService(db_session)
    snapshot = session_service.create_session(working_title="Hydration Continuity")

    continuity_bible = ContinuityBible(
        session_id=snapshot.id,
        revision_number=2,
        source_stage=WorkflowStage.STORY_SETUP,
        source_summary="Accepted story setup.",
        summary_text="Mira anchors the harbor story and still needs to resolve the drifting bell.",
        summary_data={
            "schema_version": 1,
            "facts": [
                {
                    "key": "thread:drifting-bell:1",
                    "category": "unresolved_thread",
                    "title": "Drifting bell",
                    "detail": "The bell still needs a gentle explanation before the finale.",
                    "source_stage": "beats",
                    "source_label": "Revision 2",
                }
            ],
        },
        is_selected=True,
    )
    db_session.add(continuity_bible)
    db_session.commit()

    hydrated = SessionHydrationService(db_session).hydrate_session(snapshot.id)

    assert hydrated.snapshot.continuity_bible is not None
    assert hydrated.snapshot.continuity_bible.revision_number == 2
    assert hydrated.snapshot.continuity_bible.summary_text.startswith("Mira anchors")
    assert hydrated.snapshot.continuity_bible.facts[0].title == "Drifting bell"
    assert "Continuity: Mira anchors the harbor story" in (
        hydrated.snapshot.agent_context_summary or ""
    )


def test_hydrate_session_includes_audio_segments_with_preview_assets(db_session) -> None:
    session_service = SessionService(db_session)
    snapshot = session_service.create_session(working_title="Hydration Audio Segments")

    audio_job = AudioJob(
        session_id=snapshot.id,
        status=JobStatus.IN_PROGRESS,
        voice_key="moonbeam",
        playback_speed=0.95,
        include_background_music=False,
        music_profile="lullaby_piano",
        estimated_duration_seconds=780,
        current_segment_index=2,
        config_json={
            "total_segments": 2,
            "completed_segments": 1,
            "progress_percent": 54.0,
            "current_step": "Rendering narration segment 2 of 2.",
            "current_step_index": 2,
            "total_steps": 4,
            "latest_asset_kind": AssetKind.AUDIO_SEGMENT.value,
        },
    )
    db_session.add(audio_job)
    db_session.flush()

    db_session.add_all(
        [
            NarrationSegment(
                session_id=snapshot.id,
                audio_job_id=audio_job.id,
                segment_index=1,
                status=JobStatus.COMPLETED,
                source_boundary_kind=NarrationSourceBoundaryKind.CHAPTER,
                source_outline_card_title="Lantern launch",
                text_content=(
                    "Mira set the first lantern on the water and waited for the harbor to answer."
                ),
                word_count=14,
                text_start_offset=0,
                text_end_offset=76,
                pause_after_seconds=3,
                pause_hint=NarrationPauseHint.CHAPTER_BREAK,
                completed_at=datetime.now(timezone.utc),
                metadata_json={"split_reason": "paragraph_boundary"},
            ),
            NarrationSegment(
                session_id=snapshot.id,
                audio_job_id=audio_job.id,
                segment_index=2,
                status=JobStatus.QUEUED,
                source_boundary_kind=NarrationSourceBoundaryKind.CHAPTER,
                source_outline_card_title="Silver bell crossing",
                text_content=("Otis stayed close while the silver bell called from the cove."),
                word_count=11,
                text_start_offset=78,
                text_end_offset=140,
                pause_after_seconds=0,
                pause_hint=NarrationPauseHint.NONE,
                metadata_json={"split_reason": "sentence_boundary"},
            ),
        ]
    )
    db_session.flush()

    db_session.add(
        SessionAsset(
            session_id=snapshot.id,
            audio_job_id=audio_job.id,
            asset_kind=AssetKind.AUDIO_SEGMENT,
            status=AssetStatus.READY,
            storage_bucket="storyteller-audio",
            object_path=(f"sessions/{snapshot.id}/audio/jobs/{audio_job.id}/segments/0001.wav"),
            mime_type="audio/wav",
            segment_index=1,
            ready_at=datetime.now(timezone.utc),
        )
    )
    db_session.commit()

    hydrated = SessionHydrationService(db_session).hydrate_session(snapshot.id)

    assert len(hydrated.snapshot.audio_segments) == 2
    assert hydrated.snapshot.audio_segments[0].source_outline_card_title == "Lantern launch"
    assert hydrated.snapshot.audio_segments[0].status == JobStatus.COMPLETED.value
    assert hydrated.snapshot.audio_segments[0].preview_asset is not None
    assert hydrated.snapshot.audio_segments[0].preview_asset.access is not None
    assert hydrated.snapshot.audio_segments[0].preview_asset.access.stream_path.endswith(
        f"/api/v1/sessions/{snapshot.id}/assets/"
        f"{hydrated.snapshot.audio_segments[0].preview_asset.id}/content?disposition=inline"
    )
    assert hydrated.snapshot.audio_segments[1].split_reason == "sentence_boundary"
    assert hydrated.snapshot.audio_segments[1].preview_asset is None
    assert hydrated.snapshot.active_audio_job is not None
    assert hydrated.snapshot.active_audio_job.current_segment_index == 2


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


def test_hydrate_session_recovers_draft_text_from_snapshot_asset(db_session) -> None:
    session_service = SessionService(db_session)
    snapshot = session_service.create_session(working_title="Hydration Draft Snapshot")
    _complete_stage_prefix(
        session_service,
        snapshot.id,
        through=WorkflowStage.STORY_SETUP,
    )
    session_service.update_stage_state(
        snapshot.id,
        stage=WorkflowStage.COMPOSITION,
        status=WorkflowStageState.IN_PROGRESS,
        detail="Writing paused after an autosave checkpoint.",
    )

    composition_job = CompositionJob(
        session_id=snapshot.id,
        job_kind=CompositionJobKind.DRAFT,
        status=JobStatus.PAUSED,
        progress_percent=38.0,
        current_segment_index=2,
        metadata_json={
            "total_segments": 3,
            "start_segment_index": 1,
            "status_message": (
                "Gemini hit a temporary rate limit while drafting segment 2 of 3. "
                "Retrying in 2s (attempt 2 of 3)."
            ),
        },
    )
    db_session.add(composition_job)
    db_session.flush()

    draft_asset = SessionAsset(
        session_id=snapshot.id,
        composition_job_id=composition_job.id,
        asset_kind=AssetKind.DRAFT_TEXT_SNAPSHOT,
        status=AssetStatus.READY,
        storage_bucket="storyteller-sessions",
        object_path="sessions/hydration-draft/composition/drafts/latest-stable.md",
        mime_type="text/markdown",
        segment_index=2,
        ready_at=datetime.now(timezone.utc),
    )
    db_session.add(draft_asset)
    db_session.commit()

    storage = FakeDraftSnapshotStorage(
        {
            (
                draft_asset.storage_bucket,
                draft_asset.object_path,
            ): (
                "Draft segment 1 settles the harbor.\n\n"
                "Draft segment 2 keeps the bell audible while the cove stays calm."
            )
        }
    )

    hydrated = SessionHydrationService(
        db_session,
        object_storage=storage,  # type: ignore[arg-type]
    ).hydrate_session(snapshot.id)

    assert hydrated.snapshot.active_composition_job is not None
    assert hydrated.snapshot.latest_composition_job is not None
    assert hydrated.snapshot.active_composition_job.status_message == (
        "Gemini hit a temporary rate limit while drafting segment 2 of 3. "
        "Retrying in 2s (attempt 2 of 3)."
    )
    assert (
        hydrated.snapshot.active_composition_job.accepted_story_so_far
        == "Draft segment 1 settles the harbor.\n\n"
        "Draft segment 2 keeps the bell audible while the cove stays calm."
    )
    assert (
        hydrated.snapshot.active_composition_job.latest_partial_output
        == hydrated.snapshot.active_composition_job.accepted_story_so_far
    )
    assert (
        hydrated.snapshot.latest_composition_job.accepted_story_so_far
        == hydrated.snapshot.active_composition_job.accepted_story_so_far
    )
    assert (
        hydrated.snapshot.latest_composition_job.status_message
        == hydrated.snapshot.active_composition_job.status_message
    )


def test_hydrate_session_windows_large_revision_collections(db_session) -> None:
    session_service = SessionService(db_session)
    snapshot = session_service.create_session(working_title="Hydration Windows")

    db_session.add_all(
        [
            BeatSheet(
                session_id=snapshot.id,
                revision_number=revision_number,
                summary=f"Beat sheet revision {revision_number}",
                beats={"opening_image": f"Revision {revision_number} opens softly."},
                is_selected=revision_number == 1,
                accepted_at=(datetime.now(timezone.utc) if revision_number == 1 else None),
            )
            for revision_number in range(1, 7)
        ]
    )

    composition_job = CompositionJob(
        session_id=snapshot.id,
        job_kind=CompositionJobKind.REWRITE,
        status=JobStatus.PAUSED,
        progress_percent=61.0,
        current_segment_index=1,
    )
    db_session.add(composition_job)
    db_session.flush()

    segment_versions: list[CompositionSegment] = []
    for revision_number in range(1, 8):
        acceptance_state = (
            CompositionSegmentAcceptanceState.ACCEPTED
            if revision_number == 1
            else CompositionSegmentAcceptanceState.PENDING
            if revision_number == 7
            else CompositionSegmentAcceptanceState.REJECTED
        )
        segment_versions.append(
            CompositionSegment(
                session_id=snapshot.id,
                composition_job_id=composition_job.id,
                segment_index=1,
                revision_number=revision_number,
                status=JobStatus.COMPLETED,
                acceptance_state=acceptance_state,
                accepted_text=f"Revision {revision_number} text",
                text_content=f"Revision {revision_number} text",
                word_count=3,
                payload={
                    "outline_card_title": "Harbor crossing",
                    "outline_card_summary": "Mira keeps the harbor calm.",
                },
                completed_at=datetime.now(timezone.utc),
            )
        )
    db_session.add_all(segment_versions)
    db_session.commit()

    hydrated = SessionHydrationService(db_session).hydrate_session(snapshot.id)

    assert hydrated.snapshot.selected_beat_sheet is not None
    assert hydrated.snapshot.selected_beat_sheet.revision_number == 1
    assert [revision.revision_number for revision in hydrated.snapshot.beat_sheet_revisions] == [
        6,
        5,
        4,
        3,
    ]
    assert hydrated.snapshot.collection_windows.beat_sheet_revisions.total_count == 6
    assert hydrated.snapshot.collection_windows.beat_sheet_revisions.included_count == 4
    assert hydrated.snapshot.collection_windows.beat_sheet_revisions.has_more is True

    segment = hydrated.snapshot.composition_segments[0]
    assert segment.version_count == 7
    assert segment.included_version_count == 5
    assert segment.hidden_version_count == 2
    assert [version.revision_number for version in segment.versions] == [7, 6, 5, 4, 1]
    assert hydrated.snapshot.collection_windows.composition_segment_versions.total_count == 7
    assert hydrated.snapshot.collection_windows.composition_segment_versions.included_count == 5
    assert hydrated.snapshot.collection_windows.composition_segment_versions.has_more is True


def test_hydrate_session_raises_for_missing_session(db_session) -> None:
    with pytest.raises(SessionHydrationNotFoundError):
        SessionHydrationService(db_session).hydrate_session("missing-session")

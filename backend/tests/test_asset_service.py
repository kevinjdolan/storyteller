from __future__ import annotations

from datetime import datetime, timezone

import pytest
from app.db import (
    AssetKind,
    AssetStatus,
    AudioJob,
    Base,
    CompositionJob,
    CompositionJobKind,
    CompositionSegment,
    JobStatus,
    SessionAsset,
    StorySession,
    make_engine,
)
from app.models import WorkflowStage, WorkflowStageState
from app.services import (
    AssetOwnershipError,
    AssetSessionNotFoundError,
    SessionAssetService,
)
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


def test_asset_service_creates_segmented_assets_and_lists_downloadables(db_session) -> None:
    story_session = StorySession(
        working_title="Segmented Asset Session",
        current_stage=WorkflowStage.COMPOSITION,
        resume_stage=WorkflowStage.COMPOSITION,
        overall_status=WorkflowStageState.IN_PROGRESS,
    )
    db_session.add(story_session)
    db_session.flush()

    composition_job = CompositionJob(
        session_id=story_session.id,
        job_kind=CompositionJobKind.DRAFT,
        status=JobStatus.IN_PROGRESS,
    )
    db_session.add(composition_job)
    db_session.flush()

    composition_segment = CompositionSegment(
        session_id=story_session.id,
        composition_job_id=composition_job.id,
        segment_index=0,
        revision_number=1,
        status=JobStatus.COMPLETED,
        text_content="A calm opening scene.",
    )
    db_session.add(composition_segment)
    db_session.flush()

    audio_job = AudioJob(
        session_id=story_session.id,
        source_composition_job_id=composition_job.id,
        status=JobStatus.IN_PROGRESS,
        voice_key="gemini-soft-1",
    )
    db_session.add(audio_job)
    db_session.commit()

    service = SessionAssetService(db_session)

    draft_snapshot = service.save_asset_record(
        session_id=story_session.id,
        asset_kind=AssetKind.DRAFT_TEXT_SNAPSHOT,
        storage_bucket="storyteller-sessions",
        object_path="sessions/story-1/drafts/draft-001.md",
        mime_type="text/markdown",
        status=AssetStatus.IN_PROGRESS,
        composition_job_id=composition_job.id,
        metadata_json={"checkpoint": 1},
    )
    text_segment = service.save_asset_record(
        session_id=story_session.id,
        asset_kind=AssetKind.COMPOSITION_SEGMENT,
        storage_bucket="storyteller-sessions",
        object_path="sessions/story-1/composition/segment-0001.txt",
        mime_type="text/plain",
        composition_job_id=composition_job.id,
        composition_segment_id=composition_segment.id,
    )
    audio_segment = service.save_asset_record(
        session_id=story_session.id,
        asset_kind=AssetKind.AUDIO_SEGMENT,
        storage_bucket="storyteller-audio",
        object_path="sessions/story-1/audio/segment-0001.mp3",
        mime_type="audio/mpeg",
        status=AssetStatus.IN_PROGRESS,
        audio_job_id=audio_job.id,
        segment_index=0,
    )
    story_docx = service.save_asset_record(
        session_id=story_session.id,
        asset_kind=AssetKind.STORY_DOCX,
        storage_bucket="storyteller-exports",
        object_path="sessions/story-1/exports/story.docx",
        mime_type=("application/vnd.openxmlformats-officedocument.wordprocessingml.document"),
        status=AssetStatus.READY,
    )
    final_audio = service.save_asset_record(
        session_id=story_session.id,
        asset_kind=AssetKind.FINAL_AUDIO,
        storage_bucket="storyteller-exports",
        object_path="sessions/story-1/exports/final-audio.mp3",
        mime_type="audio/mpeg",
        status=AssetStatus.READY,
        audio_job_id=audio_job.id,
    )

    all_assets = service.list_session_assets(story_session.id)
    downloadable_assets = service.list_downloadable_assets(story_session.id)

    assert draft_snapshot.status == AssetStatus.IN_PROGRESS
    assert text_segment.segment_index == 0
    assert audio_segment.segment_index == 0
    assert story_docx.ready_at is not None
    assert final_audio.ready_at is not None
    assert [asset.asset_kind for asset in all_assets] == [
        AssetKind.FINAL_AUDIO,
        AssetKind.STORY_DOCX,
        AssetKind.AUDIO_SEGMENT,
        AssetKind.COMPOSITION_SEGMENT,
        AssetKind.DRAFT_TEXT_SNAPSHOT,
    ]
    assert [asset.asset_kind for asset in downloadable_assets] == [
        AssetKind.FINAL_AUDIO,
        AssetKind.STORY_DOCX,
    ]


def test_asset_service_marks_assets_ready_and_failed(db_session) -> None:
    story_session = StorySession(working_title="Status Transitions")
    db_session.add(story_session)
    db_session.commit()

    service = SessionAssetService(db_session)
    created_asset = service.save_asset_record(
        session_id=story_session.id,
        asset_kind=AssetKind.STORY_TEXT,
        storage_bucket="storyteller-exports",
        object_path="sessions/story-2/exports/story.md",
        mime_type="text/markdown",
    )
    failed_asset = service.save_asset_record(
        session_id=story_session.id,
        asset_kind=AssetKind.STORY_DOCX,
        storage_bucket="storyteller-exports",
        object_path="sessions/story-2/exports/story.docx",
        mime_type=("application/vnd.openxmlformats-officedocument.wordprocessingml.document"),
    )

    ready_timestamp = datetime.now(timezone.utc)
    ready_asset = service.mark_asset_ready(
        created_asset.id,
        byte_size=4096,
        checksum_sha256="abc123",
        metadata_json={"variant": "reader"},
        ready_at=ready_timestamp,
    )
    failed_view = service.mark_asset_failed(
        failed_asset.id,
        error_message="docx assembly timed out",
        metadata_json={"attempt": 2},
    )

    stored_ready = db_session.get(SessionAsset, created_asset.id)
    stored_failed = db_session.get(SessionAsset, failed_asset.id)

    assert ready_asset.status == AssetStatus.READY
    assert ready_asset.byte_size == 4096
    assert ready_asset.checksum_sha256 == "abc123"
    assert ready_asset.ready_at == ready_timestamp
    assert failed_view.status == AssetStatus.FAILED
    assert failed_view.error_message == "docx assembly timed out"
    assert failed_view.failed_at is not None
    assert stored_ready is not None and stored_ready.status == AssetStatus.READY
    assert stored_failed is not None and stored_failed.status == AssetStatus.FAILED
    assert stored_failed.error_message == "docx assembly timed out"


def test_asset_service_upserts_existing_asset_records_by_storage_location(db_session) -> None:
    story_session = StorySession(working_title="Rolling Draft Snapshot")
    db_session.add(story_session)
    db_session.flush()

    composition_job = CompositionJob(
        session_id=story_session.id,
        job_kind=CompositionJobKind.DRAFT,
        status=JobStatus.IN_PROGRESS,
    )
    db_session.add(composition_job)
    db_session.flush()

    service = SessionAssetService(db_session)
    created_asset = service.upsert_asset_record(
        session_id=story_session.id,
        asset_kind=AssetKind.DRAFT_TEXT_SNAPSHOT,
        storage_bucket="storyteller-sessions",
        object_path="sessions/story-rolling/composition/drafts/latest-stable.md",
        mime_type="text/markdown",
        status=AssetStatus.READY,
        composition_job_id=composition_job.id,
        byte_size=512,
        metadata_json={"checkpoint_reason": "autosave", "word_count": 80},
    )
    updated_asset = service.upsert_asset_record(
        session_id=story_session.id,
        asset_kind=AssetKind.DRAFT_TEXT_SNAPSHOT,
        storage_bucket="storyteller-sessions",
        object_path="sessions/story-rolling/composition/drafts/latest-stable.md",
        mime_type="text/markdown",
        status=AssetStatus.READY,
        composition_job_id=composition_job.id,
        byte_size=768,
        metadata_json={"checkpoint_reason": "segment_complete", "word_count": 120},
    )

    stored_assets = (
        db_session.query(SessionAsset)
        .filter(SessionAsset.session_id == story_session.id)
        .order_by(SessionAsset.created_at.asc())
        .all()
    )

    assert created_asset.id == updated_asset.id
    assert len(stored_assets) == 1
    assert stored_assets[0].byte_size == 768
    assert stored_assets[0].ready_at is not None
    assert stored_assets[0].metadata_json == {
        "checkpoint_reason": "segment_complete",
        "word_count": 120,
    }


def test_asset_service_rejects_missing_sessions_and_cross_session_links(db_session) -> None:
    primary_session = StorySession(working_title="Primary")
    other_session = StorySession(working_title="Other")
    db_session.add_all([primary_session, other_session])
    db_session.flush()

    composition_job = CompositionJob(
        session_id=primary_session.id,
        job_kind=CompositionJobKind.DRAFT,
        status=JobStatus.IN_PROGRESS,
    )
    audio_job = AudioJob(
        session_id=primary_session.id,
        source_composition_job_id=composition_job.id,
        status=JobStatus.IN_PROGRESS,
    )
    db_session.add_all([composition_job, audio_job])
    db_session.commit()

    service = SessionAssetService(db_session)

    with pytest.raises(AssetSessionNotFoundError):
        service.list_session_assets("missing-session-id")

    with pytest.raises(AssetOwnershipError):
        service.save_asset_record(
            session_id=other_session.id,
            asset_kind=AssetKind.DRAFT_TEXT_SNAPSHOT,
            storage_bucket="storyteller-sessions",
            object_path="sessions/story-3/drafts/draft-001.md",
            mime_type="text/markdown",
            composition_job_id=composition_job.id,
        )

    with pytest.raises(AssetOwnershipError):
        service.save_asset_record(
            session_id=other_session.id,
            asset_kind=AssetKind.FINAL_AUDIO,
            storage_bucket="storyteller-exports",
            object_path="sessions/story-3/exports/final-audio.mp3",
            mime_type="audio/mpeg",
            audio_job_id=audio_job.id,
        )


def test_asset_service_supersedes_prior_final_audio_with_replacement_metadata(
    db_session,
) -> None:
    story_session = StorySession(working_title="Superseded Audio History")
    db_session.add(story_session)
    db_session.flush()

    first_job = AudioJob(
        session_id=story_session.id,
        status=JobStatus.COMPLETED,
        voice_key="moonbeam",
    )
    replacement_job = AudioJob(
        session_id=story_session.id,
        status=JobStatus.COMPLETED,
        voice_key="hearthside",
    )
    db_session.add_all([first_job, replacement_job])
    db_session.flush()

    service = SessionAssetService(db_session)
    first_asset = service.save_asset_record(
        session_id=story_session.id,
        asset_kind=AssetKind.FINAL_AUDIO,
        storage_bucket="storyteller-audio",
        object_path="sessions/story-4/audio/jobs/audio-job-1/final/story.wav",
        mime_type="audio/wav",
        status=AssetStatus.READY,
        audio_job_id=first_job.id,
        metadata_json={"duration_seconds": 101.2},
    )
    replacement_asset = service.save_asset_record(
        session_id=story_session.id,
        asset_kind=AssetKind.FINAL_AUDIO,
        storage_bucket="storyteller-audio",
        object_path="sessions/story-4/audio/jobs/audio-job-2/final/story.wav",
        mime_type="audio/wav",
        status=AssetStatus.READY,
        audio_job_id=replacement_job.id,
        metadata_json={
            "duration_seconds": 98.4,
            "supersedes_asset_ids": [first_asset.id],
        },
    )

    superseded_views = service.supersede_assets(
        story_session.id,
        asset_kinds=(AssetKind.FINAL_AUDIO,),
        exclude_asset_ids=(replacement_asset.id,),
        replacement_asset_id=replacement_asset.id,
        replacement_audio_job_id=replacement_job.id,
        reason="replaced_by_regenerated_audio",
    )

    stored_first_asset = db_session.get(SessionAsset, first_asset.id)
    stored_replacement_asset = db_session.get(SessionAsset, replacement_asset.id)

    assert len(superseded_views) == 1
    assert superseded_views[0].id == first_asset.id
    assert superseded_views[0].status == AssetStatus.SUPERSEDED
    assert superseded_views[0].audio_job_id == first_job.id
    assert superseded_views[0].duration_seconds == pytest.approx(101.2)
    assert superseded_views[0].details == {
        "duration_seconds": 101.2,
        "superseded_reason": "replaced_by_regenerated_audio",
        "superseded_by_asset_id": replacement_asset.id,
        "superseded_by_audio_job_id": replacement_job.id,
    }
    assert stored_first_asset is not None
    assert stored_first_asset.status == AssetStatus.SUPERSEDED
    assert stored_first_asset.superseded_at is not None
    assert stored_replacement_asset is not None
    assert stored_replacement_asset.status == AssetStatus.READY

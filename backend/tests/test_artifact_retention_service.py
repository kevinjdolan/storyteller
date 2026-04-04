from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest
from app.db import (
    AssetKind,
    AssetStatus,
    AudioJob,
    Base,
    CompositionJob,
    CompositionJobKind,
    CompositionSegment,
    CompositionSegmentAcceptanceState,
    JobStatus,
    SessionAsset,
    StorySession,
    make_engine,
)
from app.services.artifact_retention import ArtifactRetentionService
from app.settings import load_settings
from app.storage import ObjectNotFoundError
from sqlalchemy.orm import sessionmaker
from tests.support.in_memory_storage import InMemoryObjectStorage

FIXED_NOW = datetime(2026, 4, 4, 12, 0, tzinfo=timezone.utc)


def _build_test_settings():
    return load_settings(
        {
            "STORYTELLER_SECRETS_FILE": "",
            "STORYTELLER_DATABASE_URL": (
                "postgresql+psycopg://storyteller:storyteller@postgres:5432/storyteller"
            ),
            "STORYTELLER_GEMINI_API_KEY": "test-gemini-key",
            "STORYTELLER_GCS_ENDPOINT": "http://gcs:4443",
            "STORYTELLER_GCS_PROJECT_ID": "storyteller-local",
            "STORYTELLER_GCS_PUBLIC_URL": "http://localhost:8568",
            "STORYTELLER_GCS_SESSIONS_BUCKET_NAME": "storyteller-sessions",
            "STORYTELLER_GCS_AUDIO_BUCKET_NAME": "storyteller-audio",
            "STORYTELLER_GCS_EXPORTS_BUCKET_NAME": "storyteller-exports",
        }
    )


@pytest.fixture
def db_session():
    engine = make_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)()

    try:
        yield session
    finally:
        session.close()
        engine.dispose()


@pytest.fixture
def object_storage():
    return InMemoryObjectStorage(_build_test_settings())


def test_cleanup_plan_only_targets_expired_noncanonical_assets(db_session, object_storage) -> None:
    story_session = StorySession(working_title="Retention Plan")
    db_session.add(story_session)
    db_session.flush()

    current_composition_job = CompositionJob(
        session_id=story_session.id,
        job_kind=CompositionJobKind.DRAFT,
        status=JobStatus.COMPLETED,
    )
    old_composition_job = CompositionJob(
        session_id=story_session.id,
        job_kind=CompositionJobKind.REWRITE,
        status=JobStatus.COMPLETED,
    )
    old_audio_job = AudioJob(
        session_id=story_session.id,
        status=JobStatus.COMPLETED,
        voice_key="moonbeam",
    )
    current_audio_job = AudioJob(
        session_id=story_session.id,
        status=JobStatus.COMPLETED,
        voice_key="storykeeper",
    )
    db_session.add_all(
        [current_composition_job, old_composition_job, old_audio_job, current_audio_job]
    )
    db_session.flush()

    current_segment = CompositionSegment(
        session_id=story_session.id,
        composition_job_id=current_composition_job.id,
        segment_index=0,
        revision_number=2,
        status=JobStatus.COMPLETED,
        acceptance_state=CompositionSegmentAcceptanceState.ACCEPTED,
        text_content="Current accepted segment",
    )
    rejected_segment = CompositionSegment(
        session_id=story_session.id,
        composition_job_id=old_composition_job.id,
        segment_index=0,
        revision_number=1,
        status=JobStatus.COMPLETED,
        acceptance_state=CompositionSegmentAcceptanceState.REJECTED,
        text_content="Rejected rewrite",
    )
    db_session.add_all([current_segment, rejected_segment])
    db_session.flush()

    old_story_location = object_storage.paths.debug_artifact(
        session_id=story_session.id,
        artifact_group="composition/final",
        artifact_name="old-story",
        extension="md",
    )
    current_story_location = object_storage.paths.debug_artifact(
        session_id=story_session.id,
        artifact_group="composition/final",
        artifact_name="current-story",
        extension="md",
    )
    old_final_audio_location = object_storage.paths.final_audio(
        session_id=story_session.id,
        job_id=old_audio_job.id,
    )
    current_final_audio_location = object_storage.paths.final_audio(
        session_id=story_session.id,
        job_id=current_audio_job.id,
    )
    old_audio_segment_location = object_storage.paths.audio_segment(
        session_id=story_session.id,
        job_id=old_audio_job.id,
        segment_index=0,
    )
    current_segment_location = object_storage.paths.partial_draft_segment(
        session_id=story_session.id,
        job_id=current_composition_job.id,
        segment_index=0,
    )
    rejected_segment_location = object_storage.paths.partial_draft_segment(
        session_id=story_session.id,
        job_id=old_composition_job.id,
        segment_index=0,
    )
    draft_snapshot_location = object_storage.paths.draft_text_snapshot(session_id=story_session.id)
    narration_master_location = object_storage.paths.debug_artifact(
        session_id=story_session.id,
        artifact_group="audio/narration-master",
        artifact_name=old_audio_job.id,
        extension="wav",
    )

    object_storage.upload_text(old_story_location, "Old story")
    object_storage.upload_text(current_story_location, "Current story")
    object_storage.upload_bytes(old_final_audio_location, b"old-audio", content_type="audio/wav")
    object_storage.upload_bytes(
        current_final_audio_location,
        b"current-audio",
        content_type="audio/wav",
    )
    object_storage.upload_bytes(
        old_audio_segment_location,
        b"old-segment",
        content_type="audio/wav",
    )
    object_storage.upload_text(current_segment_location, "current segment")
    object_storage.upload_text(rejected_segment_location, "rejected segment")
    object_storage.upload_text(draft_snapshot_location, "draft snapshot")
    object_storage.upload_bytes(
        narration_master_location,
        b"master",
        content_type="audio/wav",
    )

    stale_time = FIXED_NOW - timedelta(days=45)
    current_time = FIXED_NOW - timedelta(days=2)

    current_story_asset = SessionAsset(
        session_id=story_session.id,
        composition_job_id=current_composition_job.id,
        asset_kind=AssetKind.STORY_TEXT,
        status=AssetStatus.READY,
        storage_bucket=current_story_location.bucket,
        object_path=current_story_location.key,
        mime_type="text/markdown",
        ready_at=current_time,
        created_at=current_time,
        updated_at=current_time,
    )
    old_story_asset = SessionAsset(
        session_id=story_session.id,
        composition_job_id=old_composition_job.id,
        asset_kind=AssetKind.STORY_TEXT,
        status=AssetStatus.SUPERSEDED,
        storage_bucket=old_story_location.bucket,
        object_path=old_story_location.key,
        mime_type="text/markdown",
        ready_at=stale_time,
        superseded_at=stale_time,
        created_at=stale_time,
        updated_at=stale_time,
    )
    current_final_audio_asset = SessionAsset(
        session_id=story_session.id,
        audio_job_id=current_audio_job.id,
        asset_kind=AssetKind.FINAL_AUDIO,
        status=AssetStatus.READY,
        storage_bucket=current_final_audio_location.bucket,
        object_path=current_final_audio_location.key,
        mime_type="audio/wav",
        ready_at=current_time,
        created_at=current_time,
        updated_at=current_time,
    )
    old_final_audio_asset = SessionAsset(
        session_id=story_session.id,
        audio_job_id=old_audio_job.id,
        asset_kind=AssetKind.FINAL_AUDIO,
        status=AssetStatus.SUPERSEDED,
        storage_bucket=old_final_audio_location.bucket,
        object_path=old_final_audio_location.key,
        mime_type="audio/wav",
        ready_at=stale_time,
        superseded_at=stale_time,
        created_at=stale_time,
        updated_at=stale_time,
        metadata_json={
            "debug": {
                "narration_master_bucket": narration_master_location.bucket,
                "narration_master_object_path": narration_master_location.key,
            }
        },
    )
    old_audio_segment_asset = SessionAsset(
        session_id=story_session.id,
        audio_job_id=old_audio_job.id,
        asset_kind=AssetKind.AUDIO_SEGMENT,
        status=AssetStatus.READY,
        storage_bucket=old_audio_segment_location.bucket,
        object_path=old_audio_segment_location.key,
        mime_type="audio/wav",
        segment_index=0,
        ready_at=stale_time,
        created_at=stale_time,
        updated_at=stale_time,
    )
    current_segment_asset = SessionAsset(
        session_id=story_session.id,
        composition_job_id=current_composition_job.id,
        composition_segment_id=current_segment.id,
        asset_kind=AssetKind.COMPOSITION_SEGMENT,
        status=AssetStatus.READY,
        storage_bucket=current_segment_location.bucket,
        object_path=current_segment_location.key,
        mime_type="text/markdown",
        segment_index=0,
        ready_at=current_time,
        created_at=current_time,
        updated_at=current_time,
    )
    rejected_segment_asset = SessionAsset(
        session_id=story_session.id,
        composition_job_id=old_composition_job.id,
        composition_segment_id=rejected_segment.id,
        asset_kind=AssetKind.COMPOSITION_SEGMENT,
        status=AssetStatus.READY,
        storage_bucket=rejected_segment_location.bucket,
        object_path=rejected_segment_location.key,
        mime_type="text/markdown",
        segment_index=0,
        ready_at=stale_time,
        created_at=stale_time,
        updated_at=stale_time,
    )
    draft_snapshot_asset = SessionAsset(
        session_id=story_session.id,
        composition_job_id=current_composition_job.id,
        asset_kind=AssetKind.DRAFT_TEXT_SNAPSHOT,
        status=AssetStatus.READY,
        storage_bucket=draft_snapshot_location.bucket,
        object_path=draft_snapshot_location.key,
        mime_type="text/markdown",
        ready_at=stale_time,
        created_at=stale_time,
        updated_at=stale_time,
    )
    db_session.add_all(
        [
            current_story_asset,
            old_story_asset,
            current_final_audio_asset,
            old_final_audio_asset,
            old_audio_segment_asset,
            current_segment_asset,
            rejected_segment_asset,
            draft_snapshot_asset,
        ]
    )
    db_session.commit()

    plan = ArtifactRetentionService(
        db_session,
        object_storage=object_storage,
    ).build_cleanup_plan(now=FIXED_NOW)
    candidate_ids = {candidate.asset_id for candidate in plan.candidates}

    assert old_story_asset.id in candidate_ids
    assert old_final_audio_asset.id in candidate_ids
    assert old_audio_segment_asset.id in candidate_ids
    assert rejected_segment_asset.id in candidate_ids
    assert draft_snapshot_asset.id in candidate_ids
    assert current_story_asset.id not in candidate_ids
    assert current_final_audio_asset.id not in candidate_ids
    assert current_segment_asset.id not in candidate_ids

    old_final_audio_candidate = next(
        candidate for candidate in plan.candidates if candidate.asset_id == old_final_audio_asset.id
    )
    assert {target.role for target in old_final_audio_candidate.targets} == {
        "asset_payload",
        "narration_master_debug",
    }


def test_cleanup_apply_deletes_objects_and_marks_rows(db_session, object_storage) -> None:
    story_session = StorySession(working_title="Retention Apply")
    db_session.add(story_session)
    db_session.flush()

    audio_job = AudioJob(
        session_id=story_session.id,
        status=JobStatus.COMPLETED,
        voice_key="moonbeam",
    )
    current_audio_job = AudioJob(
        session_id=story_session.id,
        status=JobStatus.COMPLETED,
        voice_key="storykeeper",
    )
    composition_job = CompositionJob(
        session_id=story_session.id,
        job_kind=CompositionJobKind.DRAFT,
        status=JobStatus.COMPLETED,
    )
    db_session.add_all([audio_job, current_audio_job, composition_job])
    db_session.flush()

    old_final_audio_location = object_storage.paths.final_audio(
        session_id=story_session.id,
        job_id=audio_job.id,
    )
    narration_master_location = object_storage.paths.debug_artifact(
        session_id=story_session.id,
        artifact_group="audio/narration-master",
        artifact_name=audio_job.id,
        extension="wav",
    )
    current_final_audio_location = object_storage.paths.final_audio(
        session_id=story_session.id,
        job_id=current_audio_job.id,
    )
    draft_snapshot_location = object_storage.paths.draft_text_snapshot(session_id=story_session.id)
    story_location = object_storage.paths.debug_artifact(
        session_id=story_session.id,
        artifact_group="composition/final",
        artifact_name="current-story",
        extension="md",
    )

    object_storage.upload_bytes(old_final_audio_location, b"old-audio", content_type="audio/wav")
    object_storage.upload_bytes(
        narration_master_location,
        b"old-master",
        content_type="audio/wav",
    )
    object_storage.upload_bytes(
        current_final_audio_location,
        b"current-audio",
        content_type="audio/wav",
    )
    object_storage.upload_text(draft_snapshot_location, "draft snapshot")
    object_storage.upload_text(story_location, "current story")

    stale_time = FIXED_NOW - timedelta(days=45)
    current_time = FIXED_NOW - timedelta(days=1)

    current_story_asset = SessionAsset(
        session_id=story_session.id,
        composition_job_id=composition_job.id,
        asset_kind=AssetKind.STORY_TEXT,
        status=AssetStatus.READY,
        storage_bucket=story_location.bucket,
        object_path=story_location.key,
        mime_type="text/markdown",
        ready_at=current_time,
        created_at=current_time,
        updated_at=current_time,
    )
    old_final_audio_asset = SessionAsset(
        session_id=story_session.id,
        audio_job_id=audio_job.id,
        asset_kind=AssetKind.FINAL_AUDIO,
        status=AssetStatus.SUPERSEDED,
        storage_bucket=old_final_audio_location.bucket,
        object_path=old_final_audio_location.key,
        mime_type="audio/wav",
        ready_at=stale_time,
        superseded_at=stale_time,
        created_at=stale_time,
        updated_at=stale_time,
        metadata_json={
            "debug": {
                "narration_master_bucket": narration_master_location.bucket,
                "narration_master_object_path": narration_master_location.key,
            }
        },
    )
    current_final_audio_asset = SessionAsset(
        session_id=story_session.id,
        audio_job_id=current_audio_job.id,
        asset_kind=AssetKind.FINAL_AUDIO,
        status=AssetStatus.READY,
        storage_bucket=current_final_audio_location.bucket,
        object_path=current_final_audio_location.key,
        mime_type="audio/wav",
        ready_at=current_time,
        created_at=current_time,
        updated_at=current_time,
    )
    draft_snapshot_asset = SessionAsset(
        session_id=story_session.id,
        composition_job_id=composition_job.id,
        asset_kind=AssetKind.DRAFT_TEXT_SNAPSHOT,
        status=AssetStatus.READY,
        storage_bucket=draft_snapshot_location.bucket,
        object_path=draft_snapshot_location.key,
        mime_type="text/markdown",
        ready_at=stale_time,
        created_at=stale_time,
        updated_at=stale_time,
    )
    db_session.add_all(
        [
            current_story_asset,
            old_final_audio_asset,
            current_final_audio_asset,
            draft_snapshot_asset,
        ]
    )
    db_session.commit()

    report = ArtifactRetentionService(
        db_session,
        object_storage=object_storage,
    ).cleanup_expired_assets(now=FIXED_NOW, dry_run=False)

    assert report.cleaned_asset_count == 2
    assert report.deleted_object_count == 3
    assert report.missing_object_count == 0

    with pytest.raises(ObjectNotFoundError):
        object_storage.fetch_object_metadata(old_final_audio_location)
    with pytest.raises(ObjectNotFoundError):
        object_storage.fetch_object_metadata(narration_master_location)
    with pytest.raises(ObjectNotFoundError):
        object_storage.fetch_object_metadata(draft_snapshot_location)

    assert object_storage.fetch_object_metadata(current_final_audio_location).size_bytes > 0

    refreshed_old_final_audio = db_session.get(SessionAsset, old_final_audio_asset.id)
    refreshed_draft_snapshot = db_session.get(SessionAsset, draft_snapshot_asset.id)
    assert refreshed_old_final_audio is not None
    assert refreshed_draft_snapshot is not None
    assert refreshed_draft_snapshot.status == AssetStatus.SUPERSEDED
    assert (
        refreshed_old_final_audio.metadata_json["retention_cleanup"]["rule_key"]
        == "superseded_export"
    )
    assert (
        refreshed_draft_snapshot.metadata_json["retention_cleanup"]["rule_key"]
        == "inactive_draft_snapshot"
    )


def test_cleanup_plan_keeps_latest_draft_snapshot_without_story_asset(
    db_session, object_storage
) -> None:
    story_session = StorySession(working_title="Draft Only")
    db_session.add(story_session)
    db_session.flush()

    composition_job = CompositionJob(
        session_id=story_session.id,
        job_kind=CompositionJobKind.DRAFT,
        status=JobStatus.FAILED,
    )
    db_session.add(composition_job)
    db_session.flush()

    draft_snapshot_location = object_storage.paths.draft_text_snapshot(session_id=story_session.id)
    object_storage.upload_text(draft_snapshot_location, "still useful")

    stale_time = FIXED_NOW - timedelta(days=45)
    draft_snapshot_asset = SessionAsset(
        session_id=story_session.id,
        composition_job_id=composition_job.id,
        asset_kind=AssetKind.DRAFT_TEXT_SNAPSHOT,
        status=AssetStatus.READY,
        storage_bucket=draft_snapshot_location.bucket,
        object_path=draft_snapshot_location.key,
        mime_type="text/markdown",
        ready_at=stale_time,
        created_at=stale_time,
        updated_at=stale_time,
    )
    db_session.add(draft_snapshot_asset)
    db_session.commit()

    plan = ArtifactRetentionService(
        db_session,
        object_storage=object_storage,
    ).build_cleanup_plan(now=FIXED_NOW)

    assert plan.candidates == ()


def test_cleanup_plan_keeps_segments_for_latest_failed_audio_job(
    db_session, object_storage
) -> None:
    story_session = StorySession(working_title="Audio Retry")
    db_session.add(story_session)
    db_session.flush()

    failed_audio_job = AudioJob(
        session_id=story_session.id,
        status=JobStatus.FAILED,
        voice_key="moonbeam",
    )
    db_session.add(failed_audio_job)
    db_session.flush()

    segment_location = object_storage.paths.audio_segment(
        session_id=story_session.id,
        job_id=failed_audio_job.id,
        segment_index=0,
    )
    object_storage.upload_bytes(segment_location, b"segment", content_type="audio/wav")

    stale_time = FIXED_NOW - timedelta(days=45)
    segment_asset = SessionAsset(
        session_id=story_session.id,
        audio_job_id=failed_audio_job.id,
        asset_kind=AssetKind.AUDIO_SEGMENT,
        status=AssetStatus.READY,
        storage_bucket=segment_location.bucket,
        object_path=segment_location.key,
        mime_type="audio/wav",
        segment_index=0,
        ready_at=stale_time,
        created_at=stale_time,
        updated_at=stale_time,
    )
    db_session.add(segment_asset)
    db_session.commit()

    plan = ArtifactRetentionService(
        db_session,
        object_storage=object_storage,
    ).build_cleanup_plan(now=FIXED_NOW)

    assert plan.candidates == ()

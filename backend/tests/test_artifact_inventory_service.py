from __future__ import annotations

from app.db import (
    AssetKind,
    AssetStatus,
    AudioJob,
    Base,
    JobStatus,
    SessionAsset,
    StorySession,
    make_engine,
)
from app.services.artifact_inventory import SessionArtifactInventoryService
from sqlalchemy.orm import sessionmaker


def test_artifact_inventory_reports_stale_docx_and_generating_audio_preview() -> None:
    engine = make_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)
    db_session = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)()

    try:
        story_session = StorySession(working_title="Lantern Harbor")
        db_session.add(story_session)
        db_session.flush()

        prior_story_asset = SessionAsset(
            session_id=story_session.id,
            asset_kind=AssetKind.STORY_TEXT,
            status=AssetStatus.SUPERSEDED,
            storage_bucket="storyteller-exports",
            object_path="sessions/story-1/story/prior.md",
            mime_type="text/markdown",
        )
        current_story_asset = SessionAsset(
            session_id=story_session.id,
            asset_kind=AssetKind.STORY_TEXT,
            status=AssetStatus.READY,
            storage_bucket="storyteller-exports",
            object_path="sessions/story-1/story/current.md",
            mime_type="text/markdown",
        )
        stale_docx_asset = SessionAsset(
            session_id=story_session.id,
            asset_kind=AssetKind.STORY_DOCX,
            status=AssetStatus.READY,
            storage_bucket="storyteller-exports",
            object_path="sessions/story-1/exports/story.docx",
            mime_type=(
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            ),
            metadata_json={"source_story_asset_id": "older-story-asset"},
        )
        audio_job = AudioJob(
            session_id=story_session.id,
            status=JobStatus.IN_PROGRESS,
            voice_key="moonbeam",
        )
        db_session.add_all(
            [
                prior_story_asset,
                current_story_asset,
                stale_docx_asset,
                audio_job,
            ]
        )
        db_session.flush()
        preview_asset = SessionAsset(
            session_id=story_session.id,
            asset_kind=AssetKind.AUDIO_SEGMENT,
            status=AssetStatus.READY,
            storage_bucket="storyteller-audio",
            object_path="sessions/story-1/audio/segment-0001.wav",
            mime_type="audio/wav",
            audio_job_id=audio_job.id,
            segment_index=0,
        )
        db_session.add(preview_asset)
        db_session.commit()

        inventory = SessionArtifactInventoryService(db_session).load_inventory(
            story_session.id
        )
        items = {item.key: item for item in inventory.items}

        assert items["story_text"].status == "ready"
        assert items["story_text"].stream_path is not None

        assert items["story_docx"].status == "stale"
        assert "Refresh it" in items["story_docx"].status_detail
        assert items["story_docx"].download_path is not None

        assert items["final_audio"].status == "generating"
        assert items["final_audio"].preview_asset_count == 1
        assert len(items["final_audio"].preview_assets) == 1
        assert items["final_audio"].preview_assets[0].asset_kind == "audio_segment"
    finally:
        db_session.close()
        engine.dispose()


def test_artifact_inventory_reports_missing_docx_and_stale_audio_master() -> None:
    engine = make_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)
    db_session = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)()

    try:
        story_session = StorySession(working_title="Lantern Harbor")
        db_session.add(story_session)
        db_session.flush()

        current_story_asset = SessionAsset(
            session_id=story_session.id,
            asset_kind=AssetKind.STORY_TEXT,
            status=AssetStatus.READY,
            storage_bucket="storyteller-exports",
            object_path="sessions/story-2/story/current.md",
            mime_type="text/markdown",
        )
        previous_audio_job = AudioJob(
            session_id=story_session.id,
            status=JobStatus.COMPLETED,
            voice_key="moonbeam",
        )
        db_session.add_all([current_story_asset, previous_audio_job])
        db_session.flush()
        current_audio_asset = SessionAsset(
            session_id=story_session.id,
            asset_kind=AssetKind.FINAL_AUDIO,
            status=AssetStatus.READY,
            storage_bucket="storyteller-audio",
            object_path="sessions/story-2/audio/final.wav",
            mime_type="audio/wav",
            audio_job_id=previous_audio_job.id,
        )
        replacement_audio_job = AudioJob(
            session_id=story_session.id,
            status=JobStatus.IN_PROGRESS,
            voice_key="storykeeper",
        )
        db_session.add_all([current_audio_asset, replacement_audio_job])
        db_session.commit()

        inventory = SessionArtifactInventoryService(db_session).load_inventory(
            story_session.id
        )
        items = {item.key: item for item in inventory.items}

        assert items["story_docx"].status == "missing"
        assert items["story_docx"].download_path is not None

        assert items["final_audio"].status == "stale"
        assert "previous published master" in items["final_audio"].status_detail
        assert items["final_audio"].download_path is not None
        assert items["final_audio"].stream_path is not None
    finally:
        db_session.close()
        engine.dispose()

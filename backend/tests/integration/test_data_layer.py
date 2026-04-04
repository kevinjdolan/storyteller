from __future__ import annotations

from collections.abc import Callable
from datetime import timedelta
from pathlib import Path
from uuid import uuid4

import pytest
from alembic import command
from alembic.config import Config
from alembic.script import ScriptDirectory
from app.db import (
    AssetKind,
    AssetStatus,
    BackgroundJob,
    EventActorType,
    EventLogEntry,
    JobStatus,
    SessionAsset,
    StorySession,
    WorkflowStageSnapshot,
    utc_now,
)
from app.models import ChatMessageRole, SelectionKind, WorkflowStage, WorkflowStageState
from app.models.identity import LOCAL_DEVELOPMENT_OWNER_ID
from app.services.assets import SessionAssetService
from app.services.event_log import SessionEventLogService
from app.services.jobs import BackgroundJobLeaseLostError, BackgroundJobService
from app.services.sessions import SessionService
from app.storage import ObjectStorageService
from sqlalchemy import create_engine, inspect, select, text, update
from sqlalchemy.orm import Session, sessionmaker

pytestmark = pytest.mark.integration

BACKEND_ROOT = Path(__file__).resolve().parents[2]
EXPECTED_TABLES = {
    "audio_jobs",
    "background_jobs",
    "beat_sheets",
    "character_sheets",
    "composition_jobs",
    "composition_segments",
    "event_log_entries",
    "genres",
    "narration_segments",
    "pitches",
    "session_memory_snapshots",
    "session_assets",
    "story_briefs",
    "story_sessions",
    "story_setups",
    "tone_profiles",
    "workflow_stage_states",
}
EXPECTED_TONE_PROFILE_COLUMNS = {
    "id",
    "genre_id",
    "slug",
    "label",
    "description",
    "bedtime_notes",
    "descriptors",
    "default_planning_hints",
    "sort_order",
    "is_active",
    "created_at",
    "updated_at",
}
EXPECTED_BACKGROUND_JOB_COLUMNS = {
    "id",
    "session_id",
    "job_type",
    "status",
    "payload",
    "result_summary",
    "attempt_count",
    "lease_owner",
    "lease_token",
    "lease_expires_at",
    "claimed_at",
    "heartbeat_at",
    "started_at",
    "completed_at",
    "failed_at",
    "error_message",
    "created_at",
    "updated_at",
}
EXPECTED_SESSION_MEMORY_COLUMNS = {
    "id",
    "session_id",
    "trigger_event_id",
    "trigger_event_type",
    "trigger_event_sequence_number",
    "summary_text",
    "summary_data",
    "created_at",
}
EXPECTED_STORY_SESSION_COLUMNS = {
    "id",
    "owner_id",
    "working_title",
    "current_stage",
    "resume_stage",
    "furthest_completed_stage",
    "overall_status",
    "selected_genre_id",
    "selected_tone_profile_id",
    "audio_voice_key",
    "audio_narration_style",
    "audio_playback_speed",
    "audio_include_background_music",
    "audio_music_profile",
    "audio_narration_volume",
    "audio_music_volume",
    "audio_guidance_notes",
    "completed_at",
    "created_at",
    "updated_at",
}
EXPECTED_STORY_BRIEF_COLUMNS = {
    "id",
    "session_id",
    "revision_number",
    "story_idea",
    "desired_themes",
    "key_images",
    "audience_notes",
    "must_have_elements",
    "raw_brief",
    "normalized_summary",
    "normalized_preferences",
    "planning_notes",
    "model_output",
    "is_active",
    "accepted_at",
    "created_at",
    "updated_at",
}
EXPECTED_COMPOSITION_SEGMENT_COLUMNS = {
    "id",
    "session_id",
    "composition_job_id",
    "superseded_by_segment_id",
    "segment_index",
    "revision_number",
    "status",
    "planned_summary",
    "raw_generated_text",
    "accepted_text",
    "accepted_summary",
    "text_content",
    "word_count",
    "payload",
    "completed_at",
    "created_at",
    "updated_at",
}
EXPECTED_NARRATION_SEGMENT_COLUMNS = {
    "id",
    "session_id",
    "audio_job_id",
    "source_composition_segment_id",
    "segment_index",
    "status",
    "source_boundary_kind",
    "source_outline_card_key",
    "source_outline_card_title",
    "text_content",
    "word_count",
    "text_start_offset",
    "text_end_offset",
    "pause_after_seconds",
    "pause_hint",
    "music_transition_hint",
    "error_message",
    "metadata_json",
    "completed_at",
    "created_at",
    "updated_at",
}


def _build_alembic_config(database_url: str) -> Config:
    config = Config(str(BACKEND_ROOT / "alembic.ini"))
    config.set_main_option("script_location", str(BACKEND_ROOT / "migrations"))
    config.set_main_option("sqlalchemy.url", database_url)
    return config


def _table_names(database_url: str) -> set[str]:
    engine = create_engine(database_url)

    try:
        return set(inspect(engine).get_table_names())
    finally:
        engine.dispose()


def _column_names(database_url: str, table_name: str) -> set[str]:
    engine = create_engine(database_url)

    try:
        return {column["name"] for column in inspect(engine).get_columns(table_name)}
    finally:
        engine.dispose()


def _alembic_version(database_url: str) -> str:
    engine = create_engine(database_url)

    try:
        with engine.connect() as connection:
            return str(
                connection.execute(text("SELECT version_num FROM alembic_version")).scalar_one()
            )
    finally:
        engine.dispose()


def test_postgres_migrations_upgrade_from_zero_to_head_and_back(
    temporary_database_url_factory: Callable[[], str],
) -> None:
    database_url = temporary_database_url_factory()
    config = _build_alembic_config(database_url)
    expected_head = ScriptDirectory.from_config(config).get_current_head()

    command.upgrade(config, "head")
    assert EXPECTED_TABLES <= _table_names(database_url)
    assert EXPECTED_TONE_PROFILE_COLUMNS <= _column_names(database_url, "tone_profiles")
    assert EXPECTED_STORY_SESSION_COLUMNS <= _column_names(database_url, "story_sessions")
    assert EXPECTED_BACKGROUND_JOB_COLUMNS <= _column_names(database_url, "background_jobs")
    assert EXPECTED_STORY_BRIEF_COLUMNS <= _column_names(database_url, "story_briefs")
    assert EXPECTED_COMPOSITION_SEGMENT_COLUMNS <= _column_names(
        database_url,
        "composition_segments",
    )
    assert EXPECTED_NARRATION_SEGMENT_COLUMNS <= _column_names(
        database_url,
        "narration_segments",
    )
    assert EXPECTED_SESSION_MEMORY_COLUMNS <= _column_names(
        database_url,
        "session_memory_snapshots",
    )
    assert _alembic_version(database_url) == expected_head

    command.downgrade(config, "base")
    assert EXPECTED_TABLES.isdisjoint(_table_names(database_url))

    command.upgrade(config, "head")
    assert EXPECTED_TABLES <= _table_names(database_url)
    assert EXPECTED_TONE_PROFILE_COLUMNS <= _column_names(database_url, "tone_profiles")
    assert EXPECTED_STORY_SESSION_COLUMNS <= _column_names(database_url, "story_sessions")
    assert EXPECTED_BACKGROUND_JOB_COLUMNS <= _column_names(database_url, "background_jobs")
    assert EXPECTED_STORY_BRIEF_COLUMNS <= _column_names(database_url, "story_briefs")
    assert EXPECTED_COMPOSITION_SEGMENT_COLUMNS <= _column_names(
        database_url,
        "composition_segments",
    )
    assert EXPECTED_NARRATION_SEGMENT_COLUMNS <= _column_names(
        database_url,
        "narration_segments",
    )
    assert EXPECTED_SESSION_MEMORY_COLUMNS <= _column_names(
        database_url,
        "session_memory_snapshots",
    )
    assert _alembic_version(database_url) == expected_head


def test_session_creation_persists_stage_rows_and_initial_event_history(
    db_session_factory: sessionmaker[Session],
) -> None:
    with db_session_factory() as session:
        created = SessionService(session).create_session(working_title="  Moonlit Mail Route  ")

    with db_session_factory() as session:
        stored_session = session.get(StorySession, created.id)
        stage_rows = list(
            session.execute(
                select(WorkflowStageSnapshot).where(WorkflowStageSnapshot.session_id == created.id)
            ).scalars()
        )
        ordered_stage_rows = sorted(
            stage_rows, key=lambda row: list(WorkflowStage).index(row.stage)
        )
        event_rows = list(
            session.execute(
                select(EventLogEntry)
                .where(EventLogEntry.session_id == created.id)
                .order_by(EventLogEntry.sequence_number.asc())
            ).scalars()
        )
        session_service = SessionService(session)
        reloaded = session_service.load_session_snapshot(created.id)
        history = session_service.load_session_history(created.id)

    assert stored_session is not None
    assert stored_session.owner_id == LOCAL_DEVELOPMENT_OWNER_ID
    assert stored_session.working_title == "Moonlit Mail Route"
    assert stored_session.current_stage == WorkflowStage.GENRE
    assert stored_session.resume_stage == WorkflowStage.GENRE
    assert stored_session.overall_status == WorkflowStageState.DRAFT
    assert [row.stage for row in ordered_stage_rows] == list(WorkflowStage)
    assert all(row.status == WorkflowStageState.DRAFT for row in ordered_stage_rows)
    assert [row.sequence_number for row in event_rows] == [1]
    assert event_rows[0].actor_type == EventActorType.USER
    assert event_rows[0].event_type == "session.created"
    assert event_rows[0].summary == "Created session: Moonlit Mail Route."
    assert event_rows[0].payload == {
        "schema_version": 1,
        "working_title": "Moonlit Mail Route",
    }
    assert reloaded.display_title == "Moonlit Mail Route"
    assert reloaded.owner_id == LOCAL_DEVELOPMENT_OWNER_ID
    assert reloaded.progress.completed_stages == 0
    assert history.latest_sequence_number == 1


def test_event_log_history_is_queryable_across_committed_postgres_sessions(
    db_session_factory: sessionmaker[Session],
) -> None:
    with db_session_factory() as session:
        story_session = StorySession(working_title="Persistent Timeline")
        session.add(story_session)
        session.commit()
        session_id = story_session.id

    with db_session_factory() as session:
        event_log = SessionEventLogService(session)
        event_log.record_selection(
            session_id,
            selection_kind=SelectionKind.GENRE,
            stage=WorkflowStage.GENRE,
            selection_id="genre-quest-fantasy",
            slug="quest-fantasy",
            label="Quest Fantasy",
        )
        event_log.record_chat_message(
            session_id,
            message_role=ChatMessageRole.USER,
            content="Please keep the lake scene calm and short.",
            stage=WorkflowStage.BEATS,
        )
        event_log.record_ui_action(
            session_id,
            action="updated_target_runtime",
            stage=WorkflowStage.STORY_SETUP,
            control_id="runtime-minutes",
            value_summary="~12 minutes",
        )
        session.commit()

    with db_session_factory() as session:
        event_log = SessionEventLogService(session)
        history = event_log.list_session_history(session_id)
        tail = event_log.list_session_history(session_id, after_sequence_number=1)

    assert history.latest_sequence_number == 3
    assert [event.sequence_number for event in history.events] == [1, 2, 3]
    assert history.events[0].event_type == "selection.recorded"
    assert history.events[0].payload is not None
    assert history.events[0].payload.selection_kind == SelectionKind.GENRE
    assert history.events[1].actor.actor_type == EventActorType.USER
    assert history.events[1].payload is not None
    assert history.events[1].payload.message_role == ChatMessageRole.USER
    assert history.events[2].summary == "Recorded UI action: updated_target_runtime."
    assert tail.latest_sequence_number == 3
    assert [event.sequence_number for event in tail.events] == [2, 3]


def test_asset_metadata_round_trips_between_fake_gcs_and_postgres_records(
    db_session_factory: sessionmaker[Session],
    object_storage: ObjectStorageService,
) -> None:
    with db_session_factory() as session:
        story_session = StorySession(working_title="Export Asset Persistence")
        session.add(story_session)
        session.commit()
        session_id = story_session.id

    location = object_storage.paths.export_asset(
        session_id=session_id,
        export_kind="docx",
        export_id=f"story-{uuid4().hex[:8]}",
        extension="docx",
    )
    payload = b"pretend-docx-binary"
    upload_metadata = object_storage.upload_bytes(
        location,
        payload,
        content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )
    fetched_metadata = object_storage.fetch_object_metadata(location)

    with db_session_factory() as session:
        asset_service = SessionAssetService(session)
        created = asset_service.save_asset_record(
            session_id=session_id,
            asset_kind=AssetKind.STORY_DOCX,
            storage_bucket=location.bucket,
            object_path=location.key,
            mime_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            status=AssetStatus.IN_PROGRESS,
            metadata_json={
                "upload_generation": upload_metadata.generation,
            },
        )
        ready = asset_service.mark_asset_ready(
            created.id,
            byte_size=upload_metadata.size_bytes,
            checksum_sha256="integration-checksum",
            metadata_json={
                "etag": upload_metadata.etag,
                "generation": upload_metadata.generation,
                "md5_hash": upload_metadata.md5_hash,
                "updated_at": upload_metadata.updated_at,
            },
        )

    with db_session_factory() as session:
        stored_asset = session.get(SessionAsset, created.id)
        downloadable_assets = SessionAssetService(session).list_downloadable_assets(session_id)

    assert fetched_metadata.location == location
    assert fetched_metadata.size_bytes == len(payload)
    assert fetched_metadata.content_type == (
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
    assert object_storage.download_bytes(location) == payload
    assert ready.status == AssetStatus.READY
    assert ready.byte_size == len(payload)
    assert ready.storage_bucket == location.bucket
    assert ready.object_path == location.key
    assert stored_asset is not None
    assert stored_asset.status == AssetStatus.READY
    assert stored_asset.byte_size == len(payload)
    assert stored_asset.metadata_json == {
        "etag": upload_metadata.etag,
        "generation": upload_metadata.generation,
        "md5_hash": upload_metadata.md5_hash,
        "updated_at": upload_metadata.updated_at,
    }
    assert [asset.id for asset in downloadable_assets] == [created.id]


def test_postgres_job_claiming_reclaims_expired_leases_and_rejects_stale_updates(
    db_session_factory: sessionmaker[Session],
) -> None:
    with db_session_factory() as session:
        story_session = StorySession(working_title="Worker Queue")
        session.add(story_session)
        session.commit()
        session_id = story_session.id

    with db_session_factory() as session:
        jobs = BackgroundJobService(session)
        first = jobs.enqueue_job(
            job_type="demo.echo",
            payload={"message": "first"},
            session_id=session_id,
        )
        second = jobs.enqueue_job(
            job_type="demo.echo",
            payload={"message": "second"},
            session_id=session_id,
        )

    with db_session_factory() as session:
        claim_a = BackgroundJobService(session).claim_next_job(
            lease_owner="worker-a",
            lease_duration=timedelta(seconds=30),
        )

    with db_session_factory() as session:
        claim_b = BackgroundJobService(session).claim_next_job(
            lease_owner="worker-b",
            lease_duration=timedelta(seconds=30),
        )

    assert claim_a is not None
    assert claim_b is not None
    assert claim_a.id == first.id
    assert claim_b.id == second.id
    assert claim_a.attempt_count == 1
    assert claim_b.attempt_count == 1

    with db_session_factory() as session:
        session.execute(
            update(BackgroundJob)
            .where(BackgroundJob.id == claim_a.id)
            .values(
                lease_expires_at=utc_now() - timedelta(seconds=5),
                updated_at=utc_now(),
            )
        )
        session.commit()

    with db_session_factory() as session:
        reclaimed = BackgroundJobService(session).claim_next_job(
            lease_owner="worker-c",
            lease_duration=timedelta(seconds=45),
        )

    assert reclaimed is not None
    assert reclaimed.id == claim_a.id
    assert reclaimed.attempt_count == 2
    assert reclaimed.lease_owner == "worker-c"
    assert reclaimed.lease_token != claim_a.lease_token

    with db_session_factory() as session:
        with pytest.raises(BackgroundJobLeaseLostError):
            BackgroundJobService(session).complete_job(
                claim_a,
                result_summary={"outcome": "stale"},
            )

    with db_session_factory() as session:
        completed = BackgroundJobService(session).complete_job(
            reclaimed,
            result_summary={"outcome": "completed"},
        )

    with db_session_factory() as session:
        stored_jobs = list(
            session.execute(
                select(BackgroundJob)
                .where(BackgroundJob.session_id == session_id)
                .order_by(BackgroundJob.created_at.asc())
            ).scalars()
        )

    assert completed.status == JobStatus.COMPLETED
    assert completed.result_summary == {"outcome": "completed"}
    assert completed.completed_at is not None
    assert completed.lease_owner is None
    assert stored_jobs[0].id == first.id
    assert stored_jobs[0].attempt_count == 2
    assert stored_jobs[0].status == JobStatus.COMPLETED
    assert stored_jobs[1].id == second.id
    assert stored_jobs[1].status == JobStatus.IN_PROGRESS

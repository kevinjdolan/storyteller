from __future__ import annotations

from collections.abc import Iterable
from datetime import datetime, timezone

from app.db import (
    AssetKind,
    AssetStatus,
    AudioJob,
    Base,
    BeatSheet,
    CharacterSheet,
    CompositionJob,
    CompositionJobKind,
    CompositionSegment,
    EventActorType,
    EventLogEntry,
    ExportAsset,
    Genre,
    JobStatus,
    Pitch,
    StoryBrief,
    StorySession,
    StorySetup,
    ToneProfile,
    WorkflowStageSnapshot,
    make_engine,
)
from app.models import WorkflowStage, WorkflowStageState
from sqlalchemy import inspect
from sqlalchemy.orm import sessionmaker


def _enable_sqlite_foreign_keys(engine) -> None:
    with engine.begin() as connection:
        connection.exec_driver_sql("PRAGMA foreign_keys=ON")


def _as_set(values: Iterable[str]) -> set[str]:
    return set(values)


def test_story_schema_can_store_in_progress_and_completed_sessions() -> None:
    engine = make_engine("sqlite+pysqlite:///:memory:")
    _enable_sqlite_foreign_keys(engine)
    Base.metadata.create_all(engine)
    db_session = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)()

    try:
        now = datetime.now(timezone.utc)
        genre = Genre(
            slug="quest-fantasy",
            label="Quest Fantasy",
            description="A gentle adventure with bedtime-safe stakes.",
        )
        tone = ToneProfile(
            genre=genre,
            slug="hushed-wonder",
            label="Hushed Wonder",
            description="Calm and luminous.",
            default_planning_hints={"pacing": "unhurried"},
        )

        draft_session = StorySession(
            working_title="Moonlit Boat Ride",
            current_stage=WorkflowStage.COMPOSITION,
            resume_stage=WorkflowStage.COMPOSITION,
            furthest_completed_stage=WorkflowStage.STORY_SETUP,
            overall_status=WorkflowStageState.IN_PROGRESS,
            selected_genre=genre,
            selected_tone_profile=tone,
        )
        completion_event = EventLogEntry(
            session=draft_session,
            sequence_number=1,
            actor_type=EventActorType.USER,
            actor_id="local-user",
            event_type="accepted_story_setup",
            stage=WorkflowStage.STORY_SETUP,
            summary="Accepted the current story setup targets.",
        )
        draft_session.workflow_stage_states.extend(
            [
                WorkflowStageSnapshot(
                    stage=WorkflowStage.GENRE,
                    status=WorkflowStageState.COMPLETED,
                    completed_at=now,
                    last_event=completion_event,
                ),
                WorkflowStageSnapshot(
                    stage=WorkflowStage.TONE,
                    status=WorkflowStageState.COMPLETED,
                    completed_at=now,
                ),
                WorkflowStageSnapshot(
                    stage=WorkflowStage.BRIEF,
                    status=WorkflowStageState.COMPLETED,
                    completed_at=now,
                ),
                WorkflowStageSnapshot(
                    stage=WorkflowStage.PITCHES,
                    status=WorkflowStageState.COMPLETED,
                    completed_at=now,
                ),
                WorkflowStageSnapshot(
                    stage=WorkflowStage.CHARACTERS,
                    status=WorkflowStageState.COMPLETED,
                    completed_at=now,
                ),
                WorkflowStageSnapshot(
                    stage=WorkflowStage.BEATS,
                    status=WorkflowStageState.COMPLETED,
                    completed_at=now,
                ),
                WorkflowStageSnapshot(
                    stage=WorkflowStage.STORY_SETUP,
                    status=WorkflowStageState.COMPLETED,
                    completed_at=now,
                ),
                WorkflowStageSnapshot(
                    stage=WorkflowStage.COMPOSITION,
                    status=WorkflowStageState.IN_PROGRESS,
                    started_at=now,
                ),
            ],
        )
        brief = StoryBrief(
            session=draft_session,
            revision_number=1,
            raw_brief="A sleepy fox rows across a moonlit lake.",
            normalized_summary=(
                "A bedtime-safe quest about crossing the lake to find a glowing reed."
            ),
            is_active=True,
            accepted_at=now,
        )
        pitch = Pitch(
            session=draft_session,
            story_brief=brief,
            generation_key="pitch-batch-1",
            pitch_index=0,
            title="The Reed of Quiet Light",
            logline="A young fox follows ripples toward a gentle night mystery.",
            is_selected=True,
            accepted_at=now,
        )
        character_sheet = CharacterSheet(
            session=draft_session,
            pitch=pitch,
            revision_number=1,
            protagonist_name="Pip",
            summary="Pip is cautious, curious, and soothed by steady rhythms.",
            is_selected=True,
            accepted_at=now,
        )
        beat_sheet = BeatSheet(
            session=draft_session,
            character_sheet=character_sheet,
            revision_number=1,
            summary="A soft Save-the-Cat arc with a reassuring return home.",
            beats={"opening_image": "Moonlight on still water"},
            is_selected=True,
            accepted_at=now,
        )
        story_setup = StorySetup(
            session=draft_session,
            beat_sheet=beat_sheet,
            revision_number=1,
            target_word_count=1800,
            target_runtime_minutes=12,
            chapter_count=3,
            chapter_style="three gentle chapters",
            is_selected=True,
            accepted_at=now,
        )
        composition_job = CompositionJob(
            session=draft_session,
            beat_sheet=beat_sheet,
            story_setup=story_setup,
            job_kind=CompositionJobKind.DRAFT,
            status=JobStatus.IN_PROGRESS,
            progress_percent=42.5,
            current_segment_index=2,
        )
        composition_segment = CompositionSegment(
            session=draft_session,
            composition_job=composition_job,
            segment_index=2,
            revision_number=1,
            status=JobStatus.IN_PROGRESS,
            planned_summary="Pip reaches the reeds and hears the lake settle.",
        )

        completed_session = StorySession(
            working_title="The Lantern Nest",
            current_stage=WorkflowStage.FINALIZE,
            resume_stage=WorkflowStage.FINALIZE,
            furthest_completed_stage=WorkflowStage.FINALIZE,
            overall_status=WorkflowStageState.COMPLETED,
            selected_genre=genre,
            selected_tone_profile=tone,
            completed_at=now,
        )
        audio_job = AudioJob(
            session=completed_session,
            source_composition_job=composition_job,
            status=JobStatus.COMPLETED,
            voice_key="gemini-soft-1",
            playback_speed=0.95,
            include_background_music=True,
            estimated_duration_seconds=620,
            completed_at=now,
        )
        final_audio = ExportAsset(
            session=completed_session,
            audio_job=audio_job,
            asset_kind=AssetKind.FINAL_AUDIO,
            status=AssetStatus.READY,
            storage_bucket="storyteller-exports",
            storage_key="sessions/final-audio.mp3",
            mime_type="audio/mpeg",
            byte_size=2048,
            ready_at=now,
        )

        db_session.add_all(
            [
                genre,
                tone,
                draft_session,
                completion_event,
                brief,
                pitch,
                character_sheet,
                beat_sheet,
                story_setup,
                composition_job,
                composition_segment,
                completed_session,
                audio_job,
                final_audio,
            ]
        )
        db_session.commit()
        db_session.expire_all()

        session_rows = (
            db_session.query(StorySession).order_by(StorySession.working_title.asc()).all()
        )

        assert [row.working_title for row in session_rows] == [
            "Moonlit Boat Ride",
            "The Lantern Nest",
        ]
        assert session_rows[0].overall_status == WorkflowStageState.IN_PROGRESS
        assert any(
            stage.stage == WorkflowStage.COMPOSITION
            and stage.status == WorkflowStageState.IN_PROGRESS
            for stage in session_rows[0].workflow_stage_states
        )
        assert session_rows[0].selected_tone_profile.default_planning_hints == {
            "pacing": "unhurried"
        }
        assert (
            session_rows[0]
            .composition_jobs[0]
            .segments[0]
            .planned_summary.startswith("Pip reaches")
        )
        assert session_rows[1].overall_status == WorkflowStageState.COMPLETED
        assert session_rows[1].audio_jobs[0].status == JobStatus.COMPLETED
        assert session_rows[1].export_assets[0].asset_kind == AssetKind.FINAL_AUDIO
        assert session_rows[1].export_assets[0].status == AssetStatus.READY
    finally:
        db_session.close()
        engine.dispose()


def test_story_schema_exposes_expected_indexes_and_foreign_keys() -> None:
    engine = make_engine("sqlite+pysqlite:///:memory:")
    _enable_sqlite_foreign_keys(engine)
    Base.metadata.create_all(engine)

    try:
        inspector = inspect(engine)

        assert _as_set(inspector.get_table_names()) >= {
            "audio_jobs",
            "beat_sheets",
            "character_sheets",
            "composition_jobs",
            "composition_segments",
            "event_log_entries",
            "export_assets",
            "genres",
            "pitches",
            "story_briefs",
            "story_sessions",
            "story_setups",
            "tone_profiles",
            "workflow_stage_states",
        }

        story_session_indexes = {index["name"] for index in inspector.get_indexes("story_sessions")}
        workflow_indexes = {
            index["name"] for index in inspector.get_indexes("workflow_stage_states")
        }
        asset_indexes = {index["name"] for index in inspector.get_indexes("export_assets")}

        assert {
            "ix_story_sessions_current_stage",
            "ix_story_sessions_overall_status_updated_at",
            "ix_story_sessions_resume_stage",
        } <= story_session_indexes
        assert {"ix_workflow_stage_states_session_id_status"} <= workflow_indexes
        assert {"ix_export_assets_session_id_asset_kind_status"} <= asset_indexes

        tone_profile_foreign_keys = {
            fk["constrained_columns"][0]: fk["referred_table"]
            for fk in inspector.get_foreign_keys("tone_profiles")
        }
        pitch_foreign_keys = {
            tuple(fk["constrained_columns"]): fk["referred_table"]
            for fk in inspector.get_foreign_keys("pitches")
        }
        asset_foreign_keys = {
            tuple(fk["constrained_columns"]): fk["referred_table"]
            for fk in inspector.get_foreign_keys("export_assets")
        }

        assert tone_profile_foreign_keys["genre_id"] == "genres"
        assert pitch_foreign_keys[("session_id",)] == "story_sessions"
        assert pitch_foreign_keys[("story_brief_id",)] == "story_briefs"
        assert asset_foreign_keys[("session_id",)] == "story_sessions"
        assert asset_foreign_keys[("audio_job_id",)] == "audio_jobs"
        assert asset_foreign_keys[("composition_job_id",)] == "composition_jobs"
    finally:
        engine.dispose()

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest
from app.ai import render_intent_parser_prompt
from app.db import (
    AudioJob,
    Base,
    BeatSheet,
    CharacterSheet,
    CompositionJob,
    CompositionJobKind,
    CompositionSegment,
    Genre,
    JobStatus,
    Pitch,
    StoryBrief,
    StorySession,
    StorySetup,
    ToneProfile,
    make_engine,
)
from app.models import (
    ChatToUIActionBatch,
    IntentParserPromptContext,
    IntentParserStageContext,
    StoryWorkflowToolExecutionMode,
    StoryWorkflowToolName,
    WorkflowStage,
    WorkflowStageState,
)
from app.services import (
    BackgroundJobService,
    SessionService,
    StoryWorkflowActionRouter,
    StoryWorkflowToolService,
    get_story_workflow_tool_registry,
    get_story_workflow_tool_schema_bundle,
)
from app.worker import JobWorker, build_default_job_handler_registry
from sqlalchemy.orm import Session, sessionmaker


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


def _build_session_factory(tmp_path: Path) -> sessionmaker[Session]:
    database_path = tmp_path / "story-tools.db"
    engine = make_engine(f"sqlite+pysqlite:///{database_path}")
    _enable_sqlite_foreign_keys(engine)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


def test_story_workflow_tool_schema_bundle_lists_expected_operations() -> None:
    bundle = get_story_workflow_tool_schema_bundle()

    tool_names = [item["tool_name"] for item in bundle["tools"]]
    assert bundle["bundle_schema_version"] == 1
    assert tool_names == [
        "compose_next_segment",
        "estimate_audio_length",
        "generate_beat_sheet",
        "generate_character_sheets",
        "generate_pitches",
        "refine_character_sheet",
        "refine_pitch",
        "rewrite_segments",
        "start_audio_generation",
        "update_setup_heuristics",
    ]
    assert bundle["tools"][0]["side_effects"]
    assert bundle["tools"][-1]["output_schema"]["title"] == "UpdateSetupHeuristicsToolResult"


def test_story_workflow_action_router_maps_chat_actions_to_shared_tool_calls() -> None:
    batch = ChatToUIActionBatch.model_validate(
        {
            "actions": [
                {
                    "action_type": "update_story_setup",
                    "target_stage": "story_setup",
                    "confidence": 0.9,
                    "requires_confirmation": False,
                    "extracted_values": {
                        "target_runtime_minutes": 8,
                        "chapter_count": 2,
                    },
                },
                {
                    "action_type": "start_composition",
                    "target_stage": "composition",
                    "confidence": 0.88,
                    "requires_confirmation": True,
                    "extracted_values": {
                        "mode": "rewrite",
                        "instructions": "Rewrite the opening scene to feel gentler.",
                        "restart_from_segment_index": 1,
                    },
                },
                {
                    "action_type": "start_audio_generation",
                    "target_stage": "audio",
                    "confidence": 0.81,
                    "requires_confirmation": True,
                    "extracted_values": {
                        "voice_key": "gemini-soft-1",
                        "playback_speed": 0.9,
                    },
                },
            ]
        }
    )

    plan = StoryWorkflowActionRouter().plan_calls(
        session_id="session-123",
        batch=batch,
    )

    assert [call.tool_name for call in plan.calls] == [
        StoryWorkflowToolName.UPDATE_SETUP_HEURISTICS,
        StoryWorkflowToolName.REWRITE_SEGMENTS,
        StoryWorkflowToolName.START_AUDIO_GENERATION,
    ]
    assert plan.calls[1].arguments == {
        "instructions": "Rewrite the opening scene to feel gentler.",
        "rewrite_from_segment_index": 1,
        "preserve_completed_segments": False,
        "schema_version": 1,
    }


def test_story_workflow_tool_service_updates_setup_and_cancels_invalidated_jobs(
    db_session,
) -> None:
    seeded = _seed_story_setup_session(
        db_session,
        composition_status=JobStatus.IN_PROGRESS,
        audio_status=JobStatus.IN_PROGRESS,
    )

    result = StoryWorkflowToolService(db_session).execute(
        tool_name=StoryWorkflowToolName.UPDATE_SETUP_HEURISTICS,
        session_id=seeded["session_id"],
        arguments={
            "target_runtime_minutes": 8,
            "chapter_count": 2,
            "guidance_notes": "Keep the ending even softer.",
        },
    )

    snapshot = SessionService(db_session).load_session_snapshot(seeded["session_id"])
    composition_job = db_session.get(CompositionJob, seeded["composition_job_id"])
    audio_job = db_session.get(AudioJob, seeded["audio_job_id"])

    assert result.story_setup_id == snapshot.selected_story_setup.id
    assert result.revision_number == 2
    assert snapshot.selected_story_setup.target_runtime_minutes == 8
    assert snapshot.selected_story_setup.chapter_count == 2
    assert snapshot.selected_story_setup.guidance_notes == "Keep the ending even softer."
    assert composition_job is not None and composition_job.status == JobStatus.CANCELLED
    assert audio_job is not None and audio_job.status == JobStatus.CANCELLED
    assert _stage_status(snapshot, WorkflowStage.STORY_SETUP) == WorkflowStageState.COMPLETED
    assert (
        _stage_status(snapshot, WorkflowStage.COMPOSITION)
        == WorkflowStageState.NEEDS_REGENERATION
    )
    assert _stage_status(snapshot, WorkflowStage.AUDIO) == WorkflowStageState.NEEDS_REGENERATION


def test_story_workflow_tool_service_estimates_audio_length_from_segments(db_session) -> None:
    seeded = _seed_story_setup_session(
        db_session,
        mark_composition_completed=True,
        composition_segment_word_counts=[240, 160],
    )

    result = StoryWorkflowToolService(db_session).execute(
        tool_name=StoryWorkflowToolName.ESTIMATE_AUDIO_LENGTH,
        session_id=seeded["session_id"],
        arguments={
            "playback_speed": 0.8,
        },
    )

    assert result.estimated_word_count == 400
    assert result.estimated_duration_seconds == 215
    assert result.basis_source == "composition_segments"


def test_worker_processes_story_tool_job_via_default_registry(tmp_path: Path) -> None:
    session_factory = _build_session_factory(tmp_path)

    with session_factory() as session:
        seeded = _seed_story_setup_session(session)
        queued = StoryWorkflowToolService(session).enqueue(
            tool_name=StoryWorkflowToolName.UPDATE_SETUP_HEURISTICS,
            session_id=seeded["session_id"],
            arguments={
                "target_runtime_minutes": 7,
                "guidance_notes": "Make the read-aloud shorter.",
            },
        )

    worker = JobWorker(
        session_factory=session_factory,
        registry=build_default_job_handler_registry(),
        worker_id="story-tool-worker",
        lease_duration=timedelta(seconds=30),
        poll_interval_seconds=0.01,
    )

    assert worker.run_once() is True

    with session_factory() as session:
        job = BackgroundJobService(session).get_job(queued.id)
        snapshot = SessionService(session).load_session_snapshot(seeded["session_id"])

    assert job.status == JobStatus.COMPLETED
    assert job.result_summary["tool_name"] == "update_setup_heuristics"
    assert snapshot.selected_story_setup is not None
    assert snapshot.selected_story_setup.target_runtime_minutes == 7


def test_eval_prompt_exposes_story_tool_catalog_for_chat_translation() -> None:
    prompt = render_intent_parser_prompt(
        IntentParserPromptContext(
            session_id="session-123",
            display_title="Moonlit Harbor",
            overall_status=WorkflowStageState.IN_PROGRESS,
            resume_stage=WorkflowStage.BEATS,
            stage_context=IntentParserStageContext(
                current_stage=WorkflowStage.BEATS,
                current_stage_label="Beat sheet",
                current_stage_description=(
                    "Store the accepted Save-the-Cat beat sheet for the session."
                ),
                current_stage_status=WorkflowStageState.IN_PROGRESS,
                current_stage_detail="Refining the midpoint tension.",
            ),
            session_summary="Selected tone: Hushed Wonder",
            user_message="make it shorter and gentler",
        )
    )

    assert "Related backend tool registry" in prompt
    assert '"tool_name": "generate_pitches"' in prompt
    assert '"tool_name": "start_audio_generation"' in prompt


def test_eval_registry_alignment_keeps_worker_and_prompt_catalogs_in_sync() -> None:
    registry = get_story_workflow_tool_registry()
    prompt_catalog_names = {item["tool_name"] for item in registry.build_prompt_catalog()}
    worker_job_types = set(build_default_job_handler_registry().registered_job_types())

    assert prompt_catalog_names == {definition.name.value for definition in registry.list_tools()}
    assert worker_job_types >= {definition.job_type for definition in registry.list_tools()}


def test_eval_background_tool_modes_cover_long_running_story_operations() -> None:
    registry = get_story_workflow_tool_registry()
    background_tools = {
        definition.name
        for definition in registry.list_tools()
        if definition.execution_mode == StoryWorkflowToolExecutionMode.BACKGROUND
    }

    assert background_tools >= {
        StoryWorkflowToolName.GENERATE_PITCHES,
        StoryWorkflowToolName.GENERATE_CHARACTER_SHEETS,
        StoryWorkflowToolName.GENERATE_BEAT_SHEET,
        StoryWorkflowToolName.COMPOSE_NEXT_SEGMENT,
        StoryWorkflowToolName.REWRITE_SEGMENTS,
        StoryWorkflowToolName.START_AUDIO_GENERATION,
    }


def _seed_story_setup_session(
    db_session: Session,
    *,
    composition_status: JobStatus | None = None,
    audio_status: JobStatus | None = None,
    mark_composition_completed: bool = False,
    composition_segment_word_counts: list[int] | None = None,
) -> dict[str, str | None]:
    now = datetime.now(timezone.utc)
    service = SessionService(db_session)
    genre = Genre(
        slug="quest-fantasy",
        label="Quest Fantasy",
        description="A gentle harbor adventure.",
    )
    tone = ToneProfile(
        genre=genre,
        slug="hushed-wonder",
        label="Hushed Wonder",
        description="Soft and luminous.",
    )
    db_session.add_all([genre, tone])
    db_session.flush()

    snapshot = service.create_session(working_title="Moonlit Harbor")
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
        WorkflowStage.BEATS,
        WorkflowStage.STORY_SETUP,
    ):
        service.update_stage_state(
            snapshot.id,
            stage=stage,
            status=WorkflowStageState.COMPLETED,
        )

    brief = StoryBrief(
        session_id=snapshot.id,
        revision_number=1,
        raw_brief="A harbor fox follows a silver clue and returns home calm.",
        normalized_summary="A bedtime harbor mystery with a gentle emotional repair.",
        planning_notes="Keep the midpoint safe and sleepy.",
        is_active=True,
        accepted_at=now,
    )
    db_session.add(brief)
    db_session.flush()

    pitch = Pitch(
        session_id=snapshot.id,
        story_brief_id=brief.id,
        generation_key="batch-1",
        pitch_index=1,
        title="The Silver Bell Buoy",
        logline="A harbor fox follows a bell across moonlit water.",
        is_selected=True,
        accepted_at=now,
    )
    db_session.add(pitch)
    db_session.flush()

    character_sheet = CharacterSheet(
        session_id=snapshot.id,
        pitch_id=pitch.id,
        revision_number=1,
        title="Mira and the Bell",
        protagonist_name="Mira",
        is_selected=True,
        accepted_at=now,
    )
    db_session.add(character_sheet)
    db_session.flush()

    beat_sheet = BeatSheet(
        session_id=snapshot.id,
        character_sheet_id=character_sheet.id,
        revision_number=1,
        summary="A soft Save-the-Cat arc.",
        is_selected=True,
        accepted_at=now,
    )
    db_session.add(beat_sheet)
    db_session.flush()

    story_setup = StorySetup(
        session_id=snapshot.id,
        beat_sheet_id=beat_sheet.id,
        revision_number=1,
        target_word_count=1600,
        target_runtime_minutes=11,
        chapter_count=3,
        chapter_style="three gentle chapters",
        guidance_notes="End each chapter with a calmer image than it began.",
        is_selected=True,
        accepted_at=now,
    )
    db_session.add(story_setup)
    db_session.flush()

    composition_job_id: str | None = None
    if composition_status is not None:
        service.update_stage_state(
            snapshot.id,
            stage=WorkflowStage.COMPOSITION,
            status=WorkflowStageState.IN_PROGRESS,
        )
        composition_job = CompositionJob(
            session_id=snapshot.id,
            beat_sheet_id=beat_sheet.id,
            story_setup_id=story_setup.id,
            job_kind=CompositionJobKind.DRAFT,
            status=composition_status,
            progress_percent=42,
            current_segment_index=2,
            started_at=now,
        )
        db_session.add(composition_job)
        db_session.flush()
        composition_job_id = composition_job.id
    elif mark_composition_completed or composition_segment_word_counts:
        service.update_stage_state(
            snapshot.id,
            stage=WorkflowStage.COMPOSITION,
            status=WorkflowStageState.COMPLETED,
        )
        composition_job = CompositionJob(
            session_id=snapshot.id,
            beat_sheet_id=beat_sheet.id,
            story_setup_id=story_setup.id,
            job_kind=CompositionJobKind.DRAFT,
            status=JobStatus.COMPLETED,
            progress_percent=100,
            current_segment_index=(
                len(composition_segment_word_counts or [])
                if composition_segment_word_counts
                else None
            ),
            started_at=now,
            completed_at=now,
        )
        db_session.add(composition_job)
        db_session.flush()
        composition_job_id = composition_job.id

        for index, word_count in enumerate(composition_segment_word_counts or [], start=1):
            db_session.add(
                CompositionSegment(
                    session_id=snapshot.id,
                    composition_job_id=composition_job.id,
                    segment_index=index,
                    revision_number=1,
                    status=JobStatus.COMPLETED,
                    word_count=word_count,
                    text_content="moonlight " * word_count,
                    completed_at=now,
                )
            )
        db_session.flush()

    audio_job_id: str | None = None
    if audio_status is not None:
        if composition_status is not None:
            service.update_stage_state(
                snapshot.id,
                stage=WorkflowStage.COMPOSITION,
                status=WorkflowStageState.COMPLETED,
            )
        service.update_stage_state(
            snapshot.id,
            stage=WorkflowStage.AUDIO,
            status=WorkflowStageState.IN_PROGRESS,
        )
        audio_job = AudioJob(
            session_id=snapshot.id,
            source_composition_job_id=composition_job_id,
            status=audio_status,
            voice_key="gemini-soft-1",
            playback_speed=1.0,
            include_background_music=False,
            started_at=now,
        )
        db_session.add(audio_job)
        db_session.flush()
        audio_job_id = audio_job.id

    db_session.commit()
    return {
        "session_id": snapshot.id,
        "composition_job_id": composition_job_id,
        "audio_job_id": audio_job_id,
    }


def _stage_status(snapshot, stage: WorkflowStage) -> WorkflowStageState:
    return next(item.status for item in snapshot.stage_states if item.stage == stage)

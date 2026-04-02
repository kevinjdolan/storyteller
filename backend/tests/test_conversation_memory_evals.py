from __future__ import annotations

from datetime import datetime, timezone

import pytest
from app.db import (
    Base,
    CompositionJob,
    CompositionJobKind,
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
    IntentParserStructuredOutput,
    SelectionKind,
    SessionContextUpdateRequest,
    WorkflowStage,
)
from app.models.workflow import WorkflowStageState
from app.services import (
    SessionEventLogService,
    SessionIntentParserService,
    SessionMemoryService,
    SessionService,
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


class StubIntentParserAdapter:
    def __init__(self, structured_output: IntentParserStructuredOutput) -> None:
        self.model_id = "gemini-3.1-flash-lite"
        self._structured_output = structured_output
        self.invocations = []

    def parse(self, invocation):
        from app.models import IntentParserInvocationResult

        self.invocations.append(invocation)
        return IntentParserInvocationResult(
            invocation=invocation,
            structured_output=self._structured_output,
            raw_response={"mock": "response"},
        )

    def close(self) -> None:
        return None


def test_eval_fresh_accepted_decisions_replace_stale_pitch_choices(db_session) -> None:
    now = datetime.now(timezone.utc)
    genre = Genre(
        slug="quest-fantasy",
        label="Quest Fantasy",
        description="A gentle bedtime adventure.",
    )
    tone = ToneProfile(
        genre=genre,
        slug="hushed-wonder",
        label="Hushed Wonder",
        description="Quiet and luminous.",
    )
    db_session.add_all([genre, tone])
    db_session.flush()

    session_service = SessionService(db_session)
    snapshot = session_service.create_session(working_title="Pitch Freshness")
    story_session = db_session.get(StorySession, snapshot.id)
    assert story_session is not None
    story_session.selected_genre = genre
    story_session.selected_tone_profile = tone

    for stage in (WorkflowStage.GENRE, WorkflowStage.TONE, WorkflowStage.BRIEF):
        session_service.update_stage_state(
            snapshot.id,
            stage=stage,
            status=WorkflowStageState.COMPLETED,
        )
    session_service.update_stage_state(
        snapshot.id,
        stage=WorkflowStage.PITCHES,
        status=WorkflowStageState.IN_PROGRESS,
        detail="Selecting the strongest bedtime pitch.",
    )

    brief = StoryBrief(
        session_id=snapshot.id,
        revision_number=1,
        raw_brief="A harbor fox follows moonlight across quiet docks.",
        normalized_summary="A sleepy harbor mystery with a safe return home.",
        is_active=True,
        accepted_at=now,
    )
    old_pitch = Pitch(
        session_id=snapshot.id,
        story_brief=brief,
        generation_key="pitch-batch-1",
        pitch_index=0,
        title="Lanterns Across the Docks",
        logline="A fox follows harbor lanterns toward a gentle answer.",
        is_selected=True,
        accepted_at=now,
    )
    stale_pitch = Pitch(
        session_id=snapshot.id,
        story_brief=brief,
        generation_key="pitch-batch-1",
        pitch_index=1,
        title="The Sleepy Tide Bell",
        logline="A tide bell rings once and everyone settles again.",
        is_selected=False,
    )
    new_pitch = Pitch(
        session_id=snapshot.id,
        story_brief=brief,
        generation_key="pitch-batch-2",
        pitch_index=0,
        title="The Moonpost Ferry",
        logline="A fox ferries one last moonlit letter before bed.",
        is_selected=False,
    )
    db_session.add_all([brief, old_pitch, stale_pitch, new_pitch])
    db_session.flush()

    event_log = SessionEventLogService(db_session)
    event_log.record_selection(
        snapshot.id,
        selection_kind=SelectionKind.PITCH,
        stage=WorkflowStage.PITCHES,
        selection_id=old_pitch.id,
        label=old_pitch.title,
    )
    db_session.commit()

    old_pitch = db_session.get(Pitch, old_pitch.id)
    new_pitch = db_session.get(Pitch, new_pitch.id)
    assert old_pitch is not None and new_pitch is not None
    old_pitch.is_selected = False
    new_pitch.is_selected = True
    new_pitch.accepted_at = now
    db_session.flush()

    event_log.record_selection(
        snapshot.id,
        selection_kind=SelectionKind.PITCH,
        stage=WorkflowStage.PITCHES,
        selection_id=new_pitch.id,
        previous_selection_id=old_pitch.id,
        label=new_pitch.title,
    )
    db_session.commit()

    memory_service = SessionMemoryService(db_session)
    latest = memory_service.load_latest_snapshot(snapshot.id)
    history = memory_service.list_snapshots(snapshot.id, limit=10)

    assert latest is not None
    assert "Selected pitch: The Moonpost Ferry" in latest.summary_text
    assert "Selected pitch: Lanterns Across the Docks" not in latest.summary_text
    assert "The Sleepy Tide Bell" not in latest.summary_text
    assert len(history) >= 3
    assert history[0].trigger_event_type == "selection.recorded"


def test_eval_user_preferences_keep_runtime_and_guidance_notes(db_session) -> None:
    now = datetime.now(timezone.utc)
    session_id = SessionService(db_session).create_session(working_title="Preference Memory").id
    story_setup = StorySetup(
        session_id=session_id,
        revision_number=1,
        target_word_count=1800,
        target_runtime_minutes=12,
        chapter_count=3,
        approximate_scene_count=9,
        chapter_style="three gentle chapters",
        guidance_notes="Let each chapter end on a calmer image than it began.",
        is_selected=True,
        accepted_at=now,
    )
    db_session.add(story_setup)
    db_session.flush()

    SessionEventLogService(db_session).record_selection(
        session_id,
        selection_kind=SelectionKind.STORY_SETUP,
        stage=WorkflowStage.STORY_SETUP,
        selection_id=story_setup.id,
        label="Selected story setup",
    )
    db_session.commit()

    latest = SessionMemoryService(db_session).load_latest_snapshot(session_id)

    assert latest is not None
    assert (
        "Story setup: 1800 words, 12 minutes, 3 chapters, about 9 scenes, three gentle chapters"
        in latest.summary_text
    )
    assert "Setup guidance: Let each chapter end on a calmer image than it began." in (
        latest.summary_text
    )


def test_eval_unresolved_stage_notes_survive_resume_progression(db_session) -> None:
    session_service = SessionService(db_session)
    snapshot = session_service.create_session(working_title="Resume Context")

    for stage in (
        WorkflowStage.GENRE,
        WorkflowStage.TONE,
        WorkflowStage.BRIEF,
        WorkflowStage.PITCHES,
        WorkflowStage.CHARACTERS,
        WorkflowStage.BEATS,
    ):
        session_service.update_stage_state(
            snapshot.id,
            stage=stage,
            status=WorkflowStageState.COMPLETED,
            detail=f"Accepted {stage.value}.",
        )

    result = session_service.apply_context_update(
        snapshot.id,
        payload=SessionContextUpdateRequest.model_validate(
            {
                "target_kind": "stage_note",
                "stage": "beats",
                "control_id": "stage-note-editor",
                "origin": "workspace",
                "values": {
                    "detail": "Add one calmer beat before the final return home.",
                },
            }
        ),
    )

    assert result.snapshot.current_stage == WorkflowStage.STORY_SETUP
    assert result.snapshot.conversation_memory is not None
    assert (
        "Latest saved UI detail: Beat sheet: Add one calmer beat before the final return home."
        in result.snapshot.conversation_memory.summary_text
    )
    assert any(
        item.startswith("Latest saved UI detail: Beat sheet:")
        for item in result.snapshot.conversation_memory.summary_data.unresolved_questions
    )


def test_eval_composition_interruptions_are_captured_at_checkpoint(db_session) -> None:
    session_service = SessionService(db_session)
    snapshot = session_service.create_session(working_title="Composition Interrupt")

    for stage in (
        WorkflowStage.GENRE,
        WorkflowStage.TONE,
        WorkflowStage.BRIEF,
        WorkflowStage.PITCHES,
        WorkflowStage.CHARACTERS,
        WorkflowStage.BEATS,
        WorkflowStage.STORY_SETUP,
    ):
        session_service.update_stage_state(
            snapshot.id,
            stage=stage,
            status=WorkflowStageState.COMPLETED,
        )

    composition_job = CompositionJob(
        session_id=snapshot.id,
        job_kind=CompositionJobKind.DRAFT,
        status=JobStatus.PAUSED,
        progress_percent=67.0,
        current_segment_index=4,
        stop_reason="User asked for a softer ending before the last chapter.",
    )
    db_session.add(composition_job)
    db_session.flush()

    SessionEventLogService(db_session).record_composition_progress(
        snapshot.id,
        job_id=composition_job.id,
        status=JobStatus.PAUSED,
        progress_percent=67.0,
        current_segment_index=4,
        total_segments=6,
    )
    db_session.commit()

    latest = SessionMemoryService(db_session).load_latest_snapshot(snapshot.id)

    assert latest is not None
    assert (
        "Composition interruption: paused (User asked for a softer ending before the last chapter.)"
        in latest.summary_text
    )
    assert "Composition job: paused at 67.0%, segment 4" in latest.summary_text
    assert latest.trigger_event_type == "composition.progress.recorded"


def test_eval_intent_parser_prompt_uses_durable_memory_summary_sections(db_session) -> None:
    now = datetime.now(timezone.utc)
    session_service = SessionService(db_session)
    snapshot = session_service.create_session(working_title="Prompt Grounding")
    story_session = db_session.get(StorySession, snapshot.id)
    assert story_session is not None

    genre = Genre(
        slug="animal-fable",
        label="Animal Fable",
        description="A gentle story with animal companions.",
    )
    tone = ToneProfile(
        genre=genre,
        slug="cozy-lantern",
        label="Cozy Lantern",
        description="Warm, calm, and bedtime-safe.",
    )
    db_session.add_all([genre, tone])
    db_session.flush()
    story_session.selected_genre = genre
    story_session.selected_tone_profile = tone

    for stage in (
        WorkflowStage.GENRE,
        WorkflowStage.TONE,
        WorkflowStage.BRIEF,
        WorkflowStage.PITCHES,
        WorkflowStage.CHARACTERS,
        WorkflowStage.BEATS,
    ):
        session_service.update_stage_state(
            snapshot.id,
            stage=stage,
            status=WorkflowStageState.COMPLETED,
        )

    brief = StoryBrief(
        session_id=snapshot.id,
        revision_number=1,
        raw_brief="A rabbit courier crosses a lantern path at dusk.",
        normalized_summary="A rabbit courier helps the village settle for sleep.",
        is_active=True,
        accepted_at=now,
    )
    story_setup = StorySetup(
        session_id=snapshot.id,
        revision_number=1,
        target_word_count=1600,
        target_runtime_minutes=10,
        chapter_count=2,
        approximate_scene_count=7,
        guidance_notes="Keep the final page especially still and reassuring.",
        is_selected=True,
        accepted_at=now,
    )
    db_session.add_all([brief, story_setup])
    db_session.flush()

    SessionEventLogService(db_session).record_selection(
        snapshot.id,
        selection_kind=SelectionKind.STORY_SETUP,
        stage=WorkflowStage.STORY_SETUP,
        selection_id=story_setup.id,
        label="Selected story setup",
    )
    db_session.commit()

    session_service.apply_context_update(
        snapshot.id,
        payload=SessionContextUpdateRequest.model_validate(
            {
                "target_kind": "stage_note",
                "stage": "beats",
                "control_id": "stage-note-editor",
                "origin": "workspace",
                "values": {
                    "detail": "Soften the midpoint and add one extra comfort beat.",
                },
            }
        ),
    )

    adapter = StubIntentParserAdapter(
        IntentParserStructuredOutput.model_validate(
            {
                "schema_version": 1,
                "status": "needs_clarification",
                "needs_clarification": True,
                "assistant_response": "Do you want to adjust the beat sheet or the setup?",
                "clarification_reason": "Need the target stage.",
                "proposed_actions": {
                    "schema_version": 1,
                    "actions": [],
                },
            }
        )
    )

    SessionIntentParserService(db_session, adapter).parse_user_message(
        snapshot.id,
        message="make it even gentler",
    )

    assert adapter.invocations
    rendered_prompt = adapter.invocations[0].rendered_prompt
    assert "Story decisions:" in rendered_prompt
    assert "User preferences:" in rendered_prompt
    assert "Unresolved questions:" in rendered_prompt
    assert "Story setup: 1600 words, 10 minutes, 2 chapters, about 7 scenes" in (
        rendered_prompt
    )
    assert "Latest saved UI detail: Beat sheet: Soften the midpoint" in rendered_prompt

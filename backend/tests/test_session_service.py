from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest
from app.db import (
    AssetKind,
    AssetStatus,
    AudioJob,
    Base,
    BeatSheet,
    CharacterSheet,
    CompositionJob,
    CompositionJobKind,
    EventActorType,
    EventLogEntry,
    Genre,
    JobStatus,
    Pitch,
    SessionAsset,
    StoryBrief,
    StorySession,
    StorySetup,
    ToneProfile,
    make_engine,
)
from app.models import (
    BriefNormalizationResult,
    NormalizedBriefPreferences,
    SessionContextUpdateRequest,
    UserEditTargetKind,
    WorkflowStage,
    WorkflowStageState,
)
from app.services.catalog import CATALOG_FILE_PATH, load_catalog_document, seed_catalog
from app.services.sessions import (
    InvalidStageTransitionError,
    SessionNotFoundError,
    SessionService,
    SessionToneSelectionError,
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


def _seed_catalog_rows(db_session) -> None:
    seed_catalog(db_session, load_catalog_document(CATALOG_FILE_PATH))


class StubBriefNormalizationService:
    def __init__(
        self,
        *,
        normalized_summary: str | None = None,
        normalized_preferences: NormalizedBriefPreferences | None = None,
    ) -> None:
        self.calls: list[dict[str, object | None]] = []
        self._normalized_summary = normalized_summary
        self._normalized_preferences = normalized_preferences or NormalizedBriefPreferences(
            protagonist_type="A child and an otter guardian",
            setting="a moonlit harbor",
            emotional_goal="a calm return home",
            constraint_notes=["End with the harbor settled and everyone tucked in."],
            bedtime_safety_concerns=["Keep every surprise quickly reassuring."],
            candidate_motifs=["floating lanterns", "still water"],
        )

    def normalize_brief(self, **kwargs) -> BriefNormalizationResult:
        self.calls.append(kwargs)
        return BriefNormalizationResult(
            source="stub",
            model_id="stub-brief-normalizer",
            prompt_version="brief_normalizer.test",
            normalized_summary=(
                self._normalized_summary
                or "A harbor bedtime quest with a calm lantern-by-lantern reunion."
            ),
            normalized_preferences=self._normalized_preferences,
            raw_response={"stub": True},
        )


def test_create_session_initializes_stage_rows_and_ui_snapshot(db_session) -> None:
    service = SessionService(db_session)

    snapshot = service.create_session(working_title="  Starlight Ferry  ")

    assert snapshot.display_title == "Starlight Ferry"
    assert snapshot.working_title == "Starlight Ferry"
    assert snapshot.current_stage == WorkflowStage.GENRE
    assert snapshot.resume_stage == WorkflowStage.GENRE
    assert snapshot.overall_status == WorkflowStageState.DRAFT
    assert snapshot.progress.total_stages == len(WorkflowStage)
    assert snapshot.progress.completed_stages == 0
    assert [stage.stage for stage in snapshot.stage_states] == list(WorkflowStage)
    assert all(stage.status == WorkflowStageState.DRAFT for stage in snapshot.stage_states)

    stored_session = db_session.get(StorySession, snapshot.id)
    assert stored_session is not None
    assert len(stored_session.workflow_stage_states) == len(WorkflowStage)

    event_rows = (
        db_session.query(EventLogEntry)
        .filter(EventLogEntry.session_id == snapshot.id)
        .order_by(EventLogEntry.sequence_number.asc())
        .all()
    )
    assert len(event_rows) == 1
    assert event_rows[0].sequence_number == 1
    assert event_rows[0].actor_type == EventActorType.USER
    assert event_rows[0].event_type == "session.created"
    assert event_rows[0].payload == {
        "schema_version": 1,
        "working_title": "Starlight Ferry",
    }

    history = service.load_session_history(snapshot.id)
    assert history.latest_sequence_number == 1
    assert len(history.events) == 1
    assert history.events[0].summary == "Created session: Starlight Ferry."
    assert history.events[0].payload is not None
    assert history.events[0].payload.working_title == "Starlight Ferry"


def test_load_session_snapshot_returns_selected_outputs_and_active_jobs(db_session) -> None:
    now = datetime.now(timezone.utc)
    genre = Genre(
        slug="quest-fantasy",
        label="Quest Fantasy",
        description="A gentle adventure.",
    )
    tone = ToneProfile(
        genre=genre,
        slug="hushed-wonder",
        label="Hushed Wonder",
        description="Quiet and luminous.",
        default_planning_hints={"pacing": "unhurried"},
    )
    story_session = StorySession(
        working_title=None,
        current_stage=WorkflowStage.COMPOSITION,
        resume_stage=WorkflowStage.COMPOSITION,
        furthest_completed_stage=WorkflowStage.STORY_SETUP,
        overall_status=WorkflowStageState.IN_PROGRESS,
        selected_genre=genre,
        selected_tone_profile=tone,
    )
    db_session.add(story_session)
    db_session.flush()

    service = SessionService(db_session)
    service.update_stage_state(
        story_session.id,
        stage=WorkflowStage.GENRE,
        status=WorkflowStageState.COMPLETED,
    )
    service.update_stage_state(
        story_session.id,
        stage=WorkflowStage.TONE,
        status=WorkflowStageState.COMPLETED,
    )
    service.update_stage_state(
        story_session.id,
        stage=WorkflowStage.BRIEF,
        status=WorkflowStageState.COMPLETED,
    )
    service.update_stage_state(
        story_session.id,
        stage=WorkflowStage.PITCHES,
        status=WorkflowStageState.COMPLETED,
    )
    service.update_stage_state(
        story_session.id,
        stage=WorkflowStage.CHARACTERS,
        status=WorkflowStageState.COMPLETED,
    )
    service.update_stage_state(
        story_session.id,
        stage=WorkflowStage.BEATS,
        status=WorkflowStageState.COMPLETED,
    )
    service.update_stage_state(
        story_session.id,
        stage=WorkflowStage.STORY_SETUP,
        status=WorkflowStageState.COMPLETED,
    )
    service.update_stage_state(
        story_session.id,
        stage=WorkflowStage.COMPOSITION,
        status=WorkflowStageState.IN_PROGRESS,
        detail="Writing the middle chapters.",
    )

    brief = StoryBrief(
        session_id=story_session.id,
        revision_number=1,
        story_idea="A young fox rows across a moonlit lake.",
        desired_themes="quiet courage, wonder, coming home soothed",
        key_images="moonlit reeds, silver water, a sleeping heron",
        audience_notes="A good fit for children who like gentle nighttime journeys.",
        must_have_elements="The fox should come home feeling calmer than when the story began.",
        raw_brief="A young fox rows across a moonlit lake.",
        normalized_summary="A sleepy quest to find a glowing reed before dawn.",
        normalized_preferences={
            "protagonist_type": "A young fox",
            "setting": "a moonlit lake",
            "emotional_goal": "a calmer return home",
            "constraint_notes": ["The fox should feel calmer by the ending."],
            "bedtime_safety_concerns": ["Keep the lake mystery quickly reassuring."],
            "candidate_motifs": ["glowing reed", "moonlit lake"],
        },
        planning_notes="Keep the tension soft and quickly reparative.",
        is_active=True,
        accepted_at=now,
    )
    db_session.add(brief)
    db_session.flush()

    pitch = Pitch(
        session_id=story_session.id,
        story_brief_id=brief.id,
        generation_key="pitch-batch-1",
        pitch_index=0,
        title="The Reed of Quiet Light",
        logline="A young fox follows the lake's hush toward a night mystery.",
        summary="Pip drifts toward a lantern-bright reed and learns the lake is helping.",
        bedtime_notes="Every surprise resolves gently.",
        is_selected=True,
        accepted_at=now,
    )
    db_session.add(pitch)
    db_session.flush()

    character_sheet = CharacterSheet(
        session_id=story_session.id,
        pitch_id=pitch.id,
        revision_number=1,
        title="Pip and the Listening Lake",
        protagonist_name="Pip",
        summary="Pip is cautious, curious, and calmed by steady rhythms.",
        supporting_cast={"friend": "a sleepy reed-heron"},
        bedtime_notes="Keep Pip emotionally safe in every scene.",
        is_selected=True,
        accepted_at=now,
    )
    db_session.add(character_sheet)
    db_session.flush()

    beat_sheet = BeatSheet(
        session_id=story_session.id,
        character_sheet_id=character_sheet.id,
        revision_number=1,
        summary="A gentle Save-the-Cat arc with a quiet return home.",
        beats={"opening_image": "Moonlight on still water"},
        bedtime_notes="The midpoint should feel magical, not scary.",
        is_selected=True,
        accepted_at=now,
    )
    db_session.add(beat_sheet)
    db_session.flush()

    story_setup = StorySetup(
        session_id=story_session.id,
        beat_sheet_id=beat_sheet.id,
        revision_number=1,
        target_word_count=1800,
        target_runtime_minutes=12,
        chapter_count=3,
        chapter_style="three gentle chapters",
        guidance_notes="Let each chapter end on a calmer image than it began.",
        preferences={"narration_style": "soft"},
        is_selected=True,
        accepted_at=now,
    )
    db_session.add(story_setup)
    db_session.flush()

    composition_job = CompositionJob(
        session_id=story_session.id,
        beat_sheet_id=beat_sheet.id,
        story_setup_id=story_setup.id,
        job_kind=CompositionJobKind.DRAFT,
        status=JobStatus.IN_PROGRESS,
        progress_percent=48.0,
        current_segment_index=2,
    )
    db_session.add(composition_job)
    db_session.flush()

    audio_job = AudioJob(
        session_id=story_session.id,
        source_composition_job_id=composition_job.id,
        status=JobStatus.PAUSED,
        voice_key="gemini-soft-1",
        playback_speed=0.95,
        include_background_music=True,
        music_profile="gentle-piano",
        estimated_duration_seconds=620,
    )
    db_session.add(audio_job)

    story_asset = SessionAsset(
        session_id=story_session.id,
        composition_job_id=composition_job.id,
        asset_kind=AssetKind.STORY_TEXT,
        status=AssetStatus.READY,
        storage_bucket="storyteller-exports",
        object_path="sessions/story-1/story.md",
        mime_type="text/markdown",
        byte_size=4096,
        ready_at=now,
    )
    audio_asset = SessionAsset(
        session_id=story_session.id,
        audio_job_id=audio_job.id,
        asset_kind=AssetKind.FINAL_AUDIO,
        status=AssetStatus.READY,
        storage_bucket="storyteller-exports",
        object_path="sessions/story-1/story.mp3",
        mime_type="audio/mpeg",
        byte_size=8192,
        ready_at=now,
    )
    db_session.add_all([story_asset, audio_asset])
    db_session.commit()

    snapshot = service.load_session_snapshot(story_session.id)

    assert snapshot.display_title == "The Reed of Quiet Light"
    assert snapshot.selected_genre is not None and snapshot.selected_genre.slug == "quest-fantasy"
    assert snapshot.selected_tone_profile is not None
    assert snapshot.story_brief is not None
    assert snapshot.story_brief.story_idea == "A young fox rows across a moonlit lake."
    assert snapshot.story_brief.raw_brief.startswith("A young fox")
    assert snapshot.selected_pitch is not None
    assert snapshot.selected_pitch.title == "The Reed of Quiet Light"
    assert snapshot.selected_character_sheet is not None
    assert snapshot.selected_beat_sheet is not None
    assert snapshot.selected_story_setup is not None
    assert snapshot.latest_composition_job is not None
    assert snapshot.latest_audio_job is not None
    assert snapshot.active_composition_job is not None
    assert snapshot.active_audio_job is not None
    assert snapshot.latest_story_asset is not None
    assert snapshot.latest_audio_asset is not None
    assert snapshot.latest_story_asset.object_path == "sessions/story-1/story.md"
    assert snapshot.latest_audio_asset.object_path == "sessions/story-1/story.mp3"
    assert snapshot.progress.completed_stages == 7
    assert snapshot.progress.in_progress_stages == 1
    assert snapshot.current_stage == WorkflowStage.COMPOSITION
    assert snapshot.agent_context_summary is not None
    assert "Selected genre: Quest Fantasy" in snapshot.agent_context_summary
    assert "Current stage: composition (in_progress)" in snapshot.agent_context_summary
    assert "Story setup: 1800 words, 12 minutes, 3 chapters" in snapshot.agent_context_summary
    composition_stage = next(
        stage for stage in snapshot.stage_states if stage.stage == WorkflowStage.COMPOSITION
    )
    assert composition_stage.detail == "Writing the middle chapters."


def test_update_stage_state_rejects_skipping_prerequisites(db_session) -> None:
    service = SessionService(db_session)
    snapshot = service.create_session(working_title="Stage Guardrails")

    with pytest.raises(InvalidStageTransitionError):
        service.update_stage_state(
            snapshot.id,
            stage=WorkflowStage.TONE,
            status=WorkflowStageState.COMPLETED,
        )


def test_select_genre_persists_catalog_choice_and_advances_to_tone(db_session) -> None:
    _seed_catalog_rows(db_session)
    service = SessionService(db_session)
    snapshot = service.create_session(working_title="Genre First")

    result = service.select_genre(snapshot.id, genre_slug="quest-fantasy")
    updated_snapshot = result.snapshot
    genre_stage = next(
        stage for stage in updated_snapshot.stage_states if stage.stage == WorkflowStage.GENRE
    )

    assert result.event.event_type == "selection.recorded"
    assert result.event.stage == WorkflowStage.GENRE
    assert result.event.payload is not None
    assert result.event.payload.selection_kind == "genre"
    assert result.event.payload.slug == "quest-fantasy"
    assert updated_snapshot.selected_genre is not None
    assert updated_snapshot.selected_genre.slug == "quest-fantasy"
    assert updated_snapshot.current_stage == WorkflowStage.TONE
    assert updated_snapshot.resume_stage == WorkflowStage.TONE
    assert updated_snapshot.overall_status == WorkflowStageState.IN_PROGRESS
    assert genre_stage.status == WorkflowStageState.COMPLETED
    assert genre_stage.detail == (
        "Selected genre: Quest Fantasy. Tone choices filter from this lane next."
    )
    assert genre_stage.last_event_type == "selection.recorded"
    assert genre_stage.last_event_summary == "Selected genre: Quest Fantasy."

    history = service.load_session_history(snapshot.id)
    assert [event.event_type for event in history.events] == [
        "session.created",
        "workflow.stage_changed",
        "selection.recorded",
    ]
    assert history.events[-1].summary == "Selected genre: Quest Fantasy."


def test_select_genre_clears_tone_and_invalidates_later_stages(db_session) -> None:
    _seed_catalog_rows(db_session)
    service = SessionService(db_session)
    snapshot = service.create_session(working_title="Genre Reset")

    first_selection = service.select_genre(snapshot.id, genre_slug="quest-fantasy").snapshot
    tone = db_session.query(ToneProfile).filter(ToneProfile.slug == "hushed-wonder").one()
    story_session = db_session.get(StorySession, snapshot.id)
    assert story_session is not None
    story_session.selected_tone_profile = tone
    db_session.commit()

    service.update_stage_state(
        snapshot.id,
        stage=WorkflowStage.TONE,
        status=WorkflowStageState.COMPLETED,
        detail="Selected tone: Hushed Wonder.",
    )
    service.update_stage_state(
        snapshot.id,
        stage=WorkflowStage.BRIEF,
        status=WorkflowStageState.COMPLETED,
        detail="Accepted normalized brief.",
    )

    result = service.select_genre(snapshot.id, genre_slug="gentle-mystery")
    updated_snapshot = result.snapshot
    stage_map = {stage.stage: stage for stage in updated_snapshot.stage_states}

    assert first_selection.selected_genre is not None
    assert updated_snapshot.selected_genre is not None
    assert updated_snapshot.selected_genre.slug == "gentle-mystery"
    assert updated_snapshot.selected_tone_profile is None
    assert updated_snapshot.current_stage == WorkflowStage.TONE
    assert updated_snapshot.resume_stage == WorkflowStage.TONE
    assert stage_map[WorkflowStage.GENRE].last_event_type == "selection.recorded"
    assert stage_map[WorkflowStage.GENRE].last_event_summary == "Selected genre: Gentle Mystery."
    assert stage_map[WorkflowStage.TONE].status == WorkflowStageState.NEEDS_REGENERATION
    assert stage_map[WorkflowStage.TONE].detail == (
        "Genre changed to Gentle Mystery. Revisit tone and any downstream planning."
    )
    assert stage_map[WorkflowStage.BRIEF].status == WorkflowStageState.NEEDS_REGENERATION

    history = service.load_session_history(snapshot.id)
    assert history.events[-2].event_type == "workflow.stage_changed"
    assert history.events[-2].payload is not None
    assert history.events[-2].payload.invalidated_stages == [
        WorkflowStage.TONE,
        WorkflowStage.BRIEF,
    ]
    assert history.events[-1].summary == "Selected genre: Gentle Mystery."


def test_select_tone_requires_genre_first(db_session) -> None:
    _seed_catalog_rows(db_session)
    service = SessionService(db_session)
    snapshot = service.create_session(working_title="Tone Guardrail")

    with pytest.raises(SessionToneSelectionError, match="select a genre before choosing a tone"):
        service.select_tone(snapshot.id, tone_profile_slug="hushed-wonder")


def test_select_tone_persists_catalog_choice_and_advances_to_brief(db_session) -> None:
    _seed_catalog_rows(db_session)
    service = SessionService(db_session)
    snapshot = service.create_session(working_title="Tone First")
    service.select_genre(snapshot.id, genre_slug="quest-fantasy")

    result = service.select_tone(snapshot.id, tone_profile_slug="hushed-wonder")
    updated_snapshot = result.snapshot
    tone_stage = next(
        stage for stage in updated_snapshot.stage_states if stage.stage == WorkflowStage.TONE
    )

    assert result.event.event_type == "selection.recorded"
    assert result.event.stage == WorkflowStage.TONE
    assert result.event.payload is not None
    assert result.event.payload.selection_kind == "tone_profile"
    assert result.event.payload.slug == "hushed-wonder"
    assert updated_snapshot.selected_tone_profile is not None
    assert updated_snapshot.selected_tone_profile.slug == "hushed-wonder"
    assert updated_snapshot.current_stage == WorkflowStage.BRIEF
    assert updated_snapshot.resume_stage == WorkflowStage.BRIEF
    assert updated_snapshot.overall_status == WorkflowStageState.IN_PROGRESS
    assert tone_stage.status == WorkflowStageState.COMPLETED
    assert tone_stage.detail == (
        "Selected tone: Hushed Wonder. The story brief will inherit this bedtime texture."
    )
    assert tone_stage.last_event_type == "selection.recorded"
    assert tone_stage.last_event_summary == "Selected tone profile: Hushed Wonder."

    history = service.load_session_history(snapshot.id)
    assert [event.event_type for event in history.events] == [
        "session.created",
        "workflow.stage_changed",
        "selection.recorded",
        "workflow.stage_changed",
        "selection.recorded",
    ]
    assert history.events[-1].summary == "Selected tone profile: Hushed Wonder."


def test_select_tone_invalidates_brief_and_later_stages_when_changed(db_session) -> None:
    _seed_catalog_rows(db_session)
    service = SessionService(db_session)
    snapshot = service.create_session(working_title="Tone Reset")

    service.select_genre(snapshot.id, genre_slug="quest-fantasy")
    first_selection = service.select_tone(snapshot.id, tone_profile_slug="hushed-wonder").snapshot
    service.update_stage_state(
        snapshot.id,
        stage=WorkflowStage.BRIEF,
        status=WorkflowStageState.COMPLETED,
        detail="Accepted normalized brief.",
    )

    result = service.select_tone(snapshot.id, tone_profile_slug="lantern-brave")
    updated_snapshot = result.snapshot
    stage_map = {stage.stage: stage for stage in updated_snapshot.stage_states}

    assert first_selection.selected_tone_profile is not None
    assert updated_snapshot.selected_tone_profile is not None
    assert updated_snapshot.selected_tone_profile.slug == "lantern-brave"
    assert updated_snapshot.current_stage == WorkflowStage.BRIEF
    assert updated_snapshot.resume_stage == WorkflowStage.BRIEF
    assert stage_map[WorkflowStage.TONE].status == WorkflowStageState.COMPLETED
    assert stage_map[WorkflowStage.TONE].last_event_type == "selection.recorded"
    assert stage_map[WorkflowStage.TONE].last_event_summary == (
        "Selected tone profile: Lantern Brave."
    )
    assert stage_map[WorkflowStage.BRIEF].status == WorkflowStageState.NEEDS_REGENERATION
    assert stage_map[WorkflowStage.BRIEF].detail == (
        "Tone changed to Lantern Brave. Revisit the brief and any downstream planning."
    )

    history = service.load_session_history(snapshot.id)
    assert history.events[-2].event_type == "workflow.stage_changed"
    assert history.events[-2].payload is not None
    assert history.events[-2].payload.invalidated_stages == [WorkflowStage.BRIEF]
    assert history.events[-1].summary == "Selected tone profile: Lantern Brave."


def test_save_story_brief_persists_revision_and_advances_to_pitches(db_session) -> None:
    _seed_catalog_rows(db_session)
    brief_normalizer = StubBriefNormalizationService()
    service = SessionService(
        db_session,
        brief_normalization_service=brief_normalizer,
    )
    snapshot = service.create_session(working_title="Brief First")
    service.select_genre(snapshot.id, genre_slug="quest-fantasy")
    service.select_tone(snapshot.id, tone_profile_slug="hushed-wonder")

    result = service.save_story_brief(
        snapshot.id,
        story_idea=(
            "A child follows floating lanterns across a harbor and helps a shy otter "
            "guardian bring every light home."
        ),
        desired_themes="gentle bravery, belonging, helping others rest",
        key_images="floating lanterns, moonlit harbor water, otter paws on a skiff rail",
        audience_notes="Best for listeners who want wonder without spooky stakes.",
        must_have_elements="End with the harbor quiet again and the child tucked safely in bed.",
    )

    updated_snapshot = result.snapshot
    brief_stage = next(
        stage for stage in updated_snapshot.stage_states if stage.stage == WorkflowStage.BRIEF
    )

    assert result.event.event_type == "content.user_edit.recorded"
    assert result.event.stage == WorkflowStage.BRIEF
    assert result.event.payload is not None
    assert result.event.payload.target_kind == UserEditTargetKind.STORY_BRIEF
    assert result.event.payload.revision_number == 1
    assert "story_idea" in result.event.payload.changed_fields
    assert updated_snapshot.current_stage == WorkflowStage.PITCHES
    assert updated_snapshot.resume_stage == WorkflowStage.PITCHES
    assert updated_snapshot.story_brief is not None
    assert (
        updated_snapshot.story_brief.story_idea
        == (
            "A child follows floating lanterns across a harbor and helps a shy "
            "otter guardian bring every light home."
        )
    )
    assert updated_snapshot.story_brief.desired_themes == (
        "gentle bravery, belonging, helping others rest"
    )
    assert (
        updated_snapshot.story_brief.normalized_summary
        == "A harbor bedtime quest with a calm lantern-by-lantern reunion."
    )
    assert updated_snapshot.story_brief.normalized_preferences is not None
    assert (
        updated_snapshot.story_brief.normalized_preferences.protagonist_type
        == "A child and an otter guardian"
    )
    assert (
        "Desired themes: gentle bravery, belonging, helping others rest"
        in updated_snapshot.story_brief.raw_brief
    )
    assert brief_stage.status == WorkflowStageState.COMPLETED
    assert brief_stage.detail is not None
    assert brief_stage.detail.startswith("Saved story brief:")
    assert brief_stage.last_event_type == "content.user_edit.recorded"

    stored_briefs = (
        db_session.query(StoryBrief)
        .filter(StoryBrief.session_id == snapshot.id)
        .order_by(StoryBrief.revision_number.asc())
        .all()
    )
    assert len(stored_briefs) == 1
    assert stored_briefs[0].is_active is True
    assert stored_briefs[0].normalized_preferences is not None
    assert brief_normalizer.calls[0]["raw_brief"] == stored_briefs[0].raw_brief

    history = service.load_session_history(snapshot.id)
    assert history.events[-2].event_type == "workflow.stage_changed"
    assert history.events[-1].event_type == "content.user_edit.recorded"


def test_save_story_brief_creates_new_revision_and_invalidates_later_stages(
    db_session,
) -> None:
    _seed_catalog_rows(db_session)
    service = SessionService(
        db_session,
        brief_normalization_service=StubBriefNormalizationService(),
    )
    snapshot = service.create_session(working_title="Brief Reset")
    service.select_genre(snapshot.id, genre_slug="quest-fantasy")
    service.select_tone(snapshot.id, tone_profile_slug="hushed-wonder")
    service.save_story_brief(
        snapshot.id,
        story_idea="A harbor child follows lanterns into the fog and returns home calm.",
        desired_themes="curiosity, trust, quiet courage",
    )
    service.update_stage_state(
        snapshot.id,
        stage=WorkflowStage.PITCHES,
        status=WorkflowStageState.COMPLETED,
        detail="Accepted the lantern harbor pitch.",
    )
    service.update_stage_state(
        snapshot.id,
        stage=WorkflowStage.CHARACTERS,
        status=WorkflowStageState.COMPLETED,
        detail="Locked the child and otter cast sheet.",
    )

    result = service.save_story_brief(
        snapshot.id,
        story_idea=(
            "A harbor child and an otter guide lanterns home before the moon "
            "slips behind the clouds."
        ),
        must_have_elements="Keep the ending tucked-in, quiet, and emotionally repaired.",
    )

    updated_snapshot = result.snapshot
    stage_map = {stage.stage: stage for stage in updated_snapshot.stage_states}
    stored_briefs = (
        db_session.query(StoryBrief)
        .filter(StoryBrief.session_id == snapshot.id)
        .order_by(StoryBrief.revision_number.asc())
        .all()
    )

    assert len(stored_briefs) == 2
    assert stored_briefs[0].is_active is False
    assert stored_briefs[1].is_active is True
    assert stored_briefs[1].revision_number == 2
    assert updated_snapshot.current_stage == WorkflowStage.PITCHES
    assert updated_snapshot.resume_stage == WorkflowStage.PITCHES
    assert updated_snapshot.overall_status == WorkflowStageState.NEEDS_REGENERATION
    assert stage_map[WorkflowStage.BRIEF].status == WorkflowStageState.COMPLETED
    assert stage_map[WorkflowStage.PITCHES].status == WorkflowStageState.NEEDS_REGENERATION
    assert stage_map[WorkflowStage.PITCHES].detail == (
        "Story brief changed. Refresh pitches and any downstream planning."
    )
    assert stage_map[WorkflowStage.CHARACTERS].status == WorkflowStageState.NEEDS_REGENERATION

    history = service.load_session_history(snapshot.id)
    assert history.events[-2].event_type == "workflow.stage_changed"
    assert history.events[-2].payload is not None
    assert history.events[-2].payload.invalidated_stages == [
        WorkflowStage.PITCHES,
        WorkflowStage.CHARACTERS,
    ]
    assert history.events[-1].payload is not None
    assert history.events[-1].payload.revision_number == 2


def test_save_story_brief_accepts_manual_normalization_overrides(db_session) -> None:
    _seed_catalog_rows(db_session)
    brief_normalizer = StubBriefNormalizationService()
    service = SessionService(
        db_session,
        brief_normalization_service=brief_normalizer,
    )
    snapshot = service.create_session(working_title="Brief Override")
    service.select_genre(snapshot.id, genre_slug="quest-fantasy")
    service.select_tone(snapshot.id, tone_profile_slug="hushed-wonder")

    manual_preferences = NormalizedBriefPreferences(
        protagonist_type="A child and an otter guardian",
        setting="a lantern-washed harbor",
        emotional_goal="a calm reunion before sleep",
        constraint_notes=["Keep the ending tucked-in and emotionally repaired."],
        bedtime_safety_concerns=["Avoid any threatening separation beats."],
        candidate_motifs=["floating lanterns", "otter paws", "quiet docks"],
    )

    result = service.save_story_brief(
        snapshot.id,
        story_idea="A child and an otter guardian guide runaway lanterns back across the harbor.",
        normalized_summary="A lantern-lit bedtime harbor story with a clearly reassuring reunion.",
        normalized_preferences=manual_preferences,
        provided_fields={"story_idea", "normalized_summary", "normalized_preferences"},
    )

    assert result.snapshot.story_brief is not None
    assert (
        result.snapshot.story_brief.normalized_summary
        == "A lantern-lit bedtime harbor story with a clearly reassuring reunion."
    )
    assert result.snapshot.story_brief.normalized_preferences == manual_preferences

    stored_brief = (
        db_session.query(StoryBrief)
        .filter(StoryBrief.session_id == snapshot.id, StoryBrief.is_active.is_(True))
        .one()
    )
    assert stored_brief.model_output["normalization_source"] == "stub_with_user_overrides"
    assert stored_brief.normalized_preferences == manual_preferences.model_dump(mode="json")


def test_save_story_brief_rejects_skipping_tone_prerequisite(db_session) -> None:
    _seed_catalog_rows(db_session)
    service = SessionService(db_session)
    snapshot = service.create_session(working_title="Brief Guardrail")
    service.select_genre(snapshot.id, genre_slug="quest-fantasy")

    with pytest.raises(InvalidStageTransitionError):
        service.save_story_brief(
            snapshot.id,
            story_idea="A sleepy harbor lantern story.",
        )


def test_refine_pitch_creates_a_linked_selected_revision_without_overwriting_history(
    db_session,
) -> None:
    _seed_catalog_rows(db_session)
    service = SessionService(
        db_session,
        brief_normalization_service=StubBriefNormalizationService(),
    )
    snapshot = service.create_session(working_title="Pitch Refinement")
    service.select_genre(snapshot.id, genre_slug="quest-fantasy")
    service.select_tone(snapshot.id, tone_profile_slug="hushed-wonder")
    service.save_story_brief(
        snapshot.id,
        story_idea=(
            "A child and an otter guardian follow floating lanterns across a harbor "
            "before bed."
        ),
    )
    generated = service.generate_pitches(
        snapshot.id,
        candidate_count=3,
        guidance="Keep the harbor mystery very gentle.",
    )
    source_pitch = generated.snapshot.pitch_batches[0].pitches[1]

    result = service.refine_pitch(
        snapshot.id,
        pitch_id=source_pitch.id,
        instructions="Make it about siblings who help each other settle down.",
    )

    assert result.snapshot.current_stage == WorkflowStage.CHARACTERS
    assert result.snapshot.resume_stage == WorkflowStage.CHARACTERS
    assert result.snapshot.selected_pitch is not None
    assert result.snapshot.selected_pitch.id != source_pitch.id
    assert result.snapshot.selected_pitch.generation_kind == "refinement"
    assert result.snapshot.selected_pitch.source_pitch_id == source_pitch.id
    assert result.snapshot.selected_pitch.source_pitch_title == source_pitch.title
    assert (
        result.snapshot.selected_pitch.refinement_instructions
        == "Make it about siblings who help each other settle down."
    )
    assert "Refined from" in (result.snapshot.selected_pitch.selection_rationale or "")
    assert result.snapshot.pitch_batches[0].generation_kind == "refinement"
    assert result.snapshot.pitch_batches[0].candidate_count == 1
    assert result.snapshot.pitch_batches[0].source_pitch_title == source_pitch.title
    assert len(result.snapshot.pitch_batches) == 2
    assert result.event.payload is not None
    assert result.event.payload.rationale is not None
    assert source_pitch.title in result.event.payload.rationale

    history = service.load_session_history(snapshot.id)
    assert history.events[-2].event_type == "ai.output.recorded"
    assert history.events[-1].event_type == "selection.recorded"


def test_update_stage_state_records_event_history_and_stage_last_event(db_session) -> None:
    service = SessionService(db_session)
    snapshot = service.create_session(working_title="Timeline Check")

    snapshot = service.update_stage_state(
        snapshot.id,
        stage=WorkflowStage.GENRE,
        status=WorkflowStageState.COMPLETED,
        detail="Accepted quest fantasy.",
    )

    history = service.load_session_history(snapshot.id)
    assert [event.event_type for event in history.events] == [
        "session.created",
        "workflow.stage_changed",
    ]
    assert history.latest_sequence_number == 2

    stage_event = history.events[-1]
    assert stage_event.stage == WorkflowStage.GENRE
    assert stage_event.payload is not None
    assert stage_event.payload.previous_status == WorkflowStageState.DRAFT
    assert stage_event.payload.status == WorkflowStageState.COMPLETED
    assert stage_event.payload.detail == "Accepted quest fantasy."
    assert stage_event.payload.invalidated_stages == []
    assert stage_event.payload.resume_stage == WorkflowStage.TONE

    genre_stage = next(
        stage for stage in snapshot.stage_states if stage.stage == WorkflowStage.GENRE
    )
    assert genre_stage.last_event_type == "workflow.stage_changed"
    assert genre_stage.last_event_summary == "Updated genre stage to completed."


def test_record_ui_action_persists_a_history_entry(db_session) -> None:
    service = SessionService(db_session)
    snapshot = service.create_session(working_title="Action Echoes")

    event = service.record_ui_action(
        snapshot.id,
        action="navigate_to_stage",
        stage=WorkflowStage.AUDIO,
        control_id="stage-navigator",
        value_summary="Audio",
        origin="workspace",
    )

    assert event.event_type == "ui.action.recorded"
    assert event.stage == WorkflowStage.AUDIO
    assert event.payload is not None
    assert event.payload.action == "navigate_to_stage"
    assert event.payload.control_id == "stage-navigator"
    assert event.payload.value_summary == "Audio"
    assert event.payload.origin == "workspace"

    history = service.load_session_history(snapshot.id)
    assert history.latest_sequence_number == 2
    assert history.events[-1].event_type == "ui.action.recorded"


def test_apply_context_update_persists_stage_note_and_invalidates_dependents(db_session) -> None:
    service = SessionService(db_session)
    snapshot = service.create_session(working_title="UI Context")

    for stage in (
        WorkflowStage.GENRE,
        WorkflowStage.TONE,
        WorkflowStage.BRIEF,
        WorkflowStage.PITCHES,
        WorkflowStage.CHARACTERS,
        WorkflowStage.BEATS,
        WorkflowStage.STORY_SETUP,
        WorkflowStage.COMPOSITION,
        WorkflowStage.AUDIO,
    ):
        snapshot = service.update_stage_state(
            snapshot.id,
            stage=stage,
            status=WorkflowStageState.COMPLETED,
            detail=f"Accepted {stage.value}.",
        )

    result = service.apply_context_update(
        snapshot.id,
        payload=SessionContextUpdateRequest.model_validate(
            {
                "target_kind": "stage_note",
                "stage": "beats",
                "control_id": "stage-note-editor",
                "origin": "workspace",
                "values": {
                    "detail": "Soften the midpoint and let the return home land faster.",
                },
            }
        ),
    )

    updated_snapshot = result.snapshot
    stage_map = {stage.stage: stage for stage in updated_snapshot.stage_states}

    assert result.event.event_type == "content.user_edit.recorded"
    assert result.event.stage == WorkflowStage.BEATS
    assert result.event.payload is not None
    assert result.event.payload.changed_fields == ["detail"]
    assert result.event.payload.field_values == {
        "detail": "Soften the midpoint and let the return home land faster.",
        "control_id": "stage-note-editor",
    }
    assert result.event.payload.summary_text == "Updated beat sheet notes from the workspace."
    assert stage_map[WorkflowStage.BEATS].detail == (
        "Soften the midpoint and let the return home land faster."
    )
    assert stage_map[WorkflowStage.BEATS].last_event_type == "content.user_edit.recorded"
    assert stage_map[WorkflowStage.COMPOSITION].status == WorkflowStageState.NEEDS_REGENERATION
    assert stage_map[WorkflowStage.AUDIO].status == WorkflowStageState.NEEDS_REGENERATION
    assert stage_map[WorkflowStage.FINALIZE].status == WorkflowStageState.DRAFT
    assert stage_map[WorkflowStage.COMPOSITION].last_event_type == "workflow.stage_changed"
    assert updated_snapshot.overall_status == WorkflowStageState.NEEDS_REGENERATION
    assert updated_snapshot.agent_context_summary is not None
    assert "Latest saved UI detail: Beat sheet: Soften the midpoint" in (
        updated_snapshot.agent_context_summary
    )
    assert "Needs regeneration: Composition, Audio" in updated_snapshot.agent_context_summary

    history = service.load_session_history(snapshot.id)
    assert history.latest_sequence_number == 12
    assert history.events[-2].event_type == "workflow.stage_changed"
    assert history.events[-1].event_type == "content.user_edit.recorded"


def test_update_stage_state_invalidates_downstream_outputs_after_upstream_edit(db_session) -> None:
    service = SessionService(db_session)
    snapshot = service.create_session(working_title="Regeneration Test")

    for stage in (
        WorkflowStage.GENRE,
        WorkflowStage.TONE,
        WorkflowStage.BRIEF,
        WorkflowStage.PITCHES,
        WorkflowStage.CHARACTERS,
        WorkflowStage.BEATS,
        WorkflowStage.STORY_SETUP,
        WorkflowStage.COMPOSITION,
        WorkflowStage.AUDIO,
        WorkflowStage.FINALIZE,
    ):
        snapshot = service.update_stage_state(
            snapshot.id,
            stage=stage,
            status=WorkflowStageState.COMPLETED,
            detail=f"Accepted {stage.value}.",
        )

    assert snapshot.overall_status == WorkflowStageState.COMPLETED
    assert snapshot.resume_stage == WorkflowStage.FINALIZE

    snapshot = service.update_stage_state(
        snapshot.id,
        stage=WorkflowStage.BRIEF,
        status=WorkflowStageState.COMPLETED,
        detail="Accepted a revised brief.",
    )

    stage_map = {stage.stage: stage for stage in snapshot.stage_states}
    assert snapshot.current_stage == WorkflowStage.PITCHES
    assert snapshot.resume_stage == WorkflowStage.PITCHES
    assert snapshot.furthest_completed_stage == WorkflowStage.STORY_SETUP
    assert snapshot.overall_status == WorkflowStageState.NEEDS_REGENERATION
    assert snapshot.completed_at is None
    assert stage_map[WorkflowStage.BRIEF].status == WorkflowStageState.COMPLETED
    assert stage_map[WorkflowStage.PITCHES].status == WorkflowStageState.NEEDS_REGENERATION
    assert stage_map[WorkflowStage.STORY_SETUP].status == WorkflowStageState.COMPLETED
    assert stage_map[WorkflowStage.COMPOSITION].status == WorkflowStageState.NEEDS_REGENERATION
    assert stage_map[WorkflowStage.FINALIZE].status == WorkflowStageState.NEEDS_REGENERATION
    assert stage_map[WorkflowStage.PITCHES].detail == "Accepted a revised brief."
    assert stage_map[WorkflowStage.PITCHES].last_event_type == "workflow.stage_changed"
    assert "invalidated pitches" in stage_map[WorkflowStage.BRIEF].last_event_summary
    assert "invalidated pitches" in stage_map[WorkflowStage.PITCHES].last_event_summary


def test_list_recent_sessions_returns_latest_first_with_progress_counts(db_session) -> None:
    service = SessionService(db_session)
    older = service.create_session(working_title="Older Session")
    newer = service.create_session(working_title="Newer Session")

    older_row = db_session.get(StorySession, older.id)
    newer_row = db_session.get(StorySession, newer.id)
    assert older_row is not None and newer_row is not None

    older_row.updated_at = datetime.now(timezone.utc) - timedelta(days=1)
    newer_row.updated_at = datetime.now(timezone.utc)
    db_session.commit()

    service.update_stage_state(
        newer.id,
        stage=WorkflowStage.GENRE,
        status=WorkflowStageState.COMPLETED,
    )
    recent = service.list_recent_sessions(limit=5)

    assert [session.id for session in recent[:2]] == [newer.id, older.id]
    assert recent[0].progress.completed_stages == 1
    assert recent[1].progress.completed_stages == 0


def test_load_session_snapshot_raises_for_missing_session(db_session) -> None:
    service = SessionService(db_session)

    with pytest.raises(SessionNotFoundError):
        service.load_session_snapshot("missing-session-id")


def test_load_session_history_raises_for_missing_session(db_session) -> None:
    service = SessionService(db_session)

    with pytest.raises(SessionNotFoundError):
        service.load_session_history("missing-session-id")

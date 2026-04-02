from __future__ import annotations

from datetime import datetime, timezone

import pytest
from app.db import Base, BeatSheet, make_engine
from app.models import (
    BeatSheetEvaluation,
    BeatSheetEvaluationCriterion,
    BeatSheetGenerationResult,
    EditSessionBeatSheetRequest,
    ExistingSelectedPitchContext,
    GeneratedBeatSheetBeat,
    GeneratedBeatSheetCandidate,
    NormalizedBriefPreferences,
    WorkflowStage,
    WorkflowStageState,
)
from app.services.catalog import CATALOG_FILE_PATH, load_catalog_document, seed_catalog
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


class StubBeatSheetGenerationService:
    def __init__(self) -> None:
        self.calls: list[dict[str, object | None]] = []

    def generate_beat_sheet(self, **kwargs) -> BeatSheetGenerationResult:
        self.calls.append(kwargs)
        beats = [
            GeneratedBeatSheetBeat(
                key=key,
                label=label,
                summary=f"{label} keeps the harbor plan high level and concrete.",
                emotional_intent=f"{label} should feel calm and emotionally legible.",
                bedtime_softening_note=(
                    f"{label} stays bedtime-safe by keeping tension readable and quickly soothed."
                ),
            )
            for key, label in (
                ("opening_image", "Opening Image"),
                ("theme_stated", "Theme Stated"),
                ("set_up", "Set-Up"),
                ("catalyst", "Catalyst"),
                ("debate", "Debate"),
                ("break_into_two", "Break into Two"),
                ("b_story", "B Story"),
                ("fun_and_games", "Fun and Games"),
                ("midpoint", "Midpoint"),
                ("bad_guys_close_in", "Bad Guys Close In"),
                ("all_is_lost", "All Is Lost"),
                ("dark_night_of_the_soul", "Dark Night of the Soul"),
                ("break_into_three", "Break into Three"),
                ("finale", "Finale"),
                ("final_image", "Final Image"),
            )
        ]
        return BeatSheetGenerationResult(
            source="stub",
            model_id="stub-beat-generator",
            prompt_version="beat_sheet_generation.test",
            beat_sheet=GeneratedBeatSheetCandidate(
                summary="A harbor Save-the-Cat arc that lands in calm belonging.",
                bedtime_notes="Keep every pressure beat quickly buffered by warmth and visibility.",
                beats=beats,
            ),
            evaluation=BeatSheetEvaluation(
                passed=True,
                criteria=[
                    BeatSheetEvaluationCriterion(
                        name="all_required_beats_present",
                        passed=True,
                        measured_value=15,
                    )
                ],
            ),
            raw_response={"stub": True},
        )


def _seed_catalog_rows(db_session) -> None:
    seed_catalog(db_session, load_catalog_document(CATALOG_FILE_PATH))


def _create_character_ready_session(db_session):
    service = SessionService(db_session)
    snapshot = service.create_session(working_title="Beat Sheet Stage")
    service.select_genre(snapshot.id, genre_slug="quest-fantasy")
    service.select_tone(snapshot.id, tone_profile_slug="hushed-wonder")
    service.save_story_brief(
        snapshot.id,
        story_idea="A child and an otter guardian follow floating lanterns across a harbor before bed.",
        normalized_preferences=NormalizedBriefPreferences(
            protagonist_type="A child and an otter guardian",
            setting="a moonlit harbor",
            emotional_goal="a calm return home",
            constraint_notes=["End with the harbor settled and safe."],
            bedtime_safety_concerns=["Keep every surprise quickly reassuring."],
            candidate_motifs=["floating lanterns", "moonlit docks"],
        ),
    )
    generated_pitches = service.generate_pitches(snapshot.id, candidate_count=3)
    service.select_pitch(
        snapshot.id,
        pitch_id=generated_pitches.snapshot.pitch_batches[0].pitches[0].id,
    )
    generated_characters = service.generate_character_sheets(snapshot.id, candidate_count=3)
    service.select_character_sheet(
        snapshot.id,
        character_sheet_id=generated_characters.snapshot.character_sheet_batches[0].character_sheets[0].id,
    )
    return service, snapshot.id


def test_generate_beat_sheet_persists_revisioned_candidate_and_keeps_stage_active(
    db_session,
) -> None:
    _seed_catalog_rows(db_session)
    service, session_id = _create_character_ready_session(db_session)
    beat_generator = StubBeatSheetGenerationService()

    result = service.generate_beat_sheet(
        session_id,
        guidance="Keep the midpoint more awestruck than tense.",
        focus_beats=["midpoint"],
        bedtime_goal="feel sleepy and safe by the ending",
        beat_sheet_generation_service=beat_generator,
    )

    assert result.event.event_type == "ai.output.recorded"
    assert result.snapshot.current_stage == WorkflowStage.BEATS
    assert result.snapshot.resume_stage == WorkflowStage.BEATS
    assert result.snapshot.selected_beat_sheet is None
    assert result.snapshot.beat_sheet_revisions[0].summary == (
        "A harbor Save-the-Cat arc that lands in calm belonging."
    )
    assert len(result.snapshot.beat_sheet_revisions[0].beats) == 15
    assert result.snapshot.stage_states[5].status == WorkflowStageState.IN_PROGRESS
    assert "Accept a revision to continue." in (result.snapshot.stage_states[5].detail or "")
    assert beat_generator.calls[0]["guidance"] == "Keep the midpoint more awestruck than tense."


def test_select_beat_sheet_marks_choice_and_advances_to_story_setup(db_session) -> None:
    _seed_catalog_rows(db_session)
    service, session_id = _create_character_ready_session(db_session)
    generated = service.generate_beat_sheet(
        session_id,
        beat_sheet_generation_service=StubBeatSheetGenerationService(),
    )
    first_revision = generated.snapshot.beat_sheet_revisions[0]

    result = service.select_beat_sheet(
        session_id,
        beat_sheet_id=first_revision.id,
    )

    assert result.event.event_type == "selection.recorded"
    assert result.event.payload is not None
    assert result.event.payload.selection_kind == "beat_sheet"
    assert result.snapshot.current_stage == WorkflowStage.STORY_SETUP
    assert result.snapshot.resume_stage == WorkflowStage.STORY_SETUP
    assert result.snapshot.selected_beat_sheet is not None
    assert result.snapshot.selected_beat_sheet.id == first_revision.id
    assert result.snapshot.selected_beat_sheet.is_selected is True
    assert result.snapshot.stage_states[5].status == WorkflowStageState.COMPLETED


def test_refine_beat_sheet_creates_selected_revision_and_invalidates_composition(
    db_session,
) -> None:
    _seed_catalog_rows(db_session)
    service, session_id = _create_character_ready_session(db_session)
    generated = service.generate_beat_sheet(
        session_id,
        beat_sheet_generation_service=StubBeatSheetGenerationService(),
    )
    selected = service.select_beat_sheet(
        session_id,
        beat_sheet_id=generated.snapshot.beat_sheet_revisions[0].id,
    )
    service.update_stage_state(
        session_id,
        stage=WorkflowStage.STORY_SETUP,
        status=WorkflowStageState.COMPLETED,
        detail="Accepted setup.",
    )
    service.update_stage_state(
        session_id,
        stage=WorkflowStage.COMPOSITION,
        status=WorkflowStageState.COMPLETED,
        detail="Drafted story text.",
    )

    result = service.refine_beat_sheet(
        session_id,
        revision_number=selected.snapshot.selected_beat_sheet.revision_number,
        instructions="Soften the midpoint and all-is-lost beats.",
        beat_names=["midpoint", "all_is_lost"],
        bedtime_goal="settle into a visibly sleepy ending",
        beat_sheet_generation_service=StubBeatSheetGenerationService(),
    )

    refreshed_beat_sheets = db_session.query(BeatSheet).filter(BeatSheet.session_id == session_id).all()
    assert len(refreshed_beat_sheets) == 2
    assert result.snapshot.selected_beat_sheet is not None
    assert result.snapshot.selected_beat_sheet.revision_number == 2
    assert result.snapshot.stage_states[5].status == WorkflowStageState.COMPLETED
    assert result.snapshot.stage_states[7].status == WorkflowStageState.NEEDS_REGENERATION
    assert result.snapshot.stage_states[8].status == WorkflowStageState.DRAFT


def test_edit_selected_beat_sheet_updates_in_place_and_tracks_history(db_session) -> None:
    _seed_catalog_rows(db_session)
    service, session_id = _create_character_ready_session(db_session)
    generated = service.generate_beat_sheet(
        session_id,
        beat_sheet_generation_service=StubBeatSheetGenerationService(),
    )
    selected = service.select_beat_sheet(
        session_id,
        beat_sheet_id=generated.snapshot.beat_sheet_revisions[0].id,
    )
    service.update_stage_state(
        session_id,
        stage=WorkflowStage.STORY_SETUP,
        status=WorkflowStageState.COMPLETED,
        detail="Accepted setup.",
    )
    service.update_stage_state(
        session_id,
        stage=WorkflowStage.COMPOSITION,
        status=WorkflowStageState.COMPLETED,
        detail="Drafted story text.",
    )

    result = service.edit_beat_sheet(
        session_id,
        payload=EditSessionBeatSheetRequest.model_validate(
            {
                "beat_sheet_id": selected.snapshot.selected_beat_sheet.id,
                "summary": "A harbor arc with a more wondrous midpoint and softer late turn.",
                "bedtime_goal": "Let the harbor settle into an even sleepier ending.",
                "beat_updates": [
                    {
                        "key": "midpoint",
                        "summary": (
                            "The midpoint becomes a lantern-halo moment that swaps urgency for awe."
                        ),
                        "emotional_intent": (
                            "Let the midpoint feel gently revelatory instead of tense."
                        ),
                    }
                ],
                "origin": "workspace",
            }
        ),
    )

    refreshed_beat_sheets = (
        db_session.query(BeatSheet).filter(BeatSheet.session_id == session_id).all()
    )
    assert len(refreshed_beat_sheets) == 1
    assert result.event.event_type == "content.user_edit.recorded"
    assert result.snapshot.selected_beat_sheet is not None
    assert result.snapshot.selected_beat_sheet.revision_number == 1
    assert (
        result.snapshot.selected_beat_sheet.summary
        == "A harbor arc with a more wondrous midpoint and softer late turn."
    )
    midpoint = next(
        beat for beat in result.snapshot.selected_beat_sheet.beats if beat.key == "midpoint"
    )
    assert midpoint.summary == "The midpoint becomes a lantern-halo moment that swaps urgency for awe."
    assert (
        midpoint.emotional_intent
        == "Let the midpoint feel gently revelatory instead of tense."
    )
    assert result.snapshot.selected_beat_sheet.edit_history[0].material_change is True
    assert result.snapshot.selected_beat_sheet.edit_history[0].refreshes_downstream is True
    assert result.snapshot.stage_states[6].status == WorkflowStageState.NEEDS_REGENERATION
    assert result.snapshot.stage_states[7].status == WorkflowStageState.NEEDS_REGENERATION
    assert "Story setup and composition need refresh." in (
        result.snapshot.selected_beat_sheet.edit_history[0].summary_text
    )

from __future__ import annotations

from datetime import datetime, timezone

import pytest
from app.db import (
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
    StoryOutline,
    StorySession,
    StorySetup,
    ToneProfile,
    make_engine,
)
from app.models import ContinuityBibleData, ContinuityFactCategory, WorkflowStage
from app.models.workflow import WorkflowStageState
from app.services.continuity import SessionContinuityService
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


def _seed_continuity_session(db_session) -> str:
    now = datetime.now(timezone.utc)
    session_service = SessionService(db_session)
    snapshot = session_service.create_session(working_title="Continuity Harbor")

    genre = Genre(
        slug="quest-fantasy",
        label="Quest Fantasy",
        description="A bedtime-safe harbor adventure.",
    )
    tone = ToneProfile(
        genre=genre,
        slug="hushed-wonder",
        label="Hushed Wonder",
        description="Soft and luminous.",
        bedtime_notes="Keep every turn reassuring and visibly safe.",
    )
    db_session.add_all([genre, tone])
    db_session.flush()

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
        session_service.update_stage_state(
            snapshot.id,
            stage=stage,
            status=WorkflowStageState.COMPLETED,
        )

    brief = StoryBrief(
        session_id=snapshot.id,
        revision_number=1,
        story_idea="Mira follows a drifting harbor bell and helps one last lantern home.",
        key_images="silver bell, lantern light, moonlit docks",
        must_have_elements="End with the harbor tucked in and the bell resting safely.",
        raw_brief="Mira follows a drifting harbor bell and helps one last lantern home.",
        normalized_summary="A gentle harbor mystery that returns everyone safely to rest.",
        normalized_preferences={
            "setting": "Juniper Harbor",
            "constraint_notes": [
                "Keep every surprise small and quickly buffered by companionship."
            ],
            "bedtime_safety_concerns": [
                "Let the harbor stay readable even when the bell drifts away."
            ],
            "candidate_motifs": ["silver bell", "lantern map"],
        },
        planning_notes="Keep the midpoint awestruck instead of sharp.",
        is_active=True,
        accepted_at=now,
    )
    db_session.add(brief)
    db_session.flush()

    pitch = Pitch(
        session_id=snapshot.id,
        story_brief_id=brief.id,
        generation_key="pitch-batch-1",
        pitch_index=0,
        title="The Last Bell Before Sleep",
        logline="Mira follows a silver harbor bell to guide one last lantern home.",
        summary=(
            "Mira wants the harbor to settle before dawn, but the drifting bell "
            "keeps calling her onward."
        ),
        bedtime_notes="Let every clue feel inviting, not alarming.",
        is_selected=True,
        accepted_at=now,
    )
    db_session.add(pitch)
    db_session.flush()

    character_sheet = CharacterSheet(
        session_id=snapshot.id,
        pitch_id=pitch.id,
        revision_number=1,
        title="Mira and Pip",
        protagonist_name="Mira",
        summary="Mira and Pip keep the harbor gentle even when the bell drifts away.",
        character_data={
            "candidate": {
                "protagonist": {
                    "name": "Mira",
                    "role": "Harbor child",
                    "goal": "Guide the last lantern home before the docks grow still.",
                    "flaw": "Tries to solve every problem alone first.",
                    "comfort_trait": "Counts lantern reflections when she needs to settle.",
                    "relationships": ["Trusts Pip to steady the plan."],
                    "visual_anchors": ["knit harbor coat", "lantern satchel"],
                },
                "supporting_cast": [
                    {
                        "name": "Pip",
                        "role": "Otter guardian",
                        "goal": "Keep Mira company and make every clue feel safe.",
                        "flaw": "Overexplains when he worries.",
                        "comfort_trait": "Hums softly before speaking.",
                        "relationships": ["Promises Mira she will not face the harbor alone."],
                        "visual_anchors": ["bell rope", "river-stone pendant"],
                    }
                ],
                "visual_motifs": ["lantern map", "silver bell"],
            }
        },
        is_selected=True,
        accepted_at=now,
    )
    db_session.add(character_sheet)
    db_session.flush()

    beat_sheet = BeatSheet(
        session_id=snapshot.id,
        character_sheet_id=character_sheet.id,
        revision_number=1,
        summary="A soft Save-the-Cat arc that lets Mira guide the harbor back into rest.",
        bedtime_notes="Keep the low point brief and immediately held by companionship.",
        beats={
            "bedtime_goal": "Land in a visibly sleepy harbor ending.",
            "beats": [
                {
                    "key": "catalyst",
                    "label": "Catalyst",
                    "summary": "The silver bell drifts away from its lantern post.",
                },
                {
                    "key": "midpoint",
                    "label": "Midpoint",
                    "summary": "Mira discovers the bell is guiding one last lantern toward home.",
                },
                {
                    "key": "all_is_lost",
                    "label": "All Is Lost",
                    "summary": (
                        "The bell goes quiet and Mira worries she has guided the lantern "
                        "wrong."
                    ),
                },
            ],
        },
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
        approximate_scene_count=8,
        chapter_style="three gentle chapters",
        guidance_notes="End each chapter on a calmer harbor image than it began.",
        is_selected=True,
        accepted_at=now,
    )
    db_session.add(story_setup)
    db_session.flush()

    story_outline = StoryOutline(
        session_id=snapshot.id,
        beat_sheet_id=beat_sheet.id,
        story_setup_id=story_setup.id,
        revision_number=1,
        outline_kind="chapter",
        summary="Three chapter cards carry the harbor bell from drift to rest.",
        cards=[
            {
                "card_key": "chapter-1",
                "position": 1,
                "title": "Chapter 1: Bell on the Water",
                "summary": "Mira notices the bell drifting and chooses to help it.",
                "bedtime_guardrail": "Keep the harbor readable and warmly lit.",
            },
            {
                "card_key": "chapter-2",
                "position": 2,
                "title": "Chapter 2: Lantern Map",
                "summary": "Mira and Pip follow the bell to the lantern's quiet destination.",
                "bedtime_guardrail": "Let wonder rise without making the harbor feel unsafe.",
            },
        ],
        is_selected=True,
        accepted_at=now,
    )
    db_session.add(story_outline)
    db_session.flush()

    composition_job = CompositionJob(
        session_id=snapshot.id,
        beat_sheet_id=beat_sheet.id,
        story_setup_id=story_setup.id,
        job_kind=CompositionJobKind.DRAFT,
        status=JobStatus.COMPLETED,
        progress_percent=100,
        current_segment_index=1,
        started_at=now,
        completed_at=now,
    )
    db_session.add(composition_job)
    db_session.flush()

    db_session.add(
        CompositionSegment(
            session_id=snapshot.id,
            composition_job_id=composition_job.id,
            segment_index=1,
            revision_number=1,
            status=JobStatus.COMPLETED,
            planned_summary="Mira promises Pip that no lantern will drift alone tonight.",
            text_content="Mira promised Pip that no lantern would drift alone tonight.",
            payload={"outline_card_title": "Chapter 1: Bell on the Water"},
            completed_at=now,
        )
    )
    db_session.commit()
    return snapshot.id


def test_refresh_for_session_creates_selected_revision_from_canonical_story_state(
    db_session,
) -> None:
    session_id = _seed_continuity_session(db_session)

    row = SessionContinuityService(db_session).refresh_for_session(
        session_id,
        source_stage=WorkflowStage.BEATS,
        source_summary="Accepted beat sheet.",
    )

    assert row is not None
    assert row.revision_number == 1
    assert row.source_stage == WorkflowStage.BEATS
    assert row.source_summary == "Accepted beat sheet."

    facts = ContinuityBibleData.model_validate(row.summary_data).facts
    categories = {fact.category for fact in facts}

    assert {
        ContinuityFactCategory.CHARACTER,
        ContinuityFactCategory.LOCATION,
        ContinuityFactCategory.OBJECT,
        ContinuityFactCategory.PROMISE,
        ContinuityFactCategory.VOICE_CONSTRAINT,
        ContinuityFactCategory.UNRESOLVED_THREAD,
        ContinuityFactCategory.LOCKED_DETAIL,
    } <= categories
    assert row.summary_text.startswith("Mira anchors the current story in Juniper Harbor.")


def test_refresh_for_session_reuses_selected_revision_when_facts_do_not_change(
    db_session,
) -> None:
    session_id = _seed_continuity_session(db_session)
    service = SessionContinuityService(db_session)

    first = service.refresh_for_session(
        session_id,
        source_stage=WorkflowStage.BEATS,
        source_summary="Accepted beat sheet.",
    )
    second = service.refresh_for_session(
        session_id,
        source_stage=WorkflowStage.COMPOSITION,
        source_summary="Prepared composition context.",
    )

    assert first is not None
    assert second is not None
    assert second.id == first.id
    assert second.revision_number == 1
    assert second.source_summary == "Accepted beat sheet."


def test_refresh_for_session_drops_invalidated_downstream_facts_from_selected_revision(
    db_session,
) -> None:
    session_id = _seed_continuity_session(db_session)
    service = SessionContinuityService(db_session)
    first = service.refresh_for_session(
        session_id,
        source_stage=WorkflowStage.BEATS,
        source_summary="Accepted beat sheet.",
    )
    assert first is not None

    story_session = db_session.get(StorySession, session_id)
    assert story_session is not None
    for stage_state in story_session.workflow_stage_states:
        if stage_state.stage in {WorkflowStage.BEATS, WorkflowStage.STORY_SETUP}:
            stage_state.status = WorkflowStageState.NEEDS_REGENERATION
    db_session.flush()

    refreshed = service.refresh_for_session(
        session_id,
        source_stage=WorkflowStage.BRIEF,
        source_summary="Resynced continuity after downstream invalidation.",
    )

    assert refreshed is not None
    assert refreshed.id != first.id
    assert refreshed.revision_number == 2

    facts = ContinuityBibleData.model_validate(refreshed.summary_data).facts
    assert not any(fact.source_stage == WorkflowStage.BEATS for fact in facts)
    assert not any(fact.source_stage == WorkflowStage.STORY_SETUP for fact in facts)
    assert any(fact.category == ContinuityFactCategory.LOCKED_DETAIL for fact in facts)

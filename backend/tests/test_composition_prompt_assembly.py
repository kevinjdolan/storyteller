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
from app.models import CompositionPromptAssemblyInput, WorkflowStage
from app.models.workflow import WorkflowStageState
from app.services import CompositionPromptAssemblyService, SessionService
from app.services.composition_prompt_assembly import CompositionPromptAssemblyServiceError
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


def test_composition_prompt_assembly_service_builds_structured_package(db_session) -> None:
    session_id = _seed_prompt_assembly_session(db_session)

    package = CompositionPromptAssemblyService(db_session).assemble_prompt_package(
        CompositionPromptAssemblyInput(
            session_id=session_id,
            job_kind="draft",
            segment_index=1,
        )
    )

    assert package.assembly_version == "composition_prompt_assembly.v1"
    assert (
        package.system_instructions.writer_role == "Backend-owned bedtime story composition engine"
    )
    assert "Stage focus for composition" in package.system_instructions.bedtime_guidelines_fragment
    assert package.dynamic_context.genre.label == "Quest Fantasy"
    assert package.dynamic_context.tone.label == "Hushed Wonder"
    assert package.dynamic_context.selected_pitch.title == "The Silver Bell Buoy"
    assert package.dynamic_context.selected_character_sheet.protagonist_name == "Mira"
    assert package.dynamic_context.beat_sheet.revision_number == 1
    assert package.dynamic_context.story_setup.target_runtime_minutes == 11
    assert package.dynamic_context.outline_card is not None
    assert package.dynamic_context.outline_card.card_key == "chapter-1"
    assert package.dynamic_context.segment_goal_summary == (
        "Chapter 1 should cover Opening Image and Catalyst while staying calm and luminous."
    )
    assert package.debug_context.continuity_fact_count >= 4


def test_composition_prompt_assembly_service_storage_payload_is_debuggable_and_safe(
    db_session,
) -> None:
    session_id = _seed_prompt_assembly_session(db_session)
    instruction = (
        "Rewrite the midpoint so Mira feels supported sooner and the bell never sounds alarming."
    )

    package = CompositionPromptAssemblyService(db_session).assemble_prompt_package(
        CompositionPromptAssemblyInput(
            session_id=session_id,
            job_kind="rewrite",
            segment_index=2,
            instructions=instruction,
            rewrite_from_segment_index=2,
        )
    )
    payload = package.build_storage_payload()

    assert payload["prompt_assembly_version"] == "composition_prompt_assembly.v1"
    assert payload["outline_card_key"] == "chapter-2"
    assert payload["continuity_bible_id"] is not None
    assert payload["composition_prompt"]["dynamic_context"]["job_kind"] == "rewrite"
    assert payload["composition_prompt"]["dynamic_context"]["request_instructions"] == instruction
    assert (
        payload["composition_prompt"]["debug_context"]["requested_instruction_excerpt"]
        == instruction
    )
    assert "api_key" not in str(payload).lower()
    assert "credential" not in str(payload).lower()


def test_eval_composition_prompt_package_covers_required_grounding_and_debug_signals(
    db_session,
) -> None:
    session_id = _seed_prompt_assembly_session(db_session)
    package = CompositionPromptAssemblyService(db_session).assemble_prompt_package(
        CompositionPromptAssemblyInput(
            session_id=session_id,
            job_kind="draft",
            segment_index=1,
        )
    )

    criteria = {
        "stable_instructions_present": (
            len(package.system_instructions.output_contract) >= 4
            and len(package.system_instructions.storytelling_guardrails) >= 4
        ),
        "composition_stage_guidelines_present": (
            "Stage focus for composition" in package.system_instructions.bedtime_guidelines_fragment
        ),
        "required_story_inputs_present": (
            package.dynamic_context.genre.label == "Quest Fantasy"
            and package.dynamic_context.tone.label == "Hushed Wonder"
            and package.dynamic_context.brief.raw_brief.startswith("A harbor fox")
            and package.dynamic_context.selected_pitch.title == "The Silver Bell Buoy"
            and package.dynamic_context.selected_character_sheet.protagonist_name == "Mira"
            and package.dynamic_context.outline_card is not None
        ),
        "continuity_facts_attached": package.debug_context.continuity_fact_count >= 4,
        "debug_context_is_inspectable": (
            package.debug_context.outline_card_key == "chapter-1"
            and package.debug_context.beat_sheet_revision_number == 1
            and package.debug_context.story_setup_revision_number == 1
        ),
        "debug_context_avoids_secret_fields": (
            "api_key" not in package.model_dump_json().lower()
            and "credential" not in package.model_dump_json().lower()
        ),
    }

    assert all(criteria.values()), criteria


def test_eval_composition_prompt_package_falls_back_when_outline_is_missing(db_session) -> None:
    session_id = _seed_prompt_assembly_session(db_session, include_outline=False)
    instruction = "Keep the opening soft and close to home."
    package = CompositionPromptAssemblyService(db_session).assemble_prompt_package(
        CompositionPromptAssemblyInput(
            session_id=session_id,
            job_kind="draft",
            segment_index=1,
            instructions=instruction,
        )
    )

    criteria = {
        "outline_card_can_be_absent_without_crashing": package.dynamic_context.outline_card is None,
        "instruction_becomes_segment_goal_summary": (
            package.dynamic_context.segment_goal_summary == instruction
        ),
        "debug_context_records_missing_outline": package.debug_context.outline_card_key is None,
        "continuity_still_available": package.debug_context.continuity_fact_count >= 3,
    }

    assert all(criteria.values()), criteria


def test_eval_composition_prompt_package_rejects_missing_selected_pitch(db_session) -> None:
    session_id = _seed_prompt_assembly_session(db_session)
    selected_pitch = db_session.query(Pitch).filter(Pitch.session_id == session_id).one()
    selected_pitch.is_selected = False
    db_session.commit()

    with pytest.raises(
        CompositionPromptAssemblyServiceError,
        match="requires a selected pitch",
    ):
        CompositionPromptAssemblyService(db_session).assemble_prompt_package(
            CompositionPromptAssemblyInput(
                session_id=session_id,
                job_kind="draft",
                segment_index=1,
            )
        )


def _seed_prompt_assembly_session(db_session, *, include_outline: bool = True) -> str:
    now = datetime.now(timezone.utc)
    session_service = SessionService(db_session)
    snapshot = session_service.create_session(working_title="Moonlit Harbor")

    genre = Genre(
        slug="quest-fantasy",
        label="Quest Fantasy",
        description="A gentle harbor adventure with a safe return.",
        bedtime_safety_notes="Keep every turn visibly safe and reassuring.",
        arc_notes={
            "bedtime_arc": "Let bravery feel gentle and always connected to home.",
        },
    )
    tone = ToneProfile(
        genre=genre,
        slug="hushed-wonder",
        label="Hushed Wonder",
        description="Soft, luminous, and patient.",
        bedtime_notes="Favor lullaby pacing and warm sensory anchors.",
        descriptors={
            "surface": "moonlit and quiet",
        },
        default_planning_hints={
            "ending": "Finish with a sleepy exhale and visible repair.",
        },
    )
    db_session.add_all([genre, tone])
    db_session.flush()

    story_session = db_session.get(StorySession, snapshot.id)
    assert story_session is not None
    story_session.selected_genre = genre
    story_session.selected_tone_profile = tone

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
        raw_brief="A harbor fox follows a silver clue and returns home calm.",
        normalized_summary="A bedtime harbor mystery with a gentle emotional repair.",
        story_idea="A drifting bell leads Mira toward one last act of care before sleep.",
        desired_themes="belonging, calm courage, and visible repair",
        key_images="silver bell, lantern light, moonlit docks",
        audience_notes="Comfort a listener who wants wonder without sharp tension.",
        must_have_elements="End with the harbor tucked in and the bell resting safely.",
        planning_notes="Keep the midpoint safe and sleepy.",
        normalized_preferences={
            "protagonist_type": "harbor fox child",
            "setting": "Juniper Harbor",
            "emotional_goal": "feel safe enough to let go of bedtime worry",
            "constraint_notes": [
                "Keep every surprise buffered by companionship.",
            ],
            "bedtime_safety_concerns": [
                "Do not let the harbor become unreadable or threatening.",
            ],
            "candidate_motifs": ["silver bell", "lantern wake"],
        },
        is_active=True,
        accepted_at=now,
    )
    db_session.add(brief)
    db_session.flush()

    pitch = Pitch(
        session_id=snapshot.id,
        story_brief_id=brief.id,
        generation_key="pitch-batch-1",
        pitch_index=1,
        title="The Silver Bell Buoy",
        logline="A harbor fox follows a silver bell to guide one last lantern home.",
        summary="Mira must help the harbor settle before the night stretches too long.",
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
                    "role": "harbor fox child",
                    "goal": "guide the last lantern home before the docks grow still",
                    "flaw": "tries to solve every problem alone first",
                    "comfort_trait": "counts lantern reflections when she needs to settle",
                    "bedtime_safety_notes": (
                        "Mira stays emotionally safe because helpers remain close."
                    ),
                    "relationships": ["Trusts Pip to steady the plan."],
                    "visual_anchors": ["knit harbor coat", "lantern satchel"],
                },
                "supporting_cast": [
                    {
                        "name": "Pip",
                        "role": "otter guardian",
                        "goal": "keep Mira company and make every clue feel safe",
                        "flaw": "over-explains when he worries",
                        "comfort_trait": "hums softly before speaking",
                        "bedtime_safety_notes": "Pip keeps each obstacle small and reassuring.",
                        "relationships": ["Promises Mira she will not face the harbor alone."],
                        "visual_anchors": ["bell rope", "river-stone pendant"],
                    }
                ],
            }
        },
        bedtime_notes="Every worry is buffered by visible helpers.",
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
        bedtime_notes="Keep the low point brief and immediately held by companionship.",
        beats={
            "bedtime_goal": "Land in a visibly sleepy harbor ending.",
            "beats": [
                {
                    "key": "opening_image",
                    "label": "Opening Image",
                    "summary": "Mira watches the harbor settle under soft moonlight.",
                    "emotional_intent": "Begin in stillness and wonder.",
                    "bedtime_softening_note": (
                        "Keep the harbor warm and legible from the first sentence."
                    ),
                },
                {
                    "key": "catalyst",
                    "label": "Catalyst",
                    "summary": "A bell buoy drifts away from the dock and asks for help.",
                    "emotional_intent": "Introduce a gentle problem.",
                    "bedtime_softening_note": (
                        "Make the problem feel small, visible, and manageable."
                    ),
                },
                {
                    "key": "midpoint",
                    "label": "Midpoint",
                    "summary": "Mira finds the hidden cove where the bell belongs.",
                    "emotional_intent": "Lift wonder while keeping the surprise soft.",
                    "bedtime_softening_note": "Keep the reveal luminous and quickly reassuring.",
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
        preferences={"ending_image": "the harbor breathing quietly together"},
        is_selected=True,
        accepted_at=now,
    )
    db_session.add(story_setup)
    db_session.flush()

    if include_outline:
        story_outline = StoryOutline(
            session_id=snapshot.id,
            beat_sheet_id=beat_sheet.id,
            story_setup_id=story_setup.id,
            revision_number=1,
            outline_kind="chapter",
            summary="Three draftable chapters mapped from the beat sheet.",
            cards=[
                {
                    "card_key": "chapter-1",
                    "card_type": "chapter",
                    "position": 1,
                    "title": "Chapter 1: Opening Image to Catalyst",
                    "summary": (
                        "Set the moonlit harbor mood and launch Mira after the drifting bell."
                    ),
                    "beat_keys": ["opening_image", "catalyst"],
                    "beat_labels": ["Opening Image", "Catalyst"],
                    "emotional_shift": "Move from stillness toward gentle motion.",
                    "target_word_count": 533,
                    "target_runtime_minutes": 4,
                    "target_scene_count": 3,
                    "tone_direction": (
                        "Stay calm and luminous while moving the harbor story forward."
                    ),
                    "bedtime_guardrail": "Keep the problem small, visible, and quickly reassuring.",
                    "drafting_brief": (
                        "Chapter 1 should cover Opening Image and Catalyst while staying calm "
                        "and luminous."
                    ),
                },
                {
                    "card_key": "chapter-2",
                    "card_type": "chapter",
                    "position": 2,
                    "title": "Chapter 2: Midpoint",
                    "summary": (
                        "Let Mira discover the hidden cove and feel the bell's meaning open up."
                    ),
                    "beat_keys": ["midpoint"],
                    "beat_labels": ["Midpoint"],
                    "emotional_shift": "Lift wonder without breaking the bedtime tone.",
                    "target_word_count": 533,
                    "target_runtime_minutes": 4,
                    "target_scene_count": 3,
                    "tone_direction": "Keep the wonder awed rather than sharp.",
                    "bedtime_guardrail": "Keep the reveal luminous and quickly reassuring.",
                    "drafting_brief": (
                        "Chapter 2 should center the midpoint reveal and make it feel safe."
                    ),
                },
            ],
            is_selected=True,
            accepted_at=now,
        )
        db_session.add(story_outline)
        db_session.flush()

    previous_job = CompositionJob(
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
    db_session.add(previous_job)
    db_session.flush()
    db_session.add(
        CompositionSegment(
            session_id=snapshot.id,
            composition_job_id=previous_job.id,
            segment_index=1,
            revision_number=1,
            status=JobStatus.COMPLETED,
            planned_summary="Mira promises Pip that no bell will drift alone tonight.",
            text_content="Mira steadied the bell rope and breathed with the harbor lights.",
            word_count=12,
            completed_at=now,
        )
    )
    db_session.commit()
    return snapshot.id

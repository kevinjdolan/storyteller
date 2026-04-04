from __future__ import annotations

import logging
from collections.abc import Mapping
from typing import Any

from sqlalchemy.orm import Session

from app.ai import build_bedtime_guidelines_fragment
from app.db import BeatSheet, CharacterSheet, Pitch, StoryBrief, StoryOutline
from app.models import (
    CompositionBeatSheetContext,
    CompositionBriefContext,
    CompositionCatalogContext,
    CompositionContinuityContext,
    CompositionOutlineCardContext,
    CompositionPromptAssemblyInput,
    CompositionPromptDebugContext,
    CompositionPromptDynamicContext,
    CompositionPromptPackage,
    CompositionSetupPreferencesContext,
    CompositionSystemInstructions,
    ContinuityBibleData,
    ExistingCharacterSheetContext,
    ExistingSelectedPitchContext,
    GeneratedBeatSheetBeat,
    NormalizedBriefPreferences,
)
from app.models.workflow import WorkflowStage
from app.observability import log_event
from app.repositories import StorySessionRepository
from app.services.continuity import SessionContinuityService

logger = logging.getLogger(__name__)

_SYSTEM_OUTPUT_CONTRACT = (
    "Write only the requested segment, not the whole story.",
    "Treat word-count and runtime targets as guidance, not rigid quotas.",
    "Advance the exact outline card and beat responsibilities assigned to this segment.",
    "Honor continuity facts and previously locked details without contradicting them.",
)
_SYSTEM_STORYTELLING_GUARDRAILS = (
    (
        "Preserve the selected genre and tone while keeping the narration calm, legible, "
        "and bedtime-safe."
    ),
    "Favor sensory grounding, emotional repair, and visible companionship over sharp escalation.",
    "End the segment on a settled handoff, not a cliffhanger spike.",
    "Keep motifs, promises, and emotional arcs consistent with the accepted plan.",
)
_DEBUG_EXCERPT_LIMIT = 220


class CompositionPromptAssemblyServiceError(Exception):
    """Raised when a composition prompt package cannot be assembled."""


class CompositionPromptAssemblyService:
    def __init__(self, session: Session) -> None:
        self._session = session
        self._sessions = StorySessionRepository(session)
        self._continuity = SessionContinuityService(session)

    def assemble_prompt_package(
        self,
        request: CompositionPromptAssemblyInput,
    ) -> CompositionPromptPackage:
        aggregate = self._sessions.get_aggregate(request.session_id)
        if aggregate is None:
            raise CompositionPromptAssemblyServiceError(
                f"session {request.session_id!r} was not found",
            )

        genre = aggregate.session.selected_genre
        if genre is None:
            raise CompositionPromptAssemblyServiceError(
                "composition prompt assembly requires a selected genre",
            )

        tone = aggregate.session.selected_tone_profile
        if tone is None:
            raise CompositionPromptAssemblyServiceError(
                "composition prompt assembly requires a selected tone",
            )

        brief = aggregate.active_story_brief
        if brief is None:
            raise CompositionPromptAssemblyServiceError(
                "composition prompt assembly requires an active story brief",
            )

        selected_pitch = aggregate.selected_pitch
        if selected_pitch is None:
            raise CompositionPromptAssemblyServiceError(
                "composition prompt assembly requires a selected pitch",
            )

        selected_character_sheet = aggregate.selected_character_sheet
        if selected_character_sheet is None:
            raise CompositionPromptAssemblyServiceError(
                "composition prompt assembly requires a selected character sheet",
            )

        selected_beat_sheet = aggregate.selected_beat_sheet
        if selected_beat_sheet is None:
            raise CompositionPromptAssemblyServiceError(
                "composition prompt assembly requires a selected beat sheet",
            )

        selected_story_setup = aggregate.selected_story_setup
        if selected_story_setup is None:
            raise CompositionPromptAssemblyServiceError(
                "composition prompt assembly requires a selected story setup",
            )

        continuity_bible = self._continuity.refresh_for_session(
            request.session_id,
            source_stage=WorkflowStage.COMPOSITION,
            source_summary=_build_continuity_source_summary(request.job_kind),
        )
        outline_card = _build_outline_card_context(
            aggregate.selected_story_outline,
            request.segment_index,
        )
        beat_sheet_context = _build_beat_sheet_context(selected_beat_sheet)
        segment_goal_summary = _resolve_segment_goal_summary(
            request.instructions,
            outline_card=outline_card,
            beat_sheet=beat_sheet_context,
            brief=brief,
        )
        display_title = _resolve_display_title(aggregate.session.working_title)
        selected_pitch_context = _build_selected_pitch_context(selected_pitch)
        character_sheet_context = _build_existing_character_sheet_context(selected_character_sheet)
        continuity_context = _build_continuity_context(continuity_bible)

        package = CompositionPromptPackage(
            system_instructions=CompositionSystemInstructions(
                bedtime_guideline_preset_key=request.bedtime_guideline_preset_key,
                writer_role="Backend-owned bedtime story composition engine",
                mission=(
                    "Draft the next story segment from durable planning state so the prose stays "
                    "consistent, bedtime-safe, and controllable across rewrites."
                ),
                output_contract=list(_SYSTEM_OUTPUT_CONTRACT),
                storytelling_guardrails=list(_SYSTEM_STORYTELLING_GUARDRAILS),
                bedtime_guidelines_fragment=build_bedtime_guidelines_fragment(
                    stage="composition",
                    preset_key=request.bedtime_guideline_preset_key,
                ),
            ),
            dynamic_context=CompositionPromptDynamicContext(
                session_id=request.session_id,
                display_title=display_title,
                bedtime_guideline_preset_key=request.bedtime_guideline_preset_key,
                job_kind=request.job_kind,
                segment_index=request.segment_index,
                request_instructions=request.instructions,
                segment_goal_summary=segment_goal_summary,
                genre=CompositionCatalogContext(
                    label=genre.label,
                    description=genre.description,
                    bedtime_notes=genre.bedtime_safety_notes,
                    curation_notes=_read_string_notes(getattr(genre, "arc_notes", None)),
                ),
                tone=CompositionCatalogContext(
                    label=tone.label,
                    description=tone.description,
                    bedtime_notes=tone.bedtime_notes,
                    curation_notes=_read_string_notes(getattr(tone, "descriptors", None))
                    + _read_string_notes(getattr(tone, "default_planning_hints", None)),
                ),
                brief=CompositionBriefContext(
                    raw_brief=brief.raw_brief,
                    normalized_summary=brief.normalized_summary,
                    story_idea=brief.story_idea,
                    desired_themes=brief.desired_themes,
                    key_images=brief.key_images,
                    audience_notes=brief.audience_notes,
                    must_have_elements=brief.must_have_elements,
                    planning_notes=brief.planning_notes,
                    normalized_preferences=_read_normalized_preferences(
                        brief.normalized_preferences,
                    ),
                ),
                selected_pitch=selected_pitch_context,
                selected_character_sheet=character_sheet_context,
                beat_sheet=beat_sheet_context,
                story_setup=CompositionSetupPreferencesContext(
                    revision_number=selected_story_setup.revision_number,
                    target_word_count=selected_story_setup.target_word_count,
                    target_runtime_minutes=selected_story_setup.target_runtime_minutes,
                    chapter_count=selected_story_setup.chapter_count,
                    approximate_scene_count=selected_story_setup.approximate_scene_count,
                    chapter_style=selected_story_setup.chapter_style,
                    guidance_notes=selected_story_setup.guidance_notes,
                    preferences=(
                        selected_story_setup.preferences
                        if isinstance(selected_story_setup.preferences, (dict, list))
                        else None
                    ),
                ),
                outline_card=outline_card,
                continuity=continuity_context,
            ),
            debug_context=CompositionPromptDebugContext(
                session_id=request.session_id,
                display_title=display_title,
                job_kind=request.job_kind,
                segment_index=request.segment_index,
                outline_card_key=outline_card.card_key if outline_card is not None else None,
                outline_card_title=outline_card.title if outline_card is not None else None,
                story_outline_revision_number=(
                    outline_card.story_outline_revision_number if outline_card is not None else None
                ),
                beat_sheet_revision_number=selected_beat_sheet.revision_number,
                story_setup_revision_number=selected_story_setup.revision_number,
                continuity_revision_number=continuity_context.revision_number,
                continuity_fact_count=len(continuity_context.facts),
                selected_pitch_title=selected_pitch_context.title,
                selected_character_sheet_title=(
                    character_sheet_context.title or character_sheet_context.protagonist_name
                ),
                requested_instruction_excerpt=_truncate(request.instructions),
                segment_goal_summary=_truncate(segment_goal_summary),
            ),
        )
        log_event(
            logger,
            logging.INFO,
            "composition.prompt.assembled",
            "Assembled the composition prompt package.",
            session_id=request.session_id,
            segment_index=request.segment_index,
            job_kind=request.job_kind,
            outline_card_key=package.debug_context.outline_card_key,
            continuity_revision=package.debug_context.continuity_revision_number,
            continuity_fact_count=package.debug_context.continuity_fact_count,
        )
        return package


def _build_continuity_source_summary(job_kind: str) -> str:
    if job_kind == "rewrite":
        return "Prepared rewrite context from the current continuity bible."
    return "Prepared composition context from the current continuity bible."


def _resolve_display_title(working_title: str | None) -> str:
    normalized = working_title.strip() if isinstance(working_title, str) else ""
    return normalized or "Untitled story session"


def _read_string_notes(value: Any) -> list[str]:
    notes: list[str] = []
    if isinstance(value, list):
        candidates = value
    elif isinstance(value, Mapping):
        candidates = list(value.values())
    else:
        return notes

    for candidate in candidates:
        if isinstance(candidate, str):
            normalized = candidate.strip()
            if normalized:
                notes.append(normalized)
    return notes


def _read_normalized_preferences(value: Any) -> NormalizedBriefPreferences:
    if isinstance(value, Mapping):
        return NormalizedBriefPreferences.model_validate(value)
    return NormalizedBriefPreferences()


def _build_selected_pitch_context(pitch: Pitch) -> ExistingSelectedPitchContext:
    return ExistingSelectedPitchContext(
        title=pitch.title,
        hook=pitch.logline,
        central_conflict=pitch.summary,
        why_it_fits=pitch.bedtime_notes,
    )


def _build_existing_character_sheet_context(
    character_sheet: CharacterSheet,
) -> ExistingCharacterSheetContext:
    protagonist_payload = None
    supporting_cast_payload: list[Any] = []
    if isinstance(character_sheet.character_data, Mapping):
        candidate_payload = character_sheet.character_data.get("candidate")
        if isinstance(candidate_payload, Mapping):
            protagonist_payload = candidate_payload.get("protagonist")
            raw_supporting_cast = candidate_payload.get("supporting_cast")
            if isinstance(raw_supporting_cast, list):
                supporting_cast_payload = raw_supporting_cast

    return ExistingCharacterSheetContext(
        title=character_sheet.title,
        summary=character_sheet.summary,
        protagonist_name=character_sheet.protagonist_name,
        bedtime_safety_notes=character_sheet.bedtime_notes,
        protagonist=protagonist_payload,
        supporting_cast=supporting_cast_payload,
    )


def _build_beat_sheet_context(beat_sheet: BeatSheet) -> CompositionBeatSheetContext:
    bedtime_goal = None
    raw_beats: list[Any] = []
    if isinstance(beat_sheet.beats, Mapping):
        bedtime_goal = _read_optional_text(beat_sheet.beats.get("bedtime_goal"))
        candidate_beats = beat_sheet.beats.get("beats")
        if isinstance(candidate_beats, list):
            raw_beats = candidate_beats

    beats: list[GeneratedBeatSheetBeat] = []
    for raw_beat in raw_beats:
        if not isinstance(raw_beat, Mapping):
            continue
        beats.append(
            GeneratedBeatSheetBeat.model_validate(
                {
                    "key": raw_beat.get("key"),
                    "label": raw_beat.get("label"),
                    "summary": raw_beat.get("summary"),
                    "emotional_intent": raw_beat.get("emotional_intent") or raw_beat.get("summary"),
                    "bedtime_softening_note": raw_beat.get("bedtime_softening_note")
                    or raw_beat.get("summary"),
                }
            )
        )

    return CompositionBeatSheetContext(
        revision_number=beat_sheet.revision_number,
        summary=beat_sheet.summary,
        bedtime_notes=beat_sheet.bedtime_notes,
        bedtime_goal=bedtime_goal,
        beats=beats,
    )


def _build_outline_card_context(
    story_outline: StoryOutline | None,
    segment_index: int,
) -> CompositionOutlineCardContext | None:
    if story_outline is None or not isinstance(story_outline.cards, list):
        return None
    if not story_outline.cards:
        return None

    card_index = min(max(segment_index - 1, 0), len(story_outline.cards) - 1)
    raw_card = story_outline.cards[card_index]
    if not isinstance(raw_card, Mapping):
        return None

    return CompositionOutlineCardContext(
        story_outline_id=story_outline.id,
        story_outline_revision_number=story_outline.revision_number,
        outline_kind=story_outline.outline_kind,
        card_key=_read_optional_text(raw_card.get("card_key")) or f"segment-{segment_index}",
        position=_read_int(raw_card.get("position"), default=segment_index),
        title=_read_optional_text(raw_card.get("title")) or f"Segment {segment_index}",
        summary=_read_optional_text(raw_card.get("summary")),
        drafting_brief=_read_optional_text(raw_card.get("drafting_brief")),
        beat_keys=_read_string_list(raw_card.get("beat_keys")),
        beat_labels=_read_string_list(raw_card.get("beat_labels")),
        emotional_shift=_read_optional_text(raw_card.get("emotional_shift")),
        tone_direction=_read_optional_text(raw_card.get("tone_direction")),
        bedtime_guardrail=_read_optional_text(raw_card.get("bedtime_guardrail")),
        target_word_count=_read_optional_int(raw_card.get("target_word_count")),
        target_runtime_minutes=_read_optional_int(raw_card.get("target_runtime_minutes")),
        target_scene_count=_read_optional_int(raw_card.get("target_scene_count")),
    )


def _build_continuity_context(continuity_bible) -> CompositionContinuityContext:
    if continuity_bible is None:
        return CompositionContinuityContext()

    facts = []
    if isinstance(getattr(continuity_bible, "summary_data", None), Mapping):
        facts = ContinuityBibleData.model_validate(continuity_bible.summary_data).facts

    return CompositionContinuityContext(
        continuity_bible_id=continuity_bible.id,
        revision_number=continuity_bible.revision_number,
        summary_text=continuity_bible.summary_text,
        facts=facts,
    )


def _resolve_segment_goal_summary(
    instructions: str | None,
    *,
    outline_card: CompositionOutlineCardContext | None,
    beat_sheet: CompositionBeatSheetContext,
    brief: StoryBrief,
) -> str:
    for candidate in (
        instructions,
        outline_card.drafting_brief if outline_card is not None else None,
        outline_card.summary if outline_card is not None else None,
        beat_sheet.summary,
        brief.normalized_summary,
        brief.raw_brief,
    ):
        normalized = _read_optional_text(candidate)
        if normalized is not None:
            return normalized
    return "Draft the next bedtime-story segment from the accepted plan."


def _truncate(value: str | None, *, limit: int = _DEBUG_EXCERPT_LIMIT) -> str | None:
    normalized = _read_optional_text(value)
    if normalized is None or len(normalized) <= limit:
        return normalized
    return normalized[: limit - 3].rstrip() + "..."


def _read_optional_text(value: Any) -> str | None:
    if not isinstance(value, str):
        return None
    normalized = value.strip()
    return normalized or None


def _read_optional_int(value: Any) -> int | None:
    if isinstance(value, bool) or value is None:
        return None
    if isinstance(value, int):
        return value if value > 0 else None
    try:
        parsed = int(str(value))
    except (TypeError, ValueError):
        return None
    return parsed if parsed > 0 else None


def _read_int(value: Any, *, default: int) -> int:
    parsed = _read_optional_int(value)
    return parsed if parsed is not None else default


def _read_string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []

    items: list[str] = []
    for entry in value:
        normalized = _read_optional_text(entry)
        if normalized is not None:
            items.append(normalized)
    return items

from __future__ import annotations

import re
from collections import defaultdict
from collections.abc import Mapping
from typing import Any

from sqlalchemy import Select, select
from sqlalchemy.orm import Session

from app.db import CompositionSegment, ContinuityBible, JobStatus
from app.models import ContinuityBibleData, ContinuityFact, ContinuityFactCategory, WorkflowStage
from app.models.workflow import WorkflowStageState, get_workflow_stage_definition
from app.repositories import SessionAggregate, StorySessionRepository

_CATEGORY_LIMITS = {
    ContinuityFactCategory.CHARACTER: 6,
    ContinuityFactCategory.LOCATION: 4,
    ContinuityFactCategory.OBJECT: 6,
    ContinuityFactCategory.PROMISE: 5,
    ContinuityFactCategory.VOICE_CONSTRAINT: 8,
    ContinuityFactCategory.UNRESOLVED_THREAD: 5,
    ContinuityFactCategory.LOCKED_DETAIL: 5,
}

_STAGE_SOURCE_LABELS = {
    WorkflowStage.GENRE: "Genre",
    WorkflowStage.TONE: "Tone",
    WorkflowStage.BRIEF: "Story brief",
    WorkflowStage.PITCHES: "Pitch",
    WorkflowStage.CHARACTERS: "Character sheet",
    WorkflowStage.BEATS: "Beat sheet",
    WorkflowStage.STORY_SETUP: "Story setup",
    WorkflowStage.COMPOSITION: "Composition",
}


class SessionContinuityService:
    def __init__(self, session: Session) -> None:
        self._session = session
        self._sessions = StorySessionRepository(session)

    def refresh_for_session(
        self,
        session_id: str,
        *,
        source_stage: WorkflowStage | None,
        source_summary: str | None = None,
    ) -> ContinuityBible | None:
        aggregate = self._sessions.get_aggregate(session_id)
        if aggregate is None:
            return None

        facts = _build_continuity_facts(
            aggregate,
            locked_segments=self._load_locked_segments(session_id),
        )
        current = self._sessions.get_selected_continuity_bible(session_id)
        if not facts:
            return current

        summary_text = _build_summary_text(facts)
        summary_data = ContinuityBibleData(facts=facts).model_dump(mode="json")

        if (
            current is not None
            and current.summary_text == summary_text
            and current.summary_data == summary_data
        ):
            return current

        if current is not None:
            current.is_selected = False

        next_revision_number = self._next_revision_number(session_id)
        continuity_bible = ContinuityBible(
            session_id=session_id,
            revision_number=next_revision_number,
            source_stage=source_stage,
            source_summary=_normalize_optional_text(source_summary),
            summary_text=summary_text,
            summary_data=summary_data,
            is_selected=True,
        )
        self._session.add(continuity_bible)
        self._session.flush()
        return continuity_bible

    def _next_revision_number(self, session_id: str) -> int:
        stmt = (
            select(ContinuityBible.revision_number)
            .where(ContinuityBible.session_id == session_id)
            .order_by(ContinuityBible.revision_number.desc())
            .limit(1)
        )
        current = self._session.execute(stmt).scalar_one_or_none()
        return int(current or 0) + 1

    def _load_locked_segments(self, session_id: str) -> list[CompositionSegment]:
        stmt: Select[tuple[CompositionSegment]] = (
            select(CompositionSegment)
            .where(
                CompositionSegment.session_id == session_id,
                CompositionSegment.superseded_by_segment_id.is_(None),
            )
            .order_by(
                CompositionSegment.segment_index.asc(),
                CompositionSegment.revision_number.desc(),
            )
        )
        rows = list(self._session.execute(stmt).scalars().all())
        latest_by_segment: dict[int, CompositionSegment] = {}
        for row in rows:
            if row.segment_index in latest_by_segment:
                continue
            if row.status != JobStatus.COMPLETED and row.completed_at is None:
                continue
            if row.text_content is None and row.planned_summary is None:
                continue
            latest_by_segment[row.segment_index] = row
        return [latest_by_segment[index] for index in sorted(latest_by_segment)]


def build_continuity_payload(row: ContinuityBible | None) -> dict[str, Any]:
    if row is None:
        return {}

    raw_summary_data = getattr(row, "summary_data", None)
    data = (
        ContinuityBibleData.model_validate(raw_summary_data)
        if isinstance(raw_summary_data, Mapping)
        else ContinuityBibleData()
    )
    return {
        "continuity_bible_id": row.id,
        "continuity_revision_number": row.revision_number,
        "continuity_summary": row.summary_text,
        "continuity_facts": data.model_dump(mode="json")["facts"],
    }


def _build_continuity_facts(
    aggregate: SessionAggregate,
    *,
    locked_segments: list[CompositionSegment],
) -> list[ContinuityFact]:
    stage_statuses = {
        stage_state.stage: stage_state.status
        for stage_state in aggregate.session.workflow_stage_states
    }
    facts: list[ContinuityFact] = []
    counts: dict[ContinuityFactCategory, int] = defaultdict(int)
    seen: set[tuple[str, str, str]] = set()

    def add_fact(
        category: ContinuityFactCategory,
        title: str | None,
        detail: str | None,
        *,
        source_stage: WorkflowStage | None,
        source_label: str | None = None,
    ) -> None:
        normalized_title = _normalize_optional_text(title)
        normalized_detail = _normalize_optional_text(detail)
        if normalized_title is None or normalized_detail is None:
            return
        if counts[category] >= _CATEGORY_LIMITS[category]:
            return

        dedupe_key = (
            category.value,
            normalized_title.casefold(),
            normalized_detail.casefold(),
        )
        if dedupe_key in seen:
            return

        counts[category] += 1
        seen.add(dedupe_key)
        fact_index = counts[category]
        facts.append(
            ContinuityFact(
                key=f"{category.value}:{_slugify(normalized_title)}:{fact_index}",
                category=category,
                title=normalized_title,
                detail=_truncate(normalized_detail, limit=220),
                source_stage=source_stage,
                source_label=source_label,
            )
        )

    if _is_stage_canonical(stage_statuses, WorkflowStage.TONE) and (
        aggregate.session.selected_tone_profile is not None
    ):
        tone = aggregate.session.selected_tone_profile
        tone_detail = " ".join(
            part
            for part in (tone.description, tone.bedtime_notes)
            if _normalize_optional_text(part) is not None
        ) or f"Preserve the {tone.label} bedtime tone."
        add_fact(
            ContinuityFactCategory.VOICE_CONSTRAINT,
            "Tone lane",
            f"{tone.label}. {tone_detail}",
            source_stage=WorkflowStage.TONE,
            source_label=tone.label,
        )

    if _is_stage_canonical(stage_statuses, WorkflowStage.BRIEF) and (
        aggregate.active_story_brief is not None
    ):
        brief = aggregate.active_story_brief
        preferences = (
            brief.normalized_preferences
            if isinstance(brief.normalized_preferences, Mapping)
            else {}
        )
        setting = _normalize_optional_text(_read_optional_mapping_text(preferences, "setting"))
        if setting is not None:
            add_fact(
                ContinuityFactCategory.LOCATION,
                setting,
                "Use this as the default world anchor unless a later accepted plan overrides it.",
                source_stage=WorkflowStage.BRIEF,
                source_label="Story brief",
            )

        for image in _split_phrases(brief.key_images, allow_commas=True):
            add_fact(
                ContinuityFactCategory.OBJECT,
                image,
                "Recurring image or prop from the accepted story brief.",
                source_stage=WorkflowStage.BRIEF,
                source_label="Story brief",
            )

        for motif in _read_string_list(preferences.get("candidate_motifs")):
            add_fact(
                ContinuityFactCategory.OBJECT,
                motif,
                "Motif from normalized brief preferences.",
                source_stage=WorkflowStage.BRIEF,
                source_label="Brief motif",
            )

        for promise in _split_phrases(brief.must_have_elements):
            add_fact(
                ContinuityFactCategory.PROMISE,
                "Must-have element",
                promise,
                source_stage=WorkflowStage.BRIEF,
                source_label="Story brief",
            )

        for note in _read_string_list(preferences.get("constraint_notes")):
            add_fact(
                ContinuityFactCategory.VOICE_CONSTRAINT,
                "Story constraint",
                note,
                source_stage=WorkflowStage.BRIEF,
                source_label="Story brief",
            )

        for note in _read_string_list(preferences.get("bedtime_safety_concerns")):
            add_fact(
                ContinuityFactCategory.VOICE_CONSTRAINT,
                "Bedtime safety",
                note,
                source_stage=WorkflowStage.BRIEF,
                source_label="Story brief",
            )

        add_fact(
            ContinuityFactCategory.VOICE_CONSTRAINT,
            "Planning note",
            brief.planning_notes,
            source_stage=WorkflowStage.BRIEF,
            source_label="Story brief",
        )

    if _is_stage_canonical(stage_statuses, WorkflowStage.PITCHES) and (
        aggregate.selected_pitch is not None
    ):
        pitch = aggregate.selected_pitch
        add_fact(
            ContinuityFactCategory.PROMISE,
            pitch.title,
            pitch.logline,
            source_stage=WorkflowStage.PITCHES,
            source_label=pitch.title,
        )
        add_fact(
            ContinuityFactCategory.UNRESOLVED_THREAD,
            "Core tension",
            pitch.summary,
            source_stage=WorkflowStage.PITCHES,
            source_label=pitch.title,
        )
        add_fact(
            ContinuityFactCategory.VOICE_CONSTRAINT,
            "Pitch bedtime note",
            pitch.bedtime_notes,
            source_stage=WorkflowStage.PITCHES,
            source_label=pitch.title,
        )

    if _is_stage_canonical(stage_statuses, WorkflowStage.CHARACTERS) and (
        aggregate.selected_character_sheet is not None
    ):
        character_sheet = aggregate.selected_character_sheet
        candidate_payload = (
            character_sheet.character_data
            if isinstance(character_sheet.character_data, Mapping)
            else {}
        )
        protagonist = (
            candidate_payload.get("candidate", {}).get("protagonist")
            if isinstance(candidate_payload.get("candidate"), Mapping)
            else None
        )
        add_fact(
            ContinuityFactCategory.CHARACTER,
            character_sheet.protagonist_name or character_sheet.title or "Lead character",
            _build_character_detail(
                protagonist if isinstance(protagonist, Mapping) else None,
                fallback_summary=character_sheet.summary,
            ),
            source_stage=WorkflowStage.CHARACTERS,
            source_label=character_sheet.title or character_sheet.protagonist_name,
        )

        supporting_cast = []
        if isinstance(candidate_payload.get("candidate"), Mapping):
            supporting_cast = candidate_payload["candidate"].get("supporting_cast", [])
        if (
            not isinstance(supporting_cast, list)
            and isinstance(character_sheet.supporting_cast, list)
        ):
            supporting_cast = character_sheet.supporting_cast
        for member in supporting_cast or []:
            if not isinstance(member, Mapping):
                continue
            add_fact(
                ContinuityFactCategory.CHARACTER,
                _read_optional_mapping_text(member, "name"),
                _build_character_detail(member),
                source_stage=WorkflowStage.CHARACTERS,
                source_label=character_sheet.title or character_sheet.protagonist_name,
            )

        visual_motifs = []
        if isinstance(candidate_payload.get("candidate"), Mapping):
            visual_motifs = candidate_payload["candidate"].get("visual_motifs", [])
        for motif in _read_string_list(visual_motifs):
            add_fact(
                ContinuityFactCategory.OBJECT,
                motif,
                "Recurring visual motif from the accepted character sheet.",
                source_stage=WorkflowStage.CHARACTERS,
                source_label=character_sheet.title or character_sheet.protagonist_name,
            )

    if _is_stage_canonical(stage_statuses, WorkflowStage.BEATS) and (
        aggregate.selected_beat_sheet is not None
    ):
        beat_sheet = aggregate.selected_beat_sheet
        payload = beat_sheet.beats if isinstance(beat_sheet.beats, Mapping) else {}
        add_fact(
            ContinuityFactCategory.PROMISE,
            f"Beat sheet revision {beat_sheet.revision_number}",
            beat_sheet.summary,
            source_stage=WorkflowStage.BEATS,
            source_label=f"Revision {beat_sheet.revision_number}",
        )
        add_fact(
            ContinuityFactCategory.VOICE_CONSTRAINT,
            "Beat bedtime note",
            beat_sheet.bedtime_notes,
            source_stage=WorkflowStage.BEATS,
            source_label=f"Revision {beat_sheet.revision_number}",
        )
        add_fact(
            ContinuityFactCategory.VOICE_CONSTRAINT,
            "Beat bedtime goal",
            _read_optional_mapping_text(payload, "bedtime_goal"),
            source_stage=WorkflowStage.BEATS,
            source_label=f"Revision {beat_sheet.revision_number}",
        )

        raw_beats = payload.get("beats")
        if isinstance(raw_beats, list):
            for raw_beat in raw_beats:
                if not isinstance(raw_beat, Mapping):
                    continue
                beat_key = _read_optional_mapping_text(raw_beat, "key")
                if beat_key not in {"catalyst", "midpoint", "all_is_lost"}:
                    continue
                add_fact(
                    ContinuityFactCategory.UNRESOLVED_THREAD,
                    _read_optional_mapping_text(raw_beat, "label")
                    or beat_key.replace("_", " ").title(),
                    _read_optional_mapping_text(raw_beat, "summary"),
                    source_stage=WorkflowStage.BEATS,
                    source_label=f"Revision {beat_sheet.revision_number}",
                )

    if _is_stage_canonical(stage_statuses, WorkflowStage.STORY_SETUP) and (
        aggregate.selected_story_setup is not None
    ):
        setup = aggregate.selected_story_setup
        add_fact(
            ContinuityFactCategory.VOICE_CONSTRAINT,
            "Story setup guidance",
            setup.guidance_notes,
            source_stage=WorkflowStage.STORY_SETUP,
            source_label=f"Revision {setup.revision_number}",
        )

    highest_locked_segment_index = max(
        (segment.segment_index for segment in locked_segments),
        default=0,
    )
    if _is_stage_canonical(stage_statuses, WorkflowStage.STORY_SETUP) and (
        aggregate.selected_story_outline is not None
    ):
        outline = aggregate.selected_story_outline
        raw_cards = outline.cards if isinstance(outline.cards, list) else []
        upcoming_cards = [
            card
            for card in raw_cards
            if isinstance(card, Mapping)
            and isinstance(card.get("position"), int)
            and card["position"] > highest_locked_segment_index
        ]
        if not upcoming_cards:
            upcoming_cards = [
                card
                for card in raw_cards
                if isinstance(card, Mapping)
            ]
        for card in upcoming_cards[:3]:
            add_fact(
                ContinuityFactCategory.UNRESOLVED_THREAD,
                _read_optional_mapping_text(card, "title"),
                _read_optional_mapping_text(card, "summary"),
                source_stage=WorkflowStage.STORY_SETUP,
                source_label=_read_optional_mapping_text(card, "card_key"),
            )
        for card in raw_cards:
            if not isinstance(card, Mapping):
                continue
            add_fact(
                ContinuityFactCategory.VOICE_CONSTRAINT,
                _read_optional_mapping_text(card, "title") or "Outline guardrail",
                _read_optional_mapping_text(card, "bedtime_guardrail"),
                source_stage=WorkflowStage.STORY_SETUP,
                source_label=_read_optional_mapping_text(card, "card_key"),
            )

    for segment in locked_segments:
        payload = segment.payload if isinstance(segment.payload, Mapping) else {}
        detail = _normalize_optional_text(segment.planned_summary) or _truncate(
            _normalize_optional_text(segment.text_content) or "",
            limit=200,
        )
        add_fact(
            ContinuityFactCategory.LOCKED_DETAIL,
            _read_optional_mapping_text(payload, "outline_card_title")
            or f"Segment {segment.segment_index}",
            detail,
            source_stage=WorkflowStage.COMPOSITION,
            source_label=f"Segment {segment.segment_index}",
        )

    return facts


def _is_stage_canonical(
    stage_statuses: Mapping[WorkflowStage, WorkflowStageState],
    stage: WorkflowStage,
) -> bool:
    status = stage_statuses.get(stage)
    return status in {WorkflowStageState.IN_PROGRESS, WorkflowStageState.COMPLETED}


def _build_character_detail(
    payload: Mapping[str, Any] | None,
    *,
    fallback_summary: str | None = None,
) -> str | None:
    parts: list[str] = []
    if payload is not None:
        for key in ("role", "goal", "flaw", "comfort_trait"):
            value = _read_optional_mapping_text(payload, key)
            if value is not None:
                humanized = key.replace("_", " ")
                parts.append(f"{humanized}: {value}")
        relationships = _read_string_list(payload.get("relationships"))
        if relationships:
            parts.append("relationships: " + "; ".join(relationships[:2]))
        anchors = _read_string_list(payload.get("visual_anchors"))
        if anchors:
            parts.append("visual anchors: " + ", ".join(anchors[:2]))
    if not parts and fallback_summary is not None:
        parts.append(fallback_summary)
    return ". ".join(parts) if parts else None


def _build_summary_text(facts: list[ContinuityFact]) -> str:
    lead = _find_first_fact(facts, ContinuityFactCategory.CHARACTER)
    location = _find_first_fact(facts, ContinuityFactCategory.LOCATION)
    promise = _find_first_fact(facts, ContinuityFactCategory.PROMISE)
    voice = _find_first_fact(facts, ContinuityFactCategory.VOICE_CONSTRAINT)
    open_thread = _find_first_fact(facts, ContinuityFactCategory.UNRESOLVED_THREAD)
    locked_detail = _find_first_fact(facts, ContinuityFactCategory.LOCKED_DETAIL)

    parts: list[str] = []
    if lead is not None and location is not None:
        parts.append(f"{lead.title} anchors the current story in {location.title}.")
    elif lead is not None:
        parts.append(f"{lead.title} anchors the current story.")
    elif location is not None:
        parts.append(f"The current story stays grounded in {location.title}.")

    if promise is not None:
        parts.append(f"Protect the promise of {_trim_sentence(promise.detail)}.")
    if voice is not None:
        parts.append(f"Voice guardrail: {_trim_sentence(voice.detail)}.")
    if open_thread is not None:
        parts.append(f"Open thread: {open_thread.title}.")
    if locked_detail is not None:
        parts.append(f"Locked detail: {locked_detail.title}.")

    if not parts:
        counts = defaultdict(int)
        for fact in facts:
            counts[fact.category] += 1
        count_parts = [
            f"{counts[category]} {category.value.replace('_', ' ')}"
            for category in ContinuityFactCategory
            if counts[category] > 0
        ]
        return "Continuity tracks " + ", ".join(count_parts) + "."

    return _truncate(" ".join(parts), limit=420)


def _find_first_fact(
    facts: list[ContinuityFact],
    category: ContinuityFactCategory,
) -> ContinuityFact | None:
    for fact in facts:
        if fact.category == category:
            return fact
    return None


def _split_phrases(value: str | None, *, allow_commas: bool = False) -> list[str]:
    normalized = _normalize_optional_text(value)
    if normalized is None:
        return []

    pattern = r"[\n;]+"
    if allow_commas:
        pattern = r"[\n;,]+"
    parts = [
        item.strip()
        for item in re.split(pattern, normalized)
    ]
    return [part for part in parts if part]


def _read_optional_mapping_text(data: Mapping[str, Any], key: str) -> str | None:
    value = data.get(key)
    return value if isinstance(value, str) and value.strip() else None


def _read_string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [entry for entry in value if isinstance(entry, str) and entry.strip()]


def _normalize_optional_text(value: str | None) -> str | None:
    if value is None:
        return None
    normalized = value.strip()
    return normalized or None


def _slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.casefold()).strip("-")
    return slug or "fact"


def _truncate(value: str, *, limit: int) -> str:
    if len(value) <= limit:
        return value
    return value[: limit - 3].rstrip() + "..."


def _trim_sentence(value: str) -> str:
    normalized = value.strip()
    return normalized[:-1] if normalized.endswith(".") else normalized


def format_continuity_source(stage: WorkflowStage | None) -> str | None:
    if stage is None:
        return None
    return _STAGE_SOURCE_LABELS.get(stage) or get_workflow_stage_definition(stage).label

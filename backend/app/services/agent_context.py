from __future__ import annotations

from datetime import timezone

from app.models.session import SessionSnapshot
from app.models.workflow import get_workflow_stage_definition
from app.services.audio_settings import build_audio_settings_memory_summary


def build_session_agent_context_summary(
    snapshot: SessionSnapshot,
    *,
    use_conversation_memory: bool = True,
) -> str:
    if use_conversation_memory and snapshot.conversation_memory is not None:
        lines = [snapshot.conversation_memory.summary_text]
    else:
        lines = [
            f"Session title: {snapshot.display_title}",
            f"Overall status: {snapshot.overall_status.value}",
            (
                "Current stage: "
                f"{snapshot.current_stage.value} "
                f"({_find_stage_state(snapshot, snapshot.current_stage).status.value})"
            ),
            f"Resume stage: {snapshot.resume_stage.value}",
        ]

        if snapshot.selected_genre is not None:
            lines.append(f"Selected genre: {snapshot.selected_genre.label}")

        if snapshot.selected_tone_profile is not None:
            lines.append(f"Selected tone: {snapshot.selected_tone_profile.label}")

        if snapshot.story_brief is not None:
            lines.append(
                "Story brief: "
                + _truncate(
                    snapshot.story_brief.normalized_summary
                    or snapshot.story_brief.story_idea
                    or snapshot.story_brief.raw_brief
                )
            )
            lines.extend(_build_brief_preference_lines(snapshot.story_brief.normalized_preferences))

        if snapshot.selected_pitch is not None:
            lines.append(f"Selected pitch: {snapshot.selected_pitch.title}")
            lines.append(f"Pitch logline: {_truncate(snapshot.selected_pitch.logline)}")
            if snapshot.selected_pitch.selection_rationale:
                lines.append(
                    "Pitch refinement note: "
                    + _truncate(snapshot.selected_pitch.selection_rationale)
                )

        if snapshot.selected_beat_sheet is not None and snapshot.selected_beat_sheet.summary:
            lines.append(f"Beat sheet: {_truncate(snapshot.selected_beat_sheet.summary)}")

        story_setup_summary = _build_story_setup_summary(snapshot)
        if story_setup_summary is not None:
            lines.append(story_setup_summary)
        if snapshot.selected_story_outline is not None:
            outline_line = (
                f"Story outline: {snapshot.selected_story_outline.outline_kind}, "
                f"{len(snapshot.selected_story_outline.cards)} cards"
            )
            if snapshot.selected_story_outline.summary:
                outline_line += f" - {_truncate(snapshot.selected_story_outline.summary)}"
            lines.append(outline_line)

        if snapshot.continuity_bible is not None:
            lines.append("Continuity: " + _truncate(snapshot.continuity_bible.summary_text))
            open_threads = [
                fact.title
                for fact in snapshot.continuity_bible.facts
                if fact.category == "unresolved_thread"
            ]
            if open_threads:
                lines.append(
                    "Open continuity threads: "
                    + "; ".join(_truncate(thread, limit=80) for thread in open_threads[:3])
                )

    lines.extend(_build_character_context_lines(snapshot))

    current_stage_detail = _find_stage_state(snapshot, snapshot.current_stage).detail
    if current_stage_detail:
        current_stage_label = get_workflow_stage_definition(snapshot.current_stage).label
        lines.append(
            f"Current {current_stage_label.lower()} detail: {_truncate(current_stage_detail)}"
        )

    latest_detail = _build_latest_detail_summary(snapshot)
    if latest_detail is not None:
        lines.append(latest_detail)

    regeneration_stages = [
        get_workflow_stage_definition(stage.stage).label
        for stage in snapshot.stage_states
        if stage.status.value == "needs_regeneration"
    ]
    if regeneration_stages:
        lines.append("Needs regeneration: " + ", ".join(regeneration_stages))

    composition_job = snapshot.active_composition_job or snapshot.latest_composition_job
    if composition_job is not None:
        lines.append(
            f"Composition job: {composition_job.status} at {composition_job.progress_percent:.1f}%"
        )

    audio_job = snapshot.active_audio_job or snapshot.latest_audio_job
    if audio_job is not None:
        lines.append(f"Audio job: {audio_job.status}, voice={audio_job.voice_key or 'unset'}")

    lines.append("Audio settings: " + build_audio_settings_memory_summary(snapshot.audio_settings))

    return "\n".join(lines)


def _build_character_context_lines(snapshot: SessionSnapshot) -> list[str]:
    lines: list[str] = []

    if snapshot.selected_character_sheet is not None:
        character_summary = snapshot.selected_character_sheet.title or "Character sheet selected"
        if snapshot.selected_character_sheet.protagonist_name:
            character_summary += (
                f" (protagonist: {snapshot.selected_character_sheet.protagonist_name})"
            )
        lines.append(character_summary)
        if snapshot.selected_character_sheet.selection_rationale:
            lines.append(
                "Character refinement note: "
                + _truncate(snapshot.selected_character_sheet.selection_rationale)
            )

    latest_batch = snapshot.character_sheet_batches[0] if snapshot.character_sheet_batches else None
    if latest_batch is None or not latest_batch.character_sheets:
        return lines

    option_summaries = []
    for character_sheet in latest_batch.character_sheets[:3]:
        option_label = (
            character_sheet.title
            or character_sheet.protagonist_name
            or f"Revision {character_sheet.revision_number}"
        )
        protagonist_tail = (
            f" ({character_sheet.protagonist_name})"
            if character_sheet.protagonist_name
            and character_sheet.protagonist_name != character_sheet.title
            else ""
        )
        option_summaries.append(
            f"Rev {character_sheet.revision_number}: {option_label}{protagonist_tail}"
        )

    lines.append("Latest character options: " + "; ".join(option_summaries))

    if latest_batch.change_summary:
        impact_prefix = (
            f"{latest_batch.change_impact.value.capitalize()} character change"
            if latest_batch.change_impact is not None
            else "Character refinement"
        )
        lines.append(f"{impact_prefix}: {_truncate(latest_batch.change_summary)}")

    return lines


def _build_story_setup_summary(snapshot: SessionSnapshot) -> str | None:
    if snapshot.selected_story_setup is None:
        return None

    setup_bits = []
    if snapshot.selected_story_setup.target_word_count is not None:
        setup_bits.append(f"{snapshot.selected_story_setup.target_word_count} words")
    if snapshot.selected_story_setup.target_runtime_minutes is not None:
        setup_bits.append(f"{snapshot.selected_story_setup.target_runtime_minutes} minutes")
    if snapshot.selected_story_setup.chapter_count is not None:
        setup_bits.append(f"{snapshot.selected_story_setup.chapter_count} chapters")
    if snapshot.selected_story_setup.approximate_scene_count is not None:
        setup_bits.append(f"about {snapshot.selected_story_setup.approximate_scene_count} scenes")
    if snapshot.selected_story_setup.chapter_style:
        setup_bits.append(snapshot.selected_story_setup.chapter_style)
    if snapshot.selected_story_setup.guidance_notes:
        setup_bits.append(_truncate(snapshot.selected_story_setup.guidance_notes))

    if not setup_bits:
        return None

    return "Story setup: " + ", ".join(setup_bits)


def _build_brief_preference_lines(normalized_preferences) -> list[str]:
    if normalized_preferences is None:
        return []

    lines: list[str] = []
    if normalized_preferences.protagonist_type:
        lines.append(f"Brief protagonist type: {normalized_preferences.protagonist_type}")
    if normalized_preferences.setting:
        lines.append(f"Brief setting: {normalized_preferences.setting}")
    if normalized_preferences.emotional_goal:
        lines.append(f"Brief emotional goal: {normalized_preferences.emotional_goal}")
    if normalized_preferences.constraint_notes:
        lines.append(
            "Brief constraints: "
            + "; ".join(
                _truncate(note, limit=80) for note in normalized_preferences.constraint_notes
            )
        )
    if normalized_preferences.bedtime_safety_concerns:
        lines.append(
            "Bedtime safety guardrails: "
            + "; ".join(
                _truncate(note, limit=80) for note in normalized_preferences.bedtime_safety_concerns
            )
        )
    if normalized_preferences.candidate_motifs:
        lines.append(
            "Brief motifs: "
            + ", ".join(
                _truncate(motif, limit=40) for motif in normalized_preferences.candidate_motifs
            )
        )

    return lines


def _build_latest_detail_summary(snapshot: SessionSnapshot) -> str | None:
    detail_candidates = [
        stage for stage in snapshot.stage_states if stage.detail and stage.last_event_at is not None
    ]
    if not detail_candidates:
        return None

    latest = max(
        detail_candidates,
        key=lambda stage: _normalize_sortable_datetime(stage.last_event_at),
    )
    if latest.stage == snapshot.current_stage:
        return None

    stage_label = get_workflow_stage_definition(latest.stage).label
    return f"Latest saved UI detail: {stage_label}: {_truncate(latest.detail or '')}"


def _find_stage_state(snapshot: SessionSnapshot, stage):
    for item in snapshot.stage_states:
        if item.stage == stage:
            return item

    raise ValueError(f"session {snapshot.id!r} is missing stage state for {stage.value}")


def _truncate(value: str, *, limit: int = 240) -> str:
    if len(value) <= limit:
        return value
    return f"{value[: limit - 3].rstrip()}..."


def _normalize_sortable_datetime(value):
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)

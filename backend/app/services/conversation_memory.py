from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from sqlalchemy.orm import Session

from app.db import EventLogEntry, JobStatus, SessionMemorySnapshot
from app.models import (
    ConversationMemorySnapshotView,
    ConversationMemorySummaryData,
    ConversationMemoryWorkflow,
    NormalizedBriefPreferences,
    WorkflowStageState,
    get_workflow_stage_definition,
)
from app.repositories import (
    SessionAggregate,
    SessionMemorySnapshotRepository,
    StorySessionRepository,
)
from app.services.audio_settings import (
    build_audio_settings_memory_summary,
    build_audio_settings_view,
)

_INTERRUPTION_JOB_STATUSES = {
    JobStatus.PAUSED,
    JobStatus.FAILED,
    JobStatus.CANCELLED,
}


@dataclass(frozen=True)
class _FallbackStageState:
    status: WorkflowStageState = WorkflowStageState.DRAFT
    detail: str | None = None
    updated_at: object | None = None
    last_event: object | None = None


class SessionMemoryService:
    def __init__(self, session: Session):
        self._session = session
        self._sessions = StorySessionRepository(session)
        self._snapshots = SessionMemorySnapshotRepository(session)

    def load_latest_snapshot(self, session_id: str) -> ConversationMemorySnapshotView | None:
        row = self._snapshots.get_latest_for_session(session_id)
        if row is None:
            return None
        return build_conversation_memory_snapshot_view(row)

    def list_snapshots(
        self,
        session_id: str,
        *,
        limit: int = 10,
    ) -> list[ConversationMemorySnapshotView]:
        if limit <= 0:
            raise ValueError("limit must be greater than zero")

        rows = self._snapshots.list_for_session(session_id, limit=limit)
        return [build_conversation_memory_snapshot_view(row) for row in rows]

    def refresh_summary(
        self,
        session_id: str,
        *,
        trigger_event: EventLogEntry | None = None,
    ) -> ConversationMemorySnapshotView | None:
        if trigger_event is not None:
            existing = self._snapshots.get_by_trigger_event_id(trigger_event.id)
            if existing is not None:
                return build_conversation_memory_snapshot_view(existing)

        aggregate = self._sessions.get_aggregate(session_id)
        if aggregate is None:
            return None

        summary_data = build_conversation_memory_summary_data(aggregate)
        summary_payload = summary_data.model_dump(mode="json")
        summary_text = render_conversation_memory_summary(summary_data)
        latest = self._snapshots.get_latest_for_session(session_id)

        if latest is not None and latest.summary_text == summary_text:
            if latest.summary_data == summary_payload:
                return build_conversation_memory_snapshot_view(latest)

        created = self._snapshots.create(
            session_id,
            summary_text=summary_text,
            summary_data=summary_payload,
            trigger_event=trigger_event,
        )
        return build_conversation_memory_snapshot_view(created)


def build_conversation_memory_snapshot_view(
    row: SessionMemorySnapshot,
) -> ConversationMemorySnapshotView:
    return ConversationMemorySnapshotView(
        id=row.id,
        trigger_event_id=row.trigger_event_id,
        trigger_event_type=row.trigger_event_type,
        trigger_event_sequence_number=row.trigger_event_sequence_number,
        summary_text=row.summary_text,
        summary_data=ConversationMemorySummaryData.model_validate(row.summary_data),
        created_at=row.created_at,
    )


def build_conversation_memory_summary_data(
    aggregate: SessionAggregate,
) -> ConversationMemorySummaryData:
    story_session = aggregate.session
    current_stage_state = _find_stage_state(aggregate, story_session.current_stage)
    return ConversationMemorySummaryData(
        session_title=_resolve_display_title(aggregate),
        workflow=ConversationMemoryWorkflow(
            current_stage=story_session.current_stage,
            current_stage_status=current_stage_state.status,
            resume_stage=story_session.resume_stage,
            overall_status=story_session.overall_status,
        ),
        story_decisions=_build_story_decisions(aggregate),
        user_preferences=_build_user_preferences(aggregate),
        unresolved_questions=_build_unresolved_questions(aggregate, current_stage_state),
        active_jobs=_build_active_jobs(aggregate),
    )


def render_conversation_memory_summary(summary: ConversationMemorySummaryData) -> str:
    lines = [
        f"Session title: {summary.session_title}",
        f"Overall status: {summary.workflow.overall_status.value}",
        (
            "Current stage: "
            f"{summary.workflow.current_stage.value} "
            f"({summary.workflow.current_stage_status.value})"
        ),
        f"Resume stage: {summary.workflow.resume_stage.value}",
    ]
    _append_section(lines, "Story decisions", summary.story_decisions)
    _append_section(lines, "User preferences", summary.user_preferences)
    _append_section(lines, "Unresolved questions", summary.unresolved_questions)
    _append_section(lines, "Active jobs", summary.active_jobs)
    return "\n".join(lines)


def _append_section(lines: list[str], title: str, values: list[str]) -> None:
    if not values:
        return

    lines.append(f"{title}:")
    lines.extend(f"- {value}" for value in values)


def _build_story_decisions(aggregate: SessionAggregate) -> list[str]:
    decisions: list[str] = []
    story_session = aggregate.session

    if story_session.selected_genre is not None:
        decisions.append(f"Selected genre: {story_session.selected_genre.label}")

    if story_session.selected_tone_profile is not None:
        decisions.append(f"Selected tone: {story_session.selected_tone_profile.label}")

    if aggregate.active_story_brief is not None:
        decisions.append(
            "Story brief: "
            + _truncate(
                aggregate.active_story_brief.normalized_summary
                or aggregate.active_story_brief.story_idea
                or aggregate.active_story_brief.raw_brief
            )
        )

    if aggregate.selected_pitch is not None:
        decisions.append(f"Selected pitch: {aggregate.selected_pitch.title}")
        decisions.append(f"Pitch logline: {_truncate(aggregate.selected_pitch.logline)}")
        pitch_rationale = _read_selected_pitch_rationale(aggregate.selected_pitch)
        if pitch_rationale is not None:
            decisions.append(f"Pitch refinement note: {_truncate(pitch_rationale)}")

    if aggregate.selected_character_sheet is not None:
        character_line = aggregate.selected_character_sheet.title or "Character sheet selected"
        if aggregate.selected_character_sheet.protagonist_name:
            character_line += (
                f" (protagonist: {aggregate.selected_character_sheet.protagonist_name})"
            )
        if aggregate.selected_character_sheet.summary:
            character_line += f" - {_truncate(aggregate.selected_character_sheet.summary)}"
        decisions.append(character_line)

    if aggregate.selected_beat_sheet is not None and aggregate.selected_beat_sheet.summary:
        decisions.append(f"Beat sheet: {_truncate(aggregate.selected_beat_sheet.summary)}")

    return decisions


def _build_user_preferences(aggregate: SessionAggregate) -> list[str]:
    preferences: list[str] = []
    audio_job = _resolve_audio_resume_job(aggregate)

    if aggregate.active_story_brief is not None:
        preferences.extend(
            _build_brief_preference_lines(aggregate.active_story_brief.normalized_preferences)
        )

    if aggregate.selected_story_setup is not None:
        story_setup_summary = _build_story_setup_summary(aggregate)
        if story_setup_summary is not None:
            preferences.append(story_setup_summary)

    if aggregate.selected_story_setup is not None and aggregate.selected_story_setup.guidance_notes:
        preferences.append(
            "Setup guidance: " + _truncate(aggregate.selected_story_setup.guidance_notes)
        )

    if aggregate.selected_story_outline is not None:
        outline_bits = [
            f"{aggregate.selected_story_outline.outline_kind} outline",
            f"{len(aggregate.selected_story_outline.cards or [])} cards",
        ]
        if aggregate.selected_story_outline.summary:
            outline_bits.append(_truncate(aggregate.selected_story_outline.summary))
        last_change_summary = _read_story_outline_last_change_summary(
            aggregate.selected_story_outline
        )
        if last_change_summary is not None:
            outline_bits.append(_truncate(last_change_summary))
        preferences.append("Story outline: " + ", ".join(outline_bits))

    if audio_job is not None or any(
        getattr(aggregate.session, field_name) is not None
        for field_name in (
            "audio_voice_key",
            "audio_narration_style",
            "audio_playback_speed",
            "audio_include_background_music",
            "audio_music_profile",
            "audio_narration_volume",
            "audio_music_volume",
            "audio_guidance_notes",
        )
    ):
        settings = build_audio_settings_view(
            story_session=aggregate.session,
            latest_audio_job=audio_job,
            composition_segments=aggregate.composition_segments,
            selected_story_setup=aggregate.selected_story_setup,
            selected_story_outline=aggregate.selected_story_outline,
        )
        preferences.append("Narration settings: " + build_audio_settings_memory_summary(settings))

    return preferences


def _read_selected_pitch_rationale(pitch) -> str | None:
    if not isinstance(getattr(pitch, "model_output", None), Mapping):
        return None

    refinement = pitch.model_output.get("refinement")
    if not isinstance(refinement, Mapping):
        return None

    rationale = refinement.get("selection_rationale")
    return rationale if isinstance(rationale, str) and rationale else None


def _read_story_outline_last_change_summary(story_outline) -> str | None:
    if not isinstance(getattr(story_outline, "metadata_json", None), Mapping):
        return None

    summary = story_outline.metadata_json.get("last_change_summary")
    return summary if isinstance(summary, str) and summary else None


def _build_brief_preference_lines(raw_preferences) -> list[str]:
    if raw_preferences is None:
        return []

    preferences = NormalizedBriefPreferences.model_validate(raw_preferences)
    lines: list[str] = []
    if preferences.protagonist_type:
        lines.append(f"Brief protagonist type: {preferences.protagonist_type}")
    if preferences.setting:
        lines.append(f"Brief setting: {preferences.setting}")
    if preferences.emotional_goal:
        lines.append(f"Brief emotional goal: {preferences.emotional_goal}")
    if preferences.constraint_notes:
        lines.append(
            "Brief constraints: "
            + "; ".join(_truncate(note, limit=80) for note in preferences.constraint_notes)
        )
    if preferences.bedtime_safety_concerns:
        lines.append(
            "Bedtime safety guardrails: "
            + "; ".join(_truncate(note, limit=80) for note in preferences.bedtime_safety_concerns)
        )
    if preferences.candidate_motifs:
        lines.append(
            "Brief motifs: "
            + ", ".join(_truncate(motif, limit=40) for motif in preferences.candidate_motifs)
        )

    return lines


def _build_unresolved_questions(
    aggregate: SessionAggregate,
    current_stage_state,
) -> list[str]:
    questions: list[str] = []
    composition_job = _resolve_composition_resume_job(aggregate)
    audio_job = _resolve_audio_resume_job(aggregate)

    if current_stage_state.detail and current_stage_state.status != WorkflowStageState.COMPLETED:
        stage_label = get_workflow_stage_definition(aggregate.session.current_stage).label
        questions.append(
            f"Current {stage_label.lower()} detail: {_truncate(current_stage_state.detail)}"
        )

    needs_regeneration = [
        get_workflow_stage_definition(stage_state.stage).label
        for stage_state in aggregate.session.workflow_stage_states
        if stage_state.status == WorkflowStageState.NEEDS_REGENERATION
    ]
    if needs_regeneration:
        questions.append("Needs regeneration: " + ", ".join(needs_regeneration))

    latest_detail_summary = _build_latest_detail_summary(aggregate)
    if latest_detail_summary is not None:
        questions.append(latest_detail_summary)

    if composition_job is not None:
        interruption = _build_job_interruption_summary(
            kind="Composition",
            status=composition_job.status,
            stop_reason=composition_job.stop_reason,
        )
        if interruption is not None:
            questions.append(interruption)

    if audio_job is not None:
        interruption = _build_job_interruption_summary(
            kind="Audio",
            status=audio_job.status,
            stop_reason=audio_job.stop_reason,
        )
        if interruption is not None:
            questions.append(interruption)

    return questions


def _build_active_jobs(aggregate: SessionAggregate) -> list[str]:
    active_jobs: list[str] = []
    composition_job = _resolve_composition_resume_job(aggregate)
    audio_job = _resolve_audio_resume_job(aggregate)

    if composition_job is not None and composition_job.status in (
        JobStatus.QUEUED,
        JobStatus.IN_PROGRESS,
        JobStatus.PAUSED,
        JobStatus.FAILED,
        JobStatus.CANCELLED,
    ):
        job_summary = (
            f"Composition job: {composition_job.status.value} at "
            f"{composition_job.progress_percent:.1f}%"
        )
        if composition_job.current_segment_index is not None:
            job_summary += f", segment {composition_job.current_segment_index}"
        active_jobs.append(job_summary)

    if audio_job is not None and audio_job.status in (
        JobStatus.QUEUED,
        JobStatus.IN_PROGRESS,
        JobStatus.PAUSED,
        JobStatus.FAILED,
        JobStatus.CANCELLED,
    ):
        job_summary = f"Audio job: {audio_job.status.value}, voice={audio_job.voice_key or 'unset'}"
        if audio_job.current_segment_index is not None:
            job_summary += f", segment {audio_job.current_segment_index}"
        active_jobs.append(job_summary)

    return active_jobs


def _build_story_setup_summary(aggregate: SessionAggregate) -> str | None:
    if aggregate.selected_story_setup is None:
        return None

    setup_bits: list[str] = []
    if aggregate.selected_story_setup.target_word_count is not None:
        setup_bits.append(f"{aggregate.selected_story_setup.target_word_count} words")
    if aggregate.selected_story_setup.target_runtime_minutes is not None:
        setup_bits.append(f"{aggregate.selected_story_setup.target_runtime_minutes} minutes")
    if aggregate.selected_story_setup.chapter_count is not None:
        setup_bits.append(f"{aggregate.selected_story_setup.chapter_count} chapters")
    if aggregate.selected_story_setup.approximate_scene_count is not None:
        setup_bits.append(f"about {aggregate.selected_story_setup.approximate_scene_count} scenes")
    if aggregate.selected_story_setup.chapter_style:
        setup_bits.append(aggregate.selected_story_setup.chapter_style)

    if not setup_bits:
        return None

    return "Story setup: " + ", ".join(setup_bits)


def _build_job_interruption_summary(
    *,
    kind: str,
    status: JobStatus,
    stop_reason: str | None,
) -> str | None:
    if status not in _INTERRUPTION_JOB_STATUSES:
        return None

    if stop_reason:
        return f"{kind} interruption: {status.value} ({_truncate(stop_reason, limit=160)})"

    return f"{kind} interruption: {status.value}"


def _resolve_composition_resume_job(aggregate: SessionAggregate):
    return aggregate.active_composition_job or aggregate.latest_composition_job


def _resolve_audio_resume_job(aggregate: SessionAggregate):
    return aggregate.active_audio_job or aggregate.latest_audio_job


def _find_stage_state(aggregate: SessionAggregate, stage):
    for item in aggregate.session.workflow_stage_states:
        if item.stage == stage:
            return item

    return _FallbackStageState()


def _build_latest_detail_summary(aggregate: SessionAggregate) -> str | None:
    detail_candidates = [
        stage_state for stage_state in aggregate.session.workflow_stage_states if stage_state.detail
    ]
    if not detail_candidates:
        return None

    latest = max(
        detail_candidates,
        key=_stage_detail_sort_key,
    )
    if latest.stage == aggregate.session.current_stage:
        return None

    stage_label = get_workflow_stage_definition(latest.stage).label
    return f"Latest saved UI detail: {stage_label}: {_truncate(latest.detail or '')}"


def _stage_detail_sort_key(stage_state) -> tuple[str, str]:
    last_event_at = (
        stage_state.last_event.created_at.isoformat()
        if getattr(stage_state, "last_event", None) is not None
        else ""
    )
    updated_at = (
        stage_state.updated_at.isoformat()
        if getattr(stage_state, "updated_at", None) is not None
        else ""
    )
    return (last_event_at, updated_at)


def _resolve_display_title(aggregate: SessionAggregate) -> str:
    for candidate in (
        aggregate.session.working_title,
        aggregate.selected_pitch.title if aggregate.selected_pitch is not None else None,
        (
            aggregate.active_story_brief.story_idea
            if aggregate.active_story_brief is not None
            else None
        ),
        (
            aggregate.active_story_brief.normalized_summary
            if aggregate.active_story_brief is not None
            else None
        ),
        (
            aggregate.active_story_brief.raw_brief
            if aggregate.active_story_brief is not None
            else None
        ),
    ):
        normalized = _normalize_optional_text(candidate)
        if normalized:
            return normalized[:120]

    return "Untitled bedtime story"


def _normalize_optional_text(value: str | None) -> str | None:
    if value is None:
        return None

    normalized = value.strip()
    return normalized or None


def _truncate(value: str, *, limit: int = 240) -> str:
    if len(value) <= limit:
        return value
    return f"{value[: limit - 3].rstrip()}..."

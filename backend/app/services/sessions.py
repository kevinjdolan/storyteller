from __future__ import annotations

from collections.abc import Mapping

from sqlalchemy.orm import Session

from app.db import (
    AudioJob,
    BeatSheet,
    CharacterSheet,
    CompositionJob,
    ExportAsset,
    StoryBrief,
)
from app.db.base import utc_now
from app.models import (
    WORKFLOW_STAGE_SEQUENCE,
    AudioJobView,
    BeatSheetView,
    CharacterSheetView,
    CompositionJobView,
    ExportAssetView,
    PitchView,
    RecentSessionSummary,
    SessionCatalogSelection,
    SessionEventActor,
    SessionHistoryView,
    SessionProgress,
    SessionSnapshot,
    SessionStageStateView,
    StoryBriefView,
    StorySetupView,
    WorkflowStage,
    WorkflowStageState,
    get_invalidated_stages_after_edit,
    get_workflow_stage_definition,
    resolve_resume_stage,
)
from app.repositories import (
    SessionAggregate,
    StorySessionRepository,
    WorkflowStageStateRepository,
)
from app.services.event_log import SessionEventLogService


class SessionServiceError(Exception):
    """Base error for session service failures."""


class SessionNotFoundError(SessionServiceError):
    """Raised when a requested session does not exist."""


class InvalidStageTransitionError(SessionServiceError):
    """Raised when a stage update violates workflow rules."""


class SessionService:
    def __init__(self, session: Session):
        self._session = session
        self._sessions = StorySessionRepository(session)
        self._stage_states = WorkflowStageStateRepository(session)
        self._event_log = SessionEventLogService(session)

    def create_session(
        self,
        *,
        working_title: str | None = None,
        actor: SessionEventActor | None = None,
    ) -> SessionSnapshot:
        story_session = self._sessions.create(working_title=_normalize_optional_text(working_title))
        stage_map = self._stage_states.ensure_for_session(story_session)
        self._apply_rollups(story_session, stage_map)
        self._event_log.record_session_created(
            story_session.id,
            working_title=story_session.working_title,
            actor=actor,
        )
        self._session.commit()
        return self.load_session_snapshot(story_session.id)

    def load_session_snapshot(self, session_id: str) -> SessionSnapshot:
        aggregate = self._sessions.get_aggregate(session_id)
        if aggregate is None:
            raise SessionNotFoundError(f"session {session_id!r} was not found")

        return _build_session_snapshot(aggregate)

    def list_recent_sessions(self, *, limit: int = 20) -> list[RecentSessionSummary]:
        if limit <= 0:
            raise ValueError("limit must be greater than zero")

        sessions = self._sessions.list_recent(limit=limit)
        return [_build_recent_session_summary(story_session) for story_session in sessions]

    def load_session_history(
        self,
        session_id: str,
        *,
        limit: int | None = None,
        after_sequence_number: int | None = None,
    ) -> SessionHistoryView:
        if limit is not None and limit <= 0:
            raise ValueError("limit must be greater than zero")

        if not self._sessions.exists(session_id):
            raise SessionNotFoundError(f"session {session_id!r} was not found")

        return self._event_log.list_session_history(
            session_id,
            limit=limit,
            after_sequence_number=after_sequence_number,
        )

    def update_stage_state(
        self,
        session_id: str,
        *,
        stage: WorkflowStage,
        status: WorkflowStageState,
        detail: str | None = None,
        actor: SessionEventActor | None = None,
    ) -> SessionSnapshot:
        story_session = self._sessions.get_for_update(session_id)
        if story_session is None:
            raise SessionNotFoundError(f"session {session_id!r} was not found")

        stage_map = self._stage_states.ensure_for_session(story_session)
        self._validate_stage_transition(stage_map, stage=stage, status=status)

        snapshot = stage_map[stage]
        previous_status = snapshot.status
        now = utc_now()
        snapshot.detail = _normalize_optional_text(detail)
        invalidated_stages: list[WorkflowStage] = []

        if status == WorkflowStageState.DRAFT:
            snapshot.status = WorkflowStageState.DRAFT
            snapshot.started_at = None
            snapshot.completed_at = None
        elif status == WorkflowStageState.IN_PROGRESS:
            snapshot.status = WorkflowStageState.IN_PROGRESS
            snapshot.started_at = snapshot.started_at or now
            snapshot.completed_at = None
        elif status == WorkflowStageState.COMPLETED:
            snapshot.status = WorkflowStageState.COMPLETED
            snapshot.started_at = snapshot.started_at or now
            snapshot.completed_at = now
            invalidated_stages = self._invalidate_dependent_stages(
                stage_map,
                stage=stage,
                detail=snapshot.detail,
            )
        else:
            snapshot.status = WorkflowStageState.NEEDS_REGENERATION
            invalidated_stages = self._invalidate_dependent_stages(
                stage_map,
                stage=stage,
                detail=snapshot.detail,
            )

        self._apply_rollups(story_session, stage_map)
        stage_event = self._event_log.record_stage_state_changed(
            story_session.id,
            stage=stage,
            previous_status=previous_status,
            status=snapshot.status,
            detail=snapshot.detail,
            invalidated_stages=invalidated_stages,
            current_stage=story_session.current_stage,
            resume_stage=story_session.resume_stage,
            furthest_completed_stage=story_session.furthest_completed_stage,
            overall_status=story_session.overall_status,
            actor=actor,
        )
        snapshot.last_event = stage_event
        for invalidated_stage in invalidated_stages:
            stage_map[invalidated_stage].last_event = stage_event
        self._session.commit()
        return self.load_session_snapshot(story_session.id)

    def _validate_stage_transition(
        self,
        stage_map: Mapping[WorkflowStage, object],
        *,
        stage: WorkflowStage,
        status: WorkflowStageState,
    ) -> None:
        if status in {WorkflowStageState.IN_PROGRESS, WorkflowStageState.COMPLETED}:
            incomplete_prerequisites = [
                prior_stage.value
                for prior_stage in _stages_before(stage)
                if getattr(stage_map[prior_stage], "status") != WorkflowStageState.COMPLETED
            ]
            if incomplete_prerequisites:
                joined = ", ".join(incomplete_prerequisites)
                raise InvalidStageTransitionError(
                    f"cannot set {stage.value!r} to {status.value!r} before prerequisites are "
                    f"completed: {joined}"
                )

        if status == WorkflowStageState.NEEDS_REGENERATION and stage == WorkflowStage.GENRE:
            raise InvalidStageTransitionError("genre cannot be marked needs_regeneration directly")

    def _invalidate_dependent_stages(
        self,
        stage_map: Mapping[WorkflowStage, object],
        *,
        stage: WorkflowStage,
        detail: str | None,
    ) -> list[WorkflowStage]:
        if stage == WorkflowStage.FINALIZE:
            return []

        reason = detail or f"Needs regeneration after {stage.value} changed."
        invalidated_stages: list[WorkflowStage] = []

        for invalidated_stage in get_invalidated_stages_after_edit(stage):
            snapshot = stage_map[invalidated_stage]
            if getattr(snapshot, "status") == WorkflowStageState.DRAFT:
                continue

            snapshot.status = WorkflowStageState.NEEDS_REGENERATION
            snapshot.detail = reason
            invalidated_stages.append(invalidated_stage)

        return invalidated_stages

    def _apply_rollups(
        self,
        story_session,
        stage_map: Mapping[WorkflowStage, object],
    ) -> None:
        statuses = {
            stage: getattr(stage_map[stage], "status")
            for stage in stage_map
        }
        resume_stage = resolve_resume_stage(statuses)
        furthest_completed_stage = _resolve_furthest_completed_stage(statuses)
        overall_status = _resolve_overall_status(statuses)

        story_session.current_stage = resume_stage
        story_session.resume_stage = resume_stage
        story_session.furthest_completed_stage = furthest_completed_stage
        story_session.overall_status = overall_status
        story_session.completed_at = (
            utc_now() if overall_status == WorkflowStageState.COMPLETED else None
        )


def _build_recent_session_summary(story_session) -> RecentSessionSummary:
    return RecentSessionSummary(
        id=story_session.id,
        display_title=_resolve_display_title(working_title=story_session.working_title),
        working_title=story_session.working_title,
        current_stage=story_session.current_stage,
        resume_stage=story_session.resume_stage,
        furthest_completed_stage=story_session.furthest_completed_stage,
        overall_status=story_session.overall_status,
        created_at=story_session.created_at,
        updated_at=story_session.updated_at,
        completed_at=story_session.completed_at,
        selected_genre=_build_catalog_selection(story_session.selected_genre),
        selected_tone_profile=_build_catalog_selection(story_session.selected_tone_profile),
        progress=_build_progress(story_session.workflow_stage_states),
    )


def _build_session_snapshot(aggregate: SessionAggregate) -> SessionSnapshot:
    story_session = aggregate.session
    return SessionSnapshot(
        id=story_session.id,
        display_title=_resolve_display_title(
            working_title=story_session.working_title,
            pitch_title=aggregate.selected_pitch.title if aggregate.selected_pitch else None,
            normalized_summary=(
                aggregate.active_story_brief.normalized_summary
                if aggregate.active_story_brief
                else None
            ),
            raw_brief=(
                aggregate.active_story_brief.raw_brief
                if aggregate.active_story_brief
                else None
            ),
        ),
        working_title=story_session.working_title,
        current_stage=story_session.current_stage,
        resume_stage=story_session.resume_stage,
        furthest_completed_stage=story_session.furthest_completed_stage,
        overall_status=story_session.overall_status,
        created_at=story_session.created_at,
        updated_at=story_session.updated_at,
        completed_at=story_session.completed_at,
        selected_genre=_build_catalog_selection(story_session.selected_genre),
        selected_tone_profile=_build_catalog_selection(story_session.selected_tone_profile),
        progress=_build_progress(story_session.workflow_stage_states),
        stage_states=_build_stage_state_views(story_session.workflow_stage_states),
        story_brief=_build_story_brief_view(aggregate.active_story_brief),
        selected_pitch=_build_pitch_view(aggregate.selected_pitch),
        selected_character_sheet=_build_character_sheet_view(aggregate.selected_character_sheet),
        selected_beat_sheet=_build_beat_sheet_view(aggregate.selected_beat_sheet),
        selected_story_setup=_build_story_setup_view(aggregate.selected_story_setup),
        active_composition_job=_build_composition_job_view(aggregate.active_composition_job),
        active_audio_job=_build_audio_job_view(aggregate.active_audio_job),
        latest_story_asset=_build_export_asset_view(aggregate.latest_story_asset),
        latest_audio_asset=_build_export_asset_view(aggregate.latest_audio_asset),
    )


def _build_catalog_selection(row) -> SessionCatalogSelection | None:
    if row is None:
        return None

    return SessionCatalogSelection(
        id=row.id,
        slug=row.slug,
        label=row.label,
    )


def _build_progress(stage_states) -> SessionProgress:
    stage_state_map = {stage_state.stage: stage_state for stage_state in stage_states}
    completed_stages = sum(
        1
        for stage in WORKFLOW_STAGE_SEQUENCE
        if stage_state_map.get(stage, None)
        and stage_state_map[stage].status == WorkflowStageState.COMPLETED
    )
    in_progress_stages = sum(
        1
        for stage in WORKFLOW_STAGE_SEQUENCE
        if stage_state_map.get(stage, None)
        and stage_state_map[stage].status == WorkflowStageState.IN_PROGRESS
    )
    needs_regeneration_stages = sum(
        1
        for stage in WORKFLOW_STAGE_SEQUENCE
        if stage_state_map.get(stage, None)
        and stage_state_map[stage].status == WorkflowStageState.NEEDS_REGENERATION
    )
    return SessionProgress(
        total_stages=len(WORKFLOW_STAGE_SEQUENCE),
        completed_stages=completed_stages,
        in_progress_stages=in_progress_stages,
        needs_regeneration_stages=needs_regeneration_stages,
    )


def _build_stage_state_views(stage_states) -> list[SessionStageStateView]:
    stage_state_map = {stage_state.stage: stage_state for stage_state in stage_states}
    views: list[SessionStageStateView] = []

    for stage in WorkflowStage:
        definition = get_workflow_stage_definition(stage)
        snapshot = stage_state_map.get(stage)
        views.append(
            SessionStageStateView(
                stage=stage,
                label=definition.label,
                description=definition.description,
                status=snapshot.status if snapshot else WorkflowStageState.DRAFT,
                detail=snapshot.detail if snapshot else None,
                started_at=snapshot.started_at if snapshot else None,
                completed_at=snapshot.completed_at if snapshot else None,
                last_event_summary=(
                    snapshot.last_event.summary if snapshot and snapshot.last_event else None
                ),
                last_event_type=(
                    snapshot.last_event.event_type if snapshot and snapshot.last_event else None
                ),
                last_event_at=(
                    snapshot.last_event.created_at if snapshot and snapshot.last_event else None
                ),
            )
        )

    return views


def _build_story_brief_view(row: StoryBrief | None) -> StoryBriefView | None:
    if row is None:
        return None

    return StoryBriefView(
        id=row.id,
        revision_number=row.revision_number,
        raw_brief=row.raw_brief,
        normalized_summary=row.normalized_summary,
        planning_notes=row.planning_notes,
        accepted_at=row.accepted_at,
    )


def _build_pitch_view(row) -> PitchView | None:
    if row is None:
        return None

    return PitchView(
        id=row.id,
        generation_key=row.generation_key,
        pitch_index=row.pitch_index,
        title=row.title,
        logline=row.logline,
        summary=row.summary,
        bedtime_notes=row.bedtime_notes,
        accepted_at=row.accepted_at,
    )


def _build_character_sheet_view(row: CharacterSheet | None) -> CharacterSheetView | None:
    if row is None:
        return None

    return CharacterSheetView(
        id=row.id,
        revision_number=row.revision_number,
        title=row.title,
        protagonist_name=row.protagonist_name,
        summary=row.summary,
        supporting_cast=row.supporting_cast,
        bedtime_notes=row.bedtime_notes,
        accepted_at=row.accepted_at,
    )


def _build_beat_sheet_view(row: BeatSheet | None) -> BeatSheetView | None:
    if row is None:
        return None

    return BeatSheetView(
        id=row.id,
        revision_number=row.revision_number,
        summary=row.summary,
        beats=row.beats,
        bedtime_notes=row.bedtime_notes,
        accepted_at=row.accepted_at,
    )


def _build_story_setup_view(row) -> StorySetupView | None:
    if row is None:
        return None

    return StorySetupView(
        id=row.id,
        revision_number=row.revision_number,
        target_word_count=row.target_word_count,
        target_runtime_minutes=row.target_runtime_minutes,
        chapter_count=row.chapter_count,
        chapter_style=row.chapter_style,
        guidance_notes=row.guidance_notes,
        preferences=row.preferences,
        accepted_at=row.accepted_at,
    )


def _build_composition_job_view(row: CompositionJob | None) -> CompositionJobView | None:
    if row is None:
        return None

    return CompositionJobView(
        id=row.id,
        job_kind=row.job_kind,
        status=row.status,
        progress_percent=row.progress_percent,
        current_segment_index=row.current_segment_index,
        attempt_count=row.attempt_count,
        stop_reason=row.stop_reason,
        error_message=row.error_message,
        started_at=row.started_at,
        completed_at=row.completed_at,
        created_at=row.created_at,
        updated_at=row.updated_at,
    )


def _build_audio_job_view(row: AudioJob | None) -> AudioJobView | None:
    if row is None:
        return None

    return AudioJobView(
        id=row.id,
        status=row.status,
        voice_key=row.voice_key,
        playback_speed=row.playback_speed,
        include_background_music=row.include_background_music,
        music_profile=row.music_profile,
        estimated_duration_seconds=row.estimated_duration_seconds,
        current_segment_index=row.current_segment_index,
        attempt_count=row.attempt_count,
        stop_reason=row.stop_reason,
        error_message=row.error_message,
        started_at=row.started_at,
        completed_at=row.completed_at,
        created_at=row.created_at,
        updated_at=row.updated_at,
    )


def _build_export_asset_view(row: ExportAsset | None) -> ExportAssetView | None:
    if row is None:
        return None

    return ExportAssetView(
        id=row.id,
        asset_kind=row.asset_kind,
        status=row.status,
        mime_type=row.mime_type,
        byte_size=row.byte_size,
        ready_at=row.ready_at,
        created_at=row.created_at,
        updated_at=row.updated_at,
    )


def _resolve_display_title(
    *,
    working_title: str | None,
    pitch_title: str | None = None,
    normalized_summary: str | None = None,
    raw_brief: str | None = None,
) -> str:
    for candidate in (working_title, pitch_title, normalized_summary, raw_brief):
        normalized = _normalize_optional_text(candidate)
        if normalized:
            return normalized[:120]

    return "Untitled bedtime story"


def _normalize_optional_text(value: str | None) -> str | None:
    if value is None:
        return None

    normalized = value.strip()
    return normalized or None


def _resolve_overall_status(
    stage_states: Mapping[WorkflowStage, WorkflowStageState],
) -> WorkflowStageState:
    statuses = tuple(stage_states.values())
    if any(status == WorkflowStageState.NEEDS_REGENERATION for status in statuses):
        return WorkflowStageState.NEEDS_REGENERATION
    if stage_states.get(WorkflowStage.FINALIZE) == WorkflowStageState.COMPLETED:
        return WorkflowStageState.COMPLETED
    if any(status == WorkflowStageState.IN_PROGRESS for status in statuses):
        return WorkflowStageState.IN_PROGRESS
    if any(status == WorkflowStageState.COMPLETED for status in statuses):
        return WorkflowStageState.IN_PROGRESS
    return WorkflowStageState.DRAFT


def _resolve_furthest_completed_stage(
    stage_states: Mapping[WorkflowStage, WorkflowStageState],
) -> WorkflowStage | None:
    furthest_stage: WorkflowStage | None = None
    for stage in WORKFLOW_STAGE_SEQUENCE:
        if stage_states.get(stage) == WorkflowStageState.COMPLETED:
            furthest_stage = stage

    return furthest_stage


def _stages_before(stage: WorkflowStage) -> tuple[WorkflowStage, ...]:
    stages = WORKFLOW_STAGE_SEQUENCE
    return stages[: stages.index(stage)]

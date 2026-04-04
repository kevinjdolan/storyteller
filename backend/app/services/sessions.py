from __future__ import annotations

from collections.abc import Mapping
from time import perf_counter
from typing import Any
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import (
    AudioJob,
    BeatSheet,
    CharacterSheet,
    CompositionJob,
    JobStatus,
    Pitch,
    StoryBrief,
    StoryOutline,
    StorySetup,
)
from app.db.base import utc_now
from app.models import (
    WORKFLOW_STAGE_SEQUENCE,
    AIOutputKind,
    CharacterChangeImpact,
    EditSessionBeatSheetRequest,
    ExistingBeatSheetContext,
    ExistingCharacterSheetContext,
    ExistingSelectedPitchContext,
    ModelCallOutcome,
    ModelUsageBucket,
    NormalizedBriefPreferences,
    RecentSessionSummary,
    SaveSessionAudioSettingsRequest,
    SelectionKind,
    SessionAudioSettingsResponse,
    SessionBeatSheetGenerationResponse,
    SessionBeatSheetUpdateResponse,
    SessionCharacterSheetGenerationResponse,
    SessionContextUpdateRequest,
    SessionContextUpdateResponse,
    SessionDebugInspectorView,
    SessionEventActor,
    SessionEventView,
    SessionHistoryView,
    SessionPitchGenerationResponse,
    SessionSelectionResponse,
    SessionSnapshot,
    SessionStoryBriefResponse,
    SessionUsageDiagnosticsView,
    StoryBriefEditMode,
    UserEditTargetKind,
    WorkflowStage,
    WorkflowStageState,
    get_invalidated_stages_after_edit,
    get_workflow_stage_definition,
    resolve_resume_stage,
)
from app.repositories import StorySessionRepository, WorkflowStageStateRepository
from app.services.artifact_inventory import SessionArtifactInventoryService
from app.services.audio_settings import (
    audio_settings_field_values,
    build_audio_runtime_estimate,
    build_audio_settings_event_summary,
    build_audio_settings_stage_detail,
    build_audio_settings_view,
    hydrate_audio_settings_view,
    persist_audio_settings,
)
from app.services.beat_sheet_generation import (
    BeatSheetGenerationService,
    build_beat_sheet_model_output,
)
from app.services.brief_normalization import (
    BriefNormalizationService,
    apply_brief_normalization_overrides,
    build_brief_model_output,
    build_brief_normalization_result_from_existing,
)
from app.services.catalog import find_active_genre, find_active_tone_for_genre
from app.services.character_generation import (
    CharacterGenerationService,
    build_character_model_output,
)
from app.services.character_sheet_changes import infer_character_change_impact
from app.services.continuity import SessionContinuityService
from app.services.event_log import SessionEventLogService
from app.services.model_usage import ModelUsageContext, SessionModelUsageService
from app.services.pitch_generation import PitchGenerationService, build_pitch_model_output
from app.services.plan_revisions import PlanRevisionService
from app.services.session_hydration import (
    SessionHydrationNotFoundError,
    SessionHydrationService,
    build_recent_session_summary,
    resolve_furthest_completed_stage,
    resolve_overall_status,
)


class SessionServiceError(Exception):
    """Base error for session service failures."""


class SessionNotFoundError(SessionServiceError):
    """Raised when a requested session does not exist."""


class InvalidStageTransitionError(SessionServiceError):
    """Raised when a stage update violates workflow rules."""


class UnsupportedSessionContextUpdateError(SessionServiceError):
    """Raised when a UI-originated context update is not supported."""


class SessionGenreSelectionError(SessionServiceError):
    """Raised when a genre selection request cannot be fulfilled."""


class SessionToneSelectionError(SessionServiceError):
    """Raised when a tone selection request cannot be fulfilled."""


class SessionStoryBriefSaveError(SessionServiceError):
    """Raised when a story brief save request cannot be fulfilled."""


class SessionAudioSettingsSaveError(SessionServiceError):
    """Raised when an audio-settings save request cannot be fulfilled."""


class SessionPitchGenerationError(SessionServiceError):
    """Raised when a pitch generation request cannot be fulfilled."""


class SessionPitchSelectionError(SessionServiceError):
    """Raised when a pitch selection request cannot be fulfilled."""


class SessionCharacterSheetGenerationError(SessionServiceError):
    """Raised when a character-sheet generation request cannot be fulfilled."""


class SessionCharacterSheetSelectionError(SessionServiceError):
    """Raised when a character-sheet selection request cannot be fulfilled."""


class SessionBeatSheetGenerationError(SessionServiceError):
    """Raised when a beat-sheet generation request cannot be fulfilled."""


class SessionBeatSheetSelectionError(SessionServiceError):
    """Raised when a beat-sheet selection request cannot be fulfilled."""


class SessionBeatSheetEditError(SessionServiceError):
    """Raised when a beat-sheet edit request cannot be fulfilled."""


class SessionPlanRevisionError(SessionServiceError):
    """Raised when a plan-revision restore request cannot be fulfilled."""


STAGE_EDIT_TARGET_KIND_MAP: dict[WorkflowStage, UserEditTargetKind] = {
    WorkflowStage.BRIEF: UserEditTargetKind.STORY_BRIEF,
    WorkflowStage.PITCHES: UserEditTargetKind.PITCH,
    WorkflowStage.CHARACTERS: UserEditTargetKind.CHARACTER_SHEET,
    WorkflowStage.BEATS: UserEditTargetKind.BEAT_SHEET,
    WorkflowStage.STORY_SETUP: UserEditTargetKind.STORY_SETUP,
    WorkflowStage.COMPOSITION: UserEditTargetKind.COMPOSITION_SEGMENT,
    WorkflowStage.AUDIO: UserEditTargetKind.AUDIO_SETTINGS,
}


class SessionService:
    def __init__(
        self,
        session: Session,
        *,
        brief_normalization_service: BriefNormalizationService | None = None,
    ):
        self._session = session
        self._sessions = StorySessionRepository(session)
        self._stage_states = WorkflowStageStateRepository(session)
        self._event_log = SessionEventLogService(session)
        self._continuity = SessionContinuityService(session)
        self._plan_revisions = PlanRevisionService(session)
        self._brief_normalizer = brief_normalization_service or BriefNormalizationService()

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
        try:
            return SessionHydrationService(self._session).load_session_snapshot(session_id)
        except SessionHydrationNotFoundError as exc:
            raise SessionNotFoundError(f"session {session_id!r} was not found") from exc

    def list_recent_sessions(
        self,
        *,
        limit: int = 20,
        query: str | None = None,
        status_filter: str | None = None,
        genre_slug: str | None = None,
    ) -> list[RecentSessionSummary]:
        if limit <= 0:
            raise ValueError("limit must be greater than zero")

        sessions = self._sessions.list_recent_library_records(
            limit=limit,
            query=query,
            status_filter=status_filter,
            genre_slug=genre_slug,
        )
        return [
            build_recent_session_summary(
                record.session,
                active_story_brief=record.active_story_brief,
                selected_pitch=record.selected_pitch,
                selected_story_setup=record.selected_story_setup,
                latest_audio_job=record.latest_audio_job,
                latest_story_asset=record.latest_story_asset,
                latest_story_export_asset=record.latest_story_export_asset,
                latest_audio_asset=record.latest_audio_asset,
            )
            for record in sessions
        ]

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

    def load_session_usage_diagnostics(
        self,
        session_id: str,
        *,
        recent_limit: int = 20,
        leaderboard_limit: int = 5,
    ) -> SessionUsageDiagnosticsView:
        if recent_limit <= 0:
            raise ValueError("recent_limit must be greater than zero")
        if leaderboard_limit <= 0:
            raise ValueError("leaderboard_limit must be greater than zero")
        if not self._sessions.exists(session_id):
            raise SessionNotFoundError(f"session {session_id!r} was not found")

        return SessionModelUsageService(self._session).load_session_diagnostics(
            session_id,
            recent_limit=recent_limit,
            leaderboard_limit=leaderboard_limit,
        )

    def load_session_debug_inspector(
        self,
        session_id: str,
        *,
        history_limit: int = 100,
        usage_recent_limit: int = 20,
        usage_leaderboard_limit: int = 5,
    ) -> SessionDebugInspectorView:
        if history_limit <= 0:
            raise ValueError("history_limit must be greater than zero")
        if usage_recent_limit <= 0:
            raise ValueError("usage_recent_limit must be greater than zero")
        if usage_leaderboard_limit <= 0:
            raise ValueError("usage_leaderboard_limit must be greater than zero")

        if not self._sessions.exists(session_id):
            raise SessionNotFoundError(f"session {session_id!r} was not found")

        hydration = SessionHydrationService(self._session).hydrate_session(
            session_id,
            history_limit=history_limit,
        )
        artifact_inventory = SessionArtifactInventoryService(self._session).load_inventory(
            session_id,
        )
        usage_diagnostics = SessionModelUsageService(self._session).load_session_diagnostics(
            session_id,
            recent_limit=usage_recent_limit,
            leaderboard_limit=usage_leaderboard_limit,
        )

        return SessionDebugInspectorView(
            session_id=session_id,
            generated_at=utc_now(),
            snapshot=hydration.snapshot,
            hydration=hydration.hydration,
            recent_history=hydration.recent_history,
            artifact_inventory=artifact_inventory,
            usage_diagnostics=usage_diagnostics,
        )

    def record_ui_action(
        self,
        session_id: str,
        *,
        action: str,
        stage: WorkflowStage | None = None,
        control_id: str | None = None,
        value_summary: str | None = None,
        origin: str = "workspace",
        actor: SessionEventActor | None = None,
    ) -> SessionEventView:
        if not self._sessions.exists(session_id):
            raise SessionNotFoundError(f"session {session_id!r} was not found")

        event = self._event_log.record_ui_action(
            session_id,
            action=action,
            stage=stage,
            control_id=control_id,
            value_summary=value_summary,
            origin=origin,
            actor=actor,
        )
        self._session.commit()
        return self._event_log.build_event_view(event)

    def select_genre(
        self,
        session_id: str,
        *,
        genre_id: str | None = None,
        genre_slug: str | None = None,
        genre_label: str | None = None,
        origin: str = "workspace",
        actor: SessionEventActor | None = None,
    ) -> SessionSelectionResponse:
        story_session = self._sessions.get_for_update(session_id)
        if story_session is None:
            raise SessionNotFoundError(f"session {session_id!r} was not found")

        selected_count = sum(value is not None for value in (genre_id, genre_slug, genre_label))
        if selected_count != 1:
            raise ValueError("exactly one genre selector is required")

        genre = self._load_active_genre(
            genre_id=genre_id,
            genre_slug=genre_slug,
            genre_label=genre_label,
        )
        if genre is None:
            raise SessionGenreSelectionError("no active genre matched the requested selection")

        previous_genre_id = story_session.selected_genre_id
        previous_tone_profile = story_session.selected_tone_profile
        if previous_tone_profile is not None and previous_tone_profile.genre_id != genre.id:
            story_session.selected_tone_profile = None

        story_session.selected_genre = genre
        stage_map = self._stage_states.ensure_for_session(story_session)
        stage_snapshot = stage_map[WorkflowStage.GENRE]
        previous_status = stage_snapshot.status
        now = utc_now()

        selection_detail = _build_genre_selection_detail(genre.label)
        stage_snapshot.status = WorkflowStageState.COMPLETED
        stage_snapshot.detail = selection_detail
        stage_snapshot.started_at = stage_snapshot.started_at or now
        stage_snapshot.completed_at = now

        invalidation_detail = _build_genre_invalidation_detail(genre.label)
        invalidated_stages = self._invalidate_dependent_stages(
            stage_map,
            stage=WorkflowStage.GENRE,
            detail=invalidation_detail,
        )
        self._apply_rollups(story_session, stage_map)

        stage_event = None
        if previous_status != stage_snapshot.status or invalidated_stages:
            stage_event = self._event_log.record_stage_state_changed(
                story_session.id,
                stage=WorkflowStage.GENRE,
                previous_status=previous_status,
                status=stage_snapshot.status,
                detail=stage_snapshot.detail,
                invalidated_stages=invalidated_stages,
                current_stage=story_session.current_stage,
                resume_stage=story_session.resume_stage,
                furthest_completed_stage=story_session.furthest_completed_stage,
                overall_status=story_session.overall_status,
                actor=actor,
            )
            for invalidated_stage in invalidated_stages:
                stage_map[invalidated_stage].last_event = stage_event

        selection_event = self._event_log.record_selection(
            story_session.id,
            selection_kind=SelectionKind.GENRE,
            stage=WorkflowStage.GENRE,
            label=genre.label,
            selection_id=genre.id,
            slug=genre.slug,
            previous_selection_id=previous_genre_id,
            source=origin,
            accepted=True,
            actor=actor,
        )
        self._refresh_continuity(
            story_session.id,
            source_stage=WorkflowStage.GENRE,
            source_summary=selection_event.summary,
        )
        stage_snapshot.last_event = selection_event
        self._session.commit()
        return SessionSelectionResponse(
            snapshot=self.load_session_snapshot(story_session.id),
            event=self._event_log.build_event_view(selection_event),
        )

    def select_tone(
        self,
        session_id: str,
        *,
        tone_profile_id: str | None = None,
        tone_profile_slug: str | None = None,
        tone_profile_label: str | None = None,
        origin: str = "workspace",
        actor: SessionEventActor | None = None,
    ) -> SessionSelectionResponse:
        story_session = self._sessions.get_for_update(session_id)
        if story_session is None:
            raise SessionNotFoundError(f"session {session_id!r} was not found")

        selected_count = sum(
            value is not None for value in (tone_profile_id, tone_profile_slug, tone_profile_label)
        )
        if selected_count != 1:
            raise ValueError("exactly one tone selector is required")

        if story_session.selected_genre_id is None:
            raise SessionToneSelectionError("select a genre before choosing a tone")

        tone_profile = self._load_active_tone_for_genre(
            genre_id=story_session.selected_genre_id,
            tone_profile_id=tone_profile_id,
            tone_profile_slug=tone_profile_slug,
            tone_profile_label=tone_profile_label,
        )
        if tone_profile is None:
            raise SessionToneSelectionError(
                "no active tone matched the requested selection for the current genre"
            )

        previous_tone_profile_id = story_session.selected_tone_profile_id
        story_session.selected_tone_profile = tone_profile
        stage_map = self._stage_states.ensure_for_session(story_session)
        stage_snapshot = stage_map[WorkflowStage.TONE]
        previous_status = stage_snapshot.status
        now = utc_now()

        selection_detail = _build_tone_selection_detail(tone_profile.label)
        stage_snapshot.status = WorkflowStageState.COMPLETED
        stage_snapshot.detail = selection_detail
        stage_snapshot.started_at = stage_snapshot.started_at or now
        stage_snapshot.completed_at = now

        invalidation_detail = _build_tone_invalidation_detail(tone_profile.label)
        invalidated_stages = self._invalidate_dependent_stages(
            stage_map,
            stage=WorkflowStage.TONE,
            detail=invalidation_detail,
        )
        self._apply_rollups(story_session, stage_map)

        stage_event = None
        if previous_status != stage_snapshot.status or invalidated_stages:
            stage_event = self._event_log.record_stage_state_changed(
                story_session.id,
                stage=WorkflowStage.TONE,
                previous_status=previous_status,
                status=stage_snapshot.status,
                detail=stage_snapshot.detail,
                invalidated_stages=invalidated_stages,
                current_stage=story_session.current_stage,
                resume_stage=story_session.resume_stage,
                furthest_completed_stage=story_session.furthest_completed_stage,
                overall_status=story_session.overall_status,
                actor=actor,
            )
            for invalidated_stage in invalidated_stages:
                stage_map[invalidated_stage].last_event = stage_event

        selection_event = self._event_log.record_selection(
            story_session.id,
            selection_kind=SelectionKind.TONE_PROFILE,
            stage=WorkflowStage.TONE,
            label=tone_profile.label,
            selection_id=tone_profile.id,
            slug=tone_profile.slug,
            previous_selection_id=previous_tone_profile_id,
            source=origin,
            accepted=True,
            actor=actor,
        )
        self._refresh_continuity(
            story_session.id,
            source_stage=WorkflowStage.TONE,
            source_summary=selection_event.summary,
        )
        stage_snapshot.last_event = selection_event
        self._session.commit()
        return SessionSelectionResponse(
            snapshot=self.load_session_snapshot(story_session.id),
            event=self._event_log.build_event_view(selection_event),
        )

    def save_story_brief(
        self,
        session_id: str,
        *,
        story_idea: str | None = None,
        desired_themes: str | None = None,
        key_images: str | None = None,
        audience_notes: str | None = None,
        must_have_elements: str | None = None,
        raw_brief: str | None = None,
        normalized_summary: str | None = None,
        normalized_preferences: NormalizedBriefPreferences | None = None,
        planning_notes: str | None = None,
        edit_mode: StoryBriefEditMode = StoryBriefEditMode.REPLACE,
        origin: str = "workspace",
        actor: SessionEventActor | None = None,
        provided_fields: set[str] | None = None,
    ) -> SessionStoryBriefResponse:
        story_session = self._sessions.get_for_update(session_id)
        if story_session is None:
            raise SessionNotFoundError(f"session {session_id!r} was not found")

        current_brief = self._sessions.get_active_story_brief(session_id)
        provided_fields = provided_fields or set()
        resolved_brief = _resolve_story_brief_revision(
            current_brief,
            story_idea=story_idea,
            desired_themes=desired_themes,
            key_images=key_images,
            audience_notes=audience_notes,
            must_have_elements=must_have_elements,
            raw_brief=raw_brief,
            planning_notes=planning_notes,
            edit_mode=edit_mode,
        )
        raw_brief_changed = (
            current_brief is None or current_brief.raw_brief != resolved_brief["raw_brief"]
        )
        normalized_summary_provided = "normalized_summary" in provided_fields
        normalized_preferences_provided = "normalized_preferences" in provided_fields

        if (
            not raw_brief_changed
            and current_brief is not None
            and (
                current_brief.normalized_summary is not None
                or current_brief.normalized_preferences is not None
            )
        ):
            normalization_result = build_brief_normalization_result_from_existing(
                normalized_summary=current_brief.normalized_summary,
                normalized_preferences=current_brief.normalized_preferences,
                model_output=current_brief.model_output,
            )
        else:
            normalization_started_at = perf_counter()
            normalization_result = self._brief_normalizer.normalize_brief(
                raw_brief=resolved_brief["raw_brief"],
                genre_label=(
                    story_session.selected_genre.label
                    if story_session.selected_genre is not None
                    else None
                ),
                tone_label=(
                    story_session.selected_tone_profile.label
                    if story_session.selected_tone_profile is not None
                    else None
                ),
                story_idea=resolved_brief["story_idea"],
                desired_themes=resolved_brief["desired_themes"],
                key_images=resolved_brief["key_images"],
                audience_notes=resolved_brief["audience_notes"],
                must_have_elements=resolved_brief["must_have_elements"],
            )
            _record_session_model_usage(
                session=self._session,
                session_id=story_session.id,
                usage_bucket="planning",
                workflow_stage=WorkflowStage.BRIEF,
                purpose="brief_normalization",
                source=normalization_result.source,
                model_id=normalization_result.model_id,
                prompt_version=normalization_result.prompt_version,
                raw_response=normalization_result.raw_response,
                elapsed_ms=_elapsed_ms_since(normalization_started_at),
            )

        normalization_result = apply_brief_normalization_overrides(
            normalization_result,
            raw_brief=resolved_brief["raw_brief"],
            normalized_summary=normalized_summary,
            normalized_summary_provided=normalized_summary_provided,
            normalized_preferences=normalized_preferences,
            normalized_preferences_provided=normalized_preferences_provided,
        )

        stage_map = self._stage_states.ensure_for_session(story_session)
        self._validate_stage_transition(
            stage_map,
            stage=WorkflowStage.BRIEF,
            status=WorkflowStageState.COMPLETED,
        )
        stage_snapshot = stage_map[WorkflowStage.BRIEF]
        previous_status = stage_snapshot.status
        now = utc_now()

        if current_brief is not None:
            current_brief.is_active = False

        next_revision_number = 1 if current_brief is None else current_brief.revision_number + 1
        new_brief = StoryBrief(
            session_id=story_session.id,
            revision_number=next_revision_number,
            story_idea=resolved_brief["story_idea"],
            desired_themes=resolved_brief["desired_themes"],
            key_images=resolved_brief["key_images"],
            audience_notes=resolved_brief["audience_notes"],
            must_have_elements=resolved_brief["must_have_elements"],
            raw_brief=resolved_brief["raw_brief"],
            normalized_summary=normalization_result.normalized_summary,
            normalized_preferences=normalization_result.normalized_preferences.model_dump(
                mode="json"
            )
            if normalization_result.normalized_preferences.has_content()
            else None,
            planning_notes=resolved_brief["planning_notes"],
            model_output=build_brief_model_output(normalization_result),
            is_active=True,
            accepted_at=now,
        )
        self._session.add(new_brief)
        self._session.flush()

        stage_snapshot.status = WorkflowStageState.COMPLETED
        stage_snapshot.detail = _build_story_brief_stage_detail(
            normalization_result.normalized_summary
            or resolved_brief["story_idea"]
            or resolved_brief["raw_brief"]
        )
        stage_snapshot.started_at = stage_snapshot.started_at or now
        stage_snapshot.completed_at = now

        invalidated_stages = self._invalidate_dependent_stages(
            stage_map,
            stage=WorkflowStage.BRIEF,
            detail=_build_story_brief_invalidation_detail(),
        )
        self._apply_rollups(story_session, stage_map)

        stage_event = None
        if previous_status != stage_snapshot.status or invalidated_stages:
            stage_event = self._event_log.record_stage_state_changed(
                story_session.id,
                stage=WorkflowStage.BRIEF,
                previous_status=previous_status,
                status=stage_snapshot.status,
                detail=stage_snapshot.detail,
                invalidated_stages=invalidated_stages,
                current_stage=story_session.current_stage,
                resume_stage=story_session.resume_stage,
                furthest_completed_stage=story_session.furthest_completed_stage,
                overall_status=story_session.overall_status,
                actor=actor,
            )
            for invalidated_stage in invalidated_stages:
                stage_map[invalidated_stage].last_event = stage_event

        edit_event = self._event_log.record_user_edit(
            story_session.id,
            target_kind=UserEditTargetKind.STORY_BRIEF,
            stage=WorkflowStage.BRIEF,
            target_id=new_brief.id,
            revision_number=new_brief.revision_number,
            changed_fields=_build_story_brief_changed_fields(current_brief, new_brief),
            source=origin,
            field_values=_build_story_brief_event_values(new_brief, edit_mode=edit_mode),
            summary_text=_build_story_brief_summary_text(
                has_existing_brief=current_brief is not None,
                origin=origin,
            ),
            actor=actor,
        )
        self._refresh_continuity(
            story_session.id,
            source_stage=WorkflowStage.BRIEF,
            source_summary=edit_event.summary,
        )
        stage_snapshot.last_event = edit_event
        self._session.commit()
        return SessionStoryBriefResponse(
            snapshot=self.load_session_snapshot(story_session.id),
            event=self._event_log.build_event_view(edit_event),
        )

    def save_audio_settings(
        self,
        session_id: str,
        *,
        payload: SaveSessionAudioSettingsRequest,
        actor: SessionEventActor | None = None,
    ) -> SessionAudioSettingsResponse:
        story_session = self._sessions.get_for_update(session_id)
        if story_session is None:
            raise SessionNotFoundError(f"session {session_id!r} was not found")

        aggregate = self._sessions.get_aggregate(session_id)
        if aggregate is None:
            raise SessionNotFoundError(f"session {session_id!r} was not found")

        current_settings = build_audio_settings_view(
            story_session=story_session,
            latest_audio_job=aggregate.latest_audio_job,
            composition_segments=aggregate.composition_segments,
            selected_story_setup=aggregate.selected_story_setup,
            selected_story_outline=aggregate.selected_story_outline,
        )
        next_settings = current_settings.model_copy(
            update={
                **(
                    {"voice_key": payload.voice_key}
                    if "voice_key" in payload.model_fields_set
                    else {}
                ),
                **(
                    {"narration_style": payload.narration_style}
                    if "narration_style" in payload.model_fields_set
                    else {}
                ),
                **(
                    {"playback_speed": payload.playback_speed}
                    if "playback_speed" in payload.model_fields_set
                    else {}
                ),
                **(
                    {"include_background_music": payload.include_background_music}
                    if "include_background_music" in payload.model_fields_set
                    else {}
                ),
                **(
                    {"music_profile": payload.music_profile}
                    if "music_profile" in payload.model_fields_set
                    else {}
                ),
                **(
                    {"narration_volume": payload.narration_volume}
                    if "narration_volume" in payload.model_fields_set
                    else {}
                ),
                **(
                    {"music_volume": payload.music_volume}
                    if "music_volume" in payload.model_fields_set
                    else {}
                ),
                **(
                    {"guidance_notes": _normalize_optional_text(payload.guidance_notes)}
                    if "guidance_notes" in payload.model_fields_set
                    else {}
                ),
            }
        )
        next_settings = hydrate_audio_settings_view(
            next_settings,
            runtime_estimate=build_audio_runtime_estimate(
                composition_segments=aggregate.composition_segments,
                selected_story_setup=aggregate.selected_story_setup,
                selected_story_outline=aggregate.selected_story_outline,
                playback_speed=next_settings.playback_speed,
            ),
        )

        changed_fields = [
            field_name
            for field_name in (
                "voice_key",
                "narration_style",
                "playback_speed",
                "include_background_music",
                "music_profile",
                "narration_volume",
                "music_volume",
                "guidance_notes",
            )
            if field_name in payload.model_fields_set
            and getattr(current_settings, field_name) != getattr(next_settings, field_name)
        ]
        if not changed_fields:
            raise SessionAudioSettingsSaveError(
                "audio settings save did not change any saved fields"
            )

        persist_audio_settings(story_session, next_settings)

        if aggregate.active_audio_job is not None:
            self._cancel_active_audio_jobs(
                session_id,
                reason="Cancelled because audio settings changed.",
            )

        stage_map = self._stage_states.ensure_for_session(story_session)
        stage_snapshot = stage_map[WorkflowStage.AUDIO]
        previous_status = stage_snapshot.status
        previous_detail = stage_snapshot.detail
        now = utc_now()
        audio_requires_regeneration = (
            aggregate.latest_audio_asset is not None
            or (
                aggregate.latest_audio_job is not None
                and aggregate.latest_audio_job.status == JobStatus.COMPLETED
            )
        )

        if stage_snapshot.status == WorkflowStageState.DRAFT:
            self._validate_stage_transition(
                stage_map,
                stage=WorkflowStage.AUDIO,
                status=WorkflowStageState.IN_PROGRESS,
            )
            stage_snapshot.started_at = stage_snapshot.started_at or now

        stage_snapshot.status = (
            WorkflowStageState.NEEDS_REGENERATION
            if audio_requires_regeneration
            else WorkflowStageState.IN_PROGRESS
        )
        stage_snapshot.detail = build_audio_settings_stage_detail(
            next_settings,
            regenerate_audio=audio_requires_regeneration,
        )
        stage_snapshot.started_at = stage_snapshot.started_at or now
        stage_snapshot.completed_at = None

        invalidated_stages = self._invalidate_dependent_stages(
            stage_map,
            stage=WorkflowStage.AUDIO,
            detail=stage_snapshot.detail,
        )
        self._apply_rollups(story_session, stage_map)

        if (
            previous_status != stage_snapshot.status
            or previous_detail != stage_snapshot.detail
            or invalidated_stages
        ):
            stage_event = self._event_log.record_stage_state_changed(
                story_session.id,
                stage=WorkflowStage.AUDIO,
                previous_status=previous_status,
                status=stage_snapshot.status,
                detail=stage_snapshot.detail,
                invalidated_stages=invalidated_stages,
                current_stage=story_session.current_stage,
                resume_stage=story_session.resume_stage,
                furthest_completed_stage=story_session.furthest_completed_stage,
                overall_status=story_session.overall_status,
                actor=actor,
            )
            for invalidated_stage in invalidated_stages:
                stage_map[invalidated_stage].last_event = stage_event

        edit_event = self._event_log.record_user_edit(
            story_session.id,
            target_kind=UserEditTargetKind.AUDIO_SETTINGS,
            stage=WorkflowStage.AUDIO,
            changed_fields=changed_fields,
            source=payload.origin,
            field_values=audio_settings_field_values(next_settings),
            summary_text=build_audio_settings_event_summary(next_settings),
            actor=actor,
        )
        stage_snapshot.last_event = edit_event
        self._session.commit()
        return SessionAudioSettingsResponse(
            snapshot=self.load_session_snapshot(story_session.id),
            event=self._event_log.build_event_view(edit_event),
        )

    def generate_pitches(
        self,
        session_id: str,
        *,
        candidate_count: int = 3,
        guidance: str | None = None,
        preserve_selected_pitch: bool = False,
        origin: str = "workspace",
        actor: SessionEventActor | None = None,
        pitch_generation_service: PitchGenerationService | None = None,
    ) -> SessionPitchGenerationResponse:
        story_session = self._sessions.get_for_update(session_id)
        if story_session is None:
            raise SessionNotFoundError(f"session {session_id!r} was not found")

        active_brief = self._sessions.get_active_story_brief(session_id)
        if active_brief is None:
            raise SessionPitchGenerationError(
                "save a story brief before generating pitches",
            )

        generator = pitch_generation_service or PitchGenerationService()
        current_selected_pitch = self._sessions.get_selected_pitch(session_id)
        pitch_generation_started_at = perf_counter()
        generation_result = generator.generate_pitches(
            candidate_count=candidate_count,
            generation_goal="alternatives",
            raw_brief=active_brief.raw_brief,
            genre_label=(
                story_session.selected_genre.label
                if story_session.selected_genre is not None
                else None
            ),
            genre_description=(
                story_session.selected_genre.description
                if story_session.selected_genre is not None
                else None
            ),
            genre_bedtime_safety_notes=(
                story_session.selected_genre.bedtime_safety_notes
                if story_session.selected_genre is not None
                else None
            ),
            tone_label=(
                story_session.selected_tone_profile.label
                if story_session.selected_tone_profile is not None
                else None
            ),
            tone_description=(
                story_session.selected_tone_profile.description
                if story_session.selected_tone_profile is not None
                else None
            ),
            tone_bedtime_notes=(
                story_session.selected_tone_profile.bedtime_notes
                if story_session.selected_tone_profile is not None
                else None
            ),
            normalized_summary=active_brief.normalized_summary,
            story_idea=active_brief.story_idea,
            desired_themes=active_brief.desired_themes,
            key_images=active_brief.key_images,
            audience_notes=active_brief.audience_notes,
            must_have_elements=active_brief.must_have_elements,
            planning_notes=active_brief.planning_notes,
            normalized_preferences=NormalizedBriefPreferences.model_validate(
                active_brief.normalized_preferences or {}
            ),
            guidance=guidance,
            selected_pitch=_build_selected_pitch_context(current_selected_pitch)
            if current_selected_pitch is not None
            else None,
        )
        _record_session_model_usage(
            session=self._session,
            session_id=story_session.id,
            usage_bucket="planning",
            workflow_stage=WorkflowStage.PITCHES,
            purpose="pitch_generation",
            source=generation_result.source,
            model_id=generation_result.model_id,
            prompt_version=generation_result.prompt_version,
            raw_response=generation_result.raw_response,
            elapsed_ms=_elapsed_ms_since(pitch_generation_started_at),
        )
        if not generation_result.evaluation.passed:
            raise SessionPitchGenerationError(
                "pitch generation produced an invalid candidate batch"
            )

        stage_map = self._stage_states.ensure_for_session(story_session)
        self._validate_stage_transition(
            stage_map,
            stage=WorkflowStage.PITCHES,
            status=WorkflowStageState.IN_PROGRESS,
        )
        stage_snapshot = stage_map[WorkflowStage.PITCHES]
        previous_status = stage_snapshot.status
        previous_detail = stage_snapshot.detail
        now = utc_now()

        stage_snapshot.status = WorkflowStageState.IN_PROGRESS
        stage_snapshot.detail = _build_pitch_generation_stage_detail(
            len(generation_result.pitches),
        )
        stage_snapshot.started_at = stage_snapshot.started_at or now
        stage_snapshot.completed_at = None

        invalidated_stages = self._invalidate_dependent_stages(
            stage_map,
            stage=WorkflowStage.PITCHES,
            detail=stage_snapshot.detail,
        )

        if not preserve_selected_pitch:
            for pitch in self._sessions.list_pitches(session_id):
                if pitch.is_selected:
                    pitch.is_selected = False

        generation_key = _build_pitch_generation_key()
        model_output = _build_pitch_persistence_metadata(
            generation_result,
            generation_kind="generated",
            guidance=guidance,
        )

        for index, candidate in enumerate(generation_result.pitches, start=1):
            self._session.add(
                Pitch(
                    session_id=story_session.id,
                    story_brief_id=active_brief.id,
                    generation_key=generation_key,
                    pitch_index=index,
                    title=candidate.title,
                    logline=candidate.hook,
                    summary=candidate.central_conflict,
                    bedtime_notes=candidate.why_it_fits,
                    model_output={
                        **model_output,
                        "candidate": candidate.model_dump(mode="json"),
                        "pitch_index": index,
                    },
                    is_selected=False,
                )
            )

        self._session.flush()
        self._apply_rollups(story_session, stage_map)

        stage_event = None
        if (
            previous_status != stage_snapshot.status
            or previous_detail != stage_snapshot.detail
            or invalidated_stages
        ):
            stage_event = self._event_log.record_stage_state_changed(
                story_session.id,
                stage=WorkflowStage.PITCHES,
                previous_status=previous_status,
                status=stage_snapshot.status,
                detail=stage_snapshot.detail,
                invalidated_stages=invalidated_stages,
                current_stage=story_session.current_stage,
                resume_stage=story_session.resume_stage,
                furthest_completed_stage=story_session.furthest_completed_stage,
                overall_status=story_session.overall_status,
                actor=actor,
            )
            for invalidated_stage in invalidated_stages:
                stage_map[invalidated_stage].last_event = stage_event

        ai_event = self._event_log.record_ai_output(
            story_session.id,
            output_kind=AIOutputKind.PITCH_BATCH,
            stage=WorkflowStage.PITCHES,
            generation_key=generation_key,
            candidate_count=len(generation_result.pitches),
            model_id=generation_result.model_id,
            summary_text=_build_pitch_generation_summary_text(generation_result.pitches),
            actor=actor,
        )
        stage_snapshot.last_event = ai_event
        self._session.commit()
        return SessionPitchGenerationResponse(
            snapshot=self.load_session_snapshot(story_session.id),
            event=self._event_log.build_event_view(ai_event),
        )

    def refine_pitch(
        self,
        session_id: str,
        *,
        instructions: str,
        pitch_id: str | None = None,
        generation_key: str | None = None,
        pitch_index: int | None = None,
        title: str | None = None,
        origin: str = "workspace",
        actor: SessionEventActor | None = None,
        pitch_generation_service: PitchGenerationService | None = None,
    ) -> SessionSelectionResponse:
        story_session = self._sessions.get_for_update(session_id)
        if story_session is None:
            raise SessionNotFoundError(f"session {session_id!r} was not found")

        active_brief = self._sessions.get_active_story_brief(session_id)
        if active_brief is None:
            raise SessionPitchGenerationError(
                "save a story brief before refining pitches",
            )

        normalized_instructions = _normalize_optional_text(instructions)
        if normalized_instructions is None:
            raise SessionPitchGenerationError("pitch refinement instructions are required")

        matches = _find_matching_pitches(
            self._sessions.list_pitches(session_id),
            pitch_id=pitch_id,
            generation_key=generation_key,
            pitch_index=pitch_index,
            title=title,
        )
        if not matches:
            raise SessionPitchSelectionError("no generated pitch matched the requested refinement")
        if len(matches) > 1:
            raise SessionPitchSelectionError(
                "the requested pitch refinement matched more than one candidate"
            )

        source_pitch = matches[0]
        previous_selected_pitch = self._sessions.get_selected_pitch(session_id)
        generator = pitch_generation_service or PitchGenerationService()
        pitch_refinement_started_at = perf_counter()
        generation_result = generator.generate_pitches(
            candidate_count=1,
            generation_goal="refinement",
            raw_brief=active_brief.raw_brief,
            genre_label=(
                story_session.selected_genre.label
                if story_session.selected_genre is not None
                else None
            ),
            genre_description=(
                story_session.selected_genre.description
                if story_session.selected_genre is not None
                else None
            ),
            genre_bedtime_safety_notes=(
                story_session.selected_genre.bedtime_safety_notes
                if story_session.selected_genre is not None
                else None
            ),
            tone_label=(
                story_session.selected_tone_profile.label
                if story_session.selected_tone_profile is not None
                else None
            ),
            tone_description=(
                story_session.selected_tone_profile.description
                if story_session.selected_tone_profile is not None
                else None
            ),
            tone_bedtime_notes=(
                story_session.selected_tone_profile.bedtime_notes
                if story_session.selected_tone_profile is not None
                else None
            ),
            normalized_summary=active_brief.normalized_summary,
            story_idea=active_brief.story_idea,
            desired_themes=active_brief.desired_themes,
            key_images=active_brief.key_images,
            audience_notes=active_brief.audience_notes,
            must_have_elements=active_brief.must_have_elements,
            planning_notes=active_brief.planning_notes,
            normalized_preferences=NormalizedBriefPreferences.model_validate(
                active_brief.normalized_preferences or {}
            ),
            guidance=normalized_instructions,
            selected_pitch=_build_selected_pitch_context(source_pitch),
        )
        _record_session_model_usage(
            session=self._session,
            session_id=story_session.id,
            usage_bucket="planning",
            workflow_stage=WorkflowStage.PITCHES,
            purpose="pitch_refinement",
            source=generation_result.source,
            model_id=generation_result.model_id,
            prompt_version=generation_result.prompt_version,
            raw_response=generation_result.raw_response,
            elapsed_ms=_elapsed_ms_since(pitch_refinement_started_at),
        )
        if not generation_result.evaluation.passed or not generation_result.pitches:
            raise SessionPitchGenerationError(
                "pitch refinement produced an invalid candidate batch"
            )

        stage_map = self._stage_states.ensure_for_session(story_session)
        self._validate_stage_transition(
            stage_map,
            stage=WorkflowStage.PITCHES,
            status=WorkflowStageState.COMPLETED,
        )
        stage_snapshot = stage_map[WorkflowStage.PITCHES]
        previous_status = stage_snapshot.status
        previous_detail = stage_snapshot.detail
        now = utc_now()

        for pitch in self._sessions.list_pitches(session_id):
            pitch.is_selected = False

        refinement_rationale = _build_pitch_refinement_rationale(
            source_pitch,
            normalized_instructions,
        )
        generation_key = _build_pitch_generation_key()
        model_output = _build_pitch_persistence_metadata(
            generation_result,
            generation_kind="refinement",
            guidance=normalized_instructions,
            source_pitch=source_pitch,
            selection_rationale=refinement_rationale,
        )
        refined_candidate = generation_result.pitches[0]
        refined_pitch = Pitch(
            session_id=story_session.id,
            story_brief_id=active_brief.id,
            generation_key=generation_key,
            pitch_index=1,
            title=refined_candidate.title,
            logline=refined_candidate.hook,
            summary=refined_candidate.central_conflict,
            bedtime_notes=refined_candidate.why_it_fits,
            model_output={
                **model_output,
                "candidate": refined_candidate.model_dump(mode="json"),
                "pitch_index": 1,
            },
            is_selected=True,
            accepted_at=now,
        )
        self._session.add(refined_pitch)
        self._session.flush()

        stage_snapshot.status = WorkflowStageState.COMPLETED
        stage_snapshot.detail = _build_pitch_selection_detail(refined_pitch)
        stage_snapshot.started_at = stage_snapshot.started_at or now
        stage_snapshot.completed_at = now

        invalidated_stages = self._invalidate_dependent_stages(
            stage_map,
            stage=WorkflowStage.PITCHES,
            detail=_build_pitch_invalidation_detail(refined_pitch),
        )
        self._apply_rollups(story_session, stage_map)

        stage_event = None
        if (
            previous_status != stage_snapshot.status
            or previous_detail != stage_snapshot.detail
            or invalidated_stages
        ):
            stage_event = self._event_log.record_stage_state_changed(
                story_session.id,
                stage=WorkflowStage.PITCHES,
                previous_status=previous_status,
                status=stage_snapshot.status,
                detail=stage_snapshot.detail,
                invalidated_stages=invalidated_stages,
                current_stage=story_session.current_stage,
                resume_stage=story_session.resume_stage,
                furthest_completed_stage=story_session.furthest_completed_stage,
                overall_status=story_session.overall_status,
                actor=actor,
            )
            for invalidated_stage in invalidated_stages:
                stage_map[invalidated_stage].last_event = stage_event

        self._event_log.record_ai_output(
            story_session.id,
            output_kind=AIOutputKind.PITCH_BATCH,
            stage=WorkflowStage.PITCHES,
            generation_key=generation_key,
            candidate_count=1,
            model_id=generation_result.model_id,
            summary_text=_build_pitch_refinement_summary_text(
                refined_pitch,
                source_pitch=source_pitch,
            ),
            actor=actor,
        )
        selection_event = self._event_log.record_selection(
            story_session.id,
            selection_kind=SelectionKind.PITCH,
            stage=WorkflowStage.PITCHES,
            label=refined_pitch.title,
            selection_id=refined_pitch.id,
            rationale=refinement_rationale,
            previous_selection_id=(
                previous_selected_pitch.id if previous_selected_pitch is not None else None
            ),
            source=origin,
            accepted=True,
            actor=actor,
        )
        self._refresh_continuity(
            story_session.id,
            source_stage=WorkflowStage.PITCHES,
            source_summary=selection_event.summary,
        )
        self._capture_plan_revision(
            story_session.id,
            source_stage=WorkflowStage.PITCHES,
            change_summary=selection_event.summary,
        )
        stage_snapshot.last_event = selection_event
        self._session.commit()
        return SessionSelectionResponse(
            snapshot=self.load_session_snapshot(story_session.id),
            event=self._event_log.build_event_view(selection_event),
        )

    def select_pitch(
        self,
        session_id: str,
        *,
        pitch_id: str | None = None,
        generation_key: str | None = None,
        pitch_index: int | None = None,
        title: str | None = None,
        origin: str = "workspace",
        actor: SessionEventActor | None = None,
    ) -> SessionSelectionResponse:
        story_session = self._sessions.get_for_update(session_id)
        if story_session is None:
            raise SessionNotFoundError(f"session {session_id!r} was not found")

        matches = _find_matching_pitches(
            self._sessions.list_pitches(session_id),
            pitch_id=pitch_id,
            generation_key=generation_key,
            pitch_index=pitch_index,
            title=title,
        )
        if not matches:
            raise SessionPitchSelectionError("no generated pitch matched the requested selection")
        if len(matches) > 1:
            raise SessionPitchSelectionError(
                "the requested pitch selection matched more than one candidate"
            )

        selected_pitch = matches[0]
        previous_selected_pitch = self._sessions.get_selected_pitch(session_id)
        for pitch in self._sessions.list_pitches(session_id):
            pitch.is_selected = pitch.id == selected_pitch.id

        now = utc_now()
        selected_pitch.accepted_at = now

        stage_map = self._stage_states.ensure_for_session(story_session)
        self._validate_stage_transition(
            stage_map,
            stage=WorkflowStage.PITCHES,
            status=WorkflowStageState.COMPLETED,
        )
        stage_snapshot = stage_map[WorkflowStage.PITCHES]
        previous_status = stage_snapshot.status

        stage_snapshot.status = WorkflowStageState.COMPLETED
        stage_snapshot.detail = _build_pitch_selection_detail(selected_pitch)
        stage_snapshot.started_at = stage_snapshot.started_at or now
        stage_snapshot.completed_at = now

        invalidated_stages = self._invalidate_dependent_stages(
            stage_map,
            stage=WorkflowStage.PITCHES,
            detail=_build_pitch_invalidation_detail(selected_pitch),
        )
        self._apply_rollups(story_session, stage_map)

        if previous_status != stage_snapshot.status or invalidated_stages:
            stage_event = self._event_log.record_stage_state_changed(
                story_session.id,
                stage=WorkflowStage.PITCHES,
                previous_status=previous_status,
                status=stage_snapshot.status,
                detail=stage_snapshot.detail,
                invalidated_stages=invalidated_stages,
                current_stage=story_session.current_stage,
                resume_stage=story_session.resume_stage,
                furthest_completed_stage=story_session.furthest_completed_stage,
                overall_status=story_session.overall_status,
                actor=actor,
            )
            for invalidated_stage in invalidated_stages:
                stage_map[invalidated_stage].last_event = stage_event

        selection_event = self._event_log.record_selection(
            story_session.id,
            selection_kind=SelectionKind.PITCH,
            stage=WorkflowStage.PITCHES,
            label=selected_pitch.title,
            selection_id=selected_pitch.id,
            previous_selection_id=(
                previous_selected_pitch.id if previous_selected_pitch is not None else None
            ),
            source=origin,
            accepted=True,
            actor=actor,
        )
        self._refresh_continuity(
            story_session.id,
            source_stage=WorkflowStage.PITCHES,
            source_summary=selection_event.summary,
        )
        self._capture_plan_revision(
            story_session.id,
            source_stage=WorkflowStage.PITCHES,
            change_summary=selection_event.summary,
        )
        stage_snapshot.last_event = selection_event
        self._session.commit()
        return SessionSelectionResponse(
            snapshot=self.load_session_snapshot(story_session.id),
            event=self._event_log.build_event_view(selection_event),
        )

    def generate_character_sheets(
        self,
        session_id: str,
        *,
        candidate_count: int = 3,
        guidance: str | None = None,
        origin: str = "workspace",
        actor: SessionEventActor | None = None,
        character_generation_service: CharacterGenerationService | None = None,
    ) -> SessionCharacterSheetGenerationResponse:
        story_session = self._sessions.get_for_update(session_id)
        if story_session is None:
            raise SessionNotFoundError(f"session {session_id!r} was not found")

        selected_pitch = self._sessions.get_selected_pitch(session_id)
        if selected_pitch is None:
            raise SessionCharacterSheetGenerationError(
                "select a pitch before generating character sheets",
            )

        active_brief = self._sessions.get_active_story_brief(session_id)
        current_selected_character_sheet = self._sessions.get_selected_character_sheet(session_id)
        raw_brief = active_brief.raw_brief if active_brief is not None else selected_pitch.logline
        normalized_summary = active_brief.normalized_summary if active_brief is not None else None
        generator = character_generation_service or CharacterGenerationService()
        character_generation_started_at = perf_counter()
        generation_result = generator.generate_character_sheets(
            candidate_count=candidate_count,
            generation_goal="alternatives",
            selected_pitch=_build_selected_pitch_context(selected_pitch),
            raw_brief=raw_brief,
            genre_label=(
                story_session.selected_genre.label
                if story_session.selected_genre is not None
                else None
            ),
            genre_description=(
                story_session.selected_genre.description
                if story_session.selected_genre is not None
                else None
            ),
            genre_bedtime_safety_notes=(
                story_session.selected_genre.bedtime_safety_notes
                if story_session.selected_genre is not None
                else None
            ),
            tone_label=(
                story_session.selected_tone_profile.label
                if story_session.selected_tone_profile is not None
                else None
            ),
            tone_description=(
                story_session.selected_tone_profile.description
                if story_session.selected_tone_profile is not None
                else None
            ),
            tone_bedtime_notes=(
                story_session.selected_tone_profile.bedtime_notes
                if story_session.selected_tone_profile is not None
                else None
            ),
            normalized_summary=normalized_summary,
            story_idea=active_brief.story_idea if active_brief is not None else None,
            desired_themes=active_brief.desired_themes if active_brief is not None else None,
            key_images=active_brief.key_images if active_brief is not None else None,
            audience_notes=active_brief.audience_notes if active_brief is not None else None,
            must_have_elements=(
                active_brief.must_have_elements if active_brief is not None else None
            ),
            planning_notes=active_brief.planning_notes if active_brief is not None else None,
            normalized_preferences=NormalizedBriefPreferences.model_validate(
                active_brief.normalized_preferences if active_brief is not None else {}
            ),
            guidance=guidance,
            existing_character_sheet=(
                _build_existing_character_sheet_context(current_selected_character_sheet)
                if current_selected_character_sheet is not None
                else None
            ),
        )
        _record_session_model_usage(
            session=self._session,
            session_id=story_session.id,
            usage_bucket="planning",
            workflow_stage=WorkflowStage.CHARACTERS,
            purpose="character_generation",
            source=generation_result.source,
            model_id=generation_result.model_id,
            prompt_version=generation_result.prompt_version,
            raw_response=generation_result.raw_response,
            elapsed_ms=_elapsed_ms_since(character_generation_started_at),
        )
        if not generation_result.evaluation.passed:
            raise SessionCharacterSheetGenerationError(
                "character generation produced an invalid candidate batch"
            )

        stage_map = self._stage_states.ensure_for_session(story_session)
        self._validate_stage_transition(
            stage_map,
            stage=WorkflowStage.CHARACTERS,
            status=WorkflowStageState.IN_PROGRESS,
        )
        stage_snapshot = stage_map[WorkflowStage.CHARACTERS]
        previous_status = stage_snapshot.status
        previous_detail = stage_snapshot.detail
        now = utc_now()

        stage_snapshot.status = WorkflowStageState.IN_PROGRESS
        stage_snapshot.detail = _build_character_sheet_generation_stage_detail(
            len(generation_result.character_sheets),
        )
        stage_snapshot.started_at = stage_snapshot.started_at or now
        stage_snapshot.completed_at = None

        invalidated_stages = self._invalidate_dependent_stages(
            stage_map,
            stage=WorkflowStage.CHARACTERS,
            detail=stage_snapshot.detail,
        )

        generation_key = _build_character_generation_key()
        model_output = _build_character_persistence_metadata(
            generation_result,
            generation_key=generation_key,
            generation_kind="generated",
            guidance=guidance,
            selected_pitch=selected_pitch,
        )
        next_revision_number = _next_character_sheet_revision_number(
            self._sessions.list_character_sheets(session_id)
        )
        for index, candidate in enumerate(generation_result.character_sheets, start=1):
            self._session.add(
                CharacterSheet(
                    session_id=story_session.id,
                    pitch_id=selected_pitch.id,
                    revision_number=next_revision_number + index - 1,
                    title=candidate.title,
                    summary=candidate.summary,
                    protagonist_name=candidate.protagonist.name,
                    supporting_cast=[
                        supporting_character.model_dump(mode="json")
                        for supporting_character in candidate.supporting_cast
                    ],
                    character_data={
                        **model_output,
                        "candidate": candidate.model_dump(mode="json"),
                        "batch_metadata": {
                            **model_output["batch_metadata"],
                            "candidate_index": index,
                        },
                    },
                    bedtime_notes=candidate.bedtime_safety_notes,
                    is_selected=False,
                )
            )

        self._session.flush()
        self._apply_rollups(story_session, stage_map)

        stage_event = None
        if (
            previous_status != stage_snapshot.status
            or previous_detail != stage_snapshot.detail
            or invalidated_stages
        ):
            stage_event = self._event_log.record_stage_state_changed(
                story_session.id,
                stage=WorkflowStage.CHARACTERS,
                previous_status=previous_status,
                status=stage_snapshot.status,
                detail=stage_snapshot.detail,
                invalidated_stages=invalidated_stages,
                current_stage=story_session.current_stage,
                resume_stage=story_session.resume_stage,
                furthest_completed_stage=story_session.furthest_completed_stage,
                overall_status=story_session.overall_status,
                actor=actor,
            )
            for invalidated_stage in invalidated_stages:
                stage_map[invalidated_stage].last_event = stage_event

        ai_event = self._event_log.record_ai_output(
            story_session.id,
            output_kind=AIOutputKind.CHARACTER_SHEET,
            stage=WorkflowStage.CHARACTERS,
            generation_key=generation_key,
            candidate_count=len(generation_result.character_sheets),
            model_id=generation_result.model_id,
            summary_text=_build_character_sheet_generation_summary_text(
                generation_result.character_sheets
            ),
            actor=actor,
        )
        stage_snapshot.last_event = ai_event
        self._session.commit()
        return SessionCharacterSheetGenerationResponse(
            snapshot=self.load_session_snapshot(story_session.id),
            event=self._event_log.build_event_view(ai_event),
        )

    def refine_character_sheet(
        self,
        session_id: str,
        *,
        instructions: str,
        character_sheet_id: str | None = None,
        revision_number: int | None = None,
        title: str | None = None,
        focus_character_names: list[str] | None = None,
        change_summary: str | None = None,
        change_impact: CharacterChangeImpact | None = None,
        origin: str = "workspace",
        actor: SessionEventActor | None = None,
        character_generation_service: CharacterGenerationService | None = None,
    ) -> SessionSelectionResponse:
        story_session = self._sessions.get_for_update(session_id)
        if story_session is None:
            raise SessionNotFoundError(f"session {session_id!r} was not found")

        selected_pitch = self._sessions.get_selected_pitch(session_id)
        if selected_pitch is None:
            raise SessionCharacterSheetGenerationError(
                "select a pitch before refining character sheets",
            )

        normalized_instructions = _normalize_optional_text(instructions)
        if normalized_instructions is None:
            raise SessionCharacterSheetGenerationError(
                "character-sheet refinement instructions are required"
            )
        normalized_change_summary = _normalize_optional_text(change_summary)
        normalized_focus_character_names = [
            normalized_name
            for character_name in (focus_character_names or [])
            if (normalized_name := _normalize_optional_text(character_name)) is not None
        ]
        resolved_change_impact = change_impact or infer_character_change_impact(
            instructions=normalized_instructions,
            change_summary=normalized_change_summary,
        )

        source_character_sheet = _resolve_source_character_sheet(
            self._sessions.list_character_sheets(session_id),
            selected_character_sheet=self._sessions.get_selected_character_sheet(session_id),
            character_sheet_id=character_sheet_id,
            revision_number=revision_number,
            title=title,
        )
        if source_character_sheet is None:
            raise SessionCharacterSheetSelectionError(
                "no character sheet matched the requested refinement"
            )
        if (
            source_character_sheet.pitch_id is not None
            and source_character_sheet.pitch_id != selected_pitch.id
        ):
            raise SessionCharacterSheetSelectionError(
                "the requested character sheet belongs to a different pitch"
            )

        active_brief = self._sessions.get_active_story_brief(session_id)
        previous_selected_character_sheet = self._sessions.get_selected_character_sheet(session_id)
        raw_brief = active_brief.raw_brief if active_brief is not None else selected_pitch.logline
        normalized_summary = active_brief.normalized_summary if active_brief is not None else None
        generator = character_generation_service or CharacterGenerationService()
        character_refinement_started_at = perf_counter()
        generation_result = generator.generate_character_sheets(
            candidate_count=1,
            generation_goal="refinement",
            selected_pitch=_build_selected_pitch_context(selected_pitch),
            raw_brief=raw_brief,
            genre_label=(
                story_session.selected_genre.label
                if story_session.selected_genre is not None
                else None
            ),
            genre_description=(
                story_session.selected_genre.description
                if story_session.selected_genre is not None
                else None
            ),
            genre_bedtime_safety_notes=(
                story_session.selected_genre.bedtime_safety_notes
                if story_session.selected_genre is not None
                else None
            ),
            tone_label=(
                story_session.selected_tone_profile.label
                if story_session.selected_tone_profile is not None
                else None
            ),
            tone_description=(
                story_session.selected_tone_profile.description
                if story_session.selected_tone_profile is not None
                else None
            ),
            tone_bedtime_notes=(
                story_session.selected_tone_profile.bedtime_notes
                if story_session.selected_tone_profile is not None
                else None
            ),
            normalized_summary=normalized_summary,
            story_idea=active_brief.story_idea if active_brief is not None else None,
            desired_themes=active_brief.desired_themes if active_brief is not None else None,
            key_images=active_brief.key_images if active_brief is not None else None,
            audience_notes=active_brief.audience_notes if active_brief is not None else None,
            must_have_elements=(
                active_brief.must_have_elements if active_brief is not None else None
            ),
            planning_notes=active_brief.planning_notes if active_brief is not None else None,
            normalized_preferences=NormalizedBriefPreferences.model_validate(
                active_brief.normalized_preferences if active_brief is not None else {}
            ),
            guidance=normalized_instructions,
            change_summary=normalized_change_summary,
            focus_character_names=normalized_focus_character_names,
            existing_character_sheet=_build_existing_character_sheet_context(
                source_character_sheet
            ),
        )
        _record_session_model_usage(
            session=self._session,
            session_id=story_session.id,
            usage_bucket="planning",
            workflow_stage=WorkflowStage.CHARACTERS,
            purpose="character_refinement",
            source=generation_result.source,
            model_id=generation_result.model_id,
            prompt_version=generation_result.prompt_version,
            raw_response=generation_result.raw_response,
            elapsed_ms=_elapsed_ms_since(character_refinement_started_at),
        )
        if not generation_result.evaluation.passed or not generation_result.character_sheets:
            raise SessionCharacterSheetGenerationError(
                "character-sheet refinement produced an invalid candidate"
            )

        stage_map = self._stage_states.ensure_for_session(story_session)
        self._validate_stage_transition(
            stage_map,
            stage=WorkflowStage.CHARACTERS,
            status=WorkflowStageState.COMPLETED,
        )
        stage_snapshot = stage_map[WorkflowStage.CHARACTERS]
        previous_status = stage_snapshot.status
        previous_detail = stage_snapshot.detail
        now = utc_now()

        for character_sheet in self._sessions.list_character_sheets(session_id):
            character_sheet.is_selected = False

        refinement_rationale = _build_character_sheet_refinement_rationale(
            source_character_sheet,
            normalized_instructions,
            focus_character_names=normalized_focus_character_names,
            change_summary=normalized_change_summary,
            change_impact=resolved_change_impact,
        )
        generation_key = _build_character_generation_key()
        model_output = _build_character_persistence_metadata(
            generation_result,
            generation_key=generation_key,
            generation_kind="refinement",
            guidance=normalized_instructions,
            selected_pitch=selected_pitch,
            source_character_sheet=source_character_sheet,
            selection_rationale=refinement_rationale,
            change_summary=normalized_change_summary,
            focus_character_names=normalized_focus_character_names,
            change_impact=resolved_change_impact,
        )
        refined_candidate = generation_result.character_sheets[0]
        refined_character_sheet = CharacterSheet(
            session_id=story_session.id,
            pitch_id=selected_pitch.id,
            revision_number=_next_character_sheet_revision_number(
                self._sessions.list_character_sheets(session_id)
            ),
            title=refined_candidate.title,
            summary=refined_candidate.summary,
            protagonist_name=refined_candidate.protagonist.name,
            supporting_cast=[
                supporting_character.model_dump(mode="json")
                for supporting_character in refined_candidate.supporting_cast
            ],
            character_data={
                **model_output,
                "candidate": refined_candidate.model_dump(mode="json"),
                "batch_metadata": {
                    **model_output["batch_metadata"],
                    "candidate_index": 1,
                },
            },
            bedtime_notes=refined_candidate.bedtime_safety_notes,
            is_selected=True,
            accepted_at=now,
        )
        self._session.add(refined_character_sheet)
        self._session.flush()

        stage_snapshot.status = WorkflowStageState.COMPLETED
        stage_snapshot.detail = _build_character_sheet_selection_detail(refined_character_sheet)
        stage_snapshot.started_at = stage_snapshot.started_at or now
        stage_snapshot.completed_at = now

        invalidated_stages: list[WorkflowStage] = []
        if resolved_change_impact == CharacterChangeImpact.MAJOR:
            invalidated_stages = self._invalidate_dependent_stages(
                stage_map,
                stage=WorkflowStage.CHARACTERS,
                detail=_build_character_sheet_invalidation_detail(
                    refined_character_sheet,
                    change_impact=resolved_change_impact,
                ),
            )
        else:
            selected_beat_sheet = self._sessions.get_selected_beat_sheet(session_id)
            if (
                selected_beat_sheet is not None
                and selected_beat_sheet.character_sheet_id == source_character_sheet.id
            ):
                selected_beat_sheet.character_sheet_id = refined_character_sheet.id
        self._apply_rollups(story_session, stage_map)

        stage_event = None
        if (
            previous_status != stage_snapshot.status
            or previous_detail != stage_snapshot.detail
            or invalidated_stages
        ):
            stage_event = self._event_log.record_stage_state_changed(
                story_session.id,
                stage=WorkflowStage.CHARACTERS,
                previous_status=previous_status,
                status=stage_snapshot.status,
                detail=stage_snapshot.detail,
                invalidated_stages=invalidated_stages,
                current_stage=story_session.current_stage,
                resume_stage=story_session.resume_stage,
                furthest_completed_stage=story_session.furthest_completed_stage,
                overall_status=story_session.overall_status,
                actor=actor,
            )
            for invalidated_stage in invalidated_stages:
                stage_map[invalidated_stage].last_event = stage_event

        self._event_log.record_ai_output(
            story_session.id,
            output_kind=AIOutputKind.CHARACTER_SHEET,
            stage=WorkflowStage.CHARACTERS,
            generation_key=generation_key,
            candidate_count=1,
            model_id=generation_result.model_id,
            summary_text=_build_character_sheet_refinement_summary_text(
                refined_character_sheet,
                source_character_sheet=source_character_sheet,
            ),
            actor=actor,
        )
        selection_event = self._event_log.record_selection(
            story_session.id,
            selection_kind=SelectionKind.CHARACTER_SHEET,
            stage=WorkflowStage.CHARACTERS,
            label=_read_character_sheet_label(refined_character_sheet),
            selection_id=refined_character_sheet.id,
            rationale=refinement_rationale,
            previous_selection_id=(
                previous_selected_character_sheet.id
                if previous_selected_character_sheet is not None
                else None
            ),
            source=origin,
            accepted=True,
            actor=actor,
        )
        self._refresh_continuity(
            story_session.id,
            source_stage=WorkflowStage.CHARACTERS,
            source_summary=selection_event.summary,
        )
        self._capture_plan_revision(
            story_session.id,
            source_stage=WorkflowStage.CHARACTERS,
            change_summary=selection_event.summary,
        )
        stage_snapshot.last_event = selection_event
        self._session.commit()
        return SessionSelectionResponse(
            snapshot=self.load_session_snapshot(story_session.id),
            event=self._event_log.build_event_view(selection_event),
        )

    def select_character_sheet(
        self,
        session_id: str,
        *,
        character_sheet_id: str | None = None,
        revision_number: int | None = None,
        title: str | None = None,
        origin: str = "workspace",
        actor: SessionEventActor | None = None,
    ) -> SessionSelectionResponse:
        story_session = self._sessions.get_for_update(session_id)
        if story_session is None:
            raise SessionNotFoundError(f"session {session_id!r} was not found")

        selected_pitch = self._sessions.get_selected_pitch(session_id)
        if selected_pitch is None:
            raise SessionCharacterSheetSelectionError(
                "select a pitch before choosing a character sheet"
            )

        matches = _find_matching_character_sheets(
            self._sessions.list_character_sheets(session_id),
            character_sheet_id=character_sheet_id,
            revision_number=revision_number,
            title=title,
        )
        if not matches:
            raise SessionCharacterSheetSelectionError(
                "no generated character sheet matched the requested selection"
            )
        if len(matches) > 1:
            raise SessionCharacterSheetSelectionError(
                "the requested character-sheet selection matched more than one candidate"
            )

        selected_character_sheet = matches[0]
        if (
            selected_character_sheet.pitch_id is not None
            and selected_character_sheet.pitch_id != selected_pitch.id
        ):
            raise SessionCharacterSheetSelectionError(
                "the requested character sheet belongs to a different pitch"
            )

        previous_selected_character_sheet = self._sessions.get_selected_character_sheet(session_id)
        for character_sheet in self._sessions.list_character_sheets(session_id):
            character_sheet.is_selected = character_sheet.id == selected_character_sheet.id

        now = utc_now()
        selected_character_sheet.accepted_at = now

        stage_map = self._stage_states.ensure_for_session(story_session)
        self._validate_stage_transition(
            stage_map,
            stage=WorkflowStage.CHARACTERS,
            status=WorkflowStageState.COMPLETED,
        )
        stage_snapshot = stage_map[WorkflowStage.CHARACTERS]
        previous_status = stage_snapshot.status
        previous_detail = stage_snapshot.detail

        stage_snapshot.status = WorkflowStageState.COMPLETED
        stage_snapshot.detail = _build_character_sheet_selection_detail(selected_character_sheet)
        stage_snapshot.started_at = stage_snapshot.started_at or now
        stage_snapshot.completed_at = now

        invalidated_stages = self._invalidate_dependent_stages(
            stage_map,
            stage=WorkflowStage.CHARACTERS,
            detail=_build_character_sheet_invalidation_detail(selected_character_sheet),
        )
        self._apply_rollups(story_session, stage_map)

        if (
            previous_status != stage_snapshot.status
            or previous_detail != stage_snapshot.detail
            or invalidated_stages
        ):
            stage_event = self._event_log.record_stage_state_changed(
                story_session.id,
                stage=WorkflowStage.CHARACTERS,
                previous_status=previous_status,
                status=stage_snapshot.status,
                detail=stage_snapshot.detail,
                invalidated_stages=invalidated_stages,
                current_stage=story_session.current_stage,
                resume_stage=story_session.resume_stage,
                furthest_completed_stage=story_session.furthest_completed_stage,
                overall_status=story_session.overall_status,
                actor=actor,
            )
            for invalidated_stage in invalidated_stages:
                stage_map[invalidated_stage].last_event = stage_event

        selection_event = self._event_log.record_selection(
            story_session.id,
            selection_kind=SelectionKind.CHARACTER_SHEET,
            stage=WorkflowStage.CHARACTERS,
            label=_read_character_sheet_label(selected_character_sheet),
            selection_id=selected_character_sheet.id,
            rationale=_read_character_sheet_selection_rationale(selected_character_sheet),
            previous_selection_id=(
                previous_selected_character_sheet.id
                if previous_selected_character_sheet is not None
                else None
            ),
            source=origin,
            accepted=True,
            actor=actor,
        )
        self._refresh_continuity(
            story_session.id,
            source_stage=WorkflowStage.CHARACTERS,
            source_summary=selection_event.summary,
        )
        self._capture_plan_revision(
            story_session.id,
            source_stage=WorkflowStage.CHARACTERS,
            change_summary=selection_event.summary,
        )
        stage_snapshot.last_event = selection_event
        self._session.commit()
        return SessionSelectionResponse(
            snapshot=self.load_session_snapshot(story_session.id),
            event=self._event_log.build_event_view(selection_event),
        )

    def generate_beat_sheet(
        self,
        session_id: str,
        *,
        guidance: str | None = None,
        focus_beats: list[str] | None = None,
        bedtime_goal: str | None = None,
        origin: str = "workspace",
        actor: SessionEventActor | None = None,
        beat_sheet_generation_service: BeatSheetGenerationService | None = None,
    ) -> SessionBeatSheetGenerationResponse:
        story_session = self._sessions.get_for_update(session_id)
        if story_session is None:
            raise SessionNotFoundError(f"session {session_id!r} was not found")

        selected_pitch = self._sessions.get_selected_pitch(session_id)
        if selected_pitch is None:
            raise SessionBeatSheetGenerationError(
                "select a pitch before generating a beat sheet",
            )

        selected_character_sheet = self._sessions.get_selected_character_sheet(session_id)
        if selected_character_sheet is None:
            raise SessionBeatSheetGenerationError(
                "select a character sheet before generating a beat sheet",
            )

        active_brief = self._sessions.get_active_story_brief(session_id)
        current_selected_beat_sheet = self._sessions.get_selected_beat_sheet(session_id)
        raw_brief = active_brief.raw_brief if active_brief is not None else selected_pitch.logline
        normalized_summary = active_brief.normalized_summary if active_brief is not None else None
        generator = beat_sheet_generation_service or BeatSheetGenerationService()
        beat_generation_started_at = perf_counter()
        generation_result = generator.generate_beat_sheet(
            generation_goal="initial",
            selected_pitch=_build_selected_pitch_context(selected_pitch),
            selected_character_sheet=_build_existing_character_sheet_context(
                selected_character_sheet
            ),
            raw_brief=raw_brief,
            genre_label=(
                story_session.selected_genre.label
                if story_session.selected_genre is not None
                else None
            ),
            genre_description=(
                story_session.selected_genre.description
                if story_session.selected_genre is not None
                else None
            ),
            genre_bedtime_safety_notes=(
                story_session.selected_genre.bedtime_safety_notes
                if story_session.selected_genre is not None
                else None
            ),
            tone_label=(
                story_session.selected_tone_profile.label
                if story_session.selected_tone_profile is not None
                else None
            ),
            tone_description=(
                story_session.selected_tone_profile.description
                if story_session.selected_tone_profile is not None
                else None
            ),
            tone_bedtime_notes=(
                story_session.selected_tone_profile.bedtime_notes
                if story_session.selected_tone_profile is not None
                else None
            ),
            normalized_summary=normalized_summary,
            story_idea=active_brief.story_idea if active_brief is not None else None,
            desired_themes=active_brief.desired_themes if active_brief is not None else None,
            key_images=active_brief.key_images if active_brief is not None else None,
            audience_notes=active_brief.audience_notes if active_brief is not None else None,
            must_have_elements=(
                active_brief.must_have_elements if active_brief is not None else None
            ),
            planning_notes=active_brief.planning_notes if active_brief is not None else None,
            normalized_preferences=NormalizedBriefPreferences.model_validate(
                active_brief.normalized_preferences if active_brief is not None else {}
            ),
            guidance=guidance,
            focus_beats=_normalize_beat_name_list(focus_beats),
            bedtime_goal=_normalize_optional_text(bedtime_goal),
            existing_beat_sheet=(
                _build_existing_beat_sheet_context(current_selected_beat_sheet)
                if current_selected_beat_sheet is not None
                and current_selected_beat_sheet.character_sheet_id == selected_character_sheet.id
                else None
            ),
        )
        _record_session_model_usage(
            session=self._session,
            session_id=story_session.id,
            usage_bucket="planning",
            workflow_stage=WorkflowStage.BEATS,
            purpose="beat_sheet_generation",
            source=generation_result.source,
            model_id=generation_result.model_id,
            prompt_version=generation_result.prompt_version,
            raw_response=generation_result.raw_response,
            elapsed_ms=_elapsed_ms_since(beat_generation_started_at),
        )
        if not generation_result.evaluation.passed:
            raise SessionBeatSheetGenerationError(
                "beat-sheet generation produced an invalid revision",
            )

        stage_map = self._stage_states.ensure_for_session(story_session)
        self._validate_stage_transition(
            stage_map,
            stage=WorkflowStage.BEATS,
            status=WorkflowStageState.IN_PROGRESS,
        )
        stage_snapshot = stage_map[WorkflowStage.BEATS]
        previous_status = stage_snapshot.status
        previous_detail = stage_snapshot.detail
        now = utc_now()

        stage_snapshot.status = WorkflowStageState.IN_PROGRESS
        stage_snapshot.detail = _build_beat_sheet_generation_stage_detail(
            generation_result.beat_sheet
        )
        stage_snapshot.started_at = stage_snapshot.started_at or now
        stage_snapshot.completed_at = None

        invalidated_stages = self._invalidate_dependent_stages(
            stage_map,
            stage=WorkflowStage.BEATS,
            detail=stage_snapshot.detail,
        )

        beat_sheet = BeatSheet(
            session_id=story_session.id,
            character_sheet_id=selected_character_sheet.id,
            revision_number=_next_beat_sheet_revision_number(
                self._sessions.list_beat_sheets(session_id)
            ),
            summary=generation_result.beat_sheet.summary,
            beats=_build_beat_sheet_persistence_payload(
                generation_result,
                generation_kind="generated",
                guidance=_normalize_optional_text(guidance),
                focus_beats=_normalize_beat_name_list(focus_beats),
                bedtime_goal=_normalize_optional_text(bedtime_goal),
                selected_pitch=selected_pitch,
                source_beat_sheet=current_selected_beat_sheet,
            ),
            bedtime_notes=generation_result.beat_sheet.bedtime_notes,
            is_selected=False,
        )
        self._session.add(beat_sheet)
        self._session.flush()
        self._apply_rollups(story_session, stage_map)

        stage_event = None
        if (
            previous_status != stage_snapshot.status
            or previous_detail != stage_snapshot.detail
            or invalidated_stages
        ):
            stage_event = self._event_log.record_stage_state_changed(
                story_session.id,
                stage=WorkflowStage.BEATS,
                previous_status=previous_status,
                status=stage_snapshot.status,
                detail=stage_snapshot.detail,
                invalidated_stages=invalidated_stages,
                current_stage=story_session.current_stage,
                resume_stage=story_session.resume_stage,
                furthest_completed_stage=story_session.furthest_completed_stage,
                overall_status=story_session.overall_status,
                actor=actor,
            )
            for invalidated_stage in invalidated_stages:
                stage_map[invalidated_stage].last_event = stage_event

        ai_event = self._event_log.record_ai_output(
            story_session.id,
            output_kind=AIOutputKind.BEAT_SHEET,
            stage=WorkflowStage.BEATS,
            resource_id=beat_sheet.id,
            candidate_count=1,
            model_id=generation_result.model_id,
            summary_text=_build_beat_sheet_generation_summary_text(generation_result.beat_sheet),
            actor=actor,
        )
        stage_snapshot.last_event = ai_event
        self._session.commit()
        return SessionBeatSheetGenerationResponse(
            snapshot=self.load_session_snapshot(story_session.id),
            event=self._event_log.build_event_view(ai_event),
        )

    def refine_beat_sheet(
        self,
        session_id: str,
        *,
        instructions: str,
        beat_sheet_id: str | None = None,
        revision_number: int | None = None,
        beat_names: list[str] | None = None,
        bedtime_goal: str | None = None,
        origin: str = "workspace",
        actor: SessionEventActor | None = None,
        beat_sheet_generation_service: BeatSheetGenerationService | None = None,
    ) -> SessionSelectionResponse:
        story_session = self._sessions.get_for_update(session_id)
        if story_session is None:
            raise SessionNotFoundError(f"session {session_id!r} was not found")

        selected_pitch = self._sessions.get_selected_pitch(session_id)
        if selected_pitch is None:
            raise SessionBeatSheetGenerationError(
                "select a pitch before refining the beat sheet",
            )

        selected_character_sheet = self._sessions.get_selected_character_sheet(session_id)
        if selected_character_sheet is None:
            raise SessionBeatSheetGenerationError(
                "select a character sheet before refining the beat sheet",
            )

        normalized_instructions = _normalize_optional_text(instructions)
        if normalized_instructions is None:
            raise SessionBeatSheetGenerationError("beat-sheet refinement instructions are required")

        source_beat_sheet = _resolve_source_beat_sheet(
            self._sessions.list_beat_sheets(session_id),
            selected_beat_sheet=self._sessions.get_selected_beat_sheet(session_id),
            beat_sheet_id=beat_sheet_id,
            revision_number=revision_number,
        )
        if source_beat_sheet is None:
            raise SessionBeatSheetSelectionError(
                "no beat sheet matched the requested refinement",
            )
        if (
            source_beat_sheet.character_sheet_id is not None
            and source_beat_sheet.character_sheet_id != selected_character_sheet.id
        ):
            raise SessionBeatSheetSelectionError(
                "the requested beat sheet belongs to a different character sheet",
            )

        active_brief = self._sessions.get_active_story_brief(session_id)
        previous_selected_beat_sheet = self._sessions.get_selected_beat_sheet(session_id)
        raw_brief = active_brief.raw_brief if active_brief is not None else selected_pitch.logline
        normalized_summary = active_brief.normalized_summary if active_brief is not None else None
        normalized_beat_names = _normalize_beat_name_list(beat_names)
        normalized_bedtime_goal = _normalize_optional_text(bedtime_goal)
        generator = beat_sheet_generation_service or BeatSheetGenerationService()
        beat_refinement_started_at = perf_counter()
        generation_result = generator.generate_beat_sheet(
            generation_goal="refinement",
            selected_pitch=_build_selected_pitch_context(selected_pitch),
            selected_character_sheet=_build_existing_character_sheet_context(
                selected_character_sheet
            ),
            raw_brief=raw_brief,
            genre_label=(
                story_session.selected_genre.label
                if story_session.selected_genre is not None
                else None
            ),
            genre_description=(
                story_session.selected_genre.description
                if story_session.selected_genre is not None
                else None
            ),
            genre_bedtime_safety_notes=(
                story_session.selected_genre.bedtime_safety_notes
                if story_session.selected_genre is not None
                else None
            ),
            tone_label=(
                story_session.selected_tone_profile.label
                if story_session.selected_tone_profile is not None
                else None
            ),
            tone_description=(
                story_session.selected_tone_profile.description
                if story_session.selected_tone_profile is not None
                else None
            ),
            tone_bedtime_notes=(
                story_session.selected_tone_profile.bedtime_notes
                if story_session.selected_tone_profile is not None
                else None
            ),
            normalized_summary=normalized_summary,
            story_idea=active_brief.story_idea if active_brief is not None else None,
            desired_themes=active_brief.desired_themes if active_brief is not None else None,
            key_images=active_brief.key_images if active_brief is not None else None,
            audience_notes=active_brief.audience_notes if active_brief is not None else None,
            must_have_elements=(
                active_brief.must_have_elements if active_brief is not None else None
            ),
            planning_notes=active_brief.planning_notes if active_brief is not None else None,
            normalized_preferences=NormalizedBriefPreferences.model_validate(
                active_brief.normalized_preferences if active_brief is not None else {}
            ),
            instructions=normalized_instructions,
            focus_beats=normalized_beat_names,
            bedtime_goal=normalized_bedtime_goal,
            existing_beat_sheet=_build_existing_beat_sheet_context(source_beat_sheet),
        )
        _record_session_model_usage(
            session=self._session,
            session_id=story_session.id,
            usage_bucket="planning",
            workflow_stage=WorkflowStage.BEATS,
            purpose="beat_sheet_refinement",
            source=generation_result.source,
            model_id=generation_result.model_id,
            prompt_version=generation_result.prompt_version,
            raw_response=generation_result.raw_response,
            elapsed_ms=_elapsed_ms_since(beat_refinement_started_at),
        )
        if not generation_result.evaluation.passed:
            raise SessionBeatSheetGenerationError(
                "beat-sheet refinement produced an invalid revision",
            )

        stage_map = self._stage_states.ensure_for_session(story_session)
        self._validate_stage_transition(
            stage_map,
            stage=WorkflowStage.BEATS,
            status=WorkflowStageState.COMPLETED,
        )
        stage_snapshot = stage_map[WorkflowStage.BEATS]
        previous_status = stage_snapshot.status
        previous_detail = stage_snapshot.detail
        now = utc_now()

        for beat_sheet in self._sessions.list_beat_sheets(session_id):
            beat_sheet.is_selected = False

        refinement_rationale = _build_beat_sheet_refinement_rationale(
            source_beat_sheet,
            normalized_instructions,
            beat_names=normalized_beat_names,
            bedtime_goal=normalized_bedtime_goal,
        )
        refined_beat_sheet = BeatSheet(
            session_id=story_session.id,
            character_sheet_id=selected_character_sheet.id,
            revision_number=_next_beat_sheet_revision_number(
                self._sessions.list_beat_sheets(session_id)
            ),
            summary=generation_result.beat_sheet.summary,
            beats=_build_beat_sheet_persistence_payload(
                generation_result,
                generation_kind="refinement",
                guidance=normalized_instructions,
                focus_beats=normalized_beat_names,
                bedtime_goal=normalized_bedtime_goal,
                selected_pitch=selected_pitch,
                source_beat_sheet=source_beat_sheet,
                selection_rationale=refinement_rationale,
            ),
            bedtime_notes=generation_result.beat_sheet.bedtime_notes,
            is_selected=True,
            accepted_at=now,
        )
        self._session.add(refined_beat_sheet)
        self._session.flush()

        stage_snapshot.status = WorkflowStageState.COMPLETED
        stage_snapshot.detail = _build_beat_sheet_selection_detail(refined_beat_sheet)
        stage_snapshot.started_at = stage_snapshot.started_at or now
        stage_snapshot.completed_at = now

        invalidated_stages = self._invalidate_dependent_stages(
            stage_map,
            stage=WorkflowStage.BEATS,
            detail=_build_beat_sheet_invalidation_detail(refined_beat_sheet),
        )
        self._apply_rollups(story_session, stage_map)

        stage_event = None
        if (
            previous_status != stage_snapshot.status
            or previous_detail != stage_snapshot.detail
            or invalidated_stages
        ):
            stage_event = self._event_log.record_stage_state_changed(
                story_session.id,
                stage=WorkflowStage.BEATS,
                previous_status=previous_status,
                status=stage_snapshot.status,
                detail=stage_snapshot.detail,
                invalidated_stages=invalidated_stages,
                current_stage=story_session.current_stage,
                resume_stage=story_session.resume_stage,
                furthest_completed_stage=story_session.furthest_completed_stage,
                overall_status=story_session.overall_status,
                actor=actor,
            )
            for invalidated_stage in invalidated_stages:
                stage_map[invalidated_stage].last_event = stage_event

        self._event_log.record_ai_output(
            story_session.id,
            output_kind=AIOutputKind.BEAT_SHEET,
            stage=WorkflowStage.BEATS,
            resource_id=refined_beat_sheet.id,
            candidate_count=1,
            model_id=generation_result.model_id,
            summary_text=_build_beat_sheet_refinement_summary_text(
                refined_beat_sheet,
                source_beat_sheet=source_beat_sheet,
            ),
            actor=actor,
        )
        selection_event = self._event_log.record_selection(
            story_session.id,
            selection_kind=SelectionKind.BEAT_SHEET,
            stage=WorkflowStage.BEATS,
            label=_read_beat_sheet_label(refined_beat_sheet),
            selection_id=refined_beat_sheet.id,
            rationale=refinement_rationale,
            previous_selection_id=(
                previous_selected_beat_sheet.id
                if previous_selected_beat_sheet is not None
                else None
            ),
            source=origin,
            accepted=True,
            actor=actor,
        )
        self._refresh_continuity(
            story_session.id,
            source_stage=WorkflowStage.BEATS,
            source_summary=selection_event.summary,
        )
        self._capture_plan_revision(
            story_session.id,
            source_stage=WorkflowStage.BEATS,
            change_summary=selection_event.summary,
        )
        stage_snapshot.last_event = selection_event
        self._session.commit()
        return SessionSelectionResponse(
            snapshot=self.load_session_snapshot(story_session.id),
            event=self._event_log.build_event_view(selection_event),
        )

    def edit_beat_sheet(
        self,
        session_id: str,
        *,
        payload: EditSessionBeatSheetRequest,
        actor: SessionEventActor | None = None,
    ) -> SessionBeatSheetUpdateResponse:
        story_session = self._sessions.get_for_update(session_id)
        if story_session is None:
            raise SessionNotFoundError(f"session {session_id!r} was not found")

        selected_character_sheet = self._sessions.get_selected_character_sheet(session_id)
        if selected_character_sheet is None:
            raise SessionBeatSheetEditError(
                "select a character sheet before editing the beat sheet"
            )

        selected_beat_sheet = self._sessions.get_selected_beat_sheet(session_id)
        target_beat_sheet = _resolve_source_beat_sheet(
            self._sessions.list_beat_sheets(session_id),
            selected_beat_sheet=selected_beat_sheet,
            beat_sheet_id=payload.beat_sheet_id,
            revision_number=payload.revision_number,
        )
        if target_beat_sheet is None:
            raise SessionBeatSheetSelectionError("no beat sheet matched the requested edit")
        if (
            target_beat_sheet.character_sheet_id is not None
            and target_beat_sheet.character_sheet_id != selected_character_sheet.id
        ):
            raise SessionBeatSheetSelectionError(
                "the requested beat sheet belongs to a different character sheet"
            )

        existing_payload = _read_beat_sheet_payload_mapping(target_beat_sheet)
        normalized_updates = _normalize_beat_sheet_edit_updates(payload.beat_updates)
        updated_beats, beat_changed_fields, beat_keys = _apply_beat_sheet_edit_updates(
            _read_serialized_beat_sheet_beats(target_beat_sheet),
            normalized_updates,
        )
        normalized_summary = _normalize_optional_text(payload.summary)
        normalized_bedtime_notes = _normalize_optional_text(payload.bedtime_notes)
        normalized_bedtime_goal = _normalize_optional_text(payload.bedtime_goal)

        changed_fields: list[str] = []
        event_field_values: dict[str, Any] = {}
        next_summary = target_beat_sheet.summary
        next_bedtime_notes = target_beat_sheet.bedtime_notes

        if normalized_summary is not None and normalized_summary != target_beat_sheet.summary:
            next_summary = normalized_summary
            changed_fields.append("summary")
            event_field_values["summary"] = normalized_summary

        if (
            normalized_bedtime_notes is not None
            and normalized_bedtime_notes != target_beat_sheet.bedtime_notes
        ):
            next_bedtime_notes = normalized_bedtime_notes
            changed_fields.append("bedtime_notes")
            event_field_values["bedtime_notes"] = normalized_bedtime_notes

        next_payload = dict(existing_payload)
        if (
            normalized_bedtime_goal is not None
            and normalized_bedtime_goal
            != _read_optional_mapping_text(existing_payload, "bedtime_goal")
        ):
            next_payload["bedtime_goal"] = normalized_bedtime_goal
            changed_fields.append("bedtime_goal")
            event_field_values["bedtime_goal"] = normalized_bedtime_goal

        if beat_changed_fields:
            next_payload["beats"] = updated_beats
            changed_fields.extend(beat_changed_fields)
            event_field_values["beat_updates"] = [dict(update) for update in normalized_updates]

        if not changed_fields:
            raise SessionBeatSheetEditError("beat-sheet edit did not change any saved fields")

        now = utc_now()
        refreshes_downstream = bool(target_beat_sheet.is_selected)
        summary_text = _build_beat_sheet_edit_summary_text(
            target_beat_sheet,
            beat_keys=beat_keys,
            changed_fields=changed_fields,
            refreshes_downstream=refreshes_downstream,
            requested_summary=_normalize_optional_text(payload.summary_text),
        )
        next_payload["edit_history"] = [
            _build_beat_sheet_edit_history_entry(
                summary_text=summary_text,
                origin=payload.origin,
                changed_fields=changed_fields,
                beat_keys=beat_keys,
                refreshes_downstream=refreshes_downstream,
                created_at=now,
            ),
            *_read_beat_sheet_edit_history_payload(existing_payload),
        ]
        next_payload["generation_kind"] = "edited"
        next_payload["refinement"] = {
            **_read_beat_sheet_refinement_payload(existing_payload),
            "source_beat_sheet_id": target_beat_sheet.id,
            "source_beat_sheet_revision_number": target_beat_sheet.revision_number,
        }

        if refreshes_downstream:
            for beat_sheet in self._sessions.list_beat_sheets(session_id):
                beat_sheet.is_selected = False

        edited_beat_sheet = BeatSheet(
            session_id=story_session.id,
            character_sheet_id=target_beat_sheet.character_sheet_id,
            revision_number=_next_beat_sheet_revision_number(
                self._sessions.list_beat_sheets(session_id)
            ),
            summary=next_summary,
            beats=next_payload,
            bedtime_notes=next_bedtime_notes,
            is_selected=refreshes_downstream,
            accepted_at=now if refreshes_downstream else None,
        )
        self._session.add(edited_beat_sheet)
        self._session.flush()

        stage_map = self._stage_states.ensure_for_session(story_session)
        stage_snapshot = stage_map[WorkflowStage.BEATS]
        previous_status = stage_snapshot.status
        previous_detail = stage_snapshot.detail
        invalidated_stages: list[WorkflowStage] = []
        touches_stage_state = False

        if refreshes_downstream:
            if stage_snapshot.status != WorkflowStageState.COMPLETED:
                self._validate_stage_transition(
                    stage_map,
                    stage=WorkflowStage.BEATS,
                    status=WorkflowStageState.COMPLETED,
                )
                stage_snapshot.status = WorkflowStageState.COMPLETED
            stage_snapshot.detail = _build_beat_sheet_selection_detail(edited_beat_sheet)
            stage_snapshot.started_at = stage_snapshot.started_at or now
            stage_snapshot.completed_at = stage_snapshot.completed_at or now
            invalidated_stages = self._invalidate_dependent_stages(
                stage_map,
                stage=WorkflowStage.BEATS,
                detail=_build_beat_sheet_edit_invalidation_detail(
                    edited_beat_sheet,
                    summary_text=summary_text,
                ),
            )
            touches_stage_state = True
        elif selected_beat_sheet is None:
            if stage_snapshot.status == WorkflowStageState.DRAFT:
                self._validate_stage_transition(
                    stage_map,
                    stage=WorkflowStage.BEATS,
                    status=WorkflowStageState.IN_PROGRESS,
                )
            stage_snapshot.status = WorkflowStageState.IN_PROGRESS
            stage_snapshot.detail = _build_beat_sheet_edit_stage_detail(edited_beat_sheet)
            stage_snapshot.started_at = stage_snapshot.started_at or now
            stage_snapshot.completed_at = None
            touches_stage_state = True

        if touches_stage_state:
            self._apply_rollups(story_session, stage_map)

        stage_event = None
        if touches_stage_state and (
            previous_status != stage_snapshot.status
            or previous_detail != stage_snapshot.detail
            or invalidated_stages
        ):
            stage_event = self._event_log.record_stage_state_changed(
                story_session.id,
                stage=WorkflowStage.BEATS,
                previous_status=previous_status,
                status=stage_snapshot.status,
                detail=stage_snapshot.detail,
                invalidated_stages=invalidated_stages,
                current_stage=story_session.current_stage,
                resume_stage=story_session.resume_stage,
                furthest_completed_stage=story_session.furthest_completed_stage,
                overall_status=story_session.overall_status,
                actor=actor,
            )
            for invalidated_stage in invalidated_stages:
                stage_map[invalidated_stage].last_event = stage_event

        event_field_values["material_change"] = True
        event_field_values["refreshes_downstream"] = refreshes_downstream
        edit_event = self._event_log.record_user_edit(
            story_session.id,
            target_kind=UserEditTargetKind.BEAT_SHEET,
            stage=WorkflowStage.BEATS,
            changed_fields=changed_fields,
            target_id=edited_beat_sheet.id,
            revision_number=edited_beat_sheet.revision_number,
            source=payload.origin,
            field_values=event_field_values,
            summary_text=summary_text,
            actor=actor,
        )
        if refreshes_downstream:
            self._refresh_continuity(
                story_session.id,
                source_stage=WorkflowStage.BEATS,
                source_summary=edit_event.summary,
            )
            self._capture_plan_revision(
                story_session.id,
                source_stage=WorkflowStage.BEATS,
                change_summary=summary_text,
            )
        stage_snapshot.last_event = edit_event
        self._session.commit()
        return SessionBeatSheetUpdateResponse(
            snapshot=self.load_session_snapshot(story_session.id),
            event=self._event_log.build_event_view(edit_event),
        )

    def select_beat_sheet(
        self,
        session_id: str,
        *,
        beat_sheet_id: str | None = None,
        revision_number: int | None = None,
        origin: str = "workspace",
        actor: SessionEventActor | None = None,
    ) -> SessionSelectionResponse:
        story_session = self._sessions.get_for_update(session_id)
        if story_session is None:
            raise SessionNotFoundError(f"session {session_id!r} was not found")

        selected_character_sheet = self._sessions.get_selected_character_sheet(session_id)
        if selected_character_sheet is None:
            raise SessionBeatSheetSelectionError(
                "select a character sheet before choosing a beat sheet"
            )

        matches = _find_matching_beat_sheets(
            self._sessions.list_beat_sheets(session_id),
            beat_sheet_id=beat_sheet_id,
            revision_number=revision_number,
        )
        if not matches:
            raise SessionBeatSheetSelectionError(
                "no generated beat sheet matched the requested selection"
            )
        if len(matches) > 1:
            raise SessionBeatSheetSelectionError(
                "the requested beat-sheet selection matched more than one revision"
            )

        selected_beat_sheet = matches[0]
        if (
            selected_beat_sheet.character_sheet_id is not None
            and selected_beat_sheet.character_sheet_id != selected_character_sheet.id
        ):
            raise SessionBeatSheetSelectionError(
                "the requested beat sheet belongs to a different character sheet"
            )

        previous_selected_beat_sheet = self._sessions.get_selected_beat_sheet(session_id)
        for beat_sheet in self._sessions.list_beat_sheets(session_id):
            beat_sheet.is_selected = beat_sheet.id == selected_beat_sheet.id

        now = utc_now()
        selected_beat_sheet.accepted_at = now

        stage_map = self._stage_states.ensure_for_session(story_session)
        self._validate_stage_transition(
            stage_map,
            stage=WorkflowStage.BEATS,
            status=WorkflowStageState.COMPLETED,
        )
        stage_snapshot = stage_map[WorkflowStage.BEATS]
        previous_status = stage_snapshot.status
        previous_detail = stage_snapshot.detail

        stage_snapshot.status = WorkflowStageState.COMPLETED
        stage_snapshot.detail = _build_beat_sheet_selection_detail(selected_beat_sheet)
        stage_snapshot.started_at = stage_snapshot.started_at or now
        stage_snapshot.completed_at = now

        invalidated_stages = self._invalidate_dependent_stages(
            stage_map,
            stage=WorkflowStage.BEATS,
            detail=_build_beat_sheet_invalidation_detail(selected_beat_sheet),
        )
        self._apply_rollups(story_session, stage_map)

        if (
            previous_status != stage_snapshot.status
            or previous_detail != stage_snapshot.detail
            or invalidated_stages
        ):
            stage_event = self._event_log.record_stage_state_changed(
                story_session.id,
                stage=WorkflowStage.BEATS,
                previous_status=previous_status,
                status=stage_snapshot.status,
                detail=stage_snapshot.detail,
                invalidated_stages=invalidated_stages,
                current_stage=story_session.current_stage,
                resume_stage=story_session.resume_stage,
                furthest_completed_stage=story_session.furthest_completed_stage,
                overall_status=story_session.overall_status,
                actor=actor,
            )
            for invalidated_stage in invalidated_stages:
                stage_map[invalidated_stage].last_event = stage_event

        selection_event = self._event_log.record_selection(
            story_session.id,
            selection_kind=SelectionKind.BEAT_SHEET,
            stage=WorkflowStage.BEATS,
            label=_read_beat_sheet_label(selected_beat_sheet),
            selection_id=selected_beat_sheet.id,
            rationale=_read_beat_sheet_selection_rationale(selected_beat_sheet),
            previous_selection_id=(
                previous_selected_beat_sheet.id
                if previous_selected_beat_sheet is not None
                else None
            ),
            source=origin,
            accepted=True,
            actor=actor,
        )
        self._refresh_continuity(
            story_session.id,
            source_stage=WorkflowStage.BEATS,
            source_summary=selection_event.summary,
        )
        self._capture_plan_revision(
            story_session.id,
            source_stage=WorkflowStage.BEATS,
            change_summary=selection_event.summary,
        )
        stage_snapshot.last_event = selection_event
        self._session.commit()
        return SessionSelectionResponse(
            snapshot=self.load_session_snapshot(story_session.id),
            event=self._event_log.build_event_view(selection_event),
        )

    def restore_plan_revision(
        self,
        session_id: str,
        *,
        revision_number: int,
        origin: str = "workspace",
        actor: SessionEventActor | None = None,
    ) -> SessionSelectionResponse:
        story_session = self._sessions.get_for_update(session_id)
        if story_session is None:
            raise SessionNotFoundError(f"session {session_id!r} was not found")

        target_plan_revision = self._plan_revisions.get_revision_by_number(
            session_id,
            revision_number,
        )
        if target_plan_revision is None:
            raise SessionPlanRevisionError(
                f"plan revision {revision_number} was not found for session {session_id!r}"
            )

        current_plan_revision = self._plan_revisions.get_current_revision(session_id)
        if (
            current_plan_revision is not None
            and current_plan_revision.id == target_plan_revision.id
        ):
            raise SessionPlanRevisionError(f"plan revision {revision_number} is already current")
        if current_plan_revision is not None and _plan_revisions_match(
            current_plan_revision, target_plan_revision
        ):
            raise SessionPlanRevisionError(
                f"plan revision {revision_number} already matches the current selected plan"
            )

        target_pitch = _require_session_scoped_row(
            row=target_plan_revision.pitch,
            session_id=session_id,
            label="pitch",
        )
        target_character_sheet = _require_session_scoped_row(
            row=target_plan_revision.character_sheet,
            session_id=session_id,
            label="character sheet",
        )
        target_beat_sheet = _require_session_scoped_row(
            row=target_plan_revision.beat_sheet,
            session_id=session_id,
            label="beat sheet",
        )
        target_story_setup = _require_session_scoped_row(
            row=target_plan_revision.story_setup,
            session_id=session_id,
            label="story setup",
        )
        target_story_outline = _require_session_scoped_row(
            row=target_plan_revision.story_outline,
            session_id=session_id,
            label="story outline",
        )

        _apply_selected_state(
            self._sessions.list_pitches(session_id),
            target_plan_revision.pitch_id,
        )
        _apply_selected_state(
            self._sessions.list_character_sheets(session_id),
            target_plan_revision.character_sheet_id,
        )
        _apply_selected_state(
            self._sessions.list_beat_sheets(session_id),
            target_plan_revision.beat_sheet_id,
        )
        _apply_selected_state(
            self._list_story_setups(session_id),
            target_plan_revision.story_setup_id,
        )
        _apply_selected_state(
            self._sessions.list_story_outlines(session_id),
            target_plan_revision.story_outline_id,
        )

        restored_stage = _resolve_restored_plan_stage(
            pitch=target_pitch,
            character_sheet=target_character_sheet,
            beat_sheet=target_beat_sheet,
            story_setup=target_story_setup,
        )
        if restored_stage is None:
            raise SessionPlanRevisionError(
                f"plan revision {revision_number} does not contain a restorable selection"
            )

        restore_reason = f"Restored plan revision {target_plan_revision.revision_number}."
        self._cancel_active_composition_jobs(
            session_id,
            reason=f"{restore_reason} Active composition was cancelled.",
        )
        self._cancel_active_audio_jobs(
            session_id,
            reason=f"{restore_reason} Active audio generation was cancelled.",
        )

        stage_map = self._stage_states.ensure_for_session(story_session)
        now = utc_now()
        invalidated_stages = self._invalidate_dependent_stages(
            stage_map,
            stage=restored_stage,
            detail=restore_reason,
        )

        stage_updates = {
            WorkflowStage.PITCHES: (
                target_pitch is not None,
                (
                    _build_pitch_selection_detail(target_pitch)
                    if target_pitch is not None
                    else restore_reason
                ),
            ),
            WorkflowStage.CHARACTERS: (
                target_character_sheet is not None,
                _build_character_sheet_selection_detail(target_character_sheet)
                if target_character_sheet is not None
                else restore_reason,
            ),
            WorkflowStage.BEATS: (
                target_beat_sheet is not None,
                _build_beat_sheet_selection_detail(target_beat_sheet)
                if target_beat_sheet is not None
                else restore_reason,
            ),
            WorkflowStage.STORY_SETUP: (
                target_story_setup is not None,
                _build_story_setup_restore_detail(
                    target_story_setup,
                    target_story_outline,
                    restore_reason=restore_reason,
                )
                if target_story_setup is not None
                else restore_reason,
            ),
        }

        changed_stages: list[tuple[WorkflowStage, WorkflowStageState]] = []
        for stage, (is_completed, detail) in stage_updates.items():
            snapshot = stage_map[stage]
            previous_status = snapshot.status
            previous_detail = snapshot.detail
            if is_completed:
                snapshot.status = WorkflowStageState.COMPLETED
                snapshot.detail = detail
                snapshot.started_at = snapshot.started_at or now
                snapshot.completed_at = now
            elif stage.value in {item.value for item in invalidated_stages}:
                snapshot.status = WorkflowStageState.NEEDS_REGENERATION
                snapshot.detail = restore_reason
                snapshot.completed_at = None
            elif snapshot.status != WorkflowStageState.DRAFT:
                snapshot.status = WorkflowStageState.NEEDS_REGENERATION
                snapshot.detail = restore_reason
                snapshot.completed_at = None

            if previous_status != snapshot.status or previous_detail != snapshot.detail:
                changed_stages.append((stage, previous_status))

        self._apply_rollups(story_session, stage_map)

        deepest_stage_event = None
        for stage, previous_status in changed_stages:
            stage_event = self._event_log.record_stage_state_changed(
                story_session.id,
                stage=stage,
                previous_status=previous_status,
                status=stage_map[stage].status,
                detail=stage_map[stage].detail,
                invalidated_stages=invalidated_stages if stage == restored_stage else [],
                current_stage=story_session.current_stage,
                resume_stage=story_session.resume_stage,
                furthest_completed_stage=story_session.furthest_completed_stage,
                overall_status=story_session.overall_status,
                actor=actor,
            )
            stage_map[stage].last_event = stage_event
            if stage == restored_stage:
                deepest_stage_event = stage_event

        if deepest_stage_event is not None:
            for invalidated_stage in invalidated_stages:
                stage_map[invalidated_stage].last_event = deepest_stage_event

        selection_event = self._event_log.record_selection(
            story_session.id,
            selection_kind=SelectionKind.PLAN_REVISION,
            stage=restored_stage,
            label=f"Revision {target_plan_revision.revision_number}",
            selection_id=target_plan_revision.id,
            rationale=target_plan_revision.change_summary,
            previous_selection_id=(
                current_plan_revision.id if current_plan_revision is not None else None
            ),
            source=origin,
            accepted=True,
            actor=actor,
        )
        self._refresh_continuity(
            story_session.id,
            source_stage=restored_stage,
            source_summary=selection_event.summary,
        )
        self._capture_plan_revision(
            story_session.id,
            source_stage=restored_stage,
            change_summary=selection_event.summary,
            restored_from_revision=target_plan_revision,
        )
        stage_map[restored_stage].last_event = selection_event
        self._session.commit()
        return SessionSelectionResponse(
            snapshot=self.load_session_snapshot(story_session.id),
            event=self._event_log.build_event_view(selection_event),
        )

    def apply_context_update(
        self,
        session_id: str,
        *,
        payload: SessionContextUpdateRequest,
        actor: SessionEventActor | None = None,
    ) -> SessionContextUpdateResponse:
        story_session = self._sessions.get_for_update(session_id)
        if story_session is None:
            raise SessionNotFoundError(f"session {session_id!r} was not found")

        if payload.target_kind != "stage_note":
            raise UnsupportedSessionContextUpdateError(
                f"unsupported context update kind {payload.target_kind!r}"
            )

        target_kind = STAGE_EDIT_TARGET_KIND_MAP.get(payload.stage)
        if target_kind is None:
            raise UnsupportedSessionContextUpdateError(
                f"stage {payload.stage.value!r} does not support durable note edits"
            )

        stage_map = self._stage_states.ensure_for_session(story_session)
        stage_snapshot = stage_map[payload.stage]
        previous_status = stage_snapshot.status
        now = utc_now()
        normalized_detail = _normalize_optional_text(payload.values.detail)

        if stage_snapshot.status == WorkflowStageState.DRAFT:
            self._validate_stage_transition(
                stage_map,
                stage=payload.stage,
                status=WorkflowStageState.IN_PROGRESS,
            )
            stage_snapshot.status = WorkflowStageState.IN_PROGRESS
            stage_snapshot.started_at = stage_snapshot.started_at or now
        elif stage_snapshot.status == WorkflowStageState.NEEDS_REGENERATION:
            stage_snapshot.status = WorkflowStageState.IN_PROGRESS
            stage_snapshot.started_at = stage_snapshot.started_at or now
            stage_snapshot.completed_at = None

        stage_snapshot.detail = normalized_detail
        invalidated_stages = self._invalidate_dependent_stages(
            stage_map,
            stage=payload.stage,
            detail=normalized_detail,
        )
        self._apply_rollups(story_session, stage_map)

        if previous_status != stage_snapshot.status or invalidated_stages:
            stage_event = self._event_log.record_stage_state_changed(
                story_session.id,
                stage=payload.stage,
                previous_status=previous_status,
                status=stage_snapshot.status,
                detail=stage_snapshot.detail,
                invalidated_stages=invalidated_stages,
                current_stage=story_session.current_stage,
                resume_stage=story_session.resume_stage,
                furthest_completed_stage=story_session.furthest_completed_stage,
                overall_status=story_session.overall_status,
                actor=actor,
            )
            for invalidated_stage in invalidated_stages:
                stage_map[invalidated_stage].last_event = stage_event

        edit_event = self._event_log.record_user_edit(
            story_session.id,
            target_kind=target_kind,
            stage=payload.stage,
            changed_fields=["detail"],
            source=payload.origin,
            field_values={
                "detail": normalized_detail,
                "control_id": payload.control_id,
            },
            summary_text=_build_stage_note_summary(payload.stage, normalized_detail),
            actor=actor,
        )
        stage_snapshot.last_event = edit_event
        self._session.commit()
        return SessionContextUpdateResponse(
            snapshot=self.load_session_snapshot(story_session.id),
            event=self._event_log.build_event_view(edit_event),
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

    def _refresh_continuity(
        self,
        session_id: str,
        *,
        source_stage: WorkflowStage | None,
        source_summary: str | None = None,
    ) -> None:
        self._continuity.refresh_for_session(
            session_id,
            source_stage=source_stage,
            source_summary=source_summary,
        )

    def _capture_plan_revision(
        self,
        session_id: str,
        *,
        source_stage: WorkflowStage | None,
        change_summary: str | None,
        restored_from_revision=None,
    ) -> None:
        self._plan_revisions.capture_current_state(
            session_id,
            source_stage=source_stage,
            change_summary=change_summary,
            restored_from_revision=restored_from_revision,
        )

    def _list_story_setups(self, session_id: str) -> list[StorySetup]:
        stmt = (
            select(StorySetup)
            .where(StorySetup.session_id == session_id)
            .order_by(StorySetup.created_at.asc(), StorySetup.revision_number.asc())
        )
        return list(self._session.execute(stmt).scalars().all())

    def _cancel_active_composition_jobs(self, session_id: str, *, reason: str) -> None:
        stmt = select(CompositionJob).where(
            CompositionJob.session_id == session_id,
            CompositionJob.status.in_((JobStatus.QUEUED, JobStatus.IN_PROGRESS, JobStatus.PAUSED)),
        )
        for row in self._session.execute(stmt).scalars().all():
            row.status = JobStatus.CANCELLED
            row.stop_reason = reason
            row.completed_at = row.completed_at or utc_now()
            for segment in row.segments:
                if segment.status in (
                    JobStatus.QUEUED,
                    JobStatus.IN_PROGRESS,
                    JobStatus.PAUSED,
                ):
                    segment.status = JobStatus.CANCELLED

    def _cancel_active_audio_jobs(self, session_id: str, *, reason: str) -> None:
        stmt = select(AudioJob).where(
            AudioJob.session_id == session_id,
            AudioJob.status.in_((JobStatus.QUEUED, JobStatus.IN_PROGRESS, JobStatus.PAUSED)),
        )
        for row in self._session.execute(stmt).scalars().all():
            row.status = JobStatus.CANCELLED
            row.stop_reason = reason
            row.completed_at = row.completed_at or utc_now()

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

    def _load_active_genre(
        self,
        *,
        genre_id: str | None = None,
        genre_slug: str | None = None,
        genre_label: str | None = None,
    ):
        return find_active_genre(
            self._session,
            genre_id=genre_id,
            genre_slug=genre_slug,
            genre_label=genre_label,
        )

    def _load_active_tone_for_genre(
        self,
        *,
        genre_id: str,
        tone_profile_id: str | None = None,
        tone_profile_slug: str | None = None,
        tone_profile_label: str | None = None,
    ):
        return find_active_tone_for_genre(
            self._session,
            genre_id=genre_id,
            tone_profile_id=tone_profile_id,
            tone_profile_slug=tone_profile_slug,
            tone_profile_label=tone_profile_label,
        )

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
        statuses = {stage: getattr(stage_map[stage], "status") for stage in stage_map}
        resume_stage = resolve_resume_stage(statuses)
        furthest_completed_stage = resolve_furthest_completed_stage(statuses)
        overall_status = resolve_overall_status(statuses)

        story_session.current_stage = resume_stage
        story_session.resume_stage = resume_stage
        story_session.furthest_completed_stage = furthest_completed_stage
        story_session.overall_status = overall_status
        story_session.completed_at = (
            utc_now() if overall_status == WorkflowStageState.COMPLETED else None
        )


def _normalize_optional_text(value: str | None) -> str | None:
    if value is None:
        return None

    normalized = value.strip()
    return normalized or None


def _apply_selected_state(rows: list[Any], selected_id: str | None) -> None:
    for row in rows:
        row.is_selected = row.id == selected_id


def _require_session_scoped_row(*, row, session_id: str, label: str):
    if row is None:
        return None

    if getattr(row, "session_id", None) != session_id:
        raise SessionPlanRevisionError(
            f"the restored {label} does not belong to session {session_id!r}"
        )

    return row


def _resolve_restored_plan_stage(
    *,
    pitch,
    character_sheet,
    beat_sheet,
    story_setup,
) -> WorkflowStage | None:
    if story_setup is not None:
        return WorkflowStage.STORY_SETUP
    if beat_sheet is not None:
        return WorkflowStage.BEATS
    if character_sheet is not None:
        return WorkflowStage.CHARACTERS
    if pitch is not None:
        return WorkflowStage.PITCHES
    return None


def _build_story_setup_restore_detail(
    story_setup: StorySetup,
    story_outline: StoryOutline | None,
    *,
    restore_reason: str,
) -> str:
    parts: list[str] = []
    setup_label = _build_story_setup_label(story_setup)
    if setup_label:
        parts.append(setup_label)
    if story_outline is not None:
        card_count = len(story_outline.cards) if isinstance(story_outline.cards, list) else 0
        parts.append(f"Outline ready: {story_outline.outline_kind} plan with {card_count} cards.")
    parts.append(restore_reason)
    return " ".join(parts)


def _build_story_setup_label(story_setup: StorySetup) -> str:
    parts: list[str] = []
    if story_setup.target_runtime_minutes is not None:
        parts.append(f"~{story_setup.target_runtime_minutes} minutes")
    if story_setup.target_word_count is not None:
        parts.append(f"{story_setup.target_word_count} words")
    if story_setup.chapter_count is not None:
        parts.append(f"{story_setup.chapter_count} chapters")
    if story_setup.approximate_scene_count is not None:
        parts.append(f"about {story_setup.approximate_scene_count} scenes")
    if story_setup.chapter_style:
        parts.append(story_setup.chapter_style)
    if story_setup.guidance_notes:
        parts.append(story_setup.guidance_notes)
    return ", ".join(parts) if parts else "Story setup preferences"


def _plan_revisions_match(left, right) -> bool:
    return (
        getattr(left, "pitch_id", None) == getattr(right, "pitch_id", None)
        and getattr(left, "character_sheet_id", None) == getattr(right, "character_sheet_id", None)
        and getattr(left, "beat_sheet_id", None) == getattr(right, "beat_sheet_id", None)
        and getattr(left, "story_setup_id", None) == getattr(right, "story_setup_id", None)
        and getattr(left, "story_outline_id", None) == getattr(right, "story_outline_id", None)
    )


def _read_optional_mapping_text(data: Mapping[str, Any], key: str) -> str | None:
    value = data.get(key)
    return value if isinstance(value, str) else None


def _stages_before(stage: WorkflowStage) -> tuple[WorkflowStage, ...]:
    stages = WORKFLOW_STAGE_SEQUENCE
    return stages[: stages.index(stage)]


def _build_stage_note_summary(stage: WorkflowStage, detail: str | None) -> str:
    label = get_workflow_stage_definition(stage).label
    if detail:
        return f"Updated {label.lower()} notes from the workspace."
    return f"Cleared {label.lower()} notes from the workspace."


def _build_genre_selection_detail(label: str) -> str:
    return f"Selected genre: {label}. Tone choices filter from this lane next."


def _build_genre_invalidation_detail(label: str) -> str:
    return f"Genre changed to {label}. Revisit tone and any downstream planning."


def _build_tone_selection_detail(label: str) -> str:
    return f"Selected tone: {label}. The story brief will inherit this bedtime texture."


def _build_tone_invalidation_detail(label: str) -> str:
    return f"Tone changed to {label}. Revisit the brief and any downstream planning."


def _build_selected_pitch_context(pitch: Pitch) -> ExistingSelectedPitchContext:
    return ExistingSelectedPitchContext(
        title=pitch.title,
        hook=pitch.logline,
        central_conflict=pitch.summary,
        why_it_fits=pitch.bedtime_notes,
    )


def _build_pitch_generation_key() -> str:
    return f"pitch-batch-{uuid4().hex[:12]}"


def _build_character_generation_key() -> str:
    return f"character-batch-{uuid4().hex[:12]}"


def _build_pitch_generation_stage_detail(candidate_count: int) -> str:
    return f"Generated {candidate_count} pitch options. Select one to continue."


def _build_character_sheet_generation_stage_detail(candidate_count: int) -> str:
    return f"Generated {candidate_count} character options. Select one to continue."


def _build_pitch_generation_summary_text(pitches: list[object]) -> str:
    titles = [getattr(pitch, "title", None) for pitch in pitches]
    summarized_titles = [title for title in titles if isinstance(title, str) and title]
    if not summarized_titles:
        return "Generated a fresh pitch batch."

    return "Generated pitches: " + ", ".join(summarized_titles[:3]) + "."


def _build_character_sheet_generation_summary_text(character_sheets: list[object]) -> str:
    titles = [getattr(character_sheet, "title", None) for character_sheet in character_sheets]
    summarized_titles = [title for title in titles if isinstance(title, str) and title]
    if not summarized_titles:
        return "Generated a fresh character-sheet batch."

    return "Generated character sheets: " + ", ".join(summarized_titles[:3]) + "."


def _build_pitch_refinement_rationale(pitch: Pitch, instructions: str) -> str:
    return f'Refined from "{pitch.title}" with: {instructions}'


def _build_character_sheet_refinement_rationale(
    character_sheet: CharacterSheet,
    instructions: str,
    *,
    focus_character_names: list[str],
    change_summary: str | None,
    change_impact: CharacterChangeImpact,
) -> str:
    focus_tail = ""
    if focus_character_names:
        focus_tail = f" Focus characters: {', '.join(focus_character_names)}."
    change_tail = ""
    if change_summary:
        change_tail = f" Requested change: {change_summary}."
    impact_tail = f" Change impact: {change_impact.value}."

    label = _read_character_sheet_label(character_sheet)
    return f'Refined from "{label}" with: {instructions}.{change_tail}{focus_tail}{impact_tail}'


def _build_pitch_refinement_summary_text(refined_pitch: Pitch, *, source_pitch: Pitch) -> str:
    return f"Generated refined pitch {refined_pitch.title} from {source_pitch.title}."


def _build_character_sheet_refinement_summary_text(
    refined_character_sheet: CharacterSheet,
    *,
    source_character_sheet: CharacterSheet,
) -> str:
    return (
        "Generated refined character sheet "
        f"{_read_character_sheet_label(refined_character_sheet)} from "
        f"{_read_character_sheet_label(source_character_sheet)}."
    )


def _build_pitch_selection_detail(pitch: Pitch) -> str:
    return f"Selected pitch: {pitch.title}. {pitch.logline}"


def _build_character_sheet_selection_detail(character_sheet: CharacterSheet) -> str:
    label = _read_character_sheet_label(character_sheet)
    change_summary = _read_character_sheet_change_summary(character_sheet)
    change_impact = _read_character_sheet_change_impact(character_sheet)
    refinement_tail = ""
    if change_summary is not None:
        impact_label = (
            f"{change_impact.value.capitalize()} refinement"
            if change_impact is not None
            else "Refinement"
        )
        refinement_tail = f" {impact_label}: {change_summary}."
    if character_sheet.protagonist_name:
        return (
            f"Selected character sheet: {label}. Lead character: "
            f"{character_sheet.protagonist_name}.{refinement_tail}"
        )

    return f"Selected character sheet: {label}.{refinement_tail}"


def _build_pitch_invalidation_detail(pitch: Pitch) -> str:
    return (
        f"Pitch selection changed to {pitch.title}. Refresh character work and any downstream "
        "planning."
    )


def _build_character_sheet_invalidation_detail(
    character_sheet: CharacterSheet,
    *,
    change_impact: CharacterChangeImpact = CharacterChangeImpact.MAJOR,
) -> str:
    label = _read_character_sheet_label(character_sheet)
    prefix = f"{change_impact.value.capitalize()} character change accepted in {label}."
    return prefix + " Refresh beats and any downstream planning."


def _find_matching_pitches(
    pitches: list[Pitch],
    *,
    pitch_id: str | None,
    generation_key: str | None,
    pitch_index: int | None,
    title: str | None,
) -> list[Pitch]:
    title_match = title.lower() if title is not None else None
    matches: list[Pitch] = []

    for pitch in pitches:
        if pitch_id is not None and pitch.id != pitch_id:
            continue
        if generation_key is not None and pitch.generation_key != generation_key:
            continue
        if pitch_index is not None and pitch.pitch_index != pitch_index:
            continue
        if title_match is not None and pitch.title.lower() != title_match:
            continue
        matches.append(pitch)

    return matches


def _find_matching_character_sheets(
    character_sheets: list[CharacterSheet],
    *,
    character_sheet_id: str | None,
    revision_number: int | None,
    title: str | None,
) -> list[CharacterSheet]:
    title_match = title.lower() if title is not None else None
    matches: list[CharacterSheet] = []

    for character_sheet in character_sheets:
        if character_sheet_id is not None and character_sheet.id != character_sheet_id:
            continue
        if revision_number is not None and character_sheet.revision_number != revision_number:
            continue
        if title_match is not None and (character_sheet.title or "").lower() != title_match:
            continue
        matches.append(character_sheet)

    return matches


def _resolve_source_character_sheet(
    character_sheets: list[CharacterSheet],
    *,
    selected_character_sheet: CharacterSheet | None,
    character_sheet_id: str | None,
    revision_number: int | None,
    title: str | None,
) -> CharacterSheet | None:
    if character_sheet_id is None and revision_number is None and title is None:
        return selected_character_sheet

    matches = _find_matching_character_sheets(
        character_sheets,
        character_sheet_id=character_sheet_id,
        revision_number=revision_number,
        title=title,
    )
    if len(matches) != 1:
        return None

    return matches[0]


def _build_pitch_persistence_metadata(
    result,
    *,
    generation_kind: str,
    guidance: str | None = None,
    source_pitch: Pitch | None = None,
    selection_rationale: str | None = None,
) -> dict[str, Any]:
    payload = build_pitch_model_output(result)
    payload["batch_metadata"] = {
        "generation_kind": generation_kind,
        "guidance": guidance,
    }
    if source_pitch is not None:
        payload["refinement"] = {
            "source_pitch_id": source_pitch.id,
            "source_pitch_title": source_pitch.title,
            "source_generation_key": source_pitch.generation_key,
            "refinement_instructions": guidance,
            "selection_rationale": selection_rationale,
        }
    return payload


def _build_character_persistence_metadata(
    result,
    *,
    generation_key: str,
    generation_kind: str,
    guidance: str | None = None,
    selected_pitch: Pitch,
    source_character_sheet: CharacterSheet | None = None,
    selection_rationale: str | None = None,
    change_summary: str | None = None,
    focus_character_names: list[str] | None = None,
    change_impact: CharacterChangeImpact | None = None,
) -> dict[str, Any]:
    payload = build_character_model_output(result)
    payload["batch_metadata"] = {
        "generation_key": generation_key,
        "generation_kind": generation_kind,
        "guidance": guidance,
    }
    payload["pitch_context"] = {
        "source_pitch_id": selected_pitch.id,
        "source_pitch_title": selected_pitch.title,
    }
    if source_character_sheet is not None:
        payload["refinement"] = {
            "source_pitch_id": selected_pitch.id,
            "source_pitch_title": selected_pitch.title,
            "source_character_sheet_id": source_character_sheet.id,
            "source_character_sheet_title": _read_character_sheet_label(source_character_sheet),
            "refinement_instructions": guidance,
            "selection_rationale": selection_rationale,
            "change_summary": change_summary,
            "focus_character_names": list(focus_character_names or []),
            "change_impact": change_impact.value if change_impact is not None else None,
        }
    return payload


def _read_character_sheet_selection_rationale(character_sheet: CharacterSheet) -> str | None:
    if not isinstance(character_sheet.character_data, Mapping):
        return None

    refinement = character_sheet.character_data.get("refinement")
    if not isinstance(refinement, Mapping):
        return None

    rationale = refinement.get("selection_rationale")
    return rationale if isinstance(rationale, str) and rationale else None


def _read_character_sheet_change_summary(character_sheet: CharacterSheet) -> str | None:
    if not isinstance(character_sheet.character_data, Mapping):
        return None

    refinement = character_sheet.character_data.get("refinement")
    if not isinstance(refinement, Mapping):
        return None

    summary = refinement.get("change_summary")
    return summary if isinstance(summary, str) and summary else None


def _read_character_sheet_change_impact(
    character_sheet: CharacterSheet,
) -> CharacterChangeImpact | None:
    if not isinstance(character_sheet.character_data, Mapping):
        return None

    refinement = character_sheet.character_data.get("refinement")
    if not isinstance(refinement, Mapping):
        return None

    change_impact = refinement.get("change_impact")
    if change_impact == CharacterChangeImpact.MINOR.value:
        return CharacterChangeImpact.MINOR
    if change_impact == CharacterChangeImpact.MAJOR.value:
        return CharacterChangeImpact.MAJOR
    return None


def _build_existing_character_sheet_context(
    character_sheet: CharacterSheet,
) -> ExistingCharacterSheetContext:
    protagonist_payload = None
    supporting_cast_payload = []
    if isinstance(character_sheet.character_data, Mapping):
        candidate_payload = character_sheet.character_data.get("candidate")
        if isinstance(candidate_payload, Mapping):
            protagonist_payload = candidate_payload.get("protagonist")
            supporting_cast_payload = candidate_payload.get("supporting_cast", [])

    return ExistingCharacterSheetContext(
        title=character_sheet.title,
        summary=character_sheet.summary,
        protagonist_name=character_sheet.protagonist_name,
        bedtime_safety_notes=character_sheet.bedtime_notes,
        protagonist=protagonist_payload,
        supporting_cast=(
            supporting_cast_payload if isinstance(supporting_cast_payload, list) else []
        ),
    )


def _next_character_sheet_revision_number(character_sheets: list[CharacterSheet]) -> int:
    if not character_sheets:
        return 1

    return max(character_sheet.revision_number for character_sheet in character_sheets) + 1


def _read_character_sheet_label(character_sheet: CharacterSheet) -> str:
    return (
        character_sheet.title
        or character_sheet.protagonist_name
        or f"Character sheet revision {character_sheet.revision_number}"
    )


def _build_beat_sheet_persistence_payload(
    result,
    *,
    generation_kind: str,
    guidance: str | None = None,
    focus_beats: list[str] | None = None,
    bedtime_goal: str | None = None,
    selected_pitch: Pitch,
    source_beat_sheet: BeatSheet | None = None,
    selection_rationale: str | None = None,
) -> dict[str, Any]:
    payload = build_beat_sheet_model_output(result)
    payload["generation_kind"] = generation_kind
    payload["guidance"] = guidance
    payload["focus_beats"] = list(focus_beats or [])
    payload["bedtime_goal"] = bedtime_goal
    payload["edit_history"] = []
    payload["beats"] = [
        {
            "key": beat.key,
            "label": beat.label,
            "order": index,
            "summary": beat.summary,
            "emotional_intent": beat.emotional_intent,
            "bedtime_softening_note": beat.bedtime_softening_note,
        }
        for index, beat in enumerate(result.beat_sheet.beats, start=1)
    ]
    payload["pitch_context"] = {
        "source_pitch_id": selected_pitch.id,
        "source_pitch_title": selected_pitch.title,
    }
    if source_beat_sheet is not None:
        payload["refinement"] = {
            "source_beat_sheet_id": source_beat_sheet.id,
            "source_beat_sheet_revision_number": source_beat_sheet.revision_number,
            "refinement_instructions": guidance,
            "selection_rationale": selection_rationale,
        }
    return payload


def _build_existing_beat_sheet_context(beat_sheet: BeatSheet) -> ExistingBeatSheetContext:
    return ExistingBeatSheetContext(
        revision_number=beat_sheet.revision_number,
        summary=beat_sheet.summary,
        bedtime_notes=beat_sheet.bedtime_notes,
        beats=_read_generated_beat_sheet_beats(beat_sheet),
    )


def _read_generated_beat_sheet_beats(beat_sheet: BeatSheet) -> list:
    if not isinstance(beat_sheet.beats, Mapping):
        return []

    raw_beats = beat_sheet.beats.get("beats")
    if not isinstance(raw_beats, list):
        return []

    generated_beats = []
    for raw_beat in raw_beats:
        if not isinstance(raw_beat, Mapping):
            continue
        generated_beats.append(
            {
                "key": raw_beat.get("key"),
                "label": raw_beat.get("label"),
                "summary": raw_beat.get("summary"),
                "emotional_intent": raw_beat.get("emotional_intent"),
                "bedtime_softening_note": raw_beat.get("bedtime_softening_note"),
            }
        )

    return generated_beats


def _read_beat_sheet_payload_mapping(beat_sheet: BeatSheet) -> dict[str, Any]:
    raw_payload = getattr(beat_sheet, "beats", None)
    return dict(raw_payload) if isinstance(raw_payload, Mapping) else {}


def _read_serialized_beat_sheet_beats(beat_sheet: BeatSheet) -> list[dict[str, Any]]:
    payload = _read_beat_sheet_payload_mapping(beat_sheet)
    raw_beats = payload.get("beats")
    if not isinstance(raw_beats, list):
        return [
            {
                "key": raw_beat.get("key"),
                "label": raw_beat.get("label"),
                "order": index,
                "summary": raw_beat.get("summary"),
                "emotional_intent": raw_beat.get("emotional_intent"),
                "bedtime_softening_note": raw_beat.get("bedtime_softening_note"),
            }
            for index, raw_beat in enumerate(_read_generated_beat_sheet_beats(beat_sheet), start=1)
            if isinstance(raw_beat, Mapping)
        ]

    serialized_beats: list[dict[str, Any]] = []
    for fallback_order, raw_beat in enumerate(raw_beats, start=1):
        if not isinstance(raw_beat, Mapping):
            continue
        key = raw_beat.get("key") if isinstance(raw_beat.get("key"), str) else None
        summary = raw_beat.get("summary") if isinstance(raw_beat.get("summary"), str) else None
        if key is None or summary is None:
            continue
        serialized_beats.append(
            {
                "key": key,
                "label": (
                    raw_beat.get("label")
                    if isinstance(raw_beat.get("label"), str)
                    else _humanize_beat_key(key)
                ),
                "order": raw_beat.get("order")
                if isinstance(raw_beat.get("order"), int)
                else fallback_order,
                "summary": summary,
                "emotional_intent": (
                    raw_beat.get("emotional_intent")
                    if isinstance(raw_beat.get("emotional_intent"), str)
                    else None
                ),
                "bedtime_softening_note": (
                    raw_beat.get("bedtime_softening_note")
                    if isinstance(raw_beat.get("bedtime_softening_note"), str)
                    else None
                ),
            }
        )

    return serialized_beats


def _normalize_beat_sheet_edit_updates(beat_updates: list[object] | None) -> list[dict[str, str]]:
    normalized_updates: list[dict[str, str]] = []

    for beat_update in beat_updates or []:
        key = _normalize_optional_text(getattr(beat_update, "key", None))
        if key is None:
            continue

        normalized_update: dict[str, str] = {"key": key}
        for field_name in ("summary", "emotional_intent", "bedtime_softening_note"):
            normalized_value = _normalize_optional_text(getattr(beat_update, field_name, None))
            if normalized_value is not None:
                normalized_update[field_name] = normalized_value

        if len(normalized_update) > 1:
            normalized_updates.append(normalized_update)

    return normalized_updates


def _apply_beat_sheet_edit_updates(
    serialized_beats: list[dict[str, Any]],
    normalized_updates: list[dict[str, str]],
) -> tuple[list[dict[str, Any]], list[str], list[str]]:
    if not normalized_updates:
        return serialized_beats, [], []

    updated_beats = [dict(beat) for beat in serialized_beats]
    beat_positions = {
        beat.get("key"): index
        for index, beat in enumerate(updated_beats)
        if isinstance(beat.get("key"), str)
    }
    changed_fields: list[str] = []
    changed_beat_keys: list[str] = []

    for normalized_update in normalized_updates:
        beat_key = normalized_update["key"]
        beat_position = beat_positions.get(beat_key)
        if beat_position is None:
            raise SessionBeatSheetEditError(f"beat {beat_key!r} does not exist on this revision")

        beat_entry = dict(updated_beats[beat_position])
        beat_changed = False
        for field_name in ("summary", "emotional_intent", "bedtime_softening_note"):
            if field_name not in normalized_update:
                continue
            next_value = normalized_update[field_name]
            if beat_entry.get(field_name) == next_value:
                continue
            beat_entry[field_name] = next_value
            changed_fields.append(f"beats.{beat_key}.{field_name}")
            beat_changed = True

        if beat_changed:
            updated_beats[beat_position] = beat_entry
            changed_beat_keys.append(beat_key)

    return updated_beats, changed_fields, changed_beat_keys


def _read_beat_sheet_edit_history_payload(payload: Mapping[str, Any]) -> list[dict[str, Any]]:
    raw_history = payload.get("edit_history")
    if not isinstance(raw_history, list):
        return []

    return [dict(entry) for entry in raw_history if isinstance(entry, Mapping)]


def _read_beat_sheet_refinement_payload(payload: Mapping[str, Any]) -> dict[str, Any]:
    raw_refinement = payload.get("refinement")
    if not isinstance(raw_refinement, Mapping):
        return {}

    return dict(raw_refinement)


def _build_beat_sheet_edit_history_entry(
    *,
    summary_text: str,
    origin: str,
    changed_fields: list[str],
    beat_keys: list[str],
    refreshes_downstream: bool,
    created_at,
) -> dict[str, Any]:
    return {
        "id": f"beat-edit-{uuid4().hex[:12]}",
        "summary_text": summary_text,
        "origin": origin,
        "changed_fields": list(changed_fields),
        "beat_keys": list(beat_keys),
        "material_change": True,
        "refreshes_downstream": refreshes_downstream,
        "created_at": created_at.isoformat(),
    }


def _next_beat_sheet_revision_number(beat_sheets: list[BeatSheet]) -> int:
    if not beat_sheets:
        return 1

    return max(beat_sheet.revision_number for beat_sheet in beat_sheets) + 1


def _build_beat_sheet_generation_stage_detail(
    beat_sheet,
) -> str:
    beat_count = len(getattr(beat_sheet, "beats", []))
    return (
        f"Generated beat-sheet revision with {beat_count} Save-the-Cat beats. "
        "Accept a revision to continue."
    )


def _build_beat_sheet_generation_summary_text(beat_sheet) -> str:
    summary = getattr(beat_sheet, "summary", None)
    if isinstance(summary, str) and summary:
        return f"Generated beat sheet: {summary}"
    return "Generated a fresh Save-the-Cat beat sheet."


def _build_beat_sheet_refinement_rationale(
    beat_sheet: BeatSheet,
    instructions: str,
    *,
    beat_names: list[str],
    bedtime_goal: str | None,
) -> str:
    focus_tail = f" Focus beats: {', '.join(beat_names)}." if beat_names else ""
    bedtime_tail = f" Bedtime goal: {bedtime_goal}." if bedtime_goal else ""
    return (
        f'Refined from "{_read_beat_sheet_label(beat_sheet)}" with: {instructions}.'
        f"{focus_tail}{bedtime_tail}"
    )


def _build_beat_sheet_refinement_summary_text(
    refined_beat_sheet: BeatSheet,
    *,
    source_beat_sheet: BeatSheet,
) -> str:
    return (
        "Generated refined beat sheet "
        f"{_read_beat_sheet_label(refined_beat_sheet)} from "
        f"{_read_beat_sheet_label(source_beat_sheet)}."
    )


def _build_beat_sheet_selection_detail(beat_sheet: BeatSheet) -> str:
    summary = beat_sheet.summary or "Beat sheet accepted for downstream planning."
    return f"Accepted beat sheet revision {beat_sheet.revision_number}. {summary}"


def _build_beat_sheet_edit_stage_detail(beat_sheet: BeatSheet) -> str:
    return (
        f"Edited beat sheet revision {beat_sheet.revision_number}. Accept a revision to continue."
    )


def _build_beat_sheet_edit_invalidation_detail(
    beat_sheet: BeatSheet,
    *,
    summary_text: str,
) -> str:
    return (
        f"Beat sheet revision {beat_sheet.revision_number} changed. "
        "Refresh story setup and composition prompts before continuing. "
        f"{summary_text}"
    )


def _build_beat_sheet_invalidation_detail(beat_sheet: BeatSheet) -> str:
    return (
        f"Beat sheet revision {beat_sheet.revision_number} was accepted. Refresh composition "
        "and any downstream planning."
    )


def _find_matching_beat_sheets(
    beat_sheets: list[BeatSheet],
    *,
    beat_sheet_id: str | None,
    revision_number: int | None,
) -> list[BeatSheet]:
    matches: list[BeatSheet] = []

    for beat_sheet in beat_sheets:
        if beat_sheet_id is not None and beat_sheet.id != beat_sheet_id:
            continue
        if revision_number is not None and beat_sheet.revision_number != revision_number:
            continue
        matches.append(beat_sheet)

    return matches


def _resolve_source_beat_sheet(
    beat_sheets: list[BeatSheet],
    *,
    selected_beat_sheet: BeatSheet | None,
    beat_sheet_id: str | None,
    revision_number: int | None,
) -> BeatSheet | None:
    if beat_sheet_id is None and revision_number is None:
        return selected_beat_sheet

    matches = _find_matching_beat_sheets(
        beat_sheets,
        beat_sheet_id=beat_sheet_id,
        revision_number=revision_number,
    )
    if len(matches) != 1:
        return None

    return matches[0]


def _read_beat_sheet_label(beat_sheet: BeatSheet) -> str:
    return f"Beat sheet revision {beat_sheet.revision_number}"


def _read_beat_sheet_selection_rationale(beat_sheet: BeatSheet) -> str | None:
    if not isinstance(beat_sheet.beats, Mapping):
        return None

    refinement = beat_sheet.beats.get("refinement")
    if not isinstance(refinement, Mapping):
        return None

    rationale = refinement.get("selection_rationale")
    return rationale if isinstance(rationale, str) and rationale else None


def _humanize_beat_key(value: str) -> str:
    return value.replace("_", " ").replace("-", " ").title()


def _format_humanized_list(values: list[str]) -> str:
    if not values:
        return ""
    if len(values) == 1:
        return values[0]
    if len(values) == 2:
        return f"{values[0]} and {values[1]}"
    return f"{', '.join(values[:-1])}, and {values[-1]}"


def _build_beat_sheet_edit_summary_text(
    beat_sheet: BeatSheet,
    *,
    beat_keys: list[str],
    changed_fields: list[str],
    refreshes_downstream: bool,
    requested_summary: str | None,
) -> str:
    if requested_summary is not None:
        return requested_summary

    targets: list[str] = []
    if beat_keys:
        targets.extend(_humanize_beat_key(beat_key) for beat_key in beat_keys)

    top_level_fields = {
        "summary": "arc summary",
        "bedtime_notes": "overall bedtime notes",
        "bedtime_goal": "bedtime goal",
    }
    for field_name, label in top_level_fields.items():
        if field_name in changed_fields:
            targets.append(label)

    target_summary = _format_humanized_list(targets) or "the beat sheet"
    message = f"Updated beat sheet revision {beat_sheet.revision_number}: {target_summary}."
    if refreshes_downstream:
        return message + " Story setup and composition need refresh."
    return message


def _normalize_beat_name_list(values: list[str] | None) -> list[str]:
    normalized: list[str] = []
    for value in values or []:
        normalized_value = _normalize_optional_text(value)
        if normalized_value is not None:
            normalized.append(normalized_value)
    return normalized


_STORY_BRIEF_TEXT_FIELDS = (
    "story_idea",
    "desired_themes",
    "key_images",
    "audience_notes",
    "must_have_elements",
    "planning_notes",
)


def _resolve_story_brief_revision(
    current_brief: StoryBrief | None,
    *,
    story_idea: str | None,
    desired_themes: str | None,
    key_images: str | None,
    audience_notes: str | None,
    must_have_elements: str | None,
    raw_brief: str | None,
    planning_notes: str | None,
    edit_mode: StoryBriefEditMode,
) -> dict[str, str | None]:
    incoming_story_idea = _normalize_optional_text(story_idea)
    if incoming_story_idea is None:
        incoming_story_idea = _normalize_optional_text(raw_brief)

    current_values = {
        "story_idea": _normalize_optional_text(current_brief.story_idea)
        if current_brief is not None
        else None,
        "desired_themes": _normalize_optional_text(current_brief.desired_themes)
        if current_brief is not None
        else None,
        "key_images": _normalize_optional_text(current_brief.key_images)
        if current_brief is not None
        else None,
        "audience_notes": _normalize_optional_text(current_brief.audience_notes)
        if current_brief is not None
        else None,
        "must_have_elements": _normalize_optional_text(current_brief.must_have_elements)
        if current_brief is not None
        else None,
        "planning_notes": _normalize_optional_text(current_brief.planning_notes)
        if current_brief is not None
        else None,
        "raw_brief": _normalize_optional_text(current_brief.raw_brief)
        if current_brief is not None
        else None,
    }
    incoming_values = {
        "story_idea": incoming_story_idea,
        "desired_themes": _normalize_optional_text(desired_themes),
        "key_images": _normalize_optional_text(key_images),
        "audience_notes": _normalize_optional_text(audience_notes),
        "must_have_elements": _normalize_optional_text(must_have_elements),
        "planning_notes": _normalize_optional_text(planning_notes),
    }

    resolved_values = {
        field_name: _resolve_story_brief_value(
            current_values[field_name],
            incoming_values[field_name],
            edit_mode=edit_mode,
        )
        for field_name in _STORY_BRIEF_TEXT_FIELDS
    }
    composed_raw_brief = _compose_story_brief_text(
        story_idea=resolved_values["story_idea"],
        desired_themes=resolved_values["desired_themes"],
        key_images=resolved_values["key_images"],
        audience_notes=resolved_values["audience_notes"],
        must_have_elements=resolved_values["must_have_elements"],
    )

    if composed_raw_brief is None:
        composed_raw_brief = _resolve_story_brief_value(
            current_values["raw_brief"],
            _normalize_optional_text(raw_brief),
            edit_mode=edit_mode,
        )

    if composed_raw_brief is None:
        raise SessionStoryBriefSaveError(
            "story brief content requires a story idea or free-form brief before it can be saved"
        )

    resolved_values["raw_brief"] = composed_raw_brief
    return resolved_values


def _resolve_story_brief_value(
    current_value: str | None,
    incoming_value: str | None,
    *,
    edit_mode: StoryBriefEditMode,
) -> str | None:
    if edit_mode == StoryBriefEditMode.REPLACE:
        return incoming_value

    if edit_mode == StoryBriefEditMode.APPEND:
        if incoming_value is None:
            return current_value
        if current_value is None:
            return incoming_value
        if incoming_value in current_value:
            return current_value
        return f"{current_value.rstrip()}\n\n{incoming_value.lstrip()}"

    return incoming_value if incoming_value is not None else current_value


def _compose_story_brief_text(
    *,
    story_idea: str | None,
    desired_themes: str | None,
    key_images: str | None,
    audience_notes: str | None,
    must_have_elements: str | None,
) -> str | None:
    sections: list[str] = []

    if story_idea is not None:
        sections.append(story_idea)

    for label, value in (
        ("Desired themes", desired_themes),
        ("Key images", key_images),
        ("Target audience notes", audience_notes),
        ("Must-have elements", must_have_elements),
    ):
        if value is not None:
            sections.append(f"{label}: {value}")

    if not sections:
        return None

    return "\n\n".join(sections)


def _build_story_brief_stage_detail(value: str) -> str:
    return f"Saved story brief: {_truncate_story_brief_text(value, limit=160)}"


def _build_story_brief_invalidation_detail() -> str:
    return "Story brief changed. Refresh pitches and any downstream planning."


def _build_story_brief_changed_fields(
    previous_brief: StoryBrief | None,
    new_brief: StoryBrief,
) -> list[str]:
    if previous_brief is None:
        return [
            field_name
            for field_name in (
                "story_idea",
                "desired_themes",
                "key_images",
                "audience_notes",
                "must_have_elements",
                "raw_brief",
                "normalized_summary",
                "normalized_preferences",
                "planning_notes",
            )
            if getattr(new_brief, field_name) is not None
        ]

    changed_fields: list[str] = []
    for field_name in (
        "story_idea",
        "desired_themes",
        "key_images",
        "audience_notes",
        "must_have_elements",
        "raw_brief",
        "normalized_summary",
        "normalized_preferences",
        "planning_notes",
    ):
        if getattr(previous_brief, field_name) != getattr(new_brief, field_name):
            changed_fields.append(field_name)

    return changed_fields or ["raw_brief"]


def _build_story_brief_event_values(
    story_brief: StoryBrief,
    *,
    edit_mode: StoryBriefEditMode,
) -> dict[str, Any]:
    return {
        "story_idea": story_brief.story_idea,
        "desired_themes": story_brief.desired_themes,
        "key_images": story_brief.key_images,
        "audience_notes": story_brief.audience_notes,
        "must_have_elements": story_brief.must_have_elements,
        "raw_brief": story_brief.raw_brief,
        "normalized_summary": story_brief.normalized_summary,
        "normalized_preferences": story_brief.normalized_preferences,
        "planning_notes": story_brief.planning_notes,
        "edit_mode": edit_mode.value,
        "revision_number": story_brief.revision_number,
    }


def _build_story_brief_summary_text(*, has_existing_brief: bool, origin: str) -> str:
    action = "Updated" if has_existing_brief else "Saved"
    return f"{action} story brief from {origin}."


def _truncate_story_brief_text(value: str, *, limit: int) -> str:
    if len(value) <= limit:
        return value

    return f"{value[: limit - 3].rstrip()}..."


def _elapsed_ms_since(started_at: float) -> int:
    return max(round((perf_counter() - started_at) * 1000), 0)


def _record_session_model_usage(
    *,
    session: Session,
    session_id: str,
    usage_bucket: str,
    workflow_stage: WorkflowStage | None,
    purpose: str,
    source: str,
    model_id: str | None,
    prompt_version: str | None,
    raw_response: Any,
    elapsed_ms: int,
) -> None:
    if model_id is None:
        return

    SessionModelUsageService(session).record_model_call(
        context=ModelUsageContext(
            session_id=session_id,
            usage_bucket=ModelUsageBucket(usage_bucket),
            workflow_stage=workflow_stage,
            purpose=purpose,
            model_id=model_id,
            prompt_version=prompt_version,
        ),
        elapsed_ms=elapsed_ms,
        outcome=_resolve_model_usage_outcome(source=source, raw_response=raw_response),
        raw_response=raw_response,
        error_message=_extract_model_usage_error_message(raw_response),
    )


def _resolve_model_usage_outcome(
    *,
    source: str,
    raw_response: Any,
) -> ModelCallOutcome:
    if source != "heuristic":
        return ModelCallOutcome.SUCCEEDED

    if isinstance(raw_response, Mapping) and isinstance(
        raw_response.get("adapter_raw_response"),
        Mapping,
    ):
        return ModelCallOutcome.SUCCEEDED_WITH_FALLBACK

    return ModelCallOutcome.FAILED


def _extract_model_usage_error_message(raw_response: Any) -> str | None:
    if not isinstance(raw_response, Mapping):
        return None

    fallback_reason = raw_response.get("fallback_reason")
    if fallback_reason is None:
        return None

    normalized = str(fallback_reason).strip()
    return normalized or None

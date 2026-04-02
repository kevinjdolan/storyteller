from __future__ import annotations

from collections.abc import Mapping
from typing import Any
from uuid import uuid4

from sqlalchemy.orm import Session

from app.db import Pitch, StoryBrief
from app.db.base import utc_now
from app.models import (
    WORKFLOW_STAGE_SEQUENCE,
    AIOutputKind,
    ExistingSelectedPitchContext,
    NormalizedBriefPreferences,
    RecentSessionSummary,
    SelectionKind,
    SessionContextUpdateRequest,
    SessionContextUpdateResponse,
    SessionEventActor,
    SessionEventView,
    SessionHistoryView,
    SessionPitchGenerationResponse,
    SessionSelectionResponse,
    SessionSnapshot,
    SessionStoryBriefResponse,
    StoryBriefEditMode,
    UserEditTargetKind,
    WorkflowStage,
    WorkflowStageState,
    get_invalidated_stages_after_edit,
    get_workflow_stage_definition,
    resolve_resume_stage,
)
from app.repositories import StorySessionRepository, WorkflowStageStateRepository
from app.services.brief_normalization import (
    BriefNormalizationService,
    apply_brief_normalization_overrides,
    build_brief_model_output,
    build_brief_normalization_result_from_existing,
)
from app.services.catalog import find_active_genre, find_active_tone_for_genre
from app.services.event_log import SessionEventLogService
from app.services.pitch_generation import PitchGenerationService, build_pitch_model_output
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


class SessionPitchGenerationError(SessionServiceError):
    """Raised when a pitch generation request cannot be fulfilled."""


class SessionPitchSelectionError(SessionServiceError):
    """Raised when a pitch selection request cannot be fulfilled."""


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

    def list_recent_sessions(self, *, limit: int = 20) -> list[RecentSessionSummary]:
        if limit <= 0:
            raise ValueError("limit must be greater than zero")

        sessions = self._sessions.list_recent(limit=limit)
        return [build_recent_session_summary(story_session) for story_session in sessions]

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
        stage_snapshot.last_event = edit_event
        self._session.commit()
        return SessionStoryBriefResponse(
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
        stage_snapshot.last_event = selection_event
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


def _build_pitch_generation_stage_detail(candidate_count: int) -> str:
    return f"Generated {candidate_count} pitch options. Select one to continue."


def _build_pitch_generation_summary_text(pitches: list[object]) -> str:
    titles = [getattr(pitch, "title", None) for pitch in pitches]
    summarized_titles = [title for title in titles if isinstance(title, str) and title]
    if not summarized_titles:
        return "Generated a fresh pitch batch."

    return "Generated pitches: " + ", ".join(summarized_titles[:3]) + "."


def _build_pitch_refinement_rationale(pitch: Pitch, instructions: str) -> str:
    return f'Refined from "{pitch.title}" with: {instructions}'


def _build_pitch_refinement_summary_text(refined_pitch: Pitch, *, source_pitch: Pitch) -> str:
    return f"Generated refined pitch {refined_pitch.title} from {source_pitch.title}."


def _build_pitch_selection_detail(pitch: Pitch) -> str:
    return f"Selected pitch: {pitch.title}. {pitch.logline}"


def _build_pitch_invalidation_detail(pitch: Pitch) -> str:
    return (
        f"Pitch selection changed to {pitch.title}. Refresh character work and any downstream "
        "planning."
    )


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

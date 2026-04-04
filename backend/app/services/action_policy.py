from __future__ import annotations

from dataclasses import dataclass, field

from sqlalchemy import Select, func, select
from sqlalchemy.orm import Session

from app.db import (
    AssetKind,
    AssetStatus,
    BeatSheet,
    CharacterSheet,
    Genre,
    JobStatus,
    Pitch,
    SessionAsset,
    ToneProfile,
)
from app.models.action_policy import (
    SessionActionDecision,
    SessionActionPolicyEvaluation,
    SessionActionPolicyEvaluationItem,
    SessionActionPolicyEvaluationRequest,
    SessionActionPolicyReason,
    SessionActionPolicySideEffect,
    SessionActionReasonCode,
    SessionActionSideEffectKind,
    build_action_policy_request_from_batch,
)
from app.models.chat_actions import (
    AcceptBeatSheetAction,
    ChatToUIAction,
    ChatToUIActionBatch,
    ChatToUIActionDefaultPolicy,
    ChatToUIActionType,
    ChatToUIJobKind,
    DownloadAssetAction,
    DownloadAssetKind,
    OpenFinalizeViewAction,
    PauseJobAction,
    RedirectCompositionAction,
    RefineCharacterSheetAction,
    RefinePitchAction,
    RegenerateBeatSheetAction,
    RegenerateCharacterSheetAction,
    RegeneratePitchesAction,
    ResumeJobAction,
    SelectCharacterSheetAction,
    SelectGenreAction,
    SelectPitchAction,
    SelectToneAction,
    StartAudioGenerationAction,
    StartCompositionAction,
    UpdateAudioSettingsAction,
    UpdateStoryBriefAction,
    UpdateStorySetupAction,
    get_chat_to_ui_action_default_policy,
)
from app.models.session import SessionSnapshot
from app.models.workflow import (
    WORKFLOW_STAGE_SEQUENCE,
    WorkflowStage,
    WorkflowStageState,
    get_invalidated_stages_after_edit,
)
from app.services.character_sheet_changes import infer_character_change_impact
from app.services.sessions import SessionService

ACTIVE_JOB_STATUSES = {
    JobStatus.QUEUED,
    JobStatus.IN_PROGRESS,
    JobStatus.PAUSED,
}
PAUSABLE_JOB_STATUSES = {
    JobStatus.QUEUED,
    JobStatus.IN_PROGRESS,
}


class SessionActionPolicyServiceError(Exception):
    """Base error for action policy failures."""


@dataclass
class _ResolvedAction:
    genre: Genre | None = None
    tone: ToneProfile | None = None
    pitch: Pitch | None = None
    character_sheet: CharacterSheet | None = None
    beat_sheet: BeatSheet | None = None


@dataclass
class _ComputedDecision:
    decision: SessionActionDecision
    reasons: list[SessionActionPolicyReason] = field(default_factory=list)
    side_effects: list[SessionActionPolicySideEffect] = field(default_factory=list)
    prerequisite_action_types: list[ChatToUIActionType] = field(default_factory=list)
    resolution: _ResolvedAction = field(default_factory=_ResolvedAction)


@dataclass
class _PolicyState:
    stage_statuses: dict[WorkflowStage, WorkflowStageState]
    selected_genre_id: str | None
    selected_tone_profile_id: str | None
    story_brief_present: bool
    selected_pitch_id: str | None
    selected_character_sheet_id: str | None
    selected_beat_sheet_id: str | None
    selected_story_setup_id: str | None
    active_composition_job_id: str | None
    active_composition_job_status: JobStatus | None
    active_composition_interruption_requested: bool
    active_audio_job_id: str | None
    active_audio_job_status: JobStatus | None
    ready_story_asset_kinds: set[AssetKind]
    ready_audio_asset_kinds: set[AssetKind]

    @classmethod
    def from_snapshot(
        cls,
        snapshot: SessionSnapshot,
        *,
        ready_story_asset_kinds: set[AssetKind],
        ready_audio_asset_kinds: set[AssetKind],
    ) -> _PolicyState:
        return cls(
            stage_statuses={item.stage: item.status for item in snapshot.stage_states},
            selected_genre_id=snapshot.selected_genre.id if snapshot.selected_genre else None,
            selected_tone_profile_id=(
                snapshot.selected_tone_profile.id if snapshot.selected_tone_profile else None
            ),
            story_brief_present=snapshot.story_brief is not None,
            selected_pitch_id=snapshot.selected_pitch.id if snapshot.selected_pitch else None,
            selected_character_sheet_id=(
                snapshot.selected_character_sheet.id if snapshot.selected_character_sheet else None
            ),
            selected_beat_sheet_id=(
                snapshot.selected_beat_sheet.id if snapshot.selected_beat_sheet else None
            ),
            selected_story_setup_id=(
                snapshot.selected_story_setup.id if snapshot.selected_story_setup else None
            ),
            active_composition_job_id=(
                snapshot.active_composition_job.id if snapshot.active_composition_job else None
            ),
            active_composition_job_status=(
                JobStatus(snapshot.active_composition_job.status)
                if snapshot.active_composition_job is not None
                else None
            ),
            active_composition_interruption_requested=(
                snapshot.active_composition_job is not None
                and snapshot.active_composition_job.interruption_request is not None
            ),
            active_audio_job_id=snapshot.active_audio_job.id if snapshot.active_audio_job else None,
            active_audio_job_status=(
                JobStatus(snapshot.active_audio_job.status)
                if snapshot.active_audio_job is not None
                else None
            ),
            ready_story_asset_kinds=ready_story_asset_kinds,
            ready_audio_asset_kinds=ready_audio_asset_kinds,
        )


class SessionActionPolicyService:
    def __init__(self, session: Session):
        self._session = session
        self._sessions = SessionService(session)

    def evaluate_request(
        self,
        session_id: str,
        *,
        request: SessionActionPolicyEvaluationRequest,
    ) -> SessionActionPolicyEvaluation:
        snapshot = self._sessions.load_session_snapshot(session_id)
        return self.evaluate_request_against_snapshot(snapshot, request=request)

    def evaluate_request_against_snapshot(
        self,
        snapshot: SessionSnapshot,
        *,
        request: SessionActionPolicyEvaluationRequest,
    ) -> SessionActionPolicyEvaluation:
        state = _PolicyState.from_snapshot(
            snapshot,
            ready_story_asset_kinds=self._load_ready_story_asset_kinds(snapshot.id),
            ready_audio_asset_kinds=self._load_ready_audio_asset_kinds(snapshot.id),
        )
        evaluated_actions: list[SessionActionPolicyEvaluationItem] = []

        for action_index, request_item in enumerate(request.actions):
            computed = self._evaluate_action(
                snapshot.id,
                state,
                request_item.action,
                confirmation_granted=request_item.confirmation_granted,
            )
            evaluation_item = SessionActionPolicyEvaluationItem(
                action_index=action_index,
                action_type=request_item.action.action_type,
                target_stage=request_item.action.target_stage,
                decision=computed.decision,
                summary=_build_decision_summary(
                    request_item.action,
                    decision=computed.decision,
                    reasons=computed.reasons,
                    side_effects=computed.side_effects,
                ),
                reasons=computed.reasons,
                side_effects=computed.side_effects,
                prerequisite_action_types=computed.prerequisite_action_types,
            )
            evaluated_actions.append(evaluation_item)

            if computed.decision in {
                SessionActionDecision.ACCEPTED,
                SessionActionDecision.ACCEPTED_WITH_SIDE_EFFECTS,
            }:
                self._apply_action_to_state(state, request_item.action, computed.resolution)

        return SessionActionPolicyEvaluation(
            session_id=snapshot.id,
            evaluated_actions=evaluated_actions,
        )

    def evaluate_proposed_actions(
        self,
        session_id: str,
        *,
        batch: ChatToUIActionBatch,
    ) -> SessionActionPolicyEvaluation:
        return self.evaluate_request(
            session_id,
            request=build_action_policy_request_from_batch(batch),
        )

    def _evaluate_action(
        self,
        session_id: str,
        state: _PolicyState,
        action: ChatToUIAction,
        *,
        confirmation_granted: bool,
    ) -> _ComputedDecision:
        if action.action_type == ChatToUIActionType.NAVIGATE_TO_STAGE:
            return _accept()

        if action.action_type == ChatToUIActionType.SELECT_GENRE:
            return self._evaluate_select_genre(
                action,
                state,
                confirmation_granted=confirmation_granted,
            )
        if action.action_type == ChatToUIActionType.SELECT_TONE:
            return self._evaluate_select_tone(
                action,
                state,
                confirmation_granted=confirmation_granted,
            )
        if action.action_type == ChatToUIActionType.UPDATE_STORY_BRIEF:
            return self._evaluate_update_story_brief(
                action,
                state,
                confirmation_granted=confirmation_granted,
            )
        if action.action_type == ChatToUIActionType.REGENERATE_PITCHES:
            return self._evaluate_regenerate_pitches(
                action,
                state,
                confirmation_granted=confirmation_granted,
            )
        if action.action_type == ChatToUIActionType.REFINE_PITCH:
            return self._evaluate_refine_pitch(
                session_id,
                action,
                state,
                confirmation_granted=confirmation_granted,
            )
        if action.action_type == ChatToUIActionType.SELECT_PITCH:
            return self._evaluate_select_pitch(
                session_id,
                action,
                state,
                confirmation_granted=confirmation_granted,
            )
        if action.action_type == ChatToUIActionType.SELECT_CHARACTER_SHEET:
            return self._evaluate_select_character_sheet(
                session_id,
                action,
                state,
                confirmation_granted=confirmation_granted,
            )
        if action.action_type == ChatToUIActionType.REFINE_CHARACTER_SHEET:
            return self._evaluate_refine_character_sheet(
                session_id,
                action,
                state,
                confirmation_granted=confirmation_granted,
            )
        if action.action_type == ChatToUIActionType.REGENERATE_CHARACTER_SHEET:
            return self._evaluate_regenerate_character_sheet(
                action,
                state,
                confirmation_granted=confirmation_granted,
            )
        if action.action_type == ChatToUIActionType.ACCEPT_BEAT_SHEET:
            return self._evaluate_accept_beat_sheet(
                session_id,
                action,
                state,
                confirmation_granted=confirmation_granted,
            )
        if action.action_type == ChatToUIActionType.REFINE_BEAT_SHEET:
            return self._evaluate_refine_beat_sheet(
                action,
                state,
                confirmation_granted=confirmation_granted,
            )
        if action.action_type == ChatToUIActionType.REGENERATE_BEAT_SHEET:
            return self._evaluate_regenerate_beat_sheet(
                action,
                state,
                confirmation_granted=confirmation_granted,
            )
        if action.action_type == ChatToUIActionType.UPDATE_STORY_SETUP:
            return self._evaluate_update_story_setup(
                action,
                state,
                confirmation_granted=confirmation_granted,
            )
        if action.action_type == ChatToUIActionType.START_COMPOSITION:
            return self._evaluate_start_composition(
                action,
                state,
                confirmation_granted=confirmation_granted,
            )
        if action.action_type == ChatToUIActionType.PAUSE_JOB:
            return self._evaluate_pause_job(
                action,
                state,
                confirmation_granted=confirmation_granted,
            )
        if action.action_type == ChatToUIActionType.RESUME_JOB:
            return self._evaluate_resume_job(
                action,
                state,
                confirmation_granted=confirmation_granted,
            )
        if action.action_type == ChatToUIActionType.REDIRECT_COMPOSITION:
            return self._evaluate_redirect_composition(
                action,
                state,
                confirmation_granted=confirmation_granted,
            )
        if action.action_type == ChatToUIActionType.UPDATE_AUDIO_SETTINGS:
            return self._evaluate_update_audio_settings(
                action,
                state,
                confirmation_granted=confirmation_granted,
            )
        if action.action_type == ChatToUIActionType.START_AUDIO_GENERATION:
            return self._evaluate_start_audio_generation(
                action,
                state,
                confirmation_granted=confirmation_granted,
            )
        if action.action_type == ChatToUIActionType.OPEN_FINALIZE_VIEW:
            return self._evaluate_open_finalize_view(action, state)
        if action.action_type == ChatToUIActionType.DOWNLOAD_ASSET:
            return self._evaluate_download_asset(action, state)

        raise SessionActionPolicyServiceError(f"unsupported action type {action.action_type!r}")

    def _evaluate_select_genre(
        self,
        action: SelectGenreAction,
        state: _PolicyState,
        *,
        confirmation_granted: bool,
    ) -> _ComputedDecision:
        genre_matches = self._find_genres(action)
        if len(genre_matches) > 1:
            return _reject(
                SessionActionReasonCode.CATALOG_ENTRY_AMBIGUOUS,
                "More than one active genre matched that request.",
                stage=WorkflowStage.GENRE,
            )
        if not genre_matches:
            return _reject(
                SessionActionReasonCode.CATALOG_ENTRY_NOT_FOUND,
                "No active genre matched that request.",
                stage=WorkflowStage.GENRE,
            )

        genre = genre_matches[0]
        if (
            state.selected_genre_id == genre.id
            and state.stage_statuses.get(WorkflowStage.GENRE)
            != WorkflowStageState.NEEDS_REGENERATION
        ):
            return _accept(
                reasons=[
                    _reason(
                        SessionActionReasonCode.ACTION_IS_NOOP,
                        f"{genre.label} is already the selected genre.",
                        stage=WorkflowStage.GENRE,
                    )
                ],
                resolution=_ResolvedAction(genre=genre),
            )

        side_effects = self._build_stage_edit_side_effects(
            state,
            WorkflowStage.GENRE,
            clear_tone_selection=(
                state.selected_tone_profile_id is not None and state.selected_genre_id != genre.id
            ),
        )
        return self._finalize_change_action(
            action,
            side_effects=side_effects,
            confirmation_granted=confirmation_granted,
            resolution=_ResolvedAction(genre=genre),
        )

    def _evaluate_select_tone(
        self,
        action: SelectToneAction,
        state: _PolicyState,
        *,
        confirmation_granted: bool,
    ) -> _ComputedDecision:
        if state.selected_genre_id is None:
            return _reject(
                SessionActionReasonCode.PREREQUISITE_SELECTION_MISSING,
                "Select a genre before choosing a tone.",
                stage=WorkflowStage.TONE,
                prerequisite_action_types=[ChatToUIActionType.SELECT_GENRE],
            )

        tone_matches = self._find_tones(action, genre_id=state.selected_genre_id)
        if len(tone_matches) > 1:
            return _reject(
                SessionActionReasonCode.CATALOG_ENTRY_AMBIGUOUS,
                "More than one tone profile matched that request for the current genre.",
                stage=WorkflowStage.TONE,
            )
        if not tone_matches:
            return _reject(
                SessionActionReasonCode.CATALOG_ENTRY_NOT_FOUND,
                "No active tone profile matched that request for the current genre.",
                stage=WorkflowStage.TONE,
            )

        tone = tone_matches[0]
        if (
            state.selected_tone_profile_id == tone.id
            and state.stage_statuses.get(WorkflowStage.TONE)
            != WorkflowStageState.NEEDS_REGENERATION
        ):
            return _accept(
                reasons=[
                    _reason(
                        SessionActionReasonCode.ACTION_IS_NOOP,
                        f"{tone.label} is already the selected tone.",
                        stage=WorkflowStage.TONE,
                    )
                ],
                resolution=_ResolvedAction(tone=tone),
            )

        blocked = _blocked_prerequisite_stages(state, WorkflowStage.TONE)
        if blocked:
            return _reject_for_blocked_stages(blocked, target_stage=WorkflowStage.TONE)

        side_effects = self._build_stage_edit_side_effects(state, WorkflowStage.TONE)
        return self._finalize_change_action(
            action,
            side_effects=side_effects,
            confirmation_granted=confirmation_granted,
            resolution=_ResolvedAction(tone=tone),
        )

    def _evaluate_update_story_brief(
        self,
        action: UpdateStoryBriefAction,
        state: _PolicyState,
        *,
        confirmation_granted: bool,
    ) -> _ComputedDecision:
        blocked = _blocked_prerequisite_stages(state, WorkflowStage.BRIEF)
        if blocked:
            return _reject_for_blocked_stages(blocked, target_stage=WorkflowStage.BRIEF)

        side_effects = self._build_stage_edit_side_effects(state, WorkflowStage.BRIEF)
        return self._finalize_change_action(
            action,
            side_effects=side_effects,
            confirmation_granted=confirmation_granted,
        )

    def _evaluate_regenerate_pitches(
        self,
        action: RegeneratePitchesAction,
        state: _PolicyState,
        *,
        confirmation_granted: bool,
    ) -> _ComputedDecision:
        blocked = _blocked_prerequisite_stages(state, WorkflowStage.PITCHES)
        if blocked:
            return _reject_for_blocked_stages(blocked, target_stage=WorkflowStage.PITCHES)
        if not state.story_brief_present:
            return _reject(
                SessionActionReasonCode.PREREQUISITE_SELECTION_MISSING,
                "Create or accept a story brief before regenerating pitches.",
                stage=WorkflowStage.PITCHES,
                prerequisite_action_types=[ChatToUIActionType.UPDATE_STORY_BRIEF],
            )

        side_effects = self._build_stage_edit_side_effects(state, WorkflowStage.PITCHES)
        return self._finalize_change_action(
            action,
            side_effects=side_effects,
            confirmation_granted=confirmation_granted,
        )

    def _evaluate_select_pitch(
        self,
        session_id: str,
        action: SelectPitchAction,
        state: _PolicyState,
        *,
        confirmation_granted: bool,
    ) -> _ComputedDecision:
        blocked = _blocked_prerequisite_stages(state, WorkflowStage.PITCHES)
        if blocked:
            return _reject_for_blocked_stages(blocked, target_stage=WorkflowStage.PITCHES)
        if not state.story_brief_present:
            return _reject(
                SessionActionReasonCode.PREREQUISITE_SELECTION_MISSING,
                "Create or accept a story brief before selecting a pitch.",
                stage=WorkflowStage.PITCHES,
                prerequisite_action_types=[ChatToUIActionType.UPDATE_STORY_BRIEF],
            )
        if state.stage_statuses.get(WorkflowStage.PITCHES) == WorkflowStageState.NEEDS_REGENERATION:
            return _reject(
                SessionActionReasonCode.TARGET_STAGE_STALE,
                (
                    "Generate fresh pitches before selecting one because the current "
                    "pitch set is stale."
                ),
                stage=WorkflowStage.PITCHES,
                prerequisite_action_types=[ChatToUIActionType.REGENERATE_PITCHES],
            )

        pitches = self._find_pitches(session_id, action)
        if len(pitches) > 1:
            return _reject(
                SessionActionReasonCode.SESSION_RESOURCE_AMBIGUOUS,
                "More than one pitch matched that request in this session.",
                stage=WorkflowStage.PITCHES,
            )
        if not pitches:
            return _reject(
                SessionActionReasonCode.SESSION_RESOURCE_NOT_FOUND,
                "No pitch matched that request in this session.",
                stage=WorkflowStage.PITCHES,
            )

        pitch = pitches[0]
        if state.selected_pitch_id == pitch.id:
            return _accept(
                reasons=[
                    _reason(
                        SessionActionReasonCode.ACTION_IS_NOOP,
                        f"{pitch.title} is already the selected pitch.",
                        stage=WorkflowStage.PITCHES,
                    )
                ],
                resolution=_ResolvedAction(pitch=pitch),
            )

        side_effects = self._build_stage_edit_side_effects(state, WorkflowStage.PITCHES)
        return self._finalize_change_action(
            action,
            side_effects=side_effects,
            confirmation_granted=confirmation_granted,
            resolution=_ResolvedAction(pitch=pitch),
        )

    def _evaluate_refine_pitch(
        self,
        session_id: str,
        action: RefinePitchAction,
        state: _PolicyState,
        *,
        confirmation_granted: bool,
    ) -> _ComputedDecision:
        blocked = _blocked_prerequisite_stages(state, WorkflowStage.PITCHES)
        if blocked:
            return _reject_for_blocked_stages(blocked, target_stage=WorkflowStage.PITCHES)
        if not state.story_brief_present:
            return _reject(
                SessionActionReasonCode.PREREQUISITE_SELECTION_MISSING,
                "Create or accept a story brief before refining a pitch.",
                stage=WorkflowStage.PITCHES,
                prerequisite_action_types=[ChatToUIActionType.UPDATE_STORY_BRIEF],
            )
        if state.stage_statuses.get(WorkflowStage.PITCHES) == WorkflowStageState.NEEDS_REGENERATION:
            return _reject(
                SessionActionReasonCode.TARGET_STAGE_STALE,
                (
                    "Generate fresh pitches before refining one because the current "
                    "pitch set is stale."
                ),
                stage=WorkflowStage.PITCHES,
                prerequisite_action_types=[ChatToUIActionType.REGENERATE_PITCHES],
            )

        pitches = self._find_pitches(session_id, action)
        if len(pitches) > 1:
            return _reject(
                SessionActionReasonCode.SESSION_RESOURCE_AMBIGUOUS,
                "More than one pitch matched that refinement request in this session.",
                stage=WorkflowStage.PITCHES,
            )
        if not pitches:
            return _reject(
                SessionActionReasonCode.SESSION_RESOURCE_NOT_FOUND,
                "No pitch matched that refinement request in this session.",
                stage=WorkflowStage.PITCHES,
            )

        pitch = pitches[0]
        side_effects = self._build_stage_edit_side_effects(state, WorkflowStage.PITCHES)
        return self._finalize_change_action(
            action,
            side_effects=side_effects,
            confirmation_granted=confirmation_granted,
            resolution=_ResolvedAction(pitch=pitch),
        )

    def _evaluate_select_character_sheet(
        self,
        session_id: str,
        action: SelectCharacterSheetAction,
        state: _PolicyState,
        *,
        confirmation_granted: bool,
    ) -> _ComputedDecision:
        blocked = _blocked_prerequisite_stages(state, WorkflowStage.CHARACTERS)
        if blocked:
            return _reject_for_blocked_stages(blocked, target_stage=WorkflowStage.CHARACTERS)
        if state.selected_pitch_id is None:
            return _reject(
                SessionActionReasonCode.PREREQUISITE_SELECTION_MISSING,
                "Select a pitch before choosing a character sheet.",
                stage=WorkflowStage.CHARACTERS,
                prerequisite_action_types=[ChatToUIActionType.SELECT_PITCH],
            )
        if (
            state.stage_statuses.get(WorkflowStage.CHARACTERS)
            == WorkflowStageState.NEEDS_REGENERATION
        ):
            return _reject(
                SessionActionReasonCode.TARGET_STAGE_STALE,
                (
                    "Generate fresh character sheets before selecting one because the "
                    "current set is stale."
                ),
                stage=WorkflowStage.CHARACTERS,
                prerequisite_action_types=[ChatToUIActionType.REGENERATE_CHARACTER_SHEET],
            )

        character_sheets = self._find_character_sheets(session_id, action)
        if len(character_sheets) > 1:
            return _reject(
                SessionActionReasonCode.SESSION_RESOURCE_AMBIGUOUS,
                "More than one character sheet matched that request in this session.",
                stage=WorkflowStage.CHARACTERS,
            )
        if not character_sheets:
            return _reject(
                SessionActionReasonCode.SESSION_RESOURCE_NOT_FOUND,
                "No character sheet matched that request in this session.",
                stage=WorkflowStage.CHARACTERS,
            )

        character_sheet = character_sheets[0]
        if (
            character_sheet.pitch_id is not None
            and character_sheet.pitch_id != state.selected_pitch_id
        ):
            return _reject(
                SessionActionReasonCode.SESSION_RESOURCE_NOT_FOUND,
                (
                    "That character sheet belongs to a different pitch than the one "
                    "currently selected."
                ),
                stage=WorkflowStage.CHARACTERS,
            )
        if state.selected_character_sheet_id == character_sheet.id:
            return _accept(
                reasons=[
                    _reason(
                        SessionActionReasonCode.ACTION_IS_NOOP,
                        "That character sheet is already selected.",
                        stage=WorkflowStage.CHARACTERS,
                    )
                ],
                resolution=_ResolvedAction(character_sheet=character_sheet),
            )

        side_effects = self._build_stage_edit_side_effects(state, WorkflowStage.CHARACTERS)
        return self._finalize_change_action(
            action,
            side_effects=side_effects,
            confirmation_granted=confirmation_granted,
            resolution=_ResolvedAction(character_sheet=character_sheet),
        )

    def _evaluate_refine_character_sheet(
        self,
        session_id: str,
        action: RefineCharacterSheetAction,
        state: _PolicyState,
        *,
        confirmation_granted: bool,
    ) -> _ComputedDecision:
        blocked = _blocked_prerequisite_stages(state, WorkflowStage.CHARACTERS)
        if blocked:
            return _reject_for_blocked_stages(blocked, target_stage=WorkflowStage.CHARACTERS)
        if state.selected_pitch_id is None:
            return _reject(
                SessionActionReasonCode.PREREQUISITE_SELECTION_MISSING,
                "Select a pitch before refining the character sheet.",
                stage=WorkflowStage.CHARACTERS,
                prerequisite_action_types=[ChatToUIActionType.SELECT_PITCH],
            )
        has_explicit_target = (
            action.extracted_values.character_sheet_id is not None
            or action.extracted_values.revision_number is not None
            or action.extracted_values.title is not None
        )
        if state.selected_character_sheet_id is None and not has_explicit_target:
            return _reject(
                SessionActionReasonCode.PREREQUISITE_SELECTION_MISSING,
                "Select a character sheet before refining it.",
                stage=WorkflowStage.CHARACTERS,
                prerequisite_action_types=[ChatToUIActionType.SELECT_CHARACTER_SHEET],
            )

        if has_explicit_target:
            character_sheets = self._find_character_sheets(session_id, action)
            if len(character_sheets) > 1:
                return _reject(
                    SessionActionReasonCode.SESSION_RESOURCE_AMBIGUOUS,
                    (
                        "More than one character sheet matched that refinement request "
                        "in this session."
                    ),
                    stage=WorkflowStage.CHARACTERS,
                )
            if not character_sheets:
                return _reject(
                    SessionActionReasonCode.SESSION_RESOURCE_NOT_FOUND,
                    "No character sheet matched that refinement request in this session.",
                    stage=WorkflowStage.CHARACTERS,
                )

            character_sheet = character_sheets[0]
            if (
                character_sheet.pitch_id is not None
                and character_sheet.pitch_id != state.selected_pitch_id
            ):
                return _reject(
                    SessionActionReasonCode.SESSION_RESOURCE_NOT_FOUND,
                    (
                        "That character sheet belongs to a different pitch than the one "
                        "currently selected."
                    ),
                    stage=WorkflowStage.CHARACTERS,
                )

        change_impact = (
            action.extracted_values.change_impact
            or infer_character_change_impact(
                instructions=action.extracted_values.instructions,
                change_summary=action.extracted_values.change_summary,
            )
        )
        side_effects = (
            self._build_stage_edit_side_effects(state, WorkflowStage.CHARACTERS)
            if change_impact.value == "major"
            else []
        )
        return self._finalize_change_action(
            action,
            side_effects=side_effects,
            confirmation_granted=confirmation_granted,
        )

    def _evaluate_regenerate_character_sheet(
        self,
        action: RegenerateCharacterSheetAction,
        state: _PolicyState,
        *,
        confirmation_granted: bool,
    ) -> _ComputedDecision:
        blocked = _blocked_prerequisite_stages(state, WorkflowStage.CHARACTERS)
        if blocked:
            return _reject_for_blocked_stages(blocked, target_stage=WorkflowStage.CHARACTERS)
        if state.selected_pitch_id is None:
            return _reject(
                SessionActionReasonCode.PREREQUISITE_SELECTION_MISSING,
                "Select a pitch before regenerating character sheets.",
                stage=WorkflowStage.CHARACTERS,
                prerequisite_action_types=[ChatToUIActionType.SELECT_PITCH],
            )

        side_effects = self._build_stage_edit_side_effects(state, WorkflowStage.CHARACTERS)
        return self._finalize_change_action(
            action,
            side_effects=side_effects,
            confirmation_granted=confirmation_granted,
        )

    def _evaluate_accept_beat_sheet(
        self,
        session_id: str,
        action: AcceptBeatSheetAction,
        state: _PolicyState,
        *,
        confirmation_granted: bool,
    ) -> _ComputedDecision:
        blocked = _blocked_prerequisite_stages(state, WorkflowStage.BEATS)
        if blocked:
            return _reject_for_blocked_stages(blocked, target_stage=WorkflowStage.BEATS)
        if state.selected_character_sheet_id is None:
            return _reject(
                SessionActionReasonCode.PREREQUISITE_SELECTION_MISSING,
                "Select a character sheet before accepting a beat sheet.",
                stage=WorkflowStage.BEATS,
                prerequisite_action_types=[ChatToUIActionType.SELECT_CHARACTER_SHEET],
            )
        if state.stage_statuses.get(WorkflowStage.BEATS) == WorkflowStageState.NEEDS_REGENERATION:
            return _reject(
                SessionActionReasonCode.TARGET_STAGE_STALE,
                (
                    "Generate fresh beats before accepting one because the current beat "
                    "sheet is stale."
                ),
                stage=WorkflowStage.BEATS,
                prerequisite_action_types=[ChatToUIActionType.REGENERATE_BEAT_SHEET],
            )

        beat_sheets = self._find_beat_sheets(session_id, action)
        if len(beat_sheets) > 1:
            return _reject(
                SessionActionReasonCode.SESSION_RESOURCE_AMBIGUOUS,
                "More than one beat sheet matched that request in this session.",
                stage=WorkflowStage.BEATS,
            )
        if not beat_sheets:
            return _reject(
                SessionActionReasonCode.SESSION_RESOURCE_NOT_FOUND,
                "No beat sheet matched that request in this session.",
                stage=WorkflowStage.BEATS,
            )

        beat_sheet = beat_sheets[0]
        if (
            beat_sheet.character_sheet_id is not None
            and beat_sheet.character_sheet_id != state.selected_character_sheet_id
        ):
            return _reject(
                SessionActionReasonCode.SESSION_RESOURCE_NOT_FOUND,
                (
                    "That beat sheet belongs to a different character sheet than the one "
                    "currently selected."
                ),
                stage=WorkflowStage.BEATS,
            )
        if state.selected_beat_sheet_id == beat_sheet.id:
            return _accept(
                reasons=[
                    _reason(
                        SessionActionReasonCode.ACTION_IS_NOOP,
                        "That beat sheet is already accepted.",
                        stage=WorkflowStage.BEATS,
                    )
                ],
                resolution=_ResolvedAction(beat_sheet=beat_sheet),
            )

        side_effects = self._build_stage_edit_side_effects(state, WorkflowStage.BEATS)
        return self._finalize_change_action(
            action,
            side_effects=side_effects,
            confirmation_granted=confirmation_granted,
            resolution=_ResolvedAction(beat_sheet=beat_sheet),
        )

    def _evaluate_refine_beat_sheet(
        self,
        action: ChatToUIAction,
        state: _PolicyState,
        *,
        confirmation_granted: bool,
    ) -> _ComputedDecision:
        blocked = _blocked_prerequisite_stages(state, WorkflowStage.BEATS)
        if blocked:
            return _reject_for_blocked_stages(blocked, target_stage=WorkflowStage.BEATS)
        if state.selected_character_sheet_id is None:
            return _reject(
                SessionActionReasonCode.PREREQUISITE_SELECTION_MISSING,
                "Select a character sheet before refining the beat sheet.",
                stage=WorkflowStage.BEATS,
                prerequisite_action_types=[ChatToUIActionType.SELECT_CHARACTER_SHEET],
            )
        if state.selected_beat_sheet_id is None:
            return _reject(
                SessionActionReasonCode.PREREQUISITE_SELECTION_MISSING,
                "Accept a beat sheet before refining it.",
                stage=WorkflowStage.BEATS,
                prerequisite_action_types=[ChatToUIActionType.ACCEPT_BEAT_SHEET],
            )

        side_effects = self._build_stage_edit_side_effects(state, WorkflowStage.BEATS)
        return self._finalize_change_action(
            action,
            side_effects=side_effects,
            confirmation_granted=confirmation_granted,
        )

    def _evaluate_regenerate_beat_sheet(
        self,
        action: RegenerateBeatSheetAction,
        state: _PolicyState,
        *,
        confirmation_granted: bool,
    ) -> _ComputedDecision:
        blocked = _blocked_prerequisite_stages(state, WorkflowStage.BEATS)
        if blocked:
            return _reject_for_blocked_stages(blocked, target_stage=WorkflowStage.BEATS)
        if state.selected_character_sheet_id is None:
            return _reject(
                SessionActionReasonCode.PREREQUISITE_SELECTION_MISSING,
                "Select a character sheet before regenerating beats.",
                stage=WorkflowStage.BEATS,
                prerequisite_action_types=[ChatToUIActionType.SELECT_CHARACTER_SHEET],
            )

        side_effects = self._build_stage_edit_side_effects(state, WorkflowStage.BEATS)
        return self._finalize_change_action(
            action,
            side_effects=side_effects,
            confirmation_granted=confirmation_granted,
        )

    def _evaluate_update_story_setup(
        self,
        action: UpdateStorySetupAction,
        state: _PolicyState,
        *,
        confirmation_granted: bool,
    ) -> _ComputedDecision:
        blocked = _blocked_prerequisite_stages(state, WorkflowStage.STORY_SETUP)
        if blocked:
            return _reject_for_blocked_stages(blocked, target_stage=WorkflowStage.STORY_SETUP)
        if state.selected_beat_sheet_id is None:
            return _reject(
                SessionActionReasonCode.PREREQUISITE_SELECTION_MISSING,
                "Accept a beat sheet before editing story setup.",
                stage=WorkflowStage.STORY_SETUP,
                prerequisite_action_types=[ChatToUIActionType.ACCEPT_BEAT_SHEET],
            )

        side_effects = self._build_stage_edit_side_effects(state, WorkflowStage.STORY_SETUP)
        return self._finalize_change_action(
            action,
            side_effects=side_effects,
            confirmation_granted=confirmation_granted,
        )

    def _evaluate_start_composition(
        self,
        action: StartCompositionAction,
        state: _PolicyState,
        *,
        confirmation_granted: bool,
    ) -> _ComputedDecision:
        blocked = _blocked_prerequisite_stages(state, WorkflowStage.COMPOSITION)
        if blocked:
            return _reject_for_blocked_stages(blocked, target_stage=WorkflowStage.COMPOSITION)
        if state.selected_beat_sheet_id is None:
            return _reject(
                SessionActionReasonCode.PREREQUISITE_SELECTION_MISSING,
                "Accept a beat sheet before starting composition.",
                stage=WorkflowStage.COMPOSITION,
                prerequisite_action_types=[ChatToUIActionType.ACCEPT_BEAT_SHEET],
            )
        if state.selected_story_setup_id is None:
            return _reject(
                SessionActionReasonCode.PREREQUISITE_SELECTION_MISSING,
                "Save story setup before starting composition.",
                stage=WorkflowStage.COMPOSITION,
                prerequisite_action_types=[ChatToUIActionType.UPDATE_STORY_SETUP],
            )
        if state.active_composition_job_status in ACTIVE_JOB_STATUSES:
            return _reject(
                SessionActionReasonCode.JOB_STATE_CONFLICT,
                (
                    "Use pause, resume, or redirect on the active composition job "
                    "instead of starting a new one."
                ),
                stage=WorkflowStage.COMPOSITION,
            )

        side_effects = self._build_stage_edit_side_effects(state, WorkflowStage.COMPOSITION)
        return self._finalize_change_action(
            action,
            side_effects=side_effects,
            confirmation_granted=confirmation_granted,
        )

    def _evaluate_pause_job(
        self,
        action: PauseJobAction,
        state: _PolicyState,
        *,
        confirmation_granted: bool,
    ) -> _ComputedDecision:
        job_status, job_id = self._resolve_requested_job(state, action)
        if job_status is None or job_id is None:
            return _reject(
                SessionActionReasonCode.JOB_NOT_ACTIVE,
                f"There is no active {action.extracted_values.job_kind.value} job to pause.",
                stage=action.target_stage,
            )
        if (
            action.extracted_values.job_kind == ChatToUIJobKind.COMPOSITION
            and state.active_composition_interruption_requested
        ):
            return _reject(
                SessionActionReasonCode.JOB_STATE_CONFLICT,
                "The writing job is already handling another pause or redirect request.",
                stage=action.target_stage,
            )
        if job_status == JobStatus.PAUSED:
            return _reject(
                SessionActionReasonCode.JOB_STATE_CONFLICT,
                f"The {action.extracted_values.job_kind.value} job is already paused.",
                stage=action.target_stage,
            )
        if job_status not in PAUSABLE_JOB_STATUSES:
            return _reject(
                SessionActionReasonCode.JOB_STATE_CONFLICT,
                (
                    f"The {action.extracted_values.job_kind.value} job cannot be paused "
                    f"from {job_status.value}."
                ),
                stage=action.target_stage,
            )

        return self._finalize_change_action(
            action,
            side_effects=[],
            confirmation_granted=confirmation_granted,
        )

    def _evaluate_resume_job(
        self,
        action: ResumeJobAction,
        state: _PolicyState,
        *,
        confirmation_granted: bool,
    ) -> _ComputedDecision:
        if state.stage_statuses.get(action.target_stage) == WorkflowStageState.NEEDS_REGENERATION:
            return _reject(
                SessionActionReasonCode.TARGET_STAGE_STALE,
                f"Resolve the stale {action.target_stage.value} stage before resuming that job.",
                stage=action.target_stage,
            )

        job_status, job_id = self._resolve_requested_job(state, action)
        if job_status is None or job_id is None:
            return _reject(
                SessionActionReasonCode.JOB_NOT_ACTIVE,
                f"There is no paused {action.extracted_values.job_kind.value} job to resume.",
                stage=action.target_stage,
            )
        if job_status != JobStatus.PAUSED:
            return _reject(
                SessionActionReasonCode.JOB_STATE_CONFLICT,
                (
                    f"The {action.extracted_values.job_kind.value} job can only be "
                    "resumed from paused."
                ),
                stage=action.target_stage,
            )

        return self._finalize_change_action(
            action,
            side_effects=[],
            confirmation_granted=confirmation_granted,
        )

    def _evaluate_redirect_composition(
        self,
        action: RedirectCompositionAction,
        state: _PolicyState,
        *,
        confirmation_granted: bool,
    ) -> _ComputedDecision:
        blocked = _blocked_prerequisite_stages(state, WorkflowStage.COMPOSITION)
        if blocked:
            return _reject_for_blocked_stages(blocked, target_stage=WorkflowStage.COMPOSITION)
        if state.active_composition_job_status not in ACTIVE_JOB_STATUSES or (
            state.active_composition_job_id is None
        ):
            return _reject(
                SessionActionReasonCode.JOB_NOT_ACTIVE,
                "Start composition before redirecting it.",
                stage=WorkflowStage.COMPOSITION,
                prerequisite_action_types=[ChatToUIActionType.START_COMPOSITION],
            )
        if state.active_composition_interruption_requested:
            return _reject(
                SessionActionReasonCode.JOB_STATE_CONFLICT,
                "The writing job is already handling another pause or redirect request.",
                stage=WorkflowStage.COMPOSITION,
            )

        side_effects = self._build_stage_edit_side_effects(
            state,
            WorkflowStage.COMPOSITION,
            force_stop_current_stage_job=True,
        )
        return self._finalize_change_action(
            action,
            side_effects=side_effects,
            confirmation_granted=confirmation_granted,
        )

    def _evaluate_update_audio_settings(
        self,
        action: UpdateAudioSettingsAction,
        state: _PolicyState,
        *,
        confirmation_granted: bool,
    ) -> _ComputedDecision:
        blocked = _blocked_prerequisite_stages(state, WorkflowStage.AUDIO)
        if blocked:
            return _reject_for_blocked_stages(blocked, target_stage=WorkflowStage.AUDIO)
        if not state.ready_story_asset_kinds:
            return _reject(
                SessionActionReasonCode.ASSET_NOT_READY,
                "Finish composition and produce story text before editing audio settings.",
                stage=WorkflowStage.AUDIO,
                prerequisite_action_types=[ChatToUIActionType.START_COMPOSITION],
            )

        side_effects = self._build_stage_edit_side_effects(
            state,
            WorkflowStage.AUDIO,
            force_stop_current_stage_job=state.active_audio_job_status in ACTIVE_JOB_STATUSES,
        )
        return self._finalize_change_action(
            action,
            side_effects=side_effects,
            confirmation_granted=confirmation_granted,
        )

    def _evaluate_start_audio_generation(
        self,
        action: StartAudioGenerationAction,
        state: _PolicyState,
        *,
        confirmation_granted: bool,
    ) -> _ComputedDecision:
        blocked = _blocked_prerequisite_stages(state, WorkflowStage.AUDIO)
        if blocked:
            return _reject_for_blocked_stages(blocked, target_stage=WorkflowStage.AUDIO)
        if not state.ready_story_asset_kinds:
            return _reject(
                SessionActionReasonCode.ASSET_NOT_READY,
                "Finish composition and produce story text before starting audio generation.",
                stage=WorkflowStage.AUDIO,
                prerequisite_action_types=[ChatToUIActionType.START_COMPOSITION],
            )
        if state.active_audio_job_status in ACTIVE_JOB_STATUSES:
            return _reject(
                SessionActionReasonCode.JOB_STATE_CONFLICT,
                "Use pause or resume on the active audio job instead of starting another one.",
                stage=WorkflowStage.AUDIO,
            )
        if (
            AssetKind.FINAL_AUDIO in state.ready_audio_asset_kinds
            and not action.extracted_values.regenerate_existing_audio
        ):
            return _reject(
                SessionActionReasonCode.ASSET_REGENERATION_REQUIRED,
                "Final audio already exists. Request regeneration explicitly before replacing it.",
                stage=WorkflowStage.AUDIO,
            )

        side_effects = self._build_stage_edit_side_effects(state, WorkflowStage.AUDIO)
        return self._finalize_change_action(
            action,
            side_effects=side_effects,
            confirmation_granted=confirmation_granted,
        )

    def _evaluate_open_finalize_view(
        self,
        action: OpenFinalizeViewAction,
        state: _PolicyState,
    ) -> _ComputedDecision:
        if (
            state.stage_statuses.get(WorkflowStage.FINALIZE)
            == WorkflowStageState.NEEDS_REGENERATION
        ):
            return _reject(
                SessionActionReasonCode.TARGET_STAGE_STALE,
                "Finalize assets are stale. Regenerate downstream work before opening that view.",
                stage=WorkflowStage.FINALIZE,
            )
        if action.extracted_values.view.value == "reader" and not state.ready_story_asset_kinds:
            return _reject(
                SessionActionReasonCode.ASSET_NOT_READY,
                "Story text is not ready to read yet.",
                stage=WorkflowStage.FINALIZE,
            )
        if (
            action.extracted_values.view.value == "player"
            and AssetKind.FINAL_AUDIO not in state.ready_audio_asset_kinds
        ):
            return _reject(
                SessionActionReasonCode.ASSET_NOT_READY,
                "Final audio is not ready to play yet.",
                stage=WorkflowStage.FINALIZE,
            )

        return _accept()

    def _evaluate_download_asset(
        self,
        action: DownloadAssetAction,
        state: _PolicyState,
    ) -> _ComputedDecision:
        if (
            state.stage_statuses.get(WorkflowStage.FINALIZE)
            == WorkflowStageState.NEEDS_REGENERATION
        ):
            return _reject(
                SessionActionReasonCode.TARGET_STAGE_STALE,
                "Finalize assets are stale. Regenerate downstream work before downloading exports.",
                stage=WorkflowStage.FINALIZE,
            )
        if action.extracted_values.asset_kind == DownloadAssetKind.STORY_DOCX:
            if AssetKind.STORY_DOCX not in state.ready_story_asset_kinds:
                return _reject(
                    SessionActionReasonCode.ASSET_NOT_READY,
                    "The Word document export is not ready yet.",
                    stage=WorkflowStage.FINALIZE,
                )
        elif AssetKind.FINAL_AUDIO not in state.ready_audio_asset_kinds:
            return _reject(
                SessionActionReasonCode.ASSET_NOT_READY,
                "The final audio export is not ready yet.",
                stage=WorkflowStage.FINALIZE,
            )

        return _accept()

    def _finalize_change_action(
        self,
        action: ChatToUIAction,
        *,
        side_effects: list[SessionActionPolicySideEffect],
        confirmation_granted: bool,
        resolution: _ResolvedAction | None = None,
    ) -> _ComputedDecision:
        if not confirmation_granted:
            if side_effects:
                return _ComputedDecision(
                    decision=SessionActionDecision.REQUIRES_CONFIRMATION,
                    reasons=[
                        _reason(
                            SessionActionReasonCode.CONFIRMATION_REQUIRED_DUE_TO_SIDE_EFFECTS,
                            (
                                "This action needs confirmation because it would "
                                "invalidate downstream work or replace active outputs."
                            ),
                            stage=action.target_stage,
                        )
                    ],
                    side_effects=side_effects,
                    resolution=resolution or _ResolvedAction(),
                )
            if (
                get_chat_to_ui_action_default_policy(action.action_type)
                == ChatToUIActionDefaultPolicy.CONFIRM_FIRST
            ):
                return _ComputedDecision(
                    decision=SessionActionDecision.REQUIRES_CONFIRMATION,
                    reasons=[
                        _reason(
                            SessionActionReasonCode.CONFIRMATION_REQUIRED_BY_DEFAULT,
                            (
                                "This action needs confirmation before it changes "
                                "accepted session state."
                            ),
                            stage=action.target_stage,
                        )
                    ],
                    resolution=resolution or _ResolvedAction(),
                )

        return _accept(
            decision=(
                SessionActionDecision.ACCEPTED_WITH_SIDE_EFFECTS
                if side_effects
                else SessionActionDecision.ACCEPTED
            ),
            side_effects=side_effects,
            resolution=resolution,
        )

    def _resolve_requested_job(
        self,
        state: _PolicyState,
        action: PauseJobAction | ResumeJobAction,
    ) -> tuple[JobStatus | None, str | None]:
        if action.extracted_values.job_kind == ChatToUIJobKind.COMPOSITION:
            job_status = state.active_composition_job_status
            job_id = state.active_composition_job_id
        else:
            job_status = state.active_audio_job_status
            job_id = state.active_audio_job_id

        if action.extracted_values.job_id is not None and action.extracted_values.job_id != job_id:
            return None, None

        return job_status, job_id

    def _build_stage_edit_side_effects(
        self,
        state: _PolicyState,
        stage: WorkflowStage,
        *,
        clear_tone_selection: bool = False,
        force_stop_current_stage_job: bool = False,
    ) -> list[SessionActionPolicySideEffect]:
        side_effects: list[SessionActionPolicySideEffect] = []
        invalidated_stages = [
            invalidated_stage
            for invalidated_stage in get_invalidated_stages_after_edit(stage)
            if state.stage_statuses.get(invalidated_stage, WorkflowStageState.DRAFT)
            != WorkflowStageState.DRAFT
        ]
        if invalidated_stages:
            side_effects.append(
                SessionActionPolicySideEffect(
                    kind=SessionActionSideEffectKind.INVALIDATE_STAGES,
                    message=(
                        "Downstream stages will be marked for regeneration: "
                        f"{_format_stage_list(invalidated_stages)}."
                    ),
                    stages=invalidated_stages,
                )
            )

        if clear_tone_selection:
            side_effects.append(
                SessionActionPolicySideEffect(
                    kind=SessionActionSideEffectKind.CLEAR_SELECTION,
                    message=(
                        "The current tone selection will be cleared because it belongs "
                        "to the previous genre."
                    ),
                    selection_field="selected_tone_profile",
                )
            )

        if force_stop_current_stage_job and stage == WorkflowStage.COMPOSITION:
            side_effects.append(
                SessionActionPolicySideEffect(
                    kind=SessionActionSideEffectKind.STOP_ACTIVE_JOB,
                    message="The active composition job must stop before the redirect can apply.",
                    job_kind=ChatToUIJobKind.COMPOSITION.value,
                )
            )
        elif force_stop_current_stage_job and stage == WorkflowStage.AUDIO:
            side_effects.append(
                SessionActionPolicySideEffect(
                    kind=SessionActionSideEffectKind.STOP_ACTIVE_JOB,
                    message="The active audio job must stop before the new settings can apply.",
                    job_kind=ChatToUIJobKind.AUDIO.value,
                )
            )

        if (
            WorkflowStage.COMPOSITION in invalidated_stages
            and state.active_composition_job_status in ACTIVE_JOB_STATUSES
        ):
            side_effects.append(
                SessionActionPolicySideEffect(
                    kind=SessionActionSideEffectKind.STOP_ACTIVE_JOB,
                    message=(
                        "The active composition job must stop before the new upstream "
                        "changes can apply."
                    ),
                    job_kind=ChatToUIJobKind.COMPOSITION.value,
                )
            )
        if (
            WorkflowStage.AUDIO in invalidated_stages
            and state.active_audio_job_status in ACTIVE_JOB_STATUSES
        ):
            side_effects.append(
                SessionActionPolicySideEffect(
                    kind=SessionActionSideEffectKind.STOP_ACTIVE_JOB,
                    message=(
                        "The active audio job must stop before the new upstream changes can apply."
                    ),
                    job_kind=ChatToUIJobKind.AUDIO.value,
                )
            )

        if (
            stage == WorkflowStage.COMPOSITION or WorkflowStage.COMPOSITION in invalidated_stages
        ) and state.ready_story_asset_kinds:
            side_effects.append(
                SessionActionPolicySideEffect(
                    kind=SessionActionSideEffectKind.SUPERSEDE_ASSET,
                    message=(
                        "Existing story exports will become stale until composition runs again."
                    ),
                    asset_kind="story",
                )
            )
        if (stage == WorkflowStage.AUDIO or WorkflowStage.AUDIO in invalidated_stages) and (
            AssetKind.FINAL_AUDIO in state.ready_audio_asset_kinds
        ):
            side_effects.append(
                SessionActionPolicySideEffect(
                    kind=SessionActionSideEffectKind.SUPERSEDE_ASSET,
                    message=(
                        "Existing final audio will become stale until audio generation runs again."
                    ),
                    asset_kind=AssetKind.FINAL_AUDIO.value,
                )
            )

        return side_effects

    def _apply_action_to_state(
        self,
        state: _PolicyState,
        action: ChatToUIAction,
        resolution: _ResolvedAction,
    ) -> None:
        if action.action_type == ChatToUIActionType.SELECT_GENRE:
            if resolution.genre is not None:
                genre_changed = state.selected_genre_id != resolution.genre.id
                state.selected_genre_id = resolution.genre.id
                if genre_changed:
                    state.selected_tone_profile_id = None
            self._mark_stage_completed(state, WorkflowStage.GENRE)
            self._invalidate_downstream_stages(state, WorkflowStage.GENRE)
            return

        if action.action_type == ChatToUIActionType.SELECT_TONE:
            if resolution.tone is not None:
                state.selected_tone_profile_id = resolution.tone.id
            self._mark_stage_completed(state, WorkflowStage.TONE)
            self._invalidate_downstream_stages(state, WorkflowStage.TONE)
            return

        if action.action_type == ChatToUIActionType.UPDATE_STORY_BRIEF:
            state.story_brief_present = True
            self._mark_stage_completed(state, WorkflowStage.BRIEF)
            self._invalidate_downstream_stages(state, WorkflowStage.BRIEF)
            return

        if action.action_type == ChatToUIActionType.REGENERATE_PITCHES:
            self._mark_stage_in_progress(state, WorkflowStage.PITCHES)
            self._invalidate_downstream_stages(state, WorkflowStage.PITCHES)
            return

        if action.action_type == ChatToUIActionType.REFINE_PITCH:
            if resolution.pitch is not None:
                state.selected_pitch_id = resolution.pitch.id
            self._mark_stage_completed(state, WorkflowStage.PITCHES)
            self._invalidate_downstream_stages(state, WorkflowStage.PITCHES)
            return

        if action.action_type == ChatToUIActionType.SELECT_PITCH:
            if resolution.pitch is not None:
                state.selected_pitch_id = resolution.pitch.id
            self._mark_stage_completed(state, WorkflowStage.PITCHES)
            self._invalidate_downstream_stages(state, WorkflowStage.PITCHES)
            return

        if action.action_type in {
            ChatToUIActionType.REFINE_CHARACTER_SHEET,
            ChatToUIActionType.REGENERATE_CHARACTER_SHEET,
        }:
            self._mark_stage_in_progress(state, WorkflowStage.CHARACTERS)
            self._invalidate_downstream_stages(state, WorkflowStage.CHARACTERS)
            return

        if action.action_type == ChatToUIActionType.SELECT_CHARACTER_SHEET:
            if resolution.character_sheet is not None:
                state.selected_character_sheet_id = resolution.character_sheet.id
            self._mark_stage_completed(state, WorkflowStage.CHARACTERS)
            self._invalidate_downstream_stages(state, WorkflowStage.CHARACTERS)
            return

        if action.action_type in {
            ChatToUIActionType.REFINE_BEAT_SHEET,
            ChatToUIActionType.REGENERATE_BEAT_SHEET,
        }:
            self._mark_stage_in_progress(state, WorkflowStage.BEATS)
            self._invalidate_downstream_stages(state, WorkflowStage.BEATS)
            return

        if action.action_type == ChatToUIActionType.ACCEPT_BEAT_SHEET:
            if resolution.beat_sheet is not None:
                state.selected_beat_sheet_id = resolution.beat_sheet.id
            self._mark_stage_completed(state, WorkflowStage.BEATS)
            self._invalidate_downstream_stages(state, WorkflowStage.BEATS)
            return

        if action.action_type == ChatToUIActionType.UPDATE_STORY_SETUP:
            state.selected_story_setup_id = state.selected_story_setup_id or "pending-story-setup"
            self._mark_stage_completed(state, WorkflowStage.STORY_SETUP)
            self._invalidate_downstream_stages(state, WorkflowStage.STORY_SETUP)
            return

        if action.action_type == ChatToUIActionType.START_COMPOSITION:
            state.active_composition_job_id = (
                state.active_composition_job_id or "pending-composition"
            )
            state.active_composition_job_status = JobStatus.IN_PROGRESS
            self._mark_stage_in_progress(state, WorkflowStage.COMPOSITION)
            self._invalidate_downstream_stages(state, WorkflowStage.COMPOSITION)
            state.ready_story_asset_kinds.clear()
            return

        if action.action_type == ChatToUIActionType.PAUSE_JOB:
            if action.extracted_values.job_kind == ChatToUIJobKind.COMPOSITION:
                state.active_composition_job_status = JobStatus.PAUSED
            else:
                state.active_audio_job_status = JobStatus.PAUSED
            return

        if action.action_type == ChatToUIActionType.RESUME_JOB:
            if action.extracted_values.job_kind == ChatToUIJobKind.COMPOSITION:
                state.active_composition_job_status = JobStatus.IN_PROGRESS
            else:
                state.active_audio_job_status = JobStatus.IN_PROGRESS
            return

        if action.action_type == ChatToUIActionType.REDIRECT_COMPOSITION:
            state.active_composition_job_status = JobStatus.IN_PROGRESS
            self._mark_stage_in_progress(state, WorkflowStage.COMPOSITION)
            self._invalidate_downstream_stages(state, WorkflowStage.COMPOSITION)
            state.ready_story_asset_kinds.clear()
            return

        if action.action_type == ChatToUIActionType.UPDATE_AUDIO_SETTINGS:
            self._mark_stage_in_progress(state, WorkflowStage.AUDIO)
            self._invalidate_downstream_stages(state, WorkflowStage.AUDIO)
            return

        if action.action_type == ChatToUIActionType.START_AUDIO_GENERATION:
            state.active_audio_job_id = state.active_audio_job_id or "pending-audio"
            state.active_audio_job_status = JobStatus.IN_PROGRESS
            self._mark_stage_in_progress(state, WorkflowStage.AUDIO)
            self._invalidate_downstream_stages(state, WorkflowStage.AUDIO)
            state.ready_audio_asset_kinds.clear()
            return

    def _mark_stage_completed(self, state: _PolicyState, stage: WorkflowStage) -> None:
        state.stage_statuses[stage] = WorkflowStageState.COMPLETED

    def _mark_stage_in_progress(self, state: _PolicyState, stage: WorkflowStage) -> None:
        state.stage_statuses[stage] = WorkflowStageState.IN_PROGRESS

    def _invalidate_downstream_stages(
        self,
        state: _PolicyState,
        stage: WorkflowStage,
    ) -> None:
        for invalidated_stage in get_invalidated_stages_after_edit(stage):
            if state.stage_statuses.get(invalidated_stage, WorkflowStageState.DRAFT) == (
                WorkflowStageState.DRAFT
            ):
                continue
            state.stage_statuses[invalidated_stage] = WorkflowStageState.NEEDS_REGENERATION

        if stage == WorkflowStage.GENRE:
            state.selected_tone_profile_id = None
        if (
            stage == WorkflowStage.COMPOSITION
            or WorkflowStage.COMPOSITION in get_invalidated_stages_after_edit(stage)
        ):
            state.active_composition_job_id = None
            state.active_composition_job_status = None
            state.ready_story_asset_kinds.clear()
        if stage == WorkflowStage.AUDIO or WorkflowStage.AUDIO in get_invalidated_stages_after_edit(
            stage
        ):
            state.active_audio_job_id = None
            state.active_audio_job_status = None
            state.ready_audio_asset_kinds.clear()

    def _load_ready_story_asset_kinds(self, session_id: str) -> set[AssetKind]:
        stmt = select(SessionAsset.asset_kind).where(
            SessionAsset.session_id == session_id,
            SessionAsset.status == AssetStatus.READY,
            SessionAsset.asset_kind.in_((AssetKind.STORY_TEXT, AssetKind.STORY_DOCX)),
        )
        return {AssetKind(kind) for kind in self._session.execute(stmt).scalars().all()}

    def _load_ready_audio_asset_kinds(self, session_id: str) -> set[AssetKind]:
        stmt = select(SessionAsset.asset_kind).where(
            SessionAsset.session_id == session_id,
            SessionAsset.status == AssetStatus.READY,
            SessionAsset.asset_kind == AssetKind.FINAL_AUDIO,
        )
        return {AssetKind(kind) for kind in self._session.execute(stmt).scalars().all()}

    def _find_genres(self, action: SelectGenreAction) -> list[Genre]:
        values = action.extracted_values
        stmt: Select[tuple[Genre]] = select(Genre).where(Genre.is_active.is_(True))
        if values.genre_id is not None:
            stmt = stmt.where(Genre.id == values.genre_id)
        if values.genre_slug is not None:
            stmt = stmt.where(Genre.slug == values.genre_slug)
        if values.genre_label is not None:
            stmt = stmt.where(func.lower(Genre.label) == values.genre_label.lower())
        return list(self._session.execute(stmt.limit(2)).scalars().all())

    def _find_tones(self, action: SelectToneAction, *, genre_id: str) -> list[ToneProfile]:
        values = action.extracted_values
        stmt: Select[tuple[ToneProfile]] = select(ToneProfile).where(
            ToneProfile.is_active.is_(True),
            ToneProfile.genre_id == genre_id,
        )
        if values.tone_profile_id is not None:
            stmt = stmt.where(ToneProfile.id == values.tone_profile_id)
        if values.tone_profile_slug is not None:
            stmt = stmt.where(ToneProfile.slug == values.tone_profile_slug)
        if values.tone_profile_label is not None:
            stmt = stmt.where(func.lower(ToneProfile.label) == values.tone_profile_label.lower())
        return list(self._session.execute(stmt.limit(2)).scalars().all())

    def _find_pitches(
        self,
        session_id: str,
        action: SelectPitchAction | RefinePitchAction,
    ) -> list[Pitch]:
        values = action.extracted_values
        stmt: Select[tuple[Pitch]] = select(Pitch).where(Pitch.session_id == session_id)
        if values.pitch_id is not None:
            stmt = stmt.where(Pitch.id == values.pitch_id)
        if values.generation_key is not None:
            stmt = stmt.where(Pitch.generation_key == values.generation_key)
        if values.pitch_index is not None:
            stmt = stmt.where(Pitch.pitch_index == values.pitch_index)
        if values.title is not None:
            stmt = stmt.where(func.lower(Pitch.title) == values.title.lower())
        return list(self._session.execute(stmt.limit(2)).scalars().all())

    def _find_character_sheets(
        self,
        session_id: str,
        action: SelectCharacterSheetAction | RefineCharacterSheetAction,
    ) -> list[CharacterSheet]:
        values = action.extracted_values
        stmt: Select[tuple[CharacterSheet]] = select(CharacterSheet).where(
            CharacterSheet.session_id == session_id
        )
        if values.character_sheet_id is not None:
            stmt = stmt.where(CharacterSheet.id == values.character_sheet_id)
        if values.revision_number is not None:
            stmt = stmt.where(CharacterSheet.revision_number == values.revision_number)
        if values.title is not None:
            stmt = stmt.where(func.lower(CharacterSheet.title) == values.title.lower())
        return list(self._session.execute(stmt.limit(2)).scalars().all())

    def _find_beat_sheets(
        self,
        session_id: str,
        action: AcceptBeatSheetAction,
    ) -> list[BeatSheet]:
        values = action.extracted_values
        stmt: Select[tuple[BeatSheet]] = select(BeatSheet).where(BeatSheet.session_id == session_id)
        if values.beat_sheet_id is not None:
            stmt = stmt.where(BeatSheet.id == values.beat_sheet_id)
        if values.revision_number is not None:
            stmt = stmt.where(BeatSheet.revision_number == values.revision_number)
        return list(self._session.execute(stmt.limit(2)).scalars().all())


def _accept(
    *,
    decision: SessionActionDecision = SessionActionDecision.ACCEPTED,
    reasons: list[SessionActionPolicyReason] | None = None,
    side_effects: list[SessionActionPolicySideEffect] | None = None,
    resolution: _ResolvedAction | None = None,
) -> _ComputedDecision:
    return _ComputedDecision(
        decision=decision,
        reasons=list(reasons or []),
        side_effects=list(side_effects or []),
        resolution=resolution or _ResolvedAction(),
    )


def _reject(
    code: SessionActionReasonCode,
    message: str,
    *,
    stage: WorkflowStage | None = None,
    related_stages: list[WorkflowStage] | None = None,
    prerequisite_action_types: list[ChatToUIActionType] | None = None,
) -> _ComputedDecision:
    return _ComputedDecision(
        decision=SessionActionDecision.REJECTED,
        reasons=[
            _reason(
                code,
                message,
                stage=stage,
                related_stages=related_stages,
                related_action_types=prerequisite_action_types,
            )
        ],
        prerequisite_action_types=list(prerequisite_action_types or []),
    )


def _reason(
    code: SessionActionReasonCode,
    message: str,
    *,
    stage: WorkflowStage | None = None,
    related_stages: list[WorkflowStage] | None = None,
    related_action_types: list[ChatToUIActionType] | None = None,
) -> SessionActionPolicyReason:
    return SessionActionPolicyReason(
        code=code,
        message=message,
        stage=stage,
        related_stages=list(related_stages or []),
        related_action_types=list(related_action_types or []),
    )


def _reject_for_blocked_stages(
    blocked_stages: list[WorkflowStage],
    *,
    target_stage: WorkflowStage,
) -> _ComputedDecision:
    return _reject(
        SessionActionReasonCode.PREREQUISITE_STAGE_INCOMPLETE,
        (
            f"Complete or regenerate {_format_stage_list(blocked_stages)} "
            f"before changing {target_stage.value}."
        ),
        stage=target_stage,
        related_stages=blocked_stages,
    )


def _blocked_prerequisite_stages(
    state: _PolicyState,
    target_stage: WorkflowStage,
) -> list[WorkflowStage]:
    blocked: list[WorkflowStage] = []
    for stage in WORKFLOW_STAGE_SEQUENCE:
        if stage == target_stage:
            break
        if (
            state.stage_statuses.get(stage, WorkflowStageState.DRAFT)
            != WorkflowStageState.COMPLETED
        ):
            blocked.append(stage)
    return blocked


def _build_decision_summary(
    action: ChatToUIAction,
    *,
    decision: SessionActionDecision,
    reasons: list[SessionActionPolicyReason],
    side_effects: list[SessionActionPolicySideEffect],
) -> str:
    if decision in {SessionActionDecision.REJECTED, SessionActionDecision.REQUIRES_CONFIRMATION}:
        return reasons[0].message
    if reasons and reasons[0].code == SessionActionReasonCode.ACTION_IS_NOOP:
        return reasons[0].message
    if decision == SessionActionDecision.ACCEPTED_WITH_SIDE_EFFECTS and side_effects:
        return side_effects[0].message
    if action.action_type == ChatToUIActionType.NAVIGATE_TO_STAGE:
        return "Navigation is allowed."
    if action.action_type == ChatToUIActionType.OPEN_FINALIZE_VIEW:
        return "Finalize view can be opened."
    if action.action_type == ChatToUIActionType.DOWNLOAD_ASSET:
        return "The requested export is ready to download."
    if action.action_type == ChatToUIActionType.PAUSE_JOB:
        return "The active job can be paused."
    if action.action_type == ChatToUIActionType.RESUME_JOB:
        return "The paused job can be resumed."
    return "Action can be applied."


def _format_stage_list(stages: list[WorkflowStage]) -> str:
    labels = [stage.value.replace("_", " ") for stage in stages]
    if len(labels) == 1:
        return labels[0]
    if len(labels) == 2:
        return f"{labels[0]} and {labels[1]}"
    return f"{', '.join(labels[:-1])}, and {labels[-1]}"

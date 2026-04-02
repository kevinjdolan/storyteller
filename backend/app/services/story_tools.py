from __future__ import annotations
from dataclasses import dataclass
from functools import lru_cache
from typing import Any

from sqlalchemy import Select, func, select
from sqlalchemy.orm import Session

from app.db import (
    AudioJob,
    CharacterSheet,
    CompositionJob,
    CompositionJobKind,
    CompositionSegment,
    JobStatus,
    Pitch,
    StorySetup,
)
from app.db.base import utc_now
from app.models import (
    WORKFLOW_STAGE_SEQUENCE,
    ChatToUIActionBatch,
    ChatToUIActionType,
    CompositionStartMode,
    SelectionKind,
    SessionEventActor,
    UserEditTargetKind,
    WorkflowStage,
    WorkflowStageState,
)
from app.models.chat_actions import (
    RedirectCompositionAction,
    StartAudioGenerationAction,
    StartCompositionAction,
)
from app.models.story_tools import (
    AudioLengthEstimateSource,
    ComposeNextSegmentToolInput,
    CompositionToolResult,
    EstimateAudioLengthToolInput,
    EstimateAudioLengthToolResult,
    GenerateBeatSheetToolInput,
    GenerateCharacterSheetsToolInput,
    GeneratePitchesToolInput,
    RefineCharacterSheetToolInput,
    RefinePitchToolInput,
    RewriteSegmentsToolInput,
    StageOperationToolResult,
    StartAudioGenerationToolInput,
    StartAudioGenerationToolResult,
    StoryWorkflowToolCall,
    StoryWorkflowToolExecutionMode,
    StoryWorkflowToolName,
    StoryWorkflowToolPlan,
    StoryWorkflowToolResultBase,
    StoryWorkflowToolSideEffect,
    StoryWorkflowToolSideEffectKind,
    UpdateSetupHeuristicsToolInput,
    UpdateSetupHeuristicsToolResult,
)
from app.services.beat_sheet_generation import BeatSheetGenerationService
from app.services.character_generation import CharacterGenerationService
from app.services.event_log import DEFAULT_SYSTEM_ACTOR, SessionEventLogService
from app.services.jobs import BackgroundJobRecord, BackgroundJobService
from app.services.planning_heuristics import estimate_narration_duration_seconds
from app.services.pitch_generation import PitchGenerationService
from app.services.sessions import SessionNotFoundError, SessionService


class StoryWorkflowToolServiceError(Exception):
    """Base error for tool-registry backed story workflow operations."""


@dataclass(frozen=True)
class StoryWorkflowToolDefinition:
    name: StoryWorkflowToolName
    stage: WorkflowStage
    description: str
    execution_mode: StoryWorkflowToolExecutionMode
    job_type: str
    request_model: type
    response_model: type[StoryWorkflowToolResultBase]
    side_effects: tuple[StoryWorkflowToolSideEffect, ...]
    related_chat_actions: tuple[ChatToUIActionType, ...] = ()
    executor_name: str = ""


class StoryWorkflowToolRegistry:
    def __init__(self, definitions: list[StoryWorkflowToolDefinition]) -> None:
        self._by_name = {definition.name: definition for definition in definitions}
        self._by_job_type = {definition.job_type: definition for definition in definitions}
        if len(self._by_name) != len(definitions):
            raise ValueError("tool names must be unique")
        if len(self._by_job_type) != len(definitions):
            raise ValueError("worker job types must be unique")

    def get(self, tool_name: StoryWorkflowToolName | str) -> StoryWorkflowToolDefinition:
        normalized = StoryWorkflowToolName(tool_name)
        return self._by_name[normalized]

    def get_by_job_type(self, job_type: str) -> StoryWorkflowToolDefinition:
        return self._by_job_type[job_type]

    def list_tools(self) -> tuple[StoryWorkflowToolDefinition, ...]:
        ordered_names = sorted(self._by_name, key=lambda item: item.value)
        return tuple(self._by_name[name] for name in ordered_names)

    def validate_arguments(
        self,
        tool_name: StoryWorkflowToolName | str,
        arguments: dict[str, Any] | None,
    ):
        definition = self.get(tool_name)
        payload = arguments if isinstance(arguments, dict) else {}
        return definition.request_model.model_validate(payload)

    def build_schema_bundle(self) -> dict[str, Any]:
        return {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "bundle_schema_version": 1,
            "tools": [
                {
                    "tool_name": definition.name.value,
                    "stage": definition.stage.value,
                    "description": definition.description,
                    "execution_mode": definition.execution_mode.value,
                    "job_type": definition.job_type,
                    "related_chat_actions": [
                        action_type.value for action_type in definition.related_chat_actions
                    ],
                    "side_effects": [
                        side_effect.model_dump(mode="json")
                        for side_effect in definition.side_effects
                    ],
                    "input_schema": definition.request_model.model_json_schema(),
                    "output_schema": definition.response_model.model_json_schema(),
                }
                for definition in self.list_tools()
            ],
        }

    def build_prompt_catalog(self) -> list[dict[str, Any]]:
        return [
            {
                "tool_name": definition.name.value,
                "stage": definition.stage.value,
                "description": definition.description,
                "execution_mode": definition.execution_mode.value,
                "related_chat_actions": [
                    action_type.value for action_type in definition.related_chat_actions
                ],
                "side_effects": [effect.summary for effect in definition.side_effects],
            }
            for definition in self.list_tools()
        ]


def get_story_workflow_tool_schema_bundle() -> dict[str, Any]:
    return get_story_workflow_tool_registry().build_schema_bundle()


def get_story_workflow_tool_prompt_catalog() -> list[dict[str, Any]]:
    return get_story_workflow_tool_registry().build_prompt_catalog()


@lru_cache(maxsize=1)
def get_story_workflow_tool_registry() -> StoryWorkflowToolRegistry:
    return StoryWorkflowToolRegistry(
        [
            StoryWorkflowToolDefinition(
                name=StoryWorkflowToolName.GENERATE_PITCHES,
                stage=WorkflowStage.PITCHES,
                description=(
                    "Start or restart pitch generation from the current story brief and planning "
                    "context."
                ),
                execution_mode=StoryWorkflowToolExecutionMode.BACKGROUND,
                job_type="story.generate_pitches",
                request_model=GeneratePitchesToolInput,
                response_model=StageOperationToolResult,
                side_effects=(
                    _side_effect(
                        StoryWorkflowToolSideEffectKind.UPDATE_WORKFLOW_STAGE,
                        "Marks the pitches stage in progress and refreshes downstream staleness.",
                        stages=[WorkflowStage.PITCHES],
                        writes_to=["workflow_stage_states"],
                    ),
                ),
                related_chat_actions=(ChatToUIActionType.REGENERATE_PITCHES,),
                executor_name="_generate_pitches",
            ),
            StoryWorkflowToolDefinition(
                name=StoryWorkflowToolName.REFINE_PITCH,
                stage=WorkflowStage.PITCHES,
                description="Refine an existing pitch candidate before the user re-selects it.",
                execution_mode=StoryWorkflowToolExecutionMode.BACKGROUND,
                job_type="story.refine_pitch",
                request_model=RefinePitchToolInput,
                response_model=StageOperationToolResult,
                side_effects=(
                    _side_effect(
                        StoryWorkflowToolSideEffectKind.UPDATE_WORKFLOW_STAGE,
                        "Keeps the pitches stage in progress while a refined pitch pass runs.",
                        stages=[WorkflowStage.PITCHES],
                        writes_to=["workflow_stage_states"],
                    ),
                ),
                related_chat_actions=(ChatToUIActionType.REFINE_PITCH,),
                executor_name="_refine_pitch",
            ),
            StoryWorkflowToolDefinition(
                name=StoryWorkflowToolName.GENERATE_CHARACTER_SHEETS,
                stage=WorkflowStage.CHARACTERS,
                description="Generate or regenerate character sheets from the selected pitch.",
                execution_mode=StoryWorkflowToolExecutionMode.BACKGROUND,
                job_type="story.generate_character_sheets",
                request_model=GenerateCharacterSheetsToolInput,
                response_model=StageOperationToolResult,
                side_effects=(
                    _side_effect(
                        StoryWorkflowToolSideEffectKind.UPDATE_WORKFLOW_STAGE,
                        "Marks the characters stage in progress and invalidates later planning.",
                        stages=[WorkflowStage.CHARACTERS],
                        writes_to=["workflow_stage_states"],
                    ),
                ),
                related_chat_actions=(ChatToUIActionType.REGENERATE_CHARACTER_SHEET,),
                executor_name="_generate_character_sheets",
            ),
            StoryWorkflowToolDefinition(
                name=StoryWorkflowToolName.REFINE_CHARACTER_SHEET,
                stage=WorkflowStage.CHARACTERS,
                description=(
                    "Apply a targeted character-sheet refinement request against the current cast."
                ),
                execution_mode=StoryWorkflowToolExecutionMode.BACKGROUND,
                job_type="story.refine_character_sheet",
                request_model=RefineCharacterSheetToolInput,
                response_model=StageOperationToolResult,
                side_effects=(
                    _side_effect(
                        StoryWorkflowToolSideEffectKind.UPDATE_WORKFLOW_STAGE,
                        "Keeps the characters stage in progress while the revision request runs.",
                        stages=[WorkflowStage.CHARACTERS],
                        writes_to=["workflow_stage_states"],
                    ),
                ),
                related_chat_actions=(ChatToUIActionType.REFINE_CHARACTER_SHEET,),
                executor_name="_refine_character_sheet",
            ),
            StoryWorkflowToolDefinition(
                name=StoryWorkflowToolName.GENERATE_BEAT_SHEET,
                stage=WorkflowStage.BEATS,
                description="Generate or revise the Save-the-Cat beat sheet for the chosen plan.",
                execution_mode=StoryWorkflowToolExecutionMode.BACKGROUND,
                job_type="story.generate_beat_sheet",
                request_model=GenerateBeatSheetToolInput,
                response_model=StageOperationToolResult,
                side_effects=(
                    _side_effect(
                        StoryWorkflowToolSideEffectKind.UPDATE_WORKFLOW_STAGE,
                        "Marks the beat-sheet stage in progress and invalidates composition work.",
                        stages=[WorkflowStage.BEATS],
                        writes_to=["workflow_stage_states"],
                    ),
                ),
                related_chat_actions=(
                    ChatToUIActionType.REFINE_BEAT_SHEET,
                    ChatToUIActionType.REGENERATE_BEAT_SHEET,
                ),
                executor_name="_generate_beat_sheet",
            ),
            StoryWorkflowToolDefinition(
                name=StoryWorkflowToolName.UPDATE_SETUP_HEURISTICS,
                stage=WorkflowStage.STORY_SETUP,
                description=(
                    "Persist a new set of soft story targets such as runtime, words, chapters, "
                    "and setup notes."
                ),
                execution_mode=StoryWorkflowToolExecutionMode.DIRECT,
                job_type="story.update_setup_heuristics",
                request_model=UpdateSetupHeuristicsToolInput,
                response_model=UpdateSetupHeuristicsToolResult,
                side_effects=(
                    _side_effect(
                        StoryWorkflowToolSideEffectKind.CREATE_REVISION,
                        "Creates a selected story-setup revision.",
                        stages=[WorkflowStage.STORY_SETUP],
                        writes_to=["story_setups"],
                    ),
                    _side_effect(
                        StoryWorkflowToolSideEffectKind.UPDATE_WORKFLOW_STAGE,
                        (
                            "Marks story setup complete and invalidates composition, audio, "
                            "and finalize."
                        ),
                        stages=[
                            WorkflowStage.STORY_SETUP,
                            WorkflowStage.COMPOSITION,
                            WorkflowStage.AUDIO,
                            WorkflowStage.FINALIZE,
                        ],
                        writes_to=["workflow_stage_states"],
                    ),
                ),
                related_chat_actions=(ChatToUIActionType.UPDATE_STORY_SETUP,),
                executor_name="_update_setup_heuristics",
            ),
            StoryWorkflowToolDefinition(
                name=StoryWorkflowToolName.COMPOSE_NEXT_SEGMENT,
                stage=WorkflowStage.COMPOSITION,
                description="Create the next durable composition job and seed the next segment.",
                execution_mode=StoryWorkflowToolExecutionMode.BACKGROUND,
                job_type="story.compose_next_segment",
                request_model=ComposeNextSegmentToolInput,
                response_model=CompositionToolResult,
                side_effects=(
                    _side_effect(
                        StoryWorkflowToolSideEffectKind.CANCEL_ACTIVE_JOB,
                        "Cancels any still-active composition job before a new segment run starts.",
                        stages=[WorkflowStage.COMPOSITION],
                        writes_to=["composition_jobs"],
                    ),
                    _side_effect(
                        StoryWorkflowToolSideEffectKind.CREATE_JOB,
                        "Creates a composition job for the next segment pass.",
                        stages=[WorkflowStage.COMPOSITION],
                        writes_to=["composition_jobs"],
                    ),
                    _side_effect(
                        StoryWorkflowToolSideEffectKind.CREATE_SEGMENT,
                        "Seeds the next durable composition segment row.",
                        stages=[WorkflowStage.COMPOSITION],
                        writes_to=["composition_segments"],
                    ),
                ),
                related_chat_actions=(ChatToUIActionType.START_COMPOSITION,),
                executor_name="_compose_next_segment",
            ),
            StoryWorkflowToolDefinition(
                name=StoryWorkflowToolName.REWRITE_SEGMENTS,
                stage=WorkflowStage.COMPOSITION,
                description="Start a rewrite pass from an earlier composition segment.",
                execution_mode=StoryWorkflowToolExecutionMode.BACKGROUND,
                job_type="story.rewrite_segments",
                request_model=RewriteSegmentsToolInput,
                response_model=CompositionToolResult,
                side_effects=(
                    _side_effect(
                        StoryWorkflowToolSideEffectKind.CANCEL_ACTIVE_JOB,
                        "Cancels any still-active composition job before a rewrite starts.",
                        stages=[WorkflowStage.COMPOSITION],
                        writes_to=["composition_jobs"],
                    ),
                    _side_effect(
                        StoryWorkflowToolSideEffectKind.CREATE_JOB,
                        "Creates a rewrite composition job.",
                        stages=[WorkflowStage.COMPOSITION],
                        writes_to=["composition_jobs"],
                    ),
                    _side_effect(
                        StoryWorkflowToolSideEffectKind.CREATE_SEGMENT,
                        (
                            "Creates a new composition-segment revision starting from the "
                            "rewrite point."
                        ),
                        stages=[WorkflowStage.COMPOSITION],
                        writes_to=["composition_segments"],
                    ),
                ),
                related_chat_actions=(
                    ChatToUIActionType.START_COMPOSITION,
                    ChatToUIActionType.REDIRECT_COMPOSITION,
                ),
                executor_name="_rewrite_segments",
            ),
            StoryWorkflowToolDefinition(
                name=StoryWorkflowToolName.ESTIMATE_AUDIO_LENGTH,
                stage=WorkflowStage.AUDIO,
                description=(
                    "Estimate narration duration from persisted composition text or story-setup "
                    "word-count guidance."
                ),
                execution_mode=StoryWorkflowToolExecutionMode.DIRECT,
                job_type="story.estimate_audio_length",
                request_model=EstimateAudioLengthToolInput,
                response_model=EstimateAudioLengthToolResult,
                side_effects=(
                    _side_effect(
                        StoryWorkflowToolSideEffectKind.COMPUTE_ESTIMATE,
                        "Computes a narration-length estimate without mutating durable state.",
                        stages=[WorkflowStage.AUDIO],
                        writes_to=[],
                    ),
                ),
                related_chat_actions=(ChatToUIActionType.START_AUDIO_GENERATION,),
                executor_name="_estimate_audio_length",
            ),
            StoryWorkflowToolDefinition(
                name=StoryWorkflowToolName.START_AUDIO_GENERATION,
                stage=WorkflowStage.AUDIO,
                description=(
                    "Create a durable audio job using the latest story text and audio settings."
                ),
                execution_mode=StoryWorkflowToolExecutionMode.BACKGROUND,
                job_type="story.start_audio_generation",
                request_model=StartAudioGenerationToolInput,
                response_model=StartAudioGenerationToolResult,
                side_effects=(
                    _side_effect(
                        StoryWorkflowToolSideEffectKind.CANCEL_ACTIVE_JOB,
                        "Cancels any active audio job before starting a new narration run.",
                        stages=[WorkflowStage.AUDIO],
                        writes_to=["audio_jobs"],
                    ),
                    _side_effect(
                        StoryWorkflowToolSideEffectKind.CREATE_JOB,
                        "Creates a new audio job and records an initial duration estimate.",
                        stages=[WorkflowStage.AUDIO],
                        writes_to=["audio_jobs"],
                    ),
                    _side_effect(
                        StoryWorkflowToolSideEffectKind.UPDATE_WORKFLOW_STAGE,
                        "Marks the audio stage in progress for the new narration run.",
                        stages=[WorkflowStage.AUDIO],
                        writes_to=["workflow_stage_states"],
                    ),
                ),
                related_chat_actions=(ChatToUIActionType.START_AUDIO_GENERATION,),
                executor_name="_start_audio_generation",
            ),
        ]
    )


class StoryWorkflowActionRouter:
    def __init__(self, registry: StoryWorkflowToolRegistry | None = None) -> None:
        self._registry = registry or get_story_workflow_tool_registry()

    def plan_calls(
        self,
        *,
        session_id: str,
        batch: ChatToUIActionBatch,
    ) -> StoryWorkflowToolPlan:
        calls: list[StoryWorkflowToolCall] = []

        for action in batch.actions:
            planned = self._plan_action(session_id=session_id, action=action)
            if planned is None:
                continue
            calls.append(planned)

        return StoryWorkflowToolPlan(calls=calls)

    def _plan_action(
        self,
        *,
        session_id: str,
        action,
    ) -> StoryWorkflowToolCall | None:
        arguments = action.extracted_values.model_dump(mode="json", exclude_none=True)

        if action.action_type == ChatToUIActionType.REGENERATE_PITCHES:
            return self._build_call(
                session_id=session_id,
                tool_name=StoryWorkflowToolName.GENERATE_PITCHES,
                arguments=arguments,
                action_type=action.action_type,
            )
        if action.action_type == ChatToUIActionType.REFINE_PITCH:
            return self._build_call(
                session_id=session_id,
                tool_name=StoryWorkflowToolName.REFINE_PITCH,
                arguments=arguments,
                action_type=action.action_type,
            )
        if action.action_type == ChatToUIActionType.REFINE_CHARACTER_SHEET:
            return self._build_call(
                session_id=session_id,
                tool_name=StoryWorkflowToolName.REFINE_CHARACTER_SHEET,
                arguments=arguments,
                action_type=action.action_type,
            )
        if action.action_type == ChatToUIActionType.REGENERATE_CHARACTER_SHEET:
            return self._build_call(
                session_id=session_id,
                tool_name=StoryWorkflowToolName.GENERATE_CHARACTER_SHEETS,
                arguments=arguments,
                action_type=action.action_type,
            )
        if action.action_type in {
            ChatToUIActionType.REFINE_BEAT_SHEET,
            ChatToUIActionType.REGENERATE_BEAT_SHEET,
        }:
            return self._build_call(
                session_id=session_id,
                tool_name=StoryWorkflowToolName.GENERATE_BEAT_SHEET,
                arguments=arguments,
                action_type=action.action_type,
            )
        if action.action_type == ChatToUIActionType.UPDATE_STORY_SETUP:
            return self._build_call(
                session_id=session_id,
                tool_name=StoryWorkflowToolName.UPDATE_SETUP_HEURISTICS,
                arguments=arguments,
                action_type=action.action_type,
            )
        if action.action_type == ChatToUIActionType.START_COMPOSITION:
            return self._plan_start_composition(
                session_id=session_id,
                action=action,
            )
        if action.action_type == ChatToUIActionType.REDIRECT_COMPOSITION:
            redirect_action = action
            if not isinstance(redirect_action, RedirectCompositionAction):
                return None
            return self._build_call(
                session_id=session_id,
                tool_name=StoryWorkflowToolName.REWRITE_SEGMENTS,
                arguments=redirect_action.extracted_values.model_dump(
                    mode="json",
                    exclude_none=True,
                ),
                action_type=redirect_action.action_type,
            )
        if action.action_type == ChatToUIActionType.START_AUDIO_GENERATION:
            start_audio_action = action
            if not isinstance(start_audio_action, StartAudioGenerationAction):
                return None
            return self._build_call(
                session_id=session_id,
                tool_name=StoryWorkflowToolName.START_AUDIO_GENERATION,
                arguments=start_audio_action.extracted_values.model_dump(
                    mode="json",
                    exclude_none=True,
                ),
                action_type=start_audio_action.action_type,
            )

        return None

    def _plan_start_composition(
        self,
        *,
        session_id: str,
        action: StartCompositionAction,
    ) -> StoryWorkflowToolCall:
        arguments = action.extracted_values.model_dump(mode="json", exclude_none=True)

        if action.extracted_values.mode == CompositionStartMode.REWRITE:
            return self._build_call(
                session_id=session_id,
                tool_name=StoryWorkflowToolName.REWRITE_SEGMENTS,
                arguments={
                    "instructions": action.extracted_values.instructions
                    or "Rewrite the selected story segment.",
                    "rewrite_from_segment_index": action.extracted_values.restart_from_segment_index
                    or 1,
                    "preserve_completed_segments": False,
                },
                action_type=action.action_type,
            )

        return self._build_call(
            session_id=session_id,
            tool_name=StoryWorkflowToolName.COMPOSE_NEXT_SEGMENT,
            arguments=arguments,
            action_type=action.action_type,
        )

    def _build_call(
        self,
        *,
        session_id: str,
        tool_name: StoryWorkflowToolName,
        arguments: dict[str, Any],
        action_type: ChatToUIActionType,
    ) -> StoryWorkflowToolCall:
        validated = self._registry.validate_arguments(tool_name, arguments)
        return StoryWorkflowToolCall(
            tool_name=tool_name,
            session_id=session_id,
            arguments=validated.model_dump(mode="json", exclude_none=True),
            source_action_type=action_type,
        )


class StoryWorkflowToolService:
    def __init__(
        self,
        session: Session,
        registry: StoryWorkflowToolRegistry | None = None,
        *,
        beat_sheet_generation_service: BeatSheetGenerationService | None = None,
        character_generation_service: CharacterGenerationService | None = None,
        pitch_generation_service: PitchGenerationService | None = None,
    ):
        self._session = session
        self._registry = registry or get_story_workflow_tool_registry()
        self._sessions = SessionService(session)
        self._events = SessionEventLogService(session)
        self._jobs = BackgroundJobService(session)
        self._beat_sheet_generation = (
            beat_sheet_generation_service or BeatSheetGenerationService()
        )
        self._character_generation = (
            character_generation_service or CharacterGenerationService()
        )
        self._pitch_generation = pitch_generation_service or PitchGenerationService()

    def enqueue(
        self,
        *,
        tool_name: StoryWorkflowToolName | str,
        session_id: str,
        arguments: dict[str, Any] | None = None,
    ) -> BackgroundJobRecord:
        definition = self._registry.get(tool_name)
        validated = self._registry.validate_arguments(definition.name, arguments)
        self._sessions.load_session_snapshot(session_id)
        return self._jobs.enqueue_job(
            job_type=definition.job_type,
            payload=validated.model_dump(mode="json", exclude_none=True),
            session_id=session_id,
        )

    def execute(
        self,
        *,
        tool_name: StoryWorkflowToolName | str,
        session_id: str,
        arguments: dict[str, Any] | None = None,
        actor: SessionEventActor | None = None,
    ) -> StoryWorkflowToolResultBase:
        definition = self._registry.get(tool_name)
        validated = self._registry.validate_arguments(definition.name, arguments)
        executor = getattr(self, definition.executor_name)
        return executor(session_id=session_id, request=validated, actor=actor)

    def _generate_pitches(
        self,
        *,
        session_id: str,
        request: GeneratePitchesToolInput,
        actor: SessionEventActor | None = None,
    ) -> StageOperationToolResult:
        response = self._sessions.generate_pitches(
            session_id,
            candidate_count=request.candidate_count,
            guidance=request.guidance,
            preserve_selected_pitch=request.preserve_selected_pitch,
            actor=actor,
            pitch_generation_service=self._pitch_generation,
        )
        snapshot = response.snapshot
        detail = _join_detail_parts(
            [
                snapshot.stage_states[WORKFLOW_STAGE_SEQUENCE.index(WorkflowStage.PITCHES)].detail,
                _optional_detail("Guidance", request.guidance),
                (
                    "Preserving the current selected pitch."
                    if request.preserve_selected_pitch
                    else None
                ),
            ]
        )
        return StageOperationToolResult(
            tool_name=StoryWorkflowToolName.GENERATE_PITCHES,
            stage=WorkflowStage.PITCHES,
            summary="Generated a fresh pitch batch from the current bedtime brief.",
            stage_status=_stage_status(snapshot, WorkflowStage.PITCHES),
            detail=detail,
        )

    def _refine_pitch(
        self,
        *,
        session_id: str,
        request: RefinePitchToolInput,
        actor: SessionEventActor | None = None,
    ) -> StageOperationToolResult:
        response = self._sessions.refine_pitch(
            session_id,
            pitch_id=request.pitch_id,
            generation_key=request.generation_key,
            pitch_index=request.pitch_index,
            title=request.title,
            instructions=request.instructions,
            origin="story_tool",
            actor=actor,
            pitch_generation_service=self._pitch_generation,
        )
        snapshot = response.snapshot
        detail = snapshot.stage_states[WORKFLOW_STAGE_SEQUENCE.index(WorkflowStage.PITCHES)].detail
        return StageOperationToolResult(
            tool_name=StoryWorkflowToolName.REFINE_PITCH,
            stage=WorkflowStage.PITCHES,
            summary="Generated and selected a refined pitch.",
            stage_status=_stage_status(snapshot, WorkflowStage.PITCHES),
            detail=detail,
        )

    def _generate_character_sheets(
        self,
        *,
        session_id: str,
        request: GenerateCharacterSheetsToolInput,
        actor: SessionEventActor | None = None,
    ) -> StageOperationToolResult:
        response = self._sessions.generate_character_sheets(
            session_id,
            candidate_count=3,
            guidance=request.guidance,
            origin="story_tool",
            actor=actor,
            character_generation_service=self._character_generation,
        )
        snapshot = response.snapshot
        detail = snapshot.stage_states[
            WORKFLOW_STAGE_SEQUENCE.index(WorkflowStage.CHARACTERS)
        ].detail
        return StageOperationToolResult(
            tool_name=StoryWorkflowToolName.GENERATE_CHARACTER_SHEETS,
            stage=WorkflowStage.CHARACTERS,
            summary="Generated a fresh character-sheet batch from the selected pitch.",
            stage_status=_stage_status(snapshot, WorkflowStage.CHARACTERS),
            detail=detail,
        )

    def _refine_character_sheet(
        self,
        *,
        session_id: str,
        request: RefineCharacterSheetToolInput,
        actor: SessionEventActor | None = None,
    ) -> StageOperationToolResult:
        response = self._sessions.refine_character_sheet(
            session_id,
            character_sheet_id=request.character_sheet_id,
            revision_number=request.revision_number,
            title=request.title,
            instructions=request.instructions,
            focus_character_names=request.focus_character_names,
            change_summary=request.change_summary,
            change_impact=request.change_impact,
            origin="story_tool",
            actor=actor,
            character_generation_service=self._character_generation,
        )
        snapshot = response.snapshot
        detail = snapshot.stage_states[
            WORKFLOW_STAGE_SEQUENCE.index(WorkflowStage.CHARACTERS)
        ].detail
        return StageOperationToolResult(
            tool_name=StoryWorkflowToolName.REFINE_CHARACTER_SHEET,
            stage=WorkflowStage.CHARACTERS,
            summary="Generated and selected a refined character sheet.",
            stage_status=_stage_status(snapshot, WorkflowStage.CHARACTERS),
            detail=detail,
        )

    def _generate_beat_sheet(
        self,
        *,
        session_id: str,
        request: GenerateBeatSheetToolInput,
        actor: SessionEventActor | None = None,
    ) -> StageOperationToolResult:
        if request.instructions is not None:
            response = self._sessions.refine_beat_sheet(
                session_id,
                instructions=request.instructions,
                beat_names=request.focus_beats,
                bedtime_goal=request.bedtime_goal,
                origin="story_tool",
                actor=actor,
                beat_sheet_generation_service=self._beat_sheet_generation,
            )
            snapshot = response.snapshot
            detail = snapshot.stage_states[
                WORKFLOW_STAGE_SEQUENCE.index(WorkflowStage.BEATS)
            ].detail
            return StageOperationToolResult(
                tool_name=StoryWorkflowToolName.GENERATE_BEAT_SHEET,
                stage=WorkflowStage.BEATS,
                summary="Generated and selected a refined beat-sheet revision.",
                stage_status=_stage_status(snapshot, WorkflowStage.BEATS),
                detail=detail,
            )

        response = self._sessions.generate_beat_sheet(
            session_id,
            guidance=request.guidance,
            focus_beats=request.focus_beats,
            bedtime_goal=request.bedtime_goal,
            origin="story_tool",
            actor=actor,
            beat_sheet_generation_service=self._beat_sheet_generation,
        )
        snapshot = response.snapshot
        detail = snapshot.stage_states[
            WORKFLOW_STAGE_SEQUENCE.index(WorkflowStage.BEATS)
        ].detail
        return StageOperationToolResult(
            tool_name=StoryWorkflowToolName.GENERATE_BEAT_SHEET,
            stage=WorkflowStage.BEATS,
            summary="Generated a fresh beat-sheet revision from the current character plan.",
            stage_status=_stage_status(snapshot, WorkflowStage.BEATS),
            detail=detail,
        )

    def _update_setup_heuristics(
        self,
        *,
        session_id: str,
        request: UpdateSetupHeuristicsToolInput,
        actor: SessionEventActor | None = None,
    ) -> UpdateSetupHeuristicsToolResult:
        snapshot = self._sessions.load_session_snapshot(session_id)
        if snapshot.selected_beat_sheet is None:
            raise StoryWorkflowToolServiceError(
                "update_setup_heuristics requires a selected beat sheet",
            )

        current_setup = self._get_selected_story_setup_row(session_id)
        provided_fields = request.model_fields_set
        merged_values = {
            "target_word_count": request.target_word_count
            if "target_word_count" in provided_fields
            else getattr(current_setup, "target_word_count", None),
            "target_runtime_minutes": request.target_runtime_minutes
            if "target_runtime_minutes" in provided_fields
            else getattr(current_setup, "target_runtime_minutes", None),
            "chapter_count": request.chapter_count
            if "chapter_count" in provided_fields
            else getattr(current_setup, "chapter_count", None),
            "approximate_scene_count": request.approximate_scene_count
            if "approximate_scene_count" in provided_fields
            else getattr(current_setup, "approximate_scene_count", None),
            "chapter_style": request.chapter_style
            if "chapter_style" in provided_fields
            else getattr(current_setup, "chapter_style", None),
            "guidance_notes": request.guidance_notes
            if "guidance_notes" in provided_fields
            else getattr(current_setup, "guidance_notes", None),
        }

        if current_setup is not None and _story_setup_matches(current_setup, merged_values):
            return UpdateSetupHeuristicsToolResult(
                tool_name=StoryWorkflowToolName.UPDATE_SETUP_HEURISTICS,
                stage=WorkflowStage.STORY_SETUP,
                summary="Story setup heuristics already match the requested values.",
                stage_status=_stage_status(snapshot, WorkflowStage.STORY_SETUP),
                story_setup_id=current_setup.id,
                revision_number=current_setup.revision_number,
            )

        self._cancel_active_composition_jobs(
            session_id,
            reason="Cancelled because story setup heuristics changed.",
        )
        self._cancel_active_audio_jobs(
            session_id,
            reason="Cancelled because story setup heuristics changed.",
        )
        previous_selection_id = current_setup.id if current_setup is not None else None
        if current_setup is not None:
            current_setup.is_selected = False

        setup = StorySetup(
            session_id=session_id,
            beat_sheet_id=snapshot.selected_beat_sheet.id,
            revision_number=self._next_revision_number(StorySetup, session_id),
            target_word_count=merged_values["target_word_count"],
            target_runtime_minutes=merged_values["target_runtime_minutes"],
            chapter_count=merged_values["chapter_count"],
            approximate_scene_count=merged_values["approximate_scene_count"],
            chapter_style=merged_values["chapter_style"],
            guidance_notes=merged_values["guidance_notes"],
            preferences={
                "source": request.origin,
            },
            is_selected=True,
            accepted_at=utc_now(),
        )
        self._session.add(setup)
        self._session.flush()

        changed_fields = sorted(
            field
            for field in provided_fields
            if field != "origin"
        )
        self._events.record_user_edit(
            session_id,
            target_kind=UserEditTargetKind.STORY_SETUP,
            stage=WorkflowStage.STORY_SETUP,
            target_id=setup.id,
            revision_number=setup.revision_number,
            changed_fields=changed_fields,
            source=request.origin,
            field_values=request.model_dump(mode="json", exclude_unset=True),
            summary_text="Updated story setup preferences.",
            actor=actor,
        )
        self._events.record_selection(
            session_id,
            selection_kind=SelectionKind.STORY_SETUP,
            stage=WorkflowStage.STORY_SETUP,
            selection_id=setup.id,
            label=_story_setup_label(setup),
            previous_selection_id=previous_selection_id,
            source=request.origin,
            actor=actor,
        )
        stage_snapshot = self._sessions.update_stage_state(
            session_id,
            stage=WorkflowStage.STORY_SETUP,
            status=WorkflowStageState.COMPLETED,
            detail=_story_setup_label(setup),
            actor=actor,
        )
        return UpdateSetupHeuristicsToolResult(
            tool_name=StoryWorkflowToolName.UPDATE_SETUP_HEURISTICS,
            stage=WorkflowStage.STORY_SETUP,
            summary="Saved a new story-setup heuristic revision.",
            stage_status=_stage_status(stage_snapshot, WorkflowStage.STORY_SETUP),
            story_setup_id=setup.id,
            revision_number=setup.revision_number,
        )

    def _compose_next_segment(
        self,
        *,
        session_id: str,
        request: ComposeNextSegmentToolInput,
        actor: SessionEventActor | None = None,
    ) -> CompositionToolResult:
        snapshot = self._sessions.load_session_snapshot(session_id)
        if snapshot.selected_story_setup is None:
            raise StoryWorkflowToolServiceError(
                "compose_next_segment requires a selected story setup",
            )
        if snapshot.selected_beat_sheet is None:
            raise StoryWorkflowToolServiceError(
                "compose_next_segment requires a selected beat sheet",
            )

        self._cancel_active_composition_jobs(
            session_id,
            reason="Cancelled because a new composition pass started.",
        )
        next_segment_index = request.restart_from_segment_index or self._next_segment_index(
            session_id
        )
        job = CompositionJob(
            session_id=session_id,
            beat_sheet_id=snapshot.selected_beat_sheet.id,
            story_setup_id=snapshot.selected_story_setup.id,
            job_kind=CompositionJobKind.DRAFT,
            status=JobStatus.IN_PROGRESS,
            progress_percent=0,
            current_segment_index=next_segment_index,
            metadata_json=request.model_dump(mode="json", exclude_none=True),
            started_at=utc_now(),
        )
        self._session.add(job)
        self._session.flush()

        segment = CompositionSegment(
            session_id=session_id,
            composition_job_id=job.id,
            segment_index=next_segment_index,
            revision_number=self._next_segment_revision(session_id, next_segment_index),
            status=JobStatus.IN_PROGRESS,
            planned_summary=request.instructions,
            payload=request.model_dump(mode="json", exclude_none=True),
        )
        self._session.add(segment)
        self._session.flush()

        self._events.record_composition_progress(
            session_id,
            job_id=job.id,
            status=job.status,
            progress_percent=0,
            current_segment_index=next_segment_index,
            total_segments=None,
            segment_id=segment.id,
            actor=actor or DEFAULT_SYSTEM_ACTOR,
        )
        stage_snapshot = self._transition_stage_to_in_progress(
            session_id,
            stage=WorkflowStage.COMPOSITION,
            detail=_join_detail_parts(
                [
                    f"Composing segment {next_segment_index}.",
                    _optional_detail("Instructions", request.instructions),
                ]
            ),
            actor=actor,
        )
        return CompositionToolResult(
            tool_name=StoryWorkflowToolName.COMPOSE_NEXT_SEGMENT,
            stage=WorkflowStage.COMPOSITION,
            summary="Created the next composition job and seeded its segment.",
            stage_status=_stage_status(stage_snapshot, WorkflowStage.COMPOSITION),
            composition_job_id=job.id,
            segment_id=segment.id,
            segment_index=segment.segment_index,
        )

    def _rewrite_segments(
        self,
        *,
        session_id: str,
        request: RewriteSegmentsToolInput,
        actor: SessionEventActor | None = None,
    ) -> CompositionToolResult:
        snapshot = self._sessions.load_session_snapshot(session_id)
        if snapshot.selected_story_setup is None:
            raise StoryWorkflowToolServiceError(
                "rewrite_segments requires a selected story setup",
            )
        if snapshot.selected_beat_sheet is None:
            raise StoryWorkflowToolServiceError(
                "rewrite_segments requires a selected beat sheet",
            )

        self._cancel_active_composition_jobs(
            session_id,
            reason="Cancelled because a rewrite pass started.",
        )
        job = CompositionJob(
            session_id=session_id,
            beat_sheet_id=snapshot.selected_beat_sheet.id,
            story_setup_id=snapshot.selected_story_setup.id,
            job_kind=CompositionJobKind.REWRITE,
            status=JobStatus.IN_PROGRESS,
            progress_percent=0,
            current_segment_index=request.rewrite_from_segment_index,
            metadata_json=request.model_dump(mode="json", exclude_none=True),
            started_at=utc_now(),
        )
        self._session.add(job)
        self._session.flush()

        segment = CompositionSegment(
            session_id=session_id,
            composition_job_id=job.id,
            segment_index=request.rewrite_from_segment_index,
            revision_number=self._next_segment_revision(
                session_id,
                request.rewrite_from_segment_index,
            ),
            status=JobStatus.IN_PROGRESS,
            planned_summary=request.instructions,
            payload=request.model_dump(mode="json", exclude_none=True),
        )
        self._session.add(segment)
        self._session.flush()

        self._events.record_composition_progress(
            session_id,
            job_id=job.id,
            status=job.status,
            progress_percent=0,
            current_segment_index=request.rewrite_from_segment_index,
            total_segments=None,
            segment_id=segment.id,
            actor=actor or DEFAULT_SYSTEM_ACTOR,
        )
        stage_snapshot = self._transition_stage_to_in_progress(
            session_id,
            stage=WorkflowStage.COMPOSITION,
            detail=_join_detail_parts(
                [
                    f"Rewriting from segment {request.rewrite_from_segment_index}.",
                    _optional_detail("Instructions", request.instructions),
                ]
            ),
            actor=actor,
        )
        return CompositionToolResult(
            tool_name=StoryWorkflowToolName.REWRITE_SEGMENTS,
            stage=WorkflowStage.COMPOSITION,
            summary="Created a rewrite job and seeded the revised segment.",
            stage_status=_stage_status(stage_snapshot, WorkflowStage.COMPOSITION),
            composition_job_id=job.id,
            segment_id=segment.id,
            segment_index=segment.segment_index,
        )

    def _estimate_audio_length(
        self,
        *,
        session_id: str,
        request: EstimateAudioLengthToolInput,
        actor: SessionEventActor | None = None,
    ) -> EstimateAudioLengthToolResult:
        del actor
        self._sessions.load_session_snapshot(session_id)
        word_count, source = self._estimate_word_count(session_id, request)
        estimated_seconds = _estimate_duration_seconds(
            word_count,
            playback_speed=request.playback_speed,
        )
        return EstimateAudioLengthToolResult(
            tool_name=StoryWorkflowToolName.ESTIMATE_AUDIO_LENGTH,
            stage=WorkflowStage.AUDIO,
            summary="Estimated narration duration from the current story material.",
            estimated_duration_seconds=estimated_seconds,
            estimated_word_count=word_count,
            playback_speed=request.playback_speed,
            basis_source=source,
        )

    def _start_audio_generation(
        self,
        *,
        session_id: str,
        request: StartAudioGenerationToolInput,
        actor: SessionEventActor | None = None,
    ) -> StartAudioGenerationToolResult:
        self._sessions.load_session_snapshot(session_id)
        self._cancel_active_audio_jobs(
            session_id,
            reason="Cancelled because a new audio generation run started.",
        )
        estimate = self._estimate_audio_length(
            session_id=session_id,
            request=EstimateAudioLengthToolInput(
                playback_speed=request.playback_speed,
                voice_key=request.voice_key,
            ),
            actor=actor,
        )
        job = AudioJob(
            session_id=session_id,
            source_composition_job_id=self._latest_composition_job_id(session_id),
            status=JobStatus.IN_PROGRESS,
            voice_key=request.voice_key,
            playback_speed=request.playback_speed,
            include_background_music=request.include_background_music,
            music_profile=request.music_profile,
            estimated_duration_seconds=estimate.estimated_duration_seconds,
            current_segment_index=1,
            config_json=request.model_dump(mode="json", exclude_none=True),
            started_at=utc_now(),
        )
        self._session.add(job)
        self._session.flush()

        self._events.record_audio_progress(
            session_id,
            job_id=job.id,
            status=job.status,
            progress_percent=0,
            current_segment_index=job.current_segment_index,
            total_segments=None,
            estimated_duration_seconds=job.estimated_duration_seconds,
            voice_key=job.voice_key,
            actor=actor or DEFAULT_SYSTEM_ACTOR,
        )
        stage_snapshot = self._transition_stage_to_in_progress(
            session_id,
            stage=WorkflowStage.AUDIO,
            detail=_join_detail_parts(
                [
                    "Starting audio generation.",
                    _optional_detail("Voice", request.voice_key),
                    f"Playback speed {request.playback_speed:g}x.",
                    "Background music enabled." if request.include_background_music else None,
                ]
            ),
            actor=actor,
        )
        return StartAudioGenerationToolResult(
            tool_name=StoryWorkflowToolName.START_AUDIO_GENERATION,
            stage=WorkflowStage.AUDIO,
            summary="Created a new audio job from the current story draft.",
            stage_status=_stage_status(stage_snapshot, WorkflowStage.AUDIO),
            audio_job_id=job.id,
            estimated_duration_seconds=estimate.estimated_duration_seconds,
        )

    def _transition_stage_to_in_progress(
        self,
        session_id: str,
        *,
        stage: WorkflowStage,
        detail: str | None,
        actor: SessionEventActor | None = None,
    ):
        snapshot = self._sessions.load_session_snapshot(session_id)
        current_status = _stage_status(snapshot, stage)
        current_detail = _stage_detail(snapshot, stage)

        if current_status == WorkflowStageState.IN_PROGRESS and current_detail == detail:
            return snapshot

        if current_status == WorkflowStageState.COMPLETED:
            self._sessions.update_stage_state(
                session_id,
                stage=stage,
                status=WorkflowStageState.NEEDS_REGENERATION,
                detail=detail,
                actor=actor,
            )

        return self._sessions.update_stage_state(
            session_id,
            stage=stage,
            status=WorkflowStageState.IN_PROGRESS,
            detail=detail,
            actor=actor,
        )

    def _get_selected_story_setup_row(self, session_id: str) -> StorySetup | None:
        stmt: Select[tuple[StorySetup]] = (
            select(StorySetup)
            .where(StorySetup.session_id == session_id, StorySetup.is_selected.is_(True))
            .order_by(StorySetup.revision_number.desc())
            .limit(1)
        )
        return self._session.execute(stmt).scalar_one_or_none()

    def _latest_composition_job_id(self, session_id: str) -> str | None:
        stmt: Select[tuple[CompositionJob]] = (
            select(CompositionJob)
            .where(CompositionJob.session_id == session_id)
            .order_by(CompositionJob.created_at.desc())
            .limit(1)
        )
        row = self._session.execute(stmt).scalar_one_or_none()
        return row.id if row is not None else None

    def _next_revision_number(self, model_cls, session_id: str) -> int:
        stmt = select(func.max(model_cls.revision_number)).where(model_cls.session_id == session_id)
        current = self._session.execute(stmt).scalar_one_or_none() or 0
        return int(current) + 1

    def _next_segment_index(self, session_id: str) -> int:
        stmt = select(func.max(CompositionSegment.segment_index)).where(
            CompositionSegment.session_id == session_id
        )
        current = self._session.execute(stmt).scalar_one_or_none() or 0
        return int(current) + 1

    def _next_segment_revision(self, session_id: str, segment_index: int) -> int:
        stmt = select(func.max(CompositionSegment.revision_number)).where(
            CompositionSegment.session_id == session_id,
            CompositionSegment.segment_index == segment_index,
        )
        current = self._session.execute(stmt).scalar_one_or_none() or 0
        return int(current) + 1

    def _estimate_word_count(
        self,
        session_id: str,
        request: EstimateAudioLengthToolInput,
    ) -> tuple[int, AudioLengthEstimateSource]:
        if request.word_count_override is not None:
            return request.word_count_override, AudioLengthEstimateSource.REQUEST_OVERRIDE

        stmt = select(CompositionSegment).where(CompositionSegment.session_id == session_id)
        segments = list(self._session.execute(stmt).scalars().all())
        total_words = 0
        for segment in segments:
            if segment.word_count is not None:
                total_words += segment.word_count
                continue
            if segment.text_content:
                total_words += len(segment.text_content.split())

        if total_words > 0:
            return total_words, AudioLengthEstimateSource.COMPOSITION_SEGMENTS

        snapshot = self._sessions.load_session_snapshot(session_id)
        if (
            snapshot.selected_story_setup is not None
            and snapshot.selected_story_setup.target_word_count is not None
        ):
            return (
                snapshot.selected_story_setup.target_word_count,
                AudioLengthEstimateSource.STORY_SETUP_TARGET,
            )

        return 0, AudioLengthEstimateSource.UNKNOWN

    def _cancel_active_composition_jobs(self, session_id: str, *, reason: str) -> None:
        stmt = select(CompositionJob).where(
            CompositionJob.session_id == session_id,
            CompositionJob.status.in_((JobStatus.QUEUED, JobStatus.IN_PROGRESS, JobStatus.PAUSED)),
        )
        for row in self._session.execute(stmt).scalars().all():
            row.status = JobStatus.CANCELLED
            row.stop_reason = reason
            row.completed_at = row.completed_at or utc_now()

    def _cancel_active_audio_jobs(self, session_id: str, *, reason: str) -> None:
        stmt = select(AudioJob).where(
            AudioJob.session_id == session_id,
            AudioJob.status.in_((JobStatus.QUEUED, JobStatus.IN_PROGRESS, JobStatus.PAUSED)),
        )
        for row in self._session.execute(stmt).scalars().all():
            row.status = JobStatus.CANCELLED
            row.stop_reason = reason
            row.completed_at = row.completed_at or utc_now()

    def _require_pitch(
        self,
        session_id: str,
        request: RefinePitchToolInput,
    ) -> Pitch:
        stmt = select(Pitch).where(Pitch.session_id == session_id)
        if request.pitch_id is not None:
            stmt = stmt.where(Pitch.id == request.pitch_id)
        if request.generation_key is not None:
            stmt = stmt.where(Pitch.generation_key == request.generation_key)
        if request.pitch_index is not None:
            stmt = stmt.where(Pitch.pitch_index == request.pitch_index)
        if request.title is not None:
            stmt = stmt.where(Pitch.title == request.title)
        pitch = self._session.execute(stmt.limit(1)).scalar_one_or_none()
        if pitch is None:
            raise StoryWorkflowToolServiceError("refine_pitch requires a matching pitch in session")
        return pitch

    def _require_character_sheet(
        self,
        *,
        session_id: str,
        character_sheet_id: str | None,
        revision_number: int | None,
    ) -> CharacterSheet:
        stmt = select(CharacterSheet).where(CharacterSheet.session_id == session_id)
        if character_sheet_id is not None:
            stmt = stmt.where(CharacterSheet.id == character_sheet_id)
        if revision_number is not None:
            stmt = stmt.where(CharacterSheet.revision_number == revision_number)
        if character_sheet_id is None and revision_number is None:
            stmt = stmt.where(CharacterSheet.is_selected.is_(True))
        ordered_stmt = stmt.order_by(CharacterSheet.revision_number.desc()).limit(1)
        sheet = self._session.execute(ordered_stmt).scalar_one_or_none()
        if sheet is None:
            raise StoryWorkflowToolServiceError(
                "refine_character_sheet requires a matching character sheet in session",
            )
        return sheet


def _side_effect(
    kind: StoryWorkflowToolSideEffectKind,
    summary: str,
    *,
    stages: list[WorkflowStage],
    writes_to: list[str],
) -> StoryWorkflowToolSideEffect:
    return StoryWorkflowToolSideEffect(
        kind=kind,
        summary=summary,
        stages=stages,
        writes_to=writes_to,
    )


def _estimate_duration_seconds(word_count: int, *, playback_speed: float) -> int:
    return estimate_narration_duration_seconds(
        word_count,
        playback_speed=playback_speed,
    )


def _stage_status(snapshot, stage: WorkflowStage) -> WorkflowStageState:
    for row in snapshot.stage_states:
        if row.stage == stage:
            return row.status
    raise SessionNotFoundError(f"session {snapshot.id!r} is missing stage state for {stage.value}")


def _stage_detail(snapshot, stage: WorkflowStage) -> str | None:
    for row in snapshot.stage_states:
        if row.stage == stage:
            return row.detail
    return None


def _join_detail_parts(parts: list[str | None]) -> str | None:
    normalized = [part.strip() for part in parts if part and part.strip()]
    if not normalized:
        return None
    return " ".join(normalized)


def _optional_detail(label: str, value: str | None) -> str | None:
    if value is None:
        return None
    normalized = value.strip()
    if not normalized:
        return None
    return f"{label}: {normalized}"


def _story_setup_label(row: StorySetup) -> str:
    parts: list[str] = []
    if row.target_runtime_minutes is not None:
        parts.append(f"~{row.target_runtime_minutes} minutes")
    if row.target_word_count is not None:
        parts.append(f"{row.target_word_count} words")
    if row.chapter_count is not None:
        parts.append(f"{row.chapter_count} chapters")
    if row.approximate_scene_count is not None:
        parts.append(f"about {row.approximate_scene_count} scenes")
    if row.chapter_style:
        parts.append(row.chapter_style)
    if row.guidance_notes:
        parts.append(row.guidance_notes)
    return ", ".join(parts) if parts else "Story setup preferences"


def _story_setup_matches(current: StorySetup, merged_values: dict[str, Any]) -> bool:
    return (
        current.target_word_count == merged_values["target_word_count"]
        and current.target_runtime_minutes == merged_values["target_runtime_minutes"]
        and current.chapter_count == merged_values["chapter_count"]
        and current.approximate_scene_count == merged_values["approximate_scene_count"]
        and current.chapter_style == merged_values["chapter_style"]
        and current.guidance_notes == merged_values["guidance_notes"]
    )

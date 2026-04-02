from __future__ import annotations

from collections.abc import Mapping
from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.models.action_policy import SessionActionPolicyEvaluation
from app.models.chat_actions import (
    CHAT_TO_UI_ACTION_SCHEMA_VERSION,
    ChatToUIActionBatch,
    ChatToUIActionType,
    ChatToUIJobKind,
)
from app.models.workflow import WorkflowStage, WorkflowStageState

INTENT_PARSER_SCHEMA_VERSION = 1
INTENT_PARSER_PROMPT_VERSION = "intent_parser.v2"
EXPLICIT_CHAT_COMMAND_PROMPT_VERSION = "explicit_command.v1"
EXPLICIT_CHAT_COMMAND_MODEL_ID = "deterministic-command-map"


class IntentParserStatus(str, Enum):
    PARSED = "parsed"
    NEEDS_CLARIFICATION = "needs_clarification"
    FAILED = "failed"


class ExplicitChatCommandId(str, Enum):
    NEXT_STAGE = "next_stage"
    SUMMARIZE_PLAN = "summarize_plan"
    REGENERATE_PITCHES = "regenerate_pitches"
    PAUSE_WRITING = "pause_writing"
    RESUME_WRITING = "resume_writing"


class ExplicitChatCommandSource(str, Enum):
    SLASH_COMMAND = "slash_command"
    QUICK_ACTION = "quick_action"


class ExplicitChatCommandRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    command_id: ExplicitChatCommandId
    source: ExplicitChatCommandSource
    proposed_actions: ChatToUIActionBatch = Field(default_factory=ChatToUIActionBatch)

    @model_validator(mode="after")
    def validate_command_matches_action_batch(self) -> "ExplicitChatCommandRequest":
        actions = self.proposed_actions.actions

        if self.command_id == ExplicitChatCommandId.SUMMARIZE_PLAN:
            if actions:
                raise ValueError("summarize_plan must not include proposed actions")
            return self

        if self.command_id == ExplicitChatCommandId.NEXT_STAGE:
            if len(actions) > 1:
                raise ValueError("next_stage supports at most one proposed action")
            if actions and actions[0].action_type != ChatToUIActionType.NAVIGATE_TO_STAGE:
                raise ValueError("next_stage must propose a navigate_to_stage action")
            return self

        if len(actions) != 1:
            raise ValueError(f"{self.command_id.value} requires exactly one proposed action")

        action = actions[0]
        if self.command_id == ExplicitChatCommandId.REGENERATE_PITCHES:
            if action.action_type != ChatToUIActionType.REGENERATE_PITCHES:
                raise ValueError(
                    "regenerate_pitches must propose a regenerate_pitches action",
                )
            return self

        if self.command_id == ExplicitChatCommandId.PAUSE_WRITING:
            if (
                action.action_type != ChatToUIActionType.PAUSE_JOB
                or action.extracted_values.job_kind != ChatToUIJobKind.COMPOSITION
            ):
                raise ValueError(
                    "pause_writing must propose a composition pause_job action",
                )
            return self

        if self.command_id == ExplicitChatCommandId.RESUME_WRITING:
            if (
                action.action_type != ChatToUIActionType.RESUME_JOB
                or action.extracted_values.job_kind != ChatToUIJobKind.COMPOSITION
            ):
                raise ValueError(
                    "resume_writing must propose a composition resume_job action",
                )
            return self

        return self


class ParseChatIntentRequest(BaseModel):
    message: str = Field(min_length=1)
    explicit_command: ExplicitChatCommandRequest | None = None

    @field_validator("message")
    @classmethod
    def validate_message(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("message must not be empty")
        return normalized


class IntentParserStageContext(BaseModel):
    current_stage: WorkflowStage
    current_stage_label: str
    current_stage_description: str
    current_stage_status: WorkflowStageState
    current_stage_detail: str | None = None


class IntentParserPromptContext(BaseModel):
    session_id: str
    display_title: str
    overall_status: WorkflowStageState
    resume_stage: WorkflowStage
    stage_context: IntentParserStageContext
    session_summary: str
    user_message: str = Field(min_length=1)

    @field_validator("user_message")
    @classmethod
    def validate_user_message(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("user_message must not be empty")
        return normalized


class IntentParserCandidateAction(BaseModel):
    model_config = ConfigDict(extra="forbid")

    action_type: ChatToUIActionType
    target_stage: WorkflowStage
    confidence: float = Field(ge=0, le=1)
    rationale: str | None = None
    requires_confirmation: bool
    extracted_values: dict[str, Any] = Field(default_factory=dict)


class IntentParserCandidateActionBatch(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: int = Field(default=CHAT_TO_UI_ACTION_SCHEMA_VERSION, ge=1)
    actions: list[IntentParserCandidateAction] = Field(default_factory=list)


class IntentParserStructuredOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: int = Field(default=INTENT_PARSER_SCHEMA_VERSION, ge=1)
    status: IntentParserStatus = IntentParserStatus.PARSED
    needs_clarification: bool = False
    assistant_response: str = Field(min_length=1)
    clarification_reason: str | None = None
    proposed_actions: IntentParserCandidateActionBatch = Field(
        default_factory=IntentParserCandidateActionBatch
    )

    @model_validator(mode="after")
    def validate_status_requirements(self) -> IntentParserStructuredOutput:
        if self.needs_clarification and self.status == IntentParserStatus.PARSED:
            self.status = IntentParserStatus.NEEDS_CLARIFICATION

        if self.status == IntentParserStatus.NEEDS_CLARIFICATION:
            self.needs_clarification = True
            if self.clarification_reason is None or not self.clarification_reason.strip():
                raise ValueError(
                    "clarification_reason is required when status is needs_clarification",
                )
            if self.proposed_actions.actions:
                raise ValueError(
                    "proposed_actions must be empty when clarification is still required",
                )

        if self.status == IntentParserStatus.FAILED:
            self.needs_clarification = False
            if self.proposed_actions.actions:
                raise ValueError("proposed_actions must be empty when status is failed")

        return self


class ParsedChatIntentResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: int = Field(default=INTENT_PARSER_SCHEMA_VERSION, ge=1)
    status: IntentParserStatus = IntentParserStatus.PARSED
    needs_clarification: bool = False
    assistant_response: str = Field(min_length=1)
    clarification_reason: str | None = None
    proposed_actions: ChatToUIActionBatch = Field(default_factory=ChatToUIActionBatch)
    policy_evaluation: SessionActionPolicyEvaluation | None = None

    @model_validator(mode="after")
    def validate_status_requirements(self) -> ParsedChatIntentResponse:
        if self.needs_clarification and self.status == IntentParserStatus.PARSED:
            self.status = IntentParserStatus.NEEDS_CLARIFICATION

        if self.status == IntentParserStatus.NEEDS_CLARIFICATION:
            self.needs_clarification = True
            if self.clarification_reason is None or not self.clarification_reason.strip():
                raise ValueError(
                    "clarification_reason is required when status is needs_clarification",
                )
            if self.proposed_actions.actions:
                raise ValueError(
                    "proposed_actions must be empty when clarification is still required",
                )

        if self.status == IntentParserStatus.FAILED:
            self.needs_clarification = False
            if self.proposed_actions.actions:
                raise ValueError("proposed_actions must be empty when status is failed")

        return self


class IntentParserInvocation(BaseModel):
    model_config = ConfigDict(extra="forbid")

    prompt_version: str = INTENT_PARSER_PROMPT_VERSION
    model_id: str
    context: IntentParserPromptContext
    rendered_prompt: str = Field(min_length=1)


class IntentParserInvocationResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    invocation: IntentParserInvocation
    structured_output: IntentParserStructuredOutput
    raw_response: Mapping[str, Any] | list[Any] | str | None = None

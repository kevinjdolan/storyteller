from __future__ import annotations

from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.ai import (
    IntentParserAdapter,
    IntentParserTransportError,
    build_intent_parser_invocation,
)
from app.models import (
    EXPLICIT_CHAT_COMMAND_MODEL_ID,
    EXPLICIT_CHAT_COMMAND_PROMPT_VERSION,
    ChatMessageRole,
    ChatToUIActionBatch,
    ExplicitChatCommandId,
    ExplicitChatCommandRequest,
    IntentParserPromptContext,
    IntentParserStageContext,
    IntentParserStatus,
    IntentParserStructuredOutput,
    ParsedChatIntentResponse,
    SessionSnapshot,
    WorkflowStage,
    build_action_policy_request_from_batch,
    get_workflow_stage_definition,
)
from app.services.action_policy import SessionActionPolicyService
from app.services.agent_context import build_session_agent_context_summary
from app.services.event_log import SessionEventLogService
from app.services.sessions import SessionNotFoundError, SessionService


class SessionIntentParserService:
    def __init__(self, session: Session, parser: IntentParserAdapter | None = None):
        self._session = session
        self._parser = parser
        self._sessions = SessionService(session)
        self._event_log = SessionEventLogService(session)

    def parse_user_message(
        self,
        session_id: str,
        *,
        message: str,
        explicit_command: ExplicitChatCommandRequest | None = None,
    ) -> ParsedChatIntentResponse:
        normalized_message = message.strip()
        if not normalized_message:
            raise ValueError("message must not be empty")

        snapshot = self._sessions.load_session_snapshot(session_id)
        context = _build_prompt_context(snapshot, normalized_message)

        self._event_log.record_chat_message(
            session_id,
            message_role=ChatMessageRole.USER,
            content=normalized_message,
            stage=context.stage_context.current_stage,
        )
        self._session.commit()

        raw_response = None
        prompt_version: str
        model_id: str
        rendered_prompt: str

        if explicit_command is not None:
            result = _build_explicit_command_result(
                snapshot,
                explicit_command=explicit_command,
            )
            prompt_version = EXPLICIT_CHAT_COMMAND_PROMPT_VERSION
            model_id = EXPLICIT_CHAT_COMMAND_MODEL_ID
            rendered_prompt = _build_explicit_command_audit_prompt(
                message=normalized_message,
                explicit_command=explicit_command,
            )
            raw_response = explicit_command.model_dump(mode="json")
        else:
            if self._parser is None:
                raise RuntimeError("intent parser adapter is required for free-form chat parsing")

            invocation = build_intent_parser_invocation(
                context,
                model_id=self._parser.model_id,
            )
            prompt_version = invocation.prompt_version
            model_id = invocation.model_id
            rendered_prompt = invocation.rendered_prompt

            try:
                invocation_result = self._parser.parse(invocation)
                raw_response = invocation_result.raw_response
                result = _normalize_parser_output(invocation_result.structured_output)
            except (IntentParserTransportError, ValidationError):
                result = _build_failed_result()

        if result.status == IntentParserStatus.PARSED and result.proposed_actions.actions:
            result.policy_evaluation = SessionActionPolicyService(
                self._session
            ).evaluate_request_against_snapshot(
                snapshot,
                request=build_action_policy_request_from_batch(result.proposed_actions),
            )
        else:
            result.policy_evaluation = None

        self._event_log.record_chat_intent_parsed(
            session_id,
            prompt_version=prompt_version,
            model_id=model_id,
            current_stage=context.stage_context.current_stage,
            stage_label=context.stage_context.current_stage_label,
            stage_description=context.stage_context.current_stage_description,
            stage_status=context.stage_context.current_stage_status,
            stage_detail=context.stage_context.current_stage_detail,
            session_summary=context.session_summary,
            user_message=normalized_message,
            rendered_prompt=rendered_prompt,
            result=result,
            raw_response=raw_response,
        )
        self._event_log.record_chat_message(
            session_id,
            message_role=ChatMessageRole.ASSISTANT,
            content=result.assistant_response,
            stage=context.stage_context.current_stage,
            source="intent_parser",
        )
        self._session.commit()
        return result


def _normalize_parser_output(
    structured_output: IntentParserStructuredOutput,
) -> ParsedChatIntentResponse:
    if structured_output.status != IntentParserStatus.PARSED:
        return ParsedChatIntentResponse(
            status=structured_output.status,
            needs_clarification=structured_output.needs_clarification,
            assistant_response=structured_output.assistant_response,
            clarification_reason=structured_output.clarification_reason,
            proposed_actions=ChatToUIActionBatch(),
        )

    strict_actions = ChatToUIActionBatch.model_validate(
        structured_output.proposed_actions.model_dump(mode="json"),
    )
    return ParsedChatIntentResponse(
        status=IntentParserStatus.PARSED,
        needs_clarification=False,
        assistant_response=structured_output.assistant_response,
        clarification_reason=None,
        proposed_actions=strict_actions,
    )


def _build_failed_result() -> ParsedChatIntentResponse:
    return ParsedChatIntentResponse(
        status=IntentParserStatus.FAILED,
        assistant_response=(
            "I couldn't safely translate that into structured story-studio actions yet. "
            "Please rephrase the change you want, like tone, runtime, beats, or audio settings."
        ),
        proposed_actions=ChatToUIActionBatch(),
    )


def _build_prompt_context(
    snapshot: SessionSnapshot,
    user_message: str,
) -> IntentParserPromptContext:
    current_stage_state = _find_stage_state(snapshot, snapshot.current_stage)
    stage_definition = get_workflow_stage_definition(snapshot.current_stage)
    return IntentParserPromptContext(
        session_id=snapshot.id,
        display_title=snapshot.display_title,
        overall_status=snapshot.overall_status,
        resume_stage=snapshot.resume_stage,
        stage_context=IntentParserStageContext(
            current_stage=snapshot.current_stage,
            current_stage_label=stage_definition.label,
            current_stage_description=stage_definition.description,
            current_stage_status=current_stage_state.status,
            current_stage_detail=current_stage_state.detail,
        ),
        session_summary=build_session_agent_context_summary(snapshot),
        user_message=user_message,
    )


def _find_stage_state(snapshot: SessionSnapshot, stage: WorkflowStage):
    for item in snapshot.stage_states:
        if item.stage == stage:
            return item
    raise SessionNotFoundError(f"session {snapshot.id!r} is missing stage state for {stage.value}")


def _build_explicit_command_result(
    snapshot: SessionSnapshot,
    *,
    explicit_command: ExplicitChatCommandRequest,
) -> ParsedChatIntentResponse:
    if explicit_command.command_id == ExplicitChatCommandId.SUMMARIZE_PLAN:
        assistant_response = _build_plan_summary_response(snapshot)
    elif explicit_command.command_id == ExplicitChatCommandId.NEXT_STAGE:
        if explicit_command.proposed_actions.actions:
            target_stage = explicit_command.proposed_actions.actions[0].target_stage
            stage_label = get_workflow_stage_definition(target_stage).label
            assistant_response = f"I can move the workspace to {stage_label}."
        else:
            assistant_response = (
                "You are already at the final stage, so there is no later "
                "workspace step to open."
            )
    elif explicit_command.command_id == ExplicitChatCommandId.REGENERATE_PITCHES:
        assistant_response = (
            "I can queue a fresh set of pitch options from the current bedtime brief."
        )
    elif explicit_command.command_id == ExplicitChatCommandId.PAUSE_WRITING:
        assistant_response = "I can pause the active writing run."
    elif explicit_command.command_id == ExplicitChatCommandId.RESUME_WRITING:
        assistant_response = "I can resume the paused writing run."
    else:
        assistant_response = "I can translate that command into the story workspace."

    return ParsedChatIntentResponse(
        status=IntentParserStatus.PARSED,
        needs_clarification=False,
        assistant_response=assistant_response,
        clarification_reason=None,
        proposed_actions=explicit_command.proposed_actions,
    )


def _build_explicit_command_audit_prompt(
    *,
    message: str,
    explicit_command: ExplicitChatCommandRequest,
) -> str:
    return (
        f"Explicit command path\n"
        f"message={message}\n"
        f"command_id={explicit_command.command_id.value}\n"
        f"source={explicit_command.source.value}\n"
        f"proposed_actions={explicit_command.proposed_actions.model_dump_json()}"
    )


def _build_plan_summary_response(snapshot: SessionSnapshot) -> str:
    stage_definition = get_workflow_stage_definition(snapshot.current_stage)
    current_focus = stage_definition.label
    current_detail = next(
        (
            stage.detail
            for stage in snapshot.stage_states
            if stage.stage == snapshot.current_stage and stage.detail
        ),
        None,
    )

    plan_parts: list[str] = []
    if snapshot.selected_genre is not None:
        plan_parts.append(snapshot.selected_genre.label)
    if snapshot.selected_tone_profile is not None:
        plan_parts.append(snapshot.selected_tone_profile.label)
    if snapshot.selected_pitch is not None:
        plan_parts.append(f'pitch "{snapshot.selected_pitch.title}"')

    if snapshot.selected_story_setup is not None:
        setup_parts: list[str] = []
        if snapshot.selected_story_setup.target_runtime_minutes is not None:
            setup_parts.append(f"~{snapshot.selected_story_setup.target_runtime_minutes} minutes")
        if snapshot.selected_story_setup.chapter_count is not None:
            setup_parts.append(f"{snapshot.selected_story_setup.chapter_count} chapters")
        if snapshot.selected_story_setup.approximate_scene_count is not None:
            setup_parts.append(
                f"about {snapshot.selected_story_setup.approximate_scene_count} scenes"
            )
        if snapshot.selected_story_setup.target_word_count is not None:
            setup_parts.append(f"{snapshot.selected_story_setup.target_word_count} words")
        if setup_parts:
            plan_parts.append(", ".join(setup_parts))

    if snapshot.active_composition_job is not None:
        plan_parts.append(
            f"writing is {snapshot.active_composition_job.status.replace('_', ' ')}"
        )
    elif snapshot.active_audio_job is not None:
        plan_parts.append(
            f"audio is {snapshot.active_audio_job.status.replace('_', ' ')}"
        )

    plan_summary = ", ".join(plan_parts) if plan_parts else "the story plan is still taking shape"
    focus_tail = f" {current_detail}" if current_detail else ""
    return f"Current focus is {current_focus.lower()}.{focus_tail} Plan so far: {plan_summary}."

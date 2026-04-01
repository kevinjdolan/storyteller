from __future__ import annotations

from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.ai import IntentParserAdapter, IntentParserTransportError, build_intent_parser_invocation
from app.models import (
    ChatMessageRole,
    ChatToUIActionBatch,
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
from app.services.event_log import SessionEventLogService
from app.services.sessions import SessionNotFoundError, SessionService


class SessionIntentParserService:
    def __init__(self, session: Session, parser: IntentParserAdapter):
        self._session = session
        self._parser = parser
        self._sessions = SessionService(session)
        self._event_log = SessionEventLogService(session)

    def parse_user_message(
        self,
        session_id: str,
        *,
        message: str,
    ) -> ParsedChatIntentResponse:
        normalized_message = message.strip()
        if not normalized_message:
            raise ValueError("message must not be empty")

        snapshot = self._sessions.load_session_snapshot(session_id)
        context = _build_prompt_context(snapshot, normalized_message)
        invocation = build_intent_parser_invocation(context, model_id=self._parser.model_id)

        self._event_log.record_chat_message(
            session_id,
            message_role=ChatMessageRole.USER,
            content=normalized_message,
            stage=context.stage_context.current_stage,
        )
        self._session.commit()

        raw_response = None
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
            prompt_version=invocation.prompt_version,
            model_id=invocation.model_id,
            current_stage=context.stage_context.current_stage,
            stage_label=context.stage_context.current_stage_label,
            stage_description=context.stage_context.current_stage_description,
            stage_status=context.stage_context.current_stage_status,
            stage_detail=context.stage_context.current_stage_detail,
            session_summary=context.session_summary,
            user_message=normalized_message,
            rendered_prompt=invocation.rendered_prompt,
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
        session_summary=_build_session_summary(snapshot),
        user_message=user_message,
    )


def _find_stage_state(snapshot: SessionSnapshot, stage: WorkflowStage):
    for item in snapshot.stage_states:
        if item.stage == stage:
            return item
    raise SessionNotFoundError(f"session {snapshot.id!r} is missing stage state for {stage.value}")


def _build_session_summary(snapshot: SessionSnapshot) -> str:
    stage_statuses = ", ".join(
        f"{item.stage.value}={item.status.value}"
        for item in snapshot.stage_states
    )
    lines = [
        f"Session title: {snapshot.display_title}",
        f"Overall status: {snapshot.overall_status.value}",
        f"Resume stage: {snapshot.resume_stage.value}",
        f"Stage statuses: {stage_statuses}",
    ]

    if snapshot.selected_genre is not None:
        lines.append(f"Selected genre: {snapshot.selected_genre.label}")
    if snapshot.selected_tone_profile is not None:
        lines.append(f"Selected tone: {snapshot.selected_tone_profile.label}")
    if snapshot.story_brief is not None:
        lines.append(
            "Story brief: "
            + _truncate(snapshot.story_brief.normalized_summary or snapshot.story_brief.raw_brief)
        )
    if snapshot.selected_pitch is not None:
        lines.append(f"Selected pitch: {snapshot.selected_pitch.title}")
        lines.append(f"Pitch logline: {_truncate(snapshot.selected_pitch.logline)}")
    if snapshot.selected_character_sheet is not None:
        character_summary = snapshot.selected_character_sheet.title or "Character sheet selected"
        if snapshot.selected_character_sheet.protagonist_name:
            character_summary += (
                f" (protagonist: {snapshot.selected_character_sheet.protagonist_name})"
            )
        lines.append(character_summary)
    if snapshot.selected_beat_sheet is not None and snapshot.selected_beat_sheet.summary:
        lines.append(f"Beat sheet: {_truncate(snapshot.selected_beat_sheet.summary)}")
    if snapshot.selected_story_setup is not None:
        setup_bits = []
        if snapshot.selected_story_setup.target_word_count is not None:
            setup_bits.append(f"{snapshot.selected_story_setup.target_word_count} words")
        if snapshot.selected_story_setup.target_runtime_minutes is not None:
            setup_bits.append(f"{snapshot.selected_story_setup.target_runtime_minutes} minutes")
        if snapshot.selected_story_setup.chapter_count is not None:
            setup_bits.append(f"{snapshot.selected_story_setup.chapter_count} chapters")
        if snapshot.selected_story_setup.chapter_style:
            setup_bits.append(snapshot.selected_story_setup.chapter_style)
        if snapshot.selected_story_setup.guidance_notes:
            setup_bits.append(_truncate(snapshot.selected_story_setup.guidance_notes))
        if setup_bits:
            lines.append("Story setup: " + ", ".join(setup_bits))
    if snapshot.active_composition_job is not None:
        lines.append(
            "Composition job: "
            f"{snapshot.active_composition_job.status} at "
            f"{snapshot.active_composition_job.progress_percent:.1f}%"
        )
    if snapshot.active_audio_job is not None:
        lines.append(
            "Audio job: "
            f"{snapshot.active_audio_job.status}, "
            f"voice={snapshot.active_audio_job.voice_key or 'unset'}, "
            f"speed={snapshot.active_audio_job.playback_speed}"
        )

    return "\n".join(lines)


def _truncate(value: str, *, limit: int = 240) -> str:
    if len(value) <= limit:
        return value
    return f"{value[: limit - 3].rstrip()}..."

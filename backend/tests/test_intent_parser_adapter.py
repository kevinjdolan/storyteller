from __future__ import annotations

import json

import httpx
from app.ai import (
    GeminiIntentParserAdapter,
    get_intent_parser_response_schema,
    render_intent_parser_prompt,
)
from app.ai.intent_parser import build_intent_parser_invocation
from app.models import (
    IntentParserPromptContext,
    IntentParserStageContext,
    IntentParserStatus,
    WorkflowStage,
    WorkflowStageState,
)


def _build_context() -> IntentParserPromptContext:
    return IntentParserPromptContext(
        session_id="session-123",
        display_title="Moonlit Harbor",
        overall_status=WorkflowStageState.IN_PROGRESS,
        resume_stage=WorkflowStage.BEATS,
        stage_context=IntentParserStageContext(
            current_stage=WorkflowStage.BEATS,
            current_stage_label="Beat sheet",
            current_stage_description="Store the accepted Save-the-Cat beat sheet for the session.",
            current_stage_status=WorkflowStageState.IN_PROGRESS,
            current_stage_detail="Refining the midpoint tension.",
        ),
        session_summary=(
            "Selected genre: Quest Fantasy\n"
            "Selected tone: Hushed Wonder\n"
            "Story brief: A harbor mystery with a calm ending."
        ),
        user_message="make it a little more mysterious and shorter",
    )


def test_render_intent_parser_prompt_includes_guardrails_and_context() -> None:
    prompt = render_intent_parser_prompt(_build_context())

    assert "backend-only chat intent parser" in prompt
    assert 'status="needs_clarification"' in prompt
    assert '"current_stage": "beats"' in prompt
    assert "Selected tone: Hushed Wonder" in prompt
    assert "make it a little more mysterious and shorter" in prompt


def test_intent_parser_response_schema_strips_unsupported_json_schema_keywords() -> None:
    schema_json = json.dumps(get_intent_parser_response_schema(), sort_keys=True)

    assert '"enum"' in schema_json
    assert '"const"' not in schema_json
    assert '"default"' not in schema_json
    assert '"discriminator"' not in schema_json
    assert '"minLength"' not in schema_json


def test_gemini_intent_parser_adapter_requests_json_schema_and_parses_response() -> None:
    seen_request: dict[str, object] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        seen_request["url"] = str(request.url)
        seen_request["headers"] = dict(request.headers)
        seen_request["body"] = json.loads(request.content.decode("utf-8"))
        return httpx.Response(
            200,
            json={
                "candidates": [
                    {
                        "content": {
                            "parts": [
                                {
                                    "text": json.dumps(
                                        {
                                            "schema_version": 1,
                                            "status": "parsed",
                                            "needs_clarification": False,
                                            "assistant_response": (
                                                "I can make the beat sheet moodier "
                                                "and shorten the target runtime."
                                            ),
                                            "clarification_reason": None,
                                            "proposed_actions": {
                                                "schema_version": 1,
                                                "actions": [
                                                    {
                                                        "action_type": "refine_beat_sheet",
                                                        "target_stage": "beats",
                                                        "confidence": 0.84,
                                                        "rationale": (
                                                            "The user asked for a more "
                                                            "mysterious beat shape."
                                                        ),
                                                        "requires_confirmation": True,
                                                        "extracted_values": {
                                                            "instructions": (
                                                                "Make the midpoint a little "
                                                                "more mysterious."
                                                            ),
                                                            "bedtime_goal": (
                                                                "Keep the tension calm and "
                                                                "bedtime-safe."
                                                            ),
                                                        },
                                                    }
                                                ],
                                            },
                                        }
                                    )
                                }
                            ]
                        }
                    }
                ]
            },
        )

    transport = httpx.MockTransport(handler)
    client = httpx.Client(transport=transport)
    adapter = GeminiIntentParserAdapter(
        credential="test-key",
        model_id="gemini-3.1-flash-lite",
        client=client,
    )

    invocation = build_intent_parser_invocation(
        _build_context(),
        model_id=adapter.model_id,
    )
    result = adapter.parse(invocation)

    request_body = seen_request["body"]
    assert isinstance(request_body, dict)
    assert seen_request["url"] == (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        "gemini-3.1-flash-lite:generateContent"
    )
    assert seen_request["headers"]["x-goog-api-key"] == "test-key"
    assert request_body["generationConfig"]["responseMimeType"] == "application/json"
    assert "responseJsonSchema" in request_body["generationConfig"]
    assert "make it a little more mysterious and shorter" in (
        request_body["contents"][0]["parts"][0]["text"]
    )
    assert result.structured_output.status == IntentParserStatus.PARSED
    assert result.structured_output.proposed_actions.actions[0].action_type == "refine_beat_sheet"
    assert result.invocation.prompt_version == "intent_parser.v1"

    adapter.close()

from __future__ import annotations

import json

import httpx
from app.ai import (
    GeminiBriefNormalizationAdapter,
    build_brief_normalization_invocation,
    get_brief_normalization_response_schema,
    render_brief_normalization_prompt,
)
from app.models import (
    BRIEF_NORMALIZATION_PROMPT_VERSION,
    BriefNormalizationPromptContext,
)


def _build_context() -> BriefNormalizationPromptContext:
    return BriefNormalizationPromptContext(
        raw_brief=(
            "A child and an otter guardian drift after runaway lanterns to "
            "bring each light home before the harbor sleeps."
        ),
        genre_label="Quest Fantasy",
        tone_label="Hushed Wonder",
        story_idea=(
            "A child and an otter guardian drift after runaway lanterns to "
            "bring each light home before the harbor sleeps."
        ),
        desired_themes="Gentle courage, belonging, and a calm return home.",
        key_images="Floating lanterns, otter paws, and quiet docks.",
        audience_notes="Keep it cozy for a sensitive five-year-old.",
        must_have_elements="End with the harbor settled and the child tucked in safely.",
    )


def test_render_brief_normalization_prompt_includes_structured_rules_and_context() -> None:
    prompt = render_brief_normalization_prompt(_build_context())

    assert "structured planning preferences" in prompt
    assert "bedtime_safety_concerns" in prompt
    assert '"tone_label": "Hushed Wonder"' in prompt
    assert "bring each light home before the harbor sleeps" in prompt


def test_brief_normalization_response_schema_strips_unsupported_json_schema_keywords() -> None:
    schema_json = json.dumps(get_brief_normalization_response_schema(), sort_keys=True)

    assert '"const"' not in schema_json
    assert '"default"' not in schema_json
    assert '"minLength"' not in schema_json


def test_gemini_brief_normalization_adapter_requests_json_schema_and_parses_response() -> None:
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
                                            "normalized_summary": (
                                                "A harbor bedtime quest where each lantern "
                                                "return settles the night."
                                            ),
                                            "normalized_preferences": {
                                                "protagonist_type": (
                                                    "A child and an otter guardian"
                                                ),
                                                "setting": "a moonlit harbor",
                                                "emotional_goal": "a calm return home",
                                                "constraint_notes": [
                                                    "End with the harbor settled and safe."
                                                ],
                                                "bedtime_safety_concerns": [
                                                    "Keep every surprise quickly reassuring."
                                                ],
                                                "candidate_motifs": [
                                                    "floating lanterns",
                                                    "moonlit water",
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
    adapter = GeminiBriefNormalizationAdapter(
        credential="test-key",
        model_id="gemini-3.1-flash-lite",
        client=client,
    )

    invocation = build_brief_normalization_invocation(
        _build_context(),
        model_id=adapter.model_id,
    )
    result = adapter.normalize(invocation)

    request_body = seen_request["body"]
    assert isinstance(request_body, dict)
    assert seen_request["url"] == (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        "gemini-3.1-flash-lite:generateContent"
    )
    assert seen_request["headers"]["x-goog-api-key"] == "test-key"
    assert request_body["generationConfig"]["responseMimeType"] == "application/json"
    assert "responseJsonSchema" in request_body["generationConfig"]
    assert (
        "bring each light home before the harbor sleeps"
        in request_body["contents"][0]["parts"][0]["text"]
    )
    assert result.structured_output.normalized_preferences.setting == "a moonlit harbor"
    assert result.invocation.prompt_version == BRIEF_NORMALIZATION_PROMPT_VERSION

    adapter.close()

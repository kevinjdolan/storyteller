from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from string import Template
from typing import Any, Protocol

import httpx

from app.models.chat_actions import DEFAULT_CHAT_TO_UI_ACTION_POLICIES
from app.models.intent_parser import (
    INTENT_PARSER_PROMPT_VERSION,
    IntentParserInvocation,
    IntentParserInvocationResult,
    IntentParserPromptContext,
    IntentParserStructuredOutput,
)

PROMPTS_ROOT = Path(__file__).resolve().parent / "prompts"
DEFAULT_GEMINI_API_BASE_URL = "https://generativelanguage.googleapis.com/v1beta"
_SUPPORTED_JSON_SCHEMA_KEYS = {
    "$anchor",
    "$defs",
    "$id",
    "$ref",
    "additionalProperties",
    "anyOf",
    "description",
    "enum",
    "format",
    "items",
    "maxItems",
    "maximum",
    "minItems",
    "minimum",
    "oneOf",
    "prefixItems",
    "properties",
    "required",
    "title",
    "type",
}
_ACTION_CATALOG = (
    {
        "action_type": "navigate_to_stage",
        "stage": "any",
        "description": "Open a different workflow stage without changing durable data.",
        "common_fields": [],
    },
    {
        "action_type": "select_genre",
        "stage": "genre",
        "description": "Select a catalog genre by id, slug, or label.",
        "common_fields": ["genre_id", "genre_slug", "genre_label"],
    },
    {
        "action_type": "select_tone",
        "stage": "tone",
        "description": "Select a tone profile by id, slug, or label.",
        "common_fields": [
            "tone_profile_id",
            "tone_profile_slug",
            "tone_profile_label",
        ],
    },
    {
        "action_type": "update_story_brief",
        "stage": "brief",
        "description": "Change the story brief text or planning notes.",
        "common_fields": [
            "raw_brief",
            "normalized_summary",
            "planning_notes",
            "edit_mode",
        ],
    },
    {
        "action_type": "regenerate_pitches",
        "stage": "pitches",
        "description": "Ask for a new batch of pitches.",
        "common_fields": ["candidate_count", "guidance", "preserve_selected_pitch"],
    },
    {
        "action_type": "select_pitch",
        "stage": "pitches",
        "description": "Select a pitch by id, generation key, index, or title.",
        "common_fields": ["pitch_id", "generation_key", "pitch_index", "title"],
    },
    {
        "action_type": "select_character_sheet",
        "stage": "characters",
        "description": "Choose a character sheet revision.",
        "common_fields": ["character_sheet_id", "revision_number", "title"],
    },
    {
        "action_type": "refine_character_sheet",
        "stage": "characters",
        "description": "Request character-sheet edits with concrete instructions.",
        "common_fields": [
            "instructions",
            "focus_character_names",
            "change_summary",
        ],
    },
    {
        "action_type": "regenerate_character_sheet",
        "stage": "characters",
        "description": "Regenerate the character sheet with optional guidance.",
        "common_fields": ["guidance"],
    },
    {
        "action_type": "accept_beat_sheet",
        "stage": "beats",
        "description": "Accept a beat sheet revision.",
        "common_fields": ["beat_sheet_id", "revision_number"],
    },
    {
        "action_type": "refine_beat_sheet",
        "stage": "beats",
        "description": "Request beat-sheet edits with explicit instructions.",
        "common_fields": ["instructions", "beat_names", "bedtime_goal"],
    },
    {
        "action_type": "regenerate_beat_sheet",
        "stage": "beats",
        "description": "Regenerate the beat sheet with guidance.",
        "common_fields": ["guidance", "focus_beats"],
    },
    {
        "action_type": "update_story_setup",
        "stage": "story_setup",
        "description": (
            "Update soft planning targets like length, runtime, chapters, or setup guidance."
        ),
        "common_fields": [
            "target_word_count",
            "target_runtime_minutes",
            "chapter_count",
            "chapter_style",
            "guidance_notes",
        ],
    },
    {
        "action_type": "start_composition",
        "stage": "composition",
        "description": "Start writing, continue, or rewrite composition.",
        "common_fields": ["mode", "instructions", "restart_from_segment_index"],
    },
    {
        "action_type": "pause_job",
        "stage": "composition|audio",
        "description": "Pause a composition or audio job.",
        "common_fields": ["job_kind", "job_id", "reason"],
    },
    {
        "action_type": "resume_job",
        "stage": "composition|audio",
        "description": "Resume a composition or audio job.",
        "common_fields": ["job_kind", "job_id", "reason"],
    },
    {
        "action_type": "redirect_composition",
        "stage": "composition",
        "description": "Redirect writing with concrete rewrite instructions.",
        "common_fields": [
            "instructions",
            "rewrite_from_segment_index",
            "preserve_completed_segments",
        ],
    },
    {
        "action_type": "update_audio_settings",
        "stage": "audio",
        "description": "Change narration settings like voice, speed, music, or guidance notes.",
        "common_fields": [
            "voice_key",
            "playback_speed",
            "include_background_music",
            "music_profile",
            "guidance_notes",
        ],
    },
    {
        "action_type": "start_audio_generation",
        "stage": "audio",
        "description": "Start or regenerate audio generation.",
        "common_fields": [
            "voice_key",
            "playback_speed",
            "include_background_music",
            "music_profile",
            "regenerate_existing_audio",
        ],
    },
    {
        "action_type": "open_finalize_view",
        "stage": "finalize",
        "description": "Open the finalize reader or player view.",
        "common_fields": ["view"],
    },
    {
        "action_type": "download_asset",
        "stage": "finalize",
        "description": "Download the story docx or final audio asset.",
        "common_fields": ["asset_kind"],
    },
)


class IntentParserError(RuntimeError):
    """Base error for intent parser adapter failures."""


class IntentParserTransportError(IntentParserError):
    """Raised when the Gemini transport call fails or returns unusable data."""


class IntentParserAdapter(Protocol):
    @property
    def model_id(self) -> str: ...

    def parse(self, invocation: IntentParserInvocation) -> IntentParserInvocationResult: ...

    def close(self) -> None: ...


class GeminiIntentParserAdapter:
    def __init__(
        self,
        *,
        credential: str,
        model_id: str,
        base_url: str = DEFAULT_GEMINI_API_BASE_URL,
        client: httpx.Client | None = None,
    ) -> None:
        self._credential = credential
        self._model_id = model_id
        self._base_url = base_url.rstrip("/")
        self._owns_client = client is None
        self._client = client or httpx.Client(timeout=30.0)

    @property
    def model_id(self) -> str:
        return self._model_id

    def parse(self, invocation: IntentParserInvocation) -> IntentParserInvocationResult:
        response = self._client.post(
            f"{self._base_url}/models/{self._model_id}:generateContent",
            headers={
                "content-type": "application/json",
                "x-goog-api-key": self._credential,
            },
            json={
                "systemInstruction": {
                    "parts": [{"text": ("Return only JSON that matches the requested schema.")}]
                },
                "contents": [
                    {
                        "role": "user",
                        "parts": [{"text": invocation.rendered_prompt}],
                    }
                ],
                "generationConfig": {
                    "temperature": 0,
                    "candidateCount": 1,
                    "maxOutputTokens": 1200,
                    "responseMimeType": "application/json",
                    "responseJsonSchema": get_intent_parser_response_schema(),
                },
            },
        )

        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise IntentParserTransportError(
                f"Gemini intent parser request failed with status {exc.response.status_code}",
            ) from exc

        raw_response = response.json()
        structured_output = _extract_structured_output(raw_response)
        return IntentParserInvocationResult(
            invocation=invocation,
            structured_output=structured_output,
            raw_response=raw_response,
        )

    def close(self) -> None:
        if self._owns_client:
            self._client.close()


def render_intent_parser_prompt(context: IntentParserPromptContext) -> str:
    template = Template(_read_prompt_template())
    return template.substitute(
        action_catalog_json=json.dumps(_ACTION_CATALOG, indent=2, sort_keys=True),
        default_policy_json=json.dumps(
            {key.value: value.value for key, value in DEFAULT_CHAT_TO_UI_ACTION_POLICIES.items()},
            indent=2,
            sort_keys=True,
        ),
        stage_context_json=json.dumps(
            context.stage_context.model_dump(mode="json"),
            indent=2,
            sort_keys=True,
        ),
        session_summary=context.session_summary,
        user_message=context.user_message,
    )


def build_intent_parser_invocation(
    context: IntentParserPromptContext,
    *,
    model_id: str,
) -> IntentParserInvocation:
    return IntentParserInvocation(
        prompt_version=INTENT_PARSER_PROMPT_VERSION,
        model_id=model_id,
        context=context,
        rendered_prompt=render_intent_parser_prompt(context),
    )


@lru_cache(maxsize=1)
def get_intent_parser_response_schema() -> dict[str, Any]:
    schema = IntentParserStructuredOutput.model_json_schema()
    return _sanitize_json_schema(schema)


@lru_cache(maxsize=1)
def _read_prompt_template() -> str:
    return (PROMPTS_ROOT / "intent_parser.md").read_text(encoding="utf-8")


def _sanitize_json_schema(value: Any) -> Any:
    if isinstance(value, list):
        return [_sanitize_json_schema(item) for item in value]

    if isinstance(value, dict):
        normalized: dict[str, Any] = {}

        if "const" in value and "enum" not in value:
            normalized["enum"] = [value["const"]]

        for key, item in value.items():
            if key == "const":
                continue
            if key not in _SUPPORTED_JSON_SCHEMA_KEYS:
                continue
            if key in {"$defs", "properties"}:
                normalized[key] = {
                    name: _sanitize_json_schema(child) for name, child in item.items()
                }
                continue
            if key == "additionalProperties" and isinstance(item, dict):
                normalized[key] = _sanitize_json_schema(item)
                continue
            normalized[key] = _sanitize_json_schema(item)

        return normalized

    return value


def _extract_structured_output(raw_response: dict[str, Any]) -> IntentParserStructuredOutput:
    blocked_reason = raw_response.get("promptFeedback", {}).get("blockReason")
    if blocked_reason:
        raise IntentParserTransportError(
            f"Gemini intent parser request was blocked: {blocked_reason}",
        )

    candidates = raw_response.get("candidates")
    if not isinstance(candidates, list) or not candidates:
        raise IntentParserTransportError("Gemini intent parser returned no candidates")

    candidate = candidates[0]
    text_parts: list[str] = []
    for part in candidate.get("content", {}).get("parts", []):
        text = part.get("text")
        if isinstance(text, str) and text.strip():
            text_parts.append(text)

    if not text_parts:
        finish_reason = candidate.get("finishReason", "unknown")
        raise IntentParserTransportError(
            f"Gemini intent parser returned no text content (finish_reason={finish_reason})",
        )

    raw_text = "".join(text_parts).strip()
    try:
        structured_payload = json.loads(raw_text)
    except json.JSONDecodeError as exc:
        raise IntentParserTransportError("Gemini intent parser returned invalid JSON") from exc

    try:
        return IntentParserStructuredOutput.model_validate(structured_payload)
    except Exception as exc:  # pragma: no cover - converted to adapter error path
        raise IntentParserTransportError(
            "Gemini intent parser returned JSON that did not match the expected structure",
        ) from exc

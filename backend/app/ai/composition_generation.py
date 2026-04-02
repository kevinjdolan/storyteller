from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from string import Template
from typing import Any, Protocol

import httpx

from app.models import (
    COMPOSITION_SEGMENT_GENERATION_PROMPT_VERSION,
    CompositionSegmentGenerationInvocation,
    CompositionSegmentGenerationInvocationResult,
    CompositionSegmentGenerationPromptContext,
    CompositionSegmentGenerationStructuredOutput,
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


class CompositionSegmentGenerationError(RuntimeError):
    """Base error for segmented composition adapter failures."""


class CompositionSegmentGenerationTransportError(CompositionSegmentGenerationError):
    """Raised when the Gemini segmented composition transport fails or returns invalid data."""


class CompositionSegmentGenerationAdapter(Protocol):
    @property
    def model_id(self) -> str: ...

    def generate(
        self,
        invocation: CompositionSegmentGenerationInvocation,
    ) -> CompositionSegmentGenerationInvocationResult: ...

    def close(self) -> None: ...


class GeminiCompositionSegmentGenerationAdapter:
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
        self._client = client or httpx.Client(timeout=60.0)

    @property
    def model_id(self) -> str:
        return self._model_id

    def generate(
        self,
        invocation: CompositionSegmentGenerationInvocation,
    ) -> CompositionSegmentGenerationInvocationResult:
        response = self._client.post(
            f"{self._base_url}/models/{self._model_id}:generateContent",
            headers={
                "content-type": "application/json",
                "x-goog-api-key": self._credential,
            },
            json={
                "systemInstruction": {
                    "parts": [{"text": "Return only JSON that matches the requested schema."}]
                },
                "contents": [
                    {
                        "role": "user",
                        "parts": [{"text": invocation.rendered_prompt}],
                    }
                ],
                "generationConfig": {
                    "temperature": 0.7,
                    "candidateCount": 1,
                    "maxOutputTokens": 3200,
                    "responseMimeType": "application/json",
                    "responseJsonSchema": get_composition_segment_generation_response_schema(),
                },
            },
        )

        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise CompositionSegmentGenerationTransportError(
                "Gemini composition segment generation request failed with status "
                f"{exc.response.status_code}",
            ) from exc

        raw_response = response.json()
        structured_output = _extract_structured_output(raw_response)
        return CompositionSegmentGenerationInvocationResult(
            invocation=invocation,
            structured_output=structured_output,
            raw_response=raw_response,
        )

    def close(self) -> None:
        if self._owns_client:
            self._client.close()


def render_composition_segment_generation_prompt(
    context: CompositionSegmentGenerationPromptContext,
) -> str:
    template = Template(_read_prompt_template())
    return template.substitute(
        composition_segment_context_json=json.dumps(
            context.model_dump(mode="json"),
            indent=2,
            sort_keys=True,
        )
    )


def build_composition_segment_generation_invocation(
    context: CompositionSegmentGenerationPromptContext,
    *,
    model_id: str,
) -> CompositionSegmentGenerationInvocation:
    return CompositionSegmentGenerationInvocation(
        prompt_version=COMPOSITION_SEGMENT_GENERATION_PROMPT_VERSION,
        model_id=model_id,
        context=context,
        rendered_prompt=render_composition_segment_generation_prompt(context),
    )


@lru_cache(maxsize=1)
def get_composition_segment_generation_response_schema() -> dict[str, Any]:
    return _sanitize_json_schema(CompositionSegmentGenerationStructuredOutput.model_json_schema())


@lru_cache(maxsize=1)
def _read_prompt_template() -> str:
    return (PROMPTS_ROOT / "composition_segment_generation.md").read_text(encoding="utf-8")


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


def _extract_structured_output(
    raw_response: dict[str, Any],
) -> CompositionSegmentGenerationStructuredOutput:
    blocked_reason = raw_response.get("promptFeedback", {}).get("blockReason")
    if blocked_reason:
        raise CompositionSegmentGenerationTransportError(
            f"Gemini composition segment request was blocked: {blocked_reason}",
        )

    candidates = raw_response.get("candidates")
    if not isinstance(candidates, list) or not candidates:
        raise CompositionSegmentGenerationTransportError(
            "Gemini composition segment generation returned no candidates",
        )

    candidate = candidates[0]
    text_parts: list[str] = []
    for part in candidate.get("content", {}).get("parts", []):
        text = part.get("text")
        if isinstance(text, str) and text.strip():
            text_parts.append(text)

    if not text_parts:
        finish_reason = candidate.get("finishReason", "unknown")
        raise CompositionSegmentGenerationTransportError(
            "Gemini composition segment generation returned no text content "
            f"(finish_reason={finish_reason})",
        )

    raw_text = "".join(text_parts).strip()
    try:
        structured_payload = json.loads(raw_text)
    except json.JSONDecodeError as exc:
        raise CompositionSegmentGenerationTransportError(
            "Gemini composition segment generation returned invalid JSON",
        ) from exc

    try:
        return CompositionSegmentGenerationStructuredOutput.model_validate(structured_payload)
    except Exception as exc:  # pragma: no cover - normalized to adapter error
        raise CompositionSegmentGenerationTransportError(
            "Gemini composition segment generation returned JSON that did not match the "
            "expected structure",
        ) from exc

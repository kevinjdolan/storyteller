from __future__ import annotations

import base64
import binascii
import json
import re
from dataclasses import dataclass
from time import sleep
from typing import Any, Mapping, Protocol

import httpx

from app.models.audio_settings import AudioNarrationStyle, AudioVoiceKey

DEFAULT_GEMINI_API_BASE_URL = "https://generativelanguage.googleapis.com/v1beta"
DEFAULT_GEMINI_TTS_SAMPLE_RATE_HZ = 24_000
DEFAULT_GEMINI_TTS_CHANNEL_COUNT = 1
DEFAULT_GEMINI_TTS_SAMPLE_WIDTH_BYTES = 2
DEFAULT_GEMINI_TTS_TIMEOUT_SECONDS = 90.0
DEFAULT_GEMINI_TTS_MAX_RETRIES = 3
DEFAULT_GEMINI_TTS_RETRY_BACKOFF_SECONDS = 0.35
GEMINI_TTS_PROMPT_VERSION = "gemini_tts.v1"
_RETRYABLE_STATUS_CODES = {429, 500, 502, 503, 504}
_MIME_RATE_PATTERN = re.compile(r"rate=(?P<rate>\d+)")

_VOICE_PROFILES: dict[AudioVoiceKey, tuple[str, str]] = {
    AudioVoiceKey.MOONBEAM: (
        "Achernar",
        "Soft, airy, and night-settling without losing diction.",
    ),
    AudioVoiceKey.HEARTHSIDE: (
        "Sulafat",
        "Warm, tucked-in, and reassuring for cozy family scenes.",
    ),
    AudioVoiceKey.STORYKEEPER: (
        "Iapetus",
        "Clear and steady for longer passages and chapter transitions.",
    ),
}

_STYLE_DIRECTIONS: dict[AudioNarrationStyle, str] = {
    AudioNarrationStyle.CALM: (
        "Keep the delivery even, calm, and bedtime-safe with gentle phrasing."
    ),
    AudioNarrationStyle.HUSHED: (
        "Keep the delivery hushed and intimate while staying fully intelligible."
    ),
    AudioNarrationStyle.WARM: (
        "Keep the delivery warm, reassuring, and softly expressive."
    ),
}


class TextToSpeechError(RuntimeError):
    """Base error for provider-backed narration synthesis failures."""


class TextToSpeechTransportError(TextToSpeechError):
    """Raised when Gemini TTS fails, retries out, or returns unusable audio."""

    def __init__(
        self,
        message: str,
        *,
        raw_response: Mapping[str, Any] | list[Any] | str | None = None,
    ) -> None:
        super().__init__(message)
        self.raw_response = raw_response


@dataclass(frozen=True)
class NarrationSynthesisRequest:
    text: str
    voice_key: AudioVoiceKey
    narration_style: AudioNarrationStyle
    playback_speed: float
    guidance_notes: str | None = None


@dataclass(frozen=True)
class NarrationSynthesisResult:
    pcm_audio_bytes: bytes
    provider: str
    model_id: str
    prompt_version: str
    rendered_prompt: str
    voice_name: str
    provider_mime_type: str
    sample_rate_hz: int
    channel_count: int
    sample_width_bytes: int
    attempts_used: int
    raw_response: Mapping[str, Any] | list[Any] | str | None = None
    response_metadata: dict[str, Any] | None = None


class NarrationTextToSpeechAdapter(Protocol):
    @property
    def model_id(self) -> str: ...

    def synthesize(self, request: NarrationSynthesisRequest) -> NarrationSynthesisResult: ...

    def close(self) -> None: ...


class GeminiTextToSpeechAdapter:
    def __init__(
        self,
        *,
        credential: str,
        model_id: str,
        base_url: str = DEFAULT_GEMINI_API_BASE_URL,
        timeout_seconds: float = DEFAULT_GEMINI_TTS_TIMEOUT_SECONDS,
        max_retries: int = DEFAULT_GEMINI_TTS_MAX_RETRIES,
        retry_backoff_seconds: float = DEFAULT_GEMINI_TTS_RETRY_BACKOFF_SECONDS,
        client: httpx.Client | None = None,
    ) -> None:
        self._credential = credential
        self._model_id = model_id
        self._base_url = base_url.rstrip("/")
        self._max_retries = max(int(max_retries), 1)
        self._retry_backoff_seconds = max(float(retry_backoff_seconds), 0.0)
        self._owns_client = client is None
        self._client = client or httpx.Client(timeout=max(float(timeout_seconds), 1.0))

    @property
    def model_id(self) -> str:
        return self._model_id

    def synthesize(self, request: NarrationSynthesisRequest) -> NarrationSynthesisResult:
        rendered_prompt = render_gemini_tts_prompt(request)
        voice_name, _voice_direction = _VOICE_PROFILES[request.voice_key]
        raw_response: dict[str, Any] | None = None
        last_error: TextToSpeechTransportError | None = None

        for attempt in range(1, self._max_retries + 1):
            try:
                response = self._client.post(
                    f"{self._base_url}/models/{self._model_id}:generateContent",
                    headers={
                        "content-type": "application/json",
                        "x-goog-api-key": self._credential,
                    },
                    json={
                        "contents": [
                            {
                                "role": "user",
                                "parts": [{"text": rendered_prompt}],
                            }
                        ],
                        "generationConfig": {
                            "responseModalities": ["AUDIO"],
                            "speechConfig": {
                                "voiceConfig": {
                                    "prebuiltVoiceConfig": {
                                        "voiceName": voice_name,
                                    }
                                }
                            },
                        },
                    },
                )
                if response.status_code in _RETRYABLE_STATUS_CODES and attempt < self._max_retries:
                    self._sleep_before_retry(attempt)
                    continue
                response.raise_for_status()
                raw_response = response.json()
                return _extract_synthesis_result(
                    raw_response=raw_response,
                    model_id=self._model_id,
                    rendered_prompt=rendered_prompt,
                    voice_name=voice_name,
                    attempts_used=attempt,
                )
            except httpx.HTTPStatusError as exc:
                last_error = TextToSpeechTransportError(
                    (
                        "Gemini TTS request failed with status "
                        f"{exc.response.status_code}: {_extract_error_message(exc.response)}"
                    ),
                    raw_response=_safe_json_payload(exc.response),
                )
                if (
                    exc.response.status_code in _RETRYABLE_STATUS_CODES
                    and attempt < self._max_retries
                ):
                    self._sleep_before_retry(attempt)
                    continue
                raise last_error from exc
            except (httpx.TimeoutException, httpx.NetworkError) as exc:
                last_error = TextToSpeechTransportError(
                    f"Gemini TTS request failed during transport: {exc}",
                )
                if attempt < self._max_retries:
                    self._sleep_before_retry(attempt)
                    continue
                raise last_error from exc

        raise last_error or TextToSpeechTransportError(
            "Gemini TTS request exhausted its retry budget without a usable response",
            raw_response=raw_response,
        )

    def close(self) -> None:
        if self._owns_client:
            self._client.close()

    def _sleep_before_retry(self, attempt: int) -> None:
        if self._retry_backoff_seconds <= 0:
            return
        sleep(self._retry_backoff_seconds * attempt)


def render_gemini_tts_prompt(request: NarrationSynthesisRequest) -> str:
    normalized_text = request.text.strip()
    if not normalized_text:
        raise ValueError("narration text must not be empty")

    voice_name, voice_direction = _VOICE_PROFILES[request.voice_key]
    style_direction = _STYLE_DIRECTIONS[request.narration_style]
    guidance_notes = request.guidance_notes.strip() if request.guidance_notes else ""

    prompt_sections = [
        "Read the bedtime-story passage exactly as written.",
        "Do not add titles, scene labels, ad-libs, paraphrases, or extra closing lines.",
        "Keep all names and wording verbatim.",
        "Performance direction:",
        f"- Use the {voice_name} voice.",
        f"- Voice profile: {voice_direction}",
        f"- Delivery style: {style_direction}",
        f"- Pace guidance: {_describe_playback_speed(request.playback_speed)}",
        "- Keep the mood reassuring, grounded, and gentle enough for bedtime listening.",
        "- Let punctuation shape natural pauses, but never skip or rewrite the text.",
    ]

    if guidance_notes:
        prompt_sections.extend(
            [
                "Additional direction:",
                guidance_notes,
            ]
        )

    prompt_sections.extend(
        [
            "Passage:",
            '"""',
            normalized_text,
            '"""',
        ]
    )
    return "\n".join(prompt_sections)


def _describe_playback_speed(playback_speed: float) -> str:
    if playback_speed <= 0:
        raise ValueError("playback_speed must be greater than zero")

    if playback_speed <= 0.8:
        pace = "Noticeably slower than a typical read-aloud, with roomy pauses."
    elif playback_speed < 0.95:
        pace = "A little slower than a typical bedtime read-aloud."
    elif playback_speed <= 1.05:
        pace = "A natural bedtime read-aloud pace."
    elif playback_speed <= 1.2:
        pace = "Slightly brisker than usual while staying calm and clear."
    else:
        pace = "Brisk but still gentle, keeping every word clear."

    return f"{pace} Target pacing: about {playback_speed:g}x."


def _extract_synthesis_result(
    *,
    raw_response: dict[str, Any],
    model_id: str,
    rendered_prompt: str,
    voice_name: str,
    attempts_used: int,
) -> NarrationSynthesisResult:
    blocked_reason = raw_response.get("promptFeedback", {}).get("blockReason")
    if blocked_reason:
        raise TextToSpeechTransportError(
            f"Gemini TTS request was blocked: {blocked_reason}",
            raw_response=raw_response,
        )

    candidates = raw_response.get("candidates")
    if not isinstance(candidates, list) or not candidates:
        raise TextToSpeechTransportError(
            "Gemini TTS returned no candidates",
            raw_response=raw_response,
        )

    candidate = candidates[0]
    parts = candidate.get("content", {}).get("parts", [])
    if not isinstance(parts, list) or not parts:
        raise TextToSpeechTransportError(
            "Gemini TTS returned no content parts",
            raw_response=raw_response,
        )

    inline_data = None
    for part in parts:
        maybe_inline = part.get("inlineData")
        if isinstance(maybe_inline, dict):
            inline_data = maybe_inline
            break

    if inline_data is None:
        raise TextToSpeechTransportError(
            "Gemini TTS response did not include inline audio data",
            raw_response=raw_response,
        )

    encoded_audio = inline_data.get("data")
    if not isinstance(encoded_audio, str) or not encoded_audio.strip():
        raise TextToSpeechTransportError(
            "Gemini TTS response included an empty inline audio payload",
            raw_response=raw_response,
        )

    try:
        pcm_audio_bytes = base64.b64decode(encoded_audio, validate=True)
    except (ValueError, binascii.Error) as exc:
        raise TextToSpeechTransportError(
            "Gemini TTS response included invalid base64 audio data",
            raw_response=raw_response,
        ) from exc

    provider_mime_type = _normalize_provider_mime_type(inline_data.get("mimeType"))
    sample_rate_hz = _extract_sample_rate(provider_mime_type)
    response_metadata = {
        "attempts_used": attempts_used,
        "finish_reason": candidate.get("finishReason"),
        "safety_ratings": candidate.get("safetyRatings"),
        "usage_metadata": raw_response.get("usageMetadata"),
        "model_version": raw_response.get("modelVersion"),
        "response_id": raw_response.get("responseId"),
    }

    return NarrationSynthesisResult(
        pcm_audio_bytes=pcm_audio_bytes,
        provider="gemini",
        model_id=model_id,
        prompt_version=GEMINI_TTS_PROMPT_VERSION,
        rendered_prompt=rendered_prompt,
        voice_name=voice_name,
        provider_mime_type=provider_mime_type,
        sample_rate_hz=sample_rate_hz,
        channel_count=DEFAULT_GEMINI_TTS_CHANNEL_COUNT,
        sample_width_bytes=DEFAULT_GEMINI_TTS_SAMPLE_WIDTH_BYTES,
        attempts_used=attempts_used,
        raw_response=raw_response,
        response_metadata=response_metadata,
    )


def _normalize_provider_mime_type(value: Any) -> str:
    if isinstance(value, str) and value.strip():
        return value.strip()
    return f"audio/L16;rate={DEFAULT_GEMINI_TTS_SAMPLE_RATE_HZ}"


def _extract_sample_rate(provider_mime_type: str) -> int:
    match = _MIME_RATE_PATTERN.search(provider_mime_type)
    if match is None:
        return DEFAULT_GEMINI_TTS_SAMPLE_RATE_HZ
    try:
        return int(match.group("rate"))
    except ValueError:
        return DEFAULT_GEMINI_TTS_SAMPLE_RATE_HZ


def _safe_json_payload(response: httpx.Response) -> Mapping[str, Any] | list[Any] | str | None:
    try:
        return response.json()
    except json.JSONDecodeError:
        return response.text.strip() or None


def _extract_error_message(response: httpx.Response) -> str:
    payload = _safe_json_payload(response)
    if isinstance(payload, dict):
        error_payload = payload.get("error")
        if isinstance(error_payload, dict):
            message = error_payload.get("message")
            if isinstance(message, str) and message.strip():
                return message.strip()

    if isinstance(payload, str) and payload:
        return payload
    return response.reason_phrase

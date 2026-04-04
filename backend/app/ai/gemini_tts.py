from __future__ import annotations

import base64
import binascii
import re
from dataclasses import dataclass
from time import sleep as default_sleep
from typing import Any, Callable, Mapping, Protocol

import httpx

from app.ai.gemini_resilience import (
    DEFAULT_GEMINI_AUDIO_RETRY_POLICY,
    GeminiFailureDetail,
    GeminiRetryNotice,
    GeminiRetryPolicy,
    build_blocked_failure,
    build_invalid_response_failure,
    classify_gemini_exception,
    execute_with_retry,
    safe_json_payload,
)
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
        failure_detail: GeminiFailureDetail | None = None,
    ) -> None:
        super().__init__(message)
        self.raw_response = raw_response
        self.failure_detail = failure_detail


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
        max_retry_backoff_seconds: float | None = None,
        retry_policy: GeminiRetryPolicy | None = None,
        retry_notifier: Callable[[GeminiRetryNotice], None] | None = None,
        client: httpx.Client | None = None,
        sleep_func: Callable[[float], None] = default_sleep,
    ) -> None:
        self._credential = credential
        self._model_id = model_id
        self._base_url = base_url.rstrip("/")
        normalized_max_retries = max(int(max_retries), 1)
        normalized_backoff_seconds = max(float(retry_backoff_seconds), 0.0)
        self._retry_policy = retry_policy or GeminiRetryPolicy(
            max_attempts=normalized_max_retries,
            initial_backoff_seconds=normalized_backoff_seconds,
            max_backoff_seconds=max(
                float(
                    max_retry_backoff_seconds
                    if max_retry_backoff_seconds is not None
                    else max(
                        DEFAULT_GEMINI_AUDIO_RETRY_POLICY.max_backoff_seconds,
                        normalized_backoff_seconds,
                    )
                ),
                normalized_backoff_seconds,
            ),
        )
        self._retry_notifier = retry_notifier
        self._owns_client = client is None
        self._client = client or httpx.Client(timeout=max(float(timeout_seconds), 1.0))
        self._sleep_func = sleep_func

    @property
    def model_id(self) -> str:
        return self._model_id

    def synthesize(self, request: NarrationSynthesisRequest) -> NarrationSynthesisResult:
        rendered_prompt = render_gemini_tts_prompt(request)
        voice_name, _voice_direction = _VOICE_PROFILES[request.voice_key]
        try:
            execution = execute_with_retry(
                lambda: self._synthesize_once(
                    rendered_prompt=rendered_prompt,
                    voice_name=voice_name,
                ),
                policy=self._retry_policy,
                classify_exception=lambda exc: classify_gemini_exception(
                    exc,
                    operation_name="text-to-speech generation",
                ),
                on_retry=self._retry_notifier,
                sleep_func=self._sleep_func,
            )
            result = execution.value
            return NarrationSynthesisResult(
                pcm_audio_bytes=result.pcm_audio_bytes,
                provider=result.provider,
                model_id=result.model_id,
                prompt_version=result.prompt_version,
                rendered_prompt=result.rendered_prompt,
                voice_name=result.voice_name,
                provider_mime_type=result.provider_mime_type,
                sample_rate_hz=result.sample_rate_hz,
                channel_count=result.channel_count,
                sample_width_bytes=result.sample_width_bytes,
                attempts_used=execution.attempts_used,
                raw_response=result.raw_response,
                response_metadata={
                    **(result.response_metadata or {}),
                    "attempts_used": execution.attempts_used,
                },
            )
        except TextToSpeechTransportError:
            raise
        except Exception as exc:
            failure_detail = classify_gemini_exception(
                exc,
                operation_name="text-to-speech generation",
            )
            raise TextToSpeechTransportError(
                failure_detail.message,
                failure_detail=failure_detail,
            ) from exc

    def close(self) -> None:
        if self._owns_client:
            self._client.close()

    def set_retry_notifier(
        self,
        retry_notifier: Callable[[GeminiRetryNotice], None] | None,
    ) -> None:
        self._retry_notifier = retry_notifier

    def _synthesize_once(
        self,
        *,
        rendered_prompt: str,
        voice_name: str,
    ) -> NarrationSynthesisResult:
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
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            failure_detail = classify_gemini_exception(
                exc,
                operation_name="text-to-speech generation",
            )
            raise TextToSpeechTransportError(
                failure_detail.message,
                raw_response=safe_json_payload(exc.response),
                failure_detail=failure_detail,
            ) from exc

        raw_response = response.json()
        return _extract_synthesis_result(
            raw_response=raw_response,
            model_id=self._model_id,
            rendered_prompt=rendered_prompt,
            voice_name=voice_name,
            attempts_used=1,
        )


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
        failure_detail = build_blocked_failure(
            operation_name="text-to-speech generation",
            blocked_reason=str(blocked_reason),
        )
        raise TextToSpeechTransportError(
            failure_detail.message,
            raw_response=raw_response,
            failure_detail=failure_detail,
        )

    candidates = raw_response.get("candidates")
    if not isinstance(candidates, list) or not candidates:
        failure_detail = build_invalid_response_failure(
            operation_name="text-to-speech generation",
            detail="Gemini returned no candidates",
        )
        raise TextToSpeechTransportError(
            failure_detail.message,
            raw_response=raw_response,
            failure_detail=failure_detail,
        )

    candidate = candidates[0]
    parts = candidate.get("content", {}).get("parts", [])
    if not isinstance(parts, list) or not parts:
        failure_detail = build_invalid_response_failure(
            operation_name="text-to-speech generation",
            detail="Gemini returned no content parts",
        )
        raise TextToSpeechTransportError(
            failure_detail.message,
            raw_response=raw_response,
            failure_detail=failure_detail,
        )

    inline_data = None
    for part in parts:
        maybe_inline = part.get("inlineData")
        if isinstance(maybe_inline, dict):
            inline_data = maybe_inline
            break

    if inline_data is None:
        failure_detail = build_invalid_response_failure(
            operation_name="text-to-speech generation",
            detail="Gemini did not include inline audio data",
        )
        raise TextToSpeechTransportError(
            failure_detail.message,
            raw_response=raw_response,
            failure_detail=failure_detail,
        )

    encoded_audio = inline_data.get("data")
    if not isinstance(encoded_audio, str) or not encoded_audio.strip():
        failure_detail = build_invalid_response_failure(
            operation_name="text-to-speech generation",
            detail="Gemini returned an empty inline audio payload",
        )
        raise TextToSpeechTransportError(
            failure_detail.message,
            raw_response=raw_response,
            failure_detail=failure_detail,
        )

    try:
        pcm_audio_bytes = base64.b64decode(encoded_audio, validate=True)
    except (ValueError, binascii.Error) as exc:
        failure_detail = build_invalid_response_failure(
            operation_name="text-to-speech generation",
            detail="Gemini returned invalid base64 audio data",
        )
        raise TextToSpeechTransportError(
            failure_detail.message,
            raw_response=raw_response,
            failure_detail=failure_detail,
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

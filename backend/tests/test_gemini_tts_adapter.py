from __future__ import annotations

import base64
import json

import httpx
import pytest
from app.ai import GeminiTextToSpeechAdapter, render_gemini_tts_prompt
from app.ai.gemini_resilience import GeminiFailureKind, GeminiRetryNotice
from app.ai.gemini_tts import NarrationSynthesisRequest, TextToSpeechTransportError
from app.models.audio_settings import AudioNarrationStyle, AudioVoiceKey


def _build_request() -> NarrationSynthesisRequest:
    return NarrationSynthesisRequest(
        text="Mira followed the lantern home and felt the harbor settle around her.",
        voice_key=AudioVoiceKey.MOONBEAM,
        narration_style=AudioNarrationStyle.HUSHED,
        playback_speed=0.9,
        guidance_notes="Keep the protagonist name crisp and land the last sentence softly.",
    )


def test_render_gemini_tts_prompt_includes_bedtime_guardrails_and_controls() -> None:
    prompt = render_gemini_tts_prompt(_build_request())

    assert "Read the bedtime-story passage exactly as written." in prompt
    assert "Do not add titles, scene labels, ad-libs, paraphrases" in prompt
    assert "- Use the Achernar voice." in prompt
    assert "Keep the delivery hushed and intimate" in prompt
    assert "Target pacing: about 0.9x." in prompt
    assert "Keep the protagonist name crisp" in prompt
    assert "Mira followed the lantern home" in prompt


def test_gemini_tts_adapter_requests_audio_generation_and_decodes_pcm_response() -> None:
    seen_request: dict[str, object] = {}
    pcm_audio = (b"\x01\x02" * 40) + (b"\x03\x04" * 40)

    def handler(request: httpx.Request) -> httpx.Response:
        seen_request["url"] = str(request.url)
        seen_request["headers"] = dict(request.headers)
        seen_request["body"] = json.loads(request.content.decode("utf-8"))
        return httpx.Response(
            200,
            json={
                "responseId": "resp-tts-1",
                "modelVersion": "gemini-2.5-flash-preview-tts-001",
                "usageMetadata": {"totalTokenCount": 123},
                "candidates": [
                    {
                        "finishReason": "STOP",
                        "content": {
                            "parts": [
                                {
                                    "inlineData": {
                                        "mimeType": "audio/L16;rate=24000",
                                        "data": base64.b64encode(pcm_audio).decode("utf-8"),
                                    }
                                }
                            ]
                        },
                    }
                ],
            },
        )

    adapter = GeminiTextToSpeechAdapter(
        credential="test-key",
        model_id="gemini-2.5-flash-preview-tts",
        retry_backoff_seconds=0,
        client=httpx.Client(transport=httpx.MockTransport(handler)),
    )

    result = adapter.synthesize(_build_request())

    request_body = seen_request["body"]
    assert isinstance(request_body, dict)
    assert seen_request["url"] == (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        "gemini-2.5-flash-preview-tts:generateContent"
    )
    assert seen_request["headers"]["x-goog-api-key"] == "test-key"
    assert request_body["generationConfig"]["responseModalities"] == ["AUDIO"]
    assert (
        request_body["generationConfig"]["speechConfig"]["voiceConfig"]["prebuiltVoiceConfig"][
            "voiceName"
        ]
        == "Achernar"
    )
    assert "Mira followed the lantern home" in request_body["contents"][0]["parts"][0]["text"]
    assert result.pcm_audio_bytes == pcm_audio
    assert result.sample_rate_hz == 24_000
    assert result.voice_name == "Achernar"
    assert result.attempts_used == 1
    assert result.response_metadata == {
        "attempts_used": 1,
        "finish_reason": "STOP",
        "safety_ratings": None,
        "usage_metadata": {"totalTokenCount": 123},
        "model_version": "gemini-2.5-flash-preview-tts-001",
        "response_id": "resp-tts-1",
    }

    adapter.close()


def test_gemini_tts_adapter_retries_retryable_failures_before_succeeding() -> None:
    attempts = {"count": 0}

    def handler(_request: httpx.Request) -> httpx.Response:
        attempts["count"] += 1
        if attempts["count"] == 1:
            return httpx.Response(503, json={"error": {"message": "backend unavailable"}})
        return httpx.Response(
            200,
            json={
                "candidates": [
                    {
                        "finishReason": "STOP",
                        "content": {
                            "parts": [
                                {
                                    "inlineData": {
                                        "data": base64.b64encode(b"\x00\x00" * 32).decode("utf-8")
                                    }
                                }
                            ]
                        },
                    }
                ]
            },
        )

    adapter = GeminiTextToSpeechAdapter(
        credential="test-key",
        model_id="gemini-2.5-flash-preview-tts",
        retry_backoff_seconds=0,
        client=httpx.Client(transport=httpx.MockTransport(handler)),
    )

    result = adapter.synthesize(_build_request())

    assert attempts["count"] == 2
    assert result.attempts_used == 2
    adapter.close()


def test_gemini_tts_adapter_emits_retry_notices_for_transient_failures() -> None:
    attempts = {"count": 0}
    notices: list[GeminiRetryNotice] = []

    def handler(_request: httpx.Request) -> httpx.Response:
        attempts["count"] += 1
        if attempts["count"] == 1:
            return httpx.Response(
                503,
                json={"error": {"message": "backend unavailable"}},
            )
        return httpx.Response(
            200,
            json={
                "candidates": [
                    {
                        "finishReason": "STOP",
                        "content": {
                            "parts": [
                                {
                                    "inlineData": {
                                        "data": base64.b64encode(b"\x00\x00" * 32).decode("utf-8")
                                    }
                                }
                            ]
                        },
                    }
                ]
            },
        )

    adapter = GeminiTextToSpeechAdapter(
        credential="test-key",
        model_id="gemini-2.5-flash-preview-tts",
        retry_backoff_seconds=0,
        retry_notifier=notices.append,
        client=httpx.Client(transport=httpx.MockTransport(handler)),
    )

    result = adapter.synthesize(_build_request())

    assert result.attempts_used == 2
    assert [(notice.failed_attempt, notice.next_attempt) for notice in notices] == [(1, 2)]
    assert notices[0].failure.kind == GeminiFailureKind.TRANSIENT
    assert notices[0].delay_seconds == 0
    adapter.close()


def test_gemini_tts_adapter_does_not_retry_quota_exhaustion() -> None:
    attempts = {"count": 0}

    def handler(_request: httpx.Request) -> httpx.Response:
        attempts["count"] += 1
        return httpx.Response(
            429,
            json={
                "error": {
                    "status": "RESOURCE_EXHAUSTED",
                    "message": (
                        "You exceeded your current quota. Check plan and billing details."
                    ),
                }
            },
        )

    adapter = GeminiTextToSpeechAdapter(
        credential="test-key",
        model_id="gemini-2.5-flash-preview-tts",
        retry_backoff_seconds=0,
        client=httpx.Client(transport=httpx.MockTransport(handler)),
    )

    with pytest.raises(TextToSpeechTransportError) as exc_info:
        adapter.synthesize(_build_request())

    assert attempts["count"] == 1
    assert exc_info.value.failure_detail is not None
    assert exc_info.value.failure_detail.kind == GeminiFailureKind.QUOTA_EXHAUSTED
    assert exc_info.value.failure_detail.retryable is False
    assert exc_info.value.failure_detail.user_action_required is True
    adapter.close()


def test_gemini_tts_adapter_raises_clear_error_for_missing_audio_payload() -> None:
    adapter = GeminiTextToSpeechAdapter(
        credential="test-key",
        model_id="gemini-2.5-flash-preview-tts",
        retry_backoff_seconds=0,
        client=httpx.Client(
            transport=httpx.MockTransport(
                lambda _request: httpx.Response(
                    200,
                    json={
                        "candidates": [
                            {
                                "content": {"parts": [{"text": "not audio"}]},
                            }
                        ]
                    },
                )
            )
        ),
    )

    with pytest.raises(TextToSpeechTransportError) as exc_info:
        adapter.synthesize(_build_request())

    assert "inline audio data" in str(exc_info.value)
    adapter.close()

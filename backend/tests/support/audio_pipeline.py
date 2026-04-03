from __future__ import annotations

from collections.abc import Sequence

from app.ai import NarrationSynthesisResult, TextToSpeechTransportError


def build_synthesis_result(
    *,
    sample_value: int = 1,
    sample_frames: int = 2400,
    provider: str = "gemini",
    model_id: str = "test-gemini-tts",
    prompt_version: str = "test-gemini-tts.v1",
    rendered_prompt: str = "Prompt for test narration.",
    voice_name: str = "TestVoice",
    sample_rate_hz: int = 24_000,
    channel_count: int = 1,
    sample_width_bytes: int = 2,
    attempts_used: int = 1,
    raw_response: dict[str, object] | None = None,
    response_metadata: dict[str, object] | None = None,
) -> NarrationSynthesisResult:
    sample_byte = sample_value % 256
    pcm_frame = bytes([sample_byte]) * (channel_count * sample_width_bytes)
    pcm_audio = pcm_frame * sample_frames
    return NarrationSynthesisResult(
        pcm_audio_bytes=pcm_audio,
        provider=provider,
        model_id=model_id,
        prompt_version=prompt_version,
        rendered_prompt=rendered_prompt,
        voice_name=voice_name,
        provider_mime_type=f"audio/L16;rate={sample_rate_hz}",
        sample_rate_hz=sample_rate_hz,
        channel_count=channel_count,
        sample_width_bytes=sample_width_bytes,
        attempts_used=attempts_used,
        raw_response=raw_response or {"usageMetadata": {"totalTokenCount": 7}},
        response_metadata=response_metadata or {"attempts_used": attempts_used},
    )


class SequenceTextToSpeechAdapter:
    def __init__(
        self,
        results: Sequence[NarrationSynthesisResult],
        *,
        fail_on_call: int | None = None,
    ) -> None:
        if not results:
            raise ValueError("results must not be empty")
        self._results = list(results)
        self.fail_on_call = fail_on_call
        self.calls: list[object] = []
        self.model_id = self._results[0].model_id

    def synthesize(self, request):
        self.calls.append(request)
        call_index = len(self.calls)
        if self.fail_on_call is not None and call_index == self.fail_on_call:
            raise TextToSpeechTransportError("Simulated Gemini TTS failure")
        result_index = min(call_index - 1, len(self._results) - 1)
        return self._results[result_index]

    def close(self) -> None:
        return None

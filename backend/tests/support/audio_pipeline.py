"""Shared audio-pipeline test helpers.

Notes on mocked versus real behavior:
- `RecordingTextToSpeechAdapter` mocks the provider boundary and returns deterministic PCM.
- `RecordingAudioMixer` and `FailingAudioMixer` mock optional ffmpeg-backed mixing.
- SQLAlchemy models, narration segmentation, WAV assembly, asset persistence, and event logging
  all run through the real application services.
- Service-level tests use `InMemoryObjectStorage` instead of the GCS HTTP adapter.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from datetime import datetime, timezone

from app.ai import NarrationSynthesisResult, TextToSpeechTransportError
from app.db import (
    CompositionJob,
    CompositionJobKind,
    CompositionSegment,
    JobStatus,
)
from app.models import WorkflowStage, WorkflowStageState
from app.services.audio_mixing import AudioMixingError, AudioMixResult
from app.services.audio_wave import wav_duration_seconds
from app.services.sessions import SessionService
from app.settings import get_settings
from sqlalchemy.orm import Session
from tests.support.in_memory_storage import InMemoryObjectStorage


@dataclass(frozen=True)
class AudioReadySessionSeed:
    session_id: str
    composition_job_id: str


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


class RecordingTextToSpeechAdapter:
    def __init__(
        self,
        *,
        fail_on_calls: Sequence[int] = (),
        sample_frames: int = 2_400,
        sample_rate_hz: int = 24_000,
        attempts_used: int = 1,
    ) -> None:
        self.fail_on_calls = set(fail_on_calls)
        self.sample_frames = sample_frames
        self.sample_rate_hz = sample_rate_hz
        self.attempts_used = attempts_used
        self.model_id = "test-gemini-tts"
        self.calls = []

    def synthesize(self, request):
        self.calls.append(request)
        call_number = len(self.calls)
        if call_number in self.fail_on_calls:
            raise TextToSpeechTransportError(
                f"Simulated Gemini TTS failure on call {call_number}.",
            )

        return build_synthesis_result(
            sample_value=call_number,
            sample_frames=self.sample_frames,
            sample_rate_hz=self.sample_rate_hz,
            attempts_used=self.attempts_used,
            model_id=self.model_id,
            rendered_prompt=f"Prompt for segment {call_number}",
            response_metadata={"attempts_used": self.attempts_used},
        )

    def close(self) -> None:
        return None


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


class RecordingAudioMixer:
    def __init__(self) -> None:
        self.calls: list[tuple[bytes, object]] = []

    def mix(self, narration_wav_bytes: bytes, *, plan) -> AudioMixResult:
        self.calls.append((narration_wav_bytes, plan))
        return AudioMixResult(
            mixed_wav_bytes=narration_wav_bytes,
            output_duration_seconds=wav_duration_seconds(narration_wav_bytes),
            ffmpeg_command="ffmpeg-test -filter_complex sidechaincompress",
        )


class FailingAudioMixer:
    def __init__(self, message: str) -> None:
        self.message = message
        self.calls: list[tuple[bytes, object]] = []

    def mix(self, narration_wav_bytes: bytes, *, plan) -> AudioMixResult:
        self.calls.append((narration_wav_bytes, plan))
        raise AudioMixingError(self.message)


def build_in_memory_object_storage() -> InMemoryObjectStorage:
    return InMemoryObjectStorage(get_settings())


def build_audio_ready_session(
    session: Session,
    *,
    chapter_texts: Sequence[str],
    working_title: str = "Moonlit Harbor",
    audio_stage_in_progress: bool = True,
) -> AudioReadySessionSeed:
    now = datetime.now(timezone.utc)
    service = SessionService(session)
    snapshot = service.create_session(working_title=working_title)

    for stage in (
        WorkflowStage.GENRE,
        WorkflowStage.TONE,
        WorkflowStage.BRIEF,
        WorkflowStage.PITCHES,
        WorkflowStage.CHARACTERS,
        WorkflowStage.BEATS,
        WorkflowStage.STORY_SETUP,
        WorkflowStage.COMPOSITION,
    ):
        service.update_stage_state(
            snapshot.id,
            stage=stage,
            status=WorkflowStageState.COMPLETED,
        )

    if audio_stage_in_progress:
        service.update_stage_state(
            snapshot.id,
            stage=WorkflowStage.AUDIO,
            status=WorkflowStageState.IN_PROGRESS,
        )

    composition_job = CompositionJob(
        session_id=snapshot.id,
        job_kind=CompositionJobKind.DRAFT,
        status=JobStatus.COMPLETED,
        progress_percent=100,
        current_segment_index=len(chapter_texts) if chapter_texts else None,
        started_at=now,
        completed_at=now,
    )
    session.add(composition_job)
    session.flush()

    for index, text in enumerate(chapter_texts, start=1):
        normalized_text = text.strip()
        session.add(
            CompositionSegment(
                session_id=snapshot.id,
                composition_job_id=composition_job.id,
                segment_index=index,
                revision_number=1,
                status=JobStatus.COMPLETED,
                accepted_text=normalized_text,
                text_content=normalized_text,
                word_count=len(normalized_text.split()),
                payload={
                    "outline_kind": "chapter",
                    "outline_card_key": f"chapter-{index}",
                    "outline_card_title": f"Chapter {index}",
                },
                completed_at=now,
            )
        )

    session.commit()
    return AudioReadySessionSeed(
        session_id=snapshot.id,
        composition_job_id=composition_job.id,
    )

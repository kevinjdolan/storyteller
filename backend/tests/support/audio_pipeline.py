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

from app.ai import (
    NarrationSynthesisResult,
    TextToSpeechTransportError,
)
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

        sample_value = call_number % 256
        pcm_audio = bytes([sample_value, 0]) * self.sample_frames
        return NarrationSynthesisResult(
            pcm_audio_bytes=pcm_audio,
            provider="gemini",
            model_id=self.model_id,
            prompt_version="test-gemini-tts.v1",
            rendered_prompt=f"Prompt for segment {call_number}",
            voice_name="TestVoice",
            provider_mime_type=f"audio/L16;rate={self.sample_rate_hz}",
            sample_rate_hz=self.sample_rate_hz,
            channel_count=1,
            sample_width_bytes=2,
            attempts_used=self.attempts_used,
            raw_response={"usageMetadata": {"totalTokenCount": 7}},
            response_metadata={"attempts_used": self.attempts_used},
        )

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

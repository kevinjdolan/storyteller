from __future__ import annotations

import hashlib
import io
import wave
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from time import perf_counter
from typing import Any

from sqlalchemy import Select, select
from sqlalchemy.orm import Session

from app.ai import (
    GEMINI_TTS_PROMPT_VERSION,
    GeminiTextToSpeechAdapter,
    NarrationSynthesisRequest,
    NarrationSynthesisResult,
    NarrationTextToSpeechAdapter,
    TextToSpeechTransportError,
)
from app.db import (
    AssetKind,
    AssetStatus,
    AudioJob,
    BackgroundJob,
    JobStatus,
    NarrationSegment,
    SessionAsset,
)
from app.db.base import utc_now
from app.models import (
    AudioSettingsView,
    ModelCallOutcome,
    ModelUsageBucket,
    SessionEventActor,
    WorkflowStage,
    WorkflowStageState,
)
from app.models.audio_settings import AudioNarrationStyle, AudioVoiceKey
from app.services.assets import SessionAssetService
from app.services.audio_mixing import AudioMixingError, AudioMixResult, FfmpegAudioMixer
from app.services.audio_music import build_audio_mix_plan, deserialize_audio_mix_plan
from app.services.event_log import DEFAULT_SYSTEM_ACTOR, SessionEventLogService
from app.services.jobs import BackgroundJobService
from app.services.model_usage import ModelUsageContext, SessionModelUsageService
from app.services.narration_segmentation import (
    NarrationSegmentationError,
    NarrationSegmentationService,
)
from app.services.sessions import SessionService
from app.settings import get_settings
from app.storage import ObjectStorageService, build_object_storage_service

AUDIO_RUNTIME_JOB_TYPE = "story.run_audio_job"
_AUDIO_SEGMENT_EXTENSION = "wav"
_AUDIO_FINAL_EXTENSION = "wav"
_AUDIO_FINAL_FILE_STEM = "story"
_AUDIO_SEGMENT_PROGRESS_CEILING = 86.0
_AUDIO_ASSEMBLY_PROGRESS = 90.0
_AUDIO_MIX_PROGRESS = 96.0
_AUDIO_PUBLISH_PROGRESS = 99.0


class AudioJobServiceError(Exception):
    """Base error for durable narration orchestration failures."""


class AudioJobNotFoundError(AudioJobServiceError):
    """Raised when an audio job cannot be resolved."""


class AudioJobStateError(AudioJobServiceError):
    """Raised when an audio job transition is invalid."""


@dataclass(frozen=True)
class AudioJobStartResult:
    job: AudioJob
    first_segment: NarrationSegment
    total_segments: int


@dataclass(frozen=True)
class _RenderedNarrationSegment:
    segment: NarrationSegment
    synthesis: NarrationSynthesisResult


class AudioJobService:
    def __init__(
        self,
        session: Session,
        *,
        object_storage: ObjectStorageService | None = None,
        tts_adapter: NarrationTextToSpeechAdapter | None = None,
        audio_mixer: FfmpegAudioMixer | None = None,
    ) -> None:
        self._session = session
        self._events = SessionEventLogService(session)
        self._jobs = BackgroundJobService(session)
        self._assets = SessionAssetService(session)
        self._sessions = SessionService(session)
        self._object_storage = object_storage
        self._tts_adapter = tts_adapter
        self._audio_mixer = audio_mixer

    def start_job(
        self,
        session_id: str,
        *,
        settings: AudioSettingsView,
        estimated_duration_seconds: int | None,
        source_composition_job_id: str | None,
        actor: SessionEventActor | None = None,
    ) -> AudioJobStartResult:
        settings_config = get_settings()
        mix_plan = build_audio_mix_plan(settings)
        job = AudioJob(
            session_id=session_id,
            source_composition_job_id=source_composition_job_id,
            status=JobStatus.QUEUED,
            voice_key=settings.voice_key.value,
            playback_speed=settings.playback_speed,
            include_background_music=settings.include_background_music,
            music_profile=settings.music_profile.value,
            estimated_duration_seconds=estimated_duration_seconds,
            current_segment_index=1,
            config_json={
                "orchestration_version": "audio_job.v1",
                "tts_provider": "gemini",
                "tts_model_id": settings_config.gemini.tts_model,
                "voice_key": settings.voice_key.value,
                "narration_style": settings.narration_style.value,
                "playback_speed": settings.playback_speed,
                "include_background_music": settings.include_background_music,
                "music_profile": settings.music_profile.value,
                "narration_volume": settings.narration_volume,
                "music_volume": settings.music_volume,
                "guidance_notes": settings.guidance_notes,
                "music_mix": mix_plan.to_config_json(),
            },
        )
        self._session.add(job)
        self._session.flush()

        try:
            narration_plan = NarrationSegmentationService(self._session).create_plan(
                session_id=session_id,
                audio_job_id=job.id,
            )
        except NarrationSegmentationError as exc:
            raise AudioJobStateError(str(exc)) from exc

        first_segment = narration_plan.segments[0]
        total_segments = narration_plan.total_segments
        job.current_segment_index = first_segment.segment_index
        job.config_json = {
            **_read_mapping(job.config_json),
            "total_segments": total_segments,
            "total_steps": _build_total_steps(
                total_segments,
                include_mix_stage=mix_plan.should_mix,
            ),
            "completed_segments": 0,
            "progress_percent": 0.0,
            "current_step": _build_queued_audio_message(total_segments),
            "current_step_index": 1,
            "planned_word_count": narration_plan.total_words,
            "compiled_text_length": narration_plan.compiled_text_length,
            "narration_plan_version": "narration_segments.v1",
            "current_segment_id": first_segment.id,
        }
        self._supersede_final_audio_assets(session_id)
        self._record_job_progress(
            job=job,
            status=JobStatus.QUEUED,
            progress_percent=0,
            current_step=_build_queued_audio_message(total_segments),
            current_step_index=1,
            total_steps=_build_total_steps(
                total_segments,
                include_mix_stage=mix_plan.should_mix,
            ),
            completed_segments=0,
            current_segment_index=first_segment.segment_index,
            total_segments=total_segments,
            segment_id=first_segment.id,
            message=_build_queued_audio_message(total_segments),
            actor=actor or DEFAULT_SYSTEM_ACTOR,
        )
        self._enqueue_runtime_job(session_id, job.id)
        self._session.refresh(job)
        self._session.refresh(first_segment)
        return AudioJobStartResult(
            job=job,
            first_segment=first_segment,
            total_segments=total_segments,
        )

    def run_job(
        self,
        audio_job_id: str,
        *,
        actor: SessionEventActor | None = None,
    ) -> dict[str, Any]:
        job = self._session.get(AudioJob, audio_job_id)
        if job is None:
            raise AudioJobNotFoundError(f"audio job {audio_job_id!r} was not found")
        if job.status in {JobStatus.CANCELLED, JobStatus.COMPLETED}:
            raise AudioJobStateError(
                f"audio job {audio_job_id!r} is already {job.status.value}",
            )

        segments = self._load_narration_segments(audio_job_id)
        if not segments:
            raise AudioJobStateError("audio job has no narration segments to render")

        total_segments = len(segments)
        adapter, owns_adapter = self._resolve_tts_adapter()
        try:
            try:
                if job.started_at is not None:
                    job.attempt_count += 1
                job.status = JobStatus.IN_PROGRESS
                job.started_at = job.started_at or utc_now()
                job.error_message = None
                job.stop_reason = None
                self._session.commit()

                rendered_segments: list[_RenderedNarrationSegment] = []
                mix_plan = self._read_audio_mix_plan(job)
                total_steps = _read_total_steps(job) or _build_total_steps(
                    total_segments,
                    include_mix_stage=mix_plan.should_mix,
                )
                for segment in segments:
                    if segment.status == JobStatus.COMPLETED:
                        rendered_segments.append(
                            _RenderedNarrationSegment(
                                segment=segment,
                                synthesis=self._load_completed_segment_audio(job, segment),
                            )
                        )
                        continue
                    if segment.status == JobStatus.CANCELLED:
                        continue

                    job.current_segment_index = segment.segment_index
                    segment_attempt_count = _increment_segment_attempt_count(segment)
                    job.config_json = {
                        **_read_mapping(job.config_json),
                        "current_segment_id": segment.id,
                    }
                    segment.status = JobStatus.IN_PROGRESS
                    segment.error_message = None
                    render_message = _build_rendering_segment_message(
                        segment.segment_index,
                        total_segments,
                        attempt_count=segment_attempt_count,
                    )
                    self._record_job_progress(
                        job=job,
                        status=JobStatus.IN_PROGRESS,
                        progress_percent=_segment_progress_percent(
                            len(rendered_segments),
                            total_segments,
                        ),
                        current_step=render_message,
                        current_step_index=segment.segment_index,
                        total_steps=total_steps,
                        completed_segments=len(rendered_segments),
                        current_segment_index=segment.segment_index,
                        total_segments=total_segments,
                        segment_id=segment.id,
                        message=render_message,
                        actor=actor or DEFAULT_SYSTEM_ACTOR,
                    )
                    self._session.commit()

                    synthesis_started_at = perf_counter()
                    try:
                        synthesis = adapter.synthesize(
                            NarrationSynthesisRequest(
                                text=segment.text_content,
                                voice_key=_coerce_voice_key(job.voice_key),
                                narration_style=_coerce_narration_style(
                                    _read_mapping(job.config_json).get("narration_style")
                                ),
                                playback_speed=float(job.playback_speed or 1.0),
                                guidance_notes=_read_optional_text(
                                    _read_mapping(job.config_json).get("guidance_notes")
                                ),
                            )
                        )
                        self._record_model_usage(
                            job=job,
                            segment=segment,
                            elapsed_ms=_elapsed_ms_since(synthesis_started_at),
                            outcome=ModelCallOutcome.SUCCEEDED,
                            raw_response=synthesis.raw_response,
                        )
                    except TextToSpeechTransportError as exc:
                        self._record_model_usage(
                            job=job,
                            segment=segment,
                            elapsed_ms=_elapsed_ms_since(synthesis_started_at),
                            outcome=ModelCallOutcome.FAILED,
                            raw_response=exc.raw_response,
                            error_message=str(exc),
                        )
                        raise

                    rendered_segments.append(
                        _RenderedNarrationSegment(segment=segment, synthesis=synthesis)
                    )
                    segment_asset = self._persist_rendered_segment(
                        job=job,
                        segment=segment,
                        synthesis=synthesis,
                    )
                    segment_ready_message = _build_segment_saved_message(
                        segment.segment_index,
                        total_segments,
                    )
                    self._record_job_progress(
                        job=job,
                        status=JobStatus.IN_PROGRESS,
                        progress_percent=_segment_progress_percent(
                            len(rendered_segments),
                            total_segments,
                        ),
                        current_step=segment_ready_message,
                        current_step_index=segment.segment_index,
                        total_steps=total_steps,
                        completed_segments=len(rendered_segments),
                        current_segment_index=segment.segment_index,
                        total_segments=total_segments,
                        segment_id=segment.id,
                        latest_asset_id=segment_asset.id,
                        latest_asset_kind=segment_asset.asset_kind,
                        message=segment_ready_message,
                        actor=actor or DEFAULT_SYSTEM_ACTOR,
                    )
                    self._session.commit()

                final_result = self._persist_final_audio(
                    job=job,
                    rendered_segments=rendered_segments,
                    total_steps=total_steps,
                    total_segments=total_segments,
                    actor=actor or DEFAULT_SYSTEM_ACTOR,
                )
                job.status = JobStatus.COMPLETED
                job.completed_at = utc_now()
                job.error_message = None
                job.config_json = {
                    **_read_mapping(job.config_json),
                    "completed_segments": len(rendered_segments),
                    "progress_percent": 100.0,
                    "current_step": final_result["message"],
                    "current_step_index": total_steps,
                    "actual_duration_seconds": final_result["duration_seconds"],
                    "final_audio_asset_id": final_result["asset_id"],
                    "final_audio_object_path": final_result["object_path"],
                    "mix_strategy": final_result["mix_strategy"],
                    "mix_applied": final_result["mix_applied"],
                    "narration_master_object_path": final_result["narration_master_object_path"],
                    "latest_asset_id": final_result["asset_id"],
                    "latest_asset_kind": AssetKind.FINAL_AUDIO.value,
                }
                self._record_job_progress(
                    job=job,
                    status=JobStatus.COMPLETED,
                    progress_percent=100,
                    current_step=final_result["message"],
                    current_step_index=total_steps,
                    total_steps=total_steps,
                    completed_segments=len(rendered_segments),
                    current_segment_index=job.current_segment_index,
                    total_segments=total_segments,
                    latest_asset_id=final_result["asset_id"],
                    latest_asset_kind=AssetKind.FINAL_AUDIO.value,
                    message=final_result["message"],
                    actor=actor or DEFAULT_SYSTEM_ACTOR,
                )
                self._sessions.update_stage_state(
                    job.session_id,
                    stage=WorkflowStage.AUDIO,
                    status=WorkflowStageState.COMPLETED,
                    detail=final_result["message"],
                    actor=actor or DEFAULT_SYSTEM_ACTOR,
                )
                self._session.commit()
                return {
                    "audio_job_id": job.id,
                    "status": job.status.value,
                    "segments_completed": len(rendered_segments),
                    "total_segments": total_segments,
                    "final_asset_id": final_result["asset_id"],
                    "final_audio_object_path": final_result["object_path"],
                    "mix_applied": final_result["mix_applied"],
                    "mix_strategy": final_result["mix_strategy"],
                }
            except Exception as exc:
                if job.status not in {JobStatus.CANCELLED, JobStatus.FAILED}:
                    self.mark_job_failed(
                        audio_job_id,
                        error_message=str(exc).strip() or exc.__class__.__name__,
                        actor=actor,
                    )
                    self._session.commit()
                raise
        finally:
            if owns_adapter:
                adapter.close()

    def mark_job_failed(
        self,
        audio_job_id: str,
        *,
        error_message: str,
        actor: SessionEventActor | None = None,
    ) -> AudioJob:
        job = self._session.get(AudioJob, audio_job_id)
        if job is None:
            raise AudioJobNotFoundError(f"audio job {audio_job_id!r} was not found")

        current_segment = self._current_segment(job)
        job.status = JobStatus.FAILED
        job.error_message = error_message.strip()
        job.completed_at = None
        if current_segment is not None and current_segment.status == JobStatus.IN_PROGRESS:
            current_segment.status = JobStatus.FAILED
            current_segment.error_message = job.error_message
        failure_message = job.error_message
        current_step_index = _read_current_step_index(job)
        self._record_job_progress(
            job=job,
            status=JobStatus.FAILED,
            progress_percent=_segment_progress_percent(
                self._completed_segment_count(job.id),
                _read_total_segments(job) or 0,
            ),
            current_step=failure_message,
            current_step_index=current_step_index,
            total_steps=_read_total_steps(job),
            completed_segments=self._completed_segment_count(job.id),
            current_segment_index=job.current_segment_index,
            total_segments=_read_total_segments(job),
            segment_id=current_segment.id if current_segment is not None else None,
            message=failure_message,
            actor=actor or DEFAULT_SYSTEM_ACTOR,
        )
        self._sessions.update_stage_state(
            job.session_id,
            stage=WorkflowStage.AUDIO,
            status=WorkflowStageState.NEEDS_REGENERATION,
            detail=job.error_message,
            actor=actor or DEFAULT_SYSTEM_ACTOR,
        )
        return job

    def _persist_rendered_segment(
        self,
        *,
        job: AudioJob,
        segment: NarrationSegment,
        synthesis: NarrationSynthesisResult,
    ):
        wav_bytes = build_wav_bytes(
            synthesis.pcm_audio_bytes,
            sample_rate_hz=synthesis.sample_rate_hz,
            channel_count=synthesis.channel_count,
            sample_width_bytes=synthesis.sample_width_bytes,
        )
        location = self._storage().paths.audio_segment(
            session_id=job.session_id,
            job_id=job.id,
            segment_index=segment.segment_index,
            extension=_AUDIO_SEGMENT_EXTENSION,
        )
        metadata = self._storage().upload_bytes(
            location,
            wav_bytes,
            content_type="audio/wav",
        )
        checksum = hashlib.sha256(wav_bytes).hexdigest()
        asset = self._assets.upsert_asset_record(
            session_id=job.session_id,
            asset_kind=AssetKind.AUDIO_SEGMENT,
            storage_bucket=location.bucket,
            object_path=location.key,
            mime_type="audio/wav",
            status=AssetStatus.READY,
            audio_job_id=job.id,
            segment_index=segment.segment_index,
            byte_size=metadata.size_bytes,
            checksum_sha256=checksum,
            metadata_json={
                "orchestration_version": "audio_job_segment.v1",
                "provider": synthesis.provider,
                "model_id": synthesis.model_id,
                "prompt_version": synthesis.prompt_version,
                "voice_name": synthesis.voice_name,
                "provider_mime_type": synthesis.provider_mime_type,
                "sample_rate_hz": synthesis.sample_rate_hz,
                "channel_count": synthesis.channel_count,
                "sample_width_bytes": synthesis.sample_width_bytes,
                "attempts_used": synthesis.attempts_used,
                "pause_after_seconds": segment.pause_after_seconds,
                "response_metadata": synthesis.response_metadata,
            },
        )
        segment.status = JobStatus.COMPLETED
        segment.completed_at = utc_now()
        segment.error_message = None
        segment.metadata_json = {
            **_read_mapping(segment.metadata_json),
            "latest_asset_id": asset.id,
            "audio_asset_path": location.key,
            "audio_asset_bucket": location.bucket,
            "provider": synthesis.provider,
            "model_id": synthesis.model_id,
            "prompt_version": synthesis.prompt_version,
            "voice_name": synthesis.voice_name,
            "sample_rate_hz": synthesis.sample_rate_hz,
            "attempts_used": synthesis.attempts_used,
            "rendered_prompt": synthesis.rendered_prompt,
        }
        return asset

    def _persist_final_audio(
        self,
        *,
        job: AudioJob,
        rendered_segments: Sequence[_RenderedNarrationSegment],
        total_steps: int,
        total_segments: int,
        actor: SessionEventActor,
    ) -> dict[str, Any]:
        if not rendered_segments:
            raise AudioJobStateError("audio job completed without any rendered segments")

        first = rendered_segments[0].synthesis
        assembly_message = _build_assembly_message(len(rendered_segments))
        self._record_job_progress(
            job=job,
            status=JobStatus.IN_PROGRESS,
            progress_percent=_AUDIO_ASSEMBLY_PROGRESS,
            current_step=assembly_message,
            current_step_index=total_segments + 1,
            total_steps=total_steps,
            completed_segments=len(rendered_segments),
            current_segment_index=job.current_segment_index,
            total_segments=total_segments,
            message=assembly_message,
            actor=actor,
        )
        narration_master_wav_bytes = self._build_narration_master_wav(rendered_segments)
        mix_plan = self._read_audio_mix_plan(job)
        narration_master_location = None
        mix_result = AudioMixResult(
            mixed_wav_bytes=narration_master_wav_bytes,
            output_duration_seconds=_wav_duration_seconds(narration_master_wav_bytes),
            ffmpeg_command=None,
        )

        if mix_plan.should_mix:
            narration_master_location = self._persist_narration_master_debug_artifact(
                job=job,
                narration_master_wav_bytes=narration_master_wav_bytes,
            )
            mix_message = _build_mix_message(mix_plan.music_track_label)
            self._record_job_progress(
                job=job,
                status=JobStatus.IN_PROGRESS,
                progress_percent=_AUDIO_MIX_PROGRESS,
                current_step=mix_message,
                current_step_index=total_segments + 2,
                total_steps=total_steps,
                completed_segments=len(rendered_segments),
                current_segment_index=job.current_segment_index,
                total_segments=total_segments,
                message=mix_message,
                actor=actor,
            )
            try:
                mix_result = self._resolve_audio_mixer().mix(
                    narration_master_wav_bytes,
                    plan=mix_plan,
                )
            except AudioMixingError as exc:
                raise AudioJobStateError(str(exc)) from exc

        final_wav_bytes = mix_result.mixed_wav_bytes
        _, final_sample_rate_hz, final_channel_count, final_sample_width_bytes = read_wav_bytes(
            final_wav_bytes
        )
        publish_message = _build_publish_message()
        self._record_job_progress(
            job=job,
            status=JobStatus.IN_PROGRESS,
            progress_percent=_AUDIO_PUBLISH_PROGRESS,
            current_step=publish_message,
            current_step_index=total_steps,
            total_steps=total_steps,
            completed_segments=len(rendered_segments),
            current_segment_index=job.current_segment_index,
            total_segments=total_segments,
            message=publish_message,
            actor=actor,
        )
        location = self._storage().paths.final_audio(
            session_id=job.session_id,
            job_id=job.id,
            extension=_AUDIO_FINAL_EXTENSION,
            file_stem=_AUDIO_FINAL_FILE_STEM,
        )
        metadata = self._storage().upload_bytes(
            location,
            final_wav_bytes,
            content_type="audio/wav",
        )
        checksum = hashlib.sha256(final_wav_bytes).hexdigest()
        self._supersede_final_audio_assets(job.session_id)
        asset = self._assets.save_asset_record(
            session_id=job.session_id,
            asset_kind=AssetKind.FINAL_AUDIO,
            storage_bucket=location.bucket,
            object_path=location.key,
            mime_type="audio/wav",
            status=AssetStatus.READY,
            audio_job_id=job.id,
            byte_size=metadata.size_bytes,
            checksum_sha256=checksum,
            metadata_json={
                "orchestration_version": "audio_job_final.v1",
                "provider": first.provider,
                "model_id": first.model_id,
                "prompt_version": first.prompt_version,
                "voice_name": first.voice_name,
                "segment_count": len(rendered_segments),
                "include_background_music": job.include_background_music,
                "music_profile": job.music_profile,
                "sample_rate_hz": final_sample_rate_hz,
                "channel_count": final_channel_count,
                "sample_width_bytes": final_sample_width_bytes,
                "mix_strategy": mix_plan.strategy,
                "mix_summary": mix_plan.summary,
                "music_track_label": mix_plan.music_track_label,
                "music_track_description": mix_plan.music_track_description,
                "music_track_file_name": mix_plan.music_track_file_name,
                "narration_gain_db": mix_plan.narration_gain_db,
                "music_gain_db": mix_plan.music_gain_db,
                "ducking_ratio": mix_plan.ducking_ratio,
                "ducking_threshold": mix_plan.ducking_threshold,
                "ducking_attack_ms": mix_plan.ducking_attack_ms,
                "ducking_release_ms": mix_plan.ducking_release_ms,
                "fade_out_seconds": mix_plan.fade_out_seconds,
                "loop_duration_seconds": mix_plan.loop_duration_seconds,
                "pause_seconds_total": sum(
                    rendered.segment.pause_after_seconds for rendered in rendered_segments
                ),
                "narration_master_bucket": (
                    narration_master_location.bucket
                    if narration_master_location is not None
                    else None
                ),
                "narration_master_object_path": (
                    narration_master_location.key if narration_master_location is not None else None
                ),
                "ffmpeg_command": mix_result.ffmpeg_command,
            },
        )
        return {
            "asset_id": asset.id,
            "object_path": asset.object_path,
            "duration_seconds": round(mix_result.output_duration_seconds),
            "mix_applied": mix_plan.should_mix,
            "mix_strategy": mix_plan.strategy,
            "narration_master_object_path": (
                narration_master_location.key if narration_master_location is not None else None
            ),
            "message": (
                "Narration finished and the final mixed audio asset is ready."
                if mix_plan.should_mix
                else "Narration finished and the final audio asset is ready."
            ),
        }

    def _load_completed_segment_audio(
        self,
        job: AudioJob,
        segment: NarrationSegment,
    ) -> NarrationSynthesisResult:
        asset = self._find_ready_segment_asset(job.id, segment.segment_index)
        if asset is None:
            raise AudioJobStateError(
                f"segment {segment.segment_index} is marked completed but its asset is missing",
            )
        wav_bytes = self._storage().download_bytes(
            self._storage().paths.audio_segment(
                session_id=job.session_id,
                job_id=job.id,
                segment_index=segment.segment_index,
                extension=_AUDIO_SEGMENT_EXTENSION,
            )
        )
        pcm_bytes, sample_rate_hz, channel_count, sample_width_bytes = read_wav_bytes(wav_bytes)
        segment_metadata = _read_mapping(segment.metadata_json)
        return NarrationSynthesisResult(
            pcm_audio_bytes=pcm_bytes,
            provider=str(segment_metadata.get("provider") or "gemini"),
            model_id=str(
                segment_metadata.get("model_id")
                or _read_mapping(job.config_json).get("tts_model_id")
                or ""
            ),
            prompt_version=str(
                segment_metadata.get("prompt_version") or GEMINI_TTS_PROMPT_VERSION
            ),
            rendered_prompt=str(segment_metadata.get("rendered_prompt") or ""),
            voice_name=str(segment_metadata.get("voice_name") or ""),
            provider_mime_type="audio/wav",
            sample_rate_hz=sample_rate_hz,
            channel_count=channel_count,
            sample_width_bytes=sample_width_bytes,
            attempts_used=int(segment_metadata.get("attempts_used") or 1),
            response_metadata=_read_mapping(segment_metadata.get("response_metadata")),
        )

    def _record_model_usage(
        self,
        *,
        job: AudioJob,
        segment: NarrationSegment,
        elapsed_ms: int,
        outcome: ModelCallOutcome,
        raw_response: Mapping[str, Any] | list[Any] | str | None,
        error_message: str | None = None,
    ) -> None:
        SessionModelUsageService(self._session).record_model_call(
            context=ModelUsageContext(
                session_id=job.session_id,
                usage_bucket=ModelUsageBucket.AUDIO,
                purpose=f"audio_segment_synthesis:{segment.segment_index}",
                model_id=str(_read_mapping(job.config_json).get("tts_model_id") or ""),
                workflow_stage=WorkflowStage.AUDIO,
                prompt_version=GEMINI_TTS_PROMPT_VERSION,
            ),
            elapsed_ms=elapsed_ms,
            outcome=outcome,
            raw_response=raw_response,
            error_message=error_message,
        )

    def _current_segment(self, job: AudioJob) -> NarrationSegment | None:
        if job.current_segment_index is None:
            return None
        stmt: Select[tuple[NarrationSegment]] = (
            select(NarrationSegment)
            .where(
                NarrationSegment.audio_job_id == job.id,
                NarrationSegment.segment_index == job.current_segment_index,
            )
            .limit(1)
        )
        return self._session.execute(stmt).scalar_one_or_none()

    def _find_ready_segment_asset(
        self,
        audio_job_id: str,
        segment_index: int,
    ) -> SessionAsset | None:
        stmt: Select[tuple[SessionAsset]] = (
            select(SessionAsset)
            .where(
                SessionAsset.audio_job_id == audio_job_id,
                SessionAsset.asset_kind == AssetKind.AUDIO_SEGMENT,
                SessionAsset.segment_index == segment_index,
                SessionAsset.status == AssetStatus.READY,
            )
            .order_by(SessionAsset.ready_at.desc(), SessionAsset.created_at.desc())
            .limit(1)
        )
        return self._session.execute(stmt).scalar_one_or_none()

    def _load_narration_segments(self, audio_job_id: str) -> list[NarrationSegment]:
        stmt: Select[tuple[NarrationSegment]] = (
            select(NarrationSegment)
            .where(NarrationSegment.audio_job_id == audio_job_id)
            .order_by(NarrationSegment.segment_index.asc())
        )
        return list(self._session.execute(stmt).scalars().all())

    def _completed_segment_count(self, audio_job_id: str) -> int:
        return sum(
            1
            for segment in self._load_narration_segments(audio_job_id)
            if segment.status == JobStatus.COMPLETED
        )

    def _build_narration_master_wav(
        self,
        rendered_segments: Sequence[_RenderedNarrationSegment],
    ) -> bytes:
        first = rendered_segments[0].synthesis
        final_pcm = bytearray()
        for rendered in rendered_segments:
            if rendered.synthesis.sample_rate_hz != first.sample_rate_hz:
                raise AudioJobStateError("audio segments must share a single sample rate")
            if rendered.synthesis.channel_count != first.channel_count:
                raise AudioJobStateError("audio segments must share a single channel layout")
            if rendered.synthesis.sample_width_bytes != first.sample_width_bytes:
                raise AudioJobStateError("audio segments must share a single sample width")
            final_pcm.extend(rendered.synthesis.pcm_audio_bytes)
            if rendered.segment.pause_after_seconds > 0:
                final_pcm.extend(
                    build_silence_pcm(
                        duration_seconds=rendered.segment.pause_after_seconds,
                        sample_rate_hz=rendered.synthesis.sample_rate_hz,
                        channel_count=rendered.synthesis.channel_count,
                        sample_width_bytes=rendered.synthesis.sample_width_bytes,
                    )
                )

        return build_wav_bytes(
            bytes(final_pcm),
            sample_rate_hz=first.sample_rate_hz,
            channel_count=first.channel_count,
            sample_width_bytes=first.sample_width_bytes,
        )

    def _persist_narration_master_debug_artifact(
        self,
        *,
        job: AudioJob,
        narration_master_wav_bytes: bytes,
    ):
        location = self._storage().paths.debug_artifact(
            session_id=job.session_id,
            artifact_group="audio-mix",
            artifact_name=f"{job.id}-narration-master",
            extension="wav",
        )
        self._storage().upload_bytes(
            location,
            narration_master_wav_bytes,
            content_type="audio/wav",
        )
        return location

    def _read_audio_mix_plan(self, job: AudioJob):
        config = _read_mapping(job.config_json)
        return deserialize_audio_mix_plan(config.get("music_mix"))

    def _resolve_tts_adapter(self) -> tuple[NarrationTextToSpeechAdapter, bool]:
        if self._tts_adapter is not None:
            return self._tts_adapter, False

        settings = get_settings()
        return (
            GeminiTextToSpeechAdapter(
                credential=settings.gemini_api_key,
                model_id=settings.gemini.tts_model,
            ),
            True,
        )

    def _resolve_audio_mixer(self) -> FfmpegAudioMixer:
        if self._audio_mixer is not None:
            return self._audio_mixer
        self._audio_mixer = FfmpegAudioMixer()
        return self._audio_mixer

    def _storage(self) -> ObjectStorageService:
        if self._object_storage is None:
            self._object_storage = build_object_storage_service(get_settings())
        return self._object_storage

    def _enqueue_runtime_job(self, session_id: str, audio_job_id: str) -> None:
        if self._has_pending_runtime_job(audio_job_id):
            return
        self._jobs.enqueue_job(
            job_type=AUDIO_RUNTIME_JOB_TYPE,
            payload={"audio_job_id": audio_job_id},
            session_id=session_id,
        )

    def _has_pending_runtime_job(self, audio_job_id: str) -> bool:
        stmt = select(BackgroundJob).where(
            BackgroundJob.job_type == AUDIO_RUNTIME_JOB_TYPE,
            BackgroundJob.status == JobStatus.QUEUED,
        )
        for row in self._session.execute(stmt).scalars().all():
            payload = row.payload if isinstance(row.payload, Mapping) else {}
            if payload.get("audio_job_id") == audio_job_id:
                return True
        return False

    def _supersede_final_audio_assets(self, session_id: str) -> None:
        stmt = select(SessionAsset).where(
            SessionAsset.session_id == session_id,
            SessionAsset.asset_kind == AssetKind.FINAL_AUDIO,
            SessionAsset.status == AssetStatus.READY,
        )
        for asset in self._session.execute(stmt).scalars().all():
            asset.status = AssetStatus.SUPERSEDED
            asset.superseded_at = utc_now()

    def _record_job_progress(
        self,
        *,
        job: AudioJob,
        status: JobStatus,
        progress_percent: float | None,
        current_step: str | None,
        current_step_index: int | None,
        total_steps: int | None,
        completed_segments: int | None,
        current_segment_index: int | None,
        total_segments: int | None,
        segment_id: str | None = None,
        latest_asset_id: str | None = None,
        latest_asset_kind: str | None = None,
        message: str | None = None,
        actor: SessionEventActor,
    ) -> None:
        job.current_segment_index = (
            current_segment_index
            if current_segment_index is not None
            else job.current_segment_index
        )
        existing_config = _read_mapping(job.config_json)
        job.config_json = {
            **existing_config,
            "progress_percent": progress_percent,
            "current_step": current_step,
            "current_step_index": current_step_index,
            "total_steps": total_steps,
            "completed_segments": completed_segments,
            "latest_asset_id": latest_asset_id or existing_config.get("latest_asset_id"),
            "latest_asset_kind": (
                latest_asset_kind or existing_config.get("latest_asset_kind")
            ),
            "current_segment_id": segment_id or existing_config.get("current_segment_id"),
        }
        self._events.record_audio_progress(
            job.session_id,
            job_id=job.id,
            status=status,
            progress_percent=progress_percent,
            current_step=current_step,
            current_step_index=current_step_index,
            total_steps=total_steps,
            completed_segments=completed_segments,
            current_segment_index=job.current_segment_index,
            total_segments=total_segments,
            segment_id=segment_id,
            latest_asset_id=latest_asset_id,
            latest_asset_kind=latest_asset_kind,
            estimated_duration_seconds=job.estimated_duration_seconds,
            voice_key=job.voice_key,
            message=message,
            actor=actor,
        )


def build_wav_bytes(
    pcm_audio_bytes: bytes,
    *,
    sample_rate_hz: int,
    channel_count: int,
    sample_width_bytes: int,
) -> bytes:
    buffer = io.BytesIO()
    with wave.open(buffer, "wb") as wav_file:
        wav_file.setnchannels(channel_count)
        wav_file.setsampwidth(sample_width_bytes)
        wav_file.setframerate(sample_rate_hz)
        wav_file.writeframes(pcm_audio_bytes)
    return buffer.getvalue()


def read_wav_bytes(wav_bytes: bytes) -> tuple[bytes, int, int, int]:
    with wave.open(io.BytesIO(wav_bytes), "rb") as wav_file:
        sample_rate_hz = wav_file.getframerate()
        channel_count = wav_file.getnchannels()
        sample_width_bytes = wav_file.getsampwidth()
        pcm_audio_bytes = wav_file.readframes(wav_file.getnframes())
    return pcm_audio_bytes, sample_rate_hz, channel_count, sample_width_bytes


def _wav_duration_seconds(wav_bytes: bytes) -> float:
    with wave.open(io.BytesIO(wav_bytes), "rb") as wav_file:
        frame_count = wav_file.getnframes()
        sample_rate_hz = wav_file.getframerate()
    if sample_rate_hz <= 0:
        raise AudioJobStateError("wav bytes must contain a valid sample rate")
    return round(frame_count / sample_rate_hz, 3)


def build_silence_pcm(
    *,
    duration_seconds: int,
    sample_rate_hz: int,
    channel_count: int,
    sample_width_bytes: int,
) -> bytes:
    frame_count = max(int(duration_seconds), 0) * sample_rate_hz
    return b"\x00" * frame_count * channel_count * sample_width_bytes


def _coerce_voice_key(value: str | AudioVoiceKey | None) -> AudioVoiceKey:
    if isinstance(value, AudioVoiceKey):
        return value
    normalized = str(value or AudioVoiceKey.MOONBEAM.value).strip()
    return AudioVoiceKey(normalized or AudioVoiceKey.MOONBEAM.value)


def _coerce_narration_style(value: Any) -> AudioNarrationStyle:
    if isinstance(value, AudioNarrationStyle):
        return value
    normalized = str(value or AudioNarrationStyle.CALM.value).strip()
    return AudioNarrationStyle(normalized or AudioNarrationStyle.CALM.value)


def _read_mapping(value: Any) -> dict[str, Any]:
    return dict(value) if isinstance(value, Mapping) else {}


def _read_optional_text(value: Any) -> str | None:
    if value is None:
        return None
    normalized = str(value).strip()
    return normalized or None


def _read_total_segments(job: AudioJob) -> int | None:
    total = _read_mapping(job.config_json).get("total_segments")
    if total is None:
        return None
    try:
        return int(total)
    except (TypeError, ValueError):
        return None


def _read_total_steps(job: AudioJob) -> int | None:
    total = _read_mapping(job.config_json).get("total_steps")
    if total is None:
        return None
    try:
        return int(total)
    except (TypeError, ValueError):
        return None


def _read_current_step_index(job: AudioJob) -> int | None:
    current_step_index = _read_mapping(job.config_json).get("current_step_index")
    if current_step_index is None:
        return None
    try:
        return int(current_step_index)
    except (TypeError, ValueError):
        return None


def _build_total_steps(total_segments: int, *, include_mix_stage: bool) -> int:
    base_steps = max(total_segments, 0) + 2
    if include_mix_stage:
        base_steps += 1
    return max(base_steps, 1)


def _segment_progress_percent(completed_segments: int, total_segments: int) -> float:
    if total_segments <= 0:
        return 0.0
    ratio = min(max(completed_segments / total_segments, 0.0), 1.0)
    return round(ratio * _AUDIO_SEGMENT_PROGRESS_CEILING, 1)


def _build_queued_audio_message(total_segments: int) -> str:
    return (
        f"Queued narration for {total_segments} segment"
        f"{'' if total_segments == 1 else 's'}."
    )


def _build_rendering_segment_message(
    segment_index: int,
    total_segments: int,
    *,
    attempt_count: int,
) -> str:
    attempt_suffix = f" (attempt {attempt_count})" if attempt_count > 1 else ""
    return (
        f"Rendering narration segment {segment_index} of {total_segments}"
        f"{attempt_suffix}."
    )


def _build_segment_saved_message(segment_index: int, total_segments: int) -> str:
    return f"Saved narration segment {segment_index} of {total_segments}."


def _build_assembly_message(total_segments: int) -> str:
    return (
        f"Assembling the narration master from {total_segments} rendered segment"
        f"{'' if total_segments == 1 else 's'}."
    )


def _build_mix_message(music_track_label: str | None) -> str:
    if music_track_label:
        return f"Mixing narration with {music_track_label.lower()}."
    return "Mixing narration with the selected background bed."


def _build_publish_message() -> str:
    return "Publishing the final audio asset."


def _increment_segment_attempt_count(segment: NarrationSegment) -> int:
    metadata = _read_mapping(segment.metadata_json)
    prior_attempts = metadata.get("render_attempt_count")
    if isinstance(prior_attempts, int):
        next_attempt = prior_attempts + 1
    else:
        next_attempt = 1
    segment.metadata_json = {
        **metadata,
        "render_attempt_count": next_attempt,
    }
    return next_attempt


def _elapsed_ms_since(started_at: float) -> int:
    return max(int(round((perf_counter() - started_at) * 1000)), 0)

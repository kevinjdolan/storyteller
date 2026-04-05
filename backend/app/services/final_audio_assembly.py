from __future__ import annotations

import hashlib
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any

from sqlalchemy import Select, select
from sqlalchemy.orm import Session

from app.ai import NarrationSynthesisResult
from app.db import AssetKind, AssetStatus, AudioJob, NarrationSegment, SessionAsset
from app.services.assets import SessionAssetService
from app.services.audio_mixing import AudioMixResult, FfmpegAudioMixer
from app.services.audio_music import AudioMixPlan
from app.services.audio_wave import (
    build_silence_pcm,
    build_wav_bytes,
    read_wav_bytes,
    wav_duration_seconds,
)
from app.settings import get_settings
from app.storage import (
    ObjectStorageService,
    StorageObjectLocation,
    build_object_storage_service,
)

_AUDIO_FINAL_EXTENSION = "wav"
_AUDIO_FINAL_FILE_STEM = "story"


class FinalAudioAssemblyError(Exception):
    """Raised when the final narration master cannot be assembled or published."""


@dataclass(frozen=True)
class RenderedNarrationSegment:
    segment: NarrationSegment
    synthesis: NarrationSynthesisResult


@dataclass(frozen=True)
class NarrationMasterBuildResult:
    wav_bytes: bytes
    duration_seconds: float
    sample_rate_hz: int
    channel_count: int
    sample_width_bytes: int
    pause_seconds_total: int
    segment_indexes: tuple[int, ...]


@dataclass(frozen=True)
class FinalAudioPublishResult:
    asset_id: str
    object_path: str
    duration_seconds: float
    mix_applied: bool
    mix_strategy: str
    narration_master_object_path: str | None
    message: str
    superseded_asset_ids: tuple[str, ...]


class FinalAudioAssemblyService:
    def __init__(
        self,
        session: Session,
        *,
        object_storage: ObjectStorageService | None = None,
        audio_mixer: FfmpegAudioMixer | None = None,
    ) -> None:
        self._session = session
        self._assets = SessionAssetService(session)
        self._object_storage = object_storage
        self._audio_mixer = audio_mixer

    def build_narration_master(
        self,
        rendered_segments: Sequence[RenderedNarrationSegment],
    ) -> NarrationMasterBuildResult:
        if not rendered_segments:
            raise FinalAudioAssemblyError(
                "audio job completed without any rendered narration segments",
            )

        first = rendered_segments[0].synthesis
        final_pcm = bytearray()
        pause_seconds_total = 0
        segment_indexes: list[int] = []
        for rendered in rendered_segments:
            if rendered.synthesis.sample_rate_hz != first.sample_rate_hz:
                raise FinalAudioAssemblyError(
                    "audio segments must share a single sample rate",
                )
            if rendered.synthesis.channel_count != first.channel_count:
                raise FinalAudioAssemblyError(
                    "audio segments must share a single channel layout",
                )
            if rendered.synthesis.sample_width_bytes != first.sample_width_bytes:
                raise FinalAudioAssemblyError(
                    "audio segments must share a single sample width",
                )
            final_pcm.extend(rendered.synthesis.pcm_audio_bytes)
            segment_indexes.append(rendered.segment.segment_index)
            if rendered.segment.pause_after_seconds > 0:
                pause_seconds_total += rendered.segment.pause_after_seconds
                final_pcm.extend(
                    build_silence_pcm(
                        duration_seconds=rendered.segment.pause_after_seconds,
                        sample_rate_hz=rendered.synthesis.sample_rate_hz,
                        channel_count=rendered.synthesis.channel_count,
                        sample_width_bytes=rendered.synthesis.sample_width_bytes,
                    )
                )

        wav_bytes = build_wav_bytes(
            bytes(final_pcm),
            sample_rate_hz=first.sample_rate_hz,
            channel_count=first.channel_count,
            sample_width_bytes=first.sample_width_bytes,
        )
        return NarrationMasterBuildResult(
            wav_bytes=wav_bytes,
            duration_seconds=wav_duration_seconds(wav_bytes),
            sample_rate_hz=first.sample_rate_hz,
            channel_count=first.channel_count,
            sample_width_bytes=first.sample_width_bytes,
            pause_seconds_total=pause_seconds_total,
            segment_indexes=tuple(segment_indexes),
        )

    def persist_narration_master_debug_artifact(
        self,
        *,
        job: AudioJob,
        narration_master_wav_bytes: bytes,
    ) -> StorageObjectLocation:
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

    def mix_narration_master(
        self,
        narration_master_wav_bytes: bytes,
        *,
        plan: AudioMixPlan,
    ) -> AudioMixResult:
        if not plan.should_mix:
            return AudioMixResult(
                mixed_wav_bytes=narration_master_wav_bytes,
                output_duration_seconds=wav_duration_seconds(narration_master_wav_bytes),
                ffmpeg_command=None,
            )

        return self._resolve_audio_mixer().mix(narration_master_wav_bytes, plan=plan)

    def publish_final_audio(
        self,
        *,
        job: AudioJob,
        rendered_segments: Sequence[RenderedNarrationSegment],
        narration_master: NarrationMasterBuildResult,
        mix_plan: AudioMixPlan,
        mix_result: AudioMixResult,
        narration_master_location: StorageObjectLocation | None,
    ) -> FinalAudioPublishResult:
        first = rendered_segments[0].synthesis
        final_wav_bytes = mix_result.mixed_wav_bytes
        _, final_sample_rate_hz, final_channel_count, final_sample_width_bytes = read_wav_bytes(
            final_wav_bytes
        )
        duration_seconds = round(mix_result.output_duration_seconds, 3)
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
        superseded_assets = self._list_ready_final_audio_assets(job.session_id)
        superseded_asset_ids = tuple(asset.id for asset in superseded_assets)

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
                "orchestration_version": "audio_job_final.v2",
                "duration_seconds": duration_seconds,
                "narration_master_duration_seconds": narration_master.duration_seconds,
                "segment_count": len(rendered_segments),
                "segment_indexes": list(narration_master.segment_indexes),
                "segment_timeline_version": "narration_segment_timeline.v1",
                "segment_timeline": _build_segment_timeline(rendered_segments),
                "pause_seconds_total": narration_master.pause_seconds_total,
                "estimated_duration_seconds": job.estimated_duration_seconds,
                "media": {
                    "sample_rate_hz": final_sample_rate_hz,
                    "channel_count": final_channel_count,
                    "sample_width_bytes": final_sample_width_bytes,
                    "mime_type": "audio/wav",
                },
                "generation": {
                    "audio_job_id": job.id,
                    "source_composition_job_id": job.source_composition_job_id,
                    "provider": first.provider,
                    "model_id": first.model_id,
                    "prompt_version": first.prompt_version,
                    "voice_key": job.voice_key,
                    "voice_name": first.voice_name,
                    "playback_speed": float(job.playback_speed or 1.0),
                    "tts_attempts_used": first.attempts_used,
                },
                "mix": {
                    "applied": mix_plan.should_mix,
                    "strategy": mix_plan.strategy,
                    "summary": mix_plan.summary,
                    "include_background_music": job.include_background_music,
                    "music_profile": job.music_profile,
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
                },
                "debug": {
                    "narration_master_bucket": (
                        narration_master_location.bucket
                        if narration_master_location is not None
                        else None
                    ),
                    "narration_master_object_path": (
                        narration_master_location.key
                        if narration_master_location is not None
                        else None
                    ),
                    "ffmpeg_command": mix_result.ffmpeg_command,
                },
                "supersedes_asset_ids": list(superseded_asset_ids),
            },
            commit=False,
        )
        self._assets.supersede_assets(
            job.session_id,
            asset_kinds=(AssetKind.FINAL_AUDIO,),
            exclude_asset_ids=(asset.id,),
            replacement_asset_id=asset.id,
            replacement_audio_job_id=job.id,
            reason="replaced_by_regenerated_audio",
            commit=False,
        )
        self._session.flush()

        return FinalAudioPublishResult(
            asset_id=asset.id,
            object_path=asset.object_path,
            duration_seconds=duration_seconds,
            mix_applied=mix_plan.should_mix,
            mix_strategy=mix_plan.strategy,
            narration_master_object_path=(
                narration_master_location.key if narration_master_location is not None else None
            ),
            message=(
                "Narration finished and the final mixed audio asset is ready."
                if mix_plan.should_mix
                else "Narration finished and the final audio asset is ready."
            ),
            superseded_asset_ids=superseded_asset_ids,
        )

    def _list_ready_final_audio_assets(self, session_id: str) -> list[SessionAsset]:
        stmt: Select[tuple[SessionAsset]] = (
            select(SessionAsset)
            .where(
                SessionAsset.session_id == session_id,
                SessionAsset.asset_kind == AssetKind.FINAL_AUDIO,
                SessionAsset.status == AssetStatus.READY,
            )
            .order_by(SessionAsset.ready_at.desc(), SessionAsset.created_at.desc())
        )
        return list(self._session.execute(stmt).scalars().all())

    def _resolve_audio_mixer(self) -> FfmpegAudioMixer:
        if self._audio_mixer is None:
            self._audio_mixer = FfmpegAudioMixer()
        return self._audio_mixer

    def _storage(self) -> ObjectStorageService:
        if self._object_storage is None:
            self._object_storage = build_object_storage_service(get_settings())
        return self._object_storage


def read_asset_detail_map(asset: SessionAsset | None) -> dict[str, Any]:
    if asset is None:
        return {}
    return _read_mapping(asset.metadata_json)


def _build_segment_timeline(
    rendered_segments: Sequence[RenderedNarrationSegment],
) -> list[dict[str, Any]]:
    timeline: list[dict[str, Any]] = []
    cursor_seconds = 0.0

    for rendered in rendered_segments:
        duration_seconds = _segment_duration_seconds(rendered)
        start_seconds = cursor_seconds
        end_seconds = start_seconds + duration_seconds
        timeline_end_seconds = end_seconds + max(rendered.segment.pause_after_seconds, 0)
        metadata = _read_mapping(rendered.segment.metadata_json)

        timeline.append(
            {
                "segment_id": rendered.segment.id,
                "segment_index": rendered.segment.segment_index,
                "start_seconds": round(start_seconds, 3),
                "end_seconds": round(end_seconds, 3),
                "timeline_end_seconds": round(timeline_end_seconds, 3),
                "duration_seconds": round(duration_seconds, 3),
                "pause_after_seconds": rendered.segment.pause_after_seconds,
                "pause_hint": (
                    rendered.segment.pause_hint.value
                    if rendered.segment.pause_hint is not None
                    else None
                ),
                "source_boundary_kind": (
                    rendered.segment.source_boundary_kind.value
                    if rendered.segment.source_boundary_kind is not None
                    else "unknown"
                ),
                "source_outline_card_key": rendered.segment.source_outline_card_key,
                "source_outline_card_title": rendered.segment.source_outline_card_title,
                "text_start_offset": rendered.segment.text_start_offset,
                "text_end_offset": rendered.segment.text_end_offset,
                "word_count": rendered.segment.word_count,
                "split_reason": metadata.get("split_reason"),
            }
        )
        cursor_seconds = timeline_end_seconds

    return timeline


def _segment_duration_seconds(rendered: RenderedNarrationSegment) -> float:
    frame_width_bytes = rendered.synthesis.channel_count * rendered.synthesis.sample_width_bytes
    if frame_width_bytes <= 0 or rendered.synthesis.sample_rate_hz <= 0:
        raise FinalAudioAssemblyError("audio segments must expose valid PCM metadata")

    frame_count = len(rendered.synthesis.pcm_audio_bytes) / frame_width_bytes
    return frame_count / rendered.synthesis.sample_rate_hz


def _read_mapping(value: Any) -> dict[str, Any]:
    return dict(value) if isinstance(value, Mapping) else {}

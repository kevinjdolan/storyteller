"""Focused audio pipeline coverage for rendering, mixing, assembly, and resumability.

See `backend/tests/audio_pipeline_test_notes.md` for the mock-versus-real test boundary notes.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest
from app.ai import NarrationSynthesisResult
from app.ai.gemini_resilience import (
    GeminiFailureDetail,
    GeminiFailureKind,
    GeminiRetryNotice,
)
from app.db import (
    AssetKind,
    AssetStatus,
    AudioJob,
    BackgroundJob,
    Base,
    JobStatus,
    NarrationMusicTransitionHint,
    NarrationPauseHint,
    NarrationSegment,
    NarrationSourceBoundaryKind,
    SessionAsset,
    StorySession,
    make_engine,
)
from app.models import WorkflowStage
from app.models.audio_settings import AudioMusicProfile, AudioSettingsView
from app.services.assets import SessionAssetService
from app.services.audio_jobs import (
    AUDIO_RUNTIME_JOB_TYPE,
    AudioJobService,
    AudioJobStateError,
)
from app.services.audio_music import build_audio_mix_plan
from app.services.event_log import SessionEventLogService
from app.services.final_audio_assembly import (
    FinalAudioAssemblyError,
    FinalAudioAssemblyService,
    RenderedNarrationSegment,
)
from app.storage import StorageObjectLocation
from app.worker import JobWorker, build_default_job_handler_registry
from sqlalchemy import select
from sqlalchemy.orm import Session, sessionmaker
from tests.support.audio_pipeline import (
    FailingAudioMixer,
    RecordingAudioMixer,
    RecordingTextToSpeechAdapter,
    build_audio_ready_session,
    build_in_memory_object_storage,
)


class RetryNoticeTextToSpeechAdapter:
    def __init__(self) -> None:
        self.model_id = "test-gemini-tts"
        self._retry_notifier = None
        self.calls: list[object] = []

    def set_retry_notifier(self, retry_notifier) -> None:
        self._retry_notifier = retry_notifier

    def synthesize(self, request):
        self.calls.append(request)
        if self._retry_notifier is not None:
            self._retry_notifier(
                GeminiRetryNotice(
                    failure=GeminiFailureDetail(
                        kind=GeminiFailureKind.RATE_LIMITED,
                        message="Gemini hit a temporary rate limit.",
                        retryable=True,
                        user_action_required=False,
                        status_code=429,
                    ),
                    failed_attempt=1,
                    next_attempt=2,
                    max_attempts=4,
                    delay_seconds=1.0,
                )
            )
        return _build_synthesis_result(7, sample_frames=24_000)

    def close(self) -> None:
        return None


def _enable_sqlite_foreign_keys(engine) -> None:
    with engine.begin() as connection:
        connection.exec_driver_sql("PRAGMA foreign_keys=ON")


def _build_session_factory(tmp_path) -> sessionmaker[Session]:
    database_path = tmp_path / "audio-pipeline.db"
    engine = make_engine(f"sqlite+pysqlite:///{database_path}")
    _enable_sqlite_foreign_keys(engine)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


def _build_synthesis_result(
    sample_value: int,
    *,
    sample_rate_hz: int = 24_000,
    sample_frames: int = 2_400,
) -> NarrationSynthesisResult:
    pcm_audio = bytes([sample_value % 256, 0]) * sample_frames
    return NarrationSynthesisResult(
        pcm_audio_bytes=pcm_audio,
        provider="gemini",
        model_id="test-gemini-tts",
        prompt_version="test-gemini-tts.v1",
        rendered_prompt=f"Prompt for segment {sample_value}",
        voice_name="TestVoice",
        provider_mime_type=f"audio/L16;rate={sample_rate_hz}",
        sample_rate_hz=sample_rate_hz,
        channel_count=1,
        sample_width_bytes=2,
        attempts_used=1,
        raw_response={"usageMetadata": {"totalTokenCount": 7}},
        response_metadata={"attempts_used": 1},
    )


def _build_rendered_segment(
    *,
    session_id: str,
    audio_job_id: str,
    segment_index: int,
    text_content: str,
    pause_after_seconds: int,
    sample_value: int,
    sample_rate_hz: int = 24_000,
):
    segment = NarrationSegment(
        session_id=session_id,
        audio_job_id=audio_job_id,
        segment_index=segment_index,
        status=JobStatus.COMPLETED,
        source_boundary_kind=NarrationSourceBoundaryKind.CHAPTER,
        text_content=text_content,
        word_count=len(text_content.split()),
        text_start_offset=0,
        text_end_offset=len(text_content),
        pause_after_seconds=pause_after_seconds,
        pause_hint=(
            NarrationPauseHint.CHAPTER_BREAK
            if pause_after_seconds > 0
            else NarrationPauseHint.NONE
        ),
        music_transition_hint=(
            NarrationMusicTransitionHint.SOFT_RESET
            if pause_after_seconds > 0
            else NarrationMusicTransitionHint.END_STORY
        ),
        completed_at=datetime.now(timezone.utc),
    )
    return segment, _build_synthesis_result(
        sample_value,
        sample_rate_hz=sample_rate_hz,
    )


def test_audio_runtime_worker_marks_partial_tts_failure_and_keeps_partial_assets(
    tmp_path,
) -> None:
    session_factory = _build_session_factory(tmp_path)
    object_storage = build_in_memory_object_storage()

    with session_factory() as session:
        seed = build_audio_ready_session(
            session,
            chapter_texts=[
                "Mira followed the first bell past the lanterns and kept the harbor calm.",
                "She found the second bell resting under reeds and felt the tide settle.",
            ],
        )
        result = AudioJobService(session, object_storage=object_storage).start_job(
            seed.session_id,
            settings=AudioSettingsView(include_background_music=False),
            estimated_duration_seconds=120,
            source_composition_job_id=seed.composition_job_id,
        )

    worker = JobWorker(
        session_factory=session_factory,
        registry=build_default_job_handler_registry(
            object_storage=object_storage,
            tts_adapter=RecordingTextToSpeechAdapter(fail_on_calls={2}),
        ),
        worker_id="audio-runtime-worker",
        lease_duration=timedelta(seconds=30),
        poll_interval_seconds=0.01,
    )

    assert worker.run_once() is True

    with session_factory() as session:
        runtime_job = session.get(AudioJob, result.job.id)
        worker_job = session.execute(
            select(BackgroundJob).where(BackgroundJob.job_type == AUDIO_RUNTIME_JOB_TYPE)
        ).scalar_one()
        narration_segments = list(
            session.execute(
                select(NarrationSegment)
                .where(NarrationSegment.audio_job_id == result.job.id)
                .order_by(NarrationSegment.segment_index.asc())
            ).scalars()
        )
        segment_assets = list(
            session.execute(
                select(SessionAsset).where(
                    SessionAsset.audio_job_id == result.job.id,
                    SessionAsset.asset_kind == AssetKind.AUDIO_SEGMENT,
                    SessionAsset.status == AssetStatus.READY,
                )
            ).scalars()
        )
        history = SessionEventLogService(session).list_session_history(seed.session_id)

    assert runtime_job is not None
    assert worker_job.status == JobStatus.FAILED
    assert runtime_job.status == JobStatus.FAILED
    assert runtime_job.error_message == "Simulated Gemini TTS failure on call 2."
    assert [segment.status for segment in narration_segments] == [
        JobStatus.COMPLETED,
        JobStatus.FAILED,
    ]
    assert len(segment_assets) == 1
    assert segment_assets[0].metadata_json["duration_seconds"] == 0.1
    audio_progress_payloads = [
        event.payload
        for event in history.events
        if event.event_type == "audio.progress.recorded"
    ]
    assert any(
        payload is not None
        and getattr(payload, "latest_asset_kind", None) == AssetKind.AUDIO_SEGMENT.value
        for payload in audio_progress_payloads
    )
    assert any(
        payload is not None
        and getattr(payload, "status", None) == JobStatus.FAILED.value
        and getattr(payload, "current_segment_index", None) == 2
        for payload in audio_progress_payloads
    )


def test_audio_job_service_resumes_after_mix_failure_without_rerendering_segments(
    tmp_path,
) -> None:
    session_factory = _build_session_factory(tmp_path)
    object_storage = build_in_memory_object_storage()

    with session_factory() as session:
        seed = build_audio_ready_session(
            session,
            chapter_texts=[
                "Mira followed the lantern bell until the docks felt slower and safer.",
                "At the cove she guided the bell home and the water settled around her.",
            ],
        )
        settings = AudioSettingsView(
            include_background_music=True,
            music_profile=AudioMusicProfile.NIGHT_AMBIENCE,
        )
        result = AudioJobService(session, object_storage=object_storage).start_job(
            seed.session_id,
            settings=settings,
            estimated_duration_seconds=180,
            source_composition_job_id=seed.composition_job_id,
        )

    first_adapter = RecordingTextToSpeechAdapter()
    with pytest.raises(AudioJobStateError, match="simulated mix outage"):
        with session_factory() as session:
            AudioJobService(
                session,
                object_storage=object_storage,
                tts_adapter=first_adapter,
                audio_mixer=FailingAudioMixer("simulated mix outage"),
            ).run_job(result.job.id)

    with session_factory() as session:
        failed_job = session.get(AudioJob, result.job.id)
        segment_assets = list(
            session.execute(
                select(SessionAsset).where(
                    SessionAsset.audio_job_id == result.job.id,
                    SessionAsset.asset_kind == AssetKind.AUDIO_SEGMENT,
                    SessionAsset.status == AssetStatus.READY,
                )
            ).scalars()
        )
        final_assets = list(
            session.execute(
                select(SessionAsset).where(
                    SessionAsset.audio_job_id == result.job.id,
                    SessionAsset.asset_kind == AssetKind.FINAL_AUDIO,
                    SessionAsset.status == AssetStatus.READY,
                )
            ).scalars()
        )
        history_after_failure = SessionEventLogService(
            session,
        ).list_session_history(seed.session_id)

    assert failed_job is not None
    assert failed_job.status == JobStatus.FAILED
    assert len(first_adapter.calls) == 2
    assert len(segment_assets) == 2
    assert not final_assets
    assert any(
        payload is not None
        and "Mixing narration with" in (getattr(payload, "current_step", "") or "")
        for payload in (
            event.payload
            for event in history_after_failure.events
            if event.event_type == "audio.progress.recorded"
        )
    )

    recovery_adapter = RecordingTextToSpeechAdapter()
    recovery_mixer = RecordingAudioMixer()
    with session_factory() as session:
        retry_result = AudioJobService(
            session,
            object_storage=object_storage,
            tts_adapter=recovery_adapter,
            audio_mixer=recovery_mixer,
        ).run_job(result.job.id)

    with session_factory() as session:
        recovered_job = session.get(AudioJob, result.job.id)
        final_audio_asset = session.execute(
            select(SessionAsset).where(
                SessionAsset.audio_job_id == result.job.id,
                SessionAsset.asset_kind == AssetKind.FINAL_AUDIO,
                SessionAsset.status == AssetStatus.READY,
            )
        ).scalar_one()

    assert retry_result["status"] == JobStatus.COMPLETED.value
    assert recovered_job is not None
    assert recovered_job.status == JobStatus.COMPLETED
    assert recovered_job.attempt_count == 2
    assert recovered_job.config_json["completed_segments"] == 2
    assert len(recovery_adapter.calls) == 0
    assert len(recovery_mixer.calls) == 1
    assert final_audio_asset.metadata_json["mix"]["applied"] is True
    assert final_audio_asset.metadata_json["generation"]["audio_job_id"] == result.job.id
    assert final_audio_asset.metadata_json["segment_count"] == 2


def test_audio_job_service_records_retry_status_messages_before_render_succeeds(
    tmp_path,
) -> None:
    session_factory = _build_session_factory(tmp_path)
    object_storage = build_in_memory_object_storage()

    with session_factory() as session:
        seed = build_audio_ready_session(
            session,
            chapter_texts=[
                "Mira followed one quiet bell along the dock until the harbor settled.",
            ],
        )
        result = AudioJobService(session, object_storage=object_storage).start_job(
            seed.session_id,
            settings=AudioSettingsView(include_background_music=False),
            estimated_duration_seconds=90,
            source_composition_job_id=seed.composition_job_id,
        )

    adapter = RetryNoticeTextToSpeechAdapter()
    with session_factory() as session:
        run_result = AudioJobService(
            session,
            object_storage=object_storage,
            tts_adapter=adapter,
        ).run_job(result.job.id)
        runtime_job = session.get(AudioJob, result.job.id)
        history = SessionEventLogService(session).list_session_history(seed.session_id)

    retry_step = (
        "Gemini hit a temporary rate limit while rendering segment 1 of 1. "
        "Retrying in 1s (attempt 2 of 4)."
    )
    retry_stage_details = [
        getattr(event.payload, "detail", None)
        for event in history.events
        if event.event_type == "workflow.stage_changed" and event.stage == WorkflowStage.AUDIO
    ]
    audio_progress_payloads = [
        event.payload
        for event in history.events
        if event.event_type == "audio.progress.recorded"
    ]

    assert run_result["status"] == "completed"
    assert len(adapter.calls) == 1
    assert runtime_job is not None
    assert runtime_job.config_json.get("provider_retry") is None
    assert any(detail == retry_step for detail in retry_stage_details)
    assert any(
        payload is not None and getattr(payload, "current_step", None) == retry_step
        for payload in audio_progress_payloads
    )


def test_final_audio_assembly_service_builds_master_and_supersedes_previous_asset(
    tmp_path,
) -> None:
    session_factory = _build_session_factory(tmp_path)
    object_storage = build_in_memory_object_storage()

    with session_factory() as session:
        story_session = StorySession(working_title="Assembly Publish")
        session.add(story_session)
        session.flush()

        previous_job = AudioJob(
            session_id=story_session.id,
            status=JobStatus.COMPLETED,
            voice_key="moonbeam",
            playback_speed=1.0,
            include_background_music=False,
        )
        current_job = AudioJob(
            session_id=story_session.id,
            status=JobStatus.IN_PROGRESS,
            voice_key="storykeeper",
            playback_speed=0.95,
            include_background_music=False,
            estimated_duration_seconds=95,
        )
        session.add_all([previous_job, current_job])
        session.flush()

        previous_asset = SessionAssetService(session).save_asset_record(
            session_id=story_session.id,
            asset_kind=AssetKind.FINAL_AUDIO,
            storage_bucket="storyteller-audio",
            object_path="sessions/assembly/final/previous-story.wav",
            mime_type="audio/wav",
            status=AssetStatus.READY,
            audio_job_id=previous_job.id,
            byte_size=128,
            checksum_sha256="previous-checksum",
            metadata_json={"orchestration_version": "audio_job_final.v2"},
        )

        first_segment, first_synthesis = _build_rendered_segment(
            session_id=story_session.id,
            audio_job_id=current_job.id,
            segment_index=1,
            text_content="Mira eased the bell through the reeds and kept the cove bright.",
            pause_after_seconds=2,
            sample_value=1,
        )
        second_segment, second_synthesis = _build_rendered_segment(
            session_id=story_session.id,
            audio_job_id=current_job.id,
            segment_index=2,
            text_content="She tucked it back to the dock and let the harbor return to sleep.",
            pause_after_seconds=0,
            sample_value=2,
        )
        session.add_all([first_segment, second_segment])
        session.flush()

        rendered_segments = [
            RenderedNarrationSegment(segment=first_segment, synthesis=first_synthesis),
            RenderedNarrationSegment(segment=second_segment, synthesis=second_synthesis),
        ]
        service = FinalAudioAssemblyService(session, object_storage=object_storage)
        narration_master = service.build_narration_master(rendered_segments)
        mix_plan = build_audio_mix_plan(
            AudioSettingsView(include_background_music=False),
        )
        mix_result = service.mix_narration_master(
            narration_master.wav_bytes,
            plan=mix_plan,
        )
        publish_result = service.publish_final_audio(
            job=current_job,
            rendered_segments=rendered_segments,
            narration_master=narration_master,
            mix_plan=mix_plan,
            mix_result=mix_result,
            narration_master_location=None,
        )
        session.commit()

    with session_factory() as session:
        superseded_asset = session.get(SessionAsset, previous_asset.id)
        final_audio_asset = session.get(SessionAsset, publish_result.asset_id)

    assert narration_master.pause_seconds_total == 2
    assert narration_master.segment_indexes == (1, 2)
    assert publish_result.mix_applied is False
    assert publish_result.superseded_asset_ids == (previous_asset.id,)
    assert superseded_asset is not None
    assert superseded_asset.status == AssetStatus.SUPERSEDED
    assert final_audio_asset is not None
    assert final_audio_asset.metadata_json["pause_seconds_total"] == 2
    assert final_audio_asset.metadata_json["segment_indexes"] == [1, 2]
    assert final_audio_asset.metadata_json["segment_timeline"] == [
        {
            "segment_id": first_segment.id,
            "segment_index": 1,
            "start_seconds": 0.0,
            "end_seconds": 0.1,
            "timeline_end_seconds": 2.1,
            "duration_seconds": 0.1,
            "pause_after_seconds": 2,
            "pause_hint": "chapter_break",
            "source_boundary_kind": "chapter",
            "source_outline_card_key": None,
            "source_outline_card_title": None,
            "text_start_offset": first_segment.text_start_offset,
            "text_end_offset": first_segment.text_end_offset,
            "word_count": first_segment.word_count,
            "split_reason": None,
        },
        {
            "segment_id": second_segment.id,
            "segment_index": 2,
            "start_seconds": 2.1,
            "end_seconds": 2.2,
            "timeline_end_seconds": 2.2,
            "duration_seconds": 0.1,
            "pause_after_seconds": 0,
            "pause_hint": "none",
            "source_boundary_kind": "chapter",
            "source_outline_card_key": None,
            "source_outline_card_title": None,
            "text_start_offset": second_segment.text_start_offset,
            "text_end_offset": second_segment.text_end_offset,
            "word_count": second_segment.word_count,
            "split_reason": None,
        },
    ]
    assert final_audio_asset.metadata_json["supersedes_asset_ids"] == [previous_asset.id]
    assert final_audio_asset.metadata_json["generation"]["audio_job_id"] == current_job.id
    assert object_storage.download_bytes(
        StorageObjectLocation(
            bucket=final_audio_asset.storage_bucket,
            key=final_audio_asset.object_path,
        )
    )


def test_final_audio_assembly_service_rejects_mismatched_segment_formats(tmp_path) -> None:
    session_factory = _build_session_factory(tmp_path)

    with session_factory() as session:
        service = FinalAudioAssemblyService(session)
        first_segment, first_synthesis = _build_rendered_segment(
            session_id="session-1",
            audio_job_id="audio-1",
            segment_index=1,
            text_content="The harbor stayed quiet.",
            pause_after_seconds=0,
            sample_value=1,
            sample_rate_hz=24_000,
        )
        second_segment, second_synthesis = _build_rendered_segment(
            session_id="session-1",
            audio_job_id="audio-1",
            segment_index=2,
            text_content="The bell found home.",
            pause_after_seconds=0,
            sample_value=2,
            sample_rate_hz=22_050,
        )

        with pytest.raises(FinalAudioAssemblyError, match="single sample rate"):
            service.build_narration_master(
                [
                    RenderedNarrationSegment(
                        segment=first_segment,
                        synthesis=first_synthesis,
                    ),
                    RenderedNarrationSegment(
                        segment=second_segment,
                        synthesis=second_synthesis,
                    ),
                ]
            )

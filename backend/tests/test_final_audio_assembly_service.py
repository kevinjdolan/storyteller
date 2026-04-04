from __future__ import annotations

import pytest
from app.db import (
    AssetKind,
    AssetStatus,
    AudioJob,
    Base,
    JobStatus,
    NarrationMusicTransitionHint,
    NarrationPauseHint,
    NarrationSegment,
    SessionAsset,
    StorySession,
    make_engine,
)
from app.models.audio_settings import AudioMusicProfile, AudioSettingsView
from app.services.assets import SessionAssetService
from app.services.audio_music import build_audio_mix_plan
from app.services.final_audio_assembly import (
    FinalAudioAssemblyError,
    FinalAudioAssemblyService,
    RenderedNarrationSegment,
)
from app.settings import load_settings
from sqlalchemy.orm import sessionmaker
from tests.support.audio_pipeline import build_synthesis_result
from tests.support.in_memory_storage import InMemoryObjectStorage


def _enable_sqlite_foreign_keys(engine) -> None:
    with engine.begin() as connection:
        connection.exec_driver_sql("PRAGMA foreign_keys=ON")


@pytest.fixture
def db_session():
    engine = make_engine("sqlite+pysqlite:///:memory:")
    _enable_sqlite_foreign_keys(engine)
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)()

    try:
        yield session
    finally:
        session.close()
        engine.dispose()


def _build_storage() -> InMemoryObjectStorage:
    settings = load_settings(
        {
            "STORYTELLER_SECRETS_FILE": "",
            "STORYTELLER_DATABASE_URL": "sqlite+pysqlite:///:memory:",
            "STORYTELLER_GEMINI_API_KEY": "test-gemini-key",
            "STORYTELLER_GCS_ENDPOINT": "http://gcs:4443",
            "STORYTELLER_GCS_PROJECT_ID": "storyteller-local",
            "STORYTELLER_GCS_PUBLIC_URL": "http://localhost:8568",
            "STORYTELLER_GCS_SESSIONS_BUCKET_NAME": "storyteller-sessions",
            "STORYTELLER_GCS_AUDIO_BUCKET_NAME": "storyteller-audio",
            "STORYTELLER_GCS_EXPORTS_BUCKET_NAME": "storyteller-exports",
        }
    )
    return InMemoryObjectStorage(settings)


def _build_rendered_segment(
    *,
    session_id: str,
    audio_job_id: str,
    segment_index: int,
    pause_after_seconds: int = 0,
    sample_frames: int = 2400,
    sample_value: int = 1,
    sample_rate_hz: int = 24_000,
) -> RenderedNarrationSegment:
    synthesis = build_synthesis_result(
        sample_frames=sample_frames,
        sample_value=sample_value,
        sample_rate_hz=sample_rate_hz,
        rendered_prompt=f"Prompt for segment {segment_index}",
    )
    text_content = f"Rendered narration segment {segment_index}."
    return RenderedNarrationSegment(
        segment=NarrationSegment(
            session_id=session_id,
            audio_job_id=audio_job_id,
            segment_index=segment_index,
            status=JobStatus.COMPLETED,
            text_content=text_content,
            word_count=len(text_content.split()),
            text_start_offset=(segment_index - 1) * len(text_content),
            text_end_offset=segment_index * len(text_content),
            pause_after_seconds=pause_after_seconds,
            pause_hint=(
                NarrationPauseHint.CHAPTER_BREAK
                if pause_after_seconds > 0
                else NarrationPauseHint.NONE
            ),
            music_transition_hint=(
                NarrationMusicTransitionHint.SOFT_RESET
                if pause_after_seconds > 0
                else NarrationMusicTransitionHint.CONTINUE_BED
            ),
        ),
        synthesis=synthesis,
    )


def test_build_narration_master_inserts_pause_silence_between_segments(db_session) -> None:
    storage = _build_storage()
    service = FinalAudioAssemblyService(db_session, object_storage=storage)
    story_session = StorySession(working_title="Assembled Master")
    db_session.add(story_session)
    db_session.flush()

    audio_job = AudioJob(
        session_id=story_session.id,
        status=JobStatus.IN_PROGRESS,
        voice_key="moonbeam",
        playback_speed=1.0,
        include_background_music=False,
    )
    db_session.add(audio_job)
    db_session.flush()

    rendered_segments = [
        _build_rendered_segment(
            session_id=story_session.id,
            audio_job_id=audio_job.id,
            segment_index=1,
            pause_after_seconds=2,
            sample_frames=2400,
            sample_value=1,
        ),
        _build_rendered_segment(
            session_id=story_session.id,
            audio_job_id=audio_job.id,
            segment_index=2,
            sample_frames=3600,
            sample_value=2,
        ),
    ]

    narration_master = service.build_narration_master(rendered_segments)

    expected_duration = round((2400 + (2 * 24_000) + 3600) / 24_000, 3)
    assert narration_master.segment_indexes == (1, 2)
    assert narration_master.pause_seconds_total == 2
    assert narration_master.sample_rate_hz == 24_000
    assert narration_master.channel_count == 1
    assert narration_master.sample_width_bytes == 2
    assert narration_master.duration_seconds == expected_duration


def test_build_narration_master_rejects_mixed_sample_rates(db_session) -> None:
    storage = _build_storage()
    service = FinalAudioAssemblyService(db_session, object_storage=storage)
    story_session = StorySession(working_title="Assembly Mismatch")
    db_session.add(story_session)
    db_session.flush()

    audio_job = AudioJob(
        session_id=story_session.id,
        status=JobStatus.IN_PROGRESS,
        voice_key="moonbeam",
        playback_speed=1.0,
        include_background_music=False,
    )
    db_session.add(audio_job)
    db_session.flush()

    rendered_segments = [
        _build_rendered_segment(
            session_id=story_session.id,
            audio_job_id=audio_job.id,
            segment_index=1,
            sample_rate_hz=24_000,
        ),
        _build_rendered_segment(
            session_id=story_session.id,
            audio_job_id=audio_job.id,
            segment_index=2,
            sample_rate_hz=22_050,
        ),
    ]

    with pytest.raises(FinalAudioAssemblyError, match="single sample rate"):
        service.build_narration_master(rendered_segments)


def test_publish_final_audio_supersedes_previous_asset_and_records_mix_metadata(
    db_session,
) -> None:
    storage = _build_storage()
    service = FinalAudioAssemblyService(db_session, object_storage=storage)
    asset_service = SessionAssetService(db_session)
    story_session = StorySession(working_title="Published Mix")
    db_session.add(story_session)
    db_session.flush()

    audio_job = AudioJob(
        session_id=story_session.id,
        status=JobStatus.IN_PROGRESS,
        voice_key="hearthside",
        playback_speed=0.9,
        include_background_music=True,
        music_profile=AudioMusicProfile.NIGHT_AMBIENCE.value,
        estimated_duration_seconds=720,
    )
    db_session.add(audio_job)
    db_session.flush()

    previous_asset = asset_service.save_asset_record(
        session_id=story_session.id,
        asset_kind=AssetKind.FINAL_AUDIO,
        storage_bucket="storyteller-exports",
        object_path=f"sessions/{story_session.id}/audio/prior-story.wav",
        mime_type="audio/wav",
        status=AssetStatus.READY,
        audio_job_id=audio_job.id,
        byte_size=512,
        checksum_sha256="old-audio-checksum",
        metadata_json={"generation": {"audio_job_id": "old-audio-job"}},
    )

    rendered_segments = [
        _build_rendered_segment(
            session_id=story_session.id,
            audio_job_id=audio_job.id,
            segment_index=1,
            pause_after_seconds=1,
            sample_frames=2400,
            sample_value=1,
        ),
        _build_rendered_segment(
            session_id=story_session.id,
            audio_job_id=audio_job.id,
            segment_index=2,
            sample_frames=2400,
            sample_value=2,
        ),
    ]
    narration_master = service.build_narration_master(rendered_segments)
    narration_master_location = service.persist_narration_master_debug_artifact(
        job=audio_job,
        narration_master_wav_bytes=narration_master.wav_bytes,
    )
    mix_plan = build_audio_mix_plan(
        AudioSettingsView(
            include_background_music=True,
            music_profile=AudioMusicProfile.NIGHT_AMBIENCE,
            narration_volume=90,
            music_volume=18,
        )
    )
    mix_result = service.mix_narration_master(
        narration_master.wav_bytes,
        plan=build_audio_mix_plan(AudioSettingsView(include_background_music=False)),
    )
    published = service.publish_final_audio(
        job=audio_job,
        rendered_segments=rendered_segments,
        narration_master=narration_master,
        mix_plan=mix_plan,
        mix_result=mix_result,
        narration_master_location=narration_master_location,
    )
    db_session.commit()

    published_asset = db_session.get(SessionAsset, published.asset_id)
    refreshed_previous_asset = db_session.get(SessionAsset, previous_asset.id)

    assert published.mix_applied is True
    assert published.mix_strategy == "curated_bed_ducked"
    assert published.narration_master_object_path == narration_master_location.key
    assert published_asset is not None
    assert refreshed_previous_asset is not None
    assert refreshed_previous_asset.status == AssetStatus.SUPERSEDED
    assert published_asset.metadata_json["mix"]["applied"] is True
    assert published_asset.metadata_json["mix"]["music_profile"] == "night_ambience"
    assert published_asset.metadata_json["debug"]["narration_master_object_path"] == (
        narration_master_location.key
    )
    assert published_asset.metadata_json["supersedes_asset_ids"] == [previous_asset.id]

from __future__ import annotations

from app.models.audio_settings import AudioMusicProfile, AudioSettingsView
from app.services.audio_music import (
    build_audio_mix_plan,
    build_audio_mix_preview,
    list_audio_music_profile_options,
)


def test_list_audio_music_profile_options_returns_curated_catalog() -> None:
    options = list_audio_music_profile_options()

    assert [option.key for option in options] == [
        AudioMusicProfile.LULLABY_PIANO,
        AudioMusicProfile.STRING_DRIFT,
        AudioMusicProfile.NIGHT_AMBIENCE,
    ]
    assert options[0].asset_file_name == "lullaby_piano.wav"
    assert options[1].recommended_music_volume_min < options[1].recommended_music_volume_max
    assert "steady sense of place" in options[2].bedtime_use_case


def test_build_audio_mix_plan_returns_voice_only_when_music_is_disabled() -> None:
    plan = build_audio_mix_plan(
        AudioSettingsView(
            include_background_music=False,
            narration_volume=92,
            music_volume=24,
        )
    )

    assert plan.strategy == "voice_only"
    assert plan.should_mix is False
    assert plan.music_profile is None
    assert "no background bed" in plan.summary


def test_build_audio_mix_plan_maps_settings_to_ducked_curated_mix() -> None:
    settings = AudioSettingsView(
        include_background_music=True,
        music_profile=AudioMusicProfile.NIGHT_AMBIENCE,
        narration_volume=88,
        music_volume=18,
    )

    plan = build_audio_mix_plan(settings)
    preview = build_audio_mix_preview(settings)

    assert plan.strategy == "curated_bed_ducked"
    assert plan.should_mix is True
    assert plan.music_profile == AudioMusicProfile.NIGHT_AMBIENCE
    assert plan.music_track_file_name == "night_ambience.wav"
    assert plan.music_gain_db is not None and plan.music_gain_db < plan.narration_gain_db
    assert plan.ducking_ratio == 8.0
    assert plan.fade_out_seconds == 8
    assert preview.strategy == "curated_bed_ducked"
    assert preview.track_key == AudioMusicProfile.NIGHT_AMBIENCE
    assert "ducking" in preview.summary

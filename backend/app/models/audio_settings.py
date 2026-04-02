from __future__ import annotations

from enum import Enum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class AudioVoiceKey(str, Enum):
    MOONBEAM = "moonbeam"
    HEARTHSIDE = "hearthside"
    STORYKEEPER = "storykeeper"


class AudioNarrationStyle(str, Enum):
    CALM = "calm"
    HUSHED = "hushed"
    WARM = "warm"


class AudioMusicProfile(str, Enum):
    LULLABY_PIANO = "lullaby_piano"
    STRING_DRIFT = "string_drift"
    NIGHT_AMBIENCE = "night_ambience"


AudioRuntimeEstimateSource = Literal["composition_segments", "story_setup_target", "unknown"]
AudioNarrationPacingBand = Literal["roomy", "balanced", "brisk"]
AudioMixStrategy = Literal["voice_only", "curated_bed_ducked"]

DEFAULT_AUDIO_VOICE_KEY = AudioVoiceKey.MOONBEAM
DEFAULT_AUDIO_NARRATION_STYLE = AudioNarrationStyle.CALM
DEFAULT_AUDIO_PLAYBACK_SPEED = 0.95
DEFAULT_AUDIO_INCLUDE_BACKGROUND_MUSIC = False
DEFAULT_AUDIO_MUSIC_PROFILE = AudioMusicProfile.LULLABY_PIANO
DEFAULT_AUDIO_NARRATION_VOLUME = 92
DEFAULT_AUDIO_MUSIC_VOLUME = 24


class AudioSettingsModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class AudioMusicProfileOptionView(AudioSettingsModel):
    key: AudioMusicProfile
    label: str = Field(min_length=1)
    description: str = Field(min_length=1)
    bedtime_use_case: str = Field(min_length=1)
    asset_file_name: str = Field(min_length=1)
    loop_duration_seconds: int = Field(ge=1)
    recommended_music_volume: int = Field(ge=0, le=100)
    recommended_music_volume_min: int = Field(ge=0, le=100)
    recommended_music_volume_max: int = Field(ge=0, le=100)
    mix_note: str = Field(min_length=1)


class AudioMixPreviewView(AudioSettingsModel):
    strategy: AudioMixStrategy
    summary: str = Field(min_length=1)
    track_key: AudioMusicProfile | None = None
    track_label: str | None = None
    track_description: str | None = None
    narration_gain_db: float = Field(ge=-80, le=6)
    music_gain_db: float | None = Field(default=None, ge=-80, le=6)
    ducking_ratio: float | None = Field(default=None, ge=1)
    ducking_threshold: float | None = Field(default=None, gt=0, le=1)
    fade_out_seconds: int | None = Field(default=None, ge=0, le=60)
    loop_duration_seconds: int | None = Field(default=None, ge=0)


class AudioRuntimeEstimateView(AudioSettingsModel):
    estimated_word_count: int = Field(ge=0)
    estimated_chapter_count: int = Field(ge=0)
    chapter_pause_count: int = Field(ge=0)
    chapter_pause_seconds: int = Field(ge=0)
    total_chapter_pause_seconds: int = Field(ge=0)
    assumed_words_per_minute: int = Field(ge=1)
    minimum_words_per_minute: int = Field(ge=1)
    maximum_words_per_minute: int = Field(ge=1)
    target_duration_seconds: int = Field(ge=0)
    minimum_duration_seconds: int = Field(ge=0)
    maximum_duration_seconds: int = Field(ge=0)
    basis_source: AudioRuntimeEstimateSource
    pacing_band: AudioNarrationPacingBand


class AudioSettingsView(AudioSettingsModel):
    voice_key: AudioVoiceKey = DEFAULT_AUDIO_VOICE_KEY
    narration_style: AudioNarrationStyle = DEFAULT_AUDIO_NARRATION_STYLE
    playback_speed: float = Field(
        default=DEFAULT_AUDIO_PLAYBACK_SPEED,
        ge=0.5,
        le=2.0,
    )
    include_background_music: bool = DEFAULT_AUDIO_INCLUDE_BACKGROUND_MUSIC
    music_profile: AudioMusicProfile = DEFAULT_AUDIO_MUSIC_PROFILE
    narration_volume: int = Field(default=DEFAULT_AUDIO_NARRATION_VOLUME, ge=0, le=100)
    music_volume: int = Field(default=DEFAULT_AUDIO_MUSIC_VOLUME, ge=0, le=100)
    guidance_notes: str | None = None
    music_profile_options: list[AudioMusicProfileOptionView] | None = None
    mix_preview: AudioMixPreviewView | None = None
    runtime_estimate: AudioRuntimeEstimateView | None = None

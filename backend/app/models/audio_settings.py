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

DEFAULT_AUDIO_VOICE_KEY = AudioVoiceKey.MOONBEAM
DEFAULT_AUDIO_NARRATION_STYLE = AudioNarrationStyle.CALM
DEFAULT_AUDIO_PLAYBACK_SPEED = 0.95
DEFAULT_AUDIO_INCLUDE_BACKGROUND_MUSIC = False
DEFAULT_AUDIO_MUSIC_PROFILE = AudioMusicProfile.LULLABY_PIANO
DEFAULT_AUDIO_NARRATION_VOLUME = 92
DEFAULT_AUDIO_MUSIC_VOLUME = 24


class AudioSettingsModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


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
    runtime_estimate: AudioRuntimeEstimateView | None = None

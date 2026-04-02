from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from app.models.audio_settings import (
    AudioMixPreviewView,
    AudioMixStrategy,
    AudioMusicProfile,
    AudioMusicProfileOptionView,
    AudioSettingsView,
)

_BACKGROUND_MUSIC_DIR = Path(__file__).resolve().parents[1] / "data" / "background_music"
_VOICE_ONLY_MIX_STRATEGY: AudioMixStrategy = "voice_only"
_CURATED_BED_MIX_STRATEGY: AudioMixStrategy = "curated_bed_ducked"


@dataclass(frozen=True)
class BackgroundMusicTrackDefinition:
    profile: AudioMusicProfile
    label: str
    description: str
    bedtime_use_case: str
    asset_file_name: str
    loop_duration_seconds: int
    recommended_music_volume: int
    recommended_music_volume_min: int
    recommended_music_volume_max: int
    mix_note: str
    base_music_gain_db: float
    ducking_ratio: float
    ducking_threshold: float
    ducking_attack_ms: int
    ducking_release_ms: int
    fade_out_seconds: int

    @property
    def asset_path(self) -> Path:
        return _BACKGROUND_MUSIC_DIR / self.asset_file_name

    def to_option_view(self) -> AudioMusicProfileOptionView:
        return AudioMusicProfileOptionView(
            key=self.profile,
            label=self.label,
            description=self.description,
            bedtime_use_case=self.bedtime_use_case,
            asset_file_name=self.asset_file_name,
            loop_duration_seconds=self.loop_duration_seconds,
            recommended_music_volume=self.recommended_music_volume,
            recommended_music_volume_min=self.recommended_music_volume_min,
            recommended_music_volume_max=self.recommended_music_volume_max,
            mix_note=self.mix_note,
        )


@dataclass(frozen=True)
class AudioMixPlan:
    strategy: AudioMixStrategy
    summary: str
    narration_gain_db: float
    music_profile: AudioMusicProfile | None = None
    music_track_label: str | None = None
    music_track_description: str | None = None
    music_track_file_name: str | None = None
    music_gain_db: float | None = None
    ducking_ratio: float | None = None
    ducking_threshold: float | None = None
    ducking_attack_ms: int | None = None
    ducking_release_ms: int | None = None
    fade_out_seconds: int | None = None
    loop_duration_seconds: int | None = None

    @property
    def should_mix(self) -> bool:
        return (
            self.strategy == _CURATED_BED_MIX_STRATEGY
            and self.music_profile is not None
            and self.music_track_file_name is not None
            and self.music_gain_db is not None
            and self.ducking_ratio is not None
            and self.ducking_threshold is not None
        )

    def to_config_json(self) -> dict[str, Any]:
        return {
            "strategy": self.strategy,
            "summary": self.summary,
            "narration_gain_db": self.narration_gain_db,
            "music_profile": self.music_profile.value if self.music_profile is not None else None,
            "music_track_label": self.music_track_label,
            "music_track_description": self.music_track_description,
            "music_track_file_name": self.music_track_file_name,
            "music_gain_db": self.music_gain_db,
            "ducking_ratio": self.ducking_ratio,
            "ducking_threshold": self.ducking_threshold,
            "ducking_attack_ms": self.ducking_attack_ms,
            "ducking_release_ms": self.ducking_release_ms,
            "fade_out_seconds": self.fade_out_seconds,
            "loop_duration_seconds": self.loop_duration_seconds,
        }


_BACKGROUND_MUSIC_TRACKS: dict[AudioMusicProfile, BackgroundMusicTrackDefinition] = {
    AudioMusicProfile.LULLABY_PIANO: BackgroundMusicTrackDefinition(
        profile=AudioMusicProfile.LULLABY_PIANO,
        label="Lullaby piano",
        description="Simple keys under the voice without pulling focus.",
        bedtime_use_case="Softest choice for tender reassurance and tucked-in endings.",
        asset_file_name="lullaby_piano.wav",
        loop_duration_seconds=24,
        recommended_music_volume=24,
        recommended_music_volume_min=12,
        recommended_music_volume_max=28,
        mix_note="Loops a sparse piano bed and fades out at the end of the narration.",
        base_music_gain_db=-11.0,
        ducking_ratio=10.0,
        ducking_threshold=0.045,
        ducking_attack_ms=35,
        ducking_release_ms=360,
        fade_out_seconds=6,
    ),
    AudioMusicProfile.STRING_DRIFT: BackgroundMusicTrackDefinition(
        profile=AudioMusicProfile.STRING_DRIFT,
        label="String drift",
        description="Long bowed textures for wonder-heavy stories.",
        bedtime_use_case="Best for spacious fantasy or travel scenes that need more glow.",
        asset_file_name="string_drift.wav",
        loop_duration_seconds=24,
        recommended_music_volume=20,
        recommended_music_volume_min=10,
        recommended_music_volume_max=24,
        mix_note="Uses a lower base gain so the texture stays behind the narration.",
        base_music_gain_db=-13.0,
        ducking_ratio=12.0,
        ducking_threshold=0.038,
        ducking_attack_ms=28,
        ducking_release_ms=420,
        fade_out_seconds=7,
    ),
    AudioMusicProfile.NIGHT_AMBIENCE: BackgroundMusicTrackDefinition(
        profile=AudioMusicProfile.NIGHT_AMBIENCE,
        label="Night ambience",
        description="Low environmental bed for harbor, forest, or sky scenes.",
        bedtime_use_case="Fits scene-setting passages that want a steady sense of place.",
        asset_file_name="night_ambience.wav",
        loop_duration_seconds=24,
        recommended_music_volume=18,
        recommended_music_volume_min=8,
        recommended_music_volume_max=22,
        mix_note="Keeps the bed darkest and quietest so consonants remain easy to hear.",
        base_music_gain_db=-16.0,
        ducking_ratio=8.0,
        ducking_threshold=0.05,
        ducking_attack_ms=40,
        ducking_release_ms=500,
        fade_out_seconds=8,
    ),
}


def list_audio_music_profile_options() -> list[AudioMusicProfileOptionView]:
    return [
        _BACKGROUND_MUSIC_TRACKS[profile].to_option_view()
        for profile in AudioMusicProfile
    ]


def build_audio_mix_preview(settings: AudioSettingsView) -> AudioMixPreviewView:
    plan = build_audio_mix_plan(settings)
    return AudioMixPreviewView(
        strategy=plan.strategy,
        summary=plan.summary,
        track_key=plan.music_profile,
        track_label=plan.music_track_label,
        track_description=plan.music_track_description,
        narration_gain_db=plan.narration_gain_db,
        music_gain_db=plan.music_gain_db,
        ducking_ratio=plan.ducking_ratio,
        ducking_threshold=plan.ducking_threshold,
        fade_out_seconds=plan.fade_out_seconds,
        loop_duration_seconds=plan.loop_duration_seconds,
    )


def build_audio_mix_plan(settings: AudioSettingsView) -> AudioMixPlan:
    narration_gain_db = _volume_percent_to_gain_db(settings.narration_volume)
    if not settings.include_background_music or settings.music_volume <= 0:
        return AudioMixPlan(
            strategy=_VOICE_ONLY_MIX_STRATEGY,
            summary=(
                "Narration stays dry with no background bed. "
                f"Voice gain {_format_db(narration_gain_db)}."
            ),
            narration_gain_db=narration_gain_db,
        )

    track = get_background_music_track(settings.music_profile)
    music_gain_db = round(
        track.base_music_gain_db + _volume_percent_to_gain_db(settings.music_volume),
        1,
    )
    return AudioMixPlan(
        strategy=_CURATED_BED_MIX_STRATEGY,
        summary=(
            f"{track.label} loops under the narration at {_format_db(music_gain_db)} "
            f"before ducking. Voice gain {_format_db(narration_gain_db)}, "
            f"{track.ducking_ratio:g}:1 ducking, and a {track.fade_out_seconds}s fade out."
        ),
        narration_gain_db=narration_gain_db,
        music_profile=track.profile,
        music_track_label=track.label,
        music_track_description=track.description,
        music_track_file_name=track.asset_file_name,
        music_gain_db=music_gain_db,
        ducking_ratio=track.ducking_ratio,
        ducking_threshold=track.ducking_threshold,
        ducking_attack_ms=track.ducking_attack_ms,
        ducking_release_ms=track.ducking_release_ms,
        fade_out_seconds=track.fade_out_seconds,
        loop_duration_seconds=track.loop_duration_seconds,
    )


def deserialize_audio_mix_plan(payload: Any) -> AudioMixPlan:
    data = dict(payload) if isinstance(payload, dict) else {}
    strategy = str(data.get("strategy") or _VOICE_ONLY_MIX_STRATEGY).strip()
    if strategy == _CURATED_BED_MIX_STRATEGY:
        music_profile = _coerce_music_profile(data.get("music_profile"))
        track = get_background_music_track(music_profile)
        fallback_summary = build_audio_mix_plan(_settings_from_track(track)).summary
        music_track_label = str(data.get("music_track_label") or track.label)
        music_track_description = str(
            data.get("music_track_description") or track.description
        )
        music_track_file_name = str(
            data.get("music_track_file_name") or track.asset_file_name
        )
        return AudioMixPlan(
            strategy=_CURATED_BED_MIX_STRATEGY,
            summary=str(data.get("summary") or fallback_summary),
            narration_gain_db=_coerce_float(data.get("narration_gain_db"), 0.0),
            music_profile=music_profile,
            music_track_label=music_track_label,
            music_track_description=music_track_description,
            music_track_file_name=music_track_file_name,
            music_gain_db=_coerce_float(
                data.get("music_gain_db"),
                track.base_music_gain_db,
            ),
            ducking_ratio=_coerce_float(data.get("ducking_ratio"), track.ducking_ratio),
            ducking_threshold=_coerce_float(
                data.get("ducking_threshold"),
                track.ducking_threshold,
            ),
            ducking_attack_ms=_coerce_int(
                data.get("ducking_attack_ms"),
                track.ducking_attack_ms,
            ),
            ducking_release_ms=_coerce_int(
                data.get("ducking_release_ms"),
                track.ducking_release_ms,
            ),
            fade_out_seconds=_coerce_int(
                data.get("fade_out_seconds"),
                track.fade_out_seconds,
            ),
            loop_duration_seconds=_coerce_int(
                data.get("loop_duration_seconds"),
                track.loop_duration_seconds,
            ),
        )

    return AudioMixPlan(
        strategy=_VOICE_ONLY_MIX_STRATEGY,
        summary=str(data.get("summary") or "Narration stays dry with no background bed."),
        narration_gain_db=_coerce_float(data.get("narration_gain_db"), 0.0),
    )


def get_background_music_track(
    profile: AudioMusicProfile | str | None,
) -> BackgroundMusicTrackDefinition:
    coerced_profile = _coerce_music_profile(profile)
    return _BACKGROUND_MUSIC_TRACKS[coerced_profile]


def _coerce_music_profile(profile: AudioMusicProfile | str | None) -> AudioMusicProfile:
    if isinstance(profile, AudioMusicProfile):
        return profile
    normalized = str(profile or AudioMusicProfile.LULLABY_PIANO.value).strip()
    return AudioMusicProfile(normalized or AudioMusicProfile.LULLABY_PIANO.value)


def _coerce_float(value: Any, fallback: float) -> float:
    try:
        return round(float(value), 1)
    except (TypeError, ValueError):
        return round(float(fallback), 1)


def _coerce_int(value: Any, fallback: int) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return int(fallback)


def _format_db(value: float) -> str:
    prefix = "+" if value > 0 else ""
    return f"{prefix}{value:.1f} dB"


def _volume_percent_to_gain_db(volume_percent: int) -> float:
    if volume_percent <= 0:
        return -80.0

    clamped_percent = min(max(int(volume_percent), 0), 100)
    normalized = max(clamped_percent / 100.0, 0.0001)
    return round(20 * math.log10(normalized), 1)


def _settings_from_track(track: BackgroundMusicTrackDefinition) -> AudioSettingsView:
    return AudioSettingsView(
        include_background_music=True,
        music_profile=track.profile,
        narration_volume=100,
        music_volume=track.recommended_music_volume,
    )

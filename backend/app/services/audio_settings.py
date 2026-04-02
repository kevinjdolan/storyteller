from __future__ import annotations

from collections.abc import Sequence

from app.db import CompositionSegment, CompositionSegmentAcceptanceState, JobStatus
from app.models.audio_settings import (
    DEFAULT_AUDIO_INCLUDE_BACKGROUND_MUSIC,
    DEFAULT_AUDIO_MUSIC_PROFILE,
    DEFAULT_AUDIO_MUSIC_VOLUME,
    DEFAULT_AUDIO_NARRATION_STYLE,
    DEFAULT_AUDIO_NARRATION_VOLUME,
    DEFAULT_AUDIO_PLAYBACK_SPEED,
    DEFAULT_AUDIO_VOICE_KEY,
    AudioMusicProfile,
    AudioNarrationStyle,
    AudioRuntimeEstimateView,
    AudioSettingsView,
    AudioVoiceKey,
)
from app.services.audio_length_estimation import (
    AudioLengthEstimateInput,
    estimate_audio_length,
)
from app.services.audio_music import (
    build_audio_mix_preview,
    list_audio_music_profile_options,
)

AUDIO_VOICE_LABELS: dict[AudioVoiceKey, str] = {
    AudioVoiceKey.MOONBEAM: "Moonbeam",
    AudioVoiceKey.HEARTHSIDE: "Hearthside",
    AudioVoiceKey.STORYKEEPER: "Storykeeper",
}

AUDIO_NARRATION_STYLE_LABELS: dict[AudioNarrationStyle, str] = {
    AudioNarrationStyle.CALM: "calm",
    AudioNarrationStyle.HUSHED: "hushed",
    AudioNarrationStyle.WARM: "warm",
}

AUDIO_MUSIC_PROFILE_LABELS: dict[AudioMusicProfile, str] = {
    AudioMusicProfile.LULLABY_PIANO: "lullaby piano",
    AudioMusicProfile.STRING_DRIFT: "string drift",
    AudioMusicProfile.NIGHT_AMBIENCE: "night ambience",
}


def build_audio_settings_view(
    *,
    story_session,
    latest_audio_job=None,
    composition_segments: Sequence[CompositionSegment] = (),
    selected_story_setup=None,
    selected_story_outline=None,
) -> AudioSettingsView:
    settings = AudioSettingsView(
        voice_key=_coerce_audio_voice_key(
            story_session.audio_voice_key,
            fallback=(
                latest_audio_job.voice_key
                if latest_audio_job is not None and latest_audio_job.voice_key
                else None
            ),
        ),
        narration_style=_coerce_audio_narration_style(story_session.audio_narration_style),
        playback_speed=_coerce_playback_speed(
            story_session.audio_playback_speed,
            fallback=(
                latest_audio_job.playback_speed if latest_audio_job is not None else None
            ),
        ),
        include_background_music=_coerce_include_background_music(
            story_session.audio_include_background_music,
            fallback=(
                latest_audio_job.include_background_music
                if latest_audio_job is not None
                else None
            ),
        ),
        music_profile=_coerce_audio_music_profile(
            story_session.audio_music_profile,
            fallback=(
                latest_audio_job.music_profile
                if latest_audio_job is not None and latest_audio_job.music_profile
                else None
            ),
        ),
        narration_volume=_coerce_volume(
            story_session.audio_narration_volume,
            DEFAULT_AUDIO_NARRATION_VOLUME,
        ),
        music_volume=_coerce_volume(story_session.audio_music_volume, DEFAULT_AUDIO_MUSIC_VOLUME),
        guidance_notes=_normalize_optional_text(story_session.audio_guidance_notes),
    )
    return hydrate_audio_settings_view(
        settings,
        runtime_estimate=build_audio_runtime_estimate(
            composition_segments=composition_segments,
            selected_story_setup=selected_story_setup,
            selected_story_outline=selected_story_outline,
            playback_speed=settings.playback_speed,
        ),
    )


def hydrate_audio_settings_view(
    settings: AudioSettingsView,
    *,
    runtime_estimate: AudioRuntimeEstimateView | None = None,
) -> AudioSettingsView:
    return settings.model_copy(
        update={
            "music_profile_options": list_audio_music_profile_options(),
            "mix_preview": build_audio_mix_preview(settings),
            "runtime_estimate": runtime_estimate,
        }
    )


def build_audio_runtime_estimate(
    *,
    composition_segments: Sequence[CompositionSegment] = (),
    selected_story_setup=None,
    selected_story_outline=None,
    playback_speed: float = DEFAULT_AUDIO_PLAYBACK_SPEED,
) -> AudioRuntimeEstimateView | None:
    estimated_word_count = _estimate_audio_word_count(
        composition_segments=composition_segments,
        selected_story_setup=selected_story_setup,
    )
    if estimated_word_count <= 0:
        return None

    estimated_chapter_count = _estimate_audio_chapter_count(
        selected_story_setup=selected_story_setup,
        selected_story_outline=selected_story_outline,
    )
    runtime = estimate_audio_length(
        estimate_input=AudioLengthEstimateInput(
            word_count=estimated_word_count,
            playback_speed=playback_speed,
            chapter_count=estimated_chapter_count,
        )
    )

    return AudioRuntimeEstimateView(
        estimated_word_count=estimated_word_count,
        estimated_chapter_count=runtime.chapter_count,
        chapter_pause_count=runtime.chapter_pause_count,
        chapter_pause_seconds=runtime.chapter_pause_seconds,
        total_chapter_pause_seconds=runtime.total_chapter_pause_seconds,
        assumed_words_per_minute=runtime.assumed_words_per_minute,
        minimum_words_per_minute=runtime.minimum_words_per_minute,
        maximum_words_per_minute=runtime.maximum_words_per_minute,
        target_duration_seconds=runtime.target_duration_seconds,
        minimum_duration_seconds=runtime.minimum_duration_seconds,
        maximum_duration_seconds=runtime.maximum_duration_seconds,
        basis_source=(
            "composition_segments"
            if _has_accepted_segments(composition_segments)
            else "story_setup_target"
            if getattr(selected_story_setup, "target_word_count", None) is not None
            else "unknown"
        ),
        pacing_band=runtime.pacing_band,
    )


def build_audio_settings_event_summary(settings: AudioSettingsView) -> str:
    fragments = [
        f"{AUDIO_VOICE_LABELS[settings.voice_key]} voice",
        f"{AUDIO_NARRATION_STYLE_LABELS[settings.narration_style]} narration",
        f"{settings.playback_speed:g}x speed",
        (
            f"music on ({AUDIO_MUSIC_PROFILE_LABELS[settings.music_profile]})"
            if settings.include_background_music
            else "no background music"
        ),
    ]
    if settings.guidance_notes:
        fragments.append(settings.guidance_notes)
    summary = "Updated audio settings: " + ", ".join(fragments)
    if summary.endswith((".", "!", "?")):
        return summary
    return summary + "."


def build_audio_settings_memory_summary(settings: AudioSettingsView) -> str:
    fragments = [
        f"voice={settings.voice_key.value}",
        f"style={settings.narration_style.value}",
        f"speed={settings.playback_speed:g}",
        (
            f"music={settings.music_profile.value}@{settings.music_volume}%"
            if settings.include_background_music
            else "music=off"
        ),
        f"narration_volume={settings.narration_volume}%",
    ]
    if settings.guidance_notes:
        fragments.append(f"notes={settings.guidance_notes}")
    return ", ".join(fragments)


def build_audio_settings_stage_detail(
    settings: AudioSettingsView,
    *,
    regenerate_audio: bool = False,
) -> str:
    detail = [
        "Audio settings updated."
        if not regenerate_audio
        else "Audio settings changed. Regenerate narration to apply them.",
        f"Voice: {AUDIO_VOICE_LABELS[settings.voice_key]}.",
        f"Style: {AUDIO_NARRATION_STYLE_LABELS[settings.narration_style]}.",
        f"Playback speed {settings.playback_speed:g}x.",
        (
            "Music: "
            f"{AUDIO_MUSIC_PROFILE_LABELS[settings.music_profile]} "
            f"at {settings.music_volume}%."
            if settings.include_background_music
            else "Music off."
        ),
    ]

    if settings.mix_preview is not None and settings.include_background_music:
        detail.append(f"Mix plan: {settings.mix_preview.summary}")

    if settings.runtime_estimate is not None:
        minimum_minutes = max(1, round(settings.runtime_estimate.minimum_duration_seconds / 60))
        maximum_minutes = max(1, round(settings.runtime_estimate.maximum_duration_seconds / 60))
        target_minutes = max(1, round(settings.runtime_estimate.target_duration_seconds / 60))
        detail.append(
            "Estimated runtime "
            f"about {target_minutes} minutes, often {minimum_minutes}-{maximum_minutes}. "
            "Final length can vary with the finished story and narration delivery."
        )
        if settings.runtime_estimate.chapter_pause_count > 0:
            detail.append(
                "Estimate includes "
                f"{settings.runtime_estimate.chapter_pause_count} short chapter pauses "
                f"at about {settings.runtime_estimate.chapter_pause_seconds} seconds each."
            )
    else:
        detail.append(
            "Runtime is still an estimate and will sharpen after story setup "
            "or accepted draft text is available."
        )

    if settings.guidance_notes:
        detail.append(settings.guidance_notes)

    return " ".join(detail)


def audio_settings_field_values(settings: AudioSettingsView) -> dict[str, object]:
    return {
        "voice_key": settings.voice_key.value,
        "narration_style": settings.narration_style.value,
        "playback_speed": settings.playback_speed,
        "include_background_music": settings.include_background_music,
        "music_profile": settings.music_profile.value,
        "narration_volume": settings.narration_volume,
        "music_volume": settings.music_volume,
        "guidance_notes": settings.guidance_notes,
    }


def persist_audio_settings(story_session, settings: AudioSettingsView) -> None:
    story_session.audio_voice_key = settings.voice_key.value
    story_session.audio_narration_style = settings.narration_style.value
    story_session.audio_playback_speed = settings.playback_speed
    story_session.audio_include_background_music = settings.include_background_music
    story_session.audio_music_profile = settings.music_profile.value
    story_session.audio_narration_volume = settings.narration_volume
    story_session.audio_music_volume = settings.music_volume
    story_session.audio_guidance_notes = settings.guidance_notes


def _estimate_audio_word_count(
    *,
    composition_segments: Sequence[CompositionSegment],
    selected_story_setup=None,
) -> int:
    latest_by_segment: dict[int, CompositionSegment] = {}
    for row in composition_segments:
        if row.segment_index in latest_by_segment:
            continue
        if row.status != JobStatus.COMPLETED and row.completed_at is None:
            continue
        if row.acceptance_state != CompositionSegmentAcceptanceState.ACCEPTED:
            continue
        if row.superseded_by_segment_id is not None:
            continue
        latest_by_segment[row.segment_index] = row

    if latest_by_segment:
        total_words = 0
        for segment_index in sorted(latest_by_segment):
            segment = latest_by_segment[segment_index]
            if segment.word_count is not None:
                total_words += segment.word_count
                continue
            accepted_text = segment.accepted_text or segment.text_content or ""
            if accepted_text:
                total_words += len(accepted_text.split())
        if total_words > 0:
            return total_words

    if getattr(selected_story_setup, "target_word_count", None) is not None:
        return int(selected_story_setup.target_word_count)

    return 0


def _has_accepted_segments(composition_segments: Sequence[CompositionSegment]) -> bool:
    return any(
        row.acceptance_state == CompositionSegmentAcceptanceState.ACCEPTED
        and row.superseded_by_segment_id is None
        and (row.word_count is not None or row.accepted_text or row.text_content)
        for row in composition_segments
    )


def _estimate_audio_chapter_count(
    *,
    selected_story_setup=None,
    selected_story_outline=None,
) -> int:
    chapter_count = getattr(selected_story_setup, "chapter_count", None)
    if chapter_count is not None:
        return max(int(chapter_count), 0)

    if (
        selected_story_outline is not None
        and getattr(selected_story_outline, "outline_kind", None) == "chapter"
    ):
        cards = getattr(selected_story_outline, "cards", None) or []
        return len(cards)

    return 0


def _coerce_audio_voice_key(
    value: str | None,
    *,
    fallback: str | None = None,
) -> AudioVoiceKey:
    for candidate in (value, fallback):
        if candidate is None:
            continue
        try:
            return AudioVoiceKey(candidate)
        except ValueError:
            continue
    return DEFAULT_AUDIO_VOICE_KEY


def _coerce_audio_narration_style(value: str | None) -> AudioNarrationStyle:
    if value is not None:
        try:
            return AudioNarrationStyle(value)
        except ValueError:
            pass
    return DEFAULT_AUDIO_NARRATION_STYLE


def _coerce_audio_music_profile(
    value: str | None,
    *,
    fallback: str | None = None,
) -> AudioMusicProfile:
    for candidate in (value, fallback):
        if candidate is None:
            continue
        try:
            return AudioMusicProfile(candidate)
        except ValueError:
            continue
    return DEFAULT_AUDIO_MUSIC_PROFILE


def _coerce_playback_speed(value: float | None, *, fallback: float | None = None) -> float:
    candidate = value if value is not None else fallback
    if candidate is None:
        return DEFAULT_AUDIO_PLAYBACK_SPEED
    return min(max(float(candidate), 0.5), 2.0)


def _coerce_include_background_music(
    value: bool | None,
    *,
    fallback: bool | None = None,
) -> bool:
    if value is not None:
        return value
    if fallback is not None:
        return fallback
    return DEFAULT_AUDIO_INCLUDE_BACKGROUND_MUSIC


def _coerce_volume(value: int | None, default: int) -> int:
    if value is None:
        return default
    return min(max(int(value), 0), 100)


def _normalize_optional_text(value: str | None) -> str | None:
    if value is None:
        return None
    normalized = value.strip()
    return normalized or None

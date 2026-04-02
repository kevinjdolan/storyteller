from __future__ import annotations

import math
from dataclasses import dataclass

from app.services.planning_heuristics import (
    DEFAULT_BEDTIME_WORDS_PER_MINUTE,
    MAX_BEDTIME_WORDS_PER_MINUTE,
    MIN_BEDTIME_WORDS_PER_MINUTE,
    classify_narration_pacing,
)

DEFAULT_AUDIO_CHAPTER_PAUSE_SECONDS = 3
DEFAULT_AUDIO_DURATION_ROUNDING_SECONDS = 15


@dataclass(frozen=True)
class AudioLengthEstimateAssumptions:
    assumed_words_per_minute: int = DEFAULT_BEDTIME_WORDS_PER_MINUTE
    minimum_words_per_minute: int = MIN_BEDTIME_WORDS_PER_MINUTE
    maximum_words_per_minute: int = MAX_BEDTIME_WORDS_PER_MINUTE
    chapter_pause_seconds: int = DEFAULT_AUDIO_CHAPTER_PAUSE_SECONDS
    duration_rounding_seconds: int = DEFAULT_AUDIO_DURATION_ROUNDING_SECONDS


@dataclass(frozen=True)
class AudioLengthEstimateInput:
    word_count: int
    playback_speed: float
    chapter_count: int = 0


@dataclass(frozen=True)
class AudioLengthEstimateResult:
    word_count: int
    chapter_count: int
    chapter_pause_count: int
    chapter_pause_seconds: int
    total_chapter_pause_seconds: int
    target_duration_seconds: int
    minimum_duration_seconds: int
    maximum_duration_seconds: int
    assumed_words_per_minute: int
    minimum_words_per_minute: int
    maximum_words_per_minute: int
    pacing_band: str


def estimate_audio_length(
    estimate_input: AudioLengthEstimateInput,
    *,
    assumptions: AudioLengthEstimateAssumptions = AudioLengthEstimateAssumptions(),
) -> AudioLengthEstimateResult:
    normalized_word_count = max(estimate_input.word_count, 0)
    normalized_chapter_count = max(estimate_input.chapter_count, 0)
    chapter_pause_count = max(normalized_chapter_count - 1, 0)
    total_pause_seconds = chapter_pause_count * assumptions.chapter_pause_seconds

    if normalized_word_count <= 0:
        return AudioLengthEstimateResult(
            word_count=0,
            chapter_count=normalized_chapter_count,
            chapter_pause_count=chapter_pause_count,
            chapter_pause_seconds=assumptions.chapter_pause_seconds,
            total_chapter_pause_seconds=total_pause_seconds,
            target_duration_seconds=0,
            minimum_duration_seconds=0,
            maximum_duration_seconds=0,
            assumed_words_per_minute=assumptions.assumed_words_per_minute,
            minimum_words_per_minute=assumptions.minimum_words_per_minute,
            maximum_words_per_minute=assumptions.maximum_words_per_minute,
            pacing_band=classify_narration_pacing(assumptions.assumed_words_per_minute),
        )

    target_seconds = _estimate_duration_seconds(
        normalized_word_count,
        words_per_minute=assumptions.assumed_words_per_minute,
        playback_speed=estimate_input.playback_speed,
    )
    minimum_seconds = _estimate_duration_seconds(
        normalized_word_count,
        words_per_minute=assumptions.maximum_words_per_minute,
        playback_speed=estimate_input.playback_speed,
    )
    maximum_seconds = _estimate_duration_seconds(
        normalized_word_count,
        words_per_minute=assumptions.minimum_words_per_minute,
        playback_speed=estimate_input.playback_speed,
    )

    target_duration_seconds = _round_seconds(
        target_seconds + total_pause_seconds,
        rounding_seconds=assumptions.duration_rounding_seconds,
        mode="nearest",
    )
    minimum_duration_seconds = _round_seconds(
        minimum_seconds + total_pause_seconds,
        rounding_seconds=assumptions.duration_rounding_seconds,
        mode="down",
    )
    maximum_duration_seconds = _round_seconds(
        maximum_seconds + total_pause_seconds,
        rounding_seconds=assumptions.duration_rounding_seconds,
        mode="up",
    )

    effective_words_per_minute = max(
        1,
        round(assumptions.assumed_words_per_minute * estimate_input.playback_speed),
    )

    return AudioLengthEstimateResult(
        word_count=normalized_word_count,
        chapter_count=normalized_chapter_count,
        chapter_pause_count=chapter_pause_count,
        chapter_pause_seconds=assumptions.chapter_pause_seconds,
        total_chapter_pause_seconds=total_pause_seconds,
        target_duration_seconds=min(
            max(target_duration_seconds, minimum_duration_seconds),
            maximum_duration_seconds,
        ),
        minimum_duration_seconds=minimum_duration_seconds,
        maximum_duration_seconds=maximum_duration_seconds,
        assumed_words_per_minute=assumptions.assumed_words_per_minute,
        minimum_words_per_minute=assumptions.minimum_words_per_minute,
        maximum_words_per_minute=assumptions.maximum_words_per_minute,
        pacing_band=classify_narration_pacing(effective_words_per_minute),
    )


def _estimate_duration_seconds(
    word_count: int,
    *,
    words_per_minute: int,
    playback_speed: float,
) -> int:
    if word_count <= 0:
        return 0

    effective_words_per_minute = max(words_per_minute * playback_speed, 1)
    return int(math.ceil((word_count / effective_words_per_minute) * 60))


def _round_seconds(
    value: int,
    *,
    rounding_seconds: int,
    mode: str,
) -> int:
    if value <= 0:
        return 0
    if rounding_seconds <= 1:
        return value

    quotient = value / rounding_seconds
    if mode == "down":
        rounded = math.floor(quotient)
    elif mode == "up":
        rounded = math.ceil(quotient)
    else:
        rounded = round(quotient)

    return max(rounding_seconds, int(rounded * rounding_seconds))

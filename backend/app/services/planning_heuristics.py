from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Literal

DEFAULT_BEDTIME_WORDS_PER_MINUTE = 140
MIN_BEDTIME_WORDS_PER_MINUTE = 120
MAX_BEDTIME_WORDS_PER_MINUTE = 160
DEFAULT_CHAPTER_VARIANCE_RATIO = 0.15

NarrationPacingBand = Literal["roomy", "balanced", "brisk"]


@dataclass(frozen=True)
class RuntimeEstimate:
    target_minutes: int
    minimum_minutes: int
    maximum_minutes: int
    assumed_words_per_minute: int
    minimum_words_per_minute: int
    maximum_words_per_minute: int


@dataclass(frozen=True)
class WordCountEstimate:
    target_word_count: int
    minimum_word_count: int
    maximum_word_count: int
    assumed_words_per_minute: int
    minimum_words_per_minute: int
    maximum_words_per_minute: int


@dataclass(frozen=True)
class ChapterSizeEstimate:
    average_words_per_chapter: int
    minimum_words_per_chapter: int
    maximum_words_per_chapter: int
    chapter_count: int
    total_word_count: int
    variability_ratio: float


def estimate_runtime_from_word_count(
    word_count: int,
    *,
    playback_speed: float = 1.0,
    assumed_words_per_minute: int = DEFAULT_BEDTIME_WORDS_PER_MINUTE,
    minimum_words_per_minute: int = MIN_BEDTIME_WORDS_PER_MINUTE,
    maximum_words_per_minute: int = MAX_BEDTIME_WORDS_PER_MINUTE,
) -> RuntimeEstimate:
    if word_count <= 0:
        return RuntimeEstimate(
            target_minutes=0,
            minimum_minutes=0,
            maximum_minutes=0,
            assumed_words_per_minute=assumed_words_per_minute,
            minimum_words_per_minute=minimum_words_per_minute,
            maximum_words_per_minute=maximum_words_per_minute,
        )

    effective_assumed_wpm = assumed_words_per_minute * playback_speed
    effective_min_wpm = minimum_words_per_minute * playback_speed
    effective_max_wpm = maximum_words_per_minute * playback_speed
    target_minutes = max(1, round(word_count / effective_assumed_wpm))
    minimum_minutes = max(1, math.floor(word_count / effective_max_wpm))
    maximum_minutes = max(minimum_minutes, math.ceil(word_count / effective_min_wpm))

    return RuntimeEstimate(
        target_minutes=min(max(target_minutes, minimum_minutes), maximum_minutes),
        minimum_minutes=minimum_minutes,
        maximum_minutes=maximum_minutes,
        assumed_words_per_minute=assumed_words_per_minute,
        minimum_words_per_minute=minimum_words_per_minute,
        maximum_words_per_minute=maximum_words_per_minute,
    )


def estimate_word_count_from_runtime(
    runtime_minutes: int,
    *,
    playback_speed: float = 1.0,
    assumed_words_per_minute: int = DEFAULT_BEDTIME_WORDS_PER_MINUTE,
    minimum_words_per_minute: int = MIN_BEDTIME_WORDS_PER_MINUTE,
    maximum_words_per_minute: int = MAX_BEDTIME_WORDS_PER_MINUTE,
) -> WordCountEstimate:
    if runtime_minutes <= 0:
        return WordCountEstimate(
            target_word_count=0,
            minimum_word_count=0,
            maximum_word_count=0,
            assumed_words_per_minute=assumed_words_per_minute,
            minimum_words_per_minute=minimum_words_per_minute,
            maximum_words_per_minute=maximum_words_per_minute,
        )

    effective_assumed_wpm = assumed_words_per_minute * playback_speed
    effective_min_wpm = minimum_words_per_minute * playback_speed
    effective_max_wpm = maximum_words_per_minute * playback_speed

    return WordCountEstimate(
        target_word_count=max(1, round(runtime_minutes * effective_assumed_wpm)),
        minimum_word_count=max(1, math.floor(runtime_minutes * effective_min_wpm)),
        maximum_word_count=max(1, math.ceil(runtime_minutes * effective_max_wpm)),
        assumed_words_per_minute=assumed_words_per_minute,
        minimum_words_per_minute=minimum_words_per_minute,
        maximum_words_per_minute=maximum_words_per_minute,
    )


def estimate_chapter_size_from_word_count(
    total_word_count: int,
    chapter_count: int,
    *,
    variability_ratio: float = DEFAULT_CHAPTER_VARIANCE_RATIO,
) -> ChapterSizeEstimate:
    if total_word_count <= 0 or chapter_count <= 0:
        return ChapterSizeEstimate(
            average_words_per_chapter=0,
            minimum_words_per_chapter=0,
            maximum_words_per_chapter=0,
            chapter_count=max(chapter_count, 0),
            total_word_count=max(total_word_count, 0),
            variability_ratio=variability_ratio,
        )

    average_words_per_chapter = max(1, round(total_word_count / chapter_count))
    variability_delta = average_words_per_chapter * variability_ratio

    return ChapterSizeEstimate(
        average_words_per_chapter=average_words_per_chapter,
        minimum_words_per_chapter=max(1, math.floor(average_words_per_chapter - variability_delta)),
        maximum_words_per_chapter=max(
            average_words_per_chapter,
            math.ceil(average_words_per_chapter + variability_delta),
        ),
        chapter_count=chapter_count,
        total_word_count=total_word_count,
        variability_ratio=variability_ratio,
    )


def infer_words_per_minute(word_count: int, runtime_minutes: int) -> int:
    if word_count <= 0 or runtime_minutes <= 0:
        return 0

    return max(1, round(word_count / runtime_minutes))


def classify_narration_pacing(words_per_minute: int) -> NarrationPacingBand:
    if words_per_minute <= 0:
        return "balanced"
    if words_per_minute < MIN_BEDTIME_WORDS_PER_MINUTE:
        return "roomy"
    if words_per_minute > MAX_BEDTIME_WORDS_PER_MINUTE:
        return "brisk"
    return "balanced"


def estimate_narration_duration_seconds(
    word_count: int,
    *,
    playback_speed: float = 1.0,
    words_per_minute: int = DEFAULT_BEDTIME_WORDS_PER_MINUTE,
) -> int:
    if word_count <= 0:
        return 0

    effective_words_per_minute = words_per_minute * playback_speed
    return int(math.ceil((word_count / effective_words_per_minute) * 60))


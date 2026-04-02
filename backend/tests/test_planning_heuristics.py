from app.services.planning_heuristics import (
    classify_narration_pacing,
    estimate_chapter_size_from_word_count,
    estimate_narration_duration_seconds,
    estimate_runtime_from_word_count,
    estimate_word_count_from_runtime,
    infer_words_per_minute,
)


def test_estimate_runtime_from_word_count_uses_bedtime_range() -> None:
    estimate = estimate_runtime_from_word_count(1800)

    assert estimate.target_minutes == 13
    assert estimate.minimum_minutes == 11
    assert estimate.maximum_minutes == 15
    assert estimate.assumed_words_per_minute == 140
    assert estimate.minimum_words_per_minute == 120
    assert estimate.maximum_words_per_minute == 160


def test_estimate_word_count_from_runtime_uses_bedtime_range() -> None:
    estimate = estimate_word_count_from_runtime(12)

    assert estimate.target_word_count == 1680
    assert estimate.minimum_word_count == 1440
    assert estimate.maximum_word_count == 1920
    assert estimate.assumed_words_per_minute == 140


def test_estimate_chapter_size_from_word_count_allows_modest_variation() -> None:
    estimate = estimate_chapter_size_from_word_count(1800, 3)

    assert estimate.average_words_per_chapter == 600
    assert estimate.minimum_words_per_chapter == 510
    assert estimate.maximum_words_per_chapter == 690
    assert estimate.variability_ratio == 0.15


def test_words_per_minute_inference_classifies_pacing_bands() -> None:
    assert infer_words_per_minute(1800, 12) == 150
    assert classify_narration_pacing(100) == "roomy"
    assert classify_narration_pacing(150) == "balanced"
    assert classify_narration_pacing(190) == "brisk"


def test_estimate_narration_duration_seconds_respects_playback_speed() -> None:
    assert estimate_narration_duration_seconds(400, playback_speed=0.8) == 215

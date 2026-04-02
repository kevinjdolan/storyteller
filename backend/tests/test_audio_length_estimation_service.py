from __future__ import annotations

from types import SimpleNamespace

from app.db import CompositionSegmentAcceptanceState, JobStatus
from app.services.audio_length_estimation import (
    AudioLengthEstimateInput,
    estimate_audio_length,
)
from app.services.audio_settings import build_audio_runtime_estimate


def test_estimate_audio_length_accounts_for_speed_and_chapter_pauses() -> None:
    estimate = estimate_audio_length(
        AudioLengthEstimateInput(
            word_count=1800,
            playback_speed=0.95,
            chapter_count=3,
        )
    )

    assert estimate.word_count == 1800
    assert estimate.chapter_count == 3
    assert estimate.chapter_pause_count == 2
    assert estimate.chapter_pause_seconds == 3
    assert estimate.total_chapter_pause_seconds == 6
    assert estimate.target_duration_seconds == 825
    assert estimate.minimum_duration_seconds == 705
    assert estimate.maximum_duration_seconds == 960
    assert estimate.assumed_words_per_minute == 140
    assert estimate.minimum_words_per_minute == 120
    assert estimate.maximum_words_per_minute == 160
    assert estimate.pacing_band == "balanced"


def test_estimate_audio_length_returns_zero_durations_without_words() -> None:
    estimate = estimate_audio_length(
        AudioLengthEstimateInput(
            word_count=0,
            playback_speed=1.0,
            chapter_count=4,
        )
    )

    assert estimate.target_duration_seconds == 0
    assert estimate.minimum_duration_seconds == 0
    assert estimate.maximum_duration_seconds == 0
    assert estimate.chapter_pause_count == 3
    assert estimate.total_chapter_pause_seconds == 9


def test_build_audio_runtime_estimate_prefers_story_setup_and_outline_chapters() -> None:
    estimate = build_audio_runtime_estimate(
        selected_story_setup=SimpleNamespace(
            target_word_count=2100,
            chapter_count=None,
        ),
        selected_story_outline=SimpleNamespace(
            outline_kind="chapter",
            cards=[
                {"card_key": "chapter-1"},
                {"card_key": "chapter-2"},
                {"card_key": "chapter-3"},
                {"card_key": "chapter-4"},
            ],
        ),
        playback_speed=1.0,
    )

    assert estimate is not None
    assert estimate.basis_source == "story_setup_target"
    assert estimate.estimated_word_count == 2100
    assert estimate.estimated_chapter_count == 4
    assert estimate.chapter_pause_count == 3
    assert estimate.total_chapter_pause_seconds == 9
    assert estimate.target_duration_seconds == 915
    assert estimate.minimum_duration_seconds == 795
    assert estimate.maximum_duration_seconds == 1065


def test_build_audio_runtime_estimate_prefers_accepted_segment_words() -> None:
    accepted_segment = SimpleNamespace(
        segment_index=0,
        status=JobStatus.COMPLETED,
        completed_at=None,
        acceptance_state=CompositionSegmentAcceptanceState.ACCEPTED,
        superseded_by_segment_id=None,
        word_count=620,
        accepted_text=None,
        text_content=None,
    )
    pending_segment = SimpleNamespace(
        segment_index=1,
        status=JobStatus.IN_PROGRESS,
        completed_at=None,
        acceptance_state=CompositionSegmentAcceptanceState.ACCEPTED,
        superseded_by_segment_id=None,
        word_count=400,
        accepted_text=None,
        text_content=None,
    )

    estimate = build_audio_runtime_estimate(
        composition_segments=[accepted_segment, pending_segment],
        selected_story_setup=SimpleNamespace(target_word_count=1800, chapter_count=2),
        playback_speed=1.0,
    )

    assert estimate is not None
    assert estimate.basis_source == "composition_segments"
    assert estimate.estimated_word_count == 620
    assert estimate.estimated_chapter_count == 2
    assert estimate.chapter_pause_count == 1

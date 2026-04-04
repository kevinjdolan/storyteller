from __future__ import annotations

from datetime import datetime, timezone

import pytest
from app.db import (
    AudioJob,
    Base,
    CompositionJob,
    CompositionJobKind,
    CompositionSegment,
    JobStatus,
    NarrationMusicTransitionHint,
    NarrationPauseHint,
    NarrationSourceBoundaryKind,
    StoryOutline,
    StorySession,
    make_engine,
)
from app.services.narration_segmentation import NarrationSegmentationService
from sqlalchemy.orm import sessionmaker


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


def test_create_plan_uses_chapter_boundaries_and_offsets(db_session) -> None:
    now = datetime.now(timezone.utc)
    story_session = StorySession(working_title="Moonlit Harbor")
    db_session.add(story_session)
    db_session.flush()

    db_session.add(
        StoryOutline(
            session_id=story_session.id,
            revision_number=1,
            outline_kind="chapter",
            summary="Three chapter plan.",
            cards=[
                {
                    "card_key": "chapter-1",
                    "card_type": "chapter",
                    "position": 1,
                    "title": "Chapter 1",
                    "summary": "Open on the harbor.",
                    "beat_keys": ["opening_image"],
                    "beat_labels": ["Opening Image"],
                    "emotional_shift": "Stillness into motion.",
                },
                {
                    "card_key": "chapter-2",
                    "card_type": "chapter",
                    "position": 2,
                    "title": "Chapter 2",
                    "summary": "Follow the bell.",
                    "beat_keys": ["midpoint"],
                    "beat_labels": ["Midpoint"],
                    "emotional_shift": "Wonder deepens.",
                },
                {
                    "card_key": "chapter-3",
                    "card_type": "chapter",
                    "position": 3,
                    "title": "Chapter 3",
                    "summary": "Return to rest.",
                    "beat_keys": ["finale"],
                    "beat_labels": ["Finale"],
                    "emotional_shift": "Repair into calm.",
                },
            ],
            is_selected=True,
            accepted_at=now,
        )
    )
    composition_job = CompositionJob(
        session_id=story_session.id,
        job_kind=CompositionJobKind.DRAFT,
        status=JobStatus.COMPLETED,
        progress_percent=100,
        completed_at=now,
    )
    db_session.add(composition_job)
    db_session.flush()

    chapter_texts = [
        "Moonlight silvered the harbor while Mira listened for the buoy.",
        "The drifting bell led her gently past reeds and sleeping boats.",
        "She guided it home, and the whole water settled into rest.",
    ]
    for index, text in enumerate(chapter_texts, start=1):
        db_session.add(
            CompositionSegment(
                session_id=story_session.id,
                composition_job_id=composition_job.id,
                segment_index=index,
                revision_number=1,
                status=JobStatus.COMPLETED,
                accepted_text=text,
                text_content=text,
                word_count=len(text.split()),
                payload={
                    "outline_kind": "chapter",
                    "outline_card_key": f"chapter-{index}",
                    "outline_card_title": f"Chapter {index}",
                },
                completed_at=now,
            )
        )
    db_session.flush()

    audio_job = AudioJob(
        session_id=story_session.id,
        source_composition_job_id=composition_job.id,
        status=JobStatus.IN_PROGRESS,
        voice_key="moonbeam",
        playback_speed=1.0,
        include_background_music=True,
        started_at=now,
    )
    db_session.add(audio_job)
    db_session.flush()

    result = NarrationSegmentationService(db_session).create_plan(
        session_id=story_session.id,
        audio_job_id=audio_job.id,
    )

    assert result.total_segments == 3
    assert [segment.segment_index for segment in result.segments] == [1, 2, 3]
    assert [segment.text_content for segment in result.segments] == chapter_texts
    assert all(
        segment.source_boundary_kind == NarrationSourceBoundaryKind.CHAPTER
        for segment in result.segments
    )
    assert result.segments[0].text_start_offset == 0
    assert result.segments[0].text_end_offset == len(chapter_texts[0])
    assert result.segments[1].text_start_offset == len(chapter_texts[0]) + 2
    assert result.segments[2].text_start_offset == (
        len(chapter_texts[0]) + len(chapter_texts[1]) + 4
    )
    assert result.segments[0].pause_after_seconds == 3
    assert result.segments[0].pause_hint == NarrationPauseHint.CHAPTER_BREAK
    assert result.segments[1].pause_after_seconds == 3
    assert result.segments[1].music_transition_hint == (
        NarrationMusicTransitionHint.SOFT_RESET
    )
    assert result.segments[2].pause_after_seconds == 0
    assert result.segments[2].music_transition_hint == (
        NarrationMusicTransitionHint.END_STORY
    )


def test_create_plan_splits_large_segment_on_sentence_boundaries(db_session) -> None:
    now = datetime.now(timezone.utc)
    story_session = StorySession(working_title="Sentence Split")
    db_session.add(story_session)
    db_session.flush()

    composition_job = CompositionJob(
        session_id=story_session.id,
        job_kind=CompositionJobKind.DRAFT,
        status=JobStatus.COMPLETED,
        progress_percent=100,
        completed_at=now,
    )
    db_session.add(composition_job)
    db_session.flush()

    text = (
        "Mira watched the lantern ripple softly tonight. "
        "Pip answered with a sleepy nod beside her. "
        "Together they let the harbor grow quiet again."
    )
    composition_segment = CompositionSegment(
        session_id=story_session.id,
        composition_job_id=composition_job.id,
        segment_index=1,
        revision_number=1,
        status=JobStatus.COMPLETED,
        accepted_text=text,
        text_content=text,
        word_count=len(text.split()),
        payload={
            "outline_kind": "scene",
            "outline_card_key": "scene-1",
            "outline_card_title": "Scene 1",
        },
        completed_at=now,
    )
    db_session.add(composition_segment)
    db_session.flush()

    audio_job = AudioJob(
        session_id=story_session.id,
        source_composition_job_id=composition_job.id,
        status=JobStatus.IN_PROGRESS,
        voice_key="moonbeam",
        playback_speed=1.0,
        include_background_music=False,
        started_at=now,
    )
    db_session.add(audio_job)
    db_session.flush()

    result = NarrationSegmentationService(
        db_session,
        max_words_per_segment=8,
    ).create_plan(
        session_id=story_session.id,
        audio_job_id=audio_job.id,
    )

    assert result.total_segments == 3
    assert [segment.word_count for segment in result.segments] == [7, 8, 8]
    assert [segment.text_content for segment in result.segments] == [
        "Mira watched the lantern ripple softly tonight.",
        "Pip answered with a sleepy nod beside her.",
        "Together they let the harbor grow quiet again.",
    ]
    assert all(
        segment.source_boundary_kind == NarrationSourceBoundaryKind.SCENE
        for segment in result.segments
    )
    assert result.segments[0].pause_hint == NarrationPauseHint.NONE
    assert result.segments[0].music_transition_hint == (
        NarrationMusicTransitionHint.CONTINUE_BED
    )
    assert result.segments[-1].music_transition_hint == (
        NarrationMusicTransitionHint.END_STORY
    )
    assert result.segments[0].metadata_json["split_reason"] == "sentence_group"


def test_create_plan_applies_chapter_break_only_to_last_split_segment(db_session) -> None:
    now = datetime.now(timezone.utc)
    story_session = StorySession(working_title="Split Chapter Boundaries")
    db_session.add(story_session)
    db_session.flush()

    composition_job = CompositionJob(
        session_id=story_session.id,
        job_kind=CompositionJobKind.DRAFT,
        status=JobStatus.COMPLETED,
        progress_percent=100,
        completed_at=now,
    )
    db_session.add(composition_job)
    db_session.flush()

    chapter_one_text = (
        "Mira followed the bell beside sleeping skiffs. "
        "Soft lantern light kept every ripple readable."
    )
    chapter_two_text = "She tucked it home and the harbor rested."
    for index, text in enumerate((chapter_one_text, chapter_two_text), start=1):
        db_session.add(
            CompositionSegment(
                session_id=story_session.id,
                composition_job_id=composition_job.id,
                segment_index=index,
                revision_number=1,
                status=JobStatus.COMPLETED,
                accepted_text=text,
                text_content=text,
                word_count=len(text.split()),
                payload={
                    "outline_kind": "chapter",
                    "outline_card_key": f"chapter-{index}",
                    "outline_card_title": f"Chapter {index}",
                },
                completed_at=now,
            )
        )
    db_session.flush()

    audio_job = AudioJob(
        session_id=story_session.id,
        source_composition_job_id=composition_job.id,
        status=JobStatus.IN_PROGRESS,
        voice_key="moonbeam",
        playback_speed=1.0,
        include_background_music=True,
        started_at=now,
    )
    db_session.add(audio_job)
    db_session.flush()

    result = NarrationSegmentationService(
        db_session,
        max_words_per_segment=8,
    ).create_plan(
        session_id=story_session.id,
        audio_job_id=audio_job.id,
    )

    assert result.total_segments == 3
    assert [segment.text_content for segment in result.segments] == [
        "Mira followed the bell beside sleeping skiffs.",
        "Soft lantern light kept every ripple readable.",
        chapter_two_text,
    ]
    assert result.segments[0].pause_after_seconds == 0
    assert result.segments[0].pause_hint == NarrationPauseHint.NONE
    assert result.segments[0].music_transition_hint == (
        NarrationMusicTransitionHint.CONTINUE_BED
    )
    assert result.segments[1].pause_after_seconds == 3
    assert result.segments[1].pause_hint == NarrationPauseHint.CHAPTER_BREAK
    assert result.segments[1].music_transition_hint == (
        NarrationMusicTransitionHint.SOFT_RESET
    )
    assert result.segments[2].music_transition_hint == (
        NarrationMusicTransitionHint.END_STORY
    )
    assert result.segments[0].metadata_json["ends_source_boundary"] is False
    assert result.segments[1].metadata_json["ends_source_boundary"] is True

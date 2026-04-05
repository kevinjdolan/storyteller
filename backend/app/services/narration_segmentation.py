from __future__ import annotations

import re
from collections.abc import Sequence
from dataclasses import dataclass

from sqlalchemy import Select, delete, select
from sqlalchemy.orm import Session

from app.db import (
    AudioJob,
    CompositionSegment,
    CompositionSegmentAcceptanceState,
    JobStatus,
    NarrationMusicTransitionHint,
    NarrationPauseHint,
    NarrationSegment,
    NarrationSourceBoundaryKind,
    StoryOutline,
)
from app.services.audio_length_estimation import DEFAULT_AUDIO_CHAPTER_PAUSE_SECONDS

DEFAULT_NARRATION_MAX_WORDS_PER_SEGMENT = 650
_WORD_PATTERN = re.compile(r"\S+")
_PARAGRAPH_SPAN_PATTERN = re.compile(r"\S[\s\S]*?(?:(?=\n\n+\S)|\Z)")
_SENTENCE_SPAN_PATTERN = re.compile(r"\S[\s\S]*?(?:(?<=[.!?])(?:\s+)|\Z)")


class NarrationSegmentationError(ValueError):
    """Raised when a durable narration plan cannot be created."""


@dataclass(frozen=True)
class NarrationPlanResult:
    segments: list[NarrationSegment]
    total_words: int
    compiled_text_length: int

    @property
    def total_segments(self) -> int:
        return len(self.segments)


@dataclass(frozen=True)
class _SourceStorySegment:
    composition_segment_id: str
    composition_segment_index: int
    source_boundary_kind: NarrationSourceBoundaryKind
    source_outline_card_key: str | None
    source_outline_card_title: str | None
    text_content: str
    text_start_offset: int
    text_end_offset: int


@dataclass(frozen=True)
class _SegmentSpan:
    start: int
    end: int
    split_reason: str
    ends_source_boundary: bool


class NarrationSegmentationService:
    def __init__(
        self,
        session: Session,
        *,
        max_words_per_segment: int = DEFAULT_NARRATION_MAX_WORDS_PER_SEGMENT,
        chapter_pause_seconds: int = DEFAULT_AUDIO_CHAPTER_PAUSE_SECONDS,
    ) -> None:
        self._session = session
        self._max_words_per_segment = max(1, max_words_per_segment)
        self._chapter_pause_seconds = max(0, chapter_pause_seconds)

    def create_plan(
        self,
        *,
        session_id: str,
        audio_job_id: str,
    ) -> NarrationPlanResult:
        audio_job = self._session.get(AudioJob, audio_job_id)
        if audio_job is None or audio_job.session_id != session_id:
            raise NarrationSegmentationError(
                f"audio job {audio_job_id!r} does not belong to session {session_id!r}",
            )

        source_segments = self._load_current_story_segments(session_id)
        if not source_segments:
            raise NarrationSegmentationError(
                "cannot build narration segments without accepted story text",
            )

        self._session.execute(
            delete(NarrationSegment).where(NarrationSegment.audio_job_id == audio_job_id)
        )

        planned_segments = self._build_narration_segments(
            session_id=session_id,
            audio_job_id=audio_job_id,
            source_segments=source_segments,
        )
        self._session.add_all(planned_segments)
        self._session.flush()

        return NarrationPlanResult(
            segments=planned_segments,
            total_words=sum(segment.word_count for segment in planned_segments),
            compiled_text_length=source_segments[-1].text_end_offset,
        )

    def _build_narration_segments(
        self,
        *,
        session_id: str,
        audio_job_id: str,
        source_segments: Sequence[_SourceStorySegment],
    ) -> list[NarrationSegment]:
        planned_segments: list[NarrationSegment] = []

        for source_segment in source_segments:
            spans = self._split_source_segment(source_segment.text_content)
            for local_index, span in enumerate(spans, start=1):
                local_start, local_end = _trim_span(
                    source_segment.text_content,
                    span.start,
                    span.end,
                )
                segment_text = source_segment.text_content[local_start:local_end]
                if not segment_text:
                    continue
                planned_segments.append(
                    NarrationSegment(
                        session_id=session_id,
                        audio_job_id=audio_job_id,
                        source_composition_segment_id=source_segment.composition_segment_id,
                        segment_index=len(planned_segments) + 1,
                        status=JobStatus.QUEUED,
                        source_boundary_kind=source_segment.source_boundary_kind,
                        source_outline_card_key=source_segment.source_outline_card_key,
                        source_outline_card_title=source_segment.source_outline_card_title,
                        text_content=segment_text,
                        word_count=_count_words(segment_text),
                        text_start_offset=source_segment.text_start_offset + local_start,
                        text_end_offset=source_segment.text_start_offset + local_end,
                        pause_after_seconds=0,
                        pause_hint=NarrationPauseHint.NONE,
                        music_transition_hint=NarrationMusicTransitionHint.CONTINUE_BED,
                        metadata_json={
                            "split_reason": span.split_reason,
                            "source_local_start_offset": local_start,
                            "source_local_end_offset": local_end,
                            "source_local_part_index": local_index,
                            "source_local_part_count": len(spans),
                            "ends_source_boundary": span.ends_source_boundary,
                        },
                    )
                )

        if not planned_segments:
            raise NarrationSegmentationError("narration planning produced no segments")

        for index, segment in enumerate(planned_segments):
            is_last_segment = index == len(planned_segments) - 1
            metadata = (
                dict(segment.metadata_json) if isinstance(segment.metadata_json, dict) else {}
            )
            ends_source_boundary = bool(metadata.get("ends_source_boundary"))

            if is_last_segment:
                segment.pause_after_seconds = 0
                segment.pause_hint = NarrationPauseHint.NONE
                segment.music_transition_hint = NarrationMusicTransitionHint.END_STORY
                continue

            if (
                ends_source_boundary
                and segment.source_boundary_kind == NarrationSourceBoundaryKind.CHAPTER
            ):
                segment.pause_after_seconds = self._chapter_pause_seconds
                segment.pause_hint = NarrationPauseHint.CHAPTER_BREAK
                segment.music_transition_hint = NarrationMusicTransitionHint.SOFT_RESET
                continue

            segment.pause_after_seconds = 0
            segment.pause_hint = NarrationPauseHint.NONE
            segment.music_transition_hint = NarrationMusicTransitionHint.CONTINUE_BED

        return planned_segments

    def _load_current_story_segments(self, session_id: str) -> list[_SourceStorySegment]:
        selected_outline = self._load_selected_story_outline(session_id)
        accepted_segments = self._load_latest_current_composition_segments(session_id)

        source_segments: list[_SourceStorySegment] = []
        cursor = 0
        for composition_segment in accepted_segments:
            text_content = (
                composition_segment.accepted_text or composition_segment.text_content or ""
            ).strip()
            if not text_content:
                continue

            if source_segments:
                cursor += 2
            text_start_offset = cursor
            text_end_offset = text_start_offset + len(text_content)
            cursor = text_end_offset

            outline_kind, outline_card_key, outline_card_title = _resolve_outline_context(
                composition_segment=composition_segment,
                selected_outline=selected_outline,
            )
            source_segments.append(
                _SourceStorySegment(
                    composition_segment_id=composition_segment.id,
                    composition_segment_index=composition_segment.segment_index,
                    source_boundary_kind=_coerce_boundary_kind(outline_kind),
                    source_outline_card_key=outline_card_key,
                    source_outline_card_title=outline_card_title,
                    text_content=text_content,
                    text_start_offset=text_start_offset,
                    text_end_offset=text_end_offset,
                )
            )

        return source_segments

    def _load_selected_story_outline(self, session_id: str) -> StoryOutline | None:
        stmt: Select[tuple[StoryOutline]] = (
            select(StoryOutline)
            .where(
                StoryOutline.session_id == session_id,
                StoryOutline.is_selected.is_(True),
            )
            .order_by(StoryOutline.revision_number.desc())
            .limit(1)
        )
        return self._session.execute(stmt).scalar_one_or_none()

    def _load_latest_current_composition_segments(
        self,
        session_id: str,
    ) -> list[CompositionSegment]:
        stmt: Select[tuple[CompositionSegment]] = (
            select(CompositionSegment)
            .where(CompositionSegment.session_id == session_id)
            .order_by(
                CompositionSegment.segment_index.asc(),
                CompositionSegment.revision_number.desc(),
            )
        )
        rows = list(self._session.execute(stmt).scalars().all())
        current_by_index: dict[int, CompositionSegment] = {}

        for row in rows:
            if row.segment_index in current_by_index:
                continue
            if row.status != JobStatus.COMPLETED and row.completed_at is None:
                continue
            if row.acceptance_state != CompositionSegmentAcceptanceState.ACCEPTED:
                continue
            if row.superseded_by_segment_id is not None:
                continue
            if not (row.accepted_text or row.text_content):
                continue
            current_by_index[row.segment_index] = row

        return [current_by_index[index] for index in sorted(current_by_index)]

    def _split_source_segment(self, text: str) -> list[_SegmentSpan]:
        if _count_words(text) <= self._max_words_per_segment:
            return [
                _SegmentSpan(
                    start=0,
                    end=len(text),
                    split_reason="whole_segment",
                    ends_source_boundary=True,
                )
            ]

        paragraph_spans = _find_spans(_PARAGRAPH_SPAN_PATTERN, text)
        grouped_spans = self._group_spans(text, paragraph_spans)

        final_spans: list[_SegmentSpan] = []
        for group_start, group_end in grouped_spans:
            group_text = text[group_start:group_end]
            if _count_words(group_text) <= self._max_words_per_segment:
                final_spans.append(
                    _SegmentSpan(
                        start=group_start,
                        end=group_end,
                        split_reason="paragraph_group",
                        ends_source_boundary=False,
                    )
                )
                continue

            sentence_spans = _find_spans(_SENTENCE_SPAN_PATTERN, group_text)
            sentence_groups = self._group_spans(group_text, sentence_spans)
            for sentence_start, sentence_end in sentence_groups:
                sentence_text = group_text[sentence_start:sentence_end]
                if _count_words(sentence_text) <= self._max_words_per_segment:
                    final_spans.append(
                        _SegmentSpan(
                            start=group_start + sentence_start,
                            end=group_start + sentence_end,
                            split_reason="sentence_group",
                            ends_source_boundary=False,
                        )
                    )
                    continue

                for word_start, word_end in _word_limited_spans(
                    sentence_text,
                    max_words=self._max_words_per_segment,
                ):
                    final_spans.append(
                        _SegmentSpan(
                            start=group_start + sentence_start + word_start,
                            end=group_start + sentence_start + word_end,
                            split_reason="word_group",
                            ends_source_boundary=False,
                        )
                    )

        if not final_spans:
            raise NarrationSegmentationError("failed to split narration text into segments")

        normalized_spans: list[_SegmentSpan] = []
        for index, span in enumerate(final_spans):
            normalized_spans.append(
                _SegmentSpan(
                    start=span.start,
                    end=span.end,
                    split_reason=span.split_reason,
                    ends_source_boundary=index == len(final_spans) - 1,
                )
            )
        return normalized_spans

    def _group_spans(
        self,
        text: str,
        spans: Sequence[tuple[int, int]],
    ) -> list[tuple[int, int]]:
        if not spans:
            return [(0, len(text))]

        grouped: list[tuple[int, int]] = []
        current_start: int | None = None
        current_end: int | None = None

        for span_start, span_end in spans:
            if current_start is None or current_end is None:
                current_start = span_start
                current_end = span_end
                continue

            candidate_text = text[current_start:span_end]
            if _count_words(candidate_text) <= self._max_words_per_segment:
                current_end = span_end
                continue

            grouped.append((current_start, current_end))
            current_start = span_start
            current_end = span_end

        assert current_start is not None and current_end is not None
        grouped.append((current_start, current_end))
        return grouped


def _resolve_outline_context(
    *,
    composition_segment: CompositionSegment,
    selected_outline: StoryOutline | None,
) -> tuple[str | None, str | None, str | None]:
    payload = composition_segment.payload if isinstance(composition_segment.payload, dict) else {}
    outline_kind = _read_optional_text(payload, "outline_kind")
    outline_card_key = _read_optional_text(payload, "outline_card_key")
    outline_card_title = _read_optional_text(payload, "outline_card_title")

    if outline_kind is not None and (
        outline_card_key is not None or outline_card_title is not None
    ):
        return outline_kind, outline_card_key, outline_card_title

    if selected_outline is None or not isinstance(selected_outline.cards, list):
        return outline_kind, outline_card_key, outline_card_title

    card = next(
        (
            item
            for item in selected_outline.cards
            if isinstance(item, dict)
            and int(item.get("position", 0) or 0) == composition_segment.segment_index
        ),
        None,
    )
    if card is None and len(selected_outline.cards) >= composition_segment.segment_index:
        maybe_card = selected_outline.cards[composition_segment.segment_index - 1]
        if isinstance(maybe_card, dict):
            card = maybe_card

    if card is None:
        return outline_kind or selected_outline.outline_kind, outline_card_key, outline_card_title

    return (
        str(card.get("card_type") or selected_outline.outline_kind),
        _normalize_optional_text(card.get("card_key")),
        _normalize_optional_text(card.get("title")),
    )


def _coerce_boundary_kind(value: str | None) -> NarrationSourceBoundaryKind:
    if value == NarrationSourceBoundaryKind.CHAPTER.value:
        return NarrationSourceBoundaryKind.CHAPTER
    if value == NarrationSourceBoundaryKind.SCENE.value:
        return NarrationSourceBoundaryKind.SCENE
    if value:
        return NarrationSourceBoundaryKind.SEGMENT
    return NarrationSourceBoundaryKind.UNKNOWN


def _find_spans(pattern: re.Pattern[str], text: str) -> list[tuple[int, int]]:
    return [match.span() for match in pattern.finditer(text)]


def _word_limited_spans(text: str, *, max_words: int) -> list[tuple[int, int]]:
    token_spans = [match.span() for match in re.finditer(r"\S+\s*", text)]
    if not token_spans:
        return [(0, len(text))]

    spans: list[tuple[int, int]] = []
    current_start: int | None = None
    current_end: int | None = None
    current_word_count = 0

    for token_start, token_end in token_spans:
        if current_start is None:
            current_start = token_start
        current_end = token_end
        current_word_count += 1
        if current_word_count >= max_words:
            spans.append((current_start, current_end))
            current_start = None
            current_end = None
            current_word_count = 0

    if current_start is not None and current_end is not None:
        spans.append((current_start, current_end))

    return spans


def _count_words(text: str) -> int:
    return len(_WORD_PATTERN.findall(text))


def _trim_span(text: str, start: int, end: int) -> tuple[int, int]:
    while start < end and text[start].isspace():
        start += 1
    while end > start and text[end - 1].isspace():
        end -= 1
    return start, end


def _read_optional_text(payload: dict[str, object], key: str) -> str | None:
    value = payload.get(key)
    return _normalize_optional_text(value)


def _normalize_optional_text(value: object) -> str | None:
    if not isinstance(value, str):
        return None
    normalized = value.strip()
    return normalized or None

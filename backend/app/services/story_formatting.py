from __future__ import annotations

import re
from collections.abc import Iterable

from app.models.session import (
    StoryReaderBlockView,
    StoryReaderDocumentView,
    StoryReaderSpanStyle,
    StoryReaderSpanView,
)

_ATX_HEADING_PATTERN = re.compile(r"^(#{1,6})\s+(.+?)(?:\s+#+\s*)?$")
_CHAPTER_HEADING_PATTERN = re.compile(
    r"^(chapter|part|prologue|epilogue)\b(?:\s+[\w][\w\s'’:,.!?-]*)?$",
    re.IGNORECASE,
)
_WORD_PATTERN = re.compile(r"\b[\w']+\b")

_INLINE_PATTERNS: tuple[tuple[StoryReaderSpanStyle, re.Pattern[str]], ...] = (
    (
        "strong_emphasis",
        re.compile(r"(?<!\*)\*\*\*(?!\s)(.+?)(?<!\s)\*\*\*(?!\*)"),
    ),
    (
        "strong_emphasis",
        re.compile(r"(?<!_)___(?![\s_])(.+?)(?<![\s_])___(?!_)"),
    ),
    (
        "strong",
        re.compile(r"(?<!\*)\*\*(?!\s)(.+?)(?<!\s)\*\*(?!\*)"),
    ),
    (
        "strong",
        re.compile(r"(?<!_)__(?![\s_])(.+?)(?<![\s_])__(?!_)"),
    ),
    (
        "emphasis",
        re.compile(r"(?<!\*)\*(?![\s*])(.+?)(?<![\s*])\*(?!\*)"),
    ),
    (
        "emphasis",
        re.compile(r"(?<!_)_(?![\s_])(.+?)(?<![\s_])_(?!_)"),
    ),
)


def build_story_reader_document(
    story_text: str,
    *,
    asset_id: str | None = None,
) -> StoryReaderDocumentView:
    normalized_story_text = _normalize_story_text(story_text)
    blocks = _build_story_blocks(normalized_story_text)
    visible_text = "\n".join(block.text for block in blocks)

    return StoryReaderDocumentView(
        asset_id=asset_id,
        word_count=len(_WORD_PATTERN.findall(visible_text)),
        chapter_count=sum(1 for block in blocks if block.kind == "chapter_heading"),
        has_structure=any(block.kind != "paragraph" for block in blocks),
        blocks=blocks,
    )


def iter_story_docx_blocks(
    story_text: str,
) -> Iterable[StoryReaderBlockView]:
    return build_story_reader_document(story_text).blocks


def _build_story_blocks(story_text: str) -> list[StoryReaderBlockView]:
    blocks: list[StoryReaderBlockView] = []
    paragraph_lines: list[str] = []

    def flush_paragraph() -> None:
        if not paragraph_lines:
            return
        paragraph_text = " ".join(
            line.strip() for line in paragraph_lines if line.strip()
        ).strip()
        paragraph_lines.clear()
        if paragraph_text:
            blocks.append(
                StoryReaderBlockView(
                    kind="paragraph",
                    text=paragraph_text,
                    spans=_build_inline_spans(paragraph_text),
                )
            )

    for raw_line in story_text.split("\n"):
        stripped_line = raw_line.strip()
        if not stripped_line:
            flush_paragraph()
            continue

        heading = _parse_heading(stripped_line)
        if heading is not None:
            flush_paragraph()
            kind, level, text = heading
            blocks.append(
                StoryReaderBlockView(
                    kind=kind,
                    level=level,
                    text=text,
                    spans=_build_inline_spans(text),
                )
            )
            continue

        paragraph_lines.append(raw_line)

    flush_paragraph()
    return blocks


def _parse_heading(
    stripped_line: str,
) -> tuple[str, int, str] | None:
    atx_match = _ATX_HEADING_PATTERN.match(stripped_line)
    if atx_match is not None:
        heading_text = atx_match.group(2).strip()
        if not heading_text:
            return None
        level = len(atx_match.group(1))
        kind = "chapter_heading" if _is_chapter_heading(heading_text) else "heading"
        return kind, level, heading_text

    if _is_chapter_heading(stripped_line):
        return "chapter_heading", 1, stripped_line

    return None


def _build_inline_spans(text: str) -> list[StoryReaderSpanView]:
    spans: list[StoryReaderSpanView] = []
    cursor = 0

    while cursor < len(text):
        earliest_match: re.Match[str] | None = None
        earliest_style: StoryReaderSpanStyle | None = None
        for style, pattern in _INLINE_PATTERNS:
            match = pattern.search(text, cursor)
            if match is None:
                continue
            if earliest_match is None or match.start() < earliest_match.start():
                earliest_match = match
                earliest_style = style

        if earliest_match is None or earliest_style is None:
            _append_span(spans, text[cursor:], style="plain")
            break

        if earliest_match.start() > cursor:
            _append_span(spans, text[cursor : earliest_match.start()], style="plain")

        emphasized_text = earliest_match.group(1).strip()
        if emphasized_text:
            _append_span(spans, emphasized_text, style=earliest_style)

        cursor = earliest_match.end()

    return spans or [StoryReaderSpanView(text=text, style="plain")]


def _append_span(
    spans: list[StoryReaderSpanView],
    text: str,
    *,
    style: StoryReaderSpanStyle,
) -> None:
    if not text:
        return

    if spans and spans[-1].style == style:
        spans[-1] = StoryReaderSpanView(
            text=f"{spans[-1].text}{text}",
            style=style,
        )
        return

    spans.append(StoryReaderSpanView(text=text, style=style))


def _is_chapter_heading(text: str) -> bool:
    return _CHAPTER_HEADING_PATTERN.match(text) is not None


def _normalize_story_text(story_text: str) -> str:
    return story_text.replace("\r\n", "\n").replace("\r", "\n").strip()

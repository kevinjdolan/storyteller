from __future__ import annotations

import re
from collections.abc import Sequence

STREAMING_MIN_CHUNK_WORDS = 8
STREAMING_MAX_CHUNK_WORDS = 22
STREAMING_TARGET_CHUNK_CHARACTERS = 120

_PARAGRAPH_BREAK_PATTERN = re.compile(r"(\n\n+)")
_STREAM_BOUNDARY_PATTERN = re.compile(r"""[.!?;:]["')\]]*$""")


def build_accepted_story_so_far(
    completed_segments: Sequence[str],
    current_text: str | None = None,
) -> str | None:
    parts = [segment.strip() for segment in completed_segments if segment and segment.strip()]
    if current_text is not None and current_text.strip():
        parts.append(current_text.strip())

    if not parts:
        return None

    return "\n\n".join(parts)


def split_text_for_streaming(prefix: str, remaining_text: str) -> list[str]:
    del prefix

    if not remaining_text:
        return []

    chunks: list[str] = []
    pending_break = ""
    parts = _PARAGRAPH_BREAK_PATTERN.split(remaining_text)
    for part in parts:
        if not part:
            continue

        if _PARAGRAPH_BREAK_PATTERN.fullmatch(part):
            pending_break += part
            continue

        paragraph_chunks = _split_paragraph_text(part)
        if not paragraph_chunks:
            continue

        paragraph_chunks[0] = f"{pending_break}{paragraph_chunks[0]}"
        pending_break = ""
        chunks.extend(paragraph_chunks)

    if pending_break:
        if chunks:
            chunks[-1] = f"{chunks[-1]}{pending_break}"
        else:
            chunks.append(pending_break)

    return chunks


def _split_paragraph_text(paragraph: str) -> list[str]:
    tokens = re.findall(r"\S+\s*", paragraph)
    if not tokens:
        return []

    chunks: list[str] = []
    current_tokens: list[str] = []
    current_word_count = 0
    current_character_count = 0

    for token in tokens:
        stripped = token.strip()
        if not stripped:
            continue

        current_tokens.append(token)
        current_word_count += 1
        current_character_count += len(token)

        should_flush = False
        if current_word_count >= STREAMING_MAX_CHUNK_WORDS:
            should_flush = True
        elif current_word_count >= STREAMING_MIN_CHUNK_WORDS and (
            current_character_count >= STREAMING_TARGET_CHUNK_CHARACTERS
            or _STREAM_BOUNDARY_PATTERN.search(stripped) is not None
        ):
            should_flush = True

        if should_flush:
            chunks.append("".join(current_tokens))
            current_tokens = []
            current_word_count = 0
            current_character_count = 0

    if current_tokens:
        chunks.append("".join(current_tokens))

    return chunks

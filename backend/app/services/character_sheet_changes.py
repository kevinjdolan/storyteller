from __future__ import annotations

from app.models.chat_actions import CharacterChangeImpact

_MINOR_CHANGE_KEYWORDS = (
    "voice",
    "tone",
    "softer",
    "soften",
    "gentler",
    "gentle",
    "warmer",
    "quieter",
    "calmer",
    "dialogue",
    "wording",
    "phrasing",
    "polish",
    "bedtime note",
    "bedtime-safe",
    "visual",
    "motif",
)
_MAJOR_CHANGE_KEYWORDS = (
    "add a character",
    "remove a character",
    "replace",
    "rename",
    "sibling",
    "guardian",
    "mentor",
    "relationship",
    "dynamic",
    "family",
    "support cast",
    "cast",
    "protagonist",
    "goal",
    "flaw",
    "motivation",
    "backstory",
    "role",
)


def infer_character_change_impact(
    *,
    instructions: str,
    change_summary: str | None = None,
) -> CharacterChangeImpact:
    text = " ".join(part for part in (change_summary, instructions) if part).lower()

    if any(keyword in text for keyword in _MINOR_CHANGE_KEYWORDS):
        if not any(keyword in text for keyword in _MAJOR_CHANGE_KEYWORDS):
            return CharacterChangeImpact.MINOR

    if any(keyword in text for keyword in _MAJOR_CHANGE_KEYWORDS):
        return CharacterChangeImpact.MAJOR

    return CharacterChangeImpact.MAJOR

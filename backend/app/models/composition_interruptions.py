from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict


def build_composition_interruption_message(
    *,
    request_kind: str,
    state: str,
    requested_progress_percent: float | None = None,
    requested_segment_index: int | None = None,
    rewrite_from_segment_index: int | None = None,
    resolution_summary: str | None = None,
) -> str:
    if state == "applying":
        if request_kind == "redirect":
            target_segment = rewrite_from_segment_index or requested_segment_index
            if target_segment is not None:
                return f"Applying the redirect from segment {target_segment}."
            return "Applying the redirect now."
        return "Applying the pause request now."

    if state in {"applied", "superseded"} and resolution_summary:
        return resolution_summary

    if request_kind == "redirect":
        target_segment = rewrite_from_segment_index or requested_segment_index
        if target_segment is not None:
            return (
                f"Rewrite requested from segment {target_segment}. "
                "The current chunk will finish saving before the redirect applies."
            )
        return "Rewrite requested. The current chunk will finish saving before it applies."

    if requested_progress_percent is not None:
        return (
            "Pause requested. The writer will stop after the current saved chunk at "
            f"about {round(requested_progress_percent)}% complete."
        )

    return "Pause requested. The writer will stop after the next safe checkpoint."


class CompositionInterruptionRequestView(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    request_kind: str
    state: str
    origin: str
    message: str
    instructions: str | None = None
    rewrite_from_segment_index: int | None = None
    requested_status: str | None = None
    requested_segment_id: str | None = None
    requested_segment_index: int | None = None
    requested_progress_percent: float | None = None
    resolution_summary: str | None = None
    created_at: datetime
    updated_at: datetime
    resolved_at: datetime | None = None

from __future__ import annotations

from collections.abc import Callable
from typing import Any

JobHandler = Callable[[dict[str, Any] | list[Any] | None, Any], dict[str, Any] | list[Any] | None]


class JobHandlerRegistry:
    def __init__(self) -> None:
        self._handlers: dict[str, JobHandler] = {}

    def register(self, job_type: str, handler: JobHandler) -> None:
        normalized_type = job_type.strip()
        if not normalized_type:
            raise ValueError("job_type must not be empty")
        if normalized_type in self._handlers:
            raise ValueError(f"job_type {normalized_type!r} is already registered")

        self._handlers[normalized_type] = handler

    def get(self, job_type: str) -> JobHandler | None:
        return self._handlers.get(job_type)

    def registered_job_types(self) -> tuple[str, ...]:
        return tuple(sorted(self._handlers))

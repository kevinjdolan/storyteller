from __future__ import annotations

from sqlalchemy import Select, desc, func, insert, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db import EventActorType, EventLogEntry
from app.models.workflow import WorkflowStage


class EventLogRepository:
    def __init__(self, session: Session):
        self._session = session

    def append(
        self,
        *,
        session_id: str,
        actor_type: EventActorType,
        actor_id: str | None,
        event_type: str,
        summary: str,
        payload: dict | None,
        stage: WorkflowStage | None = None,
    ) -> EventLogEntry:
        values = {
            "session_id": session_id,
            "actor_type": actor_type,
            "actor_id": actor_id,
            "event_type": event_type,
            "stage": stage,
            "summary": summary,
            "payload": payload,
        }
        for _attempt in range(5):
            values["sequence_number"] = self._next_sequence_number(session_id)
            try:
                with self._session.begin_nested():
                    stmt = insert(EventLogEntry).values(**values).returning(EventLogEntry.id)
                    entry_id = self._session.execute(stmt).scalar_one()
                entry = self._session.get(EventLogEntry, entry_id)
                if entry is None:  # pragma: no cover - defensive guard
                    raise RuntimeError("inserted event log entry could not be reloaded")
                return entry
            except IntegrityError as exc:
                if not _is_event_sequence_conflict(exc):
                    raise

        raise RuntimeError(
            "failed to allocate a unique event sequence number after retrying"
        )

    def get_latest_sequence_number(self, session_id: str) -> int | None:
        stmt = select(func.max(EventLogEntry.sequence_number)).where(
            EventLogEntry.session_id == session_id
        )
        latest_sequence = self._session.execute(stmt).scalar_one()
        return int(latest_sequence) if latest_sequence is not None else None

    def list_for_session(
        self,
        session_id: str,
        *,
        limit: int | None = None,
        after_sequence_number: int | None = None,
    ) -> list[EventLogEntry]:
        stmt: Select[tuple[EventLogEntry]] = select(EventLogEntry).where(
            EventLogEntry.session_id == session_id
        )

        if after_sequence_number is not None:
            stmt = stmt.where(EventLogEntry.sequence_number > after_sequence_number).order_by(
                EventLogEntry.sequence_number.asc()
            )
            if limit is not None:
                stmt = stmt.limit(limit)
            return list(self._session.execute(stmt).scalars().all())

        if limit is not None:
            limited_stmt = stmt.order_by(desc(EventLogEntry.sequence_number)).limit(limit)
            rows = list(self._session.execute(limited_stmt).scalars().all())
            rows.reverse()
            return rows

        ordered_stmt = stmt.order_by(EventLogEntry.sequence_number.asc())
        return list(self._session.execute(ordered_stmt).scalars().all())

    def _next_sequence_number(self, session_id: str) -> int:
        stmt = select(func.coalesce(func.max(EventLogEntry.sequence_number), 0) + 1).where(
            EventLogEntry.session_id == session_id
        )
        return int(self._session.execute(stmt).scalar_one())


def _is_event_sequence_conflict(error: IntegrityError) -> bool:
    message = str(error.orig)
    return (
        "uq_event_log_entries_session_id_sequence_number" in message
        or "event_log_entries.session_id, event_log_entries.sequence_number" in message
    )

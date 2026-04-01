from __future__ import annotations

from sqlalchemy import Select, desc, func, select
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
        entry = EventLogEntry(
            session_id=session_id,
            sequence_number=self._next_sequence_number(session_id),
            actor_type=actor_type,
            actor_id=actor_id,
            event_type=event_type,
            stage=stage,
            summary=summary,
            payload=payload,
        )
        self._session.add(entry)
        self._session.flush()
        return entry

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

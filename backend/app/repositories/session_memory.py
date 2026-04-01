from __future__ import annotations

from sqlalchemy import Select, desc, select
from sqlalchemy.orm import Session

from app.db import EventLogEntry, SessionMemorySnapshot


class SessionMemorySnapshotRepository:
    def __init__(self, session: Session):
        self._session = session

    def get_by_trigger_event_id(self, trigger_event_id: str) -> SessionMemorySnapshot | None:
        stmt: Select[tuple[SessionMemorySnapshot]] = select(SessionMemorySnapshot).where(
            SessionMemorySnapshot.trigger_event_id == trigger_event_id
        )
        return self._session.execute(stmt).scalar_one_or_none()

    def get_latest_for_session(self, session_id: str) -> SessionMemorySnapshot | None:
        stmt: Select[tuple[SessionMemorySnapshot]] = (
            select(SessionMemorySnapshot)
            .where(SessionMemorySnapshot.session_id == session_id)
            .order_by(
                desc(SessionMemorySnapshot.created_at),
                desc(SessionMemorySnapshot.id),
            )
            .limit(1)
        )
        return self._session.execute(stmt).scalar_one_or_none()

    def list_for_session(
        self,
        session_id: str,
        *,
        limit: int = 10,
    ) -> list[SessionMemorySnapshot]:
        stmt: Select[tuple[SessionMemorySnapshot]] = (
            select(SessionMemorySnapshot)
            .where(SessionMemorySnapshot.session_id == session_id)
            .order_by(
                desc(SessionMemorySnapshot.created_at),
                desc(SessionMemorySnapshot.id),
            )
            .limit(limit)
        )
        return list(self._session.execute(stmt).scalars().all())

    def create(
        self,
        session_id: str,
        *,
        summary_text: str,
        summary_data: dict,
        trigger_event: EventLogEntry | None = None,
    ) -> SessionMemorySnapshot:
        snapshot = SessionMemorySnapshot(
            session_id=session_id,
            trigger_event=trigger_event,
            trigger_event_type=trigger_event.event_type if trigger_event is not None else None,
            trigger_event_sequence_number=(
                trigger_event.sequence_number if trigger_event is not None else None
            ),
            summary_text=summary_text,
            summary_data=summary_data,
        )
        self._session.add(snapshot)
        self._session.flush()
        return snapshot

from __future__ import annotations

import logging
from datetime import timedelta
from pathlib import Path

from app.db import Base, JobStatus, StorySession, make_engine
from app.services.jobs import BackgroundJobService
from app.worker import JobHandlerRegistry, JobWorker
from sqlalchemy.orm import Session, sessionmaker


def _build_session_factory(tmp_path: Path) -> sessionmaker[Session]:
    database_path = tmp_path / "worker-runtime.db"
    engine = make_engine(f"sqlite+pysqlite:///{database_path}")

    with engine.begin() as connection:
        connection.exec_driver_sql("PRAGMA foreign_keys=ON")

    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


def test_worker_processes_a_registered_job(tmp_path: Path) -> None:
    session_factory = _build_session_factory(tmp_path)

    with session_factory() as session:
        service = BackgroundJobService(session)
        queued = service.enqueue_job(
            job_type="test.handler",
            payload={"message": "night breeze"},
        )

    registry = JobHandlerRegistry()

    def handler(payload, context):
        context.heartbeat()
        return {
            "message": payload["message"],
            "worker_id": context.worker_id,
        }

    registry.register("test.handler", handler)

    worker = JobWorker(
        session_factory=session_factory,
        registry=registry,
        worker_id="runtime-worker",
        lease_duration=timedelta(seconds=30),
        poll_interval_seconds=0.01,
    )

    assert worker.run_once() is True

    with session_factory() as session:
        job = BackgroundJobService(session).get_job(queued.id)

    assert job.status == JobStatus.COMPLETED
    assert job.result_summary == {
        "message": "night breeze",
        "worker_id": "runtime-worker",
    }
    assert job.heartbeat_at is not None


def test_worker_marks_unknown_job_types_failed(tmp_path: Path) -> None:
    session_factory = _build_session_factory(tmp_path)

    with session_factory() as session:
        service = BackgroundJobService(session)
        queued = service.enqueue_job(
            job_type="missing.handler",
            payload={"message": "no registry entry"},
        )

    worker = JobWorker(
        session_factory=session_factory,
        registry=JobHandlerRegistry(),
        worker_id="runtime-worker",
        lease_duration=timedelta(seconds=30),
        poll_interval_seconds=0.01,
    )

    assert worker.run_once() is True

    with session_factory() as session:
        job = BackgroundJobService(session).get_job(queued.id)

    assert job.status == JobStatus.FAILED
    assert job.error_message == "No handler registered for job type 'missing.handler'."


def test_worker_logs_correlated_job_context(tmp_path: Path) -> None:
    session_factory = _build_session_factory(tmp_path)

    class _ListHandler(logging.Handler):
        def __init__(self) -> None:
            super().__init__(level=logging.INFO)
            self.records: list[logging.LogRecord] = []

        def emit(self, record: logging.LogRecord) -> None:
            self.records.append(record)

    logger = logging.getLogger("app.worker.runtime")
    handler = _ListHandler()
    previous_level = logger.level
    previous_disabled = logger.disabled
    previous_global_disable = logging.root.manager.disable
    logging.disable(logging.NOTSET)
    logger.disabled = False
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)

    try:
        with session_factory() as session:
            session.add(StorySession(id="session-123"))
            session.flush()
            queued = BackgroundJobService(session).enqueue_job(
                job_type="test.handler",
                payload={"message": "night breeze"},
                session_id="session-123",
            )

        registry = JobHandlerRegistry()
        registry.register(
            "test.handler",
            lambda payload, _context: {"message": payload["message"]},
        )

        worker = JobWorker(
            session_factory=session_factory,
            registry=registry,
            worker_id="runtime-worker",
            lease_duration=timedelta(seconds=30),
            poll_interval_seconds=0.01,
        )

        assert worker.run_once() is True

        claimed_records = [
            record
            for record in handler.records
            if getattr(record, "event", None) == "worker.job.claimed"
        ]
        completed_records = [
            record
            for record in handler.records
            if getattr(record, "event", None) == "worker.job.completed"
        ]

        assert claimed_records
        assert completed_records
        claimed_fields = claimed_records[-1].event_fields
        completed_fields = completed_records[-1].event_fields
        assert claimed_fields["background_job_id"] == queued.id
        assert claimed_fields["session_id"] == "session-123"
        assert claimed_fields["worker_id"] == "runtime-worker"
        assert completed_fields["background_job_id"] == queued.id
        assert completed_fields["session_id"] == "session-123"
    finally:
        logger.removeHandler(handler)
        logger.setLevel(previous_level)
        logger.disabled = previous_disabled
        logging.disable(previous_global_disable)

from __future__ import annotations

from datetime import timedelta
from pathlib import Path

from app.db import Base, JobStatus, make_engine
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

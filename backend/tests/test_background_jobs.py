from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest
from app.db import BackgroundJob, Base, JobStatus, make_engine, utc_now
from app.repositories.jobs import POSTGRES_CLAIM_SQL
from app.services.jobs import (
    BackgroundJobLeaseLostError,
    BackgroundJobService,
)
from sqlalchemy import update
from sqlalchemy.orm import Session, sessionmaker


def _normalize_utc(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)


@pytest.fixture
def sqlite_session_factory(tmp_path: Path) -> sessionmaker[Session]:
    database_path = tmp_path / "background-jobs.db"
    engine = make_engine(f"sqlite+pysqlite:///{database_path}")

    with engine.begin() as connection:
        connection.exec_driver_sql("PRAGMA foreign_keys=ON")

    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


def test_postgres_claim_statement_uses_skip_locked() -> None:
    statement = str(POSTGRES_CLAIM_SQL)

    assert "FOR UPDATE SKIP LOCKED" in statement
    assert "UPDATE background_jobs" in statement


def test_background_job_service_tracks_leases_and_completion(
    sqlite_session_factory: sessionmaker[Session],
) -> None:
    with sqlite_session_factory() as session:
        service = BackgroundJobService(session)
        queued = service.enqueue_job(
            job_type="demo.echo",
            payload={"message": "hello", "steps": 2},
        )

    assert queued.status == JobStatus.QUEUED
    assert queued.attempt_count == 0
    assert queued.lease_owner is None

    with sqlite_session_factory() as session:
        service = BackgroundJobService(session)
        claimed = service.claim_next_job(
            lease_owner="worker-a",
            lease_duration=timedelta(seconds=30),
        )

    assert claimed is not None
    assert claimed.job_type == "demo.echo"
    assert claimed.attempt_count == 1
    assert claimed.lease_owner == "worker-a"

    with sqlite_session_factory() as session:
        service = BackgroundJobService(session)
        assert (
            service.claim_next_job(
                lease_owner="worker-b",
                lease_duration=timedelta(seconds=30),
            )
            is None
        )

    with sqlite_session_factory() as session:
        service = BackgroundJobService(session)
        heartbeat = service.heartbeat_job(
            claimed,
            lease_duration=timedelta(seconds=45),
        )

    assert heartbeat.status == JobStatus.IN_PROGRESS
    assert heartbeat.lease_expires_at is not None
    assert _normalize_utc(heartbeat.lease_expires_at) > _normalize_utc(claimed.lease_expires_at)

    with sqlite_session_factory() as session:
        service = BackgroundJobService(session)
        completed = service.complete_job(
            claimed,
            result_summary={"echo": "hello"},
        )

    assert completed.status == JobStatus.COMPLETED
    assert completed.result_summary == {"echo": "hello"}
    assert completed.completed_at is not None
    assert completed.lease_owner is None
    assert completed.lease_expires_at is None


def test_expired_job_can_be_reclaimed_and_stale_lease_cannot_update(
    sqlite_session_factory: sessionmaker[Session],
) -> None:
    with sqlite_session_factory() as session:
        service = BackgroundJobService(session)
        queued = service.enqueue_job(
            job_type="demo.echo",
            payload={"message": "sleepy"},
        )

    with sqlite_session_factory() as session:
        service = BackgroundJobService(session)
        original_claim = service.claim_next_job(
            lease_owner="worker-a",
            lease_duration=timedelta(seconds=30),
        )

    assert original_claim is not None

    with sqlite_session_factory() as session:
        session.execute(
            update(BackgroundJob)
            .where(BackgroundJob.id == queued.id)
            .values(
                lease_expires_at=utc_now() - timedelta(seconds=5),
                updated_at=utc_now(),
            )
        )
        session.commit()

    with sqlite_session_factory() as session:
        service = BackgroundJobService(session)
        reclaimed = service.claim_next_job(
            lease_owner="worker-b",
            lease_duration=timedelta(seconds=30),
        )

    assert reclaimed is not None
    assert reclaimed.id == queued.id
    assert reclaimed.attempt_count == 2
    assert reclaimed.lease_owner == "worker-b"
    assert reclaimed.lease_token != original_claim.lease_token

    with sqlite_session_factory() as session:
        service = BackgroundJobService(session)
        with pytest.raises(BackgroundJobLeaseLostError):
            service.complete_job(
                original_claim,
                result_summary={"echo": "stale"},
            )

    with sqlite_session_factory() as session:
        service = BackgroundJobService(session)
        failed = service.fail_job(
            reclaimed,
            error_message="simulated crash",
            result_summary={"reclaimed": True},
        )

    assert failed.status == JobStatus.FAILED
    assert failed.error_message == "simulated crash"
    assert failed.result_summary == {"reclaimed": True}
    assert failed.failed_at is not None

from __future__ import annotations

from datetime import datetime

from sqlalchemy import Select, and_, or_, select, text, update
from sqlalchemy.orm import Session

from app.db import BackgroundJob, JobStatus

POSTGRES_CLAIM_SQL = text(
    """
    WITH candidate AS (
        SELECT id
        FROM background_jobs
        WHERE (
            status = :queued_status
            OR (
                status = :in_progress_status
                AND lease_expires_at IS NOT NULL
                AND lease_expires_at < :now
            )
        )
        ORDER BY created_at ASC, id ASC
        FOR UPDATE SKIP LOCKED
        LIMIT 1
    )
    UPDATE background_jobs
    SET
        status = :in_progress_status,
        attempt_count = attempt_count + 1,
        lease_owner = :lease_owner,
        lease_token = :lease_token,
        lease_expires_at = :lease_expires_at,
        claimed_at = :now,
        heartbeat_at = :now,
        started_at = COALESCE(started_at, :now),
        completed_at = NULL,
        failed_at = NULL,
        error_message = NULL,
        updated_at = :now
    WHERE id IN (SELECT id FROM candidate)
    RETURNING id
    """
)


class BackgroundJobRepository:
    def __init__(self, session: Session):
        self._session = session

    def create(
        self,
        *,
        job_type: str,
        payload: dict | list | None,
        session_id: str | None = None,
    ) -> BackgroundJob:
        job = BackgroundJob(
            session_id=session_id,
            job_type=job_type,
            payload=payload if payload is not None else {},
        )
        self._session.add(job)
        self._session.flush()
        return job

    def get_by_id(self, job_id: str) -> BackgroundJob | None:
        stmt: Select[tuple[BackgroundJob]] = select(BackgroundJob).where(BackgroundJob.id == job_id)
        return self._session.execute(stmt).scalar_one_or_none()

    def claim_next_available(
        self,
        *,
        lease_owner: str,
        lease_token: str,
        now: datetime,
        lease_expires_at: datetime,
    ) -> BackgroundJob | None:
        dialect_name = self._session.get_bind().dialect.name

        if dialect_name == "postgresql":
            return self._claim_next_available_postgres(
                lease_owner=lease_owner,
                lease_token=lease_token,
                now=now,
                lease_expires_at=lease_expires_at,
            )

        return self._claim_next_available_generic(
            lease_owner=lease_owner,
            lease_token=lease_token,
            now=now,
            lease_expires_at=lease_expires_at,
        )

    def heartbeat(
        self,
        *,
        job_id: str,
        lease_owner: str,
        lease_token: str,
        now: datetime,
        lease_expires_at: datetime,
    ) -> BackgroundJob | None:
        return self._update_claimed_job(
            job_id=job_id,
            lease_owner=lease_owner,
            lease_token=lease_token,
            values={
                "heartbeat_at": now,
                "lease_expires_at": lease_expires_at,
                "updated_at": now,
            },
        )

    def mark_completed(
        self,
        *,
        job_id: str,
        lease_owner: str,
        lease_token: str,
        now: datetime,
        result_summary: dict | list | None,
    ) -> BackgroundJob | None:
        return self._update_claimed_job(
            job_id=job_id,
            lease_owner=lease_owner,
            lease_token=lease_token,
            values={
                "status": JobStatus.COMPLETED,
                "result_summary": result_summary,
                "completed_at": now,
                "failed_at": None,
                "heartbeat_at": now,
                "lease_owner": None,
                "lease_token": None,
                "lease_expires_at": None,
                "error_message": None,
                "updated_at": now,
            },
        )

    def mark_failed(
        self,
        *,
        job_id: str,
        lease_owner: str,
        lease_token: str,
        now: datetime,
        error_message: str,
        result_summary: dict | list | None,
    ) -> BackgroundJob | None:
        return self._update_claimed_job(
            job_id=job_id,
            lease_owner=lease_owner,
            lease_token=lease_token,
            values={
                "status": JobStatus.FAILED,
                "result_summary": result_summary,
                "failed_at": now,
                "completed_at": None,
                "heartbeat_at": now,
                "lease_owner": None,
                "lease_token": None,
                "lease_expires_at": None,
                "error_message": error_message,
                "updated_at": now,
            },
        )

    def _claim_next_available_generic(
        self,
        *,
        lease_owner: str,
        lease_token: str,
        now: datetime,
        lease_expires_at: datetime,
    ) -> BackgroundJob | None:
        stmt: Select[tuple[BackgroundJob]] = (
            select(BackgroundJob)
            .where(self._claimable_clause(now))
            .order_by(BackgroundJob.created_at.asc(), BackgroundJob.id.asc())
            .limit(1)
        )
        job = self._session.execute(stmt).scalar_one_or_none()

        if job is None:
            return None

        self._apply_claim(
            job,
            lease_owner=lease_owner,
            lease_token=lease_token,
            now=now,
            lease_expires_at=lease_expires_at,
        )
        self._session.flush()
        return job

    def _claim_next_available_postgres(
        self,
        *,
        lease_owner: str,
        lease_token: str,
        now: datetime,
        lease_expires_at: datetime,
    ) -> BackgroundJob | None:
        result = self._session.execute(
            POSTGRES_CLAIM_SQL,
            {
                "queued_status": JobStatus.QUEUED.value,
                "in_progress_status": JobStatus.IN_PROGRESS.value,
                "lease_owner": lease_owner,
                "lease_token": lease_token,
                "now": now,
                "lease_expires_at": lease_expires_at,
            },
        ).scalar_one_or_none()

        if result is None:
            return None

        return self.get_by_id(str(result))

    def _update_claimed_job(
        self,
        *,
        job_id: str,
        lease_owner: str,
        lease_token: str,
        values: dict[str, object],
    ) -> BackgroundJob | None:
        stmt = (
            update(BackgroundJob)
            .where(
                BackgroundJob.id == job_id,
                BackgroundJob.status == JobStatus.IN_PROGRESS,
                BackgroundJob.lease_owner == lease_owner,
                BackgroundJob.lease_token == lease_token,
            )
            .values(**values)
        )
        result = self._session.execute(stmt)

        if result.rowcount != 1:
            return None

        self._session.flush()
        return self.get_by_id(job_id)

    @staticmethod
    def _apply_claim(
        job: BackgroundJob,
        *,
        lease_owner: str,
        lease_token: str,
        now: datetime,
        lease_expires_at: datetime,
    ) -> None:
        job.status = JobStatus.IN_PROGRESS
        job.attempt_count += 1
        job.lease_owner = lease_owner
        job.lease_token = lease_token
        job.lease_expires_at = lease_expires_at
        job.claimed_at = now
        job.heartbeat_at = now
        job.started_at = job.started_at or now
        job.completed_at = None
        job.failed_at = None
        job.error_message = None
        job.updated_at = now

    @staticmethod
    def _claimable_clause(now: datetime):
        return or_(
            BackgroundJob.status == JobStatus.QUEUED,
            and_(
                BackgroundJob.status == JobStatus.IN_PROGRESS,
                BackgroundJob.lease_expires_at.is_not(None),
                BackgroundJob.lease_expires_at < now,
            ),
        )

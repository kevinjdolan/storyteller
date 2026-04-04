from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any
from uuid import uuid4

from sqlalchemy.orm import Session

from app.db import BackgroundJob, JobStatus, utc_now
from app.repositories import BackgroundJobRepository

JobPayload = dict[str, Any] | list[Any] | None


class BackgroundJobServiceError(Exception):
    """Base error for durable background job failures."""


class BackgroundJobNotFoundError(BackgroundJobServiceError):
    """Raised when a requested job row does not exist."""


class BackgroundJobLeaseLostError(BackgroundJobServiceError):
    """Raised when a worker tries to update a job after losing its lease."""


@dataclass(frozen=True)
class BackgroundJobRecord:
    id: str
    session_id: str | None
    job_type: str
    status: JobStatus
    payload: JobPayload
    result_summary: JobPayload
    attempt_count: int
    lease_owner: str | None
    lease_expires_at: datetime | None
    claimed_at: datetime | None
    heartbeat_at: datetime | None
    started_at: datetime | None
    completed_at: datetime | None
    failed_at: datetime | None
    error_message: str | None
    created_at: datetime
    updated_at: datetime


@dataclass(frozen=True)
class ClaimedBackgroundJob:
    id: str
    session_id: str | None
    job_type: str
    payload: JobPayload
    attempt_count: int
    lease_owner: str
    lease_token: str
    lease_expires_at: datetime
    heartbeat_at: datetime


class BackgroundJobService:
    def __init__(self, session: Session):
        self._session = session
        self._jobs = BackgroundJobRepository(session)

    def enqueue_job(
        self,
        *,
        job_type: str,
        payload: JobPayload = None,
        session_id: str | None = None,
    ) -> BackgroundJobRecord:
        normalized_type = job_type.strip()
        if not normalized_type:
            raise ValueError("job_type must not be empty")

        job = self._jobs.create(
            session_id=session_id,
            job_type=normalized_type,
            payload=payload,
        )
        self._session.commit()
        return _to_job_record(job)

    def get_job(self, job_id: str) -> BackgroundJobRecord:
        job = self._jobs.get_by_id(job_id)
        if job is None:
            raise BackgroundJobNotFoundError(f"background job {job_id!r} was not found")

        return _to_job_record(job)

    def claim_next_job(
        self,
        *,
        lease_owner: str,
        lease_duration: timedelta,
    ) -> ClaimedBackgroundJob | None:
        normalized_owner = lease_owner.strip()
        if not normalized_owner:
            raise ValueError("lease_owner must not be empty")
        if lease_duration <= timedelta(0):
            raise ValueError("lease_duration must be greater than zero")

        now = utc_now()
        job = self._jobs.claim_next_available(
            lease_owner=normalized_owner,
            lease_token=str(uuid4()),
            now=now,
            lease_expires_at=now + lease_duration,
        )

        if job is None:
            self._session.rollback()
            return None

        self._session.commit()
        return _to_claimed_job(job)

    def heartbeat_job(
        self,
        claim: ClaimedBackgroundJob,
        *,
        lease_duration: timedelta,
    ) -> BackgroundJobRecord:
        if lease_duration <= timedelta(0):
            raise ValueError("lease_duration must be greater than zero")

        now = utc_now()
        job = self._jobs.heartbeat(
            job_id=claim.id,
            lease_owner=claim.lease_owner,
            lease_token=claim.lease_token,
            now=now,
            lease_expires_at=now + lease_duration,
        )

        if job is None:
            self._session.rollback()
            raise BackgroundJobLeaseLostError(
                f"background job {claim.id!r} no longer holds lease {claim.lease_token!r}",
            )

        self._session.commit()
        return _to_job_record(job)

    def complete_job(
        self,
        claim: ClaimedBackgroundJob,
        *,
        result_summary: JobPayload = None,
    ) -> BackgroundJobRecord:
        now = utc_now()
        job = self._jobs.mark_completed(
            job_id=claim.id,
            lease_owner=claim.lease_owner,
            lease_token=claim.lease_token,
            now=now,
            result_summary=result_summary,
        )

        if job is None:
            self._session.rollback()
            raise BackgroundJobLeaseLostError(
                f"background job {claim.id!r} no longer holds lease {claim.lease_token!r}",
            )

        self._session.commit()
        return _to_job_record(job)

    def fail_job(
        self,
        claim: ClaimedBackgroundJob,
        *,
        error_message: str,
        result_summary: JobPayload = None,
    ) -> BackgroundJobRecord:
        normalized_error = error_message.strip()
        if not normalized_error:
            raise ValueError("error_message must not be empty")

        now = utc_now()
        job = self._jobs.mark_failed(
            job_id=claim.id,
            lease_owner=claim.lease_owner,
            lease_token=claim.lease_token,
            now=now,
            error_message=normalized_error,
            result_summary=result_summary,
        )

        if job is None:
            self._session.rollback()
            raise BackgroundJobLeaseLostError(
                f"background job {claim.id!r} no longer holds lease {claim.lease_token!r}",
            )

        self._session.commit()
        return _to_job_record(job)


def _to_job_record(job: BackgroundJob) -> BackgroundJobRecord:
    return BackgroundJobRecord(
        id=job.id,
        session_id=job.session_id,
        job_type=job.job_type,
        status=job.status,
        payload=job.payload,
        result_summary=job.result_summary,
        attempt_count=job.attempt_count,
        lease_owner=job.lease_owner,
        lease_expires_at=job.lease_expires_at,
        claimed_at=job.claimed_at,
        heartbeat_at=job.heartbeat_at,
        started_at=job.started_at,
        completed_at=job.completed_at,
        failed_at=job.failed_at,
        error_message=job.error_message,
        created_at=job.created_at,
        updated_at=job.updated_at,
    )


def _to_claimed_job(job: BackgroundJob) -> ClaimedBackgroundJob:
    if (
        job.lease_owner is None
        or job.lease_token is None
        or job.lease_expires_at is None
        or job.heartbeat_at is None
    ):
        raise RuntimeError(f"background job {job.id!r} was claimed without a durable lease")

    return ClaimedBackgroundJob(
        id=job.id,
        session_id=job.session_id,
        job_type=job.job_type,
        payload=job.payload,
        attempt_count=job.attempt_count,
        lease_owner=job.lease_owner,
        lease_token=job.lease_token,
        lease_expires_at=job.lease_expires_at,
        heartbeat_at=job.heartbeat_at,
    )

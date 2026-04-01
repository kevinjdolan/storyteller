from __future__ import annotations

import logging
import time
from dataclasses import dataclass
from datetime import timedelta
from typing import Callable

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, sessionmaker

from app.services import (
    BackgroundJobLeaseLostError,
    BackgroundJobRecord,
    BackgroundJobService,
    ClaimedBackgroundJob,
)
from app.worker.registry import JobHandlerRegistry

logger = logging.getLogger(__name__)


@dataclass
class JobExecutionContext:
    claim: ClaimedBackgroundJob
    worker_id: str
    _heartbeat_callback: Callable[[], BackgroundJobRecord]

    @property
    def job_id(self) -> str:
        return self.claim.id

    @property
    def job_type(self) -> str:
        return self.claim.job_type

    @property
    def session_id(self) -> str | None:
        return self.claim.session_id

    @property
    def attempt_count(self) -> int:
        return self.claim.attempt_count

    def heartbeat(self) -> BackgroundJobRecord:
        return self._heartbeat_callback()


class JobWorker:
    def __init__(
        self,
        *,
        session_factory: sessionmaker[Session],
        registry: JobHandlerRegistry,
        worker_id: str,
        lease_duration: timedelta,
        poll_interval_seconds: float,
    ) -> None:
        self._session_factory = session_factory
        self._registry = registry
        self._worker_id = worker_id
        self._lease_duration = lease_duration
        self._poll_interval_seconds = poll_interval_seconds

    def run_once(self) -> bool:
        claim = self._with_job_service(
            lambda service: service.claim_next_job(
                lease_owner=self._worker_id,
                lease_duration=self._lease_duration,
            )
        )
        if claim is None:
            return False

        handler = self._registry.get(claim.job_type)
        if handler is None:
            self._mark_job_failed(
                claim,
                error_message=f"No handler registered for job type {claim.job_type!r}.",
            )
            return True

        logger.info(
            "Worker %s claimed job %s (%s) attempt %s",
            self._worker_id,
            claim.id,
            claim.job_type,
            claim.attempt_count,
        )

        context = JobExecutionContext(
            claim=claim,
            worker_id=self._worker_id,
            _heartbeat_callback=lambda: self._with_job_service(
                lambda service: service.heartbeat_job(
                    claim,
                    lease_duration=self._lease_duration,
                )
            ),
        )

        try:
            result_summary = handler(claim.payload, context)
        except BackgroundJobLeaseLostError:
            logger.warning(
                "Worker %s lost its lease while running job %s",
                self._worker_id,
                claim.id,
            )
            return True
        except Exception as exc:  # pragma: no cover - exercised in tests via failure record
            logger.exception(
                "Worker %s failed job %s (%s)",
                self._worker_id,
                claim.id,
                claim.job_type,
            )
            self._mark_job_failed(
                claim,
                error_message=_format_exception_message(exc),
                result_summary={
                    "exception_type": exc.__class__.__name__,
                    "worker_id": self._worker_id,
                },
            )
            return True

        try:
            completed = self._with_job_service(
                lambda service: service.complete_job(
                    claim,
                    result_summary=result_summary,
                )
            )
        except BackgroundJobLeaseLostError:
            logger.warning(
                "Worker %s lost its lease before completing job %s",
                self._worker_id,
                claim.id,
            )
            return True

        logger.info(
            "Worker %s completed job %s with status %s",
            self._worker_id,
            completed.id,
            completed.status.value,
        )
        return True

    def run_forever(self) -> None:
        logger.info(
            "Worker %s listening for jobs. Registered handlers: %s",
            self._worker_id,
            ", ".join(self._registry.registered_job_types()) or "none",
        )
        while True:
            try:
                processed = self.run_once()
            except SQLAlchemyError:
                logger.exception(
                    "Worker %s could not poll the durable queue. "
                    "Check database connectivity and migrations.",
                    self._worker_id,
                )
                time.sleep(self._poll_interval_seconds)
                continue
            if processed:
                continue
            time.sleep(self._poll_interval_seconds)

    def _mark_job_failed(
        self,
        claim: ClaimedBackgroundJob,
        *,
        error_message: str,
        result_summary: dict | list | None = None,
    ) -> None:
        try:
            failed = self._with_job_service(
                lambda service: service.fail_job(
                    claim,
                    error_message=error_message,
                    result_summary=result_summary,
                )
            )
        except BackgroundJobLeaseLostError:
            logger.warning(
                "Worker %s lost its lease before failing job %s",
                self._worker_id,
                claim.id,
            )
            return

        logger.info(
            "Worker %s marked job %s as %s",
            self._worker_id,
            failed.id,
            failed.status.value,
        )

    def _with_job_service(self, operation: Callable[[BackgroundJobService], object]) -> object:
        session = self._session_factory()

        try:
            return operation(BackgroundJobService(session))
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()


def _format_exception_message(exc: Exception) -> str:
    message = str(exc).strip()
    return message or exc.__class__.__name__

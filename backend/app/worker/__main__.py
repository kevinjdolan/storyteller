from __future__ import annotations

import argparse
import socket
from datetime import timedelta

from app.db import get_session_factory
from app.main import configure_logging
from app.services import GeminiCompositionSegmentWriter
from app.settings import SettingsValidationError, get_settings
from app.storage import build_object_storage_service
from app.worker.default_handlers import build_default_job_handler_registry
from app.worker.runtime import JobWorker


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the Storyteller background worker.")
    parser.add_argument(
        "--once",
        action="store_true",
        help="Claim at most one available job, then exit.",
    )
    parser.add_argument(
        "--worker-id",
        help="Stable worker identity used for durable job leases.",
    )
    parser.add_argument(
        "--lease-duration-seconds",
        type=float,
        default=60.0,
        help="Seconds before an in-progress lease expires without a heartbeat.",
    )
    parser.add_argument(
        "--poll-interval-seconds",
        type=float,
        default=2.0,
        help="Seconds to wait between empty queue polls in long-running mode.",
    )
    return parser.parse_args()


def main() -> None:
    try:
        settings = get_settings()
    except SettingsValidationError as exc:
        raise SystemExit(exc.format_for_cli()) from None

    args = parse_args()
    configure_logging(settings)
    object_storage = build_object_storage_service(settings)

    try:
        worker = JobWorker(
            session_factory=get_session_factory(),
            registry=build_default_job_handler_registry(
                composition_chunk_delay_seconds=0.12,
                composition_writer=GeminiCompositionSegmentWriter.from_settings(),
                object_storage=object_storage,
            ),
            worker_id=args.worker_id or f"worker-{socket.gethostname()}",
            lease_duration=timedelta(seconds=args.lease_duration_seconds),
            poll_interval_seconds=args.poll_interval_seconds,
        )

        if args.once:
            worker.run_once()
            return

        worker.run_forever()
    finally:
        object_storage.close()


if __name__ == "__main__":
    main()

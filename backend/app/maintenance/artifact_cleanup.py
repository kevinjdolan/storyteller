from __future__ import annotations

import argparse

from app.db import get_session_factory
from app.main import configure_logging
from app.services.artifact_retention import ArtifactRetentionService
from app.settings import SettingsValidationError, get_settings
from app.storage import build_object_storage_service


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Inspect or clean expired temporary Storyteller artifacts while preserving "
            "current canonical outputs."
        ),
    )
    parser.add_argument(
        "--session-id",
        help="Limit cleanup planning to a single session id.",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Delete eligible storage objects and mark their asset rows as cleaned.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        help="Maximum number of cleanup candidates to inspect or apply.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        settings = get_settings()
    except SettingsValidationError as exc:
        raise SystemExit(exc.format_for_cli()) from None

    configure_logging(settings)
    session_factory = get_session_factory()
    object_storage = build_object_storage_service(settings)

    try:
        with session_factory() as session:
            report = ArtifactRetentionService(
                session,
                object_storage=object_storage,
            ).cleanup_expired_assets(
                session_id=args.session_id,
                dry_run=not args.apply,
                limit=args.limit,
            )
    finally:
        object_storage.close()

    mode = "apply" if args.apply else "dry-run"
    print(
        f"Artifact cleanup {mode}: {report.candidate_count} candidates, "
        f"{report.protected_asset_count} protected assets, "
        f"{report.cleaned_asset_count} asset rows updated, "
        f"{report.deleted_object_count} objects deleted, "
        f"{report.missing_object_count} objects already missing.",
    )

    if not report.candidates:
        return 0

    for candidate in report.candidates:
        target_summary = ", ".join(
            f"{target.role}={target.location.uri}" for target in candidate.targets
        )
        print(
            f"- session={candidate.session_id} asset={candidate.asset_id} "
            f"kind={candidate.asset_kind.value} status={candidate.status.value} "
            f"rule={candidate.rule_key} expires_at={candidate.expires_at.isoformat()} "
            f"targets=[{target_summary}] reason={candidate.reason}"
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

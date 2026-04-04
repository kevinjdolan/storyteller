from __future__ import annotations

import argparse
from pathlib import Path

from app.db import get_session_factory
from app.services.catalog import CATALOG_FILE_PATH, load_catalog_document, seed_catalog
from app.settings import SettingsValidationError, get_settings


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Seed the Storyteller genre and tone catalog into the database.",
    )
    parser.add_argument(
        "--catalog",
        type=Path,
        default=CATALOG_FILE_PATH,
        help="Path to the YAML catalog definition.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Load and validate the catalog, then flush without committing.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        get_settings()
    except SettingsValidationError as exc:
        raise SystemExit(exc.format_for_cli()) from None

    catalog = load_catalog_document(args.catalog)
    session_factory = get_session_factory()

    with session_factory() as session:
        stats = seed_catalog(session, catalog, commit=not args.dry_run)
        if args.dry_run:
            session.rollback()

    genre_summary = (
        f"genres: {stats.created_genres} created, "
        f"{stats.updated_genres} updated, "
        f"{stats.deactivated_genres} deactivated"
    )
    tone_summary = (
        f"tones: {stats.created_tones} created, "
        f"{stats.updated_tones} updated, "
        f"{stats.deactivated_tones} deactivated"
    )
    print(
        f"Seeded catalog from {args.catalog} ({genre_summary}; {tone_summary})"
        f"{' [dry-run]' if args.dry_run else ''}",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

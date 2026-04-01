from __future__ import annotations

import argparse
import json
from uuid import uuid4

from app.settings import SettingsValidationError, get_settings
from app.storage import build_object_storage_service


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Write and read a sample object through the configured storage backend.",
    )
    parser.add_argument(
        "--session-id",
        default="storage-smoke",
        help="Session identifier used to derive the debug-artifact prefix.",
    )
    parser.add_argument(
        "--artifact-group",
        default="smoke-tests",
        help="Debug-artifact group prefix used for the sample object.",
    )
    parser.add_argument(
        "--artifact-name",
        default=None,
        help="Optional object name; defaults to a generated UUID.",
    )
    parser.add_argument(
        "--payload",
        default="Storyteller storage smoke test payload.",
        help="Text payload to upload and read back.",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    try:
        settings = get_settings()
    except SettingsValidationError as exc:
        raise SystemExit(exc.format_for_cli()) from None

    object_storage = build_object_storage_service(settings)
    artifact_name = args.artifact_name or uuid4().hex

    try:
        object_storage.ensure_runtime_buckets()
        location = object_storage.paths.debug_artifact(
            session_id=args.session_id,
            artifact_group=args.artifact_group,
            artifact_name=artifact_name,
            extension="txt",
        )

        upload_metadata = object_storage.upload_text(location, args.payload)
        fetched_metadata = object_storage.fetch_object_metadata(location)
        downloaded_payload = object_storage.download_text(location)

        if downloaded_payload != args.payload:
            raise SystemExit("Storage smoke test failed: downloaded payload did not match upload.")

        print(
            json.dumps(
                {
                    "status": "ok",
                    "location": {
                        "bucket": location.bucket,
                        "key": location.key,
                        "uri": location.uri,
                    },
                    "upload": {
                        "size_bytes": upload_metadata.size_bytes,
                        "content_type": upload_metadata.content_type,
                    },
                    "metadata": {
                        "size_bytes": fetched_metadata.size_bytes,
                        "content_type": fetched_metadata.content_type,
                        "etag": fetched_metadata.etag,
                        "generation": fetched_metadata.generation,
                    },
                },
                indent=2,
            ),
        )
    finally:
        object_storage.close()


if __name__ == "__main__":
    main()

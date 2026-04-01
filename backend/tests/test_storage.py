from __future__ import annotations

import json
from urllib.parse import unquote

import httpx
import pytest

from app.settings import load_settings
from app.storage import (
    ObjectNotFoundError,
    SessionArtifactStoragePaths,
    build_object_storage_service,
)


def build_test_settings():
    return load_settings(
        {
            "STORYTELLER_SECRETS_FILE": "",
            "STORYTELLER_DATABASE_URL": (
                "postgresql://storyteller:storyteller@postgres:5432/storyteller"
            ),
            "STORYTELLER_GEMINI_API_KEY": "test-gemini-key",
            "STORYTELLER_GCS_ENDPOINT": "http://gcs:4443",
            "STORYTELLER_GCS_PROJECT_ID": "storyteller-local",
            "STORYTELLER_GCS_PUBLIC_URL": "http://localhost:8568",
            "STORYTELLER_GCS_SESSIONS_BUCKET_NAME": "storyteller-sessions",
            "STORYTELLER_GCS_AUDIO_BUCKET_NAME": "storyteller-audio",
            "STORYTELLER_GCS_EXPORTS_BUCKET_NAME": "storyteller-exports",
        },
    )


class FakeGCSJsonAPI:
    def __init__(self) -> None:
        self.buckets: set[str] = set()
        self.objects: dict[tuple[str, str], dict[str, object]] = {}

    def handle(self, request: httpx.Request) -> httpx.Response:
        path = request.url.raw_path.decode().split("?", 1)[0]

        if request.method == "POST" and path == "/storage/v1/b":
            payload = json.loads(request.content.decode("utf-8"))
            bucket_name = str(payload["name"])

            if bucket_name in self.buckets:
                return httpx.Response(
                    status_code=409,
                    json={"error": {"message": f"bucket {bucket_name} already exists"}},
                )

            self.buckets.add(bucket_name)
            return httpx.Response(status_code=200, json={"name": bucket_name})

        upload_prefix = "/upload/storage/v1/b/"
        if request.method == "POST" and path.startswith(upload_prefix) and path.endswith("/o"):
            bucket_name = unquote(path[len(upload_prefix) : -2])
            key = request.url.params["name"]

            if bucket_name not in self.buckets:
                return httpx.Response(
                    status_code=404,
                    json={"error": {"message": f"bucket {bucket_name} not found"}},
                )

            generation = str(len(self.objects) + 1)
            metadata = {
                "bucket": bucket_name,
                "name": key,
                "size": str(len(request.content)),
                "contentType": request.headers.get("Content-Type"),
                "etag": f"etag-{generation}",
                "generation": generation,
                "md5Hash": "not-real-md5",
                "updated": "2026-03-31T12:00:00Z",
            }
            self.objects[(bucket_name, key)] = {
                "metadata": metadata,
                "content": request.content,
            }
            return httpx.Response(status_code=200, json=metadata)

        metadata_prefix = "/storage/v1/b/"
        if request.method == "GET" and path.startswith(metadata_prefix) and "/o/" in path:
            remainder = path[len(metadata_prefix) :]
            bucket_name, encoded_key = remainder.split("/o/", 1)
            object_key = unquote(encoded_key)
            stored_object = self.objects.get((unquote(bucket_name), object_key))

            if stored_object is None:
                return httpx.Response(
                    status_code=404,
                    json={"error": {"message": f"object {object_key} not found"}},
                )

            if request.url.params.get("alt") == "media":
                metadata = stored_object["metadata"]
                assert isinstance(metadata, dict)
                return httpx.Response(
                    status_code=200,
                    content=stored_object["content"],
                    headers={"Content-Type": str(metadata.get("contentType") or "")},
                )

            return httpx.Response(status_code=200, json=stored_object["metadata"])

        return httpx.Response(
            status_code=500,
            json={"error": {"message": f"Unhandled fake GCS request: {request.method} {path}"}},
        )


def test_session_artifact_paths_use_stable_session_scoped_prefixes() -> None:
    settings = build_test_settings()
    paths = SessionArtifactStoragePaths.from_settings(settings)

    assert paths.partial_draft_segment(
        session_id="session-123",
        job_id="compose-01",
        segment_index=7,
    ).uri == (
        "gs://storyteller-sessions/"
        "sessions/session-123/composition/jobs/compose-01/segments/0007.md"
    )
    assert paths.audio_segment(
        session_id="session-123",
        job_id="audio-job-02",
        segment_index=3,
    ).uri == (
        "gs://storyteller-audio/"
        "sessions/session-123/audio/jobs/audio-job-02/segments/0003.mp3"
    )
    assert paths.final_audio(
        session_id="session-123",
        job_id="audio-job-02",
        file_stem="bedtime-story",
    ).uri == (
        "gs://storyteller-audio/"
        "sessions/session-123/audio/jobs/audio-job-02/final/bedtime-story.mp3"
    )
    assert paths.export_asset(
        session_id="session-123",
        export_kind="docx",
        export_id="final-manuscript",
        extension="docx",
    ).uri == (
        "gs://storyteller-exports/"
        "sessions/session-123/exports/docx/final-manuscript.docx"
    )
    assert paths.debug_artifact(
        session_id="session-123",
        artifact_group="llm traces",
        artifact_name="draft #1",
        extension="json",
    ).uri == (
        "gs://storyteller-sessions/"
        "sessions/session-123/debug/llm-traces/draft-1.json"
    )


def test_storage_service_round_trips_objects_through_gcs_json_api() -> None:
    fake_gcs = FakeGCSJsonAPI()
    settings = build_test_settings()
    client = httpx.Client(
        base_url=settings.gcs_endpoint,
        transport=httpx.MockTransport(fake_gcs.handle),
    )
    object_storage = build_object_storage_service(settings, client=client)

    try:
        object_storage.ensure_runtime_buckets()
        location = object_storage.paths.audio_segment(
            session_id="session-abc",
            job_id="audio-job-1",
            segment_index=12,
        )

        upload_metadata = object_storage.upload_bytes(
            location,
            b"pretend-mp3-bytes",
            content_type="audio/mpeg",
        )
        fetched_metadata = object_storage.fetch_object_metadata(location)
        downloaded = object_storage.download_bytes(location)
    finally:
        object_storage.close()
        client.close()

    assert fake_gcs.buckets == {
        "storyteller-sessions",
        "storyteller-audio",
        "storyteller-exports",
    }
    assert upload_metadata.location == location
    assert upload_metadata.size_bytes == len(b"pretend-mp3-bytes")
    assert fetched_metadata.content_type == "audio/mpeg"
    assert downloaded == b"pretend-mp3-bytes"


def test_storage_service_raises_clear_error_for_missing_objects() -> None:
    fake_gcs = FakeGCSJsonAPI()
    settings = build_test_settings()
    client = httpx.Client(
        base_url=settings.gcs_endpoint,
        transport=httpx.MockTransport(fake_gcs.handle),
    )
    object_storage = build_object_storage_service(settings, client=client)

    try:
        object_storage.ensure_runtime_buckets()
        location = object_storage.paths.final_audio(
            session_id="session-abc",
            job_id="audio-job-1",
        )

        with pytest.raises(ObjectNotFoundError) as exc_info:
            object_storage.fetch_object_metadata(location)
    finally:
        object_storage.close()
        client.close()

    assert location.uri in str(exc_info.value)


from __future__ import annotations

import json
from typing import Protocol
from urllib.parse import quote

import httpx

from app.settings import AppSettings
from app.storage.models import StorageObjectLocation, StorageObjectMetadata
from app.storage.paths import SessionArtifactStoragePaths

DEFAULT_STORAGE_TIMEOUT_SECONDS = 10.0


class StorageError(RuntimeError):
    pass


class ObjectNotFoundError(StorageError):
    def __init__(self, location: StorageObjectLocation) -> None:
        super().__init__(f"storage object not found: {location.uri}")
        self.location = location


class ObjectStorageBackend(Protocol):
    def create_bucket_if_missing(self, bucket_name: str) -> None: ...

    def upload_bytes(
        self,
        location: StorageObjectLocation,
        data: bytes,
        *,
        content_type: str,
    ) -> StorageObjectMetadata: ...

    def get_object_metadata(self, location: StorageObjectLocation) -> StorageObjectMetadata: ...

    def download_bytes(self, location: StorageObjectLocation) -> bytes: ...

    def delete_object(self, location: StorageObjectLocation) -> bool: ...

    def close(self) -> None: ...


class GCSStorageBackend:
    def __init__(
        self,
        *,
        endpoint: str,
        project_id: str,
        client: httpx.Client | None = None,
    ) -> None:
        self._project_id = project_id
        self._owns_client = client is None
        self._client = client or httpx.Client(
            base_url=endpoint.rstrip("/"),
            timeout=DEFAULT_STORAGE_TIMEOUT_SECONDS,
        )

    def create_bucket_if_missing(self, bucket_name: str) -> None:
        response = self._client.post(
            "/storage/v1/b",
            params={"project": self._project_id},
            json={"name": bucket_name},
        )

        if response.status_code in {200, 201, 409}:
            return

        self._raise_storage_error("create bucket", response)

    def upload_bytes(
        self,
        location: StorageObjectLocation,
        data: bytes,
        *,
        content_type: str,
    ) -> StorageObjectMetadata:
        response = self._client.post(
            f"/upload/storage/v1/b/{quote(location.bucket, safe='')}/o",
            params={
                "uploadType": "media",
                "name": location.key,
            },
            content=data,
            headers={"Content-Type": content_type},
        )

        if response.status_code not in {200, 201}:
            self._raise_storage_error("upload object", response)

        return self._metadata_from_payload(location, response.json())

    def get_object_metadata(self, location: StorageObjectLocation) -> StorageObjectMetadata:
        response = self._client.get(self._object_metadata_path(location))

        if response.status_code == 404:
            raise ObjectNotFoundError(location)

        if response.status_code != 200:
            self._raise_storage_error("fetch object metadata", response)

        return self._metadata_from_payload(location, response.json())

    def download_bytes(self, location: StorageObjectLocation) -> bytes:
        response = self._client.get(
            self._object_metadata_path(location),
            params={"alt": "media"},
        )

        if response.status_code == 404:
            raise ObjectNotFoundError(location)

        if response.status_code != 200:
            self._raise_storage_error("download object", response)

        return response.content

    def delete_object(self, location: StorageObjectLocation) -> bool:
        response = self._client.delete(self._object_metadata_path(location))

        if response.status_code == 404:
            return False

        if response.status_code not in {200, 204}:
            self._raise_storage_error("delete object", response)

        return True

    def close(self) -> None:
        if self._owns_client:
            self._client.close()

    def _object_metadata_path(self, location: StorageObjectLocation) -> str:
        return f"/storage/v1/b/{quote(location.bucket, safe='')}/o/{quote(location.key, safe='')}"

    def _metadata_from_payload(
        self,
        location: StorageObjectLocation,
        payload: dict[str, object],
    ) -> StorageObjectMetadata:
        return StorageObjectMetadata(
            location=location,
            size_bytes=int(payload.get("size", 0)),
            content_type=_read_optional_string(payload.get("contentType")),
            etag=_read_optional_string(payload.get("etag")),
            generation=_read_optional_string(payload.get("generation")),
            md5_hash=_read_optional_string(payload.get("md5Hash")),
            updated_at=_read_optional_string(payload.get("updated")),
        )

    def _raise_storage_error(self, operation: str, response: httpx.Response) -> None:
        message = _extract_error_message(response)
        raise StorageError(
            f"{operation} failed with {response.status_code}: {message}",
        )


class ObjectStorageService:
    def __init__(
        self,
        *,
        backend: ObjectStorageBackend,
        paths: SessionArtifactStoragePaths,
    ) -> None:
        self._backend = backend
        self.paths = paths

    def ensure_bucket(self, bucket_name: str) -> None:
        self._backend.create_bucket_if_missing(bucket_name)

    def ensure_runtime_buckets(self) -> None:
        for bucket_name in dict.fromkeys(self.paths.bucket_names()):
            self.ensure_bucket(bucket_name)

    def upload_bytes(
        self,
        location: StorageObjectLocation,
        data: bytes,
        *,
        content_type: str = "application/octet-stream",
    ) -> StorageObjectMetadata:
        self.ensure_bucket(location.bucket)
        return self._backend.upload_bytes(location, data, content_type=content_type)

    def upload_text(
        self,
        location: StorageObjectLocation,
        text: str,
        *,
        content_type: str = "text/plain; charset=utf-8",
        encoding: str = "utf-8",
    ) -> StorageObjectMetadata:
        return self.upload_bytes(
            location,
            text.encode(encoding),
            content_type=content_type,
        )

    def fetch_object_metadata(self, location: StorageObjectLocation) -> StorageObjectMetadata:
        return self._backend.get_object_metadata(location)

    def download_bytes(self, location: StorageObjectLocation) -> bytes:
        return self._backend.download_bytes(location)

    def download_text(
        self,
        location: StorageObjectLocation,
        *,
        encoding: str = "utf-8",
    ) -> str:
        return self.download_bytes(location).decode(encoding)

    def delete_object(
        self,
        location: StorageObjectLocation,
        *,
        missing_ok: bool = True,
    ) -> bool:
        deleted = self._backend.delete_object(location)
        if deleted or missing_ok:
            return deleted
        raise ObjectNotFoundError(location)

    def close(self) -> None:
        self._backend.close()


def build_object_storage_service(
    settings: AppSettings,
    *,
    client: httpx.Client | None = None,
) -> ObjectStorageService:
    return ObjectStorageService(
        backend=GCSStorageBackend(
            endpoint=settings.gcs_endpoint,
            project_id=settings.gcs_project_id,
            client=client,
        ),
        paths=SessionArtifactStoragePaths.from_settings(settings),
    )


def _extract_error_message(response: httpx.Response) -> str:
    try:
        payload = response.json()
    except json.JSONDecodeError:
        return response.text.strip() or response.reason_phrase

    if isinstance(payload, dict):
        error_payload = payload.get("error")
        if isinstance(error_payload, dict):
            message = error_payload.get("message")
            if isinstance(message, str) and message.strip():
                return message.strip()

    return response.text.strip() or response.reason_phrase


def _read_optional_string(value: object) -> str | None:
    if value is None:
        return None

    normalized = str(value).strip()
    return normalized or None

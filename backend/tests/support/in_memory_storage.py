from __future__ import annotations

from app.storage import (
    ObjectNotFoundError,
    SessionArtifactStoragePaths,
    StorageObjectLocation,
    StorageObjectMetadata,
)


class InMemoryObjectStorage:
    def __init__(self, settings) -> None:
        self.paths = SessionArtifactStoragePaths.from_settings(settings)
        self._objects: dict[tuple[str, str], dict[str, object]] = {}

    def ensure_bucket(self, bucket_name: str) -> None:
        return None

    def ensure_runtime_buckets(self) -> None:
        return None

    def upload_bytes(
        self,
        location: StorageObjectLocation,
        data: bytes,
        *,
        content_type: str = "application/octet-stream",
    ) -> StorageObjectMetadata:
        self._objects[(location.bucket, location.key)] = {
            "data": bytes(data),
            "content_type": content_type,
        }
        return StorageObjectMetadata(
            location=location,
            size_bytes=len(data),
            content_type=content_type,
            etag=f"etag-{len(self._objects)}",
            generation=str(len(self._objects)),
            updated_at="2026-04-02T00:00:00Z",
        )

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
        stored = self._objects.get((location.bucket, location.key))
        if stored is None:
            raise ObjectNotFoundError(location)
        return StorageObjectMetadata(
            location=location,
            size_bytes=len(stored["data"]),
            content_type=str(stored["content_type"]),
            etag=f"etag-{location.bucket}-{location.key}",
            generation="1",
            updated_at="2026-04-02T00:00:00Z",
        )

    def download_bytes(self, location: StorageObjectLocation) -> bytes:
        stored = self._objects.get((location.bucket, location.key))
        if stored is None:
            raise ObjectNotFoundError(location)
        return bytes(stored["data"])

    def delete_object(
        self,
        location: StorageObjectLocation,
        *,
        missing_ok: bool = True,
    ) -> bool:
        removed = self._objects.pop((location.bucket, location.key), None)
        if removed is not None:
            return True
        if missing_ok:
            return False
        raise ObjectNotFoundError(location)

    def download_text(
        self,
        location: StorageObjectLocation,
        *,
        encoding: str = "utf-8",
    ) -> str:
        return self.download_bytes(location).decode(encoding)

    def close(self) -> None:
        return None

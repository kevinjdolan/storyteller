from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class StorageObjectLocation:
    bucket: str
    key: str

    def __post_init__(self) -> None:
        if not self.bucket.strip():
            raise ValueError("bucket must not be empty")

        if not self.key.strip():
            raise ValueError("key must not be empty")

    @property
    def uri(self) -> str:
        return f"gs://{self.bucket}/{self.key}"


@dataclass(frozen=True)
class StorageObjectMetadata:
    location: StorageObjectLocation
    size_bytes: int
    content_type: str | None = None
    etag: str | None = None
    generation: str | None = None
    md5_hash: str | None = None
    updated_at: str | None = None


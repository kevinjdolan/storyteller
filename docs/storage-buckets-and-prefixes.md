# Storage Buckets And Prefixes

Storyteller now treats object storage as a backend-owned service behind one abstraction in
[`backend/app/storage`](/Users/kevin/code/storyteller/backend/app/storage). Business logic should
work with typed object locations and the path strategy there instead of hand-building bucket names
or keys.

## Bucket Roles

Three runtime buckets stay configurable through settings so local development can point at the file-
backed GCS emulator while later environments can swap only the backend implementation and bucket
names:

| Logical role | Default bucket | Primary contents |
| --- | --- | --- |
| Sessions | `storyteller-sessions` | Partial composition drafts and debug artifacts |
| Audio | `storyteller-audio` | Narration segments and final assembled audio |
| Exports | `storyteller-exports` | Downloadable `.docx` and future export formats |

## Stable Prefix Strategy

Every durable object key starts with a session root:

```text
sessions/{session_id}/...
```

That keeps resumable jobs, later cleanup policies, and session-scoped browsing aligned even when
artifacts land in different buckets.

Current prefix conventions:

| Artifact type | Bucket | Key shape | Example |
| --- | --- | --- | --- |
| Rolling draft snapshot | Sessions | `sessions/{session_id}/composition/drafts/latest-stable.{ext}` | `sessions/sess-42/composition/drafts/latest-stable.md` |
| Partial draft segment | Sessions | `sessions/{session_id}/composition/jobs/{job_id}/segments/{segment_index:04d}.{ext}` | `sessions/sess-42/composition/jobs/compose-9/segments/0003.md` |
| Audio segment | Audio | `sessions/{session_id}/audio/jobs/{job_id}/segments/{segment_index:04d}.{ext}` | `sessions/sess-42/audio/jobs/audio-2/segments/0007.mp3` |
| Final audio | Audio | `sessions/{session_id}/audio/jobs/{job_id}/final/{file_stem}.{ext}` | `sessions/sess-42/audio/jobs/audio-2/final/story.mp3` |
| Export asset | Exports | `sessions/{session_id}/exports/{export_kind}/{export_id}.{ext}` | `sessions/sess-42/exports/docx/final-manuscript.docx` |
| Debug artifact | Sessions | `sessions/{session_id}/debug/{artifact_group}/{artifact_name}.{ext}` | `sessions/sess-42/debug/prompt-assembly/request.json` |

Path components are normalized to storage-safe segments by replacing whitespace and other unsafe
characters with `-`. Session IDs and job IDs should still be treated as stable application-level
identifiers; the normalization only prevents accidental malformed keys.

## Usage

Typical backend flow:

```python
from app.settings import get_settings
from app.storage import build_object_storage_service

settings = get_settings()
object_storage = build_object_storage_service(settings)

location = object_storage.paths.partial_draft_segment(
    session_id="session-123",
    job_id="compose-job-7",
    segment_index=2,
)
object_storage.upload_text(location, "Draft paragraph")
metadata = object_storage.fetch_object_metadata(location)
payload = object_storage.download_text(location)
```

The storage service creates buckets on demand before upload, so business logic does not need bucket-
bootstrap code in composition, export, or audio workflows.

Cleanup policy and the maintenance command surface for expiring temporary blobs are documented in
[docs/artifact-retention-policy.md](/Users/kevin/code/storyteller/docs/artifact-retention-policy.md).

## Local Emulator Smoke Test

The repo exposes a CLI round-trip check through:

```bash
make backend-storage-smoke
```

That command writes a sample debug artifact, reads it back, and prints the resulting bucket, key,
and metadata JSON. Override `STORYTELLER_GCS_ENDPOINT` if you want to target a different emulator
or future non-local endpoint.

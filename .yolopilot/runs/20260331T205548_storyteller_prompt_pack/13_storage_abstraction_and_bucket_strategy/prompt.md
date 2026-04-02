# 13 — Storage Abstraction and Bucket Strategy

Read `base_prompt.md` first and preserve all prior prompt work.

## Objective

Add a backend storage layer that can write and read blobs through a single abstraction while targeting the local GCS emulator in development.

## Build
- Create a storage service that knows how to create buckets if needed, upload objects, fetch object metadata, and generate predictable object paths.
- Define bucket or prefix conventions for partial drafts, audio segments, final audio, exports, and debugging artifacts.
- Wire the backend to the local emulator host from configuration instead of assuming production GCS.

## Deliverables

- Backend storage abstraction module
- Bucket/prefix naming document
- A smoke test or CLI script that writes and reads a sample object

## Acceptance checks

- Blob operations work against the local emulator without code changes in business logic.
- Object paths are stable enough to support resumable jobs and later cleanup policies.
- There is one place to swap storage backends later if needed.

## Notes

Design paths around session IDs and artifact types.

## Suggested commit label

`feat(prompt-13): storage abstraction and buckets`

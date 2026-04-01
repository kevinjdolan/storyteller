# 78 — Download Endpoints and Object Access

Read `base_prompt.md` first and preserve all prior prompt work.

## Objective

Make finished artifacts accessible to the frontend in a secure, explicit way.

## Build
- Add backend endpoints for downloading or streaming finalized story exports and audio files.
- Use the asset metadata model to validate access and map from session to artifact.
- Keep emulator-specific details hidden behind the backend so the frontend only talks to your API.

## Deliverables

- Artifact download endpoints
- Streaming support where sensible
- Frontend hooks for artifact retrieval

## Acceptance checks

- The browser can retrieve final story and audio artifacts through the app backend cleanly.
- The frontend does not need direct knowledge of storage buckets or object paths.
- Downloads work for resumed sessions too.

## Notes

Design with future auth in mind even if local mode is single-user.

## Suggested commit label

`feat(prompt-78): download endpoints and object access`

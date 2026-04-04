# 18 — Postgres-Backed Job Runner Skeleton

Read `base_prompt.md` first and preserve all prior prompt work.

## Objective

Create a worker-friendly job system that uses PostgreSQL as the durable queue so the app can run long story and audio tasks without adding another data store.

## Build
- Create a job table with type, status, lease/lock fields, attempt count, payload, result summary, and heartbeat timestamps.
- Build a small worker loop that claims jobs using a safe Postgres pattern and marks progress or failure durably.
- Add a worker service entry point that can run beside the API in Docker Compose.

## Deliverables

- Job table and service
- Worker process scaffold
- Compose service entry for the worker

## Acceptance checks

- Long-running tasks can survive browser refreshes because work is not tied to the request thread.
- The queue does not require Redis or any extra persistence system.
- The worker can be started independently from the API.

## Notes

Keep the first version simple but durable. Retries and backoff can come next.

## Suggested commit label

`feat(prompt-18): postgres job runner skeleton`

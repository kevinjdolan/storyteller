# 60 — Composition Job Orchestration

Read `base_prompt.md` first and preserve all prior prompt work.

## Objective

Turn story composition into a durable background job that can stream progress to the UI while preserving state in PostgreSQL and object storage.

## Build
- Define a composition job type, payload shape, status lifecycle, and progress semantics.
- Create API endpoints or actions for starting composition, pausing, resuming, and canceling or redirecting a composition job.
- Make sure composition jobs persist their current segment, current plan revision, and latest partial output.

## Deliverables

- Composition job backend flow
- Start/pause/resume endpoints or actions
- Durable progress model

## Acceptance checks

- Composition can run outside the request lifecycle.
- The system knows exactly what segment is being written and against which plan revision.
- Pause/resume does not rely on the browser staying open.

## Notes

Durability matters more than raw throughput in this first version.

## Suggested commit label

`feat(prompt-60): composition job orchestration`

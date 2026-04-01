# 96 — Development and Production Compose Shapes

Read `base_prompt.md` first and preserve all prior prompt work.

## Objective

Refine containerization so local development remains smooth and future deployment paths are not an afterthought.

## Build
- Review the Dockerfiles and compose setup for the frontend, API, worker, Postgres, and GCS emulator.
- Split or document dev versus production concerns such as live reload, bind mounts, and image build targets.
- Make persistence behavior for Postgres and object storage explicit in the docs.

## Deliverables

- Improved Dockerfiles and compose organization
- Docs for dev versus prod assumptions
- Persistence notes for local volumes

## Acceptance checks

- Local development remains easy while images still make architectural sense.
- Persistence behavior is explicit and unsurprising.
- There is a path from local compose to real deployment.

## Notes

Do not over-engineer deployment, but leave a credible path.

## Suggested commit label

`feat(prompt-96): compose dev and prod shapes`

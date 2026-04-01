# 01 — Monorepo Skeleton and Folder Layout

Read `base_prompt.md` first and preserve all prior prompt work.

## Objective

Create a clean repository layout that can hold the web app, API, worker logic, infrastructure files, and documentation without mixing concerns.

## Build
- Create top-level folders for the frontend, backend, infrastructure, docs, scripts, and test assets.
- Choose a simple naming convention that keeps the repo approachable, for example `frontend/`, `backend/`, `infra/`, and `docs/`.
- Add placeholder READMEs in major folders so the purpose of each directory is obvious.

## Deliverables

- Repository folder structure committed
- Per-folder README placeholders
- A brief tree snapshot added to the root README

## Acceptance checks

- The web app and API live in clearly separated directories.
- There is an obvious home for Docker Compose, database migrations, and persistent data notes.
- The structure leaves room for a backend worker process even if it is not implemented yet.

## Notes

Keep the layout conventional. Avoid clever nesting that makes the repo harder to navigate.

## Suggested commit label

`feat(prompt-01): monorepo skeleton`

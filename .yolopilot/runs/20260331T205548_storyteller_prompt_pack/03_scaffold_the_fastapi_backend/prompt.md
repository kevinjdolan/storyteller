# 03 — Scaffold the FastAPI Backend

Read `base_prompt.md` first and preserve all prior prompt work.

## Objective

Initialize the backend as a FastAPI service with clear application startup, health routes, configuration loading, and room for future modules.

## Build
- Create the FastAPI app package, a health endpoint, and a versioned API router structure.
- Add a backend dependency file or `pyproject.toml` and a local run command.
- Split the code into sensible modules such as settings, api routes, db, services, and domain models.

## Deliverables

- `backend/` FastAPI project
- A `/health` endpoint
- Basic backend run instructions in the backend README

## Acceptance checks

- The API can start locally and return a successful health response.
- The code layout makes it obvious where future domain services should go.
- The scaffold does not hide everything in one giant file.

## Notes

Prefer boring, maintainable FastAPI structure over magic.

## Suggested commit label

`feat(prompt-03): fastapi scaffold`

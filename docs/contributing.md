# Contributing

Keep changes boring, typed, and easy to review. This repo is split between a React + TypeScript frontend and a FastAPI backend, so use the stack-specific tooling below instead of personal preferences.

## Quality Commands

- `make format`: run the formatter for both stacks
- `make format-check`: verify formatting without changing files
- `make lint`: run frontend ESLint and backend Ruff checks
- `make test`: run backend pytest and frontend Vitest
- `make check`: run formatting checks, lint, tests, and the frontend production build
- `make ci`: run the same full validation path that GitHub Actions uses, including backend integration tests

If you are only touching one stack, the narrower targets are:

- `make frontend-format`, `make frontend-format-check`, `make frontend-lint`, `make frontend-test`, `make frontend-build`
- `make backend-format`, `make backend-format-check`, `make backend-lint`, `make backend-test`
- `make backend-integration-test` for the real Postgres + fake GCS durability suite

## Required CI Checks

The repository GitHub Actions workflow is defined in
[`/.github/workflows/ci.yml`](/Users/kevin/code/storyteller/.github/workflows/ci.yml).

Configure these checks from the `CI` workflow as required before merge:

- `Frontend Validation`
- `Backend Validation`
- `Backend Integration`

More detail, including local reproduction and troubleshooting notes, lives in
[docs/ci.md](/Users/kevin/code/storyteller/docs/ci.md).

## Naming Conventions

- Use `PascalCase` for React components and exported TypeScript types.
- Use `camelCase` for TypeScript variables, functions, hooks, and props.
- Use `snake_case` for Python modules, functions, variables, and pytest tests.
- Prefer names that describe product concepts directly: `session`, `pitch`, `beat_sheet`, `audio_job`.

## API Shape Conventions

- Keep FastAPI route handlers thin. Parse input, call a backend-owned service, and return typed response models.
- Put durable workflow logic in backend services or repositories, not in route modules or frontend components.
- Version externally consumed HTTP APIs under `/api/v1` unless a compatibility endpoint is explicitly temporary.
- Treat the backend as the source of truth for workflow stage, job progress, and AI side effects. The browser reflects state; it does not own it.

## Error Handling

- Raise readable, domain-specific backend errors as soon as invalid state is detected; translate them once at the API boundary.
- Return structured error payloads from HTTP endpoints instead of ad hoc strings when the frontend needs to branch on the failure.
- Keep logs actionable and free of secrets. Do not log API keys, raw secrets files, or provider credentials.
- In the frontend, prefer explicit empty, loading, and error states over silent failure.

## Generated vs. Hand-Written Assets

- Keep hand-written source in `frontend/src/`, `backend/app/`, `backend/tests/`, `docs/`, and `scripts/`.
- Treat generated output as disposable. Build artifacts belong in ignored directories such as `frontend/dist/`, coverage caches, or future runtime storage paths under `infra/persistence/`.
- Do not mix generated files into source directories. If a workflow needs checked-in fixtures, place stable fixtures under `test-assets/` and document why they are committed.
- Keep AI-produced runtime assets, exported documents, and generated audio in backend-managed storage locations instead of checking them into git.

## Integration Test Expectations

- Keep fast backend unit coverage under `make backend-test`; do not make that target depend on local infrastructure.
- Put durable-state tests that require Compose-backed Postgres or fake GCS under `backend/tests/integration/` and mark them with `pytest.mark.integration`.
- Reuse `make backend-integration-test` for local validation and future CI jobs so migrations, storage, and queue semantics are exercised the same way everywhere.

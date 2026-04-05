# Continuous Integration

Storyteller now ships a first-pass GitHub Actions workflow in
[`/.github/workflows/ci.yml`](/Users/kevin/code/storyteller/.github/workflows/ci.yml). It keeps the
signal focused on regressions that should block merges: formatting drift, lint failures, broken
unit tests, migration or data-layer regressions, and frontend build breakage.

## Workflow shape

The `CI` workflow runs three independently reported jobs:

- `Frontend Validation`: `make frontend-format-check`, `make frontend-lint`, `make frontend-test`,
  and `make frontend-build`
- `Backend Validation`: `make backend-format-check`, `make backend-lint`, and
  `make backend-test`
- `Backend Integration`: `make backend-integration-test`

The integration job starts the same Compose-backed `postgres` and `gcs` services used in local
development, waits for their healthchecks to pass, then runs the durable data-layer suite. When the
integration job fails, the workflow prints the Postgres and fake GCS logs before tearing the stack
down so the failure is easier to diagnose.

## Required checks

For branch protection, mark these checks from the `CI` workflow as required:

- `Frontend Validation`
- `Backend Validation`
- `Backend Integration`

If you want one local command that mirrors the full gate, run:

```bash
make ci
```

That target runs the existing fast checks plus the backend integration suite in one repeatable path.

## Troubleshooting

- Frontend dependency failures usually mean `frontend/package-lock.json` is out of sync with
  `frontend/package.json`. Re-run `npm install` in `frontend/` and commit the lockfile update.
- Backend dependency failures usually mean `backend/requirements.txt` was not updated alongside a
  new import. Install the missing package locally, pin it in `backend/requirements.txt`, and rerun
  `make backend-test`.
- Backend integration failures often come from migrations or local service startup. Reproduce with
  `make backend-integration-test`; if startup looks suspect, inspect `./scripts/dev-compose.sh logs
  postgres gcs`.
- Frontend build failures are usually TypeScript or Vite regressions that unit tests did not cover.
  Reproduce with `make frontend-build` to get the same production build output that CI sees.

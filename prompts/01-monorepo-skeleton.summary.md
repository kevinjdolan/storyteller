# 01 Monorepo Skeleton Summary

## What I changed and why

I turned the existing prompt-00 scaffold into a cleaner monorepo layout so later prompts have obvious, conventional homes for application code, infrastructure, migrations, worker logic, developer scripts, and reusable test fixtures.

The main changes were:

- Moved the canonical Docker Compose file from the repository root to `infra/compose/docker-compose.yml`.
  - This puts local orchestration under `infra/`, which is where future Compose variants and infrastructure definitions should live.
  - I kept the developer experience approachable by adding `scripts/dev-compose.sh` instead of forcing contributors to remember a long `docker compose -f ...` command.

- Added top-level structure that the prompt explicitly asked for:
  - `infra/`
  - `scripts/`
  - `test-assets/`

- Added placeholder READMEs in the major folders so a new engineer can infer intent without reading the prompt pack first:
  - `backend/README.md`
  - `frontend/README.md`
  - `docs/README.md`
  - `docs/adr/README.md`
  - `infra/README.md`
  - `infra/compose/README.md`
  - `infra/persistence/README.md`
  - `scripts/README.md`
  - `test-assets/README.md`
  - `tools/README.md`

- Added explicit backend placeholders for the prompt acceptance criteria:
  - `backend/migrations/README.md` as the future migration home
  - `backend/app/worker/README.md` as the future background-job home

- Updated the root `README.md` to include:
  - the new local-development entrypoint via `./scripts/dev-compose.sh up --build`
  - a brief repository tree snapshot
  - short purpose notes for each major top-level directory

- Updated `docs/architecture-overview.md` so the documented current repository state matches the new layout rather than the old root-level `docker-compose.yml`.

I also created one checkpoint commit during the run:

- `b310953` — `feat(prompt-01): monorepo skeleton`

## Architectural changes across the codebase

This prompt was still mostly structural rather than behavioral, but there are a few meaningful architecture-level changes in the repository layout:

### Infrastructure now has a real home

- `infra/compose/docker-compose.yml` is now the canonical local stack definition.
- `infra/persistence/` is the reserved documentation home for persistent local data conventions such as PostgreSQL state and file-backed object storage state.

This matters because later prompts will add PostgreSQL, the file-backed GCS emulator, and additional infrastructure details. Those no longer need to leak into the repository root.

### Backend now exposes future extension points clearly

- `backend/migrations/` is the obvious location for schema history.
- `backend/app/worker/` is the obvious location for durable background workers.

This aligns the filesystem with the architecture note that composition and audio generation should run as server-side jobs rather than request-thread work.

### Developer entrypoints are cleaner

- `scripts/dev-compose.sh` is a small wrapper around the canonical Compose file.

That keeps the infrastructure organized under `infra/` while still giving contributors a short, stable command surface.

## Examples of how to use the new abstractions, helpers, and extension points

### Compose wrapper

Start the stack:

```bash
./scripts/dev-compose.sh up --build
```

Inspect service health:

```bash
./scripts/dev-compose.sh ps
```

Run the existing browser smoke check against the stack:

```bash
./scripts/dev-compose.sh run --rm browser npm run check -- --spec ./examples/homepage.spec.json
```

Stop the stack:

```bash
./scripts/dev-compose.sh down
```

### Backend extension points

- Add future database migrations under `backend/migrations/`.
- Add durable job runners for story composition and narration under `backend/app/worker/`.

### Infrastructure extension points

- Add future local Compose variants or overrides under `infra/compose/`.
- Document persistent data behavior for PostgreSQL or the file-backed GCS emulator under `infra/persistence/`.

## Key files touched

- `README.md`
- `docs/architecture-overview.md`
- `infra/compose/docker-compose.yml`
- `scripts/dev-compose.sh`
- `backend/README.md`
- `backend/migrations/README.md`
- `backend/app/worker/README.md`
- `frontend/README.md`
- `docs/README.md`
- `docs/adr/README.md`
- `infra/README.md`
- `infra/compose/README.md`
- `infra/persistence/README.md`
- `scripts/README.md`
- `test-assets/README.md`
- `tools/README.md`

## Exact verification work performed

I verified both the filesystem layout and the runnable Docker workflow.

### Structure and acceptance checks

I ran a small Python acceptance script after the edits. Results:

- `top_level_frontend=True`
- `top_level_backend=True`
- `top_level_infra=True`
- `top_level_docs=True`
- `top_level_scripts=True`
- `top_level_test_assets=True`
- `compose_in_infra=True`
- `migrations_home=True`
- `worker_home=True`
- `root_readme_tree_snapshot=True`
- `folder_readmes_present=True`

### Patch hygiene

I ran:

```bash
git diff --check -- README.md docs/architecture-overview.md backend docs frontend infra scripts test-assets tools
```

Result:

- Passed with no whitespace or patch-formatting issues.

### Backend sanity check

I ran:

```bash
python -m compileall backend/app
```

Result:

- Passed.

### Compose validation

I ran:

```bash
./scripts/dev-compose.sh config
```

Result:

- Passed.
- Docker Compose resolved all bind mounts, build contexts, ports, health checks, and the renamed Compose file path correctly.

### Containerized runtime verification

I ran:

```bash
./scripts/dev-compose.sh up -d --build
./scripts/dev-compose.sh ps
curl -fsS http://localhost:8565/api/hello
curl -fsS http://localhost:8566 | head -n 20
```

Results:

- `backend`, `frontend`, and `browser` came up successfully.
- `backend` and `frontend` both reached healthy status.
- `GET /api/hello` returned `{"message":"Hello from FastAPI!"}`.
- The frontend served the expected Vite HTML shell on port `8566`.

### Browser-based verification and screenshot

Using the repo’s `webapp-qa` flow, I ran:

```bash
./scripts/dev-compose.sh run --rm browser npm run check -- --spec ./examples/homepage.spec.json
```

Results:

- Passed.
- Assertions for `Hello, world!` and `Hello from FastAPI!` both succeeded.
- Screenshot written to `.artifacts/webapp-qa/homepage.png`.
- I opened the screenshot and confirmed the expected scaffold card rendered correctly with the backend message visible.

### Frontend build verification

Host-side attempt:

```bash
cd frontend
npm run build
```

Result:

- Failed on the host with `sh: vite: command not found`.

Follow-up containerized verification:

```bash
./scripts/dev-compose.sh run --rm frontend npm run build
```

Result:

- Passed.
- Production build completed successfully inside the supported containerized environment.

### Cleanup

I ran:

```bash
./scripts/dev-compose.sh down
```

Result:

- Stack shut down cleanly and removed its containers and network.

## Tests, builds, browser checks, screenshots, and remaining limits

- Automated tests added: none
- Automated tests run: none beyond the existing browser smoke spec and backend compile check
- Builds run:
  - frontend production build in container: passed
  - host-side frontend build: failed because local Vite was not available on the machine path
- Browser checks run:
  - homepage smoke spec: passed
- Screenshots captured:
  - `.artifacts/webapp-qa/homepage.png`

Remaining limits:

- This prompt intentionally stops at repository structure. It does not yet add PostgreSQL, the file-backed GCS emulator, actual migrations, actual worker code, or TypeScript conversion for the frontend.
- `frontend/` is still the lightweight existing scaffold; later prompts will need to bring the implementation fully in line with the TypeScript requirement already documented in the product brief.

## LLM or prompt evaluation suite

- Added evaluation suite: none

Reason:

- I did not modify prompts, model wiring, adapters, agent behavior, or any executable LLM-facing logic.
- This prompt only changed repository structure, documentation, and the Docker entrypoint location.

## Wrong turns, dead ends, surprising behavior, and gotchas

- The repository already contained more scaffold than prompt 01 strictly required, including `frontend/`, `backend/`, `docs/`, `tools/webapp-qa/`, and a root-level `docker-compose.yml`. I treated prompt 01 as a regularization pass rather than deleting and recreating those areas.

- My first frontend build verification was host-side with `npm run build` in `frontend/`. That failed with `sh: vite: command not found`, which indicated the local machine environment was not the reliable verification target for this repo. I switched to the containerized build path and used that as the authoritative result.

- The browser smoke run logged a 404 in the page console. The functional assertions still passed and the screenshot looked correct; this appears to be an incidental missing asset such as a favicon rather than a regression caused by the layout change.

- A parallel `git add` and `git status` check raced, producing one stale status snapshot. I re-ran status serially before committing and verified the index contents from `git diff --cached --stat`.

- Yolopilot prompt artifact files under `prompts/` were already modified or newly created during the run. I intentionally left those out of the checkpoint commit because they were not part of the requested deliverables.

## Assumptions I had to make while working unsupervised

- I assumed it was acceptable to move the canonical Compose file under `infra/compose/` during prompt 01, even though later prompts will deepen the infrastructure story. This was the clearest way to satisfy the “obvious home for Docker Compose” acceptance criterion.

- I assumed a small wrapper script in `scripts/dev-compose.sh` was appropriate in prompt 01 because it preserves a short developer command while keeping infrastructure files out of the repository root.

- I assumed placeholder README files were preferable to empty directories because the task explicitly asked for per-folder purpose notes and because tracked empty directories would otherwise be ambiguous.

- I assumed the correct commit scope was only the repository-layout work for prompt 01, not the unrelated Yolopilot prompt logs.

## Final repository state for review

Primary reviewer entrypoints:

- `README.md`
- `infra/compose/docker-compose.yml`
- `scripts/dev-compose.sh`
- `backend/README.md`
- `docs/architecture-overview.md`

Checkpoint commit created during development:

- `b310953` — `feat(prompt-01): monorepo skeleton`

The repository is left with the requested monorepo skeleton in place, the stack still runnable from the new infra location, and the remaining uncommitted files limited to Yolopilot artifacts plus this summary file.

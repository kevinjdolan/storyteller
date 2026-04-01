# Prompt 07 Summary: Developer Bootstrap Scripts and Convenience Commands

## What I changed and why

I added a small repo-level developer command surface so the common local workflows no longer depend on memorizing long Docker or per-package commands.

The main additions were:

- A top-level `Makefile` that exposes the intended day-to-day commands:
  - `make bootstrap`
  - `make up`
  - `make down`
  - `make logs`
  - `make ps`
  - `make reset`
  - `make lint`
  - `make test`
  - `make build`
  - `make check`
  - targeted package commands for `frontend-lint`, `frontend-test`, `frontend-build`, and `backend-test`
- A new [`scripts/bootstrap-dev.sh`](/Users/kevin/code/storyteller/scripts/bootstrap-dev.sh) helper that:
  - creates `secrets.yaml` from `secrets.example.yaml` if it is missing
  - installs the repo-managed Git hooks
  - chooses a Python interpreter that is actually compatible with the backend
  - recreates `backend/.venv` if an older incompatible interpreter was used previously
  - installs backend requirements into `backend/.venv`
  - syncs frontend dependencies in `frontend/`
  - reminds the developer if `secrets.yaml` still contains the placeholder Gemini key
- A new [`scripts/reset-local-data.sh`](/Users/kevin/code/storyteller/scripts/reset-local-data.sh) helper that stops the Compose stack and removes only the durable application data volumes:
  - `storyteller_postgres_data`
  - `storyteller_gcs_data`
  - It deliberately leaves dependency cache volumes alone.
- Documentation updates in:
  - [`README.md`](/Users/kevin/code/storyteller/README.md)
  - [`infra/compose/README.md`](/Users/kevin/code/storyteller/infra/compose/README.md)
  - [`infra/persistence/README.md`](/Users/kevin/code/storyteller/infra/persistence/README.md)
  - [`scripts/README.md`](/Users/kevin/code/storyteller/scripts/README.md)

The intent was to keep the command surface small and obvious, while keeping the existing [`scripts/dev-compose.sh`](/Users/kevin/code/storyteller/scripts/dev-compose.sh) wrapper as the canonical path to the Compose file.

## Architectural changes across the codebase

The most important architectural choice here is that the repo now has a clear developer UX layer at the root instead of relying on scattered package-level or infra-level commands.

The structure is now:

- [`Makefile`](/Users/kevin/code/storyteller/Makefile) is the stable developer-facing entrypoint.
- [`scripts/dev-compose.sh`](/Users/kevin/code/storyteller/scripts/dev-compose.sh) remains the compose implementation detail.
- [`scripts/bootstrap-dev.sh`](/Users/kevin/code/storyteller/scripts/bootstrap-dev.sh) owns first-run local environment preparation.
- [`scripts/reset-local-data.sh`](/Users/kevin/code/storyteller/scripts/reset-local-data.sh) owns the safe persistent-data reset path.

That split keeps responsibilities clean:

- The `Makefile` is thin and discoverable.
- More stateful logic lives in shell scripts where it is easier to read and extend.
- Reset behavior is intentionally separate from generic `docker compose down --volumes`, which was too broad for normal migration or seed-data resets.

I also hardened bootstrap to handle a real compatibility issue: on this machine, `python3` resolved to Python 3.9.6, but the backend already uses Python 3.10+ type syntax such as `str | None`. The bootstrap script now selects a Python 3.10+ interpreter explicitly and will rebuild an old `backend/.venv` if it was created with an incompatible interpreter.

## Examples and extension points

### Daily usage examples

```bash
make bootstrap
make up
make logs
make test
make check
make down
```

### Resetting only durable local app data

```bash
make reset
make up
```

That flow is intended for cases like schema changes, migration churn, or changed seed data. It preserves dependency cache volumes so the next startup does not need to reinstall frontend or QA dependencies.

### Targeted frontend and backend checks

```bash
make backend-test
make frontend-lint
make frontend-test
make frontend-build
```

### How to extend the command surface

If future prompts add more tooling, the intended extension points are:

- Add a new `Makefile` target using the `target: ## description` pattern so it shows up automatically in `make help`.
- Add new one-off workflow logic to `scripts/` instead of embedding complex shell in the `Makefile`.
- If the app gains more durable services later, extend the `DATA_VOLUMES` list in [`scripts/reset-local-data.sh`](/Users/kevin/code/storyteller/scripts/reset-local-data.sh).

## Exact verification work performed

### Script and command verification

I ran:

- `bash -n scripts/bootstrap-dev.sh scripts/reset-local-data.sh scripts/dev-compose.sh scripts/install-git-hooks.sh scripts/check-secret-hygiene.sh`
  - Result: passed
- `make help`
  - Result: passed
  - Confirmed the new targets render correctly and are discoverable from the root
- `make bootstrap`
  - Result: passed
  - Confirmed hook installation, backend virtualenv setup, backend dependency installation, frontend dependency sync, and placeholder-key reminder behavior

### Automated quality checks

I ran:

- `make lint`
  - Result: passed
  - Frontend ESLint passed
- `make test`
  - Result: passed after fixing bootstrap interpreter selection
  - Backend: `11` tests passed
  - Frontend: `1` test file passed, `2` tests passed
- `make build`
  - Result: passed
  - Frontend production build completed successfully
- `make check`
  - Result: passed
  - Confirmed the aggregate command correctly runs lint, tests, and build together

### Compose lifecycle verification

I ran:

- `make up`
  - Result: partially verified
  - The new root target invoked Compose correctly, built images, created the network, and started Postgres and fake GCS successfully.
  - The backend container then exited because the existing local `secrets.yaml` on this machine contains unsupported legacy keys:
    - `gemini.api_key_name`
    - `gemini.project_name`
    - `gemini.project_number`
    - `openai`
  - This appears to be a pre-existing local configuration mismatch, not a regression introduced by the new command wrappers.
- `make ps`
  - Result: passed
  - Confirmed Compose status output from the root entrypoint
- `make down`
  - Result: passed
  - Confirmed stack shutdown and cleanup without removing persistent data

### Browser checks and screenshots

No browser checks or screenshots were run.

Reason:

- This task did not change UI behavior, styling, rendering, layout, or accessibility.
- The prompt scope was developer tooling and documentation, not frontend behavior.

### Reset-path verification limits

I did not execute `make reset` end-to-end.

Reason:

- This machine already had live Docker volumes named:
  - `storyteller_postgres_data`
  - `storyteller_gcs_data`
  - `storyteller_frontend_node_modules`
  - `storyteller_webapp_qa_node_modules`
- Running `make reset` would have intentionally deleted the real local Postgres and fake GCS data volumes.
- That would have been an unnecessary destructive action for this prompt.

What I did verify instead:

- Script syntax via `bash -n`
- Target wiring via `make help`
- The exact volume names and behavior documented in the reset script
- The surrounding compose lifecycle with `make up`, `make ps`, and `make down`

## LLM or prompt evaluation suite

No LLM-facing logic changed in this task.

I did not modify:

- prompts
- evals
- model selection
- agent behavior
- structured output schemas
- AI orchestration logic

Because of that, no new LLM evaluation suite was added.

LLM evaluation status:

- `LLM-facing changes present`: `No`
- `Evaluation suite added`: `No`
- `Named criteria`: `Not applicable`

## Wrong turns, dead ends, surprising behavior, and gotchas

### Wrong turn: bootstrap initially preferred `python3`

My first version of the bootstrap script chose `python3` before `python`.

On this machine:

- `python3` was `/usr/bin/python3` at `Python 3.9.6`
- `python` was the active Conda environment at `Python 3.13.12`

That caused `make bootstrap` to create `backend/.venv` with Python 3.9, and then `make test` failed because the backend already uses Python 3.10+ typing syntax. I corrected that by making bootstrap explicitly search for a Python 3.10+ interpreter and rebuild an incompatible virtualenv automatically.

### Surprising repository behavior: local `secrets.yaml` is ahead or behind the checked-in schema

`make up` did not fail because of the new wrapper logic. It failed because the existing untracked `secrets.yaml` in this workspace contains fields that the current backend settings model rejects as extras.

That means a developer with an older local secrets file can still hit a stack-start failure even with the new commands. The docs now point more clearly at the current config shape, but the local file itself still has to be updated by the developer when the schema changes.

### Reset verification gotcha

The new `make reset` target is intentionally destructive to app data, so it was not safe to exercise directly on this machine once I confirmed the named volumes already existed. I chose not to wipe real local data just to force a green verification line for that one target.

## Assumptions made while working unsupervised

- Using a root `Makefile` plus Bash helper scripts is acceptable for this repo, as long as the shell expectations are documented.
- macOS, Linux, or WSL is the target development environment for these helper commands.
- The existing [`scripts/dev-compose.sh`](/Users/kevin/code/storyteller/scripts/dev-compose.sh) wrapper should remain the single source of truth for Compose file targeting.
- The safe reset path should preserve dependency caches and only wipe durable application data.
- Prompt 07 was about workflow wrappers and documentation, not about introducing new linting or formatting tools beyond what the repo already had.
- It was acceptable to commit the implementation changes before writing this summary file, leaving this markdown file itself as the final uncommitted filesystem change for the task.

## Final state for reviewers

The repository now has an obvious root-level workflow for:

- bootstrapping a clone
- starting and stopping the local stack
- viewing logs and service state
- resetting durable local data safely
- running the existing lint, test, and build checks from one place

The main implementation commit for the task is:

- `b01adfd` — `feat(prompt-07): developer bootstrap scripts`

The only known environment-specific limitation I hit during verification is the existing local `secrets.yaml` mismatch described above. The command wrappers themselves are in place and the quality-check flow passes.

# Prompt 06 Summary

## What I Changed and Why

This task hardened the repository against accidental secret commits and routine local-development clutter.

- Expanded [.gitignore](/Users/kevin/code/storyteller/.gitignore) so the repo now ignores:
  - live local secret files such as `secrets.yaml`
  - local env files such as `.env`, `.env.*`, and `.envrc`
  - Python caches and coverage artifacts
  - frontend build output and tool caches
  - reserved local persistence directories under `infra/persistence/`
  - editor and OS noise such as `.DS_Store`, `.idea/`, and `.vscode/`
- Tightened [docs/secrets-and-local-config.md](/Users/kevin/code/storyteller/docs/secrets-and-local-config.md) with a dedicated commit-hygiene section that explicitly states `secrets.yaml` is the live local credentials file and must never be committed.
- Added a lightweight staged-commit guard:
  - [.githooks/pre-commit](/Users/kevin/code/storyteller/.githooks/pre-commit)
  - [scripts/check-secret-hygiene.sh](/Users/kevin/code/storyteller/scripts/check-secret-hygiene.sh)
  - [scripts/install-git-hooks.sh](/Users/kevin/code/storyteller/scripts/install-git-hooks.sh)
- Updated the quick-start and script docs so contributors see the safe flow immediately:
  - [README.md](/Users/kevin/code/storyteller/README.md)
  - [scripts/README.md](/Users/kevin/code/storyteller/scripts/README.md)
  - [infra/persistence/README.md](/Users/kevin/code/storyteller/infra/persistence/README.md)

The practical outcome is that a contributor now has to bypass both `.gitignore` and an optional but repo-managed pre-commit hook to commit `secrets.yaml` or a clearly live Gemini/private-key value.

## Architectural Changes Across the Codebase

This prompt did not change product runtime architecture, but it did add a small repository-hygiene architecture that was previously missing.

### 1. Clear split between live config and tracked examples

[docs/secrets-and-local-config.md](/Users/kevin/code/storyteller/docs/secrets-and-local-config.md) now explicitly defines:

- `secrets.yaml` as the live local-only file
- `secrets.example.yaml` as the tracked template
- `*.example.*`, `.sample`, and `.template` naming as the safe pattern for tracked placeholders

That makes the repo’s intent much clearer during onboarding and review.

### 2. Repo-managed Git hook entrypoint

The new guard rail is intentionally simple:

1. A developer runs `./scripts/install-git-hooks.sh` once per clone.
2. That sets `core.hooksPath` to `.githooks`.
3. Git calls `.githooks/pre-commit`.
4. The hook delegates to `scripts/check-secret-hygiene.sh`.

That keeps the actual checking logic in a normal script under `scripts/` instead of burying it in an opaque hook file.

### 3. Reserved ignored persistence locations

[infra/persistence/README.md](/Users/kevin/code/storyteller/infra/persistence/README.md) and [.gitignore](/Users/kevin/code/storyteller/.gitignore) now agree on a convention for host-mounted local runtime data:

- `infra/persistence/runtime/`
- `infra/persistence/postgres-data/`
- `infra/persistence/gcs-data/`
- `infra/persistence/local/`

Today’s Compose setup still uses named Docker volumes, but these ignored paths give future prompts a safe place to put dev-only state without polluting git.

## New Helpers and How to Use Them

### Install the repo-managed hook

```bash
./scripts/install-git-hooks.sh
```

This configures `core.hooksPath` to `.githooks` for the current clone.

### Normal local setup

```bash
cp secrets.example.yaml secrets.yaml
./scripts/install-git-hooks.sh
./scripts/dev-compose.sh up --build
```

### What the hook blocks

- staging `secrets.yaml`
- staging `.env`, `.env.*`, or `.envrc`
- staging lines that look like live Gemini/Google API keys
- staging PEM-style private key material
- staging obvious secret assignment lines such as `STORYTELLER_GEMINI_API_KEY=...`

### Safe example-file pattern

Tracked placeholders should live in files such as:

- `secrets.example.yaml`
- `.env.example`
- `.env.local.example`

They should contain placeholders only, never live credentials.

### Safe local persistence convention

If future work needs host-mounted dev data, put it under:

- `infra/persistence/runtime/`
- `infra/persistence/postgres-data/`
- `infra/persistence/gcs-data/`
- `infra/persistence/local/`

Those paths are now ignored by default.

## Exact Verification Work Performed

### Syntax and shell validation

Ran:

```bash
bash -n scripts/check-secret-hygiene.sh scripts/install-git-hooks.sh .githooks/pre-commit
```

Outcome:

- Pass

### Ignore-rule verification

Ran:

```bash
printf '%s\n' \
  'secrets.yaml' \
  '.env' \
  '.env.local' \
  'infra/persistence/runtime/demo.db' \
  'secrets.example.yaml' \
  '.env.example' \
  | git check-ignore -v --stdin
```

Observed:

- `secrets.yaml` matched `.gitignore`
- `.env` matched `.gitignore`
- `.env.local` matched `.gitignore`
- `infra/persistence/runtime/demo.db` matched `.gitignore`
- `.env.example` was explicitly unignored by the negation rule

Then ran:

```bash
git check-ignore secrets.example.yaml .env.example
```

Outcome:

- Exit code `1`, confirming both example files remain trackable

### Hook installation verification

Ran:

```bash
./scripts/install-git-hooks.sh && git config --get core.hooksPath
```

Observed:

- installer printed `Configured repo-local Git hooks at /Users/kevin/code/storyteller/.githooks`
- `git config --get core.hooksPath` returned `.githooks`

### Behavioral verification in isolated temporary repositories

Ran a temporary-repo test harness that exercised three cases against `scripts/check-secret-hygiene.sh`.

Measured outcomes:

- `allow_sample`: `pass`
  - staged `secrets.example.yaml` with placeholder content
  - expected result: allowed
- `block_file`: `pass`
  - staged `secrets.yaml`
  - expected result: blocked
- `block_value`: `pass`
  - staged a file containing `STORYTELLER_GEMINI_API_KEY=AIza...`
  - expected result: blocked

### Safe-path commit verification

Created a checkpoint commit after installing the hook:

```text
bb1fbea feat(prompt-06): gitignore and secrets hygiene
```

That commit succeeding after `core.hooksPath` was set confirmed the safe-change path still works with the hook enabled.

### Builds, tests, browser checks, and screenshots

- Backend test suite: not run
- Frontend test suite: not run
- Type checks: not run
- Lint/build pipelines: not run
- Browser checks: not run
- Screenshots: none

Reason:

- this prompt only changed repo hygiene, docs, and shell tooling
- no backend or frontend runtime behavior changed
- there was no UI, rendering, layout, or accessibility impact to verify in a browser

### Remaining verification limits

- The hook is intentionally lightweight and pattern-based. It is not a full secret scanner.
- It focuses on the repo’s current risk profile: `secrets.yaml`, `.env` files, Gemini/Google-style keys, private keys, and obvious secret assignments.
- A determined contributor can still bypass local hooks with `--no-verify`, so `.gitignore` and documentation still matter.

## LLM or Prompt Evaluation Suite

No LLM-facing code, prompts, evals, agent wiring, or model configuration changed in this task.

Evaluation suite added:

- None

Criteria and results:

- `llm_eval_applicable`: `not_applicable`

## Wrong Turns, Dead Ends, Surprising Behavior, and Gotchas

### Wrong turn: `mapfile` portability

The first version of `scripts/check-secret-hygiene.sh` used `mapfile` to collect staged paths. That failed on the default macOS Bash available in this environment because Bash 3.2 does not provide `mapfile`.

Fix:

- replaced `mapfile` with a `while IFS= read -r` loop

Why it mattered:

- the hook needs to work with the shell contributors are likely to already have, not just with a newer Homebrew Bash

### Gotcha: `git check-ignore -v` with negation rules

`git check-ignore -v --stdin` showed the negation rule for `.env.example`, which is easy to misread at a glance. I validated the allow-case separately with `git check-ignore secrets.example.yaml .env.example` and confirmed the exit code was `1`.

### Pre-existing worktree noise

The repository already had unrelated prompt automation files in the worktree before I wrote the summary:

- modified `prompts/05-backend-settings-and-secrets-loading.yolopilot.jsonlines`
- modified `prompts/05-backend-settings-and-secrets-loading.yolopilot.md`
- untracked prompt-06 automation logs

I left those untouched and limited the commit to prompt-06 hygiene changes only.

## Assumptions Made While Working Unsupervised

- A repo-managed hook plus a one-time installer script counts as a lightweight, contributor-friendly secret guard rail.
- Reserving ignored directories under `infra/persistence/` is useful now even though current local persistence still uses named Docker volumes.
- The repo should prefer tracked example files over committed local config variants, so broad `.env` ignores with explicit example-file exceptions are appropriate.
- No browser or application-runtime verification was required because the task did not change product behavior.

## Files Touched

- [.gitignore](/Users/kevin/code/storyteller/.gitignore)
- [README.md](/Users/kevin/code/storyteller/README.md)
- [docs/secrets-and-local-config.md](/Users/kevin/code/storyteller/docs/secrets-and-local-config.md)
- [infra/persistence/README.md](/Users/kevin/code/storyteller/infra/persistence/README.md)
- [scripts/README.md](/Users/kevin/code/storyteller/scripts/README.md)
- [scripts/check-secret-hygiene.sh](/Users/kevin/code/storyteller/scripts/check-secret-hygiene.sh)
- [scripts/install-git-hooks.sh](/Users/kevin/code/storyteller/scripts/install-git-hooks.sh)
- [.githooks/pre-commit](/Users/kevin/code/storyteller/.githooks/pre-commit)

## Final State

Checkpoint commit created:

- `bb1fbea` — `feat(prompt-06): gitignore and secrets hygiene`

The required summary file for this prompt now exists at [06-gitignore-and-secrets-hygiene.summary.md](/Users/kevin/code/storyteller/prompts/06-gitignore-and-secrets-hygiene.summary.md).

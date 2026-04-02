# Prompt 09 Summary: Initial System Diagram and ADR

## What I Changed and Why

I added the first architecture decision record and a dedicated system diagram so later prompts have a stable, explicit map of where durable state, realtime updates, asset storage, and long-running generation belong.

The main additions are:

- `docs/adr/0001-core-runtime-architecture.md`
- `docs/system-diagram.md`

I also updated the existing docs entrypoints so those new references are discoverable instead of buried:

- `docs/architecture-overview.md`
- `docs/README.md`
- `docs/adr/README.md`
- `README.md`

The ADR records the project’s first durable architecture choices in plain language:

- Gemini calls stay backend-owned
- PostgreSQL is the durable source of truth for sessions, workflow state, jobs, and event history
- generated files live in the file-backed GCS emulator during local development
- live progress uses WebSockets
- long-running composition and audio work run in a separate worker process
- word count, runtime, and chapter count are soft planning hints rather than hard limits

The goal was not to add placeholder runtime code for workers or websocket endpoints before those prompts arrive. The goal was to document the intended boundaries now so future implementation work does not drift into route-thread jobs, browser-owned state, or direct browser-to-provider calls.

I also created a checkpoint commit for the architecture docs work before writing this summary:

- `c9bf1d5` — `feat(prompt-09): initial system diagram and adr`

## Architectural Changes Across the Codebase

This prompt changed documentation only. No runtime Python or TypeScript behavior changed yet.

That said, the documentation now establishes concrete architectural direction across the repo:

### 1. Core runtime decision is now codified as an ADR

`docs/adr/0001-core-runtime-architecture.md` is now the source of truth for the first set of architectural rules. It turns broad product requirements into explicit implementation constraints:

- the browser must never call Gemini directly
- the backend policy layer validates model-suggested actions
- PostgreSQL owns durable session resume and durable event history
- object storage owns large generated artifacts
- workers own long-running generation work
- WebSockets are delivery channels, not the source of truth

### 2. Session resume and event history are now first-class in the diagram

`docs/system-diagram.md` includes:

- the browser
- FastAPI API layer
- WebSocket session stream
- worker process
- PostgreSQL
- file-backed GCS emulator
- Gemini adapters

The diagram explicitly shows:

- session resume coming from durable state
- durable event history living in PostgreSQL
- workers claiming jobs and persisting partial outputs
- artifact files in object storage with metadata kept in PostgreSQL

That satisfies the acceptance check that contributors should be able to tell where realtime updates and long-running tasks belong.

### 3. Existing architecture docs now point to the new canonical references

I updated `docs/architecture-overview.md` to link to the ADR and system diagram and to restate the soft-constraint philosophy directly in the architecture overview.

I updated `docs/README.md`, `docs/adr/README.md`, and `README.md` so a contributor entering from any of the common top-level docs can find the new architecture references quickly.

## Examples: How To Use The New Decisions

No new runtime abstractions or helper modules were added in this prompt, so the useful examples here are extension-point examples for future prompts.

### Example 1: A future realtime prompt

If a later prompt adds live composition progress, it should:

- add websocket endpoints under `backend/app/api/`
- load current session state from PostgreSQL on connect or reconnect
- replay recent durable events from PostgreSQL
- then continue streaming live progress

It should not:

- treat the websocket stream as the only source of truth
- keep unsaved progress only in browser memory

### Example 2: A future worker prompt

If a later prompt adds composition or audio execution, it should:

- create durable job records from the API layer
- let a separate worker process claim those jobs
- persist segment-by-segment progress to PostgreSQL
- write generated artifacts to the GCS-backed storage layer
- append durable events that the API can expose to chat and UI

It should not:

- run long story generation directly inside FastAPI request handlers
- rely on browser refresh survival without durable job records

### Example 3: A future storage prompt

If a later prompt adds story exports or audio files, it should:

- store file metadata and relationships in PostgreSQL
- store the actual file bytes in the configured object store

It should not:

- embed large audio or document payloads directly in relational rows

### Example 4: A future prompt that intentionally changes direction

If a later prompt needs to replace one of these choices, the new process should be:

1. add a new ADR in `docs/adr/`
2. explain which decision is being replaced
3. update `docs/architecture-overview.md` and the system diagram if needed

The ADR explicitly calls for that instead of silent drift.

## Exact Verification Work Performed

### Repository checks

I ran the full repo verification target:

```bash
make check
```

Observed results:

- frontend formatting check: pass
- frontend lint: pass
- backend lint: pass
- backend tests: pass, `11/11`
- frontend tests: pass, `1/1` test file and `2/2` tests
- frontend production build: pass

The backend pytest output completed successfully with:

- `tests/test_health.py`: pass
- `tests/test_settings.py`: pass

### Docs-specific formatting verification

Because the normal repo quality commands do not validate Markdown docs, I also ran:

```bash
./node_modules/.bin/prettier --check ../README.md $(find ../docs -name '*.md' -print | sort)
```

Run location:

- `frontend/`

Observed result:

- Markdown formatting check for `README.md` and all files under `docs/`: pass

### Browser checks, screenshots, and visual QA

None performed.

Reason:

- this prompt only changed documentation
- no UI behavior, styling, rendering, layout, accessibility, or browser interaction changed

### Remaining verification limits

- I did not add Markdown linting to the repo because this prompt did not ask for tooling expansion.
- I did not render the Mermaid diagram through a separate documentation pipeline; verification was limited to source review plus Markdown formatting checks.
- I did not add or run browser-based docs rendering checks because the repository does not currently have a docs site pipeline to validate against.

## LLM or Prompt Evaluation Suite

No LLM-facing runtime code, prompts, eval harnesses, model wiring, or agent behavior changed in this task.

Evaluation suite status:

- `LLM eval suite added`: none
- `Status`: not applicable
- `Criteria measured`: none

## Wrong Turns, Dead Ends, Surprising Behavior, and Gotchas

### 1. The prompt’s `base_prompt.md` path did not match the repo layout

The task text says to read `base_prompt.md` first, but the actual file in this repository is:

- `prompts/base_prompt.md`

I read the correct repo file and used that as the product source of truth.

### 2. My first standalone Markdown format check used a shell glob that zsh rejected

This command failed because the `**` glob did not match in that shell invocation:

```bash
npm --prefix frontend exec prettier --check ../README.md ../docs/**/*.md
```

I corrected that by switching to the direct Prettier binary plus `find`, which produced a clean check result.

### 3. `npm exec prettier` behaved in a surprising way with file arguments

One intermediate attempt passed the file list through `npm exec` incorrectly, which caused file contents to be printed instead of performing the intended check. I avoided that by calling:

```bash
./node_modules/.bin/prettier ...
```

directly from `frontend/`.

### 4. The worktree already contained unrelated prompt-log churn

Before I started, the repository already had modified and untracked prompt-log files unrelated to this task:

- modified:
  - `prompts/08-repo-quality-tooling.yolopilot.jsonlines`
  - `prompts/08-repo-quality-tooling.yolopilot.md`
- untracked:
  - `prompts/09-initial-system-diagram-and-adr.codex.jsonlines`
  - `prompts/09-initial-system-diagram-and-adr.yolopilot.jsonlines`
  - `prompts/09-initial-system-diagram-and-adr.yolopilot.md`

I left those untouched and staged only the intended architecture docs and README changes for the checkpoint commit.

## Assumptions I Made While Working Unsupervised

- The correct home for the first architecture decision record is `docs/adr/` with a numbered ADR filename, so I created `0001-core-runtime-architecture.md`.
- A separate one-page diagram file was more useful than burying the only system diagram inside a longer prose doc, so I added `docs/system-diagram.md`.
- This prompt was asking for architecture documentation, not placeholder runtime implementation, so I did not add dummy websocket routes, worker services, or schema stubs just to “match” the docs.
- The architecture notes should describe the intended product shape even if parts of that shape are still future work, as long as the docs clearly avoid claiming those pieces are already implemented.
- A checkpoint commit before the final summary file best matched the instruction to commit periodically while still keeping the final action of the task as writing this summary file.

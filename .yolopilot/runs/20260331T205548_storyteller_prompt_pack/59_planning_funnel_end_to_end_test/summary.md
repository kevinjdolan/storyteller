# Prompt 59 Summary: Planning Funnel End-to-End Test

## What I changed and why

I added a dedicated backend HTTP-level end-to-end regression test in [backend/tests/test_planning_funnel_e2e.py](/Users/kevin/code/storyteller/backend/tests/test_planning_funnel_e2e.py) and a short design note in [docs/planning-funnel-e2e-test.md](/Users/kevin/code/storyteller/docs/planning-funnel-e2e-test.md).

The new test exists because the repo already had strong endpoint-level coverage for each planning step, but it did not have one coherent test that proved those steps still compose into a single durable funnel from:

1. genre selection
2. tone selection
3. story brief save
4. pitch generation and pitch selection
5. character generation and character selection
6. beat-sheet generation and beat-sheet selection
7. story-setup save with automatically generated outline

That gap meant the system could regress in the seams between stages without one test failing in a reviewer-friendly way.

## Architectural changes across the codebase

No production application code changed. The architectural changes are in the test layer and test documentation.

### 1. New HTTP-level funnel harness

The new test spins up the real FastAPI app against a temporary SQLite database and drives the real `/api/v1/sessions/...` endpoints in sequence.

What this exercises for real:

- FastAPI request validation and routing
- dependency wiring through `create_app()`
- SQLAlchemy persistence and snapshot reloads
- event log writes and replayable history
- stage transition and rollup logic
- usage tracking rollups
- plan revision capture
- story setup tool execution
- automatic outline generation
- hydration reads used by the workspace

What stays mocked:

- brief normalization adapter
- pitch generation adapter
- character generation adapter
- beat-sheet generation adapter

That boundary is intentional. The test mocks only provider-facing model calls and keeps the rest of the workflow real.

### 2. Realistic structured model doubles

The test introduces provider-boundary doubles that return realistic structured outputs and token metadata instead of toy placeholder values.

Those stubs are intentionally shaped to stress downstream assumptions:

- 3 distinct pitch candidates with different hooks/conflicts
- 3 character-sheet candidates with real protagonist/supporting-cast structure
- 15 Save-the-Cat beats with softening notes on key low points
- brief normalization output with normalized summary and preferences

This makes the test more likely to catch regressions in snapshot shaping, history payloads, usage accounting, and outline generation than a minimal fake would.

### 3. Explicit test-design documentation

The design note documents:

- why the test is HTTP-level instead of service-only
- what is real versus mocked
- why it runs in the default backend suite
- current limits, especially SQLite instead of Postgres and no browser coverage

## New helpers and extension points

The new test file includes a few reusable pieces for future funnel or journey tests.

### `planning_funnel_api_client`

This fixture creates:

- a temp SQLite database
- the real FastAPI app
- seeded genre/tone catalog data
- realistic planning-stage adapter doubles

Future tests can reuse the same pattern when they need a real app plus deterministic planning outputs.

### `PlanningFunnelJourney`

This dataclass collects the key responses from the journey so downstream assertions can stay readable instead of indexing deeply into raw response dictionaries.

### `_run_planning_funnel(client)`

This helper executes the whole funnel and returns a `PlanningFunnelJourney`.

Example:

```python
journey = _run_planning_funnel(client)

final_snapshot = journey.story_setup["snapshot"]
outline = final_snapshot["selected_story_outline"]

assert final_snapshot["current_stage"] == "composition"
assert outline["outline_kind"] == "chapter"
assert len(outline["cards"]) == 4
```

### Adapter doubles as extension points

If future prompts change the planning contract, the easiest way to keep this test realistic is to update the stub adapters first instead of weakening assertions.

Example:

```python
app.state.pitch_generation_adapter = PlanningFunnelPitchGenerationAdapter()
app.state.character_generation_adapter = PlanningFunnelCharacterGenerationAdapter()
```

That keeps the test anchored at the provider boundary.

## What the new end-to-end test verifies

The test proves the following in one run:

- stage progression advances correctly from `genre` through `story_setup`
- the final snapshot lands on `current_stage == composition`
- the first seven workflow stages are completed and later stages remain draft
- the selected genre, tone, brief, pitch, character sheet, and beat sheet remain consistent across the final snapshot
- story setup preferences persist durably
- a usable structured outline is generated automatically from the accepted beat sheet plus story setup
- outline cards remain draftable and cover the beat sheet in order
- the session reload endpoint returns the same durable outline and current plan revision
- the hydration endpoint returns the same durable planning state the workspace would consume
- event history shows the expected sequence of user edits, AI outputs, and selections
- plan revision lineage includes the accepted pitch, character, beat, and story-setup checkpoints
- model usage accounting reflects the four mocked planning calls

## Exact verification work performed

### Targeted pytest checks

Ran:

```bash
backend/.venv/bin/python -m pytest backend/tests/test_planning_funnel_e2e.py -q
```

Result:

- `1 passed in 0.69s`

### Adjacent planning-suite regression pass

Ran:

```bash
backend/.venv/bin/python -m pytest \
  backend/tests/test_session_api.py \
  backend/tests/test_session_beat_sheet_service.py \
  backend/tests/test_outline_generation_service.py \
  backend/tests/test_story_tools.py \
  backend/tests/test_planning_funnel_e2e.py \
  -q
```

Result:

- `60 passed in 6.27s`

This was the most important validation beyond the new test itself because the new journey test touches the same contracts as the existing API/session/story-tool coverage.

### Lint and formatting

Ran:

```bash
cd backend && .venv/bin/python -m ruff check tests/test_planning_funnel_e2e.py
cd backend && .venv/bin/python -m ruff format --check tests/test_planning_funnel_e2e.py
```

Result:

- Ruff lint passed
- Ruff format check passed after one formatting normalization pass

### Browser checks and screenshots

None performed.

Reason:

- this task only added backend test coverage and documentation
- no frontend/UI/runtime rendering code changed
- the new test validates the backend contract that the existing workspace UI would consume

### Builds

No frontend or backend build step was required for this change because no production code or dependency graph changed. I prioritized targeted backend verification plus lint/format checks on the touched test file.

## LLM or prompt evaluation suite

No new LLM or prompt evaluation suite was added.

Reason:

- I did not modify prompt text, model selection, evaluation heuristics, or provider wiring
- this task only added a regression test around existing planning behavior

Existing service-level evaluation logic for pitch, character, and beat generation remains unchanged and was exercised indirectly through the realistic mocked outputs.

## Wrong turns, dead ends, and gotchas

### 1. `chapter_style` looked available but is not part of the current API contract

I initially sent `chapter_style` in the story-setup request and expected it to persist because `StorySetupView` and outline-generation code already know about it.

What actually happened:

- `SaveSessionStorySetupRequest` does not currently accept `chapter_style`
- the extra field was ignored
- the final `selected_story_setup.chapter_style` was `null`

I corrected the test to stay inside the actual public API contract and asserted the drafting brief from fields that are truly persisted today.

### 2. I initially assumed the “current” plan revision would be revision 1

That was wrong.

The repository currently captures plan revisions incrementally when the user accepts:

- the pitch
- the character sheet
- the beat sheet
- the story setup

So by the end of this journey the current revision is later in the lineage. I changed the assertions to verify the meaningful invariant instead:

- the latest plan revision is sourced from `story_setup`
- it includes the generated story setup and outline
- the recent source-stage lineage includes `story_setup`, `beats`, `characters`, and `pitches`

### 3. The default shell `python3` did not have repo tooling installed

The first verification attempt failed because `/usr/bin/python3` did not have `pytest` or `ruff`.

I switched to the repo-local backend environment:

- `backend/.venv/bin/python`

That was the correct toolchain for the repo.

## Assumptions I made while working unsupervised

- A backend HTTP-level e2e test is sufficient for prompt 59 because the task is specifically about proving durable planning-funnel evolution, not browser rendering.
- Keeping mocks only at the model-adapter boundary is the right fidelity/maintenance tradeoff for this prompt.
- SQLite is acceptable for this test because it runs in the default suite and exercises the durable workflow logic without hiding behind optional integration flags.
- It is better for this task to avoid refactoring the large existing `test_session_api.py` file and instead add an explicit funnel-focused test with its own harness.
- The unrelated `.yolopilot` run-state files in the working tree should remain untouched.

## Commit checkpoint

Created commit:

- `0c0ed3a feat(prompt-59): planning funnel e2e test`

## Repository state after my work

Code and docs for prompt 59 are committed.

Unrelated `.yolopilot` run-state files were already modified/untracked in the working tree and were left alone intentionally. This summary file itself is also a new task artifact and is intentionally written after verification as required.

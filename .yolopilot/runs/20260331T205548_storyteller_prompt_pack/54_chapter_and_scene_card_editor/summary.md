# Prompt 54 — Chapter and Scene Card Editor

Commit checkpoint: `6507cc3` (`feat(prompt-54): chapter scene card editor`)

## What Changed And Why

This prompt asked for a granular outline editor between story setup and composition. The repo already had a first-pass outline save path and a minimal text editor inside `StorySetupStage`, but it was missing three core requirements:

- real card-level inspection with the fields composition actually needs at a glance
- reorder support and a sensible regenerate-this-card interaction
- explicit downstream invalidation when an outline change is structural instead of cosmetic

I completed that gap end to end.

On the backend:

- I extended the outline model so cards now carry a `purpose` field in addition to title, summary, beat links, emotional shift, and target lengths.
- I added `StoryOutlineGenerationService.regenerate_card(...)` so a single card can be rebuilt from its linked beats and saved setup targets without regenerating the whole pipeline.
- I added `backend/app/services/story_outline_editor.py`, which centralizes three concerns:
  - normalizing card order/positions
  - regenerating selected cards inside a proposed draft
  - classifying a draft revision as `minor` or `major`
- I extended the `update_story_outline` workflow tool input with `regenerate_card_keys`, so the UI can request a selective card regeneration while still saving a normal outline revision.
- I made outline saves persist richer metadata:
  - `last_change_summary`
  - `change_impact`
  - `invalidated_stages`
  - `refreshes_downstream`
  - `edit_history`
- I extended user-edit event payloads so outline revisions can carry changed card keys, regenerated card keys, reorder state, and impact metadata through durable history.
- I updated hydration so the frontend gets typed outline edit history instead of having to infer it from raw JSON.
- I propagated saved outline revision summaries into conversation memory and initial chat hydration so the session summary reflects outline edits instead of only “outline ready”.

On the frontend:

- I replaced the old “choose a card from a dropdown and edit a few text fields” UI with a true card workspace inside [StorySetupStage.tsx](/Users/kevin/code/storyteller/frontend/src/features/session/StorySetupStage.tsx):
  - visible chapter/scene cards in a rail
  - title, purpose, linked beats, target length, and summary visible per card
  - move earlier / move later controls
  - a sticky editor panel for the active card
  - a dedicated `Regenerate this card` action
- I changed the outline editor draft state to own the full card list, not just a few editable fragments. That keeps reorder, save, regenerate, and impact preview aligned to one source of truth.
- I added client-side structural-change preview logic so the user sees whether the current draft is a light revision or a structural one before saving.
- I updated the save callback from [SessionWorkspacePage.tsx](/Users/kevin/code/storyteller/frontend/src/pages/session/SessionWorkspacePage.tsx) so the page can forward `regenerateCardKeys` to the backend.
- I added styling for the two-column desktop editor and stacked mobile layout in [index.css](/Users/kevin/code/storyteller/frontend/src/styles/index.css).

## Architectural Changes Across The Codebase

### 1. Outline editing is now a first-class backend concern

Before this prompt, the frontend could save edited outline text, but the backend had no real notion of outline-change impact or selective card regeneration.

The new backend flow is:

1. UI sends the full draft card list, optionally with `regenerate_card_keys`.
2. `StoryWorkflowToolService._update_story_outline(...)` normalizes positions, selectively regenerates requested cards, and classifies the resulting revision with `assess_story_outline_edit(...)`.
3. The new revision persists edit metadata into outline `metadata_json`.
4. Hydration materializes that metadata back into `StoryOutlineView`.

That keeps outline editing durable and backend-owned instead of turning the browser into the policy engine.

### 2. Outline revision metadata now supports future extension points

The saved metadata shape is intentionally useful beyond this prompt:

- `edit_history` gives future prompts a stable revision audit trail for outline edits.
- `change_impact` gives composition/audio UI a cheap way to decide whether to show stronger stale-plan warnings.
- `invalidated_stages` makes downstream propagation explicit rather than hard-coded only in stage status transitions.

### 3. The UI now edits a full draft card list

The important frontend structural change was moving from “edit a selected saved card” to “edit a draft list of cards”.

That change made the rest of the prompt straightforward:

- reorder updates the same draft list
- save serializes the same draft list
- regenerate operates against the same draft list
- impact preview compares that same draft list against the last saved revision

## Examples Of New Abstractions, Helpers, And Extension Points

### Selective card regeneration

The shared outline save endpoint now supports this request shape:

```json
{
  "outline_id": "outline-123",
  "summary": "Four draftable chapters mapped from the beat sheet.",
  "cards": [/* full current draft card list */],
  "regenerate_card_keys": ["chapter-2"],
  "origin": "workspace"
}
```

That asks the backend to:

- keep the current draft order and non-targeted cards
- rebuild only `chapter-2` from its linked beats and saved targets
- persist the result as a normal outline revision

### Shared outline edit assessment

[story_outline_editor.py](/Users/kevin/code/storyteller/backend/app/services/story_outline_editor.py) now provides reusable helpers:

- `normalize_story_outline_cards(...)`
- `regenerate_story_outline_cards(...)`
- `assess_story_outline_edit(...)`

Current classification rules are intentionally deterministic:

- `major`
  - card order changed
  - structural fields changed
  - more than one card changed in one revision
- `minor`
  - a single card changed and the change stayed textual/editorial

That file is the right place to extend future rules if later prompts allow editable beat links, scene-count targets, or outline-card deletion/insertion.

### Hydrated outline history

`StoryOutlineView` now exposes:

- `last_change_summary`
- `change_impact`
- `refreshes_downstream`
- `invalidated_stages`
- `edit_history`

That means future prompts can build:

- outline revision timelines
- “what changed since composition started” warnings
- targeted restore/revert flows

without re-parsing raw metadata blobs.

## Verification Performed

### Backend verification

Commands run:

- `python -m compileall backend/app`
- `ruff check backend/app/models/story_outline.py backend/app/models/session.py backend/app/models/events.py backend/app/models/story_tools.py backend/app/models/__init__.py backend/app/services/outline_generation.py backend/app/services/story_outline_editor.py backend/app/services/story_tools.py backend/app/services/session_hydration.py backend/app/services/event_log.py backend/app/services/conversation_memory.py backend/tests/test_outline_generation_service.py backend/tests/test_story_tools.py`
- `pytest backend/tests/test_outline_generation_service.py backend/tests/test_story_tools.py -q`
- `pytest backend/tests/test_session_api.py -q`

Results:

- `backend/tests/test_outline_generation_service.py`: passed
- `backend/tests/test_story_tools.py`: passed
- `backend/tests/test_session_api.py`: 33 passed

Coverage added by this prompt:

- outline generation now asserts card purposes are present
- story-tool tests now cover:
  - minor outline edits
  - structural reorder edits
  - selective card regeneration metadata

### Frontend verification

Commands run:

- `npm --prefix frontend test -- --run StorySetupStage.test.tsx`
- `npm --prefix frontend test -- --run SessionWorkspacePage.test.tsx`
- `npm --prefix frontend test -- --run StorySetupStage.test.tsx SessionWorkspacePage.test.tsx`
- `npm --prefix frontend run lint`
- `npm --prefix frontend run build`
- `npx --prefix frontend prettier --write frontend/src/api/sessions.ts frontend/src/pages/session/SessionWorkspacePage.tsx frontend/src/features/session/StorySetupStage.tsx frontend/src/features/session/StorySetupStage.test.tsx frontend/src/features/session/chat/sessionChat.ts frontend/src/styles/index.css`

Results:

- `StorySetupStage.test.tsx`: 5 passed
- `SessionWorkspacePage.test.tsx`: 31 passed
- `eslint`: passed
- production build: passed

Frontend test coverage added by this prompt:

- outline save still works with the richer card payload
- reorder produces structural invalidation messaging and reordered save payloads
- regenerate forwards `regenerateCardKeys` correctly

### Browser checks and screenshots

Compose stack verification:

- `docker compose -f infra/compose/docker-compose.yml ps --format json`

Browser QA used an existing local session that already had a saved outline:

- session id: `8155bbd7-2de7-4d4c-a961-d35485225ed0`
- route verified: `http://frontend:8566/sessions/8155bbd7-2de7-4d4c-a961-d35485225ed0?stage=story_setup`

What I verified in-browser:

- the story setup stage renders the new card rail and editor panel
- each card shows purpose, linked beats, and target length
- the active editor exposes `Card purpose` and `Regenerate this card`
- clicking `Move later` on the first card surfaces the structural-change warning before save
- the layout still renders on a narrow mobile viewport

Screenshots captured:

- `/Users/kevin/code/storyteller/.artifacts/webapp-qa/prompt-54-outline-editor-desktop.png`
- `/Users/kevin/code/storyteller/.artifacts/webapp-qa/prompt-54-outline-editor-reordered.png`
- `/Users/kevin/code/storyteller/.artifacts/webapp-qa/prompt-54-outline-editor-mobile.png`

Visual verification limits:

- I did not execute a live save/regenerate mutation in the browser against the persisted local session, because that would have permanently modified existing QA session data in the shared local Postgres volume.
- Persistence for save/regenerate is instead covered by the automated backend and frontend tests above.

### LLM / prompt evaluation suite

No new LLM evaluation suite was added for this prompt.

Reason:

- this prompt did not change provider prompts, model wiring, structured-output schemas for Gemini, or intent-parser behavior
- it changed deterministic outline-editor workflow logic and UI behavior

## Wrong Turns, Dead Ends, And Gotchas

- The first obvious browser command failed because the repo does not keep its Compose file at the root; the real stack lives at `infra/compose/docker-compose.yml`.
- The `webapp-qa` skill text still references a root-level `docker-compose.yml`, so the correct invocation for this repo is `docker compose -f infra/compose/docker-compose.yml ...`.
- I initially used `pnpm` out of habit for the frontend verification step, but this repo uses `package-lock.json` and `npm`, not `pnpm`.
- Existing saved outline revisions do not have `last_change_summary` or outline edit history until they are saved again with the new code. The UI handles this by showing fallback copy instead of assuming those fields exist.

## Assumptions Made While Working Unsupervised

- I treated “light edits” as textual/editorial edits to a single card, and “significant edits” as reordering or multi-card changes. That rule is deterministic, easy to explain in the UI, and easy to extend later.
- I treated `purpose` as a new outline-card field rather than trying to overload `summary` or `drafting_brief`, because composition guidance and reviewer comprehension both benefit from a short “why this card exists” statement.
- I kept beat links and target lengths read-only in the editor. The prompt asked for structured editing and explicitly warned against turning the feature into a free-form outliner.
- I reused the existing story setup stage instead of creating a separate workflow stage, because the durable model and stage sequence already place outline planning inside story setup.

## Reviewer Notes

- The main implementation files are:
  - [story_outline_editor.py](/Users/kevin/code/storyteller/backend/app/services/story_outline_editor.py)
  - [story_tools.py](/Users/kevin/code/storyteller/backend/app/services/story_tools.py)
  - [session_hydration.py](/Users/kevin/code/storyteller/backend/app/services/session_hydration.py)
  - [StorySetupStage.tsx](/Users/kevin/code/storyteller/frontend/src/features/session/StorySetupStage.tsx)
  - [StorySetupStage.test.tsx](/Users/kevin/code/storyteller/frontend/src/features/session/StorySetupStage.test.tsx)

- The working tree after this run is coherent. The only remaining uncommitted files are Yolopilot/Codex run logs outside the implementation commit.

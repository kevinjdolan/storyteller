# Prompt 40: Genre selection API and UI

## What I changed and why

I implemented the first real workflow checkpoint for the bedtime-story studio: choosing a genre from the curated catalog, saving that choice durably, and reflecting it back into both the structured workflow UI and the session/chat history.

On the backend, I added a catalog endpoint that exposes the seeded genre list with descriptions, bedtime-safety notes, and arc notes, then added a session selection endpoint that records the chosen genre against the session. The session service now owns the real state change: it resolves the catalog entry, persists `selected_genre`, clears any incompatible tone selection, updates workflow stage status, invalidates downstream planning stages when needed, and records the resulting session event so the chat/history layer stays consistent with UI actions.

On the frontend, I replaced the placeholder genre scaffold with a real stage component that fetches the catalog, renders selectable cards, explains the bedtime guardrails, and makes the tone-stage handoff explicit. Selecting a genre now hydrates the returned backend snapshot into the runtime store, appends the returned event into chat, and previews the tone stage so the user can immediately see what comes next.

After live browser QA, I found one frontend contract bug that the mocked unit tests had not exposed: the UI was sending `genre_id`, `genre_slug`, and `genre_label` together, while the backend request model intentionally required exactly one selector. I fixed that in a follow-up commit by sending only one preferred selector per request and added a test that asserts the exact POST body.

## Architectural changes across the codebase

### Backend

- Added `GET /api/v1/catalog/genres` in [`backend/app/api/v1/routes/catalog.py`](/Users/kevin/code/storyteller/backend/app/api/v1/routes/catalog.py) and registered it from [`backend/app/api/v1/router.py`](/Users/kevin/code/storyteller/backend/app/api/v1/router.py).
- Added genre-selection request/response models in [`backend/app/models/session.py`](/Users/kevin/code/storyteller/backend/app/models/session.py) and exported them from [`backend/app/models/__init__.py`](/Users/kevin/code/storyteller/backend/app/models/__init__.py).
- Added `SessionGenreSelectionError` and `select_genre(...)` in [`backend/app/services/sessions.py`](/Users/kevin/code/storyteller/backend/app/services/sessions.py).
- Added `POST /api/v1/sessions/{session_id}/selections/genre` in [`backend/app/api/v1/routes/sessions.py`](/Users/kevin/code/storyteller/backend/app/api/v1/routes/sessions.py).

This keeps the responsibilities aligned with the existing architecture:

- route handlers stay thin
- catalog lookup and workflow mutation stay in domain services
- persistence and event recording remain backend-owned
- the frontend consumes snapshots and history events instead of inventing local workflow truth

### Frontend

- Added catalog client helpers in [`frontend/src/api/catalog.ts`](/Users/kevin/code/storyteller/frontend/src/api/catalog.ts).
- Added `useGenreCatalogQuery()` in [`frontend/src/features/session/catalogQueries.ts`](/Users/kevin/code/storyteller/frontend/src/features/session/catalogQueries.ts).
- Added the stage-specific UI in [`frontend/src/features/session/GenreSelectionStage.tsx`](/Users/kevin/code/storyteller/frontend/src/features/session/GenreSelectionStage.tsx).
- Mounted that stage component from the generic workspace shell in [`frontend/src/pages/session/SessionWorkspacePage.tsx`](/Users/kevin/code/storyteller/frontend/src/pages/session/SessionWorkspacePage.tsx).
- Added supporting card/footer styling in [`frontend/src/styles/index.css`](/Users/kevin/code/storyteller/frontend/src/styles/index.css).

This preserves the existing “generic shell + stage-specific editor” direction instead of hardcoding genre logic all through the page. The workspace still owns routing, hydration, and chat/event synchronization; the genre stage only owns rendering the catalog and initiating the selection callback.

## New abstractions, helpers, and extension points

### `GET /api/v1/catalog/genres`

This is now the backend-owned source for frontend catalog rendering.

Example:

```http
GET /api/v1/catalog/genres
```

Response shape:

```json
[
  {
    "id": "de8e8f67-289a-4555-88ee-bcae4fdc172e",
    "slug": "quest-fantasy",
    "label": "Quest Fantasy",
    "description": "A bedtime-safe adventure with a clear destination, gentle bravery, and a warm return home.",
    "bedtime_safety_notes": "Keep the journey wondrous rather than perilous...",
    "arc_notes": {
      "core_arc": "Leave a familiar safe place, face one meaningful but gentle challenge...",
      "tension_ceiling": "Low to moderate; suspense should come from uncertainty, not threat."
    },
    "sort_order": 0
  }
]
```

This endpoint is reusable for future stages that need read-only catalog data, and it avoids coupling the frontend to seed files or hardcoded constants.

### `select_genre(...)` in the session service

The service method is the extension point for future session selections that should behave like durable workflow decisions:

- resolve a catalog-backed choice
- save it to the session
- update stage status
- invalidate downstream steps when applicable
- write a history event
- return a fresh snapshot

This is the pattern to follow for the upcoming tone-selection prompt.

### `applyGenreSelection(...)` in the workspace page

The frontend helper now normalizes the request into exactly one backend selector before posting:

```ts
const requestBody =
  options.genreId != null
    ? { genre_id: options.genreId, origin: options.origin }
    : options.genreSlug != null
      ? { genre_slug: options.genreSlug, origin: options.origin }
      : { genre_label: options.genreLabel ?? null, origin: options.origin }
```

That function is also responsible for:

- hydrating the returned snapshot into the runtime store
- appending the returned event into chat
- advancing the route preview to the backend’s current stage

That keeps the “UI action -> backend truth -> chat echo -> route update” loop in one place.

### `GenreSelectionStage`

[`frontend/src/features/session/GenreSelectionStage.tsx`](/Users/kevin/code/storyteller/frontend/src/features/session/GenreSelectionStage.tsx) is a clean template for future stage implementations:

- fetch catalog/state with a dedicated query hook
- render stage-specific controls
- surface concise revision/invalidation guidance
- call back into the workspace page for durable mutations

The tone stage can follow the same pattern with a tone catalog query plus a `select_tone` callback.

## Key files touched

- [`backend/app/api/v1/routes/catalog.py`](/Users/kevin/code/storyteller/backend/app/api/v1/routes/catalog.py)
- [`backend/app/api/v1/routes/sessions.py`](/Users/kevin/code/storyteller/backend/app/api/v1/routes/sessions.py)
- [`backend/app/api/v1/router.py`](/Users/kevin/code/storyteller/backend/app/api/v1/router.py)
- [`backend/app/models/session.py`](/Users/kevin/code/storyteller/backend/app/models/session.py)
- [`backend/app/models/__init__.py`](/Users/kevin/code/storyteller/backend/app/models/__init__.py)
- [`backend/app/services/sessions.py`](/Users/kevin/code/storyteller/backend/app/services/sessions.py)
- [`backend/tests/test_session_service.py`](/Users/kevin/code/storyteller/backend/tests/test_session_service.py)
- [`backend/tests/test_session_api.py`](/Users/kevin/code/storyteller/backend/tests/test_session_api.py)
- [`frontend/src/api/catalog.ts`](/Users/kevin/code/storyteller/frontend/src/api/catalog.ts)
- [`frontend/src/features/session/catalogQueries.ts`](/Users/kevin/code/storyteller/frontend/src/features/session/catalogQueries.ts)
- [`frontend/src/features/session/GenreSelectionStage.tsx`](/Users/kevin/code/storyteller/frontend/src/features/session/GenreSelectionStage.tsx)
- [`frontend/src/pages/session/SessionWorkspacePage.tsx`](/Users/kevin/code/storyteller/frontend/src/pages/session/SessionWorkspacePage.tsx)
- [`frontend/src/pages/session/SessionWorkspacePage.test.tsx`](/Users/kevin/code/storyteller/frontend/src/pages/session/SessionWorkspacePage.test.tsx)
- [`frontend/src/styles/index.css`](/Users/kevin/code/storyteller/frontend/src/styles/index.css)

## Commits made during development

- `47f1fa4 feat(prompt-40): genre selection api and ui`
- `de4115e fix(prompt-40): send one genre selector per request`

## Exact verification work performed

### Backend verification

I ran the backend validation after implementing the catalog and selection APIs:

- `python -m pytest backend/tests/test_session_service.py backend/tests/test_session_api.py backend/tests/test_catalog.py`
  - Result: `32 passed`
- `python -m ruff check backend/app backend/tests`
  - Result: passed
- `python -m pytest backend/tests`
  - Result: `110 passed, 5 skipped`

I also formatted the touched backend files with `python -m ruff format` after the initial implementation.

### Frontend verification

I ran targeted and broader frontend verification, including a rerun after the browser-found request bug was fixed:

- `npm --prefix frontend run test -- SessionWorkspacePage`
  - Result after the final fix: `11 passed`
- `npm --prefix frontend run lint`
  - Result: passed
- `npm --prefix frontend run test`
  - Result: `14 passed (14 files), 54 passed (54 tests)`
- `npm --prefix frontend run build`
  - Result: passed
- `npx --prefix frontend prettier --write frontend/src/pages/session/SessionWorkspacePage.tsx frontend/src/pages/session/SessionWorkspacePage.test.tsx`
  - Result: no further formatting changes were needed

### Browser and visual verification

I used the repo’s browser container and Puppeteer tooling against the live local stack. The exact screenshots captured are:

- desktop before selection:
  - [`prompt-40-genre-desktop-before.png`](/Users/kevin/code/storyteller/.artifacts/webapp-qa/prompt-40-genre-desktop-before.png)
- desktop after selecting `Quest Fantasy` and moving to tone:
  - [`prompt-40-genre-desktop-after.png`](/Users/kevin/code/storyteller/.artifacts/webapp-qa/prompt-40-genre-desktop-after.png)
- mobile narrow-view genre card layout:
  - [`prompt-40-genre-mobile-before.png`](/Users/kevin/code/storyteller/.artifacts/webapp-qa/prompt-40-genre-mobile-before.png)

What I verified in the browser:

- the genre stage renders curated cards from the backend catalog
- the desktop genre screen shows the intended “tone comes next” guidance before selection
- selecting `Quest Fantasy` advances the session from `genre` to `tone`
- the tone-stage handoff is reflected in the desktop UI after selection
- the mobile layout stacks the genre card content and primary button cleanly on a `390x844` viewport

What I verified outside the browser to confirm persistence:

- I checked the live backend session for desktop QA session `912d947d-0ca5-4c5e-bc10-c14aef6929d0`
  - Result: `current_stage = tone`
  - Result: `selected_genre = Quest Fantasy`

### Local stack/runtime preparation that was required for meaningful QA

The live dev environment needed a couple of one-time fixes before browser verification was representative:

- seeded the local catalog in the live backend with `docker exec storyteller-backend-override python -m app.seed_catalog`
- applied pending local migrations with:

```bash
cd backend
STORYTELLER_DATABASE_URL='postgresql+psycopg://storyteller:storyteller@127.0.0.1:8567/storyteller' python -m alembic upgrade head
```

Without those steps, the live catalog was empty and session creation was failing against an out-of-date local Postgres volume.

## LLM and prompt evaluation suite

I did not add or modify any LLM prompts, model wiring, or eval suites in this prompt. There is therefore no new LLM-specific evaluation matrix to report for this task.

## Wrong turns, dead ends, surprising behavior, and gotchas

### 1. The live backend serving traffic was not the compose `backend` container

`docker ps` showed that `storyteller-backend-override` was the container actually bound to port `8565`, while the nominal compose backend service was exited. For QA, I treated `storyteller-backend-override` as the active backend because that was the process the frontend and the host were really talking to.

### 2. The local Postgres volume was behind the latest migration

Live session creation initially failed because the DB was missing `session_memory_snapshots`. The fix was to apply the outstanding Alembic migration against the local Postgres volume before relying on browser QA.

### 3. The live catalog was empty until seeded

The API and tests were correct, but the running local environment had not yet been seeded, so the catalog endpoint returned an empty list until I ran `python -m app.seed_catalog` in the active backend container.

### 4. Browser QA exposed a real contract bug the mocked tests missed

The first desktop click attempt produced a `422 Unprocessable Entity` from the backend. That turned out to be a genuine frontend bug: the UI sent all three selectors (`genre_id`, `genre_slug`, and `genre_label`) together, while the backend model intentionally required exactly one. I fixed the frontend request builder and then added a test assertion on the exact POST payload so the regression is now covered.

### 5. The generic JSON QA runner’s selector click was not reliable enough for this card interaction

The repo’s `tools/webapp-qa` runner was useful for the baseline screenshots and text assertions, but its selector-only click step did not reliably trigger the desired genre card button in this flow. I switched the desktop transition check to a task-specific Puppeteer script that targeted the `Quest Fantasy` card by rendered text. The browser evidence is still from the same browser container and same live app; the only change was the navigation/click mechanism.

### 6. Repo-wide formatter checks were noisy for unrelated pre-existing files

`ruff format --check` across the full backend tree would have reported unrelated existing files, so I limited formatting to the files touched by this task rather than introducing broad repository churn.

### 7. Mobile screenshots needed explicit scroll targeting

The first mobile capture only showed the workspace header area. I took a follow-up narrow-view screenshot centered on the genre cards so the responsive evidence actually included the stage content and CTA layout.

## Assumptions I made while working unsupervised

- The seeded database catalog is the intended runtime source of truth for genres, even though seed data originates from research docs and local setup commands.
- It was acceptable to migrate the local Postgres volume and seed the catalog automatically because this was necessary to make the repository’s own live dev stack usable for verification.
- It was acceptable to use the active `storyteller-backend-override` container for QA because it was the process actually serving `http://127.0.0.1:8565`.
- Temporary QA specs/scripts under `.artifacts/webapp-qa/` are disposable verification assets and intentionally not part of the tracked source tree.

## Reviewer notes

The main implementation landed in the first commit, but the live browser pass found an important follow-up fix that is worth reviewing explicitly: [`frontend/src/pages/session/SessionWorkspacePage.tsx`](/Users/kevin/code/storyteller/frontend/src/pages/session/SessionWorkspacePage.tsx) now normalizes genre-selection requests down to a single selector field, and [`frontend/src/pages/session/SessionWorkspacePage.test.tsx`](/Users/kevin/code/storyteller/frontend/src/pages/session/SessionWorkspacePage.test.tsx) now asserts that exact request shape. That second change is the one that made the browser flow line up with the backend contract.

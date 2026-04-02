# Prompt 20 Summary: Frontend App Shell and Routing

## What I changed and why

I replaced the single placeholder route with a real app-shell + router structure that can carry the sessions-first product forward without repainting the frontend again in the next few prompts.

The main user-facing changes are:

- Added explicit routes for:
  - `/` as the sessions-first home screen
  - `/sessions/:sessionId` as the route-scoped workspace shell
  - `*` as a not-found fallback
- Reworked the top-level shell so it now has:
  - primary navigation
  - a persistent backend connection indicator
  - a dedicated toast/notification dock placeholder
  - a main content outlet for routed pages
- Replaced the old single-page scaffold content with:
  - `HomePage` for the home route
  - `SessionWorkspacePage` for the session workspace shell
  - `NotFoundPage` for unmatched paths
- Split frontend concerns into clearer folders for `app`, `pages`, `shared/ui`, `hooks`, `api`, and `state`.

The goal was to satisfy prompt 20 without jumping ahead into the full workflow UI. The workspace page is intentionally a shell, not a finished feature, but it now proves that the session route accepts and displays a session ID and that the app has the chrome needed for future navigation and global status surfaces.

## Architectural changes across the codebase

### 1. Routing is now a first-class app concern

I introduced route configuration that is reusable in both the production app and memory-router tests:

- `frontend/src/app/router.tsx`
- `frontend/src/app/routePaths.ts`

`routePaths.ts` centralizes route strings and exposes `buildSessionWorkspacePath(sessionId)` so future UI links do not hardcode `/sessions/...` all over the app.

### 2. Route modules now live under `src/pages/`

I moved route-level UI out of `features/home` into page-oriented modules:

- `frontend/src/pages/home/HomePage.tsx`
- `frontend/src/pages/session/SessionWorkspacePage.tsx`
- `frontend/src/pages/not-found/NotFoundPage.tsx`

This keeps route screens distinct from reusable product/domain logic in `src/features/`.

### 3. Shared shell primitives were pulled out of route pages

I introduced reusable shell-level UI primitives:

- `frontend/src/shared/ui/ConnectionStatusBadge.tsx`
- `frontend/src/shared/ui/ToastRegion.tsx`

That keeps route pages focused on page content instead of global chrome details.

### 4. API access and hooks were separated from page rendering

The old `shared/api.ts` helper became a more explicit API layer:

- `frontend/src/api/client.ts`
- `frontend/src/api/system.ts`

The backend status hook now lives in:

- `frontend/src/hooks/useBackendStatus.ts`

That gives later prompts a cleaner place to add endpoint clients and data hooks without hiding fetch logic inside page components.

### 5. A shell-level state landing zone now exists

I added:

- `frontend/src/state/appShellStore.ts`

This is intentionally small for now, but it gives the shell a typed place to grow toast/global UI state without forcing that structure to emerge ad hoc inside `AppShell`.

### 6. Styling was expanded to support the shell, not just one card

`frontend/src/styles/index.css` now covers:

- shell frame layout
- nav styling
- utility rail styling
- home page grid
- session workspace two-pane shell
- not-found page
- responsive behavior for desktop/tablet/mobile

I kept the existing warm editorial visual direction rather than replacing it with a generic dashboard theme.

### 7. Browser QA is now reproducible for these routes

I added route smoke specs under:

- `tools/webapp-qa/examples/prompt-20-home-route.spec.json`
- `tools/webapp-qa/examples/prompt-20-session-route.spec.json`
- `tools/webapp-qa/examples/prompt-20-not-found-route.spec.json`

These assert route-specific text and generate screenshots for future regression checks.

## New abstractions and extension points

### Route helper example

Use the centralized path builder instead of hardcoding session URLs:

```tsx
import { buildSessionWorkspacePath } from '../../app/routePaths.ts'

<Link to={buildSessionWorkspacePath(sessionId)}>Resume session</Link>
```

### Adding a new routed page

The expected pattern now is:

1. Create a page under `frontend/src/pages/<feature>/`.
2. Add the route entry in `frontend/src/app/router.tsx`.
3. Add any reusable UI to `frontend/src/shared/ui/`.
4. Add data hooks to `frontend/src/hooks/`.
5. Add endpoint helpers to `frontend/src/api/`.

### Reusing the route config in tests

The new router tests use `appRoutes` directly:

```tsx
const router = createMemoryRouter(appRoutes, {
  initialEntries: ['/sessions/moonlit-harbor'],
})
```

That keeps route behavior testable without special test-only route copies.

### Shell-level global UI

`AppShell` now owns:

- navigation
- connection status
- toast dock
- the routed content outlet

That gives later prompts a stable place to add:

- websocket connection status
- toasts from background jobs
- global providers
- future app-wide navigation

## Files touched

Primary implementation files:

- `frontend/src/app/AppShell.tsx`
- `frontend/src/app/router.tsx`
- `frontend/src/app/routePaths.ts`
- `frontend/src/pages/home/HomePage.tsx`
- `frontend/src/pages/session/SessionWorkspacePage.tsx`
- `frontend/src/pages/not-found/NotFoundPage.tsx`
- `frontend/src/hooks/useBackendStatus.ts`
- `frontend/src/api/client.ts`
- `frontend/src/api/system.ts`
- `frontend/src/shared/ui/ConnectionStatusBadge.tsx`
- `frontend/src/shared/ui/ToastRegion.tsx`
- `frontend/src/state/appShellStore.ts`
- `frontend/src/styles/index.css`
- `frontend/README.md`

Test and QA files:

- `frontend/src/app/router.test.tsx`
- `frontend/src/pages/home/HomePage.test.tsx`
- `tools/webapp-qa/examples/prompt-20-home-route.spec.json`
- `tools/webapp-qa/examples/prompt-20-session-route.spec.json`
- `tools/webapp-qa/examples/prompt-20-not-found-route.spec.json`

Removed/replaced older scaffold files:

- `frontend/src/features/home/HomeRoute.tsx`
- `frontend/src/features/home/HomeRoute.test.tsx`
- `frontend/src/shared/api.ts`

The backend status hook was moved from `features/system` to `hooks/`.

## Exact verification performed

### Frontend automated checks

Ran from `frontend/`:

- `npm run test`
  - Result: pass
  - Vitest summary: `3` test files passed, `7` tests passed
- `npm run lint`
  - Result: pass
- `npm run format:check`
  - Result: failed initially on 6 files after the refactor
- `npm run format`
  - Result: pass
- `npm run format:check`
  - Result: pass after formatting
- `npm run build`
  - Result: pass

The final verified frontend state is the formatted state that was committed in `eb6fd69`.

### Browser and screenshot verification

Ran from `tools/webapp-qa/`:

- `npm run check -- --spec ./examples/prompt-20-home-route.spec.json`
  - Result: pass
  - Screenshot: `.artifacts/webapp-qa/prompt-20-home-route.png`
- `npm run check -- --spec ./examples/prompt-20-session-route.spec.json`
  - Result: pass
  - Screenshot: `.artifacts/webapp-qa/prompt-20-session-route.png`
- `npm run check -- --spec ./examples/prompt-20-not-found-route.spec.json`
  - Result: pass
  - Screenshot: `.artifacts/webapp-qa/prompt-20-not-found-route.png`

What those browser checks validated:

- the home route renders the new shell and sessions-first home content
- the workspace route accepts a real `sessionId` in the URL and renders route-scoped content
- the not-found fallback renders for unmatched routes
- screenshots were successfully captured for all three states

### Visual verification limits

- The browser checks were run against the live frontend at `http://localhost:8566`.
- The backend was not healthy during browser QA, so the connection indicator exercised the offline fallback instead of the online state.
- That did not block prompt 20 acceptance because the routing and shell behavior still rendered correctly, and the shell is explicitly designed to degrade when backend connectivity is unavailable.

## LLM or prompt evaluation suite

No LLM-facing behavior, prompts, model wiring, or agent logic changed in this task.

Evaluation suite status:

- `LLM eval suite added`: No
- `Reason`: prompt 20 was limited to frontend shell structure, routes, and layout primitives

## Wrong turns, dead ends, and repo gotchas

### 1. Parallel browser QA through Compose failed

I first tried to run the new browser QA specs in parallel through:

- `docker compose -f infra/compose/docker-compose.yml run --rm browser ...`

That was a bad fit for this repo because Compose tried to recreate the `backend` dependency for each run, and the runs collided on container naming.

### 2. The long-lived Compose browser path was also blocked

I then tried `docker compose ... up -d browser`, but that still followed the frontend dependency chain back to `backend`, which failed health startup.

### 3. Host-side Puppeteer runner initially failed

The host QA runner existed, but `tools/webapp-qa/node_modules` was empty on this machine, so `npm run check` initially failed with `ERR_MODULE_NOT_FOUND` for `puppeteer`.

I resolved that by running:

- `cd tools/webapp-qa && npm install`

That used the already-declared dependency set; no dependency files needed to change.

### 4. Browser spec paths were initially container-specific

The first version of the specs wrote screenshots to `/workspace/...`, which only works inside the Compose browser container. I changed those to repo-relative paths so the same specs could run from the host.

### 5. Local backend config is currently broken in this repo state

During browser QA, the backend emitted:

- `Storyteller configuration is invalid.`
- extra input errors for `gemini.api_key_name`
- extra input errors for `gemini.project_name`
- extra input errors for `gemini.project_number`
- extra input errors for `openai`

That appears to come from the local secrets/config shape, not from prompt 20. I did not change backend config handling here because it is outside this task, but it is important context for anyone rerunning browser checks.

## Assumptions made while working unsupervised

- I assumed prompt 20 should establish the routing and shell contract without implementing the full workflow UI.
- I assumed the current visual language should be preserved and extended rather than replaced.
- I assumed route helpers and page-folder conventions were more valuable now than keeping the old `features/home` placeholder shape.
- I assumed the header should expose a sample workspace link even though the real session list/data layer for the frontend is not built yet.
- I assumed backend availability should not be a hard prerequisite for accepting this prompt because the shell already supports offline rendering and the prompt focuses on routing/layout structure.

## Final repository state for this task

- Code checkpoint commit created: `eb6fd69` (`feat(prompt-20): frontend app shell and routing`)
- Required prompt-20 summary file written here
- Remaining uncommitted files in the worktree are unrelated prompt-log artifacts outside this task

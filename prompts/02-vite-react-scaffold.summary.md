# 02 Vite React Scaffold Summary

## What I changed and why

I replaced the placeholder JSX frontend with a real Vite React TypeScript foundation and kept the repo aligned with the product direction from `base_prompt.md`: Storyteller should be a sessions-first bedtime-story studio, not a generic demo page.

The main implementation changes were:

- I upgraded `frontend/` from the ad hoc React 18 JSX scaffold to the current Vite React TypeScript baseline.
  - `package.json` now uses a modern Vite/React/TypeScript toolchain.
  - `tsconfig.json`, `tsconfig.app.json`, `tsconfig.node.json`, and `vite.config.ts` were added so TypeScript strictness is real rather than aspirational.
  - The legacy `src/App.jsx`, `src/main.jsx`, `src/styles.css`, and `vite.config.js` files were removed.

- I introduced a minimal but production-minded app shape instead of leaving everything in one component.
  - `src/main.tsx` is now the browser entrypoint.
  - `src/app/App.tsx` mounts the router provider.
  - `src/app/router.tsx` defines the initial route tree.
  - `src/app/AppShell.tsx` provides the top-level shell for future routes.
  - `src/features/home/HomeRoute.tsx` is the branded placeholder route.

- I replaced the Vite-style demo experience with a Storyteller-branded landing route.
  - The page now communicates “past sessions come first”.
  - The route previews the intended workflow stages without pretending the real product flow exists yet.
  - The visual language is intentionally calmer and more product-specific than the generic template.

- I kept the existing backend hello-check, but made it safe for frontend-only development.
  - `src/shared/api.ts` centralizes browser-side API URL resolution.
  - `src/features/system/useBackendStatus.ts` checks `/api/hello`, surfaces backend status in the UI, and falls back cleanly to “frontend-only mode” when the backend is down.
  - This preserves the prompt-01 stack integration while satisfying prompt-02’s acceptance check that `npm run dev` should work in isolation.

- I added frontend quality tooling instead of leaving the scaffold unguarded.
  - ESLint via `frontend/eslint.config.js`
  - Prettier via `.prettierrc.json` and `.prettierignore`
  - Vitest + Testing Library via `frontend/vitest.config.ts` and `src/test/setup.ts`
  - `package.json` scripts now include `dev`, `build`, `lint`, `preview`, `format`, `format:check`, and `test`

- I updated supporting files so the scaffold is coherent across the repo.
  - `frontend/Dockerfile` now uses `npm ci`
  - `frontend/README.md` documents the new structure and scripts
  - `frontend/index.html` now references `main.tsx`, has a project description, and includes a branded favicon
  - `tools/webapp-qa/examples/homepage.spec.json` now asserts Storyteller-specific copy instead of the old “Hello, world!”
  - `README.md` and `docs/architecture-overview.md` now describe the frontend as a TypeScript foundation rather than a future plan

I created one checkpoint commit during the run:

- `1306829` — `feat(prompt-02): vite react scaffold`

## Architectural changes across the codebase

The biggest architectural shift is that the frontend now has an explicit app shape instead of a single-file demo.

### Frontend composition now has clear layers

- Entry: `src/main.tsx`
- App root: `src/app/App.tsx`
- Routing: `src/app/router.tsx`
- Shared chrome: `src/app/AppShell.tsx`
- Feature route: `src/features/home/HomeRoute.tsx`
- Shared client helper: `src/shared/api.ts`
- Feature hook for backend state: `src/features/system/useBackendStatus.ts`

This matters because later prompts can now add routes and feature modules without immediately refactoring the scaffold again.

### API URL handling is centralized

Previously the frontend built fetch URLs inline. Now `src/shared/api.ts` owns browser-side URL resolution. That gives later work one place to evolve if the frontend ever needs a different API base path in local development, preview, or production.

### The backend handshake is isolated behind a hook

`useBackendStatus()` contains the hello-check and the fallback behavior. The home route only renders the view model that the hook returns. That separation keeps network behavior out of the route markup and gives later prompts a clear pattern for other backend-backed status cards.

### Tooling is now part of the scaffold, not deferred work

Prompt 02 asked for a “small, reliable developer setup”, so I treated linting, formatting, strict TypeScript config, and at least one real test as part of the scaffold itself rather than a later cleanup prompt.

## Examples of how to use the new abstractions, helpers, and extension points

### Add a new route

The current router is intentionally small. To add another route later, extend `src/app/router.tsx`:

```tsx
import { createBrowserRouter } from 'react-router-dom'
import { AppShell } from './AppShell.tsx'
import { HomeRoute } from '../features/home/HomeRoute.tsx'
import { SessionsRoute } from '../features/sessions/SessionsRoute.tsx'

export const router = createBrowserRouter([
  {
    path: '/',
    element: <AppShell />,
    children: [
      { index: true, element: <HomeRoute /> },
      { path: 'sessions/:sessionId', element: <SessionsRoute /> },
    ],
  },
])
```

The important part is that the future route stays under `AppShell`, so shared layout/chrome does not need to be recreated per page.

### Build frontend API URLs without hardcoding origins

Use `resolveApiUrl()` from `src/shared/api.ts` instead of concatenating strings inline:

```ts
import { resolveApiUrl } from '../shared/api.ts'

const response = await fetch(resolveApiUrl('/api/hello'))
```

That preserves the current “same-origin unless `VITE_API_URL` is explicitly set” behavior.

### Reuse the backend status pattern

Future features that need a lightweight backend health/status check can follow the same pattern as `useBackendStatus()`:

```ts
const status = useBackendStatus()

if (status.state === 'offline') {
  // Render a non-blocking fallback instead of crashing the route.
}
```

The key idea is that the route renders cleanly even if the backend is missing, which keeps frontend-only development viable.

## Exact verification work I performed

I verified this prompt both host-side and through the Docker Compose/browser QA path the repo already uses.

### Dependency installation

I ran:

```bash
cd frontend
npm install
```

Result:

- Passed.
- Generated `frontend/package-lock.json`.
- Resolved current frontend dependencies successfully with no reported vulnerabilities.

### Formatting

I ran:

```bash
cd frontend
npm run format
npm run format:check
```

Results:

- `npm run format` passed and normalized the new files.
- `npm run format:check` passed with `All matched files use Prettier code style!`.

### Linting

I ran:

```bash
cd frontend
npm run lint
```

Result:

- Passed.

### Unit tests

I added and ran:

```bash
cd frontend
npm run test
```

Results:

- Passed.
- Test file: `src/features/home/HomeRoute.test.tsx`
- Assertions covered:
  - branded scaffold rendering
  - presence of the sessions-first copy
  - healthy backend status flow
  - frontend-only fallback when the backend is unavailable

Measured outcomes:

- `HomeRoute renders the branded scaffold and reports a healthy backend` — passed
- `HomeRoute falls back to frontend-only mode when the backend is unavailable` — passed

### TypeScript and production build

I ran:

```bash
cd frontend
npm run build
```

Result after fixes:

- Passed.
- Final production output reported:
  - `dist/index.html` `0.61 kB`
  - `dist/assets/index-Dz3Oao9U.css` `5.08 kB`
  - `dist/assets/index-jDEg6uWK.js` `286.94 kB`

### Isolation check with the normal Vite dev command

I ran:

```bash
cd frontend
npm run dev
curl -fsS http://127.0.0.1:8566 | sed -n '1,80p'
curl -fsS http://127.0.0.1:8566/src/features/home/HomeRoute.tsx >/dev/null && echo 'dev_server_serving_modules=yes'
```

Results:

- `npm run dev` started successfully on `http://localhost:8566/`.
- The served HTML referenced `/src/main.tsx`, which confirmed the TypeScript entrypoint was active.
- `dev_server_serving_modules=yes` confirmed the Vite dev server was serving the new module graph.
- I intentionally ran this before starting the backend to confirm the frontend still boots in isolation.

### Docker Compose runtime verification

Using the repo’s existing Compose wrapper, I ran:

```bash
./scripts/dev-compose.sh up -d --build
./scripts/dev-compose.sh ps
curl -fsS http://127.0.0.1:8565/api/hello
curl -fsS http://127.0.0.1:8566 | sed -n '1,80p'
```

Results:

- Passed.
- `backend`, `frontend`, and `browser` all built and started successfully.
- `backend` and `frontend` both reached healthy status.
- `GET /api/hello` returned `{"message":"Hello from FastAPI!"}`.
- The frontend served the expected Vite HTML shell with the Storyteller title and updated metadata.

### Browser-based verification and screenshot

Using the `webapp-qa` flow, I ran:

```bash
./scripts/dev-compose.sh run --rm browser npm run check -- --spec ./examples/homepage.spec.json
```

Results:

- Passed.
- Assertions verified:
  - `[data-testid='app-card']` rendered
  - `Storyteller` text rendered
  - `Past sessions come first` text rendered
  - `Hello from FastAPI!` rendered in the browser
- Screenshot written to:
  - `.artifacts/webapp-qa/homepage.png`
- I also confirmed the generated screenshot file exists and is the expected size:

```bash
file .artifacts/webapp-qa/homepage.png
```

Output:

- `PNG image data, 1440 x 1248, 8-bit/color RGB, non-interlaced`

Limit of visual verification:

- I generated the screenshot and validated the browser assertions around the rendered UI, but I did not do manual pixel-by-pixel review or visual diffing beyond that captured smoke evidence.

### Patch hygiene

I ran:

```bash
git diff --check -- README.md docs/architecture-overview.md frontend tools/webapp-qa/examples/homepage.spec.json
```

Result:

- Passed with no whitespace or patch-format issues.

### Cleanup

I ran:

```bash
./scripts/dev-compose.sh down
```

Result:

- Passed.
- The local stack was shut down cleanly after verification.

## Evaluation suite for LLM or prompt-related work

No LLM-, prompt-, or model-wiring logic changed in this prompt, so I did not add an LLM evaluation suite.

Evaluation status:

- `LLM-facing logic changed` — no
- `LLM eval suite required` — no
- `LLM eval criteria` — not applicable

## Wrong turns, dead ends, surprising behavior, and gotchas

- The first production build failed because I initially used the `fallbackElement` prop on `RouterProvider`, which is not available on the installed `react-router-dom` v7 API surface. I removed that prop and reran the build successfully.

- The first test run failed even though the component logic was basically correct. The issue was that this Vitest/RTL setup was not automatically cleaning the DOM between tests, so the second test saw duplicate `data-testid="backend-state"` nodes from the first render. I fixed that by adding explicit `cleanup()` in `src/test/setup.ts`.

- My first pass at `useBackendStatus()` used an `AbortController` in the effect cleanup. That is usually fine, but in React Strict Mode during development it produced an avoidable aborted `/api/hello` request in the browser QA logs. I switched the hook to an `isCurrent` guard instead, which preserved safe cleanup behavior without noisy request-abort logs.

- The first browser smoke run also showed a missing favicon 404. I added `frontend/public/favicon.svg` and referenced it from `index.html` so the scaffold is branded and the dev console stays cleaner.

- `npm create vite@latest /tmp/storyteller-vite-template -- --template react-ts` unexpectedly created the template under the repository’s `tmp/` directory rather than the system `/tmp/` I intended. I used it only as reference material, then removed that generated directory before committing.

- The frontend Docker build context is still fairly large because the repo is mounted and copied as-is into the image context. That did not block this prompt, but it is worth remembering for future prompts if Docker build times start growing.

## Assumptions I made while working unsupervised

- I assumed adding `react-router-dom` now was the right interpretation of “set up a minimal component structure, route shell, app entry point” rather than waiting for the later routing prompt. I kept that addition intentionally small: one shell, one route, no deeper route architecture yet.

- I assumed the placeholder landing screen should already reflect the product contract that “past sessions” is the first meaningful screen, even though real session data is not in scope yet. I therefore used static preview content rather than a generic marketing hero or a raw empty shell.

- I assumed the existing `/api/hello` endpoint was still useful as a lightweight integration proof for prompt 02, but that it should not be allowed to block standalone frontend development. That assumption drove the offline fallback behavior.

- I assumed staying on `node:20-alpine` in `frontend/Dockerfile` was acceptable for the current Vite version as long as the actual Compose build proved it in this environment. The Compose build passed, so I did not force a Node image bump.

- I assumed prompt-runner metadata files such as `prompts/*.yolopilot.*` and `prompts/*.codex.*` were not part of the requested code change and should be left untouched.

## Remaining limits and follow-up considerations

- The home route is still a static placeholder. It does not yet read sessions, call real frontend APIs beyond `/api/hello`, or implement the two-pane workspace.

- There is only one unit test file so far. That is appropriate for the current scaffold stage, but future prompts should expand test coverage as real routing, state, and API clients appear.

- The browser QA currently verifies copy and screenshot capture, not deeper interaction flows. That is enough for prompt 02, but later UI prompts should extend the Puppeteer specs as the product gains real controls and state transitions.

# Prompt 23 Summary

## What I changed and why

I introduced a predictable frontend state split for sessions:

- Durable backend-owned session data now goes through React Query instead of
  page-local `useEffect` fetch logic.
- Workspace-only transient state now lives in a small per-session external store
  that tracks pending UI actions and buffered live events without duplicating
  the session snapshot.
- The workspace route now has a dedicated provider layer so future child
  components can read session state through hooks instead of prop-drilling.

The immediate goal was to make the current home screen and workspace routes more
boring and predictable while setting up the shape needed for realtime updates
and optimistic UI later.

## Architectural changes across the codebase

### App-level data foundation

- Added `frontend/src/app/queryClient.ts` to create the shared React Query
  client.
- Added `frontend/src/app/AppProviders.tsx` and wrapped the router in
  `frontend/src/app/App.tsx`.
- Chose `@tanstack/react-query` as the server-state tool and added it to
  `frontend/package.json` and `frontend/package-lock.json`.

Important detail: query retries are set to `0` so the app preserves the explicit
loading, error, and retry UX that already existed on these screens.

### Session server-state hooks

- Added `frontend/src/features/session/sessionQueries.ts`.
- Centralized session query keys for list/detail cache entries.
- Added thin hooks:
  - `useRecentSessionsQuery(limit?)`
  - `useSessionSnapshotQuery(sessionId)`
  - `useCreateSessionMutation()`

This moved the home screen and workspace snapshot fetching out of ad hoc
component effects and into a shared cacheable layer.

### Session runtime store

- Added `frontend/src/features/session/sessionRuntimeStore.ts`.
- Modeled three concerns separately:
  - server snapshot: React Query cache
  - pending UI actions: local store
  - live event stream bookkeeping: local store

The runtime store currently supports:

- enqueueing optimistic/pending actions
- resolving or removing pending actions
- appending buffered live events
- tracking connection state (`idle`, `connecting`, `open`, etc.)
- resetting runtime state when the provider remounts for another session

The store also reconciles a pending action to `confirmed` when an incoming live
event carries the same `correlationId`.

### Workspace-scoped access layer

- Added `frontend/src/features/session/SessionWorkspaceProvider.tsx`.
- Added `frontend/src/features/session/sessionWorkspaceContext.ts`.

The provider owns the runtime store instance for the current session, and the
hooks expose:

- `useCurrentSessionSnapshotQuery()`
- `useSessionPendingActions()`
- `useSessionEventStream()`
- `useSessionRuntimeActions()`

This is the main anti-prop-drilling piece for prompt 23.

### Route migrations

#### Home page

`frontend/src/pages/home/HomePage.tsx` now:

- uses `useRecentSessionsQuery()` for the sessions list
- uses `useCreateSessionMutation()` for session creation
- derives loading/error/ready UI from React Query state instead of a custom
  `useEffect` loader

#### Workspace page

`frontend/src/pages/session/SessionWorkspacePage.tsx` now:

- wraps the route in `SessionWorkspaceProvider`
- loads the snapshot through `useCurrentSessionSnapshotQuery()`
- reads transient runtime state from the workspace context hooks
- shows a minimal runtime status surface in the chat lane:
  - live feed status
  - pending UI action count
  - buffered live event count

That UI is intentionally modest, but it proves the new state layer is wired and
ready for realtime prompts later.

### Documentation and test support

- Added `docs/frontend-state-architecture.md` as the short architecture note for
  this prompt.
- Updated `frontend/README.md` so the new provider/query/store files are
  discoverable.
- Added `frontend/src/test/renderWithAppProviders.tsx` so component tests render
  under the same query provider used by the app.

## Examples and extension points

### Home-screen list hook

```tsx
const recentSessionsQuery = useRecentSessionsQuery()
const sessions = recentSessionsQuery.data ?? []
```

### Workspace provider

```tsx
<SessionWorkspaceProvider sessionId={sessionId}>
  <SessionWorkspaceContent sessionId={sessionId} />
</SessionWorkspaceProvider>
```

### Reading server snapshot and runtime state together

```tsx
const snapshotQuery = useCurrentSessionSnapshotQuery()
const pendingActions = useSessionPendingActions()
const eventStream = useSessionEventStream()
```

### Future optimistic action workflow

```tsx
const runtime = useSessionRuntimeActions()

runtime.enqueuePendingAction({
  id: 'action-1',
  label: 'Accepted revised beat sheet',
  origin: 'ui',
  createdAt: new Date().toISOString(),
  correlationId: 'mutation-7',
})
```

Later websocket work can call `appendLiveEvent()` with the matching
`correlationId` to confirm that action without mutating the backend snapshot
shape directly.

## Verification performed

### Automated tests

Ran from `frontend/`:

- `npm test`
- Result: `5` test files passed, `15` tests passed

Added coverage for the new runtime store in
`frontend/src/features/session/sessionRuntimeStore.test.ts`.

### Lint and build

Ran from `frontend/`:

- `npm run lint`
- Result: passed
- `npm run build`
- Result: passed

### Browser and visual verification

Used the repo’s `webapp-qa` skill flow with Docker Compose and the Puppeteer
runner.

Commands used:

- `docker compose -f infra/compose/docker-compose.yml up -d --build`
- `curl -sS -X POST http://localhost:8565/api/v1/sessions -H 'Content-Type: application/json' -d '{"working_title":"Prompt 23 QA Session"}'`
- `docker compose -f infra/compose/docker-compose.yml run --rm browser npm run check -- --spec /workspace/.artifacts/webapp-qa/specs/prompt-23-home.spec.json`
- `docker compose -f infra/compose/docker-compose.yml run --rm browser npm run check -- --spec /workspace/.artifacts/webapp-qa/specs/prompt-23-workspace.spec.json`

Browser checks confirmed:

- the home route still renders and loads backend-backed session data
- the workspace route still hydrates the selected session snapshot
- the new runtime status copy renders in the workspace (`Live feed idle` and
  `0 pending UI actions / 0 buffered live events.`)

Screenshots captured:

- `.artifacts/webapp-qa/prompt-23-home.png`
- `.artifacts/webapp-qa/prompt-23-workspace.png`

### Remaining verification limits

- The browser specs were created under `.artifacts/` for this run and are not
  committed as source fixtures.
- I verified the new state foundation visually against one real draft session,
  not against future websocket traffic, because prompt 29 has not been built
  yet.

## LLM or prompt evaluation suite

No LLM-facing prompts, model wiring, eval logic, or agent behavior changed in
this task.

- Evaluation suite added: none
- Criteria: not applicable

## Wrong turns, dead ends, and gotchas

### 1. Provider implementation had to change after linting

My first workspace-provider version used a ref-backed store instance and
exported both the provider and hooks from the same `.tsx` file.

That hit two repo/tooling constraints:

- `react-hooks/refs` rejected reading `ref.current` during render
- `react-refresh/only-export-components` rejected exporting non-component hooks
  from the provider file

I fixed that by:

- switching the provider to `useState(createSessionRuntimeStore)`
- splitting the hook/context logic into `sessionWorkspaceContext.ts`

### 2. Query retries briefly changed the error UX

React Query’s retry behavior caused existing tests to skip straight past the
error screens. I set query retry count to `0` in the shared query client so the
app’s explicit Retry buttons remain the source of truth for these routes.

### 3. Docker Compose frontend did not pick up the new dependency automatically

The compose frontend service uses a persistent `frontend_node_modules` volume.
After adding React Query on the host, the container still served a dev build
without the dependency until I ran:

- `docker compose -f infra/compose/docker-compose.yml exec frontend npm install`
- `docker compose -f infra/compose/docker-compose.yml restart frontend`

This was a dev-stack/runtime gotcha, not a source-code problem.

### 4. Local `secrets.yaml` format blocked backend startup

The existing ignored `secrets.yaml` on this machine contains keys that the
current backend settings model now rejects. That caused `backend` in compose to
fail before frontend proxy verification.

To complete browser QA without changing tracked code or normalizing secrets in
this prompt, I temporarily:

- backed up the ignored `secrets.yaml`
- replaced it with a minimal supported shape containing only `gemini.api_key`
- started the compose stack and ran browser checks
- restored the original ignored `secrets.yaml` afterward

That workaround was local-only and was not committed.

## Assumptions made while working unsupervised

- Adding `@tanstack/react-query` was acceptable for prompt 23 because the task
  explicitly asked for a frontend data tool such as React Query.
- A custom external store was preferable to adding a second state dependency
  because the required transient state is still small and session-scoped.
- Keeping the new runtime UI surface intentionally small was the right tradeoff
  for this prompt: enough to prove the state split works, without inventing
  unreleased realtime behavior.
- Preserving the existing home/workspace UX and error states was more important
  than enabling automatic query retries.

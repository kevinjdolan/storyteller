# Frontend State Architecture

Prompt 23 introduces a small but explicit split between durable backend data and
session-local runtime state.

## State Layers

1. Server snapshots and lists live in React Query.
   - `frontend/src/features/session/sessionQueries.ts`
   - Home page lists use `useRecentSessionsQuery()`.
   - Workspace snapshots use `useSessionSnapshotQuery(sessionId)`.
2. Session-local runtime state lives in a tiny external store.
   - `frontend/src/features/session/sessionRuntimeStore.ts`
   - This tracks pending UI actions and the buffered live-event stream without
     copying the backend snapshot into local state.
3. Workspace access is scoped through a provider.
   - `frontend/src/features/session/SessionWorkspaceProvider.tsx`
   - Child components can read the current session query and runtime state with
     hooks instead of threading snapshot props down the tree.

## Why This Split

- React Query owns cache invalidation, request status, and future background
  refresh for backend snapshots.
- The local runtime store keeps websocket/event-stream concerns separate from
  durable session data.
- Optimistic UI state can be reconciled later through `correlationId` without
  mutating or duplicating the session snapshot shape.

## Usage

Home screen server data:

```tsx
const recentSessionsQuery = useRecentSessionsQuery()
const sessions = recentSessionsQuery.data ?? []
```

Workspace server snapshot plus runtime state:

```tsx
<SessionWorkspaceProvider sessionId={sessionId}>
  <SessionWorkspaceContent />
</SessionWorkspaceProvider>
```

```tsx
const snapshotQuery = useCurrentSessionSnapshotQuery()
const pendingActions = useSessionPendingActions()
const eventStream = useSessionEventStream()
```

Runtime-only updates for future realtime work:

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

When the server later emits a matching live event, `appendLiveEvent()` can mark
that optimistic action as confirmed by `correlationId`.

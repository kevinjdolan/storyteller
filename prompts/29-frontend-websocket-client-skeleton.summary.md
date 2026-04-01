# Prompt 29 Summary: Frontend WebSocket Client Skeleton

## What I changed and why

I added a frontend live-update skeleton that lets the workspace own a single session-scoped feed connection instead of having presentation components open sockets independently.

The main goal was to make prompt 29 real without pretending the backend transport already exists. The result is:

- A typed realtime contract layer in `frontend/src/features/session/live/sessionRealtime.ts` that mirrors the prompt 17 session-feed shapes: subscribe ack, `chat.message`, `workflow.stage_changed`, `ui.action_echo`, `composition.chunk`, `job.progress`, `job.status`, and `error.notification`.
- A reconnecting WebSocket client in `frontend/src/features/session/live/sessionRealtimeClient.ts` that:
  - opens one connection per workspace session,
  - sends a session subscription frame with the last durable sequence number,
  - parses and dispatches typed feed messages,
  - exposes connection health updates,
  - stays idle unless `VITE_SESSION_EVENTS_WS_URL` is configured.
- A runtime-store upgrade in `frontend/src/features/session/sessionRuntimeStore.ts` so the store now owns:
  - the merged current session snapshot,
  - buffered live events,
  - chat transcript updates from live events,
  - connection metadata such as channel, retry count, and last connected time.
- Provider wiring in `frontend/src/features/session/SessionWorkspaceProvider.tsx` so the session workspace creates one feed connection and routes all live events through the runtime store.
- Workspace UI wiring in `frontend/src/pages/session/SessionWorkspacePage.tsx` plus `frontend/src/features/session/live/SessionFeedStatusIndicator.tsx` so the page visibly shows live-feed health in the header and continues to bootstrap from React Query while preferring the merged runtime snapshot afterward.

## Architectural changes

The important architectural move is that React Query remains the durable bootstrap and refetch source, while the runtime store now owns the mutable live view layered on top of that durable snapshot.

That changed the frontend shape in three ways:

1. Transport isolation

- All websocket concerns now live under `frontend/src/features/session/live/`.
- UI components do not know how to build URLs, subscribe, parse frames, or reconnect.
- The client factory is injectable for tests, which let me verify reconnect behavior without a real backend socket.

2. State-layer event reduction

- `sessionRuntimeStore.ts` now hydrates a `sessionSnapshot` and applies typed live events into it.
- Stage change events update stage status, current/resume stage pointers, invalidation state, and recalculated progress counts.
- Chat and action-echo events update the transcript.
- Job progress/status events update composition/audio job state and related stage summaries.
- Older durable sequence numbers are ignored so replayed frames do not regress the store.

3. UI trust and debugging

- The workspace header now exposes a dedicated “Live updates” card with a compact state badge and detail line.
- The existing banner logic remains, but it now reflects a real connection-state model instead of a permanently mocked placeholder.
- Default behavior is intentionally explicit: if no websocket URL is configured, the workspace stays readable and clearly reports that live updates are idle.

## New abstractions and extension points

### 1. Realtime client

File: `frontend/src/features/session/live/sessionRealtimeClient.ts`

Typical usage:

```ts
const client = createSessionRealtimeClient()

const connection = client.connect({
  sessionId,
  getLastSequenceNumber: () =>
    runtimeStore.getState().eventStream.lastSequenceNumber,
  onEvent: (event) => runtimeStore.applyRealtimeEvent(event),
  onConnectionStateChange: (update) =>
    runtimeStore.syncConnectionStatus(update),
})
```

Why it matters:

- Future backend transport work can point `VITE_SESSION_EVENTS_WS_URL` at the real websocket endpoint without changing presentation code.
- Tests can inject a fake socket factory and deterministic reconnect delays.

### 2. Typed contract parsing

File: `frontend/src/features/session/live/sessionRealtime.ts`

Useful helpers:

- `buildSessionChannelName(sessionId)`
- `buildSessionSubscriptionRequest(...)`
- `parseSessionFeedMessage(...)`

Extension point:

- When the backend adds another event family, the frontend only needs a new payload type plus one parser branch here and one reducer branch in the runtime store.

### 3. Runtime snapshot hydration and live merge

File: `frontend/src/features/session/sessionRuntimeStore.ts`

Important store methods:

- `hydrateSessionSnapshot(snapshot)`
- `applyRealtimeEvent(event)`
- `syncConnectionStatus(update)`

The page now does:

```ts
runtimeStore.hydrateSessionSnapshot(snapshotQuery.data)
const snapshot = runtimeSnapshot ?? snapshotQuery.data
```

That preserves durable loading/error behavior while allowing live updates to take over once a snapshot exists.

### 4. Header status indicator

File: `frontend/src/features/session/live/SessionFeedStatusIndicator.tsx`

This component is deliberately dumb. It only renders `SessionEventStreamState`. Any future visual redesign can replace it without touching transport or reducer logic.

## Files touched

- `frontend/src/features/session/SessionWorkspaceProvider.tsx`
- `frontend/src/features/session/live/SessionFeedStatusIndicator.tsx`
- `frontend/src/features/session/live/sessionFeedConnection.ts`
- `frontend/src/features/session/live/sessionRealtime.ts`
- `frontend/src/features/session/live/sessionRealtimeClient.ts`
- `frontend/src/features/session/live/sessionRealtimeClient.test.ts`
- `frontend/src/features/session/sessionRuntimeStore.ts`
- `frontend/src/features/session/sessionRuntimeStore.test.ts`
- `frontend/src/features/session/sessionWorkspaceContext.ts`
- `frontend/src/pages/session/SessionWorkspacePage.tsx`
- `frontend/src/pages/session/SessionWorkspacePage.test.tsx`
- `frontend/src/styles/index.css`
- `frontend/src/vite-env.d.ts`

Checkpoint commit created during development:

- `0dfb491e7c7f251b0262f15331ccacda8b4542de` `feat(prompt-29): frontend websocket client skeleton`

## Verification performed

### Targeted automated checks

Ran:

- `npm test -- --run src/features/session/sessionRuntimeStore.test.ts src/features/session/live/sessionRealtimeClient.test.ts src/pages/session/SessionWorkspacePage.test.tsx`

Result:

- Pass. `3` test files, `10` tests passed.

Coverage added:

- runtime store initial state, snapshot hydration, stage-change merge, chat/action-echo merge, job-progress merge
- websocket client idle behavior, subscribe frame behavior, reconnect behavior, replay-sequence handoff
- workspace page idle live-feed UI rendering

### Broader frontend verification

Ran:

- `npm run lint`
- `npm test`
- `npm run build`
- `npm run format:check`

Final results after the last copy adjustment:

- `npm run lint`: pass
- `npm test`: pass, `11` test files and `36` tests passed
- `npm run build`: pass
- `npm run format:check`: pass

### Browser and visual verification

Because the real compose `backend` service is currently blocked by an existing local config problem, I verified the rendered UI in the running `browser` container with mocked `/api/hello` and `/api/v1/sessions/moonlit-harbor` responses.

Browser verification steps:

- Reused the running compose stack from `infra/compose/docker-compose.yml`
- Verified the live frontend at `http://localhost:8566`
- Used `docker compose -f infra/compose/docker-compose.yml exec -T browser node --input-type=module ...` with Puppeteer request interception
- Asserted that the workspace route rendered and that `Live feed idle` was visible
- Captured screenshots at desktop and mobile viewports

Artifacts:

- Desktop: `/Users/kevin/code/storyteller/.artifacts/webapp-qa/prompt-29-session-workspace-desktop.png`
- Mobile: `/Users/kevin/code/storyteller/.artifacts/webapp-qa/prompt-29-session-workspace-mobile.png`

What I visually verified:

- the new “Live updates” status card is present in the workspace header
- idle state badge renders as expected
- the shorter idle detail copy fits the desktop card better than the first attempt
- mobile layout stacks the session status cards vertically and keeps the live-updates card readable

Limits of the visual verification:

- I did not verify a real websocket handshake in the browser because the backend transport for this prompt is still intentionally absent
- I did not verify the browser against the real backend API because the local backend currently exits on invalid secrets configuration, described below

## LLM or prompt evaluation suite

None added. This prompt did not change prompts, model wiring, eval logic, or other LLM-facing behavior.

Named criteria:

- `llm_changes_present`: `false`
- `eval_suite_required`: `false`
- `eval_suite_added`: `not_applicable`

## Wrong turns, dead ends, and gotchas

1. I initially ran the targeted Vitest command with repo-relative paths from inside `frontend/`, which produced “No test files found.” The fix was to rerun with `src/...` paths relative to the package root.

2. The first browser verification attempt used `docker compose run --rm browser ...`, but that path failed because compose tried to start the unhealthy backend dependency chain first. Reusing the already-running `browser` service with `docker compose exec -T browser ...` avoided that startup gate.

3. The first desktop screenshot showed that the idle detail string was too long for the new status card. I shortened the copy from a descriptive sentence to `Set VITE_SESSION_EVENTS_WS_URL to enable live updates.` and reran screenshots.

4. A first mobile screenshot used `fullPage: true`, which produced an unhelpfully tall artifact. I replaced it with a viewport screenshot after scrolling the workspace header into view.

5. The compose backend unexpectedly exited even though it had previously been healthy. The backend logs show this is not caused by prompt 29 code:
   - `Storyteller configuration is invalid.`
   - `gemini.api_key_name: Extra inputs are not permitted`
   - `gemini.project_name: Extra inputs are not permitted`
   - `gemini.project_number: Extra inputs are not permitted`
   - `openai: Extra inputs are not permitted`

## Assumptions made while working unsupervised

- The frontend should follow the prompt 17 realtime contract as the source of truth for event naming and subscription shape.
- A missing websocket endpoint should be treated as a first-class idle state rather than an error, because prompt 29 explicitly says the backend transport is not fully wired yet.
- The runtime store should prefer live-applied snapshot state over an older React Query refetch, so I only rehydrate from query data when it is at least as new as the current runtime snapshot.
- Session-scoped live subscriptions will eventually use one transport endpoint plus a subscribe frame, not a separate URL per component or per event type.
- It is acceptable for the browser QA to use mocked HTTP responses when the real backend is blocked by an existing repository-local secrets issue that is unrelated to the websocket client skeleton work.

## Remaining limits and sensible follow-ups

- The websocket client is env-gated and transport-ready, but there is still no real backend websocket endpoint to connect to.
- The reducer currently merges the event families needed for prompt 29. Later prompts may want richer merging for assets, composition chunks, and replay/hydrate fallbacks.
- Once the backend transport exists, the next useful verification step is an end-to-end browser test that exercises a real subscribe ack, a real replay sequence, and a real live progress event without request interception.

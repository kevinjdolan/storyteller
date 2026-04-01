# Prompt 28 Summary: Error, Loading, and Feedback States

## What I changed and why

I added a shared feedback system to the frontend so loading, failure, connection, and notification states read as one deliberate product language instead of a set of page-local one-offs.

The main user-facing changes are:

- Shared skeletons, inline spinners, inline banners, and blocking error panels now power the home screen, workspace shell, chat composer, and connection UI.
- The shell now has a real toast/notification layer backed by a store instead of the previous placeholder dock.
- The backend status panel now supports polling, manual refresh, offline guidance, and connection-restored / connection-lost notifications.
- The workspace route now has a dedicated error boundary so unexpected render crashes fail loudly with recovery actions instead of blanking the page.
- The workspace also shows explicit live-feed connection messaging before realtime orchestration exists, so the current mocked state is visible instead of implied.

The intent was to make pre-async scaffolding feel production-minded now, so later background jobs and SSE/WebSocket wiring can plug into an existing feedback framework instead of inventing their own UI states.

Checkpoint commit created during the run:

- `ccf16b2` — `feat(prompt-28): error loading and feedback states`

## Architectural changes across the codebase

### 1. Shared feedback primitives

New file:

- `frontend/src/shared/ui/feedback.tsx`

This file introduces the shared vocabulary for async state:

- `InlineSpinner`
- `SkeletonBlock`
- `FeedbackBanner`
- `BlockingFeedback`
- `ToastDismissButton`

These abstractions are now reused across page-level blocking failures, inline retriable failures, and action-level loading states.

### 2. Store-backed notification layer

Updated file:

- `frontend/src/state/appShellStore.ts`

The old static shell state was replaced with a small external-store style notification system:

- subscribable state
- `enqueueAppShellToast`
- `dismissAppShellToast`
- `resetAppShellState`
- `useAppShellToasts`

This made it possible to drive toasts from both React components and React Query cache hooks.

### 3. React Query feedback extension point

Updated file:

- `frontend/src/app/queryClient.ts`

I added `QueryCache` and `MutationCache` error hooks that read a `meta.feedback.errorToast` contract from queries/mutations. I only used that for action-driven failures in this prompt, but it is now the extension point for later async operations that need shared toast behavior.

### 4. Shell-level connection handling

Updated files:

- `frontend/src/hooks/useBackendStatus.ts`
- `frontend/src/shared/ui/ConnectionStatusBadge.tsx`
- `frontend/src/app/AppShell.tsx`

Changes here:

- backend status now polls every 30 seconds
- the user can manually recheck connectivity
- offline state renders an inline guidance banner
- shell-level offline/online transitions enqueue notifications
- the toast region now renders as an overlay notification stack instead of a placeholder panel

### 5. Home and workspace adoption

Updated files:

- `frontend/src/pages/home/HomePage.tsx`
- `frontend/src/pages/session/SessionWorkspacePage.tsx`
- `frontend/src/features/session/chat/SessionChatPane.tsx`

Changes here:

- home loading skeletons now use shared skeleton blocks
- home blocking load failures use `BlockingFeedback`
- session creation failures use a retriable `FeedbackBanner` plus toast notification
- workspace snapshot failures use `BlockingFeedback`
- workspace shows explicit live-feed state with a shared banner
- chat submission uses shared spinner and banner language instead of isolated form text

### 6. Workspace crash containment

New files:

- `frontend/src/features/session/SessionWorkspaceErrorBoundary.tsx`
- `frontend/src/features/session/SessionWorkspaceErrorBoundary.test.tsx`

This boundary catches unexpected render failures inside the workspace shell and renders:

- a blocking crash panel
- a retry action
- a return-home action
- the React component stack in development mode

### 7. Test harness update

Updated file:

- `frontend/src/test/renderWithAppProviders.tsx`

The shared render helper now resets the shell notification store before each render so toast state does not leak between tests.

## Examples: how to use the new abstractions

### Shared inline or page banner

Use `FeedbackBanner` for retriable, non-blocking feedback:

```tsx
<FeedbackBanner
  title="Could not start a new session. Please try again."
  description="The request failed before the workspace could open."
  tone="warning"
/>
```

Use `BlockingFeedback` when the screen cannot continue without data:

```tsx
<BlockingFeedback
  eyebrow="Session workspace"
  title="Workspace unavailable"
  bannerTitle="Session snapshot unavailable"
  description="The workspace could not load this session right now."
  tone="warning"
/>
```

### Mutation-triggered toast wiring

The query client now understands a `meta.feedback.errorToast` contract:

```tsx
useMutation({
  meta: {
    feedback: {
      errorToast: {
        title: 'Could not start a new session',
        body: 'The home screen could not open a new workspace. Try the request again.',
        dedupeKey: 'create-session',
        tone: 'warning',
      },
    },
  },
  mutationFn: createSession,
})
```

This keeps toast copy near the mutation definition instead of hard-coding it inside the shell.

### Workspace crash protection

Wrap the workspace subtree with the dedicated boundary:

```tsx
<SessionWorkspaceErrorBoundary sessionId={sessionId}>
  <SessionWorkspaceContent sessionId={sessionId} />
</SessionWorkspaceErrorBoundary>
```

That pattern is ready for reuse if later prompts introduce additional volatile subtrees such as streaming composition panes or audio job dashboards.

## Verification performed

### Automated tests

Ran:

- `cd frontend && npm run test`

Result:

- `10` test files passed
- `34` tests passed

New or expanded coverage includes:

- workspace error boundary fallback rendering
- create-session failure surfacing both inline feedback and a notification
- workspace live-feed banner rendering
- updated chat submit loading state expectations

### Lint and build

Ran:

- `cd frontend && npm run lint`
- `cd frontend && npm run build`

Result:

- lint passed with `--max-warnings=0`
- production build passed

### Browser and screenshot verification

I used the repo’s bundled browser QA flow and captured the following screenshots:

- `/Users/kevin/code/storyteller/.artifacts/webapp-qa/prompt-28-home.png`
- `/Users/kevin/code/storyteller/.artifacts/webapp-qa/prompt-28-home-mobile.png`
- `/Users/kevin/code/storyteller/.artifacts/webapp-qa/prompt-28-workspace.png`
- `/Users/kevin/code/storyteller/.artifacts/webapp-qa/prompt-28-home-offline.png`
- `/Users/kevin/code/storyteller/.artifacts/webapp-qa/prompt-28-workspace-offline.png`

Commands used:

- `docker compose -f infra/compose/docker-compose.yml run --rm browser npm run check -- --spec /workspace/.artifacts/webapp-qa/prompt-28-home.spec.json`
- `docker compose -f infra/compose/docker-compose.yml run --rm browser npm run check -- --spec /workspace/.artifacts/webapp-qa/prompt-28-home-mobile.spec.json`
- `docker compose -f infra/compose/docker-compose.yml run --rm browser npm run check -- --spec /workspace/.artifacts/webapp-qa/prompt-28-workspace.spec.json`
- `docker exec storyteller-browser-1 sh -lc 'cd /workspace/tools/webapp-qa && npm run check -- --spec /workspace/.artifacts/webapp-qa/prompt-28-home-offline.spec.json'`
- `docker exec storyteller-browser-1 sh -lc 'cd /workspace/tools/webapp-qa && npm run check -- --spec /workspace/.artifacts/webapp-qa/prompt-28-workspace-offline.spec.json'`

What I visually verified:

- desktop home layout still reads cleanly with the new connection panel
- mobile home layout stacks correctly with the new feedback surfaces
- the workspace shows the new live-feed banner without collapsing the two-pane shell
- offline home state shows:
  - offline connection status
  - inline retry guidance banner
  - blocking session-load failure
  - shell-level toast notification
- offline workspace state shows:
  - shell-level offline notification
  - blocking workspace failure panel with retry and return-home actions

Visual limit:

- the normal-state workspace screenshot was captured before I took the backend down and shows the entrance transition slightly mid-fade in the top bar. The important new feedback banner and shell layout are still visible and readable.

### Environment / infrastructure verification limit

After I stopped the backend for offline-state QA, restarting it exposed an unrelated local environment problem in `secrets.yaml`:

- `gemini.api_key_name: Extra inputs are not permitted`
- `gemini.project_name: Extra inputs are not permitted`
- `gemini.project_number: Extra inputs are not permitted`
- `openai: Extra inputs are not permitted`

This is not caused by the frontend changes in this prompt, but it prevented me from taking a refreshed post-restart workspace screenshot. The frontend code-level validation still passed, and the offline screenshots were captured successfully.

## LLM / prompt evaluation suite

None added.

Reason:

- this prompt did not modify any LLM prompts, model wiring, eval logic, agent behavior, or other AI-facing orchestration

Evaluation result:

- not applicable

## Wrong turns, dead ends, and gotchas

### 1. `useEffectEvent` was the wrong fit here

I initially used `useEffectEvent` in `useBackendStatus` because the hook both polls in an effect and exposes a manual refresh action. ESLint correctly rejected returning that function for general use. I replaced it with a `useCallback` implementation, which is simpler and lint-safe for this case.

### 2. `docker compose run` is the wrong tool for offline-mode browser checks

I first used `docker compose run --rm browser ...` for failure-mode screenshots. That was wrong because Compose eagerly recreated dependencies, including the backend I had intentionally stopped. I switched to `docker exec storyteller-browser-1 ...` against the already-running browser container, which preserved the real offline state.

### 3. Restarting the backend exposed a local config mismatch

The backend had been healthy before the offline test, but once restarted it began rejecting the current local secrets shape. I did not patch secrets or backend config for this prompt because that would have been unrelated scope creep and risky in an unsupervised run.

## Assumptions I made while working unsupervised

- Blocking page-load failures should use full-width blocking panels, while action-triggered failures should use inline banners plus toasts.
- Toasts should be explicit and dismissible rather than auto-dismissing for now, because later background jobs will likely need durable notification history before timing behavior is settled.
- Polling backend reachability every 30 seconds plus a manual refresh button is enough for this pre-realtime stage.
- The existing warm glassmorphism theme should be preserved rather than introducing a new visual language for feedback components.
- It was acceptable to commit the production code changes first (`ccf16b2`) and leave only this reviewer summary plus the pre-existing prompt-log files uncommitted at handoff.

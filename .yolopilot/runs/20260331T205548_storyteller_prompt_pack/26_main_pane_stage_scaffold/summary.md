# Prompt 26 — Main Pane Stage Scaffold

## What I changed and why

I turned the existing right-hand workspace pane from a generic summary grid into a real stage scaffold for the full bedtime-story workflow.

The main user-visible changes are:

- A new ordered **stage navigator** in the main pane that lists every required workflow step from `genre` through `finalize`.
- A new **selected-stage detail panel** that shows placeholder content for the active stage, including planned controls, routing behavior, and downstream invalidation impact.
- **Stage-aware routing** through a `?stage=<stage-id>` query parameter so the visible panel can change without mutating the backend-owned `current_stage`.
- A more explicit distinction between:
  - the **durable current stage** from backend session state
  - the **currently viewed stage panel** selected via the route
- Visual treatment for stage availability states so the scaffold can later evolve into true locked/unlocked/revisitable navigation.

I made these changes because prompt 26 asked for a thin but coherent end-to-end workflow skeleton. The prior UI already exposed some session summary and stage state, but it did not provide a dedicated navigator, did not make stage-to-panel mapping explicit, and did not give the main pane a future-proof route/state model for deeper stage work.

## Architectural changes across the codebase

### 1. Canonical stage metadata expanded in `frontend/src/features/session/workflowStages.ts`

The existing workflow registry already owned the canonical stage order, labels, descriptions, and invalidation rules. I expanded it to also carry scaffold-specific UI metadata:

- `scaffoldTitle`
- `scaffoldSummary`
- `scaffoldBullets`

I also added small helper APIs:

- `isWorkflowStageId(value)`
- `getWorkflowStageDefinition(stageId)`
- `getWorkflowStageLabel(stageId)`

This keeps the workflow registry as the single source of truth for stage sequencing plus stage-specific scaffold copy, rather than scattering stage metadata across the page component.

### 2. New stage view-model adapter in `frontend/src/features/session/sessionStageScaffold.ts`

I added a dedicated frontend-only adapter that merges durable session data with the canonical stage registry:

- `buildSessionWorkspaceStageViews(snapshot, requestedStageId)`
- `resolveRequestedSessionStage(requestedStageId, currentStageId)`

This adapter normalizes the session into a full ordered stage list even if the backend snapshot only contains partial `stage_states`. It also derives:

- `isCurrent`
- `isSelected`
- `availability` as `locked | unlocked | revisitable`
- scaffold metadata attached to each stage view

That separation matters because the workspace page now renders against a stable view model instead of hand-assembling fallback stage logic inline.

### 3. Route helper extended in `frontend/src/app/routePaths.ts`

`buildSessionWorkspacePath` now accepts an optional stage:

```ts
buildSessionWorkspacePath(sessionId, { stage: 'audio' })
// => /sessions/<id>?stage=audio
```

This is the routing hook that lets the navigator preview a specific stage panel while preserving backend ownership of the real workflow state.

### 4. Main workspace page refactor in `frontend/src/pages/session/SessionWorkspacePage.tsx`

The page now:

- reads `stage` from `useSearchParams()`
- builds normalized stage views through `buildSessionWorkspaceStageViews(...)`
- renders a navigator list on the left side of the main canvas
- renders a selected-stage scaffold panel on the right side of the main canvas
- keeps the existing topbar, chat lane, progress card, and production summary intact

The selected-stage panel currently shows:

- scaffold title and summary
- stage status badge
- availability badge
- route/state behavior note
- current session signal
- route mapping indicator
- downstream invalidation summary
- planned controls list

### 5. Styling updates in `frontend/src/styles/index.css`

I added the new layout and component styling for:

- `workspace-stage-shell`
- `workspace-stage-navigator`
- `workspace-stage-nav__*`
- `workspace-stage-detail*`

The mobile layout stacks the navigator above the detail panel, which I verified with screenshots.

## Examples and extension points

### Deep-link to a stage panel

Use the route helper anywhere you need a direct link into a specific workspace panel:

```ts
import { buildSessionWorkspacePath } from '../app/routePaths.ts'

const href = buildSessionWorkspacePath(sessionId, { stage: 'composition' })
```

This changes the visible panel only. It does not mutate the durable session state.

### Build a normalized stage list from a snapshot

Use the new scaffold adapter when a component needs the full ordered workflow, even if the API returns sparse stage state:

```ts
import { buildSessionWorkspaceStageViews } from '../features/session/sessionStageScaffold.ts'

const { currentStage, selectedStage, stageViews } =
  buildSessionWorkspaceStageViews(snapshot, searchParams.get('stage'))
```

This is the main extension point for later prompt work. Real forms, selectors, beat editors, composition progress, and audio jobs can be mounted into the selected-stage panel without changing the navigator contract.

### Reuse canonical stage labeling

```ts
import { getWorkflowStageLabel } from '../features/session/workflowStages.ts'

const copy = `Resume at ${getWorkflowStageLabel(snapshot.resume_stage)}`
```

That helper removes duplicate label lookup logic from page components.

## Verification performed

### Automated frontend verification

All commands were run from `/Users/kevin/code/storyteller/frontend`.

- `npm test`
  - Result: pass
  - Outcome: `8` test files passed, `28` tests passed
- `npm run lint`
  - Result: pass
  - Outcome: no lint errors
- `npm run build`
  - Result: pass
  - Outcome: production build completed successfully with Vite

### Added / expanded test coverage

- `frontend/src/features/session/sessionStageScaffold.test.ts`
  - verifies normalization to the canonical 10-stage order
  - verifies fallback stage derivation for sparse snapshots
  - verifies locked vs revisitable state derivation
- `frontend/src/features/session/workflowStages.test.ts`
  - verifies helper functions and scaffold bullet coverage
- `frontend/src/pages/session/SessionWorkspacePage.test.tsx`
  - verifies the navigator renders
  - verifies the selected-stage scaffold heading renders
  - verifies `?stage=audio` route previews the audio scaffold without changing the durable current step

### Browser-based verification

I used the Docker Compose browser container against the running dev stack in `infra/compose`.

Live backend target:

- session used for QA: `58895f8c-97e2-4d63-b277-428cf4d9489d`
- frontend URL: `http://127.0.0.1:8566`

Captured screenshots:

- `/Users/kevin/code/storyteller/.artifacts/webapp-qa/prompt-26-workspace-desktop.png`
  - desktop view of the workspace with the navigator and genre scaffold visible
- `/Users/kevin/code/storyteller/.artifacts/webapp-qa/prompt-26-workspace-audio-preview.png`
  - desktop view of the workspace while previewing the audio stage through `?stage=audio`
- `/Users/kevin/code/storyteller/.artifacts/webapp-qa/prompt-26-workspace-mobile-stage.png`
  - mobile view showing the stacked navigator layout
- `/Users/kevin/code/storyteller/.artifacts/webapp-qa/prompt-26-workspace-mobile-detail.png`
  - mobile view showing the stacked stage detail panel layout

What I visually confirmed:

- The main pane clearly indicates the selected stage.
- Every required stage is present in the navigator.
- The audio stage can be previewed through the route without changing the topbar’s durable current stage.
- Mobile stacks the navigator and stage detail instead of trying to preserve the desktop side-by-side layout.

### Verification limits

- The live QA session used a draft session at the `genre` stage, so the “Current session signal” block mostly exercised fallback and empty-state copy rather than rich accepted data.
- I did not add backend tests because no backend files or API contracts changed in this prompt.

## LLM / prompt evaluation suite

No LLM-facing behavior changed in this prompt. I did not modify prompts, model wiring, agent behavior, or eval infrastructure.

Evaluation result:

- `LLM-facing regression suite`: not applicable

## Wrong turns, dead ends, and gotchas

- I initially ran `npm test -- --runInBand`, which failed because this Vitest setup does not support that flag. I reran using the repo’s native `npm test` command.
- I first captured a mobile screenshot that only showed the top of the page. That was not sufficient evidence for this task, so I recaptured mobile screenshots scrolled to the navigator and the stage detail panel.
- The repo-level `docker compose ps` call fails because the compose file is not at the repository root. The correct compose working directory for this project is `infra/compose`.

## Assumptions made while working unsupervised

- I assumed a query-parameter route like `?stage=audio` satisfies the prompt’s requirement for stage-aware routing while remaining compatible with backend-owned durable stage state.
- I assumed it is acceptable for “locked” stages to be previewable in the navigator during this scaffold phase, since the prompt asked for the full end-to-end flow to be visible before all business logic exists.
- I assumed the best place for stage-specific scaffold copy was the canonical frontend workflow registry, because those labels and descriptions were already centrally owned there.
- I assumed no backend API changes were needed because the existing snapshot plus frontend-derived fallback stage normalization was enough to satisfy the scaffold requirement.

## Remaining limits and likely next steps

- Locked/unlocked/revisitable state is visual only for now; the navigator previews stages rather than enforcing stage-entry policy.
- The scaffold panel is intentionally placeholder-only. Real stage editors, accept/regenerate actions, and durable mutations still need to be implemented in later prompts.
- The current route model is in place for nested behavior, but there is no browser back/forward-specific test coverage beyond the query-param preview test.

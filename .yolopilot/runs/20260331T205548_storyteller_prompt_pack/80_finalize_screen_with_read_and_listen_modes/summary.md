# Prompt 80: Finalize Screen With Read and Listen Modes

## What I changed and why

I implemented the finalize stage as a real end-state review surface instead of a narrow export/rewrite panel.

The main user-facing changes are:

- Added a tabbed `Read story` / `Listen back` experience inside [`frontend/src/features/session/FinalizeStage.tsx`](/Users/kevin/code/storyteller/frontend/src/features/session/FinalizeStage.tsx).
- Added a compact session completion summary panel showing selected genre, tone, length targets, manuscript status, narration status, and completion timestamp.
- Kept the existing revision-compare tools available below the new finish-line surfaces so late rewrite review still works from finalize.
- Made the stage tolerant of partial completion:
  - story text can render from the durable story asset when available
  - if the durable asset is still loading or unavailable inline, the reader falls back to the accepted manuscript snapshot already present in session state
  - audio can be `ready`, `queued`, `generating`, `mixing`, `paused`, or `failed`, and the UI renders those states without collapsing the stage
- Added calm reading presentation for final manuscript content, including simple heading parsing for Markdown-style story assets so chapter headings do not show as raw `#` markers.
- Added inline narration review with compiled-audio metadata chips and progress/error handling.

This work stayed frontend-only on purpose. The backend already exposed enough durable session data and asset access URLs to support the finalize experience without adding new API contracts.

## Architectural changes across the codebase

### 1. Finalize stage now owns asset-backed review behavior

[`frontend/src/features/session/FinalizeStage.tsx`](/Users/kevin/code/storyteller/frontend/src/features/session/FinalizeStage.tsx) moved from a fairly small export/rewrite panel to a fuller stateful review screen. It now:

- loads final story text from the session asset URL when available
- falls back to accepted composition text if the final story asset is not yet readable inline
- derives audio review state from existing `latest_audio_job` / `active_audio_job` data
- presents tabbed read/listen views while preserving all existing rewrite actions

This keeps finalize-specific policy and presentation logic in one place instead of spreading it into `SessionWorkspacePage`.

### 2. Shared asset helper for reading text assets

[`frontend/src/features/session/sessionArtifacts.ts`](/Users/kevin/code/storyteller/frontend/src/features/session/sessionArtifacts.ts) now exports `fetchSessionAssetText(...)`.

That helper centralizes:

- resolving the best readable URL for a session asset
- falling back from stream URL to download URL when necessary
- basic HTTP failure handling for asset reads

This matters because story reading is now an asset-backed concern, not just a download-only concern.

Example:

```ts
const storyText = await fetchSessionAssetText(snapshot.latest_story_asset)
```

If another stage later needs to render durable text assets inline, it can reuse the same helper instead of rebuilding URL selection and fetch handling.

### 3. Dedicated finalize-stage styling and browser-driven interaction hardening

[`frontend/src/styles/index.css`](/Users/kevin/code/storyteller/frontend/src/styles/index.css) now includes dedicated finalize-stage layout, tab, reader, listen-card, metadata-chip, and summary-panel styling.

During browser QA I found that the sticky review summary could intercept pointer events over the tab strip on desktop. The follow-up fix commit (`91bf5f6`) explicitly puts the experience column above the sticky summary column with `position`/`z-index` isolation so the tabs remain clickable in a real browser.

## Key files touched

- [`frontend/src/features/session/FinalizeStage.tsx`](/Users/kevin/code/storyteller/frontend/src/features/session/FinalizeStage.tsx)
- [`frontend/src/features/session/FinalizeStage.test.tsx`](/Users/kevin/code/storyteller/frontend/src/features/session/FinalizeStage.test.tsx)
- [`frontend/src/features/session/sessionArtifacts.ts`](/Users/kevin/code/storyteller/frontend/src/features/session/sessionArtifacts.ts)
- [`frontend/src/styles/index.css`](/Users/kevin/code/storyteller/frontend/src/styles/index.css)

## New abstractions, helpers, and extension points

### `fetchSessionAssetText`

Use this when a stage needs to read a durable text asset inline:

```ts
import { fetchSessionAssetText } from './sessionArtifacts.ts'

const text = await fetchSessionAssetText(snapshot.latest_story_asset)
```

Extension point:

- A future stage could use this for alternate story-asset-backed readers, inline export previews, or diffable asset history without duplicating URL resolution logic.

### Finalize-stage fallback manuscript behavior

The finalize reader prefers the durable `latest_story_asset`, but it can still render from accepted composition state. That fallback behavior means new finalize-adjacent surfaces can stay usable even while the asset pipeline lags.

Practical pattern:

```ts
const displayStoryText = storyAssetText ?? fallbackStoryText ?? null
```

Extension point:

- If a later prompt adds EPUB/PDF generation, finalize can keep the same fallback reader while waiting for additional export formats.

### Audio review state modeling from existing job data

No backend enum was added. The finalize stage derives user-facing states from existing audio job fields:

- `planned`
- `queued`
- `generating`
- `mixing`
- `paused`
- `failed`
- `completed`

Extension point:

- If the audio pipeline later exposes segment previews or publish retries inside finalize, the current state model is already the place to extend.

## Verification work performed

### Targeted frontend tests

Ran:

```bash
cd /Users/kevin/code/storyteller/frontend
npx vitest run src/features/session/FinalizeStage.test.tsx
```

Result:

- Passed: `1` file, `4` tests

Coverage added in [`frontend/src/features/session/FinalizeStage.test.tsx`](/Users/kevin/code/storyteller/frontend/src/features/session/FinalizeStage.test.tsx):

- rewrite compare actions still work from finalize
- finalized read/listen surfaces render when both assets exist
- story remains readable while audio is still processing
- audio failure state renders without collapsing finalize

### Full frontend test suite

Ran:

```bash
cd /Users/kevin/code/storyteller/frontend
npm test
```

Result:

- Passed: `22` test files
- Passed: `116` tests

### Lint

Ran:

```bash
cd /Users/kevin/code/storyteller/frontend
npm run lint
```

Result:

- Passed with `0` warnings

I reran lint after the browser-driven CSS stacking fix so the final branch state is covered.

### Build

Ran:

```bash
cd /Users/kevin/code/storyteller/frontend
npm run build
```

Result:

- Passed

Observed non-blocking warning:

- Vite reported a chunk-size warning for the main JS bundle (`~626 kB` minified). This existed as a build warning only; it did not block the build.

### Browser checks and screenshots

Because Docker could not be used in this environment, I performed browser QA with a local Vite server plus Playwright route mocks for the hydration payload and story asset.

Commands used:

```bash
cd /Users/kevin/code/storyteller/frontend
npm run dev -- --host 127.0.0.1 --port 8566
npx playwright install chromium
npx playwright test .tmp-storyteller-finalize-qa.spec.mjs --reporter=line
```

Result:

- Passed: `3` Playwright checks

Screenshot artifacts captured:

- `/tmp/storyteller-finalize-read-desktop.png`
- `/tmp/storyteller-finalize-listen-desktop.png`
- `/tmp/storyteller-finalize-listen-mobile.png`

What I visually verified:

- finalize read mode renders a calm manuscript surface with chapter headings and readable body text
- finalize listen mode renders the compiled narration surface and summary panel
- mobile layout keeps the tabbed finalize surface functional in a narrow viewport
- the sticky summary no longer blocks tab clicks after the CSS stacking fix

Limits of the browser coverage:

- This was not a full Compose-backed run because the Docker daemon never became available.
- The browser screenshots used mocked hydration/story responses that match a completed finalize session.
- The backend status card/toast remained in frontend-only mode during this browser pass, which is expected for the fallback workflow.

## LLM / prompt / eval work

No LLM-facing logic, prompts, model wiring, or eval contracts were changed in this prompt.

Evaluation suite status:

- Not applicable

Measured outcomes:

- No LLM or prompt criteria were introduced because the work was UI-only.

## Wrong turns, dead ends, surprising behavior, and gotchas

### 1. Docker-backed visual QA was blocked

I followed the preferred visual-QA path first:

- checked `docker compose -f infra/compose/docker-compose.yml ps --format json`
- started Docker Desktop with `open -a Docker`
- retried daemon access multiple times
- checked Docker Desktop status/logs

The daemon never became reachable at `unix:///Users/kevin/.docker/run/docker.sock`, so Compose-based visual QA was blocked in this run.

### 2. `odysseus` CLI was not available here

I checked `odysseus --help` per the skill instructions. The command was not installed in this environment, so I used the browser fallback path instead.

### 3. Playwright fallback required temporary QA-only setup

The repo did not have `@playwright/test` installed locally, and the `npx playwright` binary alone was not enough for an imported spec file. To get browser QA running without changing committed dependencies, I:

- installed `@playwright/test` with `npm install --no-save @playwright/test`
- installed the Chromium browser binary with `npx playwright install chromium`
- created a temporary spec file in the frontend directory for the mocked browser run
- removed the temporary spec afterward

No manifest or lockfile changes were left behind.

### 4. Browser QA found a real regression that jsdom did not

The first desktop Playwright pass showed that the sticky summary column could intercept pointer events over the finalize tab strip. This did not fail in React Testing Library because jsdom does not model real layout/pointer interception. I fixed that by giving the experience column higher stacking priority than the sticky summary column.

## Assumptions made while working unsupervised

- The existing backend asset contract for `latest_story_asset` and `latest_audio_asset` is the correct source of truth for finalize, so no backend changes were required.
- Story text assets may contain Markdown-style headings, and simple heading parsing is sufficient for the calm in-app reading surface right now.
- The accepted composition text is an acceptable reader fallback while the durable story asset loads or is unavailable inline.
- The existing audio job fields are expressive enough to derive finalize-phase statuses without introducing new API fields.
- Browser verification with mocked hydration/story responses is an acceptable fallback when Docker/Compose-backed verification is impossible in the execution environment.

## Commits created during development

- `28197fa` `feat(prompt-80): finalize screen read and listen`
- `91bf5f6` `fix(prompt-80): keep finalize tabs clickable`

## Final branch/worktree state

Code changes for prompt 80 are committed.

The only remaining uncommitted files in the worktree are `.yolopilot` run artifacts outside the app source tree.

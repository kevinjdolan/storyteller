# YoloPilot Log

- Task file: `/Users/kevin/code/storyteller/prompts/03-fastapi-scaffold.md`
- Summary file: `/Users/kevin/code/storyteller/prompts/03-fastapi-scaffold.summary.md`
- Raw Codex log: `/Users/kevin/code/storyteller/prompts/03-fastapi-scaffold.codex.jsonlines`
- Compact event log: `/Users/kevin/code/storyteller/prompts/03-fastapi-scaffold.yolopilot.jsonlines`

## YoloPilot Event

- Time: `2026-03-31T21:21:30-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `1`
- Summary: Beginning task 4 of 100: 03-fastapi-scaffold.md

### Full Text

    Beginning task 4 of 100: 03-fastapi-scaffold.md

## YoloPilot Event

- Time: `2026-03-31T21:21:30-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `2`
- Summary: Creating branch yolopilot-init-03-fastapi-scaffold from yolopilot-init-02-vite-react-scaffold.

### Full Text

    Creating branch yolopilot-init-03-fastapi-scaffold from yolopilot-init-02-vite-react-scaffold.

## YoloPilot Event

- Time: `2026-03-31T21:21:30-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `3`
- Summary: Launching Codex for 03-fastapi-scaffold.md with model gpt-5.4 and reasoning effort xhigh.

### Full Text

    Launching Codex for 03-fastapi-scaffold.md with model gpt-5.4 and reasoning effort xhigh.

## Session Started

- Time: `2026-03-31T21:21:31-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `4`
- Summary: Thread ID: 019d4746-7093-7402-a87a-16805a1fba5e

### Full Text

    Thread ID: 019d4746-7093-7402-a87a-16805a1fba5e

## Turn Started

- Time: `2026-03-31T21:21:31-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `5`
- Summary: Codex started a new turn for the current task.

### Full Text

    Codex started a new turn for the current task.

## Agent Message

- Time: `2026-03-31T21:21:41-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `6`
- Summary: I’m inspecting the existing repo structure and prior prompt work first so the FastAPI scaffold fits the current patterns instead of landing as an isolated backend blob.

### Full Text

    I’m inspecting the existing repo structure and prior prompt work first so the FastAPI scaffold fits the current patterns instead of landing as an isolated backend blob.

## Command Started

- Time: `2026-03-31T21:21:41-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `7`
- Summary: in progress: /bin/zsh -lc pwd

### Full Text

    Command: /bin/zsh -lc pwd
    Status: in progress

## Command Finished

- Time: `2026-03-31T21:21:41-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `8`
- Summary: completed, exit 0: /bin/zsh -lc pwd

### Full Text

    Command: /bin/zsh -lc pwd
    Status: completed
    Exit code: 0
    Output:
    /Users/kevin/code/storyteller

## Command Started

- Time: `2026-03-31T21:21:41-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `9`
- Summary: in progress: /bin/zsh -lc 'git status --short --branch'

### Full Text

    Command: /bin/zsh -lc 'git status --short --branch'
    Status: in progress

## Command Finished

- Time: `2026-03-31T21:21:41-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `10`
- Summary: completed, exit 0: /bin/zsh -lc 'git status --short --branch'

### Full Text

    Command: /bin/zsh -lc 'git status --short --branch'
    Status: completed
    Exit code: 0
    Output:
    ## yolopilot-init-03-fastapi-scaffold
     M prompts/02-vite-react-scaffold.yolopilot.jsonlines
     M prompts/02-vite-react-scaffold.yolopilot.md
    ?? prompts/03-fastapi-scaffold.codex.jsonlines
    ?? prompts/03-fastapi-scaffold.yolopilot.jsonlines
    ?? prompts/03-fastapi-scaffold.yolopilot.md

## Command Started

- Time: `2026-03-31T21:21:41-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `11`
- Summary: in progress: /bin/zsh -lc "rg --files -g 'AGENTS.md' -g 'README*' -g 'base_prompt.md' -g 'prompts/**' -g 'frontend/**' -g 'backend/**' ."

### Full Text

    Command: /bin/zsh -lc "rg --files -g 'AGENTS.md' -g 'README*' -g 'base_prompt.md' -g 'prompts/**' -g 'frontend/**' -g 'backend/**' ."
    Status: in progress

## Command Finished

- Time: `2026-03-31T21:21:41-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `12`
- Summary: completed, exit 0: /bin/zsh -lc "rg --files -g 'AGENTS.md' -g 'README*' -g 'base_prompt.md' -g 'prompts/**' -g 'frontend/**' -g 'backend/**' ."

### Full Text

    Command: /bin/zsh -lc "rg --files -g 'AGENTS.md' -g 'README*' -g 'base_prompt.md' -g 'prompts/**' -g 'frontend/**' -g 'backend/**' ."
    Status: completed
    Exit code: 0
    Output:
    ./prompts/00-project-charter.codex.jsonlines
    ./prompts/36-conversation-memory-summaries.md
    ./prompts/99-release-checklist-and-future-roadmap.md
    ./prompts/44-pitch-generation-pipeline.md
    ./prompts/42-story-setup-brief-form.md
    ./prompts/07-developer-bootstrap-scripts.md
    ./prompts/20-frontend-app-shell-and-routing.md
    ./prompts/52-bedtime-safety-and-content-guidelines.md
    ./prompts/02-vite-react-scaffold.md
    ./prompts/78-download-endpoints-and-object-access.md
    ./prompts/01-monorepo-skeleton.md
    ./prompts/13-storage-abstraction-and-buckets.md
    ./prompts/48-save-the-cat-beat-sheet-generation.md
    ./prompts/95-ci-pipeline.md
    ./prompts/46-character-sheet-generation.md
    ./prompts/83-artifact-packaging-and-links.md
    ./prompts/11-postgres-schema-and-migrations.md
    ./prompts/06-gitignore-and-secrets-hygiene.md
    ./prompts/65-interrupt-and-redirect-composition.md
    ./prompts/30-chat-to-ui-action-schema.md
    ./prompts/37-agent-tool-registry.md
    ./prompts/54-chapter-scene-card-editor.md
    ./prompts/62-composition-streaming-events.md
    ./prompts/26-main-pane-stage-scaffold.md
    ./prompts/56-revision-history-and-branches.md
    ./prompts/00-project-charter.md
    ./prompts/03-fastapi-scaffold.yolopilot.jsonlines
    ./prompts/01-monorepo-skeleton.yolopilot.md
    ./prompts/88-artifact-retention-and-cleanup.md
    ./prompts/63-composition-main-pane-ui.md
    ./prompts/74-background-music-mixing.md
    ./prompts/01-monorepo-skeleton.summary.md
    ./prompts/14-repositories-and-session-service.md
    ./prompts/61-segmented-writing-engine.md
    ./prompts/67-diff-and-compare-ui.md
    ./prompts/17-realtime-event-schema.md
    ./prompts/90-local-identity-and-future-auth-shape.md
    ./prompts/80-finalize-screen-read-and-listen.md
    ./prompts/45-pitch-refinement-via-chat.md
    ./prompts/01-monorepo-skeleton.yolopilot.jsonlines
    ./prompts/92-observability-and-logging.md
    ./prompts/72-narration-segmentation.md
    ./prompts/04-docker-compose-foundation.md
    ./prompts/64-agent-summary-messages-during-composition.md
    ./prompts/41-tone-selection-api-and-ui.md
    ./prompts/02-vite-react-scaffold.codex.jsonlines
    ./prompts/23-frontend-state-foundation.md
    ./prompts/97-security-review.md
    ./prompts/12-seed-genres-and-tones.md
    ./prompts/81-docx-export-pipeline.md
    ./prompts/03-fastapi-scaffold.yolopilot.md
    ./prompts/87-developer-debug-inspector.md
    ./prompts/25-chat-window-foundation.md
    ./prompts/01-monorepo-skeleton.codex.jsonlines
    ./prompts/60-composition-job-orchestration.md
    ./prompts/96-compose-dev-and-prod-shapes.md
    ./prompts/49-beat-sheet-refinement-ui-and-chat.md
    ./prompts/93-accessibility-pass-and-keyboard-support.md
    ./prompts/15-event-log-and-audit-trail.md
    ./prompts/47-character-refinement-via-chat.md
    ./prompts/16-asset-metadata-and-file-records.md
    ./prompts/02-vite-react-scaffold.yolopilot.md
    ./prompts/76-audio-preview-and-segment-status-ui.md
    ./prompts/53-outline-drill-down.md
    ./prompts/66-rewrite-prior-segments.md
    ./prompts/18-postgres-job-runner-skeleton.md
    ./prompts/43-brief-normalization-service.md
    ./prompts/base_prompt.md
    ./prompts/50-story-length-duration-and-chapter-setup.md
    ./prompts/86-completed-session-summary-and-search.md
    ./prompts/82-html-markdown-and-reader-formatting.md
    ./prompts/77-final-audio-assembly.md
    ./prompts/79-audio-pipeline-tests.md
    ./prompts/34-ui-events-to-agent-context.md
    ./prompts/89-full-journey-e2e-test.md
    ./prompts/57-composition-prompt-assembly.md
    ./prompts/39-bridge-and-replay-tests.md
    ./prompts/03-fastapi-scaffold.md
    ./prompts/31-intent-parser-service.md
    ./prompts/75-audio-job-orchestration.md
    ./prompts/02-vite-react-scaffold.yolopilot.jsonlines
    ./prompts/00-project-charter.yolopilot.md
    ./prompts/85-audio-player-with-text-sync-hooks.md
    ./prompts/00-project-charter.summary.md
    ./prompts/05-backend-settings-and-secrets-loading.md
    ./prompts/33-action-echoes-in-chat.md
    ./prompts/08-repo-quality-tooling.md
    ./prompts/19-data-layer-integration-tests.md
    ./prompts/73-gemini-tts-integration.md
    ./prompts/02-vite-react-scaffold.summary.md
    ./prompts/71-audio-length-estimation.md
    ./prompts/22-workspace-two-pane-layout.md
    ./prompts/38-session-replay-and-resume-hydration.md
    ./prompts/10-domain-model-and-state-machine.md
    ./prompts/40-genre-selection-api-and-ui.md
    ./prompts/70-audio-settings-model-and-ui.md
    ./prompts/69-composition-loop-e2e-test.md
    ./prompts/00-project-charter.yolopilot.jsonlines
    ./prompts/27-reusable-form-and-card-components.md
    ./prompts/98-demo-data-and-onboarding.md
    ./prompts/21-past-sessions-home-screen.md
    ./prompts/51-correlation-heuristics.md
    ./prompts/03-fastapi-scaffold.codex.jsonlines
    ./prompts/35-chat-commands-and-quick-actions.md
    ./prompts/55-continuity-bible.md
    ./prompts/28-error-loading-and-feedback-states.md
    ./prompts/32-ui-action-policy-engine.md
    ./prompts/94-performance-pass.md
    ./prompts/29-frontend-websocket-client-skeleton.md
    ./prompts/58-usage-cost-and-latency-metrics.md
    ./prompts/68-autosave-drafts-and-partials.md
    ./prompts/09-initial-system-diagram-and-adr.md
    ./prompts/91-rate-limits-retries-and-fallbacks.md
    ./prompts/24-design-tokens-and-accessibility-foundation.md
    ./prompts/84-reader-ui-with-navigation.md
    ./prompts/59-planning-funnel-e2e-test.md
    ./scripts/README.md
    ./README.md
    ./docs/README.md
    ./docs/adr/README.md
    ./backend/README.md
    ./backend/Dockerfile
    ./backend/requirements.txt
    ./backend/app/main.py
    ./backend/app/worker/README.md
    ./backend/app/__pycache__/main.cpython-313.pyc
    ./backend/migrations/README.md
    ./frontend/src/vite-env.d.ts
    ./frontend/src/styles/index.css
    ./frontend/src/shared/api.ts
    ./frontend/src/features/system/useBackendStatus.ts
    ./frontend/src/features/home/HomeRoute.test.tsx
    ./frontend/src/features/home/HomeRoute.tsx
    ./frontend/src/test/setup.ts
    ./frontend/src/app/router.tsx
    ./frontend/src/app/AppShell.tsx
    ./frontend/src/app/App.tsx
    ./frontend/src/main.tsx
    ./frontend/vitest.config.ts
    ./frontend/vite.config.ts
    ./frontend/eslint.config.js
    ./frontend/tsconfig.json
    ./frontend/package.json
    ./frontend/package-lock.json
    ./frontend/.prettierrc.json
    ./frontend/public/favicon.svg
    ./frontend/README.md
    ./frontend/.prettierignore
    ./frontend/node_modules/isexe/mode.js
    ./frontend/node_modules/isexe/windows.js
    ./frontend/node_modules/isexe/package.json
    ./frontend/node_modules/isexe/README.md
    ./frontend/node_modules/isexe/index.js
    ./frontend/tsconfig.node.json
    ./frontend/node_modules/isexe/test/basic.js
    ./frontend/node_modules/isexe/LICENSE
    ./frontend/node_modules/isexe/.npmignore
    ./frontend/node_modules/esrecurse/package.json
    ./frontend/node_modules/esrecurse/gulpfile.babel.js
    ./frontend/node_modules/esrecurse/README.md
    ./frontend/node_modules/esrecurse/esrecurse.js
    ./frontend/node_modules/esrecurse/.babelrc
    ./frontend/node_modules/indent-string/index.d.ts
    ./tools/README.md
    ./frontend/node_modules/indent-string/package.json
    ./frontend/node_modules/indent-string/readme.md
    ./frontend/node_modules/indent-string/index.js
    ./frontend/node_modules/indent-string/license
    ./frontend/node_modules/tinyglobby/package.json
    ./frontend/node_modules/tinyglobby/README.md
    ./frontend/node_modules/html-encoding-sniffer/LICENSE.txt
    ./frontend/node_modules/source-map-js/source-map.d.ts
    ./frontend/node_modules/escalade/index.d.ts
    ./frontend/node_modules/assertion-error/index.d.ts
    ./frontend/node_modules/assertion-error/package.json
    ./frontend/node_modules/assertion-error/README.md
    ./frontend/node_modules/assertion-error/index.js
    ./frontend/node_modules/assertion-error/LICENSE
    ./frontend/node_modules/escape-string-regexp/index.d.ts
    ./frontend/node_modules/escape-string-regexp/package.json
    ./frontend/node_modules/escape-string-regexp/readme.md
    ./frontend/node_modules/escape-string-regexp/index.js
    ./frontend/node_modules/escape-string-regexp/license
    ./frontend/node_modules/browserslist/browser.js
    ./frontend/node_modules/browserslist/index.d.ts
    ./frontend/node_modules/browserslist/cli.js
    ./frontend/node_modules/browserslist/package.json
    ./frontend/node_modules/browserslist/parse.js
    ./frontend/node_modules/browserslist/node.js
    ./frontend/node_modules/browserslist/README.md
    ./frontend/node_modules/browserslist/error.js
    ./frontend/node_modules/browserslist/index.js
    ./frontend/node_modules/browserslist/LICENSE
    ./frontend/node_modules/browserslist/error.d.ts
    ./frontend/node_modules/escalade/sync/index.d.ts
    ./frontend/node_modules/escalade/sync/index.mjs
    ./frontend/node_modules/escalade/sync/index.js
    ./frontend/node_modules/escalade/sync/index.d.mts
    ./frontend/node_modules/escalade/package.json
    ./frontend/node_modules/escalade/readme.md
    ./frontend/node_modules/escalade/index.d.mts
    ./frontend/node_modules/source-map-js/lib/source-map-generator.js
    ./frontend/node_modules/source-map-js/lib/source-node.js
    ./frontend/node_modules/source-map-js/lib/array-set.js
    ./frontend/node_modules/source-map-js/lib/base64.js
    ./frontend/node_modules/source-map-js/lib/binary-search.js
    ./frontend/node_modules/source-map-js/lib/mapping-list.js
    ./frontend/node_modules/source-map-js/lib/base64-vlq.js
    ./frontend/node_modules/source-map-js/lib/source-map-consumer.d.ts
    ./frontend/node_modules/source-map-js/lib/source-node.d.ts
    ./frontend/node_modules/source-map-js/lib/util.js
    ./frontend/node_modules/source-map-js/lib/quick-sort.js
    ./frontend/node_modules/source-map-js/lib/source-map-consumer.js
    ./frontend/node_modules/source-map-js/lib/source-map-generator.d.ts
    ./frontend/node_modules/source-map-js/source-map.js
    ./frontend/node_modules/source-map-js/package.json
    ./frontend/node_modules/source-map-js/README.md
    ./frontend/node_modules/source-map-js/LICENSE
    ./frontend/node_modules/@vitejs/plugin-react/package.json
    ./frontend/node_modules/@vitejs/plugin-react/README.md
    ./frontend/node_modules/html-encoding-sniffer/lib/html-encoding-sniffer.js
    ./frontend/node_modules/html-encoding-sniffer/package.json
    ./frontend/node_modules/html-encoding-sniffer/README.md
    ./frontend/node_modules/vitest/reporters.d.ts
    ./frontend/node_modules/vitest/import-meta.d.ts
    ./frontend/node_modules/vitest/optional-types.d.ts
    ./frontend/node_modules/vitest/node.d.ts
    ./frontend/node_modules/vitest/importMeta.d.ts
    ./frontend/node_modules/vitest/vitest.mjs
    ./frontend/node_modules/vitest/coverage.d.ts
    ./frontend/node_modules/vitest/index.cjs
    ./frontend/node_modules/vitest/jsdom.d.ts
    ./frontend/node_modules/vitest/package.json
    ./frontend/node_modules/globals/index.d.ts
    ./frontend/node_modules/globals/package.json
    ./frontend/node_modules/globals/readme.md
    ./frontend/node_modules/globals/index.js
    ./frontend/node_modules/globals/license
    ./frontend/node_modules/globals/globals.json
    ./frontend/node_modules/react-is/cjs/react-is.production.min.js
    ./frontend/node_modules/react-is/cjs/react-is.development.js
    ./frontend/node_modules/react-is/package.json
    ./frontend/node_modules/react-is/README.md
    ./frontend/node_modules/react-is/index.js
    ./infra/persistence/README.md
    ./infra/README.md
    ./frontend/node_modules/tinyglobby/dist/index.mjs
    ./frontend/node_modules/tinyglobby/dist/index.cjs
    ./frontend/node_modules/tinyglobby/dist/index.d.cts
    ./frontend/node_modules/tinyglobby/dist/index.d.mts
    ./frontend/node_modules/tinyglobby/LICENSE
    ./frontend/Dockerfile
    ./frontend/tsconfig.app.json
    ./frontend/index.html
    ./infra/compose/README.md
    ./frontend/node_modules/vitest/browser/context.js
    ./frontend/node_modules/vitest/browser/context.d.ts
    ./frontend/node_modules/vitest/README.md
    ./frontend/node_modules/vitest/worker.d.ts
    ./frontend/node_modules/vitest/suite.d.ts
    ./frontend/node_modules/vitest/snapshot.d.ts
    ./frontend/node_modules/vitest/suppress-warnings.cjs
    ./frontend/node_modules/vitest/runners.d.ts
    ./frontend/node_modules/vitest/index.d.cts
    ./frontend/node_modules/vitest/config.d.ts
    ./frontend/node_modules/@vitejs/plugin-react/dist/index.d.ts
    ./frontend/node_modules/@vitejs/plugin-react/dist/index.js
    ./frontend/node_modules/@vitejs/plugin-react/dist/refresh-runtime.js
    ./frontend/node_modules/@vitejs/plugin-react/LICENSE
    ./frontend/node_modules/escalade/dist/index.mjs
    ./frontend/node_modules/escalade/dist/index.js
    ./frontend/node_modules/escalade/license
    ./test-assets/README.md
    ./frontend/node_modules/lightningcss/node/ast.d.ts
    ./frontend/node_modules/lightningcss/node/index.d.ts
    ./frontend/node_modules/lightningcss/node/ast.js.flow
    ./frontend/node_modules/lightningcss/node/targets.js.flow
    ./frontend/node_modules/lightningcss/node/index.mjs
    ./frontend/node_modules/lightningcss/node/browserslistToTargets.js
    ./frontend/node_modules/lightningcss/node/index.js.flow
    ./frontend/node_modules/lightningcss/node/composeVisitors.js
    ./frontend/node_modules/lightningcss/node/index.js
    ./frontend/node_modules/lightningcss/node/targets.d.ts
    ./frontend/node_modules/lightningcss/node/flags.js
    ./frontend/node_modules/lightningcss/package.json
    ./frontend/node_modules/lightningcss/README.md
    ./frontend/node_modules/lightningcss/LICENSE
    ./frontend/node_modules/@vitejs/plugin-react/types/preamble.d.ts
    ./frontend/node_modules/@vitejs/plugin-react/types/optionalTypes.d.ts
    ./frontend/node_modules/obug/package.json
    ./frontend/node_modules/obug/README.md
    ./frontend/node_modules/react-is/umd/react-is.production.min.js
    ./frontend/node_modules/react-is/umd/react-is.development.js
    ./frontend/node_modules/react-is/LICENSE
    ./frontend/node_modules/react-is/build-info.json
    ./frontend/node_modules/@types/json-schema/index.d.ts
    ./frontend/node_modules/@types/json-schema/package.json
    ./frontend/node_modules/@types/json-schema/README.md
    ./frontend/node_modules/@types/json-schema/LICENSE
    ./frontend/node_modules/callsites/index.d.ts
    ./frontend/node_modules/callsites/package.json
    ./frontend/node_modules/callsites/readme.md
    ./frontend/node_modules/callsites/index.js
    ./frontend/node_modules/callsites/license
    ./frontend/node_modules/vitest/dist/config.cjs
    ./frontend/node_modules/vitest/dist/reporters.d.ts
    ./frontend/node_modules/vitest/dist/runners.js
    ./frontend/node_modules/vitest/dist/environments.js
    ./frontend/node_modules/vitest/dist/browser.d.ts
    ./frontend/node_modules/vitest/dist/nodejs-worker-loader.js
    ./frontend/node_modules/vitest/dist/node.d.ts
    ./frontend/node_modules/vitest/dist/reporters.js
    ./frontend/node_modules/vitest/dist/browser.js
    ./frontend/node_modules/vitest/dist/index.d.ts
    ./frontend/node_modules/vitest/dist/cli.js
    ./frontend/node_modules/lightningcss-darwin-arm64/package.json
    ./frontend/node_modules/lightningcss-darwin-arm64/README.md
    ./frontend/node_modules/lightningcss-darwin-arm64/LICENSE
    ./frontend/node_modules/lightningcss-darwin-arm64/lightningcss.darwin-arm64.node
    ./frontend/node_modules/node-releases/data/release-schedule/release-schedule.json
    ./frontend/node_modules/estree-walker/src/async.js
    ./frontend/node_modules/estree-walker/src/index.js
    ./frontend/node_modules/estree-walker/src/sync.js
    ./frontend/node_modules/estree-walker/src/walker.js
    ./frontend/node_modules/estree-walker/package.json
    ./frontend/node_modules/estree-walker/README.md
    ./frontend/node_modules/estree-walker/LICENSE
    ./frontend/node_modules/css-tree/cjs/walker/create.cjs
    ./frontend/node_modules/css-tree/cjs/walker/index.cjs
    ./frontend/node_modules/glob-parent/package.json
    ./frontend/node_modules/glob-parent/README.md
    ./frontend/node_modules/glob-parent/index.js
    ./frontend/node_modules/glob-parent/LICENSE
    ./frontend/node_modules/chalk/index.d.ts
    ./frontend/node_modules/chalk/package.json
    ./frontend/node_modules/chalk/readme.md
    ./frontend/node_modules/estree-walker/types/async.d.ts
    ./frontend/node_modules/estree-walker/types/index.d.ts
    ./frontend/node_modules/estree-walker/types/walker.d.ts
    ./frontend/node_modules/estree-walker/types/sync.d.ts
    ./frontend/node_modules/obug/dist/browser.min.js
    ./frontend/node_modules/obug/dist/browser.d.ts
    ./frontend/node_modules/obug/dist/node.d.ts
    ./frontend/node_modules/obug/dist/browser.js
    ./frontend/node_modules/obug/dist/node.js
    ./frontend/node_modules/obug/dist/core.d.ts
    ./frontend/node_modules/obug/dist/core.js
    ./frontend/node_modules/obug/LICENSE
    ./frontend/node_modules/@types/react/index.d.ts
    ./frontend/node_modules/node-releases/data/processed/envs.json
    ./frontend/node_modules/node-releases/package.json
    ./frontend/node_modules/node-releases/README.md
    ./frontend/node_modules/node-releases/LICENSE
    ./frontend/node_modules/min-indent/package.json
    ./frontend/node_modules/min-indent/readme.md
    ./frontend/node_modules/min-indent/index.js
    ./frontend/node_modules/min-indent/license
    ./frontend/node_modules/punycode/package.json
    ./frontend/node_modules/vitest/dist/workers/forks.js
    ./frontend/node_modules/punycode/README.md
    ./frontend/node_modules/css-tree/cjs/syntax/create.cjs
    ./frontend/node_modules/punycode/LICENSE-MIT.txt
    ./frontend/node_modules/punycode/punycode.js
    ./frontend/node_modules/punycode/punycode.es6.js
    ./frontend/node_modules/vitest/dist/workers/vmForks.js
    ./frontend/node_modules/vitest/dist/workers/threads.js
    ./frontend/node_modules/vitest/dist/workers/runVmTests.js
    ./frontend/node_modules/vitest/dist/workers/vmThreads.js
    ./frontend/node_modules/vitest/dist/coverage.d.ts
    ./frontend/node_modules/vitest/dist/path.js
    ./frontend/node_modules/vitest/dist/module-evaluator.d.ts
    ./frontend/node_modules/vitest/dist/snapshot.js
    ./frontend/node_modules/vitest/dist/module-evaluator.js
    ./frontend/node_modules/vitest/dist/node.js
    ./frontend/node_modules/@rolldown/pluginutils/package.json
    ./frontend/node_modules/@types/react/ts5.0/index.d.ts
    ./frontend/node_modules/@rolldown/pluginutils/README.md
    ./frontend/node_modules/@types/react/ts5.0/global.d.ts
    ./frontend/node_modules/@types/react/ts5.0/experimental.d.ts
    ./frontend/node_modules/@types/react/ts5.0/canary.d.ts
    ./frontend/node_modules/@types/react/ts5.0/jsx-runtime.d.ts
    ./frontend/node_modules/@types/react/ts5.0/jsx-dev-runtime.d.ts
    ./frontend/node_modules/@types/react/global.d.ts
    ./frontend/node_modules/@types/react/package.json
    ./frontend/node_modules/@types/react/README.md
    ./frontend/node_modules/@types/react/experimental.d.ts
    ./frontend/node_modules/@types/react/canary.d.ts
    ./frontend/node_modules/@types/react/LICENSE
    ./frontend/node_modules/@types/react/jsx-runtime.d.ts
    ./frontend/node_modules/@types/react/compiler-runtime.d.ts
    ./frontend/node_modules/@types/react/jsx-dev-runtime.d.ts
    ./frontend/node_modules/@types/aria-query/index.d.ts
    ./frontend/node_modules/@types/aria-query/package.json
    ./frontend/node_modules/@types/aria-query/README.md
    ./frontend/node_modules/@types/aria-query/LICENSE
    ./frontend/node_modules/chalk/source/templates.js
    ./frontend/node_modules/chalk/source/index.js
    ./frontend/node_modules/chalk/source/util.js
    ./frontend/node_modules/chalk/license
    ./frontend/node_modules/debug/src/browser.js
    ./frontend/node_modules/debug/src/common.js
    ./frontend/node_modules/debug/src/node.js
    ./frontend/node_modules/debug/src/index.js
    ./frontend/node_modules/debug/package.json
    ./frontend/node_modules/debug/README.md
    ./frontend/node_modules/debug/LICENSE
    ./frontend/node_modules/eslint-scope/lib/definition.js
    ./frontend/node_modules/eslint-scope/lib/reference.js
    ./frontend/node_modules/eslint-scope/lib/variable.js
    ./frontend/node_modules/eslint-scope/lib/pattern-visitor.js
    ./frontend/node_modules/eslint-scope/lib/scope.js
    ./frontend/node_modules/eslint-scope/lib/scope-manager.js
    ./frontend/node_modules/eslint-scope/lib/version.js
    ./frontend/node_modules/eslint-scope/lib/index.js
    ./frontend/node_modules/eslint-scope/lib/referencer.js
    ./frontend/node_modules/eslint-scope/lib/assert.js
    ./frontend/node_modules/eslint-scope/package.json
    ./frontend/node_modules/eslint-scope/README.md
    ./frontend/node_modules/@types/node/net.d.ts
    ./frontend/node_modules/require-from-string/package.json
    ./frontend/node_modules/require-from-string/readme.md
    ./frontend/node_modules/require-from-string/index.js
    ./frontend/node_modules/require-from-string/license
    ./frontend/node_modules/zod/src/index.ts
    ./frontend/node_modules/@types/chai/register-should.d.ts
    ./frontend/node_modules/@types/chai/index.d.ts
    ./frontend/node_modules/@types/chai/package.json
    ./frontend/node_modules/@types/chai/README.md
    ./frontend/node_modules/@types/chai/LICENSE
    ./frontend/node_modules/eslint-scope/dist/eslint-scope.cjs
    ./frontend/node_modules/eslint-scope/LICENSE
    ./frontend/node_modules/find-up/index.d.ts
    ./frontend/node_modules/find-up/package.json
    ./frontend/node_modules/find-up/readme.md
    ./frontend/node_modules/find-up/index.js
    ./frontend/node_modules/find-up/license
    ./frontend/node_modules/prelude-ls/lib/Obj.js
    ./frontend/node_modules/prelude-ls/lib/Func.js
    ./frontend/node_modules/prelude-ls/lib/List.js
    ./frontend/node_modules/prelude-ls/lib/index.js
    ./frontend/node_modules/prelude-ls/lib/Str.js
    ./frontend/node_modules/prelude-ls/lib/Num.js
    ./frontend/node_modules/prelude-ls/package.json
    ./frontend/node_modules/@rolldown/pluginutils/dist/index.d.ts
    ./frontend/node_modules/prelude-ls/README.md
    ./frontend/node_modules/prelude-ls/CHANGELOG.md
    ./frontend/node_modules/prelude-ls/LICENSE
    ./frontend/node_modules/css-tree/cjs/syntax/atrule/font-face.cjs
    ./frontend/node_modules/css-tree/cjs/syntax/atrule/starting-style.cjs
    ./frontend/node_modules/css-tree/cjs/syntax/atrule/scope.cjs
    ./frontend/node_modules/css-tree/cjs/syntax/atrule/index.cjs
    ./frontend/node_modules/css-tree/cjs/syntax/atrule/import.cjs
    ./frontend/node_modules/css-tree/cjs/syntax/atrule/container.cjs
    ./frontend/node_modules/css-tree/cjs/syntax/atrule/media.cjs
    ./frontend/node_modules/css-tree/cjs/syntax/atrule/page.cjs
    ./frontend/node_modules/css-tree/cjs/syntax/atrule/nest.cjs
    ./frontend/node_modules/css-tree/cjs/syntax/atrule/supports.cjs
    ./frontend/node_modules/css-tree/cjs/syntax/atrule/layer.cjs
    ./frontend/node_modules/@types/node/fs/promises.d.ts
    ./frontend/node_modules/vitest/dist/chunks/creator.DgVhQm5q.js
    ./frontend/node_modules/vitest/dist/chunks/evaluatedModules.Dg1zASAC.js
    ./frontend/node_modules/vitest/dist/chunks/cli-api.Bxr1Nn49.js
    ./frontend/node_modules/vitest/dist/chunks/coverage.kqM80boz.js
    ./frontend/node_modules/vitest/dist/chunks/test.p_J6dB8a.js
    ./frontend/node_modules/vitest/dist/chunks/utils.DK8FXp4T.js
    ./frontend/node_modules/vitest/dist/chunks/nativeModuleMocker.BRN2oBJd.js
    ./frontend/node_modules/vitest/dist/chunks/traces.d.402V_yFI.d.ts
    ./frontend/node_modules/vitest/dist/chunks/init-forks.UV3ZQGQH.js
    ./frontend/node_modules/vitest/dist/chunks/rpc.MzXet3jl.js
    ./frontend/node_modules/vitest/dist/chunks/inspector.CvyFGlXm.js
    ./frontend/node_modules/vitest/dist/chunks/nativeModuleRunner.BIakptoF.js
    ./frontend/node_modules/vitest/dist/chunks/coverage.d.BZtK59WP.d.ts
    ./frontend/node_modules/vitest/dist/chunks/base.BPik1OqN.js
    ./frontend/node_modules/vitest/dist/chunks/modules.BJuCwlRJ.js
    ./frontend/node_modules/vitest/dist/chunks/constants.CPYnjOGj.js
    ./frontend/node_modules/vitest/dist/chunks/env.D4Lgay0q.js
    ./frontend/node_modules/vitest/dist/chunks/suite.d.udJtyAgw.d.ts
    ./frontend/node_modules/vitest/dist/chunks/index.og1WyBLx.js
    ./frontend/node_modules/vitest/dist/chunks/native.DPzPHdi5.js
    ./frontend/node_modules/vitest/dist/chunks/node.COQbm6gK.js
    ./frontend/node_modules/vitest/dist/chunks/index.CMESou6r.js
    ./frontend/node_modules/vitest/dist/chunks/evaluatedModules.d.BxJ5omdx.d.ts
    ./frontend/node_modules/vitest/dist/chunks/init-threads.D3eCsY76.js
    ./frontend/node_modules/vitest/dist/chunks/defaults.9aQKnqFk.js
    ./frontend/node_modules/vitest/dist/chunks/browser.d.BMOr_Kmk.d.ts
    ./frontend/node_modules/vitest/dist/chunks/index.BCY_7LL2.js
    ./frontend/node_modules/vitest/dist/chunks/coverage.CTzCuANN.js
    ./frontend/node_modules/vitest/dist/chunks/acorn.B2iPLyUM.js
    ./frontend/node_modules/vitest/dist/chunks/benchmark.CX_oY03V.js
    ./frontend/node_modules/vitest/dist/chunks/reporters.d.B0uk8id2.d.ts
    ./frontend/node_modules/vitest/dist/chunks/plugin.d.BWbK_Jpw.d.ts
    ./frontend/node_modules/vitest/dist/chunks/index.DOa3dzoN.js
    ./frontend/node_modules/vitest/dist/chunks/utils.BX5Fg8C4.js
    ./frontend/node_modules/vitest/dist/chunks/worker.d.BT5j8dyR.d.ts
    ./frontend/node_modules/vitest/dist/chunks/environment.d.CrsxCzP1.d.ts
    ./frontend/node_modules/vitest/dist/chunks/index.DC7d2Pf8.js
    ./frontend/node_modules/vitest/dist/chunks/vm.BvVhnZPV.js
    ./frontend/node_modules/vitest/dist/chunks/index.Chj8NDwU.js
    ./frontend/node_modules/vitest/dist/chunks/setup-common.2wZXQUjS.js
    ./frontend/node_modules/vitest/dist/chunks/config.d.Cz9kPrQs.d.ts
    ./frontend/node_modules/vitest/dist/chunks/index.0GYC6HAu.js
    ./frontend/node_modules/vitest/dist/chunks/benchmark.d.DAaHLpsq.d.ts
    ./frontend/node_modules/vitest/dist/chunks/_commonjsHelpers.D26ty3Ew.js
    ./frontend/node_modules/vitest/dist/chunks/console.3WNpx0tS.js
    ./frontend/node_modules/vitest/dist/chunks/cac.DRKYQDPl.js
    ./frontend/node_modules/vitest/dist/chunks/globals.CVqIbOyt.js
    ./frontend/node_modules/vitest/dist/chunks/init.D98-gwRW.js
    ./frontend/node_modules/vitest/dist/chunks/traces.DT5aQ62U.js
    ./frontend/node_modules/vitest/dist/chunks/index.nZ2xqFgD.js
    ./frontend/node_modules/vitest/dist/chunks/global.d.x-ILCfAE.d.ts
    ./frontend/node_modules/vitest/dist/chunks/startVitestModuleRunner.bRl2_oI_.js
    ./frontend/node_modules/vitest/dist/chunks/rpc.d.BFMWpdph.d.ts
    ./frontend/node_modules/vitest/dist/worker.d.ts
    ./frontend/node_modules/vitest/dist/suite.d.ts
    ./frontend/node_modules/vitest/dist/config.js
    ./frontend/node_modules/vitest/dist/snapshot.d.ts
    ./frontend/node_modules/vitest/dist/suite.js
    ./frontend/node_modules/vitest/dist/index.js
    ./frontend/node_modules/vitest/dist/runners.d.ts
    ./frontend/node_modules/vitest/dist/worker.js
    ./frontend/node_modules/vitest/dist/config.d.ts
    ./frontend/node_modules/vitest/dist/environments.d.ts
    ./frontend/node_modules/vitest/dist/coverage.js
    ./frontend/node_modules/vitest/dist/spy.js
    ./frontend/node_modules/vitest/dist/runtime.js
    ./frontend/node_modules/vitest/dist/runtime.d.ts
    ./frontend/node_modules/vitest/optional-runtime-types.d.ts
    ./frontend/node_modules/vitest/environments.d.ts
    ./frontend/node_modules/vitest/mocker.d.ts
    ./frontend/node_modules/vitest/LICENSE.md
    ./frontend/node_modules/vitest/globals.d.ts
    ./frontend/node_modules/electron-to-chromium/full-versions.js
    ./frontend/node_modules/electron-to-chromium/chromium-versions.js
    ./frontend/node_modules/electron-to-chromium/package.json
    ./frontend/node_modules/electron-to-chromium/chromium-versions.json
    ./frontend/node_modules/electron-to-chromium/versions.js
    ./frontend/node_modules/electron-to-chromium/README.md
    ./frontend/node_modules/electron-to-chromium/full-chromium-versions.json
    ./frontend/node_modules/electron-to-chromium/index.js
    ./frontend/node_modules/electron-to-chromium/versions.json
    ./frontend/node_modules/electron-to-chromium/full-chromium-versions.js
    ./frontend/node_modules/electron-to-chromium/LICENSE
    ./frontend/node_modules/electron-to-chromium/full-versions.json
    ./frontend/node_modules/@rolldown/pluginutils/dist/filter/filter-vite-plugins.d.ts
    ./frontend/node_modules/@rolldown/pluginutils/dist/filter/index.d.ts
    ./frontend/node_modules/@rolldown/pluginutils/dist/filter/filter-vite-plugins.js
    ./frontend/node_modules/@rolldown/pluginutils/dist/filter/composable-filters.js
    ./frontend/node_modules/@rolldown/pluginutils/dist/filter/index.js
    ./frontend/node_modules/@rolldown/pluginutils/dist/filter/simple-filters.js
    ./frontend/node_modules/@rolldown/pluginutils/dist/filter/composable-filters.d.ts
    ./frontend/node_modules/@rolldown/pluginutils/dist/filter/simple-filters.d.ts
    ./frontend/node_modules/@rolldown/pluginutils/dist/utils.js
    ./frontend/node_modules/@rolldown/pluginutils/dist/utils.d.ts
    ./frontend/node_modules/@rolldown/pluginutils/dist/index.js
    ./frontend/node_modules/@rolldown/pluginutils/LICENSE
    ./frontend/node_modules/ms/package.json
    ./frontend/node_modules/ms/readme.md
    ./frontend/node_modules/ms/index.js
    ./frontend/node_modules/ms/license.md
    ./frontend/node_modules/imurmurhash/imurmurhash.min.js
    ./frontend/node_modules/imurmurhash/package.json
    ./frontend/node_modules/imurmurhash/README.md
    ./frontend/node_modules/imurmurhash/imurmurhash.js
    ./frontend/node_modules/ignore/LICENSE-MIT
    ./frontend/node_modules/ignore/index.d.ts
    ./frontend/node_modules/ignore/package.json
    ./frontend/node_modules/ignore/README.md
    ./frontend/node_modules/ignore/legacy.js
    ./frontend/node_modules/ignore/index.js
    ./frontend/node_modules/@rolldown/binding-darwin-arm64/rolldown-binding.darwin-arm64.node
    ./frontend/node_modules/@rolldown/binding-darwin-arm64/package.json
    ./frontend/node_modules/@rolldown/binding-darwin-arm64/README.md
    ./frontend/node_modules/lru-cache/package.json
    ./frontend/node_modules/lru-cache/README.md
    ./frontend/node_modules/lru-cache/index.js
    ./frontend/node_modules/lru-cache/LICENSE
    ./frontend/node_modules/react-router/package.json
    ./frontend/node_modules/react-router/README.md
    ./frontend/node_modules/typescript-eslint/package.json
    ./frontend/node_modules/typescript-eslint/README.md
    ./frontend/node_modules/esutils/lib/ast.js
    ./frontend/node_modules/esutils/lib/utils.js
    ./frontend/node_modules/esutils/lib/keyword.js
    ./frontend/node_modules/esutils/lib/code.js
    ./frontend/node_modules/esutils/package.json
    ./frontend/node_modules/esutils/LICENSE.BSD
    ./frontend/node_modules/esutils/README.md
    ./frontend/node_modules/@types/node/dns/promises.d.ts
    ./frontend/node_modules/css-tree/cjs/syntax/node/Combinator.cjs
    ./frontend/node_modules/css-tree/cjs/syntax/node/Value.cjs
    ./frontend/node_modules/css-tree/cjs/syntax/node/MediaQuery.cjs
    ./frontend/node_modules/css-tree/cjs/syntax/node/index-generate.cjs
    ./frontend/node_modules/css-tree/cjs/syntax/node/Dimension.cjs
    ./frontend/node_modules/css-tree/cjs/syntax/node/GeneralEnclosed.cjs
    ./frontend/node_modules/css-tree/cjs/syntax/node/Function.cjs
    ./frontend/node_modules/css-tree/cjs/syntax/node/Raw.cjs
    ./frontend/node_modules/css-tree/cjs/syntax/node/Atrule.cjs
    ./frontend/node_modules/css-tree/cjs/syntax/node/Scope.cjs
    ./frontend/node_modules/css-tree/cjs/syntax/node/Brackets.cjs
    ./frontend/node_modules/css-tree/cjs/syntax/node/PseudoClassSelector.cjs
    ./frontend/node_modules/css-tree/cjs/syntax/node/PseudoElementSelector.cjs
    ./frontend/node_modules/css-tree/cjs/syntax/node/LayerList.cjs
    ./frontend/node_modules/css-tree/cjs/syntax/node/FeatureFunction.cjs
    ./frontend/node_modules/css-tree/cjs/syntax/node/TypeSelector.cjs
    ./frontend/node_modules/css-tree/cjs/syntax/node/CDC.cjs
    ./frontend/node_modules/css-tree/cjs/syntax/node/SelectorList.cjs
    ./frontend/node_modules/css-tree/cjs/syntax/node/Feature.cjs
    ./frontend/node_modules/css-tree/cjs/syntax/node/Selector.cjs
    ./frontend/node_modules/css-tree/cjs/syntax/node/Rule.cjs
    ./frontend/node_modules/css-tree/cjs/syntax/node/MediaQueryList.cjs
    ./frontend/node_modules/css-tree/cjs/syntax/node/Percentage.cjs
    ./frontend/node_modules/css-tree/cjs/syntax/node/Number.cjs
    ./frontend/node_modules/css-tree/cjs/syntax/node/index.cjs
    ./frontend/node_modules/css-tree/cjs/syntax/node/IdSelector.cjs
    ./frontend/node_modules/css-tree/cjs/syntax/node/Parentheses.cjs
    ./frontend/node_modules/css-tree/cjs/syntax/node/Identifier.cjs
    ./frontend/node_modules/css-tree/cjs/syntax/node/Hash.cjs
    ./frontend/node_modules/css-tree/cjs/syntax/node/NestingSelector.cjs
    ./frontend/node_modules/css-tree/cjs/syntax/node/DeclarationList.cjs
    ./frontend/node_modules/css-tree/cjs/syntax/node/Nth.cjs
    ./frontend/node_modules/css-tree/cjs/syntax/node/Condition.cjs
    ./frontend/node_modules/css-tree/cjs/syntax/node/index-parse-selector.cjs
    ./frontend/node_modules/css-tree/cjs/syntax/node/StyleSheet.cjs
    ./frontend/node_modules/css-tree/cjs/syntax/node/ClassSelector.cjs
    ./frontend/node_modules/css-tree/cjs/syntax/node/AtrulePrelude.cjs
    ./frontend/node_modules/css-tree/cjs/syntax/node/WhiteSpace.cjs
    ./frontend/node_modules/css-tree/cjs/syntax/node/CDO.cjs
    ./frontend/node_modules/css-tree/cjs/syntax/node/index-parse.cjs
    ./frontend/node_modules/css-tree/cjs/syntax/node/String.cjs
    ./frontend/node_modules/css-tree/cjs/syntax/node/Comment.cjs
    ./frontend/node_modules/css-tree/cjs/syntax/node/AttributeSelector.cjs
    ./frontend/node_modules/css-tree/cjs/syntax/node/Declaration.cjs
    ./frontend/node_modules/css-tree/cjs/syntax/node/AnPlusB.cjs
    ./frontend/node_modules/css-tree/cjs/syntax/node/UnicodeRange.cjs
    ./frontend/node_modules/css-tree/cjs/syntax/node/SupportsDeclaration.cjs
    ./frontend/node_modules/css-tree/cjs/syntax/node/Ratio.cjs
    ./frontend/node_modules/css-tree/cjs/syntax/node/Operator.cjs
    ./frontend/node_modules/css-tree/cjs/syntax/node/Block.cjs
    ./frontend/node_modules/css-tree/cjs/syntax/node/Layer.cjs
    ./frontend/node_modules/css-tree/cjs/syntax/node/Url.cjs
    ./frontend/node_modules/css-tree/cjs/syntax/node/FeatureRange.cjs
    ./frontend/node_modules/css-tree/cjs/syntax/index.cjs
    ./frontend/node_modules/zod/src/v3/helpers/partialUtil.ts
    ./frontend/node_modules/zod/src/v3/helpers/util.ts
    ./frontend/node_modules/zod/src/v3/helpers/enumUtil.ts
    ./frontend/node_modules/zod/src/v3/helpers/parseUtil.ts
    ./frontend/node_modules/zod/src/v3/helpers/typeAliases.ts
    ./frontend/node_modules/zod/src/v3/helpers/errorUtil.ts
    ./frontend/node_modules/zod/src/v3/index.ts
    ./frontend/node_modules/zod/src/v3/ZodError.ts
    ./frontend/node_modules/strip-json-comments/index.d.ts
    ./frontend/node_modules/strip-json-comments/package.json
    ./frontend/node_modules/strip-json-comments/readme.md
    ./frontend/node_modules/strip-json-comments/index.js
    ./frontend/node_modules/strip-json-comments/license
    ./frontend/node_modules/typescript-eslint/dist/index.d.ts
    ./frontend/node_modules/typescript-eslint/dist/getTSConfigRootDirFromStack.js
    ./frontend/node_modules/typescript-eslint/dist/compatibility-types.js
    ./frontend/node_modules/typescript-eslint/dist/tsconfig.build.tsbuildinfo
    ./frontend/node_modules/typescript-eslint/dist/getTSConfigRootDirFromStack.d.ts
    ./frontend/node_modules/typescript-eslint/dist/index.js
    ./frontend/node_modules/typescript-eslint/dist/config-helper.js
    ./frontend/node_modules/typescript-eslint/dist/compatibility-types.d.ts
    ./frontend/node_modules/typescript-eslint/dist/config-helper.d.ts
    ./frontend/node_modules/typescript-eslint/LICENSE
    ./frontend/node_modules/flatted/cjs/package.json
    ./frontend/node_modules/flatted/cjs/index.js
    ./frontend/node_modules/flatted/es.js
    ./frontend/node_modules/flatted/min.js
    ./frontend/node_modules/flatted/package.json
    ./frontend/node_modules/flatted/README.md
    ./frontend/node_modules/tldts/src/data/trie.ts
    ./frontend/node_modules/tldts/src/suffix-trie.ts
    ./frontend/node_modules/tldts/index.ts
    ./frontend/node_modules/tldts/package.json
    ./frontend/node_modules/tldts/README.md
    ./frontend/node_modules/std-env/LICENCE
    ./frontend/node_modules/zod/src/v3/benchmarks/ipv4.ts
    ./frontend/node_modules/std-env/package.json
    ./frontend/node_modules/zod/src/v3/benchmarks/index.ts
    ./frontend/node_modules/std-env/README.md
    ./frontend/node_modules/zod/src/v3/benchmarks/object.ts
    ./frontend/node_modules/zod/src/v3/benchmarks/primitives.ts
    ./frontend/node_modules/zod/src/v3/benchmarks/discriminatedUnion.ts
    ./frontend/node_modules/zod/src/v3/benchmarks/realworld.ts
    ./frontend/node_modules/zod/src/v3/benchmarks/string.ts
    ./frontend/node_modules/zod/src/v3/benchmarks/datetime.ts
    ./frontend/node_modules/zod/src/v3/benchmarks/union.ts
    ./frontend/node_modules/zod/src/v3/types.ts
    ./frontend/node_modules/zod/src/v3/standard-schema.ts
    ./frontend/node_modules/ts-api-utils/lib/index.d.ts
    ./frontend/node_modules/ts-api-utils/lib/index.cjs
    ./frontend/node_modules/ts-api-utils/lib/index.js
    ./frontend/node_modules/ts-api-utils/lib/index.d.cts
    ./frontend/node_modules/ts-api-utils/package.json
    ./frontend/node_modules/ts-api-utils/README.md
    ./frontend/node_modules/ts-api-utils/LICENSE.md
    ./frontend/node_modules/css-tree/cjs/syntax/function/var.cjs
    ./frontend/node_modules/css-tree/cjs/syntax/function/expression.cjs
    ./frontend/node_modules/react-router/dist/production/index-react-server.mjs
    ./frontend/node_modules/react-router/dist/production/index.d.ts
    ./frontend/node_modules/react-router/dist/production/routeModules-BRrCYrSL.d.mts
    ./frontend/node_modules/react-router/dist/production/index-react-server-client.js
    ./frontend/node_modules/react-router/dist/production/dom-export.js
    ./frontend/node_modules/prettier/doc.js
    ./frontend/node_modules/prettier/index.d.ts
    ./frontend/node_modules/prettier/index.mjs
    ./frontend/node_modules/prettier/index.cjs
    ./frontend/node_modules/prettier/doc.mjs
    ./frontend/node_modules/prettier/doc.d.ts
    ./frontend/node_modules/prettier/package.json
    ./frontend/node_modules/prettier/README.md
    ./frontend/node_modules/prettier/standalone.d.ts
    ./frontend/node_modules/prettier/standalone.mjs
    ./frontend/node_modules/@types/node/ts5.6/index.d.ts
    ./frontend/node_modules/@types/node/ts5.6/globals.typedarray.d.ts
    ./frontend/node_modules/@types/node/ts5.6/buffer.buffer.d.ts
    ./frontend/node_modules/flatted/php/flatted.php
    ./frontend/node_modules/flatted/index.js
    ./frontend/node_modules/flatted/esm.js
    ./frontend/node_modules/@asamuzakjp/dom-selector/src/index.js
    ./frontend/node_modules/std-env/dist/index.mjs
    ./frontend/node_modules/std-env/dist/index.d.mts
    ./frontend/node_modules/css-tree/cjs/version.cjs
    ./frontend/node_modules/csstype/index.d.ts
    ./frontend/node_modules/csstype/package.json
    ./frontend/node_modules/csstype/index.js.flow
    ./frontend/node_modules/csstype/README.md
    ./frontend/node_modules/csstype/LICENSE
    ./frontend/node_modules/zod/src/v3/tests/async-refinements.test.ts
    ./frontend/node_modules/zod/src/v3/tests/array.test.ts
    ./frontend/node_modules/zod/src/v3/tests/promise.test.ts
    ./frontend/node_modules/zod/src/v3/tests/object.test.ts
    ./frontend/node_modules/zod/src/v3/tests/readonly.test.ts
    ./frontend/node_modules/zod/src/v3/tests/all-errors.test.ts
    ./frontend/node_modules/zod/src/v3/tests/standard-schema.test.ts
    ./frontend/node_modules/zod/src/v3/tests/nativeEnum.test.ts
    ./frontend/node_modules/zod/src/v3/tests/error.test.ts
    ./frontend/node_modules/zod/src/v3/tests/preprocess.test.ts
    ./frontend/node_modules/zod/src/v3/tests/complex.test.ts
    ./frontend/node_modules/zod/src/v3/tests/instanceof.test.ts
    ./frontend/node_modules/zod/src/v3/tests/map.test.ts
    ./frontend/node_modules/zod/src/v3/tests/optional.test.ts
    ./frontend/node_modules/zod/src/v3/tests/validations.test.ts
    ./frontend/node_modules/zod/src/v3/tests/refine.test.ts
    ./frontend/node_modules/zod/src/v3/tests/async-parsing.test.ts
    ./frontend/node_modules/zod/src/v3/tests/primitive.test.ts
    ./frontend/node_modules/zod/src/v3/tests/number.test.ts
    ./frontend/node_modules/zod/src/v3/tests/nullable.test.ts
    ./frontend/node_modules/zod/src/v3/tests/partials.test.ts
    ./frontend/node_modules/zod/src/v3/tests/Mocker.ts
    ./frontend/node_modules/zod/src/v3/tests/enum.test.ts
    ./frontend/node_modules/zod/src/v3/tests/date.test.ts
    ./frontend/node_modules/zod/src/v3/tests/set.test.ts
    ./frontend/node_modules/zod/src/v3/tests/discriminated-unions.test.ts
    ./frontend/node_modules/zod/src/v3/tests/firstpartyschematypes.test.ts
    ./frontend/node_modules/zod/src/v3/tests/language-server.test.ts
    ./frontend/node_modules/zod/src/v3/tests/catch.test.ts
    ./frontend/node_modules/zod/src/v3/tests/bigint.test.ts
    ./frontend/node_modules/zod/src/v3/tests/string.test.ts
    ./frontend/node_modules/zod/src/v3/tests/safeparse.test.ts
    ./frontend/node_modules/zod/src/v3/tests/branded.test.ts
    ./frontend/node_modules/zod/src/v3/tests/default.test.ts
    ./frontend/node_modules/zod/src/v3/tests/anyunknown.test.ts
    ./frontend/node_modules/zod/src/v3/tests/unions.test.ts
    ./frontend/node_modules/zod/src/v3/tests/literal.test.ts
    ./frontend/node_modules/zod/src/v3/tests/language-server.source.ts
    ./frontend/node_modules/zod/src/v3/tests/pickomit.test.ts
    ./frontend/node_modules/zod/src/v3/tests/intersection.test.ts
    ./frontend/node_modules/zod/src/v3/tests/void.test.ts
    ./frontend/node_modules/zod/src/v3/tests/deepmasking.test.ts
    ./frontend/node_modules/zod/src/v3/tests/masking.test.ts
    ./frontend/node_modules/zod/src/v3/tests/parseUtil.test.ts
    ./frontend/node_modules/zod/src/v3/tests/custom.test.ts
    ./frontend/node_modules/zod/src/v3/tests/recursive.test.ts
    ./frontend/node_modules/zod/src/v3/tests/parser.test.ts
    ./frontend/node_modules/zod/src/v3/tests/base.test.ts
    ./frontend/node_modules/zod/src/v3/tests/description.test.ts
    ./frontend/node_modules/zod/src/v3/tests/coerce.test.ts
    ./frontend/node_modules/zod/src/v3/tests/object-in-es5-env.test.ts
    ./frontend/node_modules/zod/src/v3/tests/firstparty.test.ts
    ./frontend/node_modules/zod/src/v3/tests/mocker.test.ts
    ./frontend/node_modules/zod/src/v3/tests/object-augmentation.test.ts
    ./frontend/node_modules/zod/src/v3/tests/generics.test.ts
    ./frontend/node_modules/zod/src/v3/tests/nan.test.ts
    ./frontend/node_modules/zod/src/v3/tests/function.test.ts
    ./frontend/node_modules/zod/src/v3/tests/transformer.test.ts
    ./frontend/node_modules/zod/src/v3/tests/pipeline.test.ts
    ./frontend/node_modules/zod/src/v3/tests/tuple.test.ts
    ./frontend/node_modules/zod/src/v3/tests/record.test.ts
    ./frontend/node_modules/zod/src/v3/errors.ts
    ./frontend/node_modules/css-tree/cjs/syntax/scope/value.cjs
    ./frontend/node_modules/css-tree/cjs/syntax/scope/selector.cjs
    ./frontend/node_modules/css-tree/cjs/syntax/scope/index.cjs
    ./frontend/node_modules/css-tree/cjs/syntax/scope/default.cjs
    ./frontend/node_modules/css-tree/cjs/syntax/scope/atrulePrelude.cjs
    ./frontend/node_modules/@types/node/ts5.6/compatibility/float16array.d.ts
    ./frontend/node_modules/@types/node/index.d.ts
    ./frontend/node_modules/@types/node/wasi.d.ts
    ./frontend/node_modules/@types/node/util.d.ts
    ./frontend/node_modules/@asamuzakjp/dom-selector/src/js/parser.js
    ./frontend/node_modules/@asamuzakjp/dom-selector/src/js/constant.js
    ./frontend/node_modules/@asamuzakjp/dom-selector/src/js/matcher.js
    ./frontend/node_modules/@asamuzakjp/dom-selector/src/js/finder.js
    ./frontend/node_modules/@asamuzakjp/dom-selector/src/js/utility.js
    ./frontend/node_modules/prettier/internal/legacy-cli.mjs
    ./frontend/node_modules/@asamuzakjp/dom-selector/package.json
    ./frontend/node_modules/@asamuzakjp/dom-selector/README.md
    ./frontend/node_modules/prettier/internal/experimental-cli-worker.mjs
    ./frontend/node_modules/prettier/internal/experimental-cli.mjs
    ./frontend/node_modules/zod/src/v3/locales/en.ts
    ./frontend/node_modules/zod/src/v3/external.ts
    ./frontend/node_modules/@types/node/ts5.7/index.d.ts
    ./frontend/node_modules/css-tree/data/patch.json
    ./frontend/node_modules/react-router/dist/production/lib/types/internal.mjs
    ./frontend/node_modules/react-router/dist/production/lib/types/internal.d.mts
    ./frontend/node_modules/react-router/dist/production/lib/types/internal.d.ts
    ./frontend/node_modules/react-router/dist/production/lib/types/internal.js
    ./frontend/node_modules/react-router/dist/production/index.mjs
    ./frontend/node_modules/react-router/dist/production/dom-export.mjs
    ./frontend/node_modules/react-router/dist/production/browser-Bfn3xw9E.d.ts
    ./frontend/node_modules/react-router/dist/production/index-react-server-client.mjs
    ./frontend/node_modules/react-router/dist/production/chunk-PY35PE22.mjs
    ./frontend/node_modules/react-router/dist/production/routeModules-CA7kSxJJ.d.ts
    ./frontend/node_modules/react-router/dist/production/chunk-LKUVSIBA.js
    ./frontend/node_modules/react-router/dist/production/browser-Di6-vSl-.d.mts
    ./frontend/node_modules/react-router/dist/production/chunk-XAAX7KIK.js
    ./frontend/node_modules/react-router/dist/production/index.js
    ./frontend/node_modules/react-router/dist/production/index-react-server.js
    ./frontend/node_modules/react-router/dist/production/index-react-server.d.mts
    ./frontend/node_modules/react-router/dist/production/dom-export.d.ts
    ./frontend/node_modules/react-router/dist/production/context-phCt_zmH.d.mts
    ./frontend/node_modules/react-router/dist/production/index-react-server.d.ts
    ./frontend/node_modules/react-router/dist/production/index.d.mts
    ./frontend/node_modules/react-router/dist/production/index-react-server-client.d.ts
    ./frontend/node_modules/react-router/dist/production/register-CTxsJBKQ.d.mts
    ./frontend/node_modules/react-router/dist/production/chunk-2BDJPJTA.mjs
    ./frontend/node_modules/react-router/dist/production/instrumentation-BYr6ff5D.d.ts
    ./frontend/node_modules/react-router/dist/production/dom-export.d.mts
    ./frontend/node_modules/react-router/dist/production/register-CkcGwv27.d.ts
    ./frontend/node_modules/react-router/dist/production/index-react-server-client.d.mts
    ./frontend/node_modules/react-router/dist/production/index-react-server-client-CCwMoQIT.d.ts
    ./frontend/node_modules/react-router/dist/production/index-react-server-client-BcrVT7Dd.d.mts
    ./frontend/node_modules/react-router/dist/production/chunk-CAFVLUDY.js
    ./frontend/node_modules/css-tree/cjs/syntax/pseudo/index.cjs
    ./frontend/node_modules/css-tree/cjs/syntax/pseudo/lang.cjs
    ./frontend/node_modules/@types/node/ts5.7/compatibility/float16array.d.ts
    ./frontend/node_modules/@types/node/process.d.ts
    ./frontend/node_modules/@types/node/globals.typedarray.d.ts
    ./frontend/node_modules/@types/node/sqlite.d.ts
    ./frontend/node_modules/@types/node/module.d.ts
    ./frontend/node_modules/@types/node/zlib.d.ts
    ./frontend/node_modules/@types/node/child_process.d.ts
    ./frontend/node_modules/@types/node/dgram.d.ts
    ./frontend/node_modules/@types/node/repl.d.ts
    ./frontend/node_modules/@types/node/fs.d.ts
    ./frontend/node_modules/@types/node/assert.d.ts
    ./frontend/node_modules/@types/node/https.d.ts
    ./frontend/node_modules/@types/node/package.json
    ./frontend/node_modules/@types/node/cluster.d.ts
    ./frontend/node_modules/@types/node/url.d.ts
    ./frontend/node_modules/@types/node/perf_hooks.d.ts
    ./frontend/node_modules/@types/node/v8.d.ts
    ./frontend/node_modules/@types/node/README.md
    ./frontend/node_modules/redent/index.d.ts
    ./frontend/node_modules/redent/package.json
    ./frontend/node_modules/redent/readme.md
    ./frontend/node_modules/redent/index.js
    ./frontend/node_modules/redent/license
    ./frontend/node_modules/zod/src/v4/index.ts
    ./frontend/node_modules/@asamuzakjp/dom-selector/node_modules/lru-cache/package.json
    ./frontend/node_modules/@asamuzakjp/dom-selector/node_modules/lru-cache/README.md
    ./frontend/node_modules/@types/node/assert/strict.d.ts
    ./frontend/node_modules/@types/node/inspector.d.ts
    ./frontend/node_modules/@types/node/stream.d.ts
    ./frontend/node_modules/@types/node/http2.d.ts
    ./frontend/node_modules/@types/node/http.d.ts
    ./frontend/node_modules/@types/node/test.d.ts
    ./frontend/node_modules/@types/node/timers.d.ts
    ./frontend/node_modules/@types/node/buffer.buffer.d.ts
    ./frontend/node_modules/@types/node/inspector.generated.d.ts
    ./frontend/node_modules/css-tree/cjs/syntax/config/parser-selector.cjs
    ./frontend/node_modules/css-tree/cjs/syntax/config/walker.cjs
    ./frontend/node_modules/css-tree/cjs/syntax/config/parser.cjs
    ./frontend/node_modules/css-tree/cjs/syntax/config/mix.cjs
    ./frontend/node_modules/css-tree/cjs/syntax/config/generator.cjs
    ./frontend/node_modules/css-tree/cjs/syntax/config/lexer.cjs
    ./frontend/node_modules/shebang-regex/index.d.ts
    ./frontend/node_modules/shebang-regex/package.json
    ./frontend/node_modules/shebang-regex/readme.md
    ./frontend/node_modules/shebang-regex/index.js
    ./frontend/node_modules/shebang-regex/license
    ./frontend/node_modules/flatted/golang/pkg/flatted/flatted.go
    ./frontend/node_modules/flatted/golang/README.md
    ./frontend/node_modules/tldts/dist/cjs/src/data/trie.js.map
    ./frontend/node_modules/tldts/dist/cjs/src/data/trie.js
    ./frontend/node_modules/tldts/dist/cjs/src/suffix-trie.js
    ./frontend/node_modules/tldts/dist/cjs/src/suffix-trie.js.map
    ./frontend/node_modules/tldts/dist/cjs/index.js.map
    ./frontend/node_modules/tldts/dist/cjs/index.js
    ./frontend/node_modules/tldts/dist/cjs/tsconfig.tsbuildinfo
    ./frontend/node_modules/tldts/dist/index.umd.min.js.map
    ./frontend/node_modules/tldts/dist/index.umd.min.js
    ./frontend/node_modules/prettier/plugins/estree.js
    ./frontend/node_modules/prettier/plugins/markdown.js
    ./frontend/node_modules/prettier/plugins/typescript.d.ts
    ./frontend/node_modules/prettier/plugins/graphql.d.ts
    ./frontend/node_modules/prettier/plugins/yaml.js
    ./frontend/node_modules/prettier/plugins/html.d.ts
    ./frontend/node_modules/prettier/plugins/babel.js
    ./frontend/node_modules/prettier/plugins/angular.mjs
    ./frontend/node_modules/prettier/plugins/meriyah.mjs
    ./frontend/node_modules/prettier/plugins/yaml.d.ts
    ./frontend/node_modules/prettier/plugins/angular.d.ts
    ./frontend/node_modules/prettier/plugins/acorn.js
    ./frontend/node_modules/prettier/plugins/markdown.mjs
    ./frontend/node_modules/prettier/plugins/flow.d.ts
    ./frontend/node_modules/prettier/plugins/postcss.d.ts
    ./frontend/node_modules/prettier/plugins/flow.mjs
    ./frontend/node_modules/prettier/plugins/angular.js
    ./frontend/node_modules/prettier/plugins/postcss.mjs
    ./frontend/node_modules/prettier/plugins/glimmer.mjs
    ./frontend/node_modules/prettier/plugins/estree.d.ts
    ./frontend/node_modules/prettier/plugins/acorn.d.ts
    ./frontend/node_modules/prettier/plugins/glimmer.d.ts
    ./frontend/node_modules/prettier/plugins/babel.mjs
    ./frontend/node_modules/prettier/plugins/markdown.d.ts
    ./frontend/node_modules/prettier/plugins/typescript.mjs
    ./frontend/node_modules/prettier/plugins/meriyah.js
    ./frontend/node_modules/prettier/plugins/acorn.mjs
    ./frontend/node_modules/prettier/plugins/meriyah.d.ts
    ./frontend/node_modules/prettier/plugins/graphql.js
    ./frontend/node_modules/prettier/plugins/html.mjs
    ./frontend/node_modules/prettier/plugins/flow.js
    ./frontend/node_modules/prettier/plugins/yaml.mjs
    ./frontend/node_modules/prettier/plugins/babel.d.ts
    ./frontend/node_modules/prettier/plugins/typescript.js
    ./frontend/node_modules/prettier/plugins/estree.mjs
    ./frontend/node_modules/prettier/plugins/graphql.mjs
    ./frontend/node_modules/prettier/plugins/postcss.js
    ./frontend/node_modules/prettier/plugins/glimmer.js
    ./frontend/node_modules/prettier/plugins/html.js
    ./frontend/node_modules/prettier/standalone.js
    ./frontend/node_modules/prettier/THIRD-PARTY-NOTICES.md
    ./frontend/node_modules/flatted/esm/index.js
    ./frontend/node_modules/zod/src/v4/classic/compat.ts
    ./frontend/node_modules/zod/src/v4/classic/index.ts
    ./frontend/node_modules/zod/src/v4/classic/checks.ts
    ./frontend/node_modules/zod/src/v4/classic/coerce.ts
    ./frontend/node_modules/zod/src/v4/classic/schemas.ts
    ./frontend/node_modules/zod/src/v4/classic/from-json-schema.ts
    ./frontend/node_modules/@asamuzakjp/dom-selector/node_modules/lru-cache/dist/commonjs/index.d.ts.map
    ./frontend/node_modules/@asamuzakjp/dom-selector/node_modules/lru-cache/dist/commonjs/index.min.js
    ./frontend/node_modules/@asamuzakjp/dom-selector/node_modules/lru-cache/dist/commonjs/index.d.ts
    ./frontend/node_modules/@asamuzakjp/dom-selector/node_modules/lru-cache/dist/commonjs/index.js.map
    ./frontend/node_modules/@asamuzakjp/dom-selector/node_modules/lru-cache/dist/commonjs/package.json
    ./frontend/node_modules/@asamuzakjp/dom-selector/node_modules/lru-cache/dist/commonjs/index.js
    ./frontend/node_modules/@asamuzakjp/dom-selector/node_modules/lru-cache/dist/commonjs/index.min.js.map
    ./frontend/node_modules/@types/node/web-globals/storage.d.ts
    ./frontend/node_modules/@types/node/web-globals/abortcontroller.d.ts
    ./frontend/node_modules/@types/node/web-globals/domexception.d.ts
    ./frontend/node_modules/@types/node/web-globals/navigator.d.ts
    ./frontend/node_modules/@types/node/web-globals/fetch.d.ts
    ./frontend/node_modules/@types/node/web-globals/events.d.ts
    ./frontend/node_modules/@types/node/web-globals/crypto.d.ts
    ./frontend/node_modules/@types/node/web-globals/streams.d.ts
    ./frontend/node_modules/@types/node/vm.d.ts
    ./frontend/node_modules/react-router/dist/development/chunk-GO74ODU3.js
    ./frontend/node_modules/css-tree/cjs/definition-syntax/index.cjs
    ./frontend/node_modules/css-tree/cjs/definition-syntax/generate.cjs
    ./frontend/node_modules/css-tree/cjs/definition-syntax/parse.cjs
    ./frontend/node_modules/css-tree/cjs/definition-syntax/SyntaxError.cjs
    ./frontend/node_modules/css-tree/cjs/definition-syntax/scanner.cjs
    ./frontend/node_modules/css-tree/cjs/definition-syntax/walk.cjs
    ./frontend/node_modules/css-tree/cjs/data-patch.cjs
    ./frontend/node_modules/css-tree/cjs/index.cjs
    ./frontend/node_modules/react-router/dist/development/index-react-server.mjs
    ./frontend/node_modules/react-router/dist/development/index.d.ts
    ./frontend/node_modules/react-router/dist/development/routeModules-BRrCYrSL.d.mts
    ./frontend/node_modules/react-router/dist/development/chunk-HPFFRPKK.js
    ./frontend/node_modules/react-router/dist/development/index-react-server-client.js
    ./frontend/node_modules/react-router/dist/development/dom-export.js
    ./frontend/node_modules/css-tree/lib/walker/create.js
    ./frontend/node_modules/css-tree/lib/walker/index.js
    ./frontend/node_modules/@asamuzakjp/dom-selector/node_modules/lru-cache/dist/esm/index.d.ts.map
    ./frontend/node_modules/@asamuzakjp/dom-selector/node_modules/lru-cache/dist/esm/index.min.js
    ./frontend/node_modules/@asamuzakjp/dom-selector/node_modules/lru-cache/dist/esm/index.d.ts
    ./frontend/node_modules/@asamuzakjp/dom-selector/node_modules/lru-cache/dist/esm/index.js.map
    ./frontend/node_modules/@asamuzakjp/dom-selector/node_modules/lru-cache/dist/esm/package.json
    ./frontend/node_modules/@asamuzakjp/dom-selector/node_modules/lru-cache/dist/esm/index.js
    ./frontend/node_modules/@asamuzakjp/dom-selector/node_modules/lru-cache/dist/esm/index.min.js.map
    ./frontend/node_modules/@asamuzakjp/dom-selector/node_modules/lru-cache/LICENSE.md
    ./frontend/node_modules/prettier/bin/prettier.cjs
    ./frontend/node_modules/prettier/LICENSE
    ./frontend/node_modules/@asamuzakjp/dom-selector/LICENSE
    ./frontend/node_modules/scheduler/cjs/scheduler-unstable_mock.production.js
    ./frontend/node_modules/scheduler/cjs/scheduler.production.js
    ./frontend/node_modules/scheduler/cjs/scheduler-unstable_mock.development.js
    ./frontend/node_modules/scheduler/cjs/scheduler-unstable_post_task.development.js
    ./frontend/node_modules/scheduler/cjs/scheduler.native.production.js
    ./frontend/node_modules/scheduler/cjs/scheduler.native.development.js
    ./frontend/node_modules/scheduler/cjs/scheduler-unstable_post_task.production.js
    ./frontend/node_modules/scheduler/cjs/scheduler.development.js
    ./frontend/node_modules/scheduler/index.native.js
    ./frontend/node_modules/scheduler/package.json
    ./frontend/node_modules/scheduler/README.md
    ./frontend/node_modules/scheduler/unstable_post_task.js
    ./frontend/node_modules/scheduler/index.js
    ./frontend/node_modules/scheduler/LICENSE
    ./frontend/node_modules/scheduler/unstable_mock.js
    ./frontend/node_modules/@types/node/readline/promises.d.ts
    ./frontend/node_modules/@types/node/dns.d.ts
    ./frontend/node_modules/@asamuzakjp/dom-selector/types/index.d.ts
    ./frontend/node_modules/gensync/package.json
    ./frontend/node_modules/gensync/index.js.flow
    ./frontend/node_modules/gensync/README.md
    ./frontend/node_modules/gensync/index.js
    ./frontend/node_modules/flatted/python/flatted.py
    ./frontend/node_modules/flatted/LICENSE
    ./frontend/node_modules/css-tree/cjs/generator/create.cjs
    ./frontend/node_modules/css-tree/cjs/generator/sourceMap.cjs
    ./frontend/node_modules/css-tree/cjs/generator/index.cjs
    ./frontend/node_modules/css-tree/cjs/generator/token-before.cjs
    ./frontend/node_modules/whatwg-url/LICENSE.txt
    ./frontend/node_modules/react-router/dist/development/lib/types/internal.mjs
    ./frontend/node_modules/@types/node/stream/promises.d.ts
    ./frontend/node_modules/react-router/dist/development/lib/types/internal.d.mts
    ./frontend/node_modules/react-router/dist/development/lib/types/internal.d.ts
    ./frontend/node_modules/react-router/dist/development/lib/types/internal.js
    ./frontend/node_modules/react-router/dist/development/index.mjs
    ./frontend/node_modules/react-router/dist/development/dom-export.mjs
    ./frontend/node_modules/gensync/test/index.test.js
    ./frontend/node_modules/react-router/dist/development/browser-Bfn3xw9E.d.ts
    ./frontend/node_modules/gensync/test/.babelrc
    ./frontend/node_modules/react-router/dist/development/index-react-server-client.mjs
    ./frontend/node_modules/react-router/dist/development/routeModules-CA7kSxJJ.d.ts
    ./frontend/node_modules/react-router/dist/development/browser-Di6-vSl-.d.mts
    ./frontend/node_modules/react-router/dist/development/index.js
    ./frontend/node_modules/react-router/dist/development/index-react-server.js
    ./frontend/node_modules/react-router/dist/development/index-react-server.d.mts
    ./frontend/node_modules/react-router/dist/development/dom-export.d.ts
    ./frontend/node_modules/react-router/dist/development/context-phCt_zmH.d.mts
    ./frontend/node_modules/react-router/dist/development/chunk-LLP6DRWX.js
    ./frontend/node_modules/react-router/dist/development/index-react-server.d.ts
    ./frontend/node_modules/react-router/dist/development/chunk-UVKPFVEO.mjs
    ./frontend/node_modules/react-router/dist/development/index.d.mts
    ./frontend/node_modules/react-router/dist/development/index-react-server-client.d.ts
    ./frontend/node_modules/react-router/dist/development/chunk-UALY5CBT.mjs
    ./frontend/node_modules/react-router/dist/development/register-CTxsJBKQ.d.mts
    ./frontend/node_modules/react-router/dist/development/instrumentation-BYr6ff5D.d.ts
    ./frontend/node_modules/react-router/dist/development/dom-export.d.mts
    ./frontend/node_modules/react-router/dist/development/register-CkcGwv27.d.ts
    ./frontend/node_modules/react-router/dist/development/index-react-server-client.d.mts
    ./frontend/node_modules/react-router/dist/development/index-react-server-client-CCwMoQIT.d.ts
    ./frontend/node_modules/react-router/dist/development/index-react-server-client-BcrVT7Dd.d.mts
    ./frontend/node_modules/gensync/LICENSE
    ./frontend/node_modules/react-router/CHANGELOG.md
    ./frontend/node_modules/@types/node/stream/web.d.ts
    ./frontend/node_modules/@types/node/stream/consumers.d.ts
    ./frontend/node_modules/react-router/LICENSE.md
    ./frontend/node_modules/@types/node/async_hooks.d.ts
    ./frontend/node_modules/@types/node/console.d.ts
    ./frontend/node_modules/tldts/dist/es6/src/data/trie.js.map
    ./frontend/node_modules/@types/node/timers/promises.d.ts
    ./frontend/node_modules/tldts/dist/es6/src/data/trie.js
    ./frontend/node_modules/tldts/dist/es6/src/suffix-trie.js
    ./frontend/node_modules/tldts/dist/es6/src/suffix-trie.js.map
    ./frontend/node_modules/tldts/dist/es6/index.js.map
    ./frontend/node_modules/tldts/dist/es6/tsconfig.bundle.tsbuildinfo
    ./frontend/node_modules/tldts/dist/es6/index.js
    ./frontend/node_modules/tldts/dist/index.esm.min.js
    ./frontend/node_modules/tldts/dist/index.cjs.min.js
    ./frontend/node_modules/tldts/dist/index.esm.min.js.map
    ./frontend/node_modules/tldts/dist/index.cjs.min.js.map
    ./frontend/node_modules/@types/node/worker_threads.d.ts
    ./frontend/node_modules/@types/node/querystring.d.ts
    ./frontend/node_modules/@types/node/buffer.d.ts
    ./frontend/node_modules/@types/node/os.d.ts
    ./frontend/node_modules/@types/node/events.d.ts
    ./frontend/node_modules/@types/node/trace_events.d.ts
    ./frontend/node_modules/@types/node/crypto.d.ts
    ./frontend/node_modules/@types/node/readline.d.ts
    ./frontend/node_modules/@types/node/LICENSE
    ./frontend/node_modules/@types/node/punycode.d.ts
    ./frontend/node_modules/@types/node/tty.d.ts
    ./frontend/node_modules/@types/node/tls.d.ts
    ./frontend/node_modules/@types/node/string_decoder.d.ts
    ./frontend/node_modules/whatwg-url/lib/VoidFunction.js
    ./frontend/node_modules/whatwg-url/lib/URL.js
    ./frontend/node_modules/whatwg-url/lib/url-state-machine.js
    ./frontend/node_modules/whatwg-url/lib/utils.js
    ./frontend/node_modules/whatwg-url/lib/Function.js
    ./frontend/node_modules/whatwg-url/lib/URLSearchParams.js
    ./frontend/node_modules/whatwg-url/lib/infra.js
    ./frontend/node_modules/whatwg-url/lib/urlencoded.js
    ./frontend/node_modules/whatwg-url/lib/encoding.js
    ./frontend/node_modules/whatwg-url/lib/URL-impl.js
    ./frontend/node_modules/whatwg-url/lib/percent-encoding.js
    ./frontend/node_modules/whatwg-url/lib/URLSearchParams-impl.js
    ./frontend/node_modules/whatwg-url/package.json
    ./frontend/node_modules/whatwg-url/README.md
    ./frontend/node_modules/whatwg-url/webidl2js-wrapper.js
    ./frontend/node_modules/whatwg-url/index.js
    ./frontend/node_modules/@types/node/sea.d.ts
    ./frontend/node_modules/@types/node/globals.d.ts
    ./frontend/node_modules/@types/node/diagnostics_channel.d.ts
    ./frontend/node_modules/@types/node/domain.d.ts
    ./frontend/node_modules/@types/node/constants.d.ts
    ./frontend/node_modules/@types/node/path.d.ts
    ./frontend/node_modules/hermes-parser/package.json
    ./frontend/node_modules/hermes-parser/README.md
    ./frontend/node_modules/zod/src/v4/classic/tests/continuability.test.ts
    ./frontend/node_modules/zod/src/v4/classic/tests/async-refinements.test.ts
    ./frontend/node_modules/zod/src/v4/classic/tests/array.test.ts
    ./frontend/node_modules/zod/src/v4/classic/tests/fix-json-issue.test.ts
    ./frontend/node_modules/zod/src/v4/classic/tests/promise.test.ts
    ./frontend/node_modules/zod/src/v4/classic/tests/object.test.ts
    ./frontend/node_modules/zod/src/v4/classic/tests/coalesce.test.ts
    ./frontend/node_modules/zod/src/v4/classic/tests/readonly.test.ts
    ./frontend/node_modules/zod/src/v4/classic/tests/datetime.test.ts
    ./frontend/node_modules/zod/src/v4/classic/tests/url.test.ts
    ./frontend/node_modules/zod/src/v4/classic/tests/describe-meta-checks.test.ts
    ./frontend/node_modules/zod/src/v4/classic/tests/standard-schema.test.ts
    ./frontend/node_modules/zod/src/v4/classic/tests/pipe.test.ts
    ./frontend/node_modules/zod/src/v4/classic/tests/to-json-schema-methods.test.ts
    ./frontend/node_modules/zod/src/v4/classic/tests/error.test.ts
    ./frontend/node_modules/zod/src/v4/classic/tests/prefault.test.ts
    ./frontend/node_modules/zod/src/v4/classic/tests/prototypes.test.ts
    ./frontend/node_modules/zod/src/v4/classic/tests/preprocess.test.ts
    ./frontend/node_modules/zod/src/v4/classic/tests/instanceof.test.ts
    ./frontend/node_modules/zod/src/v4/classic/tests/map.test.ts
    ./frontend/node_modules/zod/src/v4/classic/tests/optional.test.ts
    ./frontend/node_modules/zod/src/v4/classic/tests/validations.test.ts
    ./frontend/node_modules/zod/src/v4/classic/tests/refine.test.ts
    ./frontend/node_modules/zod/src/v4/classic/tests/from-json-schema.test.ts
    ./frontend/node_modules/zod/src/v4/classic/tests/async-parsing.test.ts
    ./frontend/node_modules/zod/src/v4/classic/tests/primitive.test.ts
    ./frontend/node_modules/zod/src/v4/classic/tests/number.test.ts
    ./frontend/node_modules/zod/src/v4/classic/tests/nullable.test.ts
    ./frontend/node_modules/zod/src/v4/classic/tests/to-json-schema.test.ts
    ./frontend/node_modules/zod/src/v4/classic/tests/recursive-types.test.ts
    ./frontend/node_modules/zod/src/v4/classic/tests/enum.test.ts
    ./frontend/node_modules/zod/src/v4/classic/tests/json.test.ts
    ./frontend/node_modules/zod/src/v4/classic/tests/date.test.ts
    ./frontend/node_modules/zod/src/v4/classic/tests/hash.test.ts
    ./frontend/node_modules/zod/src/v4/classic/tests/set.test.ts
    ./frontend/node_modules/zod/src/v4/classic/tests/discriminated-unions.test.ts
    ./frontend/node_modules/zod/src/v4/classic/tests/lazy.test.ts
    ./frontend/node_modules/zod/src/v4/classic/tests/codec.test.ts
    ./frontend/node_modules/zod/src/v4/classic/tests/catch.test.ts
    ./frontend/node_modules/zod/src/v4/classic/tests/bigint.test.ts
    ./frontend/node_modules/zod/src/v4/classic/tests/file.test.ts
    ./frontend/node_modules/zod/src/v4/classic/tests/codec-examples.test.ts
    ./frontend/node_modules/zod/src/v4/classic/tests/string.test.ts
    ./frontend/node_modules/zod/src/v4/classic/tests/error-utils.test.ts
    ./frontend/node_modules/zod/src/v4/classic/tests/default.test.ts
    ./frontend/node_modules/zod/src/v4/classic/tests/assignability.test.ts
    ./frontend/node_modules/zod/src/v4/classic/tests/anyunknown.test.ts
    ./frontend/node_modules/zod/src/v4/classic/tests/literal.test.ts
    ./frontend/node_modules/zod/src/v4/classic/tests/partial.test.ts
    ./frontend/node_modules/zod/src/v4/classic/tests/pickomit.test.ts
    ./frontend/node_modules/zod/src/v4/classic/tests/intersection.test.ts
    ./frontend/node_modules/zod/src/v4/classic/tests/stringbool.test.ts
    ./frontend/node_modules/zod/src/v4/classic/tests/void.test.ts
    ./frontend/node_modules/zod/src/v4/classic/tests/apply.test.ts
    ./frontend/node_modules/zod/src/v4/classic/tests/brand.test.ts
    ./frontend/node_modules/zod/src/v4/classic/tests/custom.test.ts
    ./frontend/node_modules/zod/src/v4/classic/tests/base.test.ts
    ./frontend/node_modules/zod/src/v4/classic/tests/index.test.ts
    ./frontend/node_modules/zod/src/v4/classic/tests/description.test.ts
    ./frontend/node_modules/zod/src/v4/classic/tests/coerce.test.ts
    ./frontend/node_modules/zod/src/v4/classic/tests/nonoptional.test.ts
    ./frontend/node_modules/zod/src/v4/classic/tests/firstparty.test.ts
    ./frontend/node_modules/zod/src/v4/classic/tests/registries.test.ts
    ./frontend/node_modules/zod/src/v4/classic/tests/generics.test.ts
    ./frontend/node_modules/zod/src/v4/classic/tests/nan.test.ts
    ./frontend/node_modules/zod/src/v4/classic/tests/function.test.ts
    ./frontend/node_modules/zod/src/v4/classic/tests/union.test.ts
    ./frontend/node_modules/zod/src/v4/classic/tests/tuple.test.ts
    ./frontend/node_modules/zod/src/v4/classic/tests/record.test.ts
    ./frontend/node_modules/zod/src/v4/classic/tests/nested-refine.test.ts
    ./frontend/node_modules/zod/src/v4/classic/tests/string-formats.test.ts
    ./frontend/node_modules/zod/src/v4/classic/tests/transform.test.ts
    ./frontend/node_modules/zod/src/v4/classic/tests/template-literal.test.ts
    ./frontend/node_modules/zod/src/v4/classic/errors.ts
    ./frontend/node_modules/zod/src/v4/classic/parse.ts
    ./frontend/node_modules/zod/src/v4/classic/iso.ts
    ./frontend/node_modules/zod/src/v4/classic/external.ts
    ./frontend/node_modules/flatted/types/index.d.ts
    ./frontend/node_modules/css-tree/cjs/parser/create.cjs
    ./frontend/node_modules/css-tree/cjs/parser/sequence.cjs
    ./frontend/node_modules/css-tree/cjs/parser/index.cjs
    ./frontend/node_modules/css-tree/cjs/parser/SyntaxError.cjs
    ./frontend/node_modules/css-tree/cjs/parser/parse-selector.cjs
    ./frontend/node_modules/@asamuzakjp/dom-selector/types/js/matcher.d.ts
    ./frontend/node_modules/@asamuzakjp/dom-selector/types/js/parser.d.ts
    ./frontend/node_modules/@asamuzakjp/dom-selector/types/js/constant.d.ts
    ./frontend/node_modules/@asamuzakjp/dom-selector/types/js/utility.d.ts
    ./frontend/node_modules/@asamuzakjp/dom-selector/types/js/finder.d.ts
    ./frontend/node_modules/@types/node/compatibility/iterators.d.ts
    ./frontend/node_modules/shebang-command/package.json
    ./frontend/node_modules/shebang-command/readme.md
    ./frontend/node_modules/shebang-command/index.js
    ./frontend/node_modules/shebang-command/license
    ./frontend/node_modules/css-tree/lib/index.js
    ./frontend/node_modules/css-tree/lib/syntax/atrule/layer.js
    ./frontend/node_modules/css-tree/lib/syntax/atrule/container.js
    ./frontend/node_modules/css-tree/lib/syntax/atrule/font-face.js
    ./frontend/node_modules/css-tree/lib/syntax/atrule/scope.js
    ./frontend/node_modules/css-tree/lib/syntax/atrule/nest.js
    ./frontend/node_modules/css-tree/lib/syntax/atrule/index.js
    ./frontend/node_modules/css-tree/lib/syntax/atrule/import.js
    ./frontend/node_modules/css-tree/lib/syntax/atrule/media.js
    ./frontend/node_modules/css-tree/lib/syntax/atrule/starting-style.js
    ./frontend/node_modules/css-tree/lib/syntax/atrule/page.js
    ./frontend/node_modules/css-tree/lib/syntax/atrule/supports.js
    ./frontend/node_modules/zod/src/v4/mini/index.ts
    ./frontend/node_modules/zod/src/v4/mini/checks.ts
    ./frontend/node_modules/zod/src/v4/mini/coerce.ts
    ./frontend/node_modules/zod/src/v4/mini/schemas.ts
    ./frontend/node_modules/eslint-visitor-keys/lib/index.js
    ./frontend/node_modules/eslint-visitor-keys/lib/visitor-keys.js
    ./frontend/node_modules/eslint-visitor-keys/package.json
    ./frontend/node_modules/eslint-visitor-keys/README.md
    ./frontend/node_modules/css-tree/cjs/utils/clone.cjs
    ./frontend/node_modules/css-tree/cjs/utils/List.cjs
    ./frontend/node_modules/css-tree/cjs/utils/names.cjs
    ./frontend/node_modules/css-tree/cjs/utils/index.cjs
    ./frontend/node_modules/css-tree/cjs/utils/create-custom-error.cjs
    ./frontend/node_modules/css-tree/cjs/utils/string.cjs
    ./frontend/node_modules/css-tree/cjs/utils/ident.cjs
    ./frontend/node_modules/css-tree/cjs/utils/url.cjs
    ./frontend/node_modules/@types/estree/index.d.ts
    ./frontend/node_modules/@types/estree/package.json
    ./frontend/node_modules/@types/estree/flow.d.ts
    ./frontend/node_modules/@types/estree/README.md
    ./frontend/node_modules/@types/estree/LICENSE
    ./frontend/node_modules/fast-deep-equal/index.d.ts
    ./frontend/node_modules/css-tree/lib/tokenizer/char-code-definitions.js
    ./frontend/node_modules/css-tree/lib/tokenizer/names.js
    ./frontend/node_modules/css-tree/lib/tokenizer/utils.js
    ./frontend/node_modules/css-tree/lib/tokenizer/index.js
    ./frontend/node_modules/css-tree/lib/tokenizer/adopt-buffer.js
    ./frontend/node_modules/css-tree/lib/tokenizer/types.js
    ./frontend/node_modules/css-tree/lib/tokenizer/OffsetToLocation.js
    ./frontend/node_modules/css-tree/lib/tokenizer/TokenStream.js
    ./frontend/node_modules/eslint-visitor-keys/dist/index.d.ts
    ./frontend/node_modules/eslint-visitor-keys/dist/eslint-visitor-keys.cjs
    ./frontend/node_modules/eslint-visitor-keys/dist/visitor-keys.d.ts
    ./frontend/node_modules/eslint-visitor-keys/dist/eslint-visitor-keys.d.cts
    ./frontend/node_modules/eslint-visitor-keys/LICENSE
    ./frontend/node_modules/tldts/dist/types/src/data/trie.d.ts
    ./frontend/node_modules/zod/src/v4/mini/tests/object.test.ts
    ./frontend/node_modules/zod/src/v4/mini/tests/standard-schema.test.ts
    ./frontend/node_modules/zod/src/v4/mini/tests/error.test.ts
    ./frontend/node_modules/zod/src/v4/mini/tests/prototypes.test.ts
    ./frontend/node_modules/zod/src/v4/mini/tests/number.test.ts
    ./frontend/node_modules/zod/src/v4/mini/tests/recursive-types.test.ts
    ./frontend/node_modules/zod/src/v4/mini/tests/functions.test.ts
    ./frontend/node_modules/zod/src/v4/mini/tests/checks.test.ts
    ./frontend/node_modules/zod/src/v4/mini/tests/codec.test.ts
    ./frontend/node_modules/zod/src/v4/mini/tests/string.test.ts
    ./frontend/node_modules/zod/src/v4/mini/tests/assignability.test.ts
    ./frontend/node_modules/zod/src/v4/mini/tests/apply.test.ts
    ./frontend/node_modules/zod/src/v4/mini/tests/brand.test.ts
    ./frontend/node_modules/zod/src/v4/mini/tests/index.test.ts
    ./frontend/node_modules/zod/src/v4/mini/tests/computed.test.ts
    ./frontend/node_modules/tldts/dist/types/src/suffix-trie.d.ts
    ./frontend/node_modules/zod/src/v4/mini/parse.ts
    ./frontend/node_modules/zod/src/v4/mini/iso.ts
    ./frontend/node_modules/zod/src/v4/mini/external.ts
    ./frontend/node_modules/tldts/dist/types/index.d.ts
    ./frontend/node_modules/css-tree/cjs/tokenizer/OffsetToLocation.cjs
    ./frontend/node_modules/css-tree/cjs/tokenizer/names.cjs
    ./frontend/node_modules/css-tree/cjs/tokenizer/index.cjs
    ./frontend/node_modules/css-tree/cjs/tokenizer/char-code-definitions.cjs
    ./frontend/node_modules/css-tree/cjs/tokenizer/adopt-buffer.cjs
    ./frontend/node_modules/css-tree/cjs/tokenizer/TokenStream.cjs
    ./frontend/node_modules/css-tree/cjs/tokenizer/types.cjs
    ./frontend/node_modules/css-tree/cjs/tokenizer/utils.cjs
    ./frontend/node_modules/fast-deep-equal/es6/index.d.ts
    ./frontend/node_modules/fast-deep-equal/es6/react.d.ts
    ./frontend/node_modules/fast-deep-equal/es6/index.js
    ./frontend/node_modules/fast-deep-equal/es6/react.js
    ./frontend/node_modules/fast-deep-equal/package.json
    ./frontend/node_modules/fast-deep-equal/README.md
    ./frontend/node_modules/fast-deep-equal/react.d.ts
    ./frontend/node_modules/fast-deep-equal/index.js
    ./frontend/node_modules/fast-deep-equal/react.js
    ./frontend/node_modules/fast-deep-equal/LICENSE
    ./frontend/node_modules/@types/react-dom/client.d.ts
    ./frontend/node_modules/@types/react-dom/index.d.ts
    ./frontend/node_modules/@types/react-dom/server.edge.d.ts
    ./frontend/node_modules/@types/react-dom/server.browser.d.ts
    ./frontend/node_modules/@types/react-dom/static.node.d.ts
    ./frontend/node_modules/@types/react-dom/package.json
    ./frontend/node_modules/@types/react-dom/static.browser.d.ts
    ./frontend/node_modules/@types/react-dom/README.md
    ./frontend/node_modules/@types/react-dom/experimental.d.ts
    ./frontend/node_modules/@types/react-dom/static.edge.d.ts
    ./frontend/node_modules/@types/react-dom/server.bun.d.ts
    ./frontend/node_modules/@types/react-dom/static.d.ts
    ./frontend/node_modules/@types/react-dom/canary.d.ts
    ./frontend/node_modules/@types/react-dom/server.d.ts
    ./frontend/node_modules/@types/react-dom/LICENSE
    ./frontend/node_modules/@types/react-dom/server.node.d.ts
    ./frontend/node_modules/hermes-parser/dist/HermesParser.js
    ./frontend/node_modules/hermes-parser/dist/HermesParserDeserializer.js
    ./frontend/node_modules/hermes-parser/dist/HermesParserNodeDeserializers.js
    ./frontend/node_modules/@asamuzakjp/css-color/src/index.ts
    ./frontend/node_modules/css-tree/lib/syntax/node/Percentage.js
    ./frontend/node_modules/css-tree/lib/syntax/node/Layer.js
    ./frontend/node_modules/css-tree/lib/syntax/node/AtrulePrelude.js
    ./frontend/node_modules/css-tree/lib/syntax/node/Hash.js
    ./frontend/node_modules/css-tree/lib/syntax/node/Url.js
    ./frontend/node_modules/css-tree/lib/syntax/node/AttributeSelector.js
    ./frontend/node_modules/css-tree/lib/syntax/node/FeatureRange.js
    ./frontend/node_modules/css-tree/lib/syntax/node/CDO.js
    ./frontend/node_modules/css-tree/lib/syntax/node/ClassSelector.js
    ./frontend/node_modules/css-tree/lib/syntax/node/Condition.js
    ./frontend/node_modules/css-tree/lib/syntax/node/index-parse.js
    ./frontend/node_modules/css-tree/lib/syntax/node/Rule.js
    ./frontend/node_modules/css-tree/lib/syntax/node/TypeSelector.js
    ./frontend/node_modules/css-tree/lib/syntax/node/Scope.js
    ./frontend/node_modules/css-tree/lib/syntax/node/IdSelector.js
    ./frontend/node_modules/css-tree/lib/syntax/node/Dimension.js
    ./frontend/node_modules/css-tree/lib/syntax/node/Function.js
    ./frontend/node_modules/css-tree/lib/syntax/node/WhiteSpace.js
    ./frontend/node_modules/css-tree/lib/syntax/node/MediaQueryList.js
    ./frontend/node_modules/css-tree/lib/syntax/node/SelectorList.js
    ./frontend/node_modules/css-tree/lib/syntax/node/Value.js
    ./frontend/node_modules/css-tree/lib/syntax/node/PseudoElementSelector.js
    ./frontend/node_modules/css-tree/lib/syntax/node/Block.js
    ./frontend/node_modules/css-tree/lib/syntax/node/String.js
    ./frontend/node_modules/css-tree/lib/syntax/node/StyleSheet.js
    ./frontend/node_modules/css-tree/lib/syntax/node/Identifier.js
    ./frontend/node_modules/css-tree/lib/syntax/node/GeneralEnclosed.js
    ./frontend/node_modules/css-tree/lib/syntax/node/Comment.js
    ./frontend/node_modules/css-tree/lib/syntax/node/Atrule.js
    ./frontend/node_modules/css-tree/lib/syntax/node/AnPlusB.js
    ./frontend/node_modules/css-tree/lib/syntax/node/index.js
    ./frontend/node_modules/css-tree/lib/syntax/node/UnicodeRange.js
    ./frontend/node_modules/css-tree/lib/syntax/node/Combinator.js
    ./frontend/node_modules/css-tree/lib/syntax/node/Raw.js
    ./frontend/node_modules/css-tree/lib/syntax/node/index-generate.js
    ./frontend/node_modules/css-tree/lib/syntax/node/Parentheses.js
    ./frontend/node_modules/css-tree/lib/syntax/node/CDC.js
    ./frontend/node_modules/css-tree/lib/syntax/node/Ratio.js
    ./frontend/node_modules/css-tree/lib/syntax/node/index-parse-selector.js
    ./frontend/node_modules/css-tree/lib/syntax/node/FeatureFunction.js
    ./frontend/node_modules/css-tree/lib/syntax/node/Nth.js
    ./frontend/node_modules/css-tree/lib/syntax/node/Operator.js
    ./frontend/node_modules/css-tree/lib/syntax/node/DeclarationList.js
    ./frontend/node_modules/css-tree/lib/syntax/node/Feature.js
    ./frontend/node_modules/css-tree/lib/syntax/node/PseudoClassSelector.js
    ./frontend/node_modules/css-tree/lib/syntax/node/Declaration.js
    ./frontend/node_modules/css-tree/lib/syntax/node/Brackets.js
    ./frontend/node_modules/css-tree/lib/syntax/node/MediaQuery.js
    ./frontend/node_modules/css-tree/lib/syntax/node/SupportsDeclaration.js
    ./frontend/node_modules/css-tree/lib/syntax/node/NestingSelector.js
    ./frontend/node_modules/css-tree/lib/syntax/node/LayerList.js
    ./frontend/node_modules/css-tree/lib/syntax/node/Number.js
    ./frontend/node_modules/css-tree/lib/syntax/node/Selector.js
    ./frontend/node_modules/@types/react-dom/test-utils/index.d.ts
    ./frontend/node_modules/@asamuzakjp/css-color/src/js/relative-color.ts
    ./frontend/node_modules/@asamuzakjp/css-color/src/js/css-var.ts
    ./frontend/node_modules/@asamuzakjp/css-color/src/js/color.ts
    ./frontend/node_modules/@asamuzakjp/css-color/src/js/resolve.ts
    ./frontend/node_modules/@asamuzakjp/css-color/src/js/util.ts
    ./frontend/node_modules/@asamuzakjp/css-color/src/js/convert.ts
    ./frontend/node_modules/@asamuzakjp/css-color/src/js/cache.ts
    ./frontend/node_modules/@asamuzakjp/css-color/src/js/css-gradient.ts
    ./frontend/node_modules/@asamuzakjp/css-color/src/js/typedef.ts
    ./frontend/node_modules/@asamuzakjp/css-color/src/js/common.ts
    ./frontend/node_modules/@asamuzakjp/css-color/src/js/constant.ts
    ./frontend/node_modules/@asamuzakjp/css-color/src/js/css-calc.ts
    ./frontend/node_modules/@asamuzakjp/css-color/package.json
    ./frontend/node_modules/@asamuzakjp/css-color/README.md
    ./frontend/node_modules/tldts/bin/cli.js
    ./frontend/node_modules/tldts/LICENSE
    ./frontend/node_modules/hermes-parser/dist/transform/astNodeMutationHelpers.js.flow
    ./frontend/node_modules/hermes-parser/dist/transform/SimpleTransform.js
    ./frontend/node_modules/hermes-parser/dist/transform/astArrayMutationHelpers.js.flow
    ./frontend/node_modules/hermes-parser/dist/transform/SimpleTransform.js.flow
    ./frontend/node_modules/hermes-parser/dist/transform/astNodeMutationHelpers.js
    ./frontend/node_modules/hermes-parser/dist/transform/astArrayMutationHelpers.js
    ./frontend/node_modules/css-tree/lib/lexer/generic-urange.js
    ./frontend/node_modules/css-tree/lib/lexer/Lexer.js
    ./frontend/node_modules/css-tree/lib/lexer/structure.js
    ./frontend/node_modules/css-tree/lib/lexer/match-graph.js
    ./frontend/node_modules/css-tree/lib/lexer/search.js
    ./frontend/node_modules/css-tree/lib/lexer/prepare-tokens.js
    ./frontend/node_modules/css-tree/lib/lexer/generic-an-plus-b.js
    ./frontend/node_modules/css-tree/lib/lexer/match.js
    ./frontend/node_modules/css-tree/lib/lexer/generic-const.js
    ./frontend/node_modules/css-tree/lib/lexer/error.js
    ./frontend/node_modules/css-tree/lib/lexer/units.js
    ./frontend/node_modules/css-tree/lib/lexer/index.js
    ./frontend/node_modules/css-tree/lib/lexer/trace.js
    ./frontend/node_modules/css-tree/lib/lexer/generic.js
    ./frontend/node_modules/css-tree/cjs/lexer/search.cjs
    ./frontend/node_modules/css-tree/cjs/lexer/match-graph.cjs
    ./frontend/node_modules/css-tree/cjs/lexer/index.cjs
    ./frontend/node_modules/css-tree/cjs/lexer/generic-an-plus-b.cjs
    ./frontend/node_modules/css-tree/cjs/lexer/generic-const.cjs
    ./frontend/node_modules/css-tree/cjs/lexer/units.cjs
    ./frontend/node_modules/css-tree/cjs/lexer/match.cjs
    ./frontend/node_modules/css-tree/cjs/lexer/Lexer.cjs
    ./frontend/node_modules/css-tree/cjs/lexer/generic.cjs
    ./frontend/node_modules/css-tree/cjs/lexer/error.cjs
    ./frontend/node_modules/css-tree/cjs/lexer/structure.cjs
    ./frontend/node_modules/css-tree/cjs/lexer/prepare-tokens.cjs
    ./frontend/node_modules/css-tree/cjs/lexer/trace.cjs
    ./frontend/node_modules/css-tree/cjs/lexer/generic-urange.cjs
    ./frontend/node_modules/@types/deep-eql/index.d.ts
    ./frontend/node_modules/@types/deep-eql/package.json
    ./frontend/node_modules/@types/deep-eql/README.md
    ./frontend/node_modules/@types/deep-eql/LICENSE
    ./frontend/node_modules/css-tree/lib/syntax/function/var.js
    ./frontend/node_modules/css-tree/lib/syntax/function/expression.js
    ./frontend/node_modules/zod/src/v4/core/zsf.ts
    ./frontend/node_modules/zod/src/v4/core/config.ts
    ./frontend/node_modules/zod/src/v4/core/index.ts
    ./frontend/node_modules/zod/src/v4/core/util.ts
    ./frontend/node_modules/zod/src/v4/core/json-schema-processors.ts
    ./frontend/node_modules/zod/src/v4/core/checks.ts
    ./frontend/node_modules/zod/src/v4/core/core.ts
    ./frontend/node_modules/zod/src/v4/core/to-json-schema.ts
    ./frontend/node_modules/zod/src/v4/core/standard-schema.ts
    ./frontend/node_modules/zod/src/v4/core/api.ts
    ./frontend/node_modules/zod/src/v4/core/schemas.ts
    ./frontend/node_modules/entities/src/escape.ts
    ./frontend/node_modules/entities/src/encode.spec.ts
    ./frontend/node_modules/entities/src/escape.spec.ts
    ./frontend/node_modules/entities/src/encode.ts
    ./frontend/node_modules/entities/src/index.ts
    ./frontend/node_modules/entities/src/decode-codepoint.ts
    ./frontend/node_modules/entities/src/index.spec.ts
    ./frontend/node_modules/entities/src/decode.ts
    ./frontend/node_modules/entities/src/decode.spec.ts
    ./frontend/node_modules/p-locate/index.d.ts
    ./frontend/node_modules/p-locate/package.json
    ./frontend/node_modules/p-locate/readme.md
    ./frontend/node_modules/p-locate/index.js
    ./frontend/node_modules/p-locate/license
    ./frontend/node_modules/jsesc/package.json
    ./frontend/node_modules/jsesc/README.md
    ./frontend/node_modules/jsesc/LICENSE-MIT.txt
    ./frontend/node_modules/jsesc/jsesc.js
    ./frontend/node_modules/entities/src/generated/.eslintrc.json
    ./frontend/node_modules/entities/src/generated/encode-html.ts
    ./frontend/node_modules/entities/src/generated/decode-data-xml.ts
    ./frontend/node_modules/entities/src/generated/decode-data-html.ts
    ./frontend/node_modules/entities/package.json
    ./frontend/node_modules/entities/decode.js
    ./frontend/node_modules/entities/readme.md
    ./frontend/node_modules/entities/decode.d.ts
    ./frontend/node_modules/entities/escape.js
    ./frontend/node_modules/jsesc/bin/jsesc
    ./frontend/node_modules/@asamuzakjp/css-color/node_modules/lru-cache/package.json
    ./frontend/node_modules/@asamuzakjp/css-color/node_modules/lru-cache/README.md
    ./frontend/node_modules/css-tree/lib/syntax/scope/atrulePrelude.js
    ./frontend/node_modules/css-tree/lib/syntax/scope/default.js
    ./frontend/node_modules/css-tree/lib/syntax/scope/value.js
    ./frontend/node_modules/css-tree/lib/syntax/scope/index.js
    ./frontend/node_modules/css-tree/lib/syntax/scope/selector.js
    ./frontend/node_modules/css-tree/lib/syntax/create.js
    ./frontend/node_modules/css-tree/lib/syntax/index.js
    ./frontend/node_modules/zod/src/v4/core/tests/record-constructor.test.ts
    ./frontend/node_modules/zod/src/v4/core/tests/extend.test.ts
    ./frontend/node_modules/zod/src/v4/core/tests/index.test.ts
    ./frontend/node_modules/hermes-parser/dist/estree/StripFlowTypes.js
    ./frontend/node_modules/hermes-parser/dist/estree/StripFlowTypes.js.flow
    ./frontend/node_modules/hermes-parser/dist/estree/StripComponentSyntax.js.flow
    ./frontend/node_modules/hermes-parser/dist/estree/StripFlowTypesForBabel.js
    ./frontend/node_modules/hermes-parser/dist/estree/StripFlowTypesForBabel.js.flow
    ./frontend/node_modules/hermes-parser/dist/estree/StripComponentSyntax.js
    ./frontend/node_modules/css-tree/cjs/convertor/create.cjs
    ./frontend/node_modules/css-tree/cjs/convertor/index.cjs
    ./frontend/node_modules/js-yaml/lib/loader.js
    ./frontend/node_modules/js-yaml/lib/common.js
    ./frontend/node_modules/js-yaml/lib/schema.js
    ./frontend/node_modules/jsesc/man/jsesc.1
    ./frontend/node_modules/css-tree/cjs/data.cjs
    ./frontend/node_modules/hermes-parser/dist/HermesParserDeserializer.js.flow
    ./frontend/node_modules/css-tree/lib/convertor/create.js
    ./frontend/node_modules/css-tree/lib/convertor/index.js
    ./frontend/node_modules/hermes-parser/dist/HermesParserDecodeUTF8String.js.flow
    ./frontend/node_modules/hermes-parser/dist/HermesParserWASM.js
    ./frontend/node_modules/hermes-parser/dist/HermesToESTreeAdapter.js
    ./frontend/node_modules/hermes-parser/dist/HermesParserDecodeUTF8String.js
    ./frontend/node_modules/css-tree/package.json
    ./frontend/node_modules/zod/src/v4/core/tests/locales/nl.test.ts
    ./frontend/node_modules/zod/src/v4/core/tests/locales/ru.test.ts
    ./frontend/node_modules/zod/src/v4/core/tests/locales/be.test.ts
    ./frontend/node_modules/css-tree/README.md
    ./frontend/node_modules/zod/src/v4/core/tests/locales/en.test.ts
    ./frontend/node_modules/zod/src/v4/core/tests/locales/he.test.ts
    ./frontend/node_modules/zod/src/v4/core/tests/locales/es.test.ts
    ./frontend/node_modules/zod/src/v4/core/tests/locales/uz.test.ts
    ./frontend/node_modules/zod/src/v4/core/tests/locales/tr.test.ts
    ./frontend/node_modules/zod/src/v4/core/tests/recursive-tuples.test.ts
    ./frontend/node_modules/zod/src/v4/core/doc.ts
    ./frontend/node_modules/zod/src/v4/core/regexes.ts
    ./frontend/node_modules/zod/src/v4/core/json-schema.ts
    ./frontend/node_modules/zod/src/v4/core/errors.ts
    ./frontend/node_modules/zod/src/v4/core/versions.ts
    ./frontend/node_modules/zod/src/v4/core/parse.ts
    ./frontend/node_modules/zod/src/v4/core/registries.ts
    ./frontend/node_modules/zod/src/v4/core/json-schema-generator.ts
    ./frontend/node_modules/entities/dist/commonjs/index.d.ts.map
    ./frontend/node_modules/entities/dist/commonjs/index.d.ts
    ./frontend/node_modules/entities/dist/commonjs/escape.js.map
    ./frontend/node_modules/entities/dist/commonjs/decode-codepoint.d.ts.map
    ./frontend/node_modules/entities/dist/commonjs/encode.js.map
    ./frontend/node_modules/entities/dist/commonjs/decode.d.ts.map
    ./frontend/node_modules/entities/dist/commonjs/index.js.map
    ./frontend/node_modules/entities/dist/commonjs/decode.js.map
    ./frontend/node_modules/entities/dist/commonjs/package.json
    ./frontend/node_modules/entities/dist/commonjs/decode.js
    ./frontend/node_modules/entities/dist/commonjs/decode.d.ts
    ./frontend/node_modules/entities/dist/commonjs/encode.js
    ./frontend/node_modules/entities/dist/commonjs/decode-codepoint.js.map
    ./frontend/node_modules/entities/dist/commonjs/index.js
    ./frontend/node_modules/entities/dist/commonjs/decode-codepoint.js
    ./frontend/node_modules/entities/dist/commonjs/escape.js
    ./frontend/node_modules/entities/dist/commonjs/escape.d.ts.map
    ./frontend/node_modules/entities/dist/commonjs/decode-codepoint.d.ts
    ./frontend/node_modules/entities/dist/commonjs/encode.d.ts
    ./frontend/node_modules/entities/dist/commonjs/escape.d.ts
    ./frontend/node_modules/entities/dist/commonjs/encode.d.ts.map
    ./frontend/node_modules/hermes-parser/dist/traverse/SimpleTraverser.js
    ./frontend/node_modules/hermes-parser/dist/traverse/getVisitorKeys.js
    ./frontend/node_modules/hermes-parser/dist/traverse/SimpleTraverser.js.flow
    ./frontend/node_modules/hermes-parser/dist/traverse/getVisitorKeys.js.flow
    ./frontend/node_modules/hermes-parser/dist/HermesToESTreeAdapter.js.flow
    ./frontend/node_modules/hermes-parser/dist/HermesAST.js.flow
    ./frontend/node_modules/hermes-parser/dist/getModuleDocblock.js.flow
    ./frontend/node_modules/hermes-parser/dist/HermesParserWASM.js.flow
    ./frontend/node_modules/hermes-parser/dist/ParserOptions.js.flow
    ./frontend/node_modules/postcss/lib/document.js
    ./frontend/node_modules/postcss/lib/input.js
    ./frontend/node_modules/postcss/lib/root.d.ts
    ./frontend/node_modules/postcss/lib/node.d.ts
    ./frontend/node_modules/postcss/lib/parser.js
    ./frontend/node_modules/postcss/lib/container.js
    ./frontend/node_modules/postcss/lib/warning.d.ts
    ./frontend/node_modules/postcss/lib/terminal-highlight.js
    ./frontend/node_modules/postcss/lib/result.js
    ./frontend/node_modules/postcss/lib/no-work-result.js
    ./frontend/node_modules/postcss/lib/symbols.js
    ./frontend/node_modules/postcss/lib/css-syntax-error.d.ts
    ./frontend/node_modules/postcss/lib/rule.js
    ./frontend/node_modules/postcss/lib/tokenize.js
    ./frontend/node_modules/postcss/lib/no-work-result.d.ts
    ./frontend/node_modules/postcss/lib/list.d.ts
    ./frontend/node_modules/postcss/lib/fromJSON.d.ts
    ./frontend/node_modules/postcss/lib/root.js
    ./frontend/node_modules/postcss/lib/parse.js
    ./frontend/node_modules/postcss/lib/node.js
    ./frontend/node_modules/postcss/lib/document.d.ts
    ./frontend/node_modules/postcss/lib/stringify.d.ts
    ./frontend/node_modules/postcss/lib/container.d.ts
    ./frontend/node_modules/postcss/lib/postcss.d.ts
    ./frontend/node_modules/postcss/lib/comment.js
    ./frontend/node_modules/postcss/lib/postcss.mjs
    ./frontend/node_modules/postcss/lib/lazy-result.js
    ./frontend/node_modules/postcss/lib/warn-once.js
    ./frontend/node_modules/postcss/lib/list.js
    ./frontend/node_modules/postcss/lib/processor.d.ts
    ./frontend/node_modules/postcss/lib/declaration.d.ts
    ./frontend/node_modules/postcss/lib/comment.d.ts
    ./frontend/node_modules/postcss/lib/map-generator.js
    ./frontend/node_modules/postcss/lib/stringifier.d.ts
    ./frontend/node_modules/postcss/lib/at-rule.d.ts
    ./frontend/node_modules/postcss/lib/input.d.ts
    ./frontend/node_modules/postcss/lib/fromJSON.js
    ./frontend/node_modules/postcss/lib/previous-map.js
    ./frontend/node_modules/postcss/lib/processor.js
    ./frontend/node_modules/postcss/lib/warning.js
    ./frontend/node_modules/postcss/lib/parse.d.ts
    ./frontend/node_modules/postcss/lib/declaration.js
    ./frontend/node_modules/postcss/lib/at-rule.js
    ./frontend/node_modules/postcss/lib/result.d.ts
    ./frontend/node_modules/postcss/lib/postcss.d.mts
    ./frontend/node_modules/postcss/lib/previous-map.d.ts
    ./frontend/node_modules/postcss/lib/css-syntax-error.js
    ./frontend/node_modules/postcss/lib/stringify.js
    ./frontend/node_modules/postcss/lib/stringifier.js
    ./frontend/node_modules/postcss/lib/lazy-result.d.ts
    ./frontend/node_modules/postcss/lib/rule.d.ts
    ./frontend/node_modules/postcss/lib/postcss.js
    ./frontend/node_modules/postcss/package.json
    ./frontend/node_modules/postcss/README.md
    ./frontend/node_modules/postcss/LICENSE
    ./frontend/node_modules/css-tree/lib/syntax/pseudo/index.js
    ./frontend/node_modules/css-tree/lib/syntax/pseudo/lang.js
    ./frontend/node_modules/color-name/package.json
    ./frontend/node_modules/color-name/README.md
    ./frontend/node_modules/color-name/index.js
    ./frontend/node_modules/color-name/LICENSE
    ./frontend/node_modules/@asamuzakjp/css-color/node_modules/lru-cache/dist/commonjs/index.d.ts.map
    ./frontend/node_modules/@asamuzakjp/css-color/node_modules/lru-cache/dist/commonjs/index.min.js
    ./frontend/node_modules/@asamuzakjp/css-color/node_modules/lru-cache/dist/commonjs/index.d.ts
    ./frontend/node_modules/@asamuzakjp/css-color/node_modules/lru-cache/dist/commonjs/index.js.map
    ./frontend/node_modules/@asamuzakjp/css-color/node_modules/lru-cache/dist/commonjs/package.json
    ./frontend/node_modules/@asamuzakjp/css-color/node_modules/lru-cache/dist/commonjs/index.js
    ./frontend/node_modules/@asamuzakjp/css-color/node_modules/lru-cache/dist/commonjs/index.min.js.map
    ./frontend/node_modules/entities/dist/commonjs/generated/encode-html.js
    ./frontend/node_modules/entities/dist/commonjs/generated/decode-data-xml.js
    ./frontend/node_modules/entities/dist/commonjs/generated/decode-data-html.js
    ./frontend/node_modules/entities/dist/commonjs/generated/encode-html.js.map
    ./frontend/node_modules/entities/dist/commonjs/generated/decode-data-xml.d.ts.map
    ./frontend/node_modules/entities/dist/commonjs/generated/decode-data-html.d.ts.map
    ./frontend/node_modules/entities/dist/commonjs/generated/decode-data-xml.js.map
    ./frontend/node_modules/entities/dist/commonjs/generated/encode-html.d.ts
    ./frontend/node_modules/entities/dist/commonjs/generated/decode-data-html.js.map
    ./frontend/node_modules/entities/dist/commonjs/generated/decode-data-xml.d.ts
    ./frontend/node_modules/entities/dist/commonjs/generated/decode-data-html.d.ts
    ./frontend/node_modules/entities/dist/commonjs/generated/encode-html.d.ts.map
    ./frontend/node_modules/js-yaml/lib/type/map.js
    ./frontend/node_modules/js-yaml/lib/type/int.js
    ./frontend/node_modules/js-yaml/lib/type/seq.js
    ./frontend/node_modules/js-yaml/lib/type/timestamp.js
    ./frontend/node_modules/js-yaml/lib/type/set.js
    ./frontend/node_modules/js-yaml/lib/type/omap.js
    ./frontend/node_modules/js-yaml/lib/type/str.js
    ./frontend/node_modules/js-yaml/lib/type/binary.js
    ./frontend/node_modules/js-yaml/lib/type/merge.js
    ./frontend/node_modules/js-yaml/lib/type/float.js
    ./frontend/node_modules/js-yaml/lib/type/null.js
    ./frontend/node_modules/js-yaml/lib/type/bool.js
    ./frontend/node_modules/js-yaml/lib/type/pairs.js
    ./frontend/node_modules/flat-cache/src/utils.js
    ./frontend/node_modules/flat-cache/src/del.js
    ./frontend/node_modules/flat-cache/src/cache.js
    ./frontend/node_modules/flat-cache/package.json
    ./frontend/node_modules/flat-cache/README.md
    ./frontend/node_modules/flat-cache/changelog.md
    ./frontend/node_modules/flat-cache/LICENSE
    ./frontend/node_modules/css-tree/lib/syntax/config/lexer.js
    ./frontend/node_modules/css-tree/lib/syntax/config/parser.js
    ./frontend/node_modules/css-tree/lib/syntax/config/generator.js
    ./frontend/node_modules/css-tree/lib/syntax/config/parser-selector.js
    ./frontend/node_modules/css-tree/lib/syntax/config/mix.js
    ./frontend/node_modules/css-tree/lib/syntax/config/walker.js
    ./frontend/node_modules/baseline-browser-mapping/LICENSE.txt
    ./frontend/node_modules/hermes-parser/dist/generated/ESTreeVisitorKeys.js.flow
    ./frontend/node_modules/baseline-browser-mapping/package.json
    ./frontend/node_modules/hermes-parser/dist/generated/ParserVisitorKeys.js
    ./frontend/node_modules/baseline-browser-mapping/README.md
    ./frontend/node_modules/hermes-parser/dist/generated/ESTreeVisitorKeys.js
    ./frontend/node_modules/hermes-parser/dist/generated/ParserVisitorKeys.js.flow
    ./frontend/node_modules/hermes-parser/LICENSE
    ./frontend/node_modules/hermes-parser/dist/babel/TransformESTreeToBabel.js
    ./frontend/node_modules/hermes-parser/dist/babel/TransformESTreeToBabel.js.flow
    ./frontend/node_modules/hermes-parser/dist/index.js.flow
    ./frontend/node_modules/hermes-parser/dist/ParserOptions.js
    ./frontend/node_modules/hermes-parser/dist/getModuleDocblock.js
    ./frontend/node_modules/hermes-parser/dist/HermesASTAdapter.js.flow
    ./frontend/node_modules/zod/src/v4/locales/hy.ts
    ./frontend/node_modules/zod/src/v4/locales/he.ts
    ./frontend/node_modules/zod/src/v4/locales/bg.ts
    ./frontend/node_modules/zod/src/v4/locales/ka.ts
    ./frontend/node_modules/zod/src/v4/locales/ja.ts
    ./frontend/node_modules/zod/src/v4/locales/az.ts
    ./frontend/node_modules/zod/src/v4/locales/id.ts
    ./frontend/node_modules/zod/src/v4/locales/index.ts
    ./frontend/node_modules/zod/src/v4/locales/uz.ts
    ./frontend/node_modules/zod/src/v4/locales/sl.ts
    ./frontend/node_modules/zod/src/v4/locales/is.ts
    ./frontend/node_modules/zod/src/v4/locales/ko.ts
    ./frontend/node_modules/zod/src/v4/locales/pl.ts
    ./frontend/node_modules/zod/src/v4/locales/vi.ts
    ./frontend/node_modules/zod/src/v4/locales/pt.ts
    ./frontend/node_modules/zod/src/v4/locales/no.ts
    ./frontend/node_modules/zod/src/v4/locales/yo.ts
    ./frontend/node_modules/zod/src/v4/locales/ru.ts
    ./frontend/node_modules/zod/src/v4/locales/mk.ts
    ./frontend/node_modules/zod/src/v4/locales/th.ts
    ./frontend/node_modules/zod/src/v4/locales/fi.ts
    ./frontend/node_modules/zod/src/v4/locales/ms.ts
    ./frontend/node_modules/zod/src/v4/locales/lt.ts
    ./frontend/node_modules/zod/src/v4/locales/hu.ts
    ./frontend/node_modules/zod/src/v4/locales/km.ts
    ./frontend/node_modules/zod/src/v4/locales/cs.ts
    ./frontend/node_modules/zod/src/v4/locales/nl.ts
    ./frontend/node_modules/zod/src/v4/locales/fr.ts
    ./frontend/node_modules/zod/src/v4/locales/fr-CA.ts
    ./frontend/node_modules/zod/src/v4/locales/uk.ts
    ./frontend/node_modules/zod/src/v4/locales/sv.ts
    ./frontend/node_modules/zod/src/v4/locales/en.ts
    ./frontend/node_modules/zod/src/v4/locales/tr.ts
    ./frontend/node_modules/zod/src/v4/locales/eo.ts
    ./frontend/node_modules/zod/src/v4/locales/ur.ts
    ./frontend/node_modules/zod/src/v4/locales/ps.ts
    ./frontend/node_modules/zod/src/v4/locales/es.ts
    ./frontend/node_modules/zod/src/v4/locales/kh.ts
    ./frontend/node_modules/zod/src/v4/locales/it.ts
    ./frontend/node_modules/zod/src/v4/locales/ar.ts
    ./frontend/node_modules/zod/src/v4/locales/zh-CN.ts
    ./frontend/node_modules/zod/src/v4/locales/be.ts
    ./frontend/node_modules/zod/src/v4/locales/ua.ts
    ./frontend/node_modules/zod/src/v4/locales/ca.ts
    ./frontend/node_modules/zod/src/v4/locales/ta.ts
    ./frontend/node_modules/zod/src/v4/locales/de.ts
    ./frontend/node_modules/zod/src/v4/locales/fa.ts
    ./frontend/node_modules/zod/src/v4/locales/da.ts
    ./frontend/node_modules/zod/src/v4/locales/ota.ts
    ./frontend/node_modules/zod/src/v4/locales/zh-TW.ts
    ./frontend/node_modules/is-potential-custom-element-name/package.json
    ./frontend/node_modules/is-potential-custom-element-name/README.md
    ./frontend/node_modules/is-potential-custom-element-name/LICENSE-MIT.txt
    ./frontend/node_modules/is-potential-custom-element-name/index.js
    ./frontend/node_modules/typescript/SECURITY.md
    ./frontend/node_modules/typescript/ThirdPartyNoticeText.txt
    ./frontend/node_modules/typescript/LICENSE.txt
    ./frontend/node_modules/@asamuzakjp/css-color/node_modules/lru-cache/dist/esm/index.d.ts.map
    ./frontend/node_modules/@asamuzakjp/css-color/node_modules/lru-cache/dist/esm/index.min.js
    ./frontend/node_modules/@asamuzakjp/css-color/node_modules/lru-cache/dist/esm/index.d.ts
    ./frontend/node_modules/@asamuzakjp/css-color/node_modules/lru-cache/dist/esm/index.js.map
    ./frontend/node_modules/@asamuzakjp/css-color/node_modules/lru-cache/dist/esm/package.json
    ./frontend/node_modules/@asamuzakjp/css-color/node_modules/lru-cache/dist/esm/index.js
    ./frontend/node_modules/@asamuzakjp/css-color/node_modules/lru-cache/dist/esm/index.min.js.map
    ./frontend/node_modules/@asamuzakjp/css-color/node_modules/lru-cache/LICENSE.md
    ./frontend/node_modules/entities/dist/esm/index.d.ts.map
    ./frontend/node_modules/entities/dist/esm/index.d.ts
    ./frontend/node_modules/entities/dist/esm/escape.js.map
    ./frontend/node_modules/entities/dist/esm/decode-codepoint.d.ts.map
    ./frontend/node_modules/entities/dist/esm/encode.js.map
    ./frontend/node_modules/entities/dist/esm/decode.d.ts.map
    ./frontend/node_modules/entities/dist/esm/index.js.map
    ./frontend/node_modules/entities/dist/esm/decode.js.map
    ./frontend/node_modules/entities/dist/esm/package.json
    ./frontend/node_modules/entities/dist/esm/decode.js
    ./frontend/node_modules/entities/dist/esm/decode.d.ts
    ./frontend/node_modules/entities/dist/esm/encode.js
    ./frontend/node_modules/entities/dist/esm/decode-codepoint.js.map
    ./frontend/node_modules/entities/dist/esm/index.js
    ./frontend/node_modules/entities/dist/esm/decode-codepoint.js
    ./frontend/node_modules/entities/dist/esm/escape.js
    ./frontend/node_modules/entities/dist/esm/escape.d.ts.map
    ./frontend/node_modules/entities/dist/esm/decode-codepoint.d.ts
    ./frontend/node_modules/entities/dist/esm/encode.d.ts
    ./frontend/node_modules/entities/dist/esm/escape.d.ts
    ./frontend/node_modules/entities/dist/esm/encode.d.ts.map
    ./frontend/node_modules/css-tree/dist/csstree.esm.js
    ./frontend/node_modules/js-yaml/lib/schema/failsafe.js
    ./frontend/node_modules/css-tree/dist/data.js
    ./frontend/node_modules/js-yaml/lib/schema/default.js
    ./frontend/node_modules/css-tree/dist/csstree.js
    ./frontend/node_modules/js-yaml/lib/schema/json.js
    ./frontend/node_modules/js-yaml/lib/schema/core.js
    ./frontend/node_modules/css-tree/dist/version.js
    ./frontend/node_modules/css-tree/dist/data.cjs
    ./frontend/node_modules/css-tree/dist/version.cjs
    ./frontend/node_modules/js-yaml/lib/exception.js
    ./frontend/node_modules/js-yaml/lib/type.js
    ./frontend/node_modules/js-yaml/lib/snippet.js
    ./frontend/node_modules/js-yaml/lib/dumper.js
    ./frontend/node_modules/hermes-parser/dist/utils/mutateESTreeASTForPrettier.js.flow
    ./frontend/node_modules/hermes-parser/dist/utils/createSyntaxError.js
    ./frontend/node_modules/hermes-parser/dist/utils/createSyntaxError.js.flow
    ./frontend/node_modules/hermes-parser/dist/utils/mutateESTreeASTForPrettier.js
    ./frontend/node_modules/css-tree/LICENSE
    ./frontend/node_modules/js-yaml/package.json
    ./frontend/node_modules/js-yaml/README.md
    ./frontend/node_modules/js-yaml/index.js
    ./frontend/node_modules/hermes-parser/dist/HermesParser.js.flow
    ./frontend/node_modules/hermes-parser/dist/HermesASTAdapter.js
    ./frontend/node_modules/hermes-parser/dist/index.js
    ./frontend/node_modules/hermes-parser/dist/HermesParserNodeDeserializers.js.flow
    ./frontend/node_modules/zod/README.md
    ./frontend/node_modules/zod/index.js
    ./frontend/node_modules/zod/index.d.cts
    ./frontend/node_modules/rolldown/package.json
    ./frontend/node_modules/rolldown/README.md
    ./frontend/node_modules/baseline-browser-mapping/dist/cli.cjs
    ./frontend/node_modules/baseline-browser-mapping/dist/index.d.ts
    ./frontend/node_modules/baseline-browser-mapping/dist/index.cjs
    ./frontend/node_modules/baseline-browser-mapping/dist/index.js
    ./frontend/node_modules/entities/dist/esm/generated/encode-html.js
    ./frontend/node_modules/entities/dist/esm/generated/decode-data-xml.js
    ./frontend/node_modules/entities/dist/esm/generated/decode-data-html.js
    ./frontend/node_modules/entities/dist/esm/generated/encode-html.js.map
    ./frontend/node_modules/entities/dist/esm/generated/decode-data-xml.d.ts.map
    ./frontend/node_modules/entities/dist/esm/generated/decode-data-html.d.ts.map
    ./frontend/node_modules/entities/dist/esm/generated/decode-data-xml.js.map
    ./frontend/node_modules/entities/dist/esm/generated/encode-html.d.ts
    ./frontend/node_modules/entities/dist/esm/generated/decode-data-html.js.map
    ./frontend/node_modules/entities/dist/esm/generated/decode-data-xml.d.ts
    ./frontend/node_modules/entities/dist/esm/generated/decode-data-html.d.ts
    ./frontend/node_modules/entities/dist/esm/generated/encode-html.d.ts.map
    ./frontend/node_modules/entities/LICENSE
    ./frontend/node_modules/entities/escape.d.ts
    ./frontend/node_modules/css-tree/lib/definition-syntax/walk.js
    ./frontend/node_modules/css-tree/lib/definition-syntax/parse.js
    ./frontend/node_modules/css-tree/lib/definition-syntax/index.js
    ./frontend/node_modules/css-tree/lib/definition-syntax/generate.js
    ./frontend/node_modules/css-tree/lib/definition-syntax/scanner.js
    ./frontend/node_modules/css-tree/lib/definition-syntax/SyntaxError.js
    ./frontend/node_modules/css-tree/lib/data-patch.js
    ./frontend/node_modules/css-tree/lib/data.js
    ./frontend/node_modules/zod/src/mini/index.ts
    ./frontend/node_modules/js-yaml/dist/js-yaml.mjs
    ./frontend/node_modules/js-yaml/dist/js-yaml.js
    ./frontend/node_modules/js-yaml/dist/js-yaml.min.js
    ./frontend/node_modules/zod/mini/index.d.ts
    ./frontend/node_modules/zod/mini/index.cjs
    ./frontend/node_modules/zod/mini/package.json
    ./frontend/node_modules/zod/mini/index.js
    ./frontend/node_modules/zod/mini/index.d.cts
    ./frontend/node_modules/zod/LICENSE
    ./frontend/node_modules/css-tree/lib/generator/sourceMap.js
    ./frontend/node_modules/css-tree/lib/generator/create.js
    ./frontend/node_modules/css-tree/lib/generator/index.js
    ./frontend/node_modules/css-tree/lib/generator/token-before.js
    ./frontend/node_modules/rolldown/node_modules/@rolldown/pluginutils/package.json
    ./frontend/node_modules/rolldown/node_modules/@rolldown/pluginutils/README.md
    ./frontend/node_modules/.vite/deps/react_jsx-dev-runtime.js.map
    ./frontend/node_modules/.vite/deps/react-router-dom.js.map
    ./frontend/node_modules/.vite/deps/react-dom.js
    ./frontend/node_modules/.vite/deps/package.json
    ./frontend/node_modules/.vite/deps/react_jsx-runtime.js
    ./frontend/node_modules/.vite/deps/react-router-dom.js
    ./frontend/node_modules/.vite/deps/react_jsx-runtime.js.map
    ./frontend/node_modules/.vite/deps/react-TUYU05Ph.js.map
    ./frontend/node_modules/.vite/deps/react-dom.js.map
    ./frontend/node_modules/.vite/deps/react-dom_client.js.map
    ./frontend/node_modules/.vite/deps/react.js
    ./frontend/node_modules/.vite/deps/react_jsx-dev-runtime.js
    ./frontend/node_modules/.vite/deps/react-dom_client.js
    ./frontend/node_modules/.vite/deps/react-TUYU05Ph.js
    ./frontend/node_modules/.vite/deps/_metadata.json
    ./frontend/node_modules/zod/src/locales/index.ts
    ./frontend/node_modules/@asamuzakjp/css-color/dist/esm/index.d.ts
    ./frontend/node_modules/@asamuzakjp/css-color/dist/esm/index.js.map
    ./frontend/node_modules/@asamuzakjp/css-color/dist/esm/index.js
    ./frontend/node_modules/js-yaml/bin/js-yaml.js
    ./frontend/node_modules/js-yaml/LICENSE
    ./frontend/node_modules/@typescript-eslint/visitor-keys/package.json
    ./frontend/node_modules/@typescript-eslint/visitor-keys/README.md
    ./frontend/node_modules/zod/src/v4-mini/index.ts
    ./frontend/node_modules/zod/index.d.ts
    ./frontend/node_modules/zod/index.cjs
    ./frontend/node_modules/css-tree/lib/parser/parse-selector.js
    ./frontend/node_modules/css-tree/lib/parser/create.js
    ./frontend/node_modules/css-tree/lib/parser/index.js
    ./frontend/node_modules/css-tree/lib/parser/SyntaxError.js
    ./frontend/node_modules/css-tree/lib/parser/sequence.js
    ./frontend/node_modules/zod/locales/index.d.ts
    ./frontend/node_modules/zod/locales/index.cjs
    ./frontend/node_modules/zod/locales/package.json
    ./frontend/node_modules/zod/locales/index.js
    ./frontend/node_modules/zod/locales/index.d.cts
    ./frontend/node_modules/css-tree/lib/version.js
    ./frontend/node_modules/@eslint/eslintrc/conf/environments.js
    ./frontend/node_modules/@eslint/eslintrc/conf/config-schema.js
    ./frontend/node_modules/rolldown/node_modules/@rolldown/pluginutils/dist/index.d.ts
    ./frontend/node_modules/typescript/lib/lib.es2015.d.ts
    ./frontend/node_modules/typescript/lib/lib.es2015.collection.d.ts
    ./frontend/node_modules/typescript/lib/lib.esnext.array.d.ts
    ./frontend/node_modules/typescript/lib/lib.es2017.arraybuffer.d.ts
    ./frontend/node_modules/typescript/lib/lib.es2015.symbol.d.ts
    ./frontend/node_modules/typescript/lib/lib.webworker.importscripts.d.ts
    ./frontend/node_modules/undici-types/mock-errors.d.ts
    ./frontend/node_modules/undici-types/mock-interceptor.d.ts
    ./frontend/node_modules/undici-types/content-type.d.ts
    ./frontend/node_modules/undici-types/client.d.ts
    ./frontend/node_modules/undici-types/global-dispatcher.d.ts
    ./frontend/node_modules/undici-types/retry-agent.d.ts
    ./frontend/node_modules/undici-types/proxy-agent.d.ts
    ./frontend/node_modules/undici-types/mock-pool.d.ts
    ./frontend/node_modules/undici-types/index.d.ts
    ./frontend/node_modules/undici-types/patch.d.ts
    ./frontend/node_modules/undici-types/h2c-client.d.ts
    ./frontend/node_modules/undici-types/util.d.ts
    ./frontend/node_modules/undici-types/diagnostics-channel.d.ts
    ./frontend/node_modules/undici-types/mock-call-history.d.ts
    ./frontend/node_modules/undici-types/pool.d.ts
    ./frontend/node_modules/undici-types/cookies.d.ts
    ./frontend/node_modules/undici-types/cache.d.ts
    ./frontend/node_modules/undici-types/package.json
    ./frontend/node_modules/undici-types/handlers.d.ts
    ./frontend/node_modules/undici-types/formdata.d.ts
    ./frontend/node_modules/undici-types/webidl.d.ts
    ./frontend/node_modules/undici-types/README.md
    ./frontend/node_modules/undici-types/fetch.d.ts
    ./frontend/node_modules/undici-types/interceptors.d.ts
    ./frontend/node_modules/undici-types/mock-agent.d.ts
    ./frontend/node_modules/undici-types/agent.d.ts
    ./frontend/node_modules/undici-types/balanced-pool.d.ts
    ./frontend/node_modules/undici-types/retry-handler.d.ts
    ./frontend/node_modules/undici-types/connector.d.ts
    ./frontend/node_modules/undici-types/websocket.d.ts
    ./frontend/node_modules/undici-types/client-stats.d.ts
    ./frontend/node_modules/undici-types/utility.d.ts
    ./frontend/node_modules/undici-types/errors.d.ts
    ./frontend/node_modules/undici-types/dispatcher.d.ts
    ./frontend/node_modules/undici-types/cache-interceptor.d.ts
    ./frontend/node_modules/undici-types/readable.d.ts
    ./frontend/node_modules/undici-types/LICENSE
    ./frontend/node_modules/undici-types/api.d.ts
    ./frontend/node_modules/undici-types/env-http-proxy-agent.d.ts
    ./frontend/node_modules/undici-types/eventsource.d.ts
    ./frontend/node_modules/undici-types/mock-client.d.ts
    ./frontend/node_modules/undici-types/pool-stats.d.ts
    ./frontend/node_modules/undici-types/header.d.ts
    ./frontend/node_modules/undici-types/global-origin.d.ts
    ./frontend/node_modules/undici-types/snapshot-agent.d.ts
    ./frontend/node_modules/@eslint/eslintrc/lib/config-array-factory.js
    ./frontend/node_modules/@eslint/eslintrc/lib/index-universal.js
    ./frontend/node_modules/css-tree/lib/utils/url.js
    ./frontend/node_modules/css-tree/lib/utils/names.js
    ./frontend/node_modules/css-tree/lib/utils/ident.js
    ./frontend/node_modules/css-tree/lib/utils/clone.js
    ./frontend/node_modules/css-tree/lib/utils/string.js
    ./frontend/node_modules/css-tree/lib/utils/List.js
    ./frontend/node_modules/css-tree/lib/utils/index.js
    ./frontend/node_modules/css-tree/lib/utils/create-custom-error.js
    ./frontend/node_modules/.vite/vitest/da39a3ee5e6b4b0d3255bfef95601890afd80709/results.json
    ./frontend/node_modules/rolldown/LICENSE
    ./frontend/node_modules/zod/v4-mini/index.d.ts
    ./frontend/node_modules/zod/v4-mini/index.cjs
    ./frontend/node_modules/zod/v4-mini/package.json
    ./frontend/node_modules/zod/v4-mini/index.js
    ./frontend/node_modules/zod/v4-mini/index.d.cts
    ./frontend/node_modules/rolldown/node_modules/@rolldown/pluginutils/dist/filter/filter-vite-plugins.d.ts
    ./frontend/node_modules/rolldown/node_modules/@rolldown/pluginutils/dist/filter/index.d.ts
    ./frontend/node_modules/rolldown/node_modules/@rolldown/pluginutils/dist/filter/filter-vite-plugins.js
    ./frontend/node_modules/rolldown/node_modules/@rolldown/pluginutils/dist/filter/composable-filters.js
    ./frontend/node_modules/rolldown/node_modules/@rolldown/pluginutils/dist/filter/index.js
    ./frontend/node_modules/rolldown/node_modules/@rolldown/pluginutils/dist/filter/simple-filters.js
    ./frontend/node_modules/rolldown/node_modules/@rolldown/pluginutils/dist/filter/composable-filters.d.ts
    ./frontend/node_modules/rolldown/node_modules/@rolldown/pluginutils/dist/filter/simple-filters.d.ts
    ./frontend/node_modules/rolldown/node_modules/@rolldown/pluginutils/dist/utils.js
    ./frontend/node_modules/rolldown/node_modules/@rolldown/pluginutils/dist/utils.d.ts
    ./frontend/node_modules/rolldown/node_modules/@rolldown/pluginutils/dist/index.js
    ./frontend/node_modules/rolldown/node_modules/@rolldown/pluginutils/LICENSE
    ./frontend/node_modules/@typescript-eslint/visitor-keys/node_modules/eslint-visitor-keys/lib/index.js
    ./frontend/node_modules/@asamuzakjp/css-color/dist/esm/js/constant.js.map
    ./frontend/node_modules/typescript/lib/tr/diagnosticMessages.generated.json
    ./frontend/node_modules/@typescript-eslint/visitor-keys/node_modules/eslint-visitor-keys/lib/visitor-keys.js
    ./frontend/node_modules/typescript/lib/lib.es2019.d.ts
    ./frontend/node_modules/typescript/lib/lib.es2017.string.d.ts
    ./frontend/node_modules/typescript/lib/typescript.d.ts
    ./frontend/node_modules/typescript/lib/watchGuard.js
    ./frontend/node_modules/typescript/lib/lib.es2023.d.ts
    ./frontend/node_modules/typescript/lib/lib.es2017.object.d.ts
    ./frontend/node_modules/typescript/lib/lib.es2016.full.d.ts
    ./frontend/node_modules/typescript/lib/lib.es2021.weakref.d.ts
    ./frontend/node_modules/typescript/lib/lib.es2022.d.ts
    ./frontend/node_modules/typescript/lib/typingsInstaller.js
    ./frontend/node_modules/typescript/lib/lib.es2018.asyncgenerator.d.ts
    ./frontend/node_modules/typescript/lib/lib.es2023.full.d.ts
    ./frontend/node_modules/typescript/lib/lib.es2020.string.d.ts
    ./frontend/node_modules/typescript/lib/lib.esnext.full.d.ts
    ./frontend/node_modules/typescript/lib/lib.es2018.d.ts
    ./frontend/node_modules/typescript/lib/lib.d.ts
    ./frontend/node_modules/@typescript-eslint/visitor-keys/node_modules/eslint-visitor-keys/package.json
    ./frontend/node_modules/typescript/lib/lib.es2019.symbol.d.ts
    ./frontend/node_modules/@typescript-eslint/visitor-keys/node_modules/eslint-visitor-keys/README.md
    ./frontend/node_modules/typescript/lib/tsserverlibrary.d.ts
    ./frontend/node_modules/p-limit/index.d.ts
    ./frontend/node_modules/p-limit/package.json
    ./frontend/node_modules/p-limit/readme.md
    ./frontend/node_modules/p-limit/index.js
    ./frontend/node_modules/p-limit/license
    ./frontend/node_modules/file-entry-cache/package.json
    ./frontend/node_modules/file-entry-cache/README.md
    ./frontend/node_modules/file-entry-cache/cache.js
    ./frontend/node_modules/file-entry-cache/LICENSE
    ./frontend/node_modules/@asamuzakjp/css-color/dist/esm/js/common.js.map
    ./frontend/node_modules/@asamuzakjp/css-color/dist/esm/js/relative-color.js.map
    ./frontend/node_modules/@asamuzakjp/css-color/dist/esm/js/resolve.js.map
    ./frontend/node_modules/@asamuzakjp/css-color/dist/esm/js/css-gradient.d.ts
    ./frontend/node_modules/@asamuzakjp/css-color/dist/esm/js/util.d.ts
    ./frontend/node_modules/@asamuzakjp/css-color/dist/esm/js/typedef.d.ts
    ./frontend/node_modules/@asamuzakjp/css-color/dist/esm/js/common.js
    ./frontend/node_modules/@asamuzakjp/css-color/dist/esm/js/css-calc.js.map
    ./frontend/node_modules/@asamuzakjp/css-color/dist/esm/js/css-calc.js
    ./frontend/node_modules/@asamuzakjp/css-color/dist/esm/js/constant.js
    ./frontend/node_modules/@asamuzakjp/css-color/dist/esm/js/cache.d.ts
    ./frontend/node_modules/@asamuzakjp/css-color/dist/esm/js/constant.d.ts
    ./frontend/node_modules/@asamuzakjp/css-color/dist/esm/js/css-calc.d.ts
    ./frontend/node_modules/@asamuzakjp/css-color/dist/esm/js/relative-color.js
    ./frontend/node_modules/@asamuzakjp/css-color/dist/esm/js/color.js
    ./frontend/node_modules/@asamuzakjp/css-color/dist/esm/js/css-var.js
    ./frontend/node_modules/@asamuzakjp/css-color/dist/esm/js/resolve.js
    ./frontend/node_modules/@asamuzakjp/css-color/dist/esm/js/css-gradient.js.map
    ./frontend/node_modules/@asamuzakjp/css-color/dist/esm/js/common.d.ts
    ./frontend/node_modules/@asamuzakjp/css-color/dist/esm/js/css-var.js.map
    ./frontend/node_modules/@asamuzakjp/css-color/dist/esm/js/cache.js
    ./frontend/node_modules/@asamuzakjp/css-color/dist/esm/js/css-gradient.js
    ./frontend/node_modules/@asamuzakjp/css-color/dist/esm/js/util.js.map
    ./frontend/node_modules/@asamuzakjp/css-color/dist/esm/js/color.js.map
    ./frontend/node_modules/@asamuzakjp/css-color/dist/esm/js/relative-color.d.ts
    ./frontend/node_modules/@asamuzakjp/css-color/dist/esm/js/util.js
    ./frontend/node_modules/@asamuzakjp/css-color/dist/esm/js/convert.d.ts
    ./frontend/node_modules/@asamuzakjp/css-color/dist/esm/js/convert.js
    ./frontend/node_modules/@asamuzakjp/css-color/dist/esm/js/color.d.ts
    ./frontend/node_modules/@asamuzakjp/css-color/dist/esm/js/cache.js.map
    ./frontend/node_modules/@asamuzakjp/css-color/dist/esm/js/css-var.d.ts
    ./frontend/node_modules/@asamuzakjp/css-color/dist/esm/js/resolve.d.ts
    ./frontend/node_modules/@asamuzakjp/css-color/dist/esm/js/convert.js.map
    ./frontend/node_modules/@asamuzakjp/css-color/LICENSE
    ./frontend/node_modules/locate-path/index.d.ts
    ./frontend/node_modules/locate-path/package.json
    ./frontend/node_modules/locate-path/readme.md
    ./frontend/node_modules/locate-path/index.js
    ./frontend/node_modules/locate-path/license
    ./frontend/node_modules/rolldown/dist/plugins-index.mjs
    ./frontend/node_modules/rolldown/dist/cli.mjs
    ./frontend/node_modules/rolldown/dist/config.mjs
    ./frontend/node_modules/rolldown/dist/filter-index.d.mts
    ./frontend/node_modules/rolldown/dist/experimental-runtime-types.d.ts
    ./frontend/node_modules/rolldown/dist/utils-index.d.mts
    ./frontend/node_modules/rolldown/dist/plugins-index.d.mts
    ./frontend/node_modules/rolldown/dist/cli.d.mts
    ./frontend/node_modules/rolldown/dist/index.mjs
    ./frontend/node_modules/rolldown/dist/parallel-plugin-worker.d.mts
    ./frontend/node_modules/rolldown/dist/experimental-index.mjs
    ./frontend/node_modules/zod/v4/index.d.ts
    ./frontend/node_modules/zod/v4/index.cjs
    ./frontend/node_modules/zod/v4/package.json
    ./frontend/node_modules/zod/v4/index.js
    ./frontend/node_modules/zod/v4/index.d.cts
    ./frontend/node_modules/acorn/package.json
    ./frontend/node_modules/acorn/README.md
    ./frontend/node_modules/@eslint/eslintrc/lib/shared/config-validator.js
    ./frontend/node_modules/@eslint/eslintrc/lib/shared/ajv.js
    ./frontend/node_modules/@eslint/eslintrc/lib/shared/config-ops.js
    ./frontend/node_modules/@eslint/eslintrc/lib/shared/deprecation-warnings.js
    ./frontend/node_modules/@eslint/eslintrc/lib/shared/relative-module-resolver.js
    ./frontend/node_modules/@eslint/eslintrc/lib/shared/deep-merge-arrays.js
    ./frontend/node_modules/@eslint/eslintrc/lib/shared/types.js
    ./frontend/node_modules/@eslint/eslintrc/lib/shared/naming.js
    ./frontend/node_modules/@eslint/eslintrc/lib/index.js
    ./frontend/node_modules/@eslint/eslintrc/lib/cascading-config-array-factory.js
    ./frontend/node_modules/typescript/lib/es/diagnosticMessages.generated.json
    ./frontend/node_modules/typescript/lib/lib.webworker.d.ts
    ./frontend/node_modules/@typescript-eslint/visitor-keys/node_modules/eslint-visitor-keys/dist/index.d.ts
    ./frontend/node_modules/@typescript-eslint/visitor-keys/node_modules/eslint-visitor-keys/dist/eslint-visitor-keys.cjs
    ./frontend/node_modules/@typescript-eslint/visitor-keys/node_modules/eslint-visitor-keys/dist/visitor-keys.d.ts
    ./frontend/node_modules/@typescript-eslint/visitor-keys/node_modules/eslint-visitor-keys/dist/eslint-visitor-keys.d.cts
    ./frontend/node_modules/@typescript-eslint/visitor-keys/node_modules/eslint-visitor-keys/LICENSE
    ./frontend/node_modules/strip-indent/index.d.ts
    ./frontend/node_modules/strip-indent/package.json
    ./frontend/node_modules/strip-indent/readme.md
    ./frontend/node_modules/strip-indent/index.js
    ./frontend/node_modules/strip-indent/license
    ./frontend/node_modules/acorn/dist/acorn.d.mts
    ./frontend/node_modules/acorn/dist/acorn.js
    ./frontend/node_modules/acorn/dist/acorn.d.ts
    ./frontend/node_modules/acorn/dist/acorn.mjs
    ./frontend/node_modules/acorn/dist/bin.js
    ./frontend/node_modules/acorn/CHANGELOG.md
    ./frontend/node_modules/zod/v3/helpers/util.d.cts
    ./frontend/node_modules/zod/v3/helpers/typeAliases.cjs
    ./frontend/node_modules/zod/v3/helpers/util.d.ts
    ./frontend/node_modules/zod/v3/helpers/typeAliases.d.cts
    ./frontend/node_modules/zod/v3/helpers/parseUtil.js
    ./frontend/node_modules/zod/v3/helpers/partialUtil.cjs
    ./frontend/node_modules/zod/v3/helpers/parseUtil.cjs
    ./frontend/node_modules/zod/v3/helpers/partialUtil.d.ts
    ./frontend/node_modules/zod/v3/helpers/typeAliases.js
    ./frontend/node_modules/zod/v3/helpers/parseUtil.d.cts
    ./frontend/node_modules/zod/v3/helpers/errorUtil.js
    ./frontend/node_modules/zod/v3/helpers/parseUtil.d.ts
    ./frontend/node_modules/zod/v3/helpers/enumUtil.d.cts
    ./frontend/node_modules/zod/v3/helpers/enumUtil.cjs
    ./frontend/node_modules/zod/v3/helpers/enumUtil.d.ts
    ./frontend/node_modules/zod/v3/helpers/partialUtil.d.cts
    ./frontend/node_modules/zod/v3/helpers/util.cjs
    ./frontend/node_modules/zod/v3/helpers/typeAliases.d.ts
    ./frontend/node_modules/zod/v3/helpers/errorUtil.cjs
    ./frontend/node_modules/zod/v3/helpers/partialUtil.js
    ./frontend/node_modules/zod/v3/helpers/util.js
    ./frontend/node_modules/zod/v3/helpers/errorUtil.d.ts
    ./frontend/node_modules/zod/v3/helpers/enumUtil.js
    ./frontend/node_modules/zod/v3/helpers/errorUtil.d.cts
    ./frontend/node_modules/zod/v3/standard-schema.js
    ./frontend/node_modules/zod/v3/index.d.ts
    ./frontend/node_modules/zod/v3/external.d.ts
    ./frontend/node_modules/zod/v3/index.cjs
    ./frontend/node_modules/zod/v3/errors.d.cts
    ./frontend/node_modules/zod/v3/errors.js
    ./frontend/node_modules/zod/v3/package.json
    ./frontend/node_modules/zod/v3/external.cjs
    ./frontend/node_modules/zod/v3/errors.cjs
    ./frontend/node_modules/zod/v3/types.d.cts
    ./frontend/node_modules/zod/v3/external.d.cts
    ./frontend/node_modules/zod/v3/ZodError.d.cts
    ./frontend/node_modules/zod/v3/standard-schema.cjs
    ./frontend/node_modules/zod/v3/external.js
    ./frontend/node_modules/zod/v3/index.js
    ./frontend/node_modules/zod/v3/ZodError.d.ts
    ./frontend/node_modules/zod/v3/standard-schema.d.cts
    ./frontend/node_modules/zod/v3/index.d.cts
    ./frontend/node_modules/zod/v3/types.d.ts
    ./frontend/node_modules/zod/v3/types.cjs
    ./frontend/node_modules/zod/v3/errors.d.ts
    ./frontend/node_modules/zod/v3/ZodError.cjs
    ./frontend/node_modules/zod/v3/types.js
    ./frontend/node_modules/typescript/lib/fr/diagnosticMessages.generated.json
    ./frontend/node_modules/typescript/lib/lib.es2017.intl.d.ts
    ./frontend/node_modules/typescript/lib/lib.es2017.sharedmemory.d.ts
    ./frontend/node_modules/typescript/lib/lib.es2022.regexp.d.ts
    ./frontend/node_modules/typescript/lib/lib.es2022.intl.d.ts
    ./frontend/node_modules/acorn/bin/acorn
    ./frontend/node_modules/acorn/LICENSE
    ./frontend/node_modules/zod/v4/classic/from-json-schema.d.cts
    ./frontend/node_modules/zod/v4/classic/index.d.ts
    ./frontend/node_modules/zod/v4/classic/coerce.cjs
    ./frontend/node_modules/zod/v4/classic/coerce.js
    ./frontend/node_modules/zod/v4/classic/external.d.ts
    ./frontend/node_modules/zod/v4/classic/from-json-schema.d.ts
    ./frontend/node_modules/zod/v4/classic/schemas.js
    ./frontend/node_modules/zod/v4/classic/from-json-schema.js
    ./frontend/node_modules/zod/v4/classic/compat.d.ts
    ./frontend/node_modules/zod/v4/classic/schemas.d.ts
    ./frontend/node_modules/zod/v4/classic/index.cjs
    ./frontend/node_modules/zod/v4/classic/errors.d.cts
    ./frontend/node_modules/zod/v4/classic/errors.js
    ./frontend/node_modules/zod/v4/classic/package.json
    ./frontend/node_modules/zod/v4/classic/parse.js
    ./frontend/node_modules/zod/v4/classic/external.cjs
    ./frontend/node_modules/zod/v4/classic/errors.cjs
    ./frontend/node_modules/zod/v4/classic/iso.js
    ./frontend/node_modules/zod/v4/classic/external.d.cts
    ./frontend/node_modules/zod/v4/classic/checks.d.ts
    ./frontend/node_modules/zod/v4/classic/parse.d.cts
    ./frontend/node_modules/zod/v4/classic/external.js
    ./frontend/node_modules/zod/v4/classic/compat.js
    ./frontend/node_modules/zod/v4/classic/parse.cjs
    ./frontend/node_modules/zod/v4/classic/index.js
    ./frontend/node_modules/zod/v4/classic/coerce.d.cts
    ./frontend/node_modules/zod/v4/classic/iso.d.ts
    ./frontend/node_modules/zod/v4/classic/iso.cjs
    ./frontend/node_modules/zod/v4/classic/index.d.cts
    ./frontend/node_modules/zod/v4/classic/compat.d.cts
    ./frontend/node_modules/zod/v4/classic/compat.cjs
    ./frontend/node_modules/zod/v4/classic/errors.d.ts
    ./frontend/node_modules/zod/v4/classic/from-json-schema.cjs
    ./frontend/node_modules/zod/v4/classic/parse.d.ts
    ./frontend/node_modules/zod/v4/classic/schemas.cjs
    ./frontend/node_modules/zod/v4/classic/coerce.d.ts
    ./frontend/node_modules/zod/v4/classic/checks.cjs
    ./frontend/node_modules/zod/v4/classic/iso.d.cts
    ./frontend/node_modules/zod/v4/classic/checks.js
    ./frontend/node_modules/zod/v4/classic/checks.d.cts
    ./frontend/node_modules/zod/v4/classic/schemas.d.cts
    ./frontend/node_modules/rolldown/dist/shared/constructors-D3ZqEbT5.mjs
    ./frontend/node_modules/rolldown/dist/shared/define-config-DJOr6Iwt.mjs
    ./frontend/node_modules/rolldown/dist/shared/resolve-tsconfig-DJjTYbYr.mjs
    ./frontend/node_modules/rolldown/dist/shared/error-BLhcSyeg.mjs
    ./frontend/node_modules/rolldown/dist/shared/normalize-string-or-regex-CCT059Zu.mjs
    ./frontend/node_modules/rolldown/dist/shared/load-config-CzS8HOQ2.mjs
    ./frontend/node_modules/rolldown/dist/shared/get-log-filter-semyr3Lj.d.mts
    ./frontend/node_modules/rolldown/dist/shared/transform-C_gBfjMR.d.mts
    ./frontend/node_modules/rolldown/dist/shared/define-config-BkRKRADp.d.mts
    ./frontend/node_modules/rolldown/dist/shared/constructors-DRe7RuMC.d.mts
    ./frontend/node_modules/rolldown/dist/shared/logs-D80CXhvg.mjs
    ./frontend/node_modules/rolldown/dist/shared/binding-CkWPGrSM.mjs
    ./frontend/node_modules/rolldown/dist/shared/rolldown-AJ-jnEZ_.mjs
    ./frontend/node_modules/rolldown/dist/shared/binding-CYVfiOV3.d.mts
    ./frontend/node_modules/rolldown/dist/shared/misc-DJYbNKZX.mjs
    ./frontend/node_modules/rolldown/dist/shared/prompt-BYQIwEjg.mjs
    ./frontend/node_modules/rolldown/dist/shared/bindingify-input-options-e7ze4hPR.mjs
    ./frontend/node_modules/rolldown/dist/shared/parse-BGipdujE.mjs
    ./frontend/node_modules/rolldown/dist/shared/watch-CsdkXVu3.mjs
    ./frontend/node_modules/rolldown/dist/shared/rolldown-build-CPrIX9V6.mjs
    ./frontend/node_modules/rolldown/dist/shared/logging-C6h4g8dA.d.mts
    ./frontend/node_modules/rolldown/dist/utils-index.mjs
    ./frontend/node_modules/rolldown/dist/filter-index.mjs
    ./frontend/node_modules/rolldown/dist/experimental-index.d.mts
    ./frontend/node_modules/rolldown/dist/parse-ast-index.d.mts
    ./frontend/node_modules/rolldown/dist/index.d.mts
    ./frontend/node_modules/rolldown/dist/get-log-filter.d.mts
    ./frontend/node_modules/rolldown/dist/parallel-plugin.mjs
    ./frontend/node_modules/rolldown/dist/parallel-plugin.d.mts
    ./frontend/node_modules/rolldown/dist/config.d.mts
    ./frontend/node_modules/rolldown/dist/parse-ast-index.mjs
    ./frontend/node_modules/rolldown/dist/get-log-filter.mjs
    ./frontend/node_modules/rolldown/dist/parallel-plugin-worker.mjs
    ./frontend/node_modules/nanoid/index.d.ts
    ./frontend/node_modules/nanoid/nanoid.js
    ./frontend/node_modules/type-check/lib/check.js
    ./frontend/node_modules/type-check/lib/index.js
    ./frontend/node_modules/type-check/lib/parse-type.js
    ./frontend/node_modules/type-check/package.json
    ./frontend/node_modules/type-check/README.md
    ./frontend/node_modules/type-check/LICENSE
    ./frontend/node_modules/@eslint/eslintrc/lib/types/index.d.ts
    ./frontend/node_modules/zod/v4/mini/index.d.ts
    ./frontend/node_modules/@eslint/eslintrc/lib/flat-compat.js
    ./frontend/node_modules/typescript/lib/ko/diagnosticMessages.generated.json
    ./frontend/node_modules/typescript/lib/lib.es2024.full.d.ts
    ./frontend/node_modules/nanoid/url-alphabet/index.cjs
    ./frontend/node_modules/nanoid/url-alphabet/package.json
    ./frontend/node_modules/nanoid/url-alphabet/index.js
    ./frontend/node_modules/nanoid/index.cjs
    ./frontend/node_modules/nanoid/index.browser.cjs
    ./frontend/node_modules/nanoid/package.json
    ./frontend/node_modules/zod/v3/locales/en.cjs
    ./frontend/node_modules/zod/v3/locales/en.js
    ./frontend/node_modules/zod/v3/locales/en.d.cts
    ./frontend/node_modules/zod/v3/locales/en.d.ts
    ./frontend/node_modules/zod/v3/standard-schema.d.ts
    ./frontend/node_modules/zod/v3/ZodError.js
    ./frontend/node_modules/zod/package.json
    ./frontend/node_modules/zod/v4/mini/coerce.cjs
    ./frontend/node_modules/zod/v4/mini/coerce.js
    ./frontend/node_modules/zod/v4/mini/external.d.ts
    ./frontend/node_modules/zod/v4/mini/schemas.js
    ./frontend/node_modules/zod/v4/mini/schemas.d.ts
    ./frontend/node_modules/zod/v4/mini/index.cjs
    ./frontend/node_modules/zod/v4/mini/package.json
    ./frontend/node_modules/zod/v4/mini/parse.js
    ./frontend/node_modules/zod/v4/mini/external.cjs
    ./frontend/node_modules/zod/v4/mini/iso.js
    ./frontend/node_modules/zod/v4/mini/external.d.cts
    ./frontend/node_modules/zod/v4/mini/checks.d.ts
    ./frontend/node_modules/zod/v4/mini/parse.d.cts
    ./frontend/node_modules/zod/v4/mini/external.js
    ./frontend/node_modules/zod/v4/mini/parse.cjs
    ./frontend/node_modules/zod/v4/mini/index.js
    ./frontend/node_modules/zod/v4/mini/coerce.d.cts
    ./frontend/node_modules/zod/v4/mini/iso.d.ts
    ./frontend/node_modules/zod/v4/mini/iso.cjs
    ./frontend/node_modules/zod/v4/mini/index.d.cts
    ./frontend/node_modules/zod/v4/mini/parse.d.ts
    ./frontend/node_modules/zod/v4/mini/schemas.cjs
    ./frontend/node_modules/zod/v4/mini/coerce.d.ts
    ./frontend/node_modules/zod/v4/mini/checks.cjs
    ./frontend/node_modules/zod/v4/mini/iso.d.cts
    ./frontend/node_modules/zod/v4/mini/checks.js
    ./frontend/node_modules/zod/v4/mini/checks.d.cts
    ./frontend/node_modules/zod/v4/mini/schemas.d.cts
    ./frontend/node_modules/typescript/lib/lib.es2021.d.ts
    ./frontend/node_modules/typescript/lib/lib.esnext.promise.d.ts
    ./frontend/node_modules/typescript/lib/lib.es2015.generator.d.ts
    ./frontend/node_modules/typescript/lib/lib.es2015.proxy.d.ts
    ./frontend/node_modules/typescript/lib/lib.esnext.iterator.d.ts
    ./frontend/node_modules/typescript/lib/lib.es2022.object.d.ts
    ./frontend/node_modules/typescript/lib/typescript.js
    ./frontend/node_modules/typescript/lib/lib.es2020.full.d.ts
    ./frontend/node_modules/typescript/lib/lib.es2020.d.ts
    ./frontend/node_modules/typescript/lib/lib.es2022.string.d.ts
    ./frontend/node_modules/typescript/lib/lib.es2019.intl.d.ts
    ./frontend/node_modules/@typescript-eslint/visitor-keys/dist/get-keys.js
    ./frontend/node_modules/@typescript-eslint/visitor-keys/dist/index.d.ts
    ./frontend/node_modules/@typescript-eslint/visitor-keys/dist/visitor-keys.d.ts
    ./frontend/node_modules/@typescript-eslint/visitor-keys/dist/tsconfig.build.tsbuildinfo
    ./frontend/node_modules/@typescript-eslint/visitor-keys/dist/index.js
    ./frontend/node_modules/@typescript-eslint/visitor-keys/dist/get-keys.d.ts
    ./frontend/node_modules/@typescript-eslint/visitor-keys/dist/visitor-keys.js
    ./frontend/node_modules/@typescript-eslint/visitor-keys/LICENSE
    ./frontend/node_modules/tinyrainbow/LICENCE
    ./frontend/node_modules/tinyrainbow/package.json
    ./frontend/node_modules/@eslint/eslintrc/lib/config-array/index.js
    ./frontend/node_modules/tinyrainbow/README.md
    ./frontend/node_modules/@eslint/eslintrc/lib/config-array/ignore-pattern.js
    ./frontend/node_modules/@eslint/eslintrc/lib/config-array/config-array.js
    ./frontend/node_modules/@eslint/eslintrc/lib/config-array/override-tester.js
    ./frontend/node_modules/@eslint/eslintrc/lib/config-array/extracted-config.js
    ./frontend/node_modules/@eslint/eslintrc/lib/config-array/config-dependency.js
    ./frontend/node_modules/@eslint/eslintrc/universal.js
    ./frontend/node_modules/@eslint/eslintrc/package.json
    ./frontend/node_modules/@eslint/eslintrc/README.md
    ./frontend/node_modules/rolldown/bin/cli.mjs
    ./frontend/node_modules/nanoid/non-secure/index.d.ts
    ./frontend/node_modules/nanoid/non-secure/index.cjs
    ./frontend/node_modules/nanoid/non-secure/package.json
    ./frontend/node_modules/nanoid/non-secure/index.js
    ./frontend/node_modules/nanoid/README.md
    ./frontend/node_modules/nanoid/index.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/index.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/rules.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/raw-plugin.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/package.json
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/README.md
    ./frontend/node_modules/typescript/lib/de/diagnosticMessages.generated.json
    ./frontend/node_modules/typescript/lib/lib.esnext.error.d.ts
    ./frontend/node_modules/nanoid/async/index.d.ts
    ./frontend/node_modules/nanoid/async/index.native.js
    ./frontend/node_modules/nanoid/async/index.cjs
    ./frontend/node_modules/nanoid/async/index.browser.cjs
    ./frontend/node_modules/nanoid/async/package.json
    ./frontend/node_modules/nanoid/async/index.js
    ./frontend/node_modules/nanoid/async/index.browser.js
    ./frontend/node_modules/nanoid/index.browser.js
    ./frontend/node_modules/nanoid/index.d.cts
    ./frontend/node_modules/tinyrainbow/dist/index.d.ts
    ./frontend/node_modules/tinyrainbow/dist/index.js
    ./frontend/node_modules/@humanwhocodes/module-importer/src/module-importer.cjs
    ./frontend/node_modules/@humanwhocodes/module-importer/src/module-importer.js
    ./frontend/node_modules/@humanwhocodes/module-importer/package.json
    ./frontend/node_modules/@humanwhocodes/module-importer/README.md
    ./frontend/node_modules/@asamuzakjp/nwsapi/src/nwsapi.js
    ./frontend/node_modules/@asamuzakjp/nwsapi/package.json
    ./frontend/node_modules/@asamuzakjp/nwsapi/README.md
    ./frontend/node_modules/@asamuzakjp/nwsapi/LICENSE
    ./frontend/node_modules/typescript/lib/pl/diagnosticMessages.generated.json
    ./frontend/node_modules/typescript/lib/lib.dom.asynciterable.d.ts
    ./frontend/node_modules/typescript/lib/lib.es2015.core.d.ts
    ./frontend/node_modules/typescript/lib/lib.es2016.d.ts
    ./frontend/node_modules/typescript/lib/lib.es2021.intl.d.ts
    ./frontend/node_modules/typescript/lib/lib.es2017.date.d.ts
    ./frontend/node_modules/typescript/lib/lib.es2019.string.d.ts
    ./frontend/node_modules/typescript/lib/lib.es2015.reflect.d.ts
    ./frontend/node_modules/typescript/lib/tsserverlibrary.js
    ./frontend/node_modules/typescript/lib/lib.esnext.collection.d.ts
    ./frontend/node_modules/typescript/lib/lib.es2018.full.d.ts
    ./frontend/node_modules/typescript/lib/typesMap.json
    ./frontend/node_modules/typescript/lib/lib.dom.iterable.d.ts
    ./frontend/node_modules/typescript/lib/lib.es2019.object.d.ts
    ./frontend/node_modules/typescript/package.json
    ./frontend/node_modules/typescript/README.md
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/node_modules/ignore/LICENSE-MIT
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/node_modules/ignore/index.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/node_modules/ignore/package.json
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/node_modules/ignore/README.md
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/node_modules/ignore/legacy.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/node_modules/ignore/index.js
    ./frontend/node_modules/typescript/bin/tsc
    ./frontend/node_modules/typescript/bin/tsserver
    ./frontend/node_modules/@eslint/eslintrc/node_modules/globals/index.d.ts
    ./frontend/node_modules/@eslint/eslintrc/node_modules/globals/package.json
    ./frontend/node_modules/@eslint/eslintrc/node_modules/globals/readme.md
    ./frontend/node_modules/@eslint/eslintrc/node_modules/globals/index.js
    ./frontend/node_modules/@eslint/eslintrc/node_modules/globals/license
    ./frontend/node_modules/@eslint/eslintrc/node_modules/globals/globals.json
    ./frontend/node_modules/@humanwhocodes/module-importer/dist/module-importer.d.ts
    ./frontend/node_modules/@humanwhocodes/module-importer/dist/module-importer.cjs
    ./frontend/node_modules/@humanwhocodes/module-importer/dist/module-importer.js
    ./frontend/node_modules/@humanwhocodes/module-importer/dist/module-importer.d.cts
    ./frontend/node_modules/typescript/lib/pt-br/diagnosticMessages.generated.json
    ./frontend/node_modules/@humanwhocodes/module-importer/CHANGELOG.md
    ./frontend/node_modules/@humanwhocodes/module-importer/LICENSE
    ./frontend/node_modules/typescript/lib/lib.es2021.promise.d.ts
    ./frontend/node_modules/typescript/lib/lib.es2020.sharedmemory.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/index.d.ts
    ./frontend/node_modules/xml-name-validator/LICENSE.txt
    ./frontend/node_modules/is-glob/package.json
    ./frontend/node_modules/is-glob/README.md
    ./frontend/node_modules/is-glob/index.js
    ./frontend/node_modules/is-glob/LICENSE
    ./frontend/node_modules/@eslint-community/regexpp/index.d.ts
    ./frontend/node_modules/zod/v4/core/doc.js
    ./frontend/node_modules/nanoid/bin/nanoid.cjs
    ./frontend/node_modules/@eslint-community/regexpp/index.js.map
    ./frontend/node_modules/@eslint-community/regexpp/index.mjs
    ./frontend/node_modules/@eslint-community/regexpp/package.json
    ./frontend/node_modules/@eslint-community/regexpp/README.md
    ./frontend/node_modules/@eslint-community/regexpp/index.mjs.map
    ./frontend/node_modules/@eslint-community/regexpp/index.js
    ./frontend/node_modules/@eslint-community/regexpp/LICENSE
    ./frontend/node_modules/zod/v4/core/util.d.cts
    ./frontend/node_modules/zod/v4/core/json-schema.js
    ./frontend/node_modules/zod/v4/core/regexes.js
    ./frontend/node_modules/zod/v4/core/json-schema-generator.d.ts
    ./frontend/node_modules/zod/v4/core/registries.d.ts
    ./frontend/node_modules/zod/v4/core/json-schema-generator.cjs
    ./frontend/node_modules/zod/v4/core/core.d.cts
    ./frontend/node_modules/zod/v4/core/standard-schema.js
    ./frontend/node_modules/zod/v4/core/index.d.ts
    ./frontend/node_modules/zod/v4/core/api.js
    ./frontend/node_modules/zod/v4/core/util.d.ts
    ./frontend/node_modules/zod/v4/core/regexes.cjs
    ./frontend/node_modules/zod/v4/core/json-schema-processors.d.cts
    ./frontend/node_modules/zod/v4/core/schemas.js
    ./frontend/node_modules/zod/v4/core/doc.cjs
    ./frontend/node_modules/zod/v4/core/schemas.d.ts
    ./frontend/node_modules/zod/v4/core/index.cjs
    ./frontend/node_modules/zod/v4/core/registries.js
    ./frontend/node_modules/zod/v4/core/json-schema.cjs
    ./frontend/node_modules/zod/v4/core/errors.d.cts
    ./frontend/node_modules/zod/v4/core/json-schema-generator.js
    ./frontend/node_modules/zod/v4/core/api.d.cts
    ./frontend/node_modules/zod/v4/core/doc.d.ts
    ./frontend/node_modules/zod/v4/core/errors.js
    ./frontend/node_modules/zod/v4/core/package.json
    ./frontend/node_modules/zod/v4/core/versions.js
    ./frontend/node_modules/zod/v4/core/registries.cjs
    ./frontend/node_modules/zod/v4/core/regexes.d.cts
    ./frontend/node_modules/zod/v4/core/parse.js
    ./frontend/node_modules/zod/v4/core/core.d.ts
    ./frontend/node_modules/zod/v4/core/errors.cjs
    ./frontend/node_modules/zod/v4/core/checks.d.ts
    ./frontend/node_modules/zod/v4/core/standard-schema.cjs
    ./frontend/node_modules/zod/v4/core/parse.d.cts
    ./frontend/node_modules/zod/v4/core/versions.cjs
    ./frontend/node_modules/zod/v4/core/registries.d.cts
    ./frontend/node_modules/zod/v4/core/parse.cjs
    ./frontend/node_modules/zod/v4/core/core.cjs
    ./frontend/node_modules/zod/v4/core/index.js
    ./frontend/node_modules/zod/v4/core/versions.d.ts
    ./frontend/node_modules/zod/v4/core/json-schema.d.ts
    ./frontend/node_modules/zod/v4/core/regexes.d.ts
    ./frontend/node_modules/zod/v4/core/json-schema-generator.d.cts
    ./frontend/node_modules/zod/v4/core/versions.d.cts
    ./frontend/node_modules/zod/v4/core/standard-schema.d.cts
    ./frontend/node_modules/zod/v4/core/index.d.cts
    ./frontend/node_modules/zod/v4/core/api.cjs
    ./frontend/node_modules/zod/v4/core/to-json-schema.d.ts
    ./frontend/node_modules/zod/v4/core/doc.d.cts
    ./frontend/node_modules/zod/v4/core/util.cjs
    ./frontend/node_modules/zod/v4/core/json-schema-processors.d.ts
    ./frontend/node_modules/zod/v4/core/to-json-schema.d.cts
    ./frontend/node_modules/zod/v4/core/errors.d.ts
    ./frontend/node_modules/zod/v4/core/core.js
    ./frontend/node_modules/zod/v4/core/to-json-schema.js
    ./frontend/node_modules/zod/v4/core/parse.d.ts
    ./frontend/node_modules/zod/v4/core/api.d.ts
    ./frontend/node_modules/zod/v4/core/schemas.cjs
    ./frontend/node_modules/zod/v4/core/util.js
    ./frontend/node_modules/zod/v4/core/json-schema-processors.cjs
    ./frontend/node_modules/zod/v4/core/checks.cjs
    ./frontend/node_modules/zod/v4/core/json-schema-processors.js
    ./frontend/node_modules/zod/v4/core/standard-schema.d.ts
    ./frontend/node_modules/zod/v4/core/json-schema.d.cts
    ./frontend/node_modules/zod/v4/core/checks.js
    ./frontend/node_modules/zod/v4/core/checks.d.cts
    ./frontend/node_modules/zod/v4/core/schemas.d.cts
    ./frontend/node_modules/zod/v4/core/to-json-schema.cjs
    ./frontend/node_modules/nanoid/LICENSE
    ./frontend/node_modules/@humanwhocodes/retry/package.json
    ./frontend/node_modules/@humanwhocodes/retry/README.md
    ./frontend/node_modules/typescript/lib/zh-tw/diagnosticMessages.generated.json
    ./frontend/node_modules/typescript/lib/lib.es2020.bigint.d.ts
    ./frontend/node_modules/typescript/lib/lib.webworker.iterable.d.ts
    ./frontend/node_modules/typescript/lib/lib.es2020.symbol.wellknown.d.ts
    ./frontend/node_modules/typescript/lib/lib.es2024.sharedmemory.d.ts
    ./frontend/node_modules/typescript/lib/lib.es2023.array.d.ts
    ./frontend/node_modules/typescript/lib/lib.dom.d.ts
    ./frontend/node_modules/typescript/lib/lib.es2020.promise.d.ts
    ./frontend/node_modules/typescript/lib/lib.es2017.full.d.ts
    ./frontend/node_modules/typescript/lib/_typingsInstaller.js
    ./frontend/node_modules/typescript/lib/lib.es2022.full.d.ts
    ./frontend/node_modules/typescript/lib/lib.webworker.asynciterable.d.ts
    ./frontend/node_modules/typescript/lib/lib.es2020.date.d.ts
    ./frontend/node_modules/typescript/lib/lib.es2024.regexp.d.ts
    ./frontend/node_modules/typescript/lib/lib.es2016.intl.d.ts
    ./frontend/node_modules/typescript/lib/tsc.js
    ./frontend/node_modules/typescript/lib/lib.es2024.d.ts
    ./frontend/node_modules/typescript/lib/lib.es2019.array.d.ts
    ./frontend/node_modules/typescript/lib/lib.esnext.float16.d.ts
    ./frontend/node_modules/typescript/lib/lib.es2023.intl.d.ts
    ./frontend/node_modules/xml-name-validator/lib/xml-name-validator.js
    ./frontend/node_modules/xml-name-validator/package.json
    ./frontend/node_modules/xml-name-validator/README.md
    ./frontend/node_modules/@eslint/eslintrc/dist/eslintrc-universal.cjs
    ./frontend/node_modules/@eslint/eslintrc/dist/eslintrc-universal.cjs.map
    ./frontend/node_modules/@eslint/eslintrc/dist/eslintrc.d.cts
    ./frontend/node_modules/@eslint/eslintrc/dist/eslintrc.cjs.map
    ./frontend/node_modules/@eslint/eslintrc/dist/eslintrc.cjs
    ./frontend/node_modules/@eslint/eslintrc/LICENSE
    ./frontend/node_modules/magic-string/package.json
    ./frontend/node_modules/magic-string/README.md
    ./frontend/node_modules/@humanwhocodes/retry/dist/retrier.min.js
    ./frontend/node_modules/@humanwhocodes/retry/dist/retrier.d.ts
    ./frontend/node_modules/@humanwhocodes/retry/dist/retrier.d.cts
    ./frontend/node_modules/@humanwhocodes/retry/dist/retrier.js
    ./frontend/node_modules/@humanwhocodes/retry/dist/retrier.cjs
    ./frontend/node_modules/@humanwhocodes/retry/dist/retrier.mjs
    ./frontend/node_modules/@humanwhocodes/retry/LICENSE
    ./frontend/node_modules/picomatch/lib/scan.js
    ./frontend/node_modules/picomatch/lib/utils.js
    ./frontend/node_modules/picomatch/lib/picomatch.js
    ./frontend/node_modules/picomatch/lib/parse.js
    ./frontend/node_modules/picomatch/lib/constants.js
    ./frontend/node_modules/picomatch/package.json
    ./frontend/node_modules/picomatch/posix.js
    ./frontend/node_modules/picomatch/README.md
    ./frontend/node_modules/picomatch/index.js
    ./frontend/node_modules/picomatch/LICENSE
    ./frontend/node_modules/@eslint-community/eslint-utils/index.d.ts
    ./frontend/node_modules/@eslint-community/eslint-utils/index.js.map
    ./frontend/node_modules/@eslint-community/eslint-utils/index.mjs
    ./frontend/node_modules/@eslint-community/eslint-utils/package.json
    ./frontend/node_modules/@eslint-community/eslint-utils/README.md
    ./frontend/node_modules/@eslint-community/eslint-utils/index.mjs.map
    ./frontend/node_modules/@eslint-community/eslint-utils/index.js
    ./frontend/node_modules/natural-compare/package.json
    ./frontend/node_modules/natural-compare/README.md
    ./frontend/node_modules/natural-compare/index.js
    ./frontend/node_modules/typescript/lib/zh-cn/diagnosticMessages.generated.json
    ./frontend/node_modules/typescript/lib/lib.esnext.d.ts
    ./frontend/node_modules/typescript/lib/lib.es5.d.ts
    ./frontend/node_modules/typescript/lib/lib.esnext.intl.d.ts
    ./frontend/node_modules/typescript/lib/lib.es2016.array.include.d.ts
    ./frontend/node_modules/typescript/lib/lib.es2022.error.d.ts
    ./frontend/node_modules/typescript/lib/lib.es2023.collection.d.ts
    ./frontend/node_modules/typescript/lib/lib.esnext.sharedmemory.d.ts
    ./frontend/node_modules/typescript/lib/lib.es6.d.ts
    ./frontend/node_modules/typescript/lib/tsserver.js
    ./frontend/node_modules/typescript/lib/lib.es2018.asynciterable.d.ts
    ./frontend/node_modules/typescript/lib/lib.es2021.string.d.ts
    ./frontend/node_modules/typescript/lib/lib.decorators.d.ts
    ./frontend/node_modules/typescript/lib/lib.es2018.regexp.d.ts
    ./frontend/node_modules/parent-module/package.json
    ./frontend/node_modules/parent-module/readme.md
    ./frontend/node_modules/parent-module/index.js
    ./frontend/node_modules/parent-module/license
    ./frontend/node_modules/aria-query/lib/rolesMap.js
    ./frontend/node_modules/aria-query/lib/elementRoleMap.js
    ./frontend/node_modules/aria-query/lib/roleElementMap.js
    ./frontend/node_modules/aria-query/lib/domMap.js
    ./frontend/node_modules/aria-query/lib/index.js
    ./frontend/node_modules/aria-query/lib/ariaPropsMap.js
    ./frontend/node_modules/@eslint/plugin-kit/package.json
    ./frontend/node_modules/@eslint/plugin-kit/README.md
    ./frontend/node_modules/magic-string/dist/magic-string.es.mjs.map
    ./frontend/node_modules/magic-string/dist/magic-string.es.d.mts
    ./frontend/node_modules/magic-string/dist/magic-string.cjs.js.map
    ./frontend/node_modules/magic-string/dist/magic-string.cjs.d.ts
    ./frontend/node_modules/magic-string/dist/magic-string.umd.js
    ./frontend/node_modules/magic-string/dist/magic-string.umd.js.map
    ./frontend/node_modules/magic-string/dist/magic-string.cjs.js
    ./frontend/node_modules/magic-string/dist/magic-string.es.mjs
    ./frontend/node_modules/magic-string/LICENSE
    ./frontend/node_modules/typescript/lib/lib.es2024.collection.d.ts
    ./frontend/node_modules/typescript/lib/lib.es2020.intl.d.ts
    ./frontend/node_modules/typescript/lib/lib.es2019.full.d.ts
    ./frontend/node_modules/typescript/lib/_tsc.js
    ./frontend/node_modules/typescript/lib/lib.es2024.arraybuffer.d.ts
    ./frontend/node_modules/typescript/lib/lib.esnext.decorators.d.ts
    ./frontend/node_modules/typescript/lib/lib.es2022.array.d.ts
    ./frontend/node_modules/typescript/lib/lib.scripthost.d.ts
    ./frontend/node_modules/typescript/lib/lib.es2017.typedarrays.d.ts
    ./frontend/node_modules/typescript/lib/lib.es2018.promise.d.ts
    ./frontend/node_modules/typescript/lib/lib.es2017.d.ts
    ./frontend/node_modules/typescript/lib/lib.es2020.number.d.ts
    ./frontend/node_modules/typescript/lib/lib.esnext.disposable.d.ts
    ./frontend/node_modules/typescript/lib/lib.es2024.object.d.ts
    ./frontend/node_modules/typescript/lib/lib.es2015.symbol.wellknown.d.ts
    ./frontend/node_modules/typescript/lib/lib.es2018.intl.d.ts
    ./frontend/node_modules/typescript/lib/_tsserver.js
    ./frontend/node_modules/typescript/lib/lib.es2015.promise.d.ts
    ./frontend/node_modules/typescript/lib/lib.decorators.legacy.d.ts
    ./frontend/node_modules/zod/v4/locales/hy.cjs
    ./frontend/node_modules/json-schema-traverse/.travis.yml
    ./frontend/node_modules/zod/v4/locales/tr.js
    ./frontend/node_modules/zod/v4/locales/fr.cjs
    ./frontend/node_modules/zod/v4/locales/ota.cjs
    ./frontend/node_modules/zod/v4/locales/bg.d.cts
    ./frontend/node_modules/zod/v4/locales/it.d.cts
    ./frontend/node_modules/zod/v4/locales/ps.js
    ./frontend/node_modules/zod/v4/locales/ur.js
    ./frontend/node_modules/zod/v4/locales/eo.js
    ./frontend/node_modules/zod/v4/locales/eo.d.cts
    ./frontend/node_modules/zod/v4/locales/ka.cjs
    ./frontend/node_modules/zod/v4/locales/es.js
    ./frontend/node_modules/zod/v4/locales/it.js
    ./frontend/node_modules/zod/v4/locales/kh.js
    ./frontend/node_modules/zod/v4/locales/es.d.ts
    ./frontend/node_modules/zod/v4/locales/ta.d.cts
    ./frontend/node_modules/zod/v4/locales/be.d.cts
    ./frontend/node_modules/zod/v4/locales/ms.d.cts
    ./frontend/node_modules/zod/v4/locales/ar.d.ts
    ./frontend/node_modules/zod/v4/locales/th.d.ts
    ./frontend/node_modules/zod/v4/locales/sv.d.ts
    ./frontend/node_modules/zod/v4/locales/fr-CA.d.cts
    ./frontend/node_modules/zod/v4/locales/ru.cjs
    ./frontend/node_modules/zod/v4/locales/ar.js
    ./frontend/node_modules/zod/v4/locales/kh.d.ts
    ./frontend/node_modules/zod/v4/locales/eo.cjs
    ./frontend/node_modules/zod/v4/locales/km.d.cts
    ./frontend/node_modules/zod/v4/locales/no.d.ts
    ./frontend/node_modules/zod/v4/locales/lt.js
    ./frontend/node_modules/zod/v4/locales/da.d.ts
    ./frontend/node_modules/zod/v4/locales/cs.d.cts
    ./frontend/node_modules/zod/v4/locales/index.d.ts
    ./frontend/node_modules/zod/v4/locales/id.d.ts
    ./frontend/node_modules/zod/v4/locales/sv.d.cts
    ./frontend/node_modules/zod/v4/locales/hu.js
    ./frontend/node_modules/zod/v4/locales/uz.d.ts
    ./frontend/node_modules/zod/v4/locales/en.cjs
    ./frontend/node_modules/zod/v4/locales/ja.cjs
    ./frontend/node_modules/zod/v4/locales/fr-CA.js
    ./frontend/node_modules/zod/v4/locales/nl.js
    ./frontend/node_modules/zod/v4/locales/fr.js
    ./frontend/node_modules/zod/v4/locales/km.js
    ./frontend/node_modules/zod/v4/locales/cs.js
    ./frontend/node_modules/zod/v4/locales/sv.cjs
    ./frontend/node_modules/zod/v4/locales/uk.js
    ./frontend/node_modules/zod/v4/locales/cs.d.ts
    ./frontend/node_modules/zod/v4/locales/vi.d.ts
    ./frontend/node_modules/zod/v4/locales/hy.d.cts
    ./frontend/node_modules/zod/v4/locales/fa.d.ts
    ./frontend/node_modules/zod/v4/locales/sv.js
    ./frontend/node_modules/zod/v4/locales/pl.cjs
    ./frontend/node_modules/zod/v4/locales/fa.cjs
    ./frontend/node_modules/zod/v4/locales/en.js
    ./frontend/node_modules/zod/v4/locales/ko.d.cts
    ./frontend/node_modules/zod/v4/locales/zh-TW.d.cts
    ./frontend/node_modules/zod/v4/locales/fa.d.cts
    ./frontend/node_modules/zod/v4/locales/he.d.ts
    ./frontend/node_modules/zod/v4/locales/de.js
    ./frontend/node_modules/zod/v4/locales/ja.d.cts
    ./frontend/node_modules/zod/v4/locales/zh-TW.d.ts
    ./frontend/node_modules/zod/v4/locales/ar.d.cts
    ./frontend/node_modules/zod/v4/locales/fa.js
    ./frontend/node_modules/zod/v4/locales/he.d.cts
    ./frontend/node_modules/zod/v4/locales/ur.d.cts
    ./frontend/node_modules/zod/v4/locales/de.d.cts
    ./frontend/node_modules/zod/v4/locales/nl.cjs
    ./frontend/node_modules/zod/v4/locales/kh.d.cts
    ./frontend/node_modules/zod/v4/locales/ko.d.ts
    ./frontend/node_modules/zod/v4/locales/bg.d.ts
    ./frontend/node_modules/zod/v4/locales/uk.d.cts
    ./frontend/node_modules/zod/v4/locales/index.cjs
    ./frontend/node_modules/zod/v4/locales/zh-CN.cjs
    ./frontend/node_modules/zod/v4/locales/ca.d.ts
    ./frontend/node_modules/zod/v4/locales/ota.d.ts
    ./frontend/node_modules/zod/v4/locales/da.js
    ./frontend/node_modules/zod/v4/locales/ota.js
    ./frontend/node_modules/zod/v4/locales/en.d.cts
    ./frontend/node_modules/zod/v4/locales/ur.cjs
    ./frontend/node_modules/zod/v4/locales/vi.cjs
    ./frontend/node_modules/zod/v4/locales/ta.cjs
    ./frontend/node_modules/zod/v4/locales/zh-TW.js
    ./frontend/node_modules/zod/v4/locales/no.cjs
    ./frontend/node_modules/zod/v4/locales/mk.d.cts
    ./frontend/node_modules/zod/v4/locales/lt.cjs
    ./frontend/node_modules/zod/v4/locales/zh-CN.js
    ./frontend/node_modules/zod/v4/locales/tr.cjs
    ./frontend/node_modules/json-schema-traverse/package.json
    ./frontend/node_modules/zod/v4/locales/ua.cjs
    ./frontend/node_modules/json-schema-traverse/README.md
    ./frontend/node_modules/zod/v4/locales/package.json
    ./frontend/node_modules/zod/v4/locales/be.js
    ./frontend/node_modules/json-schema-traverse/index.js
    ./frontend/node_modules/zod/v4/locales/fr.d.ts
    ./frontend/node_modules/zod/v4/locales/ar.cjs
    ./frontend/node_modules/zod/v4/locales/yo.d.cts
    ./frontend/node_modules/zod/v4/locales/ms.cjs
    ./frontend/node_modules/zod/v4/locales/fr-CA.d.ts
    ./frontend/node_modules/zod/v4/locales/da.d.cts
    ./frontend/node_modules/zod/v4/locales/ua.js
    ./frontend/node_modules/zod/v4/locales/ta.js
    ./frontend/node_modules/zod/v4/locales/ca.js
    ./frontend/node_modules/zod/v4/locales/zh-TW.cjs
    ./frontend/node_modules/zod/v4/locales/sl.d.cts
    ./frontend/node_modules/zod/v4/locales/is.d.cts
    ./frontend/node_modules/zod/v4/locales/es.d.cts
    ./frontend/node_modules/zod/v4/locales/ota.d.cts
    ./frontend/node_modules/zod/v4/locales/it.d.ts
    ./frontend/node_modules/zod/v4/locales/az.d.cts
    ./frontend/node_modules/zod/v4/locales/km.d.ts
    ./frontend/node_modules/zod/v4/locales/bg.cjs
    ./frontend/node_modules/zod/v4/locales/th.d.cts
    ./frontend/node_modules/zod/v4/locales/nl.d.cts
    ./frontend/node_modules/zod/v4/locales/fi.d.cts
    ./frontend/node_modules/zod/v4/locales/id.d.cts
    ./frontend/node_modules/zod/v4/locales/fr.d.cts
    ./frontend/node_modules/zod/v4/locales/ua.d.cts
    ./frontend/node_modules/zod/v4/locales/az.js
    ./frontend/node_modules/zod/v4/locales/id.js
    ./frontend/node_modules/zod/v4/locales/uz.d.cts
    ./frontend/node_modules/zod/v4/locales/mk.cjs
    ./frontend/node_modules/zod/v4/locales/ka.d.ts
    ./frontend/node_modules/zod/v4/locales/en.d.ts
    ./frontend/node_modules/zod/v4/locales/uz.cjs
    ./frontend/node_modules/zod/v4/locales/index.js
    ./frontend/node_modules/zod/v4/locales/az.d.ts
    ./frontend/node_modules/zod/v4/locales/uz.js
    ./frontend/node_modules/zod/v4/locales/yo.cjs
    ./frontend/node_modules/zod/v4/locales/pt.d.cts
    ./frontend/node_modules/zod/v4/locales/th.cjs
    ./frontend/node_modules/zod/v4/locales/pt.d.ts
    ./frontend/node_modules/zod/v4/locales/ca.cjs
    ./frontend/node_modules/zod/v4/locales/be.cjs
    ./frontend/node_modules/zod/v4/locales/be.d.ts
    ./frontend/node_modules/zod/v4/locales/fr-CA.cjs
    ./frontend/node_modules/zod/v4/locales/az.cjs
    ./frontend/node_modules/zod/v4/locales/ur.d.ts
    ./frontend/node_modules/zod/v4/locales/zh-CN.d.ts
    ./frontend/node_modules/zod/v4/locales/ta.d.ts
    ./frontend/node_modules/zod/v4/locales/hy.js
    ./frontend/node_modules/zod/v4/locales/cs.cjs
    ./frontend/node_modules/zod/v4/locales/eo.d.ts
    ./frontend/node_modules/zod/v4/locales/index.d.cts
    ./frontend/node_modules/zod/v4/locales/uk.cjs
    ./frontend/node_modules/zod/v4/locales/bg.js
    ./frontend/node_modules/zod/v4/locales/fi.d.ts
    ./frontend/node_modules/zod/v4/locales/he.js
    ./frontend/node_modules/zod/v4/locales/ca.d.cts
    ./frontend/node_modules/zod/v4/locales/ka.js
    ./frontend/node_modules/zod/v4/locales/ja.js
    ./frontend/node_modules/zod/v4/locales/de.d.ts
    ./frontend/node_modules/zod/v4/locales/pl.d.ts
    ./frontend/node_modules/zod/v4/locales/ru.d.ts
    ./frontend/node_modules/zod/v4/locales/uk.d.ts
    ./frontend/node_modules/zod/v4/locales/it.cjs
    ./frontend/node_modules/zod/v4/locales/ja.d.ts
    ./frontend/node_modules/zod/v4/locales/hu.d.cts
    ./frontend/node_modules/zod/v4/locales/no.d.cts
    ./frontend/node_modules/zod/v4/locales/sl.cjs
    ./frontend/node_modules/zod/v4/locales/de.cjs
    ./frontend/node_modules/zod/v4/locales/yo.js
    ./frontend/node_modules/zod/v4/locales/kh.cjs
    ./frontend/node_modules/zod/v4/locales/no.js
    ./frontend/node_modules/zod/v4/locales/mk.js
    ./frontend/node_modules/zod/v4/locales/nl.d.ts
    ./frontend/node_modules/zod/v4/locales/ru.js
    ./frontend/node_modules/zod/v4/locales/pl.d.cts
    ./frontend/node_modules/zod/v4/locales/ms.d.ts
    ./frontend/node_modules/zod/v4/locales/tr.d.cts
    ./frontend/node_modules/zod/v4/locales/th.js
    ./frontend/node_modules/zod/v4/locales/fi.js
    ./frontend/node_modules/zod/v4/locales/pt.cjs
    ./frontend/node_modules/zod/v4/locales/yo.d.ts
    ./frontend/node_modules/argparse/argparse.js
    ./frontend/node_modules/zod/v4/locales/ms.js
    ./frontend/node_modules/zod/v4/locales/ka.d.cts
    ./frontend/node_modules/zod/v4/locales/he.cjs
    ./frontend/node_modules/zod/v4/locales/km.cjs
    ./frontend/node_modules/zod/v4/locales/ko.js
    ./frontend/node_modules/zod/v4/locales/sl.js
    ./frontend/node_modules/zod/v4/locales/is.js
    ./frontend/node_modules/zod/v4/locales/vi.d.cts
    ./frontend/node_modules/zod/v4/locales/hu.d.ts
    ./frontend/node_modules/zod/v4/locales/ps.d.cts
    ./frontend/node_modules/zod/v4/locales/lt.d.ts
    ./frontend/node_modules/zod/v4/locales/id.cjs
    ./frontend/node_modules/zod/v4/locales/is.d.ts
    ./frontend/node_modules/zod/v4/locales/is.cjs
    ./frontend/node_modules/zod/v4/locales/hu.cjs
    ./frontend/node_modules/zod/v4/locales/ps.d.ts
    ./frontend/node_modules/zod/v4/locales/fi.cjs
    ./frontend/node_modules/zod/v4/locales/pl.js
    ./frontend/node_modules/zod/v4/locales/da.cjs
    ./frontend/node_modules/zod/v4/locales/ps.cjs
    ./frontend/node_modules/zod/v4/locales/vi.js
    ./frontend/node_modules/zod/v4/locales/tr.d.ts
    ./frontend/node_modules/zod/v4/locales/mk.d.ts
    ./frontend/node_modules/zod/v4/locales/sl.d.ts
    ./frontend/node_modules/zod/v4/locales/hy.d.ts
    ./frontend/node_modules/zod/v4/locales/zh-CN.d.cts
    ./frontend/node_modules/zod/v4/locales/ru.d.cts
    ./frontend/node_modules/zod/v4/locales/lt.d.cts
    ./frontend/node_modules/zod/v4/locales/pt.js
    ./frontend/node_modules/zod/v4/locales/es.cjs
    ./frontend/node_modules/zod/v4/locales/ko.cjs
    ./frontend/node_modules/zod/v4/locales/ua.d.ts
    ./frontend/node_modules/typescript/lib/ru/diagnosticMessages.generated.json
    ./frontend/node_modules/argparse/CHANGELOG.md
    ./frontend/node_modules/argparse/LICENSE
    ./frontend/node_modules/argparse/README.md
    ./frontend/node_modules/argparse/package.json
    ./frontend/node_modules/typescript/lib/lib.es2015.iterable.d.ts
    ./frontend/node_modules/typescript/lib/lib.es2024.string.d.ts
    ./frontend/node_modules/typescript/lib/lib.es2021.full.d.ts
    ./frontend/node_modules/@eslint-community/eslint-utils/node_modules/eslint-visitor-keys/lib/index.js
    ./frontend/node_modules/@eslint-community/eslint-utils/node_modules/eslint-visitor-keys/lib/visitor-keys.js
    ./frontend/node_modules/@eslint-community/eslint-utils/node_modules/eslint-visitor-keys/package.json
    ./frontend/node_modules/@eslint-community/eslint-utils/node_modules/eslint-visitor-keys/README.md
    ./frontend/node_modules/@typescript-eslint/type-utils/package.json
    ./frontend/node_modules/@typescript-eslint/type-utils/README.md
    ./frontend/node_modules/@eslint/plugin-kit/dist/cjs/types.cts
    ./frontend/node_modules/@eslint/plugin-kit/dist/cjs/index.cjs
    ./frontend/node_modules/@eslint/plugin-kit/dist/cjs/index.d.cts
    ./frontend/node_modules/typescript/lib/ja/diagnosticMessages.generated.json
    ./frontend/node_modules/argparse/lib/sub.js
    ./frontend/node_modules/argparse/lib/textwrap.js
    ./frontend/node_modules/@eslint-community/eslint-utils/node_modules/eslint-visitor-keys/dist/index.d.ts
    ./frontend/node_modules/@eslint-community/eslint-utils/node_modules/eslint-visitor-keys/dist/eslint-visitor-keys.cjs
    ./frontend/node_modules/@eslint-community/eslint-utils/node_modules/eslint-visitor-keys/dist/visitor-keys.d.ts
    ./frontend/node_modules/@eslint-community/eslint-utils/node_modules/eslint-visitor-keys/dist/eslint-visitor-keys.d.cts
    ./frontend/node_modules/@eslint-community/eslint-utils/node_modules/eslint-visitor-keys/LICENSE
    ./frontend/node_modules/@eslint-community/eslint-utils/index.d.mts
    ./frontend/node_modules/@eslint-community/eslint-utils/LICENSE
    ./frontend/node_modules/@typescript-eslint/type-utils/dist/containsAllTypesByName.js
    ./frontend/node_modules/@typescript-eslint/type-utils/dist/typeFlagUtils.js
    ./frontend/node_modules/@typescript-eslint/type-utils/dist/propertyTypes.d.ts
    ./frontend/node_modules/@typescript-eslint/type-utils/dist/index.d.ts
    ./frontend/node_modules/@typescript-eslint/type-utils/dist/getContextualType.js
    ./frontend/node_modules/@typescript-eslint/type-utils/dist/containsAllTypesByName.d.ts
    ./frontend/node_modules/@typescript-eslint/type-utils/dist/builtinSymbolLikes.js
    ./frontend/node_modules/@typescript-eslint/type-utils/dist/getSourceFileOfNode.js
    ./frontend/node_modules/@typescript-eslint/type-utils/dist/isTypeReadonly.d.ts
    ./frontend/node_modules/@typescript-eslint/type-utils/dist/requiresQuoting.d.ts
    ./frontend/node_modules/@typescript-eslint/type-utils/dist/discriminateAnyType.d.ts
    ./frontend/node_modules/@typescript-eslint/type-utils/dist/builtinSymbolLikes.d.ts
    ./frontend/node_modules/@typescript-eslint/type-utils/dist/typeFlagUtils.d.ts
    ./frontend/node_modules/@typescript-eslint/type-utils/dist/isUnsafeAssignment.d.ts
    ./frontend/node_modules/@typescript-eslint/type-utils/dist/isUnsafeAssignment.js
    ./frontend/node_modules/@typescript-eslint/type-utils/dist/TypeOrValueSpecifier.d.ts
    ./frontend/node_modules/@typescript-eslint/type-utils/dist/getTypeName.js
    ./frontend/node_modules/@typescript-eslint/type-utils/dist/isSymbolFromDefaultLibrary.js
    ./frontend/node_modules/@typescript-eslint/type-utils/dist/tsconfig.build.tsbuildinfo
    ./frontend/node_modules/@typescript-eslint/type-utils/dist/discriminateAnyType.js
    ./frontend/node_modules/typescript/lib/cs/diagnosticMessages.generated.json
    ./frontend/node_modules/typescript/lib/lib.es2024.promise.d.ts
    ./frontend/node_modules/eslint-plugin-react-hooks/cjs/eslint-plugin-react-hooks.development.js
    ./frontend/node_modules/eslint-plugin-react-hooks/cjs/eslint-plugin-react-hooks.d.ts
    ./frontend/node_modules/eslint-plugin-react-hooks/cjs/eslint-plugin-react-hooks.production.js
    ./frontend/node_modules/eslint-plugin-react-hooks/index.d.ts
    ./frontend/node_modules/eslint-plugin-react-hooks/package.json
    ./frontend/node_modules/eslint-plugin-react-hooks/README.md
    ./frontend/node_modules/eslint-plugin-react-hooks/index.js
    ./frontend/node_modules/eslint-plugin-react-hooks/LICENSE
    ./frontend/node_modules/json-schema-traverse/LICENSE
    ./frontend/node_modules/json-schema-traverse/.eslintrc.yml
    ./frontend/node_modules/@eslint/plugin-kit/dist/esm/index.d.ts
    ./frontend/node_modules/@eslint/plugin-kit/dist/esm/types.ts
    ./frontend/node_modules/@eslint/plugin-kit/dist/esm/index.js
    ./frontend/node_modules/@eslint/plugin-kit/dist/esm/types.d.ts
    ./frontend/node_modules/@eslint/plugin-kit/LICENSE
    ./frontend/node_modules/@typescript-eslint/utils/package.json
    ./frontend/node_modules/@typescript-eslint/utils/README.md
    ./frontend/node_modules/@typescript-eslint/types/package.json
    ./frontend/node_modules/@typescript-eslint/types/README.md
    ./frontend/node_modules/@eslint/object-schema/package.json
    ./frontend/node_modules/@eslint/object-schema/README.md
    ./frontend/node_modules/@typescript-eslint/type-utils/dist/typeOrValueSpecifiers/typeDeclaredInLib.js
    ./frontend/node_modules/@typescript-eslint/type-utils/dist/typeOrValueSpecifiers/typeDeclaredInPackageDeclarationFile.js
    ./frontend/node_modules/@typescript-eslint/type-utils/dist/typeOrValueSpecifiers/typeDeclaredInFile.d.ts
    ./frontend/node_modules/@typescript-eslint/type-utils/dist/typeOrValueSpecifiers/typeDeclaredInLib.d.ts
    ./frontend/node_modules/@typescript-eslint/type-utils/dist/typeOrValueSpecifiers/typeDeclaredInPackageDeclarationFile.d.ts
    ./frontend/node_modules/@typescript-eslint/type-utils/dist/typeOrValueSpecifiers/typeDeclaredInFile.js
    ./frontend/node_modules/@typescript-eslint/type-utils/dist/typeOrValueSpecifiers/specifierNameMatches.js
    ./frontend/node_modules/@typescript-eslint/type-utils/dist/typeOrValueSpecifiers/specifierNameMatches.d.ts
    ./frontend/node_modules/@typescript-eslint/type-utils/dist/index.js
    ./frontend/node_modules/@typescript-eslint/type-utils/dist/getDeclaration.d.ts
    ./frontend/node_modules/@typescript-eslint/type-utils/dist/getConstrainedTypeAtLocation.d.ts
    ./frontend/node_modules/@typescript-eslint/type-utils/dist/getTypeName.d.ts
    ./frontend/node_modules/@typescript-eslint/type-utils/dist/getConstrainedTypeAtLocation.js
    ./frontend/node_modules/@typescript-eslint/type-utils/dist/isSymbolFromDefaultLibrary.d.ts
    ./frontend/node_modules/@typescript-eslint/type-utils/dist/isTypeBrandedLiteralLike.d.ts
    ./frontend/node_modules/@typescript-eslint/type-utils/dist/isTypeBrandedLiteralLike.js
    ./frontend/node_modules/@typescript-eslint/type-utils/dist/predicates.js
    ./frontend/node_modules/@typescript-eslint/type-utils/dist/predicates.d.ts
    ./frontend/node_modules/@typescript-eslint/type-utils/dist/getDeclaration.js
    ./frontend/node_modules/@typescript-eslint/type-utils/dist/TypeOrValueSpecifier.js
    ./frontend/node_modules/@typescript-eslint/type-utils/dist/isTypeReadonly.js
    ./frontend/node_modules/@typescript-eslint/type-utils/dist/getContextualType.d.ts
    ./frontend/node_modules/@typescript-eslint/type-utils/dist/propertyTypes.js
    ./frontend/node_modules/@typescript-eslint/type-utils/dist/requiresQuoting.js
    ./frontend/node_modules/@typescript-eslint/type-utils/dist/getSourceFileOfNode.d.ts
    ./frontend/node_modules/json-schema-traverse/spec/fixtures/schema.js
    ./frontend/node_modules/@typescript-eslint/type-utils/LICENSE
    ./frontend/node_modules/typescript/lib/it/diagnosticMessages.generated.json
    ./frontend/node_modules/json-schema-traverse/spec/index.spec.js
    ./frontend/node_modules/json-schema-traverse/spec/.eslintrc.yml
    ./frontend/node_modules/webidl-conversions/lib/index.js
    ./frontend/node_modules/webidl-conversions/package.json
    ./frontend/node_modules/webidl-conversions/README.md
    ./frontend/node_modules/webidl-conversions/LICENSE.md
    ./frontend/node_modules/@typescript-eslint/parser/package.json
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-unnecessary-type-arguments.js
    ./frontend/node_modules/@typescript-eslint/parser/README.md
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-base-to-string.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-non-null-asserted-optional-chain.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/related-getter-setter-pairs.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-dupe-class-members.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/require-await.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-confusing-void-expression.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-unnecessary-type-parameters.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-non-null-asserted-optional-chain.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/ban-ts-comment.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/promise-function-async.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/prefer-enum-initializers.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-empty-function.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-require-imports.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-floating-promises.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/require-array-sort-compare.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/prefer-destructuring.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-invalid-void-type.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/array-type.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/explicit-module-boundary-types.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-useless-default-assignment.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-misused-new.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-explicit-any.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-unused-private-class-members.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-useless-empty-export.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/prefer-return-this-type.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/restrict-template-expressions.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-non-null-assertion.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-wrapper-object-types.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/related-getter-setter-pairs.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/sort-type-constituents.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/require-await.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-dynamic-delete.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-loss-of-precision.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/non-nullable-type-assertion-style.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-base-to-string.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-implied-eval.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-explicit-any.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-unnecessary-template-expression.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-unused-private-class-members.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/index.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-redeclare.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-misused-promises.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-type-alias.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-useless-default-assignment.d.ts
    ./frontend/node_modules/aria-query/lib/etc/roles/graphics/graphicsSymbolRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/graphics/graphicsDocumentRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/graphics/graphicsObjectRole.js
    ./frontend/node_modules/@typescript-eslint/project-service/package.json
    ./frontend/node_modules/@typescript-eslint/project-service/README.md
    ./frontend/node_modules/@typescript-eslint/utils/dist/ts-estree.d.ts
    ./frontend/node_modules/@typescript-eslint/utils/dist/json-schema.js
    ./frontend/node_modules/@typescript-eslint/utils/dist/index.d.ts
    ./frontend/node_modules/@typescript-eslint/types/dist/ts-estree.d.ts
    ./frontend/node_modules/@typescript-eslint/types/dist/index.d.ts
    ./frontend/node_modules/@typescript-eslint/types/dist/lib.d.ts
    ./frontend/node_modules/@typescript-eslint/types/dist/tsconfig.build.tsbuildinfo
    ./frontend/node_modules/@typescript-eslint/types/dist/index.js
    ./frontend/node_modules/@typescript-eslint/types/dist/lib.js
    ./frontend/node_modules/@typescript-eslint/types/dist/parser-options.d.ts
    ./frontend/node_modules/@typescript-eslint/types/dist/parser-options.js
    ./frontend/node_modules/@typescript-eslint/types/dist/ts-estree.js
    ./frontend/node_modules/bidi-js/src/data/bidiMirroring.data.js
    ./frontend/node_modules/bidi-js/src/data/bidiCharTypes.data.js
    ./frontend/node_modules/bidi-js/src/data/bidiBrackets.data.js
    ./frontend/node_modules/saxes/saxes.js.map
    ./frontend/node_modules/saxes/package.json
    ./frontend/node_modules/saxes/saxes.d.ts
    ./frontend/node_modules/saxes/README.md
    ./frontend/node_modules/saxes/saxes.js
    ./frontend/node_modules/bidi-js/src/charTypes.js
    ./frontend/node_modules/bidi-js/src/reordering.js
    ./frontend/node_modules/bidi-js/src/index.js
    ./frontend/node_modules/bidi-js/src/embeddingLevels.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/enum-utils/shared.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/enum-utils/shared.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-unsafe-unary-minus.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-shadow.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/prefer-ts-expect-error.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/parameter-properties.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/prefer-regexp-exec.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/typedef.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-unnecessary-type-assertion.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-unnecessary-type-assertion.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-use-before-define.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/member-ordering.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-unused-expressions.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-array-constructor.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/prefer-as-const.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/prefer-readonly-parameter-types.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-restricted-imports.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/explicit-member-accessibility.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-extra-non-null-assertion.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/default-param-last.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/prefer-return-this-type.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/prefer-namespace-keyword.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/prefer-optional-chain.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-unsafe-member-access.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-unused-expressions.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-unnecessary-qualifier.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-misused-new.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/init-declarations.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-unsafe-return.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-invalid-this.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-useless-constructor.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-this-alias.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-empty-function.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-invalid-this.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-unsafe-function-type.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-unsafe-unary-minus.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-namespace.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-unsafe-assignment.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/prefer-literal-enum-member.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-empty-object-type.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/switch-exhaustiveness-check.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-non-null-asserted-nullish-coalescing.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/naming-convention.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/default-param-last.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-unsafe-declaration-merging.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-extraneous-class.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-meaningless-void-operator.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-restricted-types.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-useless-constructor.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/sort-type-constituents.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-extra-non-null-assertion.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-loop-func.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-unnecessary-type-parameters.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/class-literal-property-style.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-array-delete.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-empty-interface.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/consistent-type-definitions.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-unsafe-argument.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/unbound-method.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-duplicate-type-constituents.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-magic-numbers.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/consistent-return.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-import-type-side-effects.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/consistent-indexed-object-style.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/consistent-type-exports.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-unsafe-call.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-unnecessary-type-constraint.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-unnecessary-boolean-literal-compare.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-unsafe-assignment.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/prefer-literal-enum-member.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/dot-notation.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/non-nullable-type-assertion-style.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-useless-empty-export.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/consistent-type-definitions.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/max-params.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/class-literal-property-style.d.ts
    ./frontend/node_modules/@typescript-eslint/project-service/dist/index.d.ts
    ./frontend/node_modules/@typescript-eslint/project-service/dist/createProjectService.js
    ./frontend/node_modules/@typescript-eslint/project-service/dist/getParsedConfigFileFromTSServer.js
    ./frontend/node_modules/@typescript-eslint/project-service/dist/tsconfig.build.tsbuildinfo
    ./frontend/node_modules/@typescript-eslint/project-service/dist/getParsedConfigFileFromTSServer.d.ts
    ./frontend/node_modules/@typescript-eslint/project-service/dist/index.js
    ./frontend/node_modules/@typescript-eslint/project-service/dist/createProjectService.d.ts
    ./frontend/node_modules/@typescript-eslint/project-service/LICENSE
    ./frontend/node_modules/bidi-js/src/util/parseCharacterMap.js
    ./frontend/node_modules/bidi-js/src/brackets.js
    ./frontend/node_modules/bidi-js/src/mirroring.js
    ./frontend/node_modules/bidi-js/LICENSE.txt
    ./frontend/node_modules/bidi-js/package.json
    ./frontend/node_modules/bidi-js/README.md
    ./frontend/node_modules/word-wrap/index.d.ts
    ./frontend/node_modules/word-wrap/package.json
    ./frontend/node_modules/word-wrap/README.md
    ./frontend/node_modules/word-wrap/index.js
    ./frontend/node_modules/word-wrap/LICENSE
    ./frontend/node_modules/@typescript-eslint/parser/dist/parser.js
    ./frontend/node_modules/@typescript-eslint/parser/dist/parser.d.ts
    ./frontend/node_modules/@typescript-eslint/parser/dist/index.d.ts
    ./frontend/node_modules/@typescript-eslint/parser/dist/tsconfig.build.tsbuildinfo
    ./frontend/node_modules/@typescript-eslint/parser/dist/index.js
    ./frontend/node_modules/@typescript-eslint/parser/LICENSE
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-misused-promises.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/return-await.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/consistent-type-assertions.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/strict-void-return.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-confusing-non-null-assertion.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/prefer-reduce-type-parameter.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/ban-tslint-comment.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/class-methods-use-this.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-confusing-non-null-assertion.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-unsafe-return.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/method-signature-style.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-unsafe-enum-comparison.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/prefer-namespace-keyword.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/prefer-includes.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/dot-notation.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/consistent-generic-constructors.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/prefer-nullish-coalescing.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/prefer-as-const.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/explicit-member-accessibility.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-redundant-type-constituents.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/only-throw-error.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/strict-void-return.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-dynamic-delete.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-duplicate-enum-values.js
    ./frontend/node_modules/tr46/lib/regexes.js
    ./frontend/node_modules/tr46/lib/mappingTable.json
    ./frontend/node_modules/tr46/lib/statusMapping.js
    ./frontend/node_modules/tr46/package.json
    ./frontend/node_modules/tr46/README.md
    ./frontend/node_modules/tr46/index.js
    ./frontend/node_modules/tr46/LICENSE.md
    ./frontend/node_modules/aria-query/lib/etc/roles/dpub/docNoterefRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/dpub/docEndnotesRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/dpub/docTipRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/dpub/docFootnoteRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/dpub/docCreditsRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/dpub/docErrataRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/dpub/docChapterRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/dpub/docPrefaceRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/dpub/docAfterwordRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/dpub/docSubtitleRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/dpub/docPullquoteRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/dpub/docEpigraphRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/dpub/docBacklinkRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/dpub/docGlossrefRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/dpub/docTocRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/dpub/docEpilogueRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/dpub/docPartRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/dpub/docConclusionRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/dpub/docDedicationRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/dpub/docIntroductionRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/dpub/docIndexRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/dpub/docCoverRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/dpub/docQnaRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/dpub/docColophonRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/dpub/docAppendixRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/dpub/docNoticeRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/dpub/docBibliorefRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/dpub/docGlossaryRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/dpub/docCreditRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/dpub/docPrologueRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/dpub/docExampleRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/dpub/docBibliographyRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/dpub/docEndnoteRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/dpub/docAbstractRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/dpub/docBiblioentryRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/dpub/docPagebreakRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/dpub/docAcknowledgmentsRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/dpub/docForewordRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/dpub/docPagelistRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/ariaAbstractRoles.js
    ./frontend/node_modules/aria-query/lib/etc/roles/ariaDpubRoles.js
    ./frontend/node_modules/aria-query/lib/etc/roles/ariaLiteralRoles.js
    ./frontend/node_modules/aria-query/lib/etc/roles/ariaGraphicsRoles.js
    ./frontend/node_modules/@typescript-eslint/utils/dist/ts-eslint/SourceCode.d.ts
    ./frontend/node_modules/@typescript-eslint/utils/dist/ts-eslint/AST.js
    ./frontend/node_modules/@typescript-eslint/utils/dist/ts-eslint/AST.d.ts
    ./frontend/node_modules/@typescript-eslint/utils/dist/ts-eslint/Parser.js
    ./frontend/node_modules/@typescript-eslint/utils/dist/ts-eslint/Parser.d.ts
    ./frontend/node_modules/@typescript-eslint/utils/dist/ts-eslint/index.d.ts
    ./frontend/node_modules/@typescript-eslint/types/dist/generated/ast-spec.d.ts
    ./frontend/node_modules/@typescript-eslint/types/dist/generated/ast-spec.js
    ./frontend/node_modules/@typescript-eslint/types/LICENSE
    ./frontend/node_modules/bidi-js/dist/bidi.mjs
    ./frontend/node_modules/bidi-js/dist/bidi.js
    ./frontend/node_modules/bidi-js/dist/bidi.min.mjs
    ./frontend/node_modules/bidi-js/dist/bidi.min.js
    ./frontend/node_modules/@eslint/object-schema/dist/cjs/types.cts
    ./frontend/node_modules/@eslint/object-schema/dist/cjs/index.cjs
    ./frontend/node_modules/@eslint/object-schema/dist/cjs/index.d.cts
    ./frontend/node_modules/@typescript-eslint/tsconfig-utils/package.json
    ./frontend/node_modules/@typescript-eslint/tsconfig-utils/README.md
    ./frontend/node_modules/ajv/.tonic_example.js
    ./frontend/node_modules/@typescript-eslint/utils/dist/ts-eslint/eslint/LegacyESLint.js
    ./frontend/node_modules/@typescript-eslint/utils/dist/ts-eslint/eslint/ESLintShared.d.ts
    ./frontend/node_modules/@typescript-eslint/utils/dist/ts-eslint/eslint/LegacyESLint.d.ts
    ./frontend/node_modules/@typescript-eslint/utils/dist/ts-eslint/eslint/FlatESLint.js
    ./frontend/node_modules/@typescript-eslint/utils/dist/ts-eslint/eslint/ESLintShared.js
    ./frontend/node_modules/@typescript-eslint/utils/dist/ts-eslint/eslint/FlatESLint.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/naming-convention-utils/enums.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/naming-convention-utils/format.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/naming-convention-utils/shared.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/naming-convention-utils/index.d.ts
    ./frontend/node_modules/@typescript-eslint/utils/dist/ts-eslint/Rule.js
    ./frontend/node_modules/@typescript-eslint/utils/dist/ts-eslint/Linter.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/naming-convention-utils/schema.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/naming-convention-utils/validator.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/naming-convention-utils/schema.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/naming-convention-utils/parse-options.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/naming-convention-utils/shared.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/naming-convention-utils/index.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/naming-convention-utils/validator.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/naming-convention-utils/parse-options.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/naming-convention-utils/enums.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/naming-convention-utils/types.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/naming-convention-utils/format.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/naming-convention-utils/types.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/prefer-optional-chain.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/consistent-indexed-object-style.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/unbound-method.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/use-unknown-in-catch-callback-variable.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/consistent-return.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-unsafe-member-access.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-loss-of-precision.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/strict-boolean-expressions.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/prefer-enum-initializers.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-empty-object-type.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-redeclare.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-inferrable-types.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-unsafe-call.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-mixed-enums.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-non-null-asserted-nullish-coalescing.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/prefer-string-starts-ends-with.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/require-array-sort-compare.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-array-delete.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/consistent-type-assertions.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-unused-vars.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/prefer-readonly-parameter-types.d.ts
    ./frontend/node_modules/@typescript-eslint/utils/dist/ts-eslint/Scope.js
    ./frontend/node_modules/@typescript-eslint/utils/dist/ts-eslint/RuleTester.js
    ./frontend/node_modules/@typescript-eslint/utils/dist/ts-eslint/ParserOptions.js
    ./frontend/node_modules/@typescript-eslint/utils/dist/ts-eslint/ParserOptions.d.ts
    ./frontend/node_modules/@typescript-eslint/utils/dist/ts-eslint/Config.js
    ./frontend/node_modules/@typescript-eslint/utils/dist/ts-eslint/RuleTester.d.ts
    ./frontend/node_modules/@typescript-eslint/utils/dist/ts-eslint/index.js
    ./frontend/node_modules/@typescript-eslint/utils/dist/ts-eslint/Processor.d.ts
    ./frontend/node_modules/@typescript-eslint/utils/dist/ts-eslint/Config.d.ts
    ./frontend/node_modules/@typescript-eslint/utils/dist/ts-eslint/Scope.d.ts
    ./frontend/node_modules/@typescript-eslint/utils/dist/ts-eslint/Processor.js
    ./frontend/node_modules/@typescript-eslint/utils/dist/ts-eslint/SourceCode.js
    ./frontend/node_modules/@typescript-eslint/utils/dist/ts-eslint/ESLint.js
    ./frontend/node_modules/@typescript-eslint/utils/dist/ts-eslint/Linter.d.ts
    ./frontend/node_modules/@typescript-eslint/utils/dist/ts-eslint/ESLint.d.ts
    ./frontend/node_modules/@typescript-eslint/utils/dist/ts-eslint/Rule.d.ts
    ./frontend/node_modules/@typescript-eslint/utils/dist/tsconfig.build.tsbuildinfo
    ./frontend/node_modules/ajv/lib/definition_schema.js
    ./frontend/node_modules/ajv/lib/ajv.js
    ./frontend/node_modules/ajv/lib/keyword.js
    ./frontend/node_modules/@typescript-eslint/tsconfig-utils/dist/getParsedConfigFile.js
    ./frontend/node_modules/@typescript-eslint/tsconfig-utils/dist/index.d.ts
    ./frontend/node_modules/@typescript-eslint/tsconfig-utils/dist/compilerOptions.js
    ./frontend/node_modules/@typescript-eslint/tsconfig-utils/dist/tsconfig.build.tsbuildinfo
    ./frontend/node_modules/@typescript-eslint/tsconfig-utils/dist/index.js
    ./frontend/node_modules/@typescript-eslint/tsconfig-utils/dist/getParsedConfigFile.d.ts
    ./frontend/node_modules/@typescript-eslint/tsconfig-utils/dist/compilerOptions.d.ts
    ./frontend/node_modules/@typescript-eslint/tsconfig-utils/LICENSE
    ./frontend/node_modules/@eslint/object-schema/dist/esm/index.d.ts
    ./frontend/node_modules/@eslint/object-schema/dist/esm/types.ts
    ./frontend/node_modules/@eslint/object-schema/dist/esm/index.js
    ./frontend/node_modules/@eslint/object-schema/dist/esm/types.d.ts
    ./frontend/node_modules/keyv/src/index.d.ts
    ./frontend/node_modules/keyv/src/index.js
    ./frontend/node_modules/keyv/package.json
    ./frontend/node_modules/keyv/README.md
    ./frontend/node_modules/@eslint/object-schema/LICENSE
    ./frontend/node_modules/@adobe/css-tools/package.json
    ./frontend/node_modules/@adobe/css-tools/README.md
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/adjacent-overload-signatures.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-meaningless-void-operator.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-unnecessary-type-conversion.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-unsafe-argument.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-import-type-side-effects.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-duplicate-enum-values.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/prefer-nullish-coalescing.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/consistent-type-exports.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/index.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-var-requires.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/init-declarations.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/restrict-plus-operands.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/consistent-generic-constructors.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/return-await.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/prefer-promise-reject-errors.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-empty-interface.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/prefer-for-of.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/unified-signatures.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-namespace.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-unnecessary-condition.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-unnecessary-qualifier.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-restricted-imports.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-unsafe-function-type.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/naming-convention.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/prefer-find.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/prefer-function-type.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-unsafe-type-assertion.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-unsafe-enum-comparison.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-for-in-array.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/explicit-function-return-type.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/only-throw-error.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-magic-numbers.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-deprecated.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-dupe-class-members.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-extraneous-class.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/prefer-readonly.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-unnecessary-parameter-property-assignment.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/explicit-function-return-type.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-require-imports.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/member-ordering.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/class-methods-use-this.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-unused-vars.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-non-null-assertion.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-unnecessary-boolean-literal-compare.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-unnecessary-type-arguments.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/parameter-properties.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/await-thenable.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/restrict-template-expressions.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/prefer-for-of.d.ts
    ./frontend/node_modules/ajv/lib/dotjs/ref.js
    ./frontend/node_modules/ajv/lib/dotjs/propertyNames.js
    ./frontend/node_modules/ajv/lib/dotjs/validate.js
    ./frontend/node_modules/ajv/lib/dotjs/not.js
    ./frontend/node_modules/ajv/lib/dotjs/uniqueItems.js
    ./frontend/node_modules/ajv/lib/dotjs/contains.js
    ./frontend/node_modules/ajv/lib/dotjs/items.js
    ./frontend/node_modules/ajv/lib/dotjs/const.js
    ./frontend/node_modules/ajv/lib/dotjs/dependencies.js
    ./frontend/node_modules/ajv/lib/dotjs/if.js
    ./frontend/node_modules/ajv/lib/dotjs/anyOf.js
    ./frontend/node_modules/ajv/lib/dotjs/enum.js
    ./frontend/node_modules/ajv/lib/dotjs/allOf.js
    ./frontend/node_modules/ajv/lib/dotjs/README.md
    ./frontend/node_modules/ajv/lib/dotjs/comment.js
    ./frontend/node_modules/ajv/lib/dotjs/custom.js
    ./frontend/node_modules/ajv/lib/dotjs/index.js
    ./frontend/node_modules/ajv/lib/dotjs/properties.js
    ./frontend/node_modules/ajv/lib/dotjs/_limit.js
    ./frontend/node_modules/ajv/lib/dotjs/_limitProperties.js
    ./frontend/node_modules/ajv/lib/dotjs/format.js
    ./frontend/node_modules/ajv/lib/dotjs/pattern.js
    ./frontend/node_modules/ajv/lib/dotjs/_limitItems.js
    ./frontend/node_modules/ajv/lib/dotjs/multipleOf.js
    ./frontend/node_modules/ajv/lib/dotjs/_limitLength.js
    ./frontend/node_modules/ajv/lib/dotjs/oneOf.js
    ./frontend/node_modules/ajv/lib/dotjs/required.js
    ./frontend/node_modules/undici/index.d.ts
    ./frontend/node_modules/react-dom/cjs/react-dom-server.node.production.js
    ./frontend/node_modules/react-dom/cjs/react-dom-test-utils.development.js
    ./frontend/node_modules/react-dom/cjs/react-dom-server-legacy.browser.development.js
    ./frontend/node_modules/react-dom/cjs/react-dom-server.browser.production.js
    ./frontend/node_modules/react-dom/cjs/react-dom.react-server.development.js
    ./frontend/node_modules/react-dom/cjs/react-dom.development.js
    ./frontend/node_modules/react-dom/cjs/react-dom-server-legacy.node.production.js
    ./frontend/node_modules/react-dom/cjs/react-dom-server.bun.development.js
    ./frontend/node_modules/react-dom/cjs/react-dom.react-server.production.js
    ./frontend/node_modules/react-dom/cjs/react-dom-server.node.development.js
    ./frontend/node_modules/react-dom/cjs/react-dom-server-legacy.browser.production.js
    ./frontend/node_modules/react-dom/cjs/react-dom-server.edge.development.js
    ./frontend/node_modules/react-dom/cjs/react-dom-client.development.js
    ./frontend/node_modules/react-dom/cjs/react-dom-server-legacy.node.development.js
    ./frontend/node_modules/react-dom/cjs/react-dom-client.production.js
    ./frontend/node_modules/react-dom/cjs/react-dom-profiling.profiling.js
    ./frontend/node_modules/react-dom/cjs/react-dom-server.browser.development.js
    ./frontend/node_modules/react-dom/cjs/react-dom-server.bun.production.js
    ./frontend/node_modules/react-dom/cjs/react-dom-test-utils.production.js
    ./frontend/node_modules/react-dom/cjs/react-dom-server.edge.production.js
    ./frontend/node_modules/react-dom/cjs/react-dom-profiling.development.js
    ./frontend/node_modules/react-dom/cjs/react-dom.production.js
    ./frontend/node_modules/react-dom/server.node.js
    ./frontend/node_modules/react-dom/static.js
    ./frontend/node_modules/react-dom/test-utils.js
    ./frontend/node_modules/react-dom/static.edge.js
    ./frontend/node_modules/react-dom/profiling.react-server.js
    ./frontend/node_modules/react-dom/server.react-server.js
    ./frontend/node_modules/react-dom/static.browser.js
    ./frontend/node_modules/react-dom/profiling.js
    ./frontend/node_modules/react-dom/package.json
    ./frontend/node_modules/react-dom/client.react-server.js
    ./frontend/node_modules/react-dom/README.md
    ./frontend/node_modules/react-dom/index.js
    ./frontend/node_modules/react-dom/server.browser.js
    ./frontend/node_modules/react-dom/static.react-server.js
    ./frontend/node_modules/react-dom/server.js
    ./frontend/node_modules/react-dom/static.node.js
    ./frontend/node_modules/react-dom/LICENSE
    ./frontend/node_modules/react-dom/server.bun.js
    ./frontend/node_modules/react-dom/server.edge.js
    ./frontend/node_modules/react-dom/react-dom.react-server.js
    ./frontend/node_modules/react-dom/client.js
    ./frontend/node_modules/ajv/lib/refs/json-schema-draft-06.json
    ./frontend/node_modules/ajv/lib/refs/json-schema-draft-07.json
    ./frontend/node_modules/ajv/lib/refs/data.json
    ./frontend/node_modules/ajv/lib/refs/json-schema-draft-04.json
    ./frontend/node_modules/ajv/lib/refs/json-schema-secure.json
    ./frontend/node_modules/ajv/lib/data.js
    ./frontend/node_modules/@adobe/css-tools/docs/CHANGELOG.md
    ./frontend/node_modules/@adobe/css-tools/docs/API.md
    ./frontend/node_modules/@adobe/css-tools/docs/AST.md
    ./frontend/node_modules/@adobe/css-tools/docs/EXAMPLES.md
    ./frontend/node_modules/@typescript-eslint/utils/dist/ast-utils/index.d.ts
    ./frontend/node_modules/@typescript-eslint/utils/dist/ast-utils/helpers.d.ts
    ./frontend/node_modules/@typescript-eslint/utils/dist/ast-utils/helpers.js
    ./frontend/node_modules/@typescript-eslint/utils/dist/ast-utils/index.js
    ./frontend/node_modules/@typescript-eslint/utils/dist/ast-utils/misc.js
    ./frontend/node_modules/@typescript-eslint/utils/dist/ast-utils/misc.d.ts
    ./frontend/node_modules/@typescript-eslint/utils/dist/ast-utils/predicates.js
    ./frontend/node_modules/@typescript-eslint/utils/dist/ast-utils/predicates.d.ts
    ./frontend/node_modules/@typescript-eslint/utils/dist/ts-utils/index.d.ts
    ./frontend/node_modules/@typescript-eslint/utils/dist/ts-utils/isArray.js
    ./frontend/node_modules/@typescript-eslint/utils/dist/ts-utils/NoInfer.js
    ./frontend/node_modules/@typescript-eslint/utils/dist/ts-utils/NoInfer.d.ts
    ./frontend/node_modules/@typescript-eslint/utils/dist/ts-utils/isArray.d.ts
    ./frontend/node_modules/@typescript-eslint/utils/dist/ts-utils/index.js
    ./frontend/node_modules/@typescript-eslint/utils/dist/ts-estree.js
    ./frontend/node_modules/@typescript-eslint/utils/LICENSE
    ./frontend/node_modules/ajv/lib/compile/formats.js
    ./frontend/node_modules/ajv/lib/compile/ucs2length.js
    ./frontend/node_modules/ajv/lib/compile/async.js
    ./frontend/node_modules/ajv/lib/compile/error_classes.js
    ./frontend/node_modules/ajv/lib/compile/resolve.js
    ./frontend/node_modules/ajv/lib/compile/equal.js
    ./frontend/node_modules/ajv/lib/compile/index.js
    ./frontend/node_modules/ajv/lib/compile/schema_obj.js
    ./frontend/node_modules/ajv/lib/compile/rules.js
    ./frontend/node_modules/ajv/lib/compile/util.js
    ./frontend/node_modules/ajv/lib/cache.js
    ./frontend/node_modules/ajv/lib/ajv.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/prefer-optional-chain-utils/PreferOptionalChainOptions.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/prefer-optional-chain-utils/analyzeChain.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/prefer-optional-chain-utils/gatherLogicalOperands.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/prefer-optional-chain-utils/analyzeChain.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/prefer-optional-chain-utils/compareNodes.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/prefer-optional-chain-utils/checkNullishAndReport.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/prefer-optional-chain-utils/PreferOptionalChainOptions.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/prefer-optional-chain-utils/compareNodes.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/prefer-optional-chain-utils/checkNullishAndReport.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/prefer-optional-chain-utils/gatherLogicalOperands.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-shadow.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/prefer-includes.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/await-thenable.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/adjacent-overload-signatures.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-var-requires.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-unsafe-declaration-merging.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-unsafe-type-assertion.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/method-signature-style.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-misused-spread.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/prefer-function-type.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-loop-func.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-deprecated.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-inferrable-types.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/prefer-destructuring.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/explicit-module-boundary-types.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/array-type.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/max-params.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-mixed-enums.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-use-before-define.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-unnecessary-template-expression.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/prefer-string-starts-ends-with.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/consistent-type-imports.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/ban-ts-comment.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-implied-eval.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-unnecessary-type-constraint.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-duplicate-type-constituents.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/triple-slash-reference.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-redundant-type-constituents.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/prefer-find.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/triple-slash-reference.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/unified-signatures.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/prefer-reduce-type-parameter.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-for-in-array.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-unnecessary-condition.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-unnecessary-type-conversion.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-array-constructor.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/use-unknown-in-catch-callback-variable.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-restricted-types.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/typedef.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/promise-function-async.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/strict-boolean-expressions.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-type-alias.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-invalid-void-type.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-confusing-void-expression.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/prefer-readonly.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/switch-exhaustiveness-check.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-unnecessary-parameter-property-assignment.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-this-alias.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-floating-promises.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/restrict-plus-operands.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/ban-tslint-comment.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/consistent-type-imports.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/prefer-ts-expect-error.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-wrapper-object-types.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/no-misused-spread.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/prefer-promise-reject-errors.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/rules/prefer-regexp-exec.d.ts
    ./frontend/node_modules/@typescript-eslint/typescript-estree/package.json
    ./frontend/node_modules/@typescript-eslint/typescript-estree/README.md
    ./frontend/node_modules/aria-query/lib/etc/roles/literal/noneRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/literal/sliderRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/literal/feedRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/literal/groupRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/literal/dialogRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/literal/menuitemcheckboxRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/literal/alertRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/literal/complementaryRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/literal/tableRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/literal/gridcellRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/literal/markRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/literal/graphicsSymbolRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/literal/mathRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/literal/emphasisRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/literal/listRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/literal/radioRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/literal/gridRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/literal/rowheaderRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/literal/articleRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/literal/checkboxRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/literal/presentationRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/literal/toolbarRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/literal/progressbarRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/literal/paragraphRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/literal/mainRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/literal/codeRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/literal/switchRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/literal/separatorRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/literal/genericRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/literal/imgRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/literal/captionRole.js
    ./frontend/node_modules/@eslint/js/src/configs/eslint-all.js
    ./frontend/node_modules/@eslint/js/src/configs/eslint-recommended.js
    ./frontend/node_modules/@eslint/js/src/index.js
    ./frontend/node_modules/@eslint/js/package.json
    ./frontend/node_modules/@eslint/js/README.md
    ./frontend/node_modules/@eslint/js/LICENSE
    ./frontend/node_modules/@typescript-eslint/utils/dist/ast-utils/eslint-utils/index.d.ts
    ./frontend/node_modules/ajv/lib/dot/format.jst
    ./frontend/node_modules/ajv/lib/dot/_limitProperties.jst
    ./frontend/node_modules/ajv/lib/dot/_limitLength.jst
    ./frontend/node_modules/@typescript-eslint/utils/dist/ast-utils/eslint-utils/PatternMatcher.js
    ./frontend/node_modules/ajv/lib/dot/contains.jst
    ./frontend/node_modules/@typescript-eslint/utils/dist/ast-utils/eslint-utils/ReferenceTracker.js
    ./frontend/node_modules/ajv/lib/dot/ref.jst
    ./frontend/node_modules/@typescript-eslint/utils/dist/ast-utils/eslint-utils/ReferenceTracker.d.ts
    ./frontend/node_modules/ajv/lib/dot/not.jst
    ./frontend/node_modules/@typescript-eslint/utils/dist/ast-utils/eslint-utils/astUtilities.d.ts
    ./frontend/node_modules/ajv/lib/dot/required.jst
    ./frontend/node_modules/@typescript-eslint/utils/dist/ast-utils/eslint-utils/scopeAnalysis.js
    ./frontend/node_modules/ajv/lib/dot/dependencies.jst
    ./frontend/node_modules/@typescript-eslint/utils/dist/ast-utils/eslint-utils/index.js
    ./frontend/node_modules/ajv/lib/dot/multipleOf.jst
    ./frontend/node_modules/@typescript-eslint/utils/dist/ast-utils/eslint-utils/astUtilities.js
    ./frontend/node_modules/ajv/lib/dot/definitions.def
    ./frontend/node_modules/undici/lib/interceptor/dump.js
    ./frontend/node_modules/@typescript-eslint/utils/dist/ast-utils/eslint-utils/predicates.js
    ./frontend/node_modules/ajv/lib/dot/validate.jst
    ./frontend/node_modules/undici/lib/interceptor/retry.js
    ./frontend/node_modules/@typescript-eslint/utils/dist/ast-utils/eslint-utils/PatternMatcher.d.ts
    ./frontend/node_modules/ajv/lib/dot/missing.def
    ./frontend/node_modules/undici/lib/interceptor/response-error.js
    ./frontend/node_modules/@typescript-eslint/utils/dist/ast-utils/eslint-utils/predicates.d.ts
    ./frontend/node_modules/undici/lib/interceptor/decompress.js
    ./frontend/node_modules/ajv/lib/dot/comment.jst
    ./frontend/node_modules/@typescript-eslint/utils/dist/ast-utils/eslint-utils/scopeAnalysis.d.ts
    ./frontend/node_modules/ajv/lib/dot/anyOf.jst
    ./frontend/node_modules/undici/lib/interceptor/dns.js
    ./frontend/node_modules/ajv/lib/dot/defaults.def
    ./frontend/node_modules/undici/lib/interceptor/cache.js
    ./frontend/node_modules/undici/lib/interceptor/redirect.js
    ./frontend/node_modules/undici/lib/interceptor/deduplicate.js
    ./frontend/node_modules/ajv/lib/dot/propertyNames.jst
    ./frontend/node_modules/ajv/lib/dot/_limit.jst
    ./frontend/node_modules/ajv/lib/dot/if.jst
    ./frontend/node_modules/ajv/lib/dot/pattern.jst
    ./frontend/node_modules/ajv/lib/dot/allOf.jst
    ./frontend/node_modules/ajv/lib/dot/uniqueItems.jst
    ./frontend/node_modules/ajv/lib/dot/errors.def
    ./frontend/node_modules/ajv/lib/dot/oneOf.jst
    ./frontend/node_modules/ajv/lib/dot/enum.jst
    ./frontend/node_modules/ajv/lib/dot/properties.jst
    ./frontend/node_modules/ajv/lib/dot/const.jst
    ./frontend/node_modules/ajv/lib/dot/custom.jst
    ./frontend/node_modules/ajv/lib/dot/items.jst
    ./frontend/node_modules/ajv/lib/dot/_limitItems.jst
    ./frontend/node_modules/ajv/lib/dot/coerce.def
    ./frontend/node_modules/@typescript-eslint/utils/dist/index.js
    ./frontend/node_modules/@typescript-eslint/utils/dist/json-schema.d.ts
    ./frontend/node_modules/aria-query/lib/etc/roles/literal/documentRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/literal/tablistRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/literal/alertdialogRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/literal/applicationRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/literal/radiogroupRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/literal/treeRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/literal/treeitemRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/literal/textboxRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/literal/columnheaderRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/literal/blockquoteRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/literal/directoryRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/literal/marqueeRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/literal/menuitemRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/literal/searchRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/literal/scrollbarRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/literal/bannerRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/literal/rowRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/literal/graphicsDocumentRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/literal/graphicsObjectRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/literal/formRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/literal/listboxRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/literal/cellRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/literal/deletionRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/literal/optionRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/literal/tabpanelRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/literal/listitemRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/literal/timerRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/literal/timeRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/literal/definitionRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/literal/rowgroupRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/literal/regionRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/literal/figureRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/literal/subscriptRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/literal/buttonRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/literal/statusRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/literal/insertionRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/literal/menuRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/literal/noteRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/literal/headingRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/literal/menuitemradioRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/literal/treegridRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/literal/tooltipRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/literal/contentinfoRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/literal/logRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/literal/meterRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/literal/navigationRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/literal/linkRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/literal/spinbuttonRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/literal/comboboxRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/literal/superscriptRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/literal/menubarRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/literal/tabRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/literal/searchboxRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/literal/strongRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/literal/termRole.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/minimatch/package.json
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/minimatch/README.md
    ./frontend/node_modules/undici/lib/api/api-pipeline.js
    ./frontend/node_modules/undici/lib/api/abort-signal.js
    ./frontend/node_modules/undici/lib/api/readable.js
    ./frontend/node_modules/undici/lib/api/api-stream.js
    ./frontend/node_modules/undici/lib/api/index.js
    ./frontend/node_modules/undici/lib/api/api-connect.js
    ./frontend/node_modules/undici/lib/api/api-request.js
    ./frontend/node_modules/undici/lib/api/api-upgrade.js
    ./frontend/node_modules/ajv/scripts/prepare-tests
    ./frontend/node_modules/ajv/scripts/publish-built-version
    ./frontend/node_modules/ajv/scripts/compile-dots.js
    ./frontend/node_modules/ajv/scripts/info
    ./frontend/node_modules/ajv/scripts/bundle.js
    ./frontend/node_modules/ajv/scripts/travis-gh-pages
    ./frontend/node_modules/ajv/scripts/.eslintrc.yml
    ./frontend/node_modules/ajv/package.json
    ./frontend/node_modules/ajv/README.md
    ./frontend/node_modules/json-stable-stringify-without-jsonify/.travis.yml
    ./frontend/node_modules/json-stable-stringify-without-jsonify/package.json
    ./frontend/node_modules/json-stable-stringify-without-jsonify/readme.markdown
    ./frontend/node_modules/json-stable-stringify-without-jsonify/index.js
    ./frontend/node_modules/@eslint/js/types/index.d.ts
    ./frontend/node_modules/@typescript-eslint/utils/dist/eslint-utils/nullThrows.d.ts
    ./frontend/node_modules/@typescript-eslint/utils/dist/eslint-utils/InferTypesFromRule.d.ts
    ./frontend/node_modules/@typescript-eslint/utils/dist/eslint-utils/parserSeemsToBeTSESLint.d.ts
    ./frontend/node_modules/@typescript-eslint/utils/dist/eslint-utils/applyDefault.js
    ./frontend/node_modules/@typescript-eslint/utils/dist/eslint-utils/index.d.ts
    ./frontend/node_modules/@typescript-eslint/utils/dist/eslint-utils/parserSeemsToBeTSESLint.js
    ./frontend/node_modules/@typescript-eslint/utils/dist/eslint-utils/deepMerge.d.ts
    ./frontend/node_modules/@typescript-eslint/utils/dist/eslint-utils/RuleCreator.js
    ./frontend/node_modules/@typescript-eslint/utils/dist/eslint-utils/InferTypesFromRule.js
    ./frontend/node_modules/@typescript-eslint/utils/dist/eslint-utils/getParserServices.d.ts
    ./frontend/node_modules/@typescript-eslint/utils/dist/eslint-utils/index.js
    ./frontend/node_modules/@typescript-eslint/utils/dist/eslint-utils/applyDefault.d.ts
    ./frontend/node_modules/@typescript-eslint/utils/dist/eslint-utils/nullThrows.js
    ./frontend/node_modules/@typescript-eslint/utils/dist/eslint-utils/RuleCreator.d.ts
    ./frontend/node_modules/@typescript-eslint/utils/dist/eslint-utils/deepMerge.js
    ./frontend/node_modules/@typescript-eslint/utils/dist/eslint-utils/getParserServices.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/index.js
    ./frontend/node_modules/@adobe/css-tools/dist/cjs/adobe-css-tools.d.cts
    ./frontend/node_modules/@adobe/css-tools/dist/cjs/adobe-css-tools.cjs
    ./frontend/node_modules/@adobe/css-tools/dist/cjs/adobe-css-tools.cjs.map
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/configs/eslintrc/all.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/configs/eslintrc/recommended.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/configs/eslintrc/strict-type-checked.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/configs/eslintrc/eslint-recommended.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/configs/eslintrc/strict-type-checked-only.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/configs/eslintrc/stylistic-type-checked.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/configs/eslintrc/recommended-type-checked-only.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/configs/eslintrc/base.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/configs/eslintrc/recommended-type-checked-only.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/configs/eslintrc/base.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/configs/eslintrc/recommended-type-checked.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/configs/eslintrc/disable-type-checked.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/configs/eslintrc/strict-type-checked.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/configs/eslintrc/stylistic-type-checked.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/configs/eslintrc/stylistic-type-checked-only.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/configs/eslintrc/eslint-recommended.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/configs/eslintrc/strict.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/configs/eslintrc/recommended-type-checked.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/configs/eslintrc/stylistic-type-checked-only.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/configs/eslintrc/stylistic.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/configs/eslintrc/strict-type-checked-only.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/configs/eslintrc/recommended.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/configs/eslintrc/stylistic.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/configs/eslintrc/all.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/configs/eslintrc/disable-type-checked.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/configs/eslintrc/strict.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/configs/eslint-recommended-raw.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/configs/eslint-recommended-raw.js
    ./frontend/node_modules/@eslint/core/package.json
    ./frontend/node_modules/@eslint/core/README.md
    ./frontend/node_modules/undici/lib/encoding/index.js
    ./frontend/node_modules/undici/lib/global.js
    ./frontend/node_modules/@adobe/css-tools/dist/umd/adobe-css-tools.js.map
    ./frontend/node_modules/@adobe/css-tools/dist/umd/adobe-css-tools.js
    ./frontend/node_modules/@adobe/css-tools/dist/umd/adobe-css-tools.d.ts
    ./frontend/node_modules/json-stable-stringify-without-jsonify/example/value_cmp.js
    ./frontend/node_modules/json-stable-stringify-without-jsonify/example/nested.js
    ./frontend/node_modules/json-stable-stringify-without-jsonify/example/str.js
    ./frontend/node_modules/json-stable-stringify-without-jsonify/example/key_cmp.js
    ./frontend/node_modules/@eslint/core/dist/cjs/types.d.cts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/configs/flat/all.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/configs/flat/recommended.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/configs/flat/strict-type-checked.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/configs/flat/eslint-recommended.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/configs/flat/strict-type-checked-only.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/configs/flat/stylistic-type-checked.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/configs/flat/recommended-type-checked-only.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/configs/flat/base.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/configs/flat/recommended-type-checked-only.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/configs/flat/base.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/configs/flat/recommended-type-checked.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/configs/flat/disable-type-checked.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/configs/flat/strict-type-checked.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/configs/flat/stylistic-type-checked.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/configs/flat/stylistic-type-checked-only.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/configs/flat/eslint-recommended.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/configs/flat/strict.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/configs/flat/recommended-type-checked.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/configs/flat/stylistic-type-checked-only.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/configs/flat/stylistic.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/configs/flat/strict-type-checked-only.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/configs/flat/recommended.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/configs/flat/stylistic.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/configs/flat/all.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/configs/flat/disable-type-checked.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/configs/flat/strict.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/raw-plugin.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/tsconfig.build.tsbuildinfo
    ./frontend/node_modules/aria-query/lib/etc/roles/abstract/inputRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/abstract/sectionheadRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/abstract/widgetRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/abstract/windowRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/abstract/sectionRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/abstract/selectRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/abstract/structureRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/abstract/compositeRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/abstract/landmarkRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/abstract/roletypeRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/abstract/commandRole.js
    ./frontend/node_modules/aria-query/lib/etc/roles/abstract/rangeRole.js
    ./frontend/node_modules/@exodus/bytes/bigint.d.ts
    ./frontend/node_modules/@exodus/bytes/base32.d.ts
    ./frontend/node_modules/@exodus/bytes/base58check.js
    ./frontend/node_modules/@exodus/bytes/wif.d.ts
    ./frontend/node_modules/@exodus/bytes/base58.js
    ./frontend/node_modules/@exodus/bytes/whatwg.d.ts
    ./frontend/node_modules/@exodus/bytes/single-byte.node.js
    ./frontend/node_modules/@exodus/bytes/multi-byte.node.js
    ./frontend/node_modules/@exodus/bytes/multi-byte.js
    ./frontend/node_modules/@exodus/bytes/index.d.ts
    ./frontend/node_modules/@exodus/bytes/hex.js
    ./frontend/node_modules/@exodus/bytes/base58check.node.js
    ./frontend/node_modules/@exodus/bytes/base64.d.ts
    ./frontend/node_modules/@exodus/bytes/encoding-browser.d.ts
    ./frontend/node_modules/@exodus/bytes/utf16.js
    ./frontend/node_modules/@exodus/bytes/utf16.native.js
    ./frontend/node_modules/@exodus/bytes/hex.d.ts
    ./frontend/node_modules/@exodus/bytes/wif.js
    ./frontend/node_modules/@exodus/bytes/hex.node.js
    ./frontend/node_modules/@exodus/bytes/package.json
    ./frontend/node_modules/@exodus/bytes/encoding-browser.browser.js
    ./frontend/node_modules/@exodus/bytes/base58.d.ts
    ./frontend/node_modules/@exodus/bytes/whatwg.js
    ./frontend/node_modules/@exodus/bytes/base32.js
    ./frontend/node_modules/@exodus/bytes/utf8.d.ts
    ./frontend/node_modules/@exodus/bytes/base58check.d.ts
    ./frontend/node_modules/@exodus/bytes/README.md
    ./frontend/node_modules/@exodus/bytes/array.js
    ./frontend/node_modules/@exodus/bytes/base64.js
    ./frontend/node_modules/@exodus/bytes/single-byte.js
    ./frontend/node_modules/@exodus/bytes/encoding.js
    ./frontend/node_modules/@exodus/bytes/multi-byte.d.ts
    ./frontend/node_modules/@exodus/bytes/index.js
    ./frontend/node_modules/@exodus/bytes/utf16.d.ts
    ./frontend/node_modules/@exodus/bytes/encoding-lite.js
    ./frontend/node_modules/@exodus/bytes/array.d.ts
    ./frontend/node_modules/@exodus/bytes/encoding-browser.js
    ./frontend/node_modules/@exodus/bytes/single-byte.d.ts
    ./frontend/node_modules/@exodus/bytes/utf8.node.js
    ./frontend/node_modules/@exodus/bytes/encoding-browser.native.js
    ./frontend/node_modules/@exodus/bytes/bech32.d.ts
    ./frontend/node_modules/@exodus/bytes/bech32.js
    ./frontend/node_modules/@exodus/bytes/bigint.js
    ./frontend/node_modules/@exodus/bytes/utf16.node.js
    ./frontend/node_modules/ajv/dist/ajv.min.js.map
    ./frontend/node_modules/ajv/dist/ajv.bundle.js
    ./frontend/node_modules/ajv/dist/ajv.min.js
    ./frontend/node_modules/ajv/LICENSE
    ./frontend/node_modules/json-stable-stringify-without-jsonify/test/to-json.js
    ./frontend/node_modules/json-stable-stringify-without-jsonify/test/cmp.js
    ./frontend/node_modules/json-stable-stringify-without-jsonify/test/replacer.js
    ./frontend/node_modules/json-stable-stringify-without-jsonify/test/nested.js
    ./frontend/node_modules/json-stable-stringify-without-jsonify/test/space.js
    ./frontend/node_modules/json-stable-stringify-without-jsonify/test/str.js
    ./frontend/node_modules/json-stable-stringify-without-jsonify/LICENSE
    ./frontend/node_modules/json-stable-stringify-without-jsonify/.npmignore
    ./frontend/node_modules/undici/lib/dispatcher/agent.js
    ./frontend/node_modules/undici/lib/dispatcher/proxy-agent.js
    ./frontend/node_modules/undici/lib/dispatcher/retry-agent.js
    ./frontend/node_modules/undici/lib/dispatcher/dispatcher-base.js
    ./frontend/node_modules/undici/lib/dispatcher/fixed-queue.js
    ./frontend/node_modules/undici/lib/dispatcher/env-http-proxy-agent.js
    ./frontend/node_modules/undici/lib/dispatcher/round-robin-pool.js
    ./frontend/node_modules/undici/lib/dispatcher/balanced-pool.js
    ./frontend/node_modules/undici/lib/dispatcher/h2c-client.js
    ./frontend/node_modules/undici/lib/dispatcher/client-h2.js
    ./frontend/node_modules/undici/lib/dispatcher/pool.js
    ./frontend/node_modules/undici/lib/dispatcher/client-h1.js
    ./frontend/node_modules/undici/lib/dispatcher/pool-base.js
    ./frontend/node_modules/undici/lib/dispatcher/dispatcher.js
    ./frontend/node_modules/undici/lib/dispatcher/socks5-proxy-agent.js
    ./frontend/node_modules/undici/lib/dispatcher/client.js
    ./frontend/node_modules/@adobe/css-tools/dist/esm/adobe-css-tools.d.mts
    ./frontend/node_modules/@adobe/css-tools/dist/esm/adobe-css-tools.mjs.map
    ./frontend/node_modules/@adobe/css-tools/dist/esm/adobe-css-tools.mjs
    ./frontend/node_modules/@adobe/css-tools/LICENSE
    ./frontend/node_modules/dom-accessibility-api/.browserslistrc
    ./frontend/node_modules/dom-accessibility-api/package.json
    ./frontend/node_modules/dom-accessibility-api/README.md
    ./frontend/node_modules/@eslint/core/dist/esm/types.d.ts
    ./frontend/node_modules/@eslint/core/LICENSE
    ./frontend/node_modules/jsdom/LICENSE.txt
    ./frontend/node_modules/siginfo/.travis.yml
    ./frontend/node_modules/siginfo/package.json
    ./frontend/node_modules/siginfo/README.md
    ./frontend/node_modules/siginfo/index.js
    ./frontend/node_modules/siginfo/LICENSE
    ./frontend/node_modules/siginfo/test.js
    ./frontend/node_modules/acorn-jsx/index.d.ts
    ./frontend/node_modules/acorn-jsx/package.json
    ./frontend/node_modules/acorn-jsx/README.md
    ./frontend/node_modules/acorn-jsx/index.js
    ./frontend/node_modules/acorn-jsx/xhtml.js
    ./frontend/node_modules/acorn-jsx/LICENSE
    ./frontend/node_modules/aria-query/lib/util/iteratorProxy.js
    ./frontend/node_modules/aria-query/lib/util/iterationDecorator.js
    ./frontend/node_modules/@eslint/config-helpers/package.json
    ./frontend/node_modules/@eslint/config-helpers/README.md
    ./frontend/node_modules/aria-query/package.json
    ./frontend/node_modules/aria-query/README.md
    ./frontend/node_modules/aria-query/CHANGELOG.md
    ./frontend/node_modules/aria-query/LICENSE
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/minimatch/dist/commonjs/index.d.ts.map
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/minimatch/dist/commonjs/ast.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/minimatch/dist/commonjs/assert-valid-pattern.d.ts
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/minimatch/dist/commonjs/ast.d.ts
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/minimatch/dist/commonjs/assert-valid-pattern.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/minimatch/dist/commonjs/brace-expressions.d.ts
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/minimatch/dist/commonjs/index.d.ts
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/minimatch/dist/commonjs/escape.js.map
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/minimatch/dist/commonjs/assert-valid-pattern.js.map
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/minimatch/dist/commonjs/unescape.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/minimatch/dist/commonjs/index.js.map
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/minimatch/dist/commonjs/assert-valid-pattern.d.ts.map
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/minimatch/dist/commonjs/brace-expressions.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/minimatch/dist/commonjs/package.json
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/minimatch/dist/commonjs/unescape.d.ts
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/minimatch/dist/commonjs/index.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/minimatch/dist/commonjs/unescape.d.ts.map
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/minimatch/dist/commonjs/escape.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/minimatch/dist/commonjs/escape.d.ts.map
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/minimatch/dist/commonjs/unescape.js.map
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/minimatch/dist/commonjs/brace-expressions.d.ts.map
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/minimatch/dist/commonjs/escape.d.ts
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/minimatch/dist/commonjs/brace-expressions.js.map
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/minimatch/dist/commonjs/ast.js.map
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/minimatch/dist/commonjs/ast.d.ts.map
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/util/collectUnusedVariables.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/util/astUtils.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/util/isNodeEqual.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/util/walkStatements.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/util/getForStatementHeadLoc.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/util/objectIterators.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/util/isAssignee.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/util/getForStatementHeadLoc.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/util/isHigherPrecedenceThanAwait.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/util/getESLintCoreRule.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/util/getOperatorPrecedence.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/util/truthinessUtils.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/util/truthinessUtils.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/util/getConstraintInfo.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/util/getWrappingFixer.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/util/index.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/util/getParentFunctionNode.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/util/escapeRegExp.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/util/rangeToLoc.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/util/getConstraintInfo.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/util/getFixOrSuggest.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/util/baseTypeUtils.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/util/getThisExpression.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/util/getTextWithParentheses.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/util/walkStatements.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/util/isArrayMethodCallWithPredicate.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/util/isStartOfExpressionStatement.d.ts
    ./frontend/node_modules/ansi-regex/index.d.ts
    ./frontend/node_modules/ansi-regex/package.json
    ./frontend/node_modules/ansi-regex/readme.md
    ./frontend/node_modules/ansi-regex/index.js
    ./frontend/node_modules/ansi-regex/license
    ./frontend/node_modules/dom-accessibility-api/dist/accessible-name-and-description.js.map
    ./frontend/node_modules/dom-accessibility-api/dist/index.d.ts.map
    ./frontend/node_modules/dom-accessibility-api/dist/accessible-name.js
    ./frontend/node_modules/dom-accessibility-api/dist/accessible-name-and-description.js
    ./frontend/node_modules/dom-accessibility-api/dist/accessible-description.js
    ./frontend/node_modules/dom-accessibility-api/dist/accessible-name.js.map
    ./frontend/node_modules/dom-accessibility-api/dist/is-inaccessible.js.map
    ./frontend/node_modules/dom-accessibility-api/dist/index.d.ts
    ./frontend/node_modules/dom-accessibility-api/dist/util.d.ts
    ./frontend/node_modules/dom-accessibility-api/dist/getRole.mjs.map
    ./frontend/node_modules/dom-accessibility-api/dist/accessible-description.d.ts
    ./frontend/node_modules/dom-accessibility-api/dist/is-inaccessible.d.ts
    ./frontend/node_modules/dom-accessibility-api/dist/index.js.map
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/minimatch/dist/esm/index.d.ts.map
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/minimatch/dist/esm/ast.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/minimatch/dist/esm/assert-valid-pattern.d.ts
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/minimatch/dist/esm/ast.d.ts
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/minimatch/dist/esm/assert-valid-pattern.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/minimatch/dist/esm/brace-expressions.d.ts
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/minimatch/dist/esm/index.d.ts
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/minimatch/dist/esm/escape.js.map
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/minimatch/dist/esm/assert-valid-pattern.js.map
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/minimatch/dist/esm/unescape.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/minimatch/dist/esm/index.js.map
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/minimatch/dist/esm/assert-valid-pattern.d.ts.map
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/minimatch/dist/esm/brace-expressions.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/minimatch/dist/esm/package.json
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/minimatch/dist/esm/unescape.d.ts
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/minimatch/dist/esm/index.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/minimatch/dist/esm/unescape.d.ts.map
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/minimatch/dist/esm/escape.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/minimatch/dist/esm/escape.d.ts.map
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/minimatch/dist/esm/unescape.js.map
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/minimatch/dist/esm/brace-expressions.d.ts.map
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/minimatch/dist/esm/escape.d.ts
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/minimatch/dist/esm/brace-expressions.js.map
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/minimatch/dist/esm/ast.js.map
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/minimatch/dist/esm/ast.d.ts.map
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/minimatch/LICENSE.md
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/util/class-scope-analyzer/extractComputedName.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/util/class-scope-analyzer/extractComputedName.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/util/class-scope-analyzer/classScopeAnalyzer.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/util/class-scope-analyzer/classScopeAnalyzer.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/util/class-scope-analyzer/types.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/util/class-scope-analyzer/types.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/util/isArrayMethodCallWithPredicate.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/util/isPromiseAggregatorMethod.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/util/isNodeEqual.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/util/rangeToLoc.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/util/createRule.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/util/getThisExpression.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/util/isTypeImport.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/util/promiseUtils.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/util/assertionFunctionUtils.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/util/getMemberHeadLoc.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/util/hasOverloadSignatures.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/util/isNullLiteral.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/util/getTextWithParentheses.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/util/collectUnusedVariables.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/util/hasOverloadSignatures.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/util/baseTypeUtils.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/util/objectIterators.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/util/getWrappingFixer.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/util/escapeRegExp.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/util/index.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/util/skipChainExpression.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/util/needsPrecedingSemiColon.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/util/getValueOfLiteralType.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/util/promiseUtils.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/util/getParentFunctionNode.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/util/getStringLength.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/util/getFunctionHeadLoc.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/util/assertionFunctionUtils.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/util/isStartOfExpressionStatement.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/util/getStaticStringValue.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/util/isAssignee.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/util/getMemberHeadLoc.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/util/getWrappedCode.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/util/getStringLength.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/util/misc.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/util/scopeUtils.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/util/isUndefinedIdentifier.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/util/getBaseTypesOfClassMember.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/util/types.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/util/misc.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/util/referenceContainsTypeQuery.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/util/needsToBeAwaited.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/util/explicitReturnTypeUtils.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/util/getStaticStringValue.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/util/isPromiseAggregatorMethod.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/util/getBaseTypesOfClassMember.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/util/needsToBeAwaited.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/util/getValueOfLiteralType.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/util/getESLintCoreRule.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/util/isNullLiteral.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/util/types.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/util/referenceContainsTypeQuery.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/util/getOperatorPrecedence.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/util/isUndefinedIdentifier.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/util/getFixOrSuggest.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/util/explicitReturnTypeUtils.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/util/needsPrecedingSemiColon.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/util/astUtils.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/util/getFunctionHeadLoc.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/util/getWrappedCode.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/util/skipChainExpression.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/util/isHigherPrecedenceThanAwait.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/util/scopeUtils.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/util/isTypeImport.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/util/createRule.d.ts
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/dist/raw-plugin.js
    ./frontend/node_modules/@typescript-eslint/eslint-plugin/LICENSE
    ./frontend/node_modules/undici/lib/mock/snapshot-utils.js
    ./frontend/node_modules/undici/lib/mock/mock-errors.js
    ./frontend/node_modules/undici/lib/mock/mock-symbols.js
    ./frontend/node_modules/undici/lib/mock/snapshot-agent.js
    ./frontend/node_modules/undici/lib/mock/mock-client.js
    ./frontend/node_modules/undici/lib/mock/mock-call-history.js
    ./frontend/node_modules/undici/lib/mock/mock-interceptor.js
    ./frontend/node_modules/undici/lib/mock/mock-pool.js
    ./frontend/node_modules/undici/lib/mock/snapshot-recorder.js
    ./frontend/node_modules/undici/lib/mock/pending-interceptors-formatter.js
    ./frontend/node_modules/undici/lib/mock/mock-utils.js
    ./frontend/node_modules/undici/lib/mock/mock-agent.js
    ./frontend/node_modules/@eslint/config-helpers/dist/cjs/types.cts
    ./frontend/node_modules/@eslint/config-helpers/dist/cjs/index.cjs
    ./frontend/node_modules/@eslint/config-helpers/dist/cjs/index.d.cts
    ./frontend/node_modules/dom-accessibility-api/dist/polyfills/iterator.d.mjs.map
    ./frontend/node_modules/dom-accessibility-api/dist/polyfills/array.from.js
    ./frontend/node_modules/dom-accessibility-api/dist/polyfills/iterator.d.js
    ./frontend/node_modules/dom-accessibility-api/dist/polyfills/SetLike.mjs
    ./frontend/node_modules/dom-accessibility-api/dist/polyfills/array.from.mjs
    ./frontend/node_modules/dom-accessibility-api/dist/polyfills/SetLike.js
    ./frontend/node_modules/dom-accessibility-api/dist/polyfills/SetLike.js.map
    ./frontend/node_modules/dom-accessibility-api/dist/polyfills/array.from.d.ts.map
    ./frontend/node_modules/dom-accessibility-api/dist/polyfills/iterator.d.js.map
    ./frontend/node_modules/dom-accessibility-api/dist/polyfills/array.from.mjs.map
    ./frontend/node_modules/dom-accessibility-api/dist/polyfills/SetLike.mjs.map
    ./frontend/node_modules/dom-accessibility-api/dist/polyfills/array.from.d.ts
    ./frontend/node_modules/dom-accessibility-api/dist/polyfills/SetLike.d.ts.map
    ./frontend/node_modules/dom-accessibility-api/dist/polyfills/SetLike.d.ts
    ./frontend/node_modules/dom-accessibility-api/dist/polyfills/iterator.d.mjs
    ./frontend/node_modules/dom-accessibility-api/dist/polyfills/array.from.js.map
    ./frontend/node_modules/dom-accessibility-api/dist/accessible-description.d.ts.map
    ./frontend/node_modules/dom-accessibility-api/dist/getRole.js
    ./frontend/node_modules/dom-accessibility-api/dist/index.mjs
    ./frontend/node_modules/dom-accessibility-api/dist/accessible-name-and-description.d.ts
    ./frontend/node_modules/dom-accessibility-api/dist/getRole.d.ts.map
    ./frontend/node_modules/dom-accessibility-api/dist/util.d.ts.map
    ./frontend/node_modules/dom-accessibility-api/dist/getRole.mjs
    ./frontend/node_modules/dom-accessibility-api/dist/accessible-name.mjs
    ./frontend/node_modules/dom-accessibility-api/dist/accessible-description.mjs.map
    ./frontend/node_modules/dom-accessibility-api/dist/accessible-name-and-description.mjs
    ./frontend/node_modules/dom-accessibility-api/dist/getRole.d.ts
    ./frontend/node_modules/dom-accessibility-api/dist/index.mjs.map
    ./frontend/node_modules/dom-accessibility-api/dist/accessible-name.d.ts
    ./frontend/node_modules/dom-accessibility-api/dist/index.js
    ./frontend/node_modules/dom-accessibility-api/dist/accessible-name-and-description.d.ts.map
    ./frontend/node_modules/dom-accessibility-api/dist/is-inaccessible.js
    ./frontend/node_modules/dom-accessibility-api/dist/is-inaccessible.mjs
    ./frontend/node_modules/dom-accessibility-api/dist/util.mjs
    ./frontend/node_modules/dom-accessibility-api/dist/accessible-name.d.ts.map
    ./frontend/node_modules/dom-accessibility-api/dist/util.js.map
    ./frontend/node_modules/dom-accessibility-api/dist/is-inaccessible.mjs.map
    ./frontend/node_modules/dom-accessibility-api/dist/accessible-description.mjs
    ./frontend/node_modules/dom-accessibility-api/dist/accessible-name-and-description.mjs.map
    ./frontend/node_modules/dom-accessibility-api/dist/is-inaccessible.d.ts.map
    ./frontend/node_modules/dom-accessibility-api/dist/util.js
    ./frontend/node_modules/dom-accessibility-api/dist/accessible-description.js.map
    ./frontend/node_modules/dom-accessibility-api/dist/accessible-name.mjs.map
    ./frontend/node_modules/dom-accessibility-api/dist/util.mjs.map
    ./frontend/node_modules/dom-accessibility-api/dist/getRole.js.map
    ./frontend/node_modules/dom-accessibility-api/LICENSE.md
    ./frontend/node_modules/@typescript-eslint/scope-manager/package.json
    ./frontend/node_modules/@typescript-eslint/scope-manager/README.md
    ./frontend/node_modules/@exodus/bytes/fallback/base58check.js
    ./frontend/node_modules/@exodus/bytes/fallback/multi-byte.js
    ./frontend/node_modules/@exodus/bytes/fallback/platform.js
    ./frontend/node_modules/@exodus/bytes/fallback/single-byte.encodings.js
    ./frontend/node_modules/@exodus/bytes/fallback/hex.js
    ./frontend/node_modules/@exodus/bytes/fallback/utf8.auto.browser.js
    ./frontend/node_modules/@exodus/bytes/fallback/multi-byte.encodings.cjs
    ./frontend/node_modules/@exodus/bytes/fallback/platform.native.js
    ./frontend/node_modules/@exodus/bytes/fallback/utf16.js
    ./frontend/node_modules/@exodus/bytes/fallback/encoding.labels.js
    ./frontend/node_modules/@exodus/bytes/fallback/_utils.js
    ./frontend/node_modules/@exodus/bytes/fallback/base32.js
    ./frontend/node_modules/@exodus/bytes/fallback/base64.js
    ./frontend/node_modules/@exodus/bytes/fallback/single-byte.js
    ./frontend/node_modules/@exodus/bytes/fallback/platform.browser.js
    ./frontend/node_modules/@exodus/bytes/fallback/encoding.js
    ./frontend/node_modules/@exodus/bytes/fallback/utf8.auto.js
    ./frontend/node_modules/@exodus/bytes/fallback/percent.js
    ./frontend/node_modules/@exodus/bytes/fallback/utf8.auto.native.js
    ./frontend/node_modules/@exodus/bytes/fallback/latin1.js
    ./frontend/node_modules/@exodus/bytes/fallback/multi-byte.table.js
    ./frontend/node_modules/@exodus/bytes/fallback/multi-byte.encodings.json
    ./frontend/node_modules/@exodus/bytes/fallback/encoding.util.js
    ./frontend/node_modules/@exodus/bytes/fallback/utf8.js
    ./frontend/node_modules/@exodus/bytes/fallback/encoding.api.js
    ./frontend/node_modules/@exodus/bytes/LICENSE
    ./frontend/node_modules/@exodus/bytes/assert.js
    ./frontend/node_modules/@exodus/bytes/encoding.d.ts
    ./frontend/node_modules/@exodus/bytes/encoding-lite.d.ts
    ./frontend/node_modules/@exodus/bytes/utf16.browser.js
    ./frontend/node_modules/@exodus/bytes/utf8.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/semver/range.bnf
    ./frontend/node_modules/@eslint/config-helpers/dist/esm/index.d.ts
    ./frontend/node_modules/@eslint/config-helpers/dist/esm/types.ts
    ./frontend/node_modules/@eslint/config-helpers/dist/esm/index.js
    ./frontend/node_modules/@eslint/config-helpers/dist/esm/types.d.ts
    ./frontend/node_modules/@eslint/config-helpers/LICENSE
    ./frontend/node_modules/jsdom/lib/api.js
    ./frontend/node_modules/which/package.json
    ./frontend/node_modules/which/which.js
    ./frontend/node_modules/which/README.md
    ./frontend/node_modules/which/CHANGELOG.md
    ./frontend/node_modules/zod-validation-error/v3/index.d.ts
    ./frontend/node_modules/zod-validation-error/v3/index.js.map
    ./frontend/node_modules/zod-validation-error/v3/index.mjs
    ./frontend/node_modules/zod-validation-error/v3/index.mjs.map
    ./frontend/node_modules/zod-validation-error/v3/index.js
    ./frontend/node_modules/zod-validation-error/v3/index.d.mts
    ./frontend/node_modules/zod-validation-error/package.json
    ./frontend/node_modules/tldts-core/src/options.ts
    ./frontend/node_modules/tldts-core/src/is-ip.ts
    ./frontend/node_modules/tldts-core/src/domain-without-suffix.ts
    ./frontend/node_modules/tldts-core/src/is-valid.ts
    ./frontend/node_modules/tldts-core/src/domain.ts
    ./frontend/node_modules/tldts-core/src/extract-hostname.ts
    ./frontend/node_modules/tldts-core/src/subdomain.ts
    ./frontend/node_modules/tldts-core/src/factory.ts
    ./frontend/node_modules/@eslint/config-array/package.json
    ./frontend/node_modules/supports-color/browser.js
    ./frontend/node_modules/@eslint/config-array/README.md
    ./frontend/node_modules/supports-color/package.json
    ./frontend/node_modules/supports-color/readme.md
    ./frontend/node_modules/supports-color/index.js
    ./frontend/node_modules/supports-color/license
    ./frontend/node_modules/which/bin/node-which
    ./frontend/node_modules/jsdom/lib/jsdom/utils.js
    ./frontend/node_modules/@csstools/css-color-parser/package.json
    ./frontend/node_modules/@csstools/css-color-parser/README.md
    ./frontend/node_modules/which/LICENSE
    ./frontend/node_modules/zod-validation-error/v4/index.d.ts
    ./frontend/node_modules/zod-validation-error/v4/index.js.map
    ./frontend/node_modules/zod-validation-error/v4/index.mjs
    ./frontend/node_modules/zod-validation-error/v4/index.mjs.map
    ./frontend/node_modules/zod-validation-error/v4/index.js
    ./frontend/node_modules/zod-validation-error/v4/index.d.mts
    ./frontend/node_modules/zod-validation-error/README.md
    ./frontend/node_modules/zod-validation-error/README.v3.md
    ./frontend/node_modules/zod-validation-error/LICENSE
    ./frontend/node_modules/undici/lib/web/cookies/parse.js
    ./frontend/node_modules/undici/lib/web/cookies/index.js
    ./frontend/node_modules/undici/lib/web/cookies/util.js
    ./frontend/node_modules/undici/lib/web/cookies/constants.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/semver/functions/prerelease.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/semver/functions/major.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/semver/functions/cmp.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/semver/functions/diff.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/semver/functions/lt.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/semver/functions/inc.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/semver/functions/coerce.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/semver/functions/compare.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/semver/functions/minor.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/semver/functions/parse.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/semver/functions/compare-loose.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/semver/functions/satisfies.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/semver/functions/valid.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/semver/functions/clean.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/semver/functions/rcompare.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/semver/functions/patch.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/semver/functions/compare-build.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/semver/functions/lte.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/semver/functions/eq.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/semver/functions/gte.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/semver/functions/neq.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/semver/functions/rsort.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/semver/functions/sort.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/semver/functions/gt.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/semver/package.json
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/semver/README.md
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/semver/index.js
    ./frontend/node_modules/has-flag/index.d.ts
    ./frontend/node_modules/has-flag/package.json
    ./frontend/node_modules/has-flag/readme.md
    ./frontend/node_modules/has-flag/index.js
    ./frontend/node_modules/has-flag/license
    ./frontend/node_modules/jsdom/lib/jsdom/browser/not-implemented.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/index.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/ID.d.ts
    ./frontend/node_modules/@csstools/css-color-parser/dist/index.d.ts
    ./frontend/node_modules/@csstools/css-color-parser/dist/index.mjs
    ./frontend/node_modules/@csstools/css-color-parser/CHANGELOG.md
    ./frontend/node_modules/@csstools/css-color-parser/LICENSE.md
    ./frontend/node_modules/@eslint/config-array/dist/cjs/types.cts
    ./frontend/node_modules/undici/lib/web/fetch/formdata.js
    ./frontend/node_modules/undici/lib/web/fetch/headers.js
    ./frontend/node_modules/undici/lib/web/fetch/formdata-parser.js
    ./frontend/node_modules/undici/lib/web/fetch/body.js
    ./frontend/node_modules/undici/lib/web/fetch/index.js
    ./frontend/node_modules/undici/lib/web/fetch/global.js
    ./frontend/node_modules/undici/lib/web/fetch/request.js
    ./frontend/node_modules/undici/lib/web/fetch/response.js
    ./frontend/node_modules/undici/lib/web/fetch/LICENSE
    ./frontend/node_modules/undici/lib/web/fetch/util.js
    ./frontend/node_modules/undici/lib/web/fetch/data-url.js
    ./frontend/node_modules/undici/lib/web/fetch/constants.js
    ./frontend/node_modules/tldts-core/src/lookup/interface.ts
    ./frontend/node_modules/tldts-core/src/lookup/fast-path.ts
    ./frontend/node_modules/tldts-core/index.ts
    ./frontend/node_modules/tldts-core/package.json
    ./frontend/node_modules/tldts-core/README.md
    ./frontend/node_modules/@csstools/css-calc/package.json
    ./frontend/node_modules/@csstools/css-calc/README.md
    ./frontend/node_modules/xmlchars/xmlchars.js
    ./frontend/node_modules/xmlchars/package.json
    ./frontend/node_modules/lz-string/reference/lz-string-1.0.2.js
    ./frontend/node_modules/lz-string/package.json
    ./frontend/node_modules/lz-string/README.md
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/semver/internal/debug.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/semver/internal/lrucache.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/semver/internal/re.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/semver/internal/parse-options.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/semver/internal/identifiers.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/semver/internal/constants.js
    ./frontend/node_modules/jsdom/node_modules/lru-cache/package.json
    ./frontend/node_modules/jsdom/node_modules/lru-cache/README.md
    ./frontend/node_modules/@eslint/config-array/dist/cjs/std__path/windows.cjs
    ./frontend/node_modules/@eslint/config-array/dist/cjs/std__path/posix.cjs
    ./frontend/node_modules/@eslint/config-array/dist/cjs/index.cjs
    ./frontend/node_modules/@eslint/config-array/dist/cjs/index.d.cts
    ./frontend/node_modules/jsdom/lib/jsdom/browser/parser/index.js
    ./frontend/node_modules/jsdom/lib/jsdom/browser/parser/xml.js
    ./frontend/node_modules/jsdom/lib/jsdom/browser/parser/html.js
    ./frontend/node_modules/jsdom/lib/jsdom/browser/Window.js
    ./frontend/node_modules/@csstools/css-calc/dist/index.d.ts
    ./frontend/node_modules/@csstools/css-calc/dist/index.mjs
    ./frontend/node_modules/@csstools/css-calc/CHANGELOG.md
    ./frontend/node_modules/@csstools/css-calc/LICENSE.md
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/semver/classes/semver.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/semver/classes/comparator.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/semver/classes/index.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/semver/classes/range.js
    ./frontend/node_modules/lz-string/libs/base64-string.js
    ./frontend/node_modules/lz-string/libs/lz-string.min.js
    ./frontend/node_modules/lz-string/libs/lz-string.js
    ./frontend/node_modules/lz-string/bower.json
    ./frontend/node_modules/@eslint/config-array/dist/esm/index.d.ts
    ./frontend/node_modules/undici/lib/web/subresource-integrity/Readme.md
    ./frontend/node_modules/undici/lib/web/subresource-integrity/subresource-integrity.js
    ./frontend/node_modules/xmlchars/xmlns/1.0/ed3.js
    ./frontend/node_modules/xmlchars/xmlns/1.0/ed3.d.ts
    ./frontend/node_modules/@csstools/color-helpers/package.json
    ./frontend/node_modules/xmlchars/xmlns/1.0/ed3.js.map
    ./frontend/node_modules/@csstools/color-helpers/README.md
    ./frontend/node_modules/xmlchars/README.md
    ./frontend/node_modules/jsdom/node_modules/lru-cache/dist/commonjs/index.d.ts.map
    ./frontend/node_modules/jsdom/node_modules/lru-cache/dist/commonjs/index.min.js
    ./frontend/node_modules/jsdom/node_modules/lru-cache/dist/commonjs/index.d.ts
    ./frontend/node_modules/jsdom/node_modules/lru-cache/dist/commonjs/index.js.map
    ./frontend/node_modules/jsdom/node_modules/lru-cache/dist/commonjs/package.json
    ./frontend/node_modules/jsdom/node_modules/lru-cache/dist/commonjs/index.js
    ./frontend/node_modules/jsdom/node_modules/lru-cache/dist/commonjs/index.min.js.map
    ./frontend/node_modules/jsdom/lib/jsdom/browser/resources/stream-handler.js
    ./frontend/node_modules/jsdom/lib/jsdom/browser/resources/request-interceptor.js
    ./frontend/node_modules/jsdom/lib/jsdom/browser/resources/per-document-resource-loader.js
    ./frontend/node_modules/jsdom/lib/jsdom/browser/resources/decompress-interceptor.js
    ./frontend/node_modules/jsdom/lib/jsdom/browser/resources/request-manager.js
    ./frontend/node_modules/jsdom/lib/jsdom/browser/resources/async-resource-queue.js
    ./frontend/node_modules/jsdom/lib/jsdom/browser/resources/jsdom-dispatcher.js
    ./frontend/node_modules/jsdom/lib/jsdom/browser/resources/resource-queue.js
    ./frontend/node_modules/jsdom/lib/jsdom/browser/default-stylesheet.css
    ./frontend/node_modules/jsdom/lib/jsdom/virtual-console.js
    ./frontend/node_modules/@eslint/config-array/dist/esm/std__path/windows.js
    ./frontend/node_modules/@eslint/config-array/dist/esm/std__path/posix.js
    ./frontend/node_modules/@eslint/config-array/dist/esm/types.ts
    ./frontend/node_modules/@eslint/config-array/dist/esm/index.js
    ./frontend/node_modules/@eslint/config-array/dist/esm/types.d.ts
    ./frontend/node_modules/@eslint/config-array/LICENSE
    ./frontend/node_modules/jsdom/node_modules/lru-cache/dist/esm/index.d.ts.map
    ./frontend/node_modules/jsdom/node_modules/lru-cache/dist/esm/index.min.js
    ./frontend/node_modules/jsdom/node_modules/lru-cache/dist/esm/index.d.ts
    ./frontend/node_modules/jsdom/node_modules/lru-cache/dist/esm/index.js.map
    ./frontend/node_modules/jsdom/node_modules/lru-cache/dist/esm/package.json
    ./frontend/node_modules/jsdom/node_modules/lru-cache/dist/esm/index.js
    ./frontend/node_modules/jsdom/node_modules/lru-cache/dist/esm/index.min.js.map
    ./frontend/node_modules/jsdom/node_modules/lru-cache/LICENSE.md
    ./frontend/node_modules/path-exists/index.d.ts
    ./frontend/node_modules/path-exists/package.json
    ./frontend/node_modules/path-exists/readme.md
    ./frontend/node_modules/path-exists/index.js
    ./frontend/node_modules/path-exists/license
    ./frontend/node_modules/tldts-core/dist/cjs/src/domain.js.map
    ./frontend/node_modules/tldts-core/dist/cjs/src/subdomain.js.map
    ./frontend/node_modules/tldts-core/dist/cjs/src/domain-without-suffix.js.map
    ./frontend/node_modules/tldts-core/dist/cjs/src/options.js.map
    ./frontend/node_modules/tldts-core/dist/cjs/src/domain.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/semver/bin/semver.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/semver/LICENSE
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/semver/preload.js
    ./frontend/node_modules/undici/lib/web/webidl/index.js
    ./frontend/node_modules/xmlchars/xml/1.1/ed2.d.ts
    ./frontend/node_modules/xmlchars/xml/1.1/ed2.js
    ./frontend/node_modules/xmlchars/xml/1.1/ed2.js.map
    ./frontend/node_modules/@csstools/color-helpers/dist/index.d.ts
    ./frontend/node_modules/@csstools/color-helpers/dist/index.mjs
    ./frontend/node_modules/@csstools/color-helpers/CHANGELOG.md
    ./frontend/node_modules/@csstools/color-helpers/LICENSE.md
    ./frontend/node_modules/brace-expansion/package.json
    ./frontend/node_modules/brace-expansion/README.md
    ./frontend/node_modules/brace-expansion/index.js
    ./frontend/node_modules/brace-expansion/LICENSE
    ./frontend/node_modules/jsdom/lib/jsdom/level3/xpath.js
    ./frontend/node_modules/tldts-core/dist/cjs/src/lookup/fast-path.js
    ./frontend/node_modules/tldts-core/dist/cjs/src/lookup/fast-path.js.map
    ./frontend/node_modules/tldts-core/dist/cjs/src/lookup/interface.js.map
    ./frontend/node_modules/tldts-core/dist/cjs/src/lookup/interface.js
    ./frontend/node_modules/tldts-core/dist/cjs/src/is-valid.js.map
    ./frontend/node_modules/tldts-core/dist/cjs/src/extract-hostname.js
    ./frontend/node_modules/tldts-core/dist/cjs/src/options.js
    ./frontend/node_modules/tldts-core/dist/cjs/src/is-ip.js
    ./frontend/node_modules/tldts-core/dist/cjs/src/domain-without-suffix.js
    ./frontend/node_modules/tldts-core/dist/cjs/src/is-ip.js.map
    ./frontend/node_modules/tldts-core/dist/cjs/src/is-valid.js
    ./frontend/node_modules/tldts-core/dist/cjs/src/subdomain.js
    ./frontend/node_modules/tldts-core/dist/cjs/src/extract-hostname.js.map
    ./frontend/node_modules/tldts-core/dist/cjs/src/factory.js
    ./frontend/node_modules/tldts-core/dist/cjs/src/factory.js.map
    ./frontend/node_modules/tldts-core/dist/cjs/index.js.map
    ./frontend/node_modules/tldts-core/dist/cjs/index.js
    ./frontend/node_modules/tldts-core/dist/cjs/tsconfig.tsbuildinfo
    ./frontend/node_modules/balanced-match/.github/FUNDING.yml
    ./frontend/node_modules/balanced-match/package.json
    ./frontend/node_modules/balanced-match/README.md
    ./frontend/node_modules/balanced-match/index.js
    ./frontend/node_modules/balanced-match/LICENSE.md
    ./frontend/node_modules/@csstools/css-syntax-patches-for-csstree/package.json
    ./frontend/node_modules/@csstools/css-syntax-patches-for-csstree/README.md
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/decorators.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2024.arraybuffer.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/esnext.weakref.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2017.date.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2016.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2022.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2018.promise.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2020.sharedmemory.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2021.promise.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2015.symbol.wellknown.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2019.symbol.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2025.float16.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2015.reflect.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2015.generator.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2022.array.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2023.array.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2025.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2024.regexp.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es7.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2025.full.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2015.iterable.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/esnext.object.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/esnext.promise.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2023.full.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2017.sharedmemory.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2024.regexp.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/esnext.typedarrays.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/esnext.string.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/esnext.asynciterable.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2015.collection.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2022.full.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/esnext.full.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/esnext.sharedmemory.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2023.full.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2022.regexp.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/index.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/esnext.promise.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2020.symbol.wellknown.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2016.full.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2020.date.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/lib.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/dom.iterable.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2021.weakref.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2025.iterator.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2024.promise.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/esnext.array.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2022.intl.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2024.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2017.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2015.proxy.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2024.sharedmemory.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2023.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/esnext.intl.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2025.intl.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2017.intl.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2015.reflect.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/esnext.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2020.bigint.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es6.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/esnext.error.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/esnext.string.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2018.asyncgenerator.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2015.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2019.array.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2015.collection.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2020.string.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2020.full.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2019.symbol.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2025.regexp.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2024.full.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/webworker.asynciterable.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2025.promise.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/esnext.iterator.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2019.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/dom.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/scripthost.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2024.arraybuffer.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2022.regexp.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2018.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/dom.asynciterable.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2024.string.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es7.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2018.intl.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2023.array.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2018.asyncgenerator.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2020.bigint.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2019.object.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/decorators.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2016.full.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2023.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2015.symbol.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2025.intl.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/esnext.iterator.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2022.full.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2015.symbol.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2019.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/decorators.legacy.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2019.intl.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/esnext.bigint.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2022.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/esnext.regexp.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2024.promise.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2018.asynciterable.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2017.full.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2024.sharedmemory.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es6.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2017.full.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2025.collection.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2020.number.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2018.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2017.sharedmemory.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2017.typedarrays.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/base-config.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/esnext.intl.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2017.object.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2017.string.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2021.full.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2023.intl.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2017.string.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2015.iterable.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2016.intl.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/esnext.weakref.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2022.string.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/esnext.error.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2015.promise.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2020.date.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2016.array.include.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2021.promise.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2024.collection.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2022.string.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/dom.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/esnext.decorators.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2017.object.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/webworker.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2022.object.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/webworker.iterable.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2024.full.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2017.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2022.object.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/esnext.bigint.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2025.collection.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/webworker.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/scripthost.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2021.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2018.asynciterable.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/esnext.disposable.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2023.intl.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2019.object.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2025.promise.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/index.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/lib.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es5.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2019.string.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/esnext.decorators.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/esnext.symbol.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2018.intl.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2025.regexp.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2020.promise.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2022.intl.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/webworker.importscripts.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2024.object.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2019.string.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2020.promise.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2020.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2021.full.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/dom.asynciterable.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/base-config.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2017.arraybuffer.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2016.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/esnext.asynciterable.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2017.arraybuffer.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2021.string.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/esnext.float16.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/esnext.float16.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2018.regexp.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/esnext.date.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2019.full.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2020.number.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2020.intl.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2023.collection.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2025.full.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/esnext.collection.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/esnext.full.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/webworker.importscripts.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2022.error.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2020.intl.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/esnext.symbol.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2024.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2024.object.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/webworker.asynciterable.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2024.string.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/dom.iterable.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/esnext.array.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/esnext.temporal.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2023.collection.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2017.typedarrays.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/esnext.regexp.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/esnext.object.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2019.array.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2018.full.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/esnext.collection.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/esnext.typedarrays.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2020.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/esnext.date.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/esnext.disposable.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2016.intl.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/esnext.sharedmemory.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es5.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/esnext.temporal.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/webworker.iterable.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2019.full.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2019.intl.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2015.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2021.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2025.float16.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2015.core.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2020.full.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2025.iterator.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/esnext.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2015.proxy.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2015.promise.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2017.intl.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2021.weakref.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2018.regexp.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2018.full.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/decorators.legacy.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2015.symbol.wellknown.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2022.array.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2021.intl.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2016.array.include.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2025.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2024.collection.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2020.symbol.wellknown.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2020.string.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2015.generator.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2020.sharedmemory.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2022.error.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2018.promise.js
    ./frontend/node_modules/detect-libc/index.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2017.date.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2015.core.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2021.intl.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/lib/es2021.string.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/analyze.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/semver/ranges/intersects.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/semver/ranges/subset.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/semver/ranges/valid.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/semver/ranges/max-satisfying.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/semver/ranges/to-comparators.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/semver/ranges/simplify.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/semver/ranges/min-satisfying.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/semver/ranges/gtr.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/semver/ranges/ltr.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/semver/ranges/outside.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/semver/ranges/min-version.js
    ./frontend/node_modules/@csstools/css-syntax-patches-for-csstree/dist/index.json
    ./frontend/node_modules/@csstools/css-syntax-patches-for-csstree/dist/index.d.ts
    ./frontend/node_modules/@csstools/css-syntax-patches-for-csstree/CHANGELOG.md
    ./frontend/node_modules/@csstools/css-syntax-patches-for-csstree/LICENSE.md
    ./frontend/node_modules/xmlchars/xml/1.0/ed4.js.map
    ./frontend/node_modules/xmlchars/xml/1.0/ed4.d.ts
    ./frontend/node_modules/xmlchars/xml/1.0/ed5.d.ts
    ./frontend/node_modules/xmlchars/xml/1.0/ed5.js.map
    ./frontend/node_modules/xmlchars/xml/1.0/ed5.js
    ./frontend/node_modules/xmlchars/xml/1.0/ed4.js
    ./frontend/node_modules/xmlchars/LICENSE
    ./frontend/node_modules/xmlchars/xmlchars.js.map
    ./frontend/node_modules/xmlchars/xmlchars.d.ts
    ./frontend/node_modules/tinybench/package.json
    ./frontend/node_modules/tinybench/README.md
    ./frontend/node_modules/detect-libc/lib/elf.js
    ./frontend/node_modules/detect-libc/lib/process.js
    ./frontend/node_modules/detect-libc/lib/detect-libc.js
    ./frontend/node_modules/detect-libc/lib/filesystem.js
    ./frontend/node_modules/detect-libc/package.json
    ./frontend/node_modules/detect-libc/README.md
    ./frontend/node_modules/detect-libc/LICENSE
    ./frontend/node_modules/lz-string/tests/lib/jasmine-1.3.1/jasmine-html.js
    ./frontend/node_modules/lz-string/tests/lib/jasmine-1.3.1/jasmine.js
    ./frontend/node_modules/lz-string/tests/lib/jasmine-1.3.1/MIT.LICENSE
    ./frontend/node_modules/lz-string/tests/lib/jasmine-1.3.1/jasmine.css
    ./frontend/node_modules/lz-string/tests/lz-string-spec.js
    ./frontend/node_modules/lz-string/tests/SpecRunner.html
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/brace-expansion/package.json
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/brace-expansion/README.md
    ./frontend/node_modules/jsdom/lib/jsdom/living/window-properties.js
    ./frontend/node_modules/tinybench/dist/index.d.ts
    ./frontend/node_modules/tinybench/dist/index.cjs
    ./frontend/node_modules/tinybench/dist/index.js
    ./frontend/node_modules/tinybench/dist/index.d.cts
    ./frontend/node_modules/tinybench/LICENSE
    ./frontend/node_modules/undici/lib/web/cache/cachestorage.js
    ./frontend/node_modules/undici/lib/web/cache/cache.js
    ./frontend/node_modules/undici/lib/web/cache/util.js
    ./frontend/node_modules/js-tokens/package.json
    ./frontend/node_modules/js-tokens/README.md
    ./frontend/node_modules/js-tokens/index.js
    ./frontend/node_modules/js-tokens/CHANGELOG.md
    ./frontend/node_modules/js-tokens/LICENSE
    ./frontend/node_modules/path-key/index.d.ts
    ./frontend/node_modules/@csstools/css-tokenizer/package.json
    ./frontend/node_modules/path-key/package.json
    ./frontend/node_modules/path-key/readme.md
    ./frontend/node_modules/path-key/index.js
    ./frontend/node_modules/path-key/license
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/definition/FunctionNameDefinition.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/definition/ImportBindingDefinition.js
    ./frontend/node_modules/fast-json-stable-stringify/.travis.yml
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/definition/Definition.js
    ./frontend/node_modules/fast-json-stable-stringify/index.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/definition/Definition.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/definition/ClassNameDefinition.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/definition/index.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/definition/ParameterDefinition.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/definition/TSModuleNameDefinition.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/definition/DefinitionBase.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/definition/VariableDefinition.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/definition/ImplicitGlobalVariableDefinition.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/definition/TSModuleNameDefinition.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/definition/CatchClauseDefinition.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/definition/TSEnumMemberDefinition.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/definition/ParameterDefinition.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/definition/FunctionNameDefinition.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/definition/ImportBindingDefinition.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/definition/TypeDefinition.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/definition/DefinitionType.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/definition/TSEnumMemberDefinition.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/definition/DefinitionBase.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/definition/index.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/definition/DefinitionType.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/definition/TypeDefinition.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/definition/TSEnumNameDefinition.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/definition/TSEnumNameDefinition.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/definition/VariableDefinition.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/definition/ClassNameDefinition.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/definition/CatchClauseDefinition.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/definition/ImplicitGlobalVariableDefinition.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/assert.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/tsconfig.build.tsbuildinfo
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/ID.js
    ./frontend/node_modules/@csstools/css-tokenizer/README.md
    ./frontend/node_modules/lz-string/typings/lz-string.d.ts
    ./frontend/node_modules/eslint-plugin-react-refresh/index.d.ts
    ./frontend/node_modules/eslint-plugin-react-refresh/package.json
    ./frontend/node_modules/eslint-plugin-react-refresh/README.md
    ./frontend/node_modules/eslint-plugin-react-refresh/index.js
    ./frontend/node_modules/eslint-plugin-react-refresh/LICENSE
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/brace-expansion/dist/commonjs/index.d.ts.map
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/brace-expansion/dist/commonjs/index.d.ts
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/brace-expansion/dist/commonjs/index.js.map
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/brace-expansion/dist/commonjs/package.json
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/brace-expansion/dist/commonjs/index.js
    ./frontend/node_modules/tldts-core/dist/es6/src/domain.js.map
    ./frontend/node_modules/tldts-core/dist/es6/src/subdomain.js.map
    ./frontend/node_modules/tldts-core/dist/es6/src/domain-without-suffix.js.map
    ./frontend/node_modules/tldts-core/dist/es6/src/options.js.map
    ./frontend/node_modules/tldts-core/dist/es6/src/domain.js
    ./frontend/node_modules/color-convert/package.json
    ./frontend/node_modules/color-convert/README.md
    ./frontend/node_modules/color-convert/index.js
    ./frontend/node_modules/color-convert/CHANGELOG.md
    ./frontend/node_modules/color-convert/LICENSE
    ./frontend/node_modules/color-convert/conversions.js
    ./frontend/node_modules/color-convert/route.js
    ./frontend/node_modules/undici/lib/web/infra/index.js
    ./frontend/node_modules/@csstools/css-tokenizer/dist/index.d.ts
    ./frontend/node_modules/@csstools/css-tokenizer/dist/index.mjs
    ./frontend/node_modules/@csstools/css-tokenizer/CHANGELOG.md
    ./frontend/node_modules/@csstools/css-tokenizer/LICENSE.md
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/brace-expansion/dist/esm/index.d.ts.map
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/brace-expansion/dist/esm/index.d.ts
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/brace-expansion/dist/esm/index.js.map
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/brace-expansion/dist/esm/package.json
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/brace-expansion/dist/esm/index.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/brace-expansion/LICENSE
    ./frontend/node_modules/jsdom/lib/jsdom/living/helpers/iterable-weak-set.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/helpers/text.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/helpers/shadow-dom.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/helpers/by-id-cache.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/helpers/details.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/helpers/binary-data.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/helpers/json.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/helpers/strings.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/helpers/namespaces.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/helpers/page-transition-event.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/helpers/html-constructor.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/helpers/number-and-date-inputs.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/helpers/dates-and-times.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/helpers/create-event-accessor.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/helpers/node.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/helpers/internal-constants.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/helpers/custom-elements.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/helpers/focusing.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/helpers/validate-names.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/helpers/encoding.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/helpers/is-window.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/helpers/runtime-script-errors.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/helpers/create-element.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/helpers/form-controls.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/helpers/mutation-observers.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/helpers/events.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/helpers/traversal.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/helpers/ordered-set.js
    ./frontend/node_modules/ansi-styles/index.d.ts
    ./frontend/node_modules/ansi-styles/package.json
    ./frontend/node_modules/ansi-styles/readme.md
    ./frontend/node_modules/ansi-styles/index.js
    ./frontend/node_modules/ansi-styles/license
    ./frontend/node_modules/tldts-core/dist/es6/src/lookup/fast-path.js
    ./frontend/node_modules/tldts-core/dist/es6/src/lookup/fast-path.js.map
    ./frontend/node_modules/tldts-core/dist/es6/src/lookup/interface.js.map
    ./frontend/node_modules/tldts-core/dist/es6/src/lookup/interface.js
    ./frontend/node_modules/tldts-core/dist/es6/src/is-valid.js.map
    ./frontend/node_modules/tldts-core/dist/es6/src/extract-hostname.js
    ./frontend/node_modules/tldts-core/dist/es6/src/options.js
    ./frontend/node_modules/tldts-core/dist/es6/src/is-ip.js
    ./frontend/node_modules/tldts-core/dist/es6/src/domain-without-suffix.js
    ./frontend/node_modules/tldts-core/dist/es6/src/is-ip.js.map
    ./frontend/node_modules/tldts-core/dist/es6/src/is-valid.js
    ./frontend/node_modules/tldts-core/dist/es6/src/subdomain.js
    ./frontend/node_modules/tldts-core/dist/es6/src/extract-hostname.js.map
    ./frontend/node_modules/tldts-core/dist/es6/src/factory.js
    ./frontend/node_modules/tldts-core/dist/es6/src/factory.js.map
    ./frontend/node_modules/tldts-core/dist/es6/index.js.map
    ./frontend/node_modules/tldts-core/dist/es6/tsconfig.bundle.tsbuildinfo
    ./frontend/node_modules/tldts-core/dist/es6/index.js
    ./frontend/node_modules/fdir/package.json
    ./frontend/node_modules/fdir/README.md
    ./frontend/node_modules/fast-json-stable-stringify/.github/FUNDING.yml
    ./frontend/node_modules/fast-json-stable-stringify/package.json
    ./frontend/node_modules/fast-json-stable-stringify/README.md
    ./frontend/node_modules/fast-json-stable-stringify/index.js
    ./frontend/node_modules/fdir/dist/index.mjs
    ./frontend/node_modules/estraverse/gulpfile.js
    ./frontend/node_modules/fdir/dist/index.cjs
    ./frontend/node_modules/fdir/dist/index.d.cts
    ./frontend/node_modules/fdir/dist/index.d.mts
    ./frontend/node_modules/fdir/LICENSE
    ./frontend/node_modules/fast-json-stable-stringify/example/value_cmp.js
    ./frontend/node_modules/fast-json-stable-stringify/example/nested.js
    ./frontend/node_modules/fast-json-stable-stringify/example/str.js
    ./frontend/node_modules/fast-json-stable-stringify/example/key_cmp.js
    ./frontend/node_modules/lz-string/bin/bin.js
    ./frontend/node_modules/lz-string/LICENSE
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/balanced-match/package.json
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/balanced-match/README.md
    ./frontend/node_modules/fast-json-stable-stringify/test/to-json.js
    ./frontend/node_modules/fast-json-stable-stringify/test/cmp.js
    ./frontend/node_modules/fast-json-stable-stringify/test/nested.js
    ./frontend/node_modules/fast-json-stable-stringify/test/str.js
    ./frontend/node_modules/fast-json-stable-stringify/LICENSE
    ./frontend/node_modules/fast-json-stable-stringify/.eslintrc.yml
    ./frontend/node_modules/estraverse/package.json
    ./frontend/node_modules/estraverse/LICENSE.BSD
    ./frontend/node_modules/estraverse/README.md
    ./frontend/node_modules/estraverse/.jshintrc
    ./frontend/node_modules/estraverse/estraverse.js
    ./frontend/node_modules/@csstools/css-parser-algorithms/package.json
    ./frontend/node_modules/@csstools/css-parser-algorithms/README.md
    ./frontend/node_modules/fast-json-stable-stringify/benchmark/test.json
    ./frontend/node_modules/fast-json-stable-stringify/benchmark/index.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/helpers/svg/render.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/helpers/svg/basic-types.js
    ./frontend/node_modules/undici/lib/web/websocket/frame.js
    ./frontend/node_modules/undici/lib/web/websocket/connection.js
    ./frontend/node_modules/undici/lib/web/websocket/websocket.js
    ./frontend/node_modules/undici/lib/web/websocket/sender.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/balanced-match/dist/commonjs/index.d.ts.map
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/balanced-match/dist/commonjs/index.d.ts
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/balanced-match/dist/commonjs/index.js.map
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/balanced-match/dist/commonjs/package.json
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/balanced-match/dist/commonjs/index.js
    ./frontend/node_modules/minimatch/minimatch.js
    ./frontend/node_modules/minimatch/package.json
    ./frontend/node_modules/minimatch/README.md
    ./frontend/node_modules/minimatch/LICENSE
    ./frontend/node_modules/@csstools/css-parser-algorithms/dist/index.d.ts
    ./frontend/node_modules/@csstools/css-parser-algorithms/dist/index.mjs
    ./frontend/node_modules/@csstools/css-parser-algorithms/CHANGELOG.md
    ./frontend/node_modules/@csstools/css-parser-algorithms/LICENSE.md
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/scope/ConditionalTypeScope.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/scope/ConditionalTypeScope.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/scope/index.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/scope/ScopeBase.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/scope/GlobalScope.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/scope/ModuleScope.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/scope/FunctionExpressionNameScope.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/scope/TSEnumScope.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/scope/Scope.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/scope/ForScope.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/scope/GlobalScope.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/scope/WithScope.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/scope/TypeScope.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/scope/MappedTypeScope.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/scope/BlockScope.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/scope/SwitchScope.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/scope/ClassStaticBlockScope.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/scope/ModuleScope.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/scope/ClassScope.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/scope/TSModuleScope.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/scope/index.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/scope/ClassFieldInitializerScope.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/scope/CatchScope.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/scope/ClassStaticBlockScope.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/scope/FunctionTypeScope.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/scope/ScopeType.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/scope/ScopeBase.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/scope/ScopeType.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/scope/BlockScope.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/scope/Scope.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/scope/CatchScope.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/scope/MappedTypeScope.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/scope/FunctionExpressionNameScope.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/scope/FunctionTypeScope.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/scope/TSEnumScope.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/scope/FunctionScope.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/scope/ForScope.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/scope/WithScope.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/scope/TSModuleScope.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/scope/ClassFieldInitializerScope.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/scope/ClassScope.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/scope/SwitchScope.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/scope/TypeScope.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/scope/FunctionScope.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/index.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/ScopeManager.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/analyze.d.ts
    ./frontend/node_modules/jsdom/lib/jsdom/living/xhr/XMLHttpRequestEventTarget-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/xhr/multipart-form-data.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/xhr/xhr-sync-worker.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/xhr/xhr-utils.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/xhr/XMLHttpRequest-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/xhr/XMLHttpRequestUpload-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/xhr/FormData-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/attributes.js
    ./frontend/node_modules/hermes-estree/package.json
    ./frontend/node_modules/hermes-estree/README.md
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/balanced-match/dist/esm/index.d.ts.map
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/balanced-match/dist/esm/index.d.ts
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/balanced-match/dist/esm/index.js.map
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/balanced-match/dist/esm/package.json
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/balanced-match/dist/esm/index.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/node_modules/balanced-match/LICENSE.md
    ./frontend/node_modules/chai/package.json
    ./frontend/node_modules/chai/register-should.js
    ./frontend/node_modules/chai/README.md
    ./frontend/node_modules/chai/index.js
    ./frontend/node_modules/chai/register-expect.js
    ./frontend/node_modules/chai/register-assert.js
    ./frontend/node_modules/chai/LICENSE
    ./frontend/node_modules/tldts-core/dist/types/src/is-ip.d.ts
    ./frontend/node_modules/tldts-core/dist/types/src/extract-hostname.d.ts
    ./frontend/node_modules/tldts-core/dist/types/src/domain.d.ts
    ./frontend/node_modules/tldts-core/dist/types/index.d.ts
    ./frontend/node_modules/tldts-core/LICENSE
    ./frontend/node_modules/tldts-core/dist/types/src/factory.d.ts
    ./frontend/node_modules/tldts-core/dist/types/src/subdomain.d.ts
    ./frontend/node_modules/tldts-core/dist/types/src/domain-without-suffix.d.ts
    ./frontend/node_modules/jsdom/lib/jsdom/living/range/AbstractRange-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/range/Range-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/range/boundary-point.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/range/StaticRange-impl.js
    ./frontend/node_modules/react/cjs/react-jsx-dev-runtime.development.js
    ./frontend/node_modules/react/cjs/react.production.js
    ./frontend/node_modules/react/cjs/react-jsx-dev-runtime.react-server.development.js
    ./frontend/node_modules/react/cjs/react-jsx-runtime.development.js
    ./frontend/node_modules/react/cjs/react.react-server.development.js
    ./frontend/node_modules/react/cjs/react-compiler-runtime.development.js
    ./frontend/node_modules/react/cjs/react.react-server.production.js
    ./frontend/node_modules/react/cjs/react-jsx-runtime.react-server.development.js
    ./frontend/node_modules/react/cjs/react-jsx-runtime.react-server.production.js
    ./frontend/node_modules/react/cjs/react-jsx-runtime.profiling.js
    ./frontend/node_modules/react/cjs/react-jsx-dev-runtime.production.js
    ./frontend/node_modules/react/cjs/react.development.js
    ./frontend/node_modules/react/cjs/react-jsx-dev-runtime.profiling.js
    ./frontend/node_modules/react/cjs/react-jsx-dev-runtime.react-server.production.js
    ./frontend/node_modules/react/cjs/react-jsx-runtime.production.js
    ./frontend/node_modules/react/cjs/react-compiler-runtime.production.js
    ./frontend/node_modules/react/cjs/react-compiler-runtime.profiling.js
    ./frontend/node_modules/react/jsx-dev-runtime.js
    ./frontend/node_modules/react/compiler-runtime.js
    ./frontend/node_modules/react/jsx-dev-runtime.react-server.js
    ./frontend/node_modules/react/package.json
    ./frontend/node_modules/react/README.md
    ./frontend/node_modules/react/index.js
    ./frontend/node_modules/react/jsx-runtime.js
    ./frontend/node_modules/react/jsx-runtime.react-server.js
    ./frontend/node_modules/react/LICENSE
    ./frontend/node_modules/react/react.react-server.js
    ./frontend/node_modules/undici/lib/web/websocket/stream/websocketstream.js
    ./frontend/node_modules/undici/lib/web/websocket/stream/websocketerror.js
    ./frontend/node_modules/undici/lib/web/websocket/receiver.js
    ./frontend/node_modules/undici/lib/web/websocket/permessage-deflate.js
    ./frontend/node_modules/undici/lib/web/websocket/util.js
    ./frontend/node_modules/undici/lib/web/websocket/events.js
    ./frontend/node_modules/undici/lib/web/websocket/constants.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/domparsing/serialization.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/domparsing/parse5-adapter-serialization.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/domparsing/XMLSerializer-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/domparsing/DOMParser-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/domparsing/InnerHTML-impl.js
    ./frontend/node_modules/dequal/index.d.ts
    ./frontend/node_modules/dequal/package.json
    ./frontend/node_modules/dequal/readme.md
    ./frontend/node_modules/tldts-core/dist/types/src/lookup/interface.d.ts
    ./frontend/node_modules/tldts-core/dist/types/src/lookup/fast-path.d.ts
    ./frontend/node_modules/tldts-core/dist/types/src/is-valid.d.ts
    ./frontend/node_modules/tldts-core/dist/types/src/options.d.ts
    ./frontend/node_modules/undici/package.json
    ./frontend/node_modules/undici/README.md
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/referencer/ClassVisitor.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/referencer/VisitorBase.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/referencer/Reference.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/referencer/ExportVisitor.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/referencer/index.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/referencer/Visitor.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/referencer/TypeVisitor.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/referencer/Visitor.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/referencer/Reference.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/referencer/TypeVisitor.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/referencer/index.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/referencer/ClassVisitor.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/referencer/ExportVisitor.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/referencer/Referencer.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/referencer/VisitorBase.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/referencer/Referencer.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/referencer/PatternVisitor.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/referencer/ImportVisitor.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/referencer/ImportVisitor.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/referencer/PatternVisitor.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/events/KeyboardEvent-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/events/CustomEvent-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/events/EventTarget-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/events/HashChangeEvent-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/events/FocusEvent-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/events/TransitionEvent-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/events/Event-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/events/CompositionEvent-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/events/StorageEvent-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/events/PromiseRejectionEvent-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/events/SubmitEvent-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/events/DeviceOrientationEvent-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/events/EventModifierMixin-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/events/PointerEvent-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/events/BeforeUnloadEvent-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/events/WheelEvent-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/events/PageTransitionEvent-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/events/MessageEvent-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/events/InputEvent-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/events/BlobEvent-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/events/DeviceMotionEvent-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/events/TouchEvent-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/events/UIEvent-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/events/PopStateEvent-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/events/ErrorEvent-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/events/CloseEvent-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/events/ProgressEvent-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/events/MouseEvent-impl.js
    ./frontend/node_modules/decimal.js/decimal.d.ts
    ./frontend/node_modules/decimal.js/package.json
    ./frontend/node_modules/decimal.js/README.md
    ./frontend/node_modules/decimal.js/decimal.mjs
    ./frontend/node_modules/decimal.js/LICENCE.md
    ./frontend/node_modules/decimal.js/decimal.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/file-api/File-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/file-api/FileList-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/file-api/Blob-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/file-api/FileReader-impl.js
    ./frontend/node_modules/hermes-estree/dist/types.js.flow
    ./frontend/node_modules/hermes-estree/dist/selectors.js.flow
    ./frontend/node_modules/hermes-estree/dist/index.js.flow
    ./frontend/node_modules/hermes-estree/dist/predicates.js.flow
    ./frontend/node_modules/hermes-estree/dist/index.js
    ./frontend/node_modules/hermes-estree/dist/predicates.js
    ./frontend/node_modules/hermes-estree/dist/selectors.js
    ./frontend/node_modules/hermes-estree/dist/types.js
    ./frontend/node_modules/dequal/lite/index.min.js
    ./frontend/node_modules/dequal/lite/index.d.ts
    ./frontend/node_modules/dequal/lite/index.mjs
    ./frontend/node_modules/dequal/lite/index.js
    ./frontend/node_modules/undici/lib/web/eventsource/eventsource.js
    ./frontend/node_modules/undici/lib/web/eventsource/util.js
    ./frontend/node_modules/undici/lib/web/eventsource/eventsource-stream.js
    ./frontend/node_modules/dequal/dist/index.min.js
    ./frontend/node_modules/dequal/dist/index.mjs
    ./frontend/node_modules/dequal/dist/index.js
    ./frontend/node_modules/dequal/license
    ./frontend/node_modules/undici/lib/util/stats.js
    ./frontend/node_modules/undici/lib/util/date.js
    ./frontend/node_modules/undici/lib/util/timers.js
    ./frontend/node_modules/undici/lib/util/runtime-features.js
    ./frontend/node_modules/undici/lib/util/promise.js
    ./frontend/node_modules/undici/lib/util/cache.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/geometry/DOMRectReadOnly-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/geometry/DOMRect-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/node-type.js
    ./frontend/node_modules/hermes-estree/dist/generated/predicates.js.flow
    ./frontend/node_modules/hermes-estree/dist/generated/predicates.js
    ./frontend/node_modules/hermes-estree/dist/generated/HermesESTreeSelectorTypes.js.flow
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/variable/ImplicitLibVariable.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/variable/Variable.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/variable/VariableBase.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/variable/index.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/variable/ESLintScopeVariable.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/variable/ImplicitLibVariable.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/variable/ESLintScopeVariable.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/variable/VariableBase.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/variable/Variable.d.ts
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/variable/index.js
    ./frontend/node_modules/hermes-estree/LICENSE
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/assert.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/dist/ScopeManager.js
    ./frontend/node_modules/@typescript-eslint/scope-manager/LICENSE
    ./frontend/node_modules/jsdom/lib/jsdom/living/encoding/TextEncoder-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/encoding/TextDecoder-impl.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/dist/parseSettings/warnAboutTSVersion.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/dist/parseSettings/getProjectConfigFiles.d.ts
    ./frontend/node_modules/@typescript-eslint/typescript-estree/dist/parseSettings/resolveProjectList.d.ts
    ./frontend/node_modules/@typescript-eslint/typescript-estree/dist/parseSettings/index.d.ts
    ./frontend/node_modules/@typescript-eslint/typescript-estree/dist/parseSettings/createParseSettings.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/dist/parseSettings/createParseSettings.d.ts
    ./frontend/node_modules/@typescript-eslint/typescript-estree/dist/parseSettings/inferSingleRun.d.ts
    ./frontend/node_modules/@typescript-eslint/typescript-estree/dist/parseSettings/index.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/dist/parseSettings/getProjectConfigFiles.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/dist/parseSettings/candidateTSConfigRootDirs.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/dist/parseSettings/ExpiringCache.d.ts
    ./frontend/node_modules/@typescript-eslint/typescript-estree/dist/parseSettings/candidateTSConfigRootDirs.d.ts
    ./frontend/node_modules/@typescript-eslint/typescript-estree/dist/parseSettings/inferSingleRun.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/dist/parseSettings/ExpiringCache.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/dist/parseSettings/warnAboutTSVersion.d.ts
    ./frontend/node_modules/@typescript-eslint/typescript-estree/dist/parseSettings/resolveProjectList.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/dist/node-utils.js
    ./frontend/node_modules/tough-cookie/package.json
    ./frontend/node_modules/tough-cookie/README.md
    ./frontend/node_modules/undici/types/mock-errors.d.ts
    ./frontend/node_modules/undici/types/mock-interceptor.d.ts
    ./frontend/node_modules/undici/types/content-type.d.ts
    ./frontend/node_modules/undici/types/client.d.ts
    ./frontend/node_modules/undici/types/global-dispatcher.d.ts
    ./frontend/node_modules/undici/types/retry-agent.d.ts
    ./frontend/node_modules/undici/types/proxy-agent.d.ts
    ./frontend/node_modules/undici/types/mock-pool.d.ts
    ./frontend/node_modules/undici/types/index.d.ts
    ./frontend/node_modules/undici/types/patch.d.ts
    ./frontend/node_modules/undici/types/h2c-client.d.ts
    ./frontend/node_modules/undici/types/util.d.ts
    ./frontend/node_modules/undici/types/diagnostics-channel.d.ts
    ./frontend/node_modules/undici/types/mock-call-history.d.ts
    ./frontend/node_modules/undici/types/pool.d.ts
    ./frontend/node_modules/undici/types/cookies.d.ts
    ./frontend/node_modules/undici/types/cache.d.ts
    ./frontend/node_modules/undici/types/handlers.d.ts
    ./frontend/node_modules/undici/types/formdata.d.ts
    ./frontend/node_modules/undici/types/webidl.d.ts
    ./frontend/node_modules/undici/types/README.md
    ./frontend/node_modules/undici/types/fetch.d.ts
    ./frontend/node_modules/undici/types/interceptors.d.ts
    ./frontend/node_modules/undici/types/socks5-proxy-agent.d.ts
    ./frontend/node_modules/undici/types/mock-agent.d.ts
    ./frontend/node_modules/undici/types/agent.d.ts
    ./frontend/node_modules/undici/types/balanced-pool.d.ts
    ./frontend/node_modules/undici/types/retry-handler.d.ts
    ./frontend/node_modules/undici/types/connector.d.ts
    ./frontend/node_modules/undici/types/websocket.d.ts
    ./frontend/node_modules/undici/types/client-stats.d.ts
    ./frontend/node_modules/undici/types/utility.d.ts
    ./frontend/node_modules/undici/types/errors.d.ts
    ./frontend/node_modules/undici/types/dispatcher.d.ts
    ./frontend/node_modules/undici/types/cache-interceptor.d.ts
    ./frontend/node_modules/undici/types/readable.d.ts
    ./frontend/node_modules/undici/types/api.d.ts
    ./frontend/node_modules/undici/types/env-http-proxy-agent.d.ts
    ./frontend/node_modules/undici/types/eventsource.d.ts
    ./frontend/node_modules/undici/types/mock-client.d.ts
    ./frontend/node_modules/undici/types/pool-stats.d.ts
    ./frontend/node_modules/undici/types/header.d.ts
    ./frontend/node_modules/undici/types/global-origin.d.ts
    ./frontend/node_modules/undici/types/round-robin-pool.d.ts
    ./frontend/node_modules/undici/types/snapshot-agent.d.ts
    ./frontend/node_modules/undici/index-fetch.js
    ./frontend/node_modules/undici/LICENSE
    ./frontend/node_modules/undici/index.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/webstorage/Storage-impl.js
    ./frontend/node_modules/undici/lib/cache/memory-cache-store.js
    ./frontend/node_modules/undici/lib/cache/sqlite-cache-store.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/websockets/WebSocket-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/interfaces.js
    ./frontend/node_modules/undici/lib/handler/redirect-handler.js
    ./frontend/node_modules/undici/lib/handler/unwrap-handler.js
    ./frontend/node_modules/undici/lib/handler/wrap-handler.js
    ./frontend/node_modules/undici/lib/handler/deduplication-handler.js
    ./frontend/node_modules/undici/lib/handler/retry-handler.js
    ./frontend/node_modules/undici/lib/handler/cache-handler.js
    ./frontend/node_modules/undici/lib/handler/decorator-handler.js
    ./frontend/node_modules/undici/lib/handler/cache-revalidation-handler.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/custom-elements/ElementInternals-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/custom-elements/CustomElementRegistry-impl.js
    ./frontend/node_modules/vite/client.d.ts
    ./frontend/node_modules/vite/package.json
    ./frontend/node_modules/vite/README.md
    ./frontend/node_modules/tough-cookie/dist/index.d.ts
    ./frontend/node_modules/tough-cookie/dist/index.js.map
    ./frontend/node_modules/tough-cookie/dist/index.cjs
    ./frontend/node_modules/tough-cookie/dist/index.cjs.map
    ./frontend/node_modules/tough-cookie/dist/index.js
    ./frontend/node_modules/tough-cookie/dist/index.d.cts
    ./frontend/node_modules/tough-cookie/LICENSE
    ./frontend/node_modules/jsdom/lib/jsdom/living/selection/Selection-impl.js
    ./frontend/node_modules/undici/scripts/strip-comments.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/dist/jsx/xhtml-entities.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/dist/jsx/xhtml-entities.d.ts
    ./frontend/node_modules/@typescript-eslint/typescript-estree/dist/use-at-your-own-risk.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/dist/simple-traverse.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/dist/ast-converter.d.ts
    ./frontend/node_modules/@typescript-eslint/typescript-estree/dist/parser.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/dist/getModifiers.d.ts
    ./frontend/node_modules/@typescript-eslint/typescript-estree/dist/parser.d.ts
    ./frontend/node_modules/@typescript-eslint/typescript-estree/dist/index.d.ts
    ./frontend/node_modules/undici/lib/core/symbols.js
    ./frontend/node_modules/undici/lib/core/socks5-utils.js
    ./frontend/node_modules/undici/lib/core/errors.js
    ./frontend/node_modules/undici/lib/core/socks5-client.js
    ./frontend/node_modules/undici/lib/core/connect.js
    ./frontend/node_modules/undici/lib/core/tree.js
    ./frontend/node_modules/undici/lib/core/request.js
    ./frontend/node_modules/undici/lib/core/util.js
    ./frontend/node_modules/undici/lib/core/diagnostics.js
    ./frontend/node_modules/undici/lib/core/constants.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/svg/SVGPreserveAspectRatio-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/svg/SVGRect-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/svg/SVGAnimatedString-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/svg/SVGListBase.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/svg/SVGAnimatedPreserveAspectRatio-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/svg/SVGStringList-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/svg/SVGNumber-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/svg/SVGAnimatedRect-impl.js
    ./frontend/node_modules/deep-is/.travis.yml
    ./frontend/node_modules/deep-is/package.json
    ./frontend/node_modules/deep-is/README.markdown
    ./frontend/node_modules/deep-is/index.js
    ./frontend/node_modules/undici/docs/docs/best-practices/proxy.md
    ./frontend/node_modules/undici/docs/docs/best-practices/client-certificate.md
    ./frontend/node_modules/undici/docs/docs/best-practices/crawling.md
    ./frontend/node_modules/undici/docs/docs/best-practices/writing-tests.md
    ./frontend/node_modules/undici/docs/docs/best-practices/mocking-request.md
    ./frontend/node_modules/undici/docs/docs/best-practices/undici-vs-builtin-fetch.md
    ./frontend/node_modules/jsdom/lib/jsdom/living/crypto/Crypto-impl.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/dist/semantic-or-syntactic-errors.d.ts
    ./frontend/node_modules/@typescript-eslint/typescript-estree/dist/parser-options.d.ts
    ./frontend/node_modules/@typescript-eslint/typescript-estree/dist/version-check.d.ts
    ./frontend/node_modules/@typescript-eslint/typescript-estree/dist/use-at-your-own-risk.d.ts
    ./frontend/node_modules/@typescript-eslint/typescript-estree/dist/clear-caches.d.ts
    ./frontend/node_modules/@typescript-eslint/typescript-estree/dist/getModifiers.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/dist/parser-options.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/documents.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/dist/semantic-or-syntactic-errors.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/dist/convert-comments.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/dist/check-syntax-errors.d.ts
    ./frontend/node_modules/@typescript-eslint/typescript-estree/dist/ast-converter.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/dist/createParserServices.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/dist/useProgramFromProjectService.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/dist/convert.d.ts
    ./frontend/node_modules/@typescript-eslint/typescript-estree/dist/version.d.ts
    ./frontend/node_modules/@typescript-eslint/typescript-estree/dist/useProgramFromProjectService.d.ts
    ./frontend/node_modules/@typescript-eslint/typescript-estree/dist/convert.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/LICENSE
    ./frontend/node_modules/@typescript-eslint/typescript-estree/dist/withoutProjectParserOptions.d.ts
    ./frontend/node_modules/@typescript-eslint/typescript-estree/dist/source-files.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/dist/tsconfig.build.tsbuildinfo
    ./frontend/node_modules/@typescript-eslint/typescript-estree/dist/version-check.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/dist/check-modifiers.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/dist/version.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/dist/withoutProjectParserOptions.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/dist/check-syntax-errors.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/dist/index.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/dist/source-files.d.ts
    ./frontend/node_modules/@typescript-eslint/typescript-estree/dist/check-modifiers.d.ts
    ./frontend/node_modules/@typescript-eslint/typescript-estree/dist/convert-comments.d.ts
    ./frontend/node_modules/@typescript-eslint/typescript-estree/dist/createParserServices.d.ts
    ./frontend/node_modules/@typescript-eslint/typescript-estree/dist/simple-traverse.d.ts
    ./frontend/node_modules/@typescript-eslint/typescript-estree/dist/node-utils.d.ts
    ./frontend/node_modules/undici/lib/llhttp/llhttp_simd-wasm.js
    ./frontend/node_modules/undici/lib/llhttp/utils.js
    ./frontend/node_modules/undici/lib/llhttp/utils.d.ts
    ./frontend/node_modules/undici/lib/llhttp/llhttp-wasm.js
    ./frontend/node_modules/undici/lib/llhttp/.gitkeep
    ./frontend/node_modules/undici/lib/llhttp/constants.d.ts
    ./frontend/node_modules/undici/lib/llhttp/constants.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/dist/clear-caches.js
    ./frontend/node_modules/jsdom/README.md
    ./frontend/node_modules/jsdom/package.json
    ./frontend/node_modules/undici/docs/docs/api/ContentType.md
    ./frontend/node_modules/undici/docs/docs/api/Client.md
    ./frontend/node_modules/undici/docs/docs/api/api-lifecycle.md
    ./frontend/node_modules/undici/docs/docs/api/Util.md
    ./frontend/node_modules/undici/docs/docs/api/MockClient.md
    ./frontend/node_modules/undici/docs/docs/api/MockCallHistory.md
    ./frontend/node_modules/undici/docs/docs/api/Fetch.md
    ./frontend/node_modules/undici/docs/docs/api/RetryHandler.md
    ./frontend/node_modules/undici/docs/docs/api/Dispatcher.md
    ./frontend/node_modules/undici/docs/docs/api/Cookies.md
    ./frontend/node_modules/undici/docs/docs/api/MockCallHistoryLog.md
    ./frontend/node_modules/undici/docs/docs/api/EventSource.md
    ./frontend/node_modules/undici/docs/docs/api/RetryAgent.md
    ./frontend/node_modules/undici/docs/docs/api/MockPool.md
    ./frontend/node_modules/undici/docs/docs/api/ClientStats.md
    ./frontend/node_modules/undici/docs/docs/api/MockErrors.md
    ./frontend/node_modules/undici/docs/docs/api/GlobalInstallation.md
    ./frontend/node_modules/undici/docs/docs/api/CacheStorage.md
    ./frontend/node_modules/undici/docs/docs/api/Pool.md
    ./frontend/node_modules/undici/docs/docs/api/PoolStats.md
    ./frontend/node_modules/undici/docs/docs/api/Errors.md
    ./frontend/node_modules/undici/docs/docs/api/MockAgent.md
    ./frontend/node_modules/undici/docs/docs/api/WebSocket.md
    ./frontend/node_modules/undici/docs/docs/api/H2CClient.md
    ./frontend/node_modules/undici/docs/docs/api/RedirectHandler.md
    ./frontend/node_modules/undici/docs/docs/api/CacheStore.md
    ./frontend/node_modules/undici/docs/docs/api/DiagnosticsChannel.md
    ./frontend/node_modules/undici/docs/docs/api/RoundRobinPool.md
    ./frontend/node_modules/undici/docs/docs/api/BalancedPool.md
    ./frontend/node_modules/undici/docs/docs/api/SnapshotAgent.md
    ./frontend/node_modules/undici/docs/docs/api/Connector.md
    ./frontend/node_modules/undici/docs/docs/api/ProxyAgent.md
    ./frontend/node_modules/undici/docs/docs/api/Socks5ProxyAgent.md
    ./frontend/node_modules/undici/docs/docs/api/Debug.md
    ./frontend/node_modules/undici/docs/docs/api/EnvHttpProxyAgent.md
    ./frontend/node_modules/undici/docs/docs/api/Agent.md
    ./frontend/node_modules/@typescript-eslint/typescript-estree/dist/ts-estree/estree-to-ts-node-types.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/dist/ts-estree/index.d.ts
    ./frontend/node_modules/@typescript-eslint/typescript-estree/dist/ts-estree/index.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/dist/ts-estree/ts-nodes.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/dist/ts-estree/estree-to-ts-node-types.d.ts
    ./frontend/node_modules/@typescript-eslint/typescript-estree/dist/ts-estree/ts-nodes.d.ts
    ./frontend/node_modules/vite/dist/client/env.mjs
    ./frontend/node_modules/vite/dist/client/client.mjs
    ./frontend/node_modules/jsdom/lib/generated/js-globals.json
    ./frontend/node_modules/jsdom/lib/generated/event-sets.js
    ./frontend/node_modules/jsdom/lib/generated/css-property-descriptors.js
    ./frontend/node_modules/jsdom/lib/generated/css-property-definitions.js
    ./frontend/node_modules/deep-is/example/cmp.js
    ./frontend/node_modules/vite/dist/node/index.d.ts
    ./frontend/node_modules/vite/dist/node/cli.js
    ./frontend/node_modules/vite/dist/node/internal.d.ts
    ./frontend/node_modules/vite/dist/node/module-runner.d.ts
    ./frontend/node_modules/jsdom/lib/jsdom/living/navigator/NavigatorLanguage-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/navigator/MimeTypeArray-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/navigator/NavigatorConcurrentHardware-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/navigator/NavigatorCookies-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/navigator/PluginArray-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/navigator/MimeType-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/navigator/NavigatorID-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/navigator/NavigatorOnLine-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/navigator/Navigator-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/navigator/Plugin-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/navigator/NavigatorPlugins-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/constraint-validation/ValidityState-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/constraint-validation/DefaultConstraintValidation-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/HTMLTableColElement-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/ShadowRoot-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/HTMLInputElement-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/SVGTests-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/HTMLSelectElement-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/HTMLTimeElement-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/CharacterData-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/HTMLUnknownElement-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/HTMLFieldSetElement-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/HTMLSlotElement-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/HTMLOutputElement-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/HTMLBRElement-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/HTMLTemplateElement-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/HTMLTableCellElement-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/NonElementParentNode-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/HTMLFontElement-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/HTMLEmbedElement-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/DocumentType-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/HTMLProgressElement-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/DOMImplementation-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/HTMLMapElement-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/GlobalEventHandlers-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/ElementContentEditable-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/Element-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/SVGSymbolElement-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/HTMLPreElement-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/ParentNode-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/SVGMetadataElement-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/HTMLDirectoryElement-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/HTMLMetaElement-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/DOMTokenList-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/HTMLOptionElement-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/RadioNodeList-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/HTMLScriptElement-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/HTMLModElement-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/LinkStyle-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/HTMLCanvasElement-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/HTMLUListElement-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/SVGSVGElement-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/HTMLTitleElement-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/HTMLAnchorElement-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/HTMLOListElement-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/HTMLBodyElement-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/HTMLParamElement-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/HTMLDetailsElement-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/HTMLDialogElement-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/SVGGraphicsElement-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/HTMLHeadElement-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/Node-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/HTMLQuoteElement-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/SVGGElement-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/SVGSwitchElement-impl.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/dist/create-program/createSourceFile.d.ts
    ./frontend/node_modules/@typescript-eslint/typescript-estree/dist/create-program/shared.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/dist/create-program/describeFilePath.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/HTMLParagraphElement-impl.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/dist/create-program/createProjectProgramError.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/dist/create-program/useProvidedPrograms.d.ts
    ./frontend/node_modules/@typescript-eslint/typescript-estree/dist/create-program/getScriptKind.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/dist/create-program/createSourceFile.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/dist/create-program/shared.d.ts
    ./frontend/node_modules/@typescript-eslint/typescript-estree/dist/create-program/createProjectProgram.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/dist/create-program/getWatchProgramsForProjects.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/dist/create-program/WatchCompilerHostOfConfigFile.d.ts
    ./frontend/node_modules/@typescript-eslint/typescript-estree/dist/create-program/createIsolatedProgram.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/dist/create-program/createIsolatedProgram.d.ts
    ./frontend/node_modules/@typescript-eslint/typescript-estree/dist/create-program/WatchCompilerHostOfConfigFile.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/dist/create-program/useProvidedPrograms.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/HTMLLabelElement-impl.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/dist/create-program/createProjectProgramError.d.ts
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/Slotable-impl.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/dist/create-program/createProjectProgram.d.ts
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/SVGDescElement-impl.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/dist/create-program/describeFilePath.d.ts
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/HTMLElement-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/HTMLVideoElement-impl.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/dist/create-program/getWatchProgramsForProjects.d.ts
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/HTMLTableCaptionElement-impl.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/dist/create-program/validateDefaultProjectForFilesGlob.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/HTMLTextAreaElement-impl.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/dist/create-program/validateDefaultProjectForFilesGlob.d.ts
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/WindowEventHandlers-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/mutation-observer/MutationRecord-impl.js
    ./frontend/node_modules/@typescript-eslint/typescript-estree/dist/create-program/getScriptKind.d.ts
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/HTMLSpanElement-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/mutation-observer/MutationObserver-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/HTMLAreaElement-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/HTMLMeterElement-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/HTMLLIElement-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/HTMLTableSectionElement-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/HTMLPictureElement-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/Comment-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/Document-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/HTMLOptionsCollection-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/HTMLAudioElement-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/SVGElement-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/HTMLDivElement-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/HTMLMarqueeElement-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/DocumentFragment-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/HTMLHeadingElement-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/XMLDocument-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/HTMLTableElement-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/SVGTitleElement-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/ProcessingInstruction-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/HTMLButtonElement-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/HTMLDataListElement-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/HTMLHtmlElement-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/HTMLLinkElement-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/HTMLFormControlsCollection-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/HTMLHyperlinkElementUtils-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/HTMLSourceElement-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/HTMLMediaElement-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/SVGDefsElement-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/HTMLTableRowElement-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/NonDocumentTypeChildNode-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/HTMLStyleElement-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/node.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/HTMLDListElement-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/HTMLOrSVGElement-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/NodeList-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/DocumentOrShadowRoot-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/HTMLFrameElement-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/HTMLIFrameElement-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/HTMLFrameSetElement-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/HTMLOptGroupElement-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/HTMLImageElement-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/HTMLMenuElement-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/HTMLTrackElement-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/HTMLFormElement-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/HTMLLegendElement-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/DOMStringMap-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/Text-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/HTMLBaseElement-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/HTMLObjectElement-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/HTMLHRElement-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/HTMLCollection-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/CDATASection-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/ChildNode-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/nodes/HTMLDataElement-impl.js
    ./frontend/node_modules/vite/dist/node/chunks/optimizer.js
    ./frontend/node_modules/vite/dist/node/chunks/dist.js
    ./frontend/node_modules/vite/dist/node/chunks/moduleRunnerTransport.d.ts
    ./frontend/node_modules/vite/dist/node/chunks/node.js
    ./frontend/node_modules/vite/dist/node/chunks/config.js
    ./frontend/node_modules/vite/dist/node/chunks/build2.js
    ./frontend/node_modules/vite/dist/node/chunks/lib.js
    ./frontend/node_modules/vite/dist/node/chunks/build.js
    ./frontend/node_modules/vite/dist/node/chunks/preview.js
    ./frontend/node_modules/vite/dist/node/chunks/postcss-import.js
    ./frontend/node_modules/vite/dist/node/chunks/server.js
    ./frontend/node_modules/vite/dist/node/chunks/logger.js
    ./frontend/node_modules/vite/dist/node/chunks/chunk.js
    ./frontend/node_modules/vite/dist/node/index.js
    ./frontend/node_modules/vite/dist/node/internal.js
    ./frontend/node_modules/vite/dist/node/module-runner.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/attributes/NamedNodeMap-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/attributes/Attr-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/node-document-position.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/css/CSSRule-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/css/helpers/stylesheets.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/css/helpers/css-parser.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/css/helpers/computed-style.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/css/helpers/colors.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/css/helpers/patched-csstree.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/css/helpers/generic-property-descriptor.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/css/helpers/css-values.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/css/helpers/shorthand-properties.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/css/helpers/system-colors.js
    ./frontend/node_modules/vite/bin/vite.js
    ./frontend/node_modules/vite/bin/openChrome.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/css/CSSStyleSheet-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/css/CSSNestedDeclarations-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/css/ElementCSSInlineStyle-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/css/CSSContainerRule-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/css/CSSLayerStatementRule-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/css/CSSStyleDeclaration-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/aborting/AbortController-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/aborting/AbortSignal-impl.js
    ./frontend/node_modules/deep-is/test/cmp.js
    ./frontend/node_modules/deep-is/test/NaN.js
    ./frontend/node_modules/deep-is/test/neg-vs-pos-0.js
    ./frontend/node_modules/deep-is/LICENSE
    ./frontend/node_modules/jsdom/lib/jsdom/living/hr-time/Performance-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/css/CSSLayerBlockRule-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/css/CSSStyleProperties-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/css/CSSGroupingRule-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/css/CSSKeyframeRule-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/css/CSSNamespaceRule-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/css/CSSConditionRule-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/css/CSSFontFaceRule-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/css/CSSPageRule-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/css/StyleSheet-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/css/CSSScopeRule-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/css/CSSImportRule-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/css/MediaList-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/css/CSSStyleRule-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/css/CSSCounterStyleRule-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/css/CSSSupportsRule-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/css/CSSKeyframesRule-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/css/StyleSheetList-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/css/CSSRuleList-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/css/CSSMediaRule-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/deviceorientation/DeviceMotionEventAcceleration-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/deviceorientation/DeviceMotionEventRotationRate-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/window/History-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/window/Location-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/window/navigation.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/window/SessionHistory.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/window/BarProp-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/window/Screen-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/window/External-impl.js
    ./frontend/node_modules/.package-lock.json
    ./frontend/node_modules/jsdom/lib/jsdom/living/traversal/TreeWalker-impl.js
    ./frontend/node_modules/vite/types/import-meta.d.ts
    ./frontend/node_modules/vite/types/importMeta.d.ts
    ./frontend/node_modules/vite/types/importGlob.d.ts
    ./frontend/node_modules/vite/types/customEvent.d.ts
    ./frontend/node_modules/vite/types/metadata.d.ts
    ./frontend/node_modules/vite/types/hot.d.ts
    ./frontend/node_modules/jsdom/lib/jsdom/living/traversal/helpers.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/traversal/NodeIterator-impl.js
    ./frontend/node_modules/vite/LICENSE.md
    ./frontend/node_modules/vite/types/hmrPayload.d.ts
    ./frontend/node_modules/jsdom/lib/jsdom/living/fetch/Headers-impl.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/fetch/header-utils.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/fetch/header-types.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/fetch/header-list.js
    ./frontend/node_modules/json-buffer/.travis.yml
    ./frontend/node_modules/json-buffer/package.json
    ./frontend/node_modules/json-buffer/README.md
    ./frontend/node_modules/json-buffer/index.js
    ./frontend/node_modules/picocolors/picocolors.d.ts
    ./frontend/node_modules/picocolors/picocolors.browser.js
    ./frontend/node_modules/picocolors/package.json
    ./frontend/node_modules/picocolors/README.md
    ./frontend/node_modules/picocolors/picocolors.js
    ./frontend/node_modules/picocolors/types.d.ts
    ./frontend/node_modules/picocolors/LICENSE
    ./frontend/node_modules/vite/misc/false.js
    ./frontend/node_modules/vite/misc/true.js
    ./frontend/node_modules/@oxc-project/types/package.json
    ./frontend/node_modules/@oxc-project/types/README.md
    ./frontend/node_modules/@oxc-project/types/types.d.ts
    ./frontend/node_modules/@oxc-project/types/LICENSE
    ./frontend/node_modules/vite/types/internal/esbuildOptions.d.ts
    ./frontend/node_modules/vite/types/internal/terserOptions.d.ts
    ./frontend/node_modules/vite/types/internal/cssPreprocessorOptions.d.ts
    ./frontend/node_modules/vite/types/internal/lightningcssOptions.d.ts
    ./frontend/node_modules/vite/types/internal/rollupTypeCompat.d.ts
    ./frontend/node_modules/expect-type/SECURITY.md
    ./frontend/node_modules/expect-type/package.json
    ./frontend/node_modules/expect-type/README.md
    ./frontend/node_modules/json-buffer/test/index.js
    ./frontend/node_modules/json-buffer/LICENSE
    ./frontend/node_modules/semver/range.bnf
    ./frontend/node_modules/semver/package.json
    ./frontend/node_modules/semver/README.md
    ./frontend/node_modules/semver/semver.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/css/properties/fontSize.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/css/properties/width.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/css/properties/fontStyle.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/css/properties/opacity.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/css/properties/flexBasis.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/css/properties/borderBlockStartColor.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/css/properties/backgroundOrigin.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/css/properties/backgroundClip.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/css/properties/outlineColor.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/css/properties/marginLeft.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/css/properties/borderCollapse.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/css/properties/borderRight.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/css/properties/borderInlineEndColor.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/css/properties/borderBottomStyle.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/css/properties/backgroundColor.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/css/properties/lineHeight.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/css/properties/floodColor.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/css/properties/paddingLeft.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/css/properties/borderBottomColor.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/css/properties/fontWeight.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/css/properties/marginBottom.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/css/properties/border.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/css/properties/padding.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/css/properties/webkitTextFillColor.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/css/properties/backgroundRepeat.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/css/properties/borderBottom.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/css/properties/borderRightStyle.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/css/properties/paddingRight.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/css/properties/borderSpacing.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/css/properties/borderColor.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/css/properties/lightingColor.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/css/properties/paddingTop.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/css/properties/borderRightColor.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/css/properties/clip.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/css/properties/borderLeftWidth.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/css/properties/borderTop.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/css/properties/flex.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/css/properties/borderStyle.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/css/properties/borderTopWidth.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/css/properties/borderLeft.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/css/properties/color.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/css/properties/left.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/css/properties/clear.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/css/properties/height.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/css/properties/textEmphasisColor.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/css/properties/webkitTextStrokeColor.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/css/properties/borderBottomWidth.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/css/properties/backgroundSize.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/css/properties/backgroundAttachment.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/css/properties/stopColor.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/css/properties/background.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/css/properties/flexShrink.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/css/properties/right.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/css/properties/fontVariant.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/css/properties/top.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/css/properties/font.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/css/properties/paddingBottom.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/css/properties/marginTop.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/css/properties/display.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/css/properties/margin.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/css/properties/borderTopStyle.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/css/properties/backgroundPosition.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/css/properties/borderWidth.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/css/properties/float.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/css/properties/borderLeftStyle.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/css/properties/bottom.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/css/properties/borderBlockEndColor.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/css/properties/fontFamily.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/css/properties/borderTopColor.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/css/properties/marginRight.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/css/properties/flexGrow.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/css/properties/backgroundImage.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/css/properties/borderLeftColor.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/css/properties/borderRightWidth.js
    ./frontend/node_modules/jsdom/lib/jsdom/living/css/properties/borderInlineStartColor.js
    ./frontend/node_modules/stackback/.travis.yml
    ./frontend/node_modules/jsdom/lib/jsdom/living/webidl/DOMException-impl.js
    ./frontend/node_modules/stackback/package.json
    ./frontend/node_modules/stackback/README.md
    ./frontend/node_modules/stackback/index.js
    ./frontend/node_modules/stackback/test.js
    ./frontend/node_modules/stackback/formatstack.js
    ./frontend/node_modules/stackback/.npmignore
    ./frontend/node_modules/yocto-queue/index.d.ts
    ./frontend/node_modules/yocto-queue/package.json
    ./frontend/node_modules/yocto-queue/readme.md
    ./frontend/node_modules/yocto-queue/index.js
    ./frontend/node_modules/yocto-queue/license
    ./frontend/node_modules/semver/LICENSE
    ./frontend/node_modules/expect-type/dist/messages.js
    ./frontend/node_modules/expect-type/dist/overloads.js
    ./frontend/node_modules/expect-type/dist/index.d.ts
    ./frontend/node_modules/expect-type/dist/utils.js
    ./frontend/node_modules/expect-type/dist/utils.d.ts
    ./frontend/node_modules/expect-type/dist/overloads.d.ts
    ./frontend/node_modules/expect-type/dist/index.js
    ./frontend/node_modules/expect-type/dist/branding.js
    ./frontend/node_modules/expect-type/dist/messages.d.ts
    ./frontend/node_modules/expect-type/dist/branding.d.ts
    ./frontend/node_modules/expect-type/LICENSE
    ./frontend/node_modules/data-urls/LICENSE.txt
    ./frontend/node_modules/caniuse-lite/data/browsers.js
    ./frontend/node_modules/caniuse-lite/data/browserVersions.js
    ./frontend/node_modules/eslint/conf/rule-type-list.json
    ./frontend/node_modules/eslint/conf/default-cli-options.js
    ./frontend/node_modules/eslint/conf/replacements.json
    ./frontend/node_modules/eslint/conf/ecma-version.js
    ./frontend/node_modules/eslint/conf/globals.js
    ./frontend/node_modules/semver/bin/semver.js
    ./frontend/node_modules/data-urls/README.md
    ./frontend/node_modules/data-urls/package.json
    ./frontend/node_modules/yallist/iterator.js
    ./frontend/node_modules/yallist/package.json
    ./frontend/node_modules/yallist/README.md
    ./frontend/node_modules/yallist/LICENSE
    ./frontend/node_modules/yallist/yallist.js
    ./frontend/node_modules/data-urls/lib/parser.js
    ./frontend/node_modules/data-urls/lib/utils.js
    ./frontend/node_modules/levn/README.md
    ./frontend/node_modules/levn/LICENSE
    ./frontend/node_modules/levn/package.json
    ./frontend/node_modules/jsdom/lib/generated/idl/HTMLStyleElement.js
    ./frontend/node_modules/jsdom/lib/generated/idl/CSSContainerRule.js
    ./frontend/node_modules/jsdom/lib/generated/idl/HTMLDataElement.js
    ./frontend/node_modules/jsdom/lib/generated/idl/CSSRule.js
    ./frontend/node_modules/jsdom/lib/generated/idl/HTMLQuoteElement.js
    ./frontend/node_modules/jsdom/lib/generated/idl/MutationObserver.js
    ./frontend/node_modules/jsdom/lib/generated/idl/MutationCallback.js
    ./frontend/node_modules/jsdom/lib/generated/idl/FilePropertyBag.js
    ./frontend/node_modules/jsdom/lib/generated/idl/HTMLMarqueeElement.js
    ./frontend/node_modules/jsdom/lib/generated/idl/EventTarget.js
    ./frontend/node_modules/jsdom/lib/generated/idl/SVGSVGElement.js
    ./frontend/node_modules/jsdom/lib/generated/idl/ScrollBehavior.js
    ./frontend/node_modules/jsdom/lib/generated/idl/CSSNamespaceRule.js
    ./frontend/node_modules/jsdom/lib/generated/idl/Range.js
    ./frontend/node_modules/jsdom/lib/generated/idl/CSSKeyframeRule.js
    ./frontend/node_modules/jsdom/lib/generated/idl/XMLHttpRequestResponseType.js
    ./frontend/node_modules/jsdom/lib/generated/idl/ElementDefinitionOptions.js
    ./frontend/node_modules/jsdom/lib/generated/idl/HTMLLIElement.js
    ./frontend/node_modules/jsdom/lib/generated/idl/OnErrorEventHandlerNonNull.js
    ./frontend/node_modules/jsdom/lib/generated/idl/SVGDescElement.js
    ./frontend/node_modules/jsdom/lib/generated/idl/AbortController.js
    ./frontend/node_modules/jsdom/lib/generated/idl/DeviceMotionEventAccelerationInit.js
    ./frontend/node_modules/jsdom/lib/generated/idl/SupportedType.js
    ./frontend/node_modules/jsdom/lib/generated/idl/XMLHttpRequest.js
    ./frontend/node_modules/jsdom/lib/generated/idl/MimeTypeArray.js
    ./frontend/node_modules/jsdom/lib/generated/idl/UIEventInit.js
    ./frontend/node_modules/jsdom/lib/generated/idl/HTMLParagraphElement.js
    ./frontend/node_modules/jsdom/lib/generated/idl/HTMLTableCaptionElement.js
    ./frontend/node_modules/jsdom/lib/generated/idl/MimeType.js
    ./frontend/node_modules/jsdom/lib/generated/idl/HTMLVideoElement.js
    ./frontend/node_modules/jsdom/lib/generated/idl/HTMLPreElement.js
    ./frontend/node_modules/jsdom/lib/generated/idl/CompositionEventInit.js
    ./frontend/node_modules/jsdom/lib/generated/idl/SVGMetadataElement.js
    ./frontend/node_modules/jsdom/lib/generated/idl/HTMLSourceElement.js
    ./frontend/node_modules/jsdom/lib/generated/idl/AddEventListenerOptions.js
    ./frontend/node_modules/jsdom/lib/generated/idl/SVGGElement.js
    ./frontend/node_modules/jsdom/lib/generated/idl/HTMLOListElement.js
    ./frontend/node_modules/jsdom/lib/generated/idl/MessageEventInit.js
    ./frontend/node_modules/jsdom/lib/generated/idl/HTMLCanvasElement.js
    ./frontend/node_modules/jsdom/lib/generated/idl/DeviceOrientationEventInit.js
    ./frontend/node_modules/jsdom/lib/generated/idl/DeviceMotionEventRotationRate.js
    ./frontend/node_modules/jsdom/lib/generated/idl/ScrollRestoration.js
    ./frontend/node_modules/jsdom/lib/generated/idl/HTMLFieldSetElement.js
    ./frontend/node_modules/jsdom/lib/generated/idl/EndingType.js
    ./frontend/node_modules/jsdom/lib/generated/idl/NodeFilter.js
    ./frontend/node_modules/jsdom/lib/generated/idl/BlobEventInit.js
    ./frontend/node_modules/jsdom/lib/generated/idl/DeviceMotionEvent.js
    ./frontend/node_modules/jsdom/lib/generated/idl/XMLDocument.js
    ./frontend/node_modules/jsdom/lib/generated/idl/StyleSheetList.js
    ./frontend/node_modules/jsdom/lib/generated/idl/HTMLHeadingElement.js
    ./frontend/node_modules/jsdom/lib/generated/idl/CSSStyleDeclaration.js
    ./frontend/node_modules/jsdom/lib/generated/idl/UIEvent.js
    ./frontend/node_modules/jsdom/lib/generated/idl/ElementCreationOptions.js
    ./frontend/node_modules/jsdom/lib/generated/idl/SVGDefsElement.js
    ./frontend/node_modules/jsdom/lib/generated/idl/HTMLOutputElement.js
    ./frontend/node_modules/jsdom/lib/generated/idl/HTMLDirectoryElement.js
    ./frontend/node_modules/jsdom/lib/generated/idl/HTMLOptionsCollection.js
    ./frontend/node_modules/jsdom/lib/generated/idl/WheelEventInit.js
    ./frontend/node_modules/jsdom/lib/generated/idl/HTMLSpanElement.js
    ./frontend/node_modules/jsdom/lib/generated/idl/ErrorEvent.js
    ./frontend/node_modules/jsdom/lib/generated/idl/HTMLBRElement.js
    ./frontend/node_modules/jsdom/lib/generated/idl/HTMLMetaElement.js
    ./frontend/node_modules/jsdom/lib/generated/idl/Element.js
    ./frontend/node_modules/jsdom/lib/generated/idl/HTMLParamElement.js
    ./frontend/node_modules/jsdom/lib/generated/idl/HTMLHRElement.js
    ./frontend/node_modules/jsdom/lib/generated/idl/SVGNumber.js
    ./frontend/node_modules/jsdom/lib/generated/idl/HTMLPictureElement.js
    ./frontend/node_modules/jsdom/lib/generated/idl/HTMLCollection.js
    ./frontend/node_modules/jsdom/lib/generated/idl/DeviceMotionEventInit.js
    ./frontend/node_modules/jsdom/lib/generated/idl/SVGPreserveAspectRatio.js
    ./frontend/node_modules/jsdom/lib/generated/idl/CSSStyleSheet.js
    ./frontend/node_modules/jsdom/lib/generated/idl/PointerEvent.js
    ./frontend/node_modules/jsdom/lib/generated/idl/PromiseRejectionEventInit.js
    ./frontend/node_modules/jsdom/lib/generated/idl/Event.js
    ./frontend/node_modules/jsdom/lib/generated/idl/ElementInternals.js
    ./frontend/node_modules/jsdom/lib/generated/idl/BinaryType.js
    ./frontend/node_modules/jsdom/lib/generated/idl/HTMLBodyElement.js
    ./frontend/node_modules/jsdom/lib/generated/idl/HTMLSlotElement.js
    ./frontend/node_modules/jsdom/lib/generated/idl/StorageEventInit.js
    ./frontend/node_modules/jsdom/lib/generated/idl/CSSImportRule.js
    ./frontend/node_modules/jsdom/lib/generated/idl/CSSLayerStatementRule.js
    ./frontend/node_modules/jsdom/lib/generated/idl/CSSStyleRule.js
    ./frontend/node_modules/jsdom/lib/generated/idl/CustomElementConstructor.js
    ./frontend/node_modules/jsdom/lib/generated/idl/StaticRangeInit.js
    ./frontend/node_modules/jsdom/lib/generated/idl/PageTransitionEventInit.js
    ./frontend/node_modules/jsdom/lib/generated/idl/HTMLHtmlElement.js
    ./frontend/node_modules/jsdom/lib/generated/idl/MutationRecord.js
    ./frontend/node_modules/jsdom/lib/generated/idl/OnBeforeUnloadEventHandlerNonNull.js
    ./frontend/node_modules/jsdom/lib/generated/idl/HTMLFrameElement.js
    ./frontend/node_modules/jsdom/lib/generated/idl/HTMLTrackElement.js
    ./frontend/node_modules/jsdom/lib/generated/idl/FileList.js
    ./frontend/node_modules/jsdom/lib/generated/idl/EventInit.js
    ./frontend/node_modules/jsdom/lib/generated/idl/HTMLMediaElement.js
    ./frontend/node_modules/jsdom/lib/generated/idl/KeyboardEvent.js
    ./frontend/node_modules/jsdom/lib/generated/idl/XMLSerializer.js
    ./frontend/node_modules/jsdom/lib/generated/idl/SVGAnimatedString.js
    ./frontend/node_modules/jsdom/lib/generated/idl/DeviceMotionEventAcceleration.js
    ./frontend/node_modules/jsdom/lib/generated/idl/EventModifierInit.js
    ./frontend/node_modules/jsdom/lib/generated/idl/CSSScopeRule.js
    ./frontend/node_modules/jsdom/lib/generated/idl/DOMRectReadOnly.js
    ./frontend/node_modules/jsdom/lib/generated/idl/AbortSignal.js
    ./frontend/node_modules/jsdom/lib/generated/idl/TreeWalker.js
    ./frontend/node_modules/levn/lib/index.js
    ./frontend/node_modules/levn/lib/cast.js
    ./frontend/node_modules/levn/lib/parse-string.js
    ./frontend/node_modules/jsdom/lib/generated/idl/HashChangeEvent.js
    ./frontend/node_modules/jsdom/lib/generated/idl/HTMLSelectElement.js
    ./frontend/node_modules/jsdom/lib/generated/idl/HTMLElement.js
    ./frontend/node_modules/jsdom/lib/generated/idl/CSSStyleProperties.js
    ./frontend/node_modules/jsdom/lib/generated/idl/BeforeUnloadEvent.js
    ./frontend/node_modules/jsdom/lib/generated/idl/TextDecoderOptions.js
    ./frontend/node_modules/jsdom/lib/generated/idl/PromiseRejectionEvent.js
    ./frontend/node_modules/jsdom/lib/generated/idl/ScrollIntoViewOptions.js
    ./frontend/node_modules/jsdom/lib/generated/idl/HTMLTitleElement.js
    ./frontend/node_modules/jsdom/lib/generated/idl/CloseEvent.js
    ./frontend/node_modules/jsdom/lib/generated/idl/HTMLEmbedElement.js
    ./frontend/node_modules/jsdom/lib/generated/idl/PopStateEventInit.js
    ./frontend/node_modules/jsdom/lib/generated/idl/HTMLTableSectionElement.js
    ./frontend/node_modules/jsdom/lib/generated/idl/CSSStyleSheetInit.js
    ./frontend/node_modules/jsdom/lib/generated/idl/MouseEventInit.js
    ./frontend/node_modules/jsdom/lib/generated/idl/HTMLModElement.js
    ./frontend/node_modules/jsdom/lib/generated/idl/SVGGraphicsElement.js
    ./frontend/node_modules/jsdom/lib/generated/idl/CSSGroupingRule.js
    ./frontend/node_modules/jsdom/lib/generated/idl/RadioNodeList.js
    ./frontend/node_modules/jsdom/lib/generated/idl/HTMLDetailsElement.js
    ./frontend/node_modules/jsdom/lib/generated/idl/HTMLLegendElement.js
    ./frontend/node_modules/jsdom/lib/generated/idl/SVGSymbolElement.js
    ./frontend/node_modules/jsdom/lib/generated/idl/KeyboardEventInit.js
    ./frontend/node_modules/jsdom/lib/generated/idl/Screen.js
    ./frontend/node_modules/jsdom/lib/generated/idl/ProgressEventInit.js
    ./frontend/node_modules/jsdom/lib/generated/idl/DOMParser.js
    ./frontend/node_modules/jsdom/lib/generated/idl/ScrollLogicalPosition.js
    ./frontend/node_modules/jsdom/lib/generated/idl/ShadowRootMode.js
    ./frontend/node_modules/jsdom/lib/generated/idl/DOMTokenList.js
    ./frontend/node_modules/jsdom/lib/generated/idl/CSSSupportsRule.js
    ./frontend/node_modules/jsdom/lib/generated/idl/StyleSheet.js
    ./frontend/node_modules/jsdom/lib/generated/idl/MessageEvent.js
    ./frontend/node_modules/jsdom/lib/generated/idl/External.js
    ./frontend/node_modules/jsdom/lib/generated/idl/HTMLAreaElement.js
    ./frontend/node_modules/jsdom/lib/generated/idl/CanPlayTypeResult.js
    ./frontend/node_modules/jsdom/lib/generated/idl/TextTrackKind.js
    ./frontend/node_modules/jsdom/lib/generated/idl/HTMLOptGroupElement.js
    ./frontend/node_modules/jsdom/lib/generated/idl/MutationObserverInit.js
    ./frontend/node_modules/jsdom/lib/generated/idl/Comment.js
    ./frontend/node_modules/jsdom/lib/generated/idl/StorageEvent.js
    ./frontend/node_modules/jsdom/lib/generated/idl/HTMLIFrameElement.js
    ./frontend/node_modules/jsdom/lib/generated/idl/EventHandlerNonNull.js
    ./frontend/node_modules/jsdom/lib/generated/idl/Performance.js
    ./frontend/node_modules/jsdom/lib/generated/idl/HTMLOptionElement.js
    ./frontend/node_modules/jsdom/lib/generated/idl/InputEvent.js
    ./frontend/node_modules/jsdom/lib/generated/idl/HTMLTemplateElement.js
    ./frontend/node_modules/jsdom/lib/generated/idl/StaticRange.js
    ./frontend/node_modules/jsdom/lib/generated/idl/PageTransitionEvent.js
    ./frontend/node_modules/jsdom/lib/generated/idl/PointerEventInit.js
    ./frontend/node_modules/jsdom/lib/generated/idl/HTMLFontElement.js
    ./frontend/node_modules/jsdom/lib/generated/idl/Headers.js
    ./frontend/node_modules/jsdom/lib/generated/idl/TextEncoder.js
    ./frontend/node_modules/jsdom/lib/generated/idl/HTMLFormControlsCollection.js
    ./frontend/node_modules/jsdom/lib/generated/idl/TouchEvent.js
    ./frontend/node_modules/jsdom/lib/generated/idl/CSSRuleList.js
    ./frontend/node_modules/jsdom/lib/generated/idl/HTMLTableRowElement.js
    ./frontend/node_modules/jsdom/lib/generated/idl/HTMLFormElement.js
    ./frontend/node_modules/jsdom/lib/generated/idl/Node.js
    ./frontend/node_modules/jsdom/lib/generated/idl/CharacterData.js
    ./frontend/node_modules/jsdom/lib/generated/idl/HTMLDialogElement.js
    ./frontend/node_modules/update-browserslist-db/index.js
    ./frontend/node_modules/update-browserslist-db/LICENSE
    ./frontend/node_modules/update-browserslist-db/check-npm-version.js
    ./frontend/node_modules/update-browserslist-db/index.d.ts
    ./frontend/node_modules/update-browserslist-db/utils.js
    ./frontend/node_modules/update-browserslist-db/cli.js
    ./frontend/node_modules/update-browserslist-db/package.json
    ./frontend/node_modules/update-browserslist-db/README.md
    ./frontend/node_modules/cross-spawn/lib/enoent.js
    ./frontend/node_modules/cross-spawn/lib/parse.js
    ./frontend/node_modules/whatwg-mimetype/LICENSE.txt
    ./frontend/node_modules/mdn-data/api/inheritance.json
    ./frontend/node_modules/mdn-data/api/index.js
    ./frontend/node_modules/mdn-data/api/inheritance.schema.json
    ./frontend/node_modules/mdn-data/package.json
    ./frontend/node_modules/mdn-data/README.md
    ./frontend/node_modules/mdn-data/index.js
    ./frontend/node_modules/@testing-library/jest-dom/jest-globals.d.ts
    ./frontend/node_modules/json5/lib/index.d.ts
    ./frontend/node_modules/@testing-library/jest-dom/jest-globals.js
    ./frontend/node_modules/@testing-library/jest-dom/matchers.js
    ./frontend/node_modules/@testing-library/jest-dom/package.json
    ./frontend/node_modules/@testing-library/jest-dom/README.md
    ./frontend/node_modules/@testing-library/jest-dom/matchers.d.ts
    ./frontend/node_modules/json5/lib/util.d.ts
    ./frontend/node_modules/json5/lib/cli.js
    ./frontend/node_modules/json5/lib/parse.js
    ./frontend/node_modules/json5/lib/require.js
    ./frontend/node_modules/json5/lib/stringify.d.ts
    ./frontend/node_modules/json5/lib/unicode.d.ts
    ./frontend/node_modules/json5/lib/register.js
    ./frontend/node_modules/json5/lib/index.js
    ./frontend/node_modules/json5/lib/unicode.js
    ./frontend/node_modules/json5/lib/parse.d.ts
    ./frontend/node_modules/json5/lib/util.js
    ./frontend/node_modules/json5/lib/stringify.js
    ./frontend/node_modules/json5/package.json
    ./frontend/node_modules/json5/README.md
    ./frontend/node_modules/@humanfs/node/src/index.js
    ./frontend/node_modules/@humanfs/node/src/node-hfs.js
    ./frontend/node_modules/@humanfs/node/package.json
    ./frontend/node_modules/@humanfs/node/README.md
    ./frontend/node_modules/jsdom/lib/generated/idl/TextDecodeOptions.js
    ./frontend/node_modules/jsdom/lib/generated/idl/SVGStringList.js
    ./frontend/node_modules/jsdom/lib/generated/idl/DeviceMotionEventRotationRateInit.js
    ./frontend/node_modules/jsdom/lib/generated/idl/FocusEventInit.js
    ./frontend/node_modules/jsdom/lib/generated/idl/NodeIterator.js
    ./frontend/node_modules/jsdom/lib/generated/idl/Storage.js
    ./frontend/node_modules/jsdom/lib/generated/idl/FormData.js
    ./frontend/node_modules/jsdom/lib/generated/idl/Document.js
    ./frontend/node_modules/jsdom/lib/generated/idl/PopStateEvent.js
    ./frontend/node_modules/jsdom/lib/generated/idl/VoidFunction.js
    ./frontend/node_modules/jsdom/lib/generated/idl/HTMLMenuElement.js
    ./frontend/node_modules/jsdom/lib/generated/idl/SVGRect.js
    ./frontend/node_modules/jsdom/lib/generated/idl/HTMLTableElement.js
    ./frontend/node_modules/jsdom/lib/generated/idl/Text.js
    ./frontend/node_modules/jsdom/lib/generated/idl/HTMLTextAreaElement.js
    ./frontend/node_modules/jsdom/lib/generated/idl/MouseEvent.js
    ./frontend/node_modules/jsdom/lib/generated/idl/CustomEventInit.js
    ./frontend/node_modules/jsdom/lib/generated/idl/CSSFontFaceRule.js
    ./frontend/node_modules/jsdom/lib/generated/idl/DOMException.js
    ./frontend/node_modules/jsdom/lib/generated/idl/CSSMediaRule.js
    ./frontend/node_modules/jsdom/lib/generated/idl/Plugin.js
    ./frontend/node_modules/jsdom/lib/generated/idl/CSSPageRule.js
    ./frontend/node_modules/jsdom/lib/generated/idl/HTMLBaseElement.js
    ./frontend/node_modules/jsdom/lib/generated/idl/TransitionEventInit.js
    ./frontend/node_modules/jsdom/lib/generated/idl/HTMLTimeElement.js
    ./frontend/node_modules/jsdom/lib/generated/idl/CustomElementRegistry.js
    ./frontend/node_modules/jsdom/lib/generated/idl/DocumentFragment.js
    ./frontend/node_modules/jsdom/lib/generated/idl/DeviceOrientationEvent.js
    ./frontend/node_modules/jsdom/lib/generated/idl/EventListenerOptions.js
    ./frontend/node_modules/jsdom/lib/generated/idl/SVGBoundingBoxOptions.js
    ./frontend/node_modules/jsdom/lib/generated/idl/NodeList.js
    ./frontend/node_modules/jsdom/lib/generated/idl/InputEventInit.js
    ./frontend/node_modules/jsdom/lib/generated/idl/HTMLHeadElement.js
    ./frontend/node_modules/jsdom/lib/generated/idl/TextDecoder.js
    ./frontend/node_modules/jsdom/lib/generated/idl/CloseEventInit.js
    ./frontend/node_modules/jsdom/lib/generated/idl/HTMLMapElement.js
    ./frontend/node_modules/jsdom/lib/generated/idl/ScrollOptions.js
    ./frontend/node_modules/jsdom/lib/generated/idl/DOMRect.js
    ./frontend/node_modules/jsdom/lib/generated/idl/HTMLFrameSetElement.js
    ./frontend/node_modules/jsdom/lib/generated/idl/AbstractRange.js
    ./frontend/node_modules/jsdom/lib/generated/idl/ProcessingInstruction.js
    ./frontend/node_modules/jsdom/lib/generated/idl/SVGSwitchElement.js
    ./frontend/node_modules/jsdom/lib/generated/idl/BlobEvent.js
    ./frontend/node_modules/jsdom/lib/generated/idl/Location.js
    ./frontend/node_modules/jsdom/lib/generated/idl/ShadowRootInit.js
    ./frontend/node_modules/jsdom/lib/generated/idl/SVGAnimatedRect.js
    ./frontend/node_modules/jsdom/lib/generated/idl/HTMLDataListElement.js
    ./frontend/node_modules/jsdom/lib/generated/idl/CSSConditionRule.js
    ./frontend/node_modules/jsdom/lib/generated/idl/GetRootNodeOptions.js
    ./frontend/node_modules/jsdom/lib/generated/idl/HTMLProgressElement.js
    ./frontend/node_modules/jsdom/lib/generated/idl/Crypto.js
    ./frontend/node_modules/jsdom/lib/generated/idl/DocumentReadyState.js
    ./frontend/node_modules/jsdom/lib/generated/idl/HTMLButtonElement.js
    ./frontend/node_modules/jsdom/lib/generated/idl/FocusEvent.js
    ./frontend/node_modules/jsdom/lib/generated/idl/HTMLLinkElement.js
    ./frontend/node_modules/jsdom/lib/generated/idl/File.js
    ./frontend/node_modules/jsdom/lib/generated/idl/XMLHttpRequestUpload.js
    ./frontend/node_modules/jsdom/lib/generated/idl/ProgressEvent.js
    ./frontend/node_modules/jsdom/lib/generated/idl/WheelEvent.js
    ./frontend/node_modules/jsdom/lib/generated/idl/ErrorEventInit.js
    ./frontend/node_modules/jsdom/lib/generated/idl/Navigator.js
    ./frontend/node_modules/jsdom/lib/generated/idl/HTMLUnknownElement.js
    ./frontend/node_modules/jsdom/lib/generated/idl/DOMImplementation.js
    ./frontend/node_modules/jsdom/lib/generated/idl/utils.js
    ./frontend/node_modules/jsdom/lib/generated/idl/HTMLDivElement.js
    ./frontend/node_modules/jsdom/lib/generated/idl/TouchEventInit.js
    ./frontend/node_modules/jsdom/lib/generated/idl/NamedNodeMap.js
    ./frontend/node_modules/jsdom/lib/generated/idl/SVGAnimatedPreserveAspectRatio.js
    ./frontend/node_modules/jsdom/lib/generated/idl/BarProp.js
    ./frontend/node_modules/jsdom/lib/generated/idl/SVGElement.js
    ./frontend/node_modules/jsdom/lib/generated/idl/HashChangeEventInit.js
    ./frontend/node_modules/jsdom/lib/generated/idl/EventListener.js
    ./frontend/node_modules/jsdom/lib/generated/idl/TextEncoderEncodeIntoResult.js
    ./frontend/node_modules/jsdom/lib/generated/idl/CSSNestedDeclarations.js
    ./frontend/node_modules/jsdom/lib/generated/idl/SelectionMode.js
    ./frontend/node_modules/jsdom/lib/generated/idl/Blob.js
    ./frontend/node_modules/jsdom/lib/generated/idl/VisibilityState.js
    ./frontend/node_modules/jsdom/lib/generated/idl/DOMRectInit.js
    ./frontend/node_modules/jsdom/lib/generated/idl/HTMLUListElement.js
    ./frontend/node_modules/jsdom/lib/generated/idl/CompositionEvent.js
    ./frontend/node_modules/jsdom/lib/generated/idl/SVGTitleElement.js
    ./frontend/node_modules/jsdom/lib/generated/idl/Attr.js
    ./frontend/node_modules/jsdom/lib/generated/idl/CSSKeyframesRule.js
    ./frontend/node_modules/jsdom/lib/generated/idl/HTMLTableCellElement.js
    ./frontend/node_modules/jsdom/lib/generated/idl/ValidityState.js
    ./frontend/node_modules/jsdom/lib/generated/idl/HTMLImageElement.js
    ./frontend/node_modules/jsdom/lib/generated/idl/HTMLAudioElement.js
    ./frontend/node_modules/jsdom/lib/generated/idl/CSSCounterStyleRule.js
    ./frontend/node_modules/jsdom/lib/generated/idl/HTMLAnchorElement.js
    ./frontend/node_modules/jsdom/lib/generated/idl/HTMLScriptElement.js
    ./frontend/node_modules/jsdom/lib/generated/idl/HTMLTableColElement.js
    ./frontend/node_modules/jsdom/lib/generated/idl/SubmitEvent.js
    ./frontend/node_modules/jsdom/lib/generated/idl/Function.js
    ./frontend/node_modules/jsdom/lib/generated/idl/TransitionEvent.js
    ./frontend/node_modules/jsdom/lib/generated/idl/BlobPropertyBag.js
    ./frontend/node_modules/jsdom/lib/generated/idl/PluginArray.js
    ./frontend/node_modules/jsdom/lib/generated/idl/BlobCallback.js
    ./frontend/node_modules/jsdom/lib/generated/idl/DOMStringMap.js
    ./frontend/node_modules/jsdom/lib/generated/idl/History.js
    ./frontend/node_modules/jsdom/lib/generated/idl/MediaList.js
    ./frontend/node_modules/jsdom/lib/generated/idl/WebSocket.js
    ./frontend/node_modules/jsdom/lib/generated/idl/CustomEvent.js
    ./frontend/node_modules/jsdom/lib/generated/idl/HTMLDListElement.js
    ./frontend/node_modules/jsdom/lib/generated/idl/XMLHttpRequestEventTarget.js
    ./frontend/node_modules/jsdom/lib/generated/idl/CSSLayerBlockRule.js
    ./frontend/node_modules/jsdom/lib/generated/idl/FileReader.js
    ./frontend/node_modules/jsdom/lib/generated/idl/HTMLInputElement.js
    ./frontend/node_modules/jsdom/lib/generated/idl/HTMLLabelElement.js
    ./frontend/node_modules/jsdom/lib/generated/idl/Selection.js
    ./frontend/node_modules/jsdom/lib/generated/idl/SubmitEventInit.js
    ./frontend/node_modules/jsdom/lib/generated/idl/CDATASection.js
    ./frontend/node_modules/jsdom/lib/generated/idl/DocumentType.js
    ./frontend/node_modules/jsdom/lib/generated/idl/ShadowRoot.js
    ./frontend/node_modules/jsdom/lib/generated/idl/AssignedNodesOptions.js
    ./frontend/node_modules/jsdom/lib/generated/idl/HTMLObjectElement.js
    ./frontend/node_modules/jsdom/lib/generated/idl/HTMLMeterElement.js
    ./frontend/node_modules/whatwg-mimetype/lib/serializer.js
    ./frontend/node_modules/whatwg-mimetype/lib/parser.js
    ./frontend/node_modules/whatwg-mimetype/lib/utils.js
    ./frontend/node_modules/whatwg-mimetype/lib/mime-type.js
    ./frontend/node_modules/whatwg-mimetype/lib/sniff.js
    ./frontend/node_modules/whatwg-mimetype/lib/index.js
    ./frontend/node_modules/whatwg-mimetype/lib/mime-type-parameters.js
    ./frontend/node_modules/whatwg-mimetype/package.json
    ./frontend/node_modules/whatwg-mimetype/README.md
    ./frontend/node_modules/eslint/lib/services/warning-service.js
    ./frontend/node_modules/eslint/lib/services/suppressions-service.js
    ./frontend/node_modules/eslint/lib/services/processor-service.js
    ./frontend/node_modules/eslint/lib/services/parser-service.js
    ./frontend/node_modules/eslint/lib/api.js
    ./frontend/node_modules/eslint/lib/cli.js
    ./frontend/node_modules/convert-source-map/package.json
    ./frontend/node_modules/convert-source-map/README.md
    ./frontend/node_modules/convert-source-map/index.js
    ./frontend/node_modules/convert-source-map/LICENSE
    ./frontend/node_modules/cross-spawn/lib/util/resolveCommand.js
    ./frontend/node_modules/cross-spawn/lib/util/escape.js
    ./frontend/node_modules/cross-spawn/lib/util/readShebang.js
    ./frontend/node_modules/json5/dist/index.min.js
    ./frontend/node_modules/json5/dist/index.mjs
    ./frontend/node_modules/json5/dist/index.js
    ./frontend/node_modules/json5/dist/index.min.mjs
    ./frontend/node_modules/json5/LICENSE.md
    ./frontend/node_modules/cross-spawn/package.json
    ./frontend/node_modules/cross-spawn/README.md
    ./frontend/node_modules/cross-spawn/index.js
    ./frontend/node_modules/cross-spawn/LICENSE
    ./frontend/node_modules/@humanfs/node/dist/index.d.ts
    ./frontend/node_modules/@humanfs/node/dist/node-hfs.d.ts
    ./frontend/node_modules/@humanfs/node/dist/node-fsx.d.ts
    ./frontend/node_modules/@humanfs/node/LICENSE
    ./frontend/node_modules/@testing-library/jest-dom/node_modules/dom-accessibility-api/package.json
    ./frontend/node_modules/@testing-library/jest-dom/node_modules/dom-accessibility-api/README.md
    ./frontend/node_modules/uri-js/package.json
    ./frontend/node_modules/uri-js/yarn.lock
    ./frontend/node_modules/uri-js/README.md
    ./frontend/node_modules/mdn-data/css/syntaxes.json
    ./frontend/node_modules/mdn-data/css/syntaxes.schema.json
    ./frontend/node_modules/mdn-data/css/types.schema.json
    ./frontend/node_modules/mdn-data/css/functions.json
    ./frontend/node_modules/mdn-data/css/definitions.json
    ./frontend/node_modules/mdn-data/css/functions.schema.json
    ./frontend/node_modules/mdn-data/css/at-rules.schema.json
    ./frontend/node_modules/mdn-data/css/units.json
    ./frontend/node_modules/mdn-data/css/index.js
    ./frontend/node_modules/mdn-data/css/properties.json
    ./frontend/node_modules/mdn-data/css/at-rules.json
    ./frontend/node_modules/mdn-data/css/selectors.json
    ./frontend/node_modules/mdn-data/css/types.json
    ./frontend/node_modules/mdn-data/css/units.schema.json
    ./frontend/node_modules/mdn-data/css/properties.schema.json
    ./frontend/node_modules/mdn-data/css/selectors.schema.json
    ./frontend/node_modules/mdn-data/LICENSE
    ./frontend/node_modules/concat-map/.travis.yml
    ./frontend/node_modules/concat-map/package.json
    ./frontend/node_modules/concat-map/README.markdown
    ./frontend/node_modules/concat-map/index.js
    ./frontend/node_modules/eslint/lib/eslint/legacy-eslint.js
    ./frontend/node_modules/eslint/lib/eslint/eslint-helpers.js
    ./frontend/node_modules/eslint/lib/eslint/index.js
    ./frontend/node_modules/eslint/lib/eslint/worker.js
    ./frontend/node_modules/eslint/lib/eslint/eslint.js
    ./frontend/node_modules/@standard-schema/spec/package.json
    ./frontend/node_modules/@standard-schema/spec/README.md
    ./frontend/node_modules/react-router-dom/package.json
    ./frontend/node_modules/react-router-dom/README.md
    ./frontend/node_modules/concat-map/example/map.js
    ./frontend/node_modules/@humanfs/core/src/path.js
    ./frontend/node_modules/@humanfs/core/src/hfs.js
    ./frontend/node_modules/@humanfs/core/src/errors.js
    ./frontend/node_modules/@humanfs/core/src/index.js
    ./frontend/node_modules/@humanfs/core/package.json
    ./frontend/node_modules/@humanfs/core/README.md
    ./frontend/node_modules/@standard-schema/spec/dist/index.d.ts
    ./frontend/node_modules/@standard-schema/spec/dist/index.cjs
    ./frontend/node_modules/@standard-schema/spec/dist/index.js
    ./frontend/node_modules/@standard-schema/spec/dist/index.d.cts
    ./frontend/node_modules/@standard-schema/spec/LICENSE
    ./frontend/node_modules/react-router-dom/dist/index.d.ts
    ./frontend/node_modules/react-router-dom/dist/index.mjs
    ./frontend/node_modules/react-router-dom/dist/index.js
    ./frontend/node_modules/react-router-dom/dist/index.d.mts
    ./frontend/node_modules/react-router-dom/LICENSE.md
    ./frontend/node_modules/@testing-library/jest-dom/node_modules/dom-accessibility-api/dist/accessible-name-and-description.js.map
    ./frontend/node_modules/@testing-library/jest-dom/node_modules/dom-accessibility-api/dist/index.d.ts.map
    ./frontend/node_modules/@testing-library/jest-dom/node_modules/dom-accessibility-api/dist/accessible-name.js
    ./frontend/node_modules/@testing-library/jest-dom/node_modules/dom-accessibility-api/dist/accessible-name-and-description.js
    ./frontend/node_modules/@testing-library/jest-dom/node_modules/dom-accessibility-api/dist/accessible-description.js
    ./frontend/node_modules/@testing-library/jest-dom/node_modules/dom-accessibility-api/dist/accessible-name.js.map
    ./frontend/node_modules/@testing-library/jest-dom/node_modules/dom-accessibility-api/dist/is-inaccessible.js.map
    ./frontend/node_modules/@testing-library/jest-dom/node_modules/dom-accessibility-api/dist/is-disabled.mjs
    ./frontend/node_modules/@testing-library/jest-dom/node_modules/dom-accessibility-api/dist/is-disabled.d.ts.map
    ./frontend/node_modules/@testing-library/jest-dom/node_modules/dom-accessibility-api/dist/index.d.ts
    ./frontend/node_modules/@testing-library/jest-dom/node_modules/dom-accessibility-api/dist/util.d.ts
    ./frontend/node_modules/@testing-library/jest-dom/node_modules/dom-accessibility-api/dist/getRole.mjs.map
    ./frontend/node_modules/@testing-library/jest-dom/node_modules/dom-accessibility-api/dist/accessible-description.d.ts
    ./frontend/node_modules/@testing-library/jest-dom/node_modules/dom-accessibility-api/dist/is-inaccessible.d.ts
    ./frontend/node_modules/@testing-library/jest-dom/node_modules/dom-accessibility-api/dist/index.js.map
    ./frontend/node_modules/mdn-data/l10n/css.json
    ./frontend/node_modules/mdn-data/l10n/index.js
    ./frontend/node_modules/concat-map/test/map.js
    ./frontend/node_modules/concat-map/LICENSE
    ./frontend/node_modules/optionator/CHANGELOG.md
    ./frontend/node_modules/optionator/LICENSE
    ./frontend/node_modules/uri-js/dist/esnext/uri.js
    ./frontend/node_modules/uri-js/dist/esnext/uri.js.map
    ./frontend/node_modules/uri-js/dist/esnext/regexps-iri.d.ts
    ./frontend/node_modules/uri-js/dist/esnext/index.d.ts
    ./frontend/node_modules/uri-js/dist/esnext/util.d.ts
    ./frontend/node_modules/uri-js/dist/esnext/regexps-iri.js
    ./frontend/node_modules/uri-js/dist/esnext/regexps-uri.d.ts
    ./frontend/node_modules/uri-js/dist/esnext/index.js.map
    ./frontend/node_modules/uri-js/dist/esnext/regexps-uri.js.map
    ./frontend/node_modules/uri-js/dist/esnext/regexps-uri.js
    ./frontend/node_modules/uri-js/dist/esnext/index.js
    ./frontend/node_modules/uri-js/dist/esnext/uri.d.ts
    ./frontend/node_modules/uri-js/dist/esnext/util.js.map
    ./frontend/node_modules/uri-js/dist/esnext/regexps-iri.js.map
    ./frontend/node_modules/uri-js/dist/esnext/util.js
    ./frontend/node_modules/@humanfs/core/dist/index.d.ts
    ./frontend/node_modules/@humanfs/core/dist/hfs.d.ts
    ./frontend/node_modules/@humanfs/core/dist/errors.d.ts
    ./frontend/node_modules/@humanfs/core/dist/fsx.d.ts
    ./frontend/node_modules/@humanfs/core/dist/path.d.ts
    ./frontend/node_modules/@humanfs/core/LICENSE
    ./frontend/node_modules/optionator/README.md
    ./frontend/node_modules/optionator/package.json
    ./frontend/node_modules/uri-js/LICENSE
    ./frontend/node_modules/optionator/lib/help.js
    ./frontend/node_modules/optionator/lib/index.js
    ./frontend/node_modules/optionator/lib/util.js
    ./frontend/node_modules/eslint/LICENSE
    ./frontend/node_modules/lodash.merge/package.json
    ./frontend/node_modules/lodash.merge/README.md
    ./frontend/node_modules/lodash.merge/index.js
    ./frontend/node_modules/lodash.merge/LICENSE
    ./frontend/node_modules/uri-js/dist/esnext/schemes/http.js
    ./frontend/node_modules/uri-js/dist/esnext/schemes/wss.js
    ./frontend/node_modules/uri-js/dist/esnext/schemes/ws.js
    ./frontend/node_modules/uri-js/dist/esnext/schemes/mailto.js
    ./frontend/node_modules/uri-js/dist/esnext/schemes/wss.d.ts
    ./frontend/node_modules/uri-js/dist/esnext/schemes/urn-uuid.js.map
    ./frontend/node_modules/uri-js/dist/esnext/schemes/https.js.map
    ./frontend/node_modules/uri-js/dist/esnext/schemes/https.d.ts
    ./frontend/node_modules/uri-js/dist/esnext/schemes/urn-uuid.d.ts
    ./frontend/node_modules/uri-js/dist/esnext/schemes/ws.js.map
    ./frontend/node_modules/uri-js/dist/esnext/schemes/http.js.map
    ./frontend/node_modules/uri-js/dist/esnext/schemes/ws.d.ts
    ./frontend/node_modules/uri-js/dist/esnext/schemes/http.d.ts
    ./frontend/node_modules/uri-js/dist/esnext/schemes/https.js
    ./frontend/node_modules/uri-js/dist/esnext/schemes/mailto.js.map
    ./frontend/node_modules/uri-js/dist/esnext/schemes/urn.d.ts
    ./frontend/node_modules/uri-js/dist/esnext/schemes/wss.js.map
    ./frontend/node_modules/uri-js/dist/esnext/schemes/mailto.d.ts
    ./frontend/node_modules/uri-js/dist/esnext/schemes/urn.js.map
    ./frontend/node_modules/uri-js/dist/esnext/schemes/urn-uuid.js
    ./frontend/node_modules/uri-js/dist/esnext/schemes/urn.js
    ./frontend/node_modules/eslint/README.md
    ./frontend/node_modules/eslint/lib/rule-tester/rule-tester.js
    ./frontend/node_modules/eslint/lib/rule-tester/index.js
    ./frontend/node_modules/es-module-lexer/lexer.js
    ./frontend/node_modules/es-module-lexer/package.json
    ./frontend/node_modules/es-module-lexer/README.md
    ./frontend/node_modules/uri-js/dist/es5/uri.all.d.ts
    ./frontend/node_modules/uri-js/dist/es5/uri.all.js
    ./frontend/node_modules/uri-js/dist/es5/uri.all.min.js.map
    ./frontend/node_modules/uri-js/dist/es5/uri.all.min.js
    ./frontend/node_modules/uri-js/dist/es5/uri.all.min.d.ts
    ./frontend/node_modules/uri-js/dist/es5/uri.all.js.map
    ./frontend/node_modules/eslint/messages/no-config-found.js
    ./frontend/node_modules/eslint/messages/shared.js
    ./frontend/node_modules/eslint/messages/config-plugin-missing.js
    ./frontend/node_modules/eslint/messages/whitespace-found.js
    ./frontend/node_modules/eslint/messages/plugin-conflict.js
    ./frontend/node_modules/eslint/messages/print-config-with-directory-path.js
    ./frontend/node_modules/eslint/messages/invalid-rule-options.js
    ./frontend/node_modules/eslint/messages/all-files-ignored.js
    ./frontend/node_modules/eslint/messages/extend-config-missing.js
    ./frontend/node_modules/eslint/messages/invalid-rule-severity.js
    ./frontend/node_modules/eslint/messages/file-not-found.js
    ./frontend/node_modules/eslint/messages/plugin-missing.js
    ./frontend/node_modules/eslint/messages/config-file-missing.js
    ./frontend/node_modules/eslint/messages/config-serialize-function.js
    ./frontend/node_modules/eslint/messages/eslintrc-incompat.js
    ./frontend/node_modules/eslint/messages/all-matched-files-ignored.js
    ./frontend/node_modules/eslint/messages/failed-to-read-json.js
    ./frontend/node_modules/eslint/messages/plugin-invalid.js
    ./frontend/node_modules/eslint/messages/eslintrc-plugins.js
    ./frontend/node_modules/@testing-library/jest-dom/node_modules/dom-accessibility-api/dist/polyfills/iterator.d.mjs.map
    ./frontend/node_modules/@testing-library/jest-dom/node_modules/dom-accessibility-api/dist/polyfills/array.from.js
    ./frontend/node_modules/@testing-library/jest-dom/node_modules/dom-accessibility-api/dist/polyfills/iterator.d.js
    ./frontend/node_modules/@testing-library/jest-dom/node_modules/dom-accessibility-api/dist/polyfills/SetLike.mjs
    ./frontend/node_modules/@testing-library/jest-dom/node_modules/dom-accessibility-api/dist/polyfills/array.from.mjs
    ./frontend/node_modules/@testing-library/jest-dom/node_modules/dom-accessibility-api/dist/polyfills/SetLike.js
    ./frontend/node_modules/@testing-library/jest-dom/node_modules/dom-accessibility-api/dist/polyfills/SetLike.js.map
    ./frontend/node_modules/@testing-library/jest-dom/node_modules/dom-accessibility-api/dist/polyfills/array.from.d.ts.map
    ./frontend/node_modules/@testing-library/jest-dom/node_modules/dom-accessibility-api/dist/polyfills/iterator.d.js.map
    ./frontend/node_modules/@testing-library/jest-dom/node_modules/dom-accessibility-api/dist/polyfills/array.from.mjs.map
    ./frontend/node_modules/@testing-library/jest-dom/node_modules/dom-accessibility-api/dist/polyfills/SetLike.mjs.map
    ./frontend/node_modules/@testing-library/jest-dom/node_modules/dom-accessibility-api/dist/polyfills/array.from.d.ts
    ./frontend/node_modules/@testing-library/jest-dom/node_modules/dom-accessibility-api/dist/polyfills/SetLike.d.ts.map
    ./frontend/node_modules/@testing-library/jest-dom/node_modules/dom-accessibility-api/dist/polyfills/SetLike.d.ts
    ./frontend/node_modules/@testing-library/jest-dom/node_modules/dom-accessibility-api/dist/polyfills/iterator.d.mjs
    ./frontend/node_modules/@testing-library/jest-dom/node_modules/dom-accessibility-api/dist/polyfills/array.from.js.map
    ./frontend/node_modules/@testing-library/jest-dom/node_modules/dom-accessibility-api/dist/accessible-description.d.ts.map
    ./frontend/node_modules/@testing-library/jest-dom/node_modules/dom-accessibility-api/dist/getRole.js
    ./frontend/node_modules/@testing-library/jest-dom/node_modules/dom-accessibility-api/dist/index.mjs
    ./frontend/node_modules/@testing-library/jest-dom/node_modules/dom-accessibility-api/dist/accessible-name-and-description.d.ts
    ./frontend/node_modules/@testing-library/jest-dom/node_modules/dom-accessibility-api/dist/getRole.d.ts.map
    ./frontend/node_modules/@testing-library/jest-dom/node_modules/dom-accessibility-api/dist/util.d.ts.map
    ./frontend/node_modules/@testing-library/jest-dom/node_modules/dom-accessibility-api/dist/is-disabled.d.ts
    ./frontend/node_modules/@testing-library/jest-dom/node_modules/dom-accessibility-api/dist/getRole.mjs
    ./frontend/node_modules/@testing-library/jest-dom/node_modules/dom-accessibility-api/dist/accessible-name.mjs
    ./frontend/node_modules/@testing-library/jest-dom/node_modules/dom-accessibility-api/dist/accessible-description.mjs.map
    ./frontend/node_modules/@testing-library/jest-dom/node_modules/dom-accessibility-api/dist/accessible-name-and-description.mjs
    ./frontend/node_modules/@testing-library/jest-dom/node_modules/dom-accessibility-api/dist/getRole.d.ts
    ./frontend/node_modules/@testing-library/jest-dom/node_modules/dom-accessibility-api/dist/index.mjs.map
    ./frontend/node_modules/@testing-library/jest-dom/node_modules/dom-accessibility-api/dist/accessible-name.d.ts
    ./frontend/node_modules/@testing-library/jest-dom/node_modules/dom-accessibility-api/dist/index.js
    ./frontend/node_modules/@testing-library/jest-dom/node_modules/dom-accessibility-api/dist/accessible-name-and-description.d.ts.map
    ./frontend/node_modules/@testing-library/jest-dom/node_modules/dom-accessibility-api/dist/is-disabled.mjs.map
    ./frontend/node_modules/@testing-library/jest-dom/node_modules/dom-accessibility-api/dist/is-inaccessible.js
    ./frontend/node_modules/@testing-library/jest-dom/node_modules/dom-accessibility-api/dist/is-inaccessible.mjs
    ./frontend/node_modules/@testing-library/jest-dom/node_modules/dom-accessibility-api/dist/util.mjs
    ./frontend/node_modules/@testing-library/jest-dom/node_modules/dom-accessibility-api/dist/is-disabled.js.map
    ./frontend/node_modules/@testing-library/jest-dom/node_modules/dom-accessibility-api/dist/accessible-name.d.ts.map
    ./frontend/node_modules/@testing-library/jest-dom/node_modules/dom-accessibility-api/dist/is-disabled.js
    ./frontend/node_modules/@testing-library/jest-dom/node_modules/dom-accessibility-api/dist/util.js.map
    ./frontend/node_modules/@testing-library/jest-dom/node_modules/dom-accessibility-api/dist/is-inaccessible.mjs.map
    ./frontend/node_modules/@testing-library/jest-dom/node_modules/dom-accessibility-api/dist/accessible-description.mjs
    ./frontend/node_modules/@testing-library/jest-dom/node_modules/dom-accessibility-api/dist/accessible-name-and-description.mjs.map
    ./frontend/node_modules/@testing-library/jest-dom/node_modules/dom-accessibility-api/dist/is-inaccessible.d.ts.map
    ./frontend/node_modules/@testing-library/jest-dom/node_modules/dom-accessibility-api/dist/util.js
    ./frontend/node_modules/@testing-library/jest-dom/node_modules/dom-accessibility-api/dist/accessible-description.js.map
    ./frontend/node_modules/@testing-library/jest-dom/node_modules/dom-accessibility-api/dist/accessible-name.mjs.map
    ./frontend/node_modules/@testing-library/jest-dom/node_modules/dom-accessibility-api/dist/util.mjs.map
    ./frontend/node_modules/@testing-library/jest-dom/node_modules/dom-accessibility-api/dist/getRole.js.map
    ./frontend/node_modules/@testing-library/jest-dom/node_modules/dom-accessibility-api/LICENSE.md
    ./frontend/node_modules/@testing-library/jest-dom/vitest.d.ts
    ./frontend/node_modules/eslint/lib/types/index.d.ts
    ./frontend/node_modules/es-module-lexer/dist/lexer.js
    ./frontend/node_modules/eslint/lib/types/config-api.d.ts
    ./frontend/node_modules/es-module-lexer/dist/lexer.asm.js
    ./frontend/node_modules/eslint/lib/types/rules.d.ts
    ./frontend/node_modules/eslint/lib/types/universal.d.ts
    ./frontend/node_modules/eslint/lib/types/use-at-your-own-risk.d.ts
    ./frontend/node_modules/es-module-lexer/dist/lexer.cjs
    ./frontend/node_modules/eslint/package.json
    ./frontend/node_modules/es-module-lexer/LICENSE
    ./frontend/node_modules/eslint/lib/options.js
    ./frontend/node_modules/espree/espree.js
    ./frontend/node_modules/@vitest/expect/package.json
    ./frontend/node_modules/es-module-lexer/types/lexer.d.ts
    ./frontend/node_modules/@vitest/expect/README.md
    ./frontend/node_modules/eslint/bin/eslint.js
    ./frontend/node_modules/@testing-library/jest-dom/dist/vitest.mjs
    ./frontend/node_modules/@testing-library/jest-dom/dist/matchers-98b869c1.js
    ./frontend/node_modules/@testing-library/jest-dom/dist/index.mjs
    ./frontend/node_modules/@testing-library/jest-dom/dist/jest-globals.js
    ./frontend/node_modules/@testing-library/jest-dom/dist/matchers-35e4d3bd.mjs
    ./frontend/node_modules/@testing-library/jest-dom/dist/matchers.js
    ./frontend/node_modules/@testing-library/jest-dom/dist/index.js
    ./frontend/node_modules/@testing-library/jest-dom/dist/matchers.mjs
    ./frontend/node_modules/@testing-library/jest-dom/dist/jest-globals.mjs
    ./frontend/node_modules/@testing-library/jest-dom/dist/vitest.js
    ./frontend/node_modules/@testing-library/jest-dom/CHANGELOG.md
    ./frontend/node_modules/@testing-library/jest-dom/LICENSE
    ./frontend/node_modules/eslint/lib/linter/interpolate.js
    ./frontend/node_modules/eslint/lib/linter/timing.js
    ./frontend/node_modules/eslint/lib/linter/file-context.js
    ./frontend/node_modules/eslint/lib/linter/linter.js
    ./frontend/node_modules/@vitest/expect/dist/index.d.ts
    ./frontend/node_modules/@vitest/expect/dist/index.js
    ./frontend/node_modules/@vitest/utils/helpers.d.ts
    ./frontend/node_modules/@vitest/utils/package.json
    ./frontend/node_modules/@vitest/utils/README.md
    ./frontend/node_modules/@vitest/expect/LICENSE
    ./frontend/node_modules/espree/lib/espree.js
    ./frontend/node_modules/espree/lib/version.js
    ./frontend/node_modules/espree/lib/token-translator.js
    ./frontend/node_modules/espree/lib/options.js
    ./frontend/node_modules/espree/lib/features.js
    ./frontend/node_modules/espree/package.json
    ./frontend/node_modules/espree/README.md
    ./frontend/node_modules/eslint/lib/cli-engine/cli-engine.js
    ./frontend/node_modules/eslint/lib/cli-engine/hash.js
    ./frontend/node_modules/eslint/lib/cli-engine/file-enumerator.js
    ./frontend/node_modules/eslint/lib/config/default-config.js
    ./frontend/node_modules/eslint/lib/config/config.js
    ./frontend/node_modules/eslint/lib/config/config-loader.js
    ./frontend/node_modules/eslint/lib/config/flat-config-array.js
    ./frontend/node_modules/eslint/lib/config/flat-config-schema.js
    ./frontend/node_modules/eslint/lib/linter/source-code-fixer.js
    ./frontend/node_modules/eslint/lib/linter/file-report.js
    ./frontend/node_modules/eslint/lib/linter/esquery.js
    ./frontend/node_modules/eslint/lib/linter/source-code-visitor.js
    ./frontend/node_modules/eslint/lib/linter/rules.js
    ./frontend/node_modules/eslint/lib/linter/apply-disable-directives.js
    ./frontend/node_modules/eslint/lib/linter/index.js
    ./frontend/node_modules/eslint/lib/linter/rule-fixer.js
    ./frontend/node_modules/eslint/lib/linter/source-code-traverser.js
    ./frontend/node_modules/eslint/lib/linter/vfile.js
    ./frontend/node_modules/eslint/lib/linter/code-path-analysis/code-path-analyzer.js
    ./frontend/node_modules/eslint/lib/linter/code-path-analysis/debug-helpers.js
    ./frontend/node_modules/eslint/lib/linter/code-path-analysis/fork-context.js
    ./frontend/node_modules/eslint/lib/linter/code-path-analysis/id-generator.js
    ./frontend/node_modules/eslint/lib/linter/code-path-analysis/code-path.js
    ./frontend/node_modules/eslint/lib/linter/code-path-analysis/code-path-segment.js
    ./frontend/node_modules/eslint/lib/linter/code-path-analysis/code-path-state.js
    ./frontend/node_modules/espree/dist/espree.cjs
    ./frontend/node_modules/@testing-library/jest-dom/types/jest-globals.d.ts
    ./frontend/node_modules/@testing-library/jest-dom/types/index.d.ts
    ./frontend/node_modules/@testing-library/jest-dom/types/matchers-standalone.d.ts
    ./frontend/node_modules/espree/LICENSE
    ./frontend/node_modules/eslint/lib/config-api.js
    ./frontend/node_modules/eslint/lib/rules/computed-property-spacing.js
    ./frontend/node_modules/eslint/lib/rules/wrap-iife.js
    ./frontend/node_modules/eslint/lib/rules/space-infix-ops.js
    ./frontend/node_modules/eslint/lib/rules/prefer-promise-reject-errors.js
    ./frontend/node_modules/eslint/lib/rules/strict.js
    ./frontend/node_modules/eslint/lib/rules/one-var.js
    ./frontend/node_modules/eslint/lib/rules/no-extra-label.js
    ./frontend/node_modules/eslint/lib/rules/no-undef.js
    ./frontend/node_modules/eslint/lib/rules/no-setter-return.js
    ./frontend/node_modules/eslint/lib/rules/semi-spacing.js
    ./frontend/node_modules/eslint/lib/rules/object-curly-newline.js
    ./frontend/node_modules/eslint/lib/rules/class-methods-use-this.js
    ./frontend/node_modules/eslint/lib/rules/no-new-native-nonconstructor.js
    ./frontend/node_modules/eslint/lib/rules/arrow-parens.js
    ./frontend/node_modules/eslint/lib/rules/guard-for-in.js
    ./frontend/node_modules/eslint/lib/rules/complexity.js
    ./frontend/node_modules/eslint/lib/rules/lines-around-comment.js
    ./frontend/node_modules/eslint/lib/rules/id-match.js
    ./frontend/node_modules/eslint/lib/rules/dot-notation.js
    ./frontend/node_modules/eslint/lib/rules/padding-line-between-statements.js
    ./frontend/node_modules/eslint/lib/rules/no-extra-semi.js
    ./frontend/node_modules/eslint/lib/rules/no-compare-neg-zero.js
    ./frontend/node_modules/eslint/lib/rules/no-new-symbol.js
    ./frontend/node_modules/eslint/lib/rules/no-buffer-constructor.js
    ./frontend/node_modules/eslint/lib/rules/implicit-arrow-linebreak.js
    ./frontend/node_modules/eslint/lib/rules/sort-vars.js
    ./frontend/node_modules/eslint/lib/rules/no-var.js
    ./frontend/node_modules/eslint/lib/universal.js
    ./frontend/node_modules/eslint/lib/rules/array-callback-return.js
    ./frontend/node_modules/eslint/lib/rules/no-irregular-whitespace.js
    ./frontend/node_modules/eslint/lib/rules/no-div-regex.js
    ./frontend/node_modules/eslint/lib/rules/no-array-constructor.js
    ./frontend/node_modules/eslint/lib/rules/no-const-assign.js
    ./frontend/node_modules/eslint/lib/rules/no-lonely-if.js
    ./frontend/node_modules/eslint/lib/rules/nonblock-statement-body-position.js
    ./frontend/node_modules/eslint/lib/rules/function-paren-newline.js
    ./frontend/node_modules/eslint/lib/rules/no-fallthrough.js
    ./frontend/node_modules/eslint/lib/rules/space-unary-ops.js
    ./frontend/node_modules/eslint/lib/rules/no-dupe-keys.js
    ./frontend/node_modules/eslint/lib/rules/newline-before-return.js
    ./frontend/node_modules/eslint/lib/rules/no-floating-decimal.js
    ./frontend/node_modules/eslint/lib/rules/consistent-this.js
    ./frontend/node_modules/eslint/lib/rules/no-unassigned-vars.js
    ./frontend/node_modules/eslint/lib/rules/function-call-argument-newline.js
    ./frontend/node_modules/eslint/lib/rules/array-bracket-newline.js
    ./frontend/node_modules/eslint/lib/rules/no-useless-escape.js
    ./frontend/node_modules/eslint/lib/rules/func-name-matching.js
    ./frontend/node_modules/eslint/lib/rules/max-params.js
    ./frontend/node_modules/eslint/lib/rules/no-empty-pattern.js
    ./frontend/node_modules/eslint/lib/rules/no-restricted-properties.js
    ./frontend/node_modules/eslint/lib/rules/for-direction.js
    ./frontend/node_modules/eslint/lib/rules/no-useless-rename.js
    ./frontend/node_modules/eslint/lib/rules/max-len.js
    ./frontend/node_modules/eslint/lib/rules/lines-between-class-members.js
    ./frontend/node_modules/eslint/lib/rules/no-implied-eval.js
    ./frontend/node_modules/eslint/lib/rules/no-empty-character-class.js
    ./frontend/node_modules/eslint/lib/rules/indent-legacy.js
    ./frontend/node_modules/eslint/lib/rules/no-constant-condition.js
    ./frontend/node_modules/eslint/lib/rules/multiline-comment-style.js
    ./frontend/node_modules/eslint/lib/rules/no-useless-concat.js
    ./frontend/node_modules/eslint/lib/rules/prefer-object-has-own.js
    ./frontend/node_modules/eslint/lib/rules/no-multi-spaces.js
    ./frontend/node_modules/eslint/lib/rules/array-element-newline.js
    ./frontend/node_modules/eslint/lib/rules/no-loop-func.js
    ./frontend/node_modules/eslint/lib/rules/no-eval.js
    ./frontend/node_modules/eslint/lib/rules/semi-style.js
    ./frontend/node_modules/eslint/lib/rules/prefer-named-capture-group.js
    ./frontend/node_modules/eslint/lib/shared/stats.js
    ./frontend/node_modules/eslint/lib/shared/traverser.js
    ./frontend/node_modules/eslint/lib/shared/ajv.js
    ./frontend/node_modules/eslint/lib/shared/directives.js
    ./frontend/node_modules/eslint/lib/shared/text-table.js
    ./frontend/node_modules/eslint/lib/shared/serialization.js
    ./frontend/node_modules/eslint/lib/shared/translate-cli-options.js
    ./frontend/node_modules/eslint/lib/shared/runtime-info.js
    ./frontend/node_modules/eslint/lib/shared/option-utils.js
    ./frontend/node_modules/eslint/lib/shared/ast-utils.js
    ./frontend/node_modules/eslint/lib/shared/severity.js
    ./frontend/node_modules/eslint/lib/shared/logging.js
    ./frontend/node_modules/eslint/lib/shared/relative-module-resolver.js
    ./frontend/node_modules/eslint/lib/shared/string-utils.js
    ./frontend/node_modules/eslint/lib/shared/deep-merge-arrays.js
    ./frontend/node_modules/eslint/lib/shared/assert.js
    ./frontend/node_modules/eslint/lib/shared/naming.js
    ./frontend/node_modules/eslint/lib/shared/flags.js
    ./frontend/node_modules/eslint/lib/rules/no-unmodified-loop-condition.js
    ./frontend/node_modules/eslint/lib/rules/space-before-function-paren.js
    ./frontend/node_modules/eslint/lib/rules/no-implicit-globals.js
    ./frontend/node_modules/eslint/lib/rules/no-new-wrappers.js
    ./frontend/node_modules/eslint/lib/rules/no-native-reassign.js
    ./frontend/node_modules/eslint/lib/rules/padded-blocks.js
    ./frontend/node_modules/eslint/lib/rules/spaced-comment.js
    ./frontend/node_modules/eslint/lib/rules/default-case-last.js
    ./frontend/node_modules/eslint/lib/rules/func-call-spacing.js
    ./frontend/node_modules/eslint/lib/rules/no-ternary.js
    ./frontend/node_modules/eslint/lib/rules/no-self-assign.js
    ./frontend/node_modules/eslint/lib/rules/no-shadow.js
    ./frontend/node_modules/eslint/lib/rules/no-eq-null.js
    ./frontend/node_modules/eslint/lib/rules/no-label-var.js
    ./frontend/node_modules/eslint/lib/rules/no-object-constructor.js
    ./frontend/node_modules/eslint/lib/rules/no-new.js
    ./frontend/node_modules/eslint/lib/rules/require-unicode-regexp.js
    ./frontend/node_modules/eslint/lib/rules/yield-star-spacing.js
    ./frontend/node_modules/eslint/lib/rules/operator-linebreak.js
    ./frontend/node_modules/eslint/lib/rules/curly.js
    ./frontend/node_modules/eslint/lib/rules/no-useless-assignment.js
    ./frontend/node_modules/eslint/lib/rules/preserve-caught-error.js
    ./frontend/node_modules/eslint/lib/rules/no-dupe-else-if.js
    ./frontend/node_modules/eslint/lib/rules/no-obj-calls.js
    ./frontend/node_modules/eslint/lib/rules/arrow-body-style.js
    ./frontend/node_modules/eslint/lib/rules/eol-last.js
    ./frontend/node_modules/eslint/lib/rules/no-magic-numbers.js
    ./frontend/node_modules/eslint/lib/rules/no-octal.js
    ./frontend/node_modules/eslint/lib/rules/no-new-object.js
    ./frontend/node_modules/eslint/lib/rules/no-mixed-operators.js
    ./frontend/node_modules/eslint/lib/rules/no-nonoctal-decimal-escape.js
    ./frontend/node_modules/eslint/lib/rules/no-param-reassign.js
    ./frontend/node_modules/@vitest/utils/dist/resolver.js
    ./frontend/node_modules/eslint/lib/rules/use-isnan.js
    ./frontend/node_modules/@vitest/utils/dist/diff.js
    ./frontend/node_modules/@vitest/utils/dist/types.d-BCElaP-c.d.ts
    ./frontend/node_modules/@vitest/utils/dist/source-map.d.ts
    ./frontend/node_modules/@vitest/utils/dist/index.d.ts
    ./frontend/node_modules/@vitest/utils/dist/helpers.d.ts
    ./frontend/node_modules/eslint/lib/rules/no-extend-native.js
    ./frontend/node_modules/eslint/lib/rules/no-negated-in-lhs.js
    ./frontend/node_modules/eslint/lib/rules/vars-on-top.js
    ./frontend/node_modules/eslint/lib/rules/no-unused-labels.js
    ./frontend/node_modules/eslint/lib/rules/no-case-declarations.js
    ./frontend/node_modules/eslint/lib/rules/no-warning-comments.js
    ./frontend/node_modules/eslint/lib/rules/no-process-exit.js
    ./frontend/node_modules/eslint/lib/rules/no-proto.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/newArrowCheck.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/writeOnlyError.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/isNativeReflectConstruct.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/interopRequireWildcard.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/classPrivateFieldDestructureSet.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/objectWithoutProperties.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/temporalRef.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/initializerDefineProperty.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/checkInRHS.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/initializerDefineProperty.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/arrayLikeToArray.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/dispose.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/applyDecoratedDescriptor.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/iterableToArrayLimit.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/classStaticPrivateFieldDestructureSet.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/readOnlyError.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/writeOnlyError.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/toPrimitive.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/OverloadYield.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/setFunctionName.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/getPrototypeOf.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/awaitAsyncGenerator.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/AwaitValue.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/classPrivateFieldLooseKey.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/isNativeFunction.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/createSuper.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/classPrivateMethodGet.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/defaults.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/construct.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/classPrivateSetter.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/classCallCheck.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/objectSpread2.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/toPropertyKey.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/defaults.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/defineEnumerableProperties.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/wrapNativeSuper.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/toArray.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/applyDecs2203.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/objectWithoutPropertiesLoose.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/regeneratorKeys.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/createSuper.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/assertClassBrand.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/toSetter.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/nullishReceiverError.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/createForOfIteratorHelperLoose.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/temporalUndefined.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/regeneratorAsyncIterator.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/inherits.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/classPrivateGetter.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/classPrivateMethodSet.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/arrayLikeToArray.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/slicedToArray.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/initializerWarningHelper.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/applyDecs.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/applyDecs.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/classPrivateSetter.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/setPrototypeOf.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/using.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/usingCtx.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/toPrimitive.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/wrapAsyncGenerator.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/temporalRef.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/setPrototypeOf.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/classApplyDescriptorDestructureSet.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/slicedToArray.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/classStaticPrivateFieldSpecGet.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/nonIterableSpread.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/isNativeReflectConstruct.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/setFunctionName.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/regenerator.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/classExtractFieldDescriptor.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/taggedTemplateLiteralLoose.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/isNativeFunction.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/arrayWithHoles.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/identity.js
    ./frontend/node_modules/@vitest/pretty-format/package.json
    ./frontend/node_modules/@babel/helpers/lib/helpers/toConsumableArray.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/tdz.js
    ./frontend/node_modules/@vitest/pretty-format/README.md
    ./frontend/node_modules/@babel/helpers/lib/helpers/superPropBase.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/checkInRHS.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/classStaticPrivateFieldDestructureSet.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/defineProperty.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/taggedTemplateLiteral.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/get.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/extends.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/awaitAsyncGenerator.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/regeneratorAsyncGen.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/iterableToArrayLimit.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/classStaticPrivateMethodGet.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/nonIterableRest.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/classPrivateMethodGet.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/objectSpread.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/regenerator.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/checkPrivateRedeclaration.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/callSuper.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/classExtractFieldDescriptor.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/AwaitValue.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/classStaticPrivateMethodGet.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/tsRewriteRelativeImportExtensions.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/getPrototypeOf.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/typeof.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/applyDecoratedDescriptor.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/toPropertyKey.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/classStaticPrivateMethodSet.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/importDeferProxy.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/possibleConstructorReturn.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/temporalUndefined.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/wrapAsyncGenerator.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/classNameTDZError.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/regeneratorDefine.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/applyDecs2203R.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/applyDecs2203R.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/classApplyDescriptorDestructureSet.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/classStaticPrivateFieldSpecSet.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/unsupportedIterableToArray.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/classNameTDZError.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/classCheckPrivateStaticAccess.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/assertThisInitialized.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/classCallCheck.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/wrapNativeSuper.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/classPrivateFieldGet2.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/objectSpread2.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/taggedTemplateLiteral.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/wrapRegExp.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/nonIterableSpread.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/classStaticPrivateMethodSet.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/createForOfIteratorHelperLoose.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/classPrivateMethodSet.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/skipFirstGeneratorNext.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/regeneratorAsyncGen.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/createForOfIteratorHelper.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/inheritsLoose.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/asyncGeneratorDelegate.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/set.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/superPropGet.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/asyncToGenerator.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/objectDestructuringEmpty.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/maybeArrayLike.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/importDeferProxy.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/classApplyDescriptorSet.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/classPrivateFieldGet.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/checkPrivateRedeclaration.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/defineProperty.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/regeneratorAsync.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/createClass.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/objectSpread.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/initializerWarningHelper.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/classPrivateFieldSet.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/classApplyDescriptorGet.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/classPrivateFieldInitSpec.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/extends.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/defineAccessor.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/tdz.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/maybeArrayLike.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/objectWithoutPropertiesLoose.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/wrapRegExp.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/nullishReceiverError.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/classPrivateFieldLooseBase.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/classCheckPrivateStaticAccess.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/classStaticPrivateFieldSpecGet.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/identity.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/superPropGet.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/asyncGeneratorDelegate.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/toConsumableArray.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/regeneratorValues.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/classPrivateFieldGet.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/classPrivateFieldLooseKey.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/dispose.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/asyncIterator.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/classPrivateMethodInitSpec.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/classApplyDescriptorGet.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/superPropSet.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/classStaticPrivateFieldSpecSet.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/iterableToArray.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/createForOfIteratorHelper.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/superPropSet.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/classPrivateFieldDestructureSet.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/applyDecs2305.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/typeof.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/OverloadYield.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/defineAccessor.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/classPrivateFieldSet.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/regeneratorDefine.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/toArray.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/classPrivateFieldLooseBase.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/classPrivateFieldSet2.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/possibleConstructorReturn.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/regeneratorRuntime.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/arrayWithoutHoles.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/classApplyDescriptorSet.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/classPrivateMethodInitSpec.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/applyDecs2311.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/callSuper.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/inherits.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/assertThisInitialized.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/classPrivateFieldSet2.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/skipFirstGeneratorNext.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/objectWithoutProperties.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/usingCtx.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/asyncIterator.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/nonIterableRest.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/applyDecs2301.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/regeneratorValues.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/assertClassBrand.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/newArrowCheck.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/decorate.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/tsRewriteRelativeImportExtensions.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/arrayWithHoles.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/classCheckPrivateStaticFieldDescriptor.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/instanceof.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/regeneratorAsyncIterator.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/inheritsLoose.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/readOnlyError.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/regeneratorAsync.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/regeneratorKeys.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/get.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/applyDecs2305.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/using.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/interopRequireDefault.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/taggedTemplateLiteralLoose.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/applyDecs2301.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/regeneratorRuntime.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/interopRequireWildcard.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/arrayWithoutHoles.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/defineEnumerableProperties.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/classCheckPrivateStaticFieldDescriptor.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/superPropBase.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/classPrivateGetter.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/applyDecs2203.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/jsx.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/applyDecs2311.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/toSetter.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/asyncToGenerator.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/instanceof.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/set.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/decorate.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/createClass.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/classPrivateFieldGet2.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/iterableToArray.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/objectDestructuringEmpty.js
    ./frontend/node_modules/@babel/helpers/lib/helpers/unsupportedIterableToArray.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/classPrivateFieldInitSpec.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/jsx.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/construct.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers/interopRequireDefault.js
    ./frontend/node_modules/@babel/helpers/lib/index.js.map
    ./frontend/node_modules/@babel/helpers/lib/index.js
    ./frontend/node_modules/@babel/helpers/lib/helpers-generated.js.map
    ./frontend/node_modules/@babel/helpers/lib/helpers-generated.js
    ./frontend/node_modules/@babel/helpers/package.json
    ./frontend/node_modules/@babel/helpers/README.md
    ./frontend/node_modules/@babel/helpers/LICENSE
    ./frontend/node_modules/eslint/lib/cli-engine/formatters/formatters-meta.json
    ./frontend/node_modules/eslint/lib/cli-engine/formatters/json.js
    ./frontend/node_modules/eslint/lib/cli-engine/formatters/json-with-metadata.js
    ./frontend/node_modules/eslint/lib/cli-engine/formatters/stylish.js
    ./frontend/node_modules/eslint/lib/cli-engine/formatters/html.js
    ./frontend/node_modules/eslint/lib/cli-engine/index.js
    ./frontend/node_modules/eslint/lib/cli-engine/lint-result-cache.js
    ./frontend/node_modules/eslint/lib/cli-engine/load-rules.js
    ./frontend/node_modules/eslint/lib/unsupported-api.js
    ./frontend/node_modules/@vitest/utils/dist/source-map/node.d.ts
    ./frontend/node_modules/@vitest/utils/dist/source-map/node.js
    ./frontend/node_modules/@vitest/utils/dist/resolver.d.ts
    ./frontend/node_modules/@vitest/utils/dist/helpers.js
    ./frontend/node_modules/@vitest/utils/dist/source-map.js
    ./frontend/node_modules/@vitest/utils/dist/offset.d.ts
    ./frontend/node_modules/@vitest/utils/dist/chunk-pathe.M-eThtNZ.js
    ./frontend/node_modules/@vitest/utils/dist/timers.js
    ./frontend/node_modules/@vitest/utils/dist/display.d.ts
    ./frontend/node_modules/@vitest/utils/dist/error.js
    ./frontend/node_modules/@vitest/utils/dist/index.js
    ./frontend/node_modules/@vitest/utils/dist/timers.d.ts
    ./frontend/node_modules/@vitest/utils/dist/serialize.js
    ./frontend/node_modules/@vitest/utils/dist/types.d.ts
    ./frontend/node_modules/@vitest/utils/dist/offset.js
    ./frontend/node_modules/@vitest/utils/dist/types.js
    ./frontend/node_modules/@vitest/utils/dist/display.js
    ./frontend/node_modules/@vitest/utils/dist/error.d.ts
    ./frontend/node_modules/@vitest/utils/dist/serialize.d.ts
    ./frontend/node_modules/@vitest/utils/dist/diff.d.ts
    ./frontend/node_modules/@vitest/utils/dist/constants.d.ts
    ./frontend/node_modules/@vitest/utils/dist/constants.js
    ./frontend/node_modules/@vitest/utils/LICENSE
    ./frontend/node_modules/@vitest/utils/error.d.ts
    ./frontend/node_modules/@vitest/utils/diff.d.ts
    ./frontend/node_modules/symbol-tree/lib/SymbolTreeNode.js
    ./frontend/node_modules/symbol-tree/lib/SymbolTree.js
    ./frontend/node_modules/@vitest/pretty-format/dist/index.d.ts
    ./frontend/node_modules/@vitest/pretty-format/dist/index.js
    ./frontend/node_modules/@vitest/pretty-format/LICENSE
    ./frontend/node_modules/@babel/compat-data/native-modules.js
    ./frontend/node_modules/.tmp/tsconfig.node.tsbuildinfo
    ./frontend/node_modules/.tmp/tsconfig.app.tsbuildinfo
    ./frontend/node_modules/symbol-tree/lib/TreeIterator.js
    ./frontend/node_modules/symbol-tree/lib/TreePosition.js
    ./frontend/node_modules/symbol-tree/package.json
    ./frontend/node_modules/symbol-tree/README.md
    ./frontend/node_modules/symbol-tree/LICENSE
    ./frontend/node_modules/@testing-library/jest-dom/types/__tests__/jest/jest-types.test.ts
    ./frontend/node_modules/@testing-library/jest-dom/types/__tests__/jest/tsconfig.json
    ./frontend/node_modules/@testing-library/jest-dom/types/__tests__/jest/jest-custom-expect-types.test.ts
    ./frontend/node_modules/@vitest/runner/utils.d.ts
    ./frontend/node_modules/@vitest/runner/package.json
    ./frontend/node_modules/@vitest/runner/README.md
    ./frontend/node_modules/@vitest/runner/types.d.ts
    ./frontend/node_modules/eslint/lib/rules/utils/fix-tracker.js
    ./frontend/node_modules/eslint/lib/rules/utils/lazy-loading-rule-map.js
    ./frontend/node_modules/@vitest/mocker/package.json
    ./frontend/node_modules/eslint/lib/rules/utils/char-source.js
    ./frontend/node_modules/@vitest/mocker/README.md
    ./frontend/node_modules/eslint/lib/rules/utils/ast-utils.js
    ./frontend/node_modules/why-is-node-running/include.js
    ./frontend/node_modules/@testing-library/jest-dom/types/__tests__/bun/bun-types.test.ts
    ./frontend/node_modules/why-is-node-running/cli.js
    ./frontend/node_modules/why-is-node-running/example.js
    ./frontend/node_modules/@testing-library/jest-dom/types/__tests__/bun/tsconfig.json
    ./frontend/node_modules/@testing-library/jest-dom/types/__tests__/bun/bun-custom-expect-types.test.ts
    ./frontend/node_modules/@babel/compat-data/data/plugins.json
    ./frontend/node_modules/@vitest/runner/dist/chunk-artifact.js
    ./frontend/node_modules/@babel/compat-data/data/plugin-bugfixes.json
    ./frontend/node_modules/@babel/compat-data/data/native-modules.json
    ./frontend/node_modules/@babel/compat-data/data/corejs3-shipped-proposals.json
    ./frontend/node_modules/@babel/compat-data/data/overlapping-plugins.json
    ./frontend/node_modules/@babel/compat-data/data/corejs2-built-ins.json
    ./frontend/node_modules/@vitest/runner/dist/index.d.ts
    ./frontend/node_modules/@vitest/runner/dist/utils.js
    ./frontend/node_modules/@vitest/runner/dist/utils.d.ts
    ./frontend/node_modules/@vitest/runner/dist/tasks.d-DI5LbrqA.d.ts
    ./frontend/node_modules/@vitest/runner/dist/index.js
    ./frontend/node_modules/@vitest/runner/dist/types.d.ts
    ./frontend/node_modules/@vitest/runner/dist/types.js
    ./frontend/node_modules/@babel/compat-data/corejs2-built-ins.js
    ./frontend/node_modules/@babel/compat-data/package.json
    ./frontend/node_modules/@babel/compat-data/corejs3-shipped-proposals.js
    ./frontend/node_modules/@babel/compat-data/README.md
    ./frontend/node_modules/@babel/compat-data/plugins.js
    ./frontend/node_modules/@babel/compat-data/overlapping-plugins.js
    ./frontend/node_modules/@babel/compat-data/LICENSE
    ./frontend/node_modules/@babel/compat-data/plugin-bugfixes.js
    ./frontend/node_modules/@vitest/runner/LICENSE
    ./frontend/node_modules/fast-levenshtein/levenshtein.js
    ./frontend/node_modules/fast-levenshtein/package.json
    ./frontend/node_modules/fast-levenshtein/README.md
    ./frontend/node_modules/fast-levenshtein/LICENSE.md
    ./frontend/node_modules/why-is-node-running/.github/FUNDING.yml
    ./frontend/node_modules/why-is-node-running/package.json
    ./frontend/node_modules/why-is-node-running/README.md
    ./frontend/node_modules/why-is-node-running/index.js
    ./frontend/node_modules/why-is-node-running/LICENSE
    ./frontend/node_modules/@testing-library/jest-dom/types/__tests__/jest-globals/tsconfig.json
    ./frontend/node_modules/@testing-library/jest-dom/types/__tests__/jest-globals/jest-globals-types.test.ts
    ./frontend/node_modules/@testing-library/jest-dom/types/__tests__/jest-globals/jest-globals-custom-expect-types.test.ts
    ./frontend/node_modules/@vitest/mocker/dist/browser.d.ts
    ./frontend/node_modules/@vitest/mocker/dist/automock.d.ts
    ./frontend/node_modules/@vitest/mocker/dist/redirect.d.ts
    ./frontend/node_modules/@vitest/mocker/dist/node.d.ts
    ./frontend/node_modules/@vitest/mocker/dist/automock.js
    ./frontend/node_modules/@vitest/mocker/dist/browser.js
    ./frontend/node_modules/@vitest/mocker/dist/index.d.ts
    ./frontend/node_modules/@vitest/mocker/dist/types.d-BjI5eAwu.d.ts
    ./frontend/node_modules/@vitest/mocker/dist/index.d-B41z0AuW.d.ts
    ./frontend/node_modules/@vitest/mocker/dist/chunk-interceptor-native.js
    ./frontend/node_modules/@vitest/mocker/dist/auto-register.d.ts
    ./frontend/node_modules/@vitest/mocker/dist/register.d.ts
    ./frontend/node_modules/@vitest/mocker/dist/chunk-hoistMocks.js
    ./frontend/node_modules/@vitest/mocker/dist/chunk-pathe.M-eThtNZ.js
    ./frontend/node_modules/@vitest/mocker/dist/node.js
    ./frontend/node_modules/@vitest/mocker/dist/chunk-registry.js
    ./frontend/node_modules/@vitest/mocker/dist/transforms.d.ts
    ./frontend/node_modules/@vitest/mocker/dist/chunk-utils.js
    ./frontend/node_modules/@vitest/mocker/dist/auto-register.js
    ./frontend/node_modules/@vitest/mocker/dist/chunk-automock.js
    ./frontend/node_modules/@vitest/mocker/dist/register.js
    ./frontend/node_modules/@vitest/mocker/dist/index.js
    ./frontend/node_modules/@vitest/mocker/dist/transforms.js
    ./frontend/node_modules/@vitest/mocker/dist/hoistMocks.d-w2ILr1dG.d.ts
    ./frontend/node_modules/@vitest/mocker/dist/chunk-helpers.js
    ./frontend/node_modules/@vitest/mocker/dist/chunk-mocker.js
    ./frontend/node_modules/@vitest/mocker/dist/mocker.d-QEntlm6J.d.ts
    ./frontend/node_modules/@vitest/mocker/dist/redirect.js
    ./frontend/node_modules/@vitest/mocker/LICENSE
    ./frontend/node_modules/cookie/package.json
    ./frontend/node_modules/cookie/README.md
    ./frontend/node_modules/@vitest/snapshot/environment.d.ts
    ./frontend/node_modules/@vitest/snapshot/manager.d.ts
    ./frontend/node_modules/@vitest/snapshot/package.json
    ./frontend/node_modules/@vitest/snapshot/README.md
    ./frontend/node_modules/@testing-library/jest-dom/types/__tests__/vitest/vitest-types.test.ts
    ./frontend/node_modules/@testing-library/jest-dom/types/__tests__/vitest/tsconfig.json
    ./frontend/node_modules/@testing-library/jest-dom/types/__tests__/vitest/vitest-custom-expect-types.test.ts
    ./frontend/node_modules/@testing-library/jest-dom/types/matchers.d.ts
    ./frontend/node_modules/@testing-library/jest-dom/types/bun.d.ts
    ./frontend/node_modules/@testing-library/jest-dom/types/vitest.d.ts
    ./frontend/node_modules/@testing-library/jest-dom/types/jest.d.ts
    ./frontend/node_modules/@testing-library/jest-dom/vitest.js
    ./frontend/node_modules/eslint/lib/rules/no-useless-computed-key.js
    ./frontend/node_modules/eslint/lib/rules/utils/unicode/is-emoji-modifier.js
    ./frontend/node_modules/eslint/lib/rules/no-misleading-character-class.js
    ./frontend/node_modules/eslint/lib/rules/no-dupe-args.js
    ./frontend/node_modules/eslint/lib/rules/max-depth.js
    ./frontend/node_modules/eslint/lib/rules/no-octal-escape.js
    ./frontend/node_modules/eslint/lib/rules/no-dupe-class-members.js
    ./frontend/node_modules/eslint/lib/rules/require-await.js
    ./frontend/node_modules/eslint/lib/rules/no-return-assign.js
    ./frontend/node_modules/eslint/lib/rules/no-sync.js
    ./frontend/node_modules/eslint/lib/rules/no-underscore-dangle.js
    ./frontend/node_modules/eslint/lib/rules/no-multiple-empty-lines.js
    ./frontend/node_modules/eslint/lib/rules/comma-spacing.js
    ./frontend/node_modules/eslint/lib/rules/sort-imports.js
    ./frontend/node_modules/eslint/lib/rules/prefer-destructuring.js
    ./frontend/node_modules/eslint/lib/rules/no-template-curly-in-string.js
    ./frontend/node_modules/eslint/lib/rules/prefer-rest-params.js
    ./frontend/node_modules/eslint/lib/rules/no-regex-spaces.js
    ./frontend/node_modules/eslint/lib/rules/lines-around-directive.js
    ./frontend/node_modules/eslint/lib/rules/new-cap.js
    ./frontend/node_modules/eslint/lib/rules/max-nested-callbacks.js
    ./frontend/node_modules/eslint/lib/rules/dot-location.js
    ./frontend/node_modules/eslint/lib/rules/wrap-regex.js
    ./frontend/node_modules/eslint/lib/rules/no-restricted-globals.js
    ./frontend/node_modules/eslint/lib/rules/no-delete-var.js
    ./frontend/node_modules/eslint/lib/rules/no-useless-return.js
    ./frontend/node_modules/eslint/lib/rules/unicode-bom.js
    ./frontend/node_modules/eslint/lib/rules/no-bitwise.js
    ./frontend/node_modules/eslint/lib/rules/max-classes-per-file.js
    ./frontend/node_modules/eslint/lib/rules/no-unused-private-class-members.js
    ./frontend/node_modules/eslint/lib/rules/no-promise-executor-return.js
    ./frontend/node_modules/eslint/lib/rules/multiline-ternary.js
    ./frontend/node_modules/eslint/lib/rules/max-statements-per-line.js
    ./frontend/node_modules/eslint/lib/rules/no-multi-str.js
    ./frontend/node_modules/eslint/lib/rules/utils/unicode/is-regional-indicator-symbol.js
    ./frontend/node_modules/eslint/lib/rules/utils/unicode/is-combining-character.js
    ./frontend/node_modules/eslint/lib/rules/no-script-url.js
    ./frontend/node_modules/eslint/lib/rules/no-negated-condition.js
    ./frontend/node_modules/eslint/lib/rules/utils/unicode/index.js
    ./frontend/node_modules/eslint/lib/rules/constructor-super.js
    ./frontend/node_modules/eslint/lib/rules/utils/unicode/is-surrogate-pair.js
    ./frontend/node_modules/eslint/lib/rules/no-empty-static-block.js
    ./frontend/node_modules/eslint/lib/rules/no-with.js
    ./frontend/node_modules/eslint/lib/rules/one-var-declaration-per-line.js
    ./frontend/node_modules/eslint/lib/rules/no-multi-assign.js
    ./frontend/node_modules/eslint/lib/rules/object-property-newline.js
    ./frontend/node_modules/eslint/lib/rules/grouped-accessor-pairs.js
    ./frontend/node_modules/eslint/lib/rules/no-self-compare.js
    ./frontend/node_modules/eslint/lib/rules/no-trailing-spaces.js
    ./frontend/node_modules/eslint/lib/rules/no-inline-comments.js
    ./frontend/node_modules/eslint/lib/rules/no-class-assign.js
    ./frontend/node_modules/eslint/lib/rules/no-return-await.js
    ./frontend/node_modules/eslint/lib/rules/space-in-parens.js
    ./frontend/node_modules/eslint/lib/rules/utils/regular-expressions.js
    ./frontend/node_modules/eslint/lib/rules/no-console.js
    ./frontend/node_modules/eslint/lib/rules/utils/keywords.js
    ./frontend/node_modules/eslint/lib/rules/no-extra-parens.js
    ./frontend/node_modules/eslint/lib/rules/prefer-const.js
    ./frontend/node_modules/eslint/lib/rules/no-useless-catch.js
    ./frontend/node_modules/eslint/lib/rules/generator-star-spacing.js
    ./frontend/node_modules/eslint/lib/rules/prefer-arrow-callback.js
    ./frontend/node_modules/eslint/lib/rules/eqeqeq.js
    ./frontend/node_modules/eslint/lib/rules/global-require.js
    ./frontend/node_modules/eslint/lib/rules/no-unreachable-loop.js
    ./frontend/node_modules/eslint/lib/rules/object-curly-spacing.js
    ./frontend/node_modules/eslint/lib/rules/prefer-exponentiation-operator.js
    ./frontend/node_modules/eslint/lib/rules/no-redeclare.js
    ./frontend/node_modules/eslint/lib/rules/index.js
    ./frontend/node_modules/eslint/lib/rules/no-mixed-spaces-and-tabs.js
    ./frontend/node_modules/eslint/lib/rules/comma-dangle.js
    ./frontend/node_modules/eslint/lib/rules/no-else-return.js
    ./frontend/node_modules/eslint/lib/rules/no-extra-bind.js
    ./frontend/node_modules/eslint/lib/rules/no-iterator.js
    ./frontend/node_modules/eslint/lib/rules/sort-keys.js
    ./frontend/node_modules/eslint/lib/rules/no-func-assign.js
    ./frontend/node_modules/eslint/lib/rules/no-continue.js
    ./frontend/node_modules/eslint/lib/rules/no-constructor-return.js
    ./frontend/node_modules/eslint/lib/rules/indent.js
    ./frontend/node_modules/eslint/lib/rules/max-lines.js
    ./frontend/node_modules/eslint/lib/rules/no-undefined.js
    ./frontend/node_modules/eslint/lib/rules/comma-style.js
    ./frontend/node_modules/eslint/lib/rules/prefer-object-spread.js
    ./frontend/node_modules/eslint/lib/rules/no-this-before-super.js
    ./frontend/node_modules/eslint/lib/rules/no-import-assign.js
    ./frontend/node_modules/eslint/lib/rules/no-shadow-restricted-names.js
    ./frontend/node_modules/eslint/lib/rules/no-empty.js
    ./frontend/node_modules/eslint/lib/rules/getter-return.js
    ./frontend/node_modules/eslint/lib/rules/new-parens.js
    ./frontend/node_modules/eslint/lib/rules/no-lone-blocks.js
    ./frontend/node_modules/eslint/lib/rules/keyword-spacing.js
    ./frontend/node_modules/eslint/lib/rules/prefer-spread.js
    ./frontend/node_modules/eslint/lib/rules/max-statements.js
    ./frontend/node_modules/eslint/lib/rules/no-debugger.js
    ./frontend/node_modules/eslint/lib/rules/id-blacklist.js
    ./frontend/node_modules/eslint/lib/rules/no-use-before-define.js
    ./frontend/node_modules/eslint/lib/rules/no-unneeded-ternary.js
    ./frontend/node_modules/eslint/lib/rules/no-restricted-imports.js
    ./frontend/node_modules/eslint/lib/rules/func-names.js
    ./frontend/node_modules/eslint/lib/rules/arrow-spacing.js
    ./frontend/node_modules/eslint/lib/rules/no-tabs.js
    ./frontend/node_modules/eslint/lib/rules/no-mixed-requires.js
    ./frontend/node_modules/eslint/lib/rules/array-bracket-spacing.js
    ./frontend/node_modules/eslint/lib/rules/rest-spread-spacing.js
    ./frontend/node_modules/eslint/lib/rules/no-cond-assign.js
    ./frontend/node_modules/eslint/lib/rules/template-tag-spacing.js
    ./frontend/node_modules/eslint/lib/rules/handle-callback-err.js
    ./frontend/node_modules/eslint/lib/rules/no-ex-assign.js
    ./frontend/node_modules/eslint/lib/languages/js/index.js
    ./frontend/node_modules/eslint/lib/languages/js/validate-language-options.js
    ./frontend/node_modules/eslint/lib/languages/js/source-code/source-code.js
    ./frontend/node_modules/eslint/lib/languages/js/source-code/index.js
    ./frontend/node_modules/eslint/lib/rules/accessor-pairs.js
    ./frontend/node_modules/eslint/lib/rules/no-global-assign.js
    ./frontend/node_modules/eslint/lib/rules/no-constant-binary-expression.js
    ./frontend/node_modules/eslint/lib/rules/radix.js
    ./frontend/node_modules/eslint/lib/rules/max-lines-per-function.js
    ./frontend/node_modules/eslint/lib/rules/no-useless-backreference.js
    ./frontend/node_modules/eslint/lib/rules/logical-assignment-operators.js
    ./frontend/node_modules/eslint/lib/rules/no-control-regex.js
    ./frontend/node_modules/eslint/lib/rules/brace-style.js
    ./frontend/node_modules/eslint/lib/rules/no-loss-of-precision.js
    ./frontend/node_modules/eslint/lib/rules/prefer-template.js
    ./frontend/node_modules/eslint/lib/rules/prefer-reflect.js
    ./frontend/node_modules/eslint/lib/rules/no-labels.js
    ./frontend/node_modules/eslint/lib/rules/no-throw-literal.js
    ./frontend/node_modules/eslint/lib/rules/no-unsafe-finally.js
    ./frontend/node_modules/eslint/lib/rules/no-plusplus.js
    ./frontend/node_modules/eslint/lib/rules/prefer-regex-literals.js
    ./frontend/node_modules/eslint/lib/rules/yoda.js
    ./frontend/node_modules/eslint/lib/rules/object-shorthand.js
    ./frontend/node_modules/eslint/lib/rules/no-duplicate-case.js
    ./frontend/node_modules/eslint/lib/rules/no-whitespace-before-property.js
    ./frontend/node_modules/eslint/lib/rules/no-sequences.js
    ./frontend/node_modules/eslint/lib/rules/no-restricted-modules.js
    ./frontend/node_modules/eslint/lib/rules/prefer-numeric-literals.js
    ./frontend/node_modules/eslint/lib/rules/no-async-promise-executor.js
    ./frontend/node_modules/eslint/lib/rules/linebreak-style.js
    ./frontend/node_modules/eslint/lib/rules/no-unsafe-negation.js
    ./frontend/node_modules/eslint/lib/rules/no-unused-vars.js
    ./frontend/node_modules/eslint/lib/rules/no-sparse-arrays.js
    ./frontend/node_modules/eslint/lib/rules/capitalized-comments.js
    ./frontend/node_modules/eslint/lib/rules/func-style.js
    ./frontend/node_modules/eslint/lib/rules/no-alert.js
    ./frontend/node_modules/eslint/lib/rules/newline-after-var.js
    ./frontend/node_modules/eslint/lib/rules/id-denylist.js
    ./frontend/node_modules/eslint/lib/rules/template-curly-spacing.js
    ./frontend/node_modules/eslint/lib/rules/default-param-last.js
    ./frontend/node_modules/eslint/lib/rules/jsx-quotes.js
    ./frontend/node_modules/eslint/lib/rules/callback-return.js
    ./frontend/node_modules/eslint/lib/rules/block-scoped-var.js
    ./frontend/node_modules/eslint/lib/rules/symbol-description.js
    ./frontend/node_modules/eslint/lib/rules/key-spacing.js
    ./frontend/node_modules/eslint/lib/rules/default-case.js
    ./frontend/node_modules/eslint/lib/rules/no-spaced-func.js
    ./frontend/node_modules/eslint/lib/rules/no-extra-boolean-cast.js
    ./frontend/node_modules/eslint/lib/rules/quotes.js
    ./frontend/node_modules/eslint/lib/rules/no-nested-ternary.js
    ./frontend/node_modules/eslint/lib/rules/operator-assignment.js
    ./frontend/node_modules/eslint/lib/rules/no-inner-declarations.js
    ./frontend/node_modules/eslint/lib/rules/no-duplicate-imports.js
    ./frontend/node_modules/eslint/lib/rules/switch-colon-spacing.js
    ./frontend/node_modules/eslint/lib/rules/consistent-return.js
    ./frontend/node_modules/eslint/lib/rules/no-caller.js
    ./frontend/node_modules/eslint/lib/rules/no-unsafe-optional-chaining.js
    ./frontend/node_modules/eslint/lib/rules/id-length.js
    ./frontend/node_modules/eslint/lib/rules/no-useless-call.js
    ./frontend/node_modules/eslint/lib/rules/no-catch-shadow.js
    ./frontend/node_modules/eslint/lib/rules/no-prototype-builtins.js
    ./frontend/node_modules/eslint/lib/rules/block-spacing.js
    ./frontend/node_modules/esquery/parser.js
    ./frontend/node_modules/eslint/lib/rules/require-atomic-updates.js
    ./frontend/node_modules/cookie/dist/index.d.ts
    ./frontend/node_modules/eslint/lib/rules/no-path-concat.js
    ./frontend/node_modules/esquery/license.txt
    ./frontend/node_modules/cookie/dist/index.js.map
    ./frontend/node_modules/esquery/package.json
    ./frontend/node_modules/cookie/dist/index.js
    ./frontend/node_modules/esquery/README.md
    ./frontend/node_modules/eslint/lib/rules/no-unexpected-multiline.js
    ./frontend/node_modules/eslint/lib/rules/no-useless-constructor.js
    ./frontend/node_modules/eslint/lib/rules/semi.js
    ./frontend/node_modules/eslint/lib/rules/no-empty-function.js
    ./frontend/node_modules/eslint/lib/rules/no-confusing-arrow.js
    ./frontend/node_modules/eslint/lib/rules/no-new-require.js
    ./frontend/node_modules/eslint/lib/rules/space-before-blocks.js
    ./frontend/node_modules/eslint/lib/rules/require-yield.js
    ./frontend/node_modules/eslint/lib/rules/no-undef-init.js
    ./frontend/node_modules/eslint/lib/rules/newline-per-chained-call.js
    ./frontend/node_modules/eslint/lib/rules/no-invalid-regexp.js
    ./frontend/node_modules/eslint/lib/rules/valid-typeof.js
    ./frontend/node_modules/eslint/lib/rules/no-unreachable.js
    ./frontend/node_modules/cookie/LICENSE
    ./frontend/node_modules/eslint/lib/rules/no-process-env.js
    ./frontend/node_modules/eslint/lib/rules/no-void.js
    ./frontend/node_modules/eslint/lib/rules/quote-props.js
    ./frontend/node_modules/eslint/lib/rules/no-invalid-this.js
    ./frontend/node_modules/eslint/lib/rules/no-new-func.js
    ./frontend/node_modules/eslint/lib/rules/no-restricted-exports.js
    ./frontend/node_modules/eslint/lib/rules/camelcase.js
    ./frontend/node_modules/eslint/lib/rules/no-implicit-coercion.js
    ./frontend/node_modules/eslint/lib/rules/no-unused-expressions.js
    ./frontend/node_modules/eslint/lib/rules/no-restricted-syntax.js
    ./frontend/node_modules/eslint/lib/rules/no-await-in-loop.js
    ./frontend/node_modules/eslint/lib/rules/init-declarations.js
    ./frontend/node_modules/eslint/lib/rules/line-comment-position.js
    ./frontend/node_modules/caniuse-lite/data/features/testfeat.js
    ./frontend/node_modules/caniuse-lite/data/features/hevc.js
    ./frontend/node_modules/caniuse-lite/data/features/css-background-offsets.js
    ./frontend/node_modules/caniuse-lite/data/features/webworkers.js
    ./frontend/node_modules/caniuse-lite/data/features/rtcpeerconnection.js
    ./frontend/node_modules/caniuse-lite/data/features/css-autofill.js
    ./frontend/node_modules/caniuse-lite/data/features/filereadersync.js
    ./frontend/node_modules/caniuse-lite/data/features/css-grid.js
    ./frontend/node_modules/caniuse-lite/data/features/asmjs.js
    ./frontend/node_modules/caniuse-lite/data/features/http3.js
    ./frontend/node_modules/caniuse-lite/data/features/object-values.js
    ./frontend/node_modules/caniuse-lite/data/features/mediasource.js
    ./frontend/node_modules/caniuse-lite/data/features/css-marker-pseudo.js
    ./frontend/node_modules/caniuse-lite/data/features/es6-number.js
    ./frontend/node_modules/caniuse-lite/data/features/css-overflow.js
    ./frontend/node_modules/caniuse-lite/data/features.js
    ./frontend/node_modules/caniuse-lite/data/agents.js
    ./frontend/node_modules/pretty-format/build/index.d.ts
    ./frontend/node_modules/pretty-format/build/collections.js
    ./frontend/node_modules/pretty-format/build/index.js
    ./frontend/node_modules/pretty-format/build/types.d.ts
    ./frontend/node_modules/@vitest/snapshot/dist/rawSnapshot.d-U2kJUxDr.d.ts
    ./frontend/node_modules/@vitest/snapshot/dist/environment.js
    ./frontend/node_modules/@vitest/snapshot/dist/environment.d-DOJxxZV9.d.ts
    ./frontend/node_modules/@vitest/snapshot/dist/environment.d.ts
    ./frontend/node_modules/@vitest/snapshot/dist/index.d.ts
    ./frontend/node_modules/@vitest/snapshot/dist/manager.d.ts
    ./frontend/node_modules/@vitest/snapshot/dist/manager.js
    ./frontend/node_modules/@vitest/snapshot/dist/index.js
    ./frontend/node_modules/@vitest/snapshot/LICENSE
    ./frontend/node_modules/@testing-library/react/package.json
    ./frontend/node_modules/@testing-library/react/dont-cleanup-after-each.js
    ./frontend/node_modules/@testing-library/react/README.md
    ./frontend/node_modules/caniuse-lite/data/features/font-loading.js
    ./frontend/node_modules/caniuse-lite/data/features/css-supports-api.js
    ./frontend/node_modules/caniuse-lite/data/features/border-image.js
    ./frontend/node_modules/caniuse-lite/data/features/transforms2d.js
    ./frontend/node_modules/caniuse-lite/data/features/magnetometer.js
    ./frontend/node_modules/caniuse-lite/data/features/unhandledrejection.js
    ./frontend/node_modules/caniuse-lite/data/features/css-transitions.js
    ./frontend/node_modules/caniuse-lite/data/features/document-scrollingelement.js
    ./frontend/node_modules/caniuse-lite/data/features/offscreencanvas.js
    ./frontend/node_modules/caniuse-lite/data/features/webkit-user-drag.js
    ./frontend/node_modules/caniuse-lite/data/features/speech-recognition.js
    ./frontend/node_modules/caniuse-lite/data/features/web-animation.js
    ./frontend/node_modules/caniuse-lite/data/features/wasm-bulk-memory.js
    ./frontend/node_modules/caniuse-lite/data/features/wasm-mutable-globals.js
    ./frontend/node_modules/caniuse-lite/data/features/import-maps.js
    ./frontend/node_modules/caniuse-lite/data/features/css-scrollbar.js
    ./frontend/node_modules/caniuse-lite/data/features/css-opacity.js
    ./frontend/node_modules/caniuse-lite/data/features/subresource-bundling.js
    ./frontend/node_modules/caniuse-lite/data/features/opus.js
    ./frontend/node_modules/caniuse-lite/data/features/transforms3d.js
    ./frontend/node_modules/caniuse-lite/data/features/css-placeholder-shown.js
    ./frontend/node_modules/caniuse-lite/data/features/ogv.js
    ./frontend/node_modules/caniuse-lite/data/features/css-unicode-bidi.js
    ./frontend/node_modules/caniuse-lite/data/features/fullscreen.js
    ./frontend/node_modules/caniuse-lite/data/features/arrow-functions.js
    ./frontend/node_modules/caniuse-lite/data/features/scrollintoview.js
    ./frontend/node_modules/@babel/helper-module-imports/lib/import-injector.js.map
    ./frontend/node_modules/caniuse-lite/data/features/media-fragments.js
    ./frontend/node_modules/@babel/helper-module-imports/lib/index.js.map
    ./frontend/node_modules/caniuse-lite/data/features/wav.js
    ./frontend/node_modules/@babel/helper-module-imports/lib/is-module.js
    ./frontend/node_modules/@babel/helper-module-imports/lib/index.js
    ./frontend/node_modules/caniuse-lite/data/features/css-color-function.js
    ./frontend/node_modules/caniuse-lite/data/features/cryptography.js
    ./frontend/node_modules/caniuse-lite/data/features/touch.js
    ./frontend/node_modules/@babel/helper-module-imports/lib/import-injector.js
    ./frontend/node_modules/caniuse-lite/data/features/wasm-multi-value.js
    ./frontend/node_modules/@babel/helper-module-imports/lib/import-builder.js.map
    ./frontend/node_modules/caniuse-lite/data/features/css-nth-child-of.js
    ./frontend/node_modules/@babel/helper-module-imports/lib/import-builder.js
    ./frontend/node_modules/@babel/helper-module-imports/lib/is-module.js.map
    ./frontend/node_modules/caniuse-lite/data/features/custom-elementsv1.js
    ./frontend/node_modules/caniuse-lite/data/features/css-not-sel-list.js
    ./frontend/node_modules/caniuse-lite/data/features/template.js
    ./frontend/node_modules/caniuse-lite/data/features/offline-apps.js
    ./frontend/node_modules/caniuse-lite/data/features/input-event.js
    ./frontend/node_modules/caniuse-lite/data/features/client-hints-dpr-width-viewport.js
    ./frontend/node_modules/caniuse-lite/data/features/calc.js
    ./frontend/node_modules/caniuse-lite/data/features/picture-in-picture.js
    ./frontend/node_modules/@babel/helper-module-imports/package.json
    ./frontend/node_modules/caniuse-lite/data/features/screen-orientation.js
    ./frontend/node_modules/@babel/helper-module-imports/README.md
    ./frontend/node_modules/@babel/helper-module-imports/LICENSE
    ./frontend/node_modules/caniuse-lite/data/features/css-line-clamp.js
    ./frontend/node_modules/caniuse-lite/data/features/dispatchevent.js
    ./frontend/node_modules/caniuse-lite/data/features/intl-pluralrules.js
    ./frontend/node_modules/caniuse-lite/data/features/mdn-css-unicode-bidi-plaintext.js
    ./frontend/node_modules/caniuse-lite/data/features/heif.js
    ./frontend/node_modules/caniuse-lite/data/features/intrinsic-width.js
    ./frontend/node_modules/caniuse-lite/data/features/maxlength.js
    ./frontend/node_modules/caniuse-lite/data/features/input-email-tel-url.js
    ./frontend/node_modules/caniuse-lite/data/features/wasm-tail-calls.js
    ./frontend/node_modules/caniuse-lite/data/features/brotli.js
    ./frontend/node_modules/caniuse-lite/data/features/css-letter-spacing.js
    ./frontend/node_modules/caniuse-lite/data/features/border-radius.js
    ./frontend/node_modules/caniuse-lite/data/features/notifications.js
    ./frontend/node_modules/caniuse-lite/data/features/css-first-line.js
    ./frontend/node_modules/caniuse-lite/data/features/css-first-letter.js
    ./frontend/node_modules/caniuse-lite/data/features/input-datetime.js
    ./frontend/node_modules/caniuse-lite/data/features/css-display-contents.js
    ./frontend/node_modules/caniuse-lite/data/features/array-flat.js
    ./frontend/node_modules/caniuse-lite/data/features/script-async.js
    ./frontend/node_modules/caniuse-lite/data/features/css-at-counter-style.js
    ./frontend/node_modules/caniuse-lite/data/features/css-boxdecorationbreak.js
    ./frontend/node_modules/caniuse-lite/data/features/spdy.js
    ./frontend/node_modules/caniuse-lite/data/features/accelerometer.js
    ./frontend/node_modules/caniuse-lite/data/features/alternate-stylesheet.js
    ./frontend/node_modules/caniuse-lite/data/features/wasm-simd.js
    ./frontend/node_modules/caniuse-lite/data/features/css-cascade-layers.js
    ./frontend/node_modules/caniuse-lite/data/features/webvtt.js
    ./frontend/node_modules/caniuse-lite/data/features/input-file-accept.js
    ./frontend/node_modules/caniuse-lite/data/features/pad-start-end.js
    ./frontend/node_modules/caniuse-lite/data/features/link-rel-preconnect.js
    ./frontend/node_modules/caniuse-lite/data/features/text-overflow.js
    ./frontend/node_modules/caniuse-lite/data/features/background-position-x-y.js
    ./frontend/node_modules/caniuse-lite/data/features/webauthn.js
    ./frontend/node_modules/caniuse-lite/data/features/dataset.js
    ./frontend/node_modules/caniuse-lite/data/features/css-backdrop-filter.js
    ./frontend/node_modules/caniuse-lite/data/features/mdn-css-backdrop-pseudo-element.js
    ./frontend/node_modules/caniuse-lite/data/features/url.js
    ./frontend/node_modules/caniuse-lite/data/features/font-variant-alternates.js
    ./frontend/node_modules/caniuse-lite/data/features/use-strict.js
    ./frontend/node_modules/caniuse-lite/data/features/webhid.js
    ./frontend/node_modules/caniuse-lite/data/features/css-resize.js
    ./frontend/node_modules/caniuse-lite/data/features/font-size-adjust.js
    ./frontend/node_modules/caniuse-lite/data/features/getcomputedstyle.js
    ./frontend/node_modules/caniuse-lite/data/features/insertadjacenthtml.js
    ./frontend/node_modules/caniuse-lite/data/features/localecompare.js
    ./frontend/node_modules/caniuse-lite/data/features/ambient-light.js
    ./frontend/node_modules/caniuse-lite/data/features/link-icon-svg.js
    ./frontend/node_modules/caniuse-lite/data/features/referrer-policy.js
    ./frontend/node_modules/caniuse-lite/data/features/input-color.js
    ./frontend/node_modules/caniuse-lite/data/features/css-media-resolution.js
    ./frontend/node_modules/caniuse-lite/data/features/input-pattern.js
    ./frontend/node_modules/caniuse-lite/data/features/keyboardevent-location.js
    ./frontend/node_modules/caniuse-lite/data/features/forms.js
    ./frontend/node_modules/caniuse-lite/data/features/dommatrix.js
    ./frontend/node_modules/caniuse-lite/data/features/menu.js
    ./frontend/node_modules/caniuse-lite/data/features/css-unset-value.js
    ./frontend/node_modules/caniuse-lite/data/features/input-autocomplete-onoff.js
    ./frontend/node_modules/caniuse-lite/data/features/classlist.js
    ./frontend/node_modules/caniuse-lite/data/features/serviceworkers.js
    ./frontend/node_modules/caniuse-lite/data/features/intersectionobserver-v2.js
    ./frontend/node_modules/caniuse-lite/data/features/font-kerning.js
    ./frontend/node_modules/caniuse-lite/data/features/datalist.js
    ./frontend/node_modules/caniuse-lite/data/features/online-status.js
    ./frontend/node_modules/caniuse-lite/data/features/web-bluetooth.js
    ./frontend/node_modules/caniuse-lite/data/features/cross-document-view-transitions.js
    ./frontend/node_modules/caniuse-lite/data/features/outline.js
    ./frontend/node_modules/caniuse-lite/data/features/let.js
    ./frontend/node_modules/caniuse-lite/data/features/rellist.js
    ./frontend/node_modules/caniuse-lite/data/features/text-size-adjust.js
    ./frontend/node_modules/caniuse-lite/data/features/resource-timing.js
    ./frontend/node_modules/caniuse-lite/data/features/hardwareconcurrency.js
    ./frontend/node_modules/caniuse-lite/data/features/css-indeterminate-pseudo.js
    ./frontend/node_modules/caniuse-lite/data/features/input-search.js
    ./frontend/node_modules/caniuse-lite/data/features/css-selection.js
    ./frontend/node_modules/caniuse-lite/data/features/details.js
    ./frontend/node_modules/caniuse-lite/data/features/css-appearance.js
    ./frontend/node_modules/caniuse-lite/data/features/prefers-reduced-motion.js
    ./frontend/node_modules/caniuse-lite/data/features/passive-event-listener.js
    ./frontend/node_modules/caniuse-lite/data/features/svg.js
    ./frontend/node_modules/caniuse-lite/data/features/wasm.js
    ./frontend/node_modules/caniuse-lite/data/features/pdf-viewer.js
    ./frontend/node_modules/caniuse-lite/data/features/mdn-text-decoration-shorthand.js
    ./frontend/node_modules/caniuse-lite/data/features/prefers-color-scheme.js
    ./frontend/node_modules/caniuse-lite/data/features/mediarecorder.js
    ./frontend/node_modules/caniuse-lite/data/features/element-from-point.js
    ./frontend/node_modules/caniuse-lite/data/features/link-icon-png.js
    ./frontend/node_modules/caniuse-lite/data/features/css-namespaces.js
    ./frontend/node_modules/caniuse-lite/data/features/link-rel-preload.js
    ./frontend/node_modules/caniuse-lite/data/features/background-attachment.js
    ./frontend/node_modules/caniuse-lite/data/features/css3-attr.js
    ./frontend/node_modules/caniuse-lite/data/features/selection-api.js
    ./frontend/node_modules/caniuse-lite/data/features/es6.js
    ./frontend/node_modules/caniuse-lite/data/features/css-initial-value.js
    ./frontend/node_modules/caniuse-lite/data/features/chacha20-poly1305.js
    ./frontend/node_modules/caniuse-lite/data/features/rel-noreferrer.js
    ./frontend/node_modules/eslint/lib/languages/js/source-code/token-store/limit-cursor.js
    ./frontend/node_modules/caniuse-lite/data/features/video.js
    ./frontend/node_modules/@testing-library/dom/package.json
    ./frontend/node_modules/eslint/lib/languages/js/source-code/token-store/decorative-cursor.js
    ./frontend/node_modules/caniuse-lite/data/features/json.js
    ./frontend/node_modules/eslint/lib/languages/js/source-code/token-store/skip-cursor.js
    ./frontend/node_modules/@testing-library/dom/README.md
    ./frontend/node_modules/caniuse-lite/data/features/dnssec.js
    ./frontend/node_modules/eslint/lib/languages/js/source-code/token-store/utils.js
    ./frontend/node_modules/eslint/lib/languages/js/source-code/token-store/cursor.js
    ./frontend/node_modules/eslint/lib/languages/js/source-code/token-store/forward-token-cursor.js
    ./frontend/node_modules/caniuse-lite/data/features/server-timing.js
    ./frontend/node_modules/eslint/lib/languages/js/source-code/token-store/padded-token-cursor.js
    ./frontend/node_modules/eslint/lib/languages/js/source-code/token-store/forward-token-comment-cursor.js
    ./frontend/node_modules/caniuse-lite/data/features/channel-messaging.js
    ./frontend/node_modules/eslint/lib/languages/js/source-code/token-store/index.js
    ./frontend/node_modules/eslint/lib/languages/js/source-code/token-store/filter-cursor.js
    ./frontend/node_modules/caniuse-lite/data/features/wai-aria.js
    ./frontend/node_modules/eslint/lib/languages/js/source-code/token-store/backward-token-comment-cursor.js
    ./frontend/node_modules/eslint/lib/languages/js/source-code/token-store/backward-token-cursor.js
    ./frontend/node_modules/eslint/lib/languages/js/source-code/token-store/cursors.js
    ./frontend/node_modules/caniuse-lite/data/features/registerprotocolhandler.js
    ./frontend/node_modules/caniuse-lite/data/features/wasm-relaxed-simd.js
    ./frontend/node_modules/caniuse-lite/data/features/beforeafterprint.js
    ./frontend/node_modules/caniuse-lite/data/features/deviceorientation.js
    ./frontend/node_modules/caniuse-lite/data/features/videotracks.js
    ./frontend/node_modules/caniuse-lite/data/features/proximity.js
    ./frontend/node_modules/caniuse-lite/data/features/svg-html5.js
    ./frontend/node_modules/caniuse-lite/data/features/innertext.js
    ./frontend/node_modules/caniuse-lite/data/features/speech-synthesis.js
    ./frontend/node_modules/caniuse-lite/data/features/queryselector.js
    ./frontend/node_modules/caniuse-lite/data/features/high-resolution-time.js
    ./frontend/node_modules/caniuse-lite/data/features/netinfo.js
    ./frontend/node_modules/caniuse-lite/data/features/mutation-events.js
    ./frontend/node_modules/caniuse-lite/data/features/native-filesystem-api.js
    ./frontend/node_modules/caniuse-lite/data/features/css-canvas.js
    ./frontend/node_modules/caniuse-lite/data/features/aac.js
    ./frontend/node_modules/caniuse-lite/data/features/iframe-srcdoc.js
    ./frontend/node_modules/caniuse-lite/data/features/web-serial.js
    ./frontend/node_modules/caniuse-lite/data/features/autofocus.js
    ./frontend/node_modules/caniuse-lite/data/features/createimagebitmap.js
    ./frontend/node_modules/caniuse-lite/data/features/ch-unit.js
    ./frontend/node_modules/caniuse-lite/data/features/css-motion-paths.js
    ./frontend/node_modules/caniuse-lite/data/features/pointer-events.js
    ./frontend/node_modules/caniuse-lite/data/features/css-boxshadow.js
    ./frontend/node_modules/caniuse-lite/data/features/font-smooth.js
    ./frontend/node_modules/caniuse-lite/data/features/rest-parameters.js
    ./frontend/node_modules/caniuse-lite/data/features/mdn-css-unicode-bidi-isolate.js
    ./frontend/node_modules/caniuse-lite/data/features/text-decoration.js
    ./frontend/node_modules/caniuse-lite/data/features/mpeg4.js
    ./frontend/node_modules/caniuse-lite/data/features/document-execcommand.js
    ./frontend/node_modules/caniuse-lite/data/features/eot.js
    ./frontend/node_modules/caniuse-lite/data/features/css-filters.js
    ./frontend/node_modules/caniuse-lite/data/features/async-clipboard.js
    ./frontend/node_modules/caniuse-lite/data/features/ping.js
    ./frontend/node_modules/caniuse-lite/data/features/console-basic.js
    ./frontend/node_modules/caniuse-lite/data/features/canvas.js
    ./frontend/node_modules/caniuse-lite/data/features/css-if.js
    ./frontend/node_modules/caniuse-lite/data/features/const.js
    ./frontend/node_modules/caniuse-lite/data/features/vector-effect.js
    ./frontend/node_modules/caniuse-lite/data/features/pointerlock.js
    ./frontend/node_modules/caniuse-lite/data/features/x-doc-messaging.js
    ./frontend/node_modules/caniuse-lite/data/features/css-clip-path.js
    ./frontend/node_modules/caniuse-lite/data/features/history.js
    ./frontend/node_modules/caniuse-lite/data/features/css-deviceadaptation.js
    ./frontend/node_modules/caniuse-lite/data/features/css-grid-lanes.js
    ./frontend/node_modules/caniuse-lite/data/features/loading-lazy-media.js
    ./frontend/node_modules/caniuse-lite/data/features/rel-noopener.js
    ./frontend/node_modules/caniuse-lite/data/features/feature-policy.js
    ./frontend/node_modules/caniuse-lite/data/features/decorators.js
    ./frontend/node_modules/caniuse-lite/data/features/style-scoped.js
    ./frontend/node_modules/caniuse-lite/data/features/css-default-pseudo.js
    ./frontend/node_modules/caniuse-lite/data/features/css-featurequeries.js
    ./frontend/node_modules/caniuse-lite/data/features/urlsearchparams.js
    ./frontend/node_modules/caniuse-lite/data/features/datauri.js
    ./frontend/node_modules/caniuse-lite/data/features/input-range.js
    ./frontend/node_modules/caniuse-lite/data/features/customevent.js
    ./frontend/node_modules/caniuse-lite/data/features/shadowdomv1.js
    ./frontend/node_modules/caniuse-lite/data/features/css-width-stretch.js
    ./frontend/node_modules/caniuse-lite/data/features/background-clip-text.js
    ./frontend/node_modules/caniuse-lite/data/features/array-find-index.js
    ./frontend/node_modules/caniuse-lite/data/features/png-alpha.js
    ./frontend/node_modules/caniuse-lite/data/features/css-descendant-gtgt.js
    ./frontend/node_modules/caniuse-lite/data/features/filereader.js
    ./frontend/node_modules/caniuse-lite/data/features/intersectionobserver.js
    ./frontend/node_modules/caniuse-lite/data/features/link-rel-prerender.js
    ./frontend/node_modules/caniuse-lite/data/features/av1.js
    ./frontend/node_modules/caniuse-lite/data/features/colr.js
    ./frontend/node_modules/caniuse-lite/data/features/publickeypinning.js
    ./frontend/node_modules/caniuse-lite/data/features/extended-system-fonts.js
    ./frontend/node_modules/caniuse-lite/data/features/pointer.js
    ./frontend/node_modules/caniuse-lite/data/features/font-variant-numeric.js
    ./frontend/node_modules/caniuse-lite/data/features/indeterminate-checkbox.js
    ./frontend/node_modules/caniuse-lite/data/features/audio.js
    ./frontend/node_modules/caniuse-lite/data/features/contenteditable.js
    ./frontend/node_modules/caniuse-lite/data/features/webvr.js
    ./frontend/node_modules/caniuse-lite/data/features/input-minlength.js
    ./frontend/node_modules/caniuse-lite/data/features/css-touch-action.js
    ./frontend/node_modules/caniuse-lite/data/features/pagevisibility.js
    ./frontend/node_modules/caniuse-lite/data/features/wasm-extended-const.js
    ./frontend/node_modules/caniuse-lite/data/features/webnfc.js
    ./frontend/node_modules/caniuse-lite/data/features/u2f.js
    ./frontend/node_modules/caniuse-lite/data/features/wasm-signext.js
    ./frontend/node_modules/caniuse-lite/data/features/font-feature.js
    ./frontend/node_modules/caniuse-lite/data/features/keyboardevent-which.js
    ./frontend/node_modules/caniuse-lite/data/features/form-attribute.js
    ./frontend/node_modules/caniuse-lite/data/features/blobbuilder.js
    ./frontend/node_modules/caniuse-lite/data/features/currentcolor.js
    ./frontend/node_modules/caniuse-lite/data/features/progress.js
    ./frontend/node_modules/caniuse-lite/data/features/css-fixed.js
    ./frontend/node_modules/caniuse-lite/data/features/gamepad.js
    ./frontend/node_modules/caniuse-lite/data/features/flexbox-gap.js
    ./frontend/node_modules/caniuse-lite/data/features/flexbox.js
    ./frontend/node_modules/caniuse-lite/data/features/canvas-text.js
    ./frontend/node_modules/caniuse-lite/data/features/html-media-capture.js
    ./frontend/node_modules/caniuse-lite/data/features/es6-module.js
    ./frontend/node_modules/caniuse-lite/data/features/css-scroll-behavior.js
    ./frontend/node_modules/caniuse-lite/data/features/css-lch-lab.js
    ./frontend/node_modules/caniuse-lite/data/features/atob-btoa.js
    ./frontend/node_modules/caniuse-lite/data/features/portals.js
    ./frontend/node_modules/caniuse-lite/data/features/woff2.js
    ./frontend/node_modules/caniuse-lite/data/features/textencoder.js
    ./frontend/node_modules/caniuse-lite/data/features/indexeddb.js
    ./frontend/node_modules/caniuse-lite/data/features/array-includes.js
    ./frontend/node_modules/caniuse-lite/data/features/run-in.js
    ./frontend/node_modules/caniuse-lite/data/features/beacon.js
    ./frontend/node_modules/caniuse-lite/data/features/css-animation.js
    ./frontend/node_modules/caniuse-lite/data/features/clipboard.js
    ./frontend/node_modules/caniuse-lite/data/features/wasm-nontrapping-fptoint.js
    ./frontend/node_modules/caniuse-lite/data/features/css-containment.js
    ./frontend/node_modules/caniuse-lite/data/features/input-file-directory.js
    ./frontend/node_modules/caniuse-lite/data/features/input-placeholder.js
    ./frontend/node_modules/caniuse-lite/data/features/css-rrggbbaa.js
    ./frontend/node_modules/caniuse-lite/data/features/jpeg2000.js
    ./frontend/node_modules/caniuse-lite/data/features/contentsecuritypolicy.js
    ./frontend/node_modules/caniuse-lite/data/features/css-all.js
    ./frontend/node_modules/caniuse-lite/data/features/getrandomvalues.js
    ./frontend/node_modules/caniuse-lite/data/features/xhtmlsmil.js
    ./frontend/node_modules/caniuse-lite/data/features/css-overflow-anchor.js
    ./frontend/node_modules/caniuse-lite/data/features/customizable-select.js
    ./frontend/node_modules/caniuse-lite/data/features/dragndrop.js
    ./frontend/node_modules/caniuse-lite/data/features/user-select-none.js
    ./frontend/node_modules/caniuse-lite/data/features/ol-reversed.js
    ./frontend/node_modules/caniuse-lite/data/features/ttf.js
    ./frontend/node_modules/caniuse-lite/data/features/input-selection.js
    ./frontend/node_modules/caniuse-lite/data/features/zstd.js
    ./frontend/node_modules/caniuse-lite/data/features/element-closest.js
    ./frontend/node_modules/caniuse-lite/data/features/css-text-indent.js
    ./frontend/node_modules/caniuse-lite/data/features/wasm-bigint.js
    ./frontend/node_modules/caniuse-lite/data/features/css-mixblendmode.js
    ./frontend/node_modules/caniuse-lite/data/features/tls1-1.js
    ./frontend/node_modules/caniuse-lite/data/features/script-defer.js
    ./frontend/node_modules/caniuse-lite/data/features/form-validation.js
    ./frontend/node_modules/caniuse-lite/data/features/rem.js
    ./frontend/node_modules/caniuse-lite/data/features/jpegxr.js
    ./frontend/node_modules/caniuse-lite/data/features/keyboardevent-key.js
    ./frontend/node_modules/caniuse-lite/data/features/css-container-queries.js
    ./frontend/node_modules/caniuse-lite/data/features/keyboardevent-charcode.js
    ./frontend/node_modules/caniuse-lite/data/features/stricttransportsecurity.js
    ./frontend/node_modules/caniuse-lite/data/features/wordwrap.js
    ./frontend/node_modules/caniuse-lite/data/features/css-anchor-positioning.js
    ./frontend/node_modules/caniuse-lite/data/features/canvas-blending.js
    ./frontend/node_modules/caniuse-lite/data/features/declarative-shadow-dom.js
    ./frontend/node_modules/caniuse-lite/data/features/fontface.js
    ./frontend/node_modules/caniuse-lite/data/features/css-mediaqueries.js
    ./frontend/node_modules/caniuse-lite/data/features/css-rebeccapurple.js
    ./frontend/node_modules/caniuse-lite/data/features/wake-lock.js
    ./frontend/node_modules/caniuse-lite/data/features/async-functions.js
    ./frontend/node_modules/caniuse-lite/data/features/css3-cursors-newer.js
    ./frontend/node_modules/caniuse-lite/data/features/css-image-orientation.js
    ./frontend/node_modules/caniuse-lite/data/features/mp3.js
    ./frontend/node_modules/caniuse-lite/data/features/webgpu.js
    ./frontend/node_modules/caniuse-lite/data/features/path2d.js
    ./frontend/node_modules/caniuse-lite/data/features/textcontent.js
    ./frontend/node_modules/caniuse-lite/data/features/requestanimationframe.js
    ./frontend/node_modules/caniuse-lite/data/features/css-print-color-adjust.js
    ./frontend/node_modules/caniuse-lite/data/features/css-snappoints.js
    ./frontend/node_modules/caniuse-lite/data/features/link-rel-prefetch.js
    ./frontend/node_modules/caniuse-lite/data/features/css-any-link.js
    ./frontend/node_modules/caniuse-lite/data/features/payment-request.js
    ./frontend/node_modules/caniuse-lite/data/features/minmaxwh.js
    ./frontend/node_modules/caniuse-lite/data/features/svg-css.js
    ./frontend/node_modules/caniuse-lite/data/features/text-emphasis.js
    ./frontend/node_modules/caniuse-lite/data/features/custom-elements.js
    ./frontend/node_modules/caniuse-lite/data/features/css-sel2.js
    ./frontend/node_modules/caniuse-lite/data/features/css-page-break.js
    ./frontend/node_modules/caniuse-lite/data/features/background-img-opts.js
    ./frontend/node_modules/caniuse-lite/data/features/webm.js
    ./frontend/node_modules/caniuse-lite/data/features/wasm-gc.js
    ./frontend/node_modules/caniuse-lite/data/features/streams.js
    ./frontend/node_modules/caniuse-lite/data/features/date-tolocaledatestring.js
    ./frontend/node_modules/caniuse-lite/data/features/matchmedia.js
    ./frontend/node_modules/caniuse-lite/data/features/js-regexp-lookbehind.js
    ./frontend/node_modules/caniuse-lite/data/features/webxr.js
    ./frontend/node_modules/caniuse-lite/data/features/webgl.js
    ./frontend/node_modules/caniuse-lite/data/features/css-read-only-write.js
    ./frontend/node_modules/caniuse-lite/data/features/dom-range.js
    ./frontend/node_modules/caniuse-lite/data/features/svg-filters.js
    ./frontend/node_modules/caniuse-lite/data/features/addeventlistener.js
    ./frontend/node_modules/caniuse-lite/data/features/woff.js
    ./frontend/node_modules/caniuse-lite/data/features/css-counters.js
    ./frontend/node_modules/caniuse-lite/data/features/css-text-align-last.js
    ./frontend/node_modules/caniuse-lite/data/features/viewport-unit-variants.js
    ./frontend/node_modules/caniuse-lite/data/features/iframe-seamless.js
    ./frontend/node_modules/caniuse-lite/data/features/sharedworkers.js
    ./frontend/node_modules/caniuse-lite/data/features/wasm-reference-types.js
    ./frontend/node_modules/caniuse-lite/data/features/sni.js
    ./frontend/node_modules/caniuse-lite/data/features/svg-img.js
    ./frontend/node_modules/caniuse-lite/data/features/ac3-ec3.js
    ./frontend/node_modules/caniuse-lite/data/features/background-sync.js
    ./frontend/node_modules/caniuse-lite/data/features/css-nesting.js
    ./frontend/node_modules/caniuse-lite/data/features/same-site-cookie-attribute.js
    ./frontend/node_modules/caniuse-lite/data/features/template-literals.js
    ./frontend/node_modules/caniuse-lite/data/features/object-observe.js
    ./frontend/node_modules/caniuse-lite/data/features/cors.js
    ./frontend/node_modules/caniuse-lite/data/features/css-overscroll-behavior.js
    ./frontend/node_modules/caniuse-lite/data/features/vibration.js
    ./frontend/node_modules/caniuse-lite/data/features/css-masks.js
    ./frontend/node_modules/caniuse-lite/data/features/font-family-system-ui.js
    ./frontend/node_modules/caniuse-lite/data/features/css-shapes.js
    ./frontend/node_modules/caniuse-lite/data/features/document-policy.js
    ./frontend/node_modules/caniuse-lite/data/features/kerning-pairs-ligatures.js
    ./frontend/node_modules/caniuse-lite/data/features/mdn-text-decoration-line.js
    ./frontend/node_modules/caniuse-lite/data/features/document-currentscript.js
    ./frontend/node_modules/caniuse-lite/data/features/picture.js
    ./frontend/node_modules/caniuse-lite/data/features/css-module-scripts.js
    ./frontend/node_modules/caniuse-lite/data/features/css-font-stretch.js
    ./frontend/node_modules/caniuse-lite/data/features/wasm-threads.js
    ./frontend/node_modules/caniuse-lite/data/features/css-caret-color.js
    ./frontend/node_modules/caniuse-lite/data/features/apng.js
    ./frontend/node_modules/caniuse-lite/data/features/multibackgrounds.js
    ./frontend/node_modules/caniuse-lite/data/features/dom-manip-convenience.js
    ./frontend/node_modules/caniuse-lite/data/features/css-placeholder.js
    ./frontend/node_modules/caniuse-lite/data/features/focusin-focusout-events.js
    ./frontend/node_modules/caniuse-lite/data/features/webusb.js
    ./frontend/node_modules/caniuse-lite/data/features/variable-fonts.js
    ./frontend/node_modules/caniuse-lite/data/features/object-fit.js
    ./frontend/node_modules/caniuse-lite/data/features/inline-block.js
    ./frontend/node_modules/caniuse-lite/data/features/spellcheck-attribute.js
    ./frontend/node_modules/caniuse-lite/data/features/dialog.js
    ./frontend/node_modules/caniuse-lite/data/features/tls1-2.js
    ./frontend/node_modules/caniuse-lite/data/features/css3-cursors-grab.js
    ./frontend/node_modules/caniuse-lite/data/features/css-backgroundblendmode.js
    ./frontend/node_modules/caniuse-lite/data/features/es6-module-dynamic-import.js
    ./frontend/node_modules/caniuse-lite/data/features/link-rel-dns-prefetch.js
    ./frontend/node_modules/caniuse-lite/data/features/justify-content-space-evenly.js
    ./frontend/node_modules/caniuse-lite/data/features/meter.js
    ./frontend/node_modules/caniuse-lite/data/features/readonly-attr.js
    ./frontend/node_modules/caniuse-lite/data/features/credential-management.js
    ./frontend/node_modules/caniuse-lite/data/features/svg-smil.js
    ./frontend/node_modules/caniuse-lite/data/features/x-frame-options.js
    ./frontend/node_modules/caniuse-lite/data/features/tabindex-attr.js
    ./frontend/node_modules/caniuse-lite/data/features/css-focus-visible.js
    ./frontend/node_modules/caniuse-lite/data/features/css-element-function.js
    ./frontend/node_modules/caniuse-lite/data/features/css-logical-props.js
    ./frontend/node_modules/caniuse-lite/data/features/css-gradients.js
    ./frontend/node_modules/caniuse-lite/data/features/user-timing.js
    ./frontend/node_modules/caniuse-lite/data/features/css-media-interaction.js
    ./frontend/node_modules/caniuse-lite/data/features/keyboardevent-code.js
    ./frontend/node_modules/caniuse-lite/data/features/css-text-orientation.js
    ./frontend/node_modules/caniuse-lite/data/features/css-content-visibility.js
    ./frontend/node_modules/caniuse-lite/data/features/css-matches-pseudo.js
    ./frontend/node_modules/caniuse-lite/data/features/mdn-text-decoration-color.js
    ./frontend/node_modules/caniuse-lite/data/features/xhtml.js
    ./frontend/node_modules/caniuse-lite/data/features/css-reflections.js
    ./frontend/node_modules/caniuse-lite/data/features/fetch.js
    ./frontend/node_modules/caniuse-lite/data/features/srcset.js
    ./frontend/node_modules/caniuse-lite/data/features/passwordrules.js
    ./frontend/node_modules/caniuse-lite/data/features/css-hyphens.js
    ./frontend/node_modules/caniuse-lite/data/features/es6-class.js
    ./frontend/node_modules/caniuse-lite/data/features/geolocation.js
    ./frontend/node_modules/caniuse-lite/data/features/subresource-integrity.js
    ./frontend/node_modules/caniuse-lite/data/features/flac.js
    ./frontend/node_modules/caniuse-lite/data/features/wasm-multi-memory.js
    ./frontend/node_modules/caniuse-lite/data/features/eventsource.js
    ./frontend/node_modules/caniuse-lite/data/features/webp.js
    ./frontend/node_modules/caniuse-lite/data/features/css-repeating-gradients.js
    ./frontend/node_modules/caniuse-lite/data/features/mediacapture-fromelement.js
    ./frontend/node_modules/caniuse-lite/data/features/img-naturalwidth-naturalheight.js
    ./frontend/node_modules/caniuse-lite/data/features/domcontentloaded.js
    ./frontend/node_modules/caniuse-lite/data/features/css-initial-letter.js
    ./frontend/node_modules/caniuse-lite/data/features/xhr2.js
    ./frontend/node_modules/caniuse-lite/data/features/tls1-3.js
    ./frontend/node_modules/caniuse-lite/data/features/once-event-listener.js
    ./frontend/node_modules/caniuse-lite/data/features/iframe-sandbox.js
    ./frontend/node_modules/caniuse-lite/data/features/css-conic-gradients.js
    ./frontend/node_modules/caniuse-lite/data/features/css-dir-pseudo.js
    ./frontend/node_modules/caniuse-lite/data/features/viewport-units.js
    ./frontend/node_modules/caniuse-lite/data/features/sdch.js
    ./frontend/node_modules/caniuse-lite/data/features/view-transitions.js
    ./frontend/node_modules/caniuse-lite/data/features/document-evaluate-xpath.js
    ./frontend/node_modules/caniuse-lite/data/features/sharedarraybuffer.js
    ./frontend/node_modules/caniuse-lite/data/features/css-grid-animation.js
    ./frontend/node_modules/caniuse-lite/data/features/jpegxl.js
    ./frontend/node_modules/caniuse-lite/data/features/link-rel-modulepreload.js
    ./frontend/node_modules/caniuse-lite/data/features/keyboardevent-getmodifierstate.js
    ./frontend/node_modules/caniuse-lite/data/features/css-variables.js
    ./frontend/node_modules/caniuse-lite/data/features/shadowdom.js
    ./frontend/node_modules/caniuse-lite/data/features/setimmediate.js
    ./frontend/node_modules/caniuse-lite/data/features/css3-colors.js
    ./frontend/node_modules/caniuse-lite/data/features/text-stroke.js
    ./frontend/node_modules/caniuse-lite/data/features/css-focus-within.js
    ./frontend/node_modules/caniuse-lite/data/features/css-file-selector-button.js
    ./frontend/node_modules/caniuse-lite/data/features/css-media-scripting.js
    ./frontend/node_modules/caniuse-lite/data/features/css-sel3.js
    ./frontend/node_modules/caniuse-lite/data/features/loading-lazy-attr.js
    ./frontend/node_modules/caniuse-lite/data/features/es6-generators.js
    ./frontend/node_modules/caniuse-lite/data/features/mdn-text-decoration-style.js
    ./frontend/node_modules/caniuse-lite/data/features/gyroscope.js
    ./frontend/node_modules/caniuse-lite/data/features/will-change.js
    ./frontend/node_modules/caniuse-lite/data/features/internationalization.js
    ./frontend/node_modules/caniuse-lite/data/features/css-widows-orphans.js
    ./frontend/node_modules/caniuse-lite/data/features/css-writing-mode.js
    ./frontend/node_modules/caniuse-lite/data/features/documenthead.js
    ./frontend/node_modules/caniuse-lite/data/features/permissions-api.js
    ./frontend/node_modules/caniuse-lite/data/features/lazyload.js
    ./frontend/node_modules/caniuse-lite/data/features/contentsecuritypolicy2.js
    ./frontend/node_modules/caniuse-lite/data/features/objectrtc.js
    ./frontend/node_modules/caniuse-lite/data/features/es6-string-includes.js
    ./frontend/node_modules/caniuse-lite/data/features/typedarrays.js
    ./frontend/node_modules/caniuse-lite/data/features/cookie-store-api.js
    ./frontend/node_modules/caniuse-lite/data/features/bloburls.js
    ./frontend/node_modules/caniuse-lite/data/features/svg-html.js
    ./frontend/node_modules/caniuse-lite/data/features/requestidlecallback.js
    ./frontend/node_modules/caniuse-lite/data/features/temporal.js
    ./frontend/node_modules/caniuse-lite/data/features/css-subgrid.js
    ./frontend/node_modules/caniuse-lite/data/features/array-find.js
    ./frontend/node_modules/caniuse-lite/data/features/meta-theme-color.js
    ./frontend/node_modules/caniuse-lite/data/features/bigint.js
    ./frontend/node_modules/caniuse-lite/data/features/css-overflow-overlay.js
    ./frontend/node_modules/caniuse-lite/data/features/css-textshadow.js
    ./frontend/node_modules/caniuse-lite/data/features/css-sticky.js
    ./frontend/node_modules/caniuse-lite/data/features/multicolumn.js
    ./frontend/node_modules/caniuse-lite/data/features/css-font-palette.js
    ./frontend/node_modules/caniuse-lite/data/features/mpeg-dash.js
    ./frontend/node_modules/caniuse-lite/data/features/css-cascade-scope.js
    ./frontend/node_modules/caniuse-lite/data/features/orientation-sensor.js
    ./frontend/node_modules/caniuse-lite/data/features/promises.js
    ./frontend/node_modules/caniuse-lite/data/features/css-has.js
    ./frontend/node_modules/caniuse-lite/data/features/css3-tabsize.js
    ./frontend/node_modules/caniuse-lite/data/features/font-unicode-range.js
    ./frontend/node_modules/caniuse-lite/data/features/css-revert-value.js
    ./frontend/node_modules/caniuse-lite/data/features/svg-fonts.js
    ./frontend/node_modules/caniuse-lite/data/features/hashchange.js
    ./frontend/node_modules/caniuse-lite/data/features/childnode-remove.js
    ./frontend/node_modules/caniuse-lite/data/features/form-submit-attributes.js
    ./frontend/node_modules/caniuse-lite/data/features/css-when-else.js
    ./frontend/node_modules/caniuse-lite/data/features/css-hanging-punctuation.js
    ./frontend/node_modules/caniuse-lite/data/features/css-env-function.js
    ./frontend/node_modules/caniuse-lite/data/features/mdn-css-unicode-bidi-isolate-override.js
    ./frontend/node_modules/caniuse-lite/data/features/ruby.js
    ./frontend/node_modules/caniuse-lite/data/features/http2.js
    ./frontend/node_modules/caniuse-lite/data/features/webgl2.js
    ./frontend/node_modules/caniuse-lite/data/features/css-media-range-syntax.js
    ./frontend/node_modules/caniuse-lite/data/features/css-gencontent.js
    ./frontend/node_modules/caniuse-lite/data/features/input-file-multiple.js
    ./frontend/node_modules/caniuse-lite/data/features/css3-cursors.js
    ./frontend/node_modules/caniuse-lite/data/features/getelementsbyclassname.js
    ./frontend/node_modules/caniuse-lite/data/features/css-paged-media.js
    ./frontend/node_modules/caniuse-lite/data/features/css-case-insensitive.js
    ./frontend/node_modules/caniuse-lite/data/features/wbr-element.js
    ./frontend/node_modules/caniuse-lite/data/features/fileapi.js
    ./frontend/node_modules/caniuse-lite/data/features/indexeddb2.js
    ./frontend/node_modules/caniuse-lite/data/features/css-color-adjust.js
    ./frontend/node_modules/caniuse-lite/data/features/namevalue-storage.js
    ./frontend/node_modules/caniuse-lite/data/features/resizeobserver.js
    ./frontend/node_modules/caniuse-lite/data/features/devicepixelratio.js
    ./frontend/node_modules/caniuse-lite/data/features/css-font-rendering-controls.js
    ./frontend/node_modules/caniuse-lite/data/features/svg-fragment.js
    ./frontend/node_modules/caniuse-lite/data/features/upgradeinsecurerequests.js
    ./frontend/node_modules/caniuse-lite/data/features/css-container-queries-style.js
    ./frontend/node_modules/caniuse-lite/data/features/css-math-functions.js
    ./frontend/node_modules/caniuse-lite/data/features/sxg.js
    ./frontend/node_modules/caniuse-lite/data/features/css-image-set.js
    ./frontend/node_modules/caniuse-lite/data/features/stream.js
    ./frontend/node_modules/caniuse-lite/data/features/http-live-streaming.js
    ./frontend/node_modules/caniuse-lite/data/features/avif.js
    ./frontend/node_modules/caniuse-lite/data/features/css-zoom.js
    ./frontend/node_modules/caniuse-lite/data/features/constraint-validation.js
    ./frontend/node_modules/caniuse-lite/data/features/imports.js
    ./frontend/node_modules/caniuse-lite/data/features/broadcastchannel.js
    ./frontend/node_modules/caniuse-lite/data/features/webtransport.js
    ./frontend/node_modules/caniuse-lite/data/features/html5semantic.js
    ./frontend/node_modules/caniuse-lite/data/features/fieldset-disabled.js
    ./frontend/node_modules/caniuse-lite/data/features/webcodecs.js
    ./frontend/node_modules/caniuse-lite/data/features/getboundingclientrect.js
    ./frontend/node_modules/caniuse-lite/data/features/input-number.js
    ./frontend/node_modules/caniuse-lite/data/features/css-crisp-edges.js
    ./frontend/node_modules/caniuse-lite/data/features/web-share.js
    ./frontend/node_modules/caniuse-lite/data/features/es5.js
    ./frontend/node_modules/caniuse-lite/data/features/colr-v1.js
    ./frontend/node_modules/caniuse-lite/data/features/scrollintoviewifneeded.js
    ./frontend/node_modules/caniuse-lite/data/features/css-relative-colors.js
    ./frontend/node_modules/caniuse-lite/data/features/web-app-manifest.js
    ./frontend/node_modules/caniuse-lite/data/features/object-entries.js
    ./frontend/node_modules/caniuse-lite/data/features/matchesselector.js
    ./frontend/node_modules/caniuse-lite/data/features/css-table.js
    ./frontend/node_modules/caniuse-lite/data/features/insert-adjacent.js
    ./frontend/node_modules/caniuse-lite/data/features/css-text-wrap-balance.js
    ./frontend/node_modules/caniuse-lite/data/features/comparedocumentposition.js
    ./frontend/node_modules/caniuse-lite/data/features/push-api.js
    ./frontend/node_modules/caniuse-lite/data/features/eme.js
    ./frontend/node_modules/caniuse-lite/data/features/permissions-policy.js
    ./frontend/node_modules/caniuse-lite/data/features/css-text-justify.js
    ./frontend/node_modules/caniuse-lite/data/features/nav-timing.js
    ./frontend/node_modules/caniuse-lite/data/features/background-repeat-round-space.js
    ./frontend/node_modules/caniuse-lite/data/features/hidden.js
    ./frontend/node_modules/caniuse-lite/data/features/css3-boxsizing.js
    ./frontend/node_modules/caniuse-lite/data/features/console-time.js
    ./frontend/node_modules/caniuse-lite/data/features/sql-storage.js
    ./frontend/node_modules/caniuse-lite/data/features/element-scroll-methods.js
    ./frontend/node_modules/caniuse-lite/data/features/mutationobserver.js
    ./frontend/node_modules/caniuse-lite/data/features/input-inputmode.js
    ./frontend/node_modules/caniuse-lite/data/features/flow-root.js
    ./frontend/node_modules/caniuse-lite/data/features/promise-finally.js
    ./frontend/node_modules/caniuse-lite/data/features/css-text-spacing.js
    ./frontend/node_modules/caniuse-lite/data/features/audio-api.js
    ./frontend/node_modules/caniuse-lite/data/features/page-transition-events.js
    ./frontend/node_modules/caniuse-lite/data/features/css-optional-pseudo.js
    ./frontend/node_modules/caniuse-lite/data/features/css-filter-function.js
    ./frontend/node_modules/caniuse-lite/data/features/css-regions.js
    ./frontend/node_modules/caniuse-lite/data/features/xml-serializer.js
    ./frontend/node_modules/caniuse-lite/data/features/proxy.js
    ./frontend/node_modules/caniuse-lite/data/features/css-exclusions.js
    ./frontend/node_modules/caniuse-lite/data/features/css-paint-api.js
    ./frontend/node_modules/caniuse-lite/data/features/word-break.js
    ./frontend/node_modules/caniuse-lite/data/features/audiotracks.js
    ./frontend/node_modules/caniuse-lite/data/features/css-text-box-trim.js
    ./frontend/node_modules/caniuse-lite/data/features/trusted-types.js
    ./frontend/node_modules/caniuse-lite/data/features/ogg-vorbis.js
    ./frontend/node_modules/caniuse-lite/data/features/passkeys.js
    ./frontend/node_modules/caniuse-lite/data/features/css-container-query-units.js
    ./frontend/node_modules/caniuse-lite/data/features/do-not-track.js
    ./frontend/node_modules/caniuse-lite/data/features/download.js
    ./frontend/node_modules/caniuse-lite/data/features/midi.js
    ./frontend/node_modules/caniuse-lite/data/features/css-cross-fade.js
    ./frontend/node_modules/caniuse-lite/data/features/battery-status.js
    ./frontend/node_modules/caniuse-lite/data/features/auxclick.js
    ./frontend/node_modules/caniuse-lite/data/features/filesystem.js
    ./frontend/node_modules/caniuse-lite/data/features/mathml.js
    ./frontend/node_modules/caniuse-lite/data/features/ime.js
    ./frontend/node_modules/caniuse-lite/data/features/abortcontroller.js
    ./frontend/node_modules/caniuse-lite/data/features/imagecapture.js
    ./frontend/node_modules/caniuse-lite/data/features/css-in-out-of-range.js
    ./frontend/node_modules/caniuse-lite/data/features/websockets.js
    ./frontend/node_modules/caniuse-lite/data/features/url-scroll-to-text-fragment.js
    ./frontend/node_modules/pretty-format/build/plugins/ReactElement.d.ts
    ./frontend/node_modules/pretty-format/build/plugins/Immutable.d.ts
    ./frontend/node_modules/esquery/dist/esquery.min.js
    ./frontend/node_modules/esquery/dist/esquery.esm.min.js
    ./frontend/node_modules/esquery/dist/esquery.esm.min.js.map
    ./frontend/node_modules/esquery/dist/esquery.lite.js
    ./frontend/node_modules/esquery/dist/esquery.lite.min.js
    ./frontend/node_modules/esquery/dist/esquery.esm.js
    ./frontend/node_modules/esquery/dist/esquery.js
    ./frontend/node_modules/esquery/dist/esquery.lite.min.js.map
    ./frontend/node_modules/esquery/dist/esquery.min.js.map
    ./frontend/node_modules/pretty-format/build/plugins/ConvertAnsi.d.ts
    ./frontend/node_modules/pretty-format/build/plugins/ConvertAnsi.js
    ./frontend/node_modules/pretty-format/build/plugins/ReactTestComponent.js
    ./frontend/node_modules/pretty-format/build/collections.d.ts
    ./frontend/node_modules/pretty-format/build/types.js
    ./frontend/node_modules/pretty-format/package.json
    ./frontend/node_modules/pretty-format/README.md
    ./frontend/node_modules/@vitest/spy/optional-types.d.ts
    ./frontend/node_modules/@testing-library/dom/dist/wait-for-element-to-be-removed.js
    ./frontend/node_modules/@vitest/spy/package.json
    ./frontend/node_modules/@vitest/spy/README.md
    ./frontend/node_modules/import-fresh/index.d.ts
    ./frontend/node_modules/import-fresh/package.json
    ./frontend/node_modules/import-fresh/readme.md
    ./frontend/node_modules/import-fresh/index.js
    ./frontend/node_modules/import-fresh/license
    ./frontend/node_modules/pretty-format/build/plugins/DOMCollection.d.ts
    ./frontend/node_modules/pretty-format/build/plugins/Immutable.js
    ./frontend/node_modules/pretty-format/build/plugins/DOMCollection.js
    ./frontend/node_modules/pretty-format/build/plugins/DOMElement.d.ts
    ./frontend/node_modules/pretty-format/build/plugins/ReactElement.js
    ./frontend/node_modules/pretty-format/build/plugins/DOMElement.js
    ./frontend/node_modules/pretty-format/build/plugins/AsymmetricMatcher.js
    ./frontend/node_modules/pretty-format/build/plugins/AsymmetricMatcher.d.ts
    ./frontend/node_modules/pretty-format/build/plugins/ReactTestComponent.d.ts
    ./frontend/node_modules/@babel/traverse/lib/traverse-node.js.map
    ./frontend/node_modules/@babel/traverse/lib/context.js.map
    ./frontend/node_modules/@babel/traverse/lib/context.js
    ./frontend/node_modules/@babel/traverse/lib/traverse-node.js
    ./frontend/node_modules/@babel/traverse/lib/index.js.map
    ./frontend/node_modules/@babel/traverse/lib/visitors.js.map
    ./frontend/node_modules/@vitest/spy/dist/index.d.ts
    ./frontend/node_modules/@vitest/spy/dist/index.js
    ./frontend/node_modules/@vitest/spy/LICENSE
    ./frontend/node_modules/pretty-format/node_modules/ansi-styles/license
    ./frontend/node_modules/pretty-format/LICENSE
    ./frontend/node_modules/pretty-format/node_modules/ansi-styles/index.js
    ./frontend/node_modules/@testing-library/dom/dist/DOMElementFilter.js
    ./frontend/node_modules/@testing-library/dom/dist/query-helpers.js
    ./frontend/node_modules/@testing-library/dom/dist/events.js
    ./frontend/node_modules/@testing-library/dom/LICENSE
    ./frontend/node_modules/pretty-format/node_modules/ansi-styles/index.d.ts
    ./frontend/node_modules/pretty-format/node_modules/ansi-styles/package.json
    ./frontend/node_modules/pretty-format/node_modules/ansi-styles/readme.md
    ./frontend/node_modules/@testing-library/dom/dist/label-helpers.js
    ./frontend/node_modules/@testing-library/dom/dist/matches.js
    ./frontend/node_modules/@testing-library/dom/dist/get-node-text.js
    ./frontend/node_modules/@testing-library/dom/dist/screen.js
    ./frontend/node_modules/@testing-library/dom/dist/role-helpers.js
    ./frontend/node_modules/@testing-library/dom/dist/event-map.js
    ./frontend/node_modules/@testing-library/dom/dist/suggestions.js
    ./frontend/node_modules/@testing-library/dom/dist/config.js
    ./frontend/node_modules/@testing-library/dom/dist/get-queries-for-element.js
    ./frontend/node_modules/@testing-library/dom/dist/index.js
    ./frontend/node_modules/@testing-library/dom/dist/wait-for.js
    ./frontend/node_modules/@testing-library/dom/dist/helpers.js
    ./frontend/node_modules/@testing-library/dom/dist/pretty-dom.js
    ./frontend/node_modules/@testing-library/dom/dist/get-user-code-frame.js
    ./frontend/node_modules/@testing-library/dom/dist/queries/text.js
    ./frontend/node_modules/@testing-library/dom/dist/queries/placeholder-text.js
    ./frontend/node_modules/@testing-library/dom/dist/queries/display-value.js
    ./frontend/node_modules/@testing-library/dom/dist/queries/title.js
    ./frontend/node_modules/@testing-library/dom/dist/queries/alt-text.js
    ./frontend/node_modules/@testing-library/dom/dist/queries/label-text.js
    ./frontend/node_modules/@testing-library/dom/dist/queries/index.js
    ./frontend/node_modules/@testing-library/dom/dist/queries/all-utils.js
    ./frontend/node_modules/@testing-library/dom/dist/queries/role.js
    ./frontend/node_modules/@testing-library/dom/dist/queries/test-id.js
    ./frontend/node_modules/w3c-xmlserializer/LICENSE.md
    ./frontend/node_modules/@testing-library/react/dist/@testing-library/react.pure.umd.min.js.map
    ./frontend/node_modules/@testing-library/react/dist/@testing-library/react.umd.min.js.map
    ./frontend/node_modules/@testing-library/react/dist/@testing-library/react.umd.js
    ./frontend/node_modules/@testing-library/react/dist/@testing-library/react.umd.js.map
    ./frontend/node_modules/@testing-library/react/dist/@testing-library/react.pure.umd.js
    ./frontend/node_modules/@testing-library/react/dist/@testing-library/react.umd.min.js
    ./frontend/node_modules/@testing-library/react/dist/@testing-library/react.pure.umd.min.js
    ./frontend/node_modules/@testing-library/react/dist/@testing-library/react.cjs.js
    ./frontend/node_modules/@testing-library/react/dist/@testing-library/react.pure.esm.js
    ./frontend/node_modules/@testing-library/react/dist/@testing-library/react.pure.umd.js.map
    ./frontend/node_modules/@testing-library/react/dist/@testing-library/react.pure.cjs.js
    ./frontend/node_modules/@testing-library/react/dist/@testing-library/react.esm.js
    ./frontend/node_modules/@testing-library/react/dist/fire-event.js
    ./frontend/node_modules/@testing-library/react/dist/config.js
    ./frontend/node_modules/@testing-library/react/dist/index.js
    ./frontend/node_modules/@testing-library/react/dist/act-compat.js
    ./frontend/node_modules/@testing-library/react/dist/pure.js
    ./frontend/node_modules/@testing-library/react/LICENSE
    ./frontend/node_modules/pretty-format/build/plugins/lib/escapeHTML.d.ts
    ./frontend/node_modules/pretty-format/build/plugins/lib/escapeHTML.js
    ./frontend/node_modules/pretty-format/build/plugins/lib/markup.d.ts
    ./frontend/node_modules/pretty-format/build/plugins/lib/markup.js
    ./frontend/node_modules/w3c-xmlserializer/README.md
    ./frontend/node_modules/w3c-xmlserializer/package.json
    ./frontend/node_modules/caniuse-lite/LICENSE
    ./frontend/node_modules/@babel/traverse/lib/scope/index.js.map
    ./frontend/node_modules/tinyexec/package.json
    ./frontend/node_modules/tinyexec/README.md
    ./frontend/node_modules/@testing-library/dom/dist/@testing-library/dom.cjs.js
    ./frontend/node_modules/@testing-library/dom/dist/@testing-library/dom.umd.min.js
    ./frontend/node_modules/@testing-library/dom/dist/@testing-library/dom.umd.js.map
    ./frontend/node_modules/@testing-library/dom/dist/@testing-library/dom.umd.min.js.map
    ./frontend/node_modules/@testing-library/dom/dist/@testing-library/dom.esm.js
    ./frontend/node_modules/@testing-library/dom/dist/@testing-library/dom.umd.js
    ./frontend/node_modules/caniuse-lite/README.md
    ./frontend/node_modules/@babel/traverse/lib/scope/lib/renamer.js.map
    ./frontend/node_modules/@babel/traverse/lib/scope/lib/renamer.js
    ./frontend/node_modules/@babel/traverse/lib/scope/binding.js.map
    ./frontend/node_modules/css.escape/css.escape.js
    ./frontend/node_modules/@babel/traverse/lib/scope/traverseForScope.js.map
    ./frontend/node_modules/@babel/traverse/lib/scope/binding.js
    ./frontend/node_modules/css.escape/package.json
    ./frontend/node_modules/@babel/traverse/lib/scope/index.js
    ./frontend/node_modules/css.escape/README.md
    ./frontend/node_modules/@babel/traverse/lib/scope/traverseForScope.js
    ./frontend/node_modules/css.escape/LICENSE-MIT.txt
    ./frontend/node_modules/@babel/traverse/lib/index.js
    ./frontend/node_modules/tinyexec/dist/LICENSES.txt
    ./frontend/node_modules/tinyexec/dist/main.mjs
    ./frontend/node_modules/tinyexec/dist/main.d.mts
    ./frontend/node_modules/tinyexec/LICENSE
    ./frontend/node_modules/@babel/template/lib/string.js.map
    ./frontend/node_modules/@babel/template/lib/builder.js
    ./frontend/node_modules/@babel/template/lib/builder.js.map
    ./frontend/node_modules/@babel/template/lib/index.js.map
    ./frontend/node_modules/@babel/template/lib/parse.js
    ./frontend/node_modules/@babel/template/lib/string.js
    ./frontend/node_modules/@babel/template/lib/populate.js
    ./frontend/node_modules/@babel/template/lib/options.js.map
    ./frontend/node_modules/@babel/template/lib/formatters.js
    ./frontend/node_modules/@babel/template/lib/literal.js
    ./frontend/node_modules/@babel/template/lib/index.js
    ./frontend/node_modules/@babel/template/lib/parse.js.map
    ./frontend/node_modules/@babel/template/lib/options.js
    ./frontend/node_modules/@babel/template/lib/formatters.js.map
    ./frontend/node_modules/@babel/template/lib/literal.js.map
    ./frontend/node_modules/@babel/template/lib/populate.js.map
    ./frontend/node_modules/@babel/template/package.json
    ./frontend/node_modules/@babel/template/README.md
    ./frontend/node_modules/@babel/template/LICENSE
    ./frontend/node_modules/w3c-xmlserializer/lib/attributes.js
    ./frontend/node_modules/w3c-xmlserializer/lib/serialize.js
    ./frontend/node_modules/w3c-xmlserializer/lib/constants.js
    ./frontend/node_modules/caniuse-lite/package.json
    ./frontend/node_modules/@testing-library/react/pure.d.ts
    ./frontend/node_modules/@testing-library/react/pure.js
    ./frontend/node_modules/parse5/package.json
    ./frontend/node_modules/parse5/README.md
    ./frontend/node_modules/pathe/utils.d.ts
    ./frontend/node_modules/pathe/package.json
    ./frontend/node_modules/pathe/README.md
    ./frontend/node_modules/set-cookie-parser/lib/set-cookie.js
    ./frontend/node_modules/set-cookie-parser/package.json
    ./frontend/node_modules/set-cookie-parser/README.md
    ./frontend/node_modules/set-cookie-parser/LICENSE
    ./frontend/node_modules/@babel/traverse/lib/path/introspection.js
    ./frontend/node_modules/@babel/traverse/lib/path/family.js
    ./frontend/node_modules/@babel/traverse/lib/path/modification.js.map
    ./frontend/node_modules/@babel/traverse/lib/path/replacement.js
    ./frontend/node_modules/@babel/traverse/lib/path/ancestry.js
    ./frontend/node_modules/@babel/traverse/lib/path/context.js.map
    ./frontend/node_modules/@babel/traverse/lib/path/context.js
    ./frontend/node_modules/@babel/traverse/lib/path/replacement.js.map
    ./frontend/node_modules/@testing-library/dom/types/index.d.ts
    ./frontend/node_modules/@testing-library/dom/types/matches.d.ts
    ./frontend/node_modules/@testing-library/dom/types/query-helpers.d.ts
    ./frontend/node_modules/@testing-library/dom/types/wait-for-element-to-be-removed.d.ts
    ./frontend/node_modules/@testing-library/dom/types/queries.d.ts
    ./frontend/node_modules/@testing-library/dom/types/suggestions.d.ts
    ./frontend/node_modules/@testing-library/dom/types/wait-for.d.ts
    ./frontend/node_modules/@testing-library/dom/types/config.d.ts
    ./frontend/node_modules/@testing-library/dom/types/get-node-text.d.ts
    ./frontend/node_modules/@testing-library/dom/types/role-helpers.d.ts
    ./frontend/node_modules/@testing-library/dom/types/get-queries-for-element.d.ts
    ./frontend/node_modules/@testing-library/dom/types/events.d.ts
    ./frontend/node_modules/@testing-library/dom/types/screen.d.ts
    ./frontend/node_modules/@testing-library/dom/types/pretty-dom.d.ts
    ./frontend/node_modules/@testing-library/react/types/index.d.ts
    ./frontend/node_modules/@testing-library/react/types/pure.d.ts
    ./frontend/node_modules/pathe/dist/index.d.ts
    ./frontend/node_modules/pathe/dist/utils.d.mts
    ./frontend/node_modules/pathe/dist/index.mjs
    ./frontend/node_modules/pathe/dist/index.cjs
    ./frontend/node_modules/pathe/dist/utils.d.cts
    ./frontend/node_modules/pathe/dist/utils.d.ts
    ./frontend/node_modules/parse5/dist/index.d.ts
    ./frontend/node_modules/is-extglob/package.json
    ./frontend/node_modules/is-extglob/README.md
    ./frontend/node_modules/is-extglob/index.js
    ./frontend/node_modules/is-extglob/LICENSE
    ./frontend/node_modules/@babel/traverse/lib/path/inference/index.js.map
    ./frontend/node_modules/@babel/traverse/lib/path/inference/inferer-reference.js
    ./frontend/node_modules/@babel/traverse/lib/path/inference/inferers.js
    ./frontend/node_modules/@babel/traverse/lib/path/inference/index.js
    ./frontend/node_modules/@babel/traverse/lib/path/inference/util.js.map
    ./frontend/node_modules/@babel/traverse/lib/path/inference/inferer-reference.js.map
    ./frontend/node_modules/@babel/traverse/lib/path/inference/util.js
    ./frontend/node_modules/@babel/traverse/lib/path/inference/inferers.js.map
    ./frontend/node_modules/@babel/traverse/lib/path/index.js.map
    ./frontend/node_modules/@babel/traverse/lib/path/conversion.js.map
    ./frontend/node_modules/caniuse-lite/dist/lib/statuses.js
    ./frontend/node_modules/caniuse-lite/dist/lib/supported.js
    ./frontend/node_modules/resolve-from/package.json
    ./frontend/node_modules/resolve-from/readme.md
    ./frontend/node_modules/resolve-from/index.js
    ./frontend/node_modules/resolve-from/license
    ./frontend/node_modules/pathe/dist/index.d.mts
    ./frontend/node_modules/pathe/dist/utils.cjs
    ./frontend/node_modules/pathe/LICENSE
    ./frontend/node_modules/pathe/dist/index.d.cts
    ./frontend/node_modules/pathe/dist/utils.mjs
    ./frontend/node_modules/pathe/dist/shared/pathe.BSlhyZSM.cjs
    ./frontend/node_modules/pathe/dist/shared/pathe.M-eThtNZ.mjs
    ./frontend/node_modules/parse5/dist/index.js
    ./frontend/node_modules/@babel/traverse/lib/path/lib/virtual-types-validator.js
    ./frontend/node_modules/@babel/traverse/lib/path/lib/hoister.js
    ./frontend/node_modules/@babel/traverse/lib/path/lib/virtual-types.js.map
    ./frontend/node_modules/@babel/traverse/lib/path/lib/removal-hooks.js
    ./frontend/node_modules/@babel/traverse/lib/path/lib/removal-hooks.js.map
    ./frontend/node_modules/@babel/traverse/lib/path/lib/virtual-types-validator.js.map
    ./frontend/node_modules/@babel/traverse/lib/path/lib/virtual-types.js
    ./frontend/node_modules/@babel/traverse/lib/path/lib/hoister.js.map
    ./frontend/node_modules/@babel/traverse/lib/path/comments.js
    ./frontend/node_modules/@babel/traverse/lib/path/comments.js.map
    ./frontend/node_modules/@babel/traverse/lib/path/removal.js.map
    ./frontend/node_modules/@babel/traverse/lib/path/modification.js
    ./frontend/node_modules/@babel/traverse/lib/path/ancestry.js.map
    ./frontend/node_modules/@babel/traverse/lib/path/removal.js
    ./frontend/node_modules/@babel/traverse/lib/path/index.js
    ./frontend/node_modules/@babel/traverse/lib/path/evaluation.js.map
    ./frontend/node_modules/@babel/traverse/lib/path/introspection.js.map
    ./frontend/node_modules/@babel/traverse/lib/path/family.js.map
    ./frontend/node_modules/@babel/traverse/lib/path/evaluation.js
    ./frontend/node_modules/@babel/traverse/lib/path/conversion.js
    ./frontend/node_modules/@babel/traverse/lib/cache.js
    ./frontend/node_modules/@babel/traverse/lib/types.js.map
    ./frontend/node_modules/@babel/traverse/lib/types.js
    ./frontend/node_modules/@babel/traverse/lib/hub.js
    ./frontend/node_modules/@babel/traverse/lib/hub.js.map
    ./frontend/node_modules/@babel/traverse/lib/visitors.js
    ./frontend/node_modules/@babel/traverse/lib/cache.js.map
    ./frontend/node_modules/@babel/runtime/regenerator/index.js
    ./frontend/node_modules/@babel/traverse/package.json
    ./frontend/node_modules/@babel/traverse/README.md
    ./frontend/node_modules/@babel/traverse/tsconfig.overrides.json
    ./frontend/node_modules/@babel/traverse/LICENSE
    ./frontend/node_modules/parse5/dist/serializer/index.d.ts
    ./frontend/node_modules/parse5/dist/serializer/index.js
    ./frontend/node_modules/parse5/dist/common/doctype.js
    ./frontend/node_modules/parse5/dist/common/html.d.ts
    ./frontend/node_modules/parse5/dist/common/doctype.d.ts
    ./frontend/node_modules/parse5/dist/common/token.js
    ./frontend/node_modules/parse5/dist/common/unicode.d.ts
    ./frontend/node_modules/parse5/dist/common/unicode.js
    ./frontend/node_modules/parse5/dist/common/error-codes.d.ts
    ./frontend/node_modules/parse5/dist/common/foreign-content.js
    ./frontend/node_modules/parse5/dist/common/foreign-content.d.ts
    ./frontend/node_modules/parse5/dist/common/token.d.ts
    ./frontend/node_modules/parse5/dist/common/error-codes.js
    ./frontend/node_modules/parse5/dist/common/html.js
    ./frontend/node_modules/@bramus/specificity/src/index.js
    ./frontend/node_modules/caniuse-lite/data/regions/DO.js
    ./frontend/node_modules/caniuse-lite/data/regions/VN.js
    ./frontend/node_modules/caniuse-lite/data/regions/SO.js
    ./frontend/node_modules/caniuse-lite/data/regions/TR.js
    ./frontend/node_modules/caniuse-lite/data/regions/CR.js
    ./frontend/node_modules/caniuse-lite/data/regions/BJ.js
    ./frontend/node_modules/caniuse-lite/data/regions/PK.js
    ./frontend/node_modules/caniuse-lite/data/regions/RW.js
    ./frontend/node_modules/caniuse-lite/data/regions/alt-eu.js
    ./frontend/node_modules/caniuse-lite/data/regions/LI.js
    ./frontend/node_modules/caniuse-lite/data/regions/TJ.js
    ./frontend/node_modules/caniuse-lite/data/regions/FK.js
    ./frontend/node_modules/caniuse-lite/data/regions/NU.js
    ./frontend/node_modules/caniuse-lite/data/regions/PS.js
    ./frontend/node_modules/caniuse-lite/data/regions/BR.js
    ./frontend/node_modules/caniuse-lite/data/regions/OM.js
    ./frontend/node_modules/caniuse-lite/data/regions/RO.js
    ./frontend/node_modules/caniuse-lite/data/regions/MQ.js
    ./frontend/node_modules/caniuse-lite/data/regions/JP.js
    ./frontend/node_modules/caniuse-lite/data/regions/BN.js
    ./frontend/node_modules/caniuse-lite/data/regions/MM.js
    ./frontend/node_modules/caniuse-lite/data/regions/ES.js
    ./frontend/node_modules/caniuse-lite/data/regions/ZM.js
    ./frontend/node_modules/caniuse-lite/data/regions/RS.js
    ./frontend/node_modules/caniuse-lite/data/regions/IT.js
    ./frontend/node_modules/caniuse-lite/data/regions/SK.js
    ./frontend/node_modules/caniuse-lite/data/regions/LU.js
    ./frontend/node_modules/caniuse-lite/data/regions/DK.js
    ./frontend/node_modules/caniuse-lite/data/regions/KH.js
    ./frontend/node_modules/caniuse-lite/data/regions/CV.js
    ./frontend/node_modules/caniuse-lite/data/regions/NI.js
    ./frontend/node_modules/caniuse-lite/data/regions/TV.js
    ./frontend/node_modules/caniuse-lite/data/regions/GW.js
    ./frontend/node_modules/caniuse-lite/data/regions/PW.js
    ./frontend/node_modules/caniuse-lite/data/regions/MU.js
    ./frontend/node_modules/caniuse-lite/data/regions/HT.js
    ./frontend/node_modules/caniuse-lite/data/regions/IL.js
    ./frontend/node_modules/caniuse-lite/data/regions/AR.js
    ./frontend/node_modules/caniuse-lite/data/regions/KP.js
    ./frontend/node_modules/caniuse-lite/data/regions/CN.js
    ./frontend/node_modules/caniuse-lite/data/regions/TN.js
    ./frontend/node_modules/caniuse-lite/data/regions/FO.js
    ./frontend/node_modules/caniuse-lite/data/regions/GN.js
    ./frontend/node_modules/caniuse-lite/data/regions/BO.js
    ./frontend/node_modules/caniuse-lite/data/regions/PN.js
    ./frontend/node_modules/caniuse-lite/data/regions/ER.js
    ./frontend/node_modules/caniuse-lite/data/regions/WS.js
    ./frontend/node_modules/caniuse-lite/data/regions/ML.js
    ./frontend/node_modules/caniuse-lite/data/regions/DJ.js
    ./frontend/node_modules/caniuse-lite/data/regions/LT.js
    ./frontend/node_modules/caniuse-lite/data/regions/KI.js
    ./frontend/node_modules/caniuse-lite/data/regions/TW.js
    ./frontend/node_modules/caniuse-lite/data/regions/BW.js
    ./frontend/node_modules/caniuse-lite/data/regions/MT.js
    ./frontend/node_modules/caniuse-lite/data/regions/HU.js
    ./frontend/node_modules/caniuse-lite/data/regions/SR.js
    ./frontend/node_modules/caniuse-lite/data/regions/AS.js
    ./frontend/node_modules/caniuse-lite/data/regions/IM.js
    ./frontend/node_modules/caniuse-lite/data/regions/CO.js
    ./frontend/node_modules/caniuse-lite/data/regions/TO.js
    ./frontend/node_modules/caniuse-lite/data/regions/NP.js
    ./frontend/node_modules/caniuse-lite/data/regions/IQ.js
    ./frontend/node_modules/caniuse-lite/data/regions/AO.js
    ./frontend/node_modules/caniuse-lite/data/regions/SN.js
    ./frontend/node_modules/caniuse-lite/data/regions/NL.js
    ./frontend/node_modules/caniuse-lite/data/regions/FR.js
    ./frontend/node_modules/caniuse-lite/data/regions/KM.js
    ./frontend/node_modules/caniuse-lite/data/regions/MH.js
    ./frontend/node_modules/caniuse-lite/data/regions/SV.js
    ./frontend/node_modules/caniuse-lite/data/regions/AW.js
    ./frontend/node_modules/caniuse-lite/data/regions/FJ.js
    ./frontend/node_modules/caniuse-lite/data/regions/YT.js
    ./frontend/node_modules/caniuse-lite/data/regions/CK.js
    ./frontend/node_modules/caniuse-lite/data/regions/JM.js
    ./frontend/node_modules/caniuse-lite/data/regions/PR.js
    ./frontend/node_modules/caniuse-lite/data/regions/BS.js
    ./frontend/node_modules/caniuse-lite/data/regions/US.js
    ./frontend/node_modules/caniuse-lite/data/regions/GR.js
    ./frontend/node_modules/caniuse-lite/data/regions/MP.js
    ./frontend/node_modules/caniuse-lite/data/regions/alt-af.js
    ./frontend/node_modules/caniuse-lite/data/regions/NG.js
    ./frontend/node_modules/caniuse-lite/data/regions/CX.js
    ./frontend/node_modules/caniuse-lite/data/regions/DE.js
    ./frontend/node_modules/caniuse-lite/data/regions/SE.js
    ./frontend/node_modules/caniuse-lite/data/regions/AD.js
    ./frontend/node_modules/caniuse-lite/data/regions/MC.js
    ./frontend/node_modules/caniuse-lite/data/regions/PA.js
    ./frontend/node_modules/caniuse-lite/data/regions/GA.js
    ./frontend/node_modules/caniuse-lite/data/regions/QA.js
    ./frontend/node_modules/caniuse-lite/data/regions/LC.js
    ./frontend/node_modules/caniuse-lite/data/regions/RE.js
    ./frontend/node_modules/caniuse-lite/data/regions/EE.js
    ./frontend/node_modules/caniuse-lite/data/regions/PY.js
    ./frontend/node_modules/caniuse-lite/data/regions/GY.js
    ./frontend/node_modules/caniuse-lite/data/regions/alt-na.js
    ./frontend/node_modules/caniuse-lite/data/regions/MG.js
    ./frontend/node_modules/caniuse-lite/data/regions/GE.js
    ./frontend/node_modules/caniuse-lite/data/regions/PE.js
    ./frontend/node_modules/caniuse-lite/data/regions/BD.js
    ./frontend/node_modules/caniuse-lite/data/regions/NC.js
    ./frontend/node_modules/caniuse-lite/data/regions/SA.js
    ./frontend/node_modules/caniuse-lite/data/regions/KZ.js
    ./frontend/node_modules/caniuse-lite/data/regions/CD.js
    ./frontend/node_modules/caniuse-lite/data/regions/TD.js
    ./frontend/node_modules/caniuse-lite/data/regions/AX.js
    ./frontend/node_modules/caniuse-lite/data/regions/SY.js
    ./frontend/node_modules/caniuse-lite/data/regions/GD.js
    ./frontend/node_modules/caniuse-lite/data/regions/BE.js
    ./frontend/node_modules/caniuse-lite/data/regions/VA.js
    ./frontend/node_modules/caniuse-lite/data/regions/NZ.js
    ./frontend/node_modules/caniuse-lite/data/regions/NF.js
    ./frontend/node_modules/caniuse-lite/data/regions/KG.js
    ./frontend/node_modules/caniuse-lite/data/regions/CY.js
    ./frontend/node_modules/caniuse-lite/data/regions/VE.js
    ./frontend/node_modules/caniuse-lite/data/regions/SD.js
    ./frontend/node_modules/caniuse-lite/data/regions/AE.js
    ./frontend/node_modules/caniuse-lite/data/regions/BA.js
    ./frontend/node_modules/caniuse-lite/data/regions/UA.js
    ./frontend/node_modules/caniuse-lite/data/regions/CA.js
    ./frontend/node_modules/caniuse-lite/data/regions/LB.js
    ./frontend/node_modules/caniuse-lite/data/regions/MZ.js
    ./frontend/node_modules/caniuse-lite/data/regions/BY.js
    ./frontend/node_modules/caniuse-lite/data/regions/UY.js
    ./frontend/node_modules/caniuse-lite/data/regions/alt-sa.js
    ./frontend/node_modules/caniuse-lite/data/regions/PG.js
    ./frontend/node_modules/caniuse-lite/data/regions/BF.js
    ./frontend/node_modules/caniuse-lite/data/regions/GG.js
    ./frontend/node_modules/caniuse-lite/data/regions/ME.js
    ./frontend/node_modules/caniuse-lite/data/regions/SC.js
    ./frontend/node_modules/caniuse-lite/data/regions/NA.js
    ./frontend/node_modules/caniuse-lite/data/regions/EC.js
    ./frontend/node_modules/caniuse-lite/data/regions/AZ.js
    ./frontend/node_modules/caniuse-lite/data/regions/ID.js
    ./frontend/node_modules/caniuse-lite/data/regions/CF.js
    ./frontend/node_modules/caniuse-lite/data/regions/alt-oc.js
    ./frontend/node_modules/caniuse-lite/data/regions/SG.js
    ./frontend/node_modules/caniuse-lite/data/regions/AF.js
    ./frontend/node_modules/caniuse-lite/data/regions/LY.js
    ./frontend/node_modules/caniuse-lite/data/regions/YE.js
    ./frontend/node_modules/caniuse-lite/data/regions/CZ.js
    ./frontend/node_modules/caniuse-lite/data/regions/NE.js
    ./frontend/node_modules/caniuse-lite/data/regions/TZ.js
    ./frontend/node_modules/caniuse-lite/data/regions/BB.js
    ./frontend/node_modules/caniuse-lite/data/regions/MA.js
    ./frontend/node_modules/caniuse-lite/data/regions/ZA.js
    ./frontend/node_modules/caniuse-lite/data/regions/LA.js
    ./frontend/node_modules/caniuse-lite/data/regions/UZ.js
    ./frontend/node_modules/caniuse-lite/data/regions/BZ.js
    ./frontend/node_modules/caniuse-lite/data/regions/MY.js
    ./frontend/node_modules/caniuse-lite/data/regions/EG.js
    ./frontend/node_modules/caniuse-lite/data/regions/WF.js
    ./frontend/node_modules/caniuse-lite/data/regions/AG.js
    ./frontend/node_modules/caniuse-lite/data/regions/VG.js
    ./frontend/node_modules/caniuse-lite/data/regions/KE.js
    ./frontend/node_modules/caniuse-lite/data/regions/GB.js
    ./frontend/node_modules/caniuse-lite/data/regions/TC.js
    ./frontend/node_modules/caniuse-lite/data/regions/JE.js
    ./frontend/node_modules/caniuse-lite/data/regions/MX.js
    ./frontend/node_modules/caniuse-lite/data/regions/PF.js
    ./frontend/node_modules/caniuse-lite/data/regions/BG.js
    ./frontend/node_modules/caniuse-lite/data/regions/UG.js
    ./frontend/node_modules/caniuse-lite/data/regions/GF.js
    ./frontend/node_modules/caniuse-lite/data/regions/MD.js
    ./frontend/node_modules/caniuse-lite/data/regions/VC.js
    ./frontend/node_modules/caniuse-lite/data/regions/SB.js
    ./frontend/node_modules/caniuse-lite/data/regions/DZ.js
    ./frontend/node_modules/caniuse-lite/data/regions/IE.js
    ./frontend/node_modules/caniuse-lite/data/regions/SZ.js
    ./frontend/node_modules/caniuse-lite/data/regions/TG.js
    ./frontend/node_modules/caniuse-lite/data/regions/KY.js
    ./frontend/node_modules/caniuse-lite/data/regions/CG.js
    ./frontend/node_modules/caniuse-lite/data/regions/HN.js
    ./frontend/node_modules/caniuse-lite/data/regions/MO.js
    ./frontend/node_modules/caniuse-lite/data/regions/PM.js
    ./frontend/node_modules/caniuse-lite/data/regions/GM.js
    ./frontend/node_modules/caniuse-lite/data/regions/TT.js
    ./frontend/node_modules/caniuse-lite/data/regions/SI.js
    ./frontend/node_modules/caniuse-lite/data/regions/ZW.js
    ./frontend/node_modules/caniuse-lite/data/regions/MW.js
    ./frontend/node_modules/caniuse-lite/data/regions/BT.js
    ./frontend/node_modules/caniuse-lite/data/regions/GU.js
    ./frontend/node_modules/caniuse-lite/data/regions/TL.js
    ./frontend/node_modules/caniuse-lite/data/regions/FM.js
    ./frontend/node_modules/caniuse-lite/data/regions/CL.js
    ./frontend/node_modules/caniuse-lite/data/regions/KR.js
    ./frontend/node_modules/caniuse-lite/data/regions/IN.js
    ./frontend/node_modules/caniuse-lite/data/regions/KN.js
    ./frontend/node_modules/caniuse-lite/data/regions/NO.js
    ./frontend/node_modules/caniuse-lite/data/regions/IR.js
    ./frontend/node_modules/caniuse-lite/data/regions/AL.js
    ./frontend/node_modules/caniuse-lite/data/regions/SM.js
    ./frontend/node_modules/caniuse-lite/data/regions/LS.js
    ./frontend/node_modules/caniuse-lite/data/regions/DM.js
    ./frontend/node_modules/caniuse-lite/data/regions/MK.js
    ./frontend/node_modules/caniuse-lite/data/regions/RU.js
    ./frontend/node_modules/caniuse-lite/data/regions/GI.js
    ./frontend/node_modules/caniuse-lite/data/regions/BH.js
    ./frontend/node_modules/caniuse-lite/data/regions/alt-an.js
    ./frontend/node_modules/caniuse-lite/data/regions/CH.js
    ./frontend/node_modules/caniuse-lite/data/regions/TH.js
    ./frontend/node_modules/caniuse-lite/data/regions/FI.js
    ./frontend/node_modules/caniuse-lite/data/regions/AT.js
    ./frontend/node_modules/caniuse-lite/data/regions/LK.js
    ./frontend/node_modules/caniuse-lite/data/regions/MS.js
    ./frontend/node_modules/caniuse-lite/data/regions/HR.js
    ./frontend/node_modules/caniuse-lite/data/regions/GQ.js
    ./frontend/node_modules/caniuse-lite/data/regions/AM.js
    ./frontend/node_modules/caniuse-lite/data/regions/SL.js
    ./frontend/node_modules/caniuse-lite/data/regions/IS.js
    ./frontend/node_modules/caniuse-lite/data/regions/LR.js
    ./frontend/node_modules/caniuse-lite/data/regions/ET.js
    ./frontend/node_modules/caniuse-lite/data/regions/HK.js
    ./frontend/node_modules/caniuse-lite/data/regions/GH.js
    ./frontend/node_modules/caniuse-lite/data/regions/BI.js
    ./frontend/node_modules/caniuse-lite/data/regions/PH.js
    ./frontend/node_modules/caniuse-lite/data/regions/alt-ww.js
    ./frontend/node_modules/caniuse-lite/data/regions/CI.js
    ./frontend/node_modules/caniuse-lite/data/regions/KW.js
    ./frontend/node_modules/caniuse-lite/data/regions/ST.js
    ./frontend/node_modules/caniuse-lite/data/regions/AU.js
    ./frontend/node_modules/caniuse-lite/data/regions/VU.js
    ./frontend/node_modules/caniuse-lite/data/regions/MR.js
    ./frontend/node_modules/caniuse-lite/data/regions/GP.js
    ./frontend/node_modules/caniuse-lite/data/regions/JO.js
    ./frontend/node_modules/caniuse-lite/data/regions/MN.js
    ./frontend/node_modules/caniuse-lite/data/regions/BM.js
    ./frontend/node_modules/caniuse-lite/data/regions/PL.js
    ./frontend/node_modules/caniuse-lite/data/regions/GL.js
    ./frontend/node_modules/caniuse-lite/data/regions/CU.js
    ./frontend/node_modules/caniuse-lite/data/regions/LV.js
    ./frontend/node_modules/caniuse-lite/data/regions/VI.js
    ./frontend/node_modules/caniuse-lite/data/regions/AI.js
    ./frontend/node_modules/caniuse-lite/data/regions/SH.js
    ./frontend/node_modules/caniuse-lite/data/regions/alt-as.js
    ./frontend/node_modules/caniuse-lite/data/regions/MV.js
    ./frontend/node_modules/caniuse-lite/data/regions/PT.js
    ./frontend/node_modules/caniuse-lite/data/regions/GT.js
    ./frontend/node_modules/caniuse-lite/data/regions/NR.js
    ./frontend/node_modules/caniuse-lite/data/regions/TM.js
    ./frontend/node_modules/caniuse-lite/data/regions/CM.js
    ./frontend/node_modules/caniuse-lite/dist/unpacker/browsers.js
    ./frontend/node_modules/caniuse-lite/dist/unpacker/browserVersions.js
    ./frontend/node_modules/caniuse-lite/dist/unpacker/index.js
    ./frontend/node_modules/caniuse-lite/dist/unpacker/features.js
    ./frontend/node_modules/caniuse-lite/dist/unpacker/feature.js
    ./frontend/node_modules/caniuse-lite/dist/unpacker/agents.js
    ./frontend/node_modules/caniuse-lite/dist/unpacker/region.js
    ./frontend/node_modules/parse5/dist/tokenizer/index.d.ts
    ./frontend/node_modules/parse5/dist/tokenizer/index.js
    ./frontend/node_modules/parse5/dist/tokenizer/preprocessor.js
    ./frontend/node_modules/parse5/dist/tokenizer/preprocessor.d.ts
    ./frontend/node_modules/@babel/types/package.json
    ./frontend/node_modules/@babel/types/README.md
    ./frontend/node_modules/@babel/types/LICENSE
    ./frontend/node_modules/parse5/dist/tree-adapters/default.d.ts
    ./frontend/node_modules/parse5/dist/tree-adapters/default.js
    ./frontend/node_modules/parse5/dist/tree-adapters/interface.d.ts
    ./frontend/node_modules/parse5/dist/tree-adapters/interface.js
    ./frontend/node_modules/parse5/LICENSE
    ./frontend/node_modules/parse5/dist/parser/index.d.ts
    ./frontend/node_modules/parse5/dist/parser/open-element-stack.d.ts
    ./frontend/node_modules/parse5/dist/parser/index.js
    ./frontend/node_modules/parse5/dist/parser/formatting-element-list.js
    ./frontend/node_modules/parse5/dist/parser/open-element-stack.js
    ./frontend/node_modules/parse5/dist/parser/formatting-element-list.d.ts
    ./frontend/node_modules/@babel/runtime/helpers/writeOnlyError.js
    ./frontend/node_modules/@babel/runtime/helpers/isNativeReflectConstruct.js
    ./frontend/node_modules/@babel/runtime/helpers/classPrivateFieldDestructureSet.js
    ./frontend/node_modules/@babel/runtime/helpers/temporalRef.js
    ./frontend/node_modules/@babel/runtime/helpers/initializerDefineProperty.js
    ./frontend/node_modules/@babel/runtime/helpers/dispose.js
    ./frontend/node_modules/@babel/runtime/helpers/applyDecoratedDescriptor.js
    ./frontend/node_modules/@babel/runtime/helpers/toPrimitive.js
    ./frontend/node_modules/@babel/runtime/helpers/OverloadYield.js
    ./frontend/node_modules/@babel/runtime/helpers/awaitAsyncGenerator.js
    ./frontend/node_modules/@babel/runtime/helpers/isNativeFunction.js
    ./frontend/node_modules/@babel/runtime/helpers/classPrivateMethodGet.js
    ./frontend/node_modules/@babel/runtime/helpers/defaults.js
    ./frontend/node_modules/@babel/runtime/helpers/construct.js
    ./frontend/node_modules/@babel/runtime/helpers/classPrivateSetter.js
    ./frontend/node_modules/@babel/runtime/helpers/toPropertyKey.js
    ./frontend/node_modules/@babel/runtime/helpers/defineEnumerableProperties.js
    ./frontend/node_modules/@babel/runtime/helpers/wrapNativeSuper.js
    ./frontend/node_modules/@babel/runtime/helpers/applyDecs2203.js
    ./frontend/node_modules/@babel/runtime/helpers/objectWithoutPropertiesLoose.js
    ./frontend/node_modules/@babel/runtime/helpers/createSuper.js
    ./frontend/node_modules/@babel/runtime/helpers/assertClassBrand.js
    ./frontend/node_modules/@babel/runtime/helpers/nullishReceiverError.js
    ./frontend/node_modules/@babel/runtime/helpers/createForOfIteratorHelperLoose.js
    ./frontend/node_modules/@babel/runtime/helpers/regeneratorAsyncIterator.js
    ./frontend/node_modules/@babel/runtime/helpers/inherits.js
    ./frontend/node_modules/@babel/runtime/helpers/classPrivateGetter.js
    ./frontend/node_modules/@babel/runtime/helpers/classPrivateMethodSet.js
    ./frontend/node_modules/@babel/runtime/helpers/arrayLikeToArray.js
    ./frontend/node_modules/@babel/runtime/helpers/slicedToArray.js
    ./frontend/node_modules/@babel/runtime/helpers/applyDecs.js
    ./frontend/node_modules/@babel/runtime/helpers/setPrototypeOf.js
    ./frontend/node_modules/@babel/runtime/helpers/usingCtx.js
    ./frontend/node_modules/@babel/runtime/helpers/nonIterableSpread.js
    ./frontend/node_modules/@babel/runtime/helpers/setFunctionName.js
    ./frontend/node_modules/@babel/runtime/helpers/regenerator.js
    ./frontend/node_modules/@babel/runtime/helpers/classExtractFieldDescriptor.js
    ./frontend/node_modules/@babel/runtime/helpers/identity.js
    ./frontend/node_modules/@babel/runtime/helpers/tdz.js
    ./frontend/node_modules/@babel/runtime/helpers/superPropBase.js
    ./frontend/node_modules/@babel/runtime/helpers/checkInRHS.js
    ./frontend/node_modules/@babel/runtime/helpers/classStaticPrivateFieldDestructureSet.js
    ./frontend/node_modules/@babel/runtime/helpers/taggedTemplateLiteral.js
    ./frontend/node_modules/@babel/runtime/helpers/get.js
    ./frontend/node_modules/@babel/runtime/helpers/regeneratorAsyncGen.js
    ./frontend/node_modules/@babel/runtime/helpers/iterableToArrayLimit.js
    ./frontend/node_modules/@babel/runtime/helpers/classStaticPrivateMethodGet.js
    ./frontend/node_modules/@babel/runtime/helpers/checkPrivateRedeclaration.js
    ./frontend/node_modules/@babel/runtime/helpers/AwaitValue.js
    ./frontend/node_modules/@babel/runtime/helpers/tsRewriteRelativeImportExtensions.js
    ./frontend/node_modules/@babel/runtime/helpers/getPrototypeOf.js
    ./frontend/node_modules/@babel/runtime/helpers/typeof.js
    ./frontend/node_modules/@babel/runtime/helpers/classStaticPrivateMethodSet.js
    ./frontend/node_modules/@babel/runtime/helpers/importDeferProxy.js
    ./frontend/node_modules/@babel/runtime/helpers/temporalUndefined.js
    ./frontend/node_modules/@babel/runtime/helpers/wrapAsyncGenerator.js
    ./frontend/node_modules/@babel/runtime/helpers/classNameTDZError.js
    ./frontend/node_modules/@babel/runtime/helpers/applyDecs2203R.js
    ./frontend/node_modules/@babel/runtime/helpers/classApplyDescriptorDestructureSet.js
    ./frontend/node_modules/@babel/runtime/helpers/unsupportedIterableToArray.js
    ./frontend/node_modules/@babel/runtime/helpers/classCallCheck.js
    ./frontend/node_modules/@babel/runtime/helpers/classPrivateFieldGet2.js
    ./frontend/node_modules/@babel/runtime/helpers/objectSpread2.js
    ./frontend/node_modules/@babel/runtime/helpers/skipFirstGeneratorNext.js
    ./frontend/node_modules/@babel/runtime/helpers/asyncGeneratorDelegate.js
    ./frontend/node_modules/@babel/runtime/helpers/set.js
    ./frontend/node_modules/@babel/runtime/helpers/maybeArrayLike.js
    ./frontend/node_modules/@babel/runtime/helpers/classPrivateFieldGet.js
    ./frontend/node_modules/@babel/runtime/helpers/defineProperty.js
    ./frontend/node_modules/@babel/runtime/helpers/regeneratorAsync.js
    ./frontend/node_modules/@babel/runtime/helpers/objectSpread.js
    ./frontend/node_modules/@babel/runtime/helpers/initializerWarningHelper.js
    ./frontend/node_modules/@babel/runtime/helpers/classApplyDescriptorGet.js
    ./frontend/node_modules/@babel/runtime/helpers/classPrivateFieldInitSpec.js
    ./frontend/node_modules/@babel/runtime/helpers/extends.js
    ./frontend/node_modules/@babel/runtime/helpers/wrapRegExp.js
    ./frontend/node_modules/@babel/runtime/helpers/classCheckPrivateStaticAccess.js
    ./frontend/node_modules/@babel/runtime/helpers/classStaticPrivateFieldSpecGet.js
    ./frontend/node_modules/@babel/runtime/helpers/superPropGet.js
    ./frontend/node_modules/@babel/runtime/helpers/toConsumableArray.js
    ./frontend/node_modules/@babel/runtime/helpers/regeneratorValues.js
    ./frontend/node_modules/@babel/runtime/helpers/classPrivateFieldLooseKey.js
    ./frontend/node_modules/@babel/runtime/helpers/classPrivateMethodInitSpec.js
    ./frontend/node_modules/@babel/runtime/helpers/superPropSet.js
    ./frontend/node_modules/@babel/runtime/helpers/classStaticPrivateFieldSpecSet.js
    ./frontend/node_modules/@babel/runtime/helpers/iterableToArray.js
    ./frontend/node_modules/@babel/runtime/helpers/createForOfIteratorHelper.js
    ./frontend/node_modules/@babel/runtime/helpers/defineAccessor.js
    ./frontend/node_modules/@babel/runtime/helpers/classPrivateFieldSet.js
    ./frontend/node_modules/@babel/runtime/helpers/regeneratorDefine.js
    ./frontend/node_modules/@babel/runtime/helpers/toArray.js
    ./frontend/node_modules/@babel/runtime/helpers/classPrivateFieldLooseBase.js
    ./frontend/node_modules/@babel/runtime/helpers/possibleConstructorReturn.js
    ./frontend/node_modules/@babel/runtime/helpers/classApplyDescriptorSet.js
    ./frontend/node_modules/@babel/runtime/helpers/applyDecs2311.js
    ./frontend/node_modules/@bramus/specificity/src/util/filter.js
    ./frontend/node_modules/@bramus/specificity/src/util/compare.js
    ./frontend/node_modules/@bramus/specificity/src/util/index.js
    ./frontend/node_modules/@bramus/specificity/src/util/sort.js
    ./frontend/node_modules/@babel/types/lib/definitions/experimental.js.map
    ./frontend/node_modules/@babel/types/lib/definitions/utils.js.map
    ./frontend/node_modules/@babel/types/lib/definitions/utils.js
    ./frontend/node_modules/@babel/types/lib/definitions/misc.js.map
    ./frontend/node_modules/@babel/types/lib/definitions/index.js.map
    ./frontend/node_modules/@babel/types/lib/definitions/placeholders.js.map
    ./frontend/node_modules/@babel/types/lib/definitions/placeholders.js
    ./frontend/node_modules/@babel/types/lib/definitions/experimental.js
    ./frontend/node_modules/@babel/types/lib/definitions/core.js.map
    ./frontend/node_modules/@babel/types/lib/definitions/index.js
    ./frontend/node_modules/@babel/types/lib/definitions/deprecated-aliases.js.map
    ./frontend/node_modules/@babel/types/lib/definitions/flow.js.map
    ./frontend/node_modules/@babel/types/lib/definitions/misc.js
    ./frontend/node_modules/@babel/types/lib/definitions/typescript.js.map
    ./frontend/node_modules/@babel/types/lib/definitions/core.js
    ./frontend/node_modules/@babel/types/lib/definitions/flow.js
    ./frontend/node_modules/@babel/types/lib/definitions/typescript.js
    ./frontend/node_modules/@babel/types/lib/definitions/jsx.js
    ./frontend/node_modules/@babel/types/lib/definitions/deprecated-aliases.js
    ./frontend/node_modules/@babel/types/lib/definitions/jsx.js.map
    ./frontend/node_modules/@babel/types/lib/index.d.ts
    ./frontend/node_modules/@babel/types/lib/converters/toSequenceExpression.js
    ./frontend/node_modules/@babel/types/lib/converters/toIdentifier.js.map
    ./frontend/node_modules/@babel/types/lib/converters/toBindingIdentifierName.js
    ./frontend/node_modules/@babel/types/lib/converters/toSequenceExpression.js.map
    ./frontend/node_modules/@babel/types/lib/converters/gatherSequenceExpressions.js
    ./frontend/node_modules/@babel/types/lib/converters/toBlock.js.map
    ./frontend/node_modules/@babel/types/lib/converters/toIdentifier.js
    ./frontend/node_modules/@babel/types/lib/converters/toKeyAlias.js.map
    ./frontend/node_modules/@babel/types/lib/converters/toComputedKey.js
    ./frontend/node_modules/@babel/types/lib/converters/toExpression.js
    ./frontend/node_modules/@babel/types/lib/converters/toBindingIdentifierName.js.map
    ./frontend/node_modules/@babel/types/lib/converters/toBlock.js
    ./frontend/node_modules/@babel/types/lib/converters/ensureBlock.js.map
    ./frontend/node_modules/@babel/types/lib/converters/toComputedKey.js.map
    ./frontend/node_modules/@babel/types/lib/converters/valueToNode.js.map
    ./frontend/node_modules/@babel/types/lib/converters/toStatement.js.map
    ./frontend/node_modules/@babel/types/lib/converters/toStatement.js
    ./frontend/node_modules/@babel/types/lib/converters/ensureBlock.js
    ./frontend/node_modules/@babel/types/lib/converters/toExpression.js.map
    ./frontend/node_modules/@babel/types/lib/converters/valueToNode.js
    ./frontend/node_modules/@babel/types/lib/converters/toKeyAlias.js
    ./frontend/node_modules/@babel/types/lib/converters/gatherSequenceExpressions.js.map
    ./frontend/node_modules/@babel/code-frame/lib/index.js.map
    ./frontend/node_modules/@babel/code-frame/lib/index.js
    ./frontend/node_modules/@babel/code-frame/package.json
    ./frontend/node_modules/@babel/code-frame/README.md
    ./frontend/node_modules/@babel/code-frame/LICENSE
    ./frontend/node_modules/@bramus/specificity/src/core/index.js
    ./frontend/node_modules/@bramus/specificity/src/core/calculate.js
    ./frontend/node_modules/@bramus/specificity/index.d.ts
    ./frontend/node_modules/@bramus/specificity/package.json
    ./frontend/node_modules/@bramus/specificity/README.md
    ./frontend/node_modules/@babel/helper-string-parser/lib/index.js.map
    ./frontend/node_modules/@babel/helper-string-parser/lib/index.js
    ./frontend/node_modules/@babel/helper-string-parser/package.json
    ./frontend/node_modules/@babel/helper-string-parser/README.md
    ./frontend/node_modules/@babel/helper-string-parser/LICENSE
    ./frontend/node_modules/@babel/helper-validator-option/README.md
    ./frontend/node_modules/@babel/helper-validator-option/LICENSE
    ./frontend/node_modules/@babel/helper-validator-option/package.json
    ./frontend/node_modules/@babel/helper-validator-option/lib/index.js.map
    ./frontend/node_modules/@babel/helper-validator-option/lib/find-suggestion.js
    ./frontend/node_modules/@babel/helper-validator-option/lib/index.js
    ./frontend/node_modules/@babel/helper-validator-option/lib/validator.js
    ./frontend/node_modules/@babel/helper-validator-option/lib/find-suggestion.js.map
    ./frontend/node_modules/@babel/helper-validator-option/lib/validator.js.map
    ./frontend/node_modules/@bramus/specificity/dist/index.js.map
    ./frontend/node_modules/@bramus/specificity/dist/index.cjs
    ./frontend/node_modules/@bramus/specificity/dist/index.cjs.map
    ./frontend/node_modules/@bramus/specificity/dist/index.js
    ./frontend/node_modules/@babel/helper-globals/data/builtin-lower.json
    ./frontend/node_modules/@babel/helper-globals/data/browser-upper.json
    ./frontend/node_modules/@babel/helper-globals/data/builtin-upper.json
    ./frontend/node_modules/@babel/helper-globals/package.json
    ./frontend/node_modules/@babel/helper-globals/README.md
    ./frontend/node_modules/@babel/helper-globals/LICENSE
    ./frontend/node_modules/@babel/runtime/helpers/applyDecs2305.js
    ./frontend/node_modules/@babel/runtime/helpers/using.js
    ./frontend/node_modules/@babel/runtime/helpers/taggedTemplateLiteralLoose.js
    ./frontend/node_modules/@babel/runtime/helpers/regeneratorRuntime.js
    ./frontend/node_modules/@babel/runtime/helpers/interopRequireWildcard.js
    ./frontend/node_modules/@babel/runtime/helpers/arrayWithoutHoles.js
    ./frontend/node_modules/@babel/runtime/helpers/jsx.js
    ./frontend/node_modules/@babel/runtime/helpers/toSetter.js
    ./frontend/node_modules/@babel/runtime/helpers/asyncToGenerator.js
    ./frontend/node_modules/@babel/runtime/helpers/createClass.js
    ./frontend/node_modules/@babel/runtime/helpers/objectDestructuringEmpty.js
    ./frontend/node_modules/@babel/runtime/helpers/interopRequireDefault.js
    ./frontend/node_modules/@babel/runtime/package.json
    ./frontend/node_modules/@babel/runtime/README.md
    ./frontend/node_modules/@babel/runtime/LICENSE
    ./frontend/node_modules/@babel/runtime/helpers/newArrowCheck.js
    ./frontend/node_modules/@babel/runtime/helpers/decorate.js
    ./frontend/node_modules/@babel/runtime/helpers/arrayWithHoles.js
    ./frontend/node_modules/@babel/runtime/helpers/classCheckPrivateStaticFieldDescriptor.js
    ./frontend/node_modules/@babel/runtime/helpers/instanceof.js
    ./frontend/node_modules/@babel/runtime/helpers/inheritsLoose.js
    ./frontend/node_modules/@babel/runtime/helpers/readOnlyError.js
    ./frontend/node_modules/@babel/runtime/helpers/regeneratorKeys.js
    ./frontend/node_modules/@babel/runtime/helpers/objectWithoutProperties.js
    ./frontend/node_modules/@babel/runtime/helpers/asyncIterator.js
    ./frontend/node_modules/@babel/runtime/helpers/nonIterableRest.js
    ./frontend/node_modules/@babel/runtime/helpers/applyDecs2301.js
    ./frontend/node_modules/@babel/runtime/helpers/assertThisInitialized.js
    ./frontend/node_modules/@babel/runtime/helpers/classPrivateFieldSet2.js
    ./frontend/node_modules/@babel/runtime/helpers/callSuper.js
    ./frontend/node_modules/@babel/types/lib/constants/index.js.map
    ./frontend/node_modules/@babel/types/lib/constants/index.js
    ./frontend/node_modules/@babel/types/lib/comments/inheritLeadingComments.js.map
    ./frontend/node_modules/@babel/types/lib/comments/inheritsComments.js.map
    ./frontend/node_modules/@babel/types/lib/comments/addComments.js.map
    ./frontend/node_modules/@babel/types/lib/comments/inheritInnerComments.js.map
    ./frontend/node_modules/@babel/types/lib/comments/addComment.js.map
    ./frontend/node_modules/@babel/types/lib/comments/removeComments.js.map
    ./frontend/node_modules/@babel/types/lib/comments/addComments.js
    ./frontend/node_modules/@babel/types/lib/comments/addComment.js
    ./frontend/node_modules/@babel/types/lib/comments/inheritsComments.js
    ./frontend/node_modules/@babel/types/lib/comments/removeComments.js
    ./frontend/node_modules/@babel/types/lib/comments/inheritTrailingComments.js.map
    ./frontend/node_modules/@babel/types/lib/comments/inheritLeadingComments.js
    ./frontend/node_modules/@babel/types/lib/comments/inheritTrailingComments.js
    ./frontend/node_modules/@babel/types/lib/comments/inheritInnerComments.js
    ./frontend/node_modules/@babel/core/src/transform-file.ts
    ./frontend/node_modules/@babel/types/lib/builders/flow/createTypeAnnotationBasedOnTypeof.js
    ./frontend/node_modules/@babel/types/lib/builders/flow/createFlowUnionType.js.map
    ./frontend/node_modules/@babel/types/lib/builders/flow/createTypeAnnotationBasedOnTypeof.js.map
    ./frontend/node_modules/@babel/types/lib/builders/flow/createFlowUnionType.js
    ./frontend/node_modules/@babel/types/lib/builders/productions.js.map
    ./frontend/node_modules/@babel/types/lib/validators/isSpecifierDefault.js
    ./frontend/node_modules/@babel/types/lib/validators/isBlockScoped.js.map
    ./frontend/node_modules/@bramus/specificity/bin/cli.js
    ./frontend/node_modules/@bramus/specificity/LICENSE
    ./frontend/node_modules/@babel/helper-compilation-targets/lib/debug.js
    ./frontend/node_modules/@babel/helper-compilation-targets/lib/targets.js.map
    ./frontend/node_modules/@babel/helper-compilation-targets/lib/pretty.js
    ./frontend/node_modules/@babel/helper-compilation-targets/lib/utils.js.map
    ./frontend/node_modules/@babel/helper-compilation-targets/lib/debug.js.map
    ./frontend/node_modules/@babel/helper-compilation-targets/lib/utils.js
    ./frontend/node_modules/@babel/helper-compilation-targets/lib/index.js.map
    ./frontend/node_modules/@babel/helper-compilation-targets/lib/pretty.js.map
    ./frontend/node_modules/@babel/helper-compilation-targets/lib/filter-items.js
    ./frontend/node_modules/@babel/helper-compilation-targets/lib/options.js.map
    ./frontend/node_modules/@babel/helper-compilation-targets/lib/targets.js
    ./frontend/node_modules/@babel/helper-compilation-targets/lib/index.js
    ./frontend/node_modules/@babel/helper-compilation-targets/lib/options.js
    ./frontend/node_modules/@babel/helper-compilation-targets/lib/filter-items.js.map
    ./frontend/node_modules/@babel/helper-compilation-targets/package.json
    ./frontend/node_modules/@babel/helper-compilation-targets/README.md
    ./frontend/node_modules/@babel/helper-compilation-targets/LICENSE
    ./frontend/node_modules/@babel/types/lib/constants/generated/index.js.map
    ./frontend/node_modules/@babel/types/lib/constants/generated/index.js
    ./frontend/node_modules/@babel/parser/lib/index.js.map
    ./frontend/node_modules/@babel/parser/lib/index.js
    ./frontend/node_modules/@babel/parser/package.json
    ./frontend/node_modules/@babel/parser/README.md
    ./frontend/node_modules/@babel/types/lib/retrievers/getAssignmentIdentifiers.js.map
    ./frontend/node_modules/@babel/types/lib/retrievers/getBindingIdentifiers.js
    ./frontend/node_modules/@babel/types/lib/retrievers/getOuterBindingIdentifiers.js
    ./frontend/node_modules/@babel/types/lib/retrievers/getFunctionName.js.map
    ./frontend/node_modules/@babel/types/lib/retrievers/getFunctionName.js
    ./frontend/node_modules/@babel/types/lib/retrievers/getBindingIdentifiers.js.map
    ./frontend/node_modules/@babel/types/lib/retrievers/getOuterBindingIdentifiers.js.map
    ./frontend/node_modules/@babel/types/lib/retrievers/getAssignmentIdentifiers.js
    ./frontend/node_modules/@babel/types/lib/builders/typescript/createTSUnionType.js.map
    ./frontend/node_modules/@babel/types/lib/builders/typescript/createTSUnionType.js
    ./frontend/node_modules/@babel/types/lib/builders/validateNode.js
    ./frontend/node_modules/@babel/types/lib/builders/validateNode.js.map
    ./frontend/node_modules/@babel/types/lib/builders/productions.js
    ./frontend/node_modules/@babel/types/lib/validators/isBinding.js
    ./frontend/node_modules/@babel/types/lib/validators/isVar.js
    ./frontend/node_modules/@babel/types/lib/validators/isValidES3Identifier.js.map
    ./frontend/node_modules/@babel/types/lib/validators/buildMatchMemberExpression.js
    ./frontend/node_modules/@babel/types/lib/validators/isLet.js
    ./frontend/node_modules/@babel/types/lib/validators/matchesPattern.js.map
    ./frontend/node_modules/@babel/types/lib/validators/isValidIdentifier.js.map
    ./frontend/node_modules/@babel/types/lib/validators/isType.js.map
    ./frontend/node_modules/@babel/types/lib/validators/isNodesEquivalent.js
    ./frontend/node_modules/@babel/types/lib/validators/is.js
    ./frontend/node_modules/@babel/types/lib/validators/isNode.js.map
    ./frontend/node_modules/@babel/types/lib/validators/isValidIdentifier.js
    ./frontend/node_modules/@babel/core/src/config/files/index.ts
    ./frontend/node_modules/@babel/core/src/config/files/index-browser.ts
    ./frontend/node_modules/@babel/core/src/config/resolve-targets-browser.ts
    ./frontend/node_modules/@babel/core/src/config/resolve-targets.ts
    ./frontend/node_modules/@babel/types/lib/builders/react/buildChildren.js.map
    ./frontend/node_modules/@babel/types/lib/builders/react/buildChildren.js
    ./frontend/node_modules/@babel/types/lib/validators/validate.js.map
    ./frontend/node_modules/@babel/types/lib/validators/isVar.js.map
    ./frontend/node_modules/@babel/types/lib/validators/isBlockScoped.js
    ./frontend/node_modules/@babel/types/lib/validators/isImmutable.js.map
    ./frontend/node_modules/@babel/types/lib/validators/isPlaceholderType.js.map
    ./frontend/node_modules/@babel/types/lib/validators/isSpecifierDefault.js.map
    ./frontend/node_modules/@babel/types/lib/validators/isBinding.js.map
    ./frontend/node_modules/@babel/types/lib/validators/isType.js
    ./frontend/node_modules/@babel/types/lib/validators/isScope.js.map
    ./frontend/node_modules/@babel/types/lib/validators/isReferenced.js
    ./frontend/node_modules/@babel/types/lib/validators/isReferenced.js.map
    ./frontend/node_modules/@babel/types/lib/validators/validate.js
    ./frontend/node_modules/@babel/types/lib/validators/isNode.js
    ./frontend/node_modules/@babel/types/lib/validators/isNodesEquivalent.js.map
    ./frontend/node_modules/@babel/types/lib/validators/isValidES3Identifier.js
    ./frontend/node_modules/@babel/types/lib/validators/isPlaceholderType.js
    ./frontend/node_modules/@babel/types/lib/validators/matchesPattern.js
    ./frontend/node_modules/@babel/types/lib/validators/isLet.js.map
    ./frontend/node_modules/@babel/types/lib/validators/buildMatchMemberExpression.js.map
    ./frontend/node_modules/@babel/types/lib/validators/isImmutable.js
    ./frontend/node_modules/@babel/types/lib/validators/isScope.js
    ./frontend/node_modules/@babel/types/lib/validators/is.js.map
    ./frontend/node_modules/@babel/core/package.json
    ./frontend/node_modules/@babel/core/README.md
    ./frontend/node_modules/@babel/core/LICENSE
    ./frontend/node_modules/@babel/core/src/transform-file-browser.ts
    ./frontend/node_modules/@babel/parser/LICENSE
    ./frontend/node_modules/@babel/parser/typings/babel-parser.d.ts
    ./frontend/node_modules/@babel/parser/CHANGELOG.md
    ./frontend/node_modules/@babel/types/lib/builders/generated/uppercase.js
    ./frontend/node_modules/@babel/types/lib/builders/generated/index.js.map
    ./frontend/node_modules/@babel/types/lib/builders/generated/uppercase.js.map
    ./frontend/node_modules/@babel/types/lib/builders/generated/lowercase.js
    ./frontend/node_modules/@babel/types/lib/builders/generated/index.js
    ./frontend/node_modules/@babel/types/lib/builders/generated/lowercase.js.map
    ./frontend/node_modules/@babel/types/lib/index.js.flow
    ./frontend/node_modules/@babel/types/lib/index-legacy.d.ts
    ./frontend/node_modules/@babel/types/lib/validators/react/isReactComponent.js.map
    ./frontend/node_modules/@babel/types/lib/validators/react/isCompatTag.js.map
    ./frontend/node_modules/@babel/types/lib/validators/react/isReactComponent.js
    ./frontend/node_modules/@babel/types/lib/validators/react/isCompatTag.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/toArray.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/classPrivateFieldLooseBase.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/possibleConstructorReturn.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/classApplyDescriptorSet.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/applyDecs2311.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/callSuper.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/assertThisInitialized.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/classPrivateFieldSet2.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/objectWithoutProperties.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/asyncIterator.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/nonIterableRest.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/applyDecs2301.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/newArrowCheck.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/decorate.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/arrayWithHoles.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/classCheckPrivateStaticFieldDescriptor.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/instanceof.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/inheritsLoose.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/readOnlyError.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/regeneratorKeys.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/applyDecs2305.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/using.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/taggedTemplateLiteralLoose.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/regeneratorRuntime.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/interopRequireWildcard.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/arrayWithoutHoles.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/jsx.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/toSetter.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/asyncToGenerator.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/createClass.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/objectDestructuringEmpty.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/interopRequireDefault.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/classApplyDescriptorGet.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/classPrivateFieldInitSpec.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/extends.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/wrapRegExp.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/classCheckPrivateStaticAccess.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/classStaticPrivateFieldSpecGet.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/superPropGet.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/toConsumableArray.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/regeneratorValues.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/classPrivateFieldLooseKey.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/classPrivateMethodInitSpec.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/superPropSet.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/classStaticPrivateFieldSpecSet.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/iterableToArray.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/createForOfIteratorHelper.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/defineAccessor.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/classPrivateFieldSet.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/regeneratorDefine.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/objectSpread2.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/skipFirstGeneratorNext.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/asyncGeneratorDelegate.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/set.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/maybeArrayLike.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/classPrivateFieldGet.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/defineProperty.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/regeneratorAsync.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/objectSpread.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/initializerWarningHelper.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/applyDecs2203R.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/classApplyDescriptorDestructureSet.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/unsupportedIterableToArray.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/classCallCheck.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/classPrivateFieldGet2.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/temporalUndefined.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/wrapAsyncGenerator.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/classNameTDZError.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/importDeferProxy.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/package.json
    ./frontend/node_modules/@babel/runtime/helpers/esm/classStaticPrivateMethodSet.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/typeof.js
    ./frontend/node_modules/@babel/helper-validator-identifier/LICENSE
    ./frontend/node_modules/@babel/runtime/helpers/esm/writeOnlyError.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/isNativeReflectConstruct.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/classPrivateFieldDestructureSet.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/temporalRef.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/initializerDefineProperty.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/dispose.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/applyDecoratedDescriptor.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/toPrimitive.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/OverloadYield.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/awaitAsyncGenerator.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/isNativeFunction.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/classPrivateMethodGet.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/defaults.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/construct.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/classPrivateSetter.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/toPropertyKey.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/defineEnumerableProperties.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/wrapNativeSuper.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/applyDecs2203.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/objectWithoutPropertiesLoose.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/createSuper.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/assertClassBrand.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/nullishReceiverError.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/createForOfIteratorHelperLoose.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/regeneratorAsyncIterator.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/inherits.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/classPrivateGetter.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/classPrivateMethodSet.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/arrayLikeToArray.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/slicedToArray.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/applyDecs.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/setPrototypeOf.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/usingCtx.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/nonIterableSpread.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/setFunctionName.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/regenerator.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/classExtractFieldDescriptor.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/identity.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/tdz.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/superPropBase.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/checkInRHS.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/classStaticPrivateFieldDestructureSet.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/taggedTemplateLiteral.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/get.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/regeneratorAsyncGen.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/iterableToArrayLimit.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/classStaticPrivateMethodGet.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/checkPrivateRedeclaration.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/AwaitValue.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/tsRewriteRelativeImportExtensions.js
    ./frontend/node_modules/@babel/runtime/helpers/esm/getPrototypeOf.js
    ./frontend/node_modules/@babel/core/lib/transform-ast.js
    ./frontend/node_modules/@babel/helper-validator-identifier/README.md
    ./frontend/node_modules/@babel/helper-validator-identifier/package.json
    ./frontend/node_modules/@babel/types/lib/validators/generated/index.js.map
    ./frontend/node_modules/@babel/types/lib/validators/generated/index.js
    ./frontend/node_modules/@babel/parser/bin/babel-parser.js
    ./frontend/node_modules/@babel/helper-validator-identifier/lib/keyword.js
    ./frontend/node_modules/@babel/helper-validator-identifier/lib/index.js.map
    ./frontend/node_modules/@babel/helper-validator-identifier/lib/identifier.js
    ./frontend/node_modules/@babel/helper-validator-identifier/lib/identifier.js.map
    ./frontend/node_modules/@babel/helper-validator-identifier/lib/index.js
    ./frontend/node_modules/@babel/helper-validator-identifier/lib/keyword.js.map
    ./frontend/node_modules/@babel/core/lib/gensync-utils/fs.js
    ./frontend/node_modules/@babel/types/lib/ast-types/generated/index.js.map
    ./frontend/node_modules/@jridgewell/remapping/src/build-source-map-tree.ts
    ./frontend/node_modules/@babel/core/lib/gensync-utils/functional.js
    ./frontend/node_modules/@babel/core/lib/gensync-utils/async.js
    ./frontend/node_modules/@babel/core/lib/gensync-utils/fs.js.map
    ./frontend/node_modules/@babel/core/lib/gensync-utils/functional.js.map
    ./frontend/node_modules/@babel/core/lib/gensync-utils/async.js.map
    ./frontend/node_modules/@babel/types/lib/ast-types/generated/index.js
    ./frontend/node_modules/@babel/generator/README.md
    ./frontend/node_modules/@babel/generator/LICENSE
    ./frontend/node_modules/@babel/types/lib/modifications/flow/removeTypeDuplicates.js.map
    ./frontend/node_modules/@babel/generator/package.json
    ./frontend/node_modules/@babel/types/lib/modifications/flow/removeTypeDuplicates.js
    ./frontend/node_modules/@jridgewell/remapping/src/types.ts
    ./frontend/node_modules/@babel/helper-module-transforms/README.md
    ./frontend/node_modules/@jridgewell/remapping/src/source-map-tree.ts
    ./frontend/node_modules/@babel/helper-module-transforms/LICENSE
    ./frontend/node_modules/@jridgewell/remapping/src/source-map.ts
    ./frontend/node_modules/@babel/helper-module-transforms/package.json
    ./frontend/node_modules/@jridgewell/remapping/src/remapping.ts
    ./frontend/node_modules/@babel/types/lib/modifications/removePropertiesDeep.js.map
    ./frontend/node_modules/@babel/types/lib/modifications/removePropertiesDeep.js
    ./frontend/node_modules/@babel/types/lib/modifications/removeProperties.js.map
    ./frontend/node_modules/@babel/types/lib/modifications/inherits.js
    ./frontend/node_modules/@babel/types/lib/modifications/appendToMemberExpression.js
    ./frontend/node_modules/@babel/types/lib/modifications/removeProperties.js
    ./frontend/node_modules/@babel/types/lib/modifications/prependToMemberExpression.js.map
    ./frontend/node_modules/@babel/types/lib/modifications/appendToMemberExpression.js.map
    ./frontend/node_modules/@jridgewell/remapping/package.json
    ./frontend/node_modules/@jridgewell/remapping/README.md
    ./frontend/node_modules/@babel/generator/lib/token-map.js
    ./frontend/node_modules/@babel/generator/lib/buffer.js
    ./frontend/node_modules/@babel/generator/lib/buffer.js.map
    ./frontend/node_modules/@babel/helper-module-transforms/lib/rewrite-this.js.map
    ./frontend/node_modules/@babel/helper-module-transforms/lib/rewrite-live-references.js
    ./frontend/node_modules/@babel/helper-module-transforms/lib/dynamic-import.js
    ./frontend/node_modules/@babel/helper-module-transforms/lib/normalize-and-load-metadata.js
    ./frontend/node_modules/@babel/helper-module-transforms/lib/rewrite-live-references.js.map
    ./frontend/node_modules/@babel/helper-module-transforms/lib/rewrite-this.js
    ./frontend/node_modules/@babel/helper-module-transforms/lib/index.js.map
    ./frontend/node_modules/@babel/helper-module-transforms/lib/lazy-modules.js.map
    ./frontend/node_modules/@babel/helper-module-transforms/lib/normalize-and-load-metadata.js.map
    ./frontend/node_modules/@babel/helper-module-transforms/lib/get-module-name.js
    ./frontend/node_modules/@babel/helper-module-transforms/lib/index.js
    ./frontend/node_modules/@babel/helper-module-transforms/lib/lazy-modules.js
    ./frontend/node_modules/@babel/helper-module-transforms/lib/dynamic-import.js.map
    ./frontend/node_modules/@babel/helper-module-transforms/lib/get-module-name.js.map
    ./frontend/node_modules/@jridgewell/remapping/dist/remapping.umd.js.map
    ./frontend/node_modules/@jridgewell/remapping/dist/remapping.mjs
    ./frontend/node_modules/@jridgewell/remapping/dist/remapping.umd.js
    ./frontend/node_modules/@jridgewell/remapping/dist/remapping.mjs.map
    ./frontend/node_modules/@jridgewell/remapping/LICENSE
    ./frontend/node_modules/@babel/types/lib/index.js
    ./frontend/node_modules/@babel/types/lib/modifications/prependToMemberExpression.js
    ./frontend/node_modules/@babel/types/lib/modifications/inherits.js.map
    ./frontend/node_modules/@babel/core/lib/vendor/import-meta-resolve.js
    ./frontend/node_modules/@babel/core/lib/vendor/import-meta-resolve.js.map
    ./frontend/node_modules/@babel/types/lib/traverse/traverseFast.js.map
    ./frontend/node_modules/@babel/types/lib/traverse/traverse.js.map
    ./frontend/node_modules/@babel/types/lib/traverse/traverse.js
    ./frontend/node_modules/@babel/types/lib/traverse/traverseFast.js
    ./frontend/node_modules/@babel/types/lib/index.js.map
    ./frontend/node_modules/@babel/core/lib/parse.js
    ./frontend/node_modules/@babel/core/lib/transform.js
    ./frontend/node_modules/@babel/core/lib/transform-file.js
    ./frontend/node_modules/@babel/core/lib/transform.js.map
    ./frontend/node_modules/@babel/generator/lib/node/index.js.map
    ./frontend/node_modules/@babel/generator/lib/node/index.js
    ./frontend/node_modules/@babel/generator/lib/node/parentheses.js
    ./frontend/node_modules/@babel/generator/lib/node/parentheses.js.map
    ./frontend/node_modules/@jridgewell/remapping/types/source-map-tree.d.cts
    ./frontend/node_modules/@jridgewell/remapping/types/source-map.d.cts.map
    ./frontend/node_modules/@jridgewell/remapping/types/source-map-tree.d.mts
    ./frontend/node_modules/@jridgewell/remapping/types/types.d.mts.map
    ./frontend/node_modules/@jridgewell/remapping/types/build-source-map-tree.d.mts
    ./frontend/node_modules/@jridgewell/remapping/types/source-map-tree.d.mts.map
    ./frontend/node_modules/@jridgewell/remapping/types/remapping.d.mts.map
    ./frontend/node_modules/@jridgewell/remapping/types/build-source-map-tree.d.cts
    ./frontend/node_modules/@jridgewell/remapping/types/remapping.d.mts
    ./frontend/node_modules/@jridgewell/remapping/types/build-source-map-tree.d.cts.map
    ./frontend/node_modules/@jridgewell/remapping/types/types.d.mts
    ./frontend/node_modules/@jridgewell/remapping/types/types.d.cts
    ./frontend/node_modules/@jridgewell/remapping/types/remapping.d.cts
    ./frontend/node_modules/@jridgewell/remapping/types/build-source-map-tree.d.mts.map
    ./frontend/node_modules/@jridgewell/remapping/types/source-map.d.cts
    ./frontend/node_modules/@jridgewell/remapping/types/source-map.d.mts
    ./frontend/node_modules/@jridgewell/remapping/types/types.d.cts.map
    ./frontend/node_modules/@jridgewell/remapping/types/source-map-tree.d.cts.map
    ./frontend/node_modules/@jridgewell/remapping/types/remapping.d.cts.map
    ./frontend/node_modules/@jridgewell/remapping/types/source-map.d.mts.map
    ./frontend/node_modules/@babel/types/lib/utils/deprecationWarning.js.map
    ./frontend/node_modules/@babel/types/lib/modifications/typescript/removeTypeDuplicates.js.map
    ./frontend/node_modules/@babel/types/lib/modifications/typescript/removeTypeDuplicates.js
    ./frontend/node_modules/@jridgewell/resolve-uri/package.json
    ./frontend/node_modules/@jridgewell/resolve-uri/README.md
    ./frontend/node_modules/@jridgewell/sourcemap-codec/src/scopes.ts
    ./frontend/node_modules/@jridgewell/sourcemap-codec/src/vlq.ts
    ./frontend/node_modules/@jridgewell/sourcemap-codec/src/strings.ts
    ./frontend/node_modules/@jridgewell/sourcemap-codec/src/sourcemap-codec.ts
    ./frontend/node_modules/@jridgewell/sourcemap-codec/package.json
    ./frontend/node_modules/@jridgewell/sourcemap-codec/README.md
    ./frontend/node_modules/@jridgewell/trace-mapping/dist/trace-mapping.mjs
    ./frontend/node_modules/@jridgewell/trace-mapping/src/resolve.ts
    ./frontend/node_modules/@jridgewell/trace-mapping/dist/trace-mapping.umd.js
    ./frontend/node_modules/@jridgewell/trace-mapping/dist/trace-mapping.umd.js.map
    ./frontend/node_modules/@jridgewell/trace-mapping/dist/trace-mapping.mjs.map
    ./frontend/node_modules/@jridgewell/trace-mapping/src/binary-search.ts
    ./frontend/node_modules/@jridgewell/trace-mapping/src/trace-mapping.ts
    ./frontend/node_modules/@jridgewell/trace-mapping/src/sort.ts
    ./frontend/node_modules/@jridgewell/trace-mapping/src/by-source.ts
    ./frontend/node_modules/@jridgewell/trace-mapping/src/types.ts
    ./frontend/node_modules/@jridgewell/trace-mapping/src/flatten-map.ts
    ./frontend/node_modules/@jridgewell/trace-mapping/src/strip-filename.ts
    ./frontend/node_modules/@jridgewell/trace-mapping/src/sourcemap-segment.ts
    ./frontend/node_modules/@babel/types/lib/clone/cloneNode.js
    ./frontend/node_modules/@babel/types/lib/clone/clone.js.map
    ./frontend/node_modules/@babel/types/lib/clone/cloneDeep.js
    ./frontend/node_modules/@babel/types/lib/clone/cloneWithoutLoc.js.map
    ./frontend/node_modules/@babel/types/lib/clone/cloneNode.js.map
    ./frontend/node_modules/@babel/types/lib/clone/clone.js
    ./frontend/node_modules/@babel/types/lib/clone/cloneDeep.js.map
    ./frontend/node_modules/@babel/types/lib/clone/cloneWithoutLoc.js
    ./frontend/node_modules/@babel/types/lib/clone/cloneDeepWithoutLoc.js.map
    ./frontend/node_modules/@babel/types/lib/clone/cloneDeepWithoutLoc.js
    ./frontend/node_modules/@jridgewell/trace-mapping/LICENSE
    ./frontend/node_modules/@jridgewell/trace-mapping/package.json
    ./frontend/node_modules/@jridgewell/trace-mapping/README.md
    ./frontend/node_modules/@babel/generator/lib/generators/classes.js.map
    ./frontend/node_modules/@babel/generator/lib/generators/methods.js.map
    ./frontend/node_modules/@babel/generator/lib/generators/base.js.map
    ./frontend/node_modules/@babel/generator/lib/generators/index.js.map
    ./frontend/node_modules/@babel/generator/lib/generators/base.js
    ./frontend/node_modules/@babel/generator/lib/generators/statements.js.map
    ./frontend/node_modules/@babel/generator/lib/generators/modules.js
    ./frontend/node_modules/@babel/generator/lib/generators/statements.js
    ./frontend/node_modules/@babel/generator/lib/generators/classes.js
    ./frontend/node_modules/@babel/generator/lib/generators/template-literals.js.map
    ./frontend/node_modules/@babel/generator/lib/generators/expressions.js.map
    ./frontend/node_modules/@babel/generator/lib/generators/template-literals.js
    ./frontend/node_modules/@babel/generator/lib/generators/index.js
    ./frontend/node_modules/@babel/generator/lib/generators/methods.js
    ./frontend/node_modules/@babel/generator/lib/generators/flow.js.map
    ./frontend/node_modules/@babel/generator/lib/generators/typescript.js.map
    ./frontend/node_modules/@babel/generator/lib/generators/flow.js
    ./frontend/node_modules/@babel/generator/lib/generators/types.js.map
    ./frontend/node_modules/@babel/generator/lib/generators/types.js
    ./frontend/node_modules/@babel/generator/lib/generators/deprecated.js.map
    ./frontend/node_modules/@babel/generator/lib/generators/typescript.js
    ./frontend/node_modules/@babel/generator/lib/generators/jsx.js
    ./frontend/node_modules/@babel/generator/lib/generators/modules.js.map
    ./frontend/node_modules/@babel/generator/lib/generators/expressions.js
    ./frontend/node_modules/@babel/generator/lib/generators/jsx.js.map
    ./frontend/node_modules/@babel/generator/lib/generators/deprecated.js
    ./frontend/node_modules/@babel/generator/lib/index.js.map
    ./frontend/node_modules/@babel/generator/lib/printer.js
    ./frontend/node_modules/@babel/generator/lib/source-map.js
    ./frontend/node_modules/@babel/generator/lib/source-map.js.map
    ./frontend/node_modules/@babel/generator/lib/nodes.js
    ./frontend/node_modules/@babel/generator/lib/index.js
    ./frontend/node_modules/@babel/generator/lib/token-map.js.map
    ./frontend/node_modules/@babel/generator/lib/nodes.js.map
    ./frontend/node_modules/@babel/generator/lib/printer.js.map
    ./frontend/node_modules/@jridgewell/resolve-uri/LICENSE
    ./frontend/node_modules/@babel/types/lib/utils/shallowEqual.js
    ./frontend/node_modules/@babel/types/lib/utils/shallowEqual.js.map
    ./frontend/node_modules/@babel/types/lib/utils/inherit.js.map
    ./frontend/node_modules/@babel/types/lib/utils/deprecationWarning.js
    ./frontend/node_modules/@babel/types/lib/utils/inherit.js
    ./frontend/node_modules/@babel/types/lib/utils/react/cleanJSXElementLiteralChild.js.map
    ./frontend/node_modules/@babel/types/lib/utils/react/cleanJSXElementLiteralChild.js
    ./frontend/node_modules/@babel/core/lib/transform-ast.js.map
    ./frontend/node_modules/@babel/core/lib/parse.js.map
    ./frontend/node_modules/@babel/core/lib/parser/index.js.map
    ./frontend/node_modules/@babel/core/lib/parser/index.js
    ./frontend/node_modules/@jridgewell/resolve-uri/dist/resolve-uri.mjs.map
    ./frontend/node_modules/@jridgewell/resolve-uri/dist/resolve-uri.mjs
    ./frontend/node_modules/@babel/core/lib/errors/rewrite-stack-trace.js.map
    ./frontend/node_modules/@babel/core/lib/errors/config-error.js.map
    ./frontend/node_modules/@babel/core/lib/errors/rewrite-stack-trace.js
    ./frontend/node_modules/@babel/core/lib/errors/config-error.js
    ./frontend/node_modules/@babel/core/lib/transform-file-browser.js
    ./frontend/node_modules/@babel/core/lib/index.js.map
    ./frontend/node_modules/@babel/core/lib/transform-file.js.map
    ./frontend/node_modules/@babel/core/lib/transform-file-browser.js.map
    ./frontend/node_modules/@babel/core/lib/config/config-descriptors.js.map
    ./frontend/node_modules/@babel/core/lib/config/config-chain.js
    ./frontend/node_modules/@babel/core/lib/config/resolve-targets-browser.js
    ./frontend/node_modules/@babel/core/lib/config/item.js.map
    ./frontend/node_modules/@jridgewell/sourcemap-codec/dist/sourcemap-codec.mjs.map
    ./frontend/node_modules/@jridgewell/sourcemap-codec/dist/sourcemap-codec.mjs
    ./frontend/node_modules/@jridgewell/sourcemap-codec/dist/sourcemap-codec.umd.js.map
    ./frontend/node_modules/@jridgewell/sourcemap-codec/dist/sourcemap-codec.umd.js
    ./frontend/node_modules/@jridgewell/sourcemap-codec/LICENSE
    ./frontend/node_modules/@jridgewell/resolve-uri/dist/resolve-uri.umd.js
    ./frontend/node_modules/@jridgewell/resolve-uri/dist/resolve-uri.umd.js.map
    ./frontend/node_modules/@babel/core/lib/config/partial.js
    ./frontend/node_modules/@babel/core/lib/config/plugin.js.map
    ./frontend/node_modules/@babel/core/lib/config/pattern-to-regex.js
    ./frontend/node_modules/@babel/core/lib/config/resolve-targets.js
    ./frontend/node_modules/@babel/core/lib/config/resolve-targets.js.map
    ./frontend/node_modules/@babel/core/lib/config/pattern-to-regex.js.map
    ./frontend/node_modules/@babel/core/lib/config/config-chain.js.map
    ./frontend/node_modules/@babel/core/lib/config/caching.js.map
    ./frontend/node_modules/@babel/core/lib/config/index.js
    ./frontend/node_modules/@babel/core/lib/config/resolve-targets-browser.js.map
    ./frontend/node_modules/@babel/core/lib/config/util.js.map
    ./frontend/node_modules/@babel/core/lib/config/printer.js.map
    ./frontend/node_modules/@babel/core/lib/config/util.js
    ./frontend/node_modules/@babel/core/lib/config/partial.js.map
    ./frontend/node_modules/@babel/core/lib/config/index.js.map
    ./frontend/node_modules/@babel/core/lib/config/printer.js
    ./frontend/node_modules/@babel/types/lib/asserts/assertNode.js
    ./frontend/node_modules/@babel/types/lib/asserts/assertNode.js.map
    ./frontend/node_modules/@babel/core/lib/config/validation/removed.js
    ./frontend/node_modules/@babel/core/lib/config/validation/options.js.map
    ./frontend/node_modules/@babel/core/lib/config/validation/options.js
    ./frontend/node_modules/@babel/core/lib/config/validation/plugins.js
    ./frontend/node_modules/@babel/core/lib/config/validation/removed.js.map
    ./frontend/node_modules/@babel/core/lib/config/validation/option-assertions.js
    ./frontend/node_modules/@babel/core/lib/config/validation/option-assertions.js.map
    ./frontend/node_modules/@babel/core/lib/config/validation/plugins.js.map
    ./frontend/node_modules/@babel/core/lib/config/plugin.js
    ./frontend/node_modules/@babel/types/lib/asserts/generated/index.js.map
    ./frontend/node_modules/@babel/types/lib/asserts/generated/index.js
    ./frontend/node_modules/@babel/core/lib/config/full.js
    ./frontend/node_modules/@babel/core/lib/config/caching.js
    ./frontend/node_modules/@babel/core/lib/config/cache-contexts.js
    ./frontend/node_modules/@babel/core/lib/config/full.js.map
    ./frontend/node_modules/@babel/core/lib/index.js
    ./frontend/node_modules/@jridgewell/sourcemap-codec/types/vlq.d.mts
    ./frontend/node_modules/@jridgewell/sourcemap-codec/types/strings.d.cts
    ./frontend/node_modules/@jridgewell/sourcemap-codec/types/vlq.d.cts
    ./frontend/node_modules/@jridgewell/sourcemap-codec/types/scopes.d.mts.map
    ./frontend/node_modules/@jridgewell/sourcemap-codec/types/sourcemap-codec.d.mts.map
    ./frontend/node_modules/@jridgewell/sourcemap-codec/types/strings.d.cts.map
    ./frontend/node_modules/@jridgewell/sourcemap-codec/types/vlq.d.cts.map
    ./frontend/node_modules/@jridgewell/sourcemap-codec/types/sourcemap-codec.d.cts.map
    ./frontend/node_modules/@jridgewell/sourcemap-codec/types/strings.d.mts.map
    ./frontend/node_modules/@jridgewell/sourcemap-codec/types/scopes.d.mts
    ./frontend/node_modules/@babel/core/lib/parser/util/missing-plugin-helper.js
    ./frontend/node_modules/@jridgewell/sourcemap-codec/types/scopes.d.cts.map
    ./frontend/node_modules/@babel/core/lib/parser/util/missing-plugin-helper.js.map
    ./frontend/node_modules/@jridgewell/sourcemap-codec/types/scopes.d.cts
    ./frontend/node_modules/@jridgewell/sourcemap-codec/types/strings.d.mts
    ./frontend/node_modules/@jridgewell/sourcemap-codec/types/sourcemap-codec.d.cts
    ./frontend/node_modules/@jridgewell/sourcemap-codec/types/sourcemap-codec.d.mts
    ./frontend/node_modules/@jridgewell/sourcemap-codec/types/vlq.d.mts.map
    ./frontend/node_modules/@babel/core/lib/config/item.js
    ./frontend/node_modules/@babel/core/lib/config/config-descriptors.js
    ./frontend/node_modules/@babel/core/lib/config/cache-contexts.js.map
    ./frontend/node_modules/@jridgewell/gen-mapping/LICENSE
    ./frontend/node_modules/@jridgewell/gen-mapping/README.md
    ./frontend/node_modules/@jridgewell/gen-mapping/package.json
    ./frontend/node_modules/@babel/core/lib/tools/build-external-helpers.js
    ./frontend/node_modules/@babel/core/lib/tools/build-external-helpers.js.map
    ./frontend/node_modules/@jridgewell/resolve-uri/dist/types/resolve-uri.d.ts
    ./frontend/node_modules/@babel/core/lib/config/helpers/environment.js.map
    ./frontend/node_modules/@babel/core/lib/config/helpers/environment.js
    ./frontend/node_modules/@babel/core/lib/config/helpers/deep-array.js
    ./frontend/node_modules/@babel/core/lib/config/helpers/deep-array.js.map
    ./frontend/node_modules/@babel/core/lib/config/helpers/config-api.js.map
    ./frontend/node_modules/@babel/core/lib/config/helpers/config-api.js
    ./frontend/node_modules/@babel/core/lib/transformation/normalize-file.js.map
    ./frontend/node_modules/@babel/core/lib/config/files/index-browser.js.map
    ./frontend/node_modules/@babel/core/lib/transformation/normalize-opts.js.map
    ./frontend/node_modules/@babel/core/lib/config/files/utils.js.map
    ./frontend/node_modules/@babel/core/lib/transformation/plugin-pass.js
    ./frontend/node_modules/@babel/core/lib/config/files/utils.js
    ./frontend/node_modules/@babel/core/lib/transformation/block-hoist-plugin.js
    ./frontend/node_modules/@babel/core/lib/config/files/index.js.map
    ./frontend/node_modules/@babel/core/lib/transformation/index.js.map
    ./frontend/node_modules/@babel/core/lib/config/files/import.cjs
    ./frontend/node_modules/@babel/core/lib/transformation/index.js
    ./frontend/node_modules/@babel/core/lib/config/files/module-types.js
    ./frontend/node_modules/@babel/core/lib/transformation/normalize-file.js
    ./frontend/node_modules/@babel/core/lib/config/files/index-browser.js
    ./frontend/node_modules/@babel/core/lib/transformation/normalize-opts.js
    ./frontend/node_modules/@babel/core/lib/config/files/index.js
    ./frontend/node_modules/@babel/core/lib/config/files/package.js.map
    ./frontend/node_modules/@babel/core/lib/config/files/package.js
    ./frontend/node_modules/@babel/core/lib/config/files/configuration.js
    ./frontend/node_modules/@babel/core/lib/config/files/plugins.js
    ./frontend/node_modules/@babel/core/lib/config/files/configuration.js.map
    ./frontend/node_modules/@babel/core/lib/config/files/import.cjs.map
    ./frontend/node_modules/@babel/core/lib/config/files/types.js.map
    ./frontend/node_modules/@babel/core/lib/config/files/types.js
    ./frontend/node_modules/@babel/core/lib/config/files/module-types.js.map
    ./frontend/node_modules/@babel/core/lib/config/files/plugins.js.map
    ./frontend/node_modules/@jridgewell/trace-mapping/types/resolve.d.cts.map
    ./frontend/node_modules/@jridgewell/trace-mapping/types/flatten-map.d.cts
    ./frontend/node_modules/@babel/core/lib/transformation/block-hoist-plugin.js.map
    ./frontend/node_modules/@babel/core/lib/transformation/plugin-pass.js.map
    ./frontend/node_modules/@jridgewell/gen-mapping/src/set-array.ts
    ./frontend/node_modules/@jridgewell/gen-mapping/src/types.ts
    ./frontend/node_modules/@jridgewell/gen-mapping/src/gen-mapping.ts
    ./frontend/node_modules/@jridgewell/gen-mapping/src/sourcemap-segment.ts
    ./frontend/node_modules/@jridgewell/gen-mapping/types/types.d.mts
    ./frontend/node_modules/@jridgewell/gen-mapping/types/types.d.cts
    ./frontend/node_modules/@jridgewell/gen-mapping/types/set-array.d.mts.map
    ./frontend/node_modules/@jridgewell/gen-mapping/types/gen-mapping.d.cts.map
    ./frontend/node_modules/@jridgewell/gen-mapping/types/types.d.cts.map
    ./frontend/node_modules/@jridgewell/gen-mapping/types/sourcemap-segment.d.mts.map
    ./frontend/node_modules/@jridgewell/gen-mapping/types/gen-mapping.d.mts.map
    ./frontend/node_modules/@jridgewell/gen-mapping/types/types.d.mts.map
    ./frontend/node_modules/@jridgewell/gen-mapping/types/set-array.d.cts.map
    ./frontend/node_modules/@jridgewell/gen-mapping/types/gen-mapping.d.mts
    ./frontend/node_modules/@jridgewell/gen-mapping/types/set-array.d.cts
    ./frontend/node_modules/@jridgewell/gen-mapping/types/sourcemap-segment.d.cts
    ./frontend/node_modules/@jridgewell/trace-mapping/types/trace-mapping.d.mts
    ./frontend/node_modules/@jridgewell/trace-mapping/types/trace-mapping.d.cts
    ./frontend/node_modules/@jridgewell/trace-mapping/types/sourcemap-segment.d.mts.map
    ./frontend/node_modules/@jridgewell/trace-mapping/types/flatten-map.d.mts
    ./frontend/node_modules/@jridgewell/gen-mapping/types/set-array.d.mts
    ./frontend/node_modules/@jridgewell/trace-mapping/types/sort.d.mts.map
    ./frontend/node_modules/@jridgewell/trace-mapping/types/by-source.d.cts
    ./frontend/node_modules/@jridgewell/trace-mapping/types/binary-search.d.mts.map
    ./frontend/node_modules/@jridgewell/trace-mapping/types/by-source.d.cts.map
    ./frontend/node_modules/@jridgewell/trace-mapping/types/types.d.cts.map
    ./frontend/node_modules/@jridgewell/gen-mapping/types/gen-mapping.d.cts
    ./frontend/node_modules/@jridgewell/gen-mapping/types/sourcemap-segment.d.cts.map
    ./frontend/node_modules/@jridgewell/gen-mapping/types/sourcemap-segment.d.mts
    ./frontend/node_modules/@jridgewell/trace-mapping/types/trace-mapping.d.mts.map
    ./frontend/node_modules/@jridgewell/trace-mapping/types/flatten-map.d.cts.map
    ./frontend/node_modules/@jridgewell/trace-mapping/types/by-source.d.mts
    ./frontend/node_modules/@jridgewell/trace-mapping/types/resolve.d.mts
    ./frontend/node_modules/@jridgewell/trace-mapping/types/strip-filename.d.cts.map
    ./frontend/node_modules/@jridgewell/trace-mapping/types/flatten-map.d.mts.map
    ./frontend/node_modules/@jridgewell/gen-mapping/dist/gen-mapping.umd.js
    ./frontend/node_modules/@jridgewell/gen-mapping/dist/gen-mapping.mjs
    ./frontend/node_modules/@jridgewell/gen-mapping/dist/gen-mapping.mjs.map
    ./frontend/node_modules/@jridgewell/gen-mapping/dist/gen-mapping.umd.js.map
    ./frontend/node_modules/@jridgewell/trace-mapping/types/sort.d.cts
    ./frontend/node_modules/@jridgewell/trace-mapping/types/sourcemap-segment.d.cts.map
    ./frontend/node_modules/@jridgewell/trace-mapping/types/sort.d.mts
    ./frontend/node_modules/@jridgewell/trace-mapping/types/resolve.d.mts.map
    ./frontend/node_modules/@jridgewell/trace-mapping/types/binary-search.d.cts.map
    ./frontend/node_modules/@jridgewell/trace-mapping/types/sourcemap-segment.d.mts
    ./frontend/node_modules/@jridgewell/trace-mapping/types/binary-search.d.cts
    ./frontend/node_modules/@jridgewell/trace-mapping/types/binary-search.d.mts
    ./frontend/node_modules/@jridgewell/trace-mapping/types/sourcemap-segment.d.cts
    ./frontend/node_modules/@jridgewell/trace-mapping/types/types.d.mts.map
    ./frontend/node_modules/@jridgewell/trace-mapping/types/strip-filename.d.cts
    ./frontend/node_modules/@jridgewell/trace-mapping/types/by-source.d.mts.map
    ./frontend/node_modules/@jridgewell/trace-mapping/types/sort.d.cts.map
    ./frontend/node_modules/@jridgewell/trace-mapping/types/strip-filename.d.mts
    ./frontend/node_modules/@jridgewell/trace-mapping/types/resolve.d.cts
    ./frontend/node_modules/@jridgewell/trace-mapping/types/strip-filename.d.mts.map
    ./frontend/node_modules/@jridgewell/trace-mapping/types/types.d.mts
    ./frontend/node_modules/@jridgewell/trace-mapping/types/trace-mapping.d.cts.map
    ./frontend/node_modules/@jridgewell/trace-mapping/types/types.d.cts
    ./frontend/node_modules/@babel/core/lib/transformation/util/clone-deep.js.map
    ./frontend/node_modules/@babel/core/lib/transformation/util/clone-deep.js
    ./frontend/node_modules/@jridgewell/gen-mapping/dist/types/sourcemap-segment.d.ts
    ./frontend/node_modules/@jridgewell/gen-mapping/dist/types/set-array.d.ts
    ./frontend/node_modules/@jridgewell/gen-mapping/dist/types/gen-mapping.d.ts
    ./frontend/node_modules/@jridgewell/gen-mapping/dist/types/types.d.ts
    ./frontend/node_modules/@babel/core/lib/transformation/file/babel-7-helpers.cjs
    ./frontend/node_modules/@babel/core/lib/transformation/file/generate.js.map
    ./frontend/node_modules/@babel/core/lib/transformation/file/file.js
    ./frontend/node_modules/@babel/core/lib/transformation/file/file.js.map
    ./frontend/node_modules/@babel/core/lib/transformation/file/merge-map.js.map
    ./frontend/node_modules/@babel/core/lib/transformation/file/generate.js
    ./frontend/node_modules/@babel/core/lib/transformation/file/babel-7-helpers.cjs.map
    ./frontend/node_modules/@babel/core/lib/transformation/file/merge-map.js

## Agent Message

- Time: `2026-03-31T21:21:54-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `13`
- Summary: I found an existing `backend/` directory, so the next step is to read the current scaffold and the prior prompt summaries to see whether this task was partially started or only stubbed.

### Full Text

    I found an existing `backend/` directory, so the next step is to read the current scaffold and the prior prompt summaries to see whether this task was partially started or only stubbed.

## Command Started

- Time: `2026-03-31T21:21:54-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `14`
- Summary: in progress: /bin/zsh -lc "sed -n '1,220p' backend/requirements.txt"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,220p' backend/requirements.txt"
    Status: in progress

## Command Finished

- Time: `2026-03-31T21:21:54-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `15`
- Summary: completed, exit 0: /bin/zsh -lc "sed -n '1,220p' backend/requirements.txt"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,220p' backend/requirements.txt"
    Status: completed
    Exit code: 0
    Output:
    fastapi==0.116.1
    uvicorn[standard]==0.35.0

## Command Started

- Time: `2026-03-31T21:21:54-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `16`
- Summary: in progress: /bin/zsh -lc "sed -n '1,220p' README.md"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,220p' README.md"
    Status: in progress

## Command Started

- Time: `2026-03-31T21:21:54-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `17`
- Summary: in progress: /bin/zsh -lc "sed -n '1,240p' backend/README.md"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,240p' backend/README.md"
    Status: in progress

## Command Finished

- Time: `2026-03-31T21:21:54-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `18`
- Summary: completed, exit 0: /bin/zsh -lc "sed -n '1,240p' backend/README.md"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,240p' backend/README.md"
    Status: completed
    Exit code: 0
    Output:
    # Backend

    This directory is the home for the FastAPI application, backend-owned workflow logic, and future durable job processing.

    Current contents:

    - `app/`: live application code
    - `migrations/`: reserved for database migrations
    - `requirements.txt`: Python dependencies
    - `Dockerfile`: backend container image

    Planned expansion inside `app/` follows the architecture notes in [docs/architecture-overview.md](/Users/kevin/code/storyteller/docs/architecture-overview.md), including explicit homes for API routes, settings, repositories, services, AI adapters, storage, and worker execution.

## Command Finished

- Time: `2026-03-31T21:21:54-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `19`
- Summary: completed, exit 0: /bin/zsh -lc "sed -n '1,220p' README.md"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,220p' README.md"
    Status: completed
    Exit code: 0
    Output:
    # Storyteller

    Storyteller is a local-first, full-stack app for creating bedtime stories from first idea to finished text and finished narration audio. The product is session-based: the first meaningful screen is a past-sessions view where a user can resume work in progress, reopen a completed story, or start a new session.

    This repository currently contains the first scaffold for that system. The project charter in this README and the supporting docs define the product and architecture that later prompts will implement.

    ## Product Vision

    The app should feel like a guided bedtime story studio, not a generic prompt box. A user should be able to:

    - See past sessions first and continue where they left off.
    - Collaborate through both chat and direct UI controls.
    - Move through a structured planning workflow before long-form writing starts.
    - Watch story composition and audio generation progress in real time.
    - Return later to read, listen, download, or revise completed work.

    The tone of the product should stay calm, readable, and trustworthy. Wonder, mystery, and adventure are welcome, but bedtime suitability is a hard requirement: emotional stakes should resolve safely and the ending should feel restful.

    ## Required Story Workflow

    The application is being built around this ordered workflow:

    1. Genre selection
    2. Tone selection
    3. Story setup / free-form brief
    4. Story pitches
    5. Character sheet
    6. Save-the-Cat beat sheet
    7. Story setup preferences such as word count, runtime, and chapters
    8. Composition
    9. Audio configuration and audio generation
    10. Finalize / read / listen / download

    Each stage must be durable, resumable, and editable. Chat messages can propose actions in the workflow, and direct UI actions must also be reflected back into the session chat log as compact summaries.

    ## Fixed Technical Decisions

    These choices are not optional for this project:

    - Frontend: React + Vite + TypeScript
    - Backend: Python + FastAPI
    - Structured data: PostgreSQL
    - Blob storage: file-backed GCS emulator in local development
    - Local orchestration: Docker Compose
    - Secrets handling: local `secrets.yaml`, never committed to git
    - AI access: Gemini 3.1 family behind backend-owned adapters and services

    Two architectural rules follow from those constraints:

    - The browser must never hold provider secrets or call Gemini directly.
    - Long-running story composition and narration generation must be durable background jobs with resumable server-side state.

    More detail is in [docs/product-brief.md](/Users/kevin/code/storyteller/docs/product-brief.md) and [docs/architecture-overview.md](/Users/kevin/code/storyteller/docs/architecture-overview.md).

    ## Local Development Expectations

    The repo is intended to run locally with Docker Compose. At the current scaffold stage:

    - `frontend/` contains a Vite React app served on `http://localhost:8566`
    - `backend/` contains a FastAPI app served on `http://localhost:8565`
    - `infra/compose/` holds the canonical Compose file for local orchestration
    - `tools/webapp-qa/` contains the browser automation container used for local UI verification

    Start the current stack with:

    ```bash
    ./scripts/dev-compose.sh up --build
    ```

    The current scaffold does not yet include PostgreSQL or the file-backed GCS emulator, but both are required parts of the target system and will be added through later prompt work. `secrets.yaml` is already gitignored and reserved for local-only credentials.

    ## Repository Shape

    ```text
    .
    ├── backend/
    │   ├── app/
    │   │   ├── main.py
    │   │   └── worker/
    │   ├── migrations/
    │   ├── Dockerfile
    │   ├── README.md
    │   └── requirements.txt
    ├── docs/
    ├── frontend/
    ├── infra/
    │   ├── compose/
    │   │   └── docker-compose.yml
    │   └── persistence/
    ├── prompts/
    ├── scripts/
    ├── test-assets/
    └── tools/
        └── webapp-qa/
    ```

    - `frontend/`: browser client and TypeScript UI foundation
    - `backend/`: API code, worker home, and migration home
    - `infra/`: Compose definitions and infrastructure notes
    - `docs/`: product notes, architecture notes, and future ADRs
    - `scripts/`: developer entrypoints such as `dev-compose.sh`
    - `test-assets/`: reusable fixtures for UI, audio, and integration testing
    - `prompts/`: sequential build prompts and task summaries
    - `tools/`: local QA and developer tooling

    ## What Success Looks Like

    A new engineer should be able to open this repository and quickly understand:

    - the first screen is the past-sessions home for resume, edit, and create flows
    - the story workflow is staged and ordered
    - the final product writes stories and generates narration audio durably
    - the backend owns AI access, long-running jobs, and persistent state

## Command Started

- Time: `2026-03-31T21:21:54-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `20`
- Summary: in progress: /bin/zsh -lc "sed -n '1,220p' backend/app/main.py"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,220p' backend/app/main.py"
    Status: in progress

## Command Started

- Time: `2026-03-31T21:21:54-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `21`
- Summary: in progress: /bin/zsh -lc 'find backend -maxdepth 3 -type f | sort'

### Full Text

    Command: /bin/zsh -lc 'find backend -maxdepth 3 -type f | sort'
    Status: in progress

## Command Finished

- Time: `2026-03-31T21:21:54-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `22`
- Summary: completed, exit 0: /bin/zsh -lc "sed -n '1,220p' backend/app/main.py"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,220p' backend/app/main.py"
    Status: completed
    Exit code: 0
    Output:
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware


    app = FastAPI(title="Storyteller API")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


    @app.get("/api/hello")
    async def hello() -> dict[str, str]:
        return {"message": "Hello from FastAPI!"}

## Command Finished

- Time: `2026-03-31T21:21:54-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `23`
- Summary: completed, exit 0: /bin/zsh -lc 'find backend -maxdepth 3 -type f | sort'

### Full Text

    Command: /bin/zsh -lc 'find backend -maxdepth 3 -type f | sort'
    Status: completed
    Exit code: 0
    Output:
    backend/Dockerfile
    backend/README.md
    backend/app/__pycache__/main.cpython-313.pyc
    backend/app/main.py
    backend/app/worker/README.md
    backend/migrations/README.md
    backend/requirements.txt

## Command Started

- Time: `2026-03-31T21:21:54-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `24`
- Summary: in progress: /bin/zsh -lc "sed -n '1,260p' prompts/01-monorepo-skeleton.summary.md"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,260p' prompts/01-monorepo-skeleton.summary.md"
    Status: in progress

## Command Finished

- Time: `2026-03-31T21:21:54-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `25`
- Summary: completed, exit 0: /bin/zsh -lc "sed -n '1,260p' prompts/01-monorepo-skeleton.summary.md"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,260p' prompts/01-monorepo-skeleton.summary.md"
    Status: completed
    Exit code: 0
    Output:
    # 01 Monorepo Skeleton Summary

    ## What I changed and why

    I turned the existing prompt-00 scaffold into a cleaner monorepo layout so later prompts have obvious, conventional homes for application code, infrastructure, migrations, worker logic, developer scripts, and reusable test fixtures.

    The main changes were:

    - Moved the canonical Docker Compose file from the repository root to `infra/compose/docker-compose.yml`.
      - This puts local orchestration under `infra/`, which is where future Compose variants and infrastructure definitions should live.
      - I kept the developer experience approachable by adding `scripts/dev-compose.sh` instead of forcing contributors to remember a long `docker compose -f ...` command.

    - Added top-level structure that the prompt explicitly asked for:
      - `infra/`
      - `scripts/`
      - `test-assets/`

    - Added placeholder READMEs in the major folders so a new engineer can infer intent without reading the prompt pack first:
      - `backend/README.md`
      - `frontend/README.md`
      - `docs/README.md`
      - `docs/adr/README.md`
      - `infra/README.md`
      - `infra/compose/README.md`
      - `infra/persistence/README.md`
      - `scripts/README.md`
      - `test-assets/README.md`
      - `tools/README.md`

    - Added explicit backend placeholders for the prompt acceptance criteria:
      - `backend/migrations/README.md` as the future migration home
      - `backend/app/worker/README.md` as the future background-job home

    - Updated the root `README.md` to include:
      - the new local-development entrypoint via `./scripts/dev-compose.sh up --build`
      - a brief repository tree snapshot
      - short purpose notes for each major top-level directory

    - Updated `docs/architecture-overview.md` so the documented current repository state matches the new layout rather than the old root-level `docker-compose.yml`.

    I also created one checkpoint commit during the run:

    - `b310953` — `feat(prompt-01): monorepo skeleton`

    ## Architectural changes across the codebase

    This prompt was still mostly structural rather than behavioral, but there are a few meaningful architecture-level changes in the repository layout:

    ### Infrastructure now has a real home

    - `infra/compose/docker-compose.yml` is now the canonical local stack definition.
    - `infra/persistence/` is the reserved documentation home for persistent local data conventions such as PostgreSQL state and file-backed object storage state.

    This matters because later prompts will add PostgreSQL, the file-backed GCS emulator, and additional infrastructure details. Those no longer need to leak into the repository root.

    ### Backend now exposes future extension points clearly

    - `backend/migrations/` is the obvious location for schema history.
    - `backend/app/worker/` is the obvious location for durable background workers.

    This aligns the filesystem with the architecture note that composition and audio generation should run as server-side jobs rather than request-thread work.

    ### Developer entrypoints are cleaner

    - `scripts/dev-compose.sh` is a small wrapper around the canonical Compose file.

    That keeps the infrastructure organized under `infra/` while still giving contributors a short, stable command surface.

    ## Examples of how to use the new abstractions, helpers, and extension points

    ### Compose wrapper

    Start the stack:

    ```bash
    ./scripts/dev-compose.sh up --build
    ```

    Inspect service health:

    ```bash
    ./scripts/dev-compose.sh ps
    ```

    Run the existing browser smoke check against the stack:

    ```bash
    ./scripts/dev-compose.sh run --rm browser npm run check -- --spec ./examples/homepage.spec.json
    ```

    Stop the stack:

    ```bash
    ./scripts/dev-compose.sh down
    ```

    ### Backend extension points

    - Add future database migrations under `backend/migrations/`.
    - Add durable job runners for story composition and narration under `backend/app/worker/`.

    ### Infrastructure extension points

    - Add future local Compose variants or overrides under `infra/compose/`.
    - Document persistent data behavior for PostgreSQL or the file-backed GCS emulator under `infra/persistence/`.

    ## Key files touched

    - `README.md`
    - `docs/architecture-overview.md`
    - `infra/compose/docker-compose.yml`
    - `scripts/dev-compose.sh`
    - `backend/README.md`
    - `backend/migrations/README.md`
    - `backend/app/worker/README.md`
    - `frontend/README.md`
    - `docs/README.md`
    - `docs/adr/README.md`
    - `infra/README.md`
    - `infra/compose/README.md`
    - `infra/persistence/README.md`
    - `scripts/README.md`
    - `test-assets/README.md`
    - `tools/README.md`

    ## Exact verification work performed

    I verified both the filesystem layout and the runnable Docker workflow.

    ### Structure and acceptance checks

    I ran a small Python acceptance script after the edits. Results:

    - `top_level_frontend=True`
    - `top_level_backend=True`
    - `top_level_infra=True`
    - `top_level_docs=True`
    - `top_level_scripts=True`
    - `top_level_test_assets=True`
    - `compose_in_infra=True`
    - `migrations_home=True`
    - `worker_home=True`
    - `root_readme_tree_snapshot=True`
    - `folder_readmes_present=True`

    ### Patch hygiene

    I ran:

    ```bash
    git diff --check -- README.md docs/architecture-overview.md backend docs frontend infra scripts test-assets tools
    ```

    Result:

    - Passed with no whitespace or patch-formatting issues.

    ### Backend sanity check

    I ran:

    ```bash
    python -m compileall backend/app
    ```

    Result:

    - Passed.

    ### Compose validation

    I ran:

    ```bash
    ./scripts/dev-compose.sh config
    ```

    Result:

    - Passed.
    - Docker Compose resolved all bind mounts, build contexts, ports, health checks, and the renamed Compose file path correctly.

    ### Containerized runtime verification

    I ran:

    ```bash
    ./scripts/dev-compose.sh up -d --build
    ./scripts/dev-compose.sh ps
    curl -fsS http://localhost:8565/api/hello
    curl -fsS http://localhost:8566 | head -n 20
    ```

    Results:

    - `backend`, `frontend`, and `browser` came up successfully.
    - `backend` and `frontend` both reached healthy status.
    - `GET /api/hello` returned `{"message":"Hello from FastAPI!"}`.
    - The frontend served the expected Vite HTML shell on port `8566`.

    ### Browser-based verification and screenshot

    Using the repo’s `webapp-qa` flow, I ran:

    ```bash
    ./scripts/dev-compose.sh run --rm browser npm run check -- --spec ./examples/homepage.spec.json
    ```

    Results:

    - Passed.
    - Assertions for `Hello, world!` and `Hello from FastAPI!` both succeeded.
    - Screenshot written to `.artifacts/webapp-qa/homepage.png`.
    - I opened the screenshot and confirmed the expected scaffold card rendered correctly with the backend message visible.

    ### Frontend build verification

    Host-side attempt:

    ```bash
    cd frontend
    npm run build
    ```

    Result:

    - Failed on the host with `sh: vite: command not found`.

    Follow-up containerized verification:

    ```bash
    ./scripts/dev-compose.sh run --rm frontend npm run build
    ```

    Result:

    - Passed.
    - Production build completed successfully inside the supported containerized environment.

    ### Cleanup

    I ran:

    ```bash
    ./scripts/dev-compose.sh down
    ```

    Result:

    - Stack shut down cleanly and removed its containers and network.

    ## Tests, builds, browser checks, screenshots, and remaining limits

    - Automated tests added: none
    - Automated tests run: none beyond the existing browser smoke spec and backend compile check
    - Builds run:
      - frontend production build in container: passed
      - host-side frontend build: failed because local Vite was not available on the machine path
    - Browser checks run:
      - homepage smoke spec: passed

## Command Started

- Time: `2026-03-31T21:21:54-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `26`
- Summary: in progress: /bin/zsh -lc "sed -n '1,260p' prompts/02-vite-react-scaffold.summary.md"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,260p' prompts/02-vite-react-scaffold.summary.md"
    Status: in progress

## Command Finished

- Time: `2026-03-31T21:21:54-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `27`
- Summary: completed, exit 0: /bin/zsh -lc "sed -n '1,260p' prompts/02-vite-react-scaffold.summary.md"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,260p' prompts/02-vite-react-scaffold.summary.md"
    Status: completed
    Exit code: 0
    Output:
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

## Command Started

- Time: `2026-03-31T21:22:00-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `28`
- Summary: in progress: /bin/zsh -lc "sed -n '1,220p' backend/Dockerfile"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,220p' backend/Dockerfile"
    Status: in progress

## Command Finished

- Time: `2026-03-31T21:22:00-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `29`
- Summary: completed, exit 0: /bin/zsh -lc "sed -n '1,220p' backend/Dockerfile"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,220p' backend/Dockerfile"
    Status: completed
    Exit code: 0
    Output:
    FROM python:3.12-slim

    WORKDIR /app

    COPY requirements.txt .
    RUN pip install --no-cache-dir -r requirements.txt

    COPY app ./app

    EXPOSE 8565

## Command Started

- Time: `2026-03-31T21:22:00-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `30`
- Summary: in progress: /bin/zsh -lc "sed -n '1,260p' infra/compose/docker-compose.yml"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,260p' infra/compose/docker-compose.yml"
    Status: in progress

## Command Finished

- Time: `2026-03-31T21:22:00-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `31`
- Summary: completed, exit 0: /bin/zsh -lc "sed -n '1,260p' infra/compose/docker-compose.yml"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,260p' infra/compose/docker-compose.yml"
    Status: completed
    Exit code: 0
    Output:
    services:
      backend:
        build:
          context: ../../backend
        working_dir: /app
        volumes:
          - ../../backend:/app
        environment:
          PYTHONDONTWRITEBYTECODE: "1"
          PYTHONUNBUFFERED: "1"
        ports:
          - "8565:8565"
        command: uvicorn app.main:app --reload --host 0.0.0.0 --port 8565
        healthcheck:
          test:
            - CMD
            - python
            - -c
            - |
              import sys, urllib.request
              urllib.request.urlopen("http://127.0.0.1:8565/api/hello")
              sys.exit(0)
          interval: 5s
          timeout: 5s
          retries: 20
          start_period: 5s

      frontend:
        build:
          context: ../../frontend
        depends_on:
          backend:
            condition: service_healthy
        working_dir: /app
        environment:
          CHOKIDAR_USEPOLLING: "true"
          VITE_DEV_PROXY_TARGET: http://backend:8565
        volumes:
          - ../../frontend:/app
          - /app/node_modules
        ports:
          - "8566:8566"
        command: npm run dev -- --host 0.0.0.0 --port 8566
        healthcheck:
          test:
            - CMD
            - node
            - -e
            - |
              require("http").get("http://127.0.0.1:8566", (response) => {
                process.exit(response.statusCode === 200 ? 0 : 1);
              }).on("error", () => process.exit(1));
          interval: 5s
          timeout: 5s
          retries: 20
          start_period: 10s

      browser:
        build:
          context: ../../tools/webapp-qa
        depends_on:
          frontend:
            condition: service_healthy
        working_dir: /workspace/tools/webapp-qa
        environment:
          PUPPETEER_EXECUTABLE_PATH: /usr/bin/chromium
          TARGET_BASE_URL: http://frontend:8566
        volumes:
          - ../../:/workspace
          - webapp_qa_node_modules:/workspace/tools/webapp-qa/node_modules
        command: sleep infinity

    volumes:
      webapp_qa_node_modules:

## Command Started

- Time: `2026-03-31T21:22:00-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `32`
- Summary: in progress: /bin/zsh -lc "sed -n '1,260p' docs/architecture-overview.md"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,260p' docs/architecture-overview.md"
    Status: in progress

## Command Finished

- Time: `2026-03-31T21:22:00-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `33`
- Summary: completed, exit 0: /bin/zsh -lc "sed -n '1,260p' docs/architecture-overview.md"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,260p' docs/architecture-overview.md"
    Status: completed
    Exit code: 0
    Output:
    # Architecture Overview

    ## System Picture

    Storyteller is a full-stack application with a browser client, a backend-owned workflow engine, durable relational state, durable object storage, and resumable background jobs.

    ```text
    React + Vite client
            |
            v
    FastAPI API layer
            |
            +--> domain services and policy layer
            |         |
            |         +--> AI adapters for planning, composition, and narration
            |         |
            |         +--> repositories for sessions, workflow state, jobs, and event log
            |
            +--> background workers for composition and audio generation
                      |
                      +--> PostgreSQL for durable structured state
                      +--> file-backed GCS emulator for artifacts and intermediate blobs
    ```

    ## Why Gemini Calls Must Stay on the Backend

    All Gemini access belongs on the server side for four reasons:

    1. Secrets control: provider credentials live in local `secrets.yaml` and must never enter the browser.
    2. Policy enforcement: chat-to-UI actions and workflow transitions need deterministic server validation before the model can change session state.
    3. Durable orchestration: prompts, structured outputs, retries, and model selection need to be coordinated with persistent session data and job records.
    4. Provider flexibility: keeping Gemini behind backend adapters lets the app keep a stable internal interface while model IDs, structured output tactics, or narration providers evolve.

    The frontend should only call the backend's API and subscribe to backend-owned progress events.

    ## Why Composition and Audio Must Use Resumable Server-Side Jobs

    Composition and narration are long-running operations that cannot safely live inside request threads or browser memory. They need server-side jobs because:

    - a user must be able to refresh the page or return later without losing progress
    - partial story text and audio segments need durable checkpoints
    - progress updates need a single source of truth that both chat and UI can observe
    - retries, cancellation, and resume logic need explicit job state rather than transient in-memory state

    The durable model should include job records, segment records, asset metadata, and an event log that can reconstruct session progress after interruption.

    ## Intended Backend Shape

    The target backend should separate concerns explicitly:

    - `api/`: HTTP routes and websocket endpoints
    - `settings/`: environment and secrets loading
    - `db/`: database engine, migrations, and persistence setup
    - `models/`: typed domain models and persistence schemas
    - `repositories/`: database access for sessions, events, jobs, and assets
    - `services/`: workflow logic and policy enforcement
    - `ai/`: Gemini planning, composition, and narration adapters
    - `worker/`: background job execution for writing and audio
    - `storage/`: object storage abstraction over the local GCS emulator

    ## Durable Domain Concepts

    The system should persist the following concepts as first-class records:

    - Session
    - Workflow stage
    - Event log
    - Selected genre
    - Selected tone
    - Story brief
    - Pitch batch and selected pitch
    - Character batch and selected character sheet
    - Beat sheet
    - Story setup preferences
    - Outline or chapter plan
    - Continuity bible
    - Composition job and segments
    - Audio job and segments
    - Asset metadata

    ## Current Repository State

    The repository currently contains an initial scaffold:

    - `frontend/`: Vite React TypeScript app
    - `backend/`: FastAPI app
    - `backend/migrations/`: reserved home for database schema history
    - `backend/app/worker/`: reserved home for background job runners
    - `infra/compose/docker-compose.yml`: local frontend, backend, and browser QA services
    - `infra/persistence/`: notes for persistent local infrastructure data
    - `scripts/dev-compose.sh`: convenience entrypoint for the Compose stack
    - `tools/webapp-qa/`: containerized browser automation support

    PostgreSQL, the file-backed GCS emulator, background workers, and most domain layers are still planned work. This document records the required direction so later prompts can extend the scaffold without changing the architectural contract.

## Command Started

- Time: `2026-03-31T21:22:00-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `34`
- Summary: in progress: /bin/zsh -lc "sed -n '1,220p' prompts/03-fastapi-scaffold.md"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,220p' prompts/03-fastapi-scaffold.md"
    Status: in progress

## Command Finished

- Time: `2026-03-31T21:22:00-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `35`
- Summary: completed, exit 0: /bin/zsh -lc "sed -n '1,220p' prompts/03-fastapi-scaffold.md"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,220p' prompts/03-fastapi-scaffold.md"
    Status: completed
    Exit code: 0
    Output:
    # 03 — Scaffold the FastAPI Backend

    Read `base_prompt.md` first and preserve all prior prompt work.

    ## Objective

    Initialize the backend as a FastAPI service with clear application startup, health routes, configuration loading, and room for future modules.

    ## Build
    - Create the FastAPI app package, a health endpoint, and a versioned API router structure.
    - Add a backend dependency file or `pyproject.toml` and a local run command.
    - Split the code into sensible modules such as settings, api routes, db, services, and domain models.

    ## Deliverables

    - `backend/` FastAPI project
    - A `/health` endpoint
    - Basic backend run instructions in the backend README

    ## Acceptance checks

    - The API can start locally and return a successful health response.
    - The code layout makes it obvious where future domain services should go.
    - The scaffold does not hide everything in one giant file.

    ## Notes

    Prefer boring, maintainable FastAPI structure over magic.

    ## Suggested commit label

    `feat(prompt-03): fastapi scaffold`

## Agent Message

- Time: `2026-03-31T21:22:44-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `36`
- Summary: I’ve confirmed the current backend is just a single `main.py` plus a legacy `/api/hello` check. I’m moving it to an app-factory layout with settings, versioned routers, a real `/health` endpoint, and a compatibility path so the existing...

### Full Text

    I’ve confirmed the current backend is just a single `main.py` plus a legacy `/api/hello` check. I’m moving it to an app-factory layout with settings, versioned routers, a real `/health` endpoint, and a compatibility path so the existing frontend doesn’t regress.

## Command Started

- Time: `2026-03-31T21:22:44-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `37`
- Summary: in progress: /bin/zsh -lc "sed -n '1,220p' frontend/src/features/system/useBackendStatus.ts"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,220p' frontend/src/features/system/useBackendStatus.ts"
    Status: in progress

## Command Finished

- Time: `2026-03-31T21:22:44-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `38`
- Summary: completed, exit 0: /bin/zsh -lc "sed -n '1,220p' frontend/src/features/system/useBackendStatus.ts"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,220p' frontend/src/features/system/useBackendStatus.ts"
    Status: completed
    Exit code: 0
    Output:
    import { useEffect, useState } from 'react'
    import { resolveApiUrl } from '../../shared/api.ts'

    type BackendState = 'loading' | 'online' | 'offline'

    type BackendStatus = {
      state: BackendState
      label: string
      detail: string
      message: string
    }

    const loadingStatus: BackendStatus = {
      state: 'loading',
      label: 'Checking',
      detail: 'Checking whether the local FastAPI backend is reachable.',
      message: 'Checking /api/hello…',
    }

    export function useBackendStatus() {
      const [status, setStatus] = useState<BackendStatus>(loadingStatus)

      useEffect(() => {
        let isCurrent = true

        async function loadBackendStatus() {
          try {
            const response = await fetch(resolveApiUrl('/api/hello'))

            if (!response.ok) {
              throw new Error(`Unexpected status code: ${response.status}`)
            }

            const payload = (await response.json()) as { message?: string }

            if (!isCurrent) {
              return
            }

            setStatus({
              state: 'online',
              label: 'Online',
              detail:
                'The frontend is talking to the backend through the Vite dev proxy.',
              message: payload.message ?? 'Backend responded without a greeting.',
            })
          } catch (error) {
            if (!isCurrent) {
              return
            }

            setStatus({
              state: 'offline',
              label: 'Offline',
              detail:
                'The app still renders without FastAPI, so npm run dev works in isolation.',
              message: 'Running in frontend-only mode.',
            })

            if (import.meta.env.DEV && import.meta.env.MODE !== 'test') {
              console.warn('Backend status check failed.', error)
            }
          }
        }

        void loadBackendStatus()

        return () => {
          isCurrent = false
        }
      }, [])

      return status
    }

## Command Started

- Time: `2026-03-31T21:22:44-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `39`
- Summary: in progress: /bin/zsh -lc "sed -n '1,220p' frontend/src/features/home/HomeRoute.test.tsx"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,220p' frontend/src/features/home/HomeRoute.test.tsx"
    Status: in progress

## Command Finished

- Time: `2026-03-31T21:22:44-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `40`
- Summary: completed, exit 0: /bin/zsh -lc "sed -n '1,220p' frontend/src/features/home/HomeRoute.test.tsx"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,220p' frontend/src/features/home/HomeRoute.test.tsx"
    Status: completed
    Exit code: 0
    Output:
    import { render, screen } from '@testing-library/react'
    import { afterEach, describe, expect, it, vi } from 'vitest'
    import { HomeRoute } from './HomeRoute.tsx'

    describe('HomeRoute', () => {
      afterEach(() => {
        vi.restoreAllMocks()
        vi.unstubAllGlobals()
      })

      it('renders the branded scaffold and reports a healthy backend', async () => {
        const fetchMock = vi.fn().mockResolvedValue({
          ok: true,
          json: async () => ({ message: 'Hello from FastAPI!' }),
        } as Response)

        vi.stubGlobal('fetch', fetchMock)

        render(<HomeRoute />)

        expect(
          screen.getByRole('heading', { level: 1, name: 'Storyteller' }),
        ).toBeInTheDocument()
        expect(screen.getByText('Past sessions come first')).toBeInTheDocument()
        expect(await screen.findByText('Hello from FastAPI!')).toBeInTheDocument()
        expect(screen.getByTestId('backend-state')).toHaveTextContent('Online')
      })

      it('falls back to frontend-only mode when the backend is unavailable', async () => {
        const fetchMock = vi.fn().mockRejectedValue(new Error('offline'))

        vi.stubGlobal('fetch', fetchMock)

        render(<HomeRoute />)

        expect(
          await screen.findByText('Running in frontend-only mode.'),
        ).toBeInTheDocument()
        expect(screen.getByTestId('backend-state')).toHaveTextContent('Offline')
      })
    })

## Command Started

- Time: `2026-03-31T21:22:44-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `41`
- Summary: in progress: /bin/zsh -lc 'git ls-files backend/app/__pycache__/main.cpython-313.pyc backend/app/main.py backend/README.md backend/Dockerfile backend/requirements.txt infra/compose/docker-compose.yml'

### Full Text

    Command: /bin/zsh -lc 'git ls-files backend/app/__pycache__/main.cpython-313.pyc backend/app/main.py backend/README.md backend/Dockerfile backend/requirements.txt infra/compose/docker-compose.yml'
    Status: in progress

## Command Finished

- Time: `2026-03-31T21:22:44-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `42`
- Summary: completed, exit 0: /bin/zsh -lc 'git ls-files backend/app/__pycache__/main.cpython-313.pyc backend/app/main.py backend/README.md backend/Dockerfile backend/requirements.txt infra/compose/docker-compose.yml'

### Full Text

    Command: /bin/zsh -lc 'git ls-files backend/app/__pycache__/main.cpython-313.pyc backend/app/main.py backend/README.md backend/Dockerfile backend/requirements.txt infra/compose/docker-compose.yml'
    Status: completed
    Exit code: 0
    Output:
    backend/Dockerfile
    backend/README.md
    backend/app/main.py
    backend/requirements.txt
    infra/compose/docker-compose.yml

## Command Started

- Time: `2026-03-31T21:22:53-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `43`
- Summary: in progress: /bin/zsh -lc "sed -n '1,260p' .gitignore"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,260p' .gitignore"
    Status: in progress

## Command Finished

- Time: `2026-03-31T21:22:53-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `44`
- Summary: completed, exit 0: /bin/zsh -lc "sed -n '1,260p' .gitignore"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,260p' .gitignore"
    Status: completed
    Exit code: 0
    Output:
    secrets.yaml
    node_modules/
    dist/
    __pycache__/
    .pytest_cache/
    .venv/
    .artifacts/

## Command Started

- Time: `2026-03-31T21:22:53-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `45`
- Summary: in progress: /bin/zsh -lc 'python3 --version'

### Full Text

    Command: /bin/zsh -lc 'python3 --version'
    Status: in progress

## Command Finished

- Time: `2026-03-31T21:22:53-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `46`
- Summary: completed, exit 0: /bin/zsh -lc 'python3 --version'

### Full Text

    Command: /bin/zsh -lc 'python3 --version'
    Status: completed
    Exit code: 0
    Output:
    Python 3.9.6

## Command Started

- Time: `2026-03-31T21:22:53-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `47`
- Summary: in progress: /bin/zsh -lc 'pip3 --version'

### Full Text

    Command: /bin/zsh -lc 'pip3 --version'
    Status: in progress

## Command Finished

- Time: `2026-03-31T21:22:53-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `48`
- Summary: completed, exit 0: /bin/zsh -lc 'pip3 --version'

### Full Text

    Command: /bin/zsh -lc 'pip3 --version'
    Status: completed
    Exit code: 0
    Output:
    pip 21.2.4 from /Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/lib/python3.9/site-packages/pip (python 3.9)

## Agent Message

- Time: `2026-03-31T21:23:11-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `49`
- Summary: Plan: 1. Restructure `backend/app` into an app factory with `settings`, `api`, `services`, `models`, and `db` packages. 2. Add `/health` plus a versioned `/api/v1/health`, while preserving `/api/hello` so the current frontend and Compose...

### Full Text

    Plan:
    1. Restructure `backend/app` into an app factory with `settings`, `api`, `services`, `models`, and `db` packages.
    2. Add `/health` plus a versioned `/api/v1/health`, while preserving `/api/hello` so the current frontend and Compose smoke checks keep working.
    3. Add a small local entrypoint and backend README instructions, then update Compose and docs to point at the new health path.
    4. Add backend tests and run targeted verification: pytest, local startup/health checks, and Compose-level health validation.

## Agent Message

- Time: `2026-03-31T21:25:09-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `50`
- Summary: I’m at the edit stage now. The backend changes will replace the one-file FastAPI app with a small package layout and add tests before I touch Compose/docs so verification stays anchored to real code paths.

### Full Text

    I’m at the edit stage now. The backend changes will replace the one-file FastAPI app with a small package layout and add tests before I touch Compose/docs so verification stays anchored to real code paths.

## File Change Started

- Time: `2026-03-31T21:25:58-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `51`
- Summary: backend/app/__init__.py
backend/app/__main__.py
backend/app/api/__init__.py
backend/app/api/router.py
backend/app/api/routes/__init__.py
backend/app/api/routes/health.py
backend/app/api/routes/legacy.py
backend/app/api/v1/__init__.py
backend/app/api/v1/router.py
backend/app/api/v1/routes/__init__.py
backend/app/api/v1/routes/health.py
backend/app/db/__init__.py
backend/app/db/status.py
backend/app/main.py
backend/app/models/__init__.py
backend/app/models/system.py
backend/app/services/__init__.py
backend/app/services/health.py
backend/app/settings/__init__.py
backend/app/settings/config.py
backend/tests/conftest.py
backend/tests/test_health.py

### Full Text

    backend/app/__init__.py
    backend/app/__main__.py
    backend/app/api/__init__.py
    backend/app/api/router.py
    backend/app/api/routes/__init__.py
    backend/app/api/routes/health.py
    backend/app/api/routes/legacy.py
    backend/app/api/v1/__init__.py
    backend/app/api/v1/router.py
    backend/app/api/v1/routes/__init__.py
    backend/app/api/v1/routes/health.py
    backend/app/db/__init__.py
    backend/app/db/status.py
    backend/app/main.py
    backend/app/models/__init__.py
    backend/app/models/system.py
    backend/app/services/__init__.py
    backend/app/services/health.py
    backend/app/settings/__init__.py
    backend/app/settings/config.py
    backend/tests/conftest.py
    backend/tests/test_health.py

    Additional details:
    {
      "status": "in_progress"
    }

## File Change Recorded

- Time: `2026-03-31T21:25:58-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `52`
- Summary: backend/app/__init__.py
backend/app/__main__.py
backend/app/api/__init__.py
backend/app/api/router.py
backend/app/api/routes/__init__.py
backend/app/api/routes/health.py
backend/app/api/routes/legacy.py
backend/app/api/v1/__init__.py
backend/app/api/v1/router.py
backend/app/api/v1/routes/__init__.py
backend/app/api/v1/routes/health.py
backend/app/db/__init__.py
backend/app/db/status.py
backend/app/main.py
backend/app/models/__init__.py
backend/app/models/system.py
backend/app/services/__init__.py
backend/app/services/health.py
backend/app/settings/__init__.py
backend/app/settings/config.py
backend/tests/conftest.py
backend/tests/test_health.py

### Full Text

    backend/app/__init__.py
    backend/app/__main__.py
    backend/app/api/__init__.py
    backend/app/api/router.py
    backend/app/api/routes/__init__.py
    backend/app/api/routes/health.py
    backend/app/api/routes/legacy.py
    backend/app/api/v1/__init__.py
    backend/app/api/v1/router.py
    backend/app/api/v1/routes/__init__.py
    backend/app/api/v1/routes/health.py
    backend/app/db/__init__.py
    backend/app/db/status.py
    backend/app/main.py
    backend/app/models/__init__.py
    backend/app/models/system.py
    backend/app/services/__init__.py
    backend/app/services/health.py
    backend/app/settings/__init__.py
    backend/app/settings/config.py
    backend/tests/conftest.py
    backend/tests/test_health.py

    Additional details:
    {
      "status": "completed"
    }

## Command Started

- Time: `2026-03-31T21:26:05-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `53`
- Summary: in progress: /bin/zsh -lc "sed -n '1,260p' backend/app/main.py"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,260p' backend/app/main.py"
    Status: in progress

## Command Started

- Time: `2026-03-31T21:26:05-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `54`
- Summary: in progress: /bin/zsh -lc "sed -n '1,260p' backend/app/settings/config.py"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,260p' backend/app/settings/config.py"
    Status: in progress

## Command Started

- Time: `2026-03-31T21:26:05-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `55`
- Summary: in progress: /bin/zsh -lc "sed -n '1,220p' backend/tests/test_health.py"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,220p' backend/tests/test_health.py"
    Status: in progress

## Command Finished

- Time: `2026-03-31T21:26:05-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `56`
- Summary: completed, exit 0: /bin/zsh -lc "sed -n '1,260p' backend/app/main.py"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,260p' backend/app/main.py"
    Status: completed
    Exit code: 0
    Output:
    from __future__ import annotations

    import logging
    from contextlib import asynccontextmanager
    from typing import AsyncIterator

    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware

    from app.api.router import router as api_router
    from app.api.v1.router import router as api_v1_router
    from app.settings import AppSettings, get_settings


    logger = logging.getLogger(__name__)


    def configure_logging(settings: AppSettings) -> None:
        logging.basicConfig(
            level=getattr(logging, settings.log_level, logging.INFO),
            format="%(levelname)s %(name)s %(message)s",
        )


    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        settings = get_settings()
        configure_logging(settings)
        app.state.settings = settings

        logger.info(
            "Starting %s in %s mode on %s:%s",
            settings.app_name,
            settings.environment,
            settings.host,
            settings.port,
        )

        yield

        logger.info("Stopping %s", settings.app_name)


    def create_app() -> FastAPI:
        settings = get_settings()

        app = FastAPI(
            title=settings.app_name,
            version=settings.version,
            lifespan=lifespan,
        )

        app.add_middleware(
            CORSMiddleware,
            allow_origins=list(settings.cors_allowed_origins),
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        app.include_router(api_router)
        app.include_router(api_v1_router, prefix=settings.api_v1_prefix)

        return app


    app = create_app()

## Command Finished

- Time: `2026-03-31T21:26:05-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `57`
- Summary: completed, exit 0: /bin/zsh -lc "sed -n '1,260p' backend/app/settings/config.py"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,260p' backend/app/settings/config.py"
    Status: completed
    Exit code: 0
    Output:
    from __future__ import annotations

    import os
    from dataclasses import dataclass
    from functools import lru_cache
    from typing import Tuple


    DEFAULT_CORS_ALLOWED_ORIGINS = (
        "http://localhost:8566",
        "http://127.0.0.1:8566",
    )


    def _read_bool(name: str, default: bool) -> bool:
        value = os.getenv(name)

        if value is None:
            return default

        return value.strip().lower() in {"1", "true", "yes", "on"}


    def _read_int(name: str, default: int) -> int:
        value = os.getenv(name)

        if value is None:
            return default

        return int(value)


    def _read_csv(name: str, default: Tuple[str, ...]) -> Tuple[str, ...]:
        value = os.getenv(name)

        if not value:
            return default

        items = tuple(item.strip() for item in value.split(",") if item.strip())
        return items or default


    def _normalize_api_prefix(value: str) -> str:
        prefix = value.strip() or "/api/v1"
        return prefix if prefix.startswith("/") else f"/{prefix}"


    @dataclass(frozen=True)
    class AppSettings:
        app_name: str
        environment: str
        version: str
        host: str
        port: int
        reload: bool
        api_v1_prefix: str
        cors_allowed_origins: Tuple[str, ...]
        database_url: str
        log_level: str


    @lru_cache(maxsize=1)
    def get_settings() -> AppSettings:
        environment = os.getenv("STORYTELLER_ENVIRONMENT", "development").strip()

        return AppSettings(
            app_name=os.getenv("STORYTELLER_APP_NAME", "Storyteller API").strip(),
            environment=environment,
            version=os.getenv("STORYTELLER_VERSION", "0.1.0").strip(),
            host=os.getenv("STORYTELLER_HOST", "0.0.0.0").strip(),
            port=_read_int("STORYTELLER_PORT", 8565),
            reload=_read_bool(
                "STORYTELLER_RELOAD",
                environment.lower() == "development",
            ),
            api_v1_prefix=_normalize_api_prefix(
                os.getenv("STORYTELLER_API_V1_PREFIX", "/api/v1"),
            ),
            cors_allowed_origins=_read_csv(
                "STORYTELLER_CORS_ALLOWED_ORIGINS",
                DEFAULT_CORS_ALLOWED_ORIGINS,
            ),
            database_url=os.getenv("STORYTELLER_DATABASE_URL", "").strip(),
            log_level=os.getenv("STORYTELLER_LOG_LEVEL", "INFO").strip().upper(),
        )

## Command Started

- Time: `2026-03-31T21:26:05-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `58`
- Summary: in progress: /bin/zsh -lc 'find backend/app -maxdepth 4 -type f | sort'

### Full Text

    Command: /bin/zsh -lc 'find backend/app -maxdepth 4 -type f | sort'
    Status: in progress

## Command Finished

- Time: `2026-03-31T21:26:05-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `59`
- Summary: completed, exit 0: /bin/zsh -lc "sed -n '1,220p' backend/tests/test_health.py"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,220p' backend/tests/test_health.py"
    Status: completed
    Exit code: 0
    Output:
    from fastapi.testclient import TestClient


    def test_health_endpoint_returns_service_metadata(client: TestClient) -> None:
        response = client.get("/health")

        assert response.status_code == 200
        assert response.json() == {
            "status": "ok",
            "service": "Storyteller API",
            "environment": "development",
            "version": "0.1.0",
            "api_version": None,
            "dependencies": {
                "database": {
                    "status": "not-configured",
                    "detail": (
                        "Database wiring lands in a later prompt; this scaffold "
                        "only reports configuration state."
                    ),
                },
            },
        }


    def test_versioned_health_endpoint_marks_the_api_version(client: TestClient) -> None:
        response = client.get("/api/v1/health")

        assert response.status_code == 200
        payload = response.json()

        assert payload["status"] == "ok"
        assert payload["api_version"] == "v1"
        assert payload["dependencies"]["database"]["status"] == "not-configured"


    def test_legacy_hello_endpoint_remains_available_for_existing_frontend_checks(
        client: TestClient,
    ) -> None:
        response = client.get("/api/hello")

        assert response.status_code == 200
        assert response.json() == {"message": "Hello from FastAPI!"}

## Command Finished

- Time: `2026-03-31T21:26:05-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `60`
- Summary: completed, exit 0: /bin/zsh -lc 'find backend/app -maxdepth 4 -type f | sort'

### Full Text

    Command: /bin/zsh -lc 'find backend/app -maxdepth 4 -type f | sort'
    Status: completed
    Exit code: 0
    Output:
    backend/app/__init__.py
    backend/app/__main__.py
    backend/app/__pycache__/main.cpython-313.pyc
    backend/app/api/__init__.py
    backend/app/api/router.py
    backend/app/api/routes/__init__.py
    backend/app/api/routes/health.py
    backend/app/api/routes/legacy.py
    backend/app/api/v1/__init__.py
    backend/app/api/v1/router.py
    backend/app/api/v1/routes/__init__.py
    backend/app/api/v1/routes/health.py
    backend/app/db/__init__.py
    backend/app/db/status.py
    backend/app/main.py
    backend/app/models/__init__.py
    backend/app/models/system.py
    backend/app/services/__init__.py
    backend/app/services/health.py
    backend/app/settings/__init__.py
    backend/app/settings/config.py
    backend/app/worker/README.md

## Agent Message

- Time: `2026-03-31T21:26:18-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `61`
- Summary: The package layout is in place. I’m wiring the developer-facing pieces now: dependency list, default run command, Compose health check, and README/docs so the scaffold is discoverable instead of only being “correct in code.”

### Full Text

    The package layout is in place. I’m wiring the developer-facing pieces now: dependency list, default run command, Compose health check, and README/docs so the scaffold is discoverable instead of only being “correct in code.”

## File Change Started

- Time: `2026-03-31T21:26:41-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `62`
- Summary: README.md
backend/Dockerfile
backend/README.md
backend/requirements.txt
docs/architecture-overview.md
infra/compose/docker-compose.yml

### Full Text

    README.md
    backend/Dockerfile
    backend/README.md
    backend/requirements.txt
    docs/architecture-overview.md
    infra/compose/docker-compose.yml

    Additional details:
    {
      "status": "in_progress"
    }

## File Change Recorded

- Time: `2026-03-31T21:26:42-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `63`
- Summary: README.md
backend/Dockerfile
backend/README.md
backend/requirements.txt
docs/architecture-overview.md
infra/compose/docker-compose.yml

### Full Text

    README.md
    backend/Dockerfile
    backend/README.md
    backend/requirements.txt
    docs/architecture-overview.md
    infra/compose/docker-compose.yml

    Additional details:
    {
      "status": "completed"
    }

## Agent Message

- Time: `2026-03-31T21:26:49-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `64`
- Summary: The backend scaffold is implemented. I’m switching to verification now: first fast local checks in a backend venv, then Compose-level startup and live health responses, and I’ll clean out generated junk like the stray `__pycache__` befor...

### Full Text

    The backend scaffold is implemented. I’m switching to verification now: first fast local checks in a backend venv, then Compose-level startup and live health responses, and I’ll clean out generated junk like the stray `__pycache__` before finishing.

## Command Started

- Time: `2026-03-31T21:26:49-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `65`
- Summary: in progress: /bin/zsh -lc "rm -rf backend/app/__pycache__ && find backend -type d -name '__pycache__' -prune"

### Full Text

    Command: /bin/zsh -lc "rm -rf backend/app/__pycache__ && find backend -type d -name '__pycache__' -prune"
    Status: in progress

## Command Finished

- Time: `2026-03-31T21:26:49-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `66`
- Summary: completed, exit 0: /bin/zsh -lc "rm -rf backend/app/__pycache__ && find backend -type d -name '__pycache__' -prune"

### Full Text

    Command: /bin/zsh -lc "rm -rf backend/app/__pycache__ && find backend -type d -name '__pycache__' -prune"
    Status: completed
    Exit code: 0

## Command Started

- Time: `2026-03-31T21:26:49-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `67`
- Summary: in progress: /bin/zsh -lc 'git diff -- backend README.md docs/architecture-overview.md infra/compose/docker-compose.yml frontend/src/features/system/useBackendStatus.ts'

### Full Text

    Command: /bin/zsh -lc 'git diff -- backend README.md docs/architecture-overview.md infra/compose/docker-compose.yml frontend/src/features/system/useBackendStatus.ts'
    Status: in progress

## Command Finished

- Time: `2026-03-31T21:26:49-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `68`
- Summary: completed, exit 0: /bin/zsh -lc 'git diff -- backend README.md docs/architecture-overview.md infra/compose/docker-compose.yml frontend/src/features/system/useBackendStatus.ts'

### Full Text

    Command: /bin/zsh -lc 'git diff -- backend README.md docs/architecture-overview.md infra/compose/docker-compose.yml frontend/src/features/system/useBackendStatus.ts'
    Status: completed
    Exit code: 0
    Output:
    diff --git a/README.md b/README.md
    index ebb7010..4ea3b93 100644
    --- a/README.md
    +++ b/README.md
    @@ -75,8 +75,14 @@ The current scaffold does not yet include PostgreSQL or the file-backed GCS emul
     .
     ├── backend/
     │   ├── app/
    +│   │   ├── api/
    +│   │   ├── db/
    +│   │   ├── models/
    +│   │   ├── services/
    +│   │   ├── settings/
     │   │   ├── main.py
     │   │   └── worker/
    +│   ├── tests/
     │   ├── migrations/
     │   ├── Dockerfile
     │   ├── README.md
    @@ -95,7 +101,7 @@ The current scaffold does not yet include PostgreSQL or the file-backed GCS emul
     ```
 
     - `frontend/`: browser client and TypeScript UI foundation
    -- `backend/`: API code, worker home, and migration home
    +- `backend/`: FastAPI API code, settings, services, tests, worker home, and migration home
     - `infra/`: Compose definitions and infrastructure notes
     - `docs/`: product notes, architecture notes, and future ADRs
     - `scripts/`: developer entrypoints such as `dev-compose.sh`
    diff --git a/backend/Dockerfile b/backend/Dockerfile
    index b7458da..8956f21 100644
    --- a/backend/Dockerfile
    +++ b/backend/Dockerfile
    @@ -8,3 +8,5 @@ RUN pip install --no-cache-dir -r requirements.txt
     COPY app ./app
 
     EXPOSE 8565
    +
    +CMD ["python", "-m", "app"]
    diff --git a/backend/README.md b/backend/README.md
    index 64be30d..515df2d 100644
    --- a/backend/README.md
    +++ b/backend/README.md
    @@ -2,11 +2,49 @@
 
     This directory is the home for the FastAPI application, backend-owned workflow logic, and future durable job processing.
 
    -Current contents:
    +## Current layout
 
     - `app/`: live application code
    +  - `api/`: unversioned and versioned route modules
    +  - `db/`: database integration points and health placeholders
    +  - `models/`: API response models and future domain models
    +  - `services/`: backend-owned business logic
    +  - `settings/`: environment-backed application settings
    +  - `worker/`: future background job runners
     - `migrations/`: reserved for database migrations
    +- `tests/`: backend test suite
     - `requirements.txt`: Python dependencies
     - `Dockerfile`: backend container image
 
    -Planned expansion inside `app/` follows the architecture notes in [docs/architecture-overview.md](/Users/kevin/code/storyteller/docs/architecture-overview.md), including explicit homes for API routes, settings, repositories, services, AI adapters, storage, and worker execution.
    +Planned expansion inside `app/` follows the architecture notes in [docs/architecture-overview.md](/Users/kevin/code/storyteller/docs/architecture-overview.md), including explicit homes for repositories, AI adapters, storage, and worker execution.
    +
    +## Local run
    +
    +Install dependencies and start the app from this directory:
    +
    +```bash
    +python3 -m venv .venv
    +source .venv/bin/activate
    +pip install -r requirements.txt
    +python -m app
    +```
    +
    +The local entrypoint reads `STORYTELLER_*` environment variables and defaults to:
    +
    +- host: `0.0.0.0`
    +- port: `8565`
    +- environment: `development`
    +- versioned API prefix: `/api/v1`
    +
    +Useful commands:
    +
    +```bash
    +pytest
    +uvicorn app.main:app --reload --host 0.0.0.0 --port 8565
    +```
    +
    +## Health routes
    +
    +- `GET /health`: primary service health endpoint
    +- `GET /api/v1/health`: versioned API health endpoint
    +- `GET /api/hello`: compatibility endpoint kept for the current frontend scaffold
    diff --git a/backend/app/main.py b/backend/app/main.py
    index 4f8d67a..df3d73b 100644
    --- a/backend/app/main.py
    +++ b/backend/app/main.py
    @@ -1,18 +1,67 @@
    +from __future__ import annotations
    +
    +import logging
    +from contextlib import asynccontextmanager
    +from typing import AsyncIterator
    +
     from fastapi import FastAPI
     from fastapi.middleware.cors import CORSMiddleware
 
    +from app.api.router import router as api_router
    +from app.api.v1.router import router as api_v1_router
    +from app.settings import AppSettings, get_settings
    +
    +
    +logger = logging.getLogger(__name__)
    +
    +
    +def configure_logging(settings: AppSettings) -> None:
    +    logging.basicConfig(
    +        level=getattr(logging, settings.log_level, logging.INFO),
    +        format="%(levelname)s %(name)s %(message)s",
    +    )
    +
    +
    +@asynccontextmanager
    +async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    +    settings = get_settings()
    +    configure_logging(settings)
    +    app.state.settings = settings
    +
    +    logger.info(
    +        "Starting %s in %s mode on %s:%s",
    +        settings.app_name,
    +        settings.environment,
    +        settings.host,
    +        settings.port,
    +    )
    +
    +    yield
    +
    +    logger.info("Stopping %s", settings.app_name)
    +
    +
    +def create_app() -> FastAPI:
    +    settings = get_settings()
    +
    +    app = FastAPI(
    +        title=settings.app_name,
    +        version=settings.version,
    +        lifespan=lifespan,
    +    )
    +
    +    app.add_middleware(
    +        CORSMiddleware,
    +        allow_origins=list(settings.cors_allowed_origins),
    +        allow_credentials=True,
    +        allow_methods=["*"],
    +        allow_headers=["*"],
    +    )
 
    -app = FastAPI(title="Storyteller API")
    +    app.include_router(api_router)
    +    app.include_router(api_v1_router, prefix=settings.api_v1_prefix)
 
    -app.add_middleware(
    -    CORSMiddleware,
    -    allow_origins=["*"],
    -    allow_credentials=True,
    -    allow_methods=["*"],
    -    allow_headers=["*"],
    -)
    +    return app
 
 
    -@app.get("/api/hello")
    -async def hello() -> dict[str, str]:
    -    return {"message": "Hello from FastAPI!"}
    +app = create_app()
    diff --git a/backend/requirements.txt b/backend/requirements.txt
    index babedd0..60b96d9 100644
    --- a/backend/requirements.txt
    +++ b/backend/requirements.txt
    @@ -1,2 +1,4 @@
     fastapi==0.116.1
    +httpx==0.28.1
    +pytest==8.4.2
     uvicorn[standard]==0.35.0
    diff --git a/docs/architecture-overview.md b/docs/architecture-overview.md
    index 21c1777..853d16f 100644
    --- a/docs/architecture-overview.md
    +++ b/docs/architecture-overview.md
    @@ -83,7 +83,7 @@ The system should persist the following concepts as first-class records:
     The repository currently contains an initial scaffold:
 
     - `frontend/`: Vite React TypeScript app
    -- `backend/`: FastAPI app
    +- `backend/`: FastAPI app with an app factory, versioned routers, settings loader, models, services, and database placeholders
     - `backend/migrations/`: reserved home for database schema history
     - `backend/app/worker/`: reserved home for background job runners
     - `infra/compose/docker-compose.yml`: local frontend, backend, and browser QA services
    diff --git a/infra/compose/docker-compose.yml b/infra/compose/docker-compose.yml
    index 8bbe2f9..692adcf 100644
    --- a/infra/compose/docker-compose.yml
    +++ b/infra/compose/docker-compose.yml
    @@ -8,9 +8,10 @@ services:
         environment:
           PYTHONDONTWRITEBYTECODE: "1"
           PYTHONUNBUFFERED: "1"
    +      STORYTELLER_ENVIRONMENT: development
         ports:
           - "8565:8565"
    -    command: uvicorn app.main:app --reload --host 0.0.0.0 --port 8565
    +    command: python -m app
         healthcheck:
           test:
             - CMD
    @@ -18,7 +19,7 @@ services:
             - -c
             - |
               import sys, urllib.request
    -          urllib.request.urlopen("http://127.0.0.1:8565/api/hello")
    +          urllib.request.urlopen("http://127.0.0.1:8565/health")
               sys.exit(0)
           interval: 5s
           timeout: 5s

## Command Started

- Time: `2026-03-31T21:26:50-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `69`
- Summary: in progress: /bin/zsh -lc 'python3 -m venv backend/.venv && source backend/.venv/bin/activate && pip install -r backend/requirements.txt'

### Full Text

    Command: /bin/zsh -lc 'python3 -m venv backend/.venv && source backend/.venv/bin/activate && pip install -r backend/requirements.txt'
    Status: in progress

## Command Finished

- Time: `2026-03-31T21:26:59-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `70`
- Summary: completed, exit 0: /bin/zsh -lc 'python3 -m venv backend/.venv && source backend/.venv/bin/activate && pip install -r backend/requirements.txt'

### Full Text

    Command: /bin/zsh -lc 'python3 -m venv backend/.venv && source backend/.venv/bin/activate && pip install -r backend/requirements.txt'
    Status: completed
    Exit code: 0
    Output:
    Collecting fastapi==0.116.1
      Downloading fastapi-0.116.1-py3-none-any.whl (95 kB)
    Collecting httpx==0.28.1
      Downloading httpx-0.28.1-py3-none-any.whl (73 kB)
    Collecting pytest==8.4.2
      Downloading pytest-8.4.2-py3-none-any.whl (365 kB)
    Collecting uvicorn[standard]==0.35.0
      Downloading uvicorn-0.35.0-py3-none-any.whl (66 kB)
    Collecting pydantic!=1.8,!=1.8.1,!=2.0.0,!=2.0.1,!=2.1.0,<3.0.0,>=1.7.4
      Downloading pydantic-2.12.5-py3-none-any.whl (463 kB)
    Collecting starlette<0.48.0,>=0.40.0
      Downloading starlette-0.47.3-py3-none-any.whl (72 kB)
    Collecting typing-extensions>=4.8.0
      Downloading typing_extensions-4.15.0-py3-none-any.whl (44 kB)
    Collecting anyio
      Downloading anyio-4.12.1-py3-none-any.whl (113 kB)
    Collecting idna
      Downloading idna-3.11-py3-none-any.whl (71 kB)
    Collecting certifi
      Downloading certifi-2026.2.25-py3-none-any.whl (153 kB)
    Collecting httpcore==1.*
      Downloading httpcore-1.0.9-py3-none-any.whl (78 kB)
    Collecting tomli>=1
      Downloading tomli-2.4.1-py3-none-any.whl (14 kB)
    Collecting exceptiongroup>=1
      Downloading exceptiongroup-1.3.1-py3-none-any.whl (16 kB)
    Collecting packaging>=20
      Using cached packaging-26.0-py3-none-any.whl (74 kB)
    Collecting pluggy<2,>=1.5
      Downloading pluggy-1.6.0-py3-none-any.whl (20 kB)
    Collecting iniconfig>=1
      Downloading iniconfig-2.1.0-py3-none-any.whl (6.0 kB)
    Collecting pygments>=2.7.2
      Downloading pygments-2.20.0-py3-none-any.whl (1.2 MB)
    Collecting h11>=0.8
      Downloading h11-0.16.0-py3-none-any.whl (37 kB)
    Collecting click>=7.0
      Using cached click-8.1.8-py3-none-any.whl (98 kB)
    Collecting httptools>=0.6.3
      Downloading httptools-0.7.1-cp39-cp39-macosx_11_0_arm64.whl (110 kB)
    Collecting websockets>=10.4
      Downloading websockets-15.0.1-cp39-cp39-macosx_11_0_arm64.whl (173 kB)
    Collecting pyyaml>=5.1
      Downloading pyyaml-6.0.3-cp39-cp39-macosx_11_0_arm64.whl (174 kB)
    Collecting python-dotenv>=0.13
      Downloading python_dotenv-1.2.1-py3-none-any.whl (21 kB)
    Collecting uvloop>=0.15.1
      Downloading uvloop-0.22.1-cp39-cp39-macosx_10_9_universal2.whl (1.3 MB)
    Collecting watchfiles>=0.13
      Downloading watchfiles-1.1.1-cp39-cp39-macosx_11_0_arm64.whl (396 kB)
    Collecting pydantic-core==2.41.5
      Downloading pydantic_core-2.41.5-cp39-cp39-macosx_11_0_arm64.whl (1.9 MB)
    Collecting typing-inspection>=0.4.2
      Downloading typing_inspection-0.4.2-py3-none-any.whl (14 kB)
    Collecting annotated-types>=0.6.0
      Downloading annotated_types-0.7.0-py3-none-any.whl (13 kB)
    Installing collected packages: typing-extensions, idna, exceptiongroup, typing-inspection, pydantic-core, h11, click, certifi, anyio, annotated-types, websockets, watchfiles, uvloop, uvicorn, tomli, starlette, pyyaml, python-dotenv, pygments, pydantic, pluggy, packaging, iniconfig, httptools, httpcore, pytest, httpx, fastapi
    Successfully installed annotated-types-0.7.0 anyio-4.12.1 certifi-2026.2.25 click-8.1.8 exceptiongroup-1.3.1 fastapi-0.116.1 h11-0.16.0 httpcore-1.0.9 httptools-0.7.1 httpx-0.28.1 idna-3.11 iniconfig-2.1.0 packaging-26.0 pluggy-1.6.0 pydantic-2.12.5 pydantic-core-2.41.5 pygments-2.20.0 pytest-8.4.2 python-dotenv-1.2.1 pyyaml-6.0.3 starlette-0.47.3 tomli-2.4.1 typing-extensions-4.15.0 typing-inspection-0.4.2 uvicorn-0.35.0 uvloop-0.22.1 watchfiles-1.1.1 websockets-15.0.1
    WARNING: You are using pip version 21.2.4; however, version 26.0.1 is available.
    You should consider upgrading via the '/Users/kevin/code/storyteller/backend/.venv/bin/python3 -m pip install --upgrade pip' command.

## Agent Message

- Time: `2026-03-31T21:26:59-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `71`
- Summary: The code diff looks structurally right. I’ve removed the stale bytecode directory and I’m waiting on the backend venv install so I can run pytest and live startup checks without relying only on Docker.

### Full Text

    The code diff looks structurally right. I’ve removed the stale bytecode directory and I’m waiting on the backend venv install so I can run pytest and live startup checks without relying only on Docker.

## Command Started

- Time: `2026-03-31T21:27:08-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `72`
- Summary: in progress: /bin/zsh -lc 'backend/.venv/bin/python -m compileall backend/app'

### Full Text

    Command: /bin/zsh -lc 'backend/.venv/bin/python -m compileall backend/app'
    Status: in progress

## Command Finished

- Time: `2026-03-31T21:27:08-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `73`
- Summary: completed, exit 0: /bin/zsh -lc 'backend/.venv/bin/python -m compileall backend/app'

### Full Text

    Command: /bin/zsh -lc 'backend/.venv/bin/python -m compileall backend/app'
    Status: completed
    Exit code: 0
    Output:
    Listing 'backend/app'...
    Compiling 'backend/app/__init__.py'...
    Compiling 'backend/app/__main__.py'...
    Listing 'backend/app/api'...
    Compiling 'backend/app/api/__init__.py'...
    Compiling 'backend/app/api/router.py'...
    Listing 'backend/app/api/routes'...
    Compiling 'backend/app/api/routes/__init__.py'...
    Compiling 'backend/app/api/routes/health.py'...
    Compiling 'backend/app/api/routes/legacy.py'...
    Listing 'backend/app/api/v1'...
    Compiling 'backend/app/api/v1/__init__.py'...
    Compiling 'backend/app/api/v1/router.py'...
    Listing 'backend/app/api/v1/routes'...
    Compiling 'backend/app/api/v1/routes/__init__.py'...
    Compiling 'backend/app/api/v1/routes/health.py'...
    Listing 'backend/app/db'...
    Compiling 'backend/app/db/__init__.py'...
    Compiling 'backend/app/db/status.py'...
    Compiling 'backend/app/main.py'...
    Listing 'backend/app/models'...
    Compiling 'backend/app/models/__init__.py'...
    Compiling 'backend/app/models/system.py'...
    Listing 'backend/app/services'...
    Compiling 'backend/app/services/__init__.py'...
    Compiling 'backend/app/services/health.py'...
    Listing 'backend/app/settings'...
    Compiling 'backend/app/settings/__init__.py'...
    Compiling 'backend/app/settings/config.py'...
    Listing 'backend/app/worker'...

## Command Started

- Time: `2026-03-31T21:27:08-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `74`
- Summary: in progress: /bin/zsh -lc 'backend/.venv/bin/python -m pytest backend/tests'

### Full Text

    Command: /bin/zsh -lc 'backend/.venv/bin/python -m pytest backend/tests'
    Status: in progress

## Command Finished

- Time: `2026-03-31T21:27:09-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `75`
- Summary: failed, exit 4: /bin/zsh -lc 'backend/.venv/bin/python -m pytest backend/tests'

### Full Text

    Command: /bin/zsh -lc 'backend/.venv/bin/python -m pytest backend/tests'
    Status: failed
    Exit code: 4
    Output:
    ImportError while loading conftest '/Users/kevin/code/storyteller/backend/tests/conftest.py'.
    backend/tests/conftest.py:6: in <module>
        from app.main import create_app
    E   ModuleNotFoundError: No module named 'app'

## Agent Message

- Time: `2026-03-31T21:27:17-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `76`
- Summary: The first pytest run surfaced a real packaging gap: running tests from the repo root couldn’t import `app`. I’m fixing that now so the backend test command works from the repository root, not only from inside `backend/`.

### Full Text

    The first pytest run surfaced a real packaging gap: running tests from the repo root couldn’t import `app`. I’m fixing that now so the backend test command works from the repository root, not only from inside `backend/`.

## File Change Started

- Time: `2026-03-31T21:27:19-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `77`
- Summary: backend/tests/conftest.py

### Full Text

    backend/tests/conftest.py

    Additional details:
    {
      "status": "in_progress"
    }

## File Change Recorded

- Time: `2026-03-31T21:27:19-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `78`
- Summary: backend/tests/conftest.py

### Full Text

    backend/tests/conftest.py

    Additional details:
    {
      "status": "completed"
    }

## Command Started

- Time: `2026-03-31T21:27:23-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `79`
- Summary: in progress: /bin/zsh -lc "sed -n '1,200p' backend/tests/conftest.py"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,200p' backend/tests/conftest.py"
    Status: in progress

## Command Finished

- Time: `2026-03-31T21:27:23-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `80`
- Summary: completed, exit 0: /bin/zsh -lc "sed -n '1,200p' backend/tests/conftest.py"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,200p' backend/tests/conftest.py"
    Status: completed
    Exit code: 0
    Output:
    from pathlib import Path
    import sys
    from collections.abc import Iterator

    import pytest
    from fastapi.testclient import TestClient

    BACKEND_ROOT = Path(__file__).resolve().parents[1]

    if str(BACKEND_ROOT) not in sys.path:
        sys.path.insert(0, str(BACKEND_ROOT))

    from app.main import create_app
    from app.settings import get_settings


    @pytest.fixture
    def client() -> Iterator[TestClient]:
        get_settings.cache_clear()

        with TestClient(create_app()) as test_client:
            yield test_client

        get_settings.cache_clear()

## Command Started

- Time: `2026-03-31T21:27:27-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `81`
- Summary: in progress: /bin/zsh -lc 'backend/.venv/bin/python -m compileall backend/app'

### Full Text

    Command: /bin/zsh -lc 'backend/.venv/bin/python -m compileall backend/app'
    Status: in progress

## Command Finished

- Time: `2026-03-31T21:27:27-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `82`
- Summary: completed, exit 0: /bin/zsh -lc 'backend/.venv/bin/python -m compileall backend/app'

### Full Text

    Command: /bin/zsh -lc 'backend/.venv/bin/python -m compileall backend/app'
    Status: completed
    Exit code: 0
    Output:
    Listing 'backend/app'...
    Listing 'backend/app/api'...
    Listing 'backend/app/api/routes'...
    Listing 'backend/app/api/v1'...
    Listing 'backend/app/api/v1/routes'...
    Listing 'backend/app/db'...
    Listing 'backend/app/models'...
    Listing 'backend/app/services'...
    Listing 'backend/app/settings'...
    Listing 'backend/app/worker'...

## Command Started

- Time: `2026-03-31T21:27:27-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `83`
- Summary: in progress: /bin/zsh -lc 'backend/.venv/bin/python -m pytest backend/tests'

### Full Text

    Command: /bin/zsh -lc 'backend/.venv/bin/python -m pytest backend/tests'
    Status: in progress

## Command Finished

- Time: `2026-03-31T21:27:28-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `84`
- Summary: completed, exit 0: /bin/zsh -lc 'backend/.venv/bin/python -m pytest backend/tests'

### Full Text

    Command: /bin/zsh -lc 'backend/.venv/bin/python -m pytest backend/tests'
    Status: completed
    Exit code: 0
    Output:
    ============================= test session starts ==============================
    platform darwin -- Python 3.9.6, pytest-8.4.2, pluggy-1.6.0
    rootdir: /Users/kevin/code/storyteller
    plugins: anyio-4.12.1
    collected 3 items

    backend/tests/test_health.py ...                                         [100%]

    ============================== 3 passed in 0.01s ===============================

## Agent Message

- Time: `2026-03-31T21:27:34-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `85`
- Summary: Pytest now passes from the repo root. I’m doing the last two runtime checks: local process startup from `backend/` itself, then the Docker Compose stack with the new `/health` health check.

### Full Text

    Pytest now passes from the repo root. I’m doing the last two runtime checks: local process startup from `backend/` itself, then the Docker Compose stack with the new `/health` health check.

## Command Started

- Time: `2026-03-31T21:27:35-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `86`
- Summary: in progress: /bin/zsh -lc '.venv/bin/python -m app'

### Full Text

    Command: /bin/zsh -lc '.venv/bin/python -m app'
    Status: in progress

## Command Started

- Time: `2026-03-31T21:27:40-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `87`
- Summary: in progress: /bin/zsh -lc 'curl -fsS http://127.0.0.1:8565/api/hello'

### Full Text

    Command: /bin/zsh -lc 'curl -fsS http://127.0.0.1:8565/api/hello'
    Status: in progress

## Command Started

- Time: `2026-03-31T21:27:40-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `88`
- Summary: in progress: /bin/zsh -lc 'curl -fsS http://127.0.0.1:8565/api/v1/health'

### Full Text

    Command: /bin/zsh -lc 'curl -fsS http://127.0.0.1:8565/api/v1/health'
    Status: in progress

## Command Started

- Time: `2026-03-31T21:27:40-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `89`
- Summary: in progress: /bin/zsh -lc 'curl -fsS http://127.0.0.1:8565/health'

### Full Text

    Command: /bin/zsh -lc 'curl -fsS http://127.0.0.1:8565/health'
    Status: in progress

## Command Finished

- Time: `2026-03-31T21:27:40-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `90`
- Summary: completed, exit 0: /bin/zsh -lc 'curl -fsS http://127.0.0.1:8565/api/v1/health'

### Full Text

    Command: /bin/zsh -lc 'curl -fsS http://127.0.0.1:8565/api/v1/health'
    Status: completed
    Exit code: 0
    Output:
    {"status":"ok","service":"Storyteller API","environment":"development","version":"0.1.0","api_version":"v1","dependencies":{"database":{"status":"not-configured","detail":"Database wiring lands in a later prompt; this scaffold only reports configuration state."}}}

## Command Finished

- Time: `2026-03-31T21:27:40-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `91`
- Summary: completed, exit 0: /bin/zsh -lc 'curl -fsS http://127.0.0.1:8565/health'

### Full Text

    Command: /bin/zsh -lc 'curl -fsS http://127.0.0.1:8565/health'
    Status: completed
    Exit code: 0
    Output:
    {"status":"ok","service":"Storyteller API","environment":"development","version":"0.1.0","api_version":null,"dependencies":{"database":{"status":"not-configured","detail":"Database wiring lands in a later prompt; this scaffold only reports configuration state."}}}

## Command Finished

- Time: `2026-03-31T21:27:40-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `92`
- Summary: completed, exit 0: /bin/zsh -lc 'curl -fsS http://127.0.0.1:8565/api/hello'

### Full Text

    Command: /bin/zsh -lc 'curl -fsS http://127.0.0.1:8565/api/hello'
    Status: completed
    Exit code: 0
    Output:
    {"message":"Hello from FastAPI!"}

## Command Finished

- Time: `2026-03-31T21:27:43-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `93`
- Summary: completed, exit 0: /bin/zsh -lc '.venv/bin/python -m app'

### Full Text

    Command: /bin/zsh -lc '.venv/bin/python -m app'
    Status: completed
    Exit code: 0
    Output:
    [32mINFO[0m:     Will watch for changes in these directories: ['/Users/kevin/code/storyteller/backend']
    [32mINFO[0m:     Uvicorn running on [1mhttp://0.0.0.0:8565[0m (Press CTRL+C to quit)
    [32mINFO[0m:     Started reloader process [[36m[1m14013[0m] using [36m[1mWatchFiles[0m
    [32mINFO[0m:     Started server process [[36m14047[0m]
    [32mINFO[0m:     Waiting for application startup.
    INFO app.main Starting Storyteller API in development mode on 0.0.0.0:8565
    [32mINFO[0m:     Application startup complete.
    [32mINFO[0m:     127.0.0.1:52339 - "[1mGET /api/hello HTTP/1.1[0m" [32m200 OK[0m
    [32mINFO[0m:     127.0.0.1:52341 - "[1mGET /api/v1/health HTTP/1.1[0m" [32m200 OK[0m
    [32mINFO[0m:     127.0.0.1:52340 - "[1mGET /health HTTP/1.1[0m" [32m200 OK[0m
    ^C[32mINFO[0m:     Shutting down
    [32mINFO[0m:     Waiting for application shutdown.
    INFO app.main Stopping Storyteller API
    [32mINFO[0m:     Application shutdown complete.
    [32mINFO[0m:     Finished server process [[36m14047[0m]
    [32mINFO[0m:     Stopping reloader process [[36m[1m14013[0m]

## Agent Message

- Time: `2026-03-31T21:27:54-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `94`
- Summary: I’ve verified the backend locally in a venv, including live responses from `/health`, `/api/v1/health`, and the legacy `/api/hello`. I’m now doing the repository-level check through Docker Compose so the stack still boots with the new en...

### Full Text

    I’ve verified the backend locally in a venv, including live responses from `/health`, `/api/v1/health`, and the legacy `/api/hello`. I’m now doing the repository-level check through Docker Compose so the stack still boots with the new entrypoint and health check.

## Command Started

- Time: `2026-03-31T21:27:55-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `95`
- Summary: in progress: /bin/zsh -lc './scripts/dev-compose.sh up -d --build'

### Full Text

    Command: /bin/zsh -lc './scripts/dev-compose.sh up -d --build'
    Status: in progress

## Command Finished

- Time: `2026-03-31T21:28:18-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `96`
- Summary: completed, exit 0: /bin/zsh -lc './scripts/dev-compose.sh up -d --build'

### Full Text

    Command: /bin/zsh -lc './scripts/dev-compose.sh up -d --build'
    Status: completed
    Exit code: 0
    Output:
    [1A[1B[0G[?25l[+] Building 0.0s (0/1)                                                         
     => [internal] load local bake definitions                                 0.0s
    [?25h[1A[1A[0G[?25l[+] Building 0.2s (1/1)                                                         
     => [internal] load local bake definitions                                 0.0s
     => => reading from stdin 1.44kB                                           0.0s
    [?25h[1A[1A[1A[0G[?25l[+] Building 0.2s (1/2)                                                         
     => [internal] load local bake definitions                                 0.0s
     => => reading from stdin 1.44kB                                           0.0s
    [?25h[1A[1A[1A[0G[?25l[+] Building 0.5s (6/9)                                                         
     => [internal] load local bake definitions                                 0.0s
     => => reading from stdin 1.44kB                                           0.0s
     => [frontend internal] load build definition from Dockerfile              0.0s
     => => transferring dockerfile: 146B                                       0.0s
     => [browser internal] load build definition from Dockerfile               0.0s
     => => transferring dockerfile: 367B                                       0.0s
     => [backend internal] load build definition from Dockerfile               0.0s
     => => transferring dockerfile: 209B                                       0.0s
     => [backend internal] load metadata for docker.io/library/python:3.12-sl  0.2s
     => [frontend internal] load metadata for docker.io/library/node:20-alpin  0.2s
     => [browser internal] load metadata for docker.io/library/node:20-bookwo  0.2s
     => [auth] library/node:pull token for registry-1.docker.io                0.0s
     => [auth] library/python:pull token for registry-1.docker.io              0.0s
    [?25h[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[0G[?25l[+] Building 0.6s (6/9)                                                         
     => [internal] load local bake definitions                                 0.0s
     => => reading from stdin 1.44kB                                           0.0s
     => [frontend internal] load build definition from Dockerfile              0.0s
     => => transferring dockerfile: 146B                                       0.0s
     => [browser internal] load build definition from Dockerfile               0.0s
     => => transferring dockerfile: 367B                                       0.0s
     => [backend internal] load build definition from Dockerfile               0.0s
     => => transferring dockerfile: 209B                                       0.0s
     => [backend internal] load metadata for docker.io/library/python:3.12-sl  0.4s
     => [frontend internal] load metadata for docker.io/library/node:20-alpin  0.4s
     => [browser internal] load metadata for docker.io/library/node:20-bookwo  0.4s
     => [auth] library/node:pull token for registry-1.docker.io                0.0s
     => [auth] library/python:pull token for registry-1.docker.io              0.0s
    [?25h[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[0G[?25l[+] Building 0.8s (6/9)                                                         
     => [internal] load local bake definitions                                 0.0s
     => => reading from stdin 1.44kB                                           0.0s
     => [frontend internal] load build definition from Dockerfile              0.0s
     => => transferring dockerfile: 146B                                       0.0s
     => [browser internal] load build definition from Dockerfile               0.0s
     => => transferring dockerfile: 367B                                       0.0s
     => [backend internal] load build definition from Dockerfile               0.0s
     => => transferring dockerfile: 209B                                       0.0s
     => [backend internal] load metadata for docker.io/library/python:3.12-sl  0.5s
     => [frontend internal] load metadata for docker.io/library/node:20-alpin  0.5s
     => [browser internal] load metadata for docker.io/library/node:20-bookwo  0.5s
     => [auth] library/node:pull token for registry-1.docker.io                0.0s
     => [auth] library/python:pull token for registry-1.docker.io              0.0s
    [?25h[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[0G[?25l[+] Building 0.9s (6/9)                                                         
     => [internal] load local bake definitions                                 0.0s
     => => reading from stdin 1.44kB                                           0.0s
     => [frontend internal] load build definition from Dockerfile              0.0s
     => => transferring dockerfile: 146B                                       0.0s
     => [browser internal] load build definition from Dockerfile               0.0s
     => => transferring dockerfile: 367B                                       0.0s
     => [backend internal] load build definition from Dockerfile               0.0s
     => => transferring dockerfile: 209B                                       0.0s
     => [backend internal] load metadata for docker.io/library/python:3.12-sl  0.7s
     => [frontend internal] load metadata for docker.io/library/node:20-alpin  0.7s
     => [browser internal] load metadata for docker.io/library/node:20-bookwo  0.7s
     => [auth] library/node:pull token for registry-1.docker.io                0.0s
     => [auth] library/python:pull token for registry-1.docker.io              0.0s
    [?25h[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[0G[?25l[+] Building 1.0s (7/9)                                                         
     => [internal] load local bake definitions                                 0.0s
     => => reading from stdin 1.44kB                                           0.0s
     => [frontend internal] load build definition from Dockerfile              0.0s
     => => transferring dockerfile: 146B                                       0.0s
     => [browser internal] load build definition from Dockerfile               0.0s
     => => transferring dockerfile: 367B                                       0.0s
     => [backend internal] load build definition from Dockerfile               0.0s
     => => transferring dockerfile: 209B                                       0.0s
     => [backend internal] load metadata for docker.io/library/python:3.12-sl  0.7s
     => [frontend internal] load metadata for docker.io/library/node:20-alpin  0.7s
     => [browser internal] load metadata for docker.io/library/node:20-bookwo  0.7s
     => [auth] library/node:pull token for registry-1.docker.io                0.0s
     => [auth] library/python:pull token for registry-1.docker.io              0.0s
    [?25h[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[0G[?25l[+] Building 1.1s (18/24)                                                       
     => [browser internal] load .dockerignore                                  0.0s
     => => transferring context: 2B                                            0.0s
     => [frontend 1/5] FROM docker.io/library/node:20-alpine@sha256:f598378b5  0.0s
     => => resolve docker.io/library/node:20-alpine@sha256:f598378b5240225e6b  0.0s
     => [browser internal] load build context                                  0.0s
     => => transferring context: 72B                                           0.0s
     => [frontend internal] load build context                                 0.1s
     => => transferring context: 34B                                           0.1s
     => [browser 1/5] FROM docker.io/library/node:20-bookworm-slim@sha256:1e8  0.0s
     => => resolve docker.io/library/node:20-bookworm-slim@sha256:1e85773c98c  0.0s
     => CACHED [browser 2/5] RUN apt-get update   && apt-get install -y --no-  0.0s
     => CACHED [browser 3/5] WORKDIR /workspace/tools/webapp-qa                0.0s
     => CACHED [browser 4/5] COPY package.json package-lock.json* ./           0.0s
     => CACHED [browser 5/5] RUN npm install                                   0.0s
     => [browser] exporting to image                                           0.1s
     => => exporting layers                                                    0.0s
     => => exporting manifest sha256:847eae24267fe1117d23f3e7bb5abb607bcdbbc4  0.0s
     => => exporting config sha256:bc8793160bb32391c252a551894eb1a94dbabdfdd3  0.0s
     => => exporting attestation manifest sha256:527eaadb6fabeaf976589861c443  0.0s
     => => exporting manifest list sha256:ef796cafeb2612f72bdffe9a1457a811287  0.0s
     => => naming to docker.io/library/compose-browser:latest                  0.0s
     => => unpacking to docker.io/library/compose-browser:latest               0.0s
    [?25h[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[0G[?25l[+] Building 1.2s (24/31)                                                       
     => [frontend internal] load build context                                 0.2s
     => => transferring context: 466.02kB                                      0.2s
     => CACHED [browser 3/5] WORKDIR /workspace/tools/webapp-qa                0.0s
     => CACHED [browser 4/5] COPY package.json package-lock.json* ./           0.0s
     => CACHED [browser 5/5] RUN npm install                                   0.0s
     => [browser] exporting to image                                           0.1s
     => => exporting layers                                                    0.0s
     => => exporting manifest sha256:847eae24267fe1117d23f3e7bb5abb607bcdbbc4  0.0s
     => => exporting config sha256:bc8793160bb32391c252a551894eb1a94dbabdfdd3  0.0s
     => => exporting attestation manifest sha256:527eaadb6fabeaf976589861c443  0.0s
     => => exporting manifest list sha256:ef796cafeb2612f72bdffe9a1457a811287  0.0s
     => => naming to docker.io/library/compose-browser:latest                  0.0s
     => => unpacking to docker.io/library/compose-browser:latest               0.0s
     => [backend internal] load .dockerignore                                  0.0s
     => => transferring context: 2B                                            0.0s
     => [backend 1/5] FROM docker.io/library/python:3.12-slim@sha256:3d5ed973  0.0s
     => => resolve docker.io/library/python:3.12-slim@sha256:3d5ed973e45820f5  0.0s
     => [backend internal] load build context                                  0.0s
     => => transferring context: 9.45kB                                        0.0s
     => CACHED [backend 2/5] WORKDIR /app                                      0.0s
     => [backend 3/5] COPY requirements.txt .                                  0.0s
     => [backend 4/5] RUN pip install --no-cache-dir -r requirements.txt       0.0s
    [?25h[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[0G[?25l[+] Building 1.3s (26/32)                                                       
     => CACHED [browser 2/5] RUN apt-get update   && apt-get install -y --no-  0.0s
     => CACHED [browser 3/5] WORKDIR /workspace/tools/webapp-qa                0.0s
     => CACHED [browser 4/5] COPY package.json package-lock.json* ./           0.0s
     => CACHED [browser 5/5] RUN npm install                                   0.0s
     => [browser] exporting to image                                           0.1s
     => => exporting layers                                                    0.0s
     => => exporting manifest sha256:847eae24267fe1117d23f3e7bb5abb607bcdbbc4  0.0s
     => => exporting config sha256:bc8793160bb32391c252a551894eb1a94dbabdfdd3  0.0s
     => => exporting attestation manifest sha256:527eaadb6fabeaf976589861c443  0.0s
     => => exporting manifest list sha256:ef796cafeb2612f72bdffe9a1457a811287  0.0s
     => => naming to docker.io/library/compose-browser:latest                  0.0s
     => => unpacking to docker.io/library/compose-browser:latest               0.0s
     => [backend internal] load .dockerignore                                  0.0s
     => => transferring context: 2B                                            0.0s
     => [backend 1/5] FROM docker.io/library/python:3.12-slim@sha256:3d5ed973  0.0s
     => => resolve docker.io/library/python:3.12-slim@sha256:3d5ed973e45820f5  0.0s
     => [backend internal] load build context                                  0.0s
     => => transferring context: 9.45kB                                        0.0s
     => CACHED [backend 2/5] WORKDIR /app                                      0.0s
     => [backend 3/5] COPY requirements.txt .                                  0.0s
     => [backend 4/5] RUN pip install --no-cache-dir -r requirements.txt       0.1s
     => [browser] resolving provenance for metadata file                       0.0s
    [?25h[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[0G[?25l[+] Building 1.4s (29/32)                                                       
     => [browser] exporting to image                                           0.1s
     => => exporting layers                                                    0.0s
     => => exporting manifest sha256:847eae24267fe1117d23f3e7bb5abb607bcdbbc4  0.0s
     => => exporting config sha256:bc8793160bb32391c252a551894eb1a94dbabdfdd3  0.0s
     => => exporting attestation manifest sha256:527eaadb6fabeaf976589861c443  0.0s
     => => exporting manifest list sha256:ef796cafeb2612f72bdffe9a1457a811287  0.0s
     => => naming to docker.io/library/compose-browser:latest                  0.0s
     => => unpacking to docker.io/library/compose-browser:latest               0.0s
     => [backend internal] load .dockerignore                                  0.0s
     => => transferring context: 2B                                            0.0s
     => [backend 1/5] FROM docker.io/library/python:3.12-slim@sha256:3d5ed973  0.0s
     => => resolve docker.io/library/python:3.12-slim@sha256:3d5ed973e45820f5  0.0s
     => [backend internal] load build context                                  0.0s
     => => transferring context: 9.45kB                                        0.0s
     => CACHED [backend 2/5] WORKDIR /app                                      0.0s
     => [backend 3/5] COPY requirements.txt .                                  0.0s
     => [backend 4/5] RUN pip install --no-cache-dir -r requirements.txt       0.3s
     => [browser] resolving provenance for metadata file                       0.0s
     => CACHED [frontend 2/5] WORKDIR /app                                     0.0s
     => CACHED [frontend 3/5] COPY package.json package-lock.json* ./          0.0s
     => CACHED [frontend 4/5] RUN npm ci                                       0.0s
     => [frontend 5/5] COPY . .                                                0.2s
    [?25h[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[0G[?25l[+] Building 1.6s (29/32)                                                       
     => [browser] exporting to image                                           0.1s
     => => exporting layers                                                    0.0s
     => => exporting manifest sha256:847eae24267fe1117d23f3e7bb5abb607bcdbbc4  0.0s
     => => exporting config sha256:bc8793160bb32391c252a551894eb1a94dbabdfdd3  0.0s
     => => exporting attestation manifest sha256:527eaadb6fabeaf976589861c443  0.0s
     => => exporting manifest list sha256:ef796cafeb2612f72bdffe9a1457a811287  0.0s
     => => naming to docker.io/library/compose-browser:latest                  0.0s
     => => unpacking to docker.io/library/compose-browser:latest               0.0s
     => [backend internal] load .dockerignore                                  0.0s
     => => transferring context: 2B                                            0.0s
     => [backend 1/5] FROM docker.io/library/python:3.12-slim@sha256:3d5ed973  0.0s
     => => resolve docker.io/library/python:3.12-slim@sha256:3d5ed973e45820f5  0.0s
     => [backend internal] load build context                                  0.0s
     => => transferring context: 9.45kB                                        0.0s
     => CACHED [backend 2/5] WORKDIR /app                                      0.0s
     => [backend 3/5] COPY requirements.txt .                                  0.0s
     => [backend 4/5] RUN pip install --no-cache-dir -r requirements.txt       0.4s
     => [browser] resolving provenance for metadata file                       0.0s
     => CACHED [frontend 2/5] WORKDIR /app                                     0.0s
     => CACHED [frontend 3/5] COPY package.json package-lock.json* ./          0.0s
     => CACHED [frontend 4/5] RUN npm ci                                       0.0s
     => [frontend 5/5] COPY . .                                                0.3s
    [?25h[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[0G[?25l[+] Building 1.7s (29/32)                                                       
     => [browser] exporting to image                                           0.1s
     => => exporting layers                                                    0.0s
     => => exporting manifest sha256:847eae24267fe1117d23f3e7bb5abb607bcdbbc4  0.0s
     => => exporting config sha256:bc8793160bb32391c252a551894eb1a94dbabdfdd3  0.0s
     => => exporting attestation manifest sha256:527eaadb6fabeaf976589861c443  0.0s
     => => exporting manifest list sha256:ef796cafeb2612f72bdffe9a1457a811287  0.0s
     => => naming to docker.io/library/compose-browser:latest                  0.0s
     => => unpacking to docker.io/library/compose-browser:latest               0.0s
     => [backend internal] load .dockerignore                                  0.0s
     => => transferring context: 2B                                            0.0s
     => [backend 1/5] FROM docker.io/library/python:3.12-slim@sha256:3d5ed973  0.0s
     => => resolve docker.io/library/python:3.12-slim@sha256:3d5ed973e45820f5  0.0s
     => [backend internal] load build context                                  0.0s
     => => transferring context: 9.45kB                                        0.0s
     => CACHED [backend 2/5] WORKDIR /app                                      0.0s
     => [backend 3/5] COPY requirements.txt .                                  0.0s
     => [backend 4/5] RUN pip install --no-cache-dir -r requirements.txt       0.6s
     => [browser] resolving provenance for metadata file                       0.0s
     => CACHED [frontend 2/5] WORKDIR /app                                     0.0s
     => CACHED [frontend 3/5] COPY package.json package-lock.json* ./          0.0s
     => CACHED [frontend 4/5] RUN npm ci                                       0.0s
     => [frontend 5/5] COPY . .                                                0.5s
    [?25h[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[0G[?25l[+] Building 1.9s (29/32)                                                       
     => [browser] exporting to image                                           0.1s
     => => exporting layers                                                    0.0s
     => => exporting manifest sha256:847eae24267fe1117d23f3e7bb5abb607bcdbbc4  0.0s
     => => exporting config sha256:bc8793160bb32391c252a551894eb1a94dbabdfdd3  0.0s
     => => exporting attestation manifest sha256:527eaadb6fabeaf976589861c443  0.0s
     => => exporting manifest list sha256:ef796cafeb2612f72bdffe9a1457a811287  0.0s
     => => naming to docker.io/library/compose-browser:latest                  0.0s
     => => unpacking to docker.io/library/compose-browser:latest               0.0s
     => [backend internal] load .dockerignore                                  0.0s
     => => transferring context: 2B                                            0.0s
     => [backend 1/5] FROM docker.io/library/python:3.12-slim@sha256:3d5ed973  0.0s
     => => resolve docker.io/library/python:3.12-slim@sha256:3d5ed973e45820f5  0.0s
     => [backend internal] load build context                                  0.0s
     => => transferring context: 9.45kB                                        0.0s
     => CACHED [backend 2/5] WORKDIR /app                                      0.0s
     => [backend 3/5] COPY requirements.txt .                                  0.0s
     => [backend 4/5] RUN pip install --no-cache-dir -r requirements.txt       0.7s
     => [browser] resolving provenance for metadata file                       0.0s
     => CACHED [frontend 2/5] WORKDIR /app                                     0.0s
     => CACHED [frontend 3/5] COPY package.json package-lock.json* ./          0.0s
     => CACHED [frontend 4/5] RUN npm ci                                       0.0s
     => [frontend 5/5] COPY . .                                                0.6s
    [?25h[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[0G[?25l[+] Building 2.0s (29/32)                                                       
     => [browser] exporting to image                                           0.1s
     => => exporting layers                                                    0.0s
     => => exporting manifest sha256:847eae24267fe1117d23f3e7bb5abb607bcdbbc4  0.0s
     => => exporting config sha256:bc8793160bb32391c252a551894eb1a94dbabdfdd3  0.0s
     => => exporting attestation manifest sha256:527eaadb6fabeaf976589861c443  0.0s
     => => exporting manifest list sha256:ef796cafeb2612f72bdffe9a1457a811287  0.0s
     => => naming to docker.io/library/compose-browser:latest                  0.0s
     => => unpacking to docker.io/library/compose-browser:latest               0.0s
     => [backend internal] load .dockerignore                                  0.0s
     => => transferring context: 2B                                            0.0s
     => [backend 1/5] FROM docker.io/library/python:3.12-slim@sha256:3d5ed973  0.0s
     => => resolve docker.io/library/python:3.12-slim@sha256:3d5ed973e45820f5  0.0s
     => [backend internal] load build context                                  0.0s
     => => transferring context: 9.45kB                                        0.0s
     => CACHED [backend 2/5] WORKDIR /app                                      0.0s
     => [backend 3/5] COPY requirements.txt .                                  0.0s
     => [backend 4/5] RUN pip install --no-cache-dir -r requirements.txt       0.9s
     => [browser] resolving provenance for metadata file                       0.0s
     => CACHED [frontend 2/5] WORKDIR /app                                     0.0s
     => CACHED [frontend 3/5] COPY package.json package-lock.json* ./          0.0s
     => CACHED [frontend 4/5] RUN npm ci                                       0.0s
     => [frontend 5/5] COPY . .                                                0.8s
    [?25h[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[0G[?25l[+] Building 2.2s (29/32)                                                       
     => [browser] exporting to image                                           0.1s
     => => exporting layers                                                    0.0s
     => => exporting manifest sha256:847eae24267fe1117d23f3e7bb5abb607bcdbbc4  0.0s
     => => exporting config sha256:bc8793160bb32391c252a551894eb1a94dbabdfdd3  0.0s
     => => exporting attestation manifest sha256:527eaadb6fabeaf976589861c443  0.0s
     => => exporting manifest list sha256:ef796cafeb2612f72bdffe9a1457a811287  0.0s
     => => naming to docker.io/library/compose-browser:latest                  0.0s
     => => unpacking to docker.io/library/compose-browser:latest               0.0s
     => [backend internal] load .dockerignore                                  0.0s
     => => transferring context: 2B                                            0.0s
     => [backend 1/5] FROM docker.io/library/python:3.12-slim@sha256:3d5ed973  0.0s
     => => resolve docker.io/library/python:3.12-slim@sha256:3d5ed973e45820f5  0.0s
     => [backend internal] load build context                                  0.0s
     => => transferring context: 9.45kB                                        0.0s
     => CACHED [backend 2/5] WORKDIR /app                                      0.0s
     => [backend 3/5] COPY requirements.txt .                                  0.0s
     => [backend 4/5] RUN pip install --no-cache-dir -r requirements.txt       1.0s
     => [browser] resolving provenance for metadata file                       0.0s
     => CACHED [frontend 2/5] WORKDIR /app                                     0.0s
     => CACHED [frontend 3/5] COPY package.json package-lock.json* ./          0.0s
     => CACHED [frontend 4/5] RUN npm ci                                       0.0s
     => [frontend 5/5] COPY . .                                                0.9s
    [?25h[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[0G[?25l[+] Building 2.3s (29/32)                                                       
     => [browser] exporting to image                                           0.1s
     => => exporting layers                                                    0.0s
     => => exporting manifest sha256:847eae24267fe1117d23f3e7bb5abb607bcdbbc4  0.0s
     => => exporting config sha256:bc8793160bb32391c252a551894eb1a94dbabdfdd3  0.0s
     => => exporting attestation manifest sha256:527eaadb6fabeaf976589861c443  0.0s
     => => exporting manifest list sha256:ef796cafeb2612f72bdffe9a1457a811287  0.0s
     => => naming to docker.io/library/compose-browser:latest                  0.0s
     => => unpacking to docker.io/library/compose-browser:latest               0.0s
     => [backend internal] load .dockerignore                                  0.0s
     => => transferring context: 2B                                            0.0s
     => [backend 1/5] FROM docker.io/library/python:3.12-slim@sha256:3d5ed973  0.0s
     => => resolve docker.io/library/python:3.12-slim@sha256:3d5ed973e45820f5  0.0s
     => [backend internal] load build context                                  0.0s
     => => transferring context: 9.45kB                                        0.0s
     => CACHED [backend 2/5] WORKDIR /app                                      0.0s
     => [backend 3/5] COPY requirements.txt .                                  0.0s
     => [backend 4/5] RUN pip install --no-cache-dir -r requirements.txt       1.2s
     => [browser] resolving provenance for metadata file                       0.0s
     => CACHED [frontend 2/5] WORKDIR /app                                     0.0s
     => CACHED [frontend 3/5] COPY package.json package-lock.json* ./          0.0s
     => CACHED [frontend 4/5] RUN npm ci                                       0.0s
     => [frontend 5/5] COPY . .                                                1.1s
    [?25h[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[0G[?25l[+] Building 2.4s (29/32)                                                       
     => => exporting layers                                                    0.0s
     => => exporting manifest sha256:847eae24267fe1117d23f3e7bb5abb607bcdbbc4  0.0s
     => => exporting config sha256:bc8793160bb32391c252a551894eb1a94dbabdfdd3  0.0s
     => => exporting attestation manifest sha256:527eaadb6fabeaf976589861c443  0.0s
     => => exporting manifest list sha256:ef796cafeb2612f72bdffe9a1457a811287  0.0s
     => => naming to docker.io/library/compose-browser:latest                  0.0s
     => => unpacking to docker.io/library/compose-browser:latest               0.0s
     => [backend internal] load .dockerignore                                  0.0s
     => => transferring context: 2B                                            0.0s
     => [backend 1/5] FROM docker.io/library/python:3.12-slim@sha256:3d5ed973  0.0s
     => => resolve docker.io/library/python:3.12-slim@sha256:3d5ed973e45820f5  0.0s
     => [backend internal] load build context                                  0.0s
     => => transferring context: 9.45kB                                        0.0s
     => CACHED [backend 2/5] WORKDIR /app                                      0.0s
     => [backend 3/5] COPY requirements.txt .                                  0.0s
     => [backend 4/5] RUN pip install --no-cache-dir -r requirements.txt       1.3s
    [2m => => # Collecting fastapi==0.116.1 (from -r requirements.txt (line 1))       
    [0m => [browser] resolving provenance for metadata file                       0.0s
     => CACHED [frontend 2/5] WORKDIR /app                                     0.0s
     => CACHED [frontend 3/5] COPY package.json package-lock.json* ./          0.0s
     => CACHED [frontend 4/5] RUN npm ci                                       0.0s
     => [frontend 5/5] COPY . .                                                1.2s
    [?25h[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[0G[?25l[+] Building 2.6s (29/32)                                                       
     => => exporting config sha256:bc8793160bb32391c252a551894eb1a94dbabdfdd3  0.0s
     => => exporting attestation manifest sha256:527eaadb6fabeaf976589861c443  0.0s
     => => exporting manifest list sha256:ef796cafeb2612f72bdffe9a1457a811287  0.0s
     => => naming to docker.io/library/compose-browser:latest                  0.0s
     => => unpacking to docker.io/library/compose-browser:latest               0.0s
     => [backend internal] load .dockerignore                                  0.0s
     => => transferring context: 2B                                            0.0s
     => [backend 1/5] FROM docker.io/library/python:3.12-slim@sha256:3d5ed973  0.0s
     => => resolve docker.io/library/python:3.12-slim@sha256:3d5ed973e45820f5  0.0s
     => [backend internal] load build context                                  0.0s
     => => transferring context: 9.45kB                                        0.0s
     => CACHED [backend 2/5] WORKDIR /app                                      0.0s
     => [backend 3/5] COPY requirements.txt .                                  0.0s
     => [backend 4/5] RUN pip install --no-cache-dir -r requirements.txt       1.4s
    [2m => => # Collecting fastapi==0.116.1 (from -r requirements.txt (line 1))       
    [0m[2m => => #   Downloading fastapi-0.116.1-py3-none-any.whl.metadata (28 kB)       
    [0m[2m => => # Collecting httpx==0.28.1 (from -r requirements.txt (line 2))          
    [0m => [browser] resolving provenance for metadata file                       0.0s
     => CACHED [frontend 2/5] WORKDIR /app                                     0.0s
     => CACHED [frontend 3/5] COPY package.json package-lock.json* ./          0.0s
     => CACHED [frontend 4/5] RUN npm ci                                       0.0s
     => [frontend 5/5] COPY . .                                                1.3s
    [?25h[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[0G[?25l[+] Building 2.7s (29/32)                                                       
     => => naming to docker.io/library/compose-browser:latest                  0.0s
     => => unpacking to docker.io/library/compose-browser:latest               0.0s
     => [backend internal] load .dockerignore                                  0.0s
     => => transferring context: 2B                                            0.0s
     => [backend 1/5] FROM docker.io/library/python:3.12-slim@sha256:3d5ed973  0.0s
     => => resolve docker.io/library/python:3.12-slim@sha256:3d5ed973e45820f5  0.0s
     => [backend internal] load build context                                  0.0s
     => => transferring context: 9.45kB                                        0.0s
     => CACHED [backend 2/5] WORKDIR /app                                      0.0s
     => [backend 3/5] COPY requirements.txt .                                  0.0s
     => [backend 4/5] RUN pip install --no-cache-dir -r requirements.txt       1.6s
    [2m => => # Collecting httpx==0.28.1 (from -r requirements.txt (line 2))          
    [0m[2m => => #   Downloading httpx-0.28.1-py3-none-any.whl.metadata (7.1 kB)         
    [0m[2m => => # Collecting pytest==8.4.2 (from -r requirements.txt (line 3))          
    [0m[2m => => #   Downloading pytest-8.4.2-py3-none-any.whl.metadata (7.7 kB)         
    [0m[2m => => # Collecting uvicorn==0.35.0 (from uvicorn[standard]==0.35.0->-r require
    [0m[2m => => # ments.txt (line 4))                                                   
    [0m => [browser] resolving provenance for metadata file                       0.0s
     => CACHED [frontend 2/5] WORKDIR /app                                     0.0s
     => CACHED [frontend 3/5] COPY package.json package-lock.json* ./          0.0s
     => CACHED [frontend 4/5] RUN npm ci                                       0.0s
     => [frontend 5/5] COPY . .                                                1.4s
    [?25h[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[0G[?25l[+] Building 2.9s (30/32)                                                       
     => => naming to docker.io/library/compose-browser:latest                  0.0s
     => => unpacking to docker.io/library/compose-browser:latest               0.0s
     => [backend internal] load .dockerignore                                  0.0s
     => => transferring context: 2B                                            0.0s
     => [backend 1/5] FROM docker.io/library/python:3.12-slim@sha256:3d5ed973  0.0s
     => => resolve docker.io/library/python:3.12-slim@sha256:3d5ed973e45820f5  0.0s
     => [backend internal] load build context                                  0.0s
     => => transferring context: 9.45kB                                        0.0s
     => CACHED [backend 2/5] WORKDIR /app                                      0.0s
     => [backend 3/5] COPY requirements.txt .                                  0.0s
     => [backend 4/5] RUN pip install --no-cache-dir -r requirements.txt       1.7s
    [2m => => # Collecting uvicorn==0.35.0 (from uvicorn[standard]==0.35.0->-r require
    [0m[2m => => # ments.txt (line 4))                                                   
    [0m[2m => => #   Downloading uvicorn-0.35.0-py3-none-any.whl.metadata (6.5 kB)       
    [0m[2m => => # Collecting starlette<0.48.0,>=0.40.0 (from fastapi==0.116.1->-r requir
    [0m[2m => => # ements.txt (line 1))                                                  
    [0m[2m => => #   Downloading starlette-0.47.3-py3-none-any.whl.metadata (6.2 kB)     
    [0m => [browser] resolving provenance for metadata file                       0.0s
     => CACHED [frontend 2/5] WORKDIR /app                                     0.0s
     => CACHED [frontend 3/5] COPY package.json package-lock.json* ./          0.0s
     => CACHED [frontend 4/5] RUN npm ci                                       0.0s
     => [frontend 5/5] COPY . .                                                1.6s
    [?25h[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[0G[?25l[+] Building 3.0s (30/33)                                                       
     => [backend internal] load .dockerignore                                  0.0s
     => => transferring context: 2B                                            0.0s
     => [backend 1/5] FROM docker.io/library/python:3.12-slim@sha256:3d5ed973  0.0s
     => => resolve docker.io/library/python:3.12-slim@sha256:3d5ed973e45820f5  0.0s
     => [backend internal] load build context                                  0.0s
     => => transferring context: 9.45kB                                        0.0s
     => CACHED [backend 2/5] WORKDIR /app                                      0.0s
     => [backend 3/5] COPY requirements.txt .                                  0.0s
     => [backend 4/5] RUN pip install --no-cache-dir -r requirements.txt       1.9s
    [2m => => #   Downloading starlette-0.47.3-py3-none-any.whl.metadata (6.2 kB)     
    [0m[2m => => # Collecting pydantic!=1.8,!=1.8.1,!=2.0.0,!=2.0.1,!=2.1.0,<3.0.0,>=1.7.
    [0m[2m => => # 4 (from fastapi==0.116.1->-r requirements.txt (line 1))               
    [0m[2m => => #   Downloading pydantic-2.12.5-py3-none-any.whl.metadata (90 kB)       
    [0m[2m => => # Collecting typing-extensions>=4.8.0 (from fastapi==0.116.1->-r require
    [0m[2m => => # ments.txt (line 1))                                                   
    [0m => [browser] resolving provenance for metadata file                       0.0s
     => CACHED [frontend 2/5] WORKDIR /app                                     0.0s
     => CACHED [frontend 3/5] COPY package.json package-lock.json* ./          0.0s
     => CACHED [frontend 4/5] RUN npm ci                                       0.0s
     => [frontend 5/5] COPY . .                                                1.6s
     => [frontend] exporting to image                                          0.2s
     => => exporting layers                                                    0.2s
    [?25h[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[0G[?25l[+] Building 3.1s (30/33)                                                       
     => [backend internal] load .dockerignore                                  0.0s
     => => transferring context: 2B                                            0.0s
     => [backend 1/5] FROM docker.io/library/python:3.12-slim@sha256:3d5ed973  0.0s
     => => resolve docker.io/library/python:3.12-slim@sha256:3d5ed973e45820f5  0.0s
     => [backend internal] load build context                                  0.0s
     => => transferring context: 9.45kB                                        0.0s
     => CACHED [backend 2/5] WORKDIR /app                                      0.0s
     => [backend 3/5] COPY requirements.txt .                                  0.0s
     => [backend 4/5] RUN pip install --no-cache-dir -r requirements.txt       2.0s
    [2m => => # ments.txt (line 1))                                                   
    [0m[2m => => #   Downloading typing_extensions-4.15.0-py3-none-any.whl.metadata (3.3 
    [0m[2m => => # kB)                                                                   
    [0m[2m => => # Collecting anyio (from httpx==0.28.1->-r requirements.txt (line 2))   
    [0m[2m => => #   Downloading anyio-4.13.0-py3-none-any.whl.metadata (4.5 kB)         
    [0m[2m => => # Collecting certifi (from httpx==0.28.1->-r requirements.txt (line 2)) 
    [0m => [browser] resolving provenance for metadata file                       0.0s
     => CACHED [frontend 2/5] WORKDIR /app                                     0.0s
     => CACHED [frontend 3/5] COPY package.json package-lock.json* ./          0.0s
     => CACHED [frontend 4/5] RUN npm ci                                       0.0s
     => [frontend 5/5] COPY . .                                                1.6s
     => [frontend] exporting to image                                          0.3s
     => => exporting layers                                                    0.3s
    [?25h[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[0G[?25l[+] Building 3.3s (30/33)                                                       
     => [backend internal] load .dockerignore                                  0.0s
     => => transferring context: 2B                                            0.0s
     => [backend 1/5] FROM docker.io/library/python:3.12-slim@sha256:3d5ed973  0.0s
     => => resolve docker.io/library/python:3.12-slim@sha256:3d5ed973e45820f5  0.0s
     => [backend internal] load build context                                  0.0s
     => => transferring context: 9.45kB                                        0.0s
     => CACHED [backend 2/5] WORKDIR /app                                      0.0s
     => [backend 3/5] COPY requirements.txt .                                  0.0s
     => [backend 4/5] RUN pip install --no-cache-dir -r requirements.txt       2.1s
    [2m => => # Collecting certifi (from httpx==0.28.1->-r requirements.txt (line 2)) 
    [0m[2m => => #   Downloading certifi-2026.2.25-py3-none-any.whl.metadata (2.5 kB)    
    [0m[2m => => # Collecting httpcore==1.* (from httpx==0.28.1->-r requirements.txt (lin
    [0m[2m => => # e 2))                                                                 
    [0m[2m => => #   Downloading httpcore-1.0.9-py3-none-any.whl.metadata (21 kB)        
    [0m[2m => => # Collecting idna (from httpx==0.28.1->-r requirements.txt (line 2))    
    [0m => [browser] resolving provenance for metadata file                       0.0s
     => CACHED [frontend 2/5] WORKDIR /app                                     0.0s
     => CACHED [frontend 3/5] COPY package.json package-lock.json* ./          0.0s
     => CACHED [frontend 4/5] RUN npm ci                                       0.0s
     => [frontend 5/5] COPY . .                                                1.6s
     => [frontend] exporting to image                                          0.4s
     => => exporting layers                                                    0.4s
    [?25h[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[0G[?25l[+] Building 3.4s (30/33)                                                       
     => [backend internal] load .dockerignore                                  0.0s
     => => transferring context: 2B                                            0.0s
     => [backend 1/5] FROM docker.io/library/python:3.12-slim@sha256:3d5ed973  0.0s
     => => resolve docker.io/library/python:3.12-slim@sha256:3d5ed973e45820f5  0.0s
     => [backend internal] load build context                                  0.0s
     => => transferring context: 9.45kB                                        0.0s
     => CACHED [backend 2/5] WORKDIR /app                                      0.0s
     => [backend 3/5] COPY requirements.txt .                                  0.0s
     => [backend 4/5] RUN pip install --no-cache-dir -r requirements.txt       2.2s
    [2m => => #   Downloading idna-3.11-py3-none-any.whl.metadata (8.4 kB)            
    [0m[2m => => # Collecting iniconfig>=1 (from pytest==8.4.2->-r requirements.txt (line
    [0m[2m => => #  3))                                                                  
    [0m[2m => => #   Downloading iniconfig-2.3.0-py3-none-any.whl.metadata (2.5 kB)      
    [0m[2m => => # Collecting packaging>=20 (from pytest==8.4.2->-r requirements.txt (lin
    [0m[2m => => # e 3))                                                                 
    [0m => [browser] resolving provenance for metadata file                       0.0s
     => CACHED [frontend 2/5] WORKDIR /app                                     0.0s
     => CACHED [frontend 3/5] COPY package.json package-lock.json* ./          0.0s
     => CACHED [frontend 4/5] RUN npm ci                                       0.0s
     => [frontend 5/5] COPY . .                                                1.6s
     => [frontend] exporting to image                                          0.5s
     => => exporting layers                                                    0.5s
    [?25h[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[0G[?25l[+] Building 3.5s (30/33)                                                       
     => [backend internal] load .dockerignore                                  0.0s
     => => transferring context: 2B                                            0.0s
     => [backend 1/5] FROM docker.io/library/python:3.12-slim@sha256:3d5ed973  0.0s
     => => resolve docker.io/library/python:3.12-slim@sha256:3d5ed973e45820f5  0.0s
     => [backend internal] load build context                                  0.0s
     => => transferring context: 9.45kB                                        0.0s
     => CACHED [backend 2/5] WORKDIR /app                                      0.0s
     => [backend 3/5] COPY requirements.txt .                                  0.0s
     => [backend 4/5] RUN pip install --no-cache-dir -r requirements.txt       2.4s
    [2m => => #   Downloading packaging-26.0-py3-none-any.whl.metadata (3.3 kB)       
    [0m[2m => => # Collecting pluggy<2,>=1.5 (from pytest==8.4.2->-r requirements.txt (li
    [0m[2m => => # ne 3))                                                                
    [0m[2m => => #   Downloading pluggy-1.6.0-py3-none-any.whl.metadata (4.8 kB)         
    [0m[2m => => # Collecting pygments>=2.7.2 (from pytest==8.4.2->-r requirements.txt (l
    [0m[2m => => # ine 3))                                                               
    [0m => [browser] resolving provenance for metadata file                       0.0s
     => CACHED [frontend 2/5] WORKDIR /app                                     0.0s
     => CACHED [frontend 3/5] COPY package.json package-lock.json* ./          0.0s
     => CACHED [frontend 4/5] RUN npm ci                                       0.0s
     => [frontend 5/5] COPY . .                                                1.6s
     => [frontend] exporting to image                                          0.6s
     => => exporting layers                                                    0.6s
    [?25h[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[0G[?25l[+] Building 3.6s (30/33)                                                       
     => [backend internal] load .dockerignore                                  0.0s
     => => transferring context: 2B                                            0.0s
     => [backend 1/5] FROM docker.io/library/python:3.12-slim@sha256:3d5ed973  0.0s
     => => resolve docker.io/library/python:3.12-slim@sha256:3d5ed973e45820f5  0.0s
     => [backend internal] load build context                                  0.0s
     => => transferring context: 9.45kB                                        0.0s
     => CACHED [backend 2/5] WORKDIR /app                                      0.0s
     => [backend 3/5] COPY requirements.txt .                                  0.0s
     => [backend 4/5] RUN pip install --no-cache-dir -r requirements.txt       2.5s
    [2m => => #   Downloading pygments-2.20.0-py3-none-any.whl.metadata (2.5 kB)      
    [0m[2m => => # Collecting click>=7.0 (from uvicorn==0.35.0->uvicorn[standard]==0.35.0
    [0m[2m => => # ->-r requirements.txt (line 4))                                       
    [0m[2m => => #   Downloading click-8.3.1-py3-none-any.whl.metadata (2.6 kB)          
    [0m[2m => => # Collecting h11>=0.8 (from uvicorn==0.35.0->uvicorn[standard]==0.35.0->
    [0m[2m => => # -r requirements.txt (line 4))                                         
    [0m => [browser] resolving provenance for metadata file                       0.0s
     => CACHED [frontend 2/5] WORKDIR /app                                     0.0s
     => CACHED [frontend 3/5] COPY package.json package-lock.json* ./          0.0s
     => CACHED [frontend 4/5] RUN npm ci                                       0.0s
     => [frontend 5/5] COPY . .                                                1.6s
     => [frontend] exporting to image                                          0.7s
     => => exporting layers                                                    0.7s
    [?25h[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[0G[?25l[+] Building 3.7s (30/33)                                                       
     => [backend internal] load .dockerignore                                  0.0s
     => => transferring context: 2B                                            0.0s
     => [backend 1/5] FROM docker.io/library/python:3.12-slim@sha256:3d5ed973  0.0s
     => => resolve docker.io/library/python:3.12-slim@sha256:3d5ed973e45820f5  0.0s
     => [backend internal] load build context                                  0.0s
     => => transferring context: 9.45kB                                        0.0s
     => CACHED [backend 2/5] WORKDIR /app                                      0.0s
     => [backend 3/5] COPY requirements.txt .                                  0.0s
     => [backend 4/5] RUN pip install --no-cache-dir -r requirements.txt       2.6s
    [2m => => # Collecting httptools>=0.6.3 (from uvicorn[standard]==0.35.0->-r requir
    [0m[2m => => # ements.txt (line 4))                                                  
    [0m[2m => => #   Downloading httptools-0.7.1-cp312-cp312-manylinux2014_aarch64.manyli
    [0m[2m => => # nux_2_17_aarch64.manylinux_2_28_aarch64.whl.metadata (3.5 kB)         
    [0m[2m => => # Collecting python-dotenv>=0.13 (from uvicorn[standard]==0.35.0->-r req
    [0m[2m => => # uirements.txt (line 4))                                               
    [0m => [browser] resolving provenance for metadata file                       0.0s
     => CACHED [frontend 2/5] WORKDIR /app                                     0.0s
     => CACHED [frontend 3/5] COPY package.json package-lock.json* ./          0.0s
     => CACHED [frontend 4/5] RUN npm ci                                       0.0s
     => [frontend 5/5] COPY . .                                                1.6s
     => [frontend] exporting to image                                          0.9s
     => => exporting layers                                                    0.9s
    [?25h[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[0G[?25l[+] Building 3.9s (30/33)                                                       
     => [backend internal] load .dockerignore                                  0.0s
     => => transferring context: 2B                                            0.0s
     => [backend 1/5] FROM docker.io/library/python:3.12-slim@sha256:3d5ed973  0.0s
     => => resolve docker.io/library/python:3.12-slim@sha256:3d5ed973e45820f5  0.0s
     => [backend internal] load build context                                  0.0s
     => => transferring context: 9.45kB                                        0.0s
     => CACHED [backend 2/5] WORKDIR /app                                      0.0s
     => [backend 3/5] COPY requirements.txt .                                  0.0s
     => [backend 4/5] RUN pip install --no-cache-dir -r requirements.txt       2.7s
    [2m => => # Collecting pyyaml>=5.1 (from uvicorn[standard]==0.35.0->-r requirement
    [0m[2m => => # s.txt (line 4))                                                       
    [0m[2m => => #   Downloading pyyaml-6.0.3-cp312-cp312-manylinux2014_aarch64.manylinux
    [0m[2m => => # _2_17_aarch64.manylinux_2_28_aarch64.whl.metadata (2.4 kB)            
    [0m[2m => => # Collecting uvloop>=0.15.1 (from uvicorn[standard]==0.35.0->-r requirem
    [0m[2m => => # ents.txt (line 4))                                                    
    [0m => [browser] resolving provenance for metadata file                       0.0s
     => CACHED [frontend 2/5] WORKDIR /app                                     0.0s
     => CACHED [frontend 3/5] COPY package.json package-lock.json* ./          0.0s
     => CACHED [frontend 4/5] RUN npm ci                                       0.0s
     => [frontend 5/5] COPY . .                                                1.6s
     => [frontend] exporting to image                                          1.0s
     => => exporting layers                                                    1.0s
    [?25h[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[0G[?25l[+] Building 4.0s (30/33)                                                       
     => [backend internal] load .dockerignore                                  0.0s
     => => transferring context: 2B                                            0.0s
     => [backend 1/5] FROM docker.io/library/python:3.12-slim@sha256:3d5ed973  0.0s
     => => resolve docker.io/library/python:3.12-slim@sha256:3d5ed973e45820f5  0.0s
     => [backend internal] load build context                                  0.0s
     => => transferring context: 9.45kB                                        0.0s
     => CACHED [backend 2/5] WORKDIR /app                                      0.0s
     => [backend 3/5] COPY requirements.txt .                                  0.0s
     => [backend 4/5] RUN pip install --no-cache-dir -r requirements.txt       2.8s
    [2m => => #   Downloading uvloop-0.22.1-cp312-cp312-manylinux2014_aarch64.manylinu
    [0m[2m => => # x_2_17_aarch64.manylinux_2_28_aarch64.whl.metadata (4.9 kB)           
    [0m[2m => => # Collecting watchfiles>=0.13 (from uvicorn[standard]==0.35.0->-r requir
    [0m[2m => => # ements.txt (line 4))                                                  
    [0m[2m => => #   Downloading watchfiles-1.1.1-cp312-cp312-manylinux_2_17_aarch64.many
    [0m[2m => => # linux2014_aarch64.whl.metadata (4.9 kB)                               
    [0m => [browser] resolving provenance for metadata file                       0.0s
     => CACHED [frontend 2/5] WORKDIR /app                                     0.0s
     => CACHED [frontend 3/5] COPY package.json package-lock.json* ./          0.0s
     => CACHED [frontend 4/5] RUN npm ci                                       0.0s
     => [frontend 5/5] COPY . .                                                1.6s
     => [frontend] exporting to image                                          1.1s
     => => exporting layers                                                    1.1s
    [?25h[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[0G[?25l[+] Building 4.1s (30/33)                                                       
     => [backend internal] load .dockerignore                                  0.0s
     => => transferring context: 2B                                            0.0s
     => [backend 1/5] FROM docker.io/library/python:3.12-slim@sha256:3d5ed973  0.0s
     => => resolve docker.io/library/python:3.12-slim@sha256:3d5ed973e45820f5  0.0s
     => [backend internal] load build context                                  0.0s
     => => transferring context: 9.45kB                                        0.0s
     => CACHED [backend 2/5] WORKDIR /app                                      0.0s
     => [backend 3/5] COPY requirements.txt .                                  0.0s
     => [backend 4/5] RUN pip install --no-cache-dir -r requirements.txt       2.9s
    [2m => => #   Downloading watchfiles-1.1.1-cp312-cp312-manylinux_2_17_aarch64.many
    [0m[2m => => # linux2014_aarch64.whl.metadata (4.9 kB)                               
    [0m[2m => => # Collecting websockets>=10.4 (from uvicorn[standard]==0.35.0->-r requir
    [0m[2m => => # ements.txt (line 4))                                                  
    [0m[2m => => #   Downloading websockets-16.0-cp312-cp312-manylinux2014_aarch64.manyli
    [0m[2m => => # nux_2_17_aarch64.manylinux_2_28_aarch64.whl.metadata (6.8 kB)         
    [0m => [browser] resolving provenance for metadata file                       0.0s
     => CACHED [frontend 2/5] WORKDIR /app                                     0.0s
     => CACHED [frontend 3/5] COPY package.json package-lock.json* ./          0.0s
     => CACHED [frontend 4/5] RUN npm ci                                       0.0s
     => [frontend 5/5] COPY . .                                                1.6s
     => [frontend] exporting to image                                          1.2s
     => => exporting layers                                                    1.2s
    [?25h[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[0G[?25l[+] Building 4.3s (30/33)                                                       
     => [backend internal] load .dockerignore                                  0.0s
     => => transferring context: 2B                                            0.0s
     => [backend 1/5] FROM docker.io/library/python:3.12-slim@sha256:3d5ed973  0.0s
     => => resolve docker.io/library/python:3.12-slim@sha256:3d5ed973e45820f5  0.0s
     => [backend internal] load build context                                  0.0s
     => => transferring context: 9.45kB                                        0.0s
     => CACHED [backend 2/5] WORKDIR /app                                      0.0s
     => [backend 3/5] COPY requirements.txt .                                  0.0s
     => [backend 4/5] RUN pip install --no-cache-dir -r requirements.txt       3.2s
    [2m => => #   Downloading websockets-16.0-cp312-cp312-manylinux2014_aarch64.manyli
    [0m[2m => => # nux_2_17_aarch64.manylinux_2_28_aarch64.whl.metadata (6.8 kB)         
    [0m[2m => => # Collecting annotated-types>=0.6.0 (from pydantic!=1.8,!=1.8.1,!=2.0.0,
    [0m[2m => => # !=2.0.1,!=2.1.0,<3.0.0,>=1.7.4->fastapi==0.116.1->-r requirements.txt 
    [0m[2m => => # (line 1))                                                             
    [0m[2m => => #   Downloading annotated_types-0.7.0-py3-none-any.whl.metadata (15 kB) 
    [0m => [browser] resolving provenance for metadata file                       0.0s
     => CACHED [frontend 2/5] WORKDIR /app                                     0.0s
     => CACHED [frontend 3/5] COPY package.json package-lock.json* ./          0.0s
     => CACHED [frontend 4/5] RUN npm ci                                       0.0s
     => [frontend 5/5] COPY . .                                                1.6s
     => [frontend] exporting to image                                          1.4s
     => => exporting layers                                                    1.4s
    [?25h[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[0G[?25l[+] Building 4.4s (30/33)                                                       
     => [backend internal] load .dockerignore                                  0.0s
     => => transferring context: 2B                                            0.0s
     => [backend 1/5] FROM docker.io/library/python:3.12-slim@sha256:3d5ed973  0.0s
     => => resolve docker.io/library/python:3.12-slim@sha256:3d5ed973e45820f5  0.0s
     => [backend internal] load build context                                  0.0s
     => => transferring context: 9.45kB                                        0.0s
     => CACHED [backend 2/5] WORKDIR /app                                      0.0s
     => [backend 3/5] COPY requirements.txt .                                  0.0s
     => [backend 4/5] RUN pip install --no-cache-dir -r requirements.txt       3.3s
    [2m => => #   Downloading websockets-16.0-cp312-cp312-manylinux2014_aarch64.manyli
    [0m[2m => => # nux_2_17_aarch64.manylinux_2_28_aarch64.whl.metadata (6.8 kB)         
    [0m[2m => => # Collecting annotated-types>=0.6.0 (from pydantic!=1.8,!=1.8.1,!=2.0.0,
    [0m[2m => => # !=2.0.1,!=2.1.0,<3.0.0,>=1.7.4->fastapi==0.116.1->-r requirements.txt 
    [0m[2m => => # (line 1))                                                             
    [0m[2m => => #   Downloading annotated_types-0.7.0-py3-none-any.whl.metadata (15 kB) 
    [0m => [browser] resolving provenance for metadata file                       0.0s
     => CACHED [frontend 2/5] WORKDIR /app                                     0.0s
     => CACHED [frontend 3/5] COPY package.json package-lock.json* ./          0.0s
     => CACHED [frontend 4/5] RUN npm ci                                       0.0s
     => [frontend 5/5] COPY . .                                                1.6s
     => [frontend] exporting to image                                          1.6s
     => => exporting layers                                                    1.6s
    [?25h[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[0G[?25l[+] Building 4.5s (30/33)                                                       
     => [backend internal] load .dockerignore                                  0.0s
     => => transferring context: 2B                                            0.0s
     => [backend 1/5] FROM docker.io/library/python:3.12-slim@sha256:3d5ed973  0.0s
     => => resolve docker.io/library/python:3.12-slim@sha256:3d5ed973e45820f5  0.0s
     => [backend internal] load build context                                  0.0s
     => => transferring context: 9.45kB                                        0.0s
     => CACHED [backend 2/5] WORKDIR /app                                      0.0s
     => [backend 3/5] COPY requirements.txt .                                  0.0s
     => [backend 4/5] RUN pip install --no-cache-dir -r requirements.txt       3.3s
    [2m => => # !=2.0.1,!=2.1.0,<3.0.0,>=1.7.4->fastapi==0.116.1->-r requirements.txt 
    [0m[2m => => # (line 1))                                                             
    [0m[2m => => #   Downloading annotated_types-0.7.0-py3-none-any.whl.metadata (15 kB) 
    [0m[2m => => # Collecting pydantic-core==2.41.5 (from pydantic!=1.8,!=1.8.1,!=2.0.0,!
    [0m[2m => => # =2.0.1,!=2.1.0,<3.0.0,>=1.7.4->fastapi==0.116.1->-r requirements.txt (
    [0m[2m => => # line 1))                                                              
    [0m => [browser] resolving provenance for metadata file                       0.0s
     => CACHED [frontend 2/5] WORKDIR /app                                     0.0s
     => CACHED [frontend 3/5] COPY package.json package-lock.json* ./          0.0s
     => CACHED [frontend 4/5] RUN npm ci                                       0.0s
     => [frontend 5/5] COPY . .                                                1.6s
     => [frontend] exporting to image                                          1.6s
     => => exporting layers                                                    1.6s
    [?25h[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[0G[?25l[+] Building 4.6s (30/33)                                                       
     => [backend internal] load .dockerignore                                  0.0s
     => => transferring context: 2B                                            0.0s
     => [backend 1/5] FROM docker.io/library/python:3.12-slim@sha256:3d5ed973  0.0s
     => => resolve docker.io/library/python:3.12-slim@sha256:3d5ed973e45820f5  0.0s
     => [backend internal] load build context                                  0.0s
     => => transferring context: 9.45kB                                        0.0s
     => CACHED [backend 2/5] WORKDIR /app                                      0.0s
     => [backend 3/5] COPY requirements.txt .                                  0.0s
     => [backend 4/5] RUN pip install --no-cache-dir -r requirements.txt       3.4s
    [2m => => # Collecting typing-inspection>=0.4.2 (from pydantic!=1.8,!=1.8.1,!=2.0.
    [0m[2m => => # 0,!=2.0.1,!=2.1.0,<3.0.0,>=1.7.4->fastapi==0.116.1->-r requirements.tx
    [0m[2m => => # t (line 1))                                                           
    [0m[2m => => #   Downloading typing_inspection-0.4.2-py3-none-any.whl.metadata (2.6 k
    [0m[2m => => # B)                                                                    
    [0m[2m => => # Downloading fastapi-0.116.1-py3-none-any.whl (95 kB)                  
    [0m => [browser] resolving provenance for metadata file                       0.0s
     => CACHED [frontend 2/5] WORKDIR /app                                     0.0s
     => CACHED [frontend 3/5] COPY package.json package-lock.json* ./          0.0s
     => CACHED [frontend 4/5] RUN npm ci                                       0.0s
     => [frontend 5/5] COPY . .                                                1.6s
     => [frontend] exporting to image                                          1.7s
     => => exporting layers                                                    1.7s
    [?25h[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[0G[?25l[+] Building 4.7s (30/33)                                                       
     => [backend internal] load .dockerignore                                  0.0s
     => => transferring context: 2B                                            0.0s
     => [backend 1/5] FROM docker.io/library/python:3.12-slim@sha256:3d5ed973  0.0s
     => => resolve docker.io/library/python:3.12-slim@sha256:3d5ed973e45820f5  0.0s
     => [backend internal] load build context                                  0.0s
     => => transferring context: 9.45kB                                        0.0s
     => CACHED [backend 2/5] WORKDIR /app                                      0.0s
     => [backend 3/5] COPY requirements.txt .                                  0.0s
     => [backend 4/5] RUN pip install --no-cache-dir -r requirements.txt       3.6s
    [2m => => #   Downloading typing_inspection-0.4.2-py3-none-any.whl.metadata (2.6 k
    [0m[2m => => # B)                                                                    
    [0m[2m => => # Downloading fastapi-0.116.1-py3-none-any.whl (95 kB)                  
    [0m[2m => => # Downloading httpx-0.28.1-py3-none-any.whl (73 kB)                     
    [0m[2m => => # Downloading pytest-8.4.2-py3-none-any.whl (365 kB)                    
    [0m[2m => => # Downloading uvicorn-0.35.0-py3-none-any.whl (66 kB)                   
    [0m => [browser] resolving provenance for metadata file                       0.0s
     => CACHED [frontend 2/5] WORKDIR /app                                     0.0s
     => CACHED [frontend 3/5] COPY package.json package-lock.json* ./          0.0s
     => CACHED [frontend 4/5] RUN npm ci                                       0.0s
     => [frontend 5/5] COPY . .                                                1.6s
     => [frontend] exporting to image                                          1.9s
     => => exporting layers                                                    1.9s
    [?25h[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[0G[?25l[+] Building 4.8s (30/33)                                                       
     => [backend internal] load .dockerignore                                  0.0s
     => => transferring context: 2B                                            0.0s
     => [backend 1/5] FROM docker.io/library/python:3.12-slim@sha256:3d5ed973  0.0s
     => => resolve docker.io/library/python:3.12-slim@sha256:3d5ed973e45820f5  0.0s
     => [backend internal] load build context                                  0.0s
     => => transferring context: 9.45kB                                        0.0s
     => CACHED [backend 2/5] WORKDIR /app                                      0.0s
     => [backend 3/5] COPY requirements.txt .                                  0.0s
     => [backend 4/5] RUN pip install --no-cache-dir -r requirements.txt       3.7s
    [2m => => # Downloading httpx-0.28.1-py3-none-any.whl (73 kB)                     
    [0m[2m => => # Downloading pytest-8.4.2-py3-none-any.whl (365 kB)                    
    [0m[2m => => # Downloading uvicorn-0.35.0-py3-none-any.whl (66 kB)                   
    [0m[2m => => # Downloading httpcore-1.0.9-py3-none-any.whl (78 kB)                   
    [0m[2m => => # Downloading click-8.3.1-py3-none-any.whl (108 kB)                     
    [0m[2m => => # Downloading h11-0.16.0-py3-none-any.whl (37 kB)                       
    [0m => [browser] resolving provenance for metadata file                       0.0s
     => CACHED [frontend 2/5] WORKDIR /app                                     0.0s
     => CACHED [frontend 3/5] COPY package.json package-lock.json* ./          0.0s
     => CACHED [frontend 4/5] RUN npm ci                                       0.0s
     => [frontend 5/5] COPY . .                                                1.6s
     => [frontend] exporting to image                                          2.0s
     => => exporting layers                                                    2.0s
    [?25h[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[0G[?25l[+] Building 5.0s (30/33)                                                       
     => [backend internal] load .dockerignore                                  0.0s
     => => transferring context: 2B                                            0.0s
     => [backend 1/5] FROM docker.io/library/python:3.12-slim@sha256:3d5ed973  0.0s
     => => resolve docker.io/library/python:3.12-slim@sha256:3d5ed973e45820f5  0.0s
     => [backend internal] load build context                                  0.0s
     => => transferring context: 9.45kB                                        0.0s
     => CACHED [backend 2/5] WORKDIR /app                                      0.0s
     => [backend 3/5] COPY requirements.txt .                                  0.0s
     => [backend 4/5] RUN pip install --no-cache-dir -r requirements.txt       3.9s
    [2m => => # Downloading uvicorn-0.35.0-py3-none-any.whl (66 kB)                   
    [0m[2m => => # Downloading httpcore-1.0.9-py3-none-any.whl (78 kB)                   
    [0m[2m => => # Downloading click-8.3.1-py3-none-any.whl (108 kB)                     
    [0m[2m => => # Downloading h11-0.16.0-py3-none-any.whl (37 kB)                       
    [0m[2m => => # Downloading httptools-0.7.1-cp312-cp312-manylinux2014_aarch64.manylinu
    [0m[2m => => # x_2_17_aarch64.manylinux_2_28_aarch64.whl (511 kB)                    
    [0m => [browser] resolving provenance for metadata file                       0.0s
     => CACHED [frontend 2/5] WORKDIR /app                                     0.0s
     => CACHED [frontend 3/5] COPY package.json package-lock.json* ./          0.0s
     => CACHED [frontend 4/5] RUN npm ci                                       0.0s
     => [frontend 5/5] COPY . .                                                1.6s
     => [frontend] exporting to image                                          2.2s
     => => exporting layers                                                    2.2s
    [?25h[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[0G[?25l[+] Building 5.1s (30/33)                                                       
     => [backend internal] load .dockerignore                                  0.0s
     => => transferring context: 2B                                            0.0s
     => [backend 1/5] FROM docker.io/library/python:3.12-slim@sha256:3d5ed973  0.0s
     => => resolve docker.io/library/python:3.12-slim@sha256:3d5ed973e45820f5  0.0s
     => [backend internal] load build context                                  0.0s
     => => transferring context: 9.45kB                                        0.0s
     => CACHED [backend 2/5] WORKDIR /app                                      0.0s
     => [backend 3/5] COPY requirements.txt .                                  0.0s
     => [backend 4/5] RUN pip install --no-cache-dir -r requirements.txt       3.9s
    [2m => => # Downloading httpcore-1.0.9-py3-none-any.whl (78 kB)                   
    [0m[2m => => # Downloading click-8.3.1-py3-none-any.whl (108 kB)                     
    [0m[2m => => # Downloading h11-0.16.0-py3-none-any.whl (37 kB)                       
    [0m[2m => => # Downloading httptools-0.7.1-cp312-cp312-manylinux2014_aarch64.manylinu
    [0m[2m => => # x_2_17_aarch64.manylinux_2_28_aarch64.whl (511 kB)                    
    [0m[2m => => # Downloading iniconfig-2.3.0-py3-none-any.whl (7.5 kB)                 
    [0m => [browser] resolving provenance for metadata file                       0.0s
     => CACHED [frontend 2/5] WORKDIR /app                                     0.0s
     => CACHED [frontend 3/5] COPY package.json package-lock.json* ./          0.0s
     => CACHED [frontend 4/5] RUN npm ci                                       0.0s
     => [frontend 5/5] COPY . .                                                1.6s
     => [frontend] exporting to image                                          2.2s
     => => exporting layers                                                    2.2s
    [?25h[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[0G[?25l[+] Building 5.2s (30/33)                                                       
     => [backend internal] load .dockerignore                                  0.0s
     => => transferring context: 2B                                            0.0s
     => [backend 1/5] FROM docker.io/library/python:3.12-slim@sha256:3d5ed973  0.0s
     => => resolve docker.io/library/python:3.12-slim@sha256:3d5ed973e45820f5  0.0s
     => [backend internal] load build context                                  0.0s
     => => transferring context: 9.45kB                                        0.0s
     => CACHED [backend 2/5] WORKDIR /app                                      0.0s
     => [backend 3/5] COPY requirements.txt .                                  0.0s
     => [backend 4/5] RUN pip install --no-cache-dir -r requirements.txt       4.0s
    [2m => => # Downloading h11-0.16.0-py3-none-any.whl (37 kB)                       
    [0m[2m => => # Downloading httptools-0.7.1-cp312-cp312-manylinux2014_aarch64.manylinu
    [0m[2m => => # x_2_17_aarch64.manylinux_2_28_aarch64.whl (511 kB)                    
    [0m[2m => => # Downloading iniconfig-2.3.0-py3-none-any.whl (7.5 kB)                 
    [0m[2m => => # Downloading packaging-26.0-py3-none-any.whl (74 kB)                   
    [0m[2m => => # Downloading pluggy-1.6.0-py3-none-any.whl (20 kB)                     
    [0m => [browser] resolving provenance for metadata file                       0.0s
     => CACHED [frontend 2/5] WORKDIR /app                                     0.0s
     => CACHED [frontend 3/5] COPY package.json package-lock.json* ./          0.0s
     => CACHED [frontend 4/5] RUN npm ci                                       0.0s
     => [frontend 5/5] COPY . .                                                1.6s
     => [frontend] exporting to image                                          2.3s
     => => exporting layers                                                    2.3s
    [?25h[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[0G[?25l[+] Building 5.3s (30/33)                                                       
     => [backend internal] load .dockerignore                                  0.0s
     => => transferring context: 2B                                            0.0s
     => [backend 1/5] FROM docker.io/library/python:3.12-slim@sha256:3d5ed973  0.0s
     => => resolve docker.io/library/python:3.12-slim@sha256:3d5ed973e45820f5  0.0s
     => [backend internal] load build context                                  0.0s
     => => transferring context: 9.45kB                                        0.0s
     => CACHED [backend 2/5] WORKDIR /app                                      0.0s
     => [backend 3/5] COPY requirements.txt .                                  0.0s
     => [backend 4/5] RUN pip install --no-cache-dir -r requirements.txt       4.2s
    [2m => => # Downloading iniconfig-2.3.0-py3-none-any.whl (7.5 kB)                 
    [0m[2m => => # Downloading packaging-26.0-py3-none-any.whl (74 kB)                   
    [0m[2m => => # Downloading pluggy-1.6.0-py3-none-any.whl (20 kB)                     
    [0m[2m => => # Downloading pydantic-2.12.5-py3-none-any.whl (463 kB)                 
    [0m[2m => => # Downloading pydantic_core-2.41.5-cp312-cp312-manylinux_2_17_aarch64.ma
    [0m[2m => => # nylinux2014_aarch64.whl (1.9 MB)                                      
    [0m => [browser] resolving provenance for metadata file                       0.0s
     => CACHED [frontend 2/5] WORKDIR /app                                     0.0s
     => CACHED [frontend 3/5] COPY package.json package-lock.json* ./          0.0s
     => CACHED [frontend 4/5] RUN npm ci                                       0.0s
     => [frontend 5/5] COPY . .                                                1.6s
     => [frontend] exporting to image                                          2.5s
     => => exporting layers                                                    2.5s
    [?25h[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[0G[?25l[+] Building 5.5s (30/33)                                                       
     => [backend 1/5] FROM docker.io/library/python:3.12-slim@sha256:3d5ed973  0.0s
     => => resolve docker.io/library/python:3.12-slim@sha256:3d5ed973e45820f5  0.0s
     => [backend internal] load build context                                  0.0s
     => => transferring context: 9.45kB                                        0.0s
     => CACHED [backend 2/5] WORKDIR /app                                      0.0s
     => [backend 3/5] COPY requirements.txt .                                  0.0s
     => [backend 4/5] RUN pip install --no-cache-dir -r requirements.txt       4.3s
    [2m => => # Downloading iniconfig-2.3.0-py3-none-any.whl (7.5 kB)                 
    [0m[2m => => # Downloading packaging-26.0-py3-none-any.whl (74 kB)                   
    [0m[2m => => # Downloading pluggy-1.6.0-py3-none-any.whl (20 kB)                     
    [0m[2m => => # Downloading pydantic-2.12.5-py3-none-any.whl (463 kB)                 
    [0m[2m => => # Downloading pydantic_core-2.41.5-cp312-cp312-manylinux_2_17_aarch64.ma
    [0m[2m => => # nylinux2014_aarch64.whl (1.9 MB)                                      
    [0m => [browser] resolving provenance for metadata file                       0.0s
     => CACHED [frontend 2/5] WORKDIR /app                                     0.0s
     => CACHED [frontend 3/5] COPY package.json package-lock.json* ./          0.0s
     => CACHED [frontend 4/5] RUN npm ci                                       0.0s
     => [frontend 5/5] COPY . .                                                1.6s
     => [frontend] exporting to image                                          2.6s
     => => exporting layers                                                    2.6s
     => => exporting manifest sha256:5590f5beedb5d595cd6fbc523d956e6b20992436  0.0s
     => => exporting config sha256:658ecac42db2e44d58f45a370df44e07eb944c0984  0.0s
    [?25h[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[0G[?25l[+] Building 5.6s (30/33)                                                       
     => CACHED [backend 2/5] WORKDIR /app                                      0.0s
     => [backend 3/5] COPY requirements.txt .                                  0.0s
     => [backend 4/5] RUN pip install --no-cache-dir -r requirements.txt       4.5s
    [2m => => # Downloading iniconfig-2.3.0-py3-none-any.whl (7.5 kB)                 
    [0m[2m => => # Downloading packaging-26.0-py3-none-any.whl (74 kB)                   
    [0m[2m => => # Downloading pluggy-1.6.0-py3-none-any.whl (20 kB)                     
    [0m[2m => => # Downloading pydantic-2.12.5-py3-none-any.whl (463 kB)                 
    [0m[2m => => # Downloading pydantic_core-2.41.5-cp312-cp312-manylinux_2_17_aarch64.ma
    [0m[2m => => # nylinux2014_aarch64.whl (1.9 MB)                                      
    [0m => [browser] resolving provenance for metadata file                       0.0s
     => CACHED [frontend 2/5] WORKDIR /app                                     0.0s
     => CACHED [frontend 3/5] COPY package.json package-lock.json* ./          0.0s
     => CACHED [frontend 4/5] RUN npm ci                                       0.0s
     => [frontend 5/5] COPY . .                                                1.6s
     => [frontend] exporting to image                                          2.8s
     => => exporting layers                                                    2.6s
     => => exporting manifest sha256:5590f5beedb5d595cd6fbc523d956e6b20992436  0.0s
     => => exporting config sha256:658ecac42db2e44d58f45a370df44e07eb944c0984  0.0s
     => => exporting attestation manifest sha256:26da59865b0be310448478f2f05d  0.0s
     => => exporting manifest list sha256:d095aeb02035e25bbb67b5be219cf439526  0.0s
     => => naming to docker.io/library/compose-frontend:latest                 0.0s
     => => unpacking to docker.io/library/compose-frontend:latest              0.2s
    [?25h[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[0G[?25l[+] Building 5.7s (30/33)                                                       
     => CACHED [backend 2/5] WORKDIR /app                                      0.0s
     => [backend 3/5] COPY requirements.txt .                                  0.0s
     => [backend 4/5] RUN pip install --no-cache-dir -r requirements.txt       4.5s
    [2m => => # Downloading pluggy-1.6.0-py3-none-any.whl (20 kB)                     
    [0m[2m => => # Downloading pydantic-2.12.5-py3-none-any.whl (463 kB)                 
    [0m[2m => => # Downloading pydantic_core-2.41.5-cp312-cp312-manylinux_2_17_aarch64.ma
    [0m[2m => => # nylinux2014_aarch64.whl (1.9 MB)                                      
    [0m[2m => => #    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.9/1.9 MB 6.4 MB/s eta 0:
    [0m[2m => => # 00:00                                                                 
    [0m => [browser] resolving provenance for metadata file                       0.0s
     => CACHED [frontend 2/5] WORKDIR /app                                     0.0s
     => CACHED [frontend 3/5] COPY package.json package-lock.json* ./          0.0s
     => CACHED [frontend 4/5] RUN npm ci                                       0.0s
     => [frontend 5/5] COPY . .                                                1.6s
     => [frontend] exporting to image                                          2.8s
     => => exporting layers                                                    2.6s
     => => exporting manifest sha256:5590f5beedb5d595cd6fbc523d956e6b20992436  0.0s
     => => exporting config sha256:658ecac42db2e44d58f45a370df44e07eb944c0984  0.0s
     => => exporting attestation manifest sha256:26da59865b0be310448478f2f05d  0.0s
     => => exporting manifest list sha256:d095aeb02035e25bbb67b5be219cf439526  0.0s
     => => naming to docker.io/library/compose-frontend:latest                 0.0s
     => => unpacking to docker.io/library/compose-frontend:latest              0.2s
    [?25h[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[0G[?25l[+] Building 5.8s (30/33)                                                       
     => CACHED [backend 2/5] WORKDIR /app                                      0.0s
     => [backend 3/5] COPY requirements.txt .                                  0.0s
     => [backend 4/5] RUN pip install --no-cache-dir -r requirements.txt       4.7s
    [2m => => # Downloading pydantic-2.12.5-py3-none-any.whl (463 kB)                 
    [0m[2m => => # Downloading pydantic_core-2.41.5-cp312-cp312-manylinux_2_17_aarch64.ma
    [0m[2m => => # nylinux2014_aarch64.whl (1.9 MB)                                      
    [0m[2m => => #    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.9/1.9 MB 6.4 MB/s eta 0:
    [0m[2m => => # 00:00                                                                 
    [0m[2m => => # Downloading pygments-2.20.0-py3-none-any.whl (1.2 MB)                 
    [0m => [browser] resolving provenance for metadata file                       0.0s
     => CACHED [frontend 2/5] WORKDIR /app                                     0.0s
     => CACHED [frontend 3/5] COPY package.json package-lock.json* ./          0.0s
     => CACHED [frontend 4/5] RUN npm ci                                       0.0s
     => [frontend 5/5] COPY . .                                                1.6s
     => [frontend] exporting to image                                          3.0s
     => => exporting layers                                                    2.6s
     => => exporting manifest sha256:5590f5beedb5d595cd6fbc523d956e6b20992436  0.0s
     => => exporting config sha256:658ecac42db2e44d58f45a370df44e07eb944c0984  0.0s
     => => exporting attestation manifest sha256:26da59865b0be310448478f2f05d  0.0s
     => => exporting manifest list sha256:d095aeb02035e25bbb67b5be219cf439526  0.0s
     => => naming to docker.io/library/compose-frontend:latest                 0.0s
     => => unpacking to docker.io/library/compose-frontend:latest              0.4s
    [?25h[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[0G[?25l[+] Building 5.9s (30/33)                                                       
     => CACHED [backend 2/5] WORKDIR /app                                      0.0s
     => [backend 3/5] COPY requirements.txt .                                  0.0s
     => [backend 4/5] RUN pip install --no-cache-dir -r requirements.txt       4.7s
    [2m => => # nylinux2014_aarch64.whl (1.9 MB)                                      
    [0m[2m => => #    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.9/1.9 MB 6.4 MB/s eta 0:
    [0m[2m => => # 00:00                                                                 
    [0m[2m => => # Downloading pygments-2.20.0-py3-none-any.whl (1.2 MB)                 
    [0m[2m => => #    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.2/1.2 MB 7.1 MB/s eta 0:
    [0m[2m => => # 00:00                                                                 
    [0m => [browser] resolving provenance for metadata file                       0.0s
     => CACHED [frontend 2/5] WORKDIR /app                                     0.0s
     => CACHED [frontend 3/5] COPY package.json package-lock.json* ./          0.0s
     => CACHED [frontend 4/5] RUN npm ci                                       0.0s
     => [frontend 5/5] COPY . .                                                1.6s
     => [frontend] exporting to image                                          3.0s
     => => exporting layers                                                    2.6s
     => => exporting manifest sha256:5590f5beedb5d595cd6fbc523d956e6b20992436  0.0s
     => => exporting config sha256:658ecac42db2e44d58f45a370df44e07eb944c0984  0.0s
     => => exporting attestation manifest sha256:26da59865b0be310448478f2f05d  0.0s
     => => exporting manifest list sha256:d095aeb02035e25bbb67b5be219cf439526  0.0s
     => => naming to docker.io/library/compose-frontend:latest                 0.0s
     => => unpacking to docker.io/library/compose-frontend:latest              0.4s
    [?25h[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[0G[?25l[+] Building 6.0s (30/33)                                                       
     => CACHED [backend 2/5] WORKDIR /app                                      0.0s
     => [backend 3/5] COPY requirements.txt .                                  0.0s
     => [backend 4/5] RUN pip install --no-cache-dir -r requirements.txt       4.9s
    [2m => => # 00:00                                                                 
    [0m[2m => => # Downloading python_dotenv-1.2.2-py3-none-any.whl (22 kB)              
    [0m[2m => => # Downloading pyyaml-6.0.3-cp312-cp312-manylinux2014_aarch64.manylinux_2
    [0m[2m => => # _17_aarch64.manylinux_2_28_aarch64.whl (775 kB)                       
    [0m[2m => => #    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 775.1/775.1 kB 7.6 MB/s et
    [0m[2m => => # a 0:00:00                                                             
    [0m => [browser] resolving provenance for metadata file                       0.0s
     => CACHED [frontend 2/5] WORKDIR /app                                     0.0s
     => CACHED [frontend 3/5] COPY package.json package-lock.json* ./          0.0s
     => CACHED [frontend 4/5] RUN npm ci                                       0.0s
     => [frontend 5/5] COPY . .                                                1.6s
     => [frontend] exporting to image                                          3.1s
     => => exporting layers                                                    2.6s
     => => exporting manifest sha256:5590f5beedb5d595cd6fbc523d956e6b20992436  0.0s
     => => exporting config sha256:658ecac42db2e44d58f45a370df44e07eb944c0984  0.0s
     => => exporting attestation manifest sha256:26da59865b0be310448478f2f05d  0.0s
     => => exporting manifest list sha256:d095aeb02035e25bbb67b5be219cf439526  0.0s
     => => naming to docker.io/library/compose-frontend:latest                 0.0s
     => => unpacking to docker.io/library/compose-frontend:latest              0.5s
    [?25h[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[0G[?25l[+] Building 6.1s (30/33)                                                       
     => CACHED [backend 2/5] WORKDIR /app                                      0.0s
     => [backend 3/5] COPY requirements.txt .                                  0.0s
     => [backend 4/5] RUN pip install --no-cache-dir -r requirements.txt       5.0s
    [2m => => # _17_aarch64.manylinux_2_28_aarch64.whl (775 kB)                       
    [0m[2m => => #    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 775.1/775.1 kB 7.6 MB/s et
    [0m[2m => => # a 0:00:00                                                             
    [0m[2m => => # Downloading starlette-0.47.3-py3-none-any.whl (72 kB)                 
    [0m[2m => => # Downloading anyio-4.13.0-py3-none-any.whl (114 kB)                    
    [0m[2m => => # Downloading idna-3.11-py3-none-any.whl (71 kB)                        
    [0m => [browser] resolving provenance for metadata file                       0.0s
     => CACHED [frontend 2/5] WORKDIR /app                                     0.0s
     => CACHED [frontend 3/5] COPY package.json package-lock.json* ./          0.0s
     => CACHED [frontend 4/5] RUN npm ci                                       0.0s
     => [frontend 5/5] COPY . .                                                1.6s
     => [frontend] exporting to image                                          3.2s
     => => exporting layers                                                    2.6s
     => => exporting manifest sha256:5590f5beedb5d595cd6fbc523d956e6b20992436  0.0s
     => => exporting config sha256:658ecac42db2e44d58f45a370df44e07eb944c0984  0.0s
     => => exporting attestation manifest sha256:26da59865b0be310448478f2f05d  0.0s
     => => exporting manifest list sha256:d095aeb02035e25bbb67b5be219cf439526  0.0s
     => => naming to docker.io/library/compose-frontend:latest                 0.0s
     => => unpacking to docker.io/library/compose-frontend:latest              0.6s
    [?25h[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[0G[?25l[+] Building 6.3s (32/34)                                                       
     => [backend 3/5] COPY requirements.txt .                                  0.0s
     => [backend 4/5] RUN pip install --no-cache-dir -r requirements.txt       5.2s
    [2m => => # Downloading starlette-0.47.3-py3-none-any.whl (72 kB)                 
    [0m[2m => => # Downloading anyio-4.13.0-py3-none-any.whl (114 kB)                    
    [0m[2m => => # Downloading idna-3.11-py3-none-any.whl (71 kB)                        
    [0m[2m => => # Downloading typing_extensions-4.15.0-py3-none-any.whl (44 kB)         
    [0m[2m => => # Downloading uvloop-0.22.1-cp312-cp312-manylinux2014_aarch64.manylinux_
    [0m[2m => => # 2_17_aarch64.manylinux_2_28_aarch64.whl (4.3 MB)                      
    [0m => [browser] resolving provenance for metadata file                       0.0s
     => CACHED [frontend 2/5] WORKDIR /app                                     0.0s
     => CACHED [frontend 3/5] COPY package.json package-lock.json* ./          0.0s
     => CACHED [frontend 4/5] RUN npm ci                                       0.0s
     => [frontend 5/5] COPY . .                                                1.6s
     => [frontend] exporting to image                                          3.2s
     => => exporting layers                                                    2.6s
     => => exporting manifest sha256:5590f5beedb5d595cd6fbc523d956e6b20992436  0.0s
     => => exporting config sha256:658ecac42db2e44d58f45a370df44e07eb944c0984  0.0s
     => => exporting attestation manifest sha256:26da59865b0be310448478f2f05d  0.0s
     => => exporting manifest list sha256:d095aeb02035e25bbb67b5be219cf439526  0.0s
     => => naming to docker.io/library/compose-frontend:latest                 0.0s
     => => unpacking to docker.io/library/compose-frontend:latest              0.6s
     => [frontend] resolving provenance for metadata file                      0.0s
    [?25h[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[0G[?25l[+] Building 6.5s (32/34)                                                       
     => [backend 3/5] COPY requirements.txt .                                  0.0s
     => [backend 4/5] RUN pip install --no-cache-dir -r requirements.txt       5.3s
    [2m => => # Downloading starlette-0.47.3-py3-none-any.whl (72 kB)                 
    [0m[2m => => # Downloading anyio-4.13.0-py3-none-any.whl (114 kB)                    
    [0m[2m => => # Downloading idna-3.11-py3-none-any.whl (71 kB)                        
    [0m[2m => => # Downloading typing_extensions-4.15.0-py3-none-any.whl (44 kB)         
    [0m[2m => => # Downloading uvloop-0.22.1-cp312-cp312-manylinux2014_aarch64.manylinux_
    [0m[2m => => # 2_17_aarch64.manylinux_2_28_aarch64.whl (4.3 MB)                      
    [0m => [browser] resolving provenance for metadata file                       0.0s
     => CACHED [frontend 2/5] WORKDIR /app                                     0.0s
     => CACHED [frontend 3/5] COPY package.json package-lock.json* ./          0.0s
     => CACHED [frontend 4/5] RUN npm ci                                       0.0s
     => [frontend 5/5] COPY . .                                                1.6s
     => [frontend] exporting to image                                          3.2s
     => => exporting layers                                                    2.6s
     => => exporting manifest sha256:5590f5beedb5d595cd6fbc523d956e6b20992436  0.0s
     => => exporting config sha256:658ecac42db2e44d58f45a370df44e07eb944c0984  0.0s
     => => exporting attestation manifest sha256:26da59865b0be310448478f2f05d  0.0s
     => => exporting manifest list sha256:d095aeb02035e25bbb67b5be219cf439526  0.0s
     => => naming to docker.io/library/compose-frontend:latest                 0.0s
     => => unpacking to docker.io/library/compose-frontend:latest              0.6s
     => [frontend] resolving provenance for metadata file                      0.0s
    [?25h[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[0G[?25l[+] Building 6.6s (32/34)                                                       
     => [backend 3/5] COPY requirements.txt .                                  0.0s
     => [backend 4/5] RUN pip install --no-cache-dir -r requirements.txt       5.5s
    [2m => => # Downloading starlette-0.47.3-py3-none-any.whl (72 kB)                 
    [0m[2m => => # Downloading anyio-4.13.0-py3-none-any.whl (114 kB)                    
    [0m[2m => => # Downloading idna-3.11-py3-none-any.whl (71 kB)                        
    [0m[2m => => # Downloading typing_extensions-4.15.0-py3-none-any.whl (44 kB)         
    [0m[2m => => # Downloading uvloop-0.22.1-cp312-cp312-manylinux2014_aarch64.manylinux_
    [0m[2m => => # 2_17_aarch64.manylinux_2_28_aarch64.whl (4.3 MB)                      
    [0m => [browser] resolving provenance for metadata file                       0.0s
     => CACHED [frontend 2/5] WORKDIR /app                                     0.0s
     => CACHED [frontend 3/5] COPY package.json package-lock.json* ./          0.0s
     => CACHED [frontend 4/5] RUN npm ci                                       0.0s
     => [frontend 5/5] COPY . .                                                1.6s
     => [frontend] exporting to image                                          3.2s
     => => exporting layers                                                    2.6s
     => => exporting manifest sha256:5590f5beedb5d595cd6fbc523d956e6b20992436  0.0s
     => => exporting config sha256:658ecac42db2e44d58f45a370df44e07eb944c0984  0.0s
     => => exporting attestation manifest sha256:26da59865b0be310448478f2f05d  0.0s
     => => exporting manifest list sha256:d095aeb02035e25bbb67b5be219cf439526  0.0s
     => => naming to docker.io/library/compose-frontend:latest                 0.0s
     => => unpacking to docker.io/library/compose-frontend:latest              0.6s
     => [frontend] resolving provenance for metadata file                      0.0s
    [?25h[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[0G[?25l[+] Building 6.8s (32/34)                                                       
     => [backend 3/5] COPY requirements.txt .                                  0.0s
     => [backend 4/5] RUN pip install --no-cache-dir -r requirements.txt       5.6s
    [2m => => # Downloading starlette-0.47.3-py3-none-any.whl (72 kB)                 
    [0m[2m => => # Downloading anyio-4.13.0-py3-none-any.whl (114 kB)                    
    [0m[2m => => # Downloading idna-3.11-py3-none-any.whl (71 kB)                        
    [0m[2m => => # Downloading typing_extensions-4.15.0-py3-none-any.whl (44 kB)         
    [0m[2m => => # Downloading uvloop-0.22.1-cp312-cp312-manylinux2014_aarch64.manylinux_
    [0m[2m => => # 2_17_aarch64.manylinux_2_28_aarch64.whl (4.3 MB)                      
    [0m => [browser] resolving provenance for metadata file                       0.0s
     => CACHED [frontend 2/5] WORKDIR /app                                     0.0s
     => CACHED [frontend 3/5] COPY package.json package-lock.json* ./          0.0s
     => CACHED [frontend 4/5] RUN npm ci                                       0.0s
     => [frontend 5/5] COPY . .                                                1.6s
     => [frontend] exporting to image                                          3.2s
     => => exporting layers                                                    2.6s
     => => exporting manifest sha256:5590f5beedb5d595cd6fbc523d956e6b20992436  0.0s
     => => exporting config sha256:658ecac42db2e44d58f45a370df44e07eb944c0984  0.0s
     => => exporting attestation manifest sha256:26da59865b0be310448478f2f05d  0.0s
     => => exporting manifest list sha256:d095aeb02035e25bbb67b5be219cf439526  0.0s
     => => naming to docker.io/library/compose-frontend:latest                 0.0s
     => => unpacking to docker.io/library/compose-frontend:latest              0.6s
     => [frontend] resolving provenance for metadata file                      0.0s
    [?25h[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[0G[?25l[+] Building 6.8s (32/34)                                                       
     => [backend 3/5] COPY requirements.txt .                                  0.0s
     => [backend 4/5] RUN pip install --no-cache-dir -r requirements.txt       5.7s
    [2m => => # Downloading idna-3.11-py3-none-any.whl (71 kB)                        
    [0m[2m => => # Downloading typing_extensions-4.15.0-py3-none-any.whl (44 kB)         
    [0m[2m => => # Downloading uvloop-0.22.1-cp312-cp312-manylinux2014_aarch64.manylinux_
    [0m[2m => => # 2_17_aarch64.manylinux_2_28_aarch64.whl (4.3 MB)                      
    [0m[2m => => #    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 4.3/4.3 MB 6.7 MB/s eta 0:
    [0m[2m => => # 00:00                                                                 
    [0m => [browser] resolving provenance for metadata file                       0.0s
     => CACHED [frontend 2/5] WORKDIR /app                                     0.0s
     => CACHED [frontend 3/5] COPY package.json package-lock.json* ./          0.0s
     => CACHED [frontend 4/5] RUN npm ci                                       0.0s
     => [frontend 5/5] COPY . .                                                1.6s
     => [frontend] exporting to image                                          3.2s
     => => exporting layers                                                    2.6s
     => => exporting manifest sha256:5590f5beedb5d595cd6fbc523d956e6b20992436  0.0s
     => => exporting config sha256:658ecac42db2e44d58f45a370df44e07eb944c0984  0.0s
     => => exporting attestation manifest sha256:26da59865b0be310448478f2f05d  0.0s
     => => exporting manifest list sha256:d095aeb02035e25bbb67b5be219cf439526  0.0s
     => => naming to docker.io/library/compose-frontend:latest                 0.0s
     => => unpacking to docker.io/library/compose-frontend:latest              0.6s
     => [frontend] resolving provenance for metadata file                      0.0s
    [?25h[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[0G[?25l[+] Building 6.9s (32/34)                                                       
     => [backend 3/5] COPY requirements.txt .                                  0.0s
     => [backend 4/5] RUN pip install --no-cache-dir -r requirements.txt       5.8s
    [2m => => #    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 4.3/4.3 MB 6.7 MB/s eta 0:
    [0m[2m => => # 00:00                                                                 
    [0m[2m => => # Downloading watchfiles-1.1.1-cp312-cp312-manylinux_2_17_aarch64.manyli
    [0m[2m => => # nux2014_aarch64.whl (449 kB)                                          
    [0m[2m => => # Downloading websockets-16.0-cp312-cp312-manylinux2014_aarch64.manylinu
    [0m[2m => => # x_2_17_aarch64.manylinux_2_28_aarch64.whl (186 kB)                    
    [0m => [browser] resolving provenance for metadata file                       0.0s
     => CACHED [frontend 2/5] WORKDIR /app                                     0.0s
     => CACHED [frontend 3/5] COPY package.json package-lock.json* ./          0.0s
     => CACHED [frontend 4/5] RUN npm ci                                       0.0s
     => [frontend 5/5] COPY . .                                                1.6s
     => [frontend] exporting to image                                          3.2s
     => => exporting layers                                                    2.6s
     => => exporting manifest sha256:5590f5beedb5d595cd6fbc523d956e6b20992436  0.0s
     => => exporting config sha256:658ecac42db2e44d58f45a370df44e07eb944c0984  0.0s
     => => exporting attestation manifest sha256:26da59865b0be310448478f2f05d  0.0s
     => => exporting manifest list sha256:d095aeb02035e25bbb67b5be219cf439526  0.0s
     => => naming to docker.io/library/compose-frontend:latest                 0.0s
     => => unpacking to docker.io/library/compose-frontend:latest              0.6s
     => [frontend] resolving provenance for metadata file                      0.0s
    [?25h[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[0G[?25l[+] Building 7.1s (32/34)                                                       
     => [backend 3/5] COPY requirements.txt .                                  0.0s
     => [backend 4/5] RUN pip install --no-cache-dir -r requirements.txt       5.9s
    [2m => => # nux2014_aarch64.whl (449 kB)                                          
    [0m[2m => => # Downloading websockets-16.0-cp312-cp312-manylinux2014_aarch64.manylinu
    [0m[2m => => # x_2_17_aarch64.manylinux_2_28_aarch64.whl (186 kB)                    
    [0m[2m => => # Downloading certifi-2026.2.25-py3-none-any.whl (153 kB)               
    [0m[2m => => # Downloading annotated_types-0.7.0-py3-none-any.whl (13 kB)            
    [0m[2m => => # Downloading typing_inspection-0.4.2-py3-none-any.whl (14 kB)          
    [0m => [browser] resolving provenance for metadata file                       0.0s
     => CACHED [frontend 2/5] WORKDIR /app                                     0.0s
     => CACHED [frontend 3/5] COPY package.json package-lock.json* ./          0.0s
     => CACHED [frontend 4/5] RUN npm ci                                       0.0s
     => [frontend 5/5] COPY . .                                                1.6s
     => [frontend] exporting to image                                          3.2s
     => => exporting layers                                                    2.6s
     => => exporting manifest sha256:5590f5beedb5d595cd6fbc523d956e6b20992436  0.0s
     => => exporting config sha256:658ecac42db2e44d58f45a370df44e07eb944c0984  0.0s
     => => exporting attestation manifest sha256:26da59865b0be310448478f2f05d  0.0s
     => => exporting manifest list sha256:d095aeb02035e25bbb67b5be219cf439526  0.0s
     => => naming to docker.io/library/compose-frontend:latest                 0.0s
     => => unpacking to docker.io/library/compose-frontend:latest              0.6s
     => [frontend] resolving provenance for metadata file                      0.0s
    [?25h[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[0G[?25l[+] Building 7.3s (32/34)                                                       
     => [backend 3/5] COPY requirements.txt .                                  0.0s
     => [backend 4/5] RUN pip install --no-cache-dir -r requirements.txt       6.1s
    [2m => => # Downloading typing_inspection-0.4.2-py3-none-any.whl (14 kB)          
    [0m[2m => => # Installing collected packages: websockets, uvloop, typing-extensions, 
    [0m[2m => => # pyyaml, python-dotenv, pygments, pluggy, packaging, iniconfig, idna, h
    [0m[2m => => # ttptools, h11, click, certifi, annotated-types, uvicorn, typing-inspec
    [0m[2m => => # tion, pytest, pydantic-core, httpcore, anyio, watchfiles, starlette, p
    [0m[2m => => # ydantic, httpx, fastapi                                               
    [0m => [browser] resolving provenance for metadata file                       0.0s
     => CACHED [frontend 2/5] WORKDIR /app                                     0.0s
     => CACHED [frontend 3/5] COPY package.json package-lock.json* ./          0.0s
     => CACHED [frontend 4/5] RUN npm ci                                       0.0s
     => [frontend 5/5] COPY . .                                                1.6s
     => [frontend] exporting to image                                          3.2s
     => => exporting layers                                                    2.6s
     => => exporting manifest sha256:5590f5beedb5d595cd6fbc523d956e6b20992436  0.0s
     => => exporting config sha256:658ecac42db2e44d58f45a370df44e07eb944c0984  0.0s
     => => exporting attestation manifest sha256:26da59865b0be310448478f2f05d  0.0s
     => => exporting manifest list sha256:d095aeb02035e25bbb67b5be219cf439526  0.0s
     => => naming to docker.io/library/compose-frontend:latest                 0.0s
     => => unpacking to docker.io/library/compose-frontend:latest              0.6s
     => [frontend] resolving provenance for metadata file                      0.0s
    [?25h[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[0G[?25l[+] Building 7.4s (32/34)                                                       
     => [backend 3/5] COPY requirements.txt .                                  0.0s
     => [backend 4/5] RUN pip install --no-cache-dir -r requirements.txt       6.3s
    [2m => => # Downloading typing_inspection-0.4.2-py3-none-any.whl (14 kB)          
    [0m[2m => => # Installing collected packages: websockets, uvloop, typing-extensions, 
    [0m[2m => => # pyyaml, python-dotenv, pygments, pluggy, packaging, iniconfig, idna, h
    [0m[2m => => # ttptools, h11, click, certifi, annotated-types, uvicorn, typing-inspec
    [0m[2m => => # tion, pytest, pydantic-core, httpcore, anyio, watchfiles, starlette, p
    [0m[2m => => # ydantic, httpx, fastapi                                               
    [0m => [browser] resolving provenance for metadata file                       0.0s
     => CACHED [frontend 2/5] WORKDIR /app                                     0.0s
     => CACHED [frontend 3/5] COPY package.json package-lock.json* ./          0.0s
     => CACHED [frontend 4/5] RUN npm ci                                       0.0s
     => [frontend 5/5] COPY . .                                                1.6s
     => [frontend] exporting to image                                          3.2s
     => => exporting layers                                                    2.6s
     => => exporting manifest sha256:5590f5beedb5d595cd6fbc523d956e6b20992436  0.0s
     => => exporting config sha256:658ecac42db2e44d58f45a370df44e07eb944c0984  0.0s
     => => exporting attestation manifest sha256:26da59865b0be310448478f2f05d  0.0s
     => => exporting manifest list sha256:d095aeb02035e25bbb67b5be219cf439526  0.0s
     => => naming to docker.io/library/compose-frontend:latest                 0.0s
     => => unpacking to docker.io/library/compose-frontend:latest              0.6s
     => [frontend] resolving provenance for metadata file                      0.0s
    [?25h[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[0G[?25l[+] Building 7.6s (32/34)                                                       
     => [backend 3/5] COPY requirements.txt .                                  0.0s
     => [backend 4/5] RUN pip install --no-cache-dir -r requirements.txt       6.4s
    [2m => => # Downloading typing_inspection-0.4.2-py3-none-any.whl (14 kB)          
    [0m[2m => => # Installing collected packages: websockets, uvloop, typing-extensions, 
    [0m[2m => => # pyyaml, python-dotenv, pygments, pluggy, packaging, iniconfig, idna, h
    [0m[2m => => # ttptools, h11, click, certifi, annotated-types, uvicorn, typing-inspec
    [0m[2m => => # tion, pytest, pydantic-core, httpcore, anyio, watchfiles, starlette, p
    [0m[2m => => # ydantic, httpx, fastapi                                               
    [0m => [browser] resolving provenance for metadata file                       0.0s
     => CACHED [frontend 2/5] WORKDIR /app                                     0.0s
     => CACHED [frontend 3/5] COPY package.json package-lock.json* ./          0.0s
     => CACHED [frontend 4/5] RUN npm ci                                       0.0s
     => [frontend 5/5] COPY . .                                                1.6s
     => [frontend] exporting to image                                          3.2s
     => => exporting layers                                                    2.6s
     => => exporting manifest sha256:5590f5beedb5d595cd6fbc523d956e6b20992436  0.0s
     => => exporting config sha256:658ecac42db2e44d58f45a370df44e07eb944c0984  0.0s
     => => exporting attestation manifest sha256:26da59865b0be310448478f2f05d  0.0s
     => => exporting manifest list sha256:d095aeb02035e25bbb67b5be219cf439526  0.0s
     => => naming to docker.io/library/compose-frontend:latest                 0.0s
     => => unpacking to docker.io/library/compose-frontend:latest              0.6s
     => [frontend] resolving provenance for metadata file                      0.0s
    [?25h[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[0G[?25l[+] Building 7.7s (32/34)                                                       
     => [backend 3/5] COPY requirements.txt .                                  0.0s
     => [backend 4/5] RUN pip install --no-cache-dir -r requirements.txt       6.6s
    [2m => => # Downloading typing_inspection-0.4.2-py3-none-any.whl (14 kB)          
    [0m[2m => => # Installing collected packages: websockets, uvloop, typing-extensions, 
    [0m[2m => => # pyyaml, python-dotenv, pygments, pluggy, packaging, iniconfig, idna, h
    [0m[2m => => # ttptools, h11, click, certifi, annotated-types, uvicorn, typing-inspec
    [0m[2m => => # tion, pytest, pydantic-core, httpcore, anyio, watchfiles, starlette, p
    [0m[2m => => # ydantic, httpx, fastapi                                               
    [0m => [browser] resolving provenance for metadata file                       0.0s
     => CACHED [frontend 2/5] WORKDIR /app                                     0.0s
     => CACHED [frontend 3/5] COPY package.json package-lock.json* ./          0.0s
     => CACHED [frontend 4/5] RUN npm ci                                       0.0s
     => [frontend 5/5] COPY . .                                                1.6s
     => [frontend] exporting to image                                          3.2s
     => => exporting layers                                                    2.6s
     => => exporting manifest sha256:5590f5beedb5d595cd6fbc523d956e6b20992436  0.0s
     => => exporting config sha256:658ecac42db2e44d58f45a370df44e07eb944c0984  0.0s
     => => exporting attestation manifest sha256:26da59865b0be310448478f2f05d  0.0s
     => => exporting manifest list sha256:d095aeb02035e25bbb67b5be219cf439526  0.0s
     => => naming to docker.io/library/compose-frontend:latest                 0.0s
     => => unpacking to docker.io/library/compose-frontend:latest              0.6s
     => [frontend] resolving provenance for metadata file                      0.0s
    [?25h[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[0G[?25l[+] Building 7.9s (32/34)                                                       
     => [backend 3/5] COPY requirements.txt .                                  0.0s
     => [backend 4/5] RUN pip install --no-cache-dir -r requirements.txt       6.7s
    [2m => => # Downloading typing_inspection-0.4.2-py3-none-any.whl (14 kB)          
    [0m[2m => => # Installing collected packages: websockets, uvloop, typing-extensions, 
    [0m[2m => => # pyyaml, python-dotenv, pygments, pluggy, packaging, iniconfig, idna, h
    [0m[2m => => # ttptools, h11, click, certifi, annotated-types, uvicorn, typing-inspec
    [0m[2m => => # tion, pytest, pydantic-core, httpcore, anyio, watchfiles, starlette, p
    [0m[2m => => # ydantic, httpx, fastapi                                               
    [0m => [browser] resolving provenance for metadata file                       0.0s
     => CACHED [frontend 2/5] WORKDIR /app                                     0.0s
     => CACHED [frontend 3/5] COPY package.json package-lock.json* ./          0.0s
     => CACHED [frontend 4/5] RUN npm ci                                       0.0s
     => [frontend 5/5] COPY . .                                                1.6s
     => [frontend] exporting to image                                          3.2s
     => => exporting layers                                                    2.6s
     => => exporting manifest sha256:5590f5beedb5d595cd6fbc523d956e6b20992436  0.0s
     => => exporting config sha256:658ecac42db2e44d58f45a370df44e07eb944c0984  0.0s
     => => exporting attestation manifest sha256:26da59865b0be310448478f2f05d  0.0s
     => => exporting manifest list sha256:d095aeb02035e25bbb67b5be219cf439526  0.0s
     => => naming to docker.io/library/compose-frontend:latest                 0.0s
     => => unpacking to docker.io/library/compose-frontend:latest              0.6s
     => [frontend] resolving provenance for metadata file                      0.0s
    [?25h[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[0G[?25l[+] Building 8.0s (32/34)                                                       
     => [backend 3/5] COPY requirements.txt .                                  0.0s
     => [backend 4/5] RUN pip install --no-cache-dir -r requirements.txt       6.9s
    [2m => => # Downloading typing_inspection-0.4.2-py3-none-any.whl (14 kB)          
    [0m[2m => => # Installing collected packages: websockets, uvloop, typing-extensions, 
    [0m[2m => => # pyyaml, python-dotenv, pygments, pluggy, packaging, iniconfig, idna, h
    [0m[2m => => # ttptools, h11, click, certifi, annotated-types, uvicorn, typing-inspec
    [0m[2m => => # tion, pytest, pydantic-core, httpcore, anyio, watchfiles, starlette, p
    [0m[2m => => # ydantic, httpx, fastapi                                               
    [0m => [browser] resolving provenance for metadata file                       0.0s
     => CACHED [frontend 2/5] WORKDIR /app                                     0.0s
     => CACHED [frontend 3/5] COPY package.json package-lock.json* ./          0.0s
     => CACHED [frontend 4/5] RUN npm ci                                       0.0s
     => [frontend 5/5] COPY . .                                                1.6s
     => [frontend] exporting to image                                          3.2s
     => => exporting layers                                                    2.6s
     => => exporting manifest sha256:5590f5beedb5d595cd6fbc523d956e6b20992436  0.0s
     => => exporting config sha256:658ecac42db2e44d58f45a370df44e07eb944c0984  0.0s
     => => exporting attestation manifest sha256:26da59865b0be310448478f2f05d  0.0s
     => => exporting manifest list sha256:d095aeb02035e25bbb67b5be219cf439526  0.0s
     => => naming to docker.io/library/compose-frontend:latest                 0.0s
     => => unpacking to docker.io/library/compose-frontend:latest              0.6s
     => [frontend] resolving provenance for metadata file                      0.0s
    [?25h[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[0G[?25l[+] Building 8.0s (32/34)                                                       
     => [backend 3/5] COPY requirements.txt .                                  0.0s
     => [backend 4/5] RUN pip install --no-cache-dir -r requirements.txt       6.9s
    [2m => => # .2.25 click-8.3.1 fastapi-0.116.1 h11-0.16.0 httpcore-1.0.9 httptools-
    [0m[2m => => # 0.7.1 httpx-0.28.1 idna-3.11 iniconfig-2.3.0 packaging-26.0 pluggy-1.6
    [0m[2m => => # .0 pydantic-2.12.5 pydantic-core-2.41.5 pygments-2.20.0 pytest-8.4.2 p
    [0m[2m => => # ython-dotenv-1.2.2 pyyaml-6.0.3 starlette-0.47.3 typing-extensions-4.1
    [0m[2m => => # 5.0 typing-inspection-0.4.2 uvicorn-0.35.0 uvloop-0.22.1 watchfiles-1.
    [0m[2m => => # 1.1 websockets-16.0                                                   
    [0m => [browser] resolving provenance for metadata file                       0.0s
     => CACHED [frontend 2/5] WORKDIR /app                                     0.0s
     => CACHED [frontend 3/5] COPY package.json package-lock.json* ./          0.0s
     => CACHED [frontend 4/5] RUN npm ci                                       0.0s
     => [frontend 5/5] COPY . .                                                1.6s
     => [frontend] exporting to image                                          3.2s
     => => exporting layers                                                    2.6s
     => => exporting manifest sha256:5590f5beedb5d595cd6fbc523d956e6b20992436  0.0s
     => => exporting config sha256:658ecac42db2e44d58f45a370df44e07eb944c0984  0.0s
     => => exporting attestation manifest sha256:26da59865b0be310448478f2f05d  0.0s
     => => exporting manifest list sha256:d095aeb02035e25bbb67b5be219cf439526  0.0s
     => => naming to docker.io/library/compose-frontend:latest                 0.0s
     => => unpacking to docker.io/library/compose-frontend:latest              0.6s
     => [frontend] resolving provenance for metadata file                      0.0s
    [?25h[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[0G[?25l[+] Building 8.1s (32/34)                                                       
     => [backend 3/5] COPY requirements.txt .                                  0.0s
     => [backend 4/5] RUN pip install --no-cache-dir -r requirements.txt       7.0s
    [2m => => #  rendering your system unusable. It is recommended to use a virtual en
    [0m[2m => => # vironment instead: https://pip.pypa.io/warnings/venv. Use the --root-u
    [0m[2m => => # ser-action option if you know what you are doing and want to suppress 
    [0m[2m => => # this warning.                                                         
    [0m[2m => => # [notice] A new release of pip is available: 25.0.1 -> 26.0.1          
    [0m[2m => => # [notice] To update, run: pip install --upgrade pip                    
    [0m => [browser] resolving provenance for metadata file                       0.0s
     => CACHED [frontend 2/5] WORKDIR /app                                     0.0s
     => CACHED [frontend 3/5] COPY package.json package-lock.json* ./          0.0s
     => CACHED [frontend 4/5] RUN npm ci                                       0.0s
     => [frontend 5/5] COPY . .                                                1.6s
     => [frontend] exporting to image                                          3.2s
     => => exporting layers                                                    2.6s
     => => exporting manifest sha256:5590f5beedb5d595cd6fbc523d956e6b20992436  0.0s
     => => exporting config sha256:658ecac42db2e44d58f45a370df44e07eb944c0984  0.0s
     => => exporting attestation manifest sha256:26da59865b0be310448478f2f05d  0.0s
     => => exporting manifest list sha256:d095aeb02035e25bbb67b5be219cf439526  0.0s
     => => naming to docker.io/library/compose-frontend:latest                 0.0s
     => => unpacking to docker.io/library/compose-frontend:latest              0.6s
     => [frontend] resolving provenance for metadata file                      0.0s
    [?25h[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[0G[?25l[+] Building 8.3s (33/34)                                                       
     => => transferring context: 2B                                            0.0s
     => [backend 1/5] FROM docker.io/library/python:3.12-slim@sha256:3d5ed973  0.0s
     => => resolve docker.io/library/python:3.12-slim@sha256:3d5ed973e45820f5  0.0s
     => [backend internal] load build context                                  0.0s
     => => transferring context: 9.45kB                                        0.0s
     => CACHED [backend 2/5] WORKDIR /app                                      0.0s
     => [backend 3/5] COPY requirements.txt .                                  0.0s
     => [backend 4/5] RUN pip install --no-cache-dir -r requirements.txt       7.1s
     => [browser] resolving provenance for metadata file                       0.0s
     => CACHED [frontend 2/5] WORKDIR /app                                     0.0s
     => CACHED [frontend 3/5] COPY package.json package-lock.json* ./          0.0s
     => CACHED [frontend 4/5] RUN npm ci                                       0.0s
     => [frontend 5/5] COPY . .                                                1.6s
     => [frontend] exporting to image                                          3.2s
     => => exporting layers                                                    2.6s
     => => exporting manifest sha256:5590f5beedb5d595cd6fbc523d956e6b20992436  0.0s
     => => exporting config sha256:658ecac42db2e44d58f45a370df44e07eb944c0984  0.0s
     => => exporting attestation manifest sha256:26da59865b0be310448478f2f05d  0.0s
     => => exporting manifest list sha256:d095aeb02035e25bbb67b5be219cf439526  0.0s
     => => naming to docker.io/library/compose-frontend:latest                 0.0s
     => => unpacking to docker.io/library/compose-frontend:latest              0.6s
     => [frontend] resolving provenance for metadata file                      0.0s
    [?25h[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[0G[?25l[+] Building 8.5s (34/35)                                                       
     => [backend internal] load build context                                  0.0s
     => => transferring context: 9.45kB                                        0.0s
     => CACHED [backend 2/5] WORKDIR /app                                      0.0s
     => [backend 3/5] COPY requirements.txt .                                  0.0s
     => [backend 4/5] RUN pip install --no-cache-dir -r requirements.txt       7.1s
     => [browser] resolving provenance for metadata file                       0.0s
     => CACHED [frontend 2/5] WORKDIR /app                                     0.0s
     => CACHED [frontend 3/5] COPY package.json package-lock.json* ./          0.0s
     => CACHED [frontend 4/5] RUN npm ci                                       0.0s
     => [frontend 5/5] COPY . .                                                1.6s
     => [frontend] exporting to image                                          3.2s
     => => exporting layers                                                    2.6s
     => => exporting manifest sha256:5590f5beedb5d595cd6fbc523d956e6b20992436  0.0s
     => => exporting config sha256:658ecac42db2e44d58f45a370df44e07eb944c0984  0.0s
     => => exporting attestation manifest sha256:26da59865b0be310448478f2f05d  0.0s
     => => exporting manifest list sha256:d095aeb02035e25bbb67b5be219cf439526  0.0s
     => => naming to docker.io/library/compose-frontend:latest                 0.0s
     => => unpacking to docker.io/library/compose-frontend:latest              0.6s
     => [frontend] resolving provenance for metadata file                      0.0s
     => [backend 5/5] COPY app ./app                                           0.0s
     => [backend] exporting to image                                           0.2s
     => => exporting layers                                                    0.2s
    [?25h[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[0G[?25l[+] Building 8.6s (34/35)                                                       
     => [backend internal] load build context                                  0.0s
     => => transferring context: 9.45kB                                        0.0s
     => CACHED [backend 2/5] WORKDIR /app                                      0.0s
     => [backend 3/5] COPY requirements.txt .                                  0.0s
     => [backend 4/5] RUN pip install --no-cache-dir -r requirements.txt       7.1s
     => [browser] resolving provenance for metadata file                       0.0s
     => CACHED [frontend 2/5] WORKDIR /app                                     0.0s
     => CACHED [frontend 3/5] COPY package.json package-lock.json* ./          0.0s
     => CACHED [frontend 4/5] RUN npm ci                                       0.0s
     => [frontend 5/5] COPY . .                                                1.6s
     => [frontend] exporting to image                                          3.2s
     => => exporting layers                                                    2.6s
     => => exporting manifest sha256:5590f5beedb5d595cd6fbc523d956e6b20992436  0.0s
     => => exporting config sha256:658ecac42db2e44d58f45a370df44e07eb944c0984  0.0s
     => => exporting attestation manifest sha256:26da59865b0be310448478f2f05d  0.0s
     => => exporting manifest list sha256:d095aeb02035e25bbb67b5be219cf439526  0.0s
     => => naming to docker.io/library/compose-frontend:latest                 0.0s
     => => unpacking to docker.io/library/compose-frontend:latest              0.6s
     => [frontend] resolving provenance for metadata file                      0.0s
     => [backend 5/5] COPY app ./app                                           0.0s
     => [backend] exporting to image                                           0.3s
     => => exporting layers                                                    0.3s
    [?25h[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[0G[?25l[+] Building 8.8s (34/35)                                                       
     => [backend internal] load build context                                  0.0s
     => => transferring context: 9.45kB                                        0.0s
     => CACHED [backend 2/5] WORKDIR /app                                      0.0s
     => [backend 3/5] COPY requirements.txt .                                  0.0s
     => [backend 4/5] RUN pip install --no-cache-dir -r requirements.txt       7.1s
     => [browser] resolving provenance for metadata file                       0.0s
     => CACHED [frontend 2/5] WORKDIR /app                                     0.0s
     => CACHED [frontend 3/5] COPY package.json package-lock.json* ./          0.0s
     => CACHED [frontend 4/5] RUN npm ci                                       0.0s
     => [frontend 5/5] COPY . .                                                1.6s
     => [frontend] exporting to image                                          3.2s
     => => exporting layers                                                    2.6s
     => => exporting manifest sha256:5590f5beedb5d595cd6fbc523d956e6b20992436  0.0s
     => => exporting config sha256:658ecac42db2e44d58f45a370df44e07eb944c0984  0.0s
     => => exporting attestation manifest sha256:26da59865b0be310448478f2f05d  0.0s
     => => exporting manifest list sha256:d095aeb02035e25bbb67b5be219cf439526  0.0s
     => => naming to docker.io/library/compose-frontend:latest                 0.0s
     => => unpacking to docker.io/library/compose-frontend:latest              0.6s
     => [frontend] resolving provenance for metadata file                      0.0s
     => [backend 5/5] COPY app ./app                                           0.0s
     => [backend] exporting to image                                           0.5s
     => => exporting layers                                                    0.5s
    [?25h[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[0G[?25l[+] Building 8.9s (34/35)                                                       
     => [backend internal] load build context                                  0.0s
     => => transferring context: 9.45kB                                        0.0s
     => CACHED [backend 2/5] WORKDIR /app                                      0.0s
     => [backend 3/5] COPY requirements.txt .                                  0.0s
     => [backend 4/5] RUN pip install --no-cache-dir -r requirements.txt       7.1s
     => [browser] resolving provenance for metadata file                       0.0s
     => CACHED [frontend 2/5] WORKDIR /app                                     0.0s
     => CACHED [frontend 3/5] COPY package.json package-lock.json* ./          0.0s
     => CACHED [frontend 4/5] RUN npm ci                                       0.0s
     => [frontend 5/5] COPY . .                                                1.6s
     => [frontend] exporting to image                                          3.2s
     => => exporting layers                                                    2.6s
     => => exporting manifest sha256:5590f5beedb5d595cd6fbc523d956e6b20992436  0.0s
     => => exporting config sha256:658ecac42db2e44d58f45a370df44e07eb944c0984  0.0s
     => => exporting attestation manifest sha256:26da59865b0be310448478f2f05d  0.0s
     => => exporting manifest list sha256:d095aeb02035e25bbb67b5be219cf439526  0.0s
     => => naming to docker.io/library/compose-frontend:latest                 0.0s
     => => unpacking to docker.io/library/compose-frontend:latest              0.6s
     => [frontend] resolving provenance for metadata file                      0.0s
     => [backend 5/5] COPY app ./app                                           0.0s
     => [backend] exporting to image                                           0.6s
     => => exporting layers                                                    0.6s
    [?25h[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[0G[?25l[+] Building 9.1s (34/35)                                                       
     => [backend internal] load build context                                  0.0s
     => => transferring context: 9.45kB                                        0.0s
     => CACHED [backend 2/5] WORKDIR /app                                      0.0s
     => [backend 3/5] COPY requirements.txt .                                  0.0s
     => [backend 4/5] RUN pip install --no-cache-dir -r requirements.txt       7.1s
     => [browser] resolving provenance for metadata file                       0.0s
     => CACHED [frontend 2/5] WORKDIR /app                                     0.0s
     => CACHED [frontend 3/5] COPY package.json package-lock.json* ./          0.0s
     => CACHED [frontend 4/5] RUN npm ci                                       0.0s
     => [frontend 5/5] COPY . .                                                1.6s
     => [frontend] exporting to image                                          3.2s
     => => exporting layers                                                    2.6s
     => => exporting manifest sha256:5590f5beedb5d595cd6fbc523d956e6b20992436  0.0s
     => => exporting config sha256:658ecac42db2e44d58f45a370df44e07eb944c0984  0.0s
     => => exporting attestation manifest sha256:26da59865b0be310448478f2f05d  0.0s
     => => exporting manifest list sha256:d095aeb02035e25bbb67b5be219cf439526  0.0s
     => => naming to docker.io/library/compose-frontend:latest                 0.0s
     => => unpacking to docker.io/library/compose-frontend:latest              0.6s
     => [frontend] resolving provenance for metadata file                      0.0s
     => [backend 5/5] COPY app ./app                                           0.0s
     => [backend] exporting to image                                           0.8s
     => => exporting layers                                                    0.8s
    [?25h[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[0G[?25l[+] Building 9.2s (34/35)                                                       
     => [backend internal] load build context                                  0.0s
     => => transferring context: 9.45kB                                        0.0s
     => CACHED [backend 2/5] WORKDIR /app                                      0.0s
     => [backend 3/5] COPY requirements.txt .                                  0.0s
     => [backend 4/5] RUN pip install --no-cache-dir -r requirements.txt       7.1s
     => [browser] resolving provenance for metadata file                       0.0s
     => CACHED [frontend 2/5] WORKDIR /app                                     0.0s
     => CACHED [frontend 3/5] COPY package.json package-lock.json* ./          0.0s
     => CACHED [frontend 4/5] RUN npm ci                                       0.0s
     => [frontend 5/5] COPY . .                                                1.6s
     => [frontend] exporting to image                                          3.2s
     => => exporting layers                                                    2.6s
     => => exporting manifest sha256:5590f5beedb5d595cd6fbc523d956e6b20992436  0.0s
     => => exporting config sha256:658ecac42db2e44d58f45a370df44e07eb944c0984  0.0s
     => => exporting attestation manifest sha256:26da59865b0be310448478f2f05d  0.0s
     => => exporting manifest list sha256:d095aeb02035e25bbb67b5be219cf439526  0.0s
     => => naming to docker.io/library/compose-frontend:latest                 0.0s
     => => unpacking to docker.io/library/compose-frontend:latest              0.6s
     => [frontend] resolving provenance for metadata file                      0.0s
     => [backend 5/5] COPY app ./app                                           0.0s
     => [backend] exporting to image                                           0.9s
     => => exporting layers                                                    0.9s
    [?25h[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[0G[?25l[+] Building 9.4s (34/35)                                                       
     => [backend internal] load build context                                  0.0s
     => => transferring context: 9.45kB                                        0.0s
     => CACHED [backend 2/5] WORKDIR /app                                      0.0s
     => [backend 3/5] COPY requirements.txt .                                  0.0s
     => [backend 4/5] RUN pip install --no-cache-dir -r requirements.txt       7.1s
     => [browser] resolving provenance for metadata file                       0.0s
     => CACHED [frontend 2/5] WORKDIR /app                                     0.0s
     => CACHED [frontend 3/5] COPY package.json package-lock.json* ./          0.0s
     => CACHED [frontend 4/5] RUN npm ci                                       0.0s
     => [frontend 5/5] COPY . .                                                1.6s
     => [frontend] exporting to image                                          3.2s
     => => exporting layers                                                    2.6s
     => => exporting manifest sha256:5590f5beedb5d595cd6fbc523d956e6b20992436  0.0s
     => => exporting config sha256:658ecac42db2e44d58f45a370df44e07eb944c0984  0.0s
     => => exporting attestation manifest sha256:26da59865b0be310448478f2f05d  0.0s
     => => exporting manifest list sha256:d095aeb02035e25bbb67b5be219cf439526  0.0s
     => => naming to docker.io/library/compose-frontend:latest                 0.0s
     => => unpacking to docker.io/library/compose-frontend:latest              0.6s
     => [frontend] resolving provenance for metadata file                      0.0s
     => [backend 5/5] COPY app ./app                                           0.0s
     => [backend] exporting to image                                           1.1s
     => => exporting layers                                                    1.1s
    [?25h[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[0G[?25l[+] Building 9.4s (34/35)                                                       
     => [backend internal] load build context                                  0.0s
     => => transferring context: 9.45kB                                        0.0s
     => CACHED [backend 2/5] WORKDIR /app                                      0.0s
     => [backend 3/5] COPY requirements.txt .                                  0.0s
     => [backend 4/5] RUN pip install --no-cache-dir -r requirements.txt       7.1s
     => [browser] resolving provenance for metadata file                       0.0s
     => CACHED [frontend 2/5] WORKDIR /app                                     0.0s
     => CACHED [frontend 3/5] COPY package.json package-lock.json* ./          0.0s
     => CACHED [frontend 4/5] RUN npm ci                                       0.0s
     => [frontend 5/5] COPY . .                                                1.6s
     => [frontend] exporting to image                                          3.2s
     => => exporting layers                                                    2.6s
     => => exporting manifest sha256:5590f5beedb5d595cd6fbc523d956e6b20992436  0.0s
     => => exporting config sha256:658ecac42db2e44d58f45a370df44e07eb944c0984  0.0s
     => => exporting attestation manifest sha256:26da59865b0be310448478f2f05d  0.0s
     => => exporting manifest list sha256:d095aeb02035e25bbb67b5be219cf439526  0.0s
     => => naming to docker.io/library/compose-frontend:latest                 0.0s
     => => unpacking to docker.io/library/compose-frontend:latest              0.6s
     => [frontend] resolving provenance for metadata file                      0.0s
     => [backend 5/5] COPY app ./app                                           0.0s
     => [backend] exporting to image                                           1.2s
     => => exporting layers                                                    1.1s
    [?25h[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[0G[?25l[+] Building 9.6s (34/35)                                                       
     => CACHED [frontend 2/5] WORKDIR /app                                     0.0s
     => CACHED [frontend 3/5] COPY package.json package-lock.json* ./          0.0s
     => CACHED [frontend 4/5] RUN npm ci                                       0.0s
     => [frontend 5/5] COPY . .                                                1.6s
     => [frontend] exporting to image                                          3.2s
     => => exporting layers                                                    2.6s
     => => exporting manifest sha256:5590f5beedb5d595cd6fbc523d956e6b20992436  0.0s
     => => exporting config sha256:658ecac42db2e44d58f45a370df44e07eb944c0984  0.0s
     => => exporting attestation manifest sha256:26da59865b0be310448478f2f05d  0.0s
     => => exporting manifest list sha256:d095aeb02035e25bbb67b5be219cf439526  0.0s
     => => naming to docker.io/library/compose-frontend:latest                 0.0s
     => => unpacking to docker.io/library/compose-frontend:latest              0.6s
     => [frontend] resolving provenance for metadata file                      0.0s
     => [backend 5/5] COPY app ./app                                           0.0s
     => [backend] exporting to image                                           1.3s
     => => exporting layers                                                    1.1s
     => => exporting manifest sha256:d52d50b11a52da7ad4a201690850d349be3481c8  0.0s
     => => exporting config sha256:7dd0b90558f459ccfd1b319762f7601f0a2bab3ecc  0.0s
     => => exporting attestation manifest sha256:276ffdc12dbe7b454c5eb1b8fbf7  0.0s
     => => exporting manifest list sha256:2ab50fe8257cbb558d23b0155148fdac876  0.0s
     => => naming to docker.io/library/compose-backend:latest                  0.0s
     => => unpacking to docker.io/library/compose-backend:latest               0.2s
    [?25h[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[0G[?25l[+] Building 9.7s (34/35)                                                       
     => CACHED [frontend 2/5] WORKDIR /app                                     0.0s
     => CACHED [frontend 3/5] COPY package.json package-lock.json* ./          0.0s
     => CACHED [frontend 4/5] RUN npm ci                                       0.0s
     => [frontend 5/5] COPY . .                                                1.6s
     => [frontend] exporting to image                                          3.2s
     => => exporting layers                                                    2.6s
     => => exporting manifest sha256:5590f5beedb5d595cd6fbc523d956e6b20992436  0.0s
     => => exporting config sha256:658ecac42db2e44d58f45a370df44e07eb944c0984  0.0s
     => => exporting attestation manifest sha256:26da59865b0be310448478f2f05d  0.0s
     => => exporting manifest list sha256:d095aeb02035e25bbb67b5be219cf439526  0.0s
     => => naming to docker.io/library/compose-frontend:latest                 0.0s
     => => unpacking to docker.io/library/compose-frontend:latest              0.6s
     => [frontend] resolving provenance for metadata file                      0.0s
     => [backend 5/5] COPY app ./app                                           0.0s
     => [backend] exporting to image                                           1.4s
     => => exporting layers                                                    1.1s
     => => exporting manifest sha256:d52d50b11a52da7ad4a201690850d349be3481c8  0.0s
     => => exporting config sha256:7dd0b90558f459ccfd1b319762f7601f0a2bab3ecc  0.0s
     => => exporting attestation manifest sha256:276ffdc12dbe7b454c5eb1b8fbf7  0.0s
     => => exporting manifest list sha256:2ab50fe8257cbb558d23b0155148fdac876  0.0s
     => => naming to docker.io/library/compose-backend:latest                  0.0s
     => => unpacking to docker.io/library/compose-backend:latest               0.2s
    [?25h[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[1A[0G[?25l[+] Building 9.7s (36/36) FINISHED                                              
     => [internal] load local bake definitions                                 0.0s
     => => reading from stdin 1.44kB                                           0.0s
     => [frontend internal] load build definition from Dockerfile              0.0s
     => => transferring dockerfile: 146B                                       0.0s
     => [browser internal] load build definition from Dockerfile               0.0s
     => => transferring dockerfile: 367B                                       0.0s
     => [backend internal] load build definition from Dockerfile               0.0s
     => => transferring dockerfile: 209B                                       0.0s
     => [backend internal] load metadata for docker.io/library/python:3.12-sl  0.8s
     => [frontend internal] load metadata for docker.io/library/node:20-alpin  0.7s
     => [browser internal] load metadata for docker.io/library/node:20-bookwo  0.7s
     => [auth] library/node:pull token for registry-1.docker.io                0.0s
     => [auth] library/python:pull token for registry-1.docker.io              0.0s
     => [frontend internal] load .dockerignore                                 0.0s
     => => transferring context: 2B                                            0.0s
     => [browser internal] load .dockerignore                                  0.0s
     => => transferring context: 2B                                            0.0s
     => [frontend 1/5] FROM docker.io/library/node:20-alpine@sha256:f598378b5  0.0s
     => => resolve docker.io/library/node:20-alpine@sha256:f598378b5240225e6b  0.0s
     => [browser internal] load build context                                  0.0s
     => => transferring context: 72B                                           0.0s
     => [frontend internal] load build context                                 0.3s
     => => transferring context: 714.88kB                                      0.3s
     => [browser 1/5] FROM docker.io/library/node:20-bookworm-slim@sha256:1e8  0.0s
     => => resolve docker.io/library/node:20-bookworm-slim@sha256:1e85773c98c  0.0s
     => CACHED [browser 2/5] RUN apt-get update   && apt-get install -y --no-  0.0s
     => CACHED [browser 3/5] WORKDIR /workspace/tools/webapp-qa                0.0s
     => CACHED [browser 4/5] COPY package.json package-lock.json* ./           0.0s
     => CACHED [browser 5/5] RUN npm install                                   0.0s
     => [browser] exporting to image                                           0.1s
     => => exporting layers                                                    0.0s
     => => exporting manifest sha256:847eae24267fe1117d23f3e7bb5abb607bcdbbc4  0.0s
     => => exporting config sha256:bc8793160bb32391c252a551894eb1a94dbabdfdd3  0.0s
     => => exporting attestation manifest sha256:527eaadb6fabeaf976589861c443  0.0s
     => => exporting manifest list sha256:ef796cafeb2612f72bdffe9a1457a811287  0.0s
     => => naming to docker.io/library/compose-browser:latest                  0.0s
     => => unpacking to docker.io/library/compose-browser:latest               0.0s
     => [backend internal] load .dockerignore                                  0.0s
     => => transferring context: 2B                                            0.0s
     => [backend 1/5] FROM docker.io/library/python:3.12-slim@sha256:3d5ed973  0.0s
     => => resolve docker.io/library/python:3.12-slim@sha256:3d5ed973e45820f5  0.0s
     => [backend internal] load build context                                  0.0s
     => => transferring context: 9.45kB                                        0.0s
     => CACHED [backend 2/5] WORKDIR /app                                      0.0s
     => [backend 3/5] COPY requirements.txt .                                  0.0s
     => [backend 4/5] RUN pip install --no-cache-dir -r requirements.txt       7.1s
     => [browser] resolving provenance for metadata file                       0.0s
     => CACHED [frontend 2/5] WORKDIR /app                                     0.0s
     => CACHED [frontend 3/5] COPY package.json package-lock.json* ./          0.0s
     => CACHED [frontend 4/5] RUN npm ci                                       0.0s
     => [frontend 5/5] COPY . .                                                1.6s
     => [frontend] exporting to image                                          3.2s
     => => exporting layers                                                    2.6s
     => => exporting manifest sha256:5590f5beedb5d595cd6fbc523d956e6b20992436  0.0s
     => => exporting config sha256:658ecac42db2e44d58f45a370df44e07eb944c0984  0.0s
     => => exporting attestation manifest sha256:26da59865b0be310448478f2f05d  0.0s
     => => exporting manifest list sha256:d095aeb02035e25bbb67b5be219cf439526  0.0s
     => => naming to docker.io/library/compose-frontend:latest                 0.0s
     => => unpacking to docker.io/library/compose-frontend:latest              0.6s
     => [frontend] resolving provenance for metadata file                      0.0s
     => [backend 5/5] COPY app ./app                                           0.0s
     => [backend] exporting to image                                           1.4s
     => => exporting layers                                                    1.1s
     => => exporting manifest sha256:d52d50b11a52da7ad4a201690850d349be3481c8  0.0s
     => => exporting config sha256:7dd0b90558f459ccfd1b319762f7601f0a2bab3ecc  0.0s
     => => exporting attestation manifest sha256:276ffdc12dbe7b454c5eb1b8fbf7  0.0s
     => => exporting manifest list sha256:2ab50fe8257cbb558d23b0155148fdac876  0.0s
     => => naming to docker.io/library/compose-backend:latest                  0.0s
     => => unpacking to docker.io/library/compose-backend:latest               0.2s
     => [backend] resolving provenance for metadata file                       0.0s
    [?25h[?25l[0G[+] up 4/5
     ✔ Image compose-frontend      Built                                        9.8s
     ✔ Image compose-browser       Built                                        9.8s
     ✔ Image compose-backend       Built                                        9.8s
     ✔ Network compose_default     Created                                      0.0s
     ⠋ Container compose-backend-1 Creating                                     0.1s
    [?25h[?25l[6A[0G[+] up 5/6
     ✔ Image compose-frontend       Built                                       9.8s
     ✔ Image compose-browser        Built                                       9.8s
     ✔ Image compose-backend        Built                                       9.8s
     ✔ Network compose_default      Created                                     0.0s
     ✔ Container compose-backend-1  Created                                     0.1s
     ⠋ Container compose-frontend-1 Creating                                    0.1s
    [?25h[?25l[7A[0G[+] up 5/6
     ✔ Image compose-frontend       Built                                       9.8s
     ✔ Image compose-browser        Built                                       9.8s
     ✔ Image compose-backend        Built                                       9.8s
     ✔ Network compose_default      Created                                     0.0s
     ✔ Container compose-backend-1  Created                                     0.1s
     ⠙ Container compose-frontend-1 Creating                                    0.2s
    [?25h[?25l[7A[0G[+] up 5/6
     ✔ Image compose-frontend       Built                                       9.8s
     ✔ Image compose-browser        Built                                       9.8s
     ✔ Image compose-backend        Built                                       9.8s
     ✔ Network compose_default      Created                                     0.0s
     ✔ Container compose-backend-1  Created                                     0.1s
     ⠹ Container compose-frontend-1 Creating                                    0.3s
    [?25h[?25l[7A[0G[+] up 5/6
     ✔ Image compose-frontend       Built                                       9.8s
     ✔ Image compose-browser        Built                                       9.8s
     ✔ Image compose-backend        Built                                       9.8s
     ✔ Network compose_default      Created                                     0.0s
     ✔ Container compose-backend-1  Created                                     0.1s
     ⠸ Container compose-frontend-1 Creating                                    0.4s
    [?25h[?25l[7A[0G[+] up 5/6
     ✔ Image compose-frontend       Built                                       9.8s
     ✔ Image compose-browser        Built                                       9.8s
     ✔ Image compose-backend        Built                                       9.8s
     ✔ Network compose_default      Created                                     0.0s
     ✔ Container compose-backend-1  Created                                     0.1s
     ⠼ Container compose-frontend-1 Creating                                    0.5s
    [?25h[?25l[7A[0G[+] up 5/6
     ✔ Image compose-frontend       Built                                       9.8s
     ✔ Image compose-browser        Built                                       9.8s
     ✔ Image compose-backend        Built                                       9.8s
     ✔ Network compose_default      Created                                     0.0s
     ✔ Container compose-backend-1  Created                                     0.1s
     ⠴ Container compose-frontend-1 Creating                                    0.6s
    [?25h[?25l[7A[0G[+] up 5/6
     ✔ Image compose-frontend       Built                                       9.8s
     ✔ Image compose-browser        Built                                       9.8s
     ✔ Image compose-backend        Built                                       9.8s
     ✔ Network compose_default      Created                                     0.0s
     ✔ Container compose-backend-1  Created                                     0.1s
     ⠦ Container compose-frontend-1 Creating                                    0.7s
    [?25h[?25l[7A[0G[+] up 5/6
     ✔ Image compose-frontend       Built                                       9.8s
     ✔ Image compose-browser        Built                                       9.8s
     ✔ Image compose-backend        Built                                       9.8s
     ✔ Network compose_default      Created                                     0.0s
     ✔ Container compose-backend-1  Created                                     0.1s
     ⠧ Container compose-frontend-1 Creating                                    0.8s
    [?25h[?25l[7A[0G[+] up 5/6
     ✔ Image compose-frontend       Built                                       9.8s
     ✔ Image compose-browser        Built                                       9.8s
     ✔ Image compose-backend        Built                                       9.8s
     ✔ Network compose_default      Created                                     0.0s
     ✔ Container compose-backend-1  Created                                     0.1s
     ⠇ Container compose-frontend-1 Creating                                    0.9s
    [?25h[?25l[7A[0G[+] up 5/6
     ✔ Image compose-frontend       Built                                       9.8s
     ✔ Image compose-browser        Built                                       9.8s
     ✔ Image compose-backend        Built                                       9.8s
     ✔ Network compose_default      Created                                     0.0s
     ✔ Container compose-backend-1  Created                                     0.1s
     ⠏ Container compose-frontend-1 Creating                                    1.0s
    [?25h[?25l[7A[0G[+] up 5/6
     ✔ Image compose-frontend       Built                                       9.8s
     ✔ Image compose-browser        Built                                       9.8s
     ✔ Image compose-backend        Built                                       9.8s
     ✔ Network compose_default      Created                                     0.0s
     ✔ Container compose-backend-1  Created                                     0.1s
     ⠋ Container compose-frontend-1 Creating                                    1.1s
    [?25h[?25l[7A[0G[+] up 5/6
     ✔ Image compose-frontend       Built                                       9.8s
     ✔ Image compose-browser        Built                                       9.8s
     ✔ Image compose-backend        Built                                       9.8s
     ✔ Network compose_default      Created                                     0.0s
     ✔ Container compose-backend-1  Created                                     0.1s
     ⠙ Container compose-frontend-1 Creating                                    1.2s
    [?25h[?25l[7A[0G[+] up 5/6
     ✔ Image compose-frontend       Built                                       9.8s
     ✔ Image compose-browser        Built                                       9.8s
     ✔ Image compose-backend        Built                                       9.8s
     ✔ Network compose_default      Created                                     0.0s
     ✔ Container compose-backend-1  Created                                     0.1s
     ⠹ Container compose-frontend-1 Creating                                    1.3s
    [?25h[?25l[7A[0G[+] up 5/6
     ✔ Image compose-frontend       Built                                       9.8s
     ✔ Image compose-browser        Built                                       9.8s
     ✔ Image compose-backend        Built                                       9.8s
     ✔ Network compose_default      Created                                     0.0s
     ✔ Container compose-backend-1  Created                                     0.1s
     ⠸ Container compose-frontend-1 Creating                                    1.4s
    [?25h[?25l[7A[0G[+] up 5/6
     ✔ Image compose-frontend       Built                                       9.8s
     ✔ Image compose-browser        Built                                       9.8s
     ✔ Image compose-backend        Built                                       9.8s
     ✔ Network compose_default      Created                                     0.0s
     ✔ Container compose-backend-1  Created                                     0.1s
     ⠼ Container compose-frontend-1 Creating                                    1.5s
    [?25h[?25l[7A[0G[+] up 5/6
     ✔ Image compose-frontend       Built                                       9.8s
     ✔ Image compose-browser        Built                                       9.8s
     ✔ Image compose-backend        Built                                       9.8s
     ✔ Network compose_default      Created                                     0.0s
     ✔ Container compose-backend-1  Created                                     0.1s
     ⠴ Container compose-frontend-1 Creating                                    1.6s
    [?25h[?25l[7A[0G[+] up 5/6
     ✔ Image compose-frontend       Built                                       9.8s
     ✔ Image compose-browser        Built                                       9.8s
     ✔ Image compose-backend        Built                                       9.8s
     ✔ Network compose_default      Created                                     0.0s
     ✔ Container compose-backend-1  Created                                     0.1s
     ⠦ Container compose-frontend-1 Creating                                    1.7s
    [?25h[?25l[7A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                       9.8s
     ✔ Image compose-browser        Built                                       9.8s
     ✔ Image compose-backend        Built                                       9.8s
     ✔ Network compose_default      Created                                     0.0s
     ✔ Container compose-backend-1  Created                                     0.1s
     ✔ Container compose-frontend-1 Created                                     1.8s
     ⠋ Container compose-browser-1  Creating                                    0.0s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                       9.8s
     ✔ Image compose-browser        Built                                       9.8s
     ✔ Image compose-backend        Built                                       9.8s
     ✔ Network compose_default      Created                                     0.0s
     ⠙ Container compose-backend-1  Starting                                    2.0s
     ✔ Container compose-frontend-1 Created                                     1.8s
     ✔ Container compose-browser-1  Created                                     0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                       9.8s
     ✔ Image compose-browser        Built                                       9.8s
     ✔ Image compose-backend        Built                                       9.8s
     ✔ Network compose_default      Created                                     0.0s
     ⠹ Container compose-backend-1  Starting                                    2.1s
     ✔ Container compose-frontend-1 Created                                     1.8s
     ✔ Container compose-browser-1  Created                                     0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                       9.8s
     ✔ Image compose-browser        Built                                       9.8s
     ✔ Image compose-backend        Built                                       9.8s
     ✔ Network compose_default      Created                                     0.0s
     ⠸ Container compose-backend-1  Waiting                                     2.2s
     ✔ Container compose-frontend-1 Created                                     1.8s
     ✔ Container compose-browser-1  Created                                     0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                       9.8s
     ✔ Image compose-browser        Built                                       9.8s
     ✔ Image compose-backend        Built                                       9.8s
     ✔ Network compose_default      Created                                     0.0s
     ⠼ Container compose-backend-1  Waiting                                     2.3s
     ✔ Container compose-frontend-1 Created                                     1.8s
     ✔ Container compose-browser-1  Created                                     0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                       9.8s
     ✔ Image compose-browser        Built                                       9.8s
     ✔ Image compose-backend        Built                                       9.8s
     ✔ Network compose_default      Created                                     0.0s
     ⠴ Container compose-backend-1  Waiting                                     2.4s
     ✔ Container compose-frontend-1 Created                                     1.8s
     ✔ Container compose-browser-1  Created                                     0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                       9.8s
     ✔ Image compose-browser        Built                                       9.8s
     ✔ Image compose-backend        Built                                       9.8s
     ✔ Network compose_default      Created                                     0.0s
     ⠦ Container compose-backend-1  Waiting                                     2.5s
     ✔ Container compose-frontend-1 Created                                     1.8s
     ✔ Container compose-browser-1  Created                                     0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                       9.8s
     ✔ Image compose-browser        Built                                       9.8s
     ✔ Image compose-backend        Built                                       9.8s
     ✔ Network compose_default      Created                                     0.0s
     ⠧ Container compose-backend-1  Waiting                                     2.6s
     ✔ Container compose-frontend-1 Created                                     1.8s
     ✔ Container compose-browser-1  Created                                     0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                       9.8s
     ✔ Image compose-browser        Built                                       9.8s
     ✔ Image compose-backend        Built                                       9.8s
     ✔ Network compose_default      Created                                     0.0s
     ⠇ Container compose-backend-1  Waiting                                     2.7s
     ✔ Container compose-frontend-1 Created                                     1.8s
     ✔ Container compose-browser-1  Created                                     0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                       9.8s
     ✔ Image compose-browser        Built                                       9.8s
     ✔ Image compose-backend        Built                                       9.8s
     ✔ Network compose_default      Created                                     0.0s
     ⠏ Container compose-backend-1  Waiting                                     2.8s
     ✔ Container compose-frontend-1 Created                                     1.8s
     ✔ Container compose-browser-1  Created                                     0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                       9.8s
     ✔ Image compose-browser        Built                                       9.8s
     ✔ Image compose-backend        Built                                       9.8s
     ✔ Network compose_default      Created                                     0.0s
     ⠋ Container compose-backend-1  Waiting                                     2.9s
     ✔ Container compose-frontend-1 Created                                     1.8s
     ✔ Container compose-browser-1  Created                                     0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                       9.8s
     ✔ Image compose-browser        Built                                       9.8s
     ✔ Image compose-backend        Built                                       9.8s
     ✔ Network compose_default      Created                                     0.0s
     ⠙ Container compose-backend-1  Waiting                                     3.0s
     ✔ Container compose-frontend-1 Created                                     1.8s
     ✔ Container compose-browser-1  Created                                     0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                       9.8s
     ✔ Image compose-browser        Built                                       9.8s
     ✔ Image compose-backend        Built                                       9.8s
     ✔ Network compose_default      Created                                     0.0s
     ⠹ Container compose-backend-1  Waiting                                     3.1s
     ✔ Container compose-frontend-1 Created                                     1.8s
     ✔ Container compose-browser-1  Created                                     0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                       9.8s
     ✔ Image compose-browser        Built                                       9.8s
     ✔ Image compose-backend        Built                                       9.8s
     ✔ Network compose_default      Created                                     0.0s
     ⠸ Container compose-backend-1  Waiting                                     3.2s
     ✔ Container compose-frontend-1 Created                                     1.8s
     ✔ Container compose-browser-1  Created                                     0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                       9.8s
     ✔ Image compose-browser        Built                                       9.8s
     ✔ Image compose-backend        Built                                       9.8s
     ✔ Network compose_default      Created                                     0.0s
     ⠼ Container compose-backend-1  Waiting                                     3.3s
     ✔ Container compose-frontend-1 Created                                     1.8s
     ✔ Container compose-browser-1  Created                                     0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                       9.8s
     ✔ Image compose-browser        Built                                       9.8s
     ✔ Image compose-backend        Built                                       9.8s
     ✔ Network compose_default      Created                                     0.0s
     ⠴ Container compose-backend-1  Waiting                                     3.4s
     ✔ Container compose-frontend-1 Created                                     1.8s
     ✔ Container compose-browser-1  Created                                     0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                       9.8s
     ✔ Image compose-browser        Built                                       9.8s
     ✔ Image compose-backend        Built                                       9.8s
     ✔ Network compose_default      Created                                     0.0s
     ⠦ Container compose-backend-1  Waiting                                     3.5s
     ✔ Container compose-frontend-1 Created                                     1.8s
     ✔ Container compose-browser-1  Created                                     0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                       9.8s
     ✔ Image compose-browser        Built                                       9.8s
     ✔ Image compose-backend        Built                                       9.8s
     ✔ Network compose_default      Created                                     0.0s
     ⠧ Container compose-backend-1  Waiting                                     3.6s
     ✔ Container compose-frontend-1 Created                                     1.8s
     ✔ Container compose-browser-1  Created                                     0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                       9.8s
     ✔ Image compose-browser        Built                                       9.8s
     ✔ Image compose-backend        Built                                       9.8s
     ✔ Network compose_default      Created                                     0.0s
     ⠇ Container compose-backend-1  Waiting                                     3.7s
     ✔ Container compose-frontend-1 Created                                     1.8s
     ✔ Container compose-browser-1  Created                                     0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                       9.8s
     ✔ Image compose-browser        Built                                       9.8s
     ✔ Image compose-backend        Built                                       9.8s
     ✔ Network compose_default      Created                                     0.0s
     ⠏ Container compose-backend-1  Waiting                                     3.8s
     ✔ Container compose-frontend-1 Created                                     1.8s
     ✔ Container compose-browser-1  Created                                     0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                       9.8s
     ✔ Image compose-browser        Built                                       9.8s
     ✔ Image compose-backend        Built                                       9.8s
     ✔ Network compose_default      Created                                     0.0s
     ⠋ Container compose-backend-1  Waiting                                     3.9s
     ✔ Container compose-frontend-1 Created                                     1.8s
     ✔ Container compose-browser-1  Created                                     0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                       9.8s
     ✔ Image compose-browser        Built                                       9.8s
     ✔ Image compose-backend        Built                                       9.8s
     ✔ Network compose_default      Created                                     0.0s
     ⠙ Container compose-backend-1  Waiting                                     4.0s
     ✔ Container compose-frontend-1 Created                                     1.8s
     ✔ Container compose-browser-1  Created                                     0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                       9.8s
     ✔ Image compose-browser        Built                                       9.8s
     ✔ Image compose-backend        Built                                       9.8s
     ✔ Network compose_default      Created                                     0.0s
     ⠹ Container compose-backend-1  Waiting                                     4.1s
     ✔ Container compose-frontend-1 Created                                     1.8s
     ✔ Container compose-browser-1  Created                                     0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                       9.8s
     ✔ Image compose-browser        Built                                       9.8s
     ✔ Image compose-backend        Built                                       9.8s
     ✔ Network compose_default      Created                                     0.0s
     ⠸ Container compose-backend-1  Waiting                                     4.2s
     ✔ Container compose-frontend-1 Created                                     1.8s
     ✔ Container compose-browser-1  Created                                     0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                       9.8s
     ✔ Image compose-browser        Built                                       9.8s
     ✔ Image compose-backend        Built                                       9.8s
     ✔ Network compose_default      Created                                     0.0s
     ⠼ Container compose-backend-1  Waiting                                     4.3s
     ✔ Container compose-frontend-1 Created                                     1.8s
     ✔ Container compose-browser-1  Created                                     0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                       9.8s
     ✔ Image compose-browser        Built                                       9.8s
     ✔ Image compose-backend        Built                                       9.8s
     ✔ Network compose_default      Created                                     0.0s
     ⠴ Container compose-backend-1  Waiting                                     4.4s
     ✔ Container compose-frontend-1 Created                                     1.8s
     ✔ Container compose-browser-1  Created                                     0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                       9.8s
     ✔ Image compose-browser        Built                                       9.8s
     ✔ Image compose-backend        Built                                       9.8s
     ✔ Network compose_default      Created                                     0.0s
     ⠦ Container compose-backend-1  Waiting                                     4.5s
     ✔ Container compose-frontend-1 Created                                     1.8s
     ✔ Container compose-browser-1  Created                                     0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                       9.8s
     ✔ Image compose-browser        Built                                       9.8s
     ✔ Image compose-backend        Built                                       9.8s
     ✔ Network compose_default      Created                                     0.0s
     ⠧ Container compose-backend-1  Waiting                                     4.6s
     ✔ Container compose-frontend-1 Created                                     1.8s
     ✔ Container compose-browser-1  Created                                     0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                       9.8s
     ✔ Image compose-browser        Built                                       9.8s
     ✔ Image compose-backend        Built                                       9.8s
     ✔ Network compose_default      Created                                     0.0s
     ⠇ Container compose-backend-1  Waiting                                     4.7s
     ✔ Container compose-frontend-1 Created                                     1.8s
     ✔ Container compose-browser-1  Created                                     0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                       9.8s
     ✔ Image compose-browser        Built                                       9.8s
     ✔ Image compose-backend        Built                                       9.8s
     ✔ Network compose_default      Created                                     0.0s
     ⠏ Container compose-backend-1  Waiting                                     4.8s
     ✔ Container compose-frontend-1 Created                                     1.8s
     ✔ Container compose-browser-1  Created                                     0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                       9.8s
     ✔ Image compose-browser        Built                                       9.8s
     ✔ Image compose-backend        Built                                       9.8s
     ✔ Network compose_default      Created                                     0.0s
     ⠋ Container compose-backend-1  Waiting                                     4.9s
     ✔ Container compose-frontend-1 Created                                     1.8s
     ✔ Container compose-browser-1  Created                                     0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                       9.8s
     ✔ Image compose-browser        Built                                       9.8s
     ✔ Image compose-backend        Built                                       9.8s
     ✔ Network compose_default      Created                                     0.0s
     ⠙ Container compose-backend-1  Waiting                                     5.0s
     ✔ Container compose-frontend-1 Created                                     1.8s
     ✔ Container compose-browser-1  Created                                     0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                       9.8s
     ✔ Image compose-browser        Built                                       9.8s
     ✔ Image compose-backend        Built                                       9.8s
     ✔ Network compose_default      Created                                     0.0s
     ⠹ Container compose-backend-1  Waiting                                     5.1s
     ✔ Container compose-frontend-1 Created                                     1.8s
     ✔ Container compose-browser-1  Created                                     0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                       9.8s
     ✔ Image compose-browser        Built                                       9.8s
     ✔ Image compose-backend        Built                                       9.8s
     ✔ Network compose_default      Created                                     0.0s
     ⠸ Container compose-backend-1  Waiting                                     5.2s
     ✔ Container compose-frontend-1 Created                                     1.8s
     ✔ Container compose-browser-1  Created                                     0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                       9.8s
     ✔ Image compose-browser        Built                                       9.8s
     ✔ Image compose-backend        Built                                       9.8s
     ✔ Network compose_default      Created                                     0.0s
     ⠼ Container compose-backend-1  Waiting                                     5.3s
     ✔ Container compose-frontend-1 Created                                     1.8s
     ✔ Container compose-browser-1  Created                                     0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                       9.8s
     ✔ Image compose-browser        Built                                       9.8s
     ✔ Image compose-backend        Built                                       9.8s
     ✔ Network compose_default      Created                                     0.0s
     ⠴ Container compose-backend-1  Waiting                                     5.4s
     ✔ Container compose-frontend-1 Created                                     1.8s
     ✔ Container compose-browser-1  Created                                     0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                       9.8s
     ✔ Image compose-browser        Built                                       9.8s
     ✔ Image compose-backend        Built                                       9.8s
     ✔ Network compose_default      Created                                     0.0s
     ⠦ Container compose-backend-1  Waiting                                     5.5s
     ✔ Container compose-frontend-1 Created                                     1.8s
     ✔ Container compose-browser-1  Created                                     0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                       9.8s
     ✔ Image compose-browser        Built                                       9.8s
     ✔ Image compose-backend        Built                                       9.8s
     ✔ Network compose_default      Created                                     0.0s
     ⠧ Container compose-backend-1  Waiting                                     5.6s
     ✔ Container compose-frontend-1 Created                                     1.8s
     ✔ Container compose-browser-1  Created                                     0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                       9.8s
     ✔ Image compose-browser        Built                                       9.8s
     ✔ Image compose-backend        Built                                       9.8s
     ✔ Network compose_default      Created                                     0.0s
     ⠇ Container compose-backend-1  Waiting                                     5.7s
     ✔ Container compose-frontend-1 Created                                     1.8s
     ✔ Container compose-browser-1  Created                                     0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                       9.8s
     ✔ Image compose-browser        Built                                       9.8s
     ✔ Image compose-backend        Built                                       9.8s
     ✔ Network compose_default      Created                                     0.0s
     ⠏ Container compose-backend-1  Waiting                                     5.8s
     ✔ Container compose-frontend-1 Created                                     1.8s
     ✔ Container compose-browser-1  Created                                     0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                       9.8s
     ✔ Image compose-browser        Built                                       9.8s
     ✔ Image compose-backend        Built                                       9.8s
     ✔ Network compose_default      Created                                     0.0s
     ⠋ Container compose-backend-1  Waiting                                     5.9s
     ✔ Container compose-frontend-1 Created                                     1.8s
     ✔ Container compose-browser-1  Created                                     0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                       9.8s
     ✔ Image compose-browser        Built                                       9.8s
     ✔ Image compose-backend        Built                                       9.8s
     ✔ Network compose_default      Created                                     0.0s
     ⠙ Container compose-backend-1  Waiting                                     6.0s
     ✔ Container compose-frontend-1 Created                                     1.8s
     ✔ Container compose-browser-1  Created                                     0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                       9.8s
     ✔ Image compose-browser        Built                                       9.8s
     ✔ Image compose-backend        Built                                       9.8s
     ✔ Network compose_default      Created                                     0.0s
     ⠹ Container compose-backend-1  Waiting                                     6.1s
     ✔ Container compose-frontend-1 Created                                     1.8s
     ✔ Container compose-browser-1  Created                                     0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                       9.8s
     ✔ Image compose-browser        Built                                       9.8s
     ✔ Image compose-backend        Built                                       9.8s
     ✔ Network compose_default      Created                                     0.0s
     ⠸ Container compose-backend-1  Waiting                                     6.2s
     ✔ Container compose-frontend-1 Created                                     1.8s
     ✔ Container compose-browser-1  Created                                     0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                       9.8s
     ✔ Image compose-browser        Built                                       9.8s
     ✔ Image compose-backend        Built                                       9.8s
     ✔ Network compose_default      Created                                     0.0s
     ⠼ Container compose-backend-1  Waiting                                     6.3s
     ✔ Container compose-frontend-1 Created                                     1.8s
     ✔ Container compose-browser-1  Created                                     0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                       9.8s
     ✔ Image compose-browser        Built                                       9.8s
     ✔ Image compose-backend        Built                                       9.8s
     ✔ Network compose_default      Created                                     0.0s
     ⠴ Container compose-backend-1  Waiting                                     6.4s
     ✔ Container compose-frontend-1 Created                                     1.8s
     ✔ Container compose-browser-1  Created                                     0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                       9.8s
     ✔ Image compose-browser        Built                                       9.8s
     ✔ Image compose-backend        Built                                       9.8s
     ✔ Network compose_default      Created                                     0.0s
     ⠦ Container compose-backend-1  Waiting                                     6.5s
     ✔ Container compose-frontend-1 Created                                     1.8s
     ✔ Container compose-browser-1  Created                                     0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                       9.8s
     ✔ Image compose-browser        Built                                       9.8s
     ✔ Image compose-backend        Built                                       9.8s
     ✔ Network compose_default      Created                                     0.0s
     ⠧ Container compose-backend-1  Waiting                                     6.6s
     ✔ Container compose-frontend-1 Created                                     1.8s
     ✔ Container compose-browser-1  Created                                     0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                       9.8s
     ✔ Image compose-browser        Built                                       9.8s
     ✔ Image compose-backend        Built                                       9.8s
     ✔ Network compose_default      Created                                     0.0s
     ⠇ Container compose-backend-1  Waiting                                     6.7s
     ✔ Container compose-frontend-1 Created                                     1.8s
     ✔ Container compose-browser-1  Created                                     0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                       9.8s
     ✔ Image compose-browser        Built                                       9.8s
     ✔ Image compose-backend        Built                                       9.8s
     ✔ Network compose_default      Created                                     0.0s
     ⠏ Container compose-backend-1  Waiting                                     6.8s
     ✔ Container compose-frontend-1 Created                                     1.8s
     ✔ Container compose-browser-1  Created                                     0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                       9.8s
     ✔ Image compose-browser        Built                                       9.8s
     ✔ Image compose-backend        Built                                       9.8s
     ✔ Network compose_default      Created                                     0.0s
     ⠋ Container compose-backend-1  Waiting                                     6.9s
     ✔ Container compose-frontend-1 Created                                     1.8s
     ✔ Container compose-browser-1  Created                                     0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                       9.8s
     ✔ Image compose-browser        Built                                       9.8s
     ✔ Image compose-backend        Built                                       9.8s
     ✔ Network compose_default      Created                                     0.0s
     ⠙ Container compose-backend-1  Waiting                                     7.0s
     ✔ Container compose-frontend-1 Created                                     1.8s
     ✔ Container compose-browser-1  Created                                     0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                       9.8s
     ✔ Image compose-browser        Built                                       9.8s
     ✔ Image compose-backend        Built                                       9.8s
     ✔ Network compose_default      Created                                     0.0s
     ⠹ Container compose-backend-1  Waiting                                     7.1s
     ✔ Container compose-frontend-1 Created                                     1.8s
     ✔ Container compose-browser-1  Created                                     0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                       9.8s
     ✔ Image compose-browser        Built                                       9.8s
     ✔ Image compose-backend        Built                                       9.8s
     ✔ Network compose_default      Created                                     0.0s
     ⠸ Container compose-backend-1  Waiting                                     7.2s
     ✔ Container compose-frontend-1 Created                                     1.8s
     ✔ Container compose-browser-1  Created                                     0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                       9.8s
     ✔ Image compose-browser        Built                                       9.8s
     ✔ Image compose-backend        Built                                       9.8s
     ✔ Network compose_default      Created                                     0.0s
     ⠼ Container compose-backend-1  Waiting                                     7.3s
     ✔ Container compose-frontend-1 Created                                     1.8s
     ✔ Container compose-browser-1  Created                                     0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                       9.8s
     ✔ Image compose-browser        Built                                       9.8s
     ✔ Image compose-backend        Built                                       9.8s
     ✔ Network compose_default      Created                                     0.0s
     ⠴ Container compose-backend-1  Waiting                                     7.4s
     ✔ Container compose-frontend-1 Created                                     1.8s
     ✔ Container compose-browser-1  Created                                     0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                       9.8s
     ✔ Image compose-browser        Built                                       9.8s
     ✔ Image compose-backend        Built                                       9.8s
     ✔ Network compose_default      Created                                     0.0s
     ⠦ Container compose-backend-1  Waiting                                     7.5s
     ✔ Container compose-frontend-1 Created                                     1.8s
     ✔ Container compose-browser-1  Created                                     0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                       9.8s
     ✔ Image compose-browser        Built                                       9.8s
     ✔ Image compose-backend        Built                                       9.8s
     ✔ Network compose_default      Created                                     0.0s
     ⠧ Container compose-backend-1  Waiting                                     7.6s
     ✔ Container compose-frontend-1 Created                                     1.8s
     ✔ Container compose-browser-1  Created                                     0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                       9.8s
     ✔ Image compose-browser        Built                                       9.8s
     ✔ Image compose-backend        Built                                       9.8s
     ✔ Network compose_default      Created                                     0.0s
     ✔ Container compose-backend-1  Healthy                                     7.7s
     ⠧ Container compose-frontend-1 Starting                                    7.6s
     ✔ Container compose-browser-1  Created                                     0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                       9.8s
     ✔ Image compose-browser        Built                                       9.8s
     ✔ Image compose-backend        Built                                       9.8s
     ✔ Network compose_default      Created                                     0.0s
     ✔ Container compose-backend-1  Healthy                                     7.7s
     ⠇ Container compose-frontend-1 Waiting                                     7.7s
     ✔ Container compose-browser-1  Created                                     0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                       9.8s
     ✔ Image compose-browser        Built                                       9.8s
     ✔ Image compose-backend        Built                                       9.8s
     ✔ Network compose_default      Created                                     0.0s
     ✔ Container compose-backend-1  Healthy                                     7.7s
     ⠏ Container compose-frontend-1 Waiting                                     7.8s
     ✔ Container compose-browser-1  Created                                     0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                       9.8s
     ✔ Image compose-browser        Built                                       9.8s
     ✔ Image compose-backend        Built                                       9.8s
     ✔ Network compose_default      Created                                     0.0s
     ✔ Container compose-backend-1  Healthy                                     7.7s
     ⠋ Container compose-frontend-1 Waiting                                     7.9s
     ✔ Container compose-browser-1  Created                                     0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                       9.8s
     ✔ Image compose-browser        Built                                       9.8s
     ✔ Image compose-backend        Built                                       9.8s
     ✔ Network compose_default      Created                                     0.0s
     ✔ Container compose-backend-1  Healthy                                     7.7s
     ⠙ Container compose-frontend-1 Waiting                                     8.0s
     ✔ Container compose-browser-1  Created                                     0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                       9.8s
     ✔ Image compose-browser        Built                                       9.8s
     ✔ Image compose-backend        Built                                       9.8s
     ✔ Network compose_default      Created                                     0.0s
     ✔ Container compose-backend-1  Healthy                                     7.7s
     ⠹ Container compose-frontend-1 Waiting                                     8.1s
     ✔ Container compose-browser-1  Created                                     0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                       9.8s
     ✔ Image compose-browser        Built                                       9.8s
     ✔ Image compose-backend        Built                                       9.8s
     ✔ Network compose_default      Created                                     0.0s
     ✔ Container compose-backend-1  Healthy                                     7.7s
     ⠸ Container compose-frontend-1 Waiting                                     8.2s
     ✔ Container compose-browser-1  Created                                     0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                       9.8s
     ✔ Image compose-browser        Built                                       9.8s
     ✔ Image compose-backend        Built                                       9.8s
     ✔ Network compose_default      Created                                     0.0s
     ✔ Container compose-backend-1  Healthy                                     7.7s
     ⠼ Container compose-frontend-1 Waiting                                     8.3s
     ✔ Container compose-browser-1  Created                                     0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                       9.8s
     ✔ Image compose-browser        Built                                       9.8s
     ✔ Image compose-backend        Built                                       9.8s
     ✔ Network compose_default      Created                                     0.0s
     ✔ Container compose-backend-1  Healthy                                     7.7s
     ⠴ Container compose-frontend-1 Waiting                                     8.4s
     ✔ Container compose-browser-1  Created                                     0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                       9.8s
     ✔ Image compose-browser        Built                                       9.8s
     ✔ Image compose-backend        Built                                       9.8s
     ✔ Network compose_default      Created                                     0.0s
     ✔ Container compose-backend-1  Healthy                                     7.7s
     ⠦ Container compose-frontend-1 Waiting                                     8.5s
     ✔ Container compose-browser-1  Created                                     0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                       9.8s
     ✔ Image compose-browser        Built                                       9.8s
     ✔ Image compose-backend        Built                                       9.8s
     ✔ Network compose_default      Created                                     0.0s
     ✔ Container compose-backend-1  Healthy                                     7.7s
     ⠧ Container compose-frontend-1 Waiting                                     8.6s
     ✔ Container compose-browser-1  Created                                     0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                       9.8s
     ✔ Image compose-browser        Built                                       9.8s
     ✔ Image compose-backend        Built                                       9.8s
     ✔ Network compose_default      Created                                     0.0s
     ✔ Container compose-backend-1  Healthy                                     7.7s
     ⠇ Container compose-frontend-1 Waiting                                     8.7s
     ✔ Container compose-browser-1  Created                                     0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                       9.8s
     ✔ Image compose-browser        Built                                       9.8s
     ✔ Image compose-backend        Built                                       9.8s
     ✔ Network compose_default      Created                                     0.0s
     ✔ Container compose-backend-1  Healthy                                     7.7s
     ⠏ Container compose-frontend-1 Waiting                                     8.8s
     ✔ Container compose-browser-1  Created                                     0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                       9.8s
     ✔ Image compose-browser        Built                                       9.8s
     ✔ Image compose-backend        Built                                       9.8s
     ✔ Network compose_default      Created                                     0.0s
     ✔ Container compose-backend-1  Healthy                                     7.7s
     ⠋ Container compose-frontend-1 Waiting                                     8.9s
     ✔ Container compose-browser-1  Created                                     0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                       9.8s
     ✔ Image compose-browser        Built                                       9.8s
     ✔ Image compose-backend        Built                                       9.8s
     ✔ Network compose_default      Created                                     0.0s
     ✔ Container compose-backend-1  Healthy                                     7.7s
     ⠙ Container compose-frontend-1 Waiting                                     9.0s
     ✔ Container compose-browser-1  Created                                     0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                       9.8s
     ✔ Image compose-browser        Built                                       9.8s
     ✔ Image compose-backend        Built                                       9.8s
     ✔ Network compose_default      Created                                     0.0s
     ✔ Container compose-backend-1  Healthy                                     7.7s
     ⠹ Container compose-frontend-1 Waiting                                     9.1s
     ✔ Container compose-browser-1  Created                                     0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                       9.8s
     ✔ Image compose-browser        Built                                       9.8s
     ✔ Image compose-backend        Built                                       9.8s
     ✔ Network compose_default      Created                                     0.0s
     ✔ Container compose-backend-1  Healthy                                     7.7s
     ⠸ Container compose-frontend-1 Waiting                                     9.2s
     ✔ Container compose-browser-1  Created                                     0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                       9.8s
     ✔ Image compose-browser        Built                                       9.8s
     ✔ Image compose-backend        Built                                       9.8s
     ✔ Network compose_default      Created                                     0.0s
     ✔ Container compose-backend-1  Healthy                                     7.7s
     ⠼ Container compose-frontend-1 Waiting                                     9.3s
     ✔ Container compose-browser-1  Created                                     0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                       9.8s
     ✔ Image compose-browser        Built                                       9.8s
     ✔ Image compose-backend        Built                                       9.8s
     ✔ Network compose_default      Created                                     0.0s
     ✔ Container compose-backend-1  Healthy                                     7.7s
     ⠴ Container compose-frontend-1 Waiting                                     9.4s
     ✔ Container compose-browser-1  Created                                     0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                       9.8s
     ✔ Image compose-browser        Built                                       9.8s
     ✔ Image compose-backend        Built                                       9.8s
     ✔ Network compose_default      Created                                     0.0s
     ✔ Container compose-backend-1  Healthy                                     7.7s
     ⠦ Container compose-frontend-1 Waiting                                     9.5s
     ✔ Container compose-browser-1  Created                                     0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                       9.8s
     ✔ Image compose-browser        Built                                       9.8s
     ✔ Image compose-backend        Built                                       9.8s
     ✔ Network compose_default      Created                                     0.0s
     ✔ Container compose-backend-1  Healthy                                     7.7s
     ⠧ Container compose-frontend-1 Waiting                                     9.6s
     ✔ Container compose-browser-1  Created                                     0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                       9.8s
     ✔ Image compose-browser        Built                                       9.8s
     ✔ Image compose-backend        Built                                       9.8s
     ✔ Network compose_default      Created                                     0.0s
     ✔ Container compose-backend-1  Healthy                                     7.7s
     ⠇ Container compose-frontend-1 Waiting                                     9.7s
     ✔ Container compose-browser-1  Created                                     0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                       9.8s
     ✔ Image compose-browser        Built                                       9.8s
     ✔ Image compose-backend        Built                                       9.8s
     ✔ Network compose_default      Created                                     0.0s
     ✔ Container compose-backend-1  Healthy                                     7.7s
     ⠏ Container compose-frontend-1 Waiting                                     9.8s
     ✔ Container compose-browser-1  Created                                     0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                       9.8s
     ✔ Image compose-browser        Built                                       9.8s
     ✔ Image compose-backend        Built                                       9.8s
     ✔ Network compose_default      Created                                     0.0s
     ✔ Container compose-backend-1  Healthy                                     7.7s
     ⠋ Container compose-frontend-1 Waiting                                     9.9s
     ✔ Container compose-browser-1  Created                                     0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                      9.8s
     ✔ Image compose-browser        Built                                      9.8s
     ✔ Image compose-backend        Built                                      9.8s
     ✔ Network compose_default      Created                                    0.0s
     ✔ Container compose-backend-1  Healthy                                    7.7s
     ⠙ Container compose-frontend-1 Waiting                                    10.0s
     ✔ Container compose-browser-1  Created                                    0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                      9.8s
     ✔ Image compose-browser        Built                                      9.8s
     ✔ Image compose-backend        Built                                      9.8s
     ✔ Network compose_default      Created                                    0.0s
     ✔ Container compose-backend-1  Healthy                                    7.7s
     ⠹ Container compose-frontend-1 Waiting                                    10.1s
     ✔ Container compose-browser-1  Created                                    0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                      9.8s
     ✔ Image compose-browser        Built                                      9.8s
     ✔ Image compose-backend        Built                                      9.8s
     ✔ Network compose_default      Created                                    0.0s
     ✔ Container compose-backend-1  Healthy                                    7.7s
     ⠸ Container compose-frontend-1 Waiting                                    10.2s
     ✔ Container compose-browser-1  Created                                    0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                      9.8s
     ✔ Image compose-browser        Built                                      9.8s
     ✔ Image compose-backend        Built                                      9.8s
     ✔ Network compose_default      Created                                    0.0s
     ✔ Container compose-backend-1  Healthy                                    7.7s
     ⠼ Container compose-frontend-1 Waiting                                    10.3s
     ✔ Container compose-browser-1  Created                                    0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                      9.8s
     ✔ Image compose-browser        Built                                      9.8s
     ✔ Image compose-backend        Built                                      9.8s
     ✔ Network compose_default      Created                                    0.0s
     ✔ Container compose-backend-1  Healthy                                    7.7s
     ⠴ Container compose-frontend-1 Waiting                                    10.4s
     ✔ Container compose-browser-1  Created                                    0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                      9.8s
     ✔ Image compose-browser        Built                                      9.8s
     ✔ Image compose-backend        Built                                      9.8s
     ✔ Network compose_default      Created                                    0.0s
     ✔ Container compose-backend-1  Healthy                                    7.7s
     ⠦ Container compose-frontend-1 Waiting                                    10.5s
     ✔ Container compose-browser-1  Created                                    0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                      9.8s
     ✔ Image compose-browser        Built                                      9.8s
     ✔ Image compose-backend        Built                                      9.8s
     ✔ Network compose_default      Created                                    0.0s
     ✔ Container compose-backend-1  Healthy                                    7.7s
     ⠧ Container compose-frontend-1 Waiting                                    10.6s
     ✔ Container compose-browser-1  Created                                    0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                      9.8s
     ✔ Image compose-browser        Built                                      9.8s
     ✔ Image compose-backend        Built                                      9.8s
     ✔ Network compose_default      Created                                    0.0s
     ✔ Container compose-backend-1  Healthy                                    7.7s
     ⠇ Container compose-frontend-1 Waiting                                    10.7s
     ✔ Container compose-browser-1  Created                                    0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                      9.8s
     ✔ Image compose-browser        Built                                      9.8s
     ✔ Image compose-backend        Built                                      9.8s
     ✔ Network compose_default      Created                                    0.0s
     ✔ Container compose-backend-1  Healthy                                    7.7s
     ⠏ Container compose-frontend-1 Waiting                                    10.8s
     ✔ Container compose-browser-1  Created                                    0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                      9.8s
     ✔ Image compose-browser        Built                                      9.8s
     ✔ Image compose-backend        Built                                      9.8s
     ✔ Network compose_default      Created                                    0.0s
     ✔ Container compose-backend-1  Healthy                                    7.7s
     ⠋ Container compose-frontend-1 Waiting                                    10.9s
     ✔ Container compose-browser-1  Created                                    0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                      9.8s
     ✔ Image compose-browser        Built                                      9.8s
     ✔ Image compose-backend        Built                                      9.8s
     ✔ Network compose_default      Created                                    0.0s
     ✔ Container compose-backend-1  Healthy                                    7.7s
     ⠙ Container compose-frontend-1 Waiting                                    11.0s
     ✔ Container compose-browser-1  Created                                    0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                      9.8s
     ✔ Image compose-browser        Built                                      9.8s
     ✔ Image compose-backend        Built                                      9.8s
     ✔ Network compose_default      Created                                    0.0s
     ✔ Container compose-backend-1  Healthy                                    7.7s
     ⠹ Container compose-frontend-1 Waiting                                    11.1s
     ✔ Container compose-browser-1  Created                                    0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                      9.8s
     ✔ Image compose-browser        Built                                      9.8s
     ✔ Image compose-backend        Built                                      9.8s
     ✔ Network compose_default      Created                                    0.0s
     ✔ Container compose-backend-1  Healthy                                    7.7s
     ⠸ Container compose-frontend-1 Waiting                                    11.2s
     ✔ Container compose-browser-1  Created                                    0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                      9.8s
     ✔ Image compose-browser        Built                                      9.8s
     ✔ Image compose-backend        Built                                      9.8s
     ✔ Network compose_default      Created                                    0.0s
     ✔ Container compose-backend-1  Healthy                                    7.7s
     ⠼ Container compose-frontend-1 Waiting                                    11.3s
     ✔ Container compose-browser-1  Created                                    0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                      9.8s
     ✔ Image compose-browser        Built                                      9.8s
     ✔ Image compose-backend        Built                                      9.8s
     ✔ Network compose_default      Created                                    0.0s
     ✔ Container compose-backend-1  Healthy                                    7.7s
     ⠴ Container compose-frontend-1 Waiting                                    11.4s
     ✔ Container compose-browser-1  Created                                    0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                      9.8s
     ✔ Image compose-browser        Built                                      9.8s
     ✔ Image compose-backend        Built                                      9.8s
     ✔ Network compose_default      Created                                    0.0s
     ✔ Container compose-backend-1  Healthy                                    7.7s
     ⠦ Container compose-frontend-1 Waiting                                    11.5s
     ✔ Container compose-browser-1  Created                                    0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                      9.8s
     ✔ Image compose-browser        Built                                      9.8s
     ✔ Image compose-backend        Built                                      9.8s
     ✔ Network compose_default      Created                                    0.0s
     ✔ Container compose-backend-1  Healthy                                    7.7s
     ⠧ Container compose-frontend-1 Waiting                                    11.6s
     ✔ Container compose-browser-1  Created                                    0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                      9.8s
     ✔ Image compose-browser        Built                                      9.8s
     ✔ Image compose-backend        Built                                      9.8s
     ✔ Network compose_default      Created                                    0.0s
     ✔ Container compose-backend-1  Healthy                                    7.7s
     ⠇ Container compose-frontend-1 Waiting                                    11.7s
     ✔ Container compose-browser-1  Created                                    0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                      9.8s
     ✔ Image compose-browser        Built                                      9.8s
     ✔ Image compose-backend        Built                                      9.8s
     ✔ Network compose_default      Created                                    0.0s
     ✔ Container compose-backend-1  Healthy                                    7.7s
     ⠏ Container compose-frontend-1 Waiting                                    11.8s
     ✔ Container compose-browser-1  Created                                    0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                      9.8s
     ✔ Image compose-browser        Built                                      9.8s
     ✔ Image compose-backend        Built                                      9.8s
     ✔ Network compose_default      Created                                    0.0s
     ✔ Container compose-backend-1  Healthy                                    7.7s
     ⠋ Container compose-frontend-1 Waiting                                    11.9s
     ✔ Container compose-browser-1  Created                                    0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                      9.8s
     ✔ Image compose-browser        Built                                      9.8s
     ✔ Image compose-backend        Built                                      9.8s
     ✔ Network compose_default      Created                                    0.0s
     ✔ Container compose-backend-1  Healthy                                    7.7s
     ⠙ Container compose-frontend-1 Waiting                                    12.0s
     ✔ Container compose-browser-1  Created                                    0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                      9.8s
     ✔ Image compose-browser        Built                                      9.8s
     ✔ Image compose-backend        Built                                      9.8s
     ✔ Network compose_default      Created                                    0.0s
     ✔ Container compose-backend-1  Healthy                                    7.7s
     ⠹ Container compose-frontend-1 Waiting                                    12.1s
     ✔ Container compose-browser-1  Created                                    0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                      9.8s
     ✔ Image compose-browser        Built                                      9.8s
     ✔ Image compose-backend        Built                                      9.8s
     ✔ Network compose_default      Created                                    0.0s
     ✔ Container compose-backend-1  Healthy                                    7.7s
     ⠸ Container compose-frontend-1 Waiting                                    12.2s
     ✔ Container compose-browser-1  Created                                    0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                      9.8s
     ✔ Image compose-browser        Built                                      9.8s
     ✔ Image compose-backend        Built                                      9.8s
     ✔ Network compose_default      Created                                    0.0s
     ✔ Container compose-backend-1  Healthy                                    7.7s
     ⠼ Container compose-frontend-1 Waiting                                    12.3s
     ✔ Container compose-browser-1  Created                                    0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                      9.8s
     ✔ Image compose-browser        Built                                      9.8s
     ✔ Image compose-backend        Built                                      9.8s
     ✔ Network compose_default      Created                                    0.0s
     ✔ Container compose-backend-1  Healthy                                    7.7s
     ⠴ Container compose-frontend-1 Waiting                                    12.4s
     ✔ Container compose-browser-1  Created                                    0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                      9.8s
     ✔ Image compose-browser        Built                                      9.8s
     ✔ Image compose-backend        Built                                      9.8s
     ✔ Network compose_default      Created                                    0.0s
     ✔ Container compose-backend-1  Healthy                                    7.7s
     ⠦ Container compose-frontend-1 Waiting                                    12.5s
     ✔ Container compose-browser-1  Created                                    0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                      9.8s
     ✔ Image compose-browser        Built                                      9.8s
     ✔ Image compose-backend        Built                                      9.8s
     ✔ Network compose_default      Created                                    0.0s
     ✔ Container compose-backend-1  Healthy                                    7.7s
     ⠧ Container compose-frontend-1 Waiting                                    12.6s
     ✔ Container compose-browser-1  Created                                    0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                      9.8s
     ✔ Image compose-browser        Built                                      9.8s
     ✔ Image compose-backend        Built                                      9.8s
     ✔ Network compose_default      Created                                    0.0s
     ✔ Container compose-backend-1  Healthy                                    7.7s
     ⠇ Container compose-frontend-1 Waiting                                    12.7s
     ✔ Container compose-browser-1  Created                                    0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                      9.8s
     ✔ Image compose-browser        Built                                      9.8s
     ✔ Image compose-backend        Built                                      9.8s
     ✔ Network compose_default      Created                                    0.0s
     ✔ Container compose-backend-1  Healthy                                    7.7s
     ⠏ Container compose-frontend-1 Waiting                                    12.8s
     ✔ Container compose-browser-1  Created                                    0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                      9.8s
     ✔ Image compose-browser        Built                                      9.8s
     ✔ Image compose-backend        Built                                      9.8s
     ✔ Network compose_default      Created                                    0.0s
     ✔ Container compose-backend-1  Healthy                                    7.7s
     ⠋ Container compose-frontend-1 Waiting                                    12.9s
     ✔ Container compose-browser-1  Created                                    0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                      9.8s
     ✔ Image compose-browser        Built                                      9.8s
     ✔ Image compose-backend        Built                                      9.8s
     ✔ Network compose_default      Created                                    0.0s
     ✔ Container compose-backend-1  Healthy                                    7.7s
     ⠙ Container compose-frontend-1 Waiting                                    13.0s
     ✔ Container compose-browser-1  Created                                    0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                      9.8s
     ✔ Image compose-browser        Built                                      9.8s
     ✔ Image compose-backend        Built                                      9.8s
     ✔ Network compose_default      Created                                    0.0s
     ✔ Container compose-backend-1  Healthy                                    7.7s
     ⠹ Container compose-frontend-1 Waiting                                    13.1s
     ✔ Container compose-browser-1  Created                                    0.1s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                      9.8s
     ✔ Image compose-browser        Built                                      9.8s
     ✔ Image compose-backend        Built                                      9.8s
     ✔ Network compose_default      Created                                    0.0s
     ✔ Container compose-backend-1  Healthy                                    7.7s
     ✔ Container compose-frontend-1 Healthy                                    13.2s
     ⠙ Container compose-browser-1  Starting                                   11.4s
    [?25h[?25l[8A[0G[+] up 6/7
     ✔ Image compose-frontend       Built                                      9.8s
     ✔ Image compose-browser        Built                                      9.8s
     ✔ Image compose-backend        Built                                      9.8s
     ✔ Network compose_default      Created                                    0.0s
     ✔ Container compose-backend-1  Healthy                                    7.7s
     ✔ Container compose-frontend-1 Healthy                                    13.2s
     ⠹ Container compose-browser-1  Starting                                   11.5s
    [?25h[?25l[8A[0G[+] up 7/7
     ✔ Image compose-frontend       Built                                      9.8s
     ✔ Image compose-browser        Built                                      9.8s
     ✔ Image compose-backend        Built                                      9.8s
     ✔ Network compose_default      Created                                    0.0s
     ✔ Container compose-backend-1  Healthy                                    7.7s
     ✔ Container compose-frontend-1 Healthy                                    13.2s
     ✔ Container compose-browser-1  Started                                    11.5s
    [?25h

## Command Started

- Time: `2026-03-31T21:28:29-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `97`
- Summary: in progress: /bin/zsh -lc 'curl -fsS http://127.0.0.1:8565/health'

### Full Text

    Command: /bin/zsh -lc 'curl -fsS http://127.0.0.1:8565/health'
    Status: in progress

## Command Finished

- Time: `2026-03-31T21:28:29-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `98`
- Summary: completed, exit 0: /bin/zsh -lc 'curl -fsS http://127.0.0.1:8565/health'

### Full Text

    Command: /bin/zsh -lc 'curl -fsS http://127.0.0.1:8565/health'
    Status: completed
    Exit code: 0
    Output:
    {"status":"ok","service":"Storyteller API","environment":"development","version":"0.1.0","api_version":null,"dependencies":{"database":{"status":"not-configured","detail":"Database wiring lands in a later prompt; this scaffold only reports configuration state."}}}

## Command Started

- Time: `2026-03-31T21:28:29-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `99`
- Summary: in progress: /bin/zsh -lc "curl -fsS http://127.0.0.1:8566 | sed -n '1,40p'"

### Full Text

    Command: /bin/zsh -lc "curl -fsS http://127.0.0.1:8566 | sed -n '1,40p'"
    Status: in progress

## Command Finished

- Time: `2026-03-31T21:28:29-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `100`
- Summary: completed, exit 0: /bin/zsh -lc "curl -fsS http://127.0.0.1:8566 | sed -n '1,40p'"

### Full Text

    Command: /bin/zsh -lc "curl -fsS http://127.0.0.1:8566 | sed -n '1,40p'"
    Status: completed
    Exit code: 0
    Output:
    <!doctype html>
    <html lang="en">
      <head>
        <script type="module">import { injectIntoGlobalHook } from "/@react-refresh";
    injectIntoGlobalHook(window);
    window.$RefreshReg$ = () => {};
    window.$RefreshSig$ = () => (type) => type;</script>

        <script type="module" src="/@vite/client"></script>

        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
        <meta
          name="description"
          content="Storyteller is a calm studio for crafting bedtime stories from first idea to finished narration."
        />
        <title>Storyteller</title>
      </head>
      <body>
        <div id="root"></div>
        <script type="module" src="/src/main.tsx"></script>
      </body>
    </html>

## Command Started

- Time: `2026-03-31T21:28:29-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `101`
- Summary: in progress: /bin/zsh -lc './scripts/dev-compose.sh ps'

### Full Text

    Command: /bin/zsh -lc './scripts/dev-compose.sh ps'
    Status: in progress

## Command Finished

- Time: `2026-03-31T21:28:29-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `102`
- Summary: completed, exit 0: /bin/zsh -lc './scripts/dev-compose.sh ps'

### Full Text

    Command: /bin/zsh -lc './scripts/dev-compose.sh ps'
    Status: completed
    Exit code: 0
    Output:
    NAME                 IMAGE              COMMAND                  SERVICE    CREATED          STATUS                    PORTS
    compose-backend-1    compose-backend    "python -m app"          backend    24 seconds ago   Up 22 seconds (healthy)   0.0.0.0:8565->8565/tcp, [::]:8565->8565/tcp
    compose-browser-1    compose-browser    "docker-entrypoint.s…"   browser    23 seconds ago   Up 11 seconds             
    compose-frontend-1   compose-frontend   "docker-entrypoint.s…"   frontend   24 seconds ago   Up 16 seconds (healthy)   0.0.0.0:8566->8566/tcp, [::]:8566->8566/tcp

## Agent Message

- Time: `2026-03-31T21:28:33-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `103`
- Summary: The Compose stack is healthy with the new `python -m app` entrypoint and `/health` container check. I’m running the existing browser smoke spec once to confirm the frontend still sees the backend through the preserved `/api/hello` path.

### Full Text

    The Compose stack is healthy with the new `python -m app` entrypoint and `/health` container check. I’m running the existing browser smoke spec once to confirm the frontend still sees the backend through the preserved `/api/hello` path.

## Command Started

- Time: `2026-03-31T21:28:34-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `104`
- Summary: in progress: /bin/zsh -lc './scripts/dev-compose.sh run --rm browser npm run check -- --spec ./examples/homepage.spec.json'

### Full Text

    Command: /bin/zsh -lc './scripts/dev-compose.sh run --rm browser npm run check -- --spec ./examples/homepage.spec.json'
    Status: in progress

## Command Finished

- Time: `2026-03-31T21:28:34-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `105`
- Summary: failed, exit 127: /bin/zsh -lc './scripts/dev-compose.sh run --rm browser npm run check -- --spec ./examples/homepage.spec.json'

### Full Text

    Command: /bin/zsh -lc './scripts/dev-compose.sh run --rm browser npm run check -- --spec ./examples/homepage.spec.json'
    Status: failed
    Exit code: 127
    Output:
    zsh:1: no such file or directory: ./scripts/dev-compose.sh

## Agent Message

- Time: `2026-03-31T21:28:39-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `106`
- Summary: The browser smoke run failed for a mundane reason: I launched it from `tools/webapp-qa/`, so the repo-level `scripts/dev-compose.sh` path wasn’t available. I’m rerunning it from the repository root.

### Full Text

    The browser smoke run failed for a mundane reason: I launched it from `tools/webapp-qa/`, so the repo-level `scripts/dev-compose.sh` path wasn’t available. I’m rerunning it from the repository root.

## Command Started

- Time: `2026-03-31T21:28:42-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `107`
- Summary: in progress: /bin/zsh -lc './scripts/dev-compose.sh run --rm browser npm run check -- --spec ./examples/homepage.spec.json'

### Full Text

    Command: /bin/zsh -lc './scripts/dev-compose.sh run --rm browser npm run check -- --spec ./examples/homepage.spec.json'
    Status: in progress

## Command Finished

- Time: `2026-03-31T21:28:45-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `108`
- Summary: completed, exit 0: /bin/zsh -lc './scripts/dev-compose.sh run --rm browser npm run check -- --spec ./examples/homepage.spec.json'

### Full Text

    Command: /bin/zsh -lc './scripts/dev-compose.sh run --rm browser npm run check -- --spec ./examples/homepage.spec.json'
    Status: completed
    Exit code: 0
    Output:
    [?25l[3A[0G[+] start 1/2
     ⠙ Container compose-backend-1  Waiting                                     0.1s
     ✔ Container compose-frontend-1 Running                                     0.0s
    [?25h[?25l[3A[0G[+] start 1/2
     ⠹ Container compose-backend-1  Waiting                                     0.2s
     ✔ Container compose-frontend-1 Running                                     0.0s
    [?25h[?25l[3A[0G[+] start 1/2
     ⠸ Container compose-backend-1  Waiting                                     0.3s
     ✔ Container compose-frontend-1 Running                                     0.0s
    [?25h[?25l[3A[0G[+] start 1/2
     ⠼ Container compose-backend-1  Waiting                                     0.4s
     ✔ Container compose-frontend-1 Running                                     0.0s
    [?25h[?25l[3A[0G[+] start 1/2
     ⠴ Container compose-backend-1  Waiting                                     0.5s
     ✔ Container compose-frontend-1 Running                                     0.0s
    [?25h[?25l[3A[0G[+] start 2/2
     ✔ Container compose-backend-1  Healthy                                     0.5s
     ✔ Container compose-frontend-1 Running                                     0.0s
    [?25h[?25l[3A[0G[+]  2/2
     ✔ Container compose-backend-1  Healthy                                     0.5s
     ✔ Container compose-frontend-1 Running                                     0.0s
    [?25hContainer compose-frontend-1 Waiting 
    Container compose-frontend-1 Healthy 
    Container compose-browser-run-e391a3328994 Creating 
    Container compose-browser-run-e391a3328994 Created 

    > storyteller-webapp-qa@1.0.0 check
    > node ./scripts/run-spec.mjs --spec ./examples/homepage.spec.json

    [1G[0K[browser:debug] [vite] connecting...
    [browser:debug] [vite] connected.
    [browser:info] %cDownload the React DevTools for a better development experience: https://react.dev/link/react-devtools font-weight:bold
    Saved screenshot to /workspace/.artifacts/webapp-qa/homepage.png
    Completed spec /workspace/tools/webapp-qa/examples/homepage.spec.json
    [1G[0K\[1G[0K

## Agent Message

- Time: `2026-03-31T21:29:00-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `109`
- Summary: Verification is complete apart from cleanup and patch hygiene. I’m shutting the stack down, running `git diff --check`, then I’ll checkpoint the implementation commit before writing the required reviewer summary file.

### Full Text

    Verification is complete apart from cleanup and patch hygiene. I’m shutting the stack down, running `git diff --check`, then I’ll checkpoint the implementation commit before writing the required reviewer summary file.

## Command Started

- Time: `2026-03-31T21:29:00-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `110`
- Summary: in progress: /bin/zsh -lc 'git diff --check'

### Full Text

    Command: /bin/zsh -lc 'git diff --check'
    Status: in progress

## Command Finished

- Time: `2026-03-31T21:29:00-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `111`
- Summary: completed, exit 0: /bin/zsh -lc 'git diff --check'

### Full Text

    Command: /bin/zsh -lc 'git diff --check'
    Status: completed
    Exit code: 0

## Command Started

- Time: `2026-03-31T21:29:00-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `112`
- Summary: in progress: /bin/zsh -lc './scripts/dev-compose.sh down'

### Full Text

    Command: /bin/zsh -lc './scripts/dev-compose.sh down'
    Status: in progress

## Command Finished

- Time: `2026-03-31T21:29:02-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `113`
- Summary: completed, exit 0: /bin/zsh -lc './scripts/dev-compose.sh down'

### Full Text

    Command: /bin/zsh -lc './scripts/dev-compose.sh down'
    Status: completed
    Exit code: 0
    Output:
    [?25l[2A[0G[+] down 0/1
     ⠙ Container compose-browser-1 Stopping                                     0.2s
    [?25h[?25l[2A[0G[+] down 0/1
     ⠹ Container compose-browser-1 Stopping                                     0.3s
    [?25h[?25l[2A[0G[+] down 0/1
     ⠸ Container compose-browser-1 Stopping                                     0.4s
    [?25h[?25l[2A[0G[+] down 0/1
     ⠼ Container compose-browser-1 Stopping                                     0.5s
    [?25h[?25l[2A[0G[+] down 0/1
     ⠴ Container compose-browser-1 Stopping                                     0.6s
    [?25h[?25l[2A[0G[+] down 0/1
     ⠦ Container compose-browser-1 Stopping                                     0.7s
    [?25h[?25l[2A[0G[+] down 0/1
     ⠧ Container compose-browser-1 Stopping                                     0.8s
    [?25h[?25l[2A[0G[+] down 0/1
     ⠇ Container compose-browser-1 Stopping                                     0.9s
    [?25h[?25l[2A[0G[+] down 0/1
     ⠏ Container compose-browser-1 Stopping                                     1.0s
    [?25h[?25l[2A[0G[+] down 0/1
     ⠋ Container compose-browser-1 Stopping                                     1.1s
    [?25h[?25l[2A[0G[+] down 1/2
     ✔ Container compose-browser-1  Removed                                     1.2s
     ⠋ Container compose-frontend-1 Stopping                                    0.0s
    [?25h[?25l[3A[0G[+] down 1/2
     ✔ Container compose-browser-1  Removed                                     1.2s
     ⠙ Container compose-frontend-1 Stopping                                    0.1s
    [?25h[?25l[3A[0G[+] down 2/3
     ✔ Container compose-browser-1  Removed                                     1.2s
     ✔ Container compose-frontend-1 Removed                                     0.2s
     ⠋ Container compose-backend-1  Stopping                                    0.0s
    [?25h[?25l[4A[0G[+] down 2/3
     ✔ Container compose-browser-1  Removed                                     1.2s
     ✔ Container compose-frontend-1 Removed                                     0.2s
     ⠙ Container compose-backend-1  Stopping                                    0.1s
    [?25h[?25l[4A[0G[+] down 2/3
     ✔ Container compose-browser-1  Removed                                     1.2s
     ✔ Container compose-frontend-1 Removed                                     0.2s
     ⠹ Container compose-backend-1  Stopping                                    0.2s
    [?25h[?25l[4A[0G[+] down 2/3
     ✔ Container compose-browser-1  Removed                                     1.2s
     ✔ Container compose-frontend-1 Removed                                     0.2s
     ⠸ Container compose-backend-1  Stopping                                    0.3s
    [?25h[?25l[4A[0G[+] down 3/4
     ✔ Container compose-browser-1  Removed                                     1.2s
     ✔ Container compose-frontend-1 Removed                                     0.2s
     ✔ Container compose-backend-1  Removed                                     0.4s
     ⠋ Network compose_default      Removing                                    0.1s
    [?25h[?25l[5A[0G[+] down 3/4
     ✔ Container compose-browser-1  Removed                                     1.2s
     ✔ Container compose-frontend-1 Removed                                     0.2s
     ✔ Container compose-backend-1  Removed                                     0.4s
     ⠙ Network compose_default      Removing                                    0.2s
    [?25h[?25l[5A[0G[+] down 4/4
     ✔ Container compose-browser-1  Removed                                     1.2s
     ✔ Container compose-frontend-1 Removed                                     0.2s
     ✔ Container compose-backend-1  Removed                                     0.4s
     ✔ Network compose_default      Removed                                     0.2s
    [?25h

## Command Started

- Time: `2026-03-31T21:29:11-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `114`
- Summary: in progress: /bin/zsh -lc "find backend -type d -name '__pycache__' -prune -exec rm -rf {} +"

### Full Text

    Command: /bin/zsh -lc "find backend -type d -name '__pycache__' -prune -exec rm -rf {} +"
    Status: in progress

## Command Finished

- Time: `2026-03-31T21:29:11-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `115`
- Summary: completed, exit 0: /bin/zsh -lc "find backend -type d -name '__pycache__' -prune -exec rm -rf {} +"

### Full Text

    Command: /bin/zsh -lc "find backend -type d -name '__pycache__' -prune -exec rm -rf {} +"
    Status: completed
    Exit code: 0

## Command Started

- Time: `2026-03-31T21:29:11-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `116`
- Summary: in progress: /bin/zsh -lc 'git status --short'

### Full Text

    Command: /bin/zsh -lc 'git status --short'
    Status: in progress

## Command Finished

- Time: `2026-03-31T21:29:11-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `117`
- Summary: completed, exit 0: /bin/zsh -lc 'git status --short'

### Full Text

    Command: /bin/zsh -lc 'git status --short'
    Status: completed
    Exit code: 0
    Output:
    M README.md
     M backend/Dockerfile
     M backend/README.md
     M backend/app/main.py
     M backend/requirements.txt
     M docs/architecture-overview.md
     M infra/compose/docker-compose.yml
     M prompts/02-vite-react-scaffold.yolopilot.jsonlines
     M prompts/02-vite-react-scaffold.yolopilot.md
    ?? backend/app/__init__.py
    ?? backend/app/__main__.py
    ?? backend/app/api/
    ?? backend/app/db/
    ?? backend/app/models/
    ?? backend/app/services/
    ?? backend/app/settings/
    ?? backend/tests/
    ?? prompts/03-fastapi-scaffold.codex.jsonlines
    ?? prompts/03-fastapi-scaffold.yolopilot.jsonlines
    ?? prompts/03-fastapi-scaffold.yolopilot.md

## Agent Message

- Time: `2026-03-31T21:29:22-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `118`
- Summary: I’ve reached the checkpoint stage. I’m committing only the prompt-03 implementation files now and leaving the unrelated YoloPilot prompt logs untouched, then I’ll write the required markdown summary as the final filesystem change.

### Full Text

    I’ve reached the checkpoint stage. I’m committing only the prompt-03 implementation files now and leaving the unrelated YoloPilot prompt logs untouched, then I’ll write the required markdown summary as the final filesystem change.

## Command Started

- Time: `2026-03-31T21:29:23-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `119`
- Summary: in progress: /bin/zsh -lc 'git add README.md backend docs/architecture-overview.md infra/compose/docker-compose.yml && git commit -m "feat(prompt-03): fastapi scaffold"'

### Full Text

    Command: /bin/zsh -lc 'git add README.md backend docs/architecture-overview.md infra/compose/docker-compose.yml && git commit -m "feat(prompt-03): fastapi scaffold"'
    Status: in progress

## Command Finished

- Time: `2026-03-31T21:29:23-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `120`
- Summary: completed, exit 0: /bin/zsh -lc 'git add README.md backend docs/architecture-overview.md infra/compose/docker-compose.yml && git commit -m "feat(prompt-03): fastapi scaffold"'

### Full Text

    Command: /bin/zsh -lc 'git add README.md backend docs/architecture-overview.md infra/compose/docker-compose.yml && git commit -m "feat(prompt-03): fastapi scaffold"'
    Status: completed
    Exit code: 0
    Output:
    [yolopilot-init-03-fastapi-scaffold 72e6065] feat(prompt-03): fastapi scaffold
     28 files changed, 424 insertions(+), 17 deletions(-)
     create mode 100644 backend/app/__init__.py
     create mode 100644 backend/app/__main__.py
     create mode 100644 backend/app/api/__init__.py
     create mode 100644 backend/app/api/router.py
     create mode 100644 backend/app/api/routes/__init__.py
     create mode 100644 backend/app/api/routes/health.py
     create mode 100644 backend/app/api/routes/legacy.py
     create mode 100644 backend/app/api/v1/__init__.py
     create mode 100644 backend/app/api/v1/router.py
     create mode 100644 backend/app/api/v1/routes/__init__.py
     create mode 100644 backend/app/api/v1/routes/health.py
     create mode 100644 backend/app/db/__init__.py
     create mode 100644 backend/app/db/status.py
     create mode 100644 backend/app/models/__init__.py
     create mode 100644 backend/app/models/system.py
     create mode 100644 backend/app/services/__init__.py
     create mode 100644 backend/app/services/health.py
     create mode 100644 backend/app/settings/__init__.py
     create mode 100644 backend/app/settings/config.py
     create mode 100644 backend/tests/conftest.py
     create mode 100644 backend/tests/test_health.py

## Command Started

- Time: `2026-03-31T21:29:32-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `121`
- Summary: in progress: /bin/zsh -lc 'git rev-parse --short HEAD'

### Full Text

    Command: /bin/zsh -lc 'git rev-parse --short HEAD'
    Status: in progress

## Command Finished

- Time: `2026-03-31T21:29:32-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `122`
- Summary: completed, exit 0: /bin/zsh -lc 'git rev-parse --short HEAD'

### Full Text

    Command: /bin/zsh -lc 'git rev-parse --short HEAD'
    Status: completed
    Exit code: 0
    Output:
    72e6065

## Command Started

- Time: `2026-03-31T21:29:32-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `123`
- Summary: in progress: /bin/zsh -lc 'git status --short'

### Full Text

    Command: /bin/zsh -lc 'git status --short'
    Status: in progress

## Command Finished

- Time: `2026-03-31T21:29:32-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `124`
- Summary: completed, exit 0: /bin/zsh -lc 'git status --short'

### Full Text

    Command: /bin/zsh -lc 'git status --short'
    Status: completed
    Exit code: 0
    Output:
    M prompts/02-vite-react-scaffold.yolopilot.jsonlines
     M prompts/02-vite-react-scaffold.yolopilot.md
    ?? prompts/03-fastapi-scaffold.codex.jsonlines
    ?? prompts/03-fastapi-scaffold.yolopilot.jsonlines
    ?? prompts/03-fastapi-scaffold.yolopilot.md

## File Change Started

- Time: `2026-03-31T21:30:54-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `125`
- Summary: prompts/03-fastapi-scaffold.summary.md

### Full Text

    prompts/03-fastapi-scaffold.summary.md

    Additional details:
    {
      "status": "in_progress"
    }

## File Change Recorded

- Time: `2026-03-31T21:30:54-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `126`
- Summary: prompts/03-fastapi-scaffold.summary.md

### Full Text

    prompts/03-fastapi-scaffold.summary.md

    Additional details:
    {
      "status": "completed"
    }

## Agent Message

- Time: `2026-03-31T21:31:10-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `127`
- Summary: Implemented the FastAPI scaffold in commit `72e6065`. The backend now uses an app-factory layout with settings, services, models, DB placeholders, unversioned and versioned routers, `GET /health`, `GET /api/v1/health`, and a preserved `G...

### Full Text

    Implemented the FastAPI scaffold in commit `72e6065`. The backend now uses an app-factory layout with settings, services, models, DB placeholders, unversioned and versioned routers, `GET /health`, `GET /api/v1/health`, and a preserved `GET /api/hello` compatibility route. Key files are [main.py](/Users/kevin/code/storyteller/backend/app/main.py), [config.py](/Users/kevin/code/storyteller/backend/app/settings/config.py), [router.py](/Users/kevin/code/storyteller/backend/app/api/router.py), and [test_health.py](/Users/kevin/code/storyteller/backend/tests/test_health.py).

    Verification passed with backend pytest, `compileall`, live local startup plus `curl` checks, Docker Compose startup with the new `/health` healthcheck, and the existing browser smoke spec. The required reviewer summary was written last to [03-fastapi-scaffold.summary.md](/Users/kevin/code/storyteller/prompts/03-fastapi-scaffold.summary.md). Current intentional limit: database wiring is still a scaffold and reports `not-configured` until later prompts.

## Turn Completed

- Time: `2026-03-31T21:31:10-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `128`
- Summary: in 2356990 | cached 2277248 | out 26379

### Full Text

    Input tokens: 2356990
    Cached input tokens: 2277248
    Output tokens: 26379

## YoloPilot Event

- Time: `2026-03-31T21:31:11-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `129`
- Summary: Checking summary file 03-fastapi-scaffold.summary.md.

### Full Text

    Checking summary file 03-fastapi-scaffold.summary.md.

## YoloPilot Event

- Time: `2026-03-31T21:31:11-07:00`
- Prompt: `03 — Scaffold the FastAPI Backend` (4/100)
- Task event: `130`
- Summary: Creating final signed-off commit for 03-fastapi-scaffold.

### Full Text

    Creating final signed-off commit for 03-fastapi-scaffold.


# Prompt 24 Summary: Design Tokens and Accessibility Foundation

Implemented in two checkpoint commits:

- `6efbe82` `feat(prompt-24): design tokens and accessibility foundation`
- `067a12c` `test(prompt-24): add keyboard focus browser coverage`

## What I changed and why

I established a reusable frontend foundation so later workflow prompts can add
screens without repeating ad hoc colors, spacing, badge styles, or accessibility
wiring.

The main change was a full token-and-primitive pass across the current React
frontend:

- Rebuilt `frontend/src/styles/index.css` around explicit typography, spacing,
  radius, surface, border, shadow, and focus tokens.
- Added shared accessible primitives in
  `frontend/src/shared/ui/primitives.tsx` and a dedicated button style helper in
  `frontend/src/shared/ui/buttonStyles.ts`.
- Refactored the existing shell and route surfaces to consume those primitives
  instead of hard-coded status-chip and link classes.
- Added a skip link, stronger global `:focus-visible` handling, and reduced
  motion handling so the product feels calmer and more usable from the keyboard.
- Documented the baseline in `docs/frontend-design-foundation.md`.

The visual direction stays warm and quiet instead of turning the app into a
generic SaaS dashboard. The palette remains parchment-like, with blue/moss/gold
accents and softened panel surfaces so the product still reads as a bedtime
story studio.

## Architectural changes across the codebase

### Shared UI layer

New shared primitives now live under `frontend/src/shared/ui/`:

- `primitives.tsx`
  - `Button`
  - `Badge`
  - `Panel`
  - `ProgressBar`
  - `StackedList`
  - `StackedListItem`
  - `TextInput`
- `buttonStyles.ts`
  - `getButtonClassName`
  - shared button tone/size types for links and buttons

This is the new low-level UI foundation for future prompts. The components are
intentionally boring and composable rather than app-specific.

### Tokenized styling

`frontend/src/styles/index.css` now acts as the theme source of truth. The file
centralizes:

- font stacks
- label/body scale
- spacing scale
- radius scale
- ink/brand/surface colors
- shadow tokens
- focus ring values
- reduced-motion behavior

This replaces the earlier pattern of repeating one-off rgba values and
component-specific link/status classes.

### Route adoption

I migrated the existing surfaces onto the new layer:

- `frontend/src/app/AppShell.tsx`
  - added a skip link
  - added an explicit `main` target for keyboard users
- `frontend/src/shared/ui/ConnectionStatusBadge.tsx`
  - now uses `Panel` and `Badge`
- `frontend/src/shared/ui/ToastRegion.tsx`
  - now uses `Panel`, `Badge`, and `StackedList`
- `frontend/src/pages/home/HomePage.tsx`
  - now uses `Panel`, `Button`, `Badge`, `ProgressBar`, and `getButtonClassName`
- `frontend/src/pages/session/SessionWorkspacePage.tsx`
  - now uses `Badge`, `Panel`, `ProgressBar`, `StackedList`, and
    `getButtonClassName`
- `frontend/src/pages/not-found/NotFoundPage.tsx`
  - switched its CTA to the shared button styling

I also formatted `frontend/src/features/session/sessionQueries.ts` because
Prettier flagged it during verification, even though its behavior did not
change.

## New abstractions and how to use them

### `Panel`

Use `Panel` for any card/surface that needs optional eyebrow text, a semantic
heading, description text, and optional actions.

```tsx
<Panel
  as="section"
  eyebrow="Story setup"
  headingLevel={2}
  title="Planning preferences"
  description="Soft targets for length and pacing."
  actions={<Badge tone="brand">Draft</Badge>}
>
  ...
</Panel>
```

Useful extension points:

- `as`: choose semantic wrapper (`article`, `section`, `aside`, `header`, `div`)
- `tone`: `default`, `hero`, or `subtle`
- `headingLevel`: keep heading hierarchy correct inside each route

### `Button` and `getButtonClassName`

Use `Button` for actual buttons. Use `getButtonClassName` when the trigger is a
router `Link`.

```tsx
<Button tone="primary">Continue</Button>

<Link className={getButtonClassName({ tone: 'ghost', size: 'compact' })} to="/">
  Return home
</Link>
```

### `Badge`

Use `Badge` instead of bespoke “status chip” classes.

```tsx
<Badge tone="success">Complete</Badge>
<Badge tone="accent">Needs refresh</Badge>
```

Available tones:

- `neutral`
- `brand`
- `accent`
- `success`
- `warning`
- `danger`

### `ProgressBar`

The progress primitive now carries proper `progressbar` semantics.

```tsx
<ProgressBar
  aria-label="Workflow progress"
  label="Workflow progress"
  value={60}
  valueText="6 of 10 stages complete"
  hint="Resume at Beat sheet."
/>
```

### `TextInput`

`TextInput` is the baseline accessible field wrapper for future form-heavy
workflow screens.

```tsx
<TextInput
  label="Target runtime"
  description="Guides narration length without enforcing a hard cap."
  placeholder="About 12 minutes"
/>
```

The component wires label, description, and error state through native
associations and `aria-describedby`.

### `StackedList`

Use `StackedList` and `StackedListItem` when the design needs inset list rows
without re-creating the same surface style for chat entries, toasts, or
workflow lists.

```tsx
<StackedList as="ol">
  <StackedListItem tone="brand">Genre</StackedListItem>
  <StackedListItem tone="accent">Beat sheet</StackedListItem>
</StackedList>
```

## Accessibility foundation delivered

The accessibility note requested by the prompt is in
`docs/frontend-design-foundation.md`.

The implemented baseline includes:

- global keyboard-visible focus rings
- a skip link to main content
- reduced-motion handling for glows, shimmer, and panel entry animations
- semantically-labeled progress bars
- text-input wiring for labels, descriptions, and errors
- retained heading hierarchy on the existing routes

## Exact verification work performed

### Automated checks

Ran from `frontend/`:

- `npm run format:check`
  - Pass
- `npm run lint`
  - Pass
- `npm test`
  - Pass
  - 6 test files
  - 18 tests
- `npm run build`
  - Pass

### Added/expanded automated tests

Added `frontend/src/shared/ui/primitives.test.tsx` with targeted coverage for:

- text input accessibility wiring
  - Pass
- semantic panel heading + progress metadata
  - Pass
- ordered list semantics for `StackedList`
  - Pass

Existing route/page tests also continued to pass as part of the full frontend
Vitest run.

### Browser and visual verification

Used the running Docker Compose stack from `infra/compose` and the repo’s
browser runner.

Commands run:

- `cd infra/compose && docker compose run --rm browser npm run check -- --spec /workspace/tools/webapp-qa/examples/prompt-24-foundation-flow.spec.json`
  - Pass
- `cd infra/compose && docker compose run --rm browser npm run check -- --spec /workspace/tools/webapp-qa/examples/prompt-24-home-mobile.spec.json`
  - Pass
- `cd infra/compose && docker compose run --rm browser npm run check -- --spec /workspace/tools/webapp-qa/examples/prompt-24-keyboard-focus.spec.json`
  - Pass

Artifacts captured:

- `.artifacts/webapp-qa/prompt-24-home-desktop.png`
- `.artifacts/webapp-qa/prompt-24-workspace-desktop.png`
- `.artifacts/webapp-qa/prompt-24-home-mobile.png`
- `.artifacts/webapp-qa/prompt-24-focus-skip-link.png`
- `.artifacts/webapp-qa/prompt-24-focus-brand-link.png`

What I visually verified:

- desktop home route tokenization and calmer panel language
- desktop workspace route layout after creating a fresh session through the UI
- mobile home route stacking and readable spacing
- keyboard-triggered skip-link visibility
- keyboard focus reaching the first header control after the skip link

Visual verification limits:

- I verified the workspace using a newly-created draft session, not a populated
  late-stage composition/audio session.
- I did not run a screen reader in this pass; accessibility verification here is
  keyboard + semantics + browser-assertion based.

## LLM or prompt evaluation suite

No LLM-facing logic, prompts, model configuration, or eval wiring changed in
this task.

- Evaluation suite added: none
- Criteria reported: not applicable
- Outcome: not applicable

## Wrong turns, dead ends, and gotchas

- I first ran `docker compose ps` from the repo root and got `no configuration
  file provided`; the actual Compose file lives under `infra/compose/`.
- The old prompt-20 browser spec was stale and failed immediately because it
  asserted selectors and copy from a prior UI. I replaced that with prompt-24
  task-specific specs.
- Full-page workspace screenshots looked washed out because the panel entry
  animation and heavy backdrop treatment were being captured mid-transition. I
  changed the QA specs to viewport screenshots and added settle delays before
  capture.
- `npm run format:check` failed because `frontend/src/features/session/sessionQueries.ts`
  was already not Prettier-compliant. I formatted that file so the verification
  suite could pass cleanly.

## Assumptions made while working unsupervised

- The existing shell, routing, and current page structure should be preserved;
  this prompt was a foundation pass, not a product-wide redesign.
- A warm parchment background with blue/moss/gold accents is a better fit for a
  bedtime-story product than a neutral dashboard theme.
- It was acceptable to add a skip link and shared primitives now, even though
  some later workflow forms have not been implemented yet.
- Browser QA should avoid hard-coded session IDs, so the desktop flow spec
  creates a fresh session dynamically before validating the workspace route.

## Reviewer notes

If you want to inspect the foundation quickly, start with these files:

- `frontend/src/shared/ui/primitives.tsx`
- `frontend/src/shared/ui/buttonStyles.ts`
- `frontend/src/styles/index.css`
- `frontend/src/pages/home/HomePage.tsx`
- `frontend/src/pages/session/SessionWorkspacePage.tsx`
- `docs/frontend-design-foundation.md`

This leaves the repo ready for later prompts to build real forms and workflow
controls on a consistent, accessible surface instead of continuing to add page-
local styling.

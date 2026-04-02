# Prompt 51: Correlation Heuristics for Word Count, Runtime, and Chapters

## What I changed and why

I implemented a simple, explicit heuristic layer that connects the story setup fields instead of leaving word count, runtime, and chapter count as isolated inputs.

On the backend, I added a dedicated planning heuristics module at `backend/app/services/planning_heuristics.py`. It centralizes the pacing assumptions for bedtime narration and chapter sizing:

- narration midpoint: `140` words per minute
- roomy bedtime range floor: `120` words per minute
- brisk bedtime range ceiling: `160` words per minute
- chapter-size drift allowance: `15%` around the average

That module now provides pure functions for:

- estimating runtime from a word count
- estimating word count from a runtime
- estimating average chapter size from total words and chapter count
- inferring effective words per minute for an existing runtime/word pairing
- classifying pacing as `roomy`, `balanced`, or `brisk`
- estimating narration duration in seconds for the audio tooling

I then updated `backend/app/services/story_tools.py` to reuse `estimate_narration_duration_seconds(...)` so the audio-length heuristic and the story-setup heuristic are no longer maintaining separate narration-speed assumptions.

On the frontend, I added `frontend/src/features/session/planningHeuristics.ts` and rewired `frontend/src/features/session/StorySetupStage.tsx` to use it. The stage now:

- explains the current word count/runtime pairing in plain language
- explains likely chapter sizing from total words and chapter count
- surfaces the explicit assumptions in a visible “Assumptions” help block
- offers an explicit apply-on-click suggestion when the user changes one field and the related field is missing or now outside the normal bedtime range

The suggestion flow is intentionally non-authoritarian. I did not auto-overwrite related fields. Instead, the UI tracks the last edited planning field and only offers a compact “Use …” action for the correlated field. This keeps user control intact while still making the heuristics useful.

## Architectural changes across the codebase

### Backend

New module:

- `backend/app/services/planning_heuristics.py`

This file is the new source of truth for maintainable, pure planning calculations. The main architectural value is that the calculations are no longer embedded in UI copy or duplicated inside tool-specific code.

Example usage:

```python
from app.services.planning_heuristics import (
    estimate_runtime_from_word_count,
    estimate_word_count_from_runtime,
    estimate_chapter_size_from_word_count,
)

estimate_runtime_from_word_count(1800)
# RuntimeEstimate(target_minutes=13, minimum_minutes=11, maximum_minutes=15, ...)

estimate_word_count_from_runtime(12)
# WordCountEstimate(target_word_count=1680, minimum_word_count=1440, maximum_word_count=1920, ...)

estimate_chapter_size_from_word_count(1800, 3)
# ChapterSizeEstimate(average_words_per_chapter=600, minimum_words_per_chapter=510, maximum_words_per_chapter=690, ...)
```

Integration point:

- `backend/app/services/story_tools.py`

The story tool service now delegates its narration duration math to the new heuristic module. That keeps the audio estimate consistent with the story-planning assumptions.

### Frontend

New helper:

- `frontend/src/features/session/planningHeuristics.ts`

This mirrors the same heuristic model in TypeScript for immediate form feedback during editing. It returns user-facing summaries plus optional suggestion objects that the stage can apply without auto-mutating state.

Example usage:

```ts
buildRuntimeHeuristicSummary({
  lastEditedField: 'targetWordCount',
  targetWordCount: 1800,
  targetRuntimeMinutes: null,
})

// {
//   body: '1800 words usually reads aloud in about 13 minutes, often somewhere near 11-15.',
//   suggestion: {
//     field: 'targetRuntimeMinutes',
//     label: 'Use ~13 minutes',
//     value: 13,
//     helpText: 'Apply the midpoint runtime if you want the related field filled in for you.'
//   }
// }
```

UI integration:

- `frontend/src/features/session/StorySetupStage.tsx`

I replaced the old one-off correlation copy with helper-driven summaries and suggestion actions. The stage now tracks `lastEditedField` locally so “field A influences field B” is helpful and explainable instead of magical.

Supporting change:

- `frontend/src/shared/ui/workflow.tsx`

During browser QA I found that `InlineHelp` wrapped its children in a `<p>`, which broke once the new heuristic content included richer markup. I changed the wrapper to a `<div>` so `InlineHelp` can safely host block content across the app.

Styling support:

- `frontend/src/styles/index.css`

I added small styles for the heuristic/suggestion blocks so the new summary text and “Use …” action stay visually compact and readable.

## Tests and verification

### Backend verification

Command:

- `pytest backend/tests/test_planning_heuristics.py backend/tests/test_story_tools.py -q`

Result:

- `13 passed in 0.49s`

What this covered:

- runtime estimation from word count
- word-count estimation from runtime
- chapter-size estimation with bounded drift
- pacing-band classification
- narration duration reuse in story tools

Additional API regression check:

- `pytest backend/tests/test_session_api.py -q -k story_setup`
- result: `3 passed, 29 deselected in 1.02s`

Sanity compile:

- `python -m compileall backend/app/services/planning_heuristics.py backend/app/services/story_tools.py`
- result: passed

### Frontend verification

Commands:

- `npm test -- --run src/features/session/planningHeuristics.test.ts src/features/session/StorySetupStage.test.tsx src/pages/session/SessionWorkspacePage.test.tsx`
- `npm run lint`
- `npm run build`

Results:

- targeted Vitest suite: `3 files, 38 tests passed`
- ESLint: passed
- Vite production build: passed

Note:

- the production build still emits the pre-existing Vite chunk-size warning for the main JS bundle exceeding 500 kB after minification. The build itself succeeded.

### Browser and visual verification

I used the local Docker Compose stack and the repo’s Puppeteer runner via the `webapp-qa` skill flow.

Stack health:

- `docker compose -f infra/compose/docker-compose.yml ps`
- backend, frontend, worker, postgres, gcs, and browser were already healthy

Browser QA command:

- `docker compose -f infra/compose/docker-compose.yml run --rm browser npm run check -- --spec /workspace/.artifacts/webapp-qa/prompt-51-story-setup-heuristics.spec.json`

Live page checked:

- `http://localhost:8566/sessions/8155bbd7-2de7-4d4c-a961-d35485225ed0?stage=story_setup`

Assertions that passed in the browser:

- story setup page loaded
- “Composition can use this plan” was visible
- runtime/word-count heuristic copy was visible
- chapter-sizing heuristic copy was visible
- assumption text was visible

Screenshot captured:

- `.artifacts/webapp-qa/prompt-51-story-setup-heuristics.png`

Visual coverage limit:

- the browser harness is reliable for asserting text and capturing screenshots, but clearing already-populated numeric inputs in the current Puppeteer spec runner is brittle for `type="number"` controls. Because of that, I validated the explicit suggestion-click behavior through unit tests and validated the inspectable heuristic copy plus layout in the live browser.

## Evaluation suites for LLM or prompt-related work

None added. This prompt did not modify LLM prompts, model wiring, or evaluation behavior.

Status:

- `Not applicable`

## Wrong turns, dead ends, and gotchas

1. The first browser spec attempted to change a pre-filled numeric field to force the new suggestion button in the live app. The current browser harness did not reliably clear the populated `type="number"` value, so the page showed a validation error instead of the intended heuristic state. I kept suggestion behavior covered in unit tests and narrowed browser QA to the stable live-copy assertions.

2. Browser QA also exposed an actual bug: `InlineHelp` rendered children inside a `<p>`. My new heuristic blocks included nested block content, which produced invalid HTML and hydration warnings in the browser. I fixed `InlineHelp` to use a `<div>` wrapper and reran validation.

3. My first targeted Vitest command used repo-root-prefixed paths while already running inside `frontend/`, so Vitest reported “No test files found.” I corrected the paths and reran successfully.

4. The first frontend build after adding the new stage test failed because the mock `BeatSheetView` fixture was missing `focus_beats`. I updated the fixture and reran the build.

## Assumptions I made while working unsupervised

1. I treated `140` words per minute as the canonical bedtime narration midpoint because the repo already used that value in audio estimation logic.

2. I assumed a `120-160` words-per-minute band is simple enough for this prompt’s “approximate, maintainable, not oversold” requirement.

3. I assumed chapter-size guidance should stay descriptive rather than prescriptive, so I exposed average chapter size and a modest range instead of auto-suggesting a new chapter count.

4. I assumed the right UX for “changing one field can influence the others” was an explicit apply-on-click suggestion, not automatic synchronization. That matches the prompt’s requirement to preserve user control.

5. For live browser QA, I assumed it was acceptable to use an existing local QA session already present in the development database rather than trying to fabricate a fresh story-setup-ready session through a long chain of API calls.

## Changed files

- `backend/app/services/planning_heuristics.py`
- `backend/app/services/story_tools.py`
- `backend/tests/test_planning_heuristics.py`
- `frontend/src/features/session/planningHeuristics.ts`
- `frontend/src/features/session/planningHeuristics.test.ts`
- `frontend/src/features/session/StorySetupStage.tsx`
- `frontend/src/features/session/StorySetupStage.test.tsx`
- `frontend/src/shared/ui/workflow.tsx`
- `frontend/src/styles/index.css`

## Checkpoint commits

- `ce0645d feat(prompt-51): add backend planning heuristics`
- `7a828bf feat(prompt-51): wire story setup heuristics`

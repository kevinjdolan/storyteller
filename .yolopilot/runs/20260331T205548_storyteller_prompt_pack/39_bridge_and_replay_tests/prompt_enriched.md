## YoloPilot Execution Context

You are being run by `yolopilot` in an unsupervised batch workflow against a live repository.
There is no interactive human available during this run. Do not pause to ask for confirmation unless a hard external blocker makes progress impossible.
Make reasonable assumptions, execute decisively, and document those assumptions in your final summary.

## Primary Objective

Complete the task end to end with production-quality changes.
Prefer finishing the job over leaving partial implementation, TODOs, or unexplained follow-up work.

## Git And Branching Rules

Stay on the current git branch at all times.
Never create, rename, switch to, or request a new branch.
Commit periodically to the current branch as meaningful checkpoints during development.
Before finishing, make sure the working tree is left in a coherent state for a final automation commit.

## Working Style

Work autonomously.
Inspect the codebase before making architectural changes.
Preserve existing patterns unless there is a strong reason to improve them.
If you discover a better approach after starting, take it, but explain the wrong turn and why you changed course in the summary.
Avoid destructive git operations unless they are unquestionably necessary and safe for the current branch.

## Verification Requirements

You must verify your work as thoroughly as the repository allows.

Functional verification:
- Run targeted tests for the touched areas.
- Add or expand automated tests when coverage is missing.
- If practical, run broader suites after targeted validation passes.
- Run linters, type checks, build steps, and formatters that are relevant to the touched code.

UI and visual verification:
- If the change affects UI, styling, rendering, layout, accessibility, or visual behavior, capture browser-based verification.
- Prefer automated browser checks, screenshots, or snapshot-style evidence over purely code-level confidence.
- Mention what you visually verified and any limits of the visual coverage in the summary.

LLM and prompt verification:
- If you modify prompts, evals, model wiring, agent behavior, or any LLM-facing logic, create a comprehensive evaluation suite as part of the work.
- The evaluation suite should cover happy paths, edge cases, regressions, safety concerns, formatting expectations, and failure modes relevant to the change.
- In the final summary, report the evaluation criteria by name and include the measured values or pass/fail outcomes for each criterion.

## Dependency Rules

If Python dependencies are needed, update `requirements.txt` and install what you need in the active conda environment.
If JavaScript dependencies are needed, use the local repository package manager files and keep lockfiles consistent.
Keep dependency additions minimal and justified.

## Delivery Requirements

Leave the repository in a usable, well-explained state.
Your final action must be to write the required markdown summary file for this task.
The summary must be detailed, candid, and useful to a reviewer who did not watch the run happen.

## Shared Base Prompt

            The following shared instructions came from `base_prompt.md` and apply to this task:

            # Base Prompt — Build the Bedtime Story + Audio App

You are building a production-minded local-first application that helps a user create a bedtime story from idea to finished text and finished narration audio.

This prompt pack is designed to be used **sequentially**. Read this file first, then work through the numbered prompts in order. Each numbered prompt should be treated as an incremental implementation task inside the same repository. Preserve prior work unless the new prompt explicitly asks you to refactor it.

## Product Summary

The product is a guided story-creation studio with a persistent session model. A user should be able to:

1. See past story sessions first, including both in-progress and completed work.
2. Open a session to resume, edit, or finalize it.
3. Use a **two-pane workspace**:
   - **Left pane:** chat window, about one-third of the desktop width.
   - **Main pane:** structured workflow UI, about two-thirds of the desktop width.
4. Control the product in **both directions**:
   - The user can type in chat, and the system can translate those messages into UI actions.
   - The user can act directly in the UI, and those actions should be reflected in the chat log and in durable session state.
5. Move through a staged workflow:
   - Genre selection
   - Tone selection
   - Story setup / free-form brief
   - Story pitches
   - Character sheet
   - Save-the-Cat beat sheet
   - Story setup preferences such as word count, runtime, and chapters
   - Composition
   - Audio configuration and audio generation
   - Finalize / read / listen / download
6. Download the final story as a **Word document** and the final narration as an audio file.
7. Read or listen inside the product UI after generation is complete.

## Story-Generation Philosophy

The app is for **bedtime stories**, not generic fiction generation. That means:

- Wonder is welcome.
- Adventure is welcome.
- Mystery is welcome.
- Tension is allowed, but it should be modulated for bedtime use.
- Emotional repair matters.
- The ending should feel safe, satisfying, and restful.
- The narration and UI tone should remain calm, readable, and trustworthy.

Use the research docs in this prompt pack as direct product input, especially the Save The Cat notes and the curated genre/tone catalog.

## Required Story Workflow

The session should support this exact conceptual flow:

1. **Genre Selection**
   - The user selects from the curated genre list.
2. **Tone Selection**
   - The user is shown preconfigured tone options for the chosen genre.
3. **Story Setup**
   - The user provides a free-form description of the story they want to tell.
4. **Story Pitches**
   - Gemini generates multiple candidate pitches.
   - The user can select one, ask for alternatives, or refine via chat.
5. **Character Sheet**
   - Gemini generates multiple candidate character sheets.
   - The user can select or refine via chat.
6. **Story Beats**
   - Gemini generates a Save-the-Cat beat sheet for the selected plan.
   - The user can refine the beats via chat or UI.
7. **Story Setup Preferences**
   - The user can set soft planning targets such as word count, read-aloud duration, and chapter organization.
   - These are **guides**, not strict constraints.
8. **Composition**
   - The system writes in segments.
   - The UI shows a live typewriter-like experience.
   - Writing should generally appear faster than the user can comfortably read.
   - A visible progress bar should show overall story progress.
   - The agent should periodically post chat summaries of what it is writing.
   - The user can interrupt and redirect composition, including causing rewrites of prior segments.
9. **Audio**
   - The user configures voice, music, speed, and related settings.
   - The system estimates final length heuristically.
   - Audio is generated in segments with visible progress.
10. **Finalize**
   - The user can read and listen in the UI.
   - The user can download the story as a Word document and the final audio as a file.

## Non-Negotiable Technical Requirements

### Frontend
- React
- Vite
- TypeScript
- The browser must **never** hold provider secrets
- Chat pane on the left, main pane on the right
- Past sessions screen must be the first meaningful screen

### Backend
- Python
- FastAPI
- Durable backend-owned business logic
- Clear separation between route handlers, domain services, AI orchestration, and persistence

### Data and Infrastructure
- PostgreSQL is the durable store for structured application state
- Use a **file-backed GCS emulator** for object/blob storage in local development
- The app must run with Docker Compose
- Postgres and object storage must both be **persistent across restarts**
- `secrets.yaml` exists locally for API keys and must **not** be committed to git

### AI
- Use the **Gemini 3.1 family** for text/planning/composition workloads
- Keep model IDs centralized in config, not scattered through the codebase
- Put AI calls behind backend services and adapters
- Use structured outputs wherever determinism matters
- Use separate adapters for:
  - planning/classification/intent parsing
  - long-form story generation
  - narration / TTS
- Keep narration generation isolated behind a provider-style interface because model offerings evolve

## Recommended Architecture

Use a calm, maintainable architecture rather than a clever one.

### Suggested application shape
- `frontend/` — React + Vite app
- `backend/` — FastAPI app plus domain services
- `infra/` — Docker Compose, Dockerfiles, local infrastructure helpers
- `docs/` — architecture notes, ADRs, product docs

### Suggested backend layers
- `api/` or route handlers
- `settings/`
- `db/`
- `models/`
- `repositories/`
- `services/`
- `worker/`
- `ai/`
- `storage/`

### Suggested durable concepts
- Session
- Workflow stage
- Event log
- Selected genre
- Selected tone
- Story brief
- Pitch batch + selected pitch
- Character batch + selected character sheet
- Beat sheet
- Story setup preferences
- Outline / chapter or scene plan
- Continuity bible
- Composition job
- Composition segment
- Audio job
- Asset record

## Real-Time and Long-Running Work

Treat composition and audio generation as **durable background jobs**, not request-thread work.

- The browser should be able to refresh without losing the job.
- The UI should receive live progress updates.
- The backend should own current truth about progress.
- A separate worker process is strongly preferred.
- Use PostgreSQL-backed durable job records.
- Persist partial outputs frequently enough that resume is trustworthy.

## Chat and UI Bridge Rules

The product must support true bidirectional interaction.

### Chat-to-UI
A user message can propose actions like:
- select a tone
- regenerate pitches
- choose a pitch
- adjust character traits
- soften the midpoint
- shorten the story target
- pause writing
- change narration speed

### UI-to-Chat
A direct UI action should appear in the chat history as a compact structured summary, for example:
- “Selected genre: Quest Fantasy”
- “Updated target runtime: ~12 minutes”
- “Accepted revised beat sheet”

### Safety rule
The model can **propose** actions, but a deterministic policy layer should decide whether they are valid in the current session state.

## Save The Cat Expectations

Use the Save The Cat method as the backbone of planning.

- The beat sheet should be explicit, editable, and stored as structured data.
- The composition stage should write against the beat sheet and the detailed outline derived from it.
- Bedtime adaptation matters: the low points can be emotionally meaningful without becoming harsh or distressing.
- The final story should still feel like a transformation story, not just a string of nice scenes.

## Genre and Tone Expectations

Use the included research docs to seed:
- a curated genre list
- per-genre tone options
- bedtime-suitable arc notes
- tone descriptors that can guide UI copy and AI prompting

Do **not** label tones with living or copyrighted-author names. Use generic tone labels and descriptors.

## Audio Expectations

Narration must be treated as a real product feature, not a side demo.

- Segment audio generation so it is resumable
- Estimate length heuristically before generation
- Support voice selection
- Support speed controls
- Support optional background music
- Keep music subordinate to narration clarity
- Produce a final compiled audio artifact
- Keep intermediate and final artifacts trackable through durable metadata

## Export Expectations

At minimum, the user must be able to get:
- final story text in the app
- final audio in the app
- downloadable `.docx`
- downloadable final audio file

## Developer Experience and Quality Bar

Favor:
- typed interfaces
- boring, explicit service boundaries
- migrations
- tests around durable state
- visible logs
- simple scripts for local dev
- useful docs

Avoid:
- stuffing everything into route handlers
- leaking secrets to the browser
- relying on browser local state as the source of truth
- making stage transitions implicit or magical
- hiding important state in giant untyped JSON blobs when relational structure is obvious

## How to Respond to Each Numbered Prompt

For each numbered prompt in this pack:

1. Treat it as the next incremental repo task.
2. Preserve prior work unless the new prompt requires refactor.
3. Make reasonable local decisions when the prompt leaves room, but stay aligned with this base prompt.
4. Prefer small, coherent commits worth reviewing.
5. After implementing, report:
   - what you changed
   - key files touched
   - tests run
   - any important follow-up risks or TODOs
6. If a prompt depends on earlier work, inspect the repo and extend it rather than rebuilding from scratch.

## Preferred Model Split

Keep exact model IDs configurable, but the intended split is:

- **High-value reasoning / plan synthesis / long-form composition:** Gemini 3.1 Pro class model
- **Fast structured tasks / intent parsing / normalization / small transforms:** Gemini 3.1 Flash-Lite class model
- **Narration:** Gemini TTS adapter, configured independently from text models

If provider offerings change, keep the application code stable and swap configuration or adapter internals.

## Final Reminder

Build this as a durable, session-based, full-stack application — not a single-shot prompt demo.

The finished experience should feel like a guided story studio where a user can:
- start from an idea,
- shape it collaboratively,
- watch it be written,
- redirect it while it is being written,
- turn it into audio,
- and come back later to continue or enjoy the finished result.

## Task File

Task source: `39-bridge-and-replay-tests.md`

# 39 — Bridge and Replay Tests

Read `base_prompt.md` first and preserve all prior prompt work.

## Objective

Add end-to-end-ish coverage around the chat/UI bridge and session replay before deeper workflow logic is layered on top.

## Build
- Test representative user messages turning into structured actions and then into durable state changes.
- Test that UI-originated changes appear in chat history and can be replayed into a resumed session snapshot.
- Add a few negative tests for invalid actions and rejected transitions.

## Deliverables

- Backend tests for the action pipeline
- Frontend or integration tests for action echoes
- Replay/resume coverage

## Acceptance checks

- The bridge behavior is proven before it becomes central to the product experience.
- A bad proposed action produces a clear rejection path.
- Replay and hydration logic are not left untested.

## Notes

These tests are about product integrity more than implementation detail.

## Suggested commit label

`feat(prompt-39): bridge and replay tests`

## Required Final Summary File

As the final step of the task, write a detailed natural-language markdown summary to:
`/Users/kevin/code/storyteller/.yolopilot/runs/20260331T205548_storyteller_prompt_pack/39_bridge_and_replay_tests/summary.md`

The summary must include:
- what you changed and why
- the architectural changes you made across the codebase
- examples showing how to use any new abstractions, helpers, or extension points
- the exact verification work you performed, including tests, builds, browser checks, screenshots, and any remaining limits
- any evaluation suite you added for LLM or prompt-related work, including named criteria and their measured values or pass/fail outcomes
- wrong turns, dead ends, surprising repository behavior, and gotchas you discovered during development
- any assumptions you had to make while working unsupervised

Write that summary file only after all code changes and verification are complete.
The summary file will be used as the pull request description, so make it reviewer-friendly and complete.

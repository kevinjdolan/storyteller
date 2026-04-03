# Prompt 82 Summary: Story Formatting for In-App Reading

## What I changed and why

I implemented a backend-owned story formatting pipeline and rewired the finalize reader to consume that formatted document instead of reparsing manuscript text in React. The main goal was to make the in-app reader and lightweight export behavior deterministic from the same formatting rules, while keeping the UI readable and calm for long-form bedtime story reading.

Concretely, I:

- Added a new backend formatter in `backend/app/services/story_formatting.py` that:
  - normalizes manuscript text,
  - turns paragraphs and chapter/heading lines into structured reader blocks,
  - preserves simple inline emphasis safely (`*`, `_`, `**`, `__`, `***`, `___`),
  - emits a typed `StoryReaderDocumentView`.
- Extended backend session models with:
  - `StoryReaderSpanView`
  - `StoryReaderBlockView`
  - `StoryReaderDocumentView`
- Added a new API endpoint:
  - `GET /api/v1/sessions/{session_id}/assets/{asset_id}/reader`
  - This returns the structured reader document for a ready text asset.
- Updated Word export generation in `backend/app/services/story_exports.py` to render from the shared formatter output, including bold/italic DOCX runs for simple emphasis instead of flattening everything into plain paragraphs.
- Added a dedicated frontend `StoryReader` component in `frontend/src/features/session/StoryReader.tsx` and replaced the finalize stage’s ad hoc story parsing with the new typed reader document.
- Tightened reader styling in `frontend/src/styles/index.css` for:
  - clearer chapter separation,
  - restrained but stronger heading hierarchy,
  - comfortable line height and measure,
  - readable inline emphasis without decorative excess.
- Kept the existing accepted-snapshot fallback path in `FinalizeStage` for resilience when the durable manuscript is not available yet, but made the primary reader path backend-formatted.

## Architectural changes across the codebase

### Backend

- `backend/app/models/session.py`
  - Added typed reader document/span/block models.
- `backend/app/models/__init__.py`
  - Exported the new reader models.
- `backend/app/services/story_formatting.py`
  - New shared formatter service.
- `backend/app/services/story_exports.py`
  - DOCX export now uses the shared reader document instead of its own private block parser.
- `backend/app/api/v1/routes/sessions.py`
  - Added the reader-document endpoint for ready text assets.
- `backend/app/services/__init__.py`
  - Re-exported `build_story_reader_document`.

### Frontend

- `frontend/src/api/sessions.ts`
  - Added typed client models for the reader document and `fetchSessionStoryReaderDocument()`.
- `frontend/src/features/session/StoryReader.tsx`
  - New reader rendering component.
- `frontend/src/features/session/FinalizeStage.tsx`
  - Replaced inline manuscript text loading/parsing with reader-document loading/rendering.
  - Kept the old local block fallback only for accepted snapshot recovery cases.
- `frontend/src/styles/index.css`
  - Added dedicated story reader styles.

### Tests

- `backend/tests/test_story_formatting.py`
  - Added formatter-focused tests for chapters, paragraphs, line wrapping, and emphasis.
- `backend/tests/test_story_export_service.py`
  - Added coverage for simple emphasis surviving into DOCX runs.
- `backend/tests/test_session_api.py`
  - Added coverage for the new reader-document API route.
- `frontend/src/features/session/StoryReader.test.tsx`
  - Added rendering tests for chapter sections and emphasis.
- `frontend/src/features/session/FinalizeStage.test.tsx`
  - Updated finalize-stage tests to use the new reader-document API contract.

## New abstractions, helpers, and extension points

### 1. Shared backend formatter

Use this when you need deterministic story structure from canonical text:

```python
from app.services.story_formatting import build_story_reader_document

document = build_story_reader_document(
    story_text,
    asset_id=story_asset.id,
)
```

This returns a typed `StoryReaderDocumentView` with:

- `chapter_count`
- `word_count`
- `has_structure`
- `blocks[]`
  - `kind`: `chapter_heading` | `heading` | `paragraph`
  - `text`
  - `spans[]` with `plain` / `emphasis` / `strong` / `strong_emphasis`

### 2. Reader API route

Use this when the frontend should render the durable manuscript exactly as the backend formats it:

```http
GET /api/v1/sessions/{session_id}/assets/{asset_id}/reader
```

Example response shape:

```json
{
  "format_version": "story_reader.v1",
  "asset_id": "story-asset-1",
  "word_count": 1782,
  "chapter_count": 3,
  "has_structure": true,
  "blocks": [
    {
      "kind": "chapter_heading",
      "level": 1,
      "text": "Chapter 1: Lantern Wake",
      "spans": [{ "text": "Chapter 1: Lantern Wake", "style": "plain" }]
    }
  ]
}
```

### 3. Frontend reader component

Use this to render a backend-formatted reader document:

```tsx
import { StoryReader } from './StoryReader'

<StoryReader document={readerDocument} />
```

The component groups chapter headings into sections and renders inline emphasis with semantic tags instead of using raw HTML injection.

## Verification work performed

### Targeted automated verification

- `pytest backend/tests/test_story_formatting.py backend/tests/test_story_export_service.py backend/tests/test_session_api.py -q`
  - Result: `51 passed in 10.37s`
- `npm test -- --run src/features/session/StoryReader.test.tsx src/features/session/FinalizeStage.test.tsx`
  - Result: `2 files, 5 tests passed`

### Broader automated verification

- `pytest backend/tests -q`
  - Result: `283 passed, 5 skipped in 33.93s`
- `ruff check backend/app backend/tests`
  - Result: passed
- `npm run lint`
  - Result: passed
- `npm run build`
  - Result: passed
  - Note: Vite still reports an existing large-chunk warning for the frontend bundle; this was not introduced by this change.

### Browser / visual verification

Because Docker was unavailable on this machine during the run, I could not use the normal Compose-backed visual QA path.

What I tried:

- `docker compose -f infra/compose/docker-compose.yml ps --format json`
  - Failed because the Docker daemon was not reachable.
- `open -ga Docker`
  - Docker still did not become available.

Fallback visual QA used:

- Local Vite dev server at `http://127.0.0.1:4174`
- Puppeteer with intercepted API responses for:
  - `/api/hello`
  - `/api/v1/sessions/session-finalize-1`
  - `/api/v1/sessions/session-finalize-1/hydrate`
  - `/api/v1/sessions/session-finalize-1/assets/story-asset-1/reader`

Artifacts captured:

- Desktop workspace viewport:
  - `/tmp/storyteller-finalize-reader-desktop.png`
- Narrow/mobile viewport:
  - `/tmp/storyteller-finalize-reader-mobile.png`
- Additional desktop crop focused on reader body:
  - `/tmp/storyteller-finalize-reader-desktop-readerbody-cleaner.png`

What I visually verified:

- Chapter headings render clearly and separate sections.
- Paragraph spacing is readable and not overly dense.
- Inline emphasis renders semantically and visually:
  - italic emphasis for soft tonal nudges
  - stronger emphasis for important words
- The reader remains readable at a narrow/mobile width.

Visual verification limits:

- The cleanest browser evidence is the narrow/mobile capture.
- The full desktop workspace capture includes surrounding workspace rails and sticky UI, which makes the raw full-screen screenshot noisier than the mobile one.
- The additional desktop crop is reviewer-friendly but derived from the desktop browser capture rather than being a direct element-only screenshot from the app.

## LLM / prompt evaluation suite

No prompt templates, model routing, agent behavior, or LLM-facing business logic were changed in this task.

Because of that, I did not add a new LLM evaluation suite. There are no new named eval criteria to report for this prompt.

## Wrong turns, dead ends, and gotchas

- I initially found two separate formatting paths:
  - backend DOCX export had its own markdown-ish parser
  - frontend finalize reader had a different, simpler parser
  - I replaced that split with a backend-owned formatter plus typed API contract.
- The first frontend test rerun failed because I passed Vitest file filters as `frontend/src/...` from inside the `frontend/` working directory. Rerunning with repo-relative `src/...` paths fixed it.
- Ruff surfaced only import ordering issues after the implementation. I fixed those with `ruff check --fix` and reran the targeted backend tests afterward.
- Docker was unavailable for the preferred visual QA path. I attempted to start Docker Desktop, but the daemon never became reachable.
- My first Puppeteer screenshots were misleading because:
  - the page was captured at the top of the app shell instead of the reader section,
  - and my first pass accidentally used the default 800x600 viewport.
  - I corrected that by explicitly setting the viewport, scrolling to the finalize reader, and capturing both desktop and narrow views.
- The desktop workspace is visually noisier than the mobile capture because the full session workspace includes multiple columns and sticky side content around the reader.

## Assumptions made during unsupervised execution

- Story manuscript assets are UTF-8 text assets, typically markdown-like text.
- “Simple emphasis” in this prompt means lightweight markdown emphasis markers only:
  - `*italic*`
  - `_italic_`
  - `**bold**`
  - `__bold__`
  - `***bold italic***`
  - `___bold italic___`
- Plain lines beginning with chapter-like labels such as `Chapter`, `Part`, `Prologue`, and `Epilogue` should count as structural headings even without markdown `#` prefixes.
- It was acceptable to keep the accepted-snapshot fallback path in the frontend as a resilience mechanism, even though the primary durable reader path is now backend-formatted.
  - Important nuance: the fallback path still uses lightweight local block parsing and does not preserve inline emphasis if the durable reader document cannot be fetched.
- It was acceptable to use intercepted API responses for browser verification when Docker/Compose could not be brought up.

## Checkpoint

- Code checkpoint commit created during the run:
  - `a07c050` — `feat(prompt-82): html markdown and reader formatting`


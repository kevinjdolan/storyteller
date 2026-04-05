# Long-Session Performance Notes

Prompt 94 adds explicit guard rails around the workspace paths that grow with long-running sessions.

## Why this exists

The session workspace accumulates three different kinds of data over time:

- durable chat and UI history
- planning revisions and candidate batches
- composition segment revisions and generated artifacts

Left unchecked, all three grow the initial hydration payload and make the UI do more work than the current view needs.

## Current guard rails

### Workspace hydration windows

`SessionSnapshot.collection_windows` now reports which bulky collections were trimmed for the main workspace payload.

The current workspace windows are:

- `pitch_batches`: most recent 4 batches
- `character_sheet_batches`: most recent 4 batches
- `beat_sheet_revisions`: most recent 4 revisions
- `story_outline_revisions`: most recent 4 revisions
- `plan_revisions`: most recent 6 revisions
- `composition_segment_versions`: most recent 5 revisions per segment, while always keeping the current accepted version and any pending rewrite version

These windows only affect the hydrated workspace shell. The selected item for each stage still ships in its dedicated `selected_*` field, and the current job state still ships in the active/latest job fields.

### Chat transcript window

The frontend now renders the most recent 80 chat messages first and lets the user reveal older transcript entries in 80-message increments.

This keeps the chat DOM stable during live updates while still allowing review of older transcript content already loaded into the client.

### Hydration history window

The workspace now asks the hydration endpoint for the most recent 30 durable history events instead of a larger default slice.

That recent window is enough to rebuild the visible transcript context on open without forcing every workspace load to hydrate a long event tail.

## Full durable history

The durable history is still preserved in PostgreSQL. These windows do not delete or rewrite history.

Use the dedicated history and debug tooling when a feature genuinely needs older data:

- `GET /api/v1/sessions/{session_id}/history`
- `GET /api/v1/sessions/{session_id}/debug-inspector`

Future features that need older revisions should prefer targeted fetches over expanding the default workspace hydration payload.

## Extension guidance

- Keep new workspace-hydrated collections behind an explicit recent-item limit.
- Preserve the currently selected or active record outside that limit when the current UI depends on it.
- If a panel needs older history, add a targeted fetch or pagination control instead of increasing the global hydration window.
- Treat expensive story parsing work the same way: memoize against the narrow data actually used, not the whole session snapshot.

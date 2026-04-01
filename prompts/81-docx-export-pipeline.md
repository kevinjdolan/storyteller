# 81 — Word Document Export Pipeline

Read `base_prompt.md` first and preserve all prior prompt work.

## Objective

Generate a downloadable Word document version of the completed story from the backend.

## Build
- Add a backend export service that creates a `.docx` file containing title, metadata, chapter structure if present, and the full story text.
- Store the generated document as an asset record in object storage.
- Make export generation idempotent or regenerable when the story text changes.

## Deliverables

- DOCX export service
- Asset storage and metadata for the export
- A backend endpoint or action that triggers export generation

## Acceptance checks

- The user can download the finished story as a Word document.
- The export is tied to the canonical final story text, not stale drafts.
- Generated exports are discoverable through the asset model.

## Notes

Do not overcomplicate formatting. Clean, readable output is enough.

## Suggested commit label

`feat(prompt-81): docx export pipeline`

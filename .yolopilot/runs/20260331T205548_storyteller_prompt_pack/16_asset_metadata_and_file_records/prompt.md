# 16 — Asset Metadata and File Records

Read `base_prompt.md` first and preserve all prior prompt work.

## Objective

Track generated files as first-class records so exports and audio are discoverable, resumable, and downloadable later.

## Build
- Create an asset table for things like draft text snapshots, composition segments, audio segments, final mixed audio, and docx exports.
- Store object path, media type, size, checksum if practical, generation status, and owning session.
- Add service methods for saving new asset records and marking them ready or failed.

## Deliverables

- Asset metadata model
- Asset service helpers
- Tests for creating and querying asset records

## Acceptance checks

- The backend can answer ‘what downloadable artifacts exist for this session?’ without scanning storage blindly.
- Failed or partial asset generation is visible in durable state.
- The schema is compatible with segmented audio generation.

## Notes

Keep file metadata separate from the blob bytes themselves.

## Suggested commit label

`feat(prompt-16): asset metadata and file records`

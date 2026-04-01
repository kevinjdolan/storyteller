# 56 — Revision History and Branch-Like Tracking for Plan Changes

Read `base_prompt.md` first and preserve all prior prompt work.

## Objective

Give the user safety when changing plans by preserving prior accepted states rather than destructively overwriting everything.

## Build
- Record important planning artifacts with versions or snapshots so the app can show what changed over time.
- Allow the session to know which version of pitch, character sheet, beat sheet, and outline are current.
- Expose a lightweight compare or restore capability for key planning artifacts.

## Deliverables

- Versioning strategy for planning artifacts
- Metadata for current versus previous revisions
- Optional compare/restore UI stubs

## Acceptance checks

- Users can make changes without feeling one click away from losing the previous plan.
- Composition can point to the specific plan revision it is based on.
- The history model stays understandable.

## Notes

A simple revision model is enough; full git-for-stories is not required.

## Suggested commit label

`feat(prompt-56): revision history and branches`

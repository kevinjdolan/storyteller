# 43 — Normalize the User Brief Into Structured Preferences

Read `base_prompt.md` first and preserve all prior prompt work.

## Objective

Use Gemini to turn the user’s free-form brief into a structured planning summary that later stages can rely on.

## Build
- Build a backend service that extracts likely protagonist type, setting, emotional goal, constraint notes, bedtime-safety concerns, and candidate motifs from the user’s brief.
- Store the normalized preferences as structured data alongside the raw brief.
- Surface the normalized result in the UI as an editable interpretation, not as hidden magic.

## Deliverables

- Brief normalization service
- Structured normalized brief model
- UI summary panel for the extracted preferences

## Acceptance checks

- Later generators can rely on structured preferences instead of reparsing raw prose every time.
- The user can correct or override the extracted interpretation.
- The normalized view stays clearly tied to the original brief.

## Notes

Use a Gemini model suited for structured output and keep the prompt strict.

## Suggested commit label

`feat(prompt-43): brief normalization service`

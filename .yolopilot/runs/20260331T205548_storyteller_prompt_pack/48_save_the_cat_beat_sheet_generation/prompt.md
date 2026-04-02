# 48 — Save-the-Cat Beat Sheet Generation

Read `base_prompt.md` first and preserve all prior prompt work.

## Objective

Generate a high-level beat sheet for the story using the Save the Cat framework adapted for bedtime storytelling.

## Build
- Implement a beat-sheet generator that outputs all required Save the Cat beats with short summaries, emotional intent, and any bedtime-specific softening notes.
- Map the selected pitch and character sheet into the beat structure while keeping the result high level rather than full prose.
- Persist the beat sheet as a structured artifact that can be revised and later used by composition.

## Deliverables

- Beat-sheet generation service
- Structured beat-sheet model
- Beat-sheet stage UI

## Acceptance checks

- The generated beat sheet clearly includes the full Save the Cat progression, not a vague outline.
- The beats feel appropriate for the chosen genre and tone.
- The beat sheet is stored in a structured form that downstream services can consume.

## Notes

Use the research docs in this pack as direct guidance for beat purposes and bedtime adaptation.

## Suggested commit label

`feat(prompt-48): save the cat beat sheet generation`

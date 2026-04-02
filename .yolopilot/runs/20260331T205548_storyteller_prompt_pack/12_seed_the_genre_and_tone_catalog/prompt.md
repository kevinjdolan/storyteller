# 12 — Seed the Genre and Tone Catalog

Read `base_prompt.md` first and preserve all prior prompt work.

## Objective

Create a durable, queryable catalog of genres and preconfigured tone choices based on the research docs in this prompt pack.

## Build
- Load the approved genre list and its tone choices into the database through a seed script or migration-based seed step.
- Store short descriptions, UI labels, bedtime-safety notes, and any default planning hints for each tone.
- Add a way to re-run the seed safely without duplicating rows.

## Deliverables

- Genre and tone seed data
- A repeatable seed command
- Docs that point back to the research files in this pack

## Acceptance checks

- The app can populate the genre and tone selectors entirely from the database or a backend-owned source of truth.
- Tone choices are filtered by genre without frontend hard-coding.
- The seed step is idempotent.

## Notes

Keep the seed format friendly to later editing by humans.

## Suggested commit label

`feat(prompt-12): seed genres and tones`

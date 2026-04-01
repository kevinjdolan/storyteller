# 41 — Tone Selection API and UI

Read `base_prompt.md` first and preserve all prior prompt work.

## Objective

Implement the tone-selection stage with preconfigured tones filtered by the selected genre.

## Build
- Add a backend endpoint that returns tone choices for the current genre with short labels, summaries, and perhaps sample excerpts or descriptors.
- Build the tone stage UI with selection cards and any supporting detail view needed to understand the options.
- Persist tone selection and surface it through the session snapshot and chat/action history.

## Deliverables

- Tone catalog endpoint
- Tone selection stage UI
- Tone selection persistence

## Acceptance checks

- Only tones relevant to the selected genre are shown.
- Tone choices feel concrete and helpful rather than vague adjectives alone.
- The selected tone is durable and resumable.

## Notes

Lean on the research pack’s generic tone descriptions.

## Suggested commit label

`feat(prompt-41): tone selection api and ui`

# 30 — Chat-to-UI Action Schema

Read `base_prompt.md` first and preserve all prior prompt work.

## Objective

Define the structured action language that lets chat messages propose concrete UI operations without directly mutating the interface in ad hoc ways.

## Build
- Create a typed schema for UI actions such as selecting a genre, selecting a tone, updating the brief, regenerating pitches, choosing a pitch, refining character details, starting composition, pausing jobs, or changing audio settings.
- Include fields for confidence, rationale, target stage, required confirmation, and any extracted structured values.
- Document which actions can be applied automatically and which should surface as suggested actions awaiting user confirmation.

## Deliverables

- Shared UI action schema
- Backend and frontend type definitions
- Policy note on auto-apply versus confirm-first actions

## Acceptance checks

- Chat intent handling has a stable contract before any model is asked to emit actions.
- The action set covers the required workflow stages from the brief.
- Risky or destructive actions can be gated behind confirmation.

## Notes

Do not let the agent directly manipulate the UI without a typed contract.

## Suggested commit label

`feat(prompt-30): chat to ui action schema`

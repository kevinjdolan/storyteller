# 55 — Continuity Bible and World-State Tracker

Read `base_prompt.md` first and preserve all prior prompt work.

## Objective

Create a structured continuity record that helps the app stay consistent during long composition and rewrite flows.

## Build
- Track facts about characters, locations, objects, promises, voice constraints, and unresolved threads.
- Update the continuity bible when the user accepts major planning decisions and when composition locks in details worth preserving.
- Make the continuity record inspectable for debugging and future refinement.

## Deliverables

- Continuity model or service
- Update hooks from planning stages
- Optional UI inspector for continuity facts

## Acceptance checks

- The system has a durable place to remember canonical details.
- Continuity data can inform later composition prompts and rewrite decisions.
- The record is concise enough to stay useful.

## Notes

This should reduce contradictions, not create busywork.

## Suggested commit label

`feat(prompt-55): continuity bible`

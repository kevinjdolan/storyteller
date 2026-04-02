# 83 — Artifact Packaging and Download Links

Read `base_prompt.md` first and preserve all prior prompt work.

## Objective

Expose all generated artifacts coherently so the user can retrieve the outputs they care about without hunting.

## Build
- Create a backend endpoint that returns a session’s current artifact inventory: final story text, docx export, final audio, and any useful preview assets.
- Build the finalize stage download area with clear labels and readiness indicators.
- Handle missing or outdated artifacts explicitly.

## Deliverables

- Artifact inventory endpoint
- Finalize download section
- Outdated/missing artifact messaging

## Acceptance checks

- The user can see what artifacts exist for the session at a glance.
- The UI distinguishes ready, generating, failed, and stale artifacts.
- Download affordances map to real backend assets reliably.

## Notes

One clean artifact panel beats scattered buttons.

## Suggested commit label

`feat(prompt-83): artifact packaging and links`

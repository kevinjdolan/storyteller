# 88 — Artifact Retention and Cleanup Policies

Read `base_prompt.md` first and preserve all prior prompt work.

## Objective

Prevent storage sprawl by defining what partial outputs should be kept, superseded, or cleaned up over time.

## Build
- Write retention rules for temporary composition checkpoints, superseded rewrites, old audio segments, preview files, and final exports.
- Implement lightweight cleanup hooks or maintenance commands for obvious expired temporary artifacts.
- Make sure cleanup never deletes the currently active canonical outputs for a session.

## Deliverables

- Retention policy document
- Cleanup commands or maintenance job stubs
- Safety checks for canonical artifacts

## Acceptance checks

- Temporary artifacts have a lifecycle instead of growing forever.
- Final user-facing artifacts are preserved safely.
- Cleanup can be run without fear of deleting the active session output accidentally.

## Notes

Start conservative. Deleting too little is better than deleting too much.

## Suggested commit label

`feat(prompt-88): artifact retention and cleanup`

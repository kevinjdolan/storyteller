# 58 — Usage, Cost, and Latency Metrics

Read `base_prompt.md` first and preserve all prior prompt work.

## Objective

Track model usage, timing, and approximate cost so the app can stay observable as more Gemini calls are introduced.

## Build
- Log the purpose of each model call, the model used, elapsed time, and any token or cost metadata that is available.
- Persist per-session summaries or lightweight counters for planning, composition, and audio usage.
- Expose a developer-facing summary view or log report.

## Deliverables

- Model usage metrics capture
- Per-session usage summary
- Developer-readable diagnostics output

## Acceptance checks

- You can answer ‘what is slow and what is expensive?’ without guessing.
- Model choices are visible per workflow stage.
- The metrics do not leak secrets or full private prompts unnecessarily.

## Notes

Keep the first version pragmatic and lightweight.

## Suggested commit label

`feat(prompt-58): usage cost and latency metrics`

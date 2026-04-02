# 95 — Continuous Integration Pipeline

Read `base_prompt.md` first and preserve all prior prompt work.

## Objective

Automate linting, tests, and build validation so regressions are caught before they land.

## Build
- Add a CI workflow that runs frontend and backend linting, unit tests, integration tests where practical, and at least one build step.
- Cache dependencies sensibly to keep CI time reasonable.
- Fail clearly with useful logs when migrations, tests, or builds break.

## Deliverables

- CI workflow config
- Documented required checks
- A short troubleshooting note for common CI failures

## Acceptance checks

- The repo has a repeatable automated validation path.
- Both frontend and backend are included in CI, not just one stack.
- CI feedback is specific enough to help fix failures quickly.

## Notes

Keep the first CI pass dependable rather than exhaustive.

## Suggested commit label

`feat(prompt-95): ci pipeline`

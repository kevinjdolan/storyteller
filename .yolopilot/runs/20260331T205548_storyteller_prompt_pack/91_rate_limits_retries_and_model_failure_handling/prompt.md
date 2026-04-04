# 91 — Rate Limits, Retries, and Model Failure Handling

Read `base_prompt.md` first and preserve all prior prompt work.

## Objective

Harden the app against transient Gemini failures, quota issues, and worker retries so long workflows do not fail messily.

## Build
- Add retry and backoff behavior where it is safe for planning, composition, and audio generation calls.
- Distinguish retryable failures from user-actionable failures such as invalid settings or exhausted quotas.
- Expose clear job status and chat or UI messages when the system is waiting, retrying, or needs user intervention.

## Deliverables

- Retry policy implementation
- Failure classification rules
- User-visible status messaging for degraded states

## Acceptance checks

- Transient provider issues do not instantly poison the whole session.
- The user can tell whether the system is retrying or actually stuck.
- Retries are bounded and observable.

## Notes

Be explicit about retry limits and side effects.

## Suggested commit label

`feat(prompt-91): rate limits retries and fallbacks`

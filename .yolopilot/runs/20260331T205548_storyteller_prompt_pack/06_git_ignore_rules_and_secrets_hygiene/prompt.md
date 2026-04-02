# 06 — Git Ignore Rules and Secrets Hygiene

Read `base_prompt.md` first and preserve all prior prompt work.

## Objective

Make accidental secret leaks and transient file clutter difficult by default.

## Build
- Update `.gitignore` so `secrets.yaml`, local env files, build artifacts, caches, and persistent dev data directories are excluded.
- Add a short security note that explains why `secrets.yaml` must never be committed and where safe sample files belong instead.
- Optionally add a simple pre-commit or grep-based guard for obviously sensitive file names and values.

## Deliverables

- Hardened `.gitignore`
- `docs/secrets-and-local-config.md`
- Any lightweight guard rails you add for secret hygiene

## Acceptance checks

- The repository clearly distinguishes example config from real config.
- Persistent local data can exist without polluting git status.
- A contributor would have to work hard to accidentally commit `secrets.yaml`.

## Notes

Do not add heavyweight secret scanners unless they remain easy for contributors to work with.

## Suggested commit label

`feat(prompt-06): gitignore and secrets hygiene`

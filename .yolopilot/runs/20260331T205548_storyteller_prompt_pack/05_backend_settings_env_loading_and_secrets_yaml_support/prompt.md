# 05 — Backend Settings, Env Loading, and `secrets.yaml` Support

Read `base_prompt.md` first and preserve all prior prompt work.

## Objective

Implement a backend configuration system that can load required settings from environment variables and a local `secrets.yaml` file that never belongs in git.

## Build
- Add a typed settings module that can read normal environment variables and, for local development, merge values from `secrets.yaml`.
- Define settings for database connection, Gemini API key, GCS emulator endpoint, bucket names, CORS origins, and feature flags.
- Fail fast with useful validation errors when required configuration is missing.

## Deliverables

- Typed backend settings module
- `secrets.example.yaml` or equivalent schema document
- Documentation for how `secrets.yaml` is discovered and merged

## Acceptance checks

- A developer can run the project locally by creating `secrets.yaml` from the example file.
- The API never requires the browser to know the Gemini API key.
- Missing config values produce readable startup errors, not stack traces full of noise.

## Notes

Keep the precedence rules simple and documented.

## Suggested commit label

`feat(prompt-05): backend settings and secrets loading`

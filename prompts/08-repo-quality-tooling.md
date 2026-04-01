# 08 — Quality Tooling and Shared Conventions

Read `base_prompt.md` first and preserve all prior prompt work.

## Objective

Establish basic linting, formatting, and code-style conventions across both the frontend and backend before product code grows.

## Build
- Configure frontend linting and formatting, plus backend formatting and linting, with commands that can run in CI later.
- Add editor settings such as `.editorconfig` if they help keep whitespace and line endings stable.
- Write a short style note that covers naming, API shape conventions, error handling style, and how generated assets should be separated from hand-written source.

## Deliverables

- Formatting and lint commands for both stacks
- Any shared editor config files
- `docs/contributing.md` with practical conventions

## Acceptance checks

- A clean checkout can run the quality commands without custom local hacks.
- The repo has one obvious formatter per language instead of dueling tools.
- The conventions are short, actionable, and tied to this project.

## Notes

Avoid style bikeshedding. Choose defaults and move on.

## Suggested commit label

`feat(prompt-08): repo quality tooling`

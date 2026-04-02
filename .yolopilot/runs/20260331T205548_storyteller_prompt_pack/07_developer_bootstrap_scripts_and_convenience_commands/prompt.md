# 07 — Developer Bootstrap Scripts and Convenience Commands

Read `base_prompt.md` first and preserve all prior prompt work.

## Objective

Create a predictable local workflow so the project is easy to start, stop, reset, lint, and test.

## Build
- Add a `Makefile`, task runner, or script collection that wraps the most common repo commands.
- Include commands for starting the stack, stopping it, viewing logs, resetting local volumes when necessary, and running lint/tests.
- Document the intended daily workflow for a developer making changes to either frontend or backend.

## Deliverables

- Top-level developer task script(s)
- README quickstart commands
- A reset strategy for local persistent data

## Acceptance checks

- The most common dev workflows can be run without memorizing long Docker commands.
- There is a safe way to reset the local stack when migrations or seed data change.
- The commands are cross-platform enough for normal team use or clearly documented if they are shell-specific.

## Notes

Keep the command surface small and obvious.

## Suggested commit label

`feat(prompt-07): developer bootstrap scripts`

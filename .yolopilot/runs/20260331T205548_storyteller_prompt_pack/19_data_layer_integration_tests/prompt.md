# 19 — Data Layer Integration Tests

Read `base_prompt.md` first and preserve all prior prompt work.

## Objective

Lock down the database, storage abstraction, and worker skeleton with a first batch of integration tests before product behavior gets complex.

## Build
- Add integration tests for migrations, session creation, event logging, asset metadata, and job claiming.
- Make the tests easy to run locally, ideally against the Docker Compose services or disposable test containers.
- Document how these tests fit into the future CI pipeline.

## Deliverables

- Backend integration test suite
- Test fixtures for DB and storage
- Docs for running integration tests

## Acceptance checks

- The most important durable state paths are covered by real tests, not only unit tests.
- A migration regression would be caught quickly.
- The worker queue claim logic has test coverage.

## Notes

Prioritize tests for durability and resumability over edge cosmetic cases.

## Suggested commit label

`feat(prompt-19): data layer integration tests`

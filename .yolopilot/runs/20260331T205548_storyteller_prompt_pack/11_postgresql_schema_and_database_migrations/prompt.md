# 11 — PostgreSQL Schema and Database Migrations

Read `base_prompt.md` first and preserve all prior prompt work.

## Objective

Implement the first real PostgreSQL schema for the durable objects identified in the domain model.

## Build
- Set up SQLAlchemy/SQLModel-style models and Alembic migrations or an equivalent migration system.
- Create tables for sessions, genres, tone profiles, pitches, character sheets, beat sheets, story setup, job records, export assets, and event logs.
- Add timestamps, status fields, and foreign keys that reflect how the UI will resume and audit work.

## Deliverables

- Initial database models
- Migration files
- Local migration commands documented

## Acceptance checks

- A fresh database can be migrated from zero to head reliably.
- The schema can represent an in-progress or completed story session without storing everything in one JSON blob.
- Primary relationships and indexes are present for obvious query paths.

## Notes

It is fine to keep some flexible JSON columns for model outputs, but do not avoid a real relational core.

## Suggested commit label

`feat(prompt-11): postgres schema and migrations`

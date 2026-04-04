# Prompt 12 Summary: Seed Genres and Tones

## What I Changed and Why

This prompt asked for a durable, queryable catalog of genres and preconfigured tone choices, seeded into the database in a repeatable way and ready for later API and UI work.

I implemented that in four parts:

1. I added a backend-owned, human-editable catalog file at
   [`backend/app/data/genre_tone_catalog.yaml`](/Users/kevin/code/storyteller/backend/app/data/genre_tone_catalog.yaml).
   It defines six curated genres and eighteen genre-specific tone profiles, each with:
   - UI labels
   - short descriptions
   - bedtime-safety notes
   - tone descriptors
   - per-tone `default_planning_hints`
   - per-genre `arc_notes`

2. I added a small catalog model and service layer so the seed data is not just static YAML. The new code validates the YAML, loads it into typed models, seeds it idempotently, and exposes read helpers for later prompt work:
   - [`backend/app/models/catalog.py`](/Users/kevin/code/storyteller/backend/app/models/catalog.py)
   - [`backend/app/services/catalog.py`](/Users/kevin/code/storyteller/backend/app/services/catalog.py)

3. I added a repeatable seed command at
   [`backend/app/seed_catalog.py`](/Users/kevin/code/storyteller/backend/app/seed_catalog.py),
   plus a `make` target:
   - `make backend-seed-catalog`
   - `python -m app.seed_catalog`
   - `python -m app.seed_catalog --dry-run`

4. I extended the schema so `tone_profiles` can store the new planning-hint payload explicitly instead of overloading an unrelated column:
   - ORM change in [`backend/app/db/models.py`](/Users/kevin/code/storyteller/backend/app/db/models.py)
   - migration in [`backend/migrations/versions/20260331_02_add_tone_profile_planning_hints.py`](/Users/kevin/code/storyteller/backend/migrations/versions/20260331_02_add_tone_profile_planning_hints.py)

The idempotency behavior is deliberate:

- existing genre rows are matched by `genres.slug`
- existing tone rows are matched by `(genre_id, slug)`
- reruns update matching rows in place
- rows removed from the catalog file are marked inactive instead of deleted

That choice keeps old session references safe while making the active selector options track the backend-owned source of truth.

## Architectural Changes Across the Codebase

The main architectural change is that catalog data is now treated as first-class backend reference data instead of an implied future constant.

### 1. Seeded reference data now has a typed lifecycle

Before this prompt, the repo had relational tables for `genres` and `tone_profiles`, but no owned catalog definition, no loader, no seed path, and no query abstraction. After this prompt:

- YAML is the editable source of truth
- Pydantic models validate that source before any write happens
- the service layer owns upsert/deactivation behavior
- the database becomes the durable active catalog for later selector APIs

### 2. Tone planning hints are now stored explicitly

Prompt 12 required default planning hints for each tone. The prior schema did not have a place for that. I added `default_planning_hints` to `tone_profiles` instead of hiding those values inside `descriptors` or a generic free-form field.

That matters because later prompts around pitching, beats, and composition will need a clean place to pull backend-owned defaults from.

### 3. Later API prompts now have stable read-side helpers

The new service module already provides the most likely access patterns for prompts 40 and 41:

- `list_active_genres(session)`
- `list_active_tones_for_genre(session, genre_slug="...")`

That should make the later catalog endpoints straightforward route-wrapper work instead of another round of model discovery.

## New Abstractions, Helpers, and Extension Points

### YAML catalog file

Use this when product or story-design direction changes:

```yaml
genres:
  - slug: quest-fantasy
    label: Quest Fantasy
    arc_notes:
      core_arc: Leave safety, explore, and return more settled.
    tones:
      - slug: hushed-wonder
        label: Hushed Wonder
        default_planning_hints:
          pacing: unhurried
          ending_style: return home carrying a small token of wonder
```

Adding a new genre or tone is just an edit to the YAML followed by rerunning the seed.

### Seed command

Examples:

```bash
make backend-seed-catalog
```

```bash
cd backend
python -m app.seed_catalog
python -m app.seed_catalog --dry-run
python -m app.seed_catalog --catalog /path/to/alternate-catalog.yaml
```

The dry run validates the file and exercises the upsert logic without committing.

### Catalog query helpers

Examples:

```python
from app.services.catalog import list_active_genres, list_active_tones_for_genre

genres = list_active_genres(session)
tones = list_active_tones_for_genre(session, genre_slug="quest-fantasy")
```

These helpers are intended as the backend-owned source for future catalog endpoints.

## Verification Performed

### Targeted automated verification

I added and ran new backend tests in
[`backend/tests/test_catalog.py`](/Users/kevin/code/storyteller/backend/tests/test_catalog.py).

Coverage added:

- `test_catalog_document_loads_seeded_genres_and_tones`
  - verifies the real YAML file loads and contains the expected ordered catalog
- `test_seed_catalog_is_idempotent_and_genre_filtered`
  - verifies first-run create behavior
  - verifies second-run update-without-duplicates behavior
  - verifies tones are queryable by genre without frontend hard-coding
- `test_seed_catalog_deactivates_rows_removed_from_source`
  - verifies catalog drift is handled by deactivation rather than deletion
- `test_seed_document_rejects_duplicate_tone_slugs`
  - verifies validation failures happen before database writes

I also extended existing tests:

- [`backend/tests/test_migrations.py`](/Users/kevin/code/storyteller/backend/tests/test_migrations.py)
  - now checks that Alembic creates the new `default_planning_hints` column
- [`backend/tests/test_db_models.py`](/Users/kevin/code/storyteller/backend/tests/test_db_models.py)
  - now round-trips a tone profile's planning hints through the ORM

### Command and migration verification

I verified the seed path end to end against a disposable migrated SQLite database:

1. `python -m alembic upgrade head`
2. `python -m app.seed_catalog`
3. `python -m app.seed_catalog --dry-run`

Observed results:

- first seed run: `genres: 6 created`, `tones: 18 created`
- dry-run rerun: `genres: 0 created, 6 updated`, `tones: 0 created, 18 updated`

This confirmed both the migration path and the CLI path work together.

### Repo quality checks

I ran:

- `make backend-format`
- `make backend-format-check`
- `make backend-lint`
- `make backend-test`
- `make check`

`make check` passed fully, including:

- backend pytest suite: `23 passed`
- frontend Vitest suite: `5 passed`
- frontend production build: passed

### Browser checks and screenshots

None were performed, and none were warranted for this prompt. The work is backend/data/docs only and does not change rendered UI, layout, styling, or browser behavior.

### LLM / prompt evaluation suite

No LLM-facing logic, prompt assembly, model routing, or eval harness was added in this prompt.

Evaluation status:

- `LLM Happy Paths`: not applicable
- `LLM Edge Cases`: not applicable
- `LLM Safety Regressions`: not applicable
- `LLM Formatting Expectations`: not applicable
- `LLM Failure Modes`: not applicable

## Wrong Turns, Dead Ends, and Gotchas

### 1. The repo did not actually contain a standalone upstream catalog file

The prompt pack referred to a curated genre/tone catalog as existing research input, but the checked-in repo did not contain a clean standalone catalog artifact. I treated that as a real repository gap and documented the assumption in
[`docs/genre-tone-catalog.md`](/Users/kevin/code/storyteller/docs/genre-tone-catalog.md)
instead of pretending a hidden file existed.

### 2. New tone rows were not initially attaching to the SQLAlchemy session correctly

My first upsert implementation created new tones with `ToneProfile(genre=genre, ...)` but did not ensure they were enrolled in the session the way I expected. The result was empty tone query results and failing tests.

I fixed that by attaching new rows through the relationship collection (`genre.tone_profiles.append(...)`), which let SQLAlchemy's relationship cascade handle persistence correctly.

### 3. The first end-to-end seed verification used the wrong shell environment

My first CLI verification attempt ran outside the backend virtualenv, which meant `alembic` and `sqlalchemy` were unavailable in that shell. I reran the same verification using the repo's backend Python environment and the command path worked correctly.

### 4. Deactivation was a better fit than deletion

I considered making the seed command only upsert matching slugs and ignore removed rows. That would have been less disruptive, but it would also leave stale active selector options in the database forever. Marking removed rows inactive gives a better long-term source-of-truth behavior while preserving referential safety for historical sessions.

## Assumptions Made While Working Unsupervised

1. The initial approved catalog had to be derived from visible prompt-pack guidance because no standalone research artifact was present in the repo.
2. It was acceptable to add a follow-on migration in prompt 12 because the existing schema lacked an explicit place for per-tone planning hints required by the prompt.
3. It was better for seed reruns to deactivate catalog entries removed from YAML rather than leave them active indefinitely.
4. Browser-based QA was unnecessary because the changes are backend-only and the broader repo check already covered frontend regression risk.

## Key Files Touched

- [`backend/app/data/genre_tone_catalog.yaml`](/Users/kevin/code/storyteller/backend/app/data/genre_tone_catalog.yaml)
- [`backend/app/models/catalog.py`](/Users/kevin/code/storyteller/backend/app/models/catalog.py)
- [`backend/app/services/catalog.py`](/Users/kevin/code/storyteller/backend/app/services/catalog.py)
- [`backend/app/seed_catalog.py`](/Users/kevin/code/storyteller/backend/app/seed_catalog.py)
- [`backend/app/db/models.py`](/Users/kevin/code/storyteller/backend/app/db/models.py)
- [`backend/migrations/versions/20260331_02_add_tone_profile_planning_hints.py`](/Users/kevin/code/storyteller/backend/migrations/versions/20260331_02_add_tone_profile_planning_hints.py)
- [`backend/tests/test_catalog.py`](/Users/kevin/code/storyteller/backend/tests/test_catalog.py)
- [`docs/genre-tone-catalog.md`](/Users/kevin/code/storyteller/docs/genre-tone-catalog.md)
- [`backend/README.md`](/Users/kevin/code/storyteller/backend/README.md)
- [`Makefile`](/Users/kevin/code/storyteller/Makefile)

## Final State

The repository now has:

- a durable seeded catalog of genres and tones
- explicit storage for tone planning hints
- an idempotent seed command
- backend query helpers for later selector APIs
- tests proving idempotency, filtering, validation, and migration compatibility
- reviewer-facing documentation tying the catalog back to the prompt pack

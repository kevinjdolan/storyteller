# Genre and Tone Catalog

Storyteller's curated genre and tone catalog is backend-owned reference data. The current seed
source lives in
[`backend/app/data/genre_tone_catalog.yaml`](/Users/kevin/code/storyteller/backend/app/data/genre_tone_catalog.yaml)
and is loaded into PostgreSQL through the seed command described below.

## Why This File Exists

Prompt 12 requires a durable, queryable catalog that later prompts can use for:

- genre selection cards
- tone options filtered by genre
- bedtime-safety notes displayed in the UI
- default planning hints that can shape prompts and workflow defaults

The prompt pack references a curated catalog as research input, but this repository does not
currently include a standalone upstream source file for that catalog. To keep the application
deterministic and editable by humans, the repo now treats the YAML file above as the canonical
expression of the approved initial catalog.

## Prompt-Pack Sources

The current catalog content is aligned to the guidance in these prompt-pack files:

- [`prompts/base_prompt.md`](/Users/kevin/code/storyteller/prompts/base_prompt.md): requires a curated genre list, per-genre tone options, bedtime-suitable arc notes, and tone descriptors.
- [`prompts/12-seed-genres-and-tones.md`](/Users/kevin/code/storyteller/prompts/12-seed-genres-and-tones.md): defines the seed-task deliverables and idempotency requirement.
- [`prompts/40-genre-selection-api-and-ui.md`](/Users/kevin/code/storyteller/prompts/40-genre-selection-api-and-ui.md): confirms the genre selector should read from the seeded catalog.
- [`prompts/41-tone-selection-api-and-ui.md`](/Users/kevin/code/storyteller/prompts/41-tone-selection-api-and-ui.md): confirms tone choices should be filtered by genre from backend-owned data.
- [`prompts/52-bedtime-safety-and-content-guidelines.md`](/Users/kevin/code/storyteller/prompts/52-bedtime-safety-and-content-guidelines.md): reinforces the bedtime-safety ceiling for tension, mystery, and emotional repair.

If product direction changes later, update the YAML file and re-run the seed command instead of
hard-coding new options in the frontend.

## Data Shape

Each genre entry stores:

- `slug`, `label`, `description`
- `bedtime_safety_notes`
- `arc_notes`
- an ordered list of tone definitions

Each tone entry stores:

- `slug`, `label`, `description`
- `bedtime_notes`
- `descriptors`
- `default_planning_hints`

The loader validates duplicate slugs at both the genre and tone levels before any database writes
begin.

## Seed Command

Run the seed from the repository root:

```bash
make backend-seed-catalog
```

Or call the module directly:

```bash
cd backend
python -m app.seed_catalog
```

Useful options:

```bash
cd backend
python -m app.seed_catalog --dry-run
python -m app.seed_catalog --catalog /path/to/alternate-catalog.yaml
```

The seed is idempotent:

- existing rows are updated in place when slugs match
- missing catalog rows are marked inactive instead of being deleted
- reruns do not create duplicate genres or duplicate tone profiles

That behavior keeps old session references intact while making the active selector options track the
backend-owned catalog file.

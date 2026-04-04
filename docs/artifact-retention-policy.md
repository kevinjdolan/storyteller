# Artifact Retention Policy

Storyteller keeps durable session history on purpose, but temporary checkpoints and superseded
blobs still need a lifecycle so the local file-backed GCS emulator does not grow without bound.
This policy starts conservative and only targets artifacts that are no longer the active
user-facing output for a session.

## Safety Rules

- Never auto-delete the latest ready story text, latest ready Word export, or latest ready final
  audio asset for a session.
- Never auto-delete assets tied to an active, queued, paused, or latest failed audio job, because
  those segment files may still be needed for resume or retry flows.
- Never auto-delete the latest rolling draft snapshot while a session has no canonical story text
  yet, because the snapshot is still the best durable recovery point.
- Cleanup is dry-run first. The maintenance CLI only deletes objects when `--apply` is passed.
- Cleanup marks the asset row with `metadata_json.retention_cleanup` so repeated runs do not keep
  targeting the same record after the blob has already been removed.

## Retention Windows

| Artifact class | Backend shape | Retention window | Cleanup action |
| --- | --- | --- | --- |
| Rolling draft snapshot | `draft_text_snapshot` | 14 days after the snapshot stops being the best recovery point | Delete the stored draft blob and mark the asset row as cleaned. |
| Superseded or rejected rewrite revisions | `composition_segment` linked to superseded or rejected segment versions | 14 days | Delete the old segment blob and mark the asset row as cleaned. |
| Old audio preview segments | `audio_segment` from completed, cancelled, or replaced audio jobs | 14 days | Delete the segment blob and mark the asset row as cleaned. |
| Superseded final exports | `story_text`, `story_docx`, and `final_audio` rows already marked `superseded` | 30 days | Delete the superseded export blob and mark the asset row as cleaned. |
| Final audio debug master | `final_audio.metadata_json.debug.narration_master_*` for superseded final audio assets | Same as the superseded final audio asset | Delete the linked narration-master debug blob alongside the superseded final audio blob. |

## Current Command Surface

Dry run from the repo root:

```bash
make backend-artifact-cleanup-dry-run
```

Direct module usage from `backend/`:

```bash
python -m app.maintenance.artifact_cleanup
python -m app.maintenance.artifact_cleanup --session-id <session-id>
python -m app.maintenance.artifact_cleanup --apply
```

The command prints:

- how many assets were protected by the safety policy
- how many cleanup candidates were found
- which storage targets would be removed
- which rule made each artifact eligible

## Extension Points

- `backend/app/services/artifact_retention.py`: policy windows, candidate selection, and safety
  guards live here.
- `backend/app/maintenance/artifact_cleanup.py`: CLI entrypoint for dry runs and apply runs.
- `backend/app/storage/service.py`: storage deletion support used by the maintenance flow.

If a future prompt adds new temporary blob classes, wire them into the retention service only after
the blob is either tracked in `session_assets` or referenced from canonical asset metadata. That
keeps cleanup auditable and avoids prefix-wide deletes that might catch a live output by mistake.

# YoloPilot Log

- Task file: `/Users/kevin/code/storyteller/prompts/37-agent-tool-registry.md`
- Summary file: `/Users/kevin/code/storyteller/prompts/37-agent-tool-registry.summary.md`
- Raw Codex log: `/Users/kevin/code/storyteller/prompts/37-agent-tool-registry.codex.jsonlines`
- Compact event log: `/Users/kevin/code/storyteller/prompts/37-agent-tool-registry.yolopilot.jsonlines`

## YoloPilot Event

- Time: `2026-04-01T07:30:52-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `1`
- Summary: Beginning task 38 of 100: 37-agent-tool-registry.md

### Full Text

    Beginning task 38 of 100: 37-agent-tool-registry.md

## YoloPilot Event

- Time: `2026-04-01T07:30:52-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `2`
- Summary: Creating branch yolopilot-init-37-agent-tool-registry from yolopilot-init-36-conversation-memory-summaries.

### Full Text

    Creating branch yolopilot-init-37-agent-tool-registry from yolopilot-init-36-conversation-memory-summaries.

## YoloPilot Event

- Time: `2026-04-01T07:30:52-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `3`
- Summary: Launching Codex for 37-agent-tool-registry.md with model gpt-5.4 and reasoning effort xhigh.

### Full Text

    Launching Codex for 37-agent-tool-registry.md with model gpt-5.4 and reasoning effort xhigh.

## Session Started

- Time: `2026-04-01T07:30:54-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `4`
- Summary: Thread ID: 019d4974-56bc-7663-8ec1-666bd5384bf4

### Full Text

    Thread ID: 019d4974-56bc-7663-8ec1-666bd5384bf4

## Turn Started

- Time: `2026-04-01T07:30:54-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `5`
- Summary: Codex started a new turn for the current task.

### Full Text

    Codex started a new turn for the current task.

## Agent Message

- Time: `2026-04-01T07:31:08-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `6`
- Summary: I’m inspecting the existing backend workflow, chat/action translation, and worker orchestration so the registry lands on top of current service boundaries instead of inventing a parallel path.

### Full Text

    I’m inspecting the existing backend workflow, chat/action translation, and worker orchestration so the registry lands on top of current service boundaries instead of inventing a parallel path.

## Command Started

- Time: `2026-04-01T07:31:08-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `7`
- Summary: in progress: /bin/zsh -lc "rg --files backend | sed 's#"'^#backend/#'"' | head -n 300"

### Full Text

    Command: /bin/zsh -lc "rg --files backend | sed 's#"'^#backend/#'"' | head -n 300"
    Status: in progress

## Command Finished

- Time: `2026-04-01T07:31:08-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `8`
- Summary: completed, exit 0: /bin/zsh -lc "rg --files backend | sed 's#"'^#backend/#'"' | head -n 300"

### Full Text

    Command: /bin/zsh -lc "rg --files backend | sed 's#"'^#backend/#'"' | head -n 300"
    Status: completed
    Exit code: 0
    Output:
    backend/backend/README.md
    backend/backend/tests/test_settings.py
    backend/backend/tests/test_event_log_service.py
    backend/backend/tests/test_asset_service.py
    backend/backend/tests/test_worker_runtime.py
    backend/backend/tests/test_health.py
    backend/backend/tests/test_chat_action_contracts.py
    backend/backend/tests/test_action_policy_api.py
    backend/backend/tests/test_action_policy_service.py
    backend/backend/tests/test_storage.py
    backend/backend/tests/test_workflow.py
    backend/backend/tests/test_realtime_contracts.py
    backend/backend/tests/test_background_jobs.py
    backend/backend/tests/test_intent_parser_service.py
    backend/backend/tests/test_migrations.py
    backend/backend/tests/test_conversation_memory_evals.py
    backend/backend/tests/test_intent_parser_api.py
    backend/backend/tests/integration/test_data_layer.py
    backend/backend/tests/integration/conftest.py
    backend/backend/tests/test_session_service.py
    backend/backend/tests/test_session_api.py
    backend/backend/tests/test_intent_parser_adapter.py
    backend/backend/tests/test_catalog.py
    backend/backend/tests/conftest.py
    backend/backend/tests/test_db_models.py
    backend/backend/pyproject.toml
    backend/backend/Dockerfile
    backend/backend/alembic.ini
    backend/backend/requirements.txt
    backend/backend/app/seed_catalog.py
    backend/backend/app/services/conversation_memory.py
    backend/backend/app/services/agent_context.py
    backend/backend/app/services/action_policy.py
    backend/backend/app/services/assets.py
    backend/backend/app/services/jobs.py
    backend/backend/app/services/intent_parser.py
    backend/backend/app/services/__init__.py
    backend/backend/app/services/health.py
    backend/backend/app/services/event_log.py
    backend/backend/app/services/sessions.py
    backend/backend/app/services/catalog.py
    backend/backend/app/__main__.py
    backend/backend/app/data/genre_tone_catalog.yaml
    backend/backend/app/main.py
    backend/backend/app/worker/__main__.py
    backend/backend/app/worker/README.md
    backend/backend/app/worker/runtime.py
    backend/backend/app/worker/__init__.py
    backend/backend/app/worker/default_handlers.py
    backend/backend/app/worker/registry.py
    backend/backend/app/api/dependencies.py
    backend/backend/app/api/routes/__init__.py
    backend/backend/app/api/routes/health.py
    backend/backend/app/api/routes/legacy.py
    backend/backend/app/api/router.py
    backend/backend/app/api/__init__.py
    backend/backend/app/api/v1/routes/__init__.py
    backend/backend/app/api/v1/routes/health.py
    backend/backend/app/api/v1/routes/sessions.py
    backend/backend/app/api/v1/router.py
    backend/backend/app/api/v1/__init__.py
    backend/backend/app/db/status.py
    backend/backend/app/db/base.py
    backend/backend/app/db/__init__.py
    backend/backend/app/db/session.py
    backend/backend/app/db/models.py
    backend/backend/app/__init__.py
    backend/backend/app/ai/__init__.py
    backend/backend/app/ai/intent_parser.py
    backend/backend/app/ai/prompts/intent_parser.md
    backend/backend/app/repositories/assets.py
    backend/backend/app/repositories/jobs.py
    backend/backend/app/repositories/__init__.py
    backend/backend/app/repositories/events.py
    backend/backend/app/repositories/sessions.py
    backend/backend/app/repositories/session_memory.py
    backend/backend/app/settings/__init__.py
    backend/backend/app/settings/config.py
    backend/backend/app/models/system.py
    backend/backend/app/models/catalog.py
    backend/backend/app/models/realtime.py
    backend/backend/app/models/action_policy.py
    backend/backend/app/models/workflow.py
    backend/backend/app/models/intent_parser.py
    backend/backend/app/models/chat_actions.py
    backend/backend/app/models/__init__.py
    backend/backend/app/models/session.py
    backend/backend/app/models/events.py
    backend/backend/app/storage/smoke_test.py
    backend/backend/app/storage/service.py
    backend/backend/migrations/README.md
    backend/backend/app/storage/status.py
    backend/backend/app/storage/__init__.py
    backend/backend/app/storage/paths.py
    backend/backend/app/storage/models.py
    backend/backend/migrations/script.py.mako
    backend/backend/migrations/env.py
    backend/backend/migrations/versions/20260331_03_generalize_export_assets_to_session_assets.py
    backend/backend/migrations/versions/20260401_01_add_background_jobs.py
    backend/backend/migrations/versions/20260331_02_add_tone_profile_planning_hints.py
    backend/backend/migrations/versions/20260401_02_add_session_memory_snapshots.py
    backend/backend/migrations/versions/20260331_01_initial_storyteller_schema.py

## Command Started

- Time: `2026-04-01T07:31:08-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `9`
- Summary: in progress: /bin/zsh -lc 'rg -n "generate pitches|pitch|character sheet|beat sheet|compose next|rewrite|audio|tool registry|registry|action vocabulary|chat translation|intent" backend tests docs -S'

### Full Text

    Command: /bin/zsh -lc 'rg -n "generate pitches|pitch|character sheet|beat sheet|compose next|rewrite|audio|tool registry|registry|action vocabulary|chat translation|intent" backend tests docs -S'
    Status: in progress

## Command Finished

- Time: `2026-04-01T07:31:08-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `10`
- Summary: failed, exit 2: /bin/zsh -lc 'rg -n "generate pitches|pitch|character sheet|beat sheet|compose next|rewrite|audio|tool registry|registry|action vocabulary|chat translation|intent" backend tests docs -S'

### Full Text

    Command: /bin/zsh -lc 'rg -n "generate pitches|pitch|character sheet|beat sheet|compose next|rewrite|audio|tool registry|registry|action vocabulary|chat translation|intent" backend tests docs -S'
    Status: failed
    Exit code: 2
    Output:
    rg: tests: No such file or directory (os error 2)
    docs/architecture-overview.md:25:        +--> background workers for composition and audio generation
    docs/architecture-overview.md:42:## Why Composition and Audio Must Use Resumable Server-Side Jobs
    docs/architecture-overview.md:47:- partial story text and audio segments need durable checkpoints
    docs/architecture-overview.md:64:- `worker/`: background job execution for writing and audio
    docs/architecture-overview.md:77:- Pitch batch and selected pitch
    docs/architecture-overview.md:78:- Character batch and selected character sheet
    docs/architecture-overview.md:79:- Beat sheet
    docs/architecture-overview.md:84:- Audio job and segments
    docs/system-diagram.md:10:    Worker["Worker process<br/>composition jobs, audio jobs, retries, interruption"]
    docs/system-diagram.md:12:    GCS[("File-backed GCS emulator<br/>story exports, audio segments,<br/>final artifacts")]
    docs/storage-buckets-and-prefixes.md:17:| Audio | `storyteller-audio` | Narration segments and final assembled audio |
    docs/storage-buckets-and-prefixes.md:36:| Audio segment | Audio | `sessions/{session_id}/audio/jobs/{job_id}/segments/{segment_index:04d}.{ext}` | `sessions/sess-42/audio/jobs/audio-2/segments/0007.mp3` |
    docs/storage-buckets-and-prefixes.md:37:| Final audio | Audio | `sessions/{session_id}/audio/jobs/{job_id}/final/{file_stem}.{ext}` | `sessions/sess-42/audio/jobs/audio-2/final/story.mp3` |
    docs/storage-buckets-and-prefixes.md:67:bootstrap code in composition, export, or audio workflows.
    backend/README.md:15:  - `worker/`: the durable PostgreSQL-backed worker loop and handler registry
    backend/README.md:126:so long-running story and audio work can move out of API request threads without adding Redis or a
    backend/README.md:136:The default worker registry includes a `demo.echo` handler that is useful for smoke tests and
    backend/README.md:137:verification before composition and audio handlers land in later prompts.
    backend/README.md:173:- `object_storage.paths`: predictable bucket/key builders for draft, audio, export, and debug paths
    docs/chat-action-echoes.md:11:- Use resolved UI labels such as `Audio` or `Beat sheet`, not raw IDs.
    docs/chat-action-echoes.md:13:  - `Opened Audio in the main pane.`
    docs/chat-action-echoes.md:16:  - `Couldn't update story setup yet. Finish Beat sheet first.`
    docs/chat-action-echoes.md:24:  - `chat.intent.parsed` echoes are reserved for blocked, gated, or not-yet-applied
    docs/chat-action-echoes.md:38:- Chat submissions still go through `POST /api/v1/sessions/{session_id}/chat/intents`.
    docs/event-taxonomy.md:29:| `selection.recorded` | Accepted or candidate selection for genre, tone, pitch, character sheet, beat sheet, or story setup. | `user` | stage-specific |
    docs/event-taxonomy.md:35:| `audio.progress.recorded` | Durable narration job progress for replay and worker debugging. | `system` | `audio` |
    docs/event-taxonomy.md:57:  "invalidated_stages": ["pitches", "characters", "beats", "composition", "audio", "finalize"],
    docs/event-taxonomy.md:58:  "current_stage": "pitches",
    docs/event-taxonomy.md:59:  "resume_stage": "pitches",
    docs/event-taxonomy.md:75:  "summary_text": "Updated beat sheet notes from the workspace."
    docs/event-taxonomy.md:97:- `record_audio_progress(...)`
    docs/event-taxonomy.md:154:- Do not rewrite or delete historical events to "fix" history. Emit a new compensating event.
    backend/tests/test_settings.py:36:    monkeypatch.setenv("STORYTELLER_GCS_AUDIO_BUCKET_NAME", "storyteller-audio")
    backend/tests/test_settings.py:51:    assert settings.gcs_bucket_names.audio == "storyteller-audio"
    backend/tests/test_settings.py:72:            audio: storyteller-audio
    backend/tests/test_settings.py:80:          enable_audio_generation: true
    backend/tests/test_settings.py:98:    assert settings.feature_flags.enable_audio_generation is True
    backend/tests/test_settings.py:115:            audio: storyteller-audio
    backend/tests/test_settings.py:164:    assert settings.gcs_bucket_names.audio == "storyteller-dev"
    backend/tests/test_settings.py:180:    monkeypatch.setenv("STORYTELLER_GCS_AUDIO_BUCKET_NAME", "storyteller-audio")
    backend/tests/test_settings.py:234:        "STORYTELLER_GCS_AUDIO_BUCKET_NAME",
    backend/tests/test_chat_action_contracts.py:13:    UpdateAudioSettingsAction,
    backend/tests/test_chat_action_contracts.py:52:                    "action_type": "update_audio_settings",
    backend/tests/test_chat_action_contracts.py:53:                    "target_stage": "audio",
    backend/tests/test_chat_action_contracts.py:69:    assert isinstance(batch.actions[2], UpdateAudioSettingsAction)
    backend/tests/test_chat_action_contracts.py:131:                        "target_stage": "audio",
    backend/tests/test_chat_action_contracts.py:145:        get_chat_to_ui_action_default_policy(ChatToUIActionType.SELECT_PITCH)
    docs/domain-model.md:11:- Composition and audio are long-running workflows backed by durable records, not one-shot request responses.
    docs/domain-model.md:28:| `selected_pitch_id` | Accepted pitch record. |
    docs/domain-model.md:32:| `active_composition_job_id` | Current composition job, if writing or rewrite work is running. |
    docs/domain-model.md:33:| `active_audio_job_id` | Current audio job, if narration work is running. |
    docs/domain-model.md:35:| `latest_audio_asset_id` | Most recent playable final audio artifact. |
    docs/domain-model.md:40:Prompt 11 keeps the relational core intentionally one-directional where practical: child records
    docs/domain-model.md:41:such as pitches, character sheets, beat sheets, and setup revisions point back to the owning
    docs/domain-model.md:54:| `pitch` | One candidate story premise. | batch or generation group, summary, hook, bedtime notes, selection flag. | `selected_pitch_id` on the session represents the accepted pitch; selection does not require a separate table. |
    docs/domain-model.md:59:| `composition_segment` | One planned or written segment of the story. | segment index, planned summary, text, revision number, superseded segment, status. | Supports interruption, partial persistence, and rewrites of earlier sections. |
    docs/domain-model.md:60:| `audio_job` | Parent job record for narration generation. | voice, speed, music setting, progress, status, compiled asset pointer. | Audio should be resumable and segment-aware. |
    docs/domain-model.md:61:| `session_asset` | Durable artifact metadata for session files and exports. | asset kind, object path, MIME type, byte size, checksum, segment index, readiness status. | Covers draft snapshots, composition segments, audio segments, `.docx`, and final audio without scanning object storage. |
    docs/domain-model.md:73:| 4 | `pitches` | Pitches | One pitch is accepted or the user intentionally keeps a current pitch set for further refinement. |
    docs/domain-model.md:74:| 5 | `characters` | Characters | One character sheet is accepted. |
    docs/domain-model.md:75:| 6 | `beats` | Beat sheet | One beat sheet is accepted. |
    docs/domain-model.md:78:| 9 | `audio` | Audio | Final narration assets are generated for the current story text and settings. |
    docs/domain-model.md:95:| `in_progress` | Durable work is actively being produced or updated. | Pitch generation is running, composition is streaming segments, or audio rendering is underway. |
    docs/domain-model.md:96:| `completed` | The stage has an accepted output that is still valid relative to all upstream dependencies. | A beat sheet was accepted and no upstream planning change has made it stale. |
    docs/domain-model.md:97:| `needs_regeneration` | The stage was completed before, but an upstream change made its accepted output stale. The old output may remain visible for comparison, but it is not the current source of truth. | The user edits characters after a beat sheet exists, so beats, composition, audio, and finalize become stale. |
    docs/domain-model.md:112:`genre -> tone -> brief -> pitches -> characters -> beats -> story_setup -> composition -> audio -> finalize`
    docs/domain-model.md:131:| `genre` | `tone`, `brief`, `pitches`, `characters`, `beats`, `composition`, `audio`, `finalize` |
    docs/domain-model.md:132:| `tone` | `brief`, `pitches`, `characters`, `beats`, `composition`, `audio`, `finalize` |
    docs/domain-model.md:133:| `brief` | `pitches`, `characters`, `beats`, `composition`, `audio`, `finalize` |
    docs/domain-model.md:134:| `pitches` | `characters`, `beats`, `composition`, `audio`, `finalize` |
    docs/domain-model.md:135:| `characters` | `beats`, `composition`, `audio`, `finalize` |
    docs/domain-model.md:136:| `beats` | `composition`, `audio`, `finalize` |
    docs/domain-model.md:137:| `story_setup` | `composition`, `audio`, `finalize` |
    docs/domain-model.md:138:| `composition` | `audio`, `finalize` |
    docs/domain-model.md:139:| `audio` | `finalize` |
    docs/domain-model.md:144:- Word count, runtime, and chapter preferences are user intent, not generated story content.
    docs/domain-model.md:145:- They still influence later composition, but a new pitch or character sheet does not automatically erase the user's preferred target length.
    docs/domain-model.md:147:## Composition Interruption and Rewrite Rules
    docs/domain-model.md:149:Composition is intentionally more flexible than the earlier planning stages.
    docs/domain-model.md:153:- A rewrite request against an earlier segment creates a new `composition_job` or new segment revision rather than mutating history in place.
    docs/domain-model.md:155:- Any accepted composition rewrite marks `audio` and `finalize` as `needs_regeneration`.
    docs/domain-model.md:163:   - Example: `genre`, `tone`, and `brief` are `completed`; `pitches` is `in_progress`.
    docs/domain-model.md:164:   - Result: open the session on `resume_stage = pitches`.
    docs/domain-model.md:166:   - Example: `composition`, `audio`, and `finalize` were `completed`, then the user edits the beat sheet.
    docs/domain-model.md:167:   - Result: `composition`, `audio`, and `finalize` become `needs_regeneration`, and `resume_stage = composition`.
    backend/tests/test_event_log_service.py:52:        output_kind=AIOutputKind.PITCH_BATCH,
    backend/tests/test_event_log_service.py:53:        stage=WorkflowStage.PITCHES,
    backend/tests/test_event_log_service.py:54:        generation_key="pitch-batch-1",
    backend/tests/test_event_log_service.py:57:        summary_text="Three bedtime-safe pitches.",
    backend/tests/test_event_log_service.py:94:    event_log.record_audio_progress(
    backend/tests/test_event_log_service.py:96:        job_id="audio-job-1",
    backend/tests/test_event_log_service.py:101:        segment_id="audio-segment-1",
    backend/tests/test_event_log_service.py:126:    assert history.events[1].payload.output_kind == AIOutputKind.PITCH_BATCH
    backend/tests/test_event_log_service.py:142:    assert history.events[6].stage == WorkflowStage.AUDIO
    backend/tests/test_action_policy_service.py:9:    AudioJob,
    backend/tests/test_action_policy_service.py:17:    Pitch,
    backend/tests/test_action_policy_service.py:213:def test_policy_rejects_audio_generation_when_story_text_is_not_ready(db_session) -> None:
    backend/tests/test_action_policy_service.py:227:                        "action_type": "start_audio_generation",
    backend/tests/test_action_policy_service.py:228:                        "target_stage": "audio",
    backend/tests/test_action_policy_service.py:250:def test_policy_rejects_resume_job_when_audio_job_is_not_paused(db_session) -> None:
    backend/tests/test_action_policy_service.py:257:        audio_status=JobStatus.IN_PROGRESS,
    backend/tests/test_action_policy_service.py:267:                        "target_stage": "audio",
    backend/tests/test_action_policy_service.py:272:                            "job_kind": "audio",
    backend/tests/test_action_policy_service.py:327:    audio_status: JobStatus | None = None,
    backend/tests/test_action_policy_service.py:345:        WorkflowStage.PITCHES,
    backend/tests/test_action_policy_service.py:368:    pitch = Pitch(
    backend/tests/test_action_policy_service.py:372:        pitch_index=1,
    backend/tests/test_action_policy_service.py:378:    db_session.add(pitch)
    backend/tests/test_action_policy_service.py:383:        pitch_id=pitch.id,
    backend/tests/test_action_policy_service.py:442:    audio_job = None
    backend/tests/test_action_policy_service.py:443:    if audio_status is not None:
    backend/tests/test_action_policy_service.py:446:            stage=WorkflowStage.AUDIO,
    backend/tests/test_action_policy_service.py:449:        audio_job = AudioJob(
    backend/tests/test_action_policy_service.py:452:            status=audio_status,
    backend/tests/test_action_policy_service.py:457:        db_session.add(audio_job)
    backend/tests/test_action_policy_service.py:478:        "audio_job_id": audio_job.id if audio_job else None,
    docs/contributing.md:24:- Prefer names that describe product concepts directly: `session`, `pitch`, `beat_sheet`, `audio_job`.
    docs/contributing.md:45:- Keep AI-produced runtime assets, exported documents, and generated audio in backend-managed storage locations instead of checking them into git.
    docs/realtime-events.md:4:prompt 17. It is intentionally boring: session-scoped channels, a small number
    docs/realtime-events.md:90:  "stage": "audio",
    docs/realtime-events.md:125:| `job.progress` | yes | Progress checkpoint for composition or audio jobs. |
    docs/realtime-events.md:144:The payload is intentionally the same shape as the durable
    docs/realtime-events.md:201:These events are intentionally ephemeral. Reconnect behavior should rebuild the
    docs/realtime-events.md:207:This event is the replayable progress checkpoint for both composition and audio.
    docs/realtime-events.md:230:- `job_kind` is `composition` or `audio`.
    docs/realtime-events.md:233:- `estimated_duration_seconds` is mainly for audio UX, but it stays available on
    docs/realtime-events.md:259:- audio completed
    docs/realtime-events.md:260:- audio failed with `error_message`
    backend/tests/test_asset_service.py:9:    AudioJob,
    backend/tests/test_asset_service.py:76:    audio_job = AudioJob(
    backend/tests/test_asset_service.py:82:    db_session.add(audio_job)
    backend/tests/test_asset_service.py:106:    audio_segment = service.save_asset_record(
    backend/tests/test_asset_service.py:108:        asset_kind=AssetKind.AUDIO_SEGMENT,
    backend/tests/test_asset_service.py:109:        storage_bucket="storyteller-audio",
    backend/tests/test_asset_service.py:110:        object_path="sessions/story-1/audio/segment-0001.mp3",
    backend/tests/test_asset_service.py:111:        mime_type="audio/mpeg",
    backend/tests/test_asset_service.py:113:        audio_job_id=audio_job.id,
    backend/tests/test_asset_service.py:124:    final_audio = service.save_asset_record(
    backend/tests/test_asset_service.py:126:        asset_kind=AssetKind.FINAL_AUDIO,
    backend/tests/test_asset_service.py:128:        object_path="sessions/story-1/exports/final-audio.mp3",
    backend/tests/test_asset_service.py:129:        mime_type="audio/mpeg",
    backend/tests/test_asset_service.py:131:        audio_job_id=audio_job.id,
    backend/tests/test_asset_service.py:139:    assert audio_segment.segment_index == 0
    backend/tests/test_asset_service.py:141:    assert final_audio.ready_at is not None
    backend/tests/test_asset_service.py:143:        AssetKind.FINAL_AUDIO,
    backend/tests/test_asset_service.py:145:        AssetKind.AUDIO_SEGMENT,
    backend/tests/test_asset_service.py:150:        AssetKind.FINAL_AUDIO,
    backend/tests/test_asset_service.py:216:    audio_job = AudioJob(
    backend/tests/test_asset_service.py:221:    db_session.add_all([composition_job, audio_job])
    backend/tests/test_asset_service.py:242:            asset_kind=AssetKind.FINAL_AUDIO,
    backend/tests/test_asset_service.py:244:            object_path="sessions/story-3/exports/final-audio.mp3",
    backend/tests/test_asset_service.py:245:            mime_type="audio/mpeg",
    backend/tests/test_asset_service.py:246:            audio_job_id=audio_job.id,
    backend/migrations/README.md:12:- story briefs, pitches, character sheets, beat sheets, and story setup revisions
    backend/migrations/README.md:14:- audio jobs
    backend/tests/test_intent_parser_service.py:6:from app.ai import IntentParserTransportError
    backend/tests/test_intent_parser_service.py:10:    IntentParserStatus,
    backend/tests/test_intent_parser_service.py:11:    IntentParserStructuredOutput,
    backend/tests/test_intent_parser_service.py:18:from app.services import SessionEventLogService, SessionIntentParserService, SessionService
    backend/tests/test_intent_parser_service.py:41:class StubIntentParserAdapter:
    backend/tests/test_intent_parser_service.py:42:    def __init__(self, structured_output: IntentParserStructuredOutput) -> None:
    backend/tests/test_intent_parser_service.py:48:        from app.models import IntentParserInvocationResult
    backend/tests/test_intent_parser_service.py:51:        return IntentParserInvocationResult(
    backend/tests/test_intent_parser_service.py:61:class RaisingIntentParserAdapter:
    backend/tests/test_intent_parser_service.py:65:        raise IntentParserTransportError("network timeout")
    backend/tests/test_intent_parser_service.py:71:def test_intent_parser_service_handles_happy_path_updates_and_audits_events(db_session) -> None:
    backend/tests/test_intent_parser_service.py:73:    adapter = StubIntentParserAdapter(
    backend/tests/test_intent_parser_service.py:74:        IntentParserStructuredOutput.model_validate(
    backend/tests/test_intent_parser_service.py:80:                    "I can make the beat sheet moodier and shorten the planned runtime."
    backend/tests/test_intent_parser_service.py:118:    service = SessionIntentParserService(db_session, adapter)
    backend/tests/test_intent_parser_service.py:124:    assert result.status == IntentParserStatus.PARSED
    backend/tests/test_intent_parser_service.py:141:    assert history.events[-2].event_type == SessionEventType.CHAT_INTENT_PARSED
    backend/tests/test_intent_parser_service.py:143:    assert history.events[-2].payload.result.status == IntentParserStatus.PARSED
    backend/tests/test_intent_parser_service.py:152:def test_intent_parser_service_requests_clarification_for_vague_message(db_session) -> None:
    backend/tests/test_intent_parser_service.py:154:    adapter = StubIntentParserAdapter(
    backend/tests/test_intent_parser_service.py:155:        IntentParserStructuredOutput.model_validate(
    backend/tests/test_intent_parser_service.py:172:    result = SessionIntentParserService(db_session, adapter).parse_user_message(
    backend/tests/test_intent_parser_service.py:177:    assert result.status == IntentParserStatus.NEEDS_CLARIFICATION
    backend/tests/test_intent_parser_service.py:183:def test_intent_parser_service_falls_back_gracefully_when_adapter_fails(db_session) -> None:
    backend/tests/test_intent_parser_service.py:185:    result = SessionIntentParserService(
    backend/tests/test_intent_parser_service.py:187:        RaisingIntentParserAdapter(),
    backend/tests/test_intent_parser_service.py:192:    assert result.status == IntentParserStatus.FAILED
    backend/tests/test_intent_parser_service.py:197:    assert history.events[-2].event_type == SessionEventType.CHAT_INTENT_PARSED
    backend/tests/test_intent_parser_service.py:200:    assert history.events[-2].payload.result.status == IntentParserStatus.FAILED
    backend/tests/test_intent_parser_service.py:203:def test_intent_parser_service_uses_updated_ui_context_in_prompt_summary(db_session) -> None:
    backend/tests/test_intent_parser_service.py:218:    adapter = StubIntentParserAdapter(
    backend/tests/test_intent_parser_service.py:219:        IntentParserStructuredOutput.model_validate(
    backend/tests/test_intent_parser_service.py:224:                "assistant_response": "Do you want me to adjust the beat sheet or story setup?",
    backend/tests/test_intent_parser_service.py:234:    SessionIntentParserService(db_session, adapter).parse_user_message(
    backend/tests/test_intent_parser_service.py:240:    assert "Current beat sheet detail: Make the midpoint gentler" in (
    backend/tests/test_intent_parser_service.py:272:        WorkflowStage.PITCHES,
    docs/chat-to-ui-actions.md:3:Prompt 30 establishes the typed contract that chat intent parsing must emit
    docs/chat-to-ui-actions.md:36:| `pitches`     | `regenerate_pitches`, `select_pitch`                                             | Covers “give me more options” and “pick this pitch” flows.                                            |
    docs/chat-to-ui-actions.md:41:| `audio`       | `update_audio_settings`, `start_audio_generation`, `pause_job`, `resume_job`     | Audio settings are separate from the command to start generation.                                     |
    docs/chat-to-ui-actions.md:46:The default policy is intentionally conservative. The parser can propose an
    docs/chat-to-ui-actions.md:55:- `update_audio_settings`
    docs/chat-to-ui-actions.md:61:- All selection actions such as `select_genre`, `select_tone`, `select_pitch`,
    docs/chat-to-ui-actions.md:64:- All composition and audio job control actions
    docs/chat-to-ui-actions.md:122:- `POST /api/v1/sessions/{session_id}/chat/intents`, which now includes
    backend/app/services/conversation_memory.py:172:    if aggregate.selected_pitch is not None:
    backend/app/services/conversation_memory.py:173:        decisions.append(f"Selected pitch: {aggregate.selected_pitch.title}")
    backend/app/services/conversation_memory.py:174:        decisions.append(f"Pitch logline: {_truncate(aggregate.selected_pitch.logline)}")
    backend/app/services/conversation_memory.py:178:            aggregate.selected_character_sheet.title or "Character sheet selected"
    backend/app/services/conversation_memory.py:189:        decisions.append(f"Beat sheet: {_truncate(aggregate.selected_beat_sheet.summary)}")
    backend/app/services/conversation_memory.py:208:    if aggregate.active_audio_job is not None:
    backend/app/services/conversation_memory.py:209:        audio_preferences = [
    backend/app/services/conversation_memory.py:210:            f"voice={aggregate.active_audio_job.voice_key or 'unset'}",
    backend/app/services/conversation_memory.py:211:            f"speed={aggregate.active_audio_job.playback_speed:g}",
    backend/app/services/conversation_memory.py:214:                if aggregate.active_audio_job.include_background_music
    backend/app/services/conversation_memory.py:218:        if aggregate.active_audio_job.music_profile:
    backend/app/services/conversation_memory.py:219:            audio_preferences.append(f"music_profile={aggregate.active_audio_job.music_profile}")
    backend/app/services/conversation_memory.py:220:        preferences.append("Narration settings: " + ", ".join(audio_preferences))
    backend/app/services/conversation_memory.py:258:    if aggregate.active_audio_job is not None:
    backend/app/services/conversation_memory.py:260:            kind="Audio",
    backend/app/services/conversation_memory.py:261:            status=aggregate.active_audio_job.status,
    backend/app/services/conversation_memory.py:262:            stop_reason=aggregate.active_audio_job.stop_reason,
    backend/app/services/conversation_memory.py:284:    if aggregate.active_audio_job is not None:
    backend/app/services/conversation_memory.py:286:            f"Audio job: {aggregate.active_audio_job.status.value}, "
    backend/app/services/conversation_memory.py:287:            f"voice={aggregate.active_audio_job.voice_key or 'unset'}"
    backend/app/services/conversation_memory.py:289:        if aggregate.active_audio_job.current_segment_index is not None:
    backend/app/services/conversation_memory.py:290:            job_summary += f", segment {aggregate.active_audio_job.current_segment_index}"
    backend/app/services/conversation_memory.py:376:        aggregate.selected_pitch.title if aggregate.selected_pitch is not None else None,
    backend/tests/test_migrations.py:11:    "audio_jobs",
    backend/tests/test_migrations.py:19:    "pitches",
    backend/tests/test_storage.py:28:            "STORYTELLER_GCS_AUDIO_BUCKET_NAME": "storyteller-audio",
    backend/tests/test_storage.py:125:    assert paths.audio_segment(
    backend/tests/test_storage.py:127:        job_id="audio-job-02",
    backend/tests/test_storage.py:130:        "gs://storyteller-audio/sessions/session-123/audio/jobs/audio-job-02/segments/0003.mp3"
    backend/tests/test_storage.py:132:    assert paths.final_audio(
    backend/tests/test_storage.py:134:        job_id="audio-job-02",
    backend/tests/test_storage.py:137:        "gs://storyteller-audio/"
    backend/tests/test_storage.py:138:        "sessions/session-123/audio/jobs/audio-job-02/final/bedtime-story.mp3"
    backend/tests/test_storage.py:165:        location = object_storage.paths.audio_segment(
    backend/tests/test_storage.py:167:            job_id="audio-job-1",
    backend/tests/test_storage.py:174:            content_type="audio/mpeg",
    backend/tests/test_storage.py:184:        "storyteller-audio",
    backend/tests/test_storage.py:189:    assert fetched_metadata.content_type == "audio/mpeg"
    backend/tests/test_storage.py:204:        location = object_storage.paths.final_audio(
    backend/tests/test_storage.py:206:            job_id="audio-job-1",
    backend/tests/test_worker_runtime.py:8:from app.worker import JobHandlerRegistry, JobWorker
    backend/tests/test_worker_runtime.py:33:    registry = JobHandlerRegistry()
    backend/tests/test_worker_runtime.py:42:    registry.register("test.handler", handler)
    backend/tests/test_worker_runtime.py:46:        registry=registry,
    backend/tests/test_worker_runtime.py:72:            payload={"message": "no registry entry"},
    backend/tests/test_worker_runtime.py:77:        registry=JobHandlerRegistry(),
    backend/app/services/agent_context.py:36:    if snapshot.selected_pitch is not None:
    backend/app/services/agent_context.py:37:        lines.append(f"Selected pitch: {snapshot.selected_pitch.title}")
    backend/app/services/agent_context.py:38:        lines.append(f"Pitch logline: {_truncate(snapshot.selected_pitch.logline)}")
    backend/app/services/agent_context.py:41:        character_summary = snapshot.selected_character_sheet.title or "Character sheet selected"
    backend/app/services/agent_context.py:49:        lines.append(f"Beat sheet: {_truncate(snapshot.selected_beat_sheet.summary)}")
    backend/app/services/agent_context.py:81:    if snapshot.active_audio_job is not None:
    backend/app/services/agent_context.py:83:            "Audio job: "
    backend/app/services/agent_context.py:84:            f"{snapshot.active_audio_job.status}, "
    backend/app/services/agent_context.py:85:            f"voice={snapshot.active_audio_job.voice_key or 'unset'}"
    backend/tests/test_conversation_memory_evals.py:12:    Pitch,
    backend/tests/test_conversation_memory_evals.py:20:    IntentParserStructuredOutput,
    backend/tests/test_conversation_memory_evals.py:28:    SessionIntentParserService,
    backend/tests/test_conversation_memory_evals.py:54:class StubIntentParserAdapter:
    backend/tests/test_conversation_memory_evals.py:55:    def __init__(self, structured_output: IntentParserStructuredOutput) -> None:
    backend/tests/test_conversation_memory_evals.py:61:        from app.models import IntentParserInvocationResult
    backend/tests/test_conversation_memory_evals.py:64:        return IntentParserInvocationResult(
    backend/tests/test_conversation_memory_evals.py:74:def test_eval_fresh_accepted_decisions_replace_stale_pitch_choices(db_session) -> None:
    backend/tests/test_conversation_memory_evals.py:91:    snapshot = session_service.create_session(working_title="Pitch Freshness")
    backend/tests/test_conversation_memory_evals.py:105:        stage=WorkflowStage.PITCHES,
    backend/tests/test_conversation_memory_evals.py:107:        detail="Selecting the strongest bedtime pitch.",
    backend/tests/test_conversation_memory_evals.py:118:    old_pitch = Pitch(
    backend/tests/test_conversation_memory_evals.py:121:        generation_key="pitch-batch-1",
    backend/tests/test_conversation_memory_evals.py:122:        pitch_index=0,
    backend/tests/test_conversation_memory_evals.py:128:    stale_pitch = Pitch(
    backend/tests/test_conversation_memory_evals.py:131:        generation_key="pitch-batch-1",
    backend/tests/test_conversation_memory_evals.py:132:        pitch_index=1,
    backend/tests/test_conversation_memory_evals.py:137:    new_pitch = Pitch(
    backend/tests/test_conversation_memory_evals.py:140:        generation_key="pitch-batch-2",
    backend/tests/test_conversation_memory_evals.py:141:        pitch_index=0,
    backend/tests/test_conversation_memory_evals.py:146:    db_session.add_all([brief, old_pitch, stale_pitch, new_pitch])
    backend/tests/test_conversation_memory_evals.py:152:        selection_kind=SelectionKind.PITCH,
    backend/tests/test_conversation_memory_evals.py:153:        stage=WorkflowStage.PITCHES,
    backend/tests/test_conversation_memory_evals.py:154:        selection_id=old_pitch.id,
    backend/tests/test_conversation_memory_evals.py:155:        label=old_pitch.title,
    backend/tests/test_conversation_memory_evals.py:159:    old_pitch = db_session.get(Pitch, old_pitch.id)
    backend/tests/test_conversation_memory_evals.py:160:    new_pitch = db_session.get(Pitch, new_pitch.id)
    backend/tests/test_conversation_memory_evals.py:161:    assert old_pitch is not None and new_pitch is not None
    backend/tests/test_conversation_memory_evals.py:162:    old_pitch.is_selected = False
    backend/tests/test_conversation_memory_evals.py:163:    new_pitch.is_selected = True
    backend/tests/test_conversation_memory_evals.py:164:    new_pitch.accepted_at = now
    backend/tests/test_conversation_memory_evals.py:169:        selection_kind=SelectionKind.PITCH,
    backend/tests/test_conversation_memory_evals.py:170:        stage=WorkflowStage.PITCHES,
    backend/tests/test_conversation_memory_evals.py:171:        selection_id=new_pitch.id,
    backend/tests/test_conversation_memory_evals.py:172:        previous_selection_id=old_pitch.id,
    backend/tests/test_conversation_memory_evals.py:173:        label=new_pitch.title,
    backend/tests/test_conversation_memory_evals.py:182:    assert "Selected pitch: The Moonpost Ferry" in latest.summary_text
    backend/tests/test_conversation_memory_evals.py:183:    assert "Selected pitch: Lanterns Across the Docks" not in latest.summary_text
    backend/tests/test_conversation_memory_evals.py:235:        WorkflowStage.PITCHES,
    backend/tests/test_conversation_memory_evals.py:264:        "Latest saved UI detail: Beat sheet: Add one calmer beat before the final return home."
    backend/tests/test_conversation_memory_evals.py:268:        item.startswith("Latest saved UI detail: Beat sheet:")
    backend/tests/test_conversation_memory_evals.py:281:        WorkflowStage.PITCHES,
    backend/tests/test_conversation_memory_evals.py:324:def test_eval_intent_parser_prompt_uses_durable_memory_summary_sections(db_session) -> None:
    backend/tests/test_conversation_memory_evals.py:351:        WorkflowStage.PITCHES,
    backend/tests/test_conversation_memory_evals.py:405:    adapter = StubIntentParserAdapter(
    backend/tests/test_conversation_memory_evals.py:406:        IntentParserStructuredOutput.model_validate(
    backend/tests/test_conversation_memory_evals.py:411:                "assistant_response": "Do you want to adjust the beat sheet or the setup?",
    backend/tests/test_conversation_memory_evals.py:421:    SessionIntentParserService(db_session, adapter).parse_user_message(
    backend/tests/test_conversation_memory_evals.py:431:    assert "Latest saved UI detail: Beat sheet: Soften the midpoint" in rendered_prompt
    docs/frontend-state-architecture.md:60:  label: 'Accepted revised beat sheet',
    backend/tests/test_intent_parser_api.py:10:from app.models import IntentParserInvocationResult, IntentParserStructuredOutput
    backend/tests/test_intent_parser_api.py:16:class StubIntentParserAdapter:
    backend/tests/test_intent_parser_api.py:17:    def __init__(self, structured_output: IntentParserStructuredOutput) -> None:
    backend/tests/test_intent_parser_api.py:24:        return IntentParserInvocationResult(
    backend/tests/test_intent_parser_api.py:35:def intent_parser_api_client(
    backend/tests/test_intent_parser_api.py:38:) -> Iterator[tuple[TestClient, StubIntentParserAdapter]]:
    backend/tests/test_intent_parser_api.py:39:    database_path = tmp_path / "intent-parser-api.sqlite3"
    backend/tests/test_intent_parser_api.py:49:    adapter = StubIntentParserAdapter(
    backend/tests/test_intent_parser_api.py:50:        IntentParserStructuredOutput.model_validate(
    backend/tests/test_intent_parser_api.py:75:    app.state.intent_parser_adapter = adapter
    backend/tests/test_intent_parser_api.py:85:def test_parse_chat_intents_endpoint_returns_structured_actions_and_logs_audit_event(
    backend/tests/test_intent_parser_api.py:86:    intent_parser_api_client: tuple[TestClient, StubIntentParserAdapter],
    backend/tests/test_intent_parser_api.py:88:    client, _adapter = intent_parser_api_client
    backend/tests/test_intent_parser_api.py:96:        f"/api/v1/sessions/{session_id}/chat/intents",
    backend/tests/test_intent_parser_api.py:119:    assert history.events[-2].event_type == "chat.intent.parsed"
    backend/tests/test_intent_parser_api.py:127:def test_parse_chat_intents_endpoint_returns_404_for_missing_session(
    backend/tests/test_intent_parser_api.py:128:    intent_parser_api_client: tuple[TestClient, StubIntentParserAdapter],
    backend/tests/test_intent_parser_api.py:130:    client, _adapter = intent_parser_api_client
    backend/tests/test_intent_parser_api.py:133:        "/api/v1/sessions/missing-session/chat/intents",
    backend/tests/test_intent_parser_api.py:143:def test_parse_chat_intents_endpoint_handles_explicit_commands_without_calling_the_parser(
    backend/tests/test_intent_parser_api.py:144:    intent_parser_api_client: tuple[TestClient, StubIntentParserAdapter],
    backend/tests/test_intent_parser_api.py:146:    client, adapter = intent_parser_api_client
    backend/tests/test_intent_parser_api.py:154:        f"/api/v1/sessions/{session_id}/chat/intents",
    backend/tests/test_intent_parser_api.py:191:    assert history.events[-2].event_type == "chat.intent.parsed"
    backend/tests/test_intent_parser_api.py:197:def test_parse_chat_intents_endpoint_supports_summary_commands_with_no_actions(
    backend/tests/test_intent_parser_api.py:198:    intent_parser_api_client: tuple[TestClient, StubIntentParserAdapter],
    backend/tests/test_intent_parser_api.py:200:    client, adapter = intent_parser_api_client
    backend/tests/test_intent_parser_api.py:208:        f"/api/v1/sessions/{session_id}/chat/intents",
    backend/app/services/action_policy.py:15:    Pitch,
    backend/app/services/action_policy.py:44:    RegeneratePitchesAction,
    backend/app/services/action_policy.py:48:    SelectPitchAction,
    backend/app/services/action_policy.py:50:    StartAudioGenerationAction,
    backend/app/services/action_policy.py:52:    UpdateAudioSettingsAction,
    backend/app/services/action_policy.py:85:    pitch: Pitch | None = None
    backend/app/services/action_policy.py:105:    selected_pitch_id: str | None
    backend/app/services/action_policy.py:111:    active_audio_job_id: str | None
    backend/app/services/action_policy.py:112:    active_audio_job_status: JobStatus | None
    backend/app/services/action_policy.py:114:    ready_audio_asset_kinds: set[AssetKind]
    backend/app/services/action_policy.py:122:        ready_audio_asset_kinds: set[AssetKind],
    backend/app/services/action_policy.py:131:            selected_pitch_id=snapshot.selected_pitch.id if snapshot.selected_pitch else None,
    backend/app/services/action_policy.py:149:            active_audio_job_id=snapshot.active_audio_job.id if snapshot.active_audio_job else None,
    backend/app/services/action_policy.py:150:            active_audio_job_status=(
    backend/app/services/action_policy.py:151:                JobStatus(snapshot.active_audio_job.status)
    backend/app/services/action_policy.py:152:                if snapshot.active_audio_job is not None
    backend/app/services/action_policy.py:156:            ready_audio_asset_kinds=ready_audio_asset_kinds,
    backend/app/services/action_policy.py:183:            ready_audio_asset_kinds=self._load_ready_audio_asset_kinds(snapshot.id),
    backend/app/services/action_policy.py:262:        if action.action_type == ChatToUIActionType.REGENERATE_PITCHES:
    backend/app/services/action_policy.py:263:            return self._evaluate_regenerate_pitches(
    backend/app/services/action_policy.py:268:        if action.action_type == ChatToUIActionType.SELECT_PITCH:
    backend/app/services/action_policy.py:269:            return self._evaluate_select_pitch(
    backend/app/services/action_policy.py:343:        if action.action_type == ChatToUIActionType.UPDATE_AUDIO_SETTINGS:
    backend/app/services/action_policy.py:344:            return self._evaluate_update_audio_settings(
    backend/app/services/action_policy.py:349:        if action.action_type == ChatToUIActionType.START_AUDIO_GENERATION:
    backend/app/services/action_policy.py:350:            return self._evaluate_start_audio_generation(
    backend/app/services/action_policy.py:490:    def _evaluate_regenerate_pitches(
    backend/app/services/action_policy.py:492:        action: RegeneratePitchesAction,
    backend/app/services/action_policy.py:497:        blocked = _blocked_prerequisite_stages(state, WorkflowStage.PITCHES)
    backend/app/services/action_policy.py:499:            return _reject_for_blocked_stages(blocked, target_stage=WorkflowStage.PITCHES)
    backend/app/services/action_policy.py:503:                "Create or accept a story brief before regenerating pitches.",
    backend/app/services/action_policy.py:504:                stage=WorkflowStage.PITCHES,
    backend/app/services/action_policy.py:508:        side_effects = self._build_stage_edit_side_effects(state, WorkflowStage.PITCHES)
    backend/app/services/action_policy.py:515:    def _evaluate_select_pitch(
    backend/app/services/action_policy.py:518:        action: SelectPitchAction,
    backend/app/services/action_policy.py:523:        blocked = _blocked_prerequisite_stages(state, WorkflowStage.PITCHES)
    backend/app/services/action_policy.py:525:            return _reject_for_blocked_stages(blocked, target_stage=WorkflowStage.PITCHES)
    backend/app/services/action_policy.py:529:                "Create or accept a story brief before selecting a pitch.",
    backend/app/services/action_policy.py:530:                stage=WorkflowStage.PITCHES,
    backend/app/services/action_policy.py:533:        if state.stage_statuses.get(WorkflowStage.PITCHES) == WorkflowStageState.NEEDS_REGENERATION:
    backend/app/services/action_policy.py:537:                    "Generate fresh pitches before selecting one because the current "
    backend/app/services/action_policy.py:538:                    "pitch set is stale."
    backend/app/services/action_policy.py:540:                stage=WorkflowStage.PITCHES,
    backend/app/services/action_policy.py:541:                prerequisite_action_types=[ChatToUIActionType.REGENERATE_PITCHES],
    backend/app/services/action_policy.py:544:        pitches = self._find_pitches(session_id, action)
    backend/app/services/action_policy.py:545:        if len(pitches) > 1:
    backend/app/services/action_policy.py:548:                "More than one pitch matched that request in this session.",
    backend/app/services/action_policy.py:549:                stage=WorkflowStage.PITCHES,
    backend/app/services/action_policy.py:551:        if not pitches:
    backend/app/services/action_policy.py:554:                "No pitch matched that request in this session.",
    backend/app/services/action_policy.py:555:                stage=WorkflowStage.PITCHES,
    backend/app/services/action_policy.py:558:        pitch = pitches[0]
    backend/app/services/action_policy.py:559:        if state.selected_pitch_id == pitch.id:
    backend/app/services/action_policy.py:564:                        f"{pitch.title} is already the selected pitch.",
    backend/app/services/action_policy.py:565:                        stage=WorkflowStage.PITCHES,
    backend/app/services/action_policy.py:568:                resolution=_ResolvedAction(pitch=pitch),
    backend/app/services/action_policy.py:571:        side_effects = self._build_stage_edit_side_effects(state, WorkflowStage.PITCHES)
    backend/app/services/action_policy.py:576:            resolution=_ResolvedAction(pitch=pitch),
    backend/app/services/action_policy.py:590:        if state.selected_pitch_id is None:
    backend/app/services/action_policy.py:593:                "Select a pitch before choosing a character sheet.",
    backend/app/services/action_policy.py:595:                prerequisite_action_types=[ChatToUIActionType.SELECT_PITCH],
    backend/app/services/action_policy.py:604:                    "Generate fresh character sheets before selecting one because the "
    backend/app/services/action_policy.py:615:                "More than one character sheet matched that request in this session.",
    backend/app/services/action_policy.py:621:                "No character sheet matched that request in this session.",
    backend/app/services/action_policy.py:627:            character_sheet.pitch_id is not None
    backend/app/services/action_policy.py:628:            and character_sheet.pitch_id != state.selected_pitch_id
    backend/app/services/action_policy.py:633:                    "That character sheet belongs to a different pitch than the one "
    backend/app/services/action_policy.py:643:                        "That character sheet is already selected.",
    backend/app/services/action_policy.py:668:        if state.selected_pitch_id is None:
    backend/app/services/action_policy.py:671:                "Select a pitch before refining the character sheet.",
    backend/app/services/action_policy.py:673:                prerequisite_action_types=[ChatToUIActionType.SELECT_PITCH],
    backend/app/services/action_policy.py:678:                "Select a character sheet before refining it.",
    backend/app/services/action_policy.py:700:        if state.selected_pitch_id is None:
    backend/app/services/action_policy.py:703:                "Select a pitch before regenerating character sheets.",
    backend/app/services/action_policy.py:705:                prerequisite_action_types=[ChatToUIActionType.SELECT_PITCH],
    backend/app/services/action_policy.py:729:                "Select a character sheet before accepting a beat sheet.",
    backend/app/services/action_policy.py:748:                "More than one beat sheet matched that request in this session.",
    backend/app/services/action_policy.py:754:                "No beat sheet matched that request in this session.",
    backend/app/services/action_policy.py:766:                    "That beat sheet belongs to a different character sheet than the one "
    backend/app/services/action_policy.py:776:                        "That beat sheet is already accepted.",
    backend/app/services/action_policy.py:804:                "Select a character sheet before refining the beat sheet.",
    backend/app/services/action_policy.py:811:                "Accept a beat sheet before refining it.",
    backend/app/services/action_policy.py:836:                "Select a character sheet before regenerating beats.",
    backend/app/services/action_policy.py:861:                "Accept a beat sheet before editing story setup.",
    backend/app/services/action_policy.py:886:                "Accept a beat sheet before starting composition.",
    backend/app/services/action_policy.py:1018:    def _evaluate_update_audio_settings(
    backend/app/services/action_policy.py:1020:        action: UpdateAudioSettingsAction,
    backend/app/services/action_policy.py:1025:        blocked = _blocked_prerequisite_stages(state, WorkflowStage.AUDIO)
    backend/app/services/action_policy.py:1027:            return _reject_for_blocked_stages(blocked, target_stage=WorkflowStage.AUDIO)
    backend/app/services/action_policy.py:1031:                "Finish composition and produce story text before editing audio settings.",
    backend/app/services/action_policy.py:1032:                stage=WorkflowStage.AUDIO,
    backend/app/services/action_policy.py:1038:            WorkflowStage.AUDIO,
    backend/app/services/action_policy.py:1039:            force_stop_current_stage_job=state.active_audio_job_status in ACTIVE_JOB_STATUSES,
    backend/app/services/action_policy.py:1047:    def _evaluate_start_audio_generation(
    backend/app/services/action_policy.py:1049:        action: StartAudioGenerationAction,
    backend/app/services/action_policy.py:1054:        blocked = _blocked_prerequisite_stages(state, WorkflowStage.AUDIO)
    backend/app/services/action_policy.py:1056:            return _reject_for_blocked_stages(blocked, target_stage=WorkflowStage.AUDIO)
    backend/app/services/action_policy.py:1060:                "Finish composition and produce story text before starting audio generation.",
    backend/app/services/action_policy.py:1061:                stage=WorkflowStage.AUDIO,
    backend/app/services/action_policy.py:1064:        if state.active_audio_job_status in ACTIVE_JOB_STATUSES:
    backend/app/services/action_policy.py:1067:                "Use pause or resume on the active audio job instead of starting another one.",
    backend/app/services/action_policy.py:1068:                stage=WorkflowStage.AUDIO,
    backend/app/services/action_policy.py:1071:            AssetKind.FINAL_AUDIO in state.ready_audio_asset_kinds
    backend/app/services/action_policy.py:1072:            and not action.extracted_values.regenerate_existing_audio
    backend/app/services/action_policy.py:1076:                "Final audio already exists. Request regeneration explicitly before replacing it.",
    backend/app/services/action_policy.py:1077:                stage=WorkflowStage.AUDIO,
    backend/app/services/action_policy.py:1080:        side_effects = self._build_stage_edit_side_effects(state, WorkflowStage.AUDIO)
    backend/app/services/action_policy.py:1109:            and AssetKind.FINAL_AUDIO not in state.ready_audio_asset_kinds
    backend/app/services/action_policy.py:1113:                "Final audio is not ready to play yet.",
    backend/app/services/action_policy.py:1140:        elif AssetKind.FINAL_AUDIO not in state.ready_audio_asset_kinds:
    backend/app/services/action_policy.py:1143:                "The final audio export is not ready yet.",
    backend/app/services/action_policy.py:1212:            job_status = state.active_audio_job_status
    backend/app/services/action_policy.py:1213:            job_id = state.active_audio_job_id
    backend/app/services/action_policy.py:1267:        elif force_stop_current_stage_job and stage == WorkflowStage.AUDIO:
    backend/app/services/action_policy.py:1271:                    message="The active audio job must stop before the new settings can apply.",
    backend/app/services/action_policy.py:1272:                    job_kind=ChatToUIJobKind.AUDIO.value,
    backend/app/services/action_policy.py:1291:            WorkflowStage.AUDIO in invalidated_stages
    backend/app/services/action_policy.py:1292:            and state.active_audio_job_status in ACTIVE_JOB_STATUSES
    backend/app/services/action_policy.py:1298:                        "The active audio job must stop before the new upstream changes can apply."
    backend/app/services/action_policy.py:1300:                    job_kind=ChatToUIJobKind.AUDIO.value,
    backend/app/services/action_policy.py:1316:        if (stage == WorkflowStage.AUDIO or WorkflowStage.AUDIO in invalidated_stages) and (
    backend/app/services/action_policy.py:1317:            AssetKind.FINAL_AUDIO in state.ready_audio_asset_kinds
    backend/app/services/action_policy.py:1323:                        "Existing final audio will become stale until audio generation runs again."
    backend/app/services/action_policy.py:1325:                    asset_kind=AssetKind.FINAL_AUDIO.value,
    backend/app/services/action_policy.py:1360:        if action.action_type == ChatToUIActionType.REGENERATE_PITCHES:
    backend/app/services/action_policy.py:1361:            self._mark_stage_in_progress(state, WorkflowStage.PITCHES)
    backend/app/services/action_policy.py:1362:            self._invalidate_downstream_stages(state, WorkflowStage.PITCHES)
    backend/app/services/action_policy.py:1365:        if action.action_type == ChatToUIActionType.SELECT_PITCH:
    backend/app/services/action_policy.py:1366:            if resolution.pitch is not None:
    backend/app/services/action_policy.py:1367:                state.selected_pitch_id = resolution.pitch.id
    backend/app/services/action_policy.py:1368:            self._mark_stage_completed(state, WorkflowStage.PITCHES)
    backend/app/services/action_policy.py:1369:            self._invalidate_downstream_stages(state, WorkflowStage.PITCHES)
    backend/app/services/action_policy.py:1422:                state.active_audio_job_status = JobStatus.PAUSED
    backend/app/services/action_policy.py:1429:                state.active_audio_job_status = JobStatus.IN_PROGRESS
    backend/app/services/action_policy.py:1439:        if action.action_type == ChatToUIActionType.UPDATE_AUDIO_SETTINGS:
    backend/app/services/action_policy.py:1440:            self._mark_stage_in_progress(state, WorkflowStage.AUDIO)
    backend/app/services/action_policy.py:1441:            self._invalidate_downstream_stages(state, WorkflowStage.AUDIO)
    backend/app/services/action_policy.py:1444:        if action.action_type == ChatToUIActionType.START_AUDIO_GENERATION:
    backend/app/services/action_policy.py:1445:            state.active_audio_job_id = state.active_audio_job_id or "pending-audio"
    backend/app/services/action_policy.py:1446:            state.active_audio_job_status = JobStatus.IN_PROGRESS
    backend/app/services/action_policy.py:1447:            self._mark_stage_in_progress(state, WorkflowStage.AUDIO)
    backend/app/services/action_policy.py:1448:            self._invalidate_downstream_stages(state, WorkflowStage.AUDIO)
    backend/app/services/action_policy.py:1449:            state.ready_audio_asset_kinds.clear()
    backend/app/services/action_policy.py:1479:        if stage == WorkflowStage.AUDIO or WorkflowStage.AUDIO in get_invalidated_stages_after_edit(
    backend/app/services/action_policy.py:1482:            state.active_audio_job_id = None
    backend/app/services/action_policy.py:1483:            state.active_audio_job_status = None
    backend/app/services/action_policy.py:1484:            state.ready_audio_asset_kinds.clear()
    backend/app/services/action_policy.py:1494:    def _load_ready_audio_asset_kinds(self, session_id: str) -> set[AssetKind]:
    backend/app/services/action_policy.py:1498:            SessionAsset.asset_kind == AssetKind.FINAL_AUDIO,
    backend/app/services/action_policy.py:1527:    def _find_pitches(self, session_id: str, action: SelectPitchAction) -> list[Pitch]:
    backend/app/services/action_policy.py:1529:        stmt: Select[tuple[Pitch]] = select(Pitch).where(Pitch.session_id == session_id)
    backend/app/services/action_policy.py:1530:        if values.pitch_id is not None:
    backend/app/services/action_policy.py:1531:            stmt = stmt.where(Pitch.id == values.pitch_id)
    backend/app/services/action_policy.py:1533:            stmt = stmt.where(Pitch.generation_key == values.generation_key)
    backend/app/services/action_policy.py:1534:        if values.pitch_index is not None:
    backend/app/services/action_policy.py:1535:            stmt = stmt.where(Pitch.pitch_index == values.pitch_index)
    backend/app/services/action_policy.py:1537:            stmt = stmt.where(func.lower(Pitch.title) == values.title.lower())
    backend/tests/test_workflow.py:17:        WorkflowStage.PITCHES,
    backend/tests/test_workflow.py:22:        WorkflowStage.AUDIO,
    backend/tests/test_workflow.py:40:        WorkflowStage.PITCHES,
    backend/tests/test_workflow.py:44:        WorkflowStage.AUDIO,
    backend/tests/test_workflow.py:49:        WorkflowStage.AUDIO,
    backend/tests/test_workflow.py:53:        WorkflowStage.AUDIO,
    backend/tests/test_workflow.py:64:        WorkflowStage.PITCHES: WorkflowStageState.IN_PROGRESS,
    backend/tests/test_workflow.py:68:    assert resolve_resume_stage(stage_states) == WorkflowStage.PITCHES
    backend/tests/test_workflow.py:76:        WorkflowStage.PITCHES: WorkflowStageState.COMPLETED,
    backend/app/services/assets.py:11:    AudioJob,
    backend/app/services/assets.py:54:        audio_job_id: str | None = None,
    backend/app/services/assets.py:64:        audio_job = self._validate_audio_job(session_id, audio_job_id)
    backend/app/services/assets.py:71:            audio_job=audio_job,
    backend/app/services/assets.py:77:        if asset_kind == AssetKind.AUDIO_SEGMENT and resolved_segment_index is None:
    backend/app/services/assets.py:78:            raise ValueError("audio_segment assets require segment_index")
    backend/app/services/assets.py:97:            audio_job_id=audio_job.id if audio_job else None,
    backend/app/services/assets.py:218:    def _validate_audio_job(self, session_id: str, audio_job_id: str | None) -> AudioJob | None:
    backend/app/services/assets.py:219:        if audio_job_id is None:
    backend/app/services/assets.py:222:        audio_job = self._session.get(AudioJob, audio_job_id)
    backend/app/services/assets.py:223:        if audio_job is None or audio_job.session_id != session_id:
    backend/app/services/assets.py:225:                f"audio job {audio_job_id!r} does not belong to session {session_id!r}"
    backend/app/services/assets.py:227:        return audio_job
    backend/app/services/assets.py:235:        audio_job: AudioJob | None,
    backend/app/services/assets.py:250:        if asset_kind == AssetKind.AUDIO_SEGMENT and audio_job is None:
    backend/app/services/assets.py:251:            raise ValueError("audio_segment assets require audio_job_id")
    backend/app/services/assets.py:253:        if asset_kind == AssetKind.FINAL_AUDIO and audio_job is None:
    backend/app/services/assets.py:254:            raise ValueError("final_audio assets require audio_job_id")
    backend/tests/test_health.py:23:            "storyteller-sessions, storyteller-audio, storyteller-exports at "
    docs/adr/0001-core-runtime-architecture.md:8:Storyteller is a session-based bedtime story studio, not a single-shot prompt demo. A user needs to move through a staged workflow, leave, come back later, and still see the current plan, generated text, generated audio, and recent activity.
    docs/adr/0001-core-runtime-architecture.md:14:- composition and audio generation are too slow and failure-prone to run inside request threads
    docs/adr/0001-core-runtime-architecture.md:41:- brief, pitch batch, selected pitch
    docs/adr/0001-core-runtime-architecture.md:42:- character sheet candidates and selection
    docs/adr/0001-core-runtime-architecture.md:43:- beat sheet
    docs/adr/0001-core-runtime-architecture.md:46:- audio jobs and segment progress
    docs/adr/0001-core-runtime-architecture.md:56:- Story exports, intermediate composition files, narration segments, and final audio artifacts live in object storage.
    docs/adr/0001-core-runtime-architecture.md:63:The browser needs live updates during composition and audio generation, and those updates need to remain tied to durable backend state.
    docs/adr/0001-core-runtime-architecture.md:73:Composition and audio generation run in a worker process that is separate from the API process.
    docs/adr/0001-core-runtime-architecture.md:85:- They guide pitch generation, beat planning, and composition prompts.
    backend/app/services/intent_parser.py:7:    IntentParserAdapter,
    backend/app/services/intent_parser.py:8:    IntentParserTransportError,
    backend/app/services/intent_parser.py:9:    build_intent_parser_invocation,
    backend/app/services/intent_parser.py:18:    IntentParserPromptContext,
    backend/app/services/intent_parser.py:19:    IntentParserStageContext,
    backend/app/services/intent_parser.py:20:    IntentParserStatus,
    backend/app/services/intent_parser.py:21:    IntentParserStructuredOutput,
    backend/app/services/intent_parser.py:22:    ParsedChatIntentResponse,
    backend/app/services/intent_parser.py:34:class SessionIntentParserService:
    backend/app/services/intent_parser.py:35:    def __init__(self, session: Session, parser: IntentParserAdapter | None = None):
    backend/app/services/intent_parser.py:47:    ) -> ParsedChatIntentResponse:
    backend/app/services/intent_parser.py:82:                raise RuntimeError("intent parser adapter is required for free-form chat parsing")
    backend/app/services/intent_parser.py:84:            invocation = build_intent_parser_invocation(
    backend/app/services/intent_parser.py:96:            except (IntentParserTransportError, ValidationError):
    backend/app/services/intent_parser.py:99:        if result.status == IntentParserStatus.PARSED and result.proposed_actions.actions:
    backend/app/services/intent_parser.py:109:        self._event_log.record_chat_intent_parsed(
    backend/app/services/intent_parser.py:129:            source="intent_parser",
    backend/app/services/intent_parser.py:136:    structured_output: IntentParserStructuredOutput,
    backend/app/services/intent_parser.py:137:) -> ParsedChatIntentResponse:
    backend/app/services/intent_parser.py:138:    if structured_output.status != IntentParserStatus.PARSED:
    backend/app/services/intent_parser.py:139:        return ParsedChatIntentResponse(
    backend/app/services/intent_parser.py:150:    return ParsedChatIntentResponse(
    backend/app/services/intent_parser.py:151:        status=IntentParserStatus.PARSED,
    backend/app/services/intent_parser.py:159:def _build_failed_result() -> ParsedChatIntentResponse:
    backend/app/services/intent_parser.py:160:    return ParsedChatIntentResponse(
    backend/app/services/intent_parser.py:161:        status=IntentParserStatus.FAILED,
    backend/app/services/intent_parser.py:164:            "Please rephrase the change you want, like tone, runtime, beats, or audio settings."
    backend/app/services/intent_parser.py:173:) -> IntentParserPromptContext:
    backend/app/services/intent_parser.py:176:    return IntentParserPromptContext(
    backend/app/services/intent_parser.py:181:        stage_context=IntentParserStageContext(
    backend/app/services/intent_parser.py:205:) -> ParsedChatIntentResponse:
    backend/app/services/intent_parser.py:218:    elif explicit_command.command_id == ExplicitChatCommandId.REGENERATE_PITCHES:
    backend/app/services/intent_parser.py:220:            "I can queue a fresh set of pitch options from the current bedtime brief."
    backend/app/services/intent_parser.py:229:    return ParsedChatIntentResponse(
    backend/app/services/intent_parser.py:230:        status=IntentParserStatus.PARSED,
    backend/app/services/intent_parser.py:269:    if snapshot.selected_pitch is not None:
    backend/app/services/intent_parser.py:270:        plan_parts.append(f'pitch "{snapshot.selected_pitch.title}"')
    backend/app/services/intent_parser.py:287:    elif snapshot.active_audio_job is not None:
    backend/app/services/intent_parser.py:289:            f"audio is {snapshot.active_audio_job.status.replace('_', ' ')}"
    backend/tests/test_realtime_contracts.py:50:                "invalidated_stages": ["pitches", "characters"],
    backend/tests/test_realtime_contracts.py:51:                "current_stage": "pitches",
    backend/tests/test_realtime_contracts.py:52:                "resume_stage": "pitches",
    backend/tests/test_realtime_contracts.py:85:    assert durable_event.payload.current_stage == WorkflowStage.PITCHES
    backend/tests/test_realtime_contracts.py:133:            "stage": "pitches",
    backend/tests/test_realtime_contracts.py:140:                "content": "Here are three gentler pitch options.",
    backend/app/services/__init__.py:16:from app.services.intent_parser import SessionIntentParserService
    backend/app/services/__init__.py:47:    "SessionIntentParserService",
    backend/app/worker/__main__.py:10:from app.worker.default_handlers import build_default_job_handler_registry
    backend/app/worker/__main__.py:51:        registry=build_default_job_handler_registry(),
    backend/app/worker/README.md:9:- `registry.py`: handler registry for mapping `job_type` strings to Python callables
    backend/app/services/event_log.py:14:    AudioProgressEventPayload,
    backend/app/services/event_log.py:15:    ChatIntentParsedEventPayload,
    backend/app/services/event_log.py:34:from app.models.intent_parser import ParsedChatIntentResponse
    backend/app/services/event_log.py:50:DEFAULT_INTENT_PARSER_ACTOR = SessionEventActor(
    backend/app/services/event_log.py:52:    actor_id="intent-parser",
    backend/app/services/event_log.py:294:    def record_chat_intent_parsed(
    backend/app/services/event_log.py:308:        result: ParsedChatIntentResponse,
    backend/app/services/event_log.py:314:            summary = "Parsed chat intent without actionable UI changes."
    backend/app/services/event_log.py:316:            summary = "Parsed chat intent into 1 proposed action."
    backend/app/services/event_log.py:318:            summary = f"Parsed chat intent into {action_count} proposed actions."
    backend/app/services/event_log.py:322:            actor=actor or DEFAULT_INTENT_PARSER_ACTOR,
    backend/app/services/event_log.py:323:            event_type=SessionEventType.CHAT_INTENT_PARSED,
    backend/app/services/event_log.py:326:            payload=ChatIntentParsedEventPayload(
    backend/app/services/event_log.py:403:    def record_audio_progress(
    backend/app/services/event_log.py:418:            f"Audio progress {progress_percent:.1f}%."
    backend/app/services/event_log.py:420:            else "Recorded audio progress."
    backend/app/services/event_log.py:425:            event_type=SessionEventType.AUDIO_PROGRESS_RECORDED,
    backend/app/services/event_log.py:427:            stage=WorkflowStage.AUDIO,
    backend/app/services/event_log.py:428:            payload=AudioProgressEventPayload(
    docs/product-brief.md:5:Storyteller is a session-based bedtime story creation studio. It helps a user move from a loose story idea to a finished written story and finished narration audio, with the ability to leave and come back later without losing progress.
    docs/product-brief.md:24:4. Story pitches generated by Gemini, with selection, refinement, or regeneration.
    docs/product-brief.md:25:5. Character sheet generation, again with selection and refinement.
    docs/product-brief.md:26:6. Save-the-Cat beat sheet generation and editing.
    docs/product-brief.md:29:9. Audio configuration and audio generation, including voice and speed controls plus optional background music.
    docs/product-brief.md:30:10. Finalize, where the user can read, listen, and download story and audio artifacts.
    docs/product-brief.md:57:- Users can interrupt, redirect, and request rewrites.
    docs/product-brief.md:59:### Audio Experience
    docs/product-brief.md:62:- Audio generation is segmented and resumable.
    docs/product-brief.md:64:- Final audio should be playable in-app and downloadable.
    docs/product-brief.md:82:- generate, play, and download narration audio
    docs/secrets-and-local-config.md:84:    audio: storyteller-audio
    docs/secrets-and-local-config.md:93:  enable_audio_generation: false
    docs/secrets-and-local-config.md:104:- `gcs.buckets.audio`
    docs/secrets-and-local-config.md:122:- `STORYTELLER_GCS_AUDIO_BUCKET_NAME`
    docs/secrets-and-local-config.md:126:- `STORYTELLER_FEATURE_ENABLE_AUDIO_GENERATION`
    backend/app/worker/runtime.py:18:from app.worker.registry import JobHandlerRegistry
    backend/app/worker/runtime.py:54:        registry: JobHandlerRegistry,
    backend/app/worker/runtime.py:60:        self._registry = registry
    backend/app/worker/runtime.py:75:        handler = self._registry.get(claim.job_type)
    backend/app/worker/runtime.py:155:            ", ".join(self._registry.registered_job_types()) or "none",
    docs/chat-to-ui-actions.schema.json:15:    "regenerate_pitches": "confirm_first",
    docs/chat-to-ui-actions.schema.json:19:    "select_pitch": "confirm_first",
    docs/chat-to-ui-actions.schema.json:21:    "start_audio_generation": "confirm_first",
    docs/chat-to-ui-actions.schema.json:23:    "update_audio_settings": "auto_apply_candidate",
    docs/chat-to-ui-actions.schema.json:100:              "title": "Beat Sheet Id"
    docs/chat-to-ui-actions.schema.json:126:          "enum": ["composition", "audio"],
    docs/chat-to-ui-actions.schema.json:131:          "enum": ["fresh", "continue", "rewrite"],
    docs/chat-to-ui-actions.schema.json:192:          "enum": ["story_docx", "final_audio"],
    docs/chat-to-ui-actions.schema.json:407:              "enum": ["composition", "audio"],
    docs/chat-to-ui-actions.schema.json:490:            "rewrite_from_segment_index": {
    docs/chat-to-ui-actions.schema.json:501:              "title": "Rewrite From Segment Index"
    docs/chat-to-ui-actions.schema.json:837:        "RegeneratePitchesAction": {
    docs/chat-to-ui-actions.schema.json:841:              "const": "regenerate_pitches",
    docs/chat-to-ui-actions.schema.json:842:              "default": "regenerate_pitches",
    docs/chat-to-ui-actions.schema.json:853:              "$ref": "#/$defs/RegeneratePitchesValues"
    docs/chat-to-ui-actions.schema.json:879:              "const": "pitches",
    docs/chat-to-ui-actions.schema.json:880:              "default": "pitches",
    docs/chat-to-ui-actions.schema.json:886:          "title": "RegeneratePitchesAction",
    docs/chat-to-ui-actions.schema.json:889:        "RegeneratePitchesValues": {
    docs/chat-to-ui-actions.schema.json:919:            "preserve_selected_pitch": {
    docs/chat-to-ui-actions.schema.json:921:              "title": "Preserve Selected Pitch",
    docs/chat-to-ui-actions.schema.json:925:          "title": "RegeneratePitchesValues",
    docs/chat-to-ui-actions.schema.json:970:              "enum": ["composition", "audio"],
    docs/chat-to-ui-actions.schema.json:1054:              "title": "Character Sheet Id"
    docs/chat-to-ui-actions.schema.json:1188:        "SelectPitchAction": {
    docs/chat-to-ui-actions.schema.json:1192:              "const": "select_pitch",
    docs/chat-to-ui-actions.schema.json:1193:              "default": "select_pitch",
    docs/chat-to-ui-actions.schema.json:1204:              "$ref": "#/$defs/SelectPitchValues"
    docs/chat-to-ui-actions.schema.json:1230:              "const": "pitches",
    docs/chat-to-ui-actions.schema.json:1231:              "default": "pitches",
    docs/chat-to-ui-actions.schema.json:1241:          "title": "SelectPitchAction",
    docs/chat-to-ui-actions.schema.json:1244:        "SelectPitchValues": {
    docs/chat-to-ui-actions.schema.json:1260:            "pitch_id": {
    docs/chat-to-ui-actions.schema.json:1271:              "title": "Pitch Id"
    docs/chat-to-ui-actions.schema.json:1273:            "pitch_index": {
    docs/chat-to-ui-actions.schema.json:1284:              "title": "Pitch Index"
    docs/chat-to-ui-actions.schema.json:1300:          "title": "SelectPitchValues",
    docs/chat-to-ui-actions.schema.json:1405:        "StartAudioGenerationAction": {
    docs/chat-to-ui-actions.schema.json:1409:              "const": "start_audio_generation",
    docs/chat-to-ui-actions.schema.json:1410:              "default": "start_audio_generation",
    docs/chat-to-ui-actions.schema.json:1421:              "$ref": "#/$defs/StartAudioGenerationValues"
    docs/chat-to-ui-actions.schema.json:1447:              "const": "audio",
    docs/chat-to-ui-actions.schema.json:1448:              "default": "audio",
    docs/chat-to-ui-actions.schema.json:1454:          "title": "StartAudioGenerationAction",
    docs/chat-to-ui-actions.schema.json:1457:        "StartAudioGenerationValues": {
    docs/chat-to-ui-actions.schema.json:1499:            "regenerate_existing_audio": {
    docs/chat-to-ui-actions.schema.json:1501:              "title": "Regenerate Existing Audio",
    docs/chat-to-ui-actions.schema.json:1518:          "title": "StartAudioGenerationValues",
    docs/chat-to-ui-actions.schema.json:1615:        "UpdateAudioSettingsAction": {
    docs/chat-to-ui-actions.schema.json:1619:              "const": "update_audio_settings",
    docs/chat-to-ui-actions.schema.json:1620:              "default": "update_audio_settings",
    docs/chat-to-ui-actions.schema.json:1631:              "$ref": "#/$defs/UpdateAudioSettingsValues"
    docs/chat-to-ui-actions.schema.json:1657:              "const": "audio",
    docs/chat-to-ui-actions.schema.json:1658:              "default": "audio",
    docs/chat-to-ui-actions.schema.json:1668:          "title": "UpdateAudioSettingsAction",
    docs/chat-to-ui-actions.schema.json:1671:        "UpdateAudioSettingsValues": {
    docs/chat-to-ui-actions.schema.json:1740:          "title": "UpdateAudioSettingsValues",
    docs/chat-to-ui-actions.schema.json:1985:            "pitches",
    docs/chat-to-ui-actions.schema.json:1990:            "audio",
    docs/chat-to-ui-actions.schema.json:2009:          "regenerate_pitches": "#/$defs/RegeneratePitchesAction",
    docs/chat-to-ui-actions.schema.json:2013:          "select_pitch": "#/$defs/SelectPitchAction",
    docs/chat-to-ui-actions.schema.json:2015:          "start_audio_generation": "#/$defs/StartAudioGenerationAction",
    docs/chat-to-ui-actions.schema.json:2017:          "update_audio_settings": "#/$defs/UpdateAudioSettingsAction",
    docs/chat-to-ui-actions.schema.json:2037:          "$ref": "#/$defs/RegeneratePitchesAction"
    docs/chat-to-ui-actions.schema.json:2040:          "$ref": "#/$defs/SelectPitchAction"
    docs/chat-to-ui-actions.schema.json:2076:          "$ref": "#/$defs/UpdateAudioSettingsAction"
    docs/chat-to-ui-actions.schema.json:2079:          "$ref": "#/$defs/StartAudioGenerationAction"
    docs/chat-to-ui-actions.schema.json:2161:              "title": "Beat Sheet Id"
    docs/chat-to-ui-actions.schema.json:2187:          "enum": ["composition", "audio"],
    docs/chat-to-ui-actions.schema.json:2192:          "enum": ["fresh", "continue", "rewrite"],
    docs/chat-to-ui-actions.schema.json:2253:          "enum": ["story_docx", "final_audio"],
    docs/chat-to-ui-actions.schema.json:2468:              "enum": ["composition", "audio"],
    docs/chat-to-ui-actions.schema.json:2551:            "rewrite_from_segment_index": {
    docs/chat-to-ui-actions.schema.json:2562:              "title": "Rewrite From Segment Index"
    docs/chat-to-ui-actions.schema.json:2898:        "RegeneratePitchesAction": {
    docs/chat-to-ui-actions.schema.json:2902:              "const": "regenerate_pitches",
    docs/chat-to-ui-actions.schema.json:2903:              "default": "regenerate_pitches",
    docs/chat-to-ui-actions.schema.json:2914:              "$ref": "#/$defs/RegeneratePitchesValues"
    docs/chat-to-ui-actions.schema.json:2940:              "const": "pitches",
    docs/chat-to-ui-actions.schema.json:2941:              "default": "pitches",
    docs/chat-to-ui-actions.schema.json:2947:          "title": "RegeneratePitchesAction",
    docs/chat-to-ui-actions.schema.json:2950:        "RegeneratePitchesValues": {
    docs/chat-to-ui-actions.schema.json:2980:            "preserve_selected_pitch": {
    docs/chat-to-ui-actions.schema.json:2982:              "title": "Preserve Selected Pitch",
    docs/chat-to-ui-actions.schema.json:2986:          "title": "RegeneratePitchesValues",
    docs/chat-to-ui-actions.schema.json:3031:              "enum": ["composition", "audio"],
    docs/chat-to-ui-actions.schema.json:3115:              "title": "Character Sheet Id"
    docs/chat-to-ui-actions.schema.json:3249:        "SelectPitchAction": {
    docs/chat-to-ui-actions.schema.json:3253:              "const": "select_pitch",
    docs/chat-to-ui-actions.schema.json:3254:              "default": "select_pitch",
    docs/chat-to-ui-actions.schema.json:3265:              "$ref": "#/$defs/SelectPitchValues"
    docs/chat-to-ui-actions.schema.json:3291:              "const": "pitches",
    docs/chat-to-ui-actions.schema.json:3292:              "default": "pitches",
    docs/chat-to-ui-actions.schema.json:3302:          "title": "SelectPitchAction",
    docs/chat-to-ui-actions.schema.json:3305:        "SelectPitchValues": {
    docs/chat-to-ui-actions.schema.json:3321:            "pitch_id": {
    docs/chat-to-ui-actions.schema.json:3332:              "title": "Pitch Id"
    docs/chat-to-ui-actions.schema.json:3334:            "pitch_index": {
    docs/chat-to-ui-actions.schema.json:3345:              "title": "Pitch Index"
    docs/chat-to-ui-actions.schema.json:3361:          "title": "SelectPitchValues",
    docs/chat-to-ui-actions.schema.json:3466:        "StartAudioGenerationAction": {
    docs/chat-to-ui-actions.schema.json:3470:              "const": "start_audio_generation",
    docs/chat-to-ui-actions.schema.json:3471:              "default": "start_audio_generation",
    docs/chat-to-ui-actions.schema.json:3482:              "$ref": "#/$defs/StartAudioGenerationValues"
    docs/chat-to-ui-actions.schema.json:3508:              "const": "audio",
    docs/chat-to-ui-actions.schema.json:3509:              "default": "audio",
    docs/chat-to-ui-actions.schema.json:3515:          "title": "StartAudioGenerationAction",
    docs/chat-to-ui-actions.schema.json:3518:        "StartAudioGenerationValues": {
    docs/chat-to-ui-actions.schema.json:3560:            "regenerate_existing_audio": {
    docs/chat-to-ui-actions.schema.json:3562:              "title": "Regenerate Existing Audio",
    docs/chat-to-ui-actions.schema.json:3579:          "title": "StartAudioGenerationValues",
    docs/chat-to-ui-actions.schema.json:3676:        "UpdateAudioSettingsAction": {
    docs/chat-to-ui-actions.schema.json:3680:              "const": "update_audio_settings",
    docs/chat-to-ui-actions.schema.json:3681:              "default": "update_audio_settings",
    docs/chat-to-ui-actions.schema.json:3692:              "$ref": "#/$defs/UpdateAudioSettingsValues"
    docs/chat-to-ui-actions.schema.json:3718:              "const": "audio",
    docs/chat-to-ui-actions.schema.json:3719:              "default": "audio",
    docs/chat-to-ui-actions.schema.json:3729:          "title": "UpdateAudioSettingsAction",
    docs/chat-to-ui-actions.schema.json:3732:        "UpdateAudioSettingsValues": {
    docs/chat-to-ui-actions.schema.json:3801:          "title": "UpdateAudioSettingsValues",
    docs/chat-to-ui-actions.schema.json:4046:            "pitches",
    docs/chat-to-ui-actions.schema.json:4051:            "audio",
    docs/chat-to-ui-actions.schema.json:4074:                "regenerate_pitches": "#/$defs/RegeneratePitchesAction",
    docs/chat-to-ui-actions.schema.json:4078:                "select_pitch": "#/$defs/SelectPitchAction",
    docs/chat-to-ui-actions.schema.json:4080:                "start_audio_generation": "#/$defs/StartAudioGenerationAction",
    docs/chat-to-ui-actions.schema.json:4082:                "update_audio_settings": "#/$defs/UpdateAudioSettingsAction",
    docs/chat-to-ui-actions.schema.json:4102:                "$ref": "#/$defs/RegeneratePitchesAction"
    docs/chat-to-ui-actions.schema.json:4105:                "$ref": "#/$defs/SelectPitchAction"
    docs/chat-to-ui-actions.schema.json:4141:                "$ref": "#/$defs/UpdateAudioSettingsAction"
    docs/chat-to-ui-actions.schema.json:4144:                "$ref": "#/$defs/StartAudioGenerationAction"
    docs/chat-to-ui-actions.schema.json:4172:    "pitches",
    docs/chat-to-ui-actions.schema.json:4177:    "audio",
    backend/app/services/sessions.py:8:    AudioJob,
    backend/app/services/sessions.py:18:    AudioJobView,
    backend/app/services/sessions.py:23:    PitchView,
    backend/app/services/sessions.py:72:    WorkflowStage.PITCHES: UserEditTargetKind.PITCH,
    backend/app/services/sessions.py:77:    WorkflowStage.AUDIO: UserEditTargetKind.AUDIO_SETTINGS,
    backend/app/services/sessions.py:415:            pitch_title=aggregate.selected_pitch.title if aggregate.selected_pitch else None,
    backend/app/services/sessions.py:438:        selected_pitch=_build_pitch_view(aggregate.selected_pitch),
    backend/app/services/sessions.py:443:        active_audio_job=_build_audio_job_view(aggregate.active_audio_job),
    backend/app/services/sessions.py:445:        latest_audio_asset=_build_session_asset_view(aggregate.latest_audio_asset),
    backend/app/services/sessions.py:540:def _build_pitch_view(row) -> PitchView | None:
    backend/app/services/sessions.py:544:    return PitchView(
    backend/app/services/sessions.py:547:        pitch_index=row.pitch_index,
    backend/app/services/sessions.py:623:def _build_audio_job_view(row: AudioJob | None) -> AudioJobView | None:
    backend/app/services/sessions.py:627:    return AudioJobView(
    backend/app/services/sessions.py:671:    pitch_title: str | None = None,
    backend/app/services/sessions.py:675:    for candidate in (working_title, pitch_title, normalized_summary, raw_brief):
    backend/app/worker/__init__.py:1:from app.worker.default_handlers import build_default_job_handler_registry
    backend/app/worker/__init__.py:2:from app.worker.registry import JobHandlerRegistry
    backend/app/worker/__init__.py:7:    "JobHandlerRegistry",
    backend/app/worker/__init__.py:9:    "build_default_job_handler_registry",
    backend/tests/test_intent_parser_adapter.py:7:    GeminiIntentParserAdapter,
    backend/tests/test_intent_parser_adapter.py:8:    get_intent_parser_response_schema,
    backend/tests/test_intent_parser_adapter.py:9:    render_intent_parser_prompt,
    backend/tests/test_intent_parser_adapter.py:11:from app.ai.intent_parser import build_intent_parser_invocation
    backend/tests/test_intent_parser_adapter.py:13:    IntentParserPromptContext,
    backend/tests/test_intent_parser_adapter.py:14:    IntentParserStageContext,
    backend/tests/test_intent_parser_adapter.py:15:    IntentParserStatus,
    backend/tests/test_intent_parser_adapter.py:21:def _build_context() -> IntentParserPromptContext:
    backend/tests/test_intent_parser_adapter.py:22:    return IntentParserPromptContext(
    backend/tests/test_intent_parser_adapter.py:27:        stage_context=IntentParserStageContext(
    backend/tests/test_intent_parser_adapter.py:29:            current_stage_label="Beat sheet",
    backend/tests/test_intent_parser_adapter.py:30:            current_stage_description="Store the accepted Save-the-Cat beat sheet for the session.",
    backend/tests/test_intent_parser_adapter.py:43:def test_render_intent_parser_prompt_includes_guardrails_and_context() -> None:
    backend/tests/test_intent_parser_adapter.py:44:    prompt = render_intent_parser_prompt(_build_context())
    backend/tests/test_intent_parser_adapter.py:46:    assert "backend-only chat intent parser" in prompt
    backend/tests/test_intent_parser_adapter.py:53:def test_intent_parser_response_schema_strips_unsupported_json_schema_keywords() -> None:
    backend/tests/test_intent_parser_adapter.py:54:    schema_json = json.dumps(get_intent_parser_response_schema(), sort_keys=True)
    backend/tests/test_intent_parser_adapter.py:63:def test_gemini_intent_parser_adapter_requests_json_schema_and_parses_response() -> None:
    backend/tests/test_intent_parser_adapter.py:84:                                                "I can make the beat sheet moodier "
    backend/tests/test_intent_parser_adapter.py:125:    adapter = GeminiIntentParserAdapter(
    backend/tests/test_intent_parser_adapter.py:131:    invocation = build_intent_parser_invocation(
    backend/tests/test_intent_parser_adapter.py:150:    assert result.structured_output.status == IntentParserStatus.PARSED
    backend/tests/test_intent_parser_adapter.py:152:    assert result.invocation.prompt_version == "intent_parser.v1"
    backend/app/worker/default_handlers.py:6:from app.worker.registry import JobHandlerRegistry
    backend/app/worker/default_handlers.py:10:def build_default_job_handler_registry() -> JobHandlerRegistry:
    backend/app/worker/default_handlers.py:11:    registry = JobHandlerRegistry()
    backend/app/worker/default_handlers.py:12:    registry.register("demo.echo", demo_echo_handler)
    backend/app/worker/default_handlers.py:13:    return registry
    backend/app/data/genre_tone_catalog.yaml:255:    description: Drifting, surreal adventures that feel secure, beautiful, and intentionally sleepy.
    backend/app/worker/registry.py:9:class JobHandlerRegistry:
    backend/app/models/workflow.py:12:    PITCHES = "pitches"
    backend/app/models/workflow.py:17:    AUDIO = "audio"
    backend/app/models/workflow.py:44:            WorkflowStage.PITCHES,
    backend/app/models/workflow.py:48:            WorkflowStage.AUDIO,
    backend/app/models/workflow.py:58:            WorkflowStage.PITCHES,
    backend/app/models/workflow.py:62:            WorkflowStage.AUDIO,
    backend/app/models/workflow.py:73:            WorkflowStage.PITCHES,
    backend/app/models/workflow.py:77:            WorkflowStage.AUDIO,
    backend/app/models/workflow.py:82:        id=WorkflowStage.PITCHES,
    backend/app/models/workflow.py:83:        label="Pitches",
    backend/app/models/workflow.py:89:            WorkflowStage.AUDIO,
    backend/app/models/workflow.py:97:            "Define the accepted character sheet that later planning and writing will reference."
    backend/app/models/workflow.py:102:            WorkflowStage.AUDIO,
    backend/app/models/workflow.py:108:        label="Beat sheet",
    backend/app/models/workflow.py:109:        description="Store the accepted Save-the-Cat beat sheet for the session.",
    backend/app/models/workflow.py:112:            WorkflowStage.AUDIO,
    backend/app/models/workflow.py:124:            WorkflowStage.AUDIO,
    backend/app/models/workflow.py:132:            "Write the story durably in segments, with room for interruption and targeted rewrites."
    backend/app/models/workflow.py:135:            WorkflowStage.AUDIO,
    backend/app/models/workflow.py:140:        id=WorkflowStage.AUDIO,
    backend/app/models/workflow.py:141:        label="Audio",
    backend/app/models/workflow.py:142:        description="Configure narration settings and generate resumable audio artifacts.",
    docs/realtime-events.schema.json:553:            "audio"
    docs/realtime-events.schema.json:1326:            "pitches",
    docs/realtime-events.schema.json:1331:            "audio",
    backend/tests/test_db_models.py:9:    AudioJob,
    backend/tests/test_db_models.py:20:    Pitch,
    backend/tests/test_db_models.py:101:                    stage=WorkflowStage.PITCHES,
    backend/tests/test_db_models.py:137:        pitch = Pitch(
    backend/tests/test_db_models.py:140:            generation_key="pitch-batch-1",
    backend/tests/test_db_models.py:141:            pitch_index=0,
    backend/tests/test_db_models.py:149:            pitch=pitch,
    backend/tests/test_db_models.py:204:        audio_job = AudioJob(
    backend/tests/test_db_models.py:214:        final_audio = SessionAsset(
    backend/tests/test_db_models.py:216:            audio_job=audio_job,
    backend/tests/test_db_models.py:217:            asset_kind=AssetKind.FINAL_AUDIO,
    backend/tests/test_db_models.py:220:            object_path="sessions/final-audio.mp3",
    backend/tests/test_db_models.py:221:            mime_type="audio/mpeg",
    backend/tests/test_db_models.py:233:                pitch,
    backend/tests/test_db_models.py:240:                audio_job,
    backend/tests/test_db_models.py:241:                final_audio,
    backend/tests/test_db_models.py:271:        assert session_rows[1].audio_jobs[0].status == JobStatus.COMPLETED
    backend/tests/test_db_models.py:272:        assert session_rows[1].assets[0].asset_kind == AssetKind.FINAL_AUDIO
    backend/tests/test_db_models.py:288:            "audio_jobs",
    backend/tests/test_db_models.py:295:            "pitches",
    backend/tests/test_db_models.py:317:            "ix_session_assets_audio_job_id_asset_kind_segment_index",
    backend/tests/test_db_models.py:326:        pitch_foreign_keys = {
    backend/tests/test_db_models.py:328:            for fk in inspector.get_foreign_keys("pitches")
    backend/tests/test_db_models.py:336:        assert pitch_foreign_keys[("session_id",)] == "story_sessions"
    backend/tests/test_db_models.py:337:        assert pitch_foreign_keys[("story_brief_id",)] == "story_briefs"
    backend/tests/test_db_models.py:339:        assert asset_foreign_keys[("audio_job_id",)] == "audio_jobs"
    backend/tests/conftest.py:20:    "STORYTELLER_GCS_AUDIO_BUCKET_NAME": "storyteller-audio",
    backend/app/models/intent_parser.py:18:INTENT_PARSER_SCHEMA_VERSION = 1
    backend/app/models/intent_parser.py:19:INTENT_PARSER_PROMPT_VERSION = "intent_parser.v1"
    backend/app/models/intent_parser.py:24:class IntentParserStatus(str, Enum):
    backend/app/models/intent_parser.py:33:    REGENERATE_PITCHES = "regenerate_pitches"
    backend/app/models/intent_parser.py:70:        if self.command_id == ExplicitChatCommandId.REGENERATE_PITCHES:
    backend/app/models/intent_parser.py:71:            if action.action_type != ChatToUIActionType.REGENERATE_PITCHES:
    backend/app/models/intent_parser.py:73:                    "regenerate_pitches must propose a regenerate_pitches action",
    backend/app/models/intent_parser.py:100:class ParseChatIntentRequest(BaseModel):
    backend/app/models/intent_parser.py:113:class IntentParserStageContext(BaseModel):
    backend/app/models/intent_parser.py:121:class IntentParserPromptContext(BaseModel):
    backend/app/models/intent_parser.py:126:    stage_context: IntentParserStageContext
    backend/app/models/intent_parser.py:139:class IntentParserCandidateAction(BaseModel):
    backend/app/models/intent_parser.py:150:class IntentParserCandidateActionBatch(BaseModel):
    backend/app/models/intent_parser.py:154:    actions: list[IntentParserCandidateAction] = Field(default_factory=list)
    backend/app/models/intent_parser.py:157:class IntentParserStructuredOutput(BaseModel):
    backend/app/models/intent_parser.py:160:    schema_version: int = Field(default=INTENT_PARSER_SCHEMA_VERSION, ge=1)
    backend/app/models/intent_parser.py:161:    status: IntentParserStatus = IntentParserStatus.PARSED
    backend/app/models/intent_parser.py:165:    proposed_actions: IntentParserCandidateActionBatch = Field(
    backend/app/models/intent_parser.py:166:        default_factory=IntentParserCandidateActionBatch
    backend/app/models/intent_parser.py:170:    def validate_status_requirements(self) -> IntentParserStructuredOutput:
    backend/app/models/intent_parser.py:171:        if self.needs_clarification and self.status == IntentParserStatus.PARSED:
    backend/app/models/intent_parser.py:172:            self.status = IntentParserStatus.NEEDS_CLARIFICATION
    backend/app/models/intent_parser.py:174:        if self.status == IntentParserStatus.NEEDS_CLARIFICATION:
    backend/app/models/intent_parser.py:185:        if self.status == IntentParserStatus.FAILED:
    backend/app/models/intent_parser.py:193:class ParsedChatIntentResponse(BaseModel):
    backend/app/models/intent_parser.py:196:    schema_version: int = Field(default=INTENT_PARSER_SCHEMA_VERSION, ge=1)
    backend/app/models/intent_parser.py:197:    status: IntentParserStatus = IntentParserStatus.PARSED
    backend/app/models/intent_parser.py:205:    def validate_status_requirements(self) -> ParsedChatIntentResponse:
    backend/app/models/intent_parser.py:206:        if self.needs_clarification and self.status == IntentParserStatus.PARSED:
    backend/app/models/intent_parser.py:207:            self.status = IntentParserStatus.NEEDS_CLARIFICATION
    backend/app/models/intent_parser.py:209:        if self.status == IntentParserStatus.NEEDS_CLARIFICATION:
    backend/app/models/intent_parser.py:220:        if self.status == IntentParserStatus.FAILED:
    backend/app/models/intent_parser.py:228:class IntentParserInvocation(BaseModel):
    backend/app/models/intent_parser.py:231:    prompt_version: str = INTENT_PARSER_PROMPT_VERSION
    backend/app/models/intent_parser.py:233:    context: IntentParserPromptContext
    backend/app/models/intent_parser.py:237:class IntentParserInvocationResult(BaseModel):
    backend/app/models/intent_parser.py:240:    invocation: IntentParserInvocation
    backend/app/models/intent_parser.py:241:    structured_output: IntentParserStructuredOutput
    backend/app/api/dependencies.py:8:from app.ai import GeminiIntentParserAdapter, IntentParserAdapter
    backend/app/api/dependencies.py:29:def get_intent_parser_adapter(request: Request) -> IntentParserAdapter:
    backend/app/api/dependencies.py:30:    adapter = getattr(request.app.state, "intent_parser_adapter", None)
    backend/app/api/dependencies.py:33:        adapter = GeminiIntentParserAdapter(
    backend/app/api/dependencies.py:37:        request.app.state.intent_parser_adapter = adapter
    backend/tests/test_session_api.py:135:            "stage": "audio",
    backend/tests/test_session_api.py:137:            "value_summary": "Audio",
    backend/tests/test_session_api.py:146:    assert payload["stage"] == "audio"
    backend/tests/test_session_api.py:149:    assert payload["payload"]["value_summary"] == "Audio"
    backend/tests/test_session_api.py:164:            WorkflowStage.PITCHES,
    backend/tests/test_session_api.py:203:        "Latest saved UI detail: Beat sheet: Add one calmer beat"
    backend/tests/test_session_api.py:226:            "stage": "audio",
    backend/tests/test_session_service.py:9:    AudioJob,
    backend/tests/test_session_service.py:19:    Pitch,
    backend/tests/test_session_service.py:141:        stage=WorkflowStage.PITCHES,
    backend/tests/test_session_service.py:178:    pitch = Pitch(
    backend/tests/test_session_service.py:181:        generation_key="pitch-batch-1",
    backend/tests/test_session_service.py:182:        pitch_index=0,
    backend/tests/test_session_service.py:190:    db_session.add(pitch)
    backend/tests/test_session_service.py:195:        pitch_id=pitch.id,
    backend/tests/test_session_service.py:249:    audio_job = AudioJob(
    backend/tests/test_session_service.py:259:    db_session.add(audio_job)
    backend/tests/test_session_service.py:272:    audio_asset = SessionAsset(
    backend/tests/test_session_service.py:274:        audio_job_id=audio_job.id,
    backend/tests/test_session_service.py:275:        asset_kind=AssetKind.FINAL_AUDIO,
    backend/tests/test_session_service.py:279:        mime_type="audio/mpeg",
    backend/tests/test_session_service.py:283:    db_session.add_all([story_asset, audio_asset])
    backend/tests/test_session_service.py:293:    assert snapshot.selected_pitch is not None
    backend/tests/test_session_service.py:294:    assert snapshot.selected_pitch.title == "The Reed of Quiet Light"
    backend/tests/test_session_service.py:299:    assert snapshot.active_audio_job is not None
    backend/tests/test_session_service.py:301:    assert snapshot.latest_audio_asset is not None
    backend/tests/test_session_service.py:303:    assert snapshot.latest_audio_asset.object_path == "sessions/story-1/story.mp3"
    backend/tests/test_session_service.py:370:        stage=WorkflowStage.AUDIO,
    backend/tests/test_session_service.py:372:        value_summary="Audio",
    backend/tests/test_session_service.py:377:    assert event.stage == WorkflowStage.AUDIO
    backend/tests/test_session_service.py:381:    assert event.payload.value_summary == "Audio"
    backend/tests/test_session_service.py:397:        WorkflowStage.PITCHES,
    backend/tests/test_session_service.py:402:        WorkflowStage.AUDIO,
    backend/tests/test_session_service.py:437:    assert result.event.payload.summary_text == "Updated beat sheet notes from the workspace."
    backend/tests/test_session_service.py:443:    assert stage_map[WorkflowStage.AUDIO].status == WorkflowStageState.NEEDS_REGENERATION
    backend/tests/test_session_service.py:448:    assert "Latest saved UI detail: Beat sheet: Soften the midpoint" in (
    backend/tests/test_session_service.py:451:    assert "Needs regeneration: Composition, Audio" in updated_snapshot.agent_context_summary
    backend/tests/test_session_service.py:467:        WorkflowStage.PITCHES,
    backend/tests/test_session_service.py:472:        WorkflowStage.AUDIO,
    backend/tests/test_session_service.py:493:    assert snapshot.current_stage == WorkflowStage.PITCHES
    backend/tests/test_session_service.py:494:    assert snapshot.resume_stage == WorkflowStage.PITCHES
    backend/tests/test_session_service.py:499:    assert stage_map[WorkflowStage.PITCHES].status == WorkflowStageState.NEEDS_REGENERATION
    backend/tests/test_session_service.py:503:    assert stage_map[WorkflowStage.PITCHES].detail == "Accepted a revised brief."
    backend/tests/test_session_service.py:504:    assert stage_map[WorkflowStage.PITCHES].last_event_type == "workflow.stage_changed"
    backend/tests/test_session_service.py:505:    assert "invalidated pitches" in stage_map[WorkflowStage.BRIEF].last_event_summary
    backend/tests/test_session_service.py:506:    assert "invalidated pitches" in stage_map[WorkflowStage.PITCHES].last_event_summary
    backend/app/models/chat_actions.py:18:    REGENERATE_PITCHES = "regenerate_pitches"
    backend/app/models/chat_actions.py:19:    SELECT_PITCH = "select_pitch"
    backend/app/models/chat_actions.py:31:    UPDATE_AUDIO_SETTINGS = "update_audio_settings"
    backend/app/models/chat_actions.py:32:    START_AUDIO_GENERATION = "start_audio_generation"
    backend/app/models/chat_actions.py:44:    AUDIO = "audio"
    backend/app/models/chat_actions.py:56:    REWRITE = "rewrite"
    backend/app/models/chat_actions.py:66:    FINAL_AUDIO = "final_audio"
    backend/app/models/chat_actions.py:74:    ChatToUIActionType.REGENERATE_PITCHES: ChatToUIActionDefaultPolicy.CONFIRM_FIRST,
    backend/app/models/chat_actions.py:75:    ChatToUIActionType.SELECT_PITCH: ChatToUIActionDefaultPolicy.CONFIRM_FIRST,
    backend/app/models/chat_actions.py:87:    ChatToUIActionType.UPDATE_AUDIO_SETTINGS: ChatToUIActionDefaultPolicy.AUTO_APPLY_CANDIDATE,
    backend/app/models/chat_actions.py:88:    ChatToUIActionType.START_AUDIO_GENERATION: ChatToUIActionDefaultPolicy.CONFIRM_FIRST,
    backend/app/models/chat_actions.py:181:class RegeneratePitchesValues(ChatToUIExtractedValues):
    backend/app/models/chat_actions.py:184:    preserve_selected_pitch: bool = False
    backend/app/models/chat_actions.py:187:class SelectPitchValues(ChatToUIExtractedValues):
    backend/app/models/chat_actions.py:188:    pitch_id: str | None = Field(default=None, min_length=1)
    backend/app/models/chat_actions.py:190:    pitch_index: int | None = Field(default=None, ge=1)
    backend/app/models/chat_actions.py:194:    def validate_identifier(self) -> SelectPitchValues:
    backend/app/models/chat_actions.py:196:            self.pitch_id,
    backend/app/models/chat_actions.py:198:            self.pitch_index,
    backend/app/models/chat_actions.py:201:                "select_pitch requires a pitch_id, generation_key, pitch_index, or title"
    backend/app/models/chat_actions.py:298:    rewrite_from_segment_index: int | None = Field(default=None, ge=1)
    backend/app/models/chat_actions.py:302:class UpdateAudioSettingsValues(ChatToUIExtractedValues):
    backend/app/models/chat_actions.py:310:    def validate_audio_settings(self) -> UpdateAudioSettingsValues:
    backend/app/models/chat_actions.py:320:                "update_audio_settings requires at least one audio setting or guidance note"
    backend/app/models/chat_actions.py:326:class StartAudioGenerationValues(ChatToUIExtractedValues):
    backend/app/models/chat_actions.py:331:    regenerate_existing_audio: bool = False
    backend/app/models/chat_actions.py:391:class RegeneratePitchesAction(ChatToUIActionBase):
    backend/app/models/chat_actions.py:392:    action_type: Literal[ChatToUIActionType.REGENERATE_PITCHES] = (
    backend/app/models/chat_actions.py:393:        ChatToUIActionType.REGENERATE_PITCHES
    backend/app/models/chat_actions.py:395:    target_stage: Literal[WorkflowStage.PITCHES] = WorkflowStage.PITCHES
    backend/app/models/chat_actions.py:396:    extracted_values: RegeneratePitchesValues = Field(default_factory=RegeneratePitchesValues)
    backend/app/models/chat_actions.py:399:class SelectPitchAction(ChatToUIActionBase):
    backend/app/models/chat_actions.py:400:    action_type: Literal[ChatToUIActionType.SELECT_PITCH] = ChatToUIActionType.SELECT_PITCH
    backend/app/models/chat_actions.py:401:    target_stage: Literal[WorkflowStage.PITCHES] = WorkflowStage.PITCHES
    backend/app/models/chat_actions.py:402:    extracted_values: SelectPitchValues
    backend/app/models/chat_actions.py:473:    target_stage: Literal[WorkflowStage.COMPOSITION, WorkflowStage.AUDIO]
    backend/app/models/chat_actions.py:481:            else WorkflowStage.AUDIO
    backend/app/models/chat_actions.py:491:    target_stage: Literal[WorkflowStage.COMPOSITION, WorkflowStage.AUDIO]
    backend/app/models/chat_actions.py:499:            else WorkflowStage.AUDIO
    backend/app/models/chat_actions.py:515:class UpdateAudioSettingsAction(ChatToUIActionBase):
    backend/app/models/chat_actions.py:516:    action_type: Literal[ChatToUIActionType.UPDATE_AUDIO_SETTINGS] = (
    backend/app/models/chat_actions.py:517:        ChatToUIActionType.UPDATE_AUDIO_SETTINGS
    backend/app/models/chat_actions.py:519:    target_stage: Literal[WorkflowStage.AUDIO] = WorkflowStage.AUDIO
    backend/app/models/chat_actions.py:520:    extracted_values: UpdateAudioSettingsValues
    backend/app/models/chat_actions.py:523:class StartAudioGenerationAction(ChatToUIActionBase):
    backend/app/models/chat_actions.py:524:    action_type: Literal[ChatToUIActionType.START_AUDIO_GENERATION] = (
    backend/app/models/chat_actions.py:525:        ChatToUIActionType.START_AUDIO_GENERATION
    backend/app/models/chat_actions.py:527:    target_stage: Literal[WorkflowStage.AUDIO] = WorkflowStage.AUDIO
    backend/app/models/chat_actions.py:528:    extracted_values: StartAudioGenerationValues = Field(default_factory=StartAudioGenerationValues)
    backend/app/models/chat_actions.py:550:    | RegeneratePitchesAction
    backend/app/models/chat_actions.py:551:    | SelectPitchAction
    backend/app/models/chat_actions.py:563:    | UpdateAudioSettingsAction
    backend/app/models/chat_actions.py:564:    | StartAudioGenerationAction
    backend/tests/integration/conftest.py:25:DEFAULT_GCS_AUDIO_BUCKET_NAME = "storyteller-audio"
    backend/tests/integration/conftest.py:211:            "STORYTELLER_GCS_AUDIO_BUCKET_NAME": os.environ.get(
    backend/tests/integration/conftest.py:212:                "STORYTELLER_INTEGRATION_GCS_AUDIO_BUCKET_NAME",
    backend/tests/integration/conftest.py:213:                DEFAULT_GCS_AUDIO_BUCKET_NAME,
    backend/app/main.py:45:        intent_parser_adapter = getattr(app.state, "intent_parser_adapter", None)
    backend/app/main.py:46:        if intent_parser_adapter is not None:
    backend/app/main.py:47:            intent_parser_adapter.close()
    backend/tests/integration/test_data_layer.py:37:    "audio_jobs",
    backend/tests/integration/test_data_layer.py:45:    "pitches",
    backend/app/models/__init__.py:52:    RegeneratePitchesAction,
    backend/app/models/__init__.py:53:    RegeneratePitchesValues,
    backend/app/models/__init__.py:59:    SelectPitchAction,
    backend/app/models/__init__.py:60:    SelectPitchValues,
    backend/app/models/__init__.py:63:    StartAudioGenerationAction,
    backend/app/models/__init__.py:64:    StartAudioGenerationValues,
    backend/app/models/__init__.py:68:    UpdateAudioSettingsAction,
    backend/app/models/__init__.py:69:    UpdateAudioSettingsValues,
    backend/app/models/__init__.py:80:    AudioProgressEventPayload,
    backend/app/models/__init__.py:81:    ChatIntentParsedEventPayload,
    backend/app/models/__init__.py:101:from app.models.intent_parser import (
    backend/app/models/__init__.py:104:    INTENT_PARSER_PROMPT_VERSION,
    backend/app/models/__init__.py:105:    INTENT_PARSER_SCHEMA_VERSION,
    backend/app/models/__init__.py:109:    IntentParserCandidateAction,
    backend/app/models/__init__.py:110:    IntentParserCandidateActionBatch,
    backend/app/models/__init__.py:111:    IntentParserInvocation,
    backend/app/models/__init__.py:112:    IntentParserInvocationResult,
    backend/app/models/__init__.py:113:    IntentParserPromptContext,
    backend/app/models/__init__.py:114:    IntentParserStageContext,
    backend/app/models/__init__.py:115:    IntentParserStatus,
    backend/app/models/__init__.py:116:    IntentParserStructuredOutput,
    backend/app/models/__init__.py:117:    ParseChatIntentRequest,
    backend/app/models/__init__.py:118:    ParsedChatIntentResponse,
    backend/app/models/__init__.py:150:    AudioJobView,
    backend/app/models/__init__.py:159:    PitchView,
    backend/app/models/__init__.py:191:    "AudioJobView",
    backend/app/models/__init__.py:192:    "AudioProgressEventPayload",
    backend/app/models/__init__.py:196:    "ChatIntentParsedEventPayload",
    backend/app/models/__init__.py:242:    "INTENT_PARSER_PROMPT_VERSION",
    backend/app/models/__init__.py:243:    "INTENT_PARSER_SCHEMA_VERSION",
    backend/app/models/__init__.py:244:    "IntentParserCandidateAction",
    backend/app/models/__init__.py:245:    "IntentParserCandidateActionBatch",
    backend/app/models/__init__.py:246:    "IntentParserInvocation",
    backend/app/models/__init__.py:247:    "IntentParserInvocationResult",
    backend/app/models/__init__.py:248:    "IntentParserPromptContext",
    backend/app/models/__init__.py:249:    "IntentParserStageContext",
    backend/app/models/__init__.py:250:    "IntentParserStatus",
    backend/app/models/__init__.py:251:    "IntentParserStructuredOutput",
    backend/app/models/__init__.py:262:    "ParseChatIntentRequest",
    backend/app/models/__init__.py:263:    "PitchView",
    backend/app/models/__init__.py:264:    "ParsedChatIntentResponse",
    backend/app/models/__init__.py:280:    "RegeneratePitchesAction",
    backend/app/models/__init__.py:281:    "RegeneratePitchesValues",
    backend/app/models/__init__.py:288:    "SelectPitchAction",
    backend/app/models/__init__.py:289:    "SelectPitchValues",
    backend/app/models/__init__.py:320:    "StartAudioGenerationAction",
    backend/app/models/__init__.py:321:    "StartAudioGenerationValues",
    backend/app/models/__init__.py:329:    "UpdateAudioSettingsAction",
    backend/app/models/__init__.py:330:    "UpdateAudioSettingsValues",
    backend/app/models/events.py:10:from app.models.intent_parser import ParsedChatIntentResponse
    backend/app/models/events.py:21:    CHAT_INTENT_PARSED = "chat.intent.parsed"
    backend/app/models/events.py:24:    AUDIO_PROGRESS_RECORDED = "audio.progress.recorded"
    backend/app/models/events.py:30:    PITCH = "pitch"
    backend/app/models/events.py:37:    PITCH_BATCH = "pitch_batch"
    backend/app/models/events.py:42:    AUDIO_SEGMENT = "audio_segment"
    backend/app/models/events.py:47:    PITCH = "pitch"
    backend/app/models/events.py:52:    AUDIO_SETTINGS = "audio_settings"
    backend/app/models/events.py:134:class ChatIntentParsedEventPayload(EventPayload):
    backend/app/models/events.py:145:    result: ParsedChatIntentResponse
    backend/app/models/events.py:165:class AudioProgressEventPayload(EventPayload):
    backend/app/models/events.py:183:    | ChatIntentParsedEventPayload
    backend/app/models/events.py:186:    | AudioProgressEventPayload
    backend/app/models/events.py:196:    SessionEventType.CHAT_INTENT_PARSED.value: ChatIntentParsedEventPayload,
    backend/app/models/events.py:199:    SessionEventType.AUDIO_PROGRESS_RECORDED.value: AudioProgressEventPayload,
    backend/app/models/session.py:47:class PitchView(BaseModel):
    backend/app/models/session.py:50:    pitch_index: int
    backend/app/models/session.py:105:class AudioJobView(BaseModel):
    backend/app/models/session.py:228:    selected_pitch: PitchView | None = None
    backend/app/models/session.py:233:    active_audio_job: AudioJobView | None = None
    backend/app/models/session.py:235:    latest_audio_asset: SessionAssetView | None = None
    backend/migrations/versions/20260331_01_initial_storyteller_schema.py:24:    "pitches",
    backend/migrations/versions/20260331_01_initial_storyteller_schema.py:29:    "audio",
    backend/migrations/versions/20260331_01_initial_storyteller_schema.py:46:COMPOSITION_JOB_KIND_VALUES = ("draft", "rewrite")
    backend/migrations/versions/20260331_01_initial_storyteller_schema.py:47:ASSET_KIND_VALUES = ("story_text", "story_docx", "audio_segment", "final_audio")
    backend/migrations/versions/20260331_01_initial_storyteller_schema.py:323:        "pitches",
    backend/migrations/versions/20260331_01_initial_storyteller_schema.py:328:        sa.Column("pitch_index", sa.Integer(), nullable=False),
    backend/migrations/versions/20260331_01_initial_storyteller_schema.py:341:            name="fk_pitches_session_id_story_sessions",
    backend/migrations/versions/20260331_01_initial_storyteller_schema.py:347:            name="fk_pitches_story_brief_id_story_briefs",
    backend/migrations/versions/20260331_01_initial_storyteller_schema.py:350:        sa.PrimaryKeyConstraint("id", name="pk_pitches"),
    backend/migrations/versions/20260331_01_initial_storyteller_schema.py:354:            "pitch_index",
    backend/migrations/versions/20260331_01_initial_storyteller_schema.py:355:            name="uq_pitches_session_id_generation_key_pitch_index",
    backend/migrations/versions/20260331_01_initial_storyteller_schema.py:359:        "ix_pitches_session_id_is_selected",
    backend/migrations/versions/20260331_01_initial_storyteller_schema.py:360:        "pitches",
    backend/migrations/versions/20260331_01_initial_storyteller_schema.py:369:        sa.Column("pitch_id", sa.String(length=36), nullable=True),
    backend/migrations/versions/20260331_01_initial_storyteller_schema.py:382:            ["pitch_id"],
    backend/migrations/versions/20260331_01_initial_storyteller_schema.py:383:            ["pitches.id"],
    backend/migrations/versions/20260331_01_initial_storyteller_schema.py:384:            name="fk_character_sheets_pitch_id_pitches",
    backend/migrations/versions/20260331_01_initial_storyteller_schema.py:599:        "audio_jobs",
    backend/migrations/versions/20260331_01_initial_storyteller_schema.py:631:            name="fk_audio_jobs_session_id_story_sessions",
    backend/migrations/versions/20260331_01_initial_storyteller_schema.py:637:            name="fk_audio_jobs_source_composition_job_id_composition_jobs",
    backend/migrations/versions/20260331_01_initial_storyteller_schema.py:640:        sa.PrimaryKeyConstraint("id", name="pk_audio_jobs"),
    backend/migrations/versions/20260331_01_initial_storyteller_schema.py:643:        "ix_audio_jobs_session_id_status_created_at",
    backend/migrations/versions/20260331_01_initial_storyteller_schema.py:644:        "audio_jobs",
    backend/migrations/versions/20260331_01_initial_storyteller_schema.py:654:        sa.Column("audio_job_id", sa.String(length=36), nullable=True),
    backend/migrations/versions/20260331_01_initial_storyteller_schema.py:668:            ["audio_job_id"],
    backend/migrations/versions/20260331_01_initial_storyteller_schema.py:669:            ["audio_jobs.id"],
    backend/migrations/versions/20260331_01_initial_storyteller_schema.py:670:            name="fk_export_assets_audio_job_id_audio_jobs",
    backend/migrations/versions/20260331_01_initial_storyteller_schema.py:704:    op.drop_index("ix_audio_jobs_session_id_status_created_at", table_name="audio_jobs")
    backend/migrations/versions/20260331_01_initial_storyteller_schema.py:705:    op.drop_table("audio_jobs")
    backend/migrations/versions/20260331_01_initial_storyteller_schema.py:729:    op.drop_index("ix_pitches_session_id_is_selected", table_name="pitches")
    backend/migrations/versions/20260331_01_initial_storyteller_schema.py:730:    op.drop_table("pitches")
    backend/app/models/realtime.py:62:    AUDIO = "audio"
    backend/app/db/models.py:54:    REWRITE = "rewrite"
    backend/app/db/models.py:62:    AUDIO_SEGMENT = "audio_segment"
    backend/app/db/models.py:63:    FINAL_AUDIO = "final_audio"
    backend/app/db/models.py:173:    pitches: Mapped[list["Pitch"]] = relationship(
    backend/app/db/models.py:201:    audio_jobs: Mapped[list["AudioJob"]] = relationship(
    backend/app/db/models.py:397:    pitches: Mapped[list["Pitch"]] = relationship(back_populates="story_brief")
    backend/app/db/models.py:407:class Pitch(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    backend/app/db/models.py:408:    __tablename__ = "pitches"
    backend/app/db/models.py:420:    pitch_index: Mapped[int] = mapped_column(Integer, nullable=False)
    backend/app/db/models.py:429:    session: Mapped["StorySession"] = relationship(back_populates="pitches")
    backend/app/db/models.py:430:    story_brief: Mapped["StoryBrief | None"] = relationship(back_populates="pitches")
    backend/app/db/models.py:431:    character_sheets: Mapped[list["CharacterSheet"]] = relationship(back_populates="pitch")
    backend/app/db/models.py:437:            "pitch_index",
    backend/app/db/models.py:438:            name="uq_pitches_session_id_generation_key_pitch_index",
    backend/app/db/models.py:440:        Index("ix_pitches_session_id_is_selected", "session_id", "is_selected"),
    backend/app/db/models.py:452:    pitch_id: Mapped[str | None] = mapped_column(
    backend/app/db/models.py:454:        ForeignKey("pitches.id", ondelete="SET NULL"),
    backend/app/db/models.py:467:    pitch: Mapped["Pitch | None"] = relationship(back_populates="character_sheets")
    backend/app/db/models.py:654:class AudioJob(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    backend/app/db/models.py:655:    __tablename__ = "audio_jobs"
    backend/app/db/models.py:688:    session: Mapped["StorySession"] = relationship(back_populates="audio_jobs")
    backend/app/db/models.py:690:    assets: Mapped[list["SessionAsset"]] = relationship(back_populates="audio_job")
    backend/app/db/models.py:693:        Index("ix_audio_jobs_session_id_status_created_at", "session_id", "status", "created_at"),
    backend/app/db/models.py:713:    audio_job_id: Mapped[str | None] = mapped_column(
    backend/app/db/models.py:715:        ForeignKey("audio_jobs.id", ondelete="SET NULL"),
    backend/app/db/models.py:738:    audio_job: Mapped["AudioJob | None"] = relationship(back_populates="assets")
    backend/app/db/models.py:748:            "ix_session_assets_audio_job_id_asset_kind_segment_index",
    backend/app/db/models.py:749:            "audio_job_id",
    backend/app/settings/config.py:25:    "gcs.buckets.audio": "STORYTELLER_GCS_AUDIO_BUCKET_NAME or gcs.buckets.audio",
    backend/app/settings/config.py:227:            "enable_audio_generation": False,
    backend/app/settings/config.py:274:                "audio": _read_string(
    backend/app/settings/config.py:275:                    environ.get("STORYTELLER_GCS_AUDIO_BUCKET_NAME"),
    backend/app/settings/config.py:289:            "enable_audio_generation": _read_env_bool(
    backend/app/settings/config.py:291:                "STORYTELLER_FEATURE_ENABLE_AUDIO_GENERATION",
    backend/app/settings/config.py:385:    audio: str
    backend/app/settings/config.py:388:    @field_validator("sessions", "audio", "exports")
    backend/app/settings/config.py:433:    enable_audio_generation: bool = False
    backend/app/db/__init__.py:12:    AudioJob,
    backend/app/db/__init__.py:24:    Pitch,
    backend/app/db/__init__.py:46:    "AudioJob",
    backend/app/db/__init__.py:58:    "Pitch",
    backend/app/storage/status.py:12:            settings.gcs_bucket_names.audio,
    backend/app/api/v1/routes/sessions.py:8:from app.ai import IntentParserAdapter
    backend/app/api/v1/routes/sessions.py:9:from app.api.dependencies import get_db_session, get_intent_parser_adapter
    backend/app/api/v1/routes/sessions.py:12:    ParseChatIntentRequest,
    backend/app/api/v1/routes/sessions.py:13:    ParsedChatIntentResponse,
    backend/app/api/v1/routes/sessions.py:24:from app.services import SessionActionPolicyService, SessionIntentParserService
    backend/app/api/v1/routes/sessions.py:159:    "/{session_id}/chat/intents",
    backend/app/api/v1/routes/sessions.py:160:    response_model=ParsedChatIntentResponse,
    backend/app/api/v1/routes/sessions.py:163:def parse_chat_intents(
    backend/app/api/v1/routes/sessions.py:165:    payload: ParseChatIntentRequest,
    backend/app/api/v1/routes/sessions.py:168:) -> ParsedChatIntentResponse:
    backend/app/api/v1/routes/sessions.py:169:    intent_parser: IntentParserAdapter | None = None
    backend/app/api/v1/routes/sessions.py:171:        intent_parser = get_intent_parser_adapter(request)
    backend/app/api/v1/routes/sessions.py:174:        return SessionIntentParserService(db_session, intent_parser).parse_user_message(
    backend/app/ai/prompts/intent_parser.md:1:You are Storyteller's backend-only chat intent parser.
    backend/migrations/versions/20260331_03_generalize_export_assets_to_session_assets.py:25:    "audio_segment",
    backend/migrations/versions/20260331_03_generalize_export_assets_to_session_assets.py:26:    "final_audio",
    backend/migrations/versions/20260331_03_generalize_export_assets_to_session_assets.py:35:LEGACY_ASSET_KIND_VALUES = ("story_text", "story_docx", "audio_segment", "final_audio")
    backend/migrations/versions/20260331_03_generalize_export_assets_to_session_assets.py:63:        sa.Column("audio_job_id", sa.String(length=36), nullable=True),
    backend/migrations/versions/20260331_03_generalize_export_assets_to_session_assets.py:85:            ["audio_job_id"],
    backend/migrations/versions/20260331_03_generalize_export_assets_to_session_assets.py:86:            ["audio_jobs.id"],
    backend/migrations/versions/20260331_03_generalize_export_assets_to_session_assets.py:87:            name="fk_session_assets_audio_job_id_audio_jobs",
    backend/migrations/versions/20260331_03_generalize_export_assets_to_session_assets.py:122:        "ix_session_assets_audio_job_id_asset_kind_segment_index",
    backend/migrations/versions/20260331_03_generalize_export_assets_to_session_assets.py:124:        ["audio_job_id", "asset_kind", "segment_index"],
    backend/migrations/versions/20260331_03_generalize_export_assets_to_session_assets.py:140:            audio_job_id,
    backend/migrations/versions/20260331_03_generalize_export_assets_to_session_assets.py:158:            audio_job_id,
    backend/migrations/versions/20260331_03_generalize_export_assets_to_session_assets.py:184:        sa.Column("audio_job_id", sa.String(length=36), nullable=True),
    backend/migrations/versions/20260331_03_generalize_export_assets_to_session_assets.py:203:            ["audio_job_id"],
    backend/migrations/versions/20260331_03_generalize_export_assets_to_session_assets.py:204:            ["audio_jobs.id"],
    backend/migrations/versions/20260331_03_generalize_export_assets_to_session_assets.py:205:            name="fk_export_assets_audio_job_id_audio_jobs",
    backend/migrations/versions/20260331_03_generalize_export_assets_to_session_assets.py:240:            audio_job_id,
    backend/migrations/versions/20260331_03_generalize_export_assets_to_session_assets.py:258:            audio_job_id,
    backend/migrations/versions/20260331_03_generalize_export_assets_to_session_assets.py:287:        "ix_session_assets_audio_job_id_asset_kind_segment_index",
    backend/app/ai/__init__.py:1:from app.ai.intent_parser import (
    backend/app/ai/__init__.py:3:    GeminiIntentParserAdapter,
    backend/app/ai/__init__.py:4:    IntentParserAdapter,
    backend/app/ai/__init__.py:5:    IntentParserError,
    backend/app/ai/__init__.py:6:    IntentParserTransportError,
    backend/app/ai/__init__.py:7:    build_intent_parser_invocation,
    backend/app/ai/__init__.py:8:    get_intent_parser_response_schema,
    backend/app/ai/__init__.py:9:    render_intent_parser_prompt,
    backend/app/ai/__init__.py:14:    "GeminiIntentParserAdapter",
    backend/app/ai/__init__.py:15:    "IntentParserAdapter",
    backend/app/ai/__init__.py:16:    "IntentParserError",
    backend/app/ai/__init__.py:17:    "IntentParserTransportError",
    backend/app/ai/__init__.py:18:    "build_intent_parser_invocation",
    backend/app/ai/__init__.py:19:    "get_intent_parser_response_schema",
    backend/app/ai/__init__.py:20:    "render_intent_parser_prompt",
    backend/app/storage/paths.py:39:    audio_bucket: str
    backend/app/storage/paths.py:47:            audio_bucket=bucket_names.audio,
    backend/app/storage/paths.py:54:            self.audio_bucket,
    backend/app/storage/paths.py:75:    def audio_segment(
    backend/app/storage/paths.py:84:            bucket=self.audio_bucket,
    backend/app/storage/paths.py:86:                f"{self._session_prefix(session_id)}/audio/jobs/"
    backend/app/storage/paths.py:92:    def final_audio(
    backend/app/storage/paths.py:101:            bucket=self.audio_bucket,
    backend/app/storage/paths.py:103:                f"{self._session_prefix(session_id)}/audio/jobs/"
    backend/app/ai/intent_parser.py:12:from app.models.intent_parser import (
    backend/app/ai/intent_parser.py:13:    INTENT_PARSER_PROMPT_VERSION,
    backend/app/ai/intent_parser.py:14:    IntentParserInvocation,
    backend/app/ai/intent_parser.py:15:    IntentParserInvocationResult,
    backend/app/ai/intent_parser.py:16:    IntentParserPromptContext,
    backend/app/ai/intent_parser.py:17:    IntentParserStructuredOutput,
    backend/app/ai/intent_parser.py:79:        "action_type": "regenerate_pitches",
    backend/app/ai/intent_parser.py:80:        "stage": "pitches",
    backend/app/ai/intent_parser.py:81:        "description": "Ask for a new batch of pitches.",
    backend/app/ai/intent_parser.py:82:        "common_fields": ["candidate_count", "guidance", "preserve_selected_pitch"],
    backend/app/ai/intent_parser.py:85:        "action_type": "select_pitch",
    backend/app/ai/intent_parser.py:86:        "stage": "pitches",
    backend/app/ai/intent_parser.py:87:        "description": "Select a pitch by id, generation key, index, or title.",
    backend/app/ai/intent_parser.py:88:        "common_fields": ["pitch_id", "generation_key", "pitch_index", "title"],
    backend/app/ai/intent_parser.py:93:        "description": "Choose a character sheet revision.",
    backend/app/ai/intent_parser.py:109:        "description": "Regenerate the character sheet with optional guidance.",
    backend/app/ai/intent_parser.py:115:        "description": "Accept a beat sheet revision.",
    backend/app/ai/intent_parser.py:127:        "description": "Regenerate the beat sheet with guidance.",
    backend/app/ai/intent_parser.py:147:        "description": "Start writing, continue, or rewrite composition.",
    backend/app/ai/intent_parser.py:152:        "stage": "composition|audio",
    backend/app/ai/intent_parser.py:153:        "description": "Pause a composition or audio job.",
    backend/app/ai/intent_parser.py:158:        "stage": "composition|audio",
    backend/app/ai/intent_parser.py:159:        "description": "Resume a composition or audio job.",
    backend/app/ai/intent_parser.py:165:        "description": "Redirect writing with concrete rewrite instructions.",
    backend/app/ai/intent_parser.py:168:            "rewrite_from_segment_index",
    backend/app/ai/intent_parser.py:173:        "action_type": "update_audio_settings",
    backend/app/ai/intent_parser.py:174:        "stage": "audio",
    backend/app/ai/intent_parser.py:185:        "action_type": "start_audio_generation",
    backend/app/ai/intent_parser.py:186:        "stage": "audio",
    backend/app/ai/intent_parser.py:187:        "description": "Start or regenerate audio generation.",
    backend/app/ai/intent_parser.py:193:            "regenerate_existing_audio",
    backend/app/ai/intent_parser.py:205:        "description": "Download the story docx or final audio asset.",
    backend/app/ai/intent_parser.py:211:class IntentParserError(RuntimeError):
    backend/app/ai/intent_parser.py:212:    """Base error for intent parser adapter failures."""
    backend/app/ai/intent_parser.py:215:class IntentParserTransportError(IntentParserError):
    backend/app/ai/intent_parser.py:219:class IntentParserAdapter(Protocol):
    backend/app/ai/intent_parser.py:223:    def parse(self, invocation: IntentParserInvocation) -> IntentParserInvocationResult: ...
    backend/app/ai/intent_parser.py:228:class GeminiIntentParserAdapter:
    backend/app/ai/intent_parser.py:247:    def parse(self, invocation: IntentParserInvocation) -> IntentParserInvocationResult:
    backend/app/ai/intent_parser.py:269:                    "responseJsonSchema": get_intent_parser_response_schema(),
    backend/app/ai/intent_parser.py:277:            raise IntentParserTransportError(
    backend/app/ai/intent_parser.py:278:                f"Gemini intent parser request failed with status {exc.response.status_code}",
    backend/app/ai/intent_parser.py:283:        return IntentParserInvocationResult(
    backend/app/ai/intent_parser.py:294:def render_intent_parser_prompt(context: IntentParserPromptContext) -> str:
    backend/app/ai/intent_parser.py:313:def build_intent_parser_invocation(
    backend/app/ai/intent_parser.py:314:    context: IntentParserPromptContext,
    backend/app/ai/intent_parser.py:317:) -> IntentParserInvocation:
    backend/app/ai/intent_parser.py:318:    return IntentParserInvocation(
    backend/app/ai/intent_parser.py:319:        prompt_version=INTENT_PARSER_PROMPT_VERSION,
    backend/app/ai/intent_parser.py:322:        rendered_prompt=render_intent_parser_prompt(context),
    backend/app/ai/intent_parser.py:327:def get_intent_parser_response_schema() -> dict[str, Any]:
    backend/app/ai/intent_parser.py:328:    schema = IntentParserStructuredOutput.model_json_schema()
    backend/app/ai/intent_parser.py:334:    return (PROMPTS_ROOT / "intent_parser.md").read_text(encoding="utf-8")
    backend/app/ai/intent_parser.py:367:def _extract_structured_output(raw_response: dict[str, Any]) -> IntentParserStructuredOutput:
    backend/app/ai/intent_parser.py:370:        raise IntentParserTransportError(
    backend/app/ai/intent_parser.py:371:            f"Gemini intent parser request was blocked: {blocked_reason}",
    backend/app/ai/intent_parser.py:376:        raise IntentParserTransportError("Gemini intent parser returned no candidates")
    backend/app/ai/intent_parser.py:387:        raise IntentParserTransportError(
    backend/app/ai/intent_parser.py:388:            f"Gemini intent parser returned no text content (finish_reason={finish_reason})",
    backend/app/ai/intent_parser.py:395:        raise IntentParserTransportError("Gemini intent parser returned invalid JSON") from exc
    backend/app/ai/intent_parser.py:398:        return IntentParserStructuredOutput.model_validate(structured_payload)
    backend/app/ai/intent_parser.py:400:        raise IntentParserTransportError(
    backend/app/ai/intent_parser.py:401:            "Gemini intent parser returned JSON that did not match the expected structure",
    backend/app/repositories/assets.py:14:    AssetKind.FINAL_AUDIO,
    backend/app/repositories/assets.py:33:        audio_job_id: str | None = None,
    backend/app/repositories/assets.py:47:            audio_job_id=audio_job_id,
    backend/app/repositories/sessions.py:11:    AudioJob,
    backend/app/repositories/sessions.py:16:    Pitch,
    backend/app/repositories/sessions.py:40:    selected_pitch: Pitch | None
    backend/app/repositories/sessions.py:45:    active_audio_job: AudioJob | None
    backend/app/repositories/sessions.py:47:    latest_audio_asset: SessionAsset | None
    backend/app/repositories/sessions.py:94:            selected_pitch=self._get_selected_pitch(session_id),
    backend/app/repositories/sessions.py:99:            active_audio_job=self._get_active_audio_job(session_id),
    backend/app/repositories/sessions.py:101:            latest_audio_asset=self._get_latest_audio_asset(session_id),
    backend/app/repositories/sessions.py:126:    def _get_selected_pitch(self, session_id: str) -> Pitch | None:
    backend/app/repositories/sessions.py:127:        stmt: Select[tuple[Pitch]] = (
    backend/app/repositories/sessions.py:128:            select(Pitch)
    backend/app/repositories/sessions.py:129:            .where(Pitch.session_id == session_id, Pitch.is_selected.is_(True))
    backend/app/repositories/sessions.py:130:            .order_by(Pitch.created_at.desc())
    backend/app/repositories/sessions.py:174:    def _get_active_audio_job(self, session_id: str) -> AudioJob | None:
    backend/app/repositories/sessions.py:175:        stmt: Select[tuple[AudioJob]] = (
    backend/app/repositories/sessions.py:176:            select(AudioJob)
    backend/app/repositories/sessions.py:178:                AudioJob.session_id == session_id,
    backend/app/repositories/sessions.py:179:                AudioJob.status.in_(ACTIVE_JOB_STATUSES),
    backend/app/repositories/sessions.py:181:            .order_by(AudioJob.created_at.desc())
    backend/app/repositories/sessions.py:199:    def _get_latest_audio_asset(self, session_id: str) -> SessionAsset | None:
    backend/app/repositories/sessions.py:204:                SessionAsset.asset_kind == AssetKind.FINAL_AUDIO,

## Command Started

- Time: `2026-04-01T07:31:08-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `11`
- Summary: in progress: /bin/zsh -lc 'pwd && git branch --show-current && git status --short'

### Full Text

    Command: /bin/zsh -lc 'pwd && git branch --show-current && git status --short'
    Status: in progress

## Command Finished

- Time: `2026-04-01T07:31:08-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `12`
- Summary: completed, exit 0: /bin/zsh -lc 'pwd && git branch --show-current && git status --short'

### Full Text

    Command: /bin/zsh -lc 'pwd && git branch --show-current && git status --short'
    Status: completed
    Exit code: 0
    Output:
    /Users/kevin/code/storyteller
    yolopilot-init-37-agent-tool-registry
     M prompts/36-conversation-memory-summaries.yolopilot.jsonlines
     M prompts/36-conversation-memory-summaries.yolopilot.md
    ?? prompts/37-agent-tool-registry.codex.jsonlines
    ?? prompts/37-agent-tool-registry.yolopilot.jsonlines
    ?? prompts/37-agent-tool-registry.yolopilot.md

## Agent Message

- Time: `2026-04-01T07:31:20-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `13`
- Summary: I found the current action vocabulary split between the intent parser prompt code, action policy rules, and worker/job handlers. Next I’m reading those seams to pull the shared story operations into one registry instead of duplicating an...

### Full Text

    I found the current action vocabulary split between the intent parser prompt code, action policy rules, and worker/job handlers. Next I’m reading those seams to pull the shared story operations into one registry instead of duplicating another layer.

## Command Started

- Time: `2026-04-01T07:31:20-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `14`
- Summary: in progress: /bin/zsh -lc "sed -n '1,260p' backend/backend/app/models/chat_actions.py"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,260p' backend/backend/app/models/chat_actions.py"
    Status: in progress

## Command Started

- Time: `2026-04-01T07:31:20-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `15`
- Summary: in progress: /bin/zsh -lc "sed -n '1,260p' backend/backend/app/services/intent_parser.py"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,260p' backend/backend/app/services/intent_parser.py"
    Status: in progress

## Command Finished

- Time: `2026-04-01T07:31:20-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `16`
- Summary: failed, exit 1: /bin/zsh -lc "sed -n '1,260p' backend/backend/app/models/chat_actions.py"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,260p' backend/backend/app/models/chat_actions.py"
    Status: failed
    Exit code: 1
    Output:
    sed: backend/backend/app/models/chat_actions.py: No such file or directory

## Command Finished

- Time: `2026-04-01T07:31:20-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `17`
- Summary: failed, exit 1: /bin/zsh -lc "sed -n '1,260p' backend/backend/app/services/intent_parser.py"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,260p' backend/backend/app/services/intent_parser.py"
    Status: failed
    Exit code: 1
    Output:
    sed: backend/backend/app/services/intent_parser.py: No such file or directory

## Command Started

- Time: `2026-04-01T07:31:20-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `18`
- Summary: in progress: /bin/zsh -lc "sed -n '1,260p' backend/backend/app/ai/intent_parser.py"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,260p' backend/backend/app/ai/intent_parser.py"
    Status: in progress

## Command Finished

- Time: `2026-04-01T07:31:20-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `19`
- Summary: failed, exit 1: /bin/zsh -lc "sed -n '1,260p' backend/backend/app/ai/intent_parser.py"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,260p' backend/backend/app/ai/intent_parser.py"
    Status: failed
    Exit code: 1
    Output:
    sed: backend/backend/app/ai/intent_parser.py: No such file or directory

## Command Started

- Time: `2026-04-01T07:31:20-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `20`
- Summary: in progress: /bin/zsh -lc "sed -n '1,260p' backend/backend/app/services/action_policy.py"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,260p' backend/backend/app/services/action_policy.py"
    Status: in progress

## Command Finished

- Time: `2026-04-01T07:31:20-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `21`
- Summary: failed, exit 1: /bin/zsh -lc "sed -n '1,260p' backend/backend/app/services/action_policy.py"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,260p' backend/backend/app/services/action_policy.py"
    Status: failed
    Exit code: 1
    Output:
    sed: backend/backend/app/services/action_policy.py: No such file or directory

## Command Started

- Time: `2026-04-01T07:31:20-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `22`
- Summary: in progress: /bin/zsh -lc "sed -n '1,260p' backend/backend/app/worker/registry.py"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,260p' backend/backend/app/worker/registry.py"
    Status: in progress

## Command Finished

- Time: `2026-04-01T07:31:20-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `23`
- Summary: failed, exit 1: /bin/zsh -lc "sed -n '1,260p' backend/backend/app/worker/registry.py"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,260p' backend/backend/app/worker/registry.py"
    Status: failed
    Exit code: 1
    Output:
    sed: backend/backend/app/worker/registry.py: No such file or directory

## Command Started

- Time: `2026-04-01T07:31:20-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `24`
- Summary: in progress: /bin/zsh -lc "sed -n '1,260p' backend/backend/app/worker/default_handlers.py"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,260p' backend/backend/app/worker/default_handlers.py"
    Status: in progress

## Command Finished

- Time: `2026-04-01T07:31:20-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `25`
- Summary: failed, exit 1: /bin/zsh -lc "sed -n '1,260p' backend/backend/app/worker/default_handlers.py"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,260p' backend/backend/app/worker/default_handlers.py"
    Status: failed
    Exit code: 1
    Output:
    sed: backend/backend/app/worker/default_handlers.py: No such file or directory

## Agent Message

- Time: `2026-04-01T07:31:40-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `26`
- Summary: The backend package lives under `backend/app`, not `backend/backend/app`. I’m correcting the read paths and continuing through the existing action, policy, and worker code.

### Full Text

    The backend package lives under `backend/app`, not `backend/backend/app`. I’m correcting the read paths and continuing through the existing action, policy, and worker code.

## Command Started

- Time: `2026-04-01T07:31:40-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `27`
- Summary: in progress: /bin/zsh -lc "sed -n '1,320p' backend/app/models/chat_actions.py"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,320p' backend/app/models/chat_actions.py"
    Status: in progress

## Command Started

- Time: `2026-04-01T07:31:40-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `28`
- Summary: in progress: /bin/zsh -lc "sed -n '1,320p' backend/app/services/intent_parser.py"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,320p' backend/app/services/intent_parser.py"
    Status: in progress

## Command Finished

- Time: `2026-04-01T07:31:40-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `29`
- Summary: completed, exit 0: /bin/zsh -lc "sed -n '1,320p' backend/app/models/chat_actions.py"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,320p' backend/app/models/chat_actions.py"
    Status: completed
    Exit code: 0
    Output:
    from __future__ import annotations

    from enum import Enum
    from typing import Annotated, Any, Literal, TypeAlias

    from pydantic import BaseModel, ConfigDict, Field, TypeAdapter, model_validator

    from app.models.workflow import WORKFLOW_STAGE_SEQUENCE, WorkflowStage

    CHAT_TO_UI_ACTION_SCHEMA_VERSION = 1


    class ChatToUIActionType(str, Enum):
        NAVIGATE_TO_STAGE = "navigate_to_stage"
        SELECT_GENRE = "select_genre"
        SELECT_TONE = "select_tone"
        UPDATE_STORY_BRIEF = "update_story_brief"
        REGENERATE_PITCHES = "regenerate_pitches"
        SELECT_PITCH = "select_pitch"
        SELECT_CHARACTER_SHEET = "select_character_sheet"
        REFINE_CHARACTER_SHEET = "refine_character_sheet"
        REGENERATE_CHARACTER_SHEET = "regenerate_character_sheet"
        ACCEPT_BEAT_SHEET = "accept_beat_sheet"
        REFINE_BEAT_SHEET = "refine_beat_sheet"
        REGENERATE_BEAT_SHEET = "regenerate_beat_sheet"
        UPDATE_STORY_SETUP = "update_story_setup"
        START_COMPOSITION = "start_composition"
        PAUSE_JOB = "pause_job"
        RESUME_JOB = "resume_job"
        REDIRECT_COMPOSITION = "redirect_composition"
        UPDATE_AUDIO_SETTINGS = "update_audio_settings"
        START_AUDIO_GENERATION = "start_audio_generation"
        OPEN_FINALIZE_VIEW = "open_finalize_view"
        DOWNLOAD_ASSET = "download_asset"


    class ChatToUIActionDefaultPolicy(str, Enum):
        AUTO_APPLY_CANDIDATE = "auto_apply_candidate"
        CONFIRM_FIRST = "confirm_first"


    class ChatToUIJobKind(str, Enum):
        COMPOSITION = "composition"
        AUDIO = "audio"


    class StoryBriefEditMode(str, Enum):
        REPLACE = "replace"
        APPEND = "append"
        MERGE = "merge"


    class CompositionStartMode(str, Enum):
        FRESH = "fresh"
        CONTINUE = "continue"
        REWRITE = "rewrite"


    class FinalizeView(str, Enum):
        READER = "reader"
        PLAYER = "player"


    class DownloadAssetKind(str, Enum):
        STORY_DOCX = "story_docx"
        FINAL_AUDIO = "final_audio"


    DEFAULT_CHAT_TO_UI_ACTION_POLICIES: dict[ChatToUIActionType, ChatToUIActionDefaultPolicy] = {
        ChatToUIActionType.NAVIGATE_TO_STAGE: ChatToUIActionDefaultPolicy.AUTO_APPLY_CANDIDATE,
        ChatToUIActionType.SELECT_GENRE: ChatToUIActionDefaultPolicy.CONFIRM_FIRST,
        ChatToUIActionType.SELECT_TONE: ChatToUIActionDefaultPolicy.CONFIRM_FIRST,
        ChatToUIActionType.UPDATE_STORY_BRIEF: ChatToUIActionDefaultPolicy.AUTO_APPLY_CANDIDATE,
        ChatToUIActionType.REGENERATE_PITCHES: ChatToUIActionDefaultPolicy.CONFIRM_FIRST,
        ChatToUIActionType.SELECT_PITCH: ChatToUIActionDefaultPolicy.CONFIRM_FIRST,
        ChatToUIActionType.SELECT_CHARACTER_SHEET: ChatToUIActionDefaultPolicy.CONFIRM_FIRST,
        ChatToUIActionType.REFINE_CHARACTER_SHEET: ChatToUIActionDefaultPolicy.CONFIRM_FIRST,
        ChatToUIActionType.REGENERATE_CHARACTER_SHEET: ChatToUIActionDefaultPolicy.CONFIRM_FIRST,
        ChatToUIActionType.ACCEPT_BEAT_SHEET: ChatToUIActionDefaultPolicy.CONFIRM_FIRST,
        ChatToUIActionType.REFINE_BEAT_SHEET: ChatToUIActionDefaultPolicy.CONFIRM_FIRST,
        ChatToUIActionType.REGENERATE_BEAT_SHEET: ChatToUIActionDefaultPolicy.CONFIRM_FIRST,
        ChatToUIActionType.UPDATE_STORY_SETUP: ChatToUIActionDefaultPolicy.AUTO_APPLY_CANDIDATE,
        ChatToUIActionType.START_COMPOSITION: ChatToUIActionDefaultPolicy.CONFIRM_FIRST,
        ChatToUIActionType.PAUSE_JOB: ChatToUIActionDefaultPolicy.CONFIRM_FIRST,
        ChatToUIActionType.RESUME_JOB: ChatToUIActionDefaultPolicy.CONFIRM_FIRST,
        ChatToUIActionType.REDIRECT_COMPOSITION: ChatToUIActionDefaultPolicy.CONFIRM_FIRST,
        ChatToUIActionType.UPDATE_AUDIO_SETTINGS: ChatToUIActionDefaultPolicy.AUTO_APPLY_CANDIDATE,
        ChatToUIActionType.START_AUDIO_GENERATION: ChatToUIActionDefaultPolicy.CONFIRM_FIRST,
        ChatToUIActionType.OPEN_FINALIZE_VIEW: ChatToUIActionDefaultPolicy.AUTO_APPLY_CANDIDATE,
        ChatToUIActionType.DOWNLOAD_ASSET: ChatToUIActionDefaultPolicy.AUTO_APPLY_CANDIDATE,
    }


    def get_chat_to_ui_action_default_policy(
        action_type: ChatToUIActionType,
    ) -> ChatToUIActionDefaultPolicy:
        return DEFAULT_CHAT_TO_UI_ACTION_POLICIES[action_type]


    class ChatToUIModel(BaseModel):
        model_config = ConfigDict(extra="forbid")

        schema_version: int = Field(default=CHAT_TO_UI_ACTION_SCHEMA_VERSION, ge=1)


    class ChatToUIExtractedValues(BaseModel):
        model_config = ConfigDict(extra="forbid")


    def _require_any_identifier(
        *values: str | int | None,
        error_message: str,
    ) -> None:
        if all(value is None for value in values):
            raise ValueError(error_message)


    def _require_any_field(
        values: dict[str, object | None],
        error_message: str,
    ) -> None:
        if all(value is None for value in values.values()):
            raise ValueError(error_message)


    class SelectGenreValues(ChatToUIExtractedValues):
        genre_id: str | None = Field(default=None, min_length=1)
        genre_slug: str | None = Field(default=None, min_length=1)
        genre_label: str | None = Field(default=None, min_length=1)

        @model_validator(mode="after")
        def validate_identifier(self) -> SelectGenreValues:
            _require_any_identifier(
                self.genre_id,
                self.genre_slug,
                self.genre_label,
                error_message="select_genre requires a genre_id, genre_slug, or genre_label",
            )
            return self


    class SelectToneValues(ChatToUIExtractedValues):
        tone_profile_id: str | None = Field(default=None, min_length=1)
        tone_profile_slug: str | None = Field(default=None, min_length=1)
        tone_profile_label: str | None = Field(default=None, min_length=1)

        @model_validator(mode="after")
        def validate_identifier(self) -> SelectToneValues:
            _require_any_identifier(
                self.tone_profile_id,
                self.tone_profile_slug,
                self.tone_profile_label,
                error_message=(
                    "select_tone requires a tone_profile_id, tone_profile_slug, or tone_profile_label"
                ),
            )
            return self


    class UpdateStoryBriefValues(ChatToUIExtractedValues):
        raw_brief: str | None = Field(default=None, min_length=1)
        normalized_summary: str | None = Field(default=None, min_length=1)
        planning_notes: str | None = Field(default=None, min_length=1)
        edit_mode: StoryBriefEditMode = StoryBriefEditMode.MERGE

        @model_validator(mode="after")
        def validate_story_brief(self) -> UpdateStoryBriefValues:
            _require_any_field(
                {
                    "raw_brief": self.raw_brief,
                    "normalized_summary": self.normalized_summary,
                    "planning_notes": self.planning_notes,
                },
                error_message=(
                    "update_story_brief requires raw_brief, normalized_summary, or planning_notes"
                ),
            )
            return self


    class RegeneratePitchesValues(ChatToUIExtractedValues):
        candidate_count: int | None = Field(default=None, ge=2, le=6)
        guidance: str | None = Field(default=None, min_length=1)
        preserve_selected_pitch: bool = False


    class SelectPitchValues(ChatToUIExtractedValues):
        pitch_id: str | None = Field(default=None, min_length=1)
        generation_key: str | None = Field(default=None, min_length=1)
        pitch_index: int | None = Field(default=None, ge=1)
        title: str | None = Field(default=None, min_length=1)

        @model_validator(mode="after")
        def validate_identifier(self) -> SelectPitchValues:
            _require_any_identifier(
                self.pitch_id,
                self.generation_key,
                self.pitch_index,
                self.title,
                error_message=(
                    "select_pitch requires a pitch_id, generation_key, pitch_index, or title"
                ),
            )
            return self


    class SelectCharacterSheetValues(ChatToUIExtractedValues):
        character_sheet_id: str | None = Field(default=None, min_length=1)
        revision_number: int | None = Field(default=None, ge=1)
        title: str | None = Field(default=None, min_length=1)

        @model_validator(mode="after")
        def validate_identifier(self) -> SelectCharacterSheetValues:
            _require_any_identifier(
                self.character_sheet_id,
                self.revision_number,
                self.title,
                error_message=(
                    "select_character_sheet requires a character_sheet_id, revision_number, or title"
                ),
            )
            return self


    class RefineCharacterSheetValues(ChatToUIExtractedValues):
        instructions: str = Field(min_length=1)
        focus_character_names: list[str] = Field(default_factory=list)
        change_summary: str | None = Field(default=None, min_length=1)


    class RegenerateCharacterSheetValues(ChatToUIExtractedValues):
        guidance: str | None = Field(default=None, min_length=1)


    class AcceptBeatSheetValues(ChatToUIExtractedValues):
        beat_sheet_id: str | None = Field(default=None, min_length=1)
        revision_number: int | None = Field(default=None, ge=1)

        @model_validator(mode="after")
        def validate_identifier(self) -> AcceptBeatSheetValues:
            _require_any_identifier(
                self.beat_sheet_id,
                self.revision_number,
                error_message="accept_beat_sheet requires a beat_sheet_id or revision_number",
            )
            return self


    class RefineBeatSheetValues(ChatToUIExtractedValues):
        instructions: str = Field(min_length=1)
        beat_names: list[str] = Field(default_factory=list)
        bedtime_goal: str | None = Field(default=None, min_length=1)


    class RegenerateBeatSheetValues(ChatToUIExtractedValues):
        guidance: str | None = Field(default=None, min_length=1)
        focus_beats: list[str] = Field(default_factory=list)


    class UpdateStorySetupValues(ChatToUIExtractedValues):
        target_word_count: int | None = Field(default=None, ge=100, le=10000)
        target_runtime_minutes: int | None = Field(default=None, ge=1, le=180)
        chapter_count: int | None = Field(default=None, ge=1, le=24)
        chapter_style: str | None = Field(default=None, min_length=1)
        guidance_notes: str | None = Field(default=None, min_length=1)

        @model_validator(mode="after")
        def validate_story_setup(self) -> UpdateStorySetupValues:
            _require_any_field(
                {
                    "target_word_count": self.target_word_count,
                    "target_runtime_minutes": self.target_runtime_minutes,
                    "chapter_count": self.chapter_count,
                    "chapter_style": self.chapter_style,
                    "guidance_notes": self.guidance_notes,
                },
                error_message=(
                    "update_story_setup requires at least one structured planning preference"
                ),
            )
            return self


    class StartCompositionValues(ChatToUIExtractedValues):
        mode: CompositionStartMode = CompositionStartMode.FRESH
        instructions: str | None = Field(default=None, min_length=1)
        restart_from_segment_index: int | None = Field(default=None, ge=1)


    class JobControlValues(ChatToUIExtractedValues):
        job_kind: ChatToUIJobKind
        job_id: str | None = Field(default=None, min_length=1)
        reason: str | None = Field(default=None, min_length=1)


    class RedirectCompositionValues(ChatToUIExtractedValues):
        instructions: str = Field(min_length=1)
        rewrite_from_segment_index: int | None = Field(default=None, ge=1)
        preserve_completed_segments: bool = True


    class UpdateAudioSettingsValues(ChatToUIExtractedValues):
        voice_key: str | None = Field(default=None, min_length=1)
        playback_speed: float | None = Field(default=None, ge=0.5, le=2.0)
        include_background_music: bool | None = None
        music_profile: str | None = Field(default=None, min_length=1)
        guidance_notes: str | None = Field(default=None, min_length=1)

        @model_validator(mode="after")
        def validate_audio_settings(self) -> UpdateAudioSettingsValues:
            _require_any_field(
                {
                    "voice_key": self.voice_key,
                    "playback_speed": self.playback_speed,
                    "include_background_music": self.include_background_music,
                    "music_profile": self.music_profile,
                    "guidance_notes": self.guidance_notes,
                },
                error_message=(
                    "update_audio_settings requires at least one audio setting or guidance note"

## Command Finished

- Time: `2026-04-01T07:31:40-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `30`
- Summary: completed, exit 0: /bin/zsh -lc "sed -n '1,320p' backend/app/services/intent_parser.py"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,320p' backend/app/services/intent_parser.py"
    Status: completed
    Exit code: 0
    Output:
    from __future__ import annotations

    from pydantic import ValidationError
    from sqlalchemy.orm import Session

    from app.ai import (
        IntentParserAdapter,
        IntentParserTransportError,
        build_intent_parser_invocation,
    )
    from app.models import (
        EXPLICIT_CHAT_COMMAND_MODEL_ID,
        EXPLICIT_CHAT_COMMAND_PROMPT_VERSION,
        ChatMessageRole,
        ChatToUIActionBatch,
        ExplicitChatCommandId,
        ExplicitChatCommandRequest,
        IntentParserPromptContext,
        IntentParserStageContext,
        IntentParserStatus,
        IntentParserStructuredOutput,
        ParsedChatIntentResponse,
        SessionSnapshot,
        WorkflowStage,
        build_action_policy_request_from_batch,
        get_workflow_stage_definition,
    )
    from app.services.action_policy import SessionActionPolicyService
    from app.services.agent_context import build_session_agent_context_summary
    from app.services.event_log import SessionEventLogService
    from app.services.sessions import SessionNotFoundError, SessionService


    class SessionIntentParserService:
        def __init__(self, session: Session, parser: IntentParserAdapter | None = None):
            self._session = session
            self._parser = parser
            self._sessions = SessionService(session)
            self._event_log = SessionEventLogService(session)

        def parse_user_message(
            self,
            session_id: str,
            *,
            message: str,
            explicit_command: ExplicitChatCommandRequest | None = None,
        ) -> ParsedChatIntentResponse:
            normalized_message = message.strip()
            if not normalized_message:
                raise ValueError("message must not be empty")

            snapshot = self._sessions.load_session_snapshot(session_id)
            context = _build_prompt_context(snapshot, normalized_message)

            self._event_log.record_chat_message(
                session_id,
                message_role=ChatMessageRole.USER,
                content=normalized_message,
                stage=context.stage_context.current_stage,
            )
            self._session.commit()

            raw_response = None
            prompt_version: str
            model_id: str
            rendered_prompt: str

            if explicit_command is not None:
                result = _build_explicit_command_result(
                    snapshot,
                    explicit_command=explicit_command,
                )
                prompt_version = EXPLICIT_CHAT_COMMAND_PROMPT_VERSION
                model_id = EXPLICIT_CHAT_COMMAND_MODEL_ID
                rendered_prompt = _build_explicit_command_audit_prompt(
                    message=normalized_message,
                    explicit_command=explicit_command,
                )
                raw_response = explicit_command.model_dump(mode="json")
            else:
                if self._parser is None:
                    raise RuntimeError("intent parser adapter is required for free-form chat parsing")

                invocation = build_intent_parser_invocation(
                    context,
                    model_id=self._parser.model_id,
                )
                prompt_version = invocation.prompt_version
                model_id = invocation.model_id
                rendered_prompt = invocation.rendered_prompt

                try:
                    invocation_result = self._parser.parse(invocation)
                    raw_response = invocation_result.raw_response
                    result = _normalize_parser_output(invocation_result.structured_output)
                except (IntentParserTransportError, ValidationError):
                    result = _build_failed_result()

            if result.status == IntentParserStatus.PARSED and result.proposed_actions.actions:
                result.policy_evaluation = SessionActionPolicyService(
                    self._session
                ).evaluate_request_against_snapshot(
                    snapshot,
                    request=build_action_policy_request_from_batch(result.proposed_actions),
                )
            else:
                result.policy_evaluation = None

            self._event_log.record_chat_intent_parsed(
                session_id,
                prompt_version=prompt_version,
                model_id=model_id,
                current_stage=context.stage_context.current_stage,
                stage_label=context.stage_context.current_stage_label,
                stage_description=context.stage_context.current_stage_description,
                stage_status=context.stage_context.current_stage_status,
                stage_detail=context.stage_context.current_stage_detail,
                session_summary=context.session_summary,
                user_message=normalized_message,
                rendered_prompt=rendered_prompt,
                result=result,
                raw_response=raw_response,
            )
            self._event_log.record_chat_message(
                session_id,
                message_role=ChatMessageRole.ASSISTANT,
                content=result.assistant_response,
                stage=context.stage_context.current_stage,
                source="intent_parser",
            )
            self._session.commit()
            return result


    def _normalize_parser_output(
        structured_output: IntentParserStructuredOutput,
    ) -> ParsedChatIntentResponse:
        if structured_output.status != IntentParserStatus.PARSED:
            return ParsedChatIntentResponse(
                status=structured_output.status,
                needs_clarification=structured_output.needs_clarification,
                assistant_response=structured_output.assistant_response,
                clarification_reason=structured_output.clarification_reason,
                proposed_actions=ChatToUIActionBatch(),
            )

        strict_actions = ChatToUIActionBatch.model_validate(
            structured_output.proposed_actions.model_dump(mode="json"),
        )
        return ParsedChatIntentResponse(
            status=IntentParserStatus.PARSED,
            needs_clarification=False,
            assistant_response=structured_output.assistant_response,
            clarification_reason=None,
            proposed_actions=strict_actions,
        )


    def _build_failed_result() -> ParsedChatIntentResponse:
        return ParsedChatIntentResponse(
            status=IntentParserStatus.FAILED,
            assistant_response=(
                "I couldn't safely translate that into structured story-studio actions yet. "
                "Please rephrase the change you want, like tone, runtime, beats, or audio settings."
            ),
            proposed_actions=ChatToUIActionBatch(),
        )


    def _build_prompt_context(
        snapshot: SessionSnapshot,
        user_message: str,
    ) -> IntentParserPromptContext:
        current_stage_state = _find_stage_state(snapshot, snapshot.current_stage)
        stage_definition = get_workflow_stage_definition(snapshot.current_stage)
        return IntentParserPromptContext(
            session_id=snapshot.id,
            display_title=snapshot.display_title,
            overall_status=snapshot.overall_status,
            resume_stage=snapshot.resume_stage,
            stage_context=IntentParserStageContext(
                current_stage=snapshot.current_stage,
                current_stage_label=stage_definition.label,
                current_stage_description=stage_definition.description,
                current_stage_status=current_stage_state.status,
                current_stage_detail=current_stage_state.detail,
            ),
            session_summary=snapshot.agent_context_summary
            or build_session_agent_context_summary(snapshot),
            user_message=user_message,
        )


    def _find_stage_state(snapshot: SessionSnapshot, stage: WorkflowStage):
        for item in snapshot.stage_states:
            if item.stage == stage:
                return item
        raise SessionNotFoundError(f"session {snapshot.id!r} is missing stage state for {stage.value}")


    def _build_explicit_command_result(
        snapshot: SessionSnapshot,
        *,
        explicit_command: ExplicitChatCommandRequest,
    ) -> ParsedChatIntentResponse:
        if explicit_command.command_id == ExplicitChatCommandId.SUMMARIZE_PLAN:
            assistant_response = _build_plan_summary_response(snapshot)
        elif explicit_command.command_id == ExplicitChatCommandId.NEXT_STAGE:
            if explicit_command.proposed_actions.actions:
                target_stage = explicit_command.proposed_actions.actions[0].target_stage
                stage_label = get_workflow_stage_definition(target_stage).label
                assistant_response = f"I can move the workspace to {stage_label}."
            else:
                assistant_response = (
                    "You are already at the final stage, so there is no later "
                    "workspace step to open."
                )
        elif explicit_command.command_id == ExplicitChatCommandId.REGENERATE_PITCHES:
            assistant_response = (
                "I can queue a fresh set of pitch options from the current bedtime brief."
            )
        elif explicit_command.command_id == ExplicitChatCommandId.PAUSE_WRITING:
            assistant_response = "I can pause the active writing run."
        elif explicit_command.command_id == ExplicitChatCommandId.RESUME_WRITING:
            assistant_response = "I can resume the paused writing run."
        else:
            assistant_response = "I can translate that command into the story workspace."

        return ParsedChatIntentResponse(
            status=IntentParserStatus.PARSED,
            needs_clarification=False,
            assistant_response=assistant_response,
            clarification_reason=None,
            proposed_actions=explicit_command.proposed_actions,
        )


    def _build_explicit_command_audit_prompt(
        *,
        message: str,
        explicit_command: ExplicitChatCommandRequest,
    ) -> str:
        return (
            f"Explicit command path\n"
            f"message={message}\n"
            f"command_id={explicit_command.command_id.value}\n"
            f"source={explicit_command.source.value}\n"
            f"proposed_actions={explicit_command.proposed_actions.model_dump_json()}"
        )


    def _build_plan_summary_response(snapshot: SessionSnapshot) -> str:
        stage_definition = get_workflow_stage_definition(snapshot.current_stage)
        current_focus = stage_definition.label
        current_detail = next(
            (
                stage.detail
                for stage in snapshot.stage_states
                if stage.stage == snapshot.current_stage and stage.detail
            ),
            None,
        )

        plan_parts: list[str] = []
        if snapshot.selected_genre is not None:
            plan_parts.append(snapshot.selected_genre.label)
        if snapshot.selected_tone_profile is not None:
            plan_parts.append(snapshot.selected_tone_profile.label)
        if snapshot.selected_pitch is not None:
            plan_parts.append(f'pitch "{snapshot.selected_pitch.title}"')

        if snapshot.selected_story_setup is not None:
            setup_parts: list[str] = []
            if snapshot.selected_story_setup.target_runtime_minutes is not None:
                setup_parts.append(f"~{snapshot.selected_story_setup.target_runtime_minutes} minutes")
            if snapshot.selected_story_setup.chapter_count is not None:
                setup_parts.append(f"{snapshot.selected_story_setup.chapter_count} chapters")
            if snapshot.selected_story_setup.target_word_count is not None:
                setup_parts.append(f"{snapshot.selected_story_setup.target_word_count} words")
            if setup_parts:
                plan_parts.append(", ".join(setup_parts))

        if snapshot.active_composition_job is not None:
            plan_parts.append(
                f"writing is {snapshot.active_composition_job.status.replace('_', ' ')}"
            )
        elif snapshot.active_audio_job is not None:
            plan_parts.append(
                f"audio is {snapshot.active_audio_job.status.replace('_', ' ')}"
            )

        plan_summary = ", ".join(plan_parts) if plan_parts else "the story plan is still taking shape"
        focus_tail = f" {current_detail}" if current_detail else ""
        return f"Current focus is {current_focus.lower()}.{focus_tail} Plan so far: {plan_summary}."

## Command Started

- Time: `2026-04-01T07:31:40-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `31`
- Summary: in progress: /bin/zsh -lc "sed -n '1,360p' backend/app/ai/intent_parser.py"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,360p' backend/app/ai/intent_parser.py"
    Status: in progress

## Command Finished

- Time: `2026-04-01T07:31:40-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `32`
- Summary: completed, exit 0: /bin/zsh -lc "sed -n '1,360p' backend/app/ai/intent_parser.py"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,360p' backend/app/ai/intent_parser.py"
    Status: completed
    Exit code: 0
    Output:
    from __future__ import annotations

    import json
    from functools import lru_cache
    from pathlib import Path
    from string import Template
    from typing import Any, Protocol

    import httpx

    from app.models.chat_actions import DEFAULT_CHAT_TO_UI_ACTION_POLICIES
    from app.models.intent_parser import (
        INTENT_PARSER_PROMPT_VERSION,
        IntentParserInvocation,
        IntentParserInvocationResult,
        IntentParserPromptContext,
        IntentParserStructuredOutput,
    )

    PROMPTS_ROOT = Path(__file__).resolve().parent / "prompts"
    DEFAULT_GEMINI_API_BASE_URL = "https://generativelanguage.googleapis.com/v1beta"
    _SUPPORTED_JSON_SCHEMA_KEYS = {
        "$anchor",
        "$defs",
        "$id",
        "$ref",
        "additionalProperties",
        "anyOf",
        "description",
        "enum",
        "format",
        "items",
        "maxItems",
        "maximum",
        "minItems",
        "minimum",
        "oneOf",
        "prefixItems",
        "properties",
        "required",
        "title",
        "type",
    }
    _ACTION_CATALOG = (
        {
            "action_type": "navigate_to_stage",
            "stage": "any",
            "description": "Open a different workflow stage without changing durable data.",
            "common_fields": [],
        },
        {
            "action_type": "select_genre",
            "stage": "genre",
            "description": "Select a catalog genre by id, slug, or label.",
            "common_fields": ["genre_id", "genre_slug", "genre_label"],
        },
        {
            "action_type": "select_tone",
            "stage": "tone",
            "description": "Select a tone profile by id, slug, or label.",
            "common_fields": [
                "tone_profile_id",
                "tone_profile_slug",
                "tone_profile_label",
            ],
        },
        {
            "action_type": "update_story_brief",
            "stage": "brief",
            "description": "Change the story brief text or planning notes.",
            "common_fields": [
                "raw_brief",
                "normalized_summary",
                "planning_notes",
                "edit_mode",
            ],
        },
        {
            "action_type": "regenerate_pitches",
            "stage": "pitches",
            "description": "Ask for a new batch of pitches.",
            "common_fields": ["candidate_count", "guidance", "preserve_selected_pitch"],
        },
        {
            "action_type": "select_pitch",
            "stage": "pitches",
            "description": "Select a pitch by id, generation key, index, or title.",
            "common_fields": ["pitch_id", "generation_key", "pitch_index", "title"],
        },
        {
            "action_type": "select_character_sheet",
            "stage": "characters",
            "description": "Choose a character sheet revision.",
            "common_fields": ["character_sheet_id", "revision_number", "title"],
        },
        {
            "action_type": "refine_character_sheet",
            "stage": "characters",
            "description": "Request character-sheet edits with concrete instructions.",
            "common_fields": [
                "instructions",
                "focus_character_names",
                "change_summary",
            ],
        },
        {
            "action_type": "regenerate_character_sheet",
            "stage": "characters",
            "description": "Regenerate the character sheet with optional guidance.",
            "common_fields": ["guidance"],
        },
        {
            "action_type": "accept_beat_sheet",
            "stage": "beats",
            "description": "Accept a beat sheet revision.",
            "common_fields": ["beat_sheet_id", "revision_number"],
        },
        {
            "action_type": "refine_beat_sheet",
            "stage": "beats",
            "description": "Request beat-sheet edits with explicit instructions.",
            "common_fields": ["instructions", "beat_names", "bedtime_goal"],
        },
        {
            "action_type": "regenerate_beat_sheet",
            "stage": "beats",
            "description": "Regenerate the beat sheet with guidance.",
            "common_fields": ["guidance", "focus_beats"],
        },
        {
            "action_type": "update_story_setup",
            "stage": "story_setup",
            "description": (
                "Update soft planning targets like length, runtime, chapters, or setup guidance."
            ),
            "common_fields": [
                "target_word_count",
                "target_runtime_minutes",
                "chapter_count",
                "chapter_style",
                "guidance_notes",
            ],
        },
        {
            "action_type": "start_composition",
            "stage": "composition",
            "description": "Start writing, continue, or rewrite composition.",
            "common_fields": ["mode", "instructions", "restart_from_segment_index"],
        },
        {
            "action_type": "pause_job",
            "stage": "composition|audio",
            "description": "Pause a composition or audio job.",
            "common_fields": ["job_kind", "job_id", "reason"],
        },
        {
            "action_type": "resume_job",
            "stage": "composition|audio",
            "description": "Resume a composition or audio job.",
            "common_fields": ["job_kind", "job_id", "reason"],
        },
        {
            "action_type": "redirect_composition",
            "stage": "composition",
            "description": "Redirect writing with concrete rewrite instructions.",
            "common_fields": [
                "instructions",
                "rewrite_from_segment_index",
                "preserve_completed_segments",
            ],
        },
        {
            "action_type": "update_audio_settings",
            "stage": "audio",
            "description": "Change narration settings like voice, speed, music, or guidance notes.",
            "common_fields": [
                "voice_key",
                "playback_speed",
                "include_background_music",
                "music_profile",
                "guidance_notes",
            ],
        },
        {
            "action_type": "start_audio_generation",
            "stage": "audio",
            "description": "Start or regenerate audio generation.",
            "common_fields": [
                "voice_key",
                "playback_speed",
                "include_background_music",
                "music_profile",
                "regenerate_existing_audio",
            ],
        },
        {
            "action_type": "open_finalize_view",
            "stage": "finalize",
            "description": "Open the finalize reader or player view.",
            "common_fields": ["view"],
        },
        {
            "action_type": "download_asset",
            "stage": "finalize",
            "description": "Download the story docx or final audio asset.",
            "common_fields": ["asset_kind"],
        },
    )


    class IntentParserError(RuntimeError):
        """Base error for intent parser adapter failures."""


    class IntentParserTransportError(IntentParserError):
        """Raised when the Gemini transport call fails or returns unusable data."""


    class IntentParserAdapter(Protocol):
        @property
        def model_id(self) -> str: ...

        def parse(self, invocation: IntentParserInvocation) -> IntentParserInvocationResult: ...

        def close(self) -> None: ...


    class GeminiIntentParserAdapter:
        def __init__(
            self,
            *,
            credential: str,
            model_id: str,
            base_url: str = DEFAULT_GEMINI_API_BASE_URL,
            client: httpx.Client | None = None,
        ) -> None:
            self._credential = credential
            self._model_id = model_id
            self._base_url = base_url.rstrip("/")
            self._owns_client = client is None
            self._client = client or httpx.Client(timeout=30.0)

        @property
        def model_id(self) -> str:
            return self._model_id

        def parse(self, invocation: IntentParserInvocation) -> IntentParserInvocationResult:
            response = self._client.post(
                f"{self._base_url}/models/{self._model_id}:generateContent",
                headers={
                    "content-type": "application/json",
                    "x-goog-api-key": self._credential,
                },
                json={
                    "systemInstruction": {
                        "parts": [{"text": ("Return only JSON that matches the requested schema.")}]
                    },
                    "contents": [
                        {
                            "role": "user",
                            "parts": [{"text": invocation.rendered_prompt}],
                        }
                    ],
                    "generationConfig": {
                        "temperature": 0,
                        "candidateCount": 1,
                        "maxOutputTokens": 1200,
                        "responseMimeType": "application/json",
                        "responseJsonSchema": get_intent_parser_response_schema(),
                    },
                },
            )

            try:
                response.raise_for_status()
            except httpx.HTTPStatusError as exc:
                raise IntentParserTransportError(
                    f"Gemini intent parser request failed with status {exc.response.status_code}",
                ) from exc

            raw_response = response.json()
            structured_output = _extract_structured_output(raw_response)
            return IntentParserInvocationResult(
                invocation=invocation,
                structured_output=structured_output,
                raw_response=raw_response,
            )

        def close(self) -> None:
            if self._owns_client:
                self._client.close()


    def render_intent_parser_prompt(context: IntentParserPromptContext) -> str:
        template = Template(_read_prompt_template())
        return template.substitute(
            action_catalog_json=json.dumps(_ACTION_CATALOG, indent=2, sort_keys=True),
            default_policy_json=json.dumps(
                {key.value: value.value for key, value in DEFAULT_CHAT_TO_UI_ACTION_POLICIES.items()},
                indent=2,
                sort_keys=True,
            ),
            stage_context_json=json.dumps(
                context.stage_context.model_dump(mode="json"),
                indent=2,
                sort_keys=True,
            ),
            session_summary=context.session_summary,
            user_message=context.user_message,
        )


    def build_intent_parser_invocation(
        context: IntentParserPromptContext,
        *,
        model_id: str,
    ) -> IntentParserInvocation:
        return IntentParserInvocation(
            prompt_version=INTENT_PARSER_PROMPT_VERSION,
            model_id=model_id,
            context=context,
            rendered_prompt=render_intent_parser_prompt(context),
        )


    @lru_cache(maxsize=1)
    def get_intent_parser_response_schema() -> dict[str, Any]:
        schema = IntentParserStructuredOutput.model_json_schema()
        return _sanitize_json_schema(schema)


    @lru_cache(maxsize=1)
    def _read_prompt_template() -> str:
        return (PROMPTS_ROOT / "intent_parser.md").read_text(encoding="utf-8")


    def _sanitize_json_schema(value: Any) -> Any:
        if isinstance(value, list):
            return [_sanitize_json_schema(item) for item in value]

        if isinstance(value, dict):
            normalized: dict[str, Any] = {}

            if "const" in value and "enum" not in value:
                normalized["enum"] = [value["const"]]

            for key, item in value.items():
                if key == "const":
                    continue
                if key not in _SUPPORTED_JSON_SCHEMA_KEYS:
                    continue
                if key in {"$defs", "properties"}:
                    normalized[key] = {
                        name: _sanitize_json_schema(child) for name, child in item.items()
                    }
                    continue
                if key == "additionalProperties" and isinstance(item, dict):
                    normalized[key] = _sanitize_json_schema(item)
                    continue
                normalized[key] = _sanitize_json_schema(item)

## Command Started

- Time: `2026-04-01T07:31:40-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `33`
- Summary: in progress: /bin/zsh -lc "sed -n '1,360p' backend/app/services/action_policy.py"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,360p' backend/app/services/action_policy.py"
    Status: in progress

## Command Finished

- Time: `2026-04-01T07:31:40-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `34`
- Summary: completed, exit 0: /bin/zsh -lc "sed -n '1,360p' backend/app/services/action_policy.py"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,360p' backend/app/services/action_policy.py"
    Status: completed
    Exit code: 0
    Output:
    from __future__ import annotations

    from dataclasses import dataclass, field

    from sqlalchemy import Select, func, select
    from sqlalchemy.orm import Session

    from app.db import (
        AssetKind,
        AssetStatus,
        BeatSheet,
        CharacterSheet,
        Genre,
        JobStatus,
        Pitch,
        SessionAsset,
        ToneProfile,
    )
    from app.models.action_policy import (
        SessionActionDecision,
        SessionActionPolicyEvaluation,
        SessionActionPolicyEvaluationItem,
        SessionActionPolicyEvaluationRequest,
        SessionActionPolicyReason,
        SessionActionPolicySideEffect,
        SessionActionReasonCode,
        SessionActionSideEffectKind,
        build_action_policy_request_from_batch,
    )
    from app.models.chat_actions import (
        AcceptBeatSheetAction,
        ChatToUIAction,
        ChatToUIActionBatch,
        ChatToUIActionDefaultPolicy,
        ChatToUIActionType,
        ChatToUIJobKind,
        DownloadAssetAction,
        DownloadAssetKind,
        OpenFinalizeViewAction,
        PauseJobAction,
        RedirectCompositionAction,
        RegenerateBeatSheetAction,
        RegenerateCharacterSheetAction,
        RegeneratePitchesAction,
        ResumeJobAction,
        SelectCharacterSheetAction,
        SelectGenreAction,
        SelectPitchAction,
        SelectToneAction,
        StartAudioGenerationAction,
        StartCompositionAction,
        UpdateAudioSettingsAction,
        UpdateStoryBriefAction,
        UpdateStorySetupAction,
        get_chat_to_ui_action_default_policy,
    )
    from app.models.session import SessionSnapshot
    from app.models.workflow import (
        WORKFLOW_STAGE_SEQUENCE,
        WorkflowStage,
        WorkflowStageState,
        get_invalidated_stages_after_edit,
    )
    from app.services.sessions import SessionService

    ACTIVE_JOB_STATUSES = {
        JobStatus.QUEUED,
        JobStatus.IN_PROGRESS,
        JobStatus.PAUSED,
    }
    PAUSABLE_JOB_STATUSES = {
        JobStatus.QUEUED,
        JobStatus.IN_PROGRESS,
    }


    class SessionActionPolicyServiceError(Exception):
        """Base error for action policy failures."""


    @dataclass
    class _ResolvedAction:
        genre: Genre | None = None
        tone: ToneProfile | None = None
        pitch: Pitch | None = None
        character_sheet: CharacterSheet | None = None
        beat_sheet: BeatSheet | None = None


    @dataclass
    class _ComputedDecision:
        decision: SessionActionDecision
        reasons: list[SessionActionPolicyReason] = field(default_factory=list)
        side_effects: list[SessionActionPolicySideEffect] = field(default_factory=list)
        prerequisite_action_types: list[ChatToUIActionType] = field(default_factory=list)
        resolution: _ResolvedAction = field(default_factory=_ResolvedAction)


    @dataclass
    class _PolicyState:
        stage_statuses: dict[WorkflowStage, WorkflowStageState]
        selected_genre_id: str | None
        selected_tone_profile_id: str | None
        story_brief_present: bool
        selected_pitch_id: str | None
        selected_character_sheet_id: str | None
        selected_beat_sheet_id: str | None
        selected_story_setup_id: str | None
        active_composition_job_id: str | None
        active_composition_job_status: JobStatus | None
        active_audio_job_id: str | None
        active_audio_job_status: JobStatus | None
        ready_story_asset_kinds: set[AssetKind]
        ready_audio_asset_kinds: set[AssetKind]

        @classmethod
        def from_snapshot(
            cls,
            snapshot: SessionSnapshot,
            *,
            ready_story_asset_kinds: set[AssetKind],
            ready_audio_asset_kinds: set[AssetKind],
        ) -> _PolicyState:
            return cls(
                stage_statuses={item.stage: item.status for item in snapshot.stage_states},
                selected_genre_id=snapshot.selected_genre.id if snapshot.selected_genre else None,
                selected_tone_profile_id=(
                    snapshot.selected_tone_profile.id if snapshot.selected_tone_profile else None
                ),
                story_brief_present=snapshot.story_brief is not None,
                selected_pitch_id=snapshot.selected_pitch.id if snapshot.selected_pitch else None,
                selected_character_sheet_id=(
                    snapshot.selected_character_sheet.id if snapshot.selected_character_sheet else None
                ),
                selected_beat_sheet_id=(
                    snapshot.selected_beat_sheet.id if snapshot.selected_beat_sheet else None
                ),
                selected_story_setup_id=(
                    snapshot.selected_story_setup.id if snapshot.selected_story_setup else None
                ),
                active_composition_job_id=(
                    snapshot.active_composition_job.id if snapshot.active_composition_job else None
                ),
                active_composition_job_status=(
                    JobStatus(snapshot.active_composition_job.status)
                    if snapshot.active_composition_job is not None
                    else None
                ),
                active_audio_job_id=snapshot.active_audio_job.id if snapshot.active_audio_job else None,
                active_audio_job_status=(
                    JobStatus(snapshot.active_audio_job.status)
                    if snapshot.active_audio_job is not None
                    else None
                ),
                ready_story_asset_kinds=ready_story_asset_kinds,
                ready_audio_asset_kinds=ready_audio_asset_kinds,
            )


    class SessionActionPolicyService:
        def __init__(self, session: Session):
            self._session = session
            self._sessions = SessionService(session)

        def evaluate_request(
            self,
            session_id: str,
            *,
            request: SessionActionPolicyEvaluationRequest,
        ) -> SessionActionPolicyEvaluation:
            snapshot = self._sessions.load_session_snapshot(session_id)
            return self.evaluate_request_against_snapshot(snapshot, request=request)

        def evaluate_request_against_snapshot(
            self,
            snapshot: SessionSnapshot,
            *,
            request: SessionActionPolicyEvaluationRequest,
        ) -> SessionActionPolicyEvaluation:
            state = _PolicyState.from_snapshot(
                snapshot,
                ready_story_asset_kinds=self._load_ready_story_asset_kinds(snapshot.id),
                ready_audio_asset_kinds=self._load_ready_audio_asset_kinds(snapshot.id),
            )
            evaluated_actions: list[SessionActionPolicyEvaluationItem] = []

            for action_index, request_item in enumerate(request.actions):
                computed = self._evaluate_action(
                    snapshot.id,
                    state,
                    request_item.action,
                    confirmation_granted=request_item.confirmation_granted,
                )
                evaluation_item = SessionActionPolicyEvaluationItem(
                    action_index=action_index,
                    action_type=request_item.action.action_type,
                    target_stage=request_item.action.target_stage,
                    decision=computed.decision,
                    summary=_build_decision_summary(
                        request_item.action,
                        decision=computed.decision,
                        reasons=computed.reasons,
                        side_effects=computed.side_effects,
                    ),
                    reasons=computed.reasons,
                    side_effects=computed.side_effects,
                    prerequisite_action_types=computed.prerequisite_action_types,
                )
                evaluated_actions.append(evaluation_item)

                if computed.decision in {
                    SessionActionDecision.ACCEPTED,
                    SessionActionDecision.ACCEPTED_WITH_SIDE_EFFECTS,
                }:
                    self._apply_action_to_state(state, request_item.action, computed.resolution)

            return SessionActionPolicyEvaluation(
                session_id=snapshot.id,
                evaluated_actions=evaluated_actions,
            )

        def evaluate_proposed_actions(
            self,
            session_id: str,
            *,
            batch: ChatToUIActionBatch,
        ) -> SessionActionPolicyEvaluation:
            return self.evaluate_request(
                session_id,
                request=build_action_policy_request_from_batch(batch),
            )

        def _evaluate_action(
            self,
            session_id: str,
            state: _PolicyState,
            action: ChatToUIAction,
            *,
            confirmation_granted: bool,
        ) -> _ComputedDecision:
            if action.action_type == ChatToUIActionType.NAVIGATE_TO_STAGE:
                return _accept()

            if action.action_type == ChatToUIActionType.SELECT_GENRE:
                return self._evaluate_select_genre(
                    action,
                    state,
                    confirmation_granted=confirmation_granted,
                )
            if action.action_type == ChatToUIActionType.SELECT_TONE:
                return self._evaluate_select_tone(
                    action,
                    state,
                    confirmation_granted=confirmation_granted,
                )
            if action.action_type == ChatToUIActionType.UPDATE_STORY_BRIEF:
                return self._evaluate_update_story_brief(
                    action,
                    state,
                    confirmation_granted=confirmation_granted,
                )
            if action.action_type == ChatToUIActionType.REGENERATE_PITCHES:
                return self._evaluate_regenerate_pitches(
                    action,
                    state,
                    confirmation_granted=confirmation_granted,
                )
            if action.action_type == ChatToUIActionType.SELECT_PITCH:
                return self._evaluate_select_pitch(
                    session_id,
                    action,
                    state,
                    confirmation_granted=confirmation_granted,
                )
            if action.action_type == ChatToUIActionType.SELECT_CHARACTER_SHEET:
                return self._evaluate_select_character_sheet(
                    session_id,
                    action,
                    state,
                    confirmation_granted=confirmation_granted,
                )
            if action.action_type == ChatToUIActionType.REFINE_CHARACTER_SHEET:
                return self._evaluate_refine_character_sheet(
                    action,
                    state,
                    confirmation_granted=confirmation_granted,
                )
            if action.action_type == ChatToUIActionType.REGENERATE_CHARACTER_SHEET:
                return self._evaluate_regenerate_character_sheet(
                    action,
                    state,
                    confirmation_granted=confirmation_granted,
                )
            if action.action_type == ChatToUIActionType.ACCEPT_BEAT_SHEET:
                return self._evaluate_accept_beat_sheet(
                    session_id,
                    action,
                    state,
                    confirmation_granted=confirmation_granted,
                )
            if action.action_type == ChatToUIActionType.REFINE_BEAT_SHEET:
                return self._evaluate_refine_beat_sheet(
                    action,
                    state,
                    confirmation_granted=confirmation_granted,
                )
            if action.action_type == ChatToUIActionType.REGENERATE_BEAT_SHEET:
                return self._evaluate_regenerate_beat_sheet(
                    action,
                    state,
                    confirmation_granted=confirmation_granted,
                )
            if action.action_type == ChatToUIActionType.UPDATE_STORY_SETUP:
                return self._evaluate_update_story_setup(
                    action,
                    state,
                    confirmation_granted=confirmation_granted,
                )
            if action.action_type == ChatToUIActionType.START_COMPOSITION:
                return self._evaluate_start_composition(
                    action,
                    state,
                    confirmation_granted=confirmation_granted,
                )
            if action.action_type == ChatToUIActionType.PAUSE_JOB:
                return self._evaluate_pause_job(
                    action,
                    state,
                    confirmation_granted=confirmation_granted,
                )
            if action.action_type == ChatToUIActionType.RESUME_JOB:
                return self._evaluate_resume_job(
                    action,
                    state,
                    confirmation_granted=confirmation_granted,
                )
            if action.action_type == ChatToUIActionType.REDIRECT_COMPOSITION:
                return self._evaluate_redirect_composition(
                    action,
                    state,
                    confirmation_granted=confirmation_granted,
                )
            if action.action_type == ChatToUIActionType.UPDATE_AUDIO_SETTINGS:
                return self._evaluate_update_audio_settings(
                    action,
                    state,
                    confirmation_granted=confirmation_granted,
                )
            if action.action_type == ChatToUIActionType.START_AUDIO_GENERATION:
                return self._evaluate_start_audio_generation(
                    action,
                    state,
                    confirmation_granted=confirmation_granted,
                )
            if action.action_type == ChatToUIActionType.OPEN_FINALIZE_VIEW:
                return self._evaluate_open_finalize_view(action, state)
            if action.action_type == ChatToUIActionType.DOWNLOAD_ASSET:
                return self._evaluate_download_asset(action, state)

            raise SessionActionPolicyServiceError(f"unsupported action type {action.action_type!r}")

## Command Started

- Time: `2026-04-01T07:31:40-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `35`
- Summary: in progress: /bin/zsh -lc "sed -n '1,320p' backend/app/worker/default_handlers.py"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,320p' backend/app/worker/default_handlers.py"
    Status: in progress

## Command Started

- Time: `2026-04-01T07:31:40-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `36`
- Summary: in progress: /bin/zsh -lc "sed -n '1,260p' backend/app/worker/registry.py"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,260p' backend/app/worker/registry.py"
    Status: in progress

## Command Finished

- Time: `2026-04-01T07:31:40-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `37`
- Summary: completed, exit 0: /bin/zsh -lc "sed -n '1,260p' backend/app/worker/registry.py"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,260p' backend/app/worker/registry.py"
    Status: completed
    Exit code: 0
    Output:
    from __future__ import annotations

    from collections.abc import Callable
    from typing import Any

    JobHandler = Callable[[dict[str, Any] | list[Any] | None, Any], dict[str, Any] | list[Any] | None]


    class JobHandlerRegistry:
        def __init__(self) -> None:
            self._handlers: dict[str, JobHandler] = {}

        def register(self, job_type: str, handler: JobHandler) -> None:
            normalized_type = job_type.strip()
            if not normalized_type:
                raise ValueError("job_type must not be empty")
            if normalized_type in self._handlers:
                raise ValueError(f"job_type {normalized_type!r} is already registered")

            self._handlers[normalized_type] = handler

        def get(self, job_type: str) -> JobHandler | None:
            return self._handlers.get(job_type)

        def registered_job_types(self) -> tuple[str, ...]:
            return tuple(sorted(self._handlers))

## Command Finished

- Time: `2026-04-01T07:31:40-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `38`
- Summary: completed, exit 0: /bin/zsh -lc "sed -n '1,320p' backend/app/worker/default_handlers.py"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,320p' backend/app/worker/default_handlers.py"
    Status: completed
    Exit code: 0
    Output:
    from __future__ import annotations

    import time
    from typing import Any

    from app.worker.registry import JobHandlerRegistry
    from app.worker.runtime import JobExecutionContext


    def build_default_job_handler_registry() -> JobHandlerRegistry:
        registry = JobHandlerRegistry()
        registry.register("demo.echo", demo_echo_handler)
        return registry


    def demo_echo_handler(
        payload: dict[str, Any] | list[Any] | None,
        context: JobExecutionContext,
    ) -> dict[str, Any]:
        payload_dict = payload if isinstance(payload, dict) else {}
        step_count = max(int(payload_dict.get("steps", 1)), 1)
        step_delay_seconds = max(float(payload_dict.get("step_delay_seconds", 0)), 0.0)

        for _ in range(step_count):
            if step_delay_seconds > 0:
                time.sleep(step_delay_seconds)
            context.heartbeat()

        return {
            "echo": payload_dict.get("message", payload),
            "step_count": step_count,
            "worker_id": context.worker_id,
        }

## Command Started

- Time: `2026-04-01T07:31:52-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `39`
- Summary: in progress: /bin/zsh -lc "sed -n '1,360p' backend/tests/test_chat_action_contracts.py"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,360p' backend/tests/test_chat_action_contracts.py"
    Status: in progress

## Command Started

- Time: `2026-04-01T07:31:52-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `40`
- Summary: in progress: /bin/zsh -lc "sed -n '1,360p' backend/tests/test_intent_parser_service.py"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,360p' backend/tests/test_intent_parser_service.py"
    Status: in progress

## Command Started

- Time: `2026-04-01T07:31:52-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `41`
- Summary: in progress: /bin/zsh -lc "sed -n '320,760p' backend/app/models/chat_actions.py"

### Full Text

    Command: /bin/zsh -lc "sed -n '320,760p' backend/app/models/chat_actions.py"
    Status: in progress

## Command Started

- Time: `2026-04-01T07:31:52-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `42`
- Summary: in progress: /bin/zsh -lc "sed -n '360,760p' backend/app/services/action_policy.py"

### Full Text

    Command: /bin/zsh -lc "sed -n '360,760p' backend/app/services/action_policy.py"
    Status: in progress

## Command Finished

- Time: `2026-04-01T07:31:52-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `43`
- Summary: completed, exit 0: /bin/zsh -lc "sed -n '1,360p' backend/tests/test_chat_action_contracts.py"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,360p' backend/tests/test_chat_action_contracts.py"
    Status: completed
    Exit code: 0
    Output:
    from __future__ import annotations

    import json
    from pathlib import Path

    import pytest
    from app.models import (
        ChatToUIActionBatch,
        ChatToUIActionDefaultPolicy,
        ChatToUIActionType,
        RefineBeatSheetAction,
        SelectGenreAction,
        UpdateAudioSettingsAction,
        get_chat_to_ui_action_default_policy,
        get_chat_to_ui_action_schema_bundle,
    )
    from pydantic import ValidationError


    def test_chat_to_ui_action_contract_supports_stage_specific_actions() -> None:
        batch = ChatToUIActionBatch.model_validate(
            {
                "schema_version": 1,
                "actions": [
                    {
                        "schema_version": 1,
                        "action_type": "select_genre",
                        "target_stage": "genre",
                        "confidence": 0.98,
                        "rationale": "The user explicitly named a catalog genre.",
                        "requires_confirmation": True,
                        "extracted_values": {
                            "genre_slug": "quest-fantasy",
                        },
                    },
                    {
                        "schema_version": 1,
                        "action_type": "refine_beat_sheet",
                        "target_stage": "beats",
                        "confidence": 0.84,
                        "rationale": "The user asked to soften the midpoint tension.",
                        "requires_confirmation": True,
                        "extracted_values": {
                            "instructions": (
                                "Soften the midpoint and make the emotional repair clearer."
                            ),
                            "beat_names": ["Midpoint", "All Is Lost"],
                        },
                    },
                    {
                        "schema_version": 1,
                        "action_type": "update_audio_settings",
                        "target_stage": "audio",
                        "confidence": 0.71,
                        "rationale": "The message requested slower narration with no music.",
                        "requires_confirmation": False,
                        "extracted_values": {
                            "playback_speed": 0.9,
                            "include_background_music": False,
                        },
                    },
                ],
            }
        )

        assert len(batch.actions) == 3
        assert isinstance(batch.actions[0], SelectGenreAction)
        assert isinstance(batch.actions[1], RefineBeatSheetAction)
        assert isinstance(batch.actions[2], UpdateAudioSettingsAction)
        assert batch.actions[2].extracted_values.playback_speed == 0.9


    def test_chat_to_ui_action_contract_rejects_confirm_first_actions_without_confirmation() -> None:
        with pytest.raises(
            ValidationError,
            match="select_genre must require confirmation under the default policy",
        ):
            ChatToUIActionBatch.model_validate(
                {
                    "schema_version": 1,
                    "actions": [
                        {
                            "schema_version": 1,
                            "action_type": "select_genre",
                            "target_stage": "genre",
                            "confidence": 0.92,
                            "requires_confirmation": False,
                            "extracted_values": {
                                "genre_label": "Quest Fantasy",
                            },
                        }
                    ],
                }
            )


    def test_chat_to_ui_action_contract_rejects_missing_structured_values() -> None:
        with pytest.raises(
            ValidationError,
            match="update_story_setup requires at least one structured planning preference",
        ):
            ChatToUIActionBatch.model_validate(
                {
                    "schema_version": 1,
                    "actions": [
                        {
                            "schema_version": 1,
                            "action_type": "update_story_setup",
                            "target_stage": "story_setup",
                            "confidence": 0.61,
                            "requires_confirmation": False,
                            "extracted_values": {},
                        }
                    ],
                }
            )


    def test_chat_to_ui_action_contract_rejects_job_stage_mismatch() -> None:
        with pytest.raises(
            ValidationError,
            match="pause_job target_stage must match the extracted job_kind",
        ):
            ChatToUIActionBatch.model_validate(
                {
                    "schema_version": 1,
                    "actions": [
                        {
                            "schema_version": 1,
                            "action_type": "pause_job",
                            "target_stage": "audio",
                            "confidence": 0.89,
                            "requires_confirmation": True,
                            "extracted_values": {
                                "job_kind": "composition",
                            },
                        }
                    ],
                }
            )


    def test_default_policy_mapping_is_stable_for_auto_apply_and_confirm_first() -> None:
        assert (
            get_chat_to_ui_action_default_policy(ChatToUIActionType.SELECT_PITCH)
            == ChatToUIActionDefaultPolicy.CONFIRM_FIRST
        )
        assert (
            get_chat_to_ui_action_default_policy(ChatToUIActionType.OPEN_FINALIZE_VIEW)
            == ChatToUIActionDefaultPolicy.AUTO_APPLY_CANDIDATE
        )


    def test_chat_to_ui_action_schema_bundle_matches_checked_in_schema_file() -> None:
        schema_path = Path(__file__).resolve().parents[2] / "docs" / "chat-to-ui-actions.schema.json"

        assert json.loads(schema_path.read_text()) == get_chat_to_ui_action_schema_bundle()

## Command Finished

- Time: `2026-04-01T07:31:52-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `44`
- Summary: completed, exit 0: /bin/zsh -lc "sed -n '1,360p' backend/tests/test_intent_parser_service.py"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,360p' backend/tests/test_intent_parser_service.py"
    Status: completed
    Exit code: 0
    Output:
    from __future__ import annotations

    from datetime import datetime, timezone

    import pytest
    from app.ai import IntentParserTransportError
    from app.db import Base, Genre, StoryBrief, StorySession, ToneProfile, make_engine
    from app.models import (
        ChatToUIActionType,
        IntentParserStatus,
        IntentParserStructuredOutput,
        SessionActionDecision,
        SessionContextUpdateRequest,
        SessionEventType,
        WorkflowStage,
        WorkflowStageState,
    )
    from app.services import SessionEventLogService, SessionIntentParserService, SessionService
    from sqlalchemy.orm import sessionmaker


    def _enable_sqlite_foreign_keys(engine) -> None:
        with engine.begin() as connection:
            connection.exec_driver_sql("PRAGMA foreign_keys=ON")


    @pytest.fixture
    def db_session():
        engine = make_engine("sqlite+pysqlite:///:memory:")
        _enable_sqlite_foreign_keys(engine)
        Base.metadata.create_all(engine)
        session = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)()

        try:
            yield session
        finally:
            session.close()
            engine.dispose()


    class StubIntentParserAdapter:
        def __init__(self, structured_output: IntentParserStructuredOutput) -> None:
            self.model_id = "gemini-3.1-flash-lite"
            self._structured_output = structured_output
            self.invocations = []

        def parse(self, invocation):
            from app.models import IntentParserInvocationResult

            self.invocations.append(invocation)
            return IntentParserInvocationResult(
                invocation=invocation,
                structured_output=self._structured_output,
                raw_response={"mock": "response"},
            )

        def close(self) -> None:
            return None


    class RaisingIntentParserAdapter:
        model_id = "gemini-3.1-flash-lite"

        def parse(self, invocation):
            raise IntentParserTransportError("network timeout")

        def close(self) -> None:
            return None


    def test_intent_parser_service_handles_happy_path_updates_and_audits_events(db_session) -> None:
        session_id = _create_beats_session(db_session)
        adapter = StubIntentParserAdapter(
            IntentParserStructuredOutput.model_validate(
                {
                    "schema_version": 1,
                    "status": "parsed",
                    "needs_clarification": False,
                    "assistant_response": (
                        "I can make the beat sheet moodier and shorten the planned runtime."
                    ),
                    "proposed_actions": {
                        "schema_version": 1,
                        "actions": [
                            {
                                "action_type": "refine_beat_sheet",
                                "target_stage": "beats",
                                "confidence": 0.88,
                                "rationale": "The user asked for a more mysterious story shape.",
                                "requires_confirmation": True,
                                "extracted_values": {
                                    "instructions": (
                                        "Make the midpoint and mystery beats feel "
                                        "a little more mysterious."
                                    ),
                                    "bedtime_goal": (
                                        "Keep the tension gentle and resolve it quickly."
                                    ),
                                },
                            },
                            {
                                "action_type": "update_story_setup",
                                "target_stage": "story_setup",
                                "confidence": 0.84,
                                "rationale": "The user asked for a shorter story.",
                                "requires_confirmation": False,
                                "extracted_values": {
                                    "target_runtime_minutes": 8,
                                    "guidance_notes": "Aim for a slightly shorter read-aloud.",
                                },
                            },
                        ],
                    },
                }
            )
        )

        service = SessionIntentParserService(db_session, adapter)
        result = service.parse_user_message(
            session_id,
            message="make it a little more mysterious and shorter",
        )

        assert result.status == IntentParserStatus.PARSED
        assert [action.action_type for action in result.proposed_actions.actions] == [
            ChatToUIActionType.REFINE_BEAT_SHEET,
            ChatToUIActionType.UPDATE_STORY_SETUP,
        ]
        assert result.policy_evaluation is not None
        assert [item.decision for item in result.policy_evaluation.evaluated_actions] == [
            SessionActionDecision.REJECTED,
            SessionActionDecision.REJECTED,
        ]
        assert adapter.invocations
        assert '"current_stage": "beats"' in adapter.invocations[0].rendered_prompt
        assert "Selected tone: Hushed Wonder" in adapter.invocations[0].rendered_prompt

        history = SessionEventLogService(db_session).list_session_history(session_id)

        assert history.events[-3].event_type == SessionEventType.CHAT_MESSAGE_RECORDED
        assert history.events[-2].event_type == SessionEventType.CHAT_INTENT_PARSED
        assert history.events[-2].payload is not None
        assert history.events[-2].payload.result.status == IntentParserStatus.PARSED
        assert history.events[-2].payload.result.proposed_actions.actions[1].action_type == (
            ChatToUIActionType.UPDATE_STORY_SETUP
        )
        assert history.events[-1].event_type == SessionEventType.CHAT_MESSAGE_RECORDED
        assert history.events[-1].payload is not None
        assert history.events[-1].payload.message_role == "assistant"


    def test_intent_parser_service_requests_clarification_for_vague_message(db_session) -> None:
        session_id = _create_beats_session(db_session)
        adapter = StubIntentParserAdapter(
            IntentParserStructuredOutput.model_validate(
                {
                    "schema_version": 1,
                    "status": "needs_clarification",
                    "needs_clarification": True,
                    "assistant_response": "Do you want the tone, beats, or runtime to change?",
                    "clarification_reason": (
                        "The request does not say which part of the session to adjust."
                    ),
                    "proposed_actions": {
                        "schema_version": 1,
                        "actions": [],
                    },
                }
            )
        )

        result = SessionIntentParserService(db_session, adapter).parse_user_message(
            session_id,
            message="make it better",
        )

        assert result.status == IntentParserStatus.NEEDS_CLARIFICATION
        assert result.needs_clarification is True
        assert result.proposed_actions.actions == []
        assert "tone, beats, or runtime" in result.assistant_response


    def test_intent_parser_service_falls_back_gracefully_when_adapter_fails(db_session) -> None:
        session_id = _create_beats_session(db_session)
        result = SessionIntentParserService(
            db_session,
            RaisingIntentParserAdapter(),
        ).parse_user_message(
            session_id, message="make it a little more mysterious and shorter"
        )

        assert result.status == IntentParserStatus.FAILED
        assert result.proposed_actions.actions == []
        assert "structured story-studio actions" in result.assistant_response

        history = SessionEventLogService(db_session).list_session_history(session_id)
        assert history.events[-2].event_type == SessionEventType.CHAT_INTENT_PARSED
        assert history.events[-2].payload is not None
        assert history.events[-2].payload.raw_response is None
        assert history.events[-2].payload.result.status == IntentParserStatus.FAILED


    def test_intent_parser_service_uses_updated_ui_context_in_prompt_summary(db_session) -> None:
        session_id = _create_beats_session(db_session)
        session_service = SessionService(db_session)
        session_service.apply_context_update(
            session_id,
            payload=SessionContextUpdateRequest.model_validate({
                "target_kind": "stage_note",
                "stage": "beats",
                "control_id": "stage-note-editor",
                "origin": "workspace",
                "values": {
                    "detail": "Make the midpoint gentler and add one calmer beat before the finale.",
                },
            }),
        )
        adapter = StubIntentParserAdapter(
            IntentParserStructuredOutput.model_validate(
                {
                    "schema_version": 1,
                    "status": "needs_clarification",
                    "needs_clarification": True,
                    "assistant_response": "Do you want me to adjust the beat sheet or story setup?",
                    "clarification_reason": "Need the target workflow stage.",
                    "proposed_actions": {
                        "schema_version": 1,
                        "actions": [],
                    },
                }
            )
        )

        SessionIntentParserService(db_session, adapter).parse_user_message(
            session_id,
            message="make it even softer",
        )

        assert adapter.invocations
        assert "Current beat sheet detail: Make the midpoint gentler" in (
            adapter.invocations[0].rendered_prompt
        )


    def _create_beats_session(db_session) -> str:
        genre = Genre(
            slug="quest-fantasy",
            label="Quest Fantasy",
            description="A gentle adventure with emotional repair.",
        )
        tone = ToneProfile(
            genre=genre,
            slug="hushed-wonder",
            label="Hushed Wonder",
            description="Quiet, luminous, and bedtime-safe.",
        )
        db_session.add_all([genre, tone])
        db_session.flush()

        session_service = SessionService(db_session)
        snapshot = session_service.create_session(working_title="Moonlit Harbor")
        story_session = db_session.get(StorySession, snapshot.id)
        assert story_session is not None
        story_session.selected_genre = genre
        story_session.selected_tone_profile = tone
        db_session.flush()

        for stage in (
            WorkflowStage.GENRE,
            WorkflowStage.TONE,
            WorkflowStage.BRIEF,
            WorkflowStage.PITCHES,
            WorkflowStage.CHARACTERS,
        ):
            session_service.update_stage_state(
                snapshot.id,
                stage=stage,
                status=WorkflowStageState.COMPLETED,
            )

        session_service.update_stage_state(
            snapshot.id,
            stage=WorkflowStage.BEATS,
            status=WorkflowStageState.IN_PROGRESS,
            detail="Refining the midpoint tension.",
        )
        db_session.add(
            StoryBrief(
                session_id=snapshot.id,
                revision_number=1,
                raw_brief="A harbor fox follows a moonlit clue across the docks.",
                normalized_summary="A sleepy harbor mystery that resolves gently before bedtime.",
                planning_notes="Keep every surprise reassuring.",
                is_active=True,
                accepted_at=datetime.now(timezone.utc),
            )
        )
        db_session.commit()
        return snapshot.id

## Command Finished

- Time: `2026-04-01T07:31:52-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `45`
- Summary: completed, exit 0: /bin/zsh -lc "sed -n '320,760p' backend/app/models/chat_actions.py"

### Full Text

    Command: /bin/zsh -lc "sed -n '320,760p' backend/app/models/chat_actions.py"
    Status: completed
    Exit code: 0
    Output:
    "update_audio_settings requires at least one audio setting or guidance note"
                ),
            )
            return self


    class StartAudioGenerationValues(ChatToUIExtractedValues):
        voice_key: str | None = Field(default=None, min_length=1)
        playback_speed: float | None = Field(default=None, ge=0.5, le=2.0)
        include_background_music: bool | None = None
        music_profile: str | None = Field(default=None, min_length=1)
        regenerate_existing_audio: bool = False


    class OpenFinalizeViewValues(ChatToUIExtractedValues):
        view: FinalizeView


    class DownloadAssetValues(ChatToUIExtractedValues):
        asset_kind: DownloadAssetKind


    class ChatToUIActionBase(ChatToUIModel):
        action_type: ChatToUIActionType
        target_stage: WorkflowStage
        confidence: float = Field(ge=0, le=1)
        rationale: str | None = Field(default=None, min_length=1)
        requires_confirmation: bool

        @model_validator(mode="after")
        def validate_confirmation_requirement(self) -> ChatToUIActionBase:
            if (
                get_chat_to_ui_action_default_policy(self.action_type)
                == ChatToUIActionDefaultPolicy.CONFIRM_FIRST
                and not self.requires_confirmation
            ):
                raise ValueError(
                    f"{self.action_type.value} must require confirmation under the default policy"
                )

            return self


    class NavigateToStageAction(ChatToUIActionBase):
        action_type: Literal[ChatToUIActionType.NAVIGATE_TO_STAGE] = (
            ChatToUIActionType.NAVIGATE_TO_STAGE
        )
        target_stage: WorkflowStage
        extracted_values: ChatToUIExtractedValues = Field(default_factory=ChatToUIExtractedValues)


    class SelectGenreAction(ChatToUIActionBase):
        action_type: Literal[ChatToUIActionType.SELECT_GENRE] = ChatToUIActionType.SELECT_GENRE
        target_stage: Literal[WorkflowStage.GENRE] = WorkflowStage.GENRE
        extracted_values: SelectGenreValues


    class SelectToneAction(ChatToUIActionBase):
        action_type: Literal[ChatToUIActionType.SELECT_TONE] = ChatToUIActionType.SELECT_TONE
        target_stage: Literal[WorkflowStage.TONE] = WorkflowStage.TONE
        extracted_values: SelectToneValues


    class UpdateStoryBriefAction(ChatToUIActionBase):
        action_type: Literal[ChatToUIActionType.UPDATE_STORY_BRIEF] = (
            ChatToUIActionType.UPDATE_STORY_BRIEF
        )
        target_stage: Literal[WorkflowStage.BRIEF] = WorkflowStage.BRIEF
        extracted_values: UpdateStoryBriefValues


    class RegeneratePitchesAction(ChatToUIActionBase):
        action_type: Literal[ChatToUIActionType.REGENERATE_PITCHES] = (
            ChatToUIActionType.REGENERATE_PITCHES
        )
        target_stage: Literal[WorkflowStage.PITCHES] = WorkflowStage.PITCHES
        extracted_values: RegeneratePitchesValues = Field(default_factory=RegeneratePitchesValues)


    class SelectPitchAction(ChatToUIActionBase):
        action_type: Literal[ChatToUIActionType.SELECT_PITCH] = ChatToUIActionType.SELECT_PITCH
        target_stage: Literal[WorkflowStage.PITCHES] = WorkflowStage.PITCHES
        extracted_values: SelectPitchValues


    class SelectCharacterSheetAction(ChatToUIActionBase):
        action_type: Literal[ChatToUIActionType.SELECT_CHARACTER_SHEET] = (
            ChatToUIActionType.SELECT_CHARACTER_SHEET
        )
        target_stage: Literal[WorkflowStage.CHARACTERS] = WorkflowStage.CHARACTERS
        extracted_values: SelectCharacterSheetValues


    class RefineCharacterSheetAction(ChatToUIActionBase):
        action_type: Literal[ChatToUIActionType.REFINE_CHARACTER_SHEET] = (
            ChatToUIActionType.REFINE_CHARACTER_SHEET
        )
        target_stage: Literal[WorkflowStage.CHARACTERS] = WorkflowStage.CHARACTERS
        extracted_values: RefineCharacterSheetValues


    class RegenerateCharacterSheetAction(ChatToUIActionBase):
        action_type: Literal[ChatToUIActionType.REGENERATE_CHARACTER_SHEET] = (
            ChatToUIActionType.REGENERATE_CHARACTER_SHEET
        )
        target_stage: Literal[WorkflowStage.CHARACTERS] = WorkflowStage.CHARACTERS
        extracted_values: RegenerateCharacterSheetValues = Field(
            default_factory=RegenerateCharacterSheetValues
        )


    class AcceptBeatSheetAction(ChatToUIActionBase):
        action_type: Literal[ChatToUIActionType.ACCEPT_BEAT_SHEET] = (
            ChatToUIActionType.ACCEPT_BEAT_SHEET
        )
        target_stage: Literal[WorkflowStage.BEATS] = WorkflowStage.BEATS
        extracted_values: AcceptBeatSheetValues


    class RefineBeatSheetAction(ChatToUIActionBase):
        action_type: Literal[ChatToUIActionType.REFINE_BEAT_SHEET] = (
            ChatToUIActionType.REFINE_BEAT_SHEET
        )
        target_stage: Literal[WorkflowStage.BEATS] = WorkflowStage.BEATS
        extracted_values: RefineBeatSheetValues


    class RegenerateBeatSheetAction(ChatToUIActionBase):
        action_type: Literal[ChatToUIActionType.REGENERATE_BEAT_SHEET] = (
            ChatToUIActionType.REGENERATE_BEAT_SHEET
        )
        target_stage: Literal[WorkflowStage.BEATS] = WorkflowStage.BEATS
        extracted_values: RegenerateBeatSheetValues = Field(default_factory=RegenerateBeatSheetValues)


    class UpdateStorySetupAction(ChatToUIActionBase):
        action_type: Literal[ChatToUIActionType.UPDATE_STORY_SETUP] = (
            ChatToUIActionType.UPDATE_STORY_SETUP
        )
        target_stage: Literal[WorkflowStage.STORY_SETUP] = WorkflowStage.STORY_SETUP
        extracted_values: UpdateStorySetupValues


    class StartCompositionAction(ChatToUIActionBase):
        action_type: Literal[ChatToUIActionType.START_COMPOSITION] = (
            ChatToUIActionType.START_COMPOSITION
        )
        target_stage: Literal[WorkflowStage.COMPOSITION] = WorkflowStage.COMPOSITION
        extracted_values: StartCompositionValues = Field(default_factory=StartCompositionValues)


    class PauseJobAction(ChatToUIActionBase):
        action_type: Literal[ChatToUIActionType.PAUSE_JOB] = ChatToUIActionType.PAUSE_JOB
        target_stage: Literal[WorkflowStage.COMPOSITION, WorkflowStage.AUDIO]
        extracted_values: JobControlValues

        @model_validator(mode="after")
        def validate_stage_matches_job_kind(self) -> PauseJobAction:
            expected_stage = (
                WorkflowStage.COMPOSITION
                if self.extracted_values.job_kind == ChatToUIJobKind.COMPOSITION
                else WorkflowStage.AUDIO
            )
            if self.target_stage != expected_stage:
                raise ValueError("pause_job target_stage must match the extracted job_kind")

            return self


    class ResumeJobAction(ChatToUIActionBase):
        action_type: Literal[ChatToUIActionType.RESUME_JOB] = ChatToUIActionType.RESUME_JOB
        target_stage: Literal[WorkflowStage.COMPOSITION, WorkflowStage.AUDIO]
        extracted_values: JobControlValues

        @model_validator(mode="after")
        def validate_stage_matches_job_kind(self) -> ResumeJobAction:
            expected_stage = (
                WorkflowStage.COMPOSITION
                if self.extracted_values.job_kind == ChatToUIJobKind.COMPOSITION
                else WorkflowStage.AUDIO
            )
            if self.target_stage != expected_stage:
                raise ValueError("resume_job target_stage must match the extracted job_kind")

            return self


    class RedirectCompositionAction(ChatToUIActionBase):
        action_type: Literal[ChatToUIActionType.REDIRECT_COMPOSITION] = (
            ChatToUIActionType.REDIRECT_COMPOSITION
        )
        target_stage: Literal[WorkflowStage.COMPOSITION] = WorkflowStage.COMPOSITION
        extracted_values: RedirectCompositionValues


    class UpdateAudioSettingsAction(ChatToUIActionBase):
        action_type: Literal[ChatToUIActionType.UPDATE_AUDIO_SETTINGS] = (
            ChatToUIActionType.UPDATE_AUDIO_SETTINGS
        )
        target_stage: Literal[WorkflowStage.AUDIO] = WorkflowStage.AUDIO
        extracted_values: UpdateAudioSettingsValues


    class StartAudioGenerationAction(ChatToUIActionBase):
        action_type: Literal[ChatToUIActionType.START_AUDIO_GENERATION] = (
            ChatToUIActionType.START_AUDIO_GENERATION
        )
        target_stage: Literal[WorkflowStage.AUDIO] = WorkflowStage.AUDIO
        extracted_values: StartAudioGenerationValues = Field(default_factory=StartAudioGenerationValues)


    class OpenFinalizeViewAction(ChatToUIActionBase):
        action_type: Literal[ChatToUIActionType.OPEN_FINALIZE_VIEW] = (
            ChatToUIActionType.OPEN_FINALIZE_VIEW
        )
        target_stage: Literal[WorkflowStage.FINALIZE] = WorkflowStage.FINALIZE
        extracted_values: OpenFinalizeViewValues


    class DownloadAssetAction(ChatToUIActionBase):
        action_type: Literal[ChatToUIActionType.DOWNLOAD_ASSET] = ChatToUIActionType.DOWNLOAD_ASSET
        target_stage: Literal[WorkflowStage.FINALIZE] = WorkflowStage.FINALIZE
        extracted_values: DownloadAssetValues


    ChatToUIAction: TypeAlias = Annotated[
        NavigateToStageAction
        | SelectGenreAction
        | SelectToneAction
        | UpdateStoryBriefAction
        | RegeneratePitchesAction
        | SelectPitchAction
        | SelectCharacterSheetAction
        | RefineCharacterSheetAction
        | RegenerateCharacterSheetAction
        | AcceptBeatSheetAction
        | RefineBeatSheetAction
        | RegenerateBeatSheetAction
        | UpdateStorySetupAction
        | StartCompositionAction
        | PauseJobAction
        | ResumeJobAction
        | RedirectCompositionAction
        | UpdateAudioSettingsAction
        | StartAudioGenerationAction
        | OpenFinalizeViewAction
        | DownloadAssetAction,
        Field(discriminator="action_type"),
    ]


    class ChatToUIActionBatch(ChatToUIModel):
        actions: list[ChatToUIAction] = Field(default_factory=list)


    def get_chat_to_ui_action_schema_bundle() -> dict[str, Any]:
        return {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "bundle_schema_version": CHAT_TO_UI_ACTION_SCHEMA_VERSION,
            "workflow_stages": [stage.value for stage in WORKFLOW_STAGE_SEQUENCE],
            "default_policy_by_action": {
                action_type.value: policy.value
                for action_type, policy in DEFAULT_CHAT_TO_UI_ACTION_POLICIES.items()
            },
            "schemas": {
                "chat_to_ui_action": TypeAdapter(ChatToUIAction).json_schema(),
                "chat_to_ui_action_batch": ChatToUIActionBatch.model_json_schema(),
            },
        }

## Command Finished

- Time: `2026-04-01T07:31:52-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `46`
- Summary: completed, exit 0: /bin/zsh -lc "sed -n '360,760p' backend/app/services/action_policy.py"

### Full Text

    Command: /bin/zsh -lc "sed -n '360,760p' backend/app/services/action_policy.py"
    Status: completed
    Exit code: 0
    Output:
    raise SessionActionPolicyServiceError(f"unsupported action type {action.action_type!r}")

        def _evaluate_select_genre(
            self,
            action: SelectGenreAction,
            state: _PolicyState,
            *,
            confirmation_granted: bool,
        ) -> _ComputedDecision:
            genre_matches = self._find_genres(action)
            if len(genre_matches) > 1:
                return _reject(
                    SessionActionReasonCode.CATALOG_ENTRY_AMBIGUOUS,
                    "More than one active genre matched that request.",
                    stage=WorkflowStage.GENRE,
                )
            if not genre_matches:
                return _reject(
                    SessionActionReasonCode.CATALOG_ENTRY_NOT_FOUND,
                    "No active genre matched that request.",
                    stage=WorkflowStage.GENRE,
                )

            genre = genre_matches[0]
            if (
                state.selected_genre_id == genre.id
                and state.stage_statuses.get(WorkflowStage.GENRE)
                != WorkflowStageState.NEEDS_REGENERATION
            ):
                return _accept(
                    reasons=[
                        _reason(
                            SessionActionReasonCode.ACTION_IS_NOOP,
                            f"{genre.label} is already the selected genre.",
                            stage=WorkflowStage.GENRE,
                        )
                    ],
                    resolution=_ResolvedAction(genre=genre),
                )

            side_effects = self._build_stage_edit_side_effects(
                state,
                WorkflowStage.GENRE,
                clear_tone_selection=(
                    state.selected_tone_profile_id is not None and state.selected_genre_id != genre.id
                ),
            )
            return self._finalize_change_action(
                action,
                side_effects=side_effects,
                confirmation_granted=confirmation_granted,
                resolution=_ResolvedAction(genre=genre),
            )

        def _evaluate_select_tone(
            self,
            action: SelectToneAction,
            state: _PolicyState,
            *,
            confirmation_granted: bool,
        ) -> _ComputedDecision:
            if state.selected_genre_id is None:
                return _reject(
                    SessionActionReasonCode.PREREQUISITE_SELECTION_MISSING,
                    "Select a genre before choosing a tone.",
                    stage=WorkflowStage.TONE,
                    prerequisite_action_types=[ChatToUIActionType.SELECT_GENRE],
                )

            tone_matches = self._find_tones(action, genre_id=state.selected_genre_id)
            if len(tone_matches) > 1:
                return _reject(
                    SessionActionReasonCode.CATALOG_ENTRY_AMBIGUOUS,
                    "More than one tone profile matched that request for the current genre.",
                    stage=WorkflowStage.TONE,
                )
            if not tone_matches:
                return _reject(
                    SessionActionReasonCode.CATALOG_ENTRY_NOT_FOUND,
                    "No active tone profile matched that request for the current genre.",
                    stage=WorkflowStage.TONE,
                )

            tone = tone_matches[0]
            if (
                state.selected_tone_profile_id == tone.id
                and state.stage_statuses.get(WorkflowStage.TONE)
                != WorkflowStageState.NEEDS_REGENERATION
            ):
                return _accept(
                    reasons=[
                        _reason(
                            SessionActionReasonCode.ACTION_IS_NOOP,
                            f"{tone.label} is already the selected tone.",
                            stage=WorkflowStage.TONE,
                        )
                    ],
                    resolution=_ResolvedAction(tone=tone),
                )

            blocked = _blocked_prerequisite_stages(state, WorkflowStage.TONE)
            if blocked:
                return _reject_for_blocked_stages(blocked, target_stage=WorkflowStage.TONE)

            side_effects = self._build_stage_edit_side_effects(state, WorkflowStage.TONE)
            return self._finalize_change_action(
                action,
                side_effects=side_effects,
                confirmation_granted=confirmation_granted,
                resolution=_ResolvedAction(tone=tone),
            )

        def _evaluate_update_story_brief(
            self,
            action: UpdateStoryBriefAction,
            state: _PolicyState,
            *,
            confirmation_granted: bool,
        ) -> _ComputedDecision:
            blocked = _blocked_prerequisite_stages(state, WorkflowStage.BRIEF)
            if blocked:
                return _reject_for_blocked_stages(blocked, target_stage=WorkflowStage.BRIEF)

            side_effects = self._build_stage_edit_side_effects(state, WorkflowStage.BRIEF)
            return self._finalize_change_action(
                action,
                side_effects=side_effects,
                confirmation_granted=confirmation_granted,
            )

        def _evaluate_regenerate_pitches(
            self,
            action: RegeneratePitchesAction,
            state: _PolicyState,
            *,
            confirmation_granted: bool,
        ) -> _ComputedDecision:
            blocked = _blocked_prerequisite_stages(state, WorkflowStage.PITCHES)
            if blocked:
                return _reject_for_blocked_stages(blocked, target_stage=WorkflowStage.PITCHES)
            if not state.story_brief_present:
                return _reject(
                    SessionActionReasonCode.PREREQUISITE_SELECTION_MISSING,
                    "Create or accept a story brief before regenerating pitches.",
                    stage=WorkflowStage.PITCHES,
                    prerequisite_action_types=[ChatToUIActionType.UPDATE_STORY_BRIEF],
                )

            side_effects = self._build_stage_edit_side_effects(state, WorkflowStage.PITCHES)
            return self._finalize_change_action(
                action,
                side_effects=side_effects,
                confirmation_granted=confirmation_granted,
            )

        def _evaluate_select_pitch(
            self,
            session_id: str,
            action: SelectPitchAction,
            state: _PolicyState,
            *,
            confirmation_granted: bool,
        ) -> _ComputedDecision:
            blocked = _blocked_prerequisite_stages(state, WorkflowStage.PITCHES)
            if blocked:
                return _reject_for_blocked_stages(blocked, target_stage=WorkflowStage.PITCHES)
            if not state.story_brief_present:
                return _reject(
                    SessionActionReasonCode.PREREQUISITE_SELECTION_MISSING,
                    "Create or accept a story brief before selecting a pitch.",
                    stage=WorkflowStage.PITCHES,
                    prerequisite_action_types=[ChatToUIActionType.UPDATE_STORY_BRIEF],
                )
            if state.stage_statuses.get(WorkflowStage.PITCHES) == WorkflowStageState.NEEDS_REGENERATION:
                return _reject(
                    SessionActionReasonCode.TARGET_STAGE_STALE,
                    (
                        "Generate fresh pitches before selecting one because the current "
                        "pitch set is stale."
                    ),
                    stage=WorkflowStage.PITCHES,
                    prerequisite_action_types=[ChatToUIActionType.REGENERATE_PITCHES],
                )

            pitches = self._find_pitches(session_id, action)
            if len(pitches) > 1:
                return _reject(
                    SessionActionReasonCode.SESSION_RESOURCE_AMBIGUOUS,
                    "More than one pitch matched that request in this session.",
                    stage=WorkflowStage.PITCHES,
                )
            if not pitches:
                return _reject(
                    SessionActionReasonCode.SESSION_RESOURCE_NOT_FOUND,
                    "No pitch matched that request in this session.",
                    stage=WorkflowStage.PITCHES,
                )

            pitch = pitches[0]
            if state.selected_pitch_id == pitch.id:
                return _accept(
                    reasons=[
                        _reason(
                            SessionActionReasonCode.ACTION_IS_NOOP,
                            f"{pitch.title} is already the selected pitch.",
                            stage=WorkflowStage.PITCHES,
                        )
                    ],
                    resolution=_ResolvedAction(pitch=pitch),
                )

            side_effects = self._build_stage_edit_side_effects(state, WorkflowStage.PITCHES)
            return self._finalize_change_action(
                action,
                side_effects=side_effects,
                confirmation_granted=confirmation_granted,
                resolution=_ResolvedAction(pitch=pitch),
            )

        def _evaluate_select_character_sheet(
            self,
            session_id: str,
            action: SelectCharacterSheetAction,
            state: _PolicyState,
            *,
            confirmation_granted: bool,
        ) -> _ComputedDecision:
            blocked = _blocked_prerequisite_stages(state, WorkflowStage.CHARACTERS)
            if blocked:
                return _reject_for_blocked_stages(blocked, target_stage=WorkflowStage.CHARACTERS)
            if state.selected_pitch_id is None:
                return _reject(
                    SessionActionReasonCode.PREREQUISITE_SELECTION_MISSING,
                    "Select a pitch before choosing a character sheet.",
                    stage=WorkflowStage.CHARACTERS,
                    prerequisite_action_types=[ChatToUIActionType.SELECT_PITCH],
                )
            if (
                state.stage_statuses.get(WorkflowStage.CHARACTERS)
                == WorkflowStageState.NEEDS_REGENERATION
            ):
                return _reject(
                    SessionActionReasonCode.TARGET_STAGE_STALE,
                    (
                        "Generate fresh character sheets before selecting one because the "
                        "current set is stale."
                    ),
                    stage=WorkflowStage.CHARACTERS,
                    prerequisite_action_types=[ChatToUIActionType.REGENERATE_CHARACTER_SHEET],
                )

            character_sheets = self._find_character_sheets(session_id, action)
            if len(character_sheets) > 1:
                return _reject(
                    SessionActionReasonCode.SESSION_RESOURCE_AMBIGUOUS,
                    "More than one character sheet matched that request in this session.",
                    stage=WorkflowStage.CHARACTERS,
                )
            if not character_sheets:
                return _reject(
                    SessionActionReasonCode.SESSION_RESOURCE_NOT_FOUND,
                    "No character sheet matched that request in this session.",
                    stage=WorkflowStage.CHARACTERS,
                )

            character_sheet = character_sheets[0]
            if (
                character_sheet.pitch_id is not None
                and character_sheet.pitch_id != state.selected_pitch_id
            ):
                return _reject(
                    SessionActionReasonCode.SESSION_RESOURCE_NOT_FOUND,
                    (
                        "That character sheet belongs to a different pitch than the one "
                        "currently selected."
                    ),
                    stage=WorkflowStage.CHARACTERS,
                )
            if state.selected_character_sheet_id == character_sheet.id:
                return _accept(
                    reasons=[
                        _reason(
                            SessionActionReasonCode.ACTION_IS_NOOP,
                            "That character sheet is already selected.",
                            stage=WorkflowStage.CHARACTERS,
                        )
                    ],
                    resolution=_ResolvedAction(character_sheet=character_sheet),
                )

            side_effects = self._build_stage_edit_side_effects(state, WorkflowStage.CHARACTERS)
            return self._finalize_change_action(
                action,
                side_effects=side_effects,
                confirmation_granted=confirmation_granted,
                resolution=_ResolvedAction(character_sheet=character_sheet),
            )

        def _evaluate_refine_character_sheet(
            self,
            action: ChatToUIAction,
            state: _PolicyState,
            *,
            confirmation_granted: bool,
        ) -> _ComputedDecision:
            blocked = _blocked_prerequisite_stages(state, WorkflowStage.CHARACTERS)
            if blocked:
                return _reject_for_blocked_stages(blocked, target_stage=WorkflowStage.CHARACTERS)
            if state.selected_pitch_id is None:
                return _reject(
                    SessionActionReasonCode.PREREQUISITE_SELECTION_MISSING,
                    "Select a pitch before refining the character sheet.",
                    stage=WorkflowStage.CHARACTERS,
                    prerequisite_action_types=[ChatToUIActionType.SELECT_PITCH],
                )
            if state.selected_character_sheet_id is None:
                return _reject(
                    SessionActionReasonCode.PREREQUISITE_SELECTION_MISSING,
                    "Select a character sheet before refining it.",
                    stage=WorkflowStage.CHARACTERS,
                    prerequisite_action_types=[ChatToUIActionType.SELECT_CHARACTER_SHEET],
                )

            side_effects = self._build_stage_edit_side_effects(state, WorkflowStage.CHARACTERS)
            return self._finalize_change_action(
                action,
                side_effects=side_effects,
                confirmation_granted=confirmation_granted,
            )

        def _evaluate_regenerate_character_sheet(
            self,
            action: RegenerateCharacterSheetAction,
            state: _PolicyState,
            *,
            confirmation_granted: bool,
        ) -> _ComputedDecision:
            blocked = _blocked_prerequisite_stages(state, WorkflowStage.CHARACTERS)
            if blocked:
                return _reject_for_blocked_stages(blocked, target_stage=WorkflowStage.CHARACTERS)
            if state.selected_pitch_id is None:
                return _reject(
                    SessionActionReasonCode.PREREQUISITE_SELECTION_MISSING,
                    "Select a pitch before regenerating character sheets.",
                    stage=WorkflowStage.CHARACTERS,
                    prerequisite_action_types=[ChatToUIActionType.SELECT_PITCH],
                )

            side_effects = self._build_stage_edit_side_effects(state, WorkflowStage.CHARACTERS)
            return self._finalize_change_action(
                action,
                side_effects=side_effects,
                confirmation_granted=confirmation_granted,
            )

        def _evaluate_accept_beat_sheet(
            self,
            session_id: str,
            action: AcceptBeatSheetAction,
            state: _PolicyState,
            *,
            confirmation_granted: bool,
        ) -> _ComputedDecision:
            blocked = _blocked_prerequisite_stages(state, WorkflowStage.BEATS)
            if blocked:
                return _reject_for_blocked_stages(blocked, target_stage=WorkflowStage.BEATS)
            if state.selected_character_sheet_id is None:
                return _reject(
                    SessionActionReasonCode.PREREQUISITE_SELECTION_MISSING,
                    "Select a character sheet before accepting a beat sheet.",
                    stage=WorkflowStage.BEATS,
                    prerequisite_action_types=[ChatToUIActionType.SELECT_CHARACTER_SHEET],
                )
            if state.stage_statuses.get(WorkflowStage.BEATS) == WorkflowStageState.NEEDS_REGENERATION:
                return _reject(
                    SessionActionReasonCode.TARGET_STAGE_STALE,
                    (
                        "Generate fresh beats before accepting one because the current beat "
                        "sheet is stale."
                    ),
                    stage=WorkflowStage.BEATS,
                    prerequisite_action_types=[ChatToUIActionType.REGENERATE_BEAT_SHEET],
                )

            beat_sheets = self._find_beat_sheets(session_id, action)
            if len(beat_sheets) > 1:
                return _reject(
                    SessionActionReasonCode.SESSION_RESOURCE_AMBIGUOUS,
                    "More than one beat sheet matched that request in this session.",
                    stage=WorkflowStage.BEATS,
                )
            if not beat_sheets:
                return _reject(
                    SessionActionReasonCode.SESSION_RESOURCE_NOT_FOUND,
                    "No beat sheet matched that request in this session.",
                    stage=WorkflowStage.BEATS,
                )

            beat_sheet = beat_sheets[0]
            if (
                beat_sheet.character_sheet_id is not None

## Command Started

- Time: `2026-04-01T07:31:52-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `47`
- Summary: in progress: /bin/zsh -lc "sed -n '1,320p' backend/tests/test_worker_runtime.py"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,320p' backend/tests/test_worker_runtime.py"
    Status: in progress

## Command Finished

- Time: `2026-04-01T07:31:52-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `48`
- Summary: completed, exit 0: /bin/zsh -lc "sed -n '1,320p' backend/tests/test_worker_runtime.py"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,320p' backend/tests/test_worker_runtime.py"
    Status: completed
    Exit code: 0
    Output:
    from __future__ import annotations

    from datetime import timedelta
    from pathlib import Path

    from app.db import Base, JobStatus, make_engine
    from app.services.jobs import BackgroundJobService
    from app.worker import JobHandlerRegistry, JobWorker
    from sqlalchemy.orm import Session, sessionmaker


    def _build_session_factory(tmp_path: Path) -> sessionmaker[Session]:
        database_path = tmp_path / "worker-runtime.db"
        engine = make_engine(f"sqlite+pysqlite:///{database_path}")

        with engine.begin() as connection:
            connection.exec_driver_sql("PRAGMA foreign_keys=ON")

        Base.metadata.create_all(engine)
        return sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


    def test_worker_processes_a_registered_job(tmp_path: Path) -> None:
        session_factory = _build_session_factory(tmp_path)

        with session_factory() as session:
            service = BackgroundJobService(session)
            queued = service.enqueue_job(
                job_type="test.handler",
                payload={"message": "night breeze"},
            )

        registry = JobHandlerRegistry()

        def handler(payload, context):
            context.heartbeat()
            return {
                "message": payload["message"],
                "worker_id": context.worker_id,
            }

        registry.register("test.handler", handler)

        worker = JobWorker(
            session_factory=session_factory,
            registry=registry,
            worker_id="runtime-worker",
            lease_duration=timedelta(seconds=30),
            poll_interval_seconds=0.01,
        )

        assert worker.run_once() is True

        with session_factory() as session:
            job = BackgroundJobService(session).get_job(queued.id)

        assert job.status == JobStatus.COMPLETED
        assert job.result_summary == {
            "message": "night breeze",
            "worker_id": "runtime-worker",
        }
        assert job.heartbeat_at is not None


    def test_worker_marks_unknown_job_types_failed(tmp_path: Path) -> None:
        session_factory = _build_session_factory(tmp_path)

        with session_factory() as session:
            service = BackgroundJobService(session)
            queued = service.enqueue_job(
                job_type="missing.handler",
                payload={"message": "no registry entry"},
            )

        worker = JobWorker(
            session_factory=session_factory,
            registry=JobHandlerRegistry(),
            worker_id="runtime-worker",
            lease_duration=timedelta(seconds=30),
            poll_interval_seconds=0.01,
        )

        assert worker.run_once() is True

        with session_factory() as session:
            job = BackgroundJobService(session).get_job(queued.id)

        assert job.status == JobStatus.FAILED
        assert job.error_message == "No handler registered for job type 'missing.handler'."

## Command Started

- Time: `2026-04-01T07:31:52-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `49`
- Summary: in progress: /bin/zsh -lc "sed -n '1,220p' backend/README.md"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,220p' backend/README.md"
    Status: in progress

## Command Finished

- Time: `2026-04-01T07:31:52-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `50`
- Summary: completed, exit 0: /bin/zsh -lc "sed -n '1,220p' backend/README.md"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,220p' backend/README.md"
    Status: completed
    Exit code: 0
    Output:
    # Backend

    This directory is the home for the FastAPI application, backend-owned workflow logic, durable
    relational models, and durable background job processing.

    ## Current layout

    - `app/`: live application code
      - `api/`: unversioned and versioned route modules
      - `db/`: SQLAlchemy metadata, ORM models, engine/session helpers, and health placeholders
      - `models/`: API response models and future domain models
      - `services/`: backend-owned business logic
      - `settings/`: environment-backed application settings
      - `storage/`: object storage abstraction, bucket/path strategy, and emulator smoke test
      - `worker/`: the durable PostgreSQL-backed worker loop and handler registry
    - `alembic.ini`: migration configuration entrypoint
    - `migrations/`: Alembic schema history and migration environment
    - `tests/`: backend test suite
    - `requirements.txt`: Python dependencies
    - `Dockerfile`: backend container image

    Planned expansion inside `app/` follows the architecture notes in [docs/architecture-overview.md](/Users/kevin/code/storyteller/docs/architecture-overview.md), including explicit homes for repositories, AI adapters, storage, and worker execution.

    ## Local run

    Install dependencies and start the app from this directory:

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    python -m app
    ```

    The local entrypoint reads `STORYTELLER_*` environment variables and defaults to:

    - host: `0.0.0.0`
    - port: `8565`
    - environment: `development`
    - versioned API prefix: `/api/v1`

    For local development, copy the repository-root example file and add a Gemini key:

    ```bash
    cp ../secrets.example.yaml ../secrets.yaml
    ```

    The settings module merges built-in defaults, `secrets.yaml`, and then `STORYTELLER_*` environment variables. Environment variables win when both sources set the same field. The backend-only Gemini key lives in `secrets.yaml` or the backend process environment and is never sent to the browser.

    Useful commands:

    ```bash
    pytest
    pytest --run-integration -m integration tests/integration
    python -m ruff check app tests
    python -m ruff format app tests
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8565
    python -m app.worker --once
    alembic upgrade head
    alembic downgrade base
    python -m app.seed_catalog
    python -m app.storage.smoke_test
    ```

    ## Database migrations

    The first PostgreSQL schema now lives in SQLAlchemy models under
    [`backend/app/db`](/Users/kevin/code/storyteller/backend/app/db) and the matching Alembic history
    under [`backend/migrations`](/Users/kevin/code/storyteller/backend/migrations).

    Run migrations against the local Compose Postgres instance:

    ```bash
    cd backend
    STORYTELLER_SECRETS_FILE="" \
    STORYTELLER_DATABASE_URL="postgresql+psycopg://storyteller:storyteller@127.0.0.1:8567/storyteller" \
    alembic upgrade head
    ```

    Create a new revision after the models change:

    ```bash
    cd backend
    STORYTELLER_SECRETS_FILE="" \
    STORYTELLER_DATABASE_URL="postgresql+psycopg://storyteller:storyteller@127.0.0.1:8567/storyteller" \
    alembic revision --autogenerate -m "describe change"
    ```

    The migration environment prefers an explicit `sqlalchemy.url` or `STORYTELLER_DATABASE_URL`. If
    neither is supplied, it falls back to the application settings loader.

    ## Integration tests

    The durable data-layer integration suite lives under
    [`backend/tests/integration`](/Users/kevin/code/storyteller/backend/tests/integration). These
    tests talk to the real local Postgres service and the file-backed fake GCS server instead of using
    SQLite or mocked HTTP transports.

    Run the suite from the repo root:

    ```bash
    make backend-integration-test
    ```

    That target starts `postgres` and `gcs` if needed, creates a disposable PostgreSQL database with
    Alembic, reuses the local fake GCS server on `http://127.0.0.1:8568`, and runs only
    `pytest.mark.integration` tests. The default `make backend-test` path keeps skipping these tests so
    the fast unit loop stays fast.

    Manual invocation from `backend/` is also supported:

    ```bash
    STORYTELLER_RUN_INTEGRATION_TESTS=1 \
    STORYTELLER_INTEGRATION_POSTGRES_ADMIN_URL="postgresql+psycopg://storyteller:storyteller@127.0.0.1:8567/postgres" \
    STORYTELLER_INTEGRATION_GCS_ENDPOINT="http://127.0.0.1:8568" \
    python -m pytest --run-integration -m integration tests/integration
    ```

    Future CI should treat `make backend-integration-test` as the durable-state gate after booting the
    same Compose-backed infrastructure. That keeps local and CI behavior aligned and makes migration,
    queue-claim, and storage regressions visible before higher-level workflow prompts add more state.

    ## Background jobs

    The durable queue now lives in the `background_jobs` table and is claimed directly from PostgreSQL,
    so long-running story and audio work can move out of API request threads without adding Redis or a
    second queue store.

    Core entrypoints:

    - `BackgroundJobService.enqueue_job(...)`: create a queued job row with a JSON payload
    - `BackgroundJobService.claim_next_job(...)`: lease one queued or expired in-progress job
    - `BackgroundJobService.heartbeat_job(...)`: extend the lease while work is still running
    - `python -m app.worker`: run the polling worker against the configured database

    The default worker registry includes a `demo.echo` handler that is useful for smoke tests and
    verification before composition and audio handlers land in later prompts.

    ## Seeded catalog

    The curated genre and tone catalog is stored in
    [`app/data/genre_tone_catalog.yaml`](/Users/kevin/code/storyteller/backend/app/data/genre_tone_catalog.yaml)
    and seeded with:

    ```bash
    cd backend
    python -m app.seed_catalog
    ```

    For local Compose Postgres:

    ```bash
    cd backend
    STORYTELLER_SECRETS_FILE="" \
    STORYTELLER_DATABASE_URL="postgresql+psycopg://storyteller:storyteller@127.0.0.1:8567/storyteller" \
    python -m app.seed_catalog
    ```

    Use `--dry-run` to validate the YAML file and report the expected write counts without committing.
    Catalog provenance and editing guidance live in
    [docs/genre-tone-catalog.md](/Users/kevin/code/storyteller/docs/genre-tone-catalog.md).

    ## Object storage

    The storage abstraction now lives in
    [`backend/app/storage`](/Users/kevin/code/storyteller/backend/app/storage). It hides the current
    GCS JSON API calls behind a small service so later prompts can keep business logic focused on
    session artifacts rather than bucket bootstrapping or emulator-specific HTTP details.

    Core entrypoints:

    - `build_object_storage_service(settings)`: build the runtime storage client from backend settings
    - `object_storage.paths`: predictable bucket/key builders for draft, audio, export, and debug paths
    - `python -m app.storage.smoke_test`: write and read a sample object through the configured backend

    The bucket and prefix conventions are documented in
    [docs/storage-buckets-and-prefixes.md](/Users/kevin/code/storyteller/docs/storage-buckets-and-prefixes.md).

    To verify the local fake GCS server from the repository root:

    ```bash
    make backend-storage-smoke
    ```

    That target defaults to `http://127.0.0.1:8568` so it can talk to the local emulator from the host
    shell even when the main Compose backend container uses `http://gcs:4443` internally.

    ## Health routes

    - `GET /health`: primary service health endpoint
    - `GET /api/v1/health`: versioned API health endpoint
    - `GET /api/hello`: compatibility endpoint kept for the current frontend scaffold

    More detail on file discovery, supported YAML shape, and matching environment variables is in [docs/secrets-and-local-config.md](/Users/kevin/code/storyteller/docs/secrets-and-local-config.md).

## Agent Message

- Time: `2026-04-01T07:32:08-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `51`
- Summary: The codebase has strong policy and chat parsing contracts, but the actual stage operations are still implicit. I’m mapping what durable services already exist so the registry wraps real business logic instead of placeholder endpoints.

### Full Text

    The codebase has strong policy and chat parsing contracts, but the actual stage operations are still implicit. I’m mapping what durable services already exist so the registry wraps real business logic instead of placeholder endpoints.

## Command Started

- Time: `2026-04-01T07:32:08-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `52`
- Summary: in progress: /bin/zsh -lc "sed -n '1,360p' backend/app/services/sessions.py"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,360p' backend/app/services/sessions.py"
    Status: in progress

## Command Started

- Time: `2026-04-01T07:32:08-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `53`
- Summary: in progress: /bin/zsh -lc "sed -n '1,360p' backend/app/services/jobs.py"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,360p' backend/app/services/jobs.py"
    Status: in progress

## Command Started

- Time: `2026-04-01T07:32:08-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `54`
- Summary: in progress: /bin/zsh -lc "sed -n '1,320p' backend/app/api/v1/routes/sessions.py"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,320p' backend/app/api/v1/routes/sessions.py"
    Status: in progress

## Command Finished

- Time: `2026-04-01T07:32:08-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `55`
- Summary: completed, exit 0: /bin/zsh -lc "sed -n '1,320p' backend/app/api/v1/routes/sessions.py"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,320p' backend/app/api/v1/routes/sessions.py"
    Status: completed
    Exit code: 0
    Output:
    from __future__ import annotations

    from typing import Annotated

    from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
    from sqlalchemy.orm import Session

    from app.ai import IntentParserAdapter
    from app.api.dependencies import get_db_session, get_intent_parser_adapter
    from app.models import (
        CreateSessionRequest,
        ParseChatIntentRequest,
        ParsedChatIntentResponse,
        RecentSessionSummary,
        RecordSessionUIActionRequest,
        SessionActionPolicyEvaluation,
        SessionActionPolicyEvaluationRequest,
        SessionContextUpdateRequest,
        SessionContextUpdateResponse,
        SessionEventView,
        SessionHistoryView,
        SessionSnapshot,
    )
    from app.services import SessionActionPolicyService, SessionIntentParserService
    from app.services.sessions import (
        SessionNotFoundError,
        SessionService,
        UnsupportedSessionContextUpdateError,
    )

    router = APIRouter(prefix="/sessions", tags=["sessions"])


    @router.get(
        "",
        response_model=list[RecentSessionSummary],
        summary="List recent story sessions",
    )
    def list_recent_sessions(
        db_session: Annotated[Session, Depends(get_db_session)],
        limit: Annotated[int, Query(ge=1, le=100)] = 20,
    ) -> list[RecentSessionSummary]:
        return SessionService(db_session).list_recent_sessions(limit=limit)


    @router.get(
        "/{session_id}",
        response_model=SessionSnapshot,
        summary="Load a story session snapshot",
    )
    def get_session_snapshot(
        session_id: str,
        db_session: Annotated[Session, Depends(get_db_session)],
    ) -> SessionSnapshot:
        try:
            return SessionService(db_session).load_session_snapshot(session_id)
        except SessionNotFoundError as exc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(exc),
            ) from exc


    @router.get(
        "/{session_id}/history",
        response_model=SessionHistoryView,
        summary="Load durable session history",
    )
    def get_session_history(
        session_id: str,
        db_session: Annotated[Session, Depends(get_db_session)],
        limit: Annotated[int | None, Query(ge=1, le=500)] = None,
        after_sequence_number: Annotated[int | None, Query(ge=0)] = None,
    ) -> SessionHistoryView:
        try:
            return SessionService(db_session).load_session_history(
                session_id,
                limit=limit,
                after_sequence_number=after_sequence_number,
            )
        except SessionNotFoundError as exc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(exc),
            ) from exc


    @router.post(
        "",
        response_model=SessionSnapshot,
        status_code=status.HTTP_201_CREATED,
        summary="Create a new story session",
    )
    def create_session(
        db_session: Annotated[Session, Depends(get_db_session)],
        payload: CreateSessionRequest | None = None,
    ) -> SessionSnapshot:
        return SessionService(db_session).create_session(
            working_title=payload.working_title if payload is not None else None,
        )


    @router.post(
        "/{session_id}/ui-actions",
        response_model=SessionEventView,
        status_code=status.HTTP_201_CREATED,
        summary="Record a durable UI-originated action",
    )
    def record_session_ui_action(
        session_id: str,
        payload: RecordSessionUIActionRequest,
        db_session: Annotated[Session, Depends(get_db_session)],
    ) -> SessionEventView:
        try:
            return SessionService(db_session).record_ui_action(
                session_id,
                action=payload.action,
                stage=payload.stage,
                control_id=payload.control_id,
                value_summary=payload.value_summary,
                origin=payload.origin,
            )
        except SessionNotFoundError as exc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(exc),
            ) from exc


    @router.post(
        "/{session_id}/context-updates",
        response_model=SessionContextUpdateResponse,
        status_code=status.HTTP_200_OK,
        summary="Apply a durable UI-originated context update",
    )
    def apply_session_context_update(
        session_id: str,
        payload: SessionContextUpdateRequest,
        db_session: Annotated[Session, Depends(get_db_session)],
    ) -> SessionContextUpdateResponse:
        try:
            return SessionService(db_session).apply_context_update(
                session_id,
                payload=payload,
            )
        except SessionNotFoundError as exc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(exc),
            ) from exc
        except UnsupportedSessionContextUpdateError as exc:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=str(exc),
            ) from exc


    @router.post(
        "/{session_id}/chat/intents",
        response_model=ParsedChatIntentResponse,
        summary="Parse a chat message into structured UI actions",
    )
    def parse_chat_intents(
        session_id: str,
        payload: ParseChatIntentRequest,
        request: Request,
        db_session: Annotated[Session, Depends(get_db_session)],
    ) -> ParsedChatIntentResponse:
        intent_parser: IntentParserAdapter | None = None
        if payload.explicit_command is None:
            intent_parser = get_intent_parser_adapter(request)

        try:
            return SessionIntentParserService(db_session, intent_parser).parse_user_message(
                session_id,
                message=payload.message,
                explicit_command=payload.explicit_command,
            )
        except SessionNotFoundError as exc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(exc),
            ) from exc


    @router.post(
        "/{session_id}/actions/evaluate",
        response_model=SessionActionPolicyEvaluation,
        summary="Evaluate proposed UI actions against durable session policy",
    )
    def evaluate_session_actions(
        session_id: str,
        payload: SessionActionPolicyEvaluationRequest,
        db_session: Annotated[Session, Depends(get_db_session)],
    ) -> SessionActionPolicyEvaluation:
        try:
            return SessionActionPolicyService(db_session).evaluate_request(
                session_id,
                request=payload,
            )
        except SessionNotFoundError as exc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(exc),
            ) from exc

## Command Finished

- Time: `2026-04-01T07:32:08-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `56`
- Summary: completed, exit 0: /bin/zsh -lc "sed -n '1,360p' backend/app/services/jobs.py"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,360p' backend/app/services/jobs.py"
    Status: completed
    Exit code: 0
    Output:
    from __future__ import annotations

    from dataclasses import dataclass
    from datetime import datetime, timedelta
    from typing import Any
    from uuid import uuid4

    from sqlalchemy.orm import Session

    from app.db import BackgroundJob, JobStatus, utc_now
    from app.repositories import BackgroundJobRepository

    JobPayload = dict[str, Any] | list[Any] | None


    class BackgroundJobServiceError(Exception):
        """Base error for durable background job failures."""


    class BackgroundJobNotFoundError(BackgroundJobServiceError):
        """Raised when a requested job row does not exist."""


    class BackgroundJobLeaseLostError(BackgroundJobServiceError):
        """Raised when a worker tries to update a job after losing its lease."""


    @dataclass(frozen=True)
    class BackgroundJobRecord:
        id: str
        session_id: str | None
        job_type: str
        status: JobStatus
        payload: JobPayload
        result_summary: JobPayload
        attempt_count: int
        lease_owner: str | None
        lease_expires_at: datetime | None
        claimed_at: datetime | None
        heartbeat_at: datetime | None
        started_at: datetime | None
        completed_at: datetime | None
        failed_at: datetime | None
        error_message: str | None
        created_at: datetime
        updated_at: datetime


    @dataclass(frozen=True)
    class ClaimedBackgroundJob:
        id: str
        session_id: str | None
        job_type: str
        payload: JobPayload
        attempt_count: int
        lease_owner: str
        lease_token: str
        lease_expires_at: datetime
        heartbeat_at: datetime


    class BackgroundJobService:
        def __init__(self, session: Session):
            self._session = session
            self._jobs = BackgroundJobRepository(session)

        def enqueue_job(
            self,
            *,
            job_type: str,
            payload: JobPayload = None,
            session_id: str | None = None,
        ) -> BackgroundJobRecord:
            normalized_type = job_type.strip()
            if not normalized_type:
                raise ValueError("job_type must not be empty")

            job = self._jobs.create(
                session_id=session_id,
                job_type=normalized_type,
                payload=payload,
            )
            self._session.commit()
            return _to_job_record(job)

        def get_job(self, job_id: str) -> BackgroundJobRecord:
            job = self._jobs.get_by_id(job_id)
            if job is None:
                raise BackgroundJobNotFoundError(f"background job {job_id!r} was not found")

            return _to_job_record(job)

        def claim_next_job(
            self,
            *,
            lease_owner: str,
            lease_duration: timedelta,
        ) -> ClaimedBackgroundJob | None:
            normalized_owner = lease_owner.strip()
            if not normalized_owner:
                raise ValueError("lease_owner must not be empty")
            if lease_duration <= timedelta(0):
                raise ValueError("lease_duration must be greater than zero")

            now = utc_now()
            job = self._jobs.claim_next_available(
                lease_owner=normalized_owner,
                lease_token=str(uuid4()),
                now=now,
                lease_expires_at=now + lease_duration,
            )

            if job is None:
                self._session.rollback()
                return None

            self._session.commit()
            return _to_claimed_job(job)

        def heartbeat_job(
            self,
            claim: ClaimedBackgroundJob,
            *,
            lease_duration: timedelta,
        ) -> BackgroundJobRecord:
            if lease_duration <= timedelta(0):
                raise ValueError("lease_duration must be greater than zero")

            now = utc_now()
            job = self._jobs.heartbeat(
                job_id=claim.id,
                lease_owner=claim.lease_owner,
                lease_token=claim.lease_token,
                now=now,
                lease_expires_at=now + lease_duration,
            )

            if job is None:
                self._session.rollback()
                raise BackgroundJobLeaseLostError(
                    f"background job {claim.id!r} no longer holds lease {claim.lease_token!r}",
                )

            self._session.commit()
            return _to_job_record(job)

        def complete_job(
            self,
            claim: ClaimedBackgroundJob,
            *,
            result_summary: JobPayload = None,
        ) -> BackgroundJobRecord:
            now = utc_now()
            job = self._jobs.mark_completed(
                job_id=claim.id,
                lease_owner=claim.lease_owner,
                lease_token=claim.lease_token,
                now=now,
                result_summary=result_summary,
            )

            if job is None:
                self._session.rollback()
                raise BackgroundJobLeaseLostError(
                    f"background job {claim.id!r} no longer holds lease {claim.lease_token!r}",
                )

            self._session.commit()
            return _to_job_record(job)

        def fail_job(
            self,
            claim: ClaimedBackgroundJob,
            *,
            error_message: str,
            result_summary: JobPayload = None,
        ) -> BackgroundJobRecord:
            normalized_error = error_message.strip()
            if not normalized_error:
                raise ValueError("error_message must not be empty")

            now = utc_now()
            job = self._jobs.mark_failed(
                job_id=claim.id,
                lease_owner=claim.lease_owner,
                lease_token=claim.lease_token,
                now=now,
                error_message=normalized_error,
                result_summary=result_summary,
            )

            if job is None:
                self._session.rollback()
                raise BackgroundJobLeaseLostError(
                    f"background job {claim.id!r} no longer holds lease {claim.lease_token!r}",
                )

            self._session.commit()
            return _to_job_record(job)


    def _to_job_record(job: BackgroundJob) -> BackgroundJobRecord:
        return BackgroundJobRecord(
            id=job.id,
            session_id=job.session_id,
            job_type=job.job_type,
            status=job.status,
            payload=job.payload,
            result_summary=job.result_summary,
            attempt_count=job.attempt_count,
            lease_owner=job.lease_owner,
            lease_expires_at=job.lease_expires_at,
            claimed_at=job.claimed_at,
            heartbeat_at=job.heartbeat_at,
            started_at=job.started_at,
            completed_at=job.completed_at,
            failed_at=job.failed_at,
            error_message=job.error_message,
            created_at=job.created_at,
            updated_at=job.updated_at,
        )


    def _to_claimed_job(job: BackgroundJob) -> ClaimedBackgroundJob:
        if (
            job.lease_owner is None
            or job.lease_token is None
            or job.lease_expires_at is None
            or job.heartbeat_at is None
        ):
            raise RuntimeError(f"background job {job.id!r} was claimed without a durable lease")

        return ClaimedBackgroundJob(
            id=job.id,
            session_id=job.session_id,
            job_type=job.job_type,
            payload=job.payload,
            attempt_count=job.attempt_count,
            lease_owner=job.lease_owner,
            lease_token=job.lease_token,
            lease_expires_at=job.lease_expires_at,
            heartbeat_at=job.heartbeat_at,
        )

## Command Finished

- Time: `2026-04-01T07:32:08-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `57`
- Summary: completed, exit 0: /bin/zsh -lc "sed -n '1,360p' backend/app/services/sessions.py"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,360p' backend/app/services/sessions.py"
    Status: completed
    Exit code: 0
    Output:
    from __future__ import annotations

    from collections.abc import Mapping

    from sqlalchemy.orm import Session

    from app.db import (
        AudioJob,
        BeatSheet,
        CharacterSheet,
        CompositionJob,
        SessionAsset,
        StoryBrief,
    )
    from app.db.base import utc_now
    from app.models import (
        WORKFLOW_STAGE_SEQUENCE,
        AudioJobView,
        BeatSheetView,
        CharacterSheetView,
        CompositionJobView,
        ConversationMemorySnapshotView,
        PitchView,
        RecentSessionSummary,
        SessionAssetView,
        SessionCatalogSelection,
        SessionContextUpdateRequest,
        SessionContextUpdateResponse,
        SessionEventActor,
        SessionEventView,
        SessionHistoryView,
        SessionProgress,
        SessionSnapshot,
        SessionStageStateView,
        StoryBriefView,
        StorySetupView,
        UserEditTargetKind,
        WorkflowStage,
        WorkflowStageState,
        get_invalidated_stages_after_edit,
        get_workflow_stage_definition,
        resolve_resume_stage,
    )
    from app.repositories import (
        SessionAggregate,
        StorySessionRepository,
        WorkflowStageStateRepository,
    )
    from app.services.agent_context import build_session_agent_context_summary
    from app.services.conversation_memory import SessionMemoryService
    from app.services.event_log import SessionEventLogService


    class SessionServiceError(Exception):
        """Base error for session service failures."""


    class SessionNotFoundError(SessionServiceError):
        """Raised when a requested session does not exist."""


    class InvalidStageTransitionError(SessionServiceError):
        """Raised when a stage update violates workflow rules."""


    class UnsupportedSessionContextUpdateError(SessionServiceError):
        """Raised when a UI-originated context update is not supported."""


    STAGE_EDIT_TARGET_KIND_MAP: dict[WorkflowStage, UserEditTargetKind] = {
        WorkflowStage.BRIEF: UserEditTargetKind.STORY_BRIEF,
        WorkflowStage.PITCHES: UserEditTargetKind.PITCH,
        WorkflowStage.CHARACTERS: UserEditTargetKind.CHARACTER_SHEET,
        WorkflowStage.BEATS: UserEditTargetKind.BEAT_SHEET,
        WorkflowStage.STORY_SETUP: UserEditTargetKind.STORY_SETUP,
        WorkflowStage.COMPOSITION: UserEditTargetKind.COMPOSITION_SEGMENT,
        WorkflowStage.AUDIO: UserEditTargetKind.AUDIO_SETTINGS,
    }


    class SessionService:
        def __init__(self, session: Session):
            self._session = session
            self._sessions = StorySessionRepository(session)
            self._stage_states = WorkflowStageStateRepository(session)
            self._event_log = SessionEventLogService(session)
            self._memory = SessionMemoryService(session)

        def create_session(
            self,
            *,
            working_title: str | None = None,
            actor: SessionEventActor | None = None,
        ) -> SessionSnapshot:
            story_session = self._sessions.create(working_title=_normalize_optional_text(working_title))
            stage_map = self._stage_states.ensure_for_session(story_session)
            self._apply_rollups(story_session, stage_map)
            self._event_log.record_session_created(
                story_session.id,
                working_title=story_session.working_title,
                actor=actor,
            )
            self._session.commit()
            return self.load_session_snapshot(story_session.id)

        def load_session_snapshot(self, session_id: str) -> SessionSnapshot:
            aggregate = self._sessions.get_aggregate(session_id)
            if aggregate is None:
                raise SessionNotFoundError(f"session {session_id!r} was not found")

            return _build_session_snapshot(
                aggregate,
                conversation_memory=self._memory.refresh_summary(session_id),
            )

        def list_recent_sessions(self, *, limit: int = 20) -> list[RecentSessionSummary]:
            if limit <= 0:
                raise ValueError("limit must be greater than zero")

            sessions = self._sessions.list_recent(limit=limit)
            return [_build_recent_session_summary(story_session) for story_session in sessions]

        def load_session_history(
            self,
            session_id: str,
            *,
            limit: int | None = None,
            after_sequence_number: int | None = None,
        ) -> SessionHistoryView:
            if limit is not None and limit <= 0:
                raise ValueError("limit must be greater than zero")

            if not self._sessions.exists(session_id):
                raise SessionNotFoundError(f"session {session_id!r} was not found")

            return self._event_log.list_session_history(
                session_id,
                limit=limit,
                after_sequence_number=after_sequence_number,
            )

        def record_ui_action(
            self,
            session_id: str,
            *,
            action: str,
            stage: WorkflowStage | None = None,
            control_id: str | None = None,
            value_summary: str | None = None,
            origin: str = "workspace",
            actor: SessionEventActor | None = None,
        ) -> SessionEventView:
            if not self._sessions.exists(session_id):
                raise SessionNotFoundError(f"session {session_id!r} was not found")

            event = self._event_log.record_ui_action(
                session_id,
                action=action,
                stage=stage,
                control_id=control_id,
                value_summary=value_summary,
                origin=origin,
                actor=actor,
            )
            self._session.commit()
            return self._event_log.build_event_view(event)

        def apply_context_update(
            self,
            session_id: str,
            *,
            payload: SessionContextUpdateRequest,
            actor: SessionEventActor | None = None,
        ) -> SessionContextUpdateResponse:
            story_session = self._sessions.get_for_update(session_id)
            if story_session is None:
                raise SessionNotFoundError(f"session {session_id!r} was not found")

            if payload.target_kind != "stage_note":
                raise UnsupportedSessionContextUpdateError(
                    f"unsupported context update kind {payload.target_kind!r}"
                )

            target_kind = STAGE_EDIT_TARGET_KIND_MAP.get(payload.stage)
            if target_kind is None:
                raise UnsupportedSessionContextUpdateError(
                    f"stage {payload.stage.value!r} does not support durable note edits"
                )

            stage_map = self._stage_states.ensure_for_session(story_session)
            stage_snapshot = stage_map[payload.stage]
            previous_status = stage_snapshot.status
            now = utc_now()
            normalized_detail = _normalize_optional_text(payload.values.detail)

            if stage_snapshot.status == WorkflowStageState.DRAFT:
                self._validate_stage_transition(
                    stage_map,
                    stage=payload.stage,
                    status=WorkflowStageState.IN_PROGRESS,
                )
                stage_snapshot.status = WorkflowStageState.IN_PROGRESS
                stage_snapshot.started_at = stage_snapshot.started_at or now
            elif stage_snapshot.status == WorkflowStageState.NEEDS_REGENERATION:
                stage_snapshot.status = WorkflowStageState.IN_PROGRESS
                stage_snapshot.started_at = stage_snapshot.started_at or now
                stage_snapshot.completed_at = None

            stage_snapshot.detail = normalized_detail
            invalidated_stages = self._invalidate_dependent_stages(
                stage_map,
                stage=payload.stage,
                detail=normalized_detail,
            )
            self._apply_rollups(story_session, stage_map)

            if previous_status != stage_snapshot.status or invalidated_stages:
                stage_event = self._event_log.record_stage_state_changed(
                    story_session.id,
                    stage=payload.stage,
                    previous_status=previous_status,
                    status=stage_snapshot.status,
                    detail=stage_snapshot.detail,
                    invalidated_stages=invalidated_stages,
                    current_stage=story_session.current_stage,
                    resume_stage=story_session.resume_stage,
                    furthest_completed_stage=story_session.furthest_completed_stage,
                    overall_status=story_session.overall_status,
                    actor=actor,
                )
                for invalidated_stage in invalidated_stages:
                    stage_map[invalidated_stage].last_event = stage_event

            edit_event = self._event_log.record_user_edit(
                story_session.id,
                target_kind=target_kind,
                stage=payload.stage,
                changed_fields=["detail"],
                source=payload.origin,
                field_values={
                    "detail": normalized_detail,
                    "control_id": payload.control_id,
                },
                summary_text=_build_stage_note_summary(payload.stage, normalized_detail),
                actor=actor,
            )
            stage_snapshot.last_event = edit_event
            self._session.commit()
            return SessionContextUpdateResponse(
                snapshot=self.load_session_snapshot(story_session.id),
                event=self._event_log.build_event_view(edit_event),
            )

        def update_stage_state(
            self,
            session_id: str,
            *,
            stage: WorkflowStage,
            status: WorkflowStageState,
            detail: str | None = None,
            actor: SessionEventActor | None = None,
        ) -> SessionSnapshot:
            story_session = self._sessions.get_for_update(session_id)
            if story_session is None:
                raise SessionNotFoundError(f"session {session_id!r} was not found")

            stage_map = self._stage_states.ensure_for_session(story_session)
            self._validate_stage_transition(stage_map, stage=stage, status=status)

            snapshot = stage_map[stage]
            previous_status = snapshot.status
            now = utc_now()
            snapshot.detail = _normalize_optional_text(detail)
            invalidated_stages: list[WorkflowStage] = []

            if status == WorkflowStageState.DRAFT:
                snapshot.status = WorkflowStageState.DRAFT
                snapshot.started_at = None
                snapshot.completed_at = None
            elif status == WorkflowStageState.IN_PROGRESS:
                snapshot.status = WorkflowStageState.IN_PROGRESS
                snapshot.started_at = snapshot.started_at or now
                snapshot.completed_at = None
            elif status == WorkflowStageState.COMPLETED:
                snapshot.status = WorkflowStageState.COMPLETED
                snapshot.started_at = snapshot.started_at or now
                snapshot.completed_at = now
                invalidated_stages = self._invalidate_dependent_stages(
                    stage_map,
                    stage=stage,
                    detail=snapshot.detail,
                )
            else:
                snapshot.status = WorkflowStageState.NEEDS_REGENERATION
                invalidated_stages = self._invalidate_dependent_stages(
                    stage_map,
                    stage=stage,
                    detail=snapshot.detail,
                )

            self._apply_rollups(story_session, stage_map)
            stage_event = self._event_log.record_stage_state_changed(
                story_session.id,
                stage=stage,
                previous_status=previous_status,
                status=snapshot.status,
                detail=snapshot.detail,
                invalidated_stages=invalidated_stages,
                current_stage=story_session.current_stage,
                resume_stage=story_session.resume_stage,
                furthest_completed_stage=story_session.furthest_completed_stage,
                overall_status=story_session.overall_status,
                actor=actor,
            )
            snapshot.last_event = stage_event
            for invalidated_stage in invalidated_stages:
                stage_map[invalidated_stage].last_event = stage_event
            self._session.commit()
            return self.load_session_snapshot(story_session.id)

        def _validate_stage_transition(
            self,
            stage_map: Mapping[WorkflowStage, object],
            *,
            stage: WorkflowStage,
            status: WorkflowStageState,
        ) -> None:
            if status in {WorkflowStageState.IN_PROGRESS, WorkflowStageState.COMPLETED}:
                incomplete_prerequisites = [
                    prior_stage.value
                    for prior_stage in _stages_before(stage)
                    if getattr(stage_map[prior_stage], "status") != WorkflowStageState.COMPLETED
                ]
                if incomplete_prerequisites:
                    joined = ", ".join(incomplete_prerequisites)
                    raise InvalidStageTransitionError(
                        f"cannot set {stage.value!r} to {status.value!r} before prerequisites are "
                        f"completed: {joined}"
                    )

            if status == WorkflowStageState.NEEDS_REGENERATION and stage == WorkflowStage.GENRE:
                raise InvalidStageTransitionError("genre cannot be marked needs_regeneration directly")

        def _invalidate_dependent_stages(
            self,
            stage_map: Mapping[WorkflowStage, object],
            *,
            stage: WorkflowStage,
            detail: str | None,
        ) -> list[WorkflowStage]:
            if stage == WorkflowStage.FINALIZE:
                return []

            reason = detail or f"Needs regeneration after {stage.value} changed."
            invalidated_stages: list[WorkflowStage] = []

            for invalidated_stage in get_invalidated_stages_after_edit(stage):
                snapshot = stage_map[invalidated_stage]
                if getattr(snapshot, "status") == WorkflowStageState.DRAFT:
                    continue

## Command Started

- Time: `2026-04-01T07:32:08-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `58`
- Summary: in progress: /bin/zsh -lc "sed -n '1,320p' backend/app/models/session.py"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,320p' backend/app/models/session.py"
    Status: in progress

## Command Finished

- Time: `2026-04-01T07:32:08-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `59`
- Summary: completed, exit 0: /bin/zsh -lc "sed -n '1,320p' backend/app/models/session.py"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,320p' backend/app/models/session.py"
    Status: completed
    Exit code: 0
    Output:
    from __future__ import annotations

    from datetime import datetime
    from typing import Any, Literal

    from pydantic import BaseModel, Field

    from app.models.events import SessionEventView
    from app.models.workflow import WorkflowStage, WorkflowStageState


    class SessionCatalogSelection(BaseModel):
        id: str
        slug: str
        label: str


    class SessionProgress(BaseModel):
        total_stages: int
        completed_stages: int
        in_progress_stages: int
        needs_regeneration_stages: int


    class SessionStageStateView(BaseModel):
        stage: WorkflowStage
        label: str
        description: str
        status: WorkflowStageState
        detail: str | None = None
        started_at: datetime | None = None
        completed_at: datetime | None = None
        last_event_summary: str | None = None
        last_event_type: str | None = None
        last_event_at: datetime | None = None


    class StoryBriefView(BaseModel):
        id: str
        revision_number: int
        raw_brief: str
        normalized_summary: str | None = None
        planning_notes: str | None = None
        accepted_at: datetime | None = None


    class PitchView(BaseModel):
        id: str
        generation_key: str
        pitch_index: int
        title: str
        logline: str
        summary: str | None = None
        bedtime_notes: str | None = None
        accepted_at: datetime | None = None


    class CharacterSheetView(BaseModel):
        id: str
        revision_number: int
        title: str | None = None
        protagonist_name: str | None = None
        summary: str | None = None
        supporting_cast: dict[str, Any] | list[Any] | None = None
        bedtime_notes: str | None = None
        accepted_at: datetime | None = None


    class BeatSheetView(BaseModel):
        id: str
        revision_number: int
        summary: str | None = None
        beats: dict[str, Any] | list[Any] | None = None
        bedtime_notes: str | None = None
        accepted_at: datetime | None = None


    class StorySetupView(BaseModel):
        id: str
        revision_number: int
        target_word_count: int | None = None
        target_runtime_minutes: int | None = None
        chapter_count: int | None = None
        chapter_style: str | None = None
        guidance_notes: str | None = None
        preferences: dict[str, Any] | list[Any] | None = None
        accepted_at: datetime | None = None


    class CompositionJobView(BaseModel):
        id: str
        job_kind: str
        status: str
        progress_percent: float
        current_segment_index: int | None = None
        attempt_count: int
        stop_reason: str | None = None
        error_message: str | None = None
        started_at: datetime | None = None
        completed_at: datetime | None = None
        created_at: datetime
        updated_at: datetime


    class AudioJobView(BaseModel):
        id: str
        status: str
        voice_key: str | None = None
        playback_speed: float
        include_background_music: bool
        music_profile: str | None = None
        estimated_duration_seconds: int | None = None
        current_segment_index: int | None = None
        attempt_count: int
        stop_reason: str | None = None
        error_message: str | None = None
        started_at: datetime | None = None
        completed_at: datetime | None = None
        created_at: datetime
        updated_at: datetime


    class SessionAssetView(BaseModel):
        id: str
        asset_kind: str
        status: str
        storage_bucket: str
        object_path: str
        mime_type: str
        byte_size: int | None = None
        checksum_sha256: str | None = None
        segment_index: int | None = None
        error_message: str | None = None
        ready_at: datetime | None = None
        failed_at: datetime | None = None
        created_at: datetime
        updated_at: datetime


    class ConversationMemoryWorkflow(BaseModel):
        current_stage: WorkflowStage
        current_stage_status: WorkflowStageState
        resume_stage: WorkflowStage
        overall_status: WorkflowStageState


    class ConversationMemorySummaryData(BaseModel):
        schema_version: int = Field(default=1, ge=1)
        session_title: str
        workflow: ConversationMemoryWorkflow
        story_decisions: list[str] = Field(default_factory=list)
        user_preferences: list[str] = Field(default_factory=list)
        unresolved_questions: list[str] = Field(default_factory=list)
        active_jobs: list[str] = Field(default_factory=list)


    class ConversationMemorySnapshotView(BaseModel):
        id: str
        trigger_event_id: str | None = None
        trigger_event_type: str | None = None
        trigger_event_sequence_number: int | None = None
        summary_text: str
        summary_data: ConversationMemorySummaryData
        created_at: datetime


    class CreateSessionRequest(BaseModel):
        working_title: str | None = None


    class RecordSessionUIActionRequest(BaseModel):
        action: str = Field(min_length=1)
        stage: WorkflowStage | None = None
        control_id: str | None = None
        value_summary: str | None = None
        origin: str = Field(default="workspace", min_length=1)


    class SessionContextStageNoteValues(BaseModel):
        detail: str | None = None


    class SessionContextUpdateRequest(BaseModel):
        target_kind: Literal["stage_note"] = "stage_note"
        stage: WorkflowStage
        control_id: str | None = None
        origin: str = Field(default="workspace", min_length=1)
        values: SessionContextStageNoteValues


    class SessionContextUpdateResponse(BaseModel):
        snapshot: "SessionSnapshot"
        event: SessionEventView


    class RecentSessionSummary(BaseModel):
        id: str
        display_title: str
        working_title: str | None = None
        current_stage: WorkflowStage
        resume_stage: WorkflowStage
        furthest_completed_stage: WorkflowStage | None = None
        overall_status: WorkflowStageState
        created_at: datetime
        updated_at: datetime
        completed_at: datetime | None = None
        selected_genre: SessionCatalogSelection | None = None
        selected_tone_profile: SessionCatalogSelection | None = None
        progress: SessionProgress


    class SessionSnapshot(BaseModel):
        id: str
        display_title: str
        working_title: str | None = None
        current_stage: WorkflowStage
        resume_stage: WorkflowStage
        furthest_completed_stage: WorkflowStage | None = None
        overall_status: WorkflowStageState
        created_at: datetime
        updated_at: datetime
        completed_at: datetime | None = None
        selected_genre: SessionCatalogSelection | None = None
        selected_tone_profile: SessionCatalogSelection | None = None
        progress: SessionProgress
        stage_states: list[SessionStageStateView] = Field(default_factory=list)
        story_brief: StoryBriefView | None = None
        selected_pitch: PitchView | None = None
        selected_character_sheet: CharacterSheetView | None = None
        selected_beat_sheet: BeatSheetView | None = None
        selected_story_setup: StorySetupView | None = None
        active_composition_job: CompositionJobView | None = None
        active_audio_job: AudioJobView | None = None
        latest_story_asset: SessionAssetView | None = None
        latest_audio_asset: SessionAssetView | None = None
        conversation_memory: ConversationMemorySnapshotView | None = None
        agent_context_summary: str | None = None


    ExportAssetView = SessionAssetView


    SessionContextUpdateResponse.model_rebuild()

## Command Started

- Time: `2026-04-01T07:32:08-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `60`
- Summary: in progress: /bin/zsh -lc "sed -n '1,260p' docs/architecture-overview.md"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,260p' docs/architecture-overview.md"
    Status: in progress

## Command Finished

- Time: `2026-04-01T07:32:08-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `61`
- Summary: completed, exit 0: /bin/zsh -lc "sed -n '1,260p' docs/architecture-overview.md"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,260p' docs/architecture-overview.md"
    Status: completed
    Exit code: 0
    Output:
    # Architecture Overview

    ## Reference Docs

    - [ADR 0001: Core Runtime Architecture](/Users/kevin/code/storyteller/docs/adr/0001-core-runtime-architecture.md)
    - [Domain Model and Session State Machine](/Users/kevin/code/storyteller/docs/domain-model.md)
    - [System Diagram](/Users/kevin/code/storyteller/docs/system-diagram.md)

    ## System Picture

    Storyteller is a full-stack application with a browser client, a backend-owned workflow engine, durable relational state, durable object storage, and resumable background jobs.

    ```text
    React + Vite client
            |
            v
    FastAPI API layer
            |
            +--> domain services and policy layer
            |         |
            |         +--> AI adapters for planning, composition, and narration
            |         |
            |         +--> repositories for sessions, workflow state, jobs, and event log
            |
            +--> background workers for composition and audio generation
                      |
                      +--> PostgreSQL for durable structured state
                      +--> file-backed GCS emulator for artifacts and intermediate blobs
    ```

    ## Why Gemini Calls Must Stay on the Backend

    All Gemini access belongs on the server side for four reasons:

    1. Secrets control: provider credentials live in local `secrets.yaml` and must never enter the browser.
    2. Policy enforcement: chat-to-UI actions and workflow transitions need deterministic server validation before the model can change session state.
    3. Durable orchestration: prompts, structured outputs, retries, and model selection need to be coordinated with persistent session data and job records.
    4. Provider flexibility: keeping Gemini behind backend adapters lets the app keep a stable internal interface while model IDs, structured output tactics, or narration providers evolve.

    The frontend should only call the backend's API and subscribe to backend-owned progress events.

    ## Why Composition and Audio Must Use Resumable Server-Side Jobs

    Composition and narration are long-running operations that cannot safely live inside request threads or browser memory. They need server-side jobs because:

    - a user must be able to refresh the page or return later without losing progress
    - partial story text and audio segments need durable checkpoints
    - progress updates need a single source of truth that both chat and UI can observe
    - retries, cancellation, and resume logic need explicit job state rather than transient in-memory state

    The durable model should include job records, segment records, asset metadata, and an event log that can reconstruct session progress after interruption.

    ## Intended Backend Shape

    The target backend should separate concerns explicitly:

    - `api/`: HTTP routes and websocket endpoints
    - `settings/`: environment and secrets loading
    - `db/`: database engine, migrations, and persistence setup
    - `models/`: typed domain models and persistence schemas
    - `repositories/`: database access for sessions, events, jobs, and assets
    - `services/`: workflow logic and policy enforcement
    - `ai/`: Gemini planning, composition, and narration adapters
    - `worker/`: background job execution for writing and audio
    - `storage/`: object storage abstraction over the local GCS emulator

    ## Durable Domain Concepts

    The system should persist the following concepts as first-class records:

    - Session
    - Workflow stage
    - Event log
    - Selected genre
    - Selected tone
    - Story brief
    - Pitch batch and selected pitch
    - Character batch and selected character sheet
    - Beat sheet
    - Story setup preferences
    - Outline or chapter plan
    - Continuity bible
    - Composition job and segments
    - Audio job and segments
    - Asset metadata

    ## Current Repository State

    The repository currently contains an initial scaffold:

    - `frontend/`: Vite React TypeScript app
    - `backend/`: FastAPI app with an app factory, versioned routers, settings loader, workflow models,
      SQLAlchemy metadata, and migration-aware database helpers
    - `backend/migrations/`: Alembic home for database schema history
    - `backend/app/worker/`: reserved home for background job runners
    - `infra/compose/docker-compose.yml`: local frontend, backend, PostgreSQL, file-backed GCS emulator, and browser QA services
    - `infra/persistence/`: notes for persistent local infrastructure data
    - `scripts/dev-compose.sh`: convenience entrypoint for the Compose stack
    - `tools/webapp-qa/`: containerized browser automation support

    Background workers and most domain layers are still planned work. PostgreSQL and the file-backed GCS emulator are now available in the local Compose stack so later prompts can connect durable state and artifact storage without redefining the infrastructure contract.

    Story setup preferences such as word count, runtime, and chapter count are planning hints rather than hard limits. The system should use them to guide prompts, estimates, and editing suggestions without forcing exact compliance at the expense of story quality or bedtime tone.

## Command Started

- Time: `2026-04-01T07:32:08-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `62`
- Summary: in progress: /bin/zsh -lc 'rg -n "class .*Service|def .*enqueue|def .*create|def .*update|def .*select|def .*generate|def .*refine|def .*estimate|def .*rewrite" backend/app/services backend/app/api backend/app/worker -S'

### Full Text

    Command: /bin/zsh -lc 'rg -n "class .*Service|def .*enqueue|def .*create|def .*update|def .*select|def .*generate|def .*refine|def .*estimate|def .*rewrite" backend/app/services backend/app/api backend/app/worker -S'
    Status: in progress

## Command Finished

- Time: `2026-04-01T07:32:08-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `63`
- Summary: completed, exit 0: /bin/zsh -lc 'rg -n "class .*Service|def .*enqueue|def .*create|def .*update|def .*select|def .*generate|def .*refine|def .*estimate|def .*rewrite" backend/app/services backend/app/api backend/app/worker -S'

### Full Text

    Command: /bin/zsh -lc 'rg -n "class .*Service|def .*enqueue|def .*create|def .*update|def .*select|def .*generate|def .*refine|def .*estimate|def .*rewrite" backend/app/services backend/app/api backend/app/worker -S'
    Status: completed
    Exit code: 0
    Output:
    backend/app/api/v1/routes/sessions.py:94:def create_session(
    backend/app/api/v1/routes/sessions.py:136:def apply_session_context_update(
    backend/app/services/event_log.py:56:class SessionEventLogService:
    backend/app/services/event_log.py:107:    def record_session_created(
    backend/app/services/event_log.py:170:    def record_selection(
    backend/app/services/conversation_memory.py:36:class SessionMemoryService:
    backend/app/services/intent_parser.py:34:class SessionIntentParserService:
    backend/app/services/sessions.py:54:class SessionServiceError(Exception):
    backend/app/services/sessions.py:58:class SessionNotFoundError(SessionServiceError):
    backend/app/services/sessions.py:62:class InvalidStageTransitionError(SessionServiceError):
    backend/app/services/sessions.py:66:class UnsupportedSessionContextUpdateError(SessionServiceError):
    backend/app/services/sessions.py:81:class SessionService:
    backend/app/services/sessions.py:89:    def create_session(
    backend/app/services/sessions.py:168:    def apply_context_update(
    backend/app/services/sessions.py:254:    def update_stage_state(
    backend/app/services/sessions.py:456:def _build_catalog_selection(row) -> SessionCatalogSelection | None:
    backend/app/services/assets.py:22:class AssetServiceError(Exception):
    backend/app/services/assets.py:26:class AssetNotFoundError(AssetServiceError):
    backend/app/services/assets.py:30:class AssetSessionNotFoundError(AssetServiceError):
    backend/app/services/assets.py:34:class AssetOwnershipError(AssetServiceError):
    backend/app/services/assets.py:38:class SessionAssetService:
    backend/app/services/jobs.py:16:class BackgroundJobServiceError(Exception):
    backend/app/services/jobs.py:20:class BackgroundJobNotFoundError(BackgroundJobServiceError):
    backend/app/services/jobs.py:24:class BackgroundJobLeaseLostError(BackgroundJobServiceError):
    backend/app/services/jobs.py:62:class BackgroundJobService:
    backend/app/services/jobs.py:67:    def enqueue_job(
    backend/app/services/action_policy.py:77:class SessionActionPolicyServiceError(Exception):
    backend/app/services/action_policy.py:160:class SessionActionPolicyService:
    backend/app/services/action_policy.py:362:    def _evaluate_select_genre(
    backend/app/services/action_policy.py:414:    def _evaluate_select_tone(
    backend/app/services/action_policy.py:472:    def _evaluate_update_story_brief(
    backend/app/services/action_policy.py:490:    def _evaluate_regenerate_pitches(
    backend/app/services/action_policy.py:515:    def _evaluate_select_pitch(
    backend/app/services/action_policy.py:579:    def _evaluate_select_character_sheet(
    backend/app/services/action_policy.py:658:    def _evaluate_refine_character_sheet(
    backend/app/services/action_policy.py:690:    def _evaluate_regenerate_character_sheet(
    backend/app/services/action_policy.py:791:    def _evaluate_refine_beat_sheet(
    backend/app/services/action_policy.py:823:    def _evaluate_regenerate_beat_sheet(
    backend/app/services/action_policy.py:848:    def _evaluate_update_story_setup(
    backend/app/services/action_policy.py:1018:    def _evaluate_update_audio_settings(

## Command Started

- Time: `2026-04-01T07:32:20-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `64`
- Summary: in progress: /bin/zsh -lc "sed -n '1,320p' backend/app/models/action_policy.py"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,320p' backend/app/models/action_policy.py"
    Status: in progress

## Command Started

- Time: `2026-04-01T07:32:20-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `65`
- Summary: in progress: /bin/zsh -lc "sed -n '300,860p' backend/app/db/models.py"

### Full Text

    Command: /bin/zsh -lc "sed -n '300,860p' backend/app/db/models.py"
    Status: in progress

## Command Started

- Time: `2026-04-01T07:32:20-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `66`
- Summary: in progress: /bin/zsh -lc "sed -n '1,320p' backend/app/repositories/sessions.py"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,320p' backend/app/repositories/sessions.py"
    Status: in progress

## Command Finished

- Time: `2026-04-01T07:32:20-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `67`
- Summary: completed, exit 0: /bin/zsh -lc "sed -n '1,320p' backend/app/models/action_policy.py"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,320p' backend/app/models/action_policy.py"
    Status: completed
    Exit code: 0
    Output:
    from __future__ import annotations

    from enum import Enum

    from pydantic import BaseModel, ConfigDict, Field

    from app.models.chat_actions import ChatToUIAction, ChatToUIActionBatch, ChatToUIActionType
    from app.models.workflow import WorkflowStage

    SESSION_ACTION_POLICY_SCHEMA_VERSION = 1


    class SessionActionDecision(str, Enum):
        ACCEPTED = "accepted"
        REJECTED = "rejected"
        REQUIRES_CONFIRMATION = "requires_confirmation"
        ACCEPTED_WITH_SIDE_EFFECTS = "accepted_with_side_effects"


    class SessionActionReasonCode(str, Enum):
        CONFIRMATION_REQUIRED_BY_DEFAULT = "confirmation_required_by_default"
        CONFIRMATION_REQUIRED_DUE_TO_SIDE_EFFECTS = "confirmation_required_due_to_side_effects"
        PREREQUISITE_STAGE_INCOMPLETE = "prerequisite_stage_incomplete"
        PREREQUISITE_SELECTION_MISSING = "prerequisite_selection_missing"
        TARGET_STAGE_STALE = "target_stage_stale"
        CATALOG_ENTRY_NOT_FOUND = "catalog_entry_not_found"
        CATALOG_ENTRY_AMBIGUOUS = "catalog_entry_ambiguous"
        CATALOG_ENTRY_MISMATCH = "catalog_entry_mismatch"
        SESSION_RESOURCE_NOT_FOUND = "session_resource_not_found"
        SESSION_RESOURCE_AMBIGUOUS = "session_resource_ambiguous"
        JOB_NOT_ACTIVE = "job_not_active"
        JOB_STATE_CONFLICT = "job_state_conflict"
        ASSET_NOT_READY = "asset_not_ready"
        ASSET_REGENERATION_REQUIRED = "asset_regeneration_required"
        ACTION_IS_NOOP = "action_is_noop"


    class SessionActionSideEffectKind(str, Enum):
        INVALIDATE_STAGES = "invalidate_stages"
        STOP_ACTIVE_JOB = "stop_active_job"
        SUPERSEDE_ASSET = "supersede_asset"
        CLEAR_SELECTION = "clear_selection"


    class SessionActionPolicyReason(BaseModel):
        model_config = ConfigDict(extra="forbid")

        code: SessionActionReasonCode
        message: str = Field(min_length=1)
        stage: WorkflowStage | None = None
        related_stages: list[WorkflowStage] = Field(default_factory=list)
        related_action_types: list[ChatToUIActionType] = Field(default_factory=list)


    class SessionActionPolicySideEffect(BaseModel):
        model_config = ConfigDict(extra="forbid")

        kind: SessionActionSideEffectKind
        message: str = Field(min_length=1)
        stages: list[WorkflowStage] = Field(default_factory=list)
        selection_field: str | None = Field(default=None, min_length=1)
        job_kind: str | None = Field(default=None, min_length=1)
        asset_kind: str | None = Field(default=None, min_length=1)


    class SessionActionPolicyRequestItem(BaseModel):
        model_config = ConfigDict(extra="forbid")

        action: ChatToUIAction
        confirmation_granted: bool = False


    class SessionActionPolicyEvaluationRequest(BaseModel):
        model_config = ConfigDict(extra="forbid")

        schema_version: int = Field(default=SESSION_ACTION_POLICY_SCHEMA_VERSION, ge=1)
        actions: list[SessionActionPolicyRequestItem] = Field(default_factory=list)


    class SessionActionPolicyEvaluationItem(BaseModel):
        model_config = ConfigDict(extra="forbid")

        action_index: int = Field(ge=0)
        action_type: ChatToUIActionType
        target_stage: WorkflowStage
        decision: SessionActionDecision
        summary: str = Field(min_length=1)
        reasons: list[SessionActionPolicyReason] = Field(default_factory=list)
        side_effects: list[SessionActionPolicySideEffect] = Field(default_factory=list)
        prerequisite_action_types: list[ChatToUIActionType] = Field(default_factory=list)


    class SessionActionPolicyEvaluation(BaseModel):
        model_config = ConfigDict(extra="forbid")

        schema_version: int = Field(default=SESSION_ACTION_POLICY_SCHEMA_VERSION, ge=1)
        session_id: str
        evaluated_actions: list[SessionActionPolicyEvaluationItem] = Field(default_factory=list)


    def build_action_policy_request_from_batch(
        batch: ChatToUIActionBatch,
        *,
        confirmation_granted: bool = False,
    ) -> SessionActionPolicyEvaluationRequest:
        return SessionActionPolicyEvaluationRequest(
            actions=[
                SessionActionPolicyRequestItem(
                    action=action,
                    confirmation_granted=confirmation_granted,
                )
                for action in batch.actions
            ]
        )

## Command Finished

- Time: `2026-04-01T07:32:20-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `68`
- Summary: completed, exit 0: /bin/zsh -lc "sed -n '1,320p' backend/app/repositories/sessions.py"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,320p' backend/app/repositories/sessions.py"
    Status: completed
    Exit code: 0
    Output:
    from __future__ import annotations

    from dataclasses import dataclass

    from sqlalchemy import Select, select
    from sqlalchemy.orm import Session, selectinload

    from app.db import (
        AssetKind,
        AssetStatus,
        AudioJob,
        BeatSheet,
        CharacterSheet,
        CompositionJob,
        JobStatus,
        Pitch,
        SessionAsset,
        StoryBrief,
        StorySession,
        StorySetup,
        WorkflowStageSnapshot,
    )
    from app.models.workflow import WORKFLOW_STAGE_SEQUENCE, WorkflowStage, WorkflowStageState

    ACTIVE_JOB_STATUSES = (
        JobStatus.QUEUED,
        JobStatus.IN_PROGRESS,
        JobStatus.PAUSED,
    )
    STORY_ASSET_KINDS = (
        AssetKind.STORY_TEXT,
        AssetKind.STORY_DOCX,
    )


    @dataclass(frozen=True)
    class SessionAggregate:
        session: StorySession
        active_story_brief: StoryBrief | None
        selected_pitch: Pitch | None
        selected_character_sheet: CharacterSheet | None
        selected_beat_sheet: BeatSheet | None
        selected_story_setup: StorySetup | None
        active_composition_job: CompositionJob | None
        active_audio_job: AudioJob | None
        latest_story_asset: SessionAsset | None
        latest_audio_asset: SessionAsset | None


    class StorySessionRepository:
        def __init__(self, session: Session):
            self._session = session

        def create(self, *, working_title: str | None = None) -> StorySession:
            story_session = StorySession(working_title=working_title)
            self._session.add(story_session)
            self._session.flush()
            return story_session

        def get_by_id(self, session_id: str) -> StorySession | None:
            stmt: Select[tuple[StorySession]] = (
                select(StorySession)
                .options(
                    selectinload(StorySession.selected_genre),
                    selectinload(StorySession.selected_tone_profile),
                    selectinload(StorySession.workflow_stage_states).selectinload(
                        WorkflowStageSnapshot.last_event
                    ),
                )
                .where(StorySession.id == session_id)
            )
            return self._session.execute(stmt).scalar_one_or_none()

        def exists(self, session_id: str) -> bool:
            stmt = select(StorySession.id).where(StorySession.id == session_id).limit(1)
            return self._session.execute(stmt).scalar_one_or_none() is not None

        def get_for_update(self, session_id: str) -> StorySession | None:
            stmt: Select[tuple[StorySession]] = (
                select(StorySession)
                .options(selectinload(StorySession.workflow_stage_states))
                .where(StorySession.id == session_id)
            )
            return self._session.execute(stmt).scalar_one_or_none()

        def get_aggregate(self, session_id: str) -> SessionAggregate | None:
            story_session = self.get_by_id(session_id)
            if story_session is None:
                return None

            return SessionAggregate(
                session=story_session,
                active_story_brief=self._get_active_story_brief(session_id),
                selected_pitch=self._get_selected_pitch(session_id),
                selected_character_sheet=self._get_selected_character_sheet(session_id),
                selected_beat_sheet=self._get_selected_beat_sheet(session_id),
                selected_story_setup=self._get_selected_story_setup(session_id),
                active_composition_job=self._get_active_composition_job(session_id),
                active_audio_job=self._get_active_audio_job(session_id),
                latest_story_asset=self._get_latest_story_asset(session_id),
                latest_audio_asset=self._get_latest_audio_asset(session_id),
            )

        def list_recent(self, *, limit: int = 20) -> list[StorySession]:
            stmt: Select[tuple[StorySession]] = (
                select(StorySession)
                .options(
                    selectinload(StorySession.selected_genre),
                    selectinload(StorySession.selected_tone_profile),
                    selectinload(StorySession.workflow_stage_states),
                )
                .order_by(StorySession.updated_at.desc(), StorySession.created_at.desc())
                .limit(limit)
            )
            return list(self._session.execute(stmt).scalars().all())

        def _get_active_story_brief(self, session_id: str) -> StoryBrief | None:
            stmt: Select[tuple[StoryBrief]] = (
                select(StoryBrief)
                .where(StoryBrief.session_id == session_id, StoryBrief.is_active.is_(True))
                .order_by(StoryBrief.revision_number.desc())
                .limit(1)
            )
            return self._session.execute(stmt).scalar_one_or_none()

        def _get_selected_pitch(self, session_id: str) -> Pitch | None:
            stmt: Select[tuple[Pitch]] = (
                select(Pitch)
                .where(Pitch.session_id == session_id, Pitch.is_selected.is_(True))
                .order_by(Pitch.created_at.desc())
                .limit(1)
            )
            return self._session.execute(stmt).scalar_one_or_none()

        def _get_selected_character_sheet(self, session_id: str) -> CharacterSheet | None:
            stmt: Select[tuple[CharacterSheet]] = (
                select(CharacterSheet)
                .where(CharacterSheet.session_id == session_id, CharacterSheet.is_selected.is_(True))
                .order_by(CharacterSheet.revision_number.desc())
                .limit(1)
            )
            return self._session.execute(stmt).scalar_one_or_none()

        def _get_selected_beat_sheet(self, session_id: str) -> BeatSheet | None:
            stmt: Select[tuple[BeatSheet]] = (
                select(BeatSheet)
                .where(BeatSheet.session_id == session_id, BeatSheet.is_selected.is_(True))
                .order_by(BeatSheet.revision_number.desc())
                .limit(1)
            )
            return self._session.execute(stmt).scalar_one_or_none()

        def _get_selected_story_setup(self, session_id: str) -> StorySetup | None:
            stmt: Select[tuple[StorySetup]] = (
                select(StorySetup)
                .where(StorySetup.session_id == session_id, StorySetup.is_selected.is_(True))
                .order_by(StorySetup.revision_number.desc())
                .limit(1)
            )
            return self._session.execute(stmt).scalar_one_or_none()

        def _get_active_composition_job(self, session_id: str) -> CompositionJob | None:
            stmt: Select[tuple[CompositionJob]] = (
                select(CompositionJob)
                .where(
                    CompositionJob.session_id == session_id,
                    CompositionJob.status.in_(ACTIVE_JOB_STATUSES),
                )
                .order_by(CompositionJob.created_at.desc())
                .limit(1)
            )
            return self._session.execute(stmt).scalar_one_or_none()

        def _get_active_audio_job(self, session_id: str) -> AudioJob | None:
            stmt: Select[tuple[AudioJob]] = (
                select(AudioJob)
                .where(
                    AudioJob.session_id == session_id,
                    AudioJob.status.in_(ACTIVE_JOB_STATUSES),
                )
                .order_by(AudioJob.created_at.desc())
                .limit(1)
            )
            return self._session.execute(stmt).scalar_one_or_none()

        def _get_latest_story_asset(self, session_id: str) -> SessionAsset | None:
            stmt: Select[tuple[SessionAsset]] = (
                select(SessionAsset)
                .where(
                    SessionAsset.session_id == session_id,
                    SessionAsset.asset_kind.in_(STORY_ASSET_KINDS),
                    SessionAsset.status == AssetStatus.READY,
                )
                .order_by(SessionAsset.ready_at.desc(), SessionAsset.created_at.desc())
                .limit(1)
            )
            return self._session.execute(stmt).scalar_one_or_none()

        def _get_latest_audio_asset(self, session_id: str) -> SessionAsset | None:
            stmt: Select[tuple[SessionAsset]] = (
                select(SessionAsset)
                .where(
                    SessionAsset.session_id == session_id,
                    SessionAsset.asset_kind == AssetKind.FINAL_AUDIO,
                    SessionAsset.status == AssetStatus.READY,
                )
                .order_by(SessionAsset.ready_at.desc(), SessionAsset.created_at.desc())
                .limit(1)
            )
            return self._session.execute(stmt).scalar_one_or_none()


    class WorkflowStageStateRepository:
        def __init__(self, session: Session):
            self._session = session

        def ensure_for_session(
            self,
            story_session: StorySession,
        ) -> dict[WorkflowStage, WorkflowStageSnapshot]:
            stage_map = {row.stage: row for row in story_session.workflow_stage_states}

            for stage in WORKFLOW_STAGE_SEQUENCE:
                if stage in stage_map:
                    continue

                snapshot = WorkflowStageSnapshot(
                    stage=stage,
                    status=WorkflowStageState.DRAFT,
                )
                story_session.workflow_stage_states.append(snapshot)
                stage_map[stage] = snapshot

            self._session.flush()
            return stage_map

## Command Finished

- Time: `2026-04-01T07:32:20-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `69`
- Summary: completed, exit 0: /bin/zsh -lc "sed -n '300,860p' backend/app/db/models.py"

### Full Text

    Command: /bin/zsh -lc "sed -n '300,860p' backend/app/db/models.py"
    Status: completed
    Exit code: 0
    Output:
    __table_args__ = (
            UniqueConstraint(
                "session_id", "sequence_number", name="uq_event_log_entries_session_id_sequence_number"
            ),
            Index("ix_event_log_entries_session_id_created_at", "session_id", "created_at"),
            Index("ix_event_log_entries_session_id_stage", "session_id", "stage"),
        )


    class SessionMemorySnapshot(UUIDPrimaryKeyMixin, Base):
        __tablename__ = "session_memory_snapshots"

        session_id: Mapped[str] = mapped_column(
            String(36),
            ForeignKey("story_sessions.id", ondelete="CASCADE"),
            nullable=False,
        )
        trigger_event_id: Mapped[str | None] = mapped_column(
            String(36),
            ForeignKey("event_log_entries.id", ondelete="SET NULL"),
        )
        trigger_event_type: Mapped[str | None] = mapped_column(String(120))
        trigger_event_sequence_number: Mapped[int | None] = mapped_column(Integer)
        summary_text: Mapped[str] = mapped_column(Text, nullable=False)
        summary_data: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
        created_at: Mapped[datetime] = mapped_column(
            DateTime(timezone=True),
            nullable=False,
            default=utc_now,
        )

        session: Mapped["StorySession"] = relationship(back_populates="memory_snapshots")
        trigger_event: Mapped["EventLogEntry | None"] = relationship(back_populates="memory_snapshots")

        __table_args__ = (
            UniqueConstraint(
                "trigger_event_id",
                name="uq_session_memory_snapshots_trigger_event_id",
            ),
            Index(
                "ix_session_memory_snapshots_session_id_created_at",
                "session_id",
                "created_at",
            ),
        )


    class WorkflowStageSnapshot(UUIDPrimaryKeyMixin, TimestampMixin, Base):
        __tablename__ = "workflow_stage_states"

        session_id: Mapped[str] = mapped_column(
            String(36),
            ForeignKey("story_sessions.id", ondelete="CASCADE"),
            nullable=False,
        )
        stage: Mapped[WorkflowStage] = mapped_column(WORKFLOW_STAGE_ENUM, nullable=False)
        status: Mapped[WorkflowStageState] = mapped_column(
            WORKFLOW_STAGE_STATE_ENUM,
            nullable=False,
            default=WorkflowStageState.DRAFT,
        )
        detail: Mapped[str | None] = mapped_column(Text)
        started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
        completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
        last_event_id: Mapped[str | None] = mapped_column(
            String(36),
            ForeignKey("event_log_entries.id", ondelete="SET NULL"),
        )

        session: Mapped["StorySession"] = relationship(back_populates="workflow_stage_states")
        last_event: Mapped["EventLogEntry | None"] = relationship(
            back_populates="workflow_stage_states"
        )

        __table_args__ = (
            UniqueConstraint("session_id", "stage", name="uq_workflow_stage_states_session_id_stage"),
            Index("ix_workflow_stage_states_session_id_status", "session_id", "status"),
        )


    class StoryBrief(UUIDPrimaryKeyMixin, TimestampMixin, Base):
        __tablename__ = "story_briefs"

        session_id: Mapped[str] = mapped_column(
            String(36),
            ForeignKey("story_sessions.id", ondelete="CASCADE"),
            nullable=False,
        )
        revision_number: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
        raw_brief: Mapped[str] = mapped_column(Text, nullable=False)
        normalized_summary: Mapped[str | None] = mapped_column(Text)
        planning_notes: Mapped[str | None] = mapped_column(Text)
        model_output: Mapped[dict[str, Any] | list[Any] | None] = mapped_column(JSON)
        is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
        accepted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

        session: Mapped["StorySession"] = relationship(back_populates="story_briefs")
        pitches: Mapped[list["Pitch"]] = relationship(back_populates="story_brief")

        __table_args__ = (
            UniqueConstraint(
                "session_id", "revision_number", name="uq_story_briefs_session_id_revision_number"
            ),
            Index("ix_story_briefs_session_id_is_active", "session_id", "is_active"),
        )


    class Pitch(UUIDPrimaryKeyMixin, TimestampMixin, Base):
        __tablename__ = "pitches"

        session_id: Mapped[str] = mapped_column(
            String(36),
            ForeignKey("story_sessions.id", ondelete="CASCADE"),
            nullable=False,
        )
        story_brief_id: Mapped[str | None] = mapped_column(
            String(36),
            ForeignKey("story_briefs.id", ondelete="SET NULL"),
        )
        generation_key: Mapped[str] = mapped_column(String(80), nullable=False)
        pitch_index: Mapped[int] = mapped_column(Integer, nullable=False)
        title: Mapped[str] = mapped_column(String(255), nullable=False)
        logline: Mapped[str] = mapped_column(Text, nullable=False)
        summary: Mapped[str | None] = mapped_column(Text)
        bedtime_notes: Mapped[str | None] = mapped_column(Text)
        model_output: Mapped[dict[str, Any] | list[Any] | None] = mapped_column(JSON)
        is_selected: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
        accepted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

        session: Mapped["StorySession"] = relationship(back_populates="pitches")
        story_brief: Mapped["StoryBrief | None"] = relationship(back_populates="pitches")
        character_sheets: Mapped[list["CharacterSheet"]] = relationship(back_populates="pitch")

        __table_args__ = (
            UniqueConstraint(
                "session_id",
                "generation_key",
                "pitch_index",
                name="uq_pitches_session_id_generation_key_pitch_index",
            ),
            Index("ix_pitches_session_id_is_selected", "session_id", "is_selected"),
        )


    class CharacterSheet(UUIDPrimaryKeyMixin, TimestampMixin, Base):
        __tablename__ = "character_sheets"

        session_id: Mapped[str] = mapped_column(
            String(36),
            ForeignKey("story_sessions.id", ondelete="CASCADE"),
            nullable=False,
        )
        pitch_id: Mapped[str | None] = mapped_column(
            String(36),
            ForeignKey("pitches.id", ondelete="SET NULL"),
        )
        revision_number: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
        title: Mapped[str | None] = mapped_column(String(255))
        summary: Mapped[str | None] = mapped_column(Text)
        protagonist_name: Mapped[str | None] = mapped_column(String(120))
        supporting_cast: Mapped[dict[str, Any] | list[Any] | None] = mapped_column(JSON)
        character_data: Mapped[dict[str, Any] | list[Any] | None] = mapped_column(JSON)
        bedtime_notes: Mapped[str | None] = mapped_column(Text)
        is_selected: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
        accepted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

        session: Mapped["StorySession"] = relationship(back_populates="character_sheets")
        pitch: Mapped["Pitch | None"] = relationship(back_populates="character_sheets")
        beat_sheets: Mapped[list["BeatSheet"]] = relationship(back_populates="character_sheet")

        __table_args__ = (
            UniqueConstraint(
                "session_id",
                "revision_number",
                name="uq_character_sheets_session_id_revision_number",
            ),
            Index("ix_character_sheets_session_id_is_selected", "session_id", "is_selected"),
        )


    class BeatSheet(UUIDPrimaryKeyMixin, TimestampMixin, Base):
        __tablename__ = "beat_sheets"

        session_id: Mapped[str] = mapped_column(
            String(36),
            ForeignKey("story_sessions.id", ondelete="CASCADE"),
            nullable=False,
        )
        character_sheet_id: Mapped[str | None] = mapped_column(
            String(36),
            ForeignKey("character_sheets.id", ondelete="SET NULL"),
        )
        revision_number: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
        summary: Mapped[str | None] = mapped_column(Text)
        beats: Mapped[dict[str, Any] | list[Any] | None] = mapped_column(JSON)
        bedtime_notes: Mapped[str | None] = mapped_column(Text)
        is_selected: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
        accepted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

        session: Mapped["StorySession"] = relationship(back_populates="beat_sheets")
        character_sheet: Mapped["CharacterSheet | None"] = relationship(back_populates="beat_sheets")
        story_setups: Mapped[list["StorySetup"]] = relationship(back_populates="beat_sheet")
        composition_jobs: Mapped[list["CompositionJob"]] = relationship(back_populates="beat_sheet")

        __table_args__ = (
            UniqueConstraint(
                "session_id", "revision_number", name="uq_beat_sheets_session_id_revision_number"
            ),
            Index("ix_beat_sheets_session_id_is_selected", "session_id", "is_selected"),
        )


    class StorySetup(UUIDPrimaryKeyMixin, TimestampMixin, Base):
        __tablename__ = "story_setups"

        session_id: Mapped[str] = mapped_column(
            String(36),
            ForeignKey("story_sessions.id", ondelete="CASCADE"),
            nullable=False,
        )
        beat_sheet_id: Mapped[str | None] = mapped_column(
            String(36),
            ForeignKey("beat_sheets.id", ondelete="SET NULL"),
        )
        revision_number: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
        target_word_count: Mapped[int | None] = mapped_column(Integer)
        target_runtime_minutes: Mapped[int | None] = mapped_column(Integer)
        chapter_count: Mapped[int | None] = mapped_column(Integer)
        chapter_style: Mapped[str | None] = mapped_column(String(120))
        guidance_notes: Mapped[str | None] = mapped_column(Text)
        preferences: Mapped[dict[str, Any] | list[Any] | None] = mapped_column(JSON)
        is_selected: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
        accepted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

        session: Mapped["StorySession"] = relationship(back_populates="story_setups")
        beat_sheet: Mapped["BeatSheet | None"] = relationship(back_populates="story_setups")
        composition_jobs: Mapped[list["CompositionJob"]] = relationship(back_populates="story_setup")

        __table_args__ = (
            UniqueConstraint(
                "session_id", "revision_number", name="uq_story_setups_session_id_revision_number"
            ),
            Index("ix_story_setups_session_id_is_selected", "session_id", "is_selected"),
        )


    class CompositionJob(UUIDPrimaryKeyMixin, TimestampMixin, Base):
        __tablename__ = "composition_jobs"

        session_id: Mapped[str] = mapped_column(
            String(36),
            ForeignKey("story_sessions.id", ondelete="CASCADE"),
            nullable=False,
        )
        beat_sheet_id: Mapped[str | None] = mapped_column(
            String(36),
            ForeignKey("beat_sheets.id", ondelete="SET NULL"),
        )
        story_setup_id: Mapped[str | None] = mapped_column(
            String(36),
            ForeignKey("story_setups.id", ondelete="SET NULL"),
        )
        job_kind: Mapped[CompositionJobKind] = mapped_column(
            COMPOSITION_JOB_KIND_ENUM,
            nullable=False,
            default=CompositionJobKind.DRAFT,
        )
        status: Mapped[JobStatus] = mapped_column(
            JOB_STATUS_ENUM,
            nullable=False,
            default=JobStatus.QUEUED,
        )
        progress_percent: Mapped[float] = mapped_column(
            Numeric(5, 2, asdecimal=False),
            nullable=False,
            default=0,
        )
        current_segment_index: Mapped[int | None] = mapped_column(Integer)
        attempt_count: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
        stop_reason: Mapped[str | None] = mapped_column(String(255))
        error_message: Mapped[str | None] = mapped_column(Text)
        metadata_json: Mapped[dict[str, Any] | list[Any] | None] = mapped_column(JSON)
        started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
        completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

        session: Mapped["StorySession"] = relationship(back_populates="composition_jobs")
        beat_sheet: Mapped["BeatSheet | None"] = relationship(back_populates="composition_jobs")
        story_setup: Mapped["StorySetup | None"] = relationship(back_populates="composition_jobs")
        segments: Mapped[list["CompositionSegment"]] = relationship(
            back_populates="composition_job",
            cascade="all, delete-orphan",
        )
        assets: Mapped[list["SessionAsset"]] = relationship(back_populates="composition_job")

        __table_args__ = (
            Index(
                "ix_composition_jobs_session_id_status_created_at", "session_id", "status", "created_at"
            ),
            Index("ix_composition_jobs_session_id_job_kind", "session_id", "job_kind"),
        )


    class CompositionSegment(UUIDPrimaryKeyMixin, TimestampMixin, Base):
        __tablename__ = "composition_segments"

        session_id: Mapped[str] = mapped_column(
            String(36),
            ForeignKey("story_sessions.id", ondelete="CASCADE"),
            nullable=False,
        )
        composition_job_id: Mapped[str] = mapped_column(
            String(36),
            ForeignKey("composition_jobs.id", ondelete="CASCADE"),
            nullable=False,
        )
        superseded_by_segment_id: Mapped[str | None] = mapped_column(
            String(36),
            ForeignKey(
                "composition_segments.id",
                ondelete="SET NULL",
                name="fk_comp_segments_superseded_by",
            ),
        )
        segment_index: Mapped[int] = mapped_column(Integer, nullable=False)
        revision_number: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
        status: Mapped[JobStatus] = mapped_column(
            JOB_STATUS_ENUM,
            nullable=False,
            default=JobStatus.QUEUED,
        )
        planned_summary: Mapped[str | None] = mapped_column(Text)
        text_content: Mapped[str | None] = mapped_column(Text)
        word_count: Mapped[int | None] = mapped_column(Integer)
        payload: Mapped[dict[str, Any] | list[Any] | None] = mapped_column(JSON)
        completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

        session: Mapped["StorySession"] = relationship(back_populates="composition_segments")
        composition_job: Mapped["CompositionJob"] = relationship(back_populates="segments")
        superseded_by_segment: Mapped["CompositionSegment | None"] = relationship(
            remote_side="CompositionSegment.id"
        )
        assets: Mapped[list["SessionAsset"]] = relationship(back_populates="composition_segment")

        __table_args__ = (
            UniqueConstraint(
                "composition_job_id",
                "segment_index",
                "revision_number",
                name="uq_composition_segments_job_segment_revision",
            ),
            Index("ix_composition_segments_session_id_status", "session_id", "status"),
        )


    class AudioJob(UUIDPrimaryKeyMixin, TimestampMixin, Base):
        __tablename__ = "audio_jobs"

        session_id: Mapped[str] = mapped_column(
            String(36),
            ForeignKey("story_sessions.id", ondelete="CASCADE"),
            nullable=False,
        )
        source_composition_job_id: Mapped[str | None] = mapped_column(
            String(36),
            ForeignKey("composition_jobs.id", ondelete="SET NULL"),
        )
        status: Mapped[JobStatus] = mapped_column(
            JOB_STATUS_ENUM,
            nullable=False,
            default=JobStatus.QUEUED,
        )
        voice_key: Mapped[str | None] = mapped_column(String(120))
        playback_speed: Mapped[float] = mapped_column(
            Numeric(4, 2, asdecimal=False),
            nullable=False,
            default=1.0,
        )
        include_background_music: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
        music_profile: Mapped[str | None] = mapped_column(String(120))
        estimated_duration_seconds: Mapped[int | None] = mapped_column(Integer)
        current_segment_index: Mapped[int | None] = mapped_column(Integer)
        attempt_count: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
        stop_reason: Mapped[str | None] = mapped_column(String(255))
        error_message: Mapped[str | None] = mapped_column(Text)
        config_json: Mapped[dict[str, Any] | list[Any] | None] = mapped_column(JSON)
        started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
        completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

        session: Mapped["StorySession"] = relationship(back_populates="audio_jobs")
        source_composition_job: Mapped["CompositionJob | None"] = relationship()
        assets: Mapped[list["SessionAsset"]] = relationship(back_populates="audio_job")

        __table_args__ = (
            Index("ix_audio_jobs_session_id_status_created_at", "session_id", "status", "created_at"),
        )


    class SessionAsset(UUIDPrimaryKeyMixin, TimestampMixin, Base):
        __tablename__ = "session_assets"

        session_id: Mapped[str] = mapped_column(
            String(36),
            ForeignKey("story_sessions.id", ondelete="CASCADE"),
            nullable=False,
        )
        composition_job_id: Mapped[str | None] = mapped_column(
            String(36),
            ForeignKey("composition_jobs.id", ondelete="SET NULL"),
        )
        composition_segment_id: Mapped[str | None] = mapped_column(
            String(36),
            ForeignKey("composition_segments.id", ondelete="SET NULL"),
        )
        audio_job_id: Mapped[str | None] = mapped_column(
            String(36),
            ForeignKey("audio_jobs.id", ondelete="SET NULL"),
        )
        asset_kind: Mapped[AssetKind] = mapped_column(ASSET_KIND_ENUM, nullable=False)
        status: Mapped[AssetStatus] = mapped_column(
            ASSET_STATUS_ENUM,
            nullable=False,
            default=AssetStatus.PENDING,
        )
        storage_bucket: Mapped[str] = mapped_column(String(120), nullable=False)
        object_path: Mapped[str] = mapped_column(String(255), nullable=False)
        mime_type: Mapped[str] = mapped_column(String(120), nullable=False)
        byte_size: Mapped[int | None] = mapped_column(Integer)
        checksum_sha256: Mapped[str | None] = mapped_column(String(64))
        metadata_json: Mapped[dict[str, Any] | list[Any] | None] = mapped_column(JSON)
        segment_index: Mapped[int | None] = mapped_column(Integer)
        error_message: Mapped[str | None] = mapped_column(Text)
        ready_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
        failed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
        superseded_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

        session: Mapped["StorySession"] = relationship(back_populates="assets")
        composition_job: Mapped["CompositionJob | None"] = relationship(back_populates="assets")
        composition_segment: Mapped["CompositionSegment | None"] = relationship(back_populates="assets")
        audio_job: Mapped["AudioJob | None"] = relationship(back_populates="assets")

        __table_args__ = (
            UniqueConstraint(
                "storage_bucket", "object_path", name="uq_session_assets_storage_bucket_object_path"
            ),
            Index(
                "ix_session_assets_session_id_asset_kind_status", "session_id", "asset_kind", "status"
            ),
            Index(
                "ix_session_assets_audio_job_id_asset_kind_segment_index",
                "audio_job_id",
                "asset_kind",
                "segment_index",
            ),
            Index(
                "ix_session_assets_composition_job_id_asset_kind_segment_index",
                "composition_job_id",
                "asset_kind",
                "segment_index",
            ),
        )


    ExportAsset = SessionAsset

## Command Started

- Time: `2026-04-01T07:32:20-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `70`
- Summary: in progress: /bin/zsh -lc "sed -n '1,260p' docs/domain-model.md"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,260p' docs/domain-model.md"
    Status: in progress

## Command Finished

- Time: `2026-04-01T07:32:20-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `71`
- Summary: completed, exit 0: /bin/zsh -lc "sed -n '1,260p' docs/domain-model.md"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,260p' docs/domain-model.md"
    Status: completed
    Exit code: 0
    Output:
    # Domain Model and Session State Machine

    This document defines the durable business objects and workflow rules for a single story-creation session. The goal is to give the backend, frontend, migrations, and later AI orchestration code one shared contract for how a session progresses, pauses, rewinds, and resumes.

    ## Core Modeling Rules

    - The `story_session` is the durable unit of work.
    - Workflow truth lives on the backend, not in browser-only UI state.
    - Every workflow stage is tracked explicitly, even when later stages are generated from earlier ones.
    - Backward edits are allowed on purpose and must mark downstream outputs stale instead of silently pretending they are still current.
    - Composition and audio are long-running workflows backed by durable records, not one-shot request responses.
    - Event history is append-only and explains how the current snapshot was reached.

    ## Session Snapshot Contract

    The session snapshot returned to the UI should eventually include these fields, even if some land in later prompts:

    | Field | Purpose |
    | --- | --- |
    | `id` | Stable UUID for the story session. |
    | `working_title` | Best current human-readable label for lists and search. |
    | `current_stage` | Stage the user is actively viewing or editing right now. |
    | `resume_stage` | Earliest stage that still needs work when a session is reopened. |
    | `furthest_completed_stage` | Highest ordered stage that is still valid and completed. |
    | `overall_status` | Session-level rollup such as `draft`, `in_progress`, `completed`, or `needs_regeneration`. |
    | `selected_genre_id` | Accepted genre catalog row for the session. |
    | `selected_tone_profile_id` | Accepted tone profile row for the session. |
    | `selected_pitch_id` | Accepted pitch record. |
    | `selected_character_sheet_id` | Accepted character-sheet record. |
    | `accepted_beat_sheet_id` | Accepted beat-sheet record. |
    | `story_setup_id` | Accepted story-setup preferences record. |
    | `active_composition_job_id` | Current composition job, if writing or rewrite work is running. |
    | `active_audio_job_id` | Current audio job, if narration work is running. |
    | `latest_story_asset_id` | Most recent readable story artifact or aggregate text record. |
    | `latest_audio_asset_id` | Most recent playable final audio artifact. |
    | `created_at`, `updated_at`, `completed_at` | Audit and list-view timestamps. |

    `resume_stage` is the key anti-guessing field. The backend computes it from durable stage states so the frontend does not need to infer where to reopen a session by looking at which panels happen to have data.

    Prompt 11 keeps the relational core intentionally one-directional where practical: child records
    such as pitches, character sheets, beat sheets, and setup revisions point back to the owning
    session, and the accepted row is tracked on the child record itself. The API snapshot can still
    surface selected child IDs without forcing the first migration into a web of circular foreign keys.

    ## Major Entities

    | Entity | Durable role | Key fields | Notes |
    | --- | --- | --- | --- |
    | `story_session` | Root aggregate for one bedtime-story project. | IDs, title, stage pointers, overall status, timestamps. | Owns the current accepted choices and job pointers. |
    | `workflow_stage_state` | Per-stage state for the session. | `session_id`, `stage`, `status`, `updated_at`, `last_event_id`. | Stored explicitly so resume does not depend on sparse child tables. |
    | `genre` | Curated genre catalog entry. | slug, label, description, bedtime-safety notes, arc notes. | Backend-owned reference data. |
    | `tone_profile` | Curated tone option linked to a genre. | `genre_id`, slug, label, descriptors, bedtime notes, default planning hints. | Tone choices are filtered by genre. |
    | `story_brief` | User-authored idea plus any normalized planning summary. | raw brief text, normalized summary, revision number. | Keeps user input separate from later generated planning outputs. |
    | `pitch` | One candidate story premise. | batch or generation group, summary, hook, bedtime notes, selection flag. | `selected_pitch_id` on the session represents the accepted pitch; selection does not require a separate table. |
    | `character_sheet` | Accepted cast and character traits for the chosen direction. | protagonist/supporting cast data, revision, generation metadata. | Multiple revisions may exist; the session points at the accepted one. |
    | `beat_sheet` | Structured Save-the-Cat plan. | ordered beats, bedtime-adaptation notes, revision. | Must be editable and versioned. |
    | `story_setup` | Soft planning targets. | target words, target runtime, chapter count, chapter style, notes. | These are guides, not hard constraints. |
    | `composition_job` | Parent job record for writing or rewriting text. | status, progress, attempt count, stop reason, current segment pointer. | Not listed in the prompt title, but needed to make `composition_segment` durable and resumable. |
    | `composition_segment` | One planned or written segment of the story. | segment index, planned summary, text, revision number, superseded segment, status. | Supports interruption, partial persistence, and rewrites of earlier sections. |
    | `audio_job` | Parent job record for narration generation. | voice, speed, music setting, progress, status, compiled asset pointer. | Audio should be resumable and segment-aware. |
    | `session_asset` | Durable artifact metadata for session files and exports. | asset kind, object path, MIME type, byte size, checksum, segment index, readiness status. | Covers draft snapshots, composition segments, audio segments, `.docx`, and final audio without scanning object storage. |
    | `event_log_entry` | Append-only session history. | actor, event type, stage context, payload with `schema_version`, created_at. | Supports replay, resume hydration, debugging, and audit. |

    ## Canonical Workflow Stages

    These lowercase identifiers are the wire-format contract. API payloads should use the IDs, not numeric indexes or UI labels.

    | Order | Stage ID | UI label | Stage completes when |
    | --- | --- | --- | --- |
    | 1 | `genre` | Genre | The user accepts a genre for the session. |
    | 2 | `tone` | Tone | The user accepts a tone profile for the selected genre. |
    | 3 | `brief` | Story brief | The session has an accepted free-form brief and any required normalized summary. |
    | 4 | `pitches` | Pitches | One pitch is accepted or the user intentionally keeps a current pitch set for further refinement. |
    | 5 | `characters` | Characters | One character sheet is accepted. |
    | 6 | `beats` | Beat sheet | One beat sheet is accepted. |
    | 7 | `story_setup` | Story setup | The user accepts soft targets such as runtime and chapter plan. |
    | 8 | `composition` | Composition | The current story text is complete enough to hand off to narration. |
    | 9 | `audio` | Audio | Final narration assets are generated for the current story text and settings. |
    | 10 | `finalize` | Finalize | Read/listen/download assets are ready for the current accepted story state. |

    Current code mirrors this contract in:

    - `backend/app/models/workflow.py`
    - `frontend/src/features/session/workflowStages.ts`

    The backend remains the authority for validating transitions. The frontend should use the same literal IDs for rendering, navigation, and optimistic display only.

    ## Stage State Semantics

    The same four-state lifecycle should be used for stage rows and for generated artifacts that can become stale.

    | State | Meaning | Example |
    | --- | --- | --- |
    | `draft` | The stage has no accepted durable output yet. Partial input may exist, but the stage is not considered complete. | The user typed part of a brief but has not accepted it yet. |
    | `in_progress` | Durable work is actively being produced or updated. | Pitch generation is running, composition is streaming segments, or audio rendering is underway. |
    | `completed` | The stage has an accepted output that is still valid relative to all upstream dependencies. | A beat sheet was accepted and no upstream planning change has made it stale. |
    | `needs_regeneration` | The stage was completed before, but an upstream change made its accepted output stale. The old output may remain visible for comparison, but it is not the current source of truth. | The user edits characters after a beat sheet exists, so beats, composition, audio, and finalize become stale. |

    ### Session-Level Rollup

    The session-level `overall_status` should be derived, not manually entered:

    - `draft`: no stage has reached `completed` yet.
    - `in_progress`: at least one stage is `in_progress`, or some stages are completed but the session has not reached a valid finalization state.
    - `completed`: `finalize` is `completed` and no stage is `needs_regeneration`.
    - `needs_regeneration`: one or more stages are `needs_regeneration`, even if the session also has readable prior outputs.

    ## Allowed Forward Progression

    The default happy-path order is linear:

    `genre -> tone -> brief -> pitches -> characters -> beats -> story_setup -> composition -> audio -> finalize`

    Forward movement rule:

    - The user may enter the next stage once the current stage is `completed`.

    Resume rule:

    - On reopen, the backend should send the earliest stage whose state is not `completed`.
    - If all stages are `completed`, `resume_stage` is `finalize`.

    This is the behavior implemented by the `resolve_resume_stage` helper in both the backend and frontend contract files.

    ## Safe Backward Edits and Regeneration Rules

    Backward navigation is allowed to any already-reached earlier stage. The important rule is what happens after the user accepts a change there.

    | Edited stage | Stages marked `needs_regeneration` after acceptance |
    | --- | --- |
    | `genre` | `tone`, `brief`, `pitches`, `characters`, `beats`, `composition`, `audio`, `finalize` |
    | `tone` | `brief`, `pitches`, `characters`, `beats`, `composition`, `audio`, `finalize` |
    | `brief` | `pitches`, `characters`, `beats`, `composition`, `audio`, `finalize` |
    | `pitches` | `characters`, `beats`, `composition`, `audio`, `finalize` |
    | `characters` | `beats`, `composition`, `audio`, `finalize` |
    | `beats` | `composition`, `audio`, `finalize` |
    | `story_setup` | `composition`, `audio`, `finalize` |
    | `composition` | `audio`, `finalize` |
    | `audio` | `finalize` |
    | `finalize` | none |

    Why `story_setup` is not invalidated by earlier planning edits:

    - Word count, runtime, and chapter preferences are user intent, not generated story content.
    - They still influence later composition, but a new pitch or character sheet does not automatically erase the user's preferred target length.

    ## Composition Interruption and Rewrite Rules

    Composition is intentionally more flexible than the earlier planning stages.

    - A composition job may move between `in_progress`, paused, resumed, or cancelled states without leaving the `composition` stage.
    - Partial text is persisted segment by segment so a refresh or crash does not erase progress.
    - A rewrite request against an earlier segment creates a new `composition_job` or new segment revision rather than mutating history in place.
    - Superseded segments remain durable for comparison and audit.
    - Any accepted composition rewrite marks `audio` and `finalize` as `needs_regeneration`.
    - If the user decides the plan itself is wrong, they may navigate back to `beats` or `story_setup`, accept changes there, and let the backend mark `composition` and later stages stale.

    ## Re-entry From Past Sessions

    The system should support these reopen flows without guessing from UI state:

    1. Planning session reopened midstream:
       - Example: `genre`, `tone`, and `brief` are `completed`; `pitches` is `in_progress`.
       - Result: open the session on `resume_stage = pitches`.
    2. Finished draft reopened for upstream change:
       - Example: `composition`, `audio`, and `finalize` were `completed`, then the user edits the beat sheet.
       - Result: `composition`, `audio`, and `finalize` become `needs_regeneration`, and `resume_stage = composition`.
    3. Fully completed story reopened for reading only:
       - Example: every stage is `completed`.
       - Result: open on `resume_stage = finalize`, but still allow explicit navigation back to earlier stages for edits.

    ## Shared Enum and Constants Plan

    The repo does not yet have a generated cross-language schema package, so prompt 10 uses a boring mirrored-contract approach:

    - Backend authority: `backend/app/models/workflow.py`
    - Frontend mirror for rendering and client-side navigation: `frontend/src/features/session/workflowStages.ts`
    - Tests on both sides assert the same stage order, lifecycle states, and regeneration map.

    Rules for later prompts:

    - Keep the literal stage IDs stable once APIs start returning them.
    - Keep the literal stage-state values stable once they enter database rows or websocket payloads.
    - If a later prompt introduces JSON Schema or code generation, generate from these same identifiers instead of renaming them.
    - The backend service layer, not the frontend, decides whether a requested stage transition is valid for the current session snapshot.

## Command Started

- Time: `2026-04-01T07:32:20-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `72`
- Summary: in progress: /bin/zsh -lc "rg -n \"CompositionJob|AudioJob|Pitch\\(|CharacterSheet\\(|BeatSheet\\(|StorySetup|CompositionSegment|active_composition_job|active_audio_job|selected_pitch_id|selected_character_sheet_id|selected_beat_sheet_id|story_setup\" backend/app backend/tests -S"

### Full Text

    Command: /bin/zsh -lc "rg -n \"CompositionJob|AudioJob|Pitch\\(|CharacterSheet\\(|BeatSheet\\(|StorySetup|CompositionSegment|active_composition_job|active_audio_job|selected_pitch_id|selected_character_sheet_id|selected_beat_sheet_id|story_setup\" backend/app backend/tests -S"
    Status: in progress

## Command Finished

- Time: `2026-04-01T07:32:20-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `73`
- Summary: completed, exit 0: /bin/zsh -lc "rg -n \"CompositionJob|AudioJob|Pitch\\(|CharacterSheet\\(|BeatSheet\\(|StorySetup|CompositionSegment|active_composition_job|active_audio_job|selected_pitch_id|selected_character_sheet_id|selected_beat_sheet_id|story_setup\" backend/app backend/tests -S"

### Full Text

    Command: /bin/zsh -lc "rg -n \"CompositionJob|AudioJob|Pitch\\(|CharacterSheet\\(|BeatSheet\\(|StorySetup|CompositionSegment|active_composition_job|active_audio_job|selected_pitch_id|selected_character_sheet_id|selected_beat_sheet_id|story_setup\" backend/app backend/tests -S"
    Status: completed
    Exit code: 0
    Output:
    backend/tests/test_asset_service.py:9:    AudioJob,
    backend/tests/test_asset_service.py:11:    CompositionJob,
    backend/tests/test_asset_service.py:12:    CompositionJobKind,
    backend/tests/test_asset_service.py:13:    CompositionSegment,
    backend/tests/test_asset_service.py:57:    composition_job = CompositionJob(
    backend/tests/test_asset_service.py:59:        job_kind=CompositionJobKind.DRAFT,
    backend/tests/test_asset_service.py:65:    composition_segment = CompositionSegment(
    backend/tests/test_asset_service.py:76:    audio_job = AudioJob(
    backend/tests/test_asset_service.py:211:    composition_job = CompositionJob(
    backend/tests/test_asset_service.py:213:        job_kind=CompositionJobKind.DRAFT,
    backend/tests/test_asset_service.py:216:    audio_job = AudioJob(
    backend/app/services/conversation_memory.py:197:    if aggregate.selected_story_setup is not None:
    backend/app/services/conversation_memory.py:198:        story_setup_summary = _build_story_setup_summary(aggregate)
    backend/app/services/conversation_memory.py:199:        if story_setup_summary is not None:
    backend/app/services/conversation_memory.py:200:            preferences.append(story_setup_summary)
    backend/app/services/conversation_memory.py:202:    if aggregate.selected_story_setup is not None and aggregate.selected_story_setup.guidance_notes:
    backend/app/services/conversation_memory.py:205:            + _truncate(aggregate.selected_story_setup.guidance_notes)
    backend/app/services/conversation_memory.py:208:    if aggregate.active_audio_job is not None:
    backend/app/services/conversation_memory.py:210:            f"voice={aggregate.active_audio_job.voice_key or 'unset'}",
    backend/app/services/conversation_memory.py:211:            f"speed={aggregate.active_audio_job.playback_speed:g}",
    backend/app/services/conversation_memory.py:214:                if aggregate.active_audio_job.include_background_music
    backend/app/services/conversation_memory.py:218:        if aggregate.active_audio_job.music_profile:
    backend/app/services/conversation_memory.py:219:            audio_preferences.append(f"music_profile={aggregate.active_audio_job.music_profile}")
    backend/app/services/conversation_memory.py:249:    if aggregate.active_composition_job is not None:
    backend/app/services/conversation_memory.py:252:            status=aggregate.active_composition_job.status,
    backend/app/services/conversation_memory.py:253:            stop_reason=aggregate.active_composition_job.stop_reason,
    backend/app/services/conversation_memory.py:258:    if aggregate.active_audio_job is not None:
    backend/app/services/conversation_memory.py:261:            status=aggregate.active_audio_job.status,
    backend/app/services/conversation_memory.py:262:            stop_reason=aggregate.active_audio_job.stop_reason,
    backend/app/services/conversation_memory.py:273:    if aggregate.active_composition_job is not None:
    backend/app/services/conversation_memory.py:275:            f"Composition job: {aggregate.active_composition_job.status.value} at "
    backend/app/services/conversation_memory.py:276:            f"{aggregate.active_composition_job.progress_percent:.1f}%"
    backend/app/services/conversation_memory.py:278:        if aggregate.active_composition_job.current_segment_index is not None:
    backend/app/services/conversation_memory.py:280:                f", segment {aggregate.active_composition_job.current_segment_index}"
    backend/app/services/conversation_memory.py:284:    if aggregate.active_audio_job is not None:
    backend/app/services/conversation_memory.py:286:            f"Audio job: {aggregate.active_audio_job.status.value}, "
    backend/app/services/conversation_memory.py:287:            f"voice={aggregate.active_audio_job.voice_key or 'unset'}"
    backend/app/services/conversation_memory.py:289:        if aggregate.active_audio_job.current_segment_index is not None:
    backend/app/services/conversation_memory.py:290:            job_summary += f", segment {aggregate.active_audio_job.current_segment_index}"
    backend/app/services/conversation_memory.py:296:def _build_story_setup_summary(aggregate: SessionAggregate) -> str | None:
    backend/app/services/conversation_memory.py:297:    if aggregate.selected_story_setup is None:
    backend/app/services/conversation_memory.py:301:    if aggregate.selected_story_setup.target_word_count is not None:
    backend/app/services/conversation_memory.py:302:        setup_bits.append(f"{aggregate.selected_story_setup.target_word_count} words")
    backend/app/services/conversation_memory.py:303:    if aggregate.selected_story_setup.target_runtime_minutes is not None:
    backend/app/services/conversation_memory.py:304:        setup_bits.append(f"{aggregate.selected_story_setup.target_runtime_minutes} minutes")
    backend/app/services/conversation_memory.py:305:    if aggregate.selected_story_setup.chapter_count is not None:
    backend/app/services/conversation_memory.py:306:        setup_bits.append(f"{aggregate.selected_story_setup.chapter_count} chapters")
    backend/app/services/conversation_memory.py:307:    if aggregate.selected_story_setup.chapter_style:
    backend/app/services/conversation_memory.py:308:        setup_bits.append(aggregate.selected_story_setup.chapter_style)
    backend/app/services/agent_context.py:51:    story_setup_summary = _build_story_setup_summary(snapshot)
    backend/app/services/agent_context.py:52:    if story_setup_summary is not None:
    backend/app/services/agent_context.py:53:        lines.append(story_setup_summary)
    backend/app/services/agent_context.py:74:    if snapshot.active_composition_job is not None:
    backend/app/services/agent_context.py:77:            f"{snapshot.active_composition_job.status} at "
    backend/app/services/agent_context.py:78:            f"{snapshot.active_composition_job.progress_percent:.1f}%"
    backend/app/services/agent_context.py:81:    if snapshot.active_audio_job is not None:
    backend/app/services/agent_context.py:84:            f"{snapshot.active_audio_job.status}, "
    backend/app/services/agent_context.py:85:            f"voice={snapshot.active_audio_job.voice_key or 'unset'}"
    backend/app/services/agent_context.py:91:def _build_story_setup_summary(snapshot: SessionSnapshot) -> str | None:
    backend/app/services/agent_context.py:92:    if snapshot.selected_story_setup is None:
    backend/app/services/agent_context.py:96:    if snapshot.selected_story_setup.target_word_count is not None:
    backend/app/services/agent_context.py:97:        setup_bits.append(f"{snapshot.selected_story_setup.target_word_count} words")
    backend/app/services/agent_context.py:98:    if snapshot.selected_story_setup.target_runtime_minutes is not None:
    backend/app/services/agent_context.py:99:        setup_bits.append(f"{snapshot.selected_story_setup.target_runtime_minutes} minutes")
    backend/app/services/agent_context.py:100:    if snapshot.selected_story_setup.chapter_count is not None:
    backend/app/services/agent_context.py:101:        setup_bits.append(f"{snapshot.selected_story_setup.chapter_count} chapters")
    backend/app/services/agent_context.py:102:    if snapshot.selected_story_setup.chapter_style:
    backend/app/services/agent_context.py:103:        setup_bits.append(snapshot.selected_story_setup.chapter_style)
    backend/app/services/agent_context.py:104:    if snapshot.selected_story_setup.guidance_notes:
    backend/app/services/agent_context.py:105:        setup_bits.append(_truncate(snapshot.selected_story_setup.guidance_notes))
    backend/app/services/action_policy.py:54:    UpdateStorySetupAction,
    backend/app/services/action_policy.py:105:    selected_pitch_id: str | None
    backend/app/services/action_policy.py:106:    selected_character_sheet_id: str | None
    backend/app/services/action_policy.py:107:    selected_beat_sheet_id: str | None
    backend/app/services/action_policy.py:108:    selected_story_setup_id: str | None
    backend/app/services/action_policy.py:109:    active_composition_job_id: str | None
    backend/app/services/action_policy.py:110:    active_composition_job_status: JobStatus | None
    backend/app/services/action_policy.py:111:    active_audio_job_id: str | None
    backend/app/services/action_policy.py:112:    active_audio_job_status: JobStatus | None
    backend/app/services/action_policy.py:131:            selected_pitch_id=snapshot.selected_pitch.id if snapshot.selected_pitch else None,
    backend/app/services/action_policy.py:132:            selected_character_sheet_id=(
    backend/app/services/action_policy.py:135:            selected_beat_sheet_id=(
    backend/app/services/action_policy.py:138:            selected_story_setup_id=(
    backend/app/services/action_policy.py:139:                snapshot.selected_story_setup.id if snapshot.selected_story_setup else None
    backend/app/services/action_policy.py:141:            active_composition_job_id=(
    backend/app/services/action_policy.py:142:                snapshot.active_composition_job.id if snapshot.active_composition_job else None
    backend/app/services/action_policy.py:144:            active_composition_job_status=(
    backend/app/services/action_policy.py:145:                JobStatus(snapshot.active_composition_job.status)
    backend/app/services/action_policy.py:146:                if snapshot.active_composition_job is not None
    backend/app/services/action_policy.py:149:            active_audio_job_id=snapshot.active_audio_job.id if snapshot.active_audio_job else None,
    backend/app/services/action_policy.py:150:            active_audio_job_status=(
    backend/app/services/action_policy.py:151:                JobStatus(snapshot.active_audio_job.status)
    backend/app/services/action_policy.py:152:                if snapshot.active_audio_job is not None
    backend/app/services/action_policy.py:314:            return self._evaluate_update_story_setup(
    backend/app/services/action_policy.py:559:        if state.selected_pitch_id == pitch.id:
    backend/app/services/action_policy.py:590:        if state.selected_pitch_id is None:
    backend/app/services/action_policy.py:628:            and character_sheet.pitch_id != state.selected_pitch_id
    backend/app/services/action_policy.py:638:        if state.selected_character_sheet_id == character_sheet.id:
    backend/app/services/action_policy.py:668:        if state.selected_pitch_id is None:
    backend/app/services/action_policy.py:675:        if state.selected_character_sheet_id is None:
    backend/app/services/action_policy.py:700:        if state.selected_pitch_id is None:
    backend/app/services/action_policy.py:726:        if state.selected_character_sheet_id is None:
    backend/app/services/action_policy.py:761:            and beat_sheet.character_sheet_id != state.selected_character_sheet_id
    backend/app/services/action_policy.py:771:        if state.selected_beat_sheet_id == beat_sheet.id:
    backend/app/services/action_policy.py:801:        if state.selected_character_sheet_id is None:
    backend/app/services/action_policy.py:808:        if state.selected_beat_sheet_id is None:
    backend/app/services/action_policy.py:833:        if state.selected_character_sheet_id is None:
    backend/app/services/action_policy.py:848:    def _evaluate_update_story_setup(
    backend/app/services/action_policy.py:850:        action: UpdateStorySetupAction,
    backend/app/services/action_policy.py:858:        if state.selected_beat_sheet_id is None:
    backend/app/services/action_policy.py:883:        if state.selected_beat_sheet_id is None:
    backend/app/services/action_policy.py:890:        if state.selected_story_setup_id is None:
    backend/app/services/action_policy.py:897:        if state.active_composition_job_status in ACTIVE_JOB_STATUSES:
    backend/app/services/action_policy.py:997:        if state.active_composition_job_status not in ACTIVE_JOB_STATUSES or (
    backend/app/services/action_policy.py:998:            state.active_composition_job_id is None
    backend/app/services/action_policy.py:1039:            force_stop_current_stage_job=state.active_audio_job_status in ACTIVE_JOB_STATUSES,
    backend/app/services/action_policy.py:1064:        if state.active_audio_job_status in ACTIVE_JOB_STATUSES:
    backend/app/services/action_policy.py:1209:            job_status = state.active_composition_job_status
    backend/app/services/action_policy.py:1210:            job_id = state.active_composition_job_id
    backend/app/services/action_policy.py:1212:            job_status = state.active_audio_job_status
    backend/app/services/action_policy.py:1213:            job_id = state.active_audio_job_id
    backend/app/services/action_policy.py:1278:            and state.active_composition_job_status in ACTIVE_JOB_STATUSES
    backend/app/services/action_policy.py:1292:            and state.active_audio_job_status in ACTIVE_JOB_STATUSES
    backend/app/services/action_policy.py:1367:                state.selected_pitch_id = resolution.pitch.id
    backend/app/services/action_policy.py:1382:                state.selected_character_sheet_id = resolution.character_sheet.id
    backend/app/services/action_policy.py:1397:                state.selected_beat_sheet_id = resolution.beat_sheet.id
    backend/app/services/action_policy.py:1403:            state.selected_story_setup_id = state.selected_story_setup_id or "pending-story-setup"
    backend/app/services/action_policy.py:1409:            state.active_composition_job_id = (
    backend/app/services/action_policy.py:1410:                state.active_composition_job_id or "pending-composition"
    backend/app/services/action_policy.py:1412:            state.active_composition_job_status = JobStatus.IN_PROGRESS
    backend/app/services/action_policy.py:1420:                state.active_composition_job_status = JobStatus.PAUSED
    backend/app/services/action_policy.py:1422:                state.active_audio_job_status = JobStatus.PAUSED
    backend/app/services/action_policy.py:1427:                state.active_composition_job_status = JobStatus.IN_PROGRESS
    backend/app/services/action_policy.py:1429:                state.active_audio_job_status = JobStatus.IN_PROGRESS
    backend/app/services/action_policy.py:1433:            state.active_composition_job_status = JobStatus.IN_PROGRESS
    backend/app/services/action_policy.py:1445:            state.active_audio_job_id = state.active_audio_job_id or "pending-audio"
    backend/app/services/action_policy.py:1446:            state.active_audio_job_status = JobStatus.IN_PROGRESS
    backend/app/services/action_policy.py:1476:            state.active_composition_job_id = None
    backend/app/services/action_policy.py:1477:            state.active_composition_job_status = None
    backend/app/services/action_policy.py:1482:            state.active_audio_job_id = None
    backend/app/services/action_policy.py:1483:            state.active_audio_job_status = None
    backend/app/services/assets.py:11:    AudioJob,
    backend/app/services/assets.py:12:    CompositionJob,
    backend/app/services/assets.py:13:    CompositionSegment,
    backend/app/services/assets.py:191:    ) -> CompositionJob | None:
    backend/app/services/assets.py:195:        composition_job = self._session.get(CompositionJob, composition_job_id)
    backend/app/services/assets.py:206:    ) -> CompositionSegment | None:
    backend/app/services/assets.py:210:        composition_segment = self._session.get(CompositionSegment, composition_segment_id)
    backend/app/services/assets.py:218:    def _validate_audio_job(self, session_id: str, audio_job_id: str | None) -> AudioJob | None:
    backend/app/services/assets.py:222:        audio_job = self._session.get(AudioJob, audio_job_id)
    backend/app/services/assets.py:233:        composition_job: CompositionJob | None,
    backend/app/services/assets.py:234:        composition_segment: CompositionSegment | None,
    backend/app/services/assets.py:235:        audio_job: AudioJob | None,
    backend/tests/test_chat_action_contracts.py:100:        match="update_story_setup requires at least one structured planning preference",
    backend/tests/test_chat_action_contracts.py:108:                        "action_type": "update_story_setup",
    backend/tests/test_chat_action_contracts.py:109:                        "target_stage": "story_setup",
    backend/app/services/intent_parser.py:272:    if snapshot.selected_story_setup is not None:
    backend/app/services/intent_parser.py:274:        if snapshot.selected_story_setup.target_runtime_minutes is not None:
    backend/app/services/intent_parser.py:275:            setup_parts.append(f"~{snapshot.selected_story_setup.target_runtime_minutes} minutes")
    backend/app/services/intent_parser.py:276:        if snapshot.selected_story_setup.chapter_count is not None:
    backend/app/services/intent_parser.py:277:            setup_parts.append(f"{snapshot.selected_story_setup.chapter_count} chapters")
    backend/app/services/intent_parser.py:278:        if snapshot.selected_story_setup.target_word_count is not None:
    backend/app/services/intent_parser.py:279:            setup_parts.append(f"{snapshot.selected_story_setup.target_word_count} words")
    backend/app/services/intent_parser.py:283:    if snapshot.active_composition_job is not None:
    backend/app/services/intent_parser.py:285:            f"writing is {snapshot.active_composition_job.status.replace('_', ' ')}"
    backend/app/services/intent_parser.py:287:    elif snapshot.active_audio_job is not None:
    backend/app/services/intent_parser.py:289:            f"audio is {snapshot.active_audio_job.status.replace('_', ' ')}"
    backend/tests/test_action_policy_service.py:9:    AudioJob,
    backend/tests/test_action_policy_service.py:13:    CompositionJob,
    backend/tests/test_action_policy_service.py:14:    CompositionJobKind,
    backend/tests/test_action_policy_service.py:21:    StorySetup,
    backend/tests/test_action_policy_service.py:143:def test_policy_escalates_story_setup_edits_when_an_active_composition_job_would_be_invalidated(
    backend/tests/test_action_policy_service.py:147:    seeded = _create_story_setup_session(
    backend/tests/test_action_policy_service.py:158:                        "action_type": "update_story_setup",
    backend/tests/test_action_policy_service.py:159:                        "target_stage": "story_setup",
    backend/tests/test_action_policy_service.py:215:    seeded = _create_story_setup_session(
    backend/tests/test_action_policy_service.py:252:    seeded = _create_story_setup_session(
    backend/tests/test_action_policy_service.py:322:def _create_story_setup_session(
    backend/tests/test_action_policy_service.py:368:    pitch = Pitch(
    backend/tests/test_action_policy_service.py:381:    character_sheet = CharacterSheet(
    backend/tests/test_action_policy_service.py:393:    beat_sheet = BeatSheet(
    backend/tests/test_action_policy_service.py:404:    story_setup = StorySetup(
    backend/tests/test_action_policy_service.py:414:    db_session.add(story_setup)
    backend/tests/test_action_policy_service.py:424:        composition_job = CompositionJob(
    backend/tests/test_action_policy_service.py:427:            story_setup_id=story_setup.id,
    backend/tests/test_action_policy_service.py:428:            job_kind=CompositionJobKind.DRAFT,
    backend/tests/test_action_policy_service.py:449:        audio_job = AudioJob(
    backend/app/services/sessions.py:8:    AudioJob,
    backend/app/services/sessions.py:11:    CompositionJob,
    backend/app/services/sessions.py:18:    AudioJobView,
    backend/app/services/sessions.py:21:    CompositionJobView,
    backend/app/services/sessions.py:36:    StorySetupView,
    backend/app/services/sessions.py:441:        selected_story_setup=_build_story_setup_view(aggregate.selected_story_setup),
    backend/app/services/sessions.py:442:        active_composition_job=_build_composition_job_view(aggregate.active_composition_job),
    backend/app/services/sessions.py:443:        active_audio_job=_build_audio_job_view(aggregate.active_audio_job),
    backend/app/services/sessions.py:586:def _build_story_setup_view(row) -> StorySetupView | None:
    backend/app/services/sessions.py:590:    return StorySetupView(
    backend/app/services/sessions.py:603:def _build_composition_job_view(row: CompositionJob | None) -> CompositionJobView | None:
    backend/app/services/sessions.py:607:    return CompositionJobView(
    backend/app/services/sessions.py:623:def _build_audio_job_view(row: AudioJob | None) -> AudioJobView | None:
    backend/app/services/sessions.py:627:    return AudioJobView(
    backend/tests/test_intent_parser_service.py:102:                            "action_type": "update_story_setup",
    backend/tests/test_intent_parser_service.py:103:                            "target_stage": "story_setup",
    backend/tests/test_migrations.py:24:    "story_setups",
    backend/tests/test_conversation_memory_evals.py:8:    CompositionJob,
    backend/tests/test_conversation_memory_evals.py:9:    CompositionJobKind,
    backend/tests/test_conversation_memory_evals.py:15:    StorySetup,
    backend/tests/test_conversation_memory_evals.py:118:    old_pitch = Pitch(
    backend/tests/test_conversation_memory_evals.py:128:    stale_pitch = Pitch(
    backend/tests/test_conversation_memory_evals.py:137:    new_pitch = Pitch(
    backend/tests/test_conversation_memory_evals.py:192:    story_setup = StorySetup(
    backend/tests/test_conversation_memory_evals.py:203:    db_session.add(story_setup)
    backend/tests/test_conversation_memory_evals.py:210:        selection_id=story_setup.id,
    backend/tests/test_conversation_memory_evals.py:292:    composition_job = CompositionJob(
    backend/tests/test_conversation_memory_evals.py:294:        job_kind=CompositionJobKind.DRAFT,
    backend/tests/test_conversation_memory_evals.py:369:    story_setup = StorySetup(
    backend/tests/test_conversation_memory_evals.py:378:    db_session.add_all([brief, story_setup])
    backend/tests/test_conversation_memory_evals.py:385:        selection_id=story_setup.id,
    backend/tests/test_intent_parser_api.py:60:                            "action_type": "update_story_setup",
    backend/tests/test_intent_parser_api.py:61:                            "target_stage": "story_setup",
    backend/tests/test_intent_parser_api.py:106:    assert payload["proposed_actions"]["actions"][0]["action_type"] == "update_story_setup"
    backend/tests/test_intent_parser_api.py:123:        "update_story_setup"
    backend/tests/integration/test_data_layer.py:50:    "story_setups",
    backend/tests/test_db_models.py:9:    AudioJob,
    backend/tests/test_db_models.py:13:    CompositionJob,
    backend/tests/test_db_models.py:14:    CompositionJobKind,
    backend/tests/test_db_models.py:15:    CompositionSegment,
    backend/tests/test_db_models.py:24:    StorySetup,
    backend/tests/test_db_models.py:78:            event_type="accepted_story_setup",
    backend/tests/test_db_models.py:137:        pitch = Pitch(
    backend/tests/test_db_models.py:147:        character_sheet = CharacterSheet(
    backend/tests/test_db_models.py:156:        beat_sheet = BeatSheet(
    backend/tests/test_db_models.py:165:        story_setup = StorySetup(
    backend/tests/test_db_models.py:176:        composition_job = CompositionJob(
    backend/tests/test_db_models.py:179:            story_setup=story_setup,
    backend/tests/test_db_models.py:180:            job_kind=CompositionJobKind.DRAFT,
    backend/tests/test_db_models.py:185:        composition_segment = CompositionSegment(
    backend/tests/test_db_models.py:204:        audio_job = AudioJob(
    backend/tests/test_db_models.py:236:                story_setup,
    backend/tests/test_db_models.py:299:            "story_setups",
    backend/tests/test_session_service.py:9:    AudioJob,
    backend/tests/test_session_service.py:13:    CompositionJob,
    backend/tests/test_session_service.py:14:    CompositionJobKind,
    backend/tests/test_session_service.py:23:    StorySetup,
    backend/tests/test_session_service.py:178:    pitch = Pitch(
    backend/tests/test_session_service.py:193:    character_sheet = CharacterSheet(
    backend/tests/test_session_service.py:208:    beat_sheet = BeatSheet(
    backend/tests/test_session_service.py:221:    story_setup = StorySetup(
    backend/tests/test_session_service.py:234:    db_session.add(story_setup)
    backend/tests/test_session_service.py:237:    composition_job = CompositionJob(
    backend/tests/test_session_service.py:240:        story_setup_id=story_setup.id,
    backend/tests/test_session_service.py:241:        job_kind=CompositionJobKind.DRAFT,
    backend/tests/test_session_service.py:249:    audio_job = AudioJob(
    backend/tests/test_session_service.py:297:    assert snapshot.selected_story_setup is not None
    backend/tests/test_session_service.py:298:    assert snapshot.active_composition_job is not None
    backend/tests/test_session_service.py:299:    assert snapshot.active_audio_job is not None
    backend/app/models/workflow.py:15:    STORY_SETUP = "story_setup"
    backend/app/models/events.py:33:    STORY_SETUP = "story_setup"
    backend/app/models/events.py:40:    STORY_SETUP = "story_setup"
    backend/app/models/events.py:50:    STORY_SETUP = "story_setup"
    backend/app/models/chat_actions.py:26:    UPDATE_STORY_SETUP = "update_story_setup"
    backend/app/models/chat_actions.py:260:class UpdateStorySetupValues(ChatToUIExtractedValues):
    backend/app/models/chat_actions.py:268:    def validate_story_setup(self) -> UpdateStorySetupValues:
    backend/app/models/chat_actions.py:278:                "update_story_setup requires at least one structured planning preference"
    backend/app/models/chat_actions.py:455:class UpdateStorySetupAction(ChatToUIActionBase):
    backend/app/models/chat_actions.py:460:    extracted_values: UpdateStorySetupValues
    backend/app/models/chat_actions.py:558:    | UpdateStorySetupAction
    backend/app/ai/intent_parser.py:131:        "action_type": "update_story_setup",
    backend/app/ai/intent_parser.py:132:        "stage": "story_setup",
    backend/app/models/__init__.py:72:    UpdateStorySetupAction,
    backend/app/models/__init__.py:73:    UpdateStorySetupValues,
    backend/app/models/__init__.py:150:    AudioJobView,
    backend/app/models/__init__.py:153:    CompositionJobView,
    backend/app/models/__init__.py:171:    StorySetupView,
    backend/app/models/__init__.py:191:    "AudioJobView",
    backend/app/models/__init__.py:218:    "CompositionJobView",
    backend/app/models/__init__.py:324:    "StorySetupView",
    backend/app/models/__init__.py:333:    "UpdateStorySetupAction",
    backend/app/models/__init__.py:334:    "UpdateStorySetupValues",
    backend/app/db/models.py:52:class CompositionJobKind(str, Enum):
    backend/app/db/models.py:77:COMPOSITION_JOB_KIND_ENUM = build_enum(CompositionJobKind, "composition_job_kind")
    backend/app/db/models.py:185:    story_setups: Mapped[list["StorySetup"]] = relationship(
    backend/app/db/models.py:189:    composition_jobs: Mapped[list["CompositionJob"]] = relationship(
    backend/app/db/models.py:197:    composition_segments: Mapped[list["CompositionSegment"]] = relationship(
    backend/app/db/models.py:201:    audio_jobs: Mapped[list["AudioJob"]] = relationship(
    backend/app/db/models.py:407:class Pitch(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    backend/app/db/models.py:444:class CharacterSheet(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    backend/app/db/models.py:480:class BeatSheet(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    backend/app/db/models.py:501:    story_setups: Mapped[list["StorySetup"]] = relationship(back_populates="beat_sheet")
    backend/app/db/models.py:502:    composition_jobs: Mapped[list["CompositionJob"]] = relationship(back_populates="beat_sheet")
    backend/app/db/models.py:512:class StorySetup(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    backend/app/db/models.py:513:    __tablename__ = "story_setups"
    backend/app/db/models.py:534:    session: Mapped["StorySession"] = relationship(back_populates="story_setups")
    backend/app/db/models.py:535:    beat_sheet: Mapped["BeatSheet | None"] = relationship(back_populates="story_setups")
    backend/app/db/models.py:536:    composition_jobs: Mapped[list["CompositionJob"]] = relationship(back_populates="story_setup")
    backend/app/db/models.py:540:            "session_id", "revision_number", name="uq_story_setups_session_id_revision_number"
    backend/app/db/models.py:542:        Index("ix_story_setups_session_id_is_selected", "session_id", "is_selected"),
    backend/app/db/models.py:546:class CompositionJob(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    backend/app/db/models.py:558:    story_setup_id: Mapped[str | None] = mapped_column(
    backend/app/db/models.py:560:        ForeignKey("story_setups.id", ondelete="SET NULL"),
    backend/app/db/models.py:562:    job_kind: Mapped[CompositionJobKind] = mapped_column(
    backend/app/db/models.py:565:        default=CompositionJobKind.DRAFT,
    backend/app/db/models.py:587:    story_setup: Mapped["StorySetup | None"] = relationship(back_populates="composition_jobs")
    backend/app/db/models.py:588:    segments: Mapped[list["CompositionSegment"]] = relationship(
    backend/app/db/models.py:602:class CompositionSegment(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    backend/app/db/models.py:637:    composition_job: Mapped["CompositionJob"] = relationship(back_populates="segments")
    backend/app/db/models.py:638:    superseded_by_segment: Mapped["CompositionSegment | None"] = relationship(
    backend/app/db/models.py:639:        remote_side="CompositionSegment.id"
    backend/app/db/models.py:654:class AudioJob(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    backend/app/db/models.py:689:    source_composition_job: Mapped["CompositionJob | None"] = relationship()
    backend/app/db/models.py:736:    composition_job: Mapped["CompositionJob | None"] = relationship(back_populates="assets")
    backend/app/db/models.py:737:    composition_segment: Mapped["CompositionSegment | None"] = relationship(back_populates="assets")
    backend/app/db/models.py:738:    audio_job: Mapped["AudioJob | None"] = relationship(back_populates="assets")
    backend/app/db/__init__.py:12:    AudioJob,
    backend/app/db/__init__.py:16:    CompositionJob,
    backend/app/db/__init__.py:17:    CompositionJobKind,
    backend/app/db/__init__.py:18:    CompositionSegment,
    backend/app/db/__init__.py:29:    StorySetup,
    backend/app/db/__init__.py:46:    "AudioJob",
    backend/app/db/__init__.py:50:    "CompositionJob",
    backend/app/db/__init__.py:51:    "CompositionJobKind",
    backend/app/db/__init__.py:52:    "CompositionSegment",
    backend/app/db/__init__.py:63:    "StorySetup",
    backend/app/models/session.py:78:class StorySetupView(BaseModel):
    backend/app/models/session.py:90:class CompositionJobView(BaseModel):
    backend/app/models/session.py:105:class AudioJobView(BaseModel):
    backend/app/models/session.py:231:    selected_story_setup: StorySetupView | None = None
    backend/app/models/session.py:232:    active_composition_job: CompositionJobView | None = None
    backend/app/models/session.py:233:    active_audio_job: AudioJobView | None = None
    backend/app/repositories/sessions.py:11:    AudioJob,
    backend/app/repositories/sessions.py:14:    CompositionJob,
    backend/app/repositories/sessions.py:20:    StorySetup,
    backend/app/repositories/sessions.py:43:    selected_story_setup: StorySetup | None
    backend/app/repositories/sessions.py:44:    active_composition_job: CompositionJob | None
    backend/app/repositories/sessions.py:45:    active_audio_job: AudioJob | None
    backend/app/repositories/sessions.py:97:            selected_story_setup=self._get_selected_story_setup(session_id),
    backend/app/repositories/sessions.py:98:            active_composition_job=self._get_active_composition_job(session_id),
    backend/app/repositories/sessions.py:99:            active_audio_job=self._get_active_audio_job(session_id),
    backend/app/repositories/sessions.py:153:    def _get_selected_story_setup(self, session_id: str) -> StorySetup | None:
    backend/app/repositories/sessions.py:154:        stmt: Select[tuple[StorySetup]] = (
    backend/app/repositories/sessions.py:155:            select(StorySetup)
    backend/app/repositories/sessions.py:156:            .where(StorySetup.session_id == session_id, StorySetup.is_selected.is_(True))
    backend/app/repositories/sessions.py:157:            .order_by(StorySetup.revision_number.desc())
    backend/app/repositories/sessions.py:162:    def _get_active_composition_job(self, session_id: str) -> CompositionJob | None:
    backend/app/repositories/sessions.py:163:        stmt: Select[tuple[CompositionJob]] = (
    backend/app/repositories/sessions.py:164:            select(CompositionJob)
    backend/app/repositories/sessions.py:166:                CompositionJob.session_id == session_id,
    backend/app/repositories/sessions.py:167:                CompositionJob.status.in_(ACTIVE_JOB_STATUSES),
    backend/app/repositories/sessions.py:169:            .order_by(CompositionJob.created_at.desc())
    backend/app/repositories/sessions.py:174:    def _get_active_audio_job(self, session_id: str) -> AudioJob | None:
    backend/app/repositories/sessions.py:175:        stmt: Select[tuple[AudioJob]] = (
    backend/app/repositories/sessions.py:176:            select(AudioJob)
    backend/app/repositories/sessions.py:178:                AudioJob.session_id == session_id,
    backend/app/repositories/sessions.py:179:                AudioJob.status.in_(ACTIVE_JOB_STATUSES),
    backend/app/repositories/sessions.py:181:            .order_by(AudioJob.created_at.desc())

## Agent Message

- Time: `2026-04-01T07:32:54-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `74`
- Summary: I have enough context to sketch the implementation shape. I’m checking the worker runtime and event log interfaces now so the new registry can describe side effects precisely and wire cleanly into job execution instead of staying purely...

### Full Text

    I have enough context to sketch the implementation shape. I’m checking the worker runtime and event log interfaces now so the new registry can describe side effects precisely and wire cleanly into job execution instead of staying purely declarative.

## Command Started

- Time: `2026-04-01T07:32:54-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `75`
- Summary: in progress: /bin/zsh -lc "sed -n '1,340p' backend/app/worker/runtime.py"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,340p' backend/app/worker/runtime.py"
    Status: in progress

## Command Finished

- Time: `2026-04-01T07:32:54-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `76`
- Summary: completed, exit 0: /bin/zsh -lc "sed -n '1,340p' backend/app/worker/runtime.py"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,340p' backend/app/worker/runtime.py"
    Status: completed
    Exit code: 0
    Output:
    from __future__ import annotations

    import logging
    import time
    from dataclasses import dataclass
    from datetime import timedelta
    from typing import Callable

    from sqlalchemy.exc import SQLAlchemyError
    from sqlalchemy.orm import Session, sessionmaker

    from app.services import (
        BackgroundJobLeaseLostError,
        BackgroundJobRecord,
        BackgroundJobService,
        ClaimedBackgroundJob,
    )
    from app.worker.registry import JobHandlerRegistry

    logger = logging.getLogger(__name__)


    @dataclass
    class JobExecutionContext:
        claim: ClaimedBackgroundJob
        worker_id: str
        _heartbeat_callback: Callable[[], BackgroundJobRecord]

        @property
        def job_id(self) -> str:
            return self.claim.id

        @property
        def job_type(self) -> str:
            return self.claim.job_type

        @property
        def session_id(self) -> str | None:
            return self.claim.session_id

        @property
        def attempt_count(self) -> int:
            return self.claim.attempt_count

        def heartbeat(self) -> BackgroundJobRecord:
            return self._heartbeat_callback()


    class JobWorker:
        def __init__(
            self,
            *,
            session_factory: sessionmaker[Session],
            registry: JobHandlerRegistry,
            worker_id: str,
            lease_duration: timedelta,
            poll_interval_seconds: float,
        ) -> None:
            self._session_factory = session_factory
            self._registry = registry
            self._worker_id = worker_id
            self._lease_duration = lease_duration
            self._poll_interval_seconds = poll_interval_seconds

        def run_once(self) -> bool:
            claim = self._with_job_service(
                lambda service: service.claim_next_job(
                    lease_owner=self._worker_id,
                    lease_duration=self._lease_duration,
                )
            )
            if claim is None:
                return False

            handler = self._registry.get(claim.job_type)
            if handler is None:
                self._mark_job_failed(
                    claim,
                    error_message=f"No handler registered for job type {claim.job_type!r}.",
                )
                return True

            logger.info(
                "Worker %s claimed job %s (%s) attempt %s",
                self._worker_id,
                claim.id,
                claim.job_type,
                claim.attempt_count,
            )

            context = JobExecutionContext(
                claim=claim,
                worker_id=self._worker_id,
                _heartbeat_callback=lambda: self._with_job_service(
                    lambda service: service.heartbeat_job(
                        claim,
                        lease_duration=self._lease_duration,
                    )
                ),
            )

            try:
                result_summary = handler(claim.payload, context)
            except BackgroundJobLeaseLostError:
                logger.warning(
                    "Worker %s lost its lease while running job %s",
                    self._worker_id,
                    claim.id,
                )
                return True
            except Exception as exc:  # pragma: no cover - exercised in tests via failure record
                logger.exception(
                    "Worker %s failed job %s (%s)",
                    self._worker_id,
                    claim.id,
                    claim.job_type,
                )
                self._mark_job_failed(
                    claim,
                    error_message=_format_exception_message(exc),
                    result_summary={
                        "exception_type": exc.__class__.__name__,
                        "worker_id": self._worker_id,
                    },
                )
                return True

            try:
                completed = self._with_job_service(
                    lambda service: service.complete_job(
                        claim,
                        result_summary=result_summary,
                    )
                )
            except BackgroundJobLeaseLostError:
                logger.warning(
                    "Worker %s lost its lease before completing job %s",
                    self._worker_id,
                    claim.id,
                )
                return True

            logger.info(
                "Worker %s completed job %s with status %s",
                self._worker_id,
                completed.id,
                completed.status.value,
            )
            return True

        def run_forever(self) -> None:
            logger.info(
                "Worker %s listening for jobs. Registered handlers: %s",
                self._worker_id,
                ", ".join(self._registry.registered_job_types()) or "none",
            )
            while True:
                try:
                    processed = self.run_once()
                except SQLAlchemyError:
                    logger.exception(
                        "Worker %s could not poll the durable queue. "
                        "Check database connectivity and migrations.",
                        self._worker_id,
                    )
                    time.sleep(self._poll_interval_seconds)
                    continue
                if processed:
                    continue
                time.sleep(self._poll_interval_seconds)

        def _mark_job_failed(
            self,
            claim: ClaimedBackgroundJob,
            *,
            error_message: str,
            result_summary: dict | list | None = None,
        ) -> None:
            try:
                failed = self._with_job_service(
                    lambda service: service.fail_job(
                        claim,
                        error_message=error_message,
                        result_summary=result_summary,
                    )
                )
            except BackgroundJobLeaseLostError:
                logger.warning(
                    "Worker %s lost its lease before failing job %s",
                    self._worker_id,
                    claim.id,
                )
                return

            logger.info(
                "Worker %s marked job %s as %s",
                self._worker_id,
                failed.id,
                failed.status.value,
            )

        def _with_job_service(self, operation: Callable[[BackgroundJobService], object]) -> object:
            session = self._session_factory()

            try:
                return operation(BackgroundJobService(session))
            except Exception:
                session.rollback()
                raise
            finally:
                session.close()


    def _format_exception_message(exc: Exception) -> str:
        message = str(exc).strip()
        return message or exc.__class__.__name__

## Command Started

- Time: `2026-04-01T07:32:54-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `77`
- Summary: in progress: /bin/zsh -lc "sed -n '1,260p' backend/app/worker/__init__.py"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,260p' backend/app/worker/__init__.py"
    Status: in progress

## Command Started

- Time: `2026-04-01T07:32:54-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `78`
- Summary: in progress: /bin/zsh -lc "sed -n '1,320p' backend/app/services/event_log.py"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,320p' backend/app/services/event_log.py"
    Status: in progress

## Command Finished

- Time: `2026-04-01T07:32:54-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `79`
- Summary: completed, exit 0: /bin/zsh -lc "sed -n '1,260p' backend/app/worker/__init__.py"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,260p' backend/app/worker/__init__.py"
    Status: completed
    Exit code: 0
    Output:
    from app.worker.default_handlers import build_default_job_handler_registry
    from app.worker.registry import JobHandlerRegistry
    from app.worker.runtime import JobExecutionContext, JobWorker

    __all__ = [
        "JobExecutionContext",
        "JobHandlerRegistry",
        "JobWorker",
        "build_default_job_handler_registry",
    ]

## Command Finished

- Time: `2026-04-01T07:32:54-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `80`
- Summary: completed, exit 0: /bin/zsh -lc "sed -n '1,320p' backend/app/services/event_log.py"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,320p' backend/app/services/event_log.py"
    Status: completed
    Exit code: 0
    Output:
    from __future__ import annotations

    from collections.abc import Mapping, Sequence
    from enum import Enum
    from typing import Any

    from sqlalchemy.orm import Session

    from app.db import EventActorType, EventLogEntry
    from app.models import WorkflowStage, WorkflowStageState
    from app.models.events import (
        AIOutputKind,
        AIOutputRecordedEventPayload,
        AudioProgressEventPayload,
        ChatIntentParsedEventPayload,
        ChatMessageRecordedEventPayload,
        ChatMessageRole,
        CompositionProgressEventPayload,
        EventPayload,
        SelectionKind,
        SelectionRecordedEventPayload,
        SessionCreatedEventPayload,
        SessionEventActor,
        SessionEventType,
        SessionEventView,
        SessionHistoryView,
        UIActionRecordedEventPayload,
        UserEditRecordedEventPayload,
        UserEditTargetKind,
        WorkflowStageChangedEventPayload,
        parse_event_payload,
        serialize_event_payload,
    )
    from app.models.intent_parser import ParsedChatIntentResponse
    from app.repositories import EventLogRepository
    from app.services.conversation_memory import SessionMemoryService

    DEFAULT_LOCAL_USER_ACTOR = SessionEventActor(
        actor_type=EventActorType.USER,
        actor_id="local-user",
    )
    DEFAULT_ASSISTANT_ACTOR = SessionEventActor(
        actor_type=EventActorType.ASSISTANT,
        actor_id="story-planner",
    )
    DEFAULT_SYSTEM_ACTOR = SessionEventActor(
        actor_type=EventActorType.SYSTEM,
        actor_id="worker",
    )
    DEFAULT_INTENT_PARSER_ACTOR = SessionEventActor(
        actor_type=EventActorType.SERVICE,
        actor_id="intent-parser",
    )


    class SessionEventLogService:
        def __init__(self, session: Session):
            self._session = session
            self._events = EventLogRepository(session)

        def append_event(
            self,
            session_id: str,
            *,
            actor: SessionEventActor,
            event_type: SessionEventType | str,
            summary: str,
            payload: EventPayload | Mapping[str, Any] | None = None,
            stage: WorkflowStage | None = None,
        ) -> EventLogEntry:
            normalized_summary = summary.strip()
            if not normalized_summary:
                raise ValueError("event summary must not be empty")

            return self._events.append(
                session_id=session_id,
                actor_type=actor.actor_type,
                actor_id=actor.actor_id,
                event_type=_enum_value(event_type),
                summary=normalized_summary,
                payload=serialize_event_payload(payload),
                stage=stage,
            )

        def list_session_history(
            self,
            session_id: str,
            *,
            limit: int | None = None,
            after_sequence_number: int | None = None,
        ) -> SessionHistoryView:
            rows = self._events.list_for_session(
                session_id,
                limit=limit,
                after_sequence_number=after_sequence_number,
            )
            latest_sequence_number = self._events.get_latest_sequence_number(session_id)
            return SessionHistoryView(
                session_id=session_id,
                latest_sequence_number=latest_sequence_number,
                events=[_build_session_event_view(row) for row in rows],
            )

        def build_event_view(self, entry: EventLogEntry) -> SessionEventView:
            return _build_session_event_view(entry)

        def record_session_created(
            self,
            session_id: str,
            *,
            working_title: str | None,
            actor: SessionEventActor | None = None,
        ) -> EventLogEntry:
            title = working_title or "Untitled bedtime story"
            event = self.append_event(
                session_id,
                actor=actor or DEFAULT_LOCAL_USER_ACTOR,
                event_type=SessionEventType.SESSION_CREATED,
                summary=f"Created session: {title}.",
                payload=SessionCreatedEventPayload(working_title=working_title),
            )
            self._refresh_memory_snapshot(session_id, event)
            return event

        def record_stage_state_changed(
            self,
            session_id: str,
            *,
            stage: WorkflowStage,
            previous_status: WorkflowStageState,
            status: WorkflowStageState,
            detail: str | None,
            invalidated_stages: Sequence[WorkflowStage],
            current_stage: WorkflowStage,
            resume_stage: WorkflowStage,
            furthest_completed_stage: WorkflowStage | None,
            overall_status: WorkflowStageState,
            actor: SessionEventActor | None = None,
        ) -> EventLogEntry:
            invalidated = list(invalidated_stages)
            if invalidated:
                invalidated_summary = ", ".join(stage_id.value for stage_id in invalidated)
                summary = (
                    f"Updated {stage.value} stage to {status.value} and invalidated "
                    f"{invalidated_summary}."
                )
            else:
                summary = f"Updated {stage.value} stage to {status.value}."

            event = self.append_event(
                session_id,
                actor=actor or DEFAULT_LOCAL_USER_ACTOR,
                event_type=SessionEventType.WORKFLOW_STAGE_CHANGED,
                summary=summary,
                stage=stage,
                payload=WorkflowStageChangedEventPayload(
                    previous_status=previous_status,
                    status=status,
                    detail=detail,
                    invalidated_stages=invalidated,
                    current_stage=current_stage,
                    resume_stage=resume_stage,
                    furthest_completed_stage=furthest_completed_stage,
                    overall_status=overall_status,
                ),
            )
            self._refresh_memory_snapshot(session_id, event)
            return event

        def record_selection(
            self,
            session_id: str,
            *,
            selection_kind: SelectionKind,
            stage: WorkflowStage | None,
            label: str | None = None,
            selection_id: str | None = None,
            slug: str | None = None,
            previous_selection_id: str | None = None,
            source: str = "ui",
            accepted: bool = True,
            actor: SessionEventActor | None = None,
        ) -> EventLogEntry:
            selection_label = label or slug or selection_id or selection_kind.value
            action = "Selected" if accepted else "Recorded candidate"
            event = self.append_event(
                session_id,
                actor=actor or DEFAULT_LOCAL_USER_ACTOR,
                event_type=SessionEventType.SELECTION_RECORDED,
                summary=f"{action} {selection_kind.value.replace('_', ' ')}: {selection_label}.",
                stage=stage,
                payload=SelectionRecordedEventPayload(
                    selection_kind=selection_kind,
                    selection_id=selection_id,
                    slug=slug,
                    label=label,
                    previous_selection_id=previous_selection_id,
                    source=source,
                    accepted=accepted,
                ),
            )
            self._refresh_memory_snapshot(session_id, event)
            return event

        def record_ai_output(
            self,
            session_id: str,
            *,
            output_kind: AIOutputKind,
            stage: WorkflowStage | None,
            resource_id: str | None = None,
            generation_key: str | None = None,
            candidate_count: int | None = None,
            model_id: str | None = None,
            summary_text: str | None = None,
            actor: SessionEventActor | None = None,
        ) -> EventLogEntry:
            return self.append_event(
                session_id,
                actor=actor or DEFAULT_ASSISTANT_ACTOR,
                event_type=SessionEventType.AI_OUTPUT_RECORDED,
                summary=f"Recorded AI output for {output_kind.value}.",
                stage=stage,
                payload=AIOutputRecordedEventPayload(
                    output_kind=output_kind,
                    resource_id=resource_id,
                    generation_key=generation_key,
                    candidate_count=candidate_count,
                    model_id=model_id,
                    summary=summary_text,
                ),
            )

        def record_user_edit(
            self,
            session_id: str,
            *,
            target_kind: UserEditTargetKind,
            stage: WorkflowStage | None,
            changed_fields: Sequence[str],
            target_id: str | None = None,
            revision_number: int | None = None,
            source: str = "ui",
            field_values: Mapping[str, Any] | None = None,
            summary_text: str | None = None,
            actor: SessionEventActor | None = None,
        ) -> EventLogEntry:
            event = self.append_event(
                session_id,
                actor=actor or DEFAULT_LOCAL_USER_ACTOR,
                event_type=SessionEventType.USER_EDIT_RECORDED,
                summary=f"Saved user edit for {target_kind.value.replace('_', ' ')}.",
                stage=stage,
                payload=UserEditRecordedEventPayload(
                    target_kind=target_kind,
                    target_id=target_id,
                    revision_number=revision_number,
                    changed_fields=list(changed_fields),
                    source=source,
                    field_values=dict(field_values) if field_values is not None else None,
                    summary_text=summary_text,
                ),
            )
            self._refresh_memory_snapshot(session_id, event)
            return event

        def record_chat_message(
            self,
            session_id: str,
            *,
            message_role: ChatMessageRole,
            content: str,
            stage: WorkflowStage | None = None,
            message_id: str | None = None,
            source: str = "chat",
            actor: SessionEventActor | None = None,
        ) -> EventLogEntry:
            normalized_content = content.strip()
            return self.append_event(
                session_id,
                actor=actor or _default_actor_for_chat_role(message_role),
                event_type=SessionEventType.CHAT_MESSAGE_RECORDED,
                summary=f"Recorded {message_role.value} chat message.",
                stage=stage,
                payload=ChatMessageRecordedEventPayload(
                    message_role=message_role,
                    message_id=message_id,
                    content_preview=_truncate_preview(normalized_content),
                    content_length=len(normalized_content),
                    source=source,
                ),
            )

        def record_chat_intent_parsed(
            self,
            session_id: str,
            *,
            prompt_version: str,
            model_id: str,
            current_stage: WorkflowStage,
            stage_label: str,
            stage_description: str,
            stage_status: WorkflowStageState,
            stage_detail: str | None,
            session_summary: str,
            user_message: str,
            rendered_prompt: str,
            result: ParsedChatIntentResponse,
            raw_response: Mapping[str, Any] | list[Any] | str | None = None,
            actor: SessionEventActor | None = None,
        ) -> EventLogEntry:
            action_count = len(result.proposed_actions.actions)
            if action_count == 0:
                summary = "Parsed chat intent without actionable UI changes."
            elif action_count == 1:
                summary = "Parsed chat intent into 1 proposed action."
            else:
                summary = f"Parsed chat intent into {action_count} proposed actions."

            return self.append_event(

## Command Started

- Time: `2026-04-01T07:32:54-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `81`
- Summary: in progress: /bin/zsh -lc "sed -n '1,240p' backend/app/services/__init__.py"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,240p' backend/app/services/__init__.py"
    Status: in progress

## Command Finished

- Time: `2026-04-01T07:32:54-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `82`
- Summary: completed, exit 0: /bin/zsh -lc "sed -n '1,240p' backend/app/services/__init__.py"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,240p' backend/app/services/__init__.py"
    Status: completed
    Exit code: 0
    Output:
    """Domain services for the Storyteller backend."""

    from app.services.action_policy import (
        SessionActionPolicyService,
        SessionActionPolicyServiceError,
    )
    from app.services.assets import (
        AssetNotFoundError,
        AssetOwnershipError,
        AssetServiceError,
        AssetSessionNotFoundError,
        SessionAssetService,
    )
    from app.services.conversation_memory import SessionMemoryService
    from app.services.event_log import SessionEventLogService
    from app.services.intent_parser import SessionIntentParserService
    from app.services.jobs import (
        BackgroundJobLeaseLostError,
        BackgroundJobNotFoundError,
        BackgroundJobRecord,
        BackgroundJobService,
        BackgroundJobServiceError,
        ClaimedBackgroundJob,
    )
    from app.services.sessions import (
        InvalidStageTransitionError,
        SessionNotFoundError,
        SessionService,
        SessionServiceError,
        UnsupportedSessionContextUpdateError,
    )

    __all__ = [
        "AssetNotFoundError",
        "AssetOwnershipError",
        "AssetServiceError",
        "AssetSessionNotFoundError",
        "BackgroundJobLeaseLostError",
        "BackgroundJobNotFoundError",
        "BackgroundJobRecord",
        "BackgroundJobService",
        "BackgroundJobServiceError",
        "ClaimedBackgroundJob",
        "InvalidStageTransitionError",
        "SessionActionPolicyService",
        "SessionActionPolicyServiceError",
        "SessionIntentParserService",
        "SessionMemoryService",
        "SessionNotFoundError",
        "SessionAssetService",
        "SessionEventLogService",
        "SessionService",
        "SessionServiceError",
        "UnsupportedSessionContextUpdateError",
    ]

## Command Started

- Time: `2026-04-01T07:32:54-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `83`
- Summary: in progress: /bin/zsh -lc "sed -n '1,260p' backend/app/models/__init__.py"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,260p' backend/app/models/__init__.py"
    Status: in progress

## Command Finished

- Time: `2026-04-01T07:32:54-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `84`
- Summary: completed, exit 0: /bin/zsh -lc "sed -n '1,260p' backend/app/models/__init__.py"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,260p' backend/app/models/__init__.py"
    Status: completed
    Exit code: 0
    Output:
    from app.models.action_policy import (
        SESSION_ACTION_POLICY_SCHEMA_VERSION,
        SessionActionDecision,
        SessionActionPolicyEvaluation,
        SessionActionPolicyEvaluationItem,
        SessionActionPolicyEvaluationRequest,
        SessionActionPolicyReason,
        SessionActionPolicyRequestItem,
        SessionActionPolicySideEffect,
        SessionActionReasonCode,
        SessionActionSideEffectKind,
        build_action_policy_request_from_batch,
    )
    from app.models.catalog import (
        GenreCatalogEntry,
        GenreCatalogSeed,
        GenreToneCatalogDocument,
        ToneCatalogEntry,
        ToneCatalogSeed,
    )
    from app.models.chat_actions import (
        CHAT_TO_UI_ACTION_SCHEMA_VERSION,
        DEFAULT_CHAT_TO_UI_ACTION_POLICIES,
        AcceptBeatSheetAction,
        AcceptBeatSheetValues,
        ChatToUIAction,
        ChatToUIActionBase,
        ChatToUIActionBatch,
        ChatToUIActionDefaultPolicy,
        ChatToUIActionType,
        ChatToUIExtractedValues,
        ChatToUIJobKind,
        CompositionStartMode,
        DownloadAssetAction,
        DownloadAssetKind,
        DownloadAssetValues,
        FinalizeView,
        NavigateToStageAction,
        OpenFinalizeViewAction,
        OpenFinalizeViewValues,
        PauseJobAction,
        RedirectCompositionAction,
        RedirectCompositionValues,
        RefineBeatSheetAction,
        RefineBeatSheetValues,
        RefineCharacterSheetAction,
        RefineCharacterSheetValues,
        RegenerateBeatSheetAction,
        RegenerateBeatSheetValues,
        RegenerateCharacterSheetAction,
        RegenerateCharacterSheetValues,
        RegeneratePitchesAction,
        RegeneratePitchesValues,
        ResumeJobAction,
        SelectCharacterSheetAction,
        SelectCharacterSheetValues,
        SelectGenreAction,
        SelectGenreValues,
        SelectPitchAction,
        SelectPitchValues,
        SelectToneAction,
        SelectToneValues,
        StartAudioGenerationAction,
        StartAudioGenerationValues,
        StartCompositionAction,
        StartCompositionValues,
        StoryBriefEditMode,
        UpdateAudioSettingsAction,
        UpdateAudioSettingsValues,
        UpdateStoryBriefAction,
        UpdateStoryBriefValues,
        UpdateStorySetupAction,
        UpdateStorySetupValues,
        get_chat_to_ui_action_default_policy,
        get_chat_to_ui_action_schema_bundle,
    )
    from app.models.events import (
        AIOutputKind,
        AIOutputRecordedEventPayload,
        AudioProgressEventPayload,
        ChatIntentParsedEventPayload,
        ChatMessageRecordedEventPayload,
        ChatMessageRole,
        CompositionProgressEventPayload,
        EventActorType,
        EventPayload,
        SelectionKind,
        SelectionRecordedEventPayload,
        SessionCreatedEventPayload,
        SessionEventActor,
        SessionEventType,
        SessionEventView,
        SessionHistoryView,
        UIActionRecordedEventPayload,
        UserEditRecordedEventPayload,
        UserEditTargetKind,
        WorkflowStageChangedEventPayload,
        parse_event_payload,
        serialize_event_payload,
    )
    from app.models.intent_parser import (
        EXPLICIT_CHAT_COMMAND_MODEL_ID,
        EXPLICIT_CHAT_COMMAND_PROMPT_VERSION,
        INTENT_PARSER_PROMPT_VERSION,
        INTENT_PARSER_SCHEMA_VERSION,
        ExplicitChatCommandId,
        ExplicitChatCommandRequest,
        ExplicitChatCommandSource,
        IntentParserCandidateAction,
        IntentParserCandidateActionBatch,
        IntentParserInvocation,
        IntentParserInvocationResult,
        IntentParserPromptContext,
        IntentParserStageContext,
        IntentParserStatus,
        IntentParserStructuredOutput,
        ParseChatIntentRequest,
        ParsedChatIntentResponse,
    )
    from app.models.realtime import (
        ChatContentFormat,
        ChatMessageEventPayload,
        ChatMessageRealtimeEvent,
        CompositionChunkEventPayload,
        CompositionChunkKind,
        CompositionChunkRealtimeEvent,
        ErrorNotificationEventPayload,
        ErrorNotificationRealtimeEvent,
        ErrorSeverity,
        JobKind,
        JobProgressEventPayload,
        JobProgressRealtimeEvent,
        JobStatusEventPayload,
        JobStatusRealtimeEvent,
        RealtimeDeliveryMode,
        RealtimeEventType,
        RealtimeJobStatus,
        RealtimeReplayStrategy,
        SessionRealtimeEvent,
        SessionSubscriptionAck,
        SessionSubscriptionRequest,
        UIActionEchoEventPayload,
        UIActionEchoRealtimeEvent,
        UIActionEchoResult,
        WorkflowStageChangedRealtimeEvent,
        build_session_channel_name,
        get_realtime_contract_schema_bundle,
    )
    from app.models.session import (
        AudioJobView,
        BeatSheetView,
        CharacterSheetView,
        CompositionJobView,
        ConversationMemorySnapshotView,
        ConversationMemorySummaryData,
        ConversationMemoryWorkflow,
        CreateSessionRequest,
        ExportAssetView,
        PitchView,
        RecentSessionSummary,
        RecordSessionUIActionRequest,
        SessionAssetView,
        SessionCatalogSelection,
        SessionContextStageNoteValues,
        SessionContextUpdateRequest,
        SessionContextUpdateResponse,
        SessionProgress,
        SessionSnapshot,
        SessionStageStateView,
        StoryBriefView,
        StorySetupView,
    )
    from app.models.system import DependencyStatus, HealthResponse, HelloResponse
    from app.models.workflow import (
        WORKFLOW_STAGE_DEFINITIONS,
        WORKFLOW_STAGE_SEQUENCE,
        WORKFLOW_STAGE_STATES,
        WorkflowStage,
        WorkflowStageDefinition,
        WorkflowStageState,
        get_invalidated_stages_after_edit,
        get_workflow_stage_definition,
        resolve_resume_stage,
    )

    __all__ = [
        "AIOutputKind",
        "AIOutputRecordedEventPayload",
        "AcceptBeatSheetAction",
        "AcceptBeatSheetValues",
        "AudioJobView",
        "AudioProgressEventPayload",
        "BeatSheetView",
        "CHAT_TO_UI_ACTION_SCHEMA_VERSION",
        "SESSION_ACTION_POLICY_SCHEMA_VERSION",
        "ChatIntentParsedEventPayload",
        "ChatMessageRecordedEventPayload",
        "ChatMessageRole",
        "ChatContentFormat",
        "ChatMessageEventPayload",
        "ChatMessageRealtimeEvent",
        "ChatToUIAction",
        "ChatToUIActionBase",
        "ChatToUIActionBatch",
        "ChatToUIActionDefaultPolicy",
        "ChatToUIActionType",
        "ChatToUIExtractedValues",
        "ChatToUIJobKind",
        "CharacterSheetView",
        "ConversationMemorySnapshotView",
        "ConversationMemorySummaryData",
        "ConversationMemoryWorkflow",
        "CompositionStartMode",
        "CompositionChunkEventPayload",
        "CompositionChunkKind",
        "CompositionChunkRealtimeEvent",
        "CompositionProgressEventPayload",
        "CompositionJobView",
        "CreateSessionRequest",
        "DEFAULT_CHAT_TO_UI_ACTION_POLICIES",
        "DependencyStatus",
        "DownloadAssetAction",
        "DownloadAssetKind",
        "DownloadAssetValues",
        "EXPLICIT_CHAT_COMMAND_MODEL_ID",
        "EXPLICIT_CHAT_COMMAND_PROMPT_VERSION",
        "ErrorNotificationEventPayload",
        "ErrorNotificationRealtimeEvent",
        "ErrorSeverity",
        "EventActorType",
        "EventPayload",
        "ExplicitChatCommandId",
        "ExplicitChatCommandRequest",
        "ExplicitChatCommandSource",
        "ExportAssetView",
        "FinalizeView",
        "GenreCatalogEntry",
        "GenreCatalogSeed",
        "GenreToneCatalogDocument",
        "HealthResponse",
        "HelloResponse",
        "INTENT_PARSER_PROMPT_VERSION",
        "INTENT_PARSER_SCHEMA_VERSION",
        "IntentParserCandidateAction",
        "IntentParserCandidateActionBatch",
        "IntentParserInvocation",
        "IntentParserInvocationResult",
        "IntentParserPromptContext",
        "IntentParserStageContext",
        "IntentParserStatus",
        "IntentParserStructuredOutput",
        "JobKind",
        "JobProgressEventPayload",
        "JobProgressRealtimeEvent",
        "RealtimeJobStatus",
        "JobStatusEventPayload",
        "JobStatusRealtimeEvent",
        "NavigateToStageAction",
        "OpenFinalizeViewAction",
        "OpenFinalizeViewValues",

## Command Started

- Time: `2026-04-01T07:33:09-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `85`
- Summary: in progress: /bin/zsh -lc "sed -n '1,320p' backend/tests/test_intent_parser_api.py"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,320p' backend/tests/test_intent_parser_api.py"
    Status: in progress

## Command Started

- Time: `2026-04-01T07:33:09-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `86`
- Summary: in progress: /bin/zsh -lc "sed -n '1,320p' backend/tests/test_intent_parser_adapter.py"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,320p' backend/tests/test_intent_parser_adapter.py"
    Status: in progress

## Command Finished

- Time: `2026-04-01T07:33:09-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `87`
- Summary: completed, exit 0: /bin/zsh -lc "sed -n '1,320p' backend/tests/test_intent_parser_adapter.py"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,320p' backend/tests/test_intent_parser_adapter.py"
    Status: completed
    Exit code: 0
    Output:
    from __future__ import annotations

    import json

    import httpx
    from app.ai import (
        GeminiIntentParserAdapter,
        get_intent_parser_response_schema,
        render_intent_parser_prompt,
    )
    from app.ai.intent_parser import build_intent_parser_invocation
    from app.models import (
        IntentParserPromptContext,
        IntentParserStageContext,
        IntentParserStatus,
        WorkflowStage,
        WorkflowStageState,
    )


    def _build_context() -> IntentParserPromptContext:
        return IntentParserPromptContext(
            session_id="session-123",
            display_title="Moonlit Harbor",
            overall_status=WorkflowStageState.IN_PROGRESS,
            resume_stage=WorkflowStage.BEATS,
            stage_context=IntentParserStageContext(
                current_stage=WorkflowStage.BEATS,
                current_stage_label="Beat sheet",
                current_stage_description="Store the accepted Save-the-Cat beat sheet for the session.",
                current_stage_status=WorkflowStageState.IN_PROGRESS,
                current_stage_detail="Refining the midpoint tension.",
            ),
            session_summary=(
                "Selected genre: Quest Fantasy\n"
                "Selected tone: Hushed Wonder\n"
                "Story brief: A harbor mystery with a calm ending."
            ),
            user_message="make it a little more mysterious and shorter",
        )


    def test_render_intent_parser_prompt_includes_guardrails_and_context() -> None:
        prompt = render_intent_parser_prompt(_build_context())

        assert "backend-only chat intent parser" in prompt
        assert 'status="needs_clarification"' in prompt
        assert '"current_stage": "beats"' in prompt
        assert "Selected tone: Hushed Wonder" in prompt
        assert "make it a little more mysterious and shorter" in prompt


    def test_intent_parser_response_schema_strips_unsupported_json_schema_keywords() -> None:
        schema_json = json.dumps(get_intent_parser_response_schema(), sort_keys=True)

        assert '"enum"' in schema_json
        assert '"const"' not in schema_json
        assert '"default"' not in schema_json
        assert '"discriminator"' not in schema_json
        assert '"minLength"' not in schema_json


    def test_gemini_intent_parser_adapter_requests_json_schema_and_parses_response() -> None:
        seen_request: dict[str, object] = {}

        def handler(request: httpx.Request) -> httpx.Response:
            seen_request["url"] = str(request.url)
            seen_request["headers"] = dict(request.headers)
            seen_request["body"] = json.loads(request.content.decode("utf-8"))
            return httpx.Response(
                200,
                json={
                    "candidates": [
                        {
                            "content": {
                                "parts": [
                                    {
                                        "text": json.dumps(
                                            {
                                                "schema_version": 1,
                                                "status": "parsed",
                                                "needs_clarification": False,
                                                "assistant_response": (
                                                    "I can make the beat sheet moodier "
                                                    "and shorten the target runtime."
                                                ),
                                                "clarification_reason": None,
                                                "proposed_actions": {
                                                    "schema_version": 1,
                                                    "actions": [
                                                        {
                                                            "action_type": "refine_beat_sheet",
                                                            "target_stage": "beats",
                                                            "confidence": 0.84,
                                                            "rationale": (
                                                                "The user asked for a more "
                                                                "mysterious beat shape."
                                                            ),
                                                            "requires_confirmation": True,
                                                            "extracted_values": {
                                                                "instructions": (
                                                                    "Make the midpoint a little "
                                                                    "more mysterious."
                                                                ),
                                                                "bedtime_goal": (
                                                                    "Keep the tension calm and "
                                                                    "bedtime-safe."
                                                                ),
                                                            },
                                                        }
                                                    ],
                                                },
                                            }
                                        )
                                    }
                                ]
                            }
                        }
                    ]
                },
            )

        transport = httpx.MockTransport(handler)
        client = httpx.Client(transport=transport)
        adapter = GeminiIntentParserAdapter(
            credential="test-key",
            model_id="gemini-3.1-flash-lite",
            client=client,
        )

        invocation = build_intent_parser_invocation(
            _build_context(),
            model_id=adapter.model_id,
        )
        result = adapter.parse(invocation)

        request_body = seen_request["body"]
        assert isinstance(request_body, dict)
        assert seen_request["url"] == (
            "https://generativelanguage.googleapis.com/v1beta/models/"
            "gemini-3.1-flash-lite:generateContent"
        )
        assert seen_request["headers"]["x-goog-api-key"] == "test-key"
        assert request_body["generationConfig"]["responseMimeType"] == "application/json"
        assert "responseJsonSchema" in request_body["generationConfig"]
        assert (
            "make it a little more mysterious and shorter"
            in (request_body["contents"][0]["parts"][0]["text"])
        )
        assert result.structured_output.status == IntentParserStatus.PARSED
        assert result.structured_output.proposed_actions.actions[0].action_type == "refine_beat_sheet"
        assert result.invocation.prompt_version == "intent_parser.v1"

        adapter.close()

## Command Finished

- Time: `2026-04-01T07:33:09-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `88`
- Summary: completed, exit 0: /bin/zsh -lc "sed -n '1,320p' backend/tests/test_intent_parser_api.py"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,320p' backend/tests/test_intent_parser_api.py"
    Status: completed
    Exit code: 0
    Output:
    from __future__ import annotations

    from pathlib import Path
    from typing import Iterator

    import pytest
    from app.db import Base
    from app.db.session import get_engine, get_session_factory
    from app.main import create_app
    from app.models import IntentParserInvocationResult, IntentParserStructuredOutput
    from app.services import SessionEventLogService, SessionService
    from app.settings import get_settings
    from fastapi.testclient import TestClient


    class StubIntentParserAdapter:
        def __init__(self, structured_output: IntentParserStructuredOutput) -> None:
            self.model_id = "gemini-3.1-flash-lite"
            self._structured_output = structured_output
            self.parse_calls = 0

        def parse(self, invocation):
            self.parse_calls += 1
            return IntentParserInvocationResult(
                invocation=invocation,
                structured_output=self._structured_output,
                raw_response={"mock": "response"},
            )

        def close(self) -> None:
            return None


    @pytest.fixture
    def intent_parser_api_client(
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> Iterator[tuple[TestClient, StubIntentParserAdapter]]:
        database_path = tmp_path / "intent-parser-api.sqlite3"
        monkeypatch.setenv("STORYTELLER_DATABASE_URL", f"sqlite+pysqlite:///{database_path}")

        get_settings.cache_clear()
        get_engine.cache_clear()
        get_session_factory.cache_clear()

        engine = get_engine()
        Base.metadata.create_all(engine)
        app = create_app()
        adapter = StubIntentParserAdapter(
            IntentParserStructuredOutput.model_validate(
                {
                    "schema_version": 1,
                    "status": "parsed",
                    "needs_clarification": False,
                    "assistant_response": "I can shorten the setup target and make the notes moodier.",
                    "proposed_actions": {
                        "schema_version": 1,
                        "actions": [
                            {
                                "action_type": "update_story_setup",
                                "target_stage": "story_setup",
                                "confidence": 0.86,
                                "rationale": "The user asked for a shorter story.",
                                "requires_confirmation": False,
                                "extracted_values": {
                                    "target_runtime_minutes": 9,
                                    "guidance_notes": "Lean slightly more mysterious.",
                                },
                            }
                        ],
                    },
                }
            )
        )
        app.state.intent_parser_adapter = adapter

        with TestClient(app) as test_client:
            yield test_client, adapter

        get_settings.cache_clear()
        get_engine.cache_clear()
        get_session_factory.cache_clear()


    def test_parse_chat_intents_endpoint_returns_structured_actions_and_logs_audit_event(
        intent_parser_api_client: tuple[TestClient, StubIntentParserAdapter],
    ) -> None:
        client, _adapter = intent_parser_api_client
        db_session = get_session_factory()()
        try:
            session_id = SessionService(db_session).create_session(working_title="Lantern Cove").id
        finally:
            db_session.close()

        response = client.post(
            f"/api/v1/sessions/{session_id}/chat/intents",
            json={"message": "make it shorter and moodier"},
        )

        assert response.status_code == 200
        payload = response.json()
        assert payload["status"] == "parsed"
        assert payload["assistant_response"] == (
            "I can shorten the setup target and make the notes moodier."
        )
        assert payload["proposed_actions"]["actions"][0]["action_type"] == "update_story_setup"
        assert payload["proposed_actions"]["actions"][0]["requires_confirmation"] is False
        assert payload["policy_evaluation"]["evaluated_actions"][0]["decision"] == "rejected"
        assert payload["policy_evaluation"]["evaluated_actions"][0]["reasons"][0]["code"] == (
            "prerequisite_stage_incomplete"
        )

        db_session = get_session_factory()()
        try:
            history = SessionEventLogService(db_session).list_session_history(session_id)
        finally:
            db_session.close()

        assert history.events[-2].event_type == "chat.intent.parsed"
        assert history.events[-2].payload is not None
        assert history.events[-2].payload.model_id == "gemini-3.1-flash-lite"
        assert history.events[-2].payload.result.proposed_actions.actions[0].action_type == (
            "update_story_setup"
        )


    def test_parse_chat_intents_endpoint_returns_404_for_missing_session(
        intent_parser_api_client: tuple[TestClient, StubIntentParserAdapter],
    ) -> None:
        client, _adapter = intent_parser_api_client

        response = client.post(
            "/api/v1/sessions/missing-session/chat/intents",
            json={"message": "make it shorter and moodier"},
        )

        assert response.status_code == 404
        assert response.json() == {
            "detail": "session 'missing-session' was not found",
        }


    def test_parse_chat_intents_endpoint_handles_explicit_commands_without_calling_the_parser(
        intent_parser_api_client: tuple[TestClient, StubIntentParserAdapter],
    ) -> None:
        client, adapter = intent_parser_api_client
        db_session = get_session_factory()()
        try:
            session_id = SessionService(db_session).create_session(working_title="Lantern Cove").id
        finally:
            db_session.close()

        response = client.post(
            f"/api/v1/sessions/{session_id}/chat/intents",
            json={
                "message": "/next-stage",
                "explicit_command": {
                    "command_id": "next_stage",
                    "source": "quick_action",
                    "proposed_actions": {
                        "schema_version": 1,
                        "actions": [
                            {
                                "schema_version": 1,
                                "action_type": "navigate_to_stage",
                                "target_stage": "tone",
                                "confidence": 1,
                                "rationale": "Explicit command requested navigation to Tone.",
                                "requires_confirmation": False,
                                "extracted_values": {},
                            }
                        ],
                    },
                },
            },
        )

        assert response.status_code == 200
        payload = response.json()
        assert payload["assistant_response"] == "I can move the workspace to Tone."
        assert payload["proposed_actions"]["actions"][0]["action_type"] == "navigate_to_stage"
        assert payload["policy_evaluation"]["evaluated_actions"][0]["decision"] == "accepted"
        assert adapter.parse_calls == 0

        db_session = get_session_factory()()
        try:
            history = SessionEventLogService(db_session).list_session_history(session_id)
        finally:
            db_session.close()

        assert history.events[-2].event_type == "chat.intent.parsed"
        assert history.events[-2].payload is not None
        assert history.events[-2].payload.prompt_version == "explicit_command.v1"
        assert history.events[-2].payload.model_id == "deterministic-command-map"


    def test_parse_chat_intents_endpoint_supports_summary_commands_with_no_actions(
        intent_parser_api_client: tuple[TestClient, StubIntentParserAdapter],
    ) -> None:
        client, adapter = intent_parser_api_client
        db_session = get_session_factory()()
        try:
            session_id = SessionService(db_session).create_session(working_title="Lantern Cove").id
        finally:
            db_session.close()

        response = client.post(
            f"/api/v1/sessions/{session_id}/chat/intents",
            json={
                "message": "/plan",
                "explicit_command": {
                    "command_id": "summarize_plan",
                    "source": "slash_command",
                    "proposed_actions": {
                        "schema_version": 1,
                        "actions": [],
                    },
                },
            },
        )

        assert response.status_code == 200
        payload = response.json()
        assert payload["status"] == "parsed"
        assert payload["needs_clarification"] is False
        assert payload["proposed_actions"]["actions"] == []
        assert payload["policy_evaluation"] is None
        assert "Current focus is genre." in payload["assistant_response"]
        assert adapter.parse_calls == 0

## Command Started

- Time: `2026-04-01T07:33:09-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `89`
- Summary: in progress: /bin/zsh -lc 'rg -n "_ACTION_CATALOG|default_policy_by_action|chat-to-ui-actions.schema.json|action catalog" backend tests docs -S'

### Full Text

    Command: /bin/zsh -lc 'rg -n "_ACTION_CATALOG|default_policy_by_action|chat-to-ui-actions.schema.json|action catalog" backend tests docs -S'
    Status: in progress

## Command Finished

- Time: `2026-04-01T07:33:09-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `90`
- Summary: failed, exit 2: /bin/zsh -lc 'rg -n "_ACTION_CATALOG|default_policy_by_action|chat-to-ui-actions.schema.json|action catalog" backend tests docs -S'

### Full Text

    Command: /bin/zsh -lc 'rg -n "_ACTION_CATALOG|default_policy_by_action|chat-to-ui-actions.schema.json|action catalog" backend tests docs -S'
    Status: failed
    Exit code: 2
    Output:
    rg: tests: No such file or directory (os error 2)
    docs/README.md:10:- `chat-to-ui-actions.md`: proposed action contract, action catalog, default confirmation policy, and deterministic action-policy evaluator
    docs/README.md:12:- `chat-to-ui-actions.schema.json`: machine-readable schema bundle for chat-to-UI proposed actions
    backend/tests/test_chat_action_contracts.py:155:    schema_path = Path(__file__).resolve().parents[2] / "docs" / "chat-to-ui-actions.schema.json"
    docs/chat-to-ui-actions.schema.json:4:  "default_policy_by_action": {
    docs/chat-to-ui-actions.md:12:`docs/chat-to-ui-actions.schema.json`.
    backend/app/ai/prompts/intent_parser.md:15:Allowed action catalog:
    backend/app/ai/intent_parser.py:44:_ACTION_CATALOG = (
    backend/app/ai/intent_parser.py:297:        action_catalog_json=json.dumps(_ACTION_CATALOG, indent=2, sort_keys=True),
    backend/app/models/chat_actions.py:580:        "default_policy_by_action": {

## Command Started

- Time: `2026-04-01T07:33:24-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `91`
- Summary: in progress: /bin/zsh -lc "sed -n '1,260p' prompts/37-agent-tool-registry.md"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,260p' prompts/37-agent-tool-registry.md"
    Status: in progress

## Command Finished

- Time: `2026-04-01T07:33:24-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `92`
- Summary: completed, exit 0: /bin/zsh -lc "sed -n '1,260p' prompts/37-agent-tool-registry.md"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,260p' prompts/37-agent-tool-registry.md"
    Status: completed
    Exit code: 0
    Output:
    # 37 — Agent Tool Registry for Story Workflow Operations

    Read `base_prompt.md` first and preserve all prior prompt work.

    ## Objective

    Organize the backend’s callable story operations into a clear registry so planning, generation, and chat translation can share the same action vocabulary.

    ## Build
    - Define backend tools or service functions for operations like generate pitches, refine pitch, generate character sheets, refine character sheet, generate beat sheet, update setup heuristics, compose next segment, rewrite segments, estimate audio length, and start audio generation.
    - Describe the inputs, outputs, and side effects of each tool in a central registry.
    - Use the registry to reduce duplicate logic across routes, workers, and future model orchestration.

    ## Deliverables

    - Tool registry or capability map
    - Centralized tool interfaces
    - Documentation of side effects and expected outputs

    ## Acceptance checks

    - Story operations are discoverable in one place.
    - The chat/action layer and the worker layer call the same domain services.
    - Adding a new stage operation later would be straightforward.

    ## Notes

    Keep tools thin wrappers around real business services.

    ## Suggested commit label

    `feat(prompt-37): agent tool registry`

## Unkown Event

- Time: `2026-04-01T07:33:34-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `93`
- Summary: { "item": { "id": "item_46", "items": [ { "completed": true, "text": "Inspect existing backend action, worker, and session services to find the right registry seam" }, { "completed": false, "text": "Implement story operation models, doma...

### Full Text

    {
      "item": {
        "id": "item_46",
        "items": [
          {
            "completed": true,
            "text": "Inspect existing backend action, worker, and session services to find the right registry seam"
          },
          {
            "completed": false,
            "text": "Implement story operation models, domain services, and a central registry with invocation helpers"
          },
          {
            "completed": false,
            "text": "Wire the registry into chat/orchestration and worker handler registration"
          },
          {
            "completed": false,
            "text": "Add tests and docs covering discoverability, invocation, side effects, and extension points"
          },
          {
            "completed": false,
            "text": "Run targeted verification, commit checkpoints, and write the required summary file"
          }
        ],
        "type": "todo_list"
      },
      "type": "item.started"
    }

## Command Started

- Time: `2026-04-01T07:36:17-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `94`
- Summary: in progress: /bin/zsh -lc "sed -n '1,120p' backend/app/db/models.py"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,120p' backend/app/db/models.py"
    Status: in progress

## Command Finished

- Time: `2026-04-01T07:36:17-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `95`
- Summary: completed, exit 0: /bin/zsh -lc "sed -n '1,120p' backend/app/db/models.py"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,120p' backend/app/db/models.py"
    Status: completed
    Exit code: 0
    Output:
    from __future__ import annotations

    from datetime import datetime
    from enum import Enum
    from typing import Any

    from sqlalchemy import (
        JSON,
        Boolean,
        DateTime,
        ForeignKey,
        Index,
        Integer,
        Numeric,
        String,
        Text,
        UniqueConstraint,
    )
    from sqlalchemy import (
        Enum as SQLAlchemyEnum,
    )
    from sqlalchemy.orm import Mapped, mapped_column, relationship

    from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin, utc_now
    from app.models.events import EventActorType
    from app.models.workflow import WorkflowStage, WorkflowStageState


    def _enum_values(enum_cls: type[Enum]) -> list[str]:
        return [member.value for member in enum_cls]


    def build_enum(enum_cls: type[Enum], name: str) -> SQLAlchemyEnum:
        return SQLAlchemyEnum(
            enum_cls,
            name=name,
            native_enum=False,
            values_callable=_enum_values,
            validate_strings=True,
        )


    class JobStatus(str, Enum):
        QUEUED = "queued"
        IN_PROGRESS = "in_progress"
        PAUSED = "paused"
        COMPLETED = "completed"
        FAILED = "failed"
        CANCELLED = "cancelled"


    class CompositionJobKind(str, Enum):
        DRAFT = "draft"
        REWRITE = "rewrite"


    class AssetKind(str, Enum):
        DRAFT_TEXT_SNAPSHOT = "draft_text_snapshot"
        COMPOSITION_SEGMENT = "composition_segment"
        STORY_TEXT = "story_text"
        STORY_DOCX = "story_docx"
        AUDIO_SEGMENT = "audio_segment"
        FINAL_AUDIO = "final_audio"


    class AssetStatus(str, Enum):
        PENDING = "pending"
        IN_PROGRESS = "in_progress"
        READY = "ready"
        FAILED = "failed"
        SUPERSEDED = "superseded"


    WORKFLOW_STAGE_ENUM = build_enum(WorkflowStage, "workflow_stage")
    WORKFLOW_STAGE_STATE_ENUM = build_enum(WorkflowStageState, "workflow_stage_state")
    JOB_STATUS_ENUM = build_enum(JobStatus, "job_status")
    COMPOSITION_JOB_KIND_ENUM = build_enum(CompositionJobKind, "composition_job_kind")
    ASSET_KIND_ENUM = build_enum(AssetKind, "asset_kind")
    ASSET_STATUS_ENUM = build_enum(AssetStatus, "asset_status")
    EVENT_ACTOR_TYPE_ENUM = build_enum(EventActorType, "event_actor_type")


    class Genre(UUIDPrimaryKeyMixin, TimestampMixin, Base):
        __tablename__ = "genres"

        slug: Mapped[str] = mapped_column(String(80), nullable=False, unique=True)
        label: Mapped[str] = mapped_column(String(120), nullable=False)
        description: Mapped[str | None] = mapped_column(Text)
        bedtime_safety_notes: Mapped[str | None] = mapped_column(Text)
        arc_notes: Mapped[dict[str, Any] | list[Any] | None] = mapped_column(JSON)
        sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
        is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

        tone_profiles: Mapped[list["ToneProfile"]] = relationship(
            back_populates="genre",
            cascade="all, delete-orphan",
        )
        sessions: Mapped[list["StorySession"]] = relationship(back_populates="selected_genre")

        __table_args__ = (
            Index("ix_genres_sort_order", "sort_order"),
            Index("ix_genres_is_active", "is_active"),
        )


    class ToneProfile(UUIDPrimaryKeyMixin, TimestampMixin, Base):
        __tablename__ = "tone_profiles"

        genre_id: Mapped[str] = mapped_column(
            String(36),
            ForeignKey("genres.id", ondelete="CASCADE"),
            nullable=False,
        )
        slug: Mapped[str] = mapped_column(String(80), nullable=False)
        label: Mapped[str] = mapped_column(String(120), nullable=False)
        description: Mapped[str | None] = mapped_column(Text)
        bedtime_notes: Mapped[str | None] = mapped_column(Text)
        descriptors: Mapped[dict[str, Any] | list[Any] | None] = mapped_column(JSON)
        default_planning_hints: Mapped[dict[str, Any] | list[Any] | None] = mapped_column(JSON)
        sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

## Command Started

- Time: `2026-04-01T07:37:00-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `96`
- Summary: in progress: /bin/zsh -lc "sed -n '1,260p' backend/app/ai/prompts/intent_parser.md"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,260p' backend/app/ai/prompts/intent_parser.md"
    Status: in progress

## Command Finished

- Time: `2026-04-01T07:37:00-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `97`
- Summary: completed, exit 0: /bin/zsh -lc "sed -n '1,260p' backend/app/ai/prompts/intent_parser.md"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,260p' backend/app/ai/prompts/intent_parser.md"
    Status: completed
    Exit code: 0
    Output:
    You are Storyteller's backend-only chat intent parser.

    Your job is to translate a single user chat message into a structured backend proposal for the bedtime-story workflow.

    Rules:
    - Return JSON only. Do not wrap it in markdown.
    - Never invent action types, stages, or extracted fields beyond the allowed catalog.
    - You may propose zero or more actions, but you must never claim that an action has already been applied.
    - Use the current stage context and session summary to decide which stage the message is most likely trying to change.
    - If the message is too vague to turn into a safe proposal, return `status="needs_clarification"`, set `needs_clarification=true`, leave `proposed_actions.actions` empty, explain the ambiguity in `clarification_reason`, and ask one concise follow-up question in `assistant_response`.
    - Keep `assistant_response` calm, concise, and useful. Prefer one or two sentences.
    - Respect the default confirmation policy. Any action whose default policy is `confirm_first` must set `requires_confirmation=true`.
    - Do not use copyrighted-author labels or unsafe bedtime framing.

    Allowed action catalog:
    $action_catalog_json

    Default policy by action type:
    $default_policy_json

    Current stage context:
    $stage_context_json

    Session summary:
    $session_summary

    User message:
    $user_message

## Command Started

- Time: `2026-04-01T07:38:26-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `98`
- Summary: in progress: /bin/zsh -lc "sed -n '1,220p' backend/pyproject.toml"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,220p' backend/pyproject.toml"
    Status: in progress

## Command Finished

- Time: `2026-04-01T07:38:26-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `99`
- Summary: completed, exit 0: /bin/zsh -lc "sed -n '1,220p' backend/pyproject.toml"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,220p' backend/pyproject.toml"
    Status: completed
    Exit code: 0
    Output:
    [tool.ruff]
    target-version = "py310"
    line-length = 100
    src = ["app", "tests"]

    [tool.ruff.lint]
    select = ["E", "F", "I"]

    [tool.pytest.ini_options]
    markers = [
        "integration: exercises real Postgres and fake GCS services",
    ]

## Agent Message

- Time: `2026-04-01T07:38:29-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `100`
- Summary: I’m moving into code changes now. The plan is to add typed story-tool contracts and a registry, put the execution logic behind one service, then hook the worker and chat-action mapping into that registry so the vocabulary only lives once.

### Full Text

    I’m moving into code changes now. The plan is to add typed story-tool contracts and a registry, put the execution logic behind one service, then hook the worker and chat-action mapping into that registry so the vocabulary only lives once.

## Command Started

- Time: `2026-04-01T07:39:57-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `101`
- Summary: in progress: /bin/zsh -lc 'rg -n "class SelectionKind|STORY_SETUP|AUDIO_SETTINGS|COMPOSITION_SEGMENT" backend/app/models/events.py backend/app/models -S'

### Full Text

    Command: /bin/zsh -lc 'rg -n "class SelectionKind|STORY_SETUP|AUDIO_SETTINGS|COMPOSITION_SEGMENT" backend/app/models/events.py backend/app/models -S'
    Status: in progress

## Command Finished

- Time: `2026-04-01T07:39:57-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `102`
- Summary: completed, exit 0: /bin/zsh -lc 'rg -n "class SelectionKind|STORY_SETUP|AUDIO_SETTINGS|COMPOSITION_SEGMENT" backend/app/models/events.py backend/app/models -S'

### Full Text

    Command: /bin/zsh -lc 'rg -n "class SelectionKind|STORY_SETUP|AUDIO_SETTINGS|COMPOSITION_SEGMENT" backend/app/models/events.py backend/app/models -S'
    Status: completed
    Exit code: 0
    Output:
    backend/app/models/events.py:27:class SelectionKind(str, Enum):
    backend/app/models/events.py:33:    STORY_SETUP = "story_setup"
    backend/app/models/events.py:40:    STORY_SETUP = "story_setup"
    backend/app/models/events.py:41:    COMPOSITION_SEGMENT = "composition_segment"
    backend/app/models/events.py:50:    STORY_SETUP = "story_setup"
    backend/app/models/events.py:51:    COMPOSITION_SEGMENT = "composition_segment"
    backend/app/models/events.py:52:    AUDIO_SETTINGS = "audio_settings"
    backend/app/models/workflow.py:15:    STORY_SETUP = "story_setup"
    backend/app/models/workflow.py:117:        id=WorkflowStage.STORY_SETUP,
    backend/app/models/chat_actions.py:26:    UPDATE_STORY_SETUP = "update_story_setup"
    backend/app/models/chat_actions.py:31:    UPDATE_AUDIO_SETTINGS = "update_audio_settings"
    backend/app/models/chat_actions.py:82:    ChatToUIActionType.UPDATE_STORY_SETUP: ChatToUIActionDefaultPolicy.AUTO_APPLY_CANDIDATE,
    backend/app/models/chat_actions.py:87:    ChatToUIActionType.UPDATE_AUDIO_SETTINGS: ChatToUIActionDefaultPolicy.AUTO_APPLY_CANDIDATE,
    backend/app/models/chat_actions.py:456:    action_type: Literal[ChatToUIActionType.UPDATE_STORY_SETUP] = (
    backend/app/models/chat_actions.py:457:        ChatToUIActionType.UPDATE_STORY_SETUP
    backend/app/models/chat_actions.py:459:    target_stage: Literal[WorkflowStage.STORY_SETUP] = WorkflowStage.STORY_SETUP
    backend/app/models/chat_actions.py:516:    action_type: Literal[ChatToUIActionType.UPDATE_AUDIO_SETTINGS] = (
    backend/app/models/chat_actions.py:517:        ChatToUIActionType.UPDATE_AUDIO_SETTINGS
    backend/app/models/events.py:27:class SelectionKind(str, Enum):
    backend/app/models/events.py:33:    STORY_SETUP = "story_setup"
    backend/app/models/events.py:40:    STORY_SETUP = "story_setup"
    backend/app/models/events.py:41:    COMPOSITION_SEGMENT = "composition_segment"
    backend/app/models/events.py:50:    STORY_SETUP = "story_setup"
    backend/app/models/events.py:51:    COMPOSITION_SEGMENT = "composition_segment"
    backend/app/models/events.py:52:    AUDIO_SETTINGS = "audio_settings"

## Command Started

- Time: `2026-04-01T07:40:01-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `103`
- Summary: in progress: /bin/zsh -lc "sed -n '1,120p' backend/app/models/events.py"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,120p' backend/app/models/events.py"
    Status: in progress

## Command Finished

- Time: `2026-04-01T07:40:01-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `104`
- Summary: completed, exit 0: /bin/zsh -lc "sed -n '1,120p' backend/app/models/events.py"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,120p' backend/app/models/events.py"
    Status: completed
    Exit code: 0
    Output:
    from __future__ import annotations

    from collections.abc import Mapping
    from datetime import datetime
    from enum import Enum
    from typing import Any, TypeAlias

    from pydantic import BaseModel, ConfigDict, Field

    from app.models.intent_parser import ParsedChatIntentResponse
    from app.models.workflow import WorkflowStage, WorkflowStageState


    class SessionEventType(str, Enum):
        SESSION_CREATED = "session.created"
        WORKFLOW_STAGE_CHANGED = "workflow.stage_changed"
        SELECTION_RECORDED = "selection.recorded"
        AI_OUTPUT_RECORDED = "ai.output.recorded"
        USER_EDIT_RECORDED = "content.user_edit.recorded"
        CHAT_MESSAGE_RECORDED = "chat.message.recorded"
        CHAT_INTENT_PARSED = "chat.intent.parsed"
        UI_ACTION_RECORDED = "ui.action.recorded"
        COMPOSITION_PROGRESS_RECORDED = "composition.progress.recorded"
        AUDIO_PROGRESS_RECORDED = "audio.progress.recorded"


    class SelectionKind(str, Enum):
        GENRE = "genre"
        TONE_PROFILE = "tone_profile"
        PITCH = "pitch"
        CHARACTER_SHEET = "character_sheet"
        BEAT_SHEET = "beat_sheet"
        STORY_SETUP = "story_setup"


    class AIOutputKind(str, Enum):
        PITCH_BATCH = "pitch_batch"
        CHARACTER_SHEET = "character_sheet"
        BEAT_SHEET = "beat_sheet"
        STORY_SETUP = "story_setup"
        COMPOSITION_SEGMENT = "composition_segment"
        AUDIO_SEGMENT = "audio_segment"


    class UserEditTargetKind(str, Enum):
        STORY_BRIEF = "story_brief"
        PITCH = "pitch"
        CHARACTER_SHEET = "character_sheet"
        BEAT_SHEET = "beat_sheet"
        STORY_SETUP = "story_setup"
        COMPOSITION_SEGMENT = "composition_segment"
        AUDIO_SETTINGS = "audio_settings"


    class ChatMessageRole(str, Enum):
        USER = "user"
        ASSISTANT = "assistant"
        SYSTEM = "system"
        TOOL = "tool"


    class EventActorType(str, Enum):
        USER = "user"
        ASSISTANT = "assistant"
        SYSTEM = "system"
        SERVICE = "service"


    class SessionEventActor(BaseModel):
        model_config = ConfigDict(extra="forbid", frozen=True)

        actor_type: EventActorType
        actor_id: str | None = None


    class EventPayload(BaseModel):
        model_config = ConfigDict(extra="forbid")

        schema_version: int = Field(default=1, ge=1)


    class SessionCreatedEventPayload(EventPayload):
        working_title: str | None = None


    class WorkflowStageChangedEventPayload(EventPayload):
        previous_status: WorkflowStageState
        status: WorkflowStageState
        detail: str | None = None
        invalidated_stages: list[WorkflowStage] = Field(default_factory=list)
        current_stage: WorkflowStage
        resume_stage: WorkflowStage
        furthest_completed_stage: WorkflowStage | None = None
        overall_status: WorkflowStageState


    class SelectionRecordedEventPayload(EventPayload):
        selection_kind: SelectionKind
        selection_id: str | None = None
        slug: str | None = None
        label: str | None = None
        previous_selection_id: str | None = None
        source: str = "unknown"
        accepted: bool = True


    class AIOutputRecordedEventPayload(EventPayload):
        output_kind: AIOutputKind
        resource_id: str | None = None
        generation_key: str | None = None
        candidate_count: int | None = None
        model_id: str | None = None
        summary: str | None = None


    class UserEditRecordedEventPayload(EventPayload):
        target_kind: UserEditTargetKind
        target_id: str | None = None
        revision_number: int | None = None
        changed_fields: list[str] = Field(default_factory=list)

## Command Started

- Time: `2026-04-01T07:40:09-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `105`
- Summary: in progress: /bin/zsh -lc 'rg -n "record_composition_progress|record_audio_progress" -n backend/app/services/event_log.py'

### Full Text

    Command: /bin/zsh -lc 'rg -n "record_composition_progress|record_audio_progress" -n backend/app/services/event_log.py'
    Status: in progress

## Command Finished

- Time: `2026-04-01T07:40:09-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `106`
- Summary: completed, exit 0: /bin/zsh -lc 'rg -n "record_composition_progress|record_audio_progress" -n backend/app/services/event_log.py'

### Full Text

    Command: /bin/zsh -lc 'rg -n "record_composition_progress|record_audio_progress" -n backend/app/services/event_log.py'
    Status: completed
    Exit code: 0
    Output:
    367:    def record_composition_progress(
    403:    def record_audio_progress(

## Command Started

- Time: `2026-04-01T07:40:13-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `107`
- Summary: in progress: /bin/zsh -lc "sed -n '340,460p' backend/app/services/event_log.py"

### Full Text

    Command: /bin/zsh -lc "sed -n '340,460p' backend/app/services/event_log.py"
    Status: in progress

## Command Finished

- Time: `2026-04-01T07:40:13-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `108`
- Summary: completed, exit 0: /bin/zsh -lc "sed -n '340,460p' backend/app/services/event_log.py"

### Full Text

    Command: /bin/zsh -lc "sed -n '340,460p' backend/app/services/event_log.py"
    Status: completed
    Exit code: 0
    Output:
    )

        def record_ui_action(
            self,
            session_id: str,
            *,
            action: str,
            stage: WorkflowStage | None = None,
            control_id: str | None = None,
            value_summary: str | None = None,
            origin: str = "workspace",
            actor: SessionEventActor | None = None,
        ) -> EventLogEntry:
            return self.append_event(
                session_id,
                actor=actor or DEFAULT_LOCAL_USER_ACTOR,
                event_type=SessionEventType.UI_ACTION_RECORDED,
                summary=f"Recorded UI action: {action}.",
                stage=stage,
                payload=UIActionRecordedEventPayload(
                    action=action,
                    control_id=control_id,
                    value_summary=value_summary,
                    origin=origin,
                ),
            )

        def record_composition_progress(
            self,
            session_id: str,
            *,
            job_id: str,
            status: str | Enum,
            progress_percent: float | None = None,
            current_segment_index: int | None = None,
            total_segments: int | None = None,
            segment_id: str | None = None,
            actor: SessionEventActor | None = None,
        ) -> EventLogEntry:
            summary = (
                f"Composition progress {progress_percent:.1f}%."
                if progress_percent is not None
                else "Recorded composition progress."
            )
            event = self.append_event(
                session_id,
                actor=actor or DEFAULT_SYSTEM_ACTOR,
                event_type=SessionEventType.COMPOSITION_PROGRESS_RECORDED,
                summary=summary,
                stage=WorkflowStage.COMPOSITION,
                payload=CompositionProgressEventPayload(
                    job_id=job_id,
                    status=_enum_value(status),
                    progress_percent=progress_percent,
                    current_segment_index=current_segment_index,
                    total_segments=total_segments,
                    segment_id=segment_id,
                ),
            )
            if _should_refresh_memory_for_job_status(_enum_value(status)):
                self._refresh_memory_snapshot(session_id, event)
            return event

        def record_audio_progress(
            self,
            session_id: str,
            *,
            job_id: str,
            status: str | Enum,
            progress_percent: float | None = None,
            current_segment_index: int | None = None,
            total_segments: int | None = None,
            segment_id: str | None = None,
            estimated_duration_seconds: int | None = None,
            voice_key: str | None = None,
            actor: SessionEventActor | None = None,
        ) -> EventLogEntry:
            summary = (
                f"Audio progress {progress_percent:.1f}%."
                if progress_percent is not None
                else "Recorded audio progress."
            )
            event = self.append_event(
                session_id,
                actor=actor or DEFAULT_SYSTEM_ACTOR,
                event_type=SessionEventType.AUDIO_PROGRESS_RECORDED,
                summary=summary,
                stage=WorkflowStage.AUDIO,
                payload=AudioProgressEventPayload(
                    job_id=job_id,
                    status=_enum_value(status),
                    progress_percent=progress_percent,
                    current_segment_index=current_segment_index,
                    total_segments=total_segments,
                    segment_id=segment_id,
                    estimated_duration_seconds=estimated_duration_seconds,
                    voice_key=voice_key,
                ),
            )
            if _should_refresh_memory_for_job_status(_enum_value(status)):
                self._refresh_memory_snapshot(session_id, event)
            return event

        def _refresh_memory_snapshot(
            self,
            session_id: str,
            event: EventLogEntry,
        ) -> None:
            SessionMemoryService(self._session).refresh_summary(
                session_id,
                trigger_event=event,
            )


    def _build_session_event_view(row: EventLogEntry) -> SessionEventView:
        return SessionEventView(
            id=row.id,
            session_id=row.session_id,
            sequence_number=row.sequence_number,
            actor=SessionEventActor(
                actor_type=row.actor_type,

## Command Started

- Time: `2026-04-01T07:41:48-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `109`
- Summary: in progress: /bin/zsh -lc "sed -n '1,120p' docs/README.md"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,120p' docs/README.md"
    Status: in progress

## Command Finished

- Time: `2026-04-01T07:41:48-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `110`
- Summary: completed, exit 0: /bin/zsh -lc "sed -n '1,120p' docs/README.md"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,120p' docs/README.md"
    Status: completed
    Exit code: 0
    Output:
    # Docs

    This directory holds product notes, architecture notes, ADRs, diagrams, and other reviewer-oriented documentation.

    Current entrypoints:

    - `product-brief.md`: product expectations and workflow
    - `architecture-overview.md`: target system shape and durable boundaries
    - `domain-model.md`: durable session entities, workflow-stage contract, and stage-state rules
    - `chat-to-ui-actions.md`: proposed action contract, action catalog, default confirmation policy, and deterministic action-policy evaluator
    - `chat-action-echoes.md`: transcript echo rules, durable wiring, and compact summary guidelines for UI and chat actions
    - `chat-to-ui-actions.schema.json`: machine-readable schema bundle for chat-to-UI proposed actions
    - `event-taxonomy.md`: append-only event families, payload versioning rules, and helper usage
    - `realtime-events.md`: session-channel contract, live event families, replay rules, and local auth assumptions
    - `realtime-events.schema.json`: machine-readable schema bundle for subscription frames and session events
    - `genre-tone-catalog.md`: curated catalog provenance, editing rules, and seed command
    - `storage-buckets-and-prefixes.md`: bucket roles, stable object-key conventions, and storage usage
    - `system-diagram.md`: one-page runtime diagram for browser, API, worker, storage, and Gemini flows
    - `contributing.md`: shared quality commands and code-style conventions
    - `adr/`: architecture decision records, starting with the core runtime architecture ADR

## Agent Message

- Time: `2026-04-01T07:42:04-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `111`
- Summary: I’m adding the typed tool contracts first. That gives the registry, the worker, and the action router one canonical set of request/response shapes before I wire execution on top.

### Full Text

    I’m adding the typed tool contracts first. That gives the registry, the worker, and the action router one canonical set of request/response shapes before I wire execution on top.

## File Change Started

- Time: `2026-04-01T07:42:41-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `112`
- Summary: backend/app/models/story_tools.py

### Full Text

    backend/app/models/story_tools.py

    Additional details:
    {
      "status": "in_progress"
    }

## File Change Recorded

- Time: `2026-04-01T07:42:42-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `113`
- Summary: backend/app/models/story_tools.py

### Full Text

    backend/app/models/story_tools.py

    Additional details:
    {
      "status": "completed"
    }

## File Change Started

- Time: `2026-04-01T07:47:04-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `114`
- Summary: backend/app/services/story_tools.py

### Full Text

    backend/app/services/story_tools.py

    Additional details:
    {
      "status": "in_progress"
    }

## File Change Recorded

- Time: `2026-04-01T07:47:04-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `115`
- Summary: backend/app/services/story_tools.py

### Full Text

    backend/app/services/story_tools.py

    Additional details:
    {
      "status": "completed"
    }

## Agent Message

- Time: `2026-04-01T07:47:08-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `116`
- Summary: The contracts and service skeleton are in. I’m exporting them through the existing package surfaces next, then I’ll wire worker dispatch and the chat-action router onto the same registry.

### Full Text

    The contracts and service skeleton are in. I’m exporting them through the existing package surfaces next, then I’ll wire worker dispatch and the chat-action router onto the same registry.

## Codex Output

- Time: `2026-04-01T14:47:19.562683Z`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `117`
- Summary: ERROR codex_core::tools::router: error=apply_patch verification failed: Failed to find expected lines in /Users/kevin/code/storyteller/backend/app/models/__init__.py:

### Full Text

    ERROR codex_core::tools::router: error=apply_patch verification failed: Failed to find expected lines in /Users/kevin/code/storyteller/backend/app/models/__init__.py:

## Codex Output

- Time: `2026-04-01T07:47:19-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `118`
- Summary: "StorySetupView",

### Full Text

    "StorySetupView",

## Codex Output

- Time: `2026-04-01T07:47:19-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `119`
- Summary: "UpdateStorySetupAction",

### Full Text

    "UpdateStorySetupAction",

## Codex Output

- Time: `2026-04-01T07:47:19-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `120`
- Summary: "UpdateStorySetupValues",

### Full Text

    "UpdateStorySetupValues",

## Codex Output

- Time: `2026-04-01T07:47:19-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `121`
- Summary: "WorkflowStage",

### Full Text

    "WorkflowStage",

## Codex Output

- Time: `2026-04-01T07:47:19-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `122`
- Summary: "WorkflowStageDefinition",

### Full Text

    "WorkflowStageDefinition",

## Codex Output

- Time: `2026-04-01T07:47:19-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `123`
- Summary: "WorkflowStageState",

### Full Text

    "WorkflowStageState",

## Codex Output

- Time: `2026-04-01T07:47:19-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `124`
- Summary: "SessionActionDecision",

### Full Text

    "SessionActionDecision",

## Command Started

- Time: `2026-04-01T07:47:25-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `125`
- Summary: in progress: /bin/zsh -lc "sed -n '120,260p' backend/app/models/__init__.py"

### Full Text

    Command: /bin/zsh -lc "sed -n '120,260p' backend/app/models/__init__.py"
    Status: in progress

## Command Started

- Time: `2026-04-01T07:47:25-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `126`
- Summary: in progress: /bin/zsh -lc "sed -n '260,420p' backend/app/models/__init__.py"

### Full Text

    Command: /bin/zsh -lc "sed -n '260,420p' backend/app/models/__init__.py"
    Status: in progress

## Command Finished

- Time: `2026-04-01T07:47:25-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `127`
- Summary: completed, exit 0: /bin/zsh -lc "sed -n '260,420p' backend/app/models/__init__.py"

### Full Text

    Command: /bin/zsh -lc "sed -n '260,420p' backend/app/models/__init__.py"
    Status: completed
    Exit code: 0
    Output:
    "OpenFinalizeViewValues",
        "PauseJobAction",
        "ParseChatIntentRequest",
        "PitchView",
        "ParsedChatIntentResponse",
        "RealtimeDeliveryMode",
        "RealtimeEventType",
        "RealtimeReplayStrategy",
        "RecentSessionSummary",
        "RecordSessionUIActionRequest",
        "RedirectCompositionAction",
        "RedirectCompositionValues",
        "RefineBeatSheetAction",
        "RefineBeatSheetValues",
        "RefineCharacterSheetAction",
        "RefineCharacterSheetValues",
        "RegenerateBeatSheetAction",
        "RegenerateBeatSheetValues",
        "RegenerateCharacterSheetAction",
        "RegenerateCharacterSheetValues",
        "RegeneratePitchesAction",
        "RegeneratePitchesValues",
        "ResumeJobAction",
        "SelectionKind",
        "SelectCharacterSheetAction",
        "SelectCharacterSheetValues",
        "SelectGenreAction",
        "SelectGenreValues",
        "SelectPitchAction",
        "SelectPitchValues",
        "SelectToneAction",
        "SelectToneValues",
        "SelectionRecordedEventPayload",
        "SessionAssetView",
        "SessionActionDecision",
        "SessionActionPolicyEvaluation",
        "SessionActionPolicyEvaluationItem",
        "SessionActionPolicyEvaluationRequest",
        "SessionActionPolicyReason",
        "SessionActionPolicyRequestItem",
        "SessionActionPolicySideEffect",
        "SessionActionReasonCode",
        "SessionActionSideEffectKind",
        "SessionCatalogSelection",
        "SessionContextStageNoteValues",
        "SessionContextUpdateRequest",
        "SessionContextUpdateResponse",
        "SessionCreatedEventPayload",
        "SessionEventActor",
        "SessionEventType",
        "SessionEventView",
        "SessionHistoryView",
        "SessionRealtimeEvent",
        "SessionSubscriptionAck",
        "SessionSubscriptionRequest",
        "SessionProgress",
        "SessionSnapshot",
        "SessionStageStateView",
        "StoryBriefView",
        "StoryBriefEditMode",
        "StartAudioGenerationAction",
        "StartAudioGenerationValues",
        "StartCompositionAction",
        "StartCompositionValues",
        "StorySetupView",
        "UIActionEchoEventPayload",
        "UIActionEchoRealtimeEvent",
        "UIActionEchoResult",
        "UIActionRecordedEventPayload",
        "UpdateAudioSettingsAction",
        "UpdateAudioSettingsValues",
        "UpdateStoryBriefAction",
        "UpdateStoryBriefValues",
        "UpdateStorySetupAction",
        "UpdateStorySetupValues",
        "WORKFLOW_STAGE_DEFINITIONS",
        "WORKFLOW_STAGE_SEQUENCE",
        "WORKFLOW_STAGE_STATES",
        "ToneCatalogEntry",
        "ToneCatalogSeed",
        "build_action_policy_request_from_batch",
        "UserEditRecordedEventPayload",
        "UserEditTargetKind",
        "WorkflowStage",
        "WorkflowStageDefinition",
        "WorkflowStageState",
        "WorkflowStageChangedEventPayload",
        "WorkflowStageChangedRealtimeEvent",
        "build_session_channel_name",
        "get_chat_to_ui_action_default_policy",
        "get_chat_to_ui_action_schema_bundle",
        "get_realtime_contract_schema_bundle",
        "get_invalidated_stages_after_edit",
        "get_workflow_stage_definition",
        "parse_event_payload",
        "resolve_resume_stage",
        "serialize_event_payload",
    ]

## Command Finished

- Time: `2026-04-01T07:47:25-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `128`
- Summary: completed, exit 0: /bin/zsh -lc "sed -n '120,260p' backend/app/models/__init__.py"

### Full Text

    Command: /bin/zsh -lc "sed -n '120,260p' backend/app/models/__init__.py"
    Status: completed
    Exit code: 0
    Output:
    from app.models.realtime import (
        ChatContentFormat,
        ChatMessageEventPayload,
        ChatMessageRealtimeEvent,
        CompositionChunkEventPayload,
        CompositionChunkKind,
        CompositionChunkRealtimeEvent,
        ErrorNotificationEventPayload,
        ErrorNotificationRealtimeEvent,
        ErrorSeverity,
        JobKind,
        JobProgressEventPayload,
        JobProgressRealtimeEvent,
        JobStatusEventPayload,
        JobStatusRealtimeEvent,
        RealtimeDeliveryMode,
        RealtimeEventType,
        RealtimeJobStatus,
        RealtimeReplayStrategy,
        SessionRealtimeEvent,
        SessionSubscriptionAck,
        SessionSubscriptionRequest,
        UIActionEchoEventPayload,
        UIActionEchoRealtimeEvent,
        UIActionEchoResult,
        WorkflowStageChangedRealtimeEvent,
        build_session_channel_name,
        get_realtime_contract_schema_bundle,
    )
    from app.models.session import (
        AudioJobView,
        BeatSheetView,
        CharacterSheetView,
        CompositionJobView,
        ConversationMemorySnapshotView,
        ConversationMemorySummaryData,
        ConversationMemoryWorkflow,
        CreateSessionRequest,
        ExportAssetView,
        PitchView,
        RecentSessionSummary,
        RecordSessionUIActionRequest,
        SessionAssetView,
        SessionCatalogSelection,
        SessionContextStageNoteValues,
        SessionContextUpdateRequest,
        SessionContextUpdateResponse,
        SessionProgress,
        SessionSnapshot,
        SessionStageStateView,
        StoryBriefView,
        StorySetupView,
    )
    from app.models.system import DependencyStatus, HealthResponse, HelloResponse
    from app.models.workflow import (
        WORKFLOW_STAGE_DEFINITIONS,
        WORKFLOW_STAGE_SEQUENCE,
        WORKFLOW_STAGE_STATES,
        WorkflowStage,
        WorkflowStageDefinition,
        WorkflowStageState,
        get_invalidated_stages_after_edit,
        get_workflow_stage_definition,
        resolve_resume_stage,
    )

    __all__ = [
        "AIOutputKind",
        "AIOutputRecordedEventPayload",
        "AcceptBeatSheetAction",
        "AcceptBeatSheetValues",
        "AudioJobView",
        "AudioProgressEventPayload",
        "BeatSheetView",
        "CHAT_TO_UI_ACTION_SCHEMA_VERSION",
        "SESSION_ACTION_POLICY_SCHEMA_VERSION",
        "ChatIntentParsedEventPayload",
        "ChatMessageRecordedEventPayload",
        "ChatMessageRole",
        "ChatContentFormat",
        "ChatMessageEventPayload",
        "ChatMessageRealtimeEvent",
        "ChatToUIAction",
        "ChatToUIActionBase",
        "ChatToUIActionBatch",
        "ChatToUIActionDefaultPolicy",
        "ChatToUIActionType",
        "ChatToUIExtractedValues",
        "ChatToUIJobKind",
        "CharacterSheetView",
        "ConversationMemorySnapshotView",
        "ConversationMemorySummaryData",
        "ConversationMemoryWorkflow",
        "CompositionStartMode",
        "CompositionChunkEventPayload",
        "CompositionChunkKind",
        "CompositionChunkRealtimeEvent",
        "CompositionProgressEventPayload",
        "CompositionJobView",
        "CreateSessionRequest",
        "DEFAULT_CHAT_TO_UI_ACTION_POLICIES",
        "DependencyStatus",
        "DownloadAssetAction",
        "DownloadAssetKind",
        "DownloadAssetValues",
        "EXPLICIT_CHAT_COMMAND_MODEL_ID",
        "EXPLICIT_CHAT_COMMAND_PROMPT_VERSION",
        "ErrorNotificationEventPayload",
        "ErrorNotificationRealtimeEvent",
        "ErrorSeverity",
        "EventActorType",
        "EventPayload",
        "ExplicitChatCommandId",
        "ExplicitChatCommandRequest",
        "ExplicitChatCommandSource",
        "ExportAssetView",
        "FinalizeView",
        "GenreCatalogEntry",
        "GenreCatalogSeed",
        "GenreToneCatalogDocument",
        "HealthResponse",
        "HelloResponse",
        "INTENT_PARSER_PROMPT_VERSION",
        "INTENT_PARSER_SCHEMA_VERSION",
        "IntentParserCandidateAction",
        "IntentParserCandidateActionBatch",
        "IntentParserInvocation",
        "IntentParserInvocationResult",
        "IntentParserPromptContext",
        "IntentParserStageContext",
        "IntentParserStatus",
        "IntentParserStructuredOutput",
        "JobKind",
        "JobProgressEventPayload",
        "JobProgressRealtimeEvent",
        "RealtimeJobStatus",
        "JobStatusEventPayload",
        "JobStatusRealtimeEvent",
        "NavigateToStageAction",
        "OpenFinalizeViewAction",
        "OpenFinalizeViewValues",

## Command Started

- Time: `2026-04-01T07:47:25-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `129`
- Summary: in progress: /bin/zsh -lc "rg -n \"from app.models.session|from app.models.system|__all__ = \\[|StorySetupView|UpdateStorySetupAction|StartAudioGenerationAction|WorkflowStageDefinition\" backend/app/models/__init__.py"

### Full Text

    Command: /bin/zsh -lc "rg -n \"from app.models.session|from app.models.system|__all__ = \\[|StorySetupView|UpdateStorySetupAction|StartAudioGenerationAction|WorkflowStageDefinition\" backend/app/models/__init__.py"
    Status: in progress

## Command Finished

- Time: `2026-04-01T07:47:25-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `130`
- Summary: completed, exit 0: /bin/zsh -lc "rg -n \"from app.models.session|from app.models.system|__all__ = \\[|StorySetupView|UpdateStorySetupAction|StartAudioGenerationAction|WorkflowStageDefinition\" backend/app/models/__init__.py"

### Full Text

    Command: /bin/zsh -lc "rg -n \"from app.models.session|from app.models.system|__all__ = \\[|StorySetupView|UpdateStorySetupAction|StartAudioGenerationAction|WorkflowStageDefinition\" backend/app/models/__init__.py"
    Status: completed
    Exit code: 0
    Output:
    63:    StartAudioGenerationAction,
    72:    UpdateStorySetupAction,
    149:from app.models.session import (
    171:    StorySetupView,
    173:from app.models.system import DependencyStatus, HealthResponse, HelloResponse
    179:    WorkflowStageDefinition,
    186:__all__ = [
    320:    "StartAudioGenerationAction",
    324:    "StorySetupView",
    333:    "UpdateStorySetupAction",
    344:    "WorkflowStageDefinition",

## Codex Output

- Time: `2026-04-01T14:47:40.616702Z`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `131`
- Summary: ERROR codex_core::tools::router: error=apply_patch verification failed: Failed to find expected lines in /Users/kevin/code/storyteller/backend/app/models/__init__.py:

### Full Text

    ERROR codex_core::tools::router: error=apply_patch verification failed: Failed to find expected lines in /Users/kevin/code/storyteller/backend/app/models/__init__.py:

## Codex Output

- Time: `2026-04-01T07:47:40-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `132`
- Summary: "EstimateAudioLengthToolInput",

### Full Text

    "EstimateAudioLengthToolInput",

## File Change Started

- Time: `2026-04-01T07:48:02-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `133`
- Summary: backend/app/models/__init__.py

### Full Text

    backend/app/models/__init__.py

    Additional details:
    {
      "status": "in_progress"
    }

## File Change Recorded

- Time: `2026-04-01T07:48:02-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `134`
- Summary: backend/app/models/__init__.py

### Full Text

    backend/app/models/__init__.py

    Additional details:
    {
      "status": "completed"
    }

## File Change Started

- Time: `2026-04-01T07:48:18-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `135`
- Summary: backend/app/models/__init__.py

### Full Text

    backend/app/models/__init__.py

    Additional details:
    {
      "status": "in_progress"
    }

## File Change Recorded

- Time: `2026-04-01T07:48:18-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `136`
- Summary: backend/app/models/__init__.py

### Full Text

    backend/app/models/__init__.py

    Additional details:
    {
      "status": "completed"
    }

## File Change Started

- Time: `2026-04-01T07:48:27-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `137`
- Summary: backend/app/services/__init__.py

### Full Text

    backend/app/services/__init__.py

    Additional details:
    {
      "status": "in_progress"
    }

## File Change Recorded

- Time: `2026-04-01T07:48:27-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `138`
- Summary: backend/app/services/__init__.py

### Full Text

    backend/app/services/__init__.py

    Additional details:
    {
      "status": "completed"
    }

## File Change Started

- Time: `2026-04-01T07:48:39-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `139`
- Summary: backend/app/worker/runtime.py

### Full Text

    backend/app/worker/runtime.py

    Additional details:
    {
      "status": "in_progress"
    }

## File Change Recorded

- Time: `2026-04-01T07:48:39-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `140`
- Summary: backend/app/worker/runtime.py

### Full Text

    backend/app/worker/runtime.py

    Additional details:
    {
      "status": "completed"
    }

## File Change Started

- Time: `2026-04-01T07:48:50-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `141`
- Summary: backend/app/worker/default_handlers.py

### Full Text

    backend/app/worker/default_handlers.py

    Additional details:
    {
      "status": "in_progress"
    }

## File Change Recorded

- Time: `2026-04-01T07:48:50-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `142`
- Summary: backend/app/worker/default_handlers.py

### Full Text

    backend/app/worker/default_handlers.py

    Additional details:
    {
      "status": "completed"
    }

## Agent Message

- Time: `2026-04-01T07:49:00-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `143`
- Summary: I’m wiring the registry into the intent-parser prompt now. The parser will still emit chat actions, but it will see the shared backend tool catalog that those actions map onto, so the vocabulary stops drifting between orchestration layers.

### Full Text

    I’m wiring the registry into the intent-parser prompt now. The parser will still emit chat actions, but it will see the shared backend tool catalog that those actions map onto, so the vocabulary stops drifting between orchestration layers.

## File Change Started

- Time: `2026-04-01T07:49:06-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `144`
- Summary: backend/app/ai/intent_parser.py

### Full Text

    backend/app/ai/intent_parser.py

    Additional details:
    {
      "status": "in_progress"
    }

## File Change Recorded

- Time: `2026-04-01T07:49:06-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `145`
- Summary: backend/app/ai/intent_parser.py

### Full Text

    backend/app/ai/intent_parser.py

    Additional details:
    {
      "status": "completed"
    }

## File Change Started

- Time: `2026-04-01T07:49:10-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `146`
- Summary: backend/app/ai/prompts/intent_parser.md

### Full Text

    backend/app/ai/prompts/intent_parser.md

    Additional details:
    {
      "status": "in_progress"
    }

## File Change Recorded

- Time: `2026-04-01T07:49:10-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `147`
- Summary: backend/app/ai/prompts/intent_parser.md

### Full Text

    backend/app/ai/prompts/intent_parser.md

    Additional details:
    {
      "status": "completed"
    }

## Agent Message

- Time: `2026-04-01T07:49:22-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `148`
- Summary: The core wiring is in place. I’m running lint on the touched backend files now to catch import drift, line-length issues, and any typing mistakes before I add the verification tests.

### Full Text

    The core wiring is in place. I’m running lint on the touched backend files now to catch import drift, line-length issues, and any typing mistakes before I add the verification tests.

## Command Started

- Time: `2026-04-01T07:49:23-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `149`
- Summary: in progress: /bin/zsh -lc 'python -m ruff check backend/app/models/story_tools.py backend/app/services/story_tools.py backend/app/worker/runtime.py backend/app/worker/default_handlers.py backend/app/ai/intent_parser.py backend/app/models/__init__.py backend/app/services/__init__.py'

### Full Text

    Command: /bin/zsh -lc 'python -m ruff check backend/app/models/story_tools.py backend/app/services/story_tools.py backend/app/worker/runtime.py backend/app/worker/default_handlers.py backend/app/ai/intent_parser.py backend/app/models/__init__.py backend/app/services/__init__.py'
    Status: in progress

## Command Finished

- Time: `2026-04-01T07:49:23-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `150`
- Summary: failed, exit 1: /bin/zsh -lc 'python -m ruff check backend/app/models/story_tools.py backend/app/services/story_tools.py backend/app/worker/runtime.py backend/app/worker/default_handlers.py backend/app/ai/intent_parser.py backend/app/models/__init__.py backend/app/services/__init__.py'

### Full Text

    Command: /bin/zsh -lc 'python -m ruff check backend/app/models/story_tools.py backend/app/services/story_tools.py backend/app/worker/runtime.py backend/app/worker/default_handlers.py backend/app/ai/intent_parser.py backend/app/models/__init__.py backend/app/services/__init__.py'
    Status: failed
    Exit code: 1
    Output:
    E902 No such file or directory (os error 2)
    --> backend/app/ai/intent_parser.py:1:1

    E902 No such file or directory (os error 2)
    --> backend/app/models/__init__.py:1:1

    E902 No such file or directory (os error 2)
    --> backend/app/models/story_tools.py:1:1

    E902 No such file or directory (os error 2)
    --> backend/app/services/__init__.py:1:1

    E902 No such file or directory (os error 2)
    --> backend/app/services/story_tools.py:1:1

    E902 No such file or directory (os error 2)
    --> backend/app/worker/default_handlers.py:1:1

    E902 No such file or directory (os error 2)
    --> backend/app/worker/runtime.py:1:1

    Found 7 errors.

## Agent Message

- Time: `2026-04-01T07:49:34-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `151`
- Summary: I ran lint from the backend directory with repo-root paths by mistake. I’m rerunning against the correct module paths and then I’ll fix the import and style issues it reports.

### Full Text

    I ran lint from the backend directory with repo-root paths by mistake. I’m rerunning against the correct module paths and then I’ll fix the import and style issues it reports.

## Command Started

- Time: `2026-04-01T07:49:36-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `152`
- Summary: in progress: /bin/zsh -lc 'python -m ruff check app/models/story_tools.py app/services/story_tools.py app/worker/runtime.py app/worker/default_handlers.py app/ai/intent_parser.py app/models/__init__.py app/services/__init__.py'

### Full Text

    Command: /bin/zsh -lc 'python -m ruff check app/models/story_tools.py app/services/story_tools.py app/worker/runtime.py app/worker/default_handlers.py app/ai/intent_parser.py app/models/__init__.py app/services/__init__.py'
    Status: in progress

## Command Finished

- Time: `2026-04-01T07:49:36-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `153`
- Summary: failed, exit 1: /bin/zsh -lc 'python -m ruff check app/models/story_tools.py app/services/story_tools.py app/worker/runtime.py app/worker/default_handlers.py app/ai/intent_parser.py app/models/__init__.py app/services/__init__.py'

### Full Text

    Command: /bin/zsh -lc 'python -m ruff check app/models/story_tools.py app/services/story_tools.py app/worker/runtime.py app/worker/default_handlers.py app/ai/intent_parser.py app/models/__init__.py app/services/__init__.py'
    Status: failed
    Exit code: 1
    Output:
    F401 [*] `app.db.BeatSheet` imported but unused
      --> app/services/story_tools.py:13:5
       |
    11 | from app.db import (
    12 |     AudioJob,
    13 |     BeatSheet,
       |     ^^^^^^^^^
    14 |     CharacterSheet,
    15 |     CompositionJob,
       |
    help: Remove unused import: `app.db.BeatSheet`

    F401 [*] `app.models.ChatToUIJobKind` imported but unused
      --> app/services/story_tools.py:26:5
       |
    24 |     ChatToUIActionBatch,
    25 |     ChatToUIActionType,
    26 |     ChatToUIJobKind,
       |     ^^^^^^^^^^^^^^^
    27 |     CompositionStartMode,
    28 |     SelectionKind,
       |
    help: Remove unused import: `app.models.ChatToUIJobKind`

    F401 [*] `app.models.chat_actions.UpdateStorySetupAction` imported but unused
      --> app/services/story_tools.py:38:5
       |
    36 |     StartAudioGenerationAction,
    37 |     StartCompositionAction,
    38 |     UpdateStorySetupAction,
       |     ^^^^^^^^^^^^^^^^^^^^^^
    39 | )
    40 | from app.models.story_tools import (
       |
    help: Remove unused import: `app.models.chat_actions.UpdateStorySetupAction`

    E501 Line too long (104 > 100)
       --> app/services/story_tools.py:108:101
        |
    107 |     def list_tools(self) -> tuple[StoryWorkflowToolDefinition, ...]:
    108 |         return tuple(self._by_name[name] for name in sorted(self._by_name, key=lambda item: item.value))
        |                                                                                                     ^^^^
    109 |
    110 |     def validate_arguments(
        |

    E501 Line too long (102 > 100)
       --> app/services/story_tools.py:134:101
        |
    132 |                     ],
    133 |                     "side_effects": [
    134 |                         side_effect.model_dump(mode="json") for side_effect in definition.side_effects
        |                                                                                                     ^^
    135 |                     ],
    136 |                     "input_schema": definition.request_model.model_json_schema(),
        |

    E501 Line too long (103 > 100)
       --> app/services/story_tools.py:294:101
        |
    292 |                     _side_effect(
    293 |                         StoryWorkflowToolSideEffectKind.UPDATE_WORKFLOW_STAGE,
    294 |                         "Marks story setup complete and invalidates composition, audio, and finalize.",
        |                                                                                                     ^^^
    295 |                         stages=[
    296 |                             WorkflowStage.STORY_SETUP,
        |

    E501 Line too long (102 > 100)
       --> app/services/story_tools.py:361:101
        |
    359 |                     _side_effect(
    360 |                         StoryWorkflowToolSideEffectKind.CREATE_SEGMENT,
    361 |                         "Creates a new composition-segment revision starting from the rewrite point.",
        |                                                                                                     ^^
    362 |                         stages=[WorkflowStage.COMPOSITION],
    363 |                         writes_to=["composition_segments"],
        |

    E501 Line too long (105 > 100)
       --> app/services/story_tools.py:397:101
        |
    395 |                 name=StoryWorkflowToolName.START_AUDIO_GENERATION,
    396 |                 stage=WorkflowStage.AUDIO,
    397 |                 description="Create a durable audio job using the latest story text and audio settings.",
        |                                                                                                     ^^^^^
    398 |                 execution_mode=StoryWorkflowToolExecutionMode.BACKGROUND,
    399 |                 job_type="story.start_audio_generation",
        |

    E501 Line too long (102 > 100)
       --> app/services/story_tools.py:625:101
        |
    623 |                 f"Generating {request.candidate_count} pitch candidates.",
    624 |                 _optional_detail("Guidance", request.guidance),
    625 |                 "Preserving the current selected pitch." if request.preserve_selected_pitch else None,
        |                                                                                                     ^^
    626 |             ]
    627 |         )
        |

    E501 Line too long (117 > 100)
       --> app/services/story_tools.py:851:101
        |
    850 |         changed_fields = sorted(
    851 |             field for field, value in request.model_dump(mode="json", exclude_none=True).items() if value is not None
        |                                                                                                     ^^^^^^^^^^^^^^^^^
    852 |         )
    853 |         self._events.record_user_edit(
        |

    E501 Line too long (103 > 100)
       --> app/services/story_tools.py:912:101
        |
    910 |             reason="Cancelled because a new composition pass started.",
    911 |         )
    912 |         next_segment_index = request.restart_from_segment_index or self._next_segment_index(session_id)
        |                                                                                                     ^^^
    913 |         job = CompositionJob(
    914 |             session_id=session_id,
        |

    E501 Line too long (121 > 100)
        --> app/services/story_tools.py:1301:101
         |
    1299 |         if character_sheet_id is None and revision_number is None:
    1300 |             stmt = stmt.where(CharacterSheet.is_selected.is_(True))
    1301 |         sheet = self._session.execute(stmt.order_by(CharacterSheet.revision_number.desc()).limit(1)).scalar_one_or_none()
         |                                                                                                     ^^^^^^^^^^^^^^^^^^^^^
    1302 |         if sheet is None:
    1303 |             raise StoryWorkflowToolServiceError(
         |

    I001 [*] Import block is un-sorted or un-formatted
     --> app/worker/default_handlers.py:1:1
      |
    1 | / from __future__ import annotations
    2 | |
    3 | | import time
    4 | | from typing import Any
    5 | |
    6 | | from app.services.story_tools import get_story_workflow_tool_registry, StoryWorkflowToolService
    7 | | from app.worker.registry import JobHandlerRegistry
    8 | | from app.worker.runtime import JobExecutionContext
      | |__________________________________________________^
      |
    help: Organize imports

    Found 13 errors.
    [*] 4 fixable with the `--fix` option.

## Codex Output

- Time: `2026-04-01T14:50:14.715164Z`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `154`
- Summary: ERROR codex_core::tools::router: error=apply_patch verification failed: Failed to find expected lines in /Users/kevin/code/storyteller/backend/app/services/story_tools.py:

### Full Text

    ERROR codex_core::tools::router: error=apply_patch verification failed: Failed to find expected lines in /Users/kevin/code/storyteller/backend/app/services/story_tools.py:

## Codex Output

- Time: `2026-04-01T07:50:14-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `155`
- Summary: def list_tools(self) -> tuple[StoryWorkflowToolDefinition, ...]:

### Full Text

    def list_tools(self) -> tuple[StoryWorkflowToolDefinition, ...]:

## Codex Output

- Time: `2026-04-01T07:50:14-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `156`
- Summary: return tuple(self._by_name[name] for name in sorted(self._by_name, key=lambda item: item.value))

### Full Text

    return tuple(self._by_name[name] for name in sorted(self._by_name, key=lambda item: item.value))

## Command Started

- Time: `2026-04-01T07:50:30-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `157`
- Summary: in progress: /bin/zsh -lc "sed -n '1288,1310p' app/services/story_tools.py"

### Full Text

    Command: /bin/zsh -lc "sed -n '1288,1310p' app/services/story_tools.py"
    Status: in progress

## Command Started

- Time: `2026-04-01T07:50:30-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `158`
- Summary: in progress: /bin/zsh -lc "sed -n '612,660p' app/services/story_tools.py"

### Full Text

    Command: /bin/zsh -lc "sed -n '612,660p' app/services/story_tools.py"
    Status: in progress

## Command Started

- Time: `2026-04-01T07:50:30-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `159`
- Summary: in progress: /bin/zsh -lc "sed -n '1,120p' app/services/story_tools.py"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,120p' app/services/story_tools.py"
    Status: in progress

## Command Started

- Time: `2026-04-01T07:50:30-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `160`
- Summary: in progress: /bin/zsh -lc "sed -n '280,420p' app/services/story_tools.py"

### Full Text

    Command: /bin/zsh -lc "sed -n '280,420p' app/services/story_tools.py"
    Status: in progress

## Command Started

- Time: `2026-04-01T07:50:30-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `161`
- Summary: in progress: /bin/zsh -lc "sed -n '100,180p' app/services/story_tools.py"

### Full Text

    Command: /bin/zsh -lc "sed -n '100,180p' app/services/story_tools.py"
    Status: in progress

## Command Finished

- Time: `2026-04-01T07:50:30-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `162`
- Summary: completed, exit 0: /bin/zsh -lc "sed -n '1288,1310p' app/services/story_tools.py"

### Full Text

    Command: /bin/zsh -lc "sed -n '1288,1310p' app/services/story_tools.py"
    Status: completed
    Exit code: 0
    Output:
    self,
            *,
            session_id: str,
            character_sheet_id: str | None,
            revision_number: int | None,
        ) -> CharacterSheet:
            stmt = select(CharacterSheet).where(CharacterSheet.session_id == session_id)
            if character_sheet_id is not None:
                stmt = stmt.where(CharacterSheet.id == character_sheet_id)
            if revision_number is not None:
                stmt = stmt.where(CharacterSheet.revision_number == revision_number)
            if character_sheet_id is None and revision_number is None:
                stmt = stmt.where(CharacterSheet.is_selected.is_(True))
            sheet = self._session.execute(stmt.order_by(CharacterSheet.revision_number.desc()).limit(1)).scalar_one_or_none()
            if sheet is None:
                raise StoryWorkflowToolServiceError(
                    "refine_character_sheet requires a matching character sheet in session",
                )
            return sheet


    def _side_effect(
        kind: StoryWorkflowToolSideEffectKind,

## Command Started

- Time: `2026-04-01T07:50:30-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `163`
- Summary: in progress: /bin/zsh -lc "sed -n '844,924p' app/services/story_tools.py"

### Full Text

    Command: /bin/zsh -lc "sed -n '844,924p' app/services/story_tools.py"
    Status: in progress

## Command Finished

- Time: `2026-04-01T07:50:30-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `164`
- Summary: completed, exit 0: /bin/zsh -lc "sed -n '612,660p' app/services/story_tools.py"

### Full Text

    Command: /bin/zsh -lc "sed -n '612,660p' app/services/story_tools.py"
    Status: completed
    Exit code: 0
    Output:
    def _generate_pitches(
            self,
            *,
            session_id: str,
            request: GeneratePitchesToolInput,
            actor: SessionEventActor | None = None,
        ) -> StageOperationToolResult:
            self._sessions.load_session_snapshot(session_id)
            detail = _join_detail_parts(
                [
                    f"Generating {request.candidate_count} pitch candidates.",
                    _optional_detail("Guidance", request.guidance),
                    "Preserving the current selected pitch." if request.preserve_selected_pitch else None,
                ]
            )
            snapshot = self._transition_stage_to_in_progress(
                session_id,
                stage=WorkflowStage.PITCHES,
                detail=detail,
                actor=actor,
            )
            return StageOperationToolResult(
                tool_name=StoryWorkflowToolName.GENERATE_PITCHES,
                stage=WorkflowStage.PITCHES,
                summary="Queued pitch generation from the current bedtime brief.",
                stage_status=_stage_status(snapshot, WorkflowStage.PITCHES),
                detail=detail,
            )

        def _refine_pitch(
            self,
            *,
            session_id: str,
            request: RefinePitchToolInput,
            actor: SessionEventActor | None = None,
        ) -> StageOperationToolResult:
            self._require_pitch(session_id, request)
            detail = _join_detail_parts(
                [
                    "Refining the current pitch direction.",
                    _optional_detail("Instructions", request.instructions),
                ]
            )
            snapshot = self._transition_stage_to_in_progress(
                session_id,
                stage=WorkflowStage.PITCHES,
                detail=detail,
                actor=actor,

## Command Finished

- Time: `2026-04-01T07:50:30-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `165`
- Summary: completed, exit 0: /bin/zsh -lc "sed -n '1,120p' app/services/story_tools.py"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,120p' app/services/story_tools.py"
    Status: completed
    Exit code: 0
    Output:
    from __future__ import annotations

    import math
    from dataclasses import dataclass
    from functools import lru_cache
    from typing import Any

    from sqlalchemy import Select, func, select
    from sqlalchemy.orm import Session

    from app.db import (
        AudioJob,
        BeatSheet,
        CharacterSheet,
        CompositionJob,
        CompositionJobKind,
        CompositionSegment,
        JobStatus,
        Pitch,
        StorySetup,
    )
    from app.db.base import utc_now
    from app.models import (
        ChatToUIActionBatch,
        ChatToUIActionType,
        ChatToUIJobKind,
        CompositionStartMode,
        SelectionKind,
        SessionEventActor,
        UserEditTargetKind,
        WorkflowStage,
        WorkflowStageState,
    )
    from app.models.chat_actions import (
        RedirectCompositionAction,
        StartAudioGenerationAction,
        StartCompositionAction,
        UpdateStorySetupAction,
    )
    from app.models.story_tools import (
        AudioLengthEstimateSource,
        ComposeNextSegmentToolInput,
        CompositionToolResult,
        EstimateAudioLengthToolInput,
        EstimateAudioLengthToolResult,
        GenerateBeatSheetToolInput,
        GenerateCharacterSheetsToolInput,
        GeneratePitchesToolInput,
        RefineCharacterSheetToolInput,
        RefinePitchToolInput,
        RewriteSegmentsToolInput,
        StageOperationToolResult,
        StartAudioGenerationToolInput,
        StartAudioGenerationToolResult,
        StoryWorkflowToolCall,
        StoryWorkflowToolExecutionMode,
        StoryWorkflowToolName,
        StoryWorkflowToolPlan,
        StoryWorkflowToolResultBase,
        StoryWorkflowToolSideEffect,
        StoryWorkflowToolSideEffectKind,
        UpdateSetupHeuristicsToolInput,
        UpdateSetupHeuristicsToolResult,
    )
    from app.repositories import StorySessionRepository
    from app.services.event_log import DEFAULT_SYSTEM_ACTOR, SessionEventLogService
    from app.services.jobs import BackgroundJobRecord, BackgroundJobService
    from app.services.sessions import SessionNotFoundError, SessionService

    ESTIMATED_NARRATION_WORDS_PER_MINUTE = 140


    class StoryWorkflowToolServiceError(Exception):
        """Base error for tool-registry backed story workflow operations."""


    @dataclass(frozen=True)
    class StoryWorkflowToolDefinition:
        name: StoryWorkflowToolName
        stage: WorkflowStage
        description: str
        execution_mode: StoryWorkflowToolExecutionMode
        job_type: str
        request_model: type
        response_model: type[StoryWorkflowToolResultBase]
        side_effects: tuple[StoryWorkflowToolSideEffect, ...]
        related_chat_actions: tuple[ChatToUIActionType, ...] = ()
        executor_name: str = ""


    class StoryWorkflowToolRegistry:
        def __init__(self, definitions: list[StoryWorkflowToolDefinition]) -> None:
            self._by_name = {definition.name: definition for definition in definitions}
            self._by_job_type = {definition.job_type: definition for definition in definitions}
            if len(self._by_name) != len(definitions):
                raise ValueError("tool names must be unique")
            if len(self._by_job_type) != len(definitions):
                raise ValueError("worker job types must be unique")

        def get(self, tool_name: StoryWorkflowToolName | str) -> StoryWorkflowToolDefinition:
            normalized = StoryWorkflowToolName(tool_name)
            return self._by_name[normalized]

        def get_by_job_type(self, job_type: str) -> StoryWorkflowToolDefinition:
            return self._by_job_type[job_type]

        def list_tools(self) -> tuple[StoryWorkflowToolDefinition, ...]:
            return tuple(self._by_name[name] for name in sorted(self._by_name, key=lambda item: item.value))

        def validate_arguments(
            self,
            tool_name: StoryWorkflowToolName | str,
            arguments: dict[str, Any] | None,
        ):
            definition = self.get(tool_name)
            payload = arguments if isinstance(arguments, dict) else {}
            return definition.request_model.model_validate(payload)

        def build_schema_bundle(self) -> dict[str, Any]:
            return {

## Command Finished

- Time: `2026-04-01T07:50:30-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `166`
- Summary: completed, exit 0: /bin/zsh -lc "sed -n '280,420p' app/services/story_tools.py"

### Full Text

    Command: /bin/zsh -lc "sed -n '280,420p' app/services/story_tools.py"
    Status: completed
    Exit code: 0
    Output:
    ),
                    execution_mode=StoryWorkflowToolExecutionMode.DIRECT,
                    job_type="story.update_setup_heuristics",
                    request_model=UpdateSetupHeuristicsToolInput,
                    response_model=UpdateSetupHeuristicsToolResult,
                    side_effects=(
                        _side_effect(
                            StoryWorkflowToolSideEffectKind.CREATE_REVISION,
                            "Creates a selected story-setup revision.",
                            stages=[WorkflowStage.STORY_SETUP],
                            writes_to=["story_setups"],
                        ),
                        _side_effect(
                            StoryWorkflowToolSideEffectKind.UPDATE_WORKFLOW_STAGE,
                            "Marks story setup complete and invalidates composition, audio, and finalize.",
                            stages=[
                                WorkflowStage.STORY_SETUP,
                                WorkflowStage.COMPOSITION,
                                WorkflowStage.AUDIO,
                                WorkflowStage.FINALIZE,
                            ],
                            writes_to=["workflow_stage_states"],
                        ),
                    ),
                    related_chat_actions=(ChatToUIActionType.UPDATE_STORY_SETUP,),
                    executor_name="_update_setup_heuristics",
                ),
                StoryWorkflowToolDefinition(
                    name=StoryWorkflowToolName.COMPOSE_NEXT_SEGMENT,
                    stage=WorkflowStage.COMPOSITION,
                    description="Create the next durable composition job and seed the next segment.",
                    execution_mode=StoryWorkflowToolExecutionMode.BACKGROUND,
                    job_type="story.compose_next_segment",
                    request_model=ComposeNextSegmentToolInput,
                    response_model=CompositionToolResult,
                    side_effects=(
                        _side_effect(
                            StoryWorkflowToolSideEffectKind.CANCEL_ACTIVE_JOB,
                            "Cancels any still-active composition job before a new segment run starts.",
                            stages=[WorkflowStage.COMPOSITION],
                            writes_to=["composition_jobs"],
                        ),
                        _side_effect(
                            StoryWorkflowToolSideEffectKind.CREATE_JOB,
                            "Creates a composition job for the next segment pass.",
                            stages=[WorkflowStage.COMPOSITION],
                            writes_to=["composition_jobs"],
                        ),
                        _side_effect(
                            StoryWorkflowToolSideEffectKind.CREATE_SEGMENT,
                            "Seeds the next durable composition segment row.",
                            stages=[WorkflowStage.COMPOSITION],
                            writes_to=["composition_segments"],
                        ),
                    ),
                    related_chat_actions=(ChatToUIActionType.START_COMPOSITION,),
                    executor_name="_compose_next_segment",
                ),
                StoryWorkflowToolDefinition(
                    name=StoryWorkflowToolName.REWRITE_SEGMENTS,
                    stage=WorkflowStage.COMPOSITION,
                    description="Start a rewrite pass from an earlier composition segment.",
                    execution_mode=StoryWorkflowToolExecutionMode.BACKGROUND,
                    job_type="story.rewrite_segments",
                    request_model=RewriteSegmentsToolInput,
                    response_model=CompositionToolResult,
                    side_effects=(
                        _side_effect(
                            StoryWorkflowToolSideEffectKind.CANCEL_ACTIVE_JOB,
                            "Cancels any still-active composition job before a rewrite starts.",
                            stages=[WorkflowStage.COMPOSITION],
                            writes_to=["composition_jobs"],
                        ),
                        _side_effect(
                            StoryWorkflowToolSideEffectKind.CREATE_JOB,
                            "Creates a rewrite composition job.",
                            stages=[WorkflowStage.COMPOSITION],
                            writes_to=["composition_jobs"],
                        ),
                        _side_effect(
                            StoryWorkflowToolSideEffectKind.CREATE_SEGMENT,
                            "Creates a new composition-segment revision starting from the rewrite point.",
                            stages=[WorkflowStage.COMPOSITION],
                            writes_to=["composition_segments"],
                        ),
                    ),
                    related_chat_actions=(
                        ChatToUIActionType.START_COMPOSITION,
                        ChatToUIActionType.REDIRECT_COMPOSITION,
                    ),
                    executor_name="_rewrite_segments",
                ),
                StoryWorkflowToolDefinition(
                    name=StoryWorkflowToolName.ESTIMATE_AUDIO_LENGTH,
                    stage=WorkflowStage.AUDIO,
                    description=(
                        "Estimate narration duration from persisted composition text or story-setup "
                        "word-count guidance."
                    ),
                    execution_mode=StoryWorkflowToolExecutionMode.DIRECT,
                    job_type="story.estimate_audio_length",
                    request_model=EstimateAudioLengthToolInput,
                    response_model=EstimateAudioLengthToolResult,
                    side_effects=(
                        _side_effect(
                            StoryWorkflowToolSideEffectKind.COMPUTE_ESTIMATE,
                            "Computes a narration-length estimate without mutating durable state.",
                            stages=[WorkflowStage.AUDIO],
                            writes_to=[],
                        ),
                    ),
                    related_chat_actions=(ChatToUIActionType.START_AUDIO_GENERATION,),
                    executor_name="_estimate_audio_length",
                ),
                StoryWorkflowToolDefinition(
                    name=StoryWorkflowToolName.START_AUDIO_GENERATION,
                    stage=WorkflowStage.AUDIO,
                    description="Create a durable audio job using the latest story text and audio settings.",
                    execution_mode=StoryWorkflowToolExecutionMode.BACKGROUND,
                    job_type="story.start_audio_generation",
                    request_model=StartAudioGenerationToolInput,
                    response_model=StartAudioGenerationToolResult,
                    side_effects=(
                        _side_effect(
                            StoryWorkflowToolSideEffectKind.CANCEL_ACTIVE_JOB,
                            "Cancels any active audio job before starting a new narration run.",
                            stages=[WorkflowStage.AUDIO],
                            writes_to=["audio_jobs"],
                        ),
                        _side_effect(
                            StoryWorkflowToolSideEffectKind.CREATE_JOB,
                            "Creates a new audio job and records an initial duration estimate.",
                            stages=[WorkflowStage.AUDIO],
                            writes_to=["audio_jobs"],
                        ),
                        _side_effect(
                            StoryWorkflowToolSideEffectKind.UPDATE_WORKFLOW_STAGE,
                            "Marks the audio stage in progress for the new narration run.",
                            stages=[WorkflowStage.AUDIO],
                            writes_to=["workflow_stage_states"],
                        ),

## Command Finished

- Time: `2026-04-01T07:50:30-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `167`
- Summary: completed, exit 0: /bin/zsh -lc "sed -n '100,180p' app/services/story_tools.py"

### Full Text

    Command: /bin/zsh -lc "sed -n '100,180p' app/services/story_tools.py"
    Status: completed
    Exit code: 0
    Output:
    def get(self, tool_name: StoryWorkflowToolName | str) -> StoryWorkflowToolDefinition:
            normalized = StoryWorkflowToolName(tool_name)
            return self._by_name[normalized]

        def get_by_job_type(self, job_type: str) -> StoryWorkflowToolDefinition:
            return self._by_job_type[job_type]

        def list_tools(self) -> tuple[StoryWorkflowToolDefinition, ...]:
            return tuple(self._by_name[name] for name in sorted(self._by_name, key=lambda item: item.value))

        def validate_arguments(
            self,
            tool_name: StoryWorkflowToolName | str,
            arguments: dict[str, Any] | None,
        ):
            definition = self.get(tool_name)
            payload = arguments if isinstance(arguments, dict) else {}
            return definition.request_model.model_validate(payload)

        def build_schema_bundle(self) -> dict[str, Any]:
            return {
                "$schema": "https://json-schema.org/draft/2020-12/schema",
                "bundle_schema_version": 1,
                "tools": [
                    {
                        "tool_name": definition.name.value,
                        "stage": definition.stage.value,
                        "description": definition.description,
                        "execution_mode": definition.execution_mode.value,
                        "job_type": definition.job_type,
                        "related_chat_actions": [
                            action_type.value for action_type in definition.related_chat_actions
                        ],
                        "side_effects": [
                            side_effect.model_dump(mode="json") for side_effect in definition.side_effects
                        ],
                        "input_schema": definition.request_model.model_json_schema(),
                        "output_schema": definition.response_model.model_json_schema(),
                    }
                    for definition in self.list_tools()
                ],
            }

        def build_prompt_catalog(self) -> list[dict[str, Any]]:
            return [
                {
                    "tool_name": definition.name.value,
                    "stage": definition.stage.value,
                    "description": definition.description,
                    "execution_mode": definition.execution_mode.value,
                    "related_chat_actions": [
                        action_type.value for action_type in definition.related_chat_actions
                    ],
                    "side_effects": [effect.summary for effect in definition.side_effects],
                }
                for definition in self.list_tools()
            ]


    def get_story_workflow_tool_schema_bundle() -> dict[str, Any]:
        return get_story_workflow_tool_registry().build_schema_bundle()


    def get_story_workflow_tool_prompt_catalog() -> list[dict[str, Any]]:
        return get_story_workflow_tool_registry().build_prompt_catalog()


    @lru_cache(maxsize=1)
    def get_story_workflow_tool_registry() -> StoryWorkflowToolRegistry:
        return StoryWorkflowToolRegistry(
            [
                StoryWorkflowToolDefinition(
                    name=StoryWorkflowToolName.GENERATE_PITCHES,
                    stage=WorkflowStage.PITCHES,
                    description=(
                        "Start or restart pitch generation from the current story brief and planning "
                        "context."
                    ),
                    execution_mode=StoryWorkflowToolExecutionMode.BACKGROUND,
                    job_type="story.generate_pitches",
                    request_model=GeneratePitchesToolInput,

## Command Finished

- Time: `2026-04-01T07:50:30-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `168`
- Summary: completed, exit 0: /bin/zsh -lc "sed -n '844,924p' app/services/story_tools.py"

### Full Text

    Command: /bin/zsh -lc "sed -n '844,924p' app/services/story_tools.py"
    Status: completed
    Exit code: 0
    Output:
    is_selected=True,
                accepted_at=utc_now(),
            )
            self._session.add(setup)
            self._session.flush()

            changed_fields = sorted(
                field for field, value in request.model_dump(mode="json", exclude_none=True).items() if value is not None
            )
            self._events.record_user_edit(
                session_id,
                target_kind=UserEditTargetKind.STORY_SETUP,
                stage=WorkflowStage.STORY_SETUP,
                target_id=setup.id,
                revision_number=setup.revision_number,
                changed_fields=changed_fields,
                source="story_tool",
                field_values=request.model_dump(mode="json", exclude_none=True),
                summary_text="Updated story setup heuristics from the shared tool registry.",
                actor=actor,
            )
            self._events.record_selection(
                session_id,
                selection_kind=SelectionKind.STORY_SETUP,
                stage=WorkflowStage.STORY_SETUP,
                selection_id=setup.id,
                label=_story_setup_label(setup),
                previous_selection_id=previous_selection_id,
                source="story_tool",
                actor=actor,
            )
            stage_snapshot = self._sessions.update_stage_state(
                session_id,
                stage=WorkflowStage.STORY_SETUP,
                status=WorkflowStageState.COMPLETED,
                detail=_story_setup_label(setup),
                actor=actor,
            )
            return UpdateSetupHeuristicsToolResult(
                tool_name=StoryWorkflowToolName.UPDATE_SETUP_HEURISTICS,
                stage=WorkflowStage.STORY_SETUP,
                summary="Saved a new story-setup heuristic revision.",
                stage_status=_stage_status(stage_snapshot, WorkflowStage.STORY_SETUP),
                story_setup_id=setup.id,
                revision_number=setup.revision_number,
            )

        def _compose_next_segment(
            self,
            *,
            session_id: str,
            request: ComposeNextSegmentToolInput,
            actor: SessionEventActor | None = None,
        ) -> CompositionToolResult:
            snapshot = self._sessions.load_session_snapshot(session_id)
            if snapshot.selected_story_setup is None:
                raise StoryWorkflowToolServiceError(
                    "compose_next_segment requires a selected story setup",
                )
            if snapshot.selected_beat_sheet is None:
                raise StoryWorkflowToolServiceError(
                    "compose_next_segment requires a selected beat sheet",
                )

            self._cancel_active_composition_jobs(
                session_id,
                reason="Cancelled because a new composition pass started.",
            )
            next_segment_index = request.restart_from_segment_index or self._next_segment_index(session_id)
            job = CompositionJob(
                session_id=session_id,
                beat_sheet_id=snapshot.selected_beat_sheet.id,
                story_setup_id=snapshot.selected_story_setup.id,
                job_kind=CompositionJobKind.DRAFT,
                status=JobStatus.IN_PROGRESS,
                progress_percent=0,
                current_segment_index=next_segment_index,
                metadata_json=request.model_dump(mode="json", exclude_none=True),
                started_at=utc_now(),
            )
            self._session.add(job)

## File Change Started

- Time: `2026-04-01T07:50:42-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `169`
- Summary: backend/app/services/story_tools.py

### Full Text

    backend/app/services/story_tools.py

    Additional details:
    {
      "status": "in_progress"
    }

## File Change Recorded

- Time: `2026-04-01T07:50:43-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `170`
- Summary: backend/app/services/story_tools.py

### Full Text

    backend/app/services/story_tools.py

    Additional details:
    {
      "status": "completed"
    }

## File Change Started

- Time: `2026-04-01T07:50:55-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `171`
- Summary: backend/app/services/story_tools.py

### Full Text

    backend/app/services/story_tools.py

    Additional details:
    {
      "status": "in_progress"
    }

## File Change Recorded

- Time: `2026-04-01T07:50:55-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `172`
- Summary: backend/app/services/story_tools.py

### Full Text

    backend/app/services/story_tools.py

    Additional details:
    {
      "status": "completed"
    }

## File Change Started

- Time: `2026-04-01T07:51:01-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `173`
- Summary: backend/app/services/story_tools.py

### Full Text

    backend/app/services/story_tools.py

    Additional details:
    {
      "status": "in_progress"
    }

## File Change Recorded

- Time: `2026-04-01T07:51:01-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `174`
- Summary: backend/app/services/story_tools.py

### Full Text

    backend/app/services/story_tools.py

    Additional details:
    {
      "status": "completed"
    }

## File Change Started

- Time: `2026-04-01T07:51:05-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `175`
- Summary: backend/app/services/story_tools.py

### Full Text

    backend/app/services/story_tools.py

    Additional details:
    {
      "status": "in_progress"
    }

## File Change Recorded

- Time: `2026-04-01T07:51:05-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `176`
- Summary: backend/app/services/story_tools.py

### Full Text

    backend/app/services/story_tools.py

    Additional details:
    {
      "status": "completed"
    }

## File Change Started

- Time: `2026-04-01T07:51:10-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `177`
- Summary: backend/app/services/story_tools.py

### Full Text

    backend/app/services/story_tools.py

    Additional details:
    {
      "status": "in_progress"
    }

## File Change Recorded

- Time: `2026-04-01T07:51:10-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `178`
- Summary: backend/app/services/story_tools.py

### Full Text

    backend/app/services/story_tools.py

    Additional details:
    {
      "status": "completed"
    }

## File Change Started

- Time: `2026-04-01T07:51:16-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `179`
- Summary: backend/app/services/story_tools.py

### Full Text

    backend/app/services/story_tools.py

    Additional details:
    {
      "status": "in_progress"
    }

## File Change Recorded

- Time: `2026-04-01T07:51:16-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `180`
- Summary: backend/app/services/story_tools.py

### Full Text

    backend/app/services/story_tools.py

    Additional details:
    {
      "status": "completed"
    }

## Command Started

- Time: `2026-04-01T07:51:22-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `181`
- Summary: in progress: /bin/zsh -lc "sed -n '1,120p' app/worker/default_handlers.py"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,120p' app/worker/default_handlers.py"
    Status: in progress

## Command Finished

- Time: `2026-04-01T07:51:22-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `182`
- Summary: completed, exit 0: /bin/zsh -lc "sed -n '1,120p' app/worker/default_handlers.py"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,120p' app/worker/default_handlers.py"
    Status: completed
    Exit code: 0
    Output:
    from __future__ import annotations

    import time
    from typing import Any

    from app.services.story_tools import get_story_workflow_tool_registry, StoryWorkflowToolService
    from app.worker.registry import JobHandlerRegistry
    from app.worker.runtime import JobExecutionContext


    def build_default_job_handler_registry() -> JobHandlerRegistry:
        registry = JobHandlerRegistry()
        registry.register("demo.echo", demo_echo_handler)
        tool_registry = get_story_workflow_tool_registry()
        for definition in tool_registry.list_tools():
            registry.register(
                definition.job_type,
                build_story_workflow_tool_handler(definition.job_type),
            )
        return registry


    def demo_echo_handler(
        payload: dict[str, Any] | list[Any] | None,
        context: JobExecutionContext,
    ) -> dict[str, Any]:
        payload_dict = payload if isinstance(payload, dict) else {}
        step_count = max(int(payload_dict.get("steps", 1)), 1)
        step_delay_seconds = max(float(payload_dict.get("step_delay_seconds", 0)), 0.0)

        for _ in range(step_count):
            if step_delay_seconds > 0:
                time.sleep(step_delay_seconds)
            context.heartbeat()

        return {
            "echo": payload_dict.get("message", payload),
            "step_count": step_count,
            "worker_id": context.worker_id,
        }


    def build_story_workflow_tool_handler(job_type: str):
        def handler(
            payload: dict[str, Any] | list[Any] | None,
            context: JobExecutionContext,
        ) -> dict[str, Any]:
            if context.session_id is None:
                raise ValueError(f"job type {job_type!r} requires a session_id")

            payload_dict = payload if isinstance(payload, dict) else {}
            tool_registry = get_story_workflow_tool_registry()
            definition = tool_registry.get_by_job_type(job_type)
            context.heartbeat()
            result = context.with_session(
                lambda session: StoryWorkflowToolService(session, tool_registry).execute(
                    tool_name=definition.name,
                    session_id=context.session_id,
                    arguments=payload_dict,
                )
            )
            return result.model_dump(mode="json")

        return handler

## File Change Started

- Time: `2026-04-01T07:51:30-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `183`
- Summary: backend/app/worker/default_handlers.py

### Full Text

    backend/app/worker/default_handlers.py

    Additional details:
    {
      "status": "in_progress"
    }

## File Change Recorded

- Time: `2026-04-01T07:51:30-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `184`
- Summary: backend/app/worker/default_handlers.py

### Full Text

    backend/app/worker/default_handlers.py

    Additional details:
    {
      "status": "completed"
    }

## Command Started

- Time: `2026-04-01T07:51:36-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `185`
- Summary: in progress: /bin/zsh -lc 'python -m ruff check app/services/story_tools.py app/worker/default_handlers.py'

### Full Text

    Command: /bin/zsh -lc 'python -m ruff check app/services/story_tools.py app/worker/default_handlers.py'
    Status: in progress

## Command Finished

- Time: `2026-04-01T07:51:36-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `186`
- Summary: completed, exit 0: /bin/zsh -lc 'python -m ruff check app/services/story_tools.py app/worker/default_handlers.py'

### Full Text

    Command: /bin/zsh -lc 'python -m ruff check app/services/story_tools.py app/worker/default_handlers.py'
    Status: completed
    Exit code: 0
    Output:
    All checks passed!

## Command Started

- Time: `2026-04-01T07:51:46-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `187`
- Summary: in progress: /bin/zsh -lc 'python -m ruff check app/models/story_tools.py app/services/story_tools.py app/worker/runtime.py app/worker/default_handlers.py app/ai/intent_parser.py app/models/__init__.py app/services/__init__.py'

### Full Text

    Command: /bin/zsh -lc 'python -m ruff check app/models/story_tools.py app/services/story_tools.py app/worker/runtime.py app/worker/default_handlers.py app/ai/intent_parser.py app/models/__init__.py app/services/__init__.py'
    Status: in progress

## Command Finished

- Time: `2026-04-01T07:51:46-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `188`
- Summary: completed, exit 0: /bin/zsh -lc 'python -m ruff check app/models/story_tools.py app/services/story_tools.py app/worker/runtime.py app/worker/default_handlers.py app/ai/intent_parser.py app/models/__init__.py app/services/__init__.py'

### Full Text

    Command: /bin/zsh -lc 'python -m ruff check app/models/story_tools.py app/services/story_tools.py app/worker/runtime.py app/worker/default_handlers.py app/ai/intent_parser.py app/models/__init__.py app/services/__init__.py'
    Status: completed
    Exit code: 0
    Output:
    All checks passed!

## Command Started

- Time: `2026-04-01T07:51:54-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `189`
- Summary: in progress: /bin/zsh -lc "sed -n '1,260p' tests/conftest.py"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,260p' tests/conftest.py"
    Status: in progress

## Command Finished

- Time: `2026-04-01T07:51:54-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `190`
- Summary: completed, exit 0: /bin/zsh -lc "sed -n '1,260p' tests/conftest.py"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,260p' tests/conftest.py"
    Status: completed
    Exit code: 0
    Output:
    import os
    import sys
    from collections.abc import Iterator
    from pathlib import Path

    import pytest
    from fastapi.testclient import TestClient

    BACKEND_ROOT = Path(__file__).resolve().parents[1]
    TEST_ENVIRONMENT_DEFAULTS = {
        "STORYTELLER_SECRETS_FILE": "",
        "STORYTELLER_DATABASE_URL": (
            "postgresql+psycopg://storyteller:storyteller@postgres:5432/storyteller"
        ),
        "STORYTELLER_GEMINI_API_KEY": "test-gemini-key",
        "STORYTELLER_GCS_ENDPOINT": "http://gcs:4443",
        "STORYTELLER_GCS_PROJECT_ID": "storyteller-local",
        "STORYTELLER_GCS_PUBLIC_URL": "http://localhost:8568",
        "STORYTELLER_GCS_SESSIONS_BUCKET_NAME": "storyteller-sessions",
        "STORYTELLER_GCS_AUDIO_BUCKET_NAME": "storyteller-audio",
        "STORYTELLER_GCS_EXPORTS_BUCKET_NAME": "storyteller-exports",
    }

    if str(BACKEND_ROOT) not in sys.path:
        sys.path.insert(0, str(BACKEND_ROOT))

    for name, value in TEST_ENVIRONMENT_DEFAULTS.items():
        os.environ.setdefault(name, value)


    def _integration_enabled(config: pytest.Config) -> bool:
        if config.getoption("--run-integration"):
            return True

        return os.environ.get("STORYTELLER_RUN_INTEGRATION_TESTS", "").strip().lower() in {
            "1",
            "true",
            "yes",
            "on",
        }


    def pytest_addoption(parser: pytest.Parser) -> None:
        parser.addoption(
            "--run-integration",
            action="store_true",
            default=False,
            help="run integration tests that require local Postgres and fake GCS services",
        )


    def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
        if _integration_enabled(config):
            return

        skip_integration = pytest.mark.skip(
            reason=(
                "integration tests are disabled by default; pass --run-integration or set "
                "STORYTELLER_RUN_INTEGRATION_TESTS=1"
            ),
        )

        for item in items:
            if "integration" in item.keywords:
                item.add_marker(skip_integration)


    @pytest.fixture
    def client() -> Iterator[TestClient]:
        from app.main import create_app
        from app.settings import get_settings

        get_settings.cache_clear()

        with TestClient(create_app()) as test_client:
            yield test_client

        get_settings.cache_clear()

## Command Started

- Time: `2026-04-01T07:52:02-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `191`
- Summary: in progress: /bin/zsh -lc "sed -n '1,260p' tests/test_session_service.py"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,260p' tests/test_session_service.py"
    Status: in progress

## Command Started

- Time: `2026-04-01T07:52:02-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `192`
- Summary: in progress: /bin/zsh -lc "sed -n '1,220p' tests/test_action_policy_service.py"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,220p' tests/test_action_policy_service.py"
    Status: in progress

## Command Started

- Time: `2026-04-01T07:52:02-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `193`
- Summary: in progress: /bin/zsh -lc "sed -n '322,500p' tests/test_action_policy_service.py"

### Full Text

    Command: /bin/zsh -lc "sed -n '322,500p' tests/test_action_policy_service.py"
    Status: in progress

## Command Finished

- Time: `2026-04-01T07:52:02-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `194`
- Summary: completed, exit 0: /bin/zsh -lc "sed -n '1,220p' tests/test_action_policy_service.py"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,220p' tests/test_action_policy_service.py"
    Status: completed
    Exit code: 0
    Output:
    from __future__ import annotations

    from datetime import datetime, timezone

    import pytest
    from app.db import (
        AssetKind,
        AssetStatus,
        AudioJob,
        Base,
        BeatSheet,
        CharacterSheet,
        CompositionJob,
        CompositionJobKind,
        Genre,
        JobStatus,
        Pitch,
        SessionAsset,
        StoryBrief,
        StorySession,
        StorySetup,
        ToneProfile,
        make_engine,
    )
    from app.models import (
        SessionActionDecision,
        SessionActionPolicyEvaluationRequest,
        SessionActionReasonCode,
        SessionActionSideEffectKind,
        WorkflowStage,
        WorkflowStageState,
    )
    from app.services import SessionActionPolicyService, SessionService
    from sqlalchemy.orm import sessionmaker


    def _enable_sqlite_foreign_keys(engine) -> None:
        with engine.begin() as connection:
            connection.exec_driver_sql("PRAGMA foreign_keys=ON")


    @pytest.fixture
    def db_session():
        engine = make_engine("sqlite+pysqlite:///:memory:")
        _enable_sqlite_foreign_keys(engine)
        Base.metadata.create_all(engine)
        session = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)()

        try:
            yield session
        finally:
            session.close()
            engine.dispose()


    def test_policy_rejects_tone_selection_without_genre_and_suggests_prerequisite(
        db_session,
    ) -> None:
        catalog = _seed_catalog(db_session)
        session_id = SessionService(db_session).create_session(working_title="Policy").id

        request = SessionActionPolicyEvaluationRequest.model_validate(
            {
                "actions": [
                    {
                        "action": {
                            "schema_version": 1,
                            "action_type": "select_tone",
                            "target_stage": "tone",
                            "confidence": 0.94,
                            "rationale": "The user explicitly named a tone.",
                            "requires_confirmation": True,
                            "extracted_values": {
                                "tone_profile_slug": catalog["hushed_wonder"].slug,
                            },
                        }
                    }
                ]
            }
        )

        result = SessionActionPolicyService(db_session).evaluate_request(
            session_id,
            request=request,
        )

        assert result.evaluated_actions[0].decision == SessionActionDecision.REJECTED
        assert result.evaluated_actions[0].prerequisite_action_types == ["select_genre"]
        assert (
            result.evaluated_actions[0].reasons[0].code
            == SessionActionReasonCode.PREREQUISITE_SELECTION_MISSING
        )


    def test_policy_uses_confirmed_prerequisite_actions_earlier_in_the_batch(db_session) -> None:
        catalog = _seed_catalog(db_session)
        session_id = SessionService(db_session).create_session(working_title="Policy").id

        request = SessionActionPolicyEvaluationRequest.model_validate(
            {
                "actions": [
                    {
                        "confirmation_granted": True,
                        "action": {
                            "schema_version": 1,
                            "action_type": "select_genre",
                            "target_stage": "genre",
                            "confidence": 0.98,
                            "rationale": "The user asked for quest fantasy.",
                            "requires_confirmation": True,
                            "extracted_values": {
                                "genre_slug": catalog["quest_fantasy"].slug,
                            },
                        },
                    },
                    {
                        "action": {
                            "schema_version": 1,
                            "action_type": "select_tone",
                            "target_stage": "tone",
                            "confidence": 0.91,
                            "rationale": "The user asked for a hushed tone.",
                            "requires_confirmation": True,
                            "extracted_values": {
                                "tone_profile_slug": catalog["hushed_wonder"].slug,
                            },
                        },
                    },
                ]
            }
        )

        result = SessionActionPolicyService(db_session).evaluate_request(
            session_id,
            request=request,
        )

        assert result.evaluated_actions[0].decision == SessionActionDecision.ACCEPTED
        assert result.evaluated_actions[1].decision == SessionActionDecision.REQUIRES_CONFIRMATION
        assert not result.evaluated_actions[1].prerequisite_action_types


    def test_policy_escalates_story_setup_edits_when_an_active_composition_job_would_be_invalidated(
        db_session,
    ) -> None:
        catalog = _seed_catalog(db_session)
        seeded = _create_story_setup_session(
            db_session,
            catalog,
            composition_status=JobStatus.IN_PROGRESS,
        )
        request = SessionActionPolicyEvaluationRequest.model_validate(
            {
                "actions": [
                    {
                        "action": {
                            "schema_version": 1,
                            "action_type": "update_story_setup",
                            "target_stage": "story_setup",
                            "confidence": 0.84,
                            "rationale": "The user asked for a shorter read-aloud target.",
                            "requires_confirmation": False,
                            "extracted_values": {
                                "target_runtime_minutes": 8,
                            },
                        }
                    }
                ]
            }
        )

        preview = SessionActionPolicyService(db_session).evaluate_request(
            seeded["session_id"],
            request=request,
        )
        confirmed = SessionActionPolicyEvaluationRequest.model_validate(
            {
                "actions": [
                    {
                        **request.model_dump(mode="json")["actions"][0],
                        "confirmation_granted": True,
                    }
                ]
            }
        )
        applied = SessionActionPolicyService(db_session).evaluate_request(
            seeded["session_id"],
            request=confirmed,
        )

        preview_item = preview.evaluated_actions[0]
        applied_item = applied.evaluated_actions[0]

        assert preview_item.decision == SessionActionDecision.REQUIRES_CONFIRMATION
        assert (
            preview_item.reasons[0].code
            == SessionActionReasonCode.CONFIRMATION_REQUIRED_DUE_TO_SIDE_EFFECTS
        )
        assert any(
            effect.kind == SessionActionSideEffectKind.INVALIDATE_STAGES
            and effect.stages == [WorkflowStage.COMPOSITION]
            for effect in preview_item.side_effects
        )
        assert any(
            effect.kind == SessionActionSideEffectKind.STOP_ACTIVE_JOB
            and effect.job_kind == "composition"
            for effect in preview_item.side_effects
        )

        assert applied_item.decision == SessionActionDecision.ACCEPTED_WITH_SIDE_EFFECTS


    def test_policy_rejects_audio_generation_when_story_text_is_not_ready(db_session) -> None:
        catalog = _seed_catalog(db_session)
        seeded = _create_story_setup_session(
            db_session,
            catalog,
            mark_composition_completed=True,
        )
        request = SessionActionPolicyEvaluationRequest.model_validate(

## Command Finished

- Time: `2026-04-01T07:52:02-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `195`
- Summary: completed, exit 0: /bin/zsh -lc "sed -n '1,260p' tests/test_session_service.py"

### Full Text

    Command: /bin/zsh -lc "sed -n '1,260p' tests/test_session_service.py"
    Status: completed
    Exit code: 0
    Output:
    from __future__ import annotations

    from datetime import datetime, timedelta, timezone

    import pytest
    from app.db import (
        AssetKind,
        AssetStatus,
        AudioJob,
        Base,
        BeatSheet,
        CharacterSheet,
        CompositionJob,
        CompositionJobKind,
        EventActorType,
        EventLogEntry,
        Genre,
        JobStatus,
        Pitch,
        SessionAsset,
        StoryBrief,
        StorySession,
        StorySetup,
        ToneProfile,
        make_engine,
    )
    from app.models import SessionContextUpdateRequest, WorkflowStage, WorkflowStageState
    from app.services.sessions import (
        InvalidStageTransitionError,
        SessionNotFoundError,
        SessionService,
    )
    from sqlalchemy.orm import sessionmaker


    def _enable_sqlite_foreign_keys(engine) -> None:
        with engine.begin() as connection:
            connection.exec_driver_sql("PRAGMA foreign_keys=ON")


    @pytest.fixture
    def db_session():
        engine = make_engine("sqlite+pysqlite:///:memory:")
        _enable_sqlite_foreign_keys(engine)
        Base.metadata.create_all(engine)
        session = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)()

        try:
            yield session
        finally:
            session.close()
            engine.dispose()


    def test_create_session_initializes_stage_rows_and_ui_snapshot(db_session) -> None:
        service = SessionService(db_session)

        snapshot = service.create_session(working_title="  Starlight Ferry  ")

        assert snapshot.display_title == "Starlight Ferry"
        assert snapshot.working_title == "Starlight Ferry"
        assert snapshot.current_stage == WorkflowStage.GENRE
        assert snapshot.resume_stage == WorkflowStage.GENRE
        assert snapshot.overall_status == WorkflowStageState.DRAFT
        assert snapshot.progress.total_stages == len(WorkflowStage)
        assert snapshot.progress.completed_stages == 0
        assert [stage.stage for stage in snapshot.stage_states] == list(WorkflowStage)
        assert all(stage.status == WorkflowStageState.DRAFT for stage in snapshot.stage_states)

        stored_session = db_session.get(StorySession, snapshot.id)
        assert stored_session is not None
        assert len(stored_session.workflow_stage_states) == len(WorkflowStage)

        event_rows = (
            db_session.query(EventLogEntry)
            .filter(EventLogEntry.session_id == snapshot.id)
            .order_by(EventLogEntry.sequence_number.asc())
            .all()
        )
        assert len(event_rows) == 1
        assert event_rows[0].sequence_number == 1
        assert event_rows[0].actor_type == EventActorType.USER
        assert event_rows[0].event_type == "session.created"
        assert event_rows[0].payload == {
            "schema_version": 1,
            "working_title": "Starlight Ferry",
        }

        history = service.load_session_history(snapshot.id)
        assert history.latest_sequence_number == 1
        assert len(history.events) == 1
        assert history.events[0].summary == "Created session: Starlight Ferry."
        assert history.events[0].payload is not None
        assert history.events[0].payload.working_title == "Starlight Ferry"


    def test_load_session_snapshot_returns_selected_outputs_and_active_jobs(db_session) -> None:
        now = datetime.now(timezone.utc)
        genre = Genre(
            slug="quest-fantasy",
            label="Quest Fantasy",
            description="A gentle adventure.",
        )
        tone = ToneProfile(
            genre=genre,
            slug="hushed-wonder",
            label="Hushed Wonder",
            description="Quiet and luminous.",
            default_planning_hints={"pacing": "unhurried"},
        )
        story_session = StorySession(
            working_title=None,
            current_stage=WorkflowStage.COMPOSITION,
            resume_stage=WorkflowStage.COMPOSITION,
            furthest_completed_stage=WorkflowStage.STORY_SETUP,
            overall_status=WorkflowStageState.IN_PROGRESS,
            selected_genre=genre,
            selected_tone_profile=tone,
        )
        db_session.add(story_session)
        db_session.flush()

        service = SessionService(db_session)
        service.update_stage_state(
            story_session.id,
            stage=WorkflowStage.GENRE,
            status=WorkflowStageState.COMPLETED,
        )
        service.update_stage_state(
            story_session.id,
            stage=WorkflowStage.TONE,
            status=WorkflowStageState.COMPLETED,
        )
        service.update_stage_state(
            story_session.id,
            stage=WorkflowStage.BRIEF,
            status=WorkflowStageState.COMPLETED,
        )
        service.update_stage_state(
            story_session.id,
            stage=WorkflowStage.PITCHES,
            status=WorkflowStageState.COMPLETED,
        )
        service.update_stage_state(
            story_session.id,
            stage=WorkflowStage.CHARACTERS,
            status=WorkflowStageState.COMPLETED,
        )
        service.update_stage_state(
            story_session.id,
            stage=WorkflowStage.BEATS,
            status=WorkflowStageState.COMPLETED,
        )
        service.update_stage_state(
            story_session.id,
            stage=WorkflowStage.STORY_SETUP,
            status=WorkflowStageState.COMPLETED,
        )
        service.update_stage_state(
            story_session.id,
            stage=WorkflowStage.COMPOSITION,
            status=WorkflowStageState.IN_PROGRESS,
            detail="Writing the middle chapters.",
        )

        brief = StoryBrief(
            session_id=story_session.id,
            revision_number=1,
            raw_brief="A young fox rows across a moonlit lake.",
            normalized_summary="A sleepy quest to find a glowing reed before dawn.",
            planning_notes="Keep the tension soft and quickly reparative.",
            is_active=True,
            accepted_at=now,
        )
        db_session.add(brief)
        db_session.flush()

        pitch = Pitch(
            session_id=story_session.id,
            story_brief_id=brief.id,
            generation_key="pitch-batch-1",
            pitch_index=0,
            title="The Reed of Quiet Light",
            logline="A young fox follows the lake's hush toward a night mystery.",
            summary="Pip drifts toward a lantern-bright reed and learns the lake is helping.",
            bedtime_notes="Every surprise resolves gently.",
            is_selected=True,
            accepted_at=now,
        )
        db_session.add(pitch)
        db_session.flush()

        character_sheet = CharacterSheet(
            session_id=story_session.id,
            pitch_id=pitch.id,
            revision_number=1,
            title="Pip and the Listening Lake",
            protagonist_name="Pip",
            summary="Pip is cautious, curious, and calmed by steady rhythms.",
            supporting_cast={"friend": "a sleepy reed-heron"},
            bedtime_notes="Keep Pip emotionally safe in every scene.",
            is_selected=True,
            accepted_at=now,
        )
        db_session.add(character_sheet)
        db_session.flush()

        beat_sheet = BeatSheet(
            session_id=story_session.id,
            character_sheet_id=character_sheet.id,
            revision_number=1,
            summary="A gentle Save-the-Cat arc with a quiet return home.",
            beats={"opening_image": "Moonlight on still water"},
            bedtime_notes="The midpoint should feel magical, not scary.",
            is_selected=True,
            accepted_at=now,
        )
        db_session.add(beat_sheet)
        db_session.flush()

        story_setup = StorySetup(
            session_id=story_session.id,
            beat_sheet_id=beat_sheet.id,
            revision_number=1,
            target_word_count=1800,
            target_runtime_minutes=12,
            chapter_count=3,
            chapter_style="three gentle chapters",
            guidance_notes="Let each chapter end on a calmer image than it began.",
            preferences={"narration_style": "soft"},
            is_selected=True,
            accepted_at=now,
        )
        db_session.add(story_setup)
        db_session.flush()

        composition_job = CompositionJob(
            session_id=story_session.id,
            beat_sheet_id=beat_sheet.id,
            story_setup_id=story_setup.id,
            job_kind=CompositionJobKind.DRAFT,
            status=JobStatus.IN_PROGRESS,
            progress_percent=48.0,
            current_segment_index=2,
        )
        db_session.add(composition_job)
        db_session.flush()

        audio_job = AudioJob(
            session_id=story_session.id,
            source_composition_job_id=composition_job.id,
            status=JobStatus.PAUSED,
            voice_key="gemini-soft-1",
            playback_speed=0.95,
            include_background_music=True,
            music_profile="gentle-piano",
            estimated_duration_seconds=620,
        )
        db_session.add(audio_job)

## Command Finished

- Time: `2026-04-01T07:52:02-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `196`
- Summary: completed, exit 0: /bin/zsh -lc "sed -n '322,500p' tests/test_action_policy_service.py"

### Full Text

    Command: /bin/zsh -lc "sed -n '322,500p' tests/test_action_policy_service.py"
    Status: completed
    Exit code: 0
    Output:
    def _create_story_setup_session(
        db_session,
        catalog,
        *,
        composition_status: JobStatus | None = None,
        audio_status: JobStatus | None = None,
        mark_composition_completed: bool = False,
        story_asset_kinds: list[AssetKind] | None = None,
    ):
        story_asset_kinds = story_asset_kinds or []
        now = datetime.now(timezone.utc)
        service = SessionService(db_session)
        snapshot = service.create_session(working_title="Bedtime Harbor")
        story_session = db_session.get(StorySession, snapshot.id)
        assert story_session is not None
        story_session.selected_genre = catalog["quest_fantasy"]
        story_session.selected_tone_profile = catalog["hushed_wonder"]
        db_session.flush()

        for stage in (
            WorkflowStage.GENRE,
            WorkflowStage.TONE,
            WorkflowStage.BRIEF,
            WorkflowStage.PITCHES,
            WorkflowStage.CHARACTERS,
            WorkflowStage.BEATS,
            WorkflowStage.STORY_SETUP,
        ):
            service.update_stage_state(
                snapshot.id,
                stage=stage,
                status=WorkflowStageState.COMPLETED,
            )

        brief = StoryBrief(
            session_id=snapshot.id,
            revision_number=1,
            raw_brief="A sleepy harbor mystery with a calm ending.",
            normalized_summary="A harbor fox follows a silver clue and comes home safe.",
            planning_notes="Keep the midpoint gentle.",
            is_active=True,
            accepted_at=now,
        )
        db_session.add(brief)
        db_session.flush()

        pitch = Pitch(
            session_id=snapshot.id,
            story_brief_id=brief.id,
            generation_key="batch-1",
            pitch_index=1,
            title="The Silver Bell Buoy",
            logline="A harbor fox follows a bell across moonlit water.",
            is_selected=True,
            accepted_at=now,
        )
        db_session.add(pitch)
        db_session.flush()

        character_sheet = CharacterSheet(
            session_id=snapshot.id,
            pitch_id=pitch.id,
            revision_number=1,
            title="Mira and the Bell",
            protagonist_name="Mira",
            is_selected=True,
            accepted_at=now,
        )
        db_session.add(character_sheet)
        db_session.flush()

        beat_sheet = BeatSheet(
            session_id=snapshot.id,
            character_sheet_id=character_sheet.id,
            revision_number=1,
            summary="A soft Save-the-Cat arc.",
            is_selected=True,
            accepted_at=now,
        )
        db_session.add(beat_sheet)
        db_session.flush()

        story_setup = StorySetup(
            session_id=snapshot.id,
            beat_sheet_id=beat_sheet.id,
            revision_number=1,
            target_runtime_minutes=11,
            chapter_count=3,
            guidance_notes="Keep the harbor warm and safe.",
            is_selected=True,
            accepted_at=now,
        )
        db_session.add(story_setup)
        db_session.flush()

        composition_job = None
        if composition_status is not None:
            service.update_stage_state(
                snapshot.id,
                stage=WorkflowStage.COMPOSITION,
                status=WorkflowStageState.IN_PROGRESS,
            )
            composition_job = CompositionJob(
                session_id=snapshot.id,
                beat_sheet_id=beat_sheet.id,
                story_setup_id=story_setup.id,
                job_kind=CompositionJobKind.DRAFT,
                status=composition_status,
                progress_percent=42.0,
                current_segment_index=2,
            )
            db_session.add(composition_job)
            db_session.flush()
        elif mark_composition_completed:
            service.update_stage_state(
                snapshot.id,
                stage=WorkflowStage.COMPOSITION,
                status=WorkflowStageState.COMPLETED,
            )

        audio_job = None
        if audio_status is not None:
            service.update_stage_state(
                snapshot.id,
                stage=WorkflowStage.AUDIO,
                status=WorkflowStageState.IN_PROGRESS,
            )
            audio_job = AudioJob(
                session_id=snapshot.id,
                source_composition_job_id=composition_job.id if composition_job else None,
                status=audio_status,
                voice_key="gemini-soft-1",
                playback_speed=1.0,
                include_background_music=False,
            )
            db_session.add(audio_job)
            db_session.flush()

        for asset_kind in story_asset_kinds:
            db_session.add(
                SessionAsset(
                    session_id=snapshot.id,
                    composition_job_id=composition_job.id if composition_job else None,
                    asset_kind=asset_kind,
                    status=AssetStatus.READY,
                    storage_bucket="storyteller",
                    object_path=f"sessions/{snapshot.id}/{asset_kind.value}",
                    mime_type="text/plain",
                    ready_at=now,
                )
            )

        db_session.commit()
        return {
            "session_id": snapshot.id,
            "composition_job_id": composition_job.id if composition_job else None,
            "audio_job_id": audio_job.id if audio_job else None,
        }

## Agent Message

- Time: `2026-04-01T07:52:41-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `197`
- Summary: I’m adding the verification suite now. It covers discoverability, chat-action routing, worker dispatch through the shared registry, and prompt exposure of the tool catalog so the LLM-facing layer stays aligned with the execution layer.

### Full Text

    I’m adding the verification suite now. It covers discoverability, chat-action routing, worker dispatch through the shared registry, and prompt exposure of the tool catalog so the LLM-facing layer stays aligned with the execution layer.

## File Change Started

- Time: `2026-04-01T07:53:52-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `198`
- Summary: backend/tests/test_story_tools.py

### Full Text

    backend/tests/test_story_tools.py

    Additional details:
    {
      "status": "in_progress"
    }

## File Change Recorded

- Time: `2026-04-01T07:53:52-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `199`
- Summary: backend/tests/test_story_tools.py

### Full Text

    backend/tests/test_story_tools.py

    Additional details:
    {
      "status": "completed"
    }

## Agent Message

- Time: `2026-04-01T07:54:15-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `200`
- Summary: The new tests are in. I’m linting them before running pytest so I can fix syntax or style problems once instead of chasing them through failed test runs.

### Full Text

    The new tests are in. I’m linting them before running pytest so I can fix syntax or style problems once instead of chasing them through failed test runs.

## Command Started

- Time: `2026-04-01T07:54:16-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `201`
- Summary: in progress: /bin/zsh -lc 'python -m ruff check app/models/story_tools.py app/services/story_tools.py app/worker/runtime.py app/worker/default_handlers.py app/ai/intent_parser.py app/models/__init__.py app/services/__init__.py tests/test_story_tools.py'

### Full Text

    Command: /bin/zsh -lc 'python -m ruff check app/models/story_tools.py app/services/story_tools.py app/worker/runtime.py app/worker/default_handlers.py app/ai/intent_parser.py app/models/__init__.py app/services/__init__.py tests/test_story_tools.py'
    Status: in progress

## Command Finished

- Time: `2026-04-01T07:54:16-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `202`
- Summary: failed, exit 1: /bin/zsh -lc 'python -m ruff check app/models/story_tools.py app/services/story_tools.py app/worker/runtime.py app/worker/default_handlers.py app/ai/intent_parser.py app/models/__init__.py app/services/__init__.py tests/test_story_tools.py'

### Full Text

    Command: /bin/zsh -lc 'python -m ruff check app/models/story_tools.py app/services/story_tools.py app/worker/runtime.py app/worker/default_handlers.py app/ai/intent_parser.py app/models/__init__.py app/services/__init__.py tests/test_story_tools.py'
    Status: failed
    Exit code: 1
    Output:
    I001 [*] Import block is un-sorted or un-formatted
      --> tests/test_story_tools.py:1:1
       |
     1 | / from __future__ import annotations
     2 | |
     3 | | from datetime import datetime, timezone, timedelta
     4 | | from pathlib import Path
     5 | |
     6 | | import pytest
     7 | | from app.ai import render_intent_parser_prompt
     8 | | from app.db import (
     9 | |     AudioJob,
    10 | |     Base,
    11 | |     BeatSheet,
    12 | |     CharacterSheet,
    13 | |     CompositionJob,
    14 | |     CompositionJobKind,
    15 | |     CompositionSegment,
    16 | |     Genre,
    17 | |     JobStatus,
    18 | |     Pitch,
    19 | |     StoryBrief,
    20 | |     StorySession,
    21 | |     StorySetup,
    22 | |     ToneProfile,
    23 | |     make_engine,
    24 | | )
    25 | | from app.models import (
    26 | |     ChatToUIActionBatch,
    27 | |     IntentParserPromptContext,
    28 | |     IntentParserStageContext,
    29 | |     StoryWorkflowToolExecutionMode,
    30 | |     StoryWorkflowToolName,
    31 | |     WorkflowStage,
    32 | |     WorkflowStageState,
    33 | | )
    34 | | from app.services import (
    35 | |     BackgroundJobService,
    36 | |     SessionService,
    37 | |     StoryWorkflowActionRouter,
    38 | |     StoryWorkflowToolService,
    39 | |     get_story_workflow_tool_registry,
    40 | |     get_story_workflow_tool_schema_bundle,
    41 | | )
    42 | | from app.worker import JobWorker, build_default_job_handler_registry
    43 | | from sqlalchemy.orm import Session, sessionmaker
       | |________________________________________________^
       |
    help: Organize imports

    E501 Line too long (102 > 100)
       --> tests/test_story_tools.py:182:101
        |
    180 |     assert audio_job is not None and audio_job.status == JobStatus.CANCELLED
    181 |     assert _stage_status(snapshot, WorkflowStage.STORY_SETUP) == WorkflowStageState.COMPLETED
    182 |     assert _stage_status(snapshot, WorkflowStage.COMPOSITION) == WorkflowStageState.NEEDS_REGENERATION
        |                                                                                                     ^^
    183 |     assert _stage_status(snapshot, WorkflowStage.AUDIO) == WorkflowStageState.NEEDS_REGENERATION
        |

    E501 Line too long (104 > 100)
       --> tests/test_story_tools.py:250:101
        |
    248 |                 current_stage=WorkflowStage.BEATS,
    249 |                 current_stage_label="Beat sheet",
    250 |                 current_stage_description="Store the accepted Save-the-Cat beat sheet for the session.",
        |                                                                                                     ^^^^
    251 |                 current_stage_status=WorkflowStageState.IN_PROGRESS,
    252 |                 current_stage_detail="Refining the midpoint tension.",
        |

    E501 Line too long (103 > 100)
       --> tests/test_story_tools.py:434:101
        |
    432 |             progress_percent=100,
    433 |             current_segment_index=(
    434 |                 len(composition_segment_word_counts or []) if composition_segment_word_counts else None
        |                                                                                                     ^^^
    435 |             ),
    436 |             started_at=now,
        |

    Found 4 errors.
    [*] 1 fixable with the `--fix` option.

## File Change Started

- Time: `2026-04-01T07:54:30-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `203`
- Summary: backend/tests/test_story_tools.py

### Full Text

    backend/tests/test_story_tools.py

    Additional details:
    {
      "status": "in_progress"
    }

## File Change Recorded

- Time: `2026-04-01T07:54:30-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `204`
- Summary: backend/tests/test_story_tools.py

### Full Text

    backend/tests/test_story_tools.py

    Additional details:
    {
      "status": "completed"
    }

## Command Started

- Time: `2026-04-01T07:54:38-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `205`
- Summary: in progress: /bin/zsh -lc 'python -m ruff check tests/test_story_tools.py --fix'

### Full Text

    Command: /bin/zsh -lc 'python -m ruff check tests/test_story_tools.py --fix'
    Status: in progress

## Command Finished

- Time: `2026-04-01T07:54:38-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `206`
- Summary: completed, exit 0: /bin/zsh -lc 'python -m ruff check tests/test_story_tools.py --fix'

### Full Text

    Command: /bin/zsh -lc 'python -m ruff check tests/test_story_tools.py --fix'
    Status: completed
    Exit code: 0
    Output:
    Found 1 error (1 fixed, 0 remaining).

## Command Started

- Time: `2026-04-01T07:54:43-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `207`
- Summary: in progress: /bin/zsh -lc 'python -m ruff check app/models/story_tools.py app/services/story_tools.py app/worker/runtime.py app/worker/default_handlers.py app/ai/intent_parser.py app/models/__init__.py app/services/__init__.py tests/test_story_tools.py'

### Full Text

    Command: /bin/zsh -lc 'python -m ruff check app/models/story_tools.py app/services/story_tools.py app/worker/runtime.py app/worker/default_handlers.py app/ai/intent_parser.py app/models/__init__.py app/services/__init__.py tests/test_story_tools.py'
    Status: in progress

## Command Finished

- Time: `2026-04-01T07:54:43-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `208`
- Summary: completed, exit 0: /bin/zsh -lc 'python -m ruff check app/models/story_tools.py app/services/story_tools.py app/worker/runtime.py app/worker/default_handlers.py app/ai/intent_parser.py app/models/__init__.py app/services/__init__.py tests/test_story_tools.py'

### Full Text

    Command: /bin/zsh -lc 'python -m ruff check app/models/story_tools.py app/services/story_tools.py app/worker/runtime.py app/worker/default_handlers.py app/ai/intent_parser.py app/models/__init__.py app/services/__init__.py tests/test_story_tools.py'
    Status: completed
    Exit code: 0
    Output:
    All checks passed!

## Agent Message

- Time: `2026-04-01T07:54:49-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `209`
- Summary: I’m moving from lint to behavior checks. The first pytest pass is targeted at the new story-tool tests plus the worker and intent-parser tests that the registry wiring touches.

### Full Text

    I’m moving from lint to behavior checks. The first pytest pass is targeted at the new story-tool tests plus the worker and intent-parser tests that the registry wiring touches.

## Command Started

- Time: `2026-04-01T07:54:50-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `210`
- Summary: in progress: /bin/zsh -lc 'python -m pytest tests/test_story_tools.py tests/test_worker_runtime.py tests/test_intent_parser_adapter.py tests/test_intent_parser_service.py -q'

### Full Text

    Command: /bin/zsh -lc 'python -m pytest tests/test_story_tools.py tests/test_worker_runtime.py tests/test_intent_parser_adapter.py tests/test_intent_parser_service.py -q'
    Status: in progress

## Command Finished

- Time: `2026-04-01T07:54:51-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `211`
- Summary: failed, exit 2: /bin/zsh -lc 'python -m pytest tests/test_story_tools.py tests/test_worker_runtime.py tests/test_intent_parser_adapter.py tests/test_intent_parser_service.py -q'

### Full Text

    Command: /bin/zsh -lc 'python -m pytest tests/test_story_tools.py tests/test_worker_runtime.py tests/test_intent_parser_adapter.py tests/test_intent_parser_service.py -q'
    Status: failed
    Exit code: 2
    Output:
    ==================================== ERRORS ====================================
    __________________ ERROR collecting tests/test_story_tools.py __________________
    ImportError while importing test module '/Users/kevin/code/storyteller/backend/tests/test_story_tools.py'.
    Hint: make sure your test modules/packages have valid Python names.
    Traceback:
    /opt/homebrew/Caskroom/miniconda/base/envs/storyteller/lib/python3.13/importlib/__init__.py:88: in import_module
        return _bootstrap._gcd_import(name[level:], package, level)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    tests/test_story_tools.py:7: in <module>
        from app.ai import render_intent_parser_prompt
    app/ai/__init__.py:1: in <module>
        from app.ai.intent_parser import (
    app/ai/intent_parser.py:19: in <module>
        from app.services.story_tools import get_story_workflow_tool_prompt_catalog
    app/services/__init__.py:16: in <module>
        from app.services.intent_parser import SessionIntentParserService
    app/services/intent_parser.py:6: in <module>
        from app.ai import (
    E   ImportError: cannot import name 'IntentParserAdapter' from partially initialized module 'app.ai' (most likely due to a circular import) (/Users/kevin/code/storyteller/backend/app/ai/__init__.py)
    =========================== short test summary info ============================
    ERROR tests/test_story_tools.py
    !!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
    1 error in 0.22s

## Agent Message

- Time: `2026-04-01T07:55:02-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `212`
- Summary: The first pytest run found an import cycle between `app.ai` and `app.services`. I’m breaking that by deferring the tool-catalog import to prompt-render time instead of module import time.

### Full Text

    The first pytest run found an import cycle between `app.ai` and `app.services`. I’m breaking that by deferring the tool-catalog import to prompt-render time instead of module import time.

## File Change Started

- Time: `2026-04-01T07:55:04-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `213`
- Summary: backend/app/ai/intent_parser.py

### Full Text

    backend/app/ai/intent_parser.py

    Additional details:
    {
      "status": "in_progress"
    }

## File Change Recorded

- Time: `2026-04-01T07:55:04-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `214`
- Summary: backend/app/ai/intent_parser.py

### Full Text

    backend/app/ai/intent_parser.py

    Additional details:
    {
      "status": "completed"
    }

## Command Started

- Time: `2026-04-01T07:55:18-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `215`
- Summary: in progress: /bin/zsh -lc 'python -m ruff check app/ai/intent_parser.py'

### Full Text

    Command: /bin/zsh -lc 'python -m ruff check app/ai/intent_parser.py'
    Status: in progress

## Command Finished

- Time: `2026-04-01T07:55:18-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `216`
- Summary: completed, exit 0: /bin/zsh -lc 'python -m ruff check app/ai/intent_parser.py'

### Full Text

    Command: /bin/zsh -lc 'python -m ruff check app/ai/intent_parser.py'
    Status: completed
    Exit code: 0
    Output:
    All checks passed!

## Command Started

- Time: `2026-04-01T07:55:25-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `217`
- Summary: in progress: /bin/zsh -lc 'python -m pytest tests/test_story_tools.py tests/test_worker_runtime.py tests/test_intent_parser_adapter.py tests/test_intent_parser_service.py -q'

### Full Text

    Command: /bin/zsh -lc 'python -m pytest tests/test_story_tools.py tests/test_worker_runtime.py tests/test_intent_parser_adapter.py tests/test_intent_parser_service.py -q'
    Status: in progress

## Command Finished

- Time: `2026-04-01T07:55:26-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `218`
- Summary: failed, exit 1: /bin/zsh -lc 'python -m pytest tests/test_story_tools.py tests/test_worker_runtime.py tests/test_intent_parser_adapter.py tests/test_intent_parser_service.py -q'

### Full Text

    Command: /bin/zsh -lc 'python -m pytest tests/test_story_tools.py tests/test_worker_runtime.py tests/test_intent_parser_adapter.py tests/test_intent_parser_service.py -q'
    Status: failed
    Exit code: 1
    Output:
    ..F..............                                                        [100%]
    =================================== FAILURES ===================================
    _ test_story_workflow_tool_service_updates_setup_and_cancels_invalidated_jobs __

    db_session = <sqlalchemy.orm.session.Session object at 0x111470980>

        def test_story_workflow_tool_service_updates_setup_and_cancels_invalidated_jobs(
            db_session,
        ) -> None:
    >       seeded = _seed_story_setup_session(
                db_session,
                composition_status=JobStatus.IN_PROGRESS,
                audio_status=JobStatus.IN_PROGRESS,
            )

    tests/test_story_tools.py:154: 
    _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
    tests/test_story_tools.py:467: in _seed_story_setup_session
        service.update_stage_state(
    app/services/sessions.py:268: in update_stage_state
        self._validate_stage_transition(stage_map, stage=stage, status=status)
    _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

    self = <app.services.sessions.SessionService object at 0x111470830>
    stage_map = {<WorkflowStage.AUDIO: 'audio'>: <app.db.models.WorkflowStageSnapshot object at 0x11144bb50>, <WorkflowStage.BEATS: 'b...1118456d0>, <WorkflowStage.CHARACTERS: 'characters'>: <app.db.models.WorkflowStageSnapshot object at 0x111592fd0>, ...}

        def _validate_stage_transition(
            self,
            stage_map: Mapping[WorkflowStage, object],
            *,
            stage: WorkflowStage,
            status: WorkflowStageState,
        ) -> None:
            if status in {WorkflowStageState.IN_PROGRESS, WorkflowStageState.COMPLETED}:
                incomplete_prerequisites = [
                    prior_stage.value
                    for prior_stage in _stages_before(stage)
                    if getattr(stage_map[prior_stage], "status") != WorkflowStageState.COMPLETED
                ]
                if incomplete_prerequisites:
                    joined = ", ".join(incomplete_prerequisites)
    >               raise InvalidStageTransitionError(
                        f"cannot set {stage.value!r} to {status.value!r} before prerequisites are "
                        f"completed: {joined}"
                    )
    E               app.services.sessions.InvalidStageTransitionError: cannot set 'audio' to 'in_progress' before prerequisites are completed: composition

    app/services/sessions.py:336: InvalidStageTransitionError
    =========================== short test summary info ============================
    FAILED tests/test_story_tools.py::test_story_workflow_tool_service_updates_setup_and_cancels_invalidated_jobs
    1 failed, 16 passed in 0.76s

## File Change Started

- Time: `2026-04-01T07:55:41-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `219`
- Summary: backend/tests/test_story_tools.py

### Full Text

    backend/tests/test_story_tools.py

    Additional details:
    {
      "status": "in_progress"
    }

## File Change Recorded

- Time: `2026-04-01T07:55:41-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `220`
- Summary: backend/tests/test_story_tools.py

### Full Text

    backend/tests/test_story_tools.py

    Additional details:
    {
      "status": "completed"
    }

## Command Started

- Time: `2026-04-01T07:55:55-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `221`
- Summary: in progress: /bin/zsh -lc 'python -m pytest tests/test_story_tools.py tests/test_worker_runtime.py tests/test_intent_parser_adapter.py tests/test_intent_parser_service.py -q'

### Full Text

    Command: /bin/zsh -lc 'python -m pytest tests/test_story_tools.py tests/test_worker_runtime.py tests/test_intent_parser_adapter.py tests/test_intent_parser_service.py -q'
    Status: in progress

## Command Finished

- Time: `2026-04-01T07:55:56-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `222`
- Summary: completed, exit 0: /bin/zsh -lc 'python -m pytest tests/test_story_tools.py tests/test_worker_runtime.py tests/test_intent_parser_adapter.py tests/test_intent_parser_service.py -q'

### Full Text

    Command: /bin/zsh -lc 'python -m pytest tests/test_story_tools.py tests/test_worker_runtime.py tests/test_intent_parser_adapter.py tests/test_intent_parser_service.py -q'
    Status: completed
    Exit code: 0
    Output:
    .................                                                        [100%]
    17 passed in 0.79s

## Agent Message

- Time: `2026-04-01T07:56:12-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `223`
- Summary: The focused tests passed, so I’m widening the verification to the broader backend unit suite. That should catch any import-surface regressions from exporting the new registry through `app.models` and `app.services`.

### Full Text

    The focused tests passed, so I’m widening the verification to the broader backend unit suite. That should catch any import-surface regressions from exporting the new registry through `app.models` and `app.services`.

## Command Started

- Time: `2026-04-01T07:56:13-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `224`
- Summary: in progress: /bin/zsh -lc 'python -m pytest -q'

### Full Text

    Command: /bin/zsh -lc 'python -m pytest -q'
    Status: in progress

## Command Finished

- Time: `2026-04-01T07:56:17-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `225`
- Summary: completed, exit 0: /bin/zsh -lc 'python -m pytest -q'

### Full Text

    Command: /bin/zsh -lc 'python -m pytest -q'
    Status: completed
    Exit code: 0
    Output:
    sssss................................................................... [ 70%]
    ..............................                                           [100%]
    97 passed, 5 skipped in 2.79s

## Agent Message

- Time: `2026-04-01T07:56:25-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `226`
- Summary: The code path is stable, so I’m writing the reviewer-facing docs now: what the registry is, how the tool contracts are structured, how chat actions map into it, and how worker dispatch picks it up automatically.

### Full Text

    The code path is stable, so I’m writing the reviewer-facing docs now: what the registry is, how the tool contracts are structured, how chat actions map into it, and how worker dispatch picks it up automatically.

## File Change Started

- Time: `2026-04-01T07:56:55-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `227`
- Summary: docs/story-workflow-tool-registry.md

### Full Text

    docs/story-workflow-tool-registry.md

    Additional details:
    {
      "status": "in_progress"
    }

## File Change Recorded

- Time: `2026-04-01T07:56:55-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `228`
- Summary: docs/story-workflow-tool-registry.md

### Full Text

    docs/story-workflow-tool-registry.md

    Additional details:
    {
      "status": "completed"
    }

## File Change Started

- Time: `2026-04-01T07:57:02-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `229`
- Summary: docs/README.md

### Full Text

    docs/README.md

    Additional details:
    {
      "status": "in_progress"
    }

## File Change Recorded

- Time: `2026-04-01T07:57:02-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `230`
- Summary: docs/README.md

### Full Text

    docs/README.md

    Additional details:
    {
      "status": "completed"
    }

## File Change Started

- Time: `2026-04-01T07:57:13-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `231`
- Summary: backend/README.md

### Full Text

    backend/README.md

    Additional details:
    {
      "status": "in_progress"
    }

## File Change Recorded

- Time: `2026-04-01T07:57:13-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `232`
- Summary: backend/README.md

### Full Text

    backend/README.md

    Additional details:
    {
      "status": "completed"
    }

## Agent Message

- Time: `2026-04-01T07:57:21-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `233`
- Summary: The code and tests are in good shape. I’m running the repo’s backend lint target over all `app` and `tests` files now so the new exports and test helpers are validated in the same scope reviewers will expect.

### Full Text

    The code and tests are in good shape. I’m running the repo’s backend lint target over all `app` and `tests` files now so the new exports and test helpers are validated in the same scope reviewers will expect.

## Command Started

- Time: `2026-04-01T07:57:22-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `234`
- Summary: in progress: /bin/zsh -lc 'python -m ruff check app tests'

### Full Text

    Command: /bin/zsh -lc 'python -m ruff check app tests'
    Status: in progress

## Command Finished

- Time: `2026-04-01T07:57:22-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `235`
- Summary: completed, exit 0: /bin/zsh -lc 'python -m ruff check app tests'

### Full Text

    Command: /bin/zsh -lc 'python -m ruff check app tests'
    Status: completed
    Exit code: 0
    Output:
    All checks passed!

## Command Started

- Time: `2026-04-01T07:57:31-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `236`
- Summary: in progress: /bin/zsh -lc 'git status --short'

### Full Text

    Command: /bin/zsh -lc 'git status --short'
    Status: in progress

## Command Finished

- Time: `2026-04-01T07:57:31-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `237`
- Summary: completed, exit 0: /bin/zsh -lc 'git status --short'

### Full Text

    Command: /bin/zsh -lc 'git status --short'
    Status: completed
    Exit code: 0
    Output:
    M backend/README.md
     M backend/app/ai/intent_parser.py
     M backend/app/ai/prompts/intent_parser.md
     M backend/app/models/__init__.py
     M backend/app/services/__init__.py
     M backend/app/worker/default_handlers.py
     M backend/app/worker/runtime.py
     M docs/README.md
     M prompts/36-conversation-memory-summaries.yolopilot.jsonlines
     M prompts/36-conversation-memory-summaries.yolopilot.md
    ?? backend/app/models/story_tools.py
    ?? backend/app/services/story_tools.py
    ?? backend/tests/test_story_tools.py
    ?? docs/story-workflow-tool-registry.md
    ?? prompts/37-agent-tool-registry.codex.jsonlines
    ?? prompts/37-agent-tool-registry.yolopilot.jsonlines
    ?? prompts/37-agent-tool-registry.yolopilot.md

## Agent Message

- Time: `2026-04-01T07:57:47-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `238`
- Summary: The implementation is verified, so I’m checkpointing the code changes on the current branch before I write the task summary file. I’m only staging the files from this prompt so the unrelated prompt-run artifacts stay untouched.

### Full Text

    The implementation is verified, so I’m checkpointing the code changes on the current branch before I write the task summary file. I’m only staging the files from this prompt so the unrelated prompt-run artifacts stay untouched.

## Command Started

- Time: `2026-04-01T07:57:48-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `239`
- Summary: in progress: /bin/zsh -lc 'git add backend/README.md backend/app/ai/intent_parser.py backend/app/ai/prompts/intent_parser.md backend/app/models/__init__.py backend/app/models/story_tools.py backend/app/services/__init__.py backend/app/services/story_tools.py backend/app/worker/default_handlers.py backend/app/worker/runtime.py backend/tests/test_story_tools.py docs/README.md docs/story-workflow-tool-registry.md && git commit -m "feat(prompt-37): agent tool registry"'

### Full Text

    Command: /bin/zsh -lc 'git add backend/README.md backend/app/ai/intent_parser.py backend/app/ai/prompts/intent_parser.md backend/app/models/__init__.py backend/app/models/story_tools.py backend/app/services/__init__.py backend/app/services/story_tools.py backend/app/worker/default_handlers.py backend/app/worker/runtime.py backend/tests/test_story_tools.py docs/README.md docs/story-workflow-tool-registry.md && git commit -m "feat(prompt-37): agent tool registry"'
    Status: in progress

## Command Finished

- Time: `2026-04-01T07:57:48-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `240`
- Summary: completed, exit 0: /bin/zsh -lc 'git add backend/README.md backend/app/ai/intent_parser.py backend/app/ai/prompts/intent_parser.md backend/app/models/__init__.py backend/app/models/story_tools.py backend/app/services/__init__.py backend/app/services/story_tools.py backend/app/worker/default_handlers.py backend/app/worker/runtime.py backend/tests/test_story_tools.py docs/README.md docs/story-workflow-tool-registry.md && git commit -m "feat(prompt-37): agent tool registry"'

### Full Text

    Command: /bin/zsh -lc 'git add backend/README.md backend/app/ai/intent_parser.py backend/app/ai/prompts/intent_parser.md backend/app/models/__init__.py backend/app/models/story_tools.py backend/app/services/__init__.py backend/app/services/story_tools.py backend/app/worker/default_handlers.py backend/app/worker/runtime.py backend/tests/test_story_tools.py docs/README.md docs/story-workflow-tool-registry.md && git commit -m "feat(prompt-37): agent tool registry"'
    Status: completed
    Exit code: 0
    Output:
    [yolopilot-init-37-agent-tool-registry d2b621f] feat(prompt-37): agent tool registry
     12 files changed, 2393 insertions(+), 4 deletions(-)
     create mode 100644 backend/app/models/story_tools.py
     create mode 100644 backend/app/services/story_tools.py
     create mode 100644 backend/tests/test_story_tools.py
     create mode 100644 docs/story-workflow-tool-registry.md

## Command Started

- Time: `2026-04-01T07:57:52-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `241`
- Summary: in progress: /bin/zsh -lc 'git status --short'

### Full Text

    Command: /bin/zsh -lc 'git status --short'
    Status: in progress

## Command Finished

- Time: `2026-04-01T07:57:52-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `242`
- Summary: completed, exit 0: /bin/zsh -lc 'git status --short'

### Full Text

    Command: /bin/zsh -lc 'git status --short'
    Status: completed
    Exit code: 0
    Output:
    M prompts/36-conversation-memory-summaries.yolopilot.jsonlines
     M prompts/36-conversation-memory-summaries.yolopilot.md
    ?? prompts/37-agent-tool-registry.codex.jsonlines
    ?? prompts/37-agent-tool-registry.yolopilot.jsonlines
    ?? prompts/37-agent-tool-registry.yolopilot.md

## Command Started

- Time: `2026-04-01T07:58:05-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `243`
- Summary: in progress: /bin/zsh -lc 'git show --stat --oneline --no-patch HEAD && git show --stat --format=short HEAD'

### Full Text

    Command: /bin/zsh -lc 'git show --stat --oneline --no-patch HEAD && git show --stat --format=short HEAD'
    Status: in progress

## Command Finished

- Time: `2026-04-01T07:58:05-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `244`
- Summary: completed, exit 0: /bin/zsh -lc 'git show --stat --oneline --no-patch HEAD && git show --stat --format=short HEAD'

### Full Text

    Command: /bin/zsh -lc 'git show --stat --oneline --no-patch HEAD && git show --stat --format=short HEAD'
    Status: completed
    Exit code: 0
    Output:
    d2b621f feat(prompt-37): agent tool registry
    commit d2b621feb0a420c7b465f1e80a1b26143e5a065e
    Author: Kevin J Dolan <norelaxation@gmail.com>

        feat(prompt-37): agent tool registry

     backend/README.md                       |   16 +-
     backend/app/ai/intent_parser.py         |    7 +
     backend/app/ai/prompts/intent_parser.md |    3 +
     backend/app/models/__init__.py          |   50 ++
     backend/app/models/story_tools.py       |  220 +++++
     backend/app/services/__init__.py        |   18 +
     backend/app/services/story_tools.py     | 1397 +++++++++++++++++++++++++++++++
     backend/app/worker/default_handlers.py  |   34 +
     backend/app/worker/runtime.py           |   16 +-
     backend/tests/test_story_tools.py       |  500 +++++++++++
     docs/README.md                          |    1 +
     docs/story-workflow-tool-registry.md    |  135 +++
     12 files changed, 2393 insertions(+), 4 deletions(-)

## Agent Message

- Time: `2026-04-01T07:58:41-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `245`
- Summary: I’ve reached the final step. I’m writing the required reviewer summary file now with the implementation notes, verification results, eval criteria, wrong turns, and assumptions from the unsupervised run.

### Full Text

    I’ve reached the final step. I’m writing the required reviewer summary file now with the implementation notes, verification results, eval criteria, wrong turns, and assumptions from the unsupervised run.

## File Change Started

- Time: `2026-04-01T07:59:44-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `246`
- Summary: prompts/37-agent-tool-registry.summary.md

### Full Text

    prompts/37-agent-tool-registry.summary.md

    Additional details:
    {
      "status": "in_progress"
    }

## File Change Recorded

- Time: `2026-04-01T07:59:44-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `247`
- Summary: prompts/37-agent-tool-registry.summary.md

### Full Text

    prompts/37-agent-tool-registry.summary.md

    Additional details:
    {
      "status": "completed"
    }

## Agent Message

- Time: `2026-04-01T08:00:01-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `248`
- Summary: Implemented the agent tool registry and committed the code changes in `d2b621f` (`feat(prompt-37): agent tool registry`). The backend now has typed story-tool contracts in [story_tools.py](/Users/kevin/code/storyteller/backend/app/models...

### Full Text

    Implemented the agent tool registry and committed the code changes in `d2b621f` (`feat(prompt-37): agent tool registry`).

    The backend now has typed story-tool contracts in [story_tools.py](/Users/kevin/code/storyteller/backend/app/models/story_tools.py), a shared registry/executor/action-router in [story_tools.py](/Users/kevin/code/storyteller/backend/app/services/story_tools.py), worker auto-registration in [default_handlers.py](/Users/kevin/code/storyteller/backend/app/worker/default_handlers.py), and prompt exposure of the shared tool catalog in [intent_parser.py](/Users/kevin/code/storyteller/backend/app/ai/intent_parser.py). I also added reviewer docs in [story-workflow-tool-registry.md](/Users/kevin/code/storyteller/docs/story-workflow-tool-registry.md) and coverage in [test_story_tools.py](/Users/kevin/code/storyteller/backend/tests/test_story_tools.py).

    Verification:
    `python -m pytest -q` -> `97 passed, 5 skipped`
    `python -m ruff check app tests` -> passed

    The required reviewer summary was written as the final action to [37-agent-tool-registry.summary.md](/Users/kevin/code/storyteller/prompts/37-agent-tool-registry.summary.md).

## Unkown Event

- Time: `2026-04-01T08:00:01-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `249`
- Summary: { "item": { "id": "item_46", "items": [ { "completed": true, "text": "Inspect existing backend action, worker, and session services to find the right registry seam" }, { "completed": false, "text": "Implement story operation models, doma...

### Full Text

    {
      "item": {
        "id": "item_46",
        "items": [
          {
            "completed": true,
            "text": "Inspect existing backend action, worker, and session services to find the right registry seam"
          },
          {
            "completed": false,
            "text": "Implement story operation models, domain services, and a central registry with invocation helpers"
          },
          {
            "completed": false,
            "text": "Wire the registry into chat/orchestration and worker handler registration"
          },
          {
            "completed": false,
            "text": "Add tests and docs covering discoverability, invocation, side effects, and extension points"
          },
          {
            "completed": false,
            "text": "Run targeted verification, commit checkpoints, and write the required summary file"
          }
        ],
        "type": "todo_list"
      },
      "type": "item.completed"
    }

## Turn Completed

- Time: `2026-04-01T08:00:01-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `250`
- Summary: in 9967304 | cached 8473216 | out 65990

### Full Text

    Input tokens: 9967304
    Cached input tokens: 8473216
    Output tokens: 65990

## YoloPilot Event

- Time: `2026-04-01T08:00:01-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `251`
- Summary: Checking summary file 37-agent-tool-registry.summary.md.

### Full Text

    Checking summary file 37-agent-tool-registry.summary.md.

## YoloPilot Event

- Time: `2026-04-01T08:00:01-07:00`
- Prompt: `37 — Agent Tool Registry for Story Workflow Operations` (38/100)
- Task event: `252`
- Summary: Creating final signed-off commit for 37-agent-tool-registry.

### Full Text

    Creating final signed-off commit for 37-agent-tool-registry.


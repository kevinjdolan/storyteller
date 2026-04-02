# Chat-to-UI Actions

Prompt 30 establishes the typed contract that chat intent parsing must emit
before any model suggestion is allowed to touch the workspace.

## Contract Shape

The backend source of truth lives in `backend/app/models/chat_actions.py`.
The mirrored frontend parser and type layer live in
`frontend/src/features/session/chat/chatToUiActions.ts`.
The machine-readable schema bundle lives in
`docs/chat-to-ui-actions.schema.json`.

Every proposed action is wrapped in a batch object:

- `schema_version`: contract version for the batch payload.
- `actions`: ordered list of discriminated action objects.

Every action carries the same envelope fields:

- `action_type`: stable discriminator such as `select_genre` or `pause_job`.
- `target_stage`: workflow stage the action is meant to affect.
- `confidence`: normalized `0..1` parser confidence.
- `rationale`: short explanation of why the parser extracted the action.
- `requires_confirmation`: whether the action should wait for a user confirm step.
- `extracted_values`: typed structured fields specific to that action.

## Action Catalog

| Stage         | Action types                                                                     | Notes                                                                                                 |
| ------------- | -------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| Any           | `navigate_to_stage`                                                              | Safe view-navigation request with no durable mutation.                                                |
| `genre`       | `select_genre`                                                                   | Accepts genre identifiers by id, slug, or label.                                                      |
| `tone`        | `select_tone`                                                                    | Accepts tone-profile identifiers by id, slug, or label.                                               |
| `brief`       | `update_story_brief`                                                             | Supports `replace`, `append`, or `merge` edits for raw brief, normalized summary, and planning notes. |
| `pitches`     | `regenerate_pitches`, `refine_pitch`, `select_pitch`                              | Covers “give me more options,” “revise that pitch,” and “pick this pitch” flows.                      |
| `characters`  | `select_character_sheet`, `refine_character_sheet`, `regenerate_character_sheet` | Separates picking a sheet from refinement instructions or a full regenerate request.                  |
| `beats`       | `accept_beat_sheet`, `refine_beat_sheet`, `regenerate_beat_sheet`                | Keeps Save-the-Cat acceptance distinct from edit requests.                                            |
| `story_setup` | `update_story_setup`                                                             | Captures soft targets like word count, runtime, chapters, and guidance notes.                         |
| `composition` | `start_composition`, `pause_job`, `resume_job`, `redirect_composition`           | Job control is explicit and stage-bound. Redirects require concrete instructions.                     |
| `audio`       | `update_audio_settings`, `start_audio_generation`, `pause_job`, `resume_job`     | Audio settings are separate from the command to start generation.                                     |
| `finalize`    | `open_finalize_view`, `download_asset`                                           | Supports read/listen navigation plus export actions.                                                  |

## Default Policy

The default policy is intentionally conservative. The parser can propose an
action, but the later policy engine still has to validate current session state,
prerequisites, and downstream invalidation effects.

Default `auto_apply_candidate` actions:

- `navigate_to_stage`
- `update_story_brief`
- `update_story_setup`
- `update_audio_settings`
- `open_finalize_view`
- `download_asset`

Default `confirm_first` actions:

- All acceptance or refinement actions such as `select_genre`, `select_tone`,
  `select_pitch`, `refine_pitch`, `select_character_sheet`, and
  `accept_beat_sheet`
- All regenerate actions
- All composition and audio job control actions
- `redirect_composition`

Policy expectations:

- Confirm-first is mandatory for actions that can invalidate downstream work,
  launch or stop jobs, or change accepted planning decisions.
- Auto-apply candidates are still only candidates. The backend policy layer may
  escalate them to confirmation when existing downstream artifacts would be
  invalidated.
- The frontend mirror rejects payloads that violate the default confirm-first
  rule so UI suggestions and backend validation start from the same baseline.

## Example

```json
{
  "schema_version": 1,
  "actions": [
    {
      "schema_version": 1,
      "action_type": "update_story_setup",
      "target_stage": "story_setup",
      "confidence": 0.81,
      "rationale": "The user explicitly asked for a shorter read-aloud target.",
      "requires_confirmation": false,
      "extracted_values": {
        "target_runtime_minutes": 10,
        "chapter_count": 3
      }
    },
    {
      "schema_version": 1,
      "action_type": "start_composition",
      "target_stage": "composition",
      "confidence": 0.94,
      "rationale": "The user asked to start writing now.",
      "requires_confirmation": true,
      "extracted_values": {
        "mode": "fresh"
      }
    }
  ]
}
```

Prompt 31 should ask Gemini to emit this batch shape directly. Prompt 32 should
decide whether each proposed action is accepted, rejected, or upgraded to a
confirmation gate in the current session state.

## Policy Evaluation

The deterministic evaluator now lives in `backend/app/services/action_policy.py`
with typed request and response models in `backend/app/models/action_policy.py`.

Two backend entrypoints expose the same engine:

- `POST /api/v1/sessions/{session_id}/actions/evaluate` for direct UI or test-driven policy checks
- `POST /api/v1/sessions/{session_id}/chat/intents`, which now includes
  `policy_evaluation` beside the parsed `proposed_actions`

Each evaluated action returns one of four decisions:

- `accepted`
- `rejected`
- `requires_confirmation`
- `accepted_with_side_effects`

The response also carries:

- stable reason codes for blockers or confirmation upgrades
- prerequisite action hints such as `select_genre` before `select_tone`
- explicit side effects such as downstream stage invalidation, active-job stops,
  or stale asset replacement

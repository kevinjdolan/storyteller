# Prompt 47 Summary: Character Sheet Selection and Refinement via Chat

## What I Changed And Why

This prompt asked for character sheet selection and refinement to work cleanly through both chat and direct UI controls, while keeping durable structured state authoritative and correctly invalidating downstream planning when necessary.

I implemented that in three layers:

- Backend action and persistence support for targeted character refinement. Chat actions can now point at a specific saved character sheet by `character_sheet_id`, `revision_number`, or `title`, and can carry structured refinement metadata such as `focus_character_names`, `change_summary`, and `change_impact`.
- Session and policy logic that distinguishes minor versus major character changes. Minor changes preserve downstream planning when the story arc is intentionally unchanged; major changes mark later stages as needing regeneration.
- Frontend hydration and workspace updates so the selected/refined character sheet stays inspectable in the main pane and the chat log reflects accepted character actions with the same durable rationale used by the backend.

The goal was to prevent the exact failure mode called out in the prompt notes: free-form character edits drifting away from structured session state.

## Architectural Changes Across The Codebase

### Backend

- Added `CharacterChangeImpact` support to the domain models and chat action contracts in:
  - `backend/app/models/chat_actions.py`
  - `backend/app/models/intent_parser.py`
  - `backend/app/models/session.py`
  - `backend/app/models/story_tools.py`
  - `backend/app/models/__init__.py`
- Added `backend/app/services/character_sheet_changes.py` to centralize character change impact inference. This gives future adapters and workflows one place to reuse the same major/minor invalidation heuristics instead of embedding ad hoc rules in multiple services.
- Extended `SessionService.refine_character_sheet(...)` in `backend/app/services/sessions.py` to:
  - persist refinement metadata
  - preserve/refit downstream state for minor refinements
  - invalidate downstream stages for major refinements
  - carry the persisted rationale through selection and hydration
- Added `get_selected_beat_sheet()` to `backend/app/repositories/sessions.py` so the session service can relink the selected beat sheet to a refined character sheet when the change is minor and the accepted beat plan remains valid.
- Updated action policy handling in `backend/app/services/action_policy.py` so minor character refinements do not create unnecessary invalidation side effects, while major refinements still escalate correctly.
- Updated intent parsing and prompt grounding in:
  - `backend/app/ai/prompts/intent_parser.md`
  - `backend/app/ai/intent_parser.py`
  - `backend/app/services/intent_parser.py`
  - `backend/app/services/agent_context.py`

The intent parser now sees the latest saved character options and the selected character refinement state, which gives it enough durable grounding to interpret follow-ups like “soften the revised one” without inventing hidden state.

### API And Hydration

- Extended the session routes and hydration path in:
  - `backend/app/api/v1/routes/sessions.py`
  - `backend/app/services/session_hydration.py`

Hydrated session snapshots now expose:

- `focus_character_names`
- `change_summary`
- `change_impact`

for both the selected character sheet and the containing character sheet batches.

### Frontend

- Extended the API types in `frontend/src/api/sessions.ts` so the workspace can round-trip the new character refinement fields without dropping them.
- Updated `frontend/src/features/session/chat/chatToUiActions.ts` so frontend chat action decoding accepts targeted `refine_character_sheet` actions and preserves selectors plus impact metadata.
- Updated `frontend/src/pages/session/SessionWorkspacePage.tsx` to pass the new structured refinement fields through when chat-approved actions are applied.
- Expanded `frontend/src/features/session/CharacterSelectionStage.tsx` with refinement-oriented controls:
  - `Focus characters`
  - `Change summary`
  - `Planning impact`

This gives the user an explicit way to refine a saved character sheet without falling back to opaque free-text edits.

- Updated chat display behavior in:
  - `frontend/src/features/session/chat/sessionChat.ts`
  - `frontend/src/features/session/chat/actionEchoes.ts`

The chat log now reflects refined/selected character sheets using the same durable rationale stored on the backend, instead of generating unrelated summary text on the client.

### Documentation

- Regenerated `docs/chat-to-ui-actions.schema.json` so the contract docs stay aligned with the new structured action format.

## Examples Of New Abstractions, Helpers, And Extension Points

### 1. Targeted character refinement from a parser or future tool

The action contract now supports selector-based refinement:

```json
{
  "action_type": "refine_character_sheet",
  "target_stage": "characters",
  "confidence": 0.86,
  "requires_confirmation": true,
  "extracted_values": {
    "revision_number": 2,
    "title": "Lantern Keeper Cast",
    "instructions": "Soften Mira's voice and keep the same comfort ritual.",
    "focus_character_names": ["Mira"],
    "change_summary": "Keep the same arc but make the dialogue gentler.",
    "change_impact": "minor"
  }
}
```

That structure is accepted by the backend contract models, the API layer, and the frontend chat-to-UI bridge.

### 2. Service-level refinement call

`SessionService.refine_character_sheet(...)` now supports richer refinement inputs:

```python
service.refine_character_sheet(
    session_id,
    character_sheet_id=sheet_id,
    instructions="Soften the protagonist voice so the reassurance feels warmer.",
    focus_character_names=["Mira"],
    change_summary="Keep the same arc but make the dialogue gentler.",
    change_impact=CharacterChangeImpact.MINOR,
    character_generation_service=generator,
)
```

This is the main extension point for future tools, worker flows, or admin scripts that need to refine a persisted character sheet without bypassing invalidation logic.

### 3. Reusable change-impact helper

`backend/app/services/character_sheet_changes.py` provides a dedicated home for impact inference. Future prompt adapters or moderation layers can reuse it when they need to classify a refinement but only have user instructions or partial structured fields.

## Exact Verification Work Performed

### Backend tests

Targeted backend verification:

- `pytest backend/tests/test_session_service.py backend/tests/test_action_policy_service.py backend/tests/test_intent_parser_service.py backend/tests/test_intent_parser_adapter.py backend/tests/test_chat_action_contracts.py -q`
  - Result: pass
- `pytest backend/tests/test_session_api.py backend/tests/test_story_tools.py backend/tests/test_session_hydration_service.py backend/tests/test_intent_parser_api.py -q`
  - Result: `44 passed`

Broader backend verification:

- `pytest backend/tests -q`
  - Result: `155 passed, 5 skipped`

### Frontend tests and checks

Targeted frontend verification:

- `npm --prefix frontend test -- src/pages/session/SessionWorkspacePage.test.tsx src/features/session/chat/chatToUiActions.test.ts src/features/session/chat/actionEchoes.test.ts src/features/session/chat/SessionChatPane.test.tsx`
  - Result: pass

Broader frontend verification:

- `npm --prefix frontend test`
  - Result: `14 passed, 71 passed tests`
- `npm --prefix frontend run lint`
  - Result: pass
- `npm --prefix frontend run build`
  - Result: pass

### Browser-based visual QA

I used the `webapp-qa` skill and the repo’s Docker Compose browser runner.

Compose command used to run the app for QA:

- `docker compose -f infra/compose/docker-compose.yml -f /tmp/storyteller-qa.override.yml up -d backend frontend browser`

The override was necessary because the checked-out local `secrets.yaml` was not compatible with the current backend config shape. The override set:

- `STORYTELLER_SECRETS_FILE=""`
- `STORYTELLER_GEMINI_API_KEY=qa-placeholder-key`

I seeded a session directly through the local backend and verified the characters stage for:

- selected refined character sheet rendering
- visible `Minor refinement` metadata
- the new `Focus characters`, `Change summary`, and `Planning impact` controls

Browser spec run:

- `docker compose -f infra/compose/docker-compose.yml -f /tmp/storyteller-qa.override.yml run --rm browser npm run check -- --spec /workspace/.artifacts/webapp-qa/character-refinement-stage.spec.json`
  - Result: pass

Screenshot artifact:

- `.artifacts/webapp-qa/character-refinement-stage.png`

Visual coverage limit:

- The browser QA covered persisted UI rendering on a seeded session, not a live Gemini-backed chat round-trip, because the QA stack intentionally used a placeholder API key. The chat-driven refinement path is covered through contract, parser, policy, and workspace tests instead.

## LLM And Prompt Evaluation Coverage

I did not add a new standalone eval harness file, but I did extend and preserve the existing prompt/intent evaluation coverage. The relevant named criteria and outcomes are:

- `targeted_character_refinement_contract`
  - Source: `backend/tests/test_chat_action_contracts.py::test_chat_to_ui_action_contract_supports_targeted_character_refinement`
  - Outcome: pass
  - Measured behavior: selector fields, `focus_character_names`, and `change_impact="minor"` parse successfully.
- `latest_character_options_grounding`
  - Source: `backend/tests/test_intent_parser_service.py::test_intent_parser_service_includes_latest_character_options_in_prompt_summary`
  - Outcome: pass
  - Measured behavior: rendered prompt includes `Latest character options:` plus revision-tagged entries for the current saved character sheets.
- `durable_memory_summary_sections_preserved`
  - Source: `backend/tests/test_conversation_memory_evals.py::test_eval_intent_parser_prompt_uses_durable_memory_summary_sections`
  - Outcome: pass
  - Measured behavior: durable memory section headings remain present in the rendered prompt context after the character-grounding changes.
- `minor_character_refinement_policy_side_effects`
  - Source: `backend/tests/test_action_policy_service.py::test_policy_treats_minor_character_refinement_as_non_invalidating`
  - Outcome: pass
  - Measured behavior: preview requires confirmation, but accepted minor refinement produces no invalidation side effects.
- `minor_character_refinement_relinks_selected_beats`
  - Source: `backend/tests/test_session_service.py::test_minor_character_sheet_refinement_preserves_completed_beats_and_relinks_them`
  - Outcome: pass
  - Measured behavior: completed beats remain completed and the selected beat sheet is relinked to the refined character sheet.

## Wrong Turns, Dead Ends, And Gotchas

- I initially changed prompt-context assembly in a way that broke the existing durable-memory eval. The failure came from flattening context instead of preserving the existing summary-section builder. I corrected that by routing the prompt through `build_session_agent_context_summary(snapshot)` and then appending the new character-specific context instead of reconstructing the full summary manually.
- I first assumed the repo root owned the active Docker Compose file. It does not. The correct compose entrypoint for QA in this repo is `infra/compose/docker-compose.yml`.
- The local `secrets.yaml` on disk did not match the current backend settings expectations, which caused the backend container to fail during browser QA. I avoided mutating repo config and used a temporary Compose override instead.
- The worktree already contained unrelated `.yolopilot` log and status churn. I left those alone and committed only the code and test changes for this prompt.

## Assumptions I Had To Make While Working Unsupervised

- Minor character refinements are those that preserve the underlying arc and downstream beat compatibility. In that case, the correct behavior is to keep the accepted beat sheet valid and relink it to the refined character sheet.
- Major character refinements are any changes substantial enough to invalidate downstream planning, even if the user reached them via a conversational refinement request rather than a full regenerate action.
- The intent parser and the UI are both allowed to provide `change_impact`; if they do not, backend helpers should still be able to infer a reasonable default.
- Reusing the persisted refinement rationale in chat echoes is better than synthesizing a new client-only description, because it keeps the chat log and durable state aligned.
- For browser QA, a seeded local session is an acceptable substitute for a live provider-backed generation round-trip as long as the user-visible state and the refinement controls being validated are the real hydrated app surfaces.

## Repository State

- Feature checkpoint commit: `d7c0df1` (`feat(prompt-47): character refinement via chat`)
- The code changes for prompt 47 are committed.
- I intentionally did not modify or clean unrelated `.yolopilot` run-log files already present in the worktree.

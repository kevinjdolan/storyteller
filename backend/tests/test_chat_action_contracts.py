from __future__ import annotations

import json
from pathlib import Path

import pytest
from app.models import (
    ChatToUIActionBatch,
    ChatToUIActionDefaultPolicy,
    ChatToUIActionType,
    RefineBeatSheetAction,
    RefineCharacterSheetAction,
    RefinePitchAction,
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
                    "action_type": "refine_pitch",
                    "target_stage": "pitches",
                    "confidence": 0.9,
                    "rationale": "The user wants pitch two to become a sibling story.",
                    "requires_confirmation": True,
                    "extracted_values": {
                        "pitch_index": 2,
                        "instructions": "Make it about siblings.",
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

    assert len(batch.actions) == 4
    assert isinstance(batch.actions[0], SelectGenreAction)
    assert isinstance(batch.actions[1], RefineBeatSheetAction)
    assert isinstance(batch.actions[2], RefinePitchAction)
    assert isinstance(batch.actions[3], UpdateAudioSettingsAction)
    assert batch.actions[2].extracted_values.instructions == "Make it about siblings."
    assert batch.actions[3].extracted_values.playback_speed == 0.9


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


def test_chat_to_ui_action_contract_supports_targeted_character_refinement() -> None:
    batch = ChatToUIActionBatch.model_validate(
        {
            "schema_version": 1,
            "actions": [
                {
                    "schema_version": 1,
                    "action_type": "refine_character_sheet",
                    "target_stage": "characters",
                    "confidence": 0.86,
                    "rationale": "The user asked to soften Mira's voice on revision two.",
                    "requires_confirmation": True,
                    "extracted_values": {
                        "revision_number": 2,
                        "title": "Lantern Keeper Cast",
                        "instructions": "Soften Mira's voice and keep the same comfort ritual.",
                        "focus_character_names": ["Mira"],
                        "change_summary": "Keep the same arc but make the dialogue gentler.",
                        "change_impact": "minor",
                    },
                }
            ],
        }
    )

    assert isinstance(batch.actions[0], RefineCharacterSheetAction)
    assert batch.actions[0].extracted_values.revision_number == 2
    assert batch.actions[0].extracted_values.change_impact.value == "minor"


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

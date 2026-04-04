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
    CharacterChangeImpact,
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


def test_policy_requires_confirmation_for_pitch_refinement_and_resolves_source_pitch(
    db_session,
) -> None:
    catalog = _seed_catalog(db_session)
    seeded = _create_story_setup_session(db_session, catalog)
    request = SessionActionPolicyEvaluationRequest.model_validate(
        {
            "actions": [
                {
                    "action": {
                        "schema_version": 1,
                        "action_type": "refine_pitch",
                        "target_stage": "pitches",
                        "confidence": 0.9,
                        "rationale": "The user asked to turn the pitch into a sibling story.",
                        "requires_confirmation": True,
                        "extracted_values": {
                            "pitch_index": 1,
                            "instructions": "Make it about siblings.",
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

    assert preview.evaluated_actions[0].decision == SessionActionDecision.REQUIRES_CONFIRMATION
    assert applied.evaluated_actions[0].decision == SessionActionDecision.ACCEPTED_WITH_SIDE_EFFECTS


def test_policy_allows_story_docx_download_when_manuscript_is_ready_even_before_export_exists(
    db_session,
) -> None:
    catalog = _seed_catalog(db_session)
    seeded = _create_story_setup_session(
        db_session,
        catalog,
        mark_composition_completed=True,
        story_asset_kinds=[AssetKind.STORY_TEXT],
    )
    service = SessionService(db_session)
    service.update_stage_state(
        seeded["session_id"],
        stage=WorkflowStage.AUDIO,
        status=WorkflowStageState.COMPLETED,
    )
    service.update_stage_state(
        seeded["session_id"],
        stage=WorkflowStage.FINALIZE,
        status=WorkflowStageState.COMPLETED,
    )

    request = SessionActionPolicyEvaluationRequest.model_validate(
        {
            "actions": [
                {
                    "action": {
                        "schema_version": 1,
                        "action_type": "download_asset",
                        "target_stage": "finalize",
                        "confidence": 0.94,
                        "rationale": "The user asked to download the Word manuscript.",
                        "requires_confirmation": False,
                        "extracted_values": {
                            "asset_kind": "story_docx",
                        },
                    }
                }
            ]
        }
    )

    result = SessionActionPolicyService(db_session).evaluate_request(
        seeded["session_id"],
        request=request,
    )

    assert result.evaluated_actions[0].decision == SessionActionDecision.ACCEPTED


def test_policy_treats_minor_character_refinement_as_non_invalidating(
    db_session,
) -> None:
    catalog = _seed_catalog(db_session)
    seeded = _create_story_setup_session(db_session, catalog)
    request = SessionActionPolicyEvaluationRequest.model_validate(
        {
            "actions": [
                {
                    "action": {
                        "schema_version": 1,
                        "action_type": "refine_character_sheet",
                        "target_stage": "characters",
                        "confidence": 0.87,
                        "rationale": "The user only wants a softer character voice.",
                        "requires_confirmation": True,
                        "extracted_values": {
                            "instructions": "Soften Mira's voice and make the reassurance warmer.",
                            "change_summary": "Keep the same arc but make the dialogue gentler.",
                            "change_impact": CharacterChangeImpact.MINOR.value,
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

    assert preview.evaluated_actions[0].decision == SessionActionDecision.REQUIRES_CONFIRMATION
    assert preview.evaluated_actions[0].side_effects == []
    assert applied.evaluated_actions[0].decision == SessionActionDecision.ACCEPTED


def test_policy_rejects_audio_generation_when_story_text_is_not_ready(db_session) -> None:
    catalog = _seed_catalog(db_session)
    seeded = _create_story_setup_session(
        db_session,
        catalog,
        mark_composition_completed=True,
    )
    request = SessionActionPolicyEvaluationRequest.model_validate(
        {
            "actions": [
                {
                    "confirmation_granted": True,
                    "action": {
                        "schema_version": 1,
                        "action_type": "start_audio_generation",
                        "target_stage": "audio",
                        "confidence": 0.93,
                        "rationale": "The user wants narration now.",
                        "requires_confirmation": True,
                        "extracted_values": {
                            "voice_key": "gemini-soft-1",
                        },
                    },
                }
            ]
        }
    )

    result = SessionActionPolicyService(db_session).evaluate_request(
        seeded["session_id"],
        request=request,
    )

    assert result.evaluated_actions[0].decision == SessionActionDecision.REJECTED
    assert result.evaluated_actions[0].reasons[0].code == SessionActionReasonCode.ASSET_NOT_READY


def test_policy_rejects_resume_job_when_audio_job_is_not_paused(db_session) -> None:
    catalog = _seed_catalog(db_session)
    seeded = _create_story_setup_session(
        db_session,
        catalog,
        mark_composition_completed=True,
        story_asset_kinds=[AssetKind.STORY_TEXT],
        audio_status=JobStatus.IN_PROGRESS,
    )
    request = SessionActionPolicyEvaluationRequest.model_validate(
        {
            "actions": [
                {
                    "confirmation_granted": True,
                    "action": {
                        "schema_version": 1,
                        "action_type": "resume_job",
                        "target_stage": "audio",
                        "confidence": 0.87,
                        "rationale": "The user asked to continue narration.",
                        "requires_confirmation": True,
                        "extracted_values": {
                            "job_kind": "audio",
                        },
                    },
                }
            ]
        }
    )

    result = SessionActionPolicyService(db_session).evaluate_request(
        seeded["session_id"],
        request=request,
    )

    assert result.evaluated_actions[0].decision == SessionActionDecision.REJECTED
    assert result.evaluated_actions[0].reasons[0].code == SessionActionReasonCode.JOB_STATE_CONFLICT


def _seed_catalog(db_session):
    quest_fantasy = Genre(
        slug="quest-fantasy",
        label="Quest Fantasy",
        description="A soft quest.",
    )
    hushed_wonder = ToneProfile(
        genre=quest_fantasy,
        slug="hushed-wonder",
        label="Hushed Wonder",
        description="Quiet and luminous.",
    )
    moon_mystery = Genre(
        slug="moon-mystery",
        label="Moon Mystery",
        description="A calm puzzle.",
    )
    silver_hush = ToneProfile(
        genre=moon_mystery,
        slug="silver-hush",
        label="Silver Hush",
        description="Softly mysterious.",
    )
    db_session.add_all([quest_fantasy, hushed_wonder, moon_mystery, silver_hush])
    db_session.flush()
    return {
        "quest_fantasy": quest_fantasy,
        "hushed_wonder": hushed_wonder,
        "moon_mystery": moon_mystery,
        "silver_hush": silver_hush,
    }


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

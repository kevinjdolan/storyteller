from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from threading import Thread
from time import sleep
from urllib.parse import unquote

import httpx
import pytest
from app.ai import render_intent_parser_prompt
from app.db import (
    AssetKind,
    AssetStatus,
    AudioJob,
    BackgroundJob,
    Base,
    BeatSheet,
    CharacterSheet,
    CompositionInterruptionRequest,
    CompositionInterruptionState,
    CompositionJob,
    CompositionJobKind,
    CompositionSegment,
    CompositionSegmentAcceptanceState,
    Genre,
    JobStatus,
    Pitch,
    SessionAsset,
    StoryBrief,
    StoryOutline,
    StorySession,
    StorySetup,
    ToneProfile,
    make_engine,
)
from app.models import (
    ChatMessageRole,
    ChatToUIActionBatch,
    IntentParserPromptContext,
    IntentParserStageContext,
    StoryWorkflowToolExecutionMode,
    StoryWorkflowToolName,
    WorkflowStage,
    WorkflowStageState,
)
from app.services import (
    COMPOSITION_RUNTIME_JOB_TYPE,
    BackgroundJobService,
    CompositionJobService,
    SessionService,
    StoryWorkflowActionRouter,
    StoryWorkflowToolService,
    evaluate_composition_segment_draft,
    get_story_workflow_tool_registry,
    get_story_workflow_tool_schema_bundle,
)
from app.services.composition_jobs import (
    GeneratedCompositionSegmentDraft,
    _build_composition_summary_message,
    _has_emitted_summary_checkpoint,
    _plan_composition_summary_checkpoints,
)
from app.services.composition_streaming import (
    STREAMING_MAX_CHUNK_WORDS,
    STREAMING_MIN_CHUNK_WORDS,
    split_text_for_streaming,
)
from app.services.event_log import SessionEventLogService
from app.services.session_hydration import SessionHydrationService
from app.services.session_realtime import CompositionChunkCursor, SessionRealtimeService
from app.settings import load_settings
from app.storage import ObjectStorageService, StorageObjectLocation, build_object_storage_service
from app.worker import JobWorker, build_default_job_handler_registry
from sqlalchemy import select
from sqlalchemy.orm import Session, sessionmaker


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


def _build_session_factory(tmp_path: Path) -> sessionmaker[Session]:
    database_path = tmp_path / "story-tools.db"
    engine = make_engine(f"sqlite+pysqlite:///{database_path}")
    _enable_sqlite_foreign_keys(engine)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


def _wait_for_condition(
    predicate,
    *,
    timeout_seconds: float = 3.0,
    interval_seconds: float = 0.02,
) -> None:
    deadline = datetime.now(timezone.utc) + timedelta(seconds=timeout_seconds)
    while datetime.now(timezone.utc) < deadline:
        if predicate():
            return
        sleep(interval_seconds)

    raise AssertionError("timed out waiting for condition")


def _job_progress_percent(
    session_factory: sessionmaker[Session],
    composition_job_id: str,
) -> float:
    with session_factory() as session:
        job = session.get(CompositionJob, composition_job_id)
        return float(job.progress_percent if job is not None else 0)


class FakeGCSJsonAPI:
    def __init__(self) -> None:
        self.buckets: set[str] = set()
        self.objects: dict[tuple[str, str], dict[str, object]] = {}

    def handle(self, request: httpx.Request) -> httpx.Response:
        path = request.url.raw_path.decode().split("?", 1)[0]

        if request.method == "POST" and path == "/storage/v1/b":
            payload = json.loads(request.content.decode("utf-8"))
            bucket_name = str(payload["name"])
            if bucket_name in self.buckets:
                return httpx.Response(status_code=409, json={"error": {"message": "exists"}})
            self.buckets.add(bucket_name)
            return httpx.Response(status_code=200, json={"name": bucket_name})

        upload_prefix = "/upload/storage/v1/b/"
        if request.method == "POST" and path.startswith(upload_prefix) and path.endswith("/o"):
            bucket_name = unquote(path[len(upload_prefix) : -2])
            key = unquote(request.url.params["name"])
            if bucket_name not in self.buckets:
                self.buckets.add(bucket_name)
            generation = str(len(self.objects) + 1)
            metadata = {
                "bucket": bucket_name,
                "name": key,
                "size": str(len(request.content)),
                "contentType": request.headers.get("Content-Type"),
                "etag": f"etag-{generation}",
                "generation": generation,
                "md5Hash": "fake-md5",
                "updated": "2026-04-02T00:00:00Z",
            }
            self.objects[(bucket_name, key)] = {
                "metadata": metadata,
                "content": request.content,
            }
            return httpx.Response(status_code=200, json=metadata)

        metadata_prefix = "/storage/v1/b/"
        if request.method == "GET" and path.startswith(metadata_prefix) and "/o/" in path:
            remainder = path[len(metadata_prefix) :]
            bucket_name, key = remainder.split("/o/", 1)
            stored = self.objects.get((unquote(bucket_name), unquote(key)))
            if stored is None:
                return httpx.Response(status_code=404, json={"error": {"message": "missing"}})
            if request.url.params.get("alt") == "media":
                return httpx.Response(
                    status_code=200,
                    content=stored["content"],
                    headers={
                        "Content-Type": str(
                            stored["metadata"].get("contentType")
                            if isinstance(stored["metadata"], dict)
                            else ""
                        )
                    },
                )
            return httpx.Response(status_code=200, json=stored["metadata"])

        return httpx.Response(status_code=500, json={"error": {"message": "unhandled"}})


class RecordingCompositionWriter:
    def __init__(self, *, label: str) -> None:
        self.label = label
        self.payloads: list[dict[str, object]] = []

    def compose_segment(
        self,
        *,
        segment_payload,
        prior_segments,
        current_partial_text,
        total_segments,
    ) -> GeneratedCompositionSegmentDraft:
        del prior_segments, current_partial_text, total_segments
        payload = dict(segment_payload)
        self.payloads.append(payload)
        prompt = payload["composition_prompt"]
        dynamic_context = prompt["dynamic_context"]
        segment_index = int(dynamic_context["segment_index"])
        protagonist_name = (
            dynamic_context["selected_character_sheet"].get("protagonist_name") or "Mira"
        )
        companion_name = "Pip"
        accepted_text = _build_recorded_segment_text(
            label=self.label,
            segment_index=segment_index,
            protagonist_name=protagonist_name,
            companion_name=companion_name,
        )
        carryover_summary = (
            f"{self.label} segment {segment_index} leaves {protagonist_name} calmer, keeps the "
            f"bell promise active, and sends {companion_name} forward as visible support."
        )
        evaluation = evaluate_composition_segment_draft(
            accepted_text,
            protagonist_name=protagonist_name,
            supporting_character_name=companion_name,
            carryover_summary=carryover_summary,
        )
        paragraphs = [paragraph for paragraph in accepted_text.split("\n\n") if paragraph.strip()]
        return GeneratedCompositionSegmentDraft(
            raw_text=f"{accepted_text}\n\nRaw drafting note: {self.label} pass.",
            accepted_text=accepted_text,
            carryover_summary=carryover_summary,
            remaining_chunks=tuple(paragraphs),
            evaluation=evaluation,
            source="heuristic",
        )


class SummaryCheckpointCompositionWriter:
    def compose_segment(
        self,
        *,
        segment_payload,
        prior_segments,
        current_partial_text,
        total_segments,
    ) -> GeneratedCompositionSegmentDraft:
        del prior_segments, current_partial_text, total_segments
        dynamic_context = segment_payload["composition_prompt"]["dynamic_context"]
        segment_index = int(dynamic_context["segment_index"])
        protagonist_name = (
            dynamic_context["selected_character_sheet"].get("protagonist_name") or "Mira"
        )
        companion_name = "Pip"
        chunks = (
            (
                f"{protagonist_name} followed the bell along the quieter dock while the "
                "lantern glow stayed gentle and easy to trust. "
            ),
            (
                f"{companion_name} answered each new question before the harbor could "
                "feel uncertain or sharp. "
            ),
            (
                "The cove widened into silver water that felt hushed, companioned, and "
                "ready for a softer midpoint reveal. "
            ),
            (
                "Together they noticed the bell guiding them toward a sheltered rope "
                "where the tide sounded restful instead of strange. "
            ),
            (
                f"Every next step stayed calm enough for {protagonist_name} to keep "
                "wondering without losing a sense of safety. "
            ),
            (
                f"The moment landed in visible repair, leaving {protagonist_name} and "
                f"{companion_name} ready for the next handoff. "
            ),
        )
        accepted_text = "".join(chunks).strip()
        carryover_summary = (
            f"Segment {segment_index} moves {protagonist_name} deeper into the sheltered cove, "
            f"keeps {companion_name} close, and ends in calm repair."
        )
        evaluation = evaluate_composition_segment_draft(
            accepted_text,
            protagonist_name=protagonist_name,
            supporting_character_name=companion_name,
            carryover_summary=carryover_summary,
        )
        return GeneratedCompositionSegmentDraft(
            raw_text=accepted_text,
            accepted_text=accepted_text,
            carryover_summary=carryover_summary,
            remaining_chunks=chunks,
            evaluation=evaluation,
            source="heuristic",
        )


class StreamingLoopCompositionWriter:
    def compose_segment(
        self,
        *,
        segment_payload,
        prior_segments,
        current_partial_text,
        total_segments,
    ) -> GeneratedCompositionSegmentDraft:
        del prior_segments, current_partial_text, total_segments
        dynamic_context = segment_payload["composition_prompt"]["dynamic_context"]
        segment_index = int(dynamic_context["segment_index"])
        protagonist_name = (
            dynamic_context["selected_character_sheet"].get("protagonist_name") or "Mira"
        )
        companion_name = "Pip"
        accepted_text = self.segment_text(
            segment_index=segment_index,
            protagonist_name=protagonist_name,
            companion_name=companion_name,
        )
        carryover_summary = (
            f"Segment {segment_index} keeps {protagonist_name} moving forward calmly, "
            f"keeps {companion_name} visible, and lands the handoff in repair."
        )
        evaluation = evaluate_composition_segment_draft(
            accepted_text,
            protagonist_name=protagonist_name,
            supporting_character_name=companion_name,
            carryover_summary=carryover_summary,
        )
        return GeneratedCompositionSegmentDraft(
            raw_text=accepted_text,
            accepted_text=accepted_text,
            carryover_summary=carryover_summary,
            remaining_chunks=tuple(split_text_for_streaming("", accepted_text)),
            evaluation=evaluation,
            source="heuristic",
        )

    def segment_text(
        self,
        *,
        segment_index: int,
        protagonist_name: str = "Mira",
        companion_name: str = "Pip",
    ) -> str:
        return "\n\n".join(
            [
                (
                    f"Draft segment {segment_index} lets {protagonist_name} follow the silver "
                    "bell along a lantern path where every ripple stays readable, warm, and "
                    "gentle enough for bedtime listening."
                ),
                (
                    f"{companion_name} stays close beside {protagonist_name}, answering each new "
                    "question before the harbor can feel sharp, and the prose keeps the movement "
                    "soft, patient, visibly cared for, and easy to trust."
                ),
                (
                    f"The segment closes in calm repair, so {protagonist_name} and "
                    f"{companion_name} can hand the story forward with the promise intact, the "
                    "water settled, and the night ready for the next quiet turn."
                ),
            ]
        )

    def story_text(self, segment_indexes: list[int]) -> str:
        return "\n\n".join(
            self.segment_text(segment_index=segment_index)
            for segment_index in segment_indexes
        )


def _build_recorded_segment_text(
    *,
    label: str,
    segment_index: int,
    protagonist_name: str,
    companion_name: str,
) -> str:
    return "\n\n".join(
        [
            (
                f"{label} segment {segment_index} lets {protagonist_name} follow the silver bell "
                f"through a gentle stretch of harbor water while the night stays readable, warm, "
                "and unmistakably safe for bedtime listening."
            ),
            (
                f"{companion_name} stays close enough to steady every surprise, and the prose "
                "keeps "
                "the movement soft, patient, visibly cared for, and easy for a sleepy child to "
                "trust."
            ),
            (
                f"The moment lands in calm repair, so {protagonist_name} and {companion_name} can "
                "rest before the next handoff, with the harbor settled, the promise intact, and "
                "the final image quiet."
            ),
        ]
    )


def _build_test_object_storage() -> tuple[FakeGCSJsonAPI, httpx.Client, ObjectStorageService]:
    fake_gcs = FakeGCSJsonAPI()
    settings = load_settings(
        {
            "STORYTELLER_SECRETS_FILE": "",
            "STORYTELLER_DATABASE_URL": "sqlite+pysqlite:///:memory:",
            "STORYTELLER_GEMINI_API_KEY": "test-gemini-key",
            "STORYTELLER_GCS_ENDPOINT": "http://gcs:4443",
            "STORYTELLER_GCS_PROJECT_ID": "storyteller-local",
            "STORYTELLER_GCS_PUBLIC_URL": "http://localhost:8568",
            "STORYTELLER_GCS_SESSIONS_BUCKET_NAME": "storyteller-sessions",
            "STORYTELLER_GCS_AUDIO_BUCKET_NAME": "storyteller-audio",
            "STORYTELLER_GCS_EXPORTS_BUCKET_NAME": "storyteller-exports",
        },
    )
    client = httpx.Client(
        base_url=settings.gcs_endpoint,
        transport=httpx.MockTransport(fake_gcs.handle),
    )
    object_storage = build_object_storage_service(settings, client=client)
    return fake_gcs, client, object_storage


def test_story_workflow_tool_schema_bundle_lists_expected_operations() -> None:
    bundle = get_story_workflow_tool_schema_bundle()

    tool_names = [item["tool_name"] for item in bundle["tools"]]
    assert bundle["bundle_schema_version"] == 1
    assert tool_names == [
        "compose_next_segment",
        "estimate_audio_length",
        "generate_beat_sheet",
        "generate_character_sheets",
        "generate_pitches",
        "refine_character_sheet",
        "refine_pitch",
        "rewrite_segments",
        "start_audio_generation",
        "update_setup_heuristics",
        "update_story_outline",
    ]
    assert bundle["tools"][0]["side_effects"]
    assert bundle["tools"][-1]["output_schema"]["title"] == "UpdateStoryOutlineToolResult"


def test_story_workflow_action_router_maps_chat_actions_to_shared_tool_calls() -> None:
    batch = ChatToUIActionBatch.model_validate(
        {
            "actions": [
                {
                    "action_type": "refine_pitch",
                    "target_stage": "pitches",
                    "confidence": 0.86,
                    "requires_confirmation": True,
                    "extracted_values": {
                        "pitch_index": 2,
                        "instructions": "Make the pitch about siblings.",
                    },
                },
                {
                    "action_type": "update_story_setup",
                    "target_stage": "story_setup",
                    "confidence": 0.9,
                    "requires_confirmation": False,
                    "extracted_values": {
                        "target_runtime_minutes": 8,
                        "chapter_count": 2,
                    },
                },
                {
                    "action_type": "start_composition",
                    "target_stage": "composition",
                    "confidence": 0.88,
                    "requires_confirmation": True,
                    "extracted_values": {
                        "mode": "rewrite",
                        "instructions": "Rewrite the opening scene to feel gentler.",
                        "restart_from_segment_index": 1,
                    },
                },
                {
                    "action_type": "start_audio_generation",
                    "target_stage": "audio",
                    "confidence": 0.81,
                    "requires_confirmation": True,
                    "extracted_values": {
                        "voice_key": "gemini-soft-1",
                        "playback_speed": 0.9,
                    },
                },
            ]
        }
    )

    plan = StoryWorkflowActionRouter().plan_calls(
        session_id="session-123",
        batch=batch,
    )

    assert [call.tool_name for call in plan.calls] == [
        StoryWorkflowToolName.REFINE_PITCH,
        StoryWorkflowToolName.UPDATE_SETUP_HEURISTICS,
        StoryWorkflowToolName.REWRITE_SEGMENTS,
        StoryWorkflowToolName.START_AUDIO_GENERATION,
    ]
    assert plan.calls[0].arguments == {
        "instructions": "Make the pitch about siblings.",
        "pitch_index": 2,
        "schema_version": 1,
    }
    assert plan.calls[2].arguments == {
        "instructions": "Rewrite the opening scene to feel gentler.",
        "rewrite_from_segment_index": 1,
        "preserve_completed_segments": False,
        "schema_version": 1,
    }


def test_story_workflow_tool_service_updates_setup_and_cancels_invalidated_jobs(
    db_session,
) -> None:
    seeded = _seed_story_setup_session(
        db_session,
        composition_status=JobStatus.IN_PROGRESS,
        audio_status=JobStatus.IN_PROGRESS,
    )

    result = StoryWorkflowToolService(db_session).execute(
        tool_name=StoryWorkflowToolName.UPDATE_SETUP_HEURISTICS,
        session_id=seeded["session_id"],
        arguments={
            "target_runtime_minutes": 8,
            "chapter_count": 2,
            "approximate_scene_count": 7,
            "guidance_notes": "Keep the ending even softer.",
        },
    )

    snapshot = SessionService(db_session).load_session_snapshot(seeded["session_id"])
    composition_job = db_session.get(CompositionJob, seeded["composition_job_id"])
    audio_job = db_session.get(AudioJob, seeded["audio_job_id"])

    assert result.story_setup_id == snapshot.selected_story_setup.id
    assert result.revision_number == 2
    assert snapshot.selected_story_setup.target_runtime_minutes == 8
    assert snapshot.selected_story_setup.chapter_count == 2
    assert snapshot.selected_story_setup.approximate_scene_count == 7
    assert snapshot.selected_story_setup.guidance_notes == "Keep the ending even softer."
    assert snapshot.selected_story_outline is not None
    assert snapshot.selected_story_outline.outline_kind == "chapter"
    assert len(snapshot.selected_story_outline.cards) == 2
    assert composition_job is not None and composition_job.status == JobStatus.CANCELLED
    assert audio_job is not None and audio_job.status == JobStatus.CANCELLED
    assert _stage_status(snapshot, WorkflowStage.STORY_SETUP) == WorkflowStageState.COMPLETED
    assert (
        _stage_status(snapshot, WorkflowStage.COMPOSITION) == WorkflowStageState.NEEDS_REGENERATION
    )
    assert _stage_status(snapshot, WorkflowStage.AUDIO) == WorkflowStageState.NEEDS_REGENERATION


def test_story_workflow_tool_service_tracks_minor_outline_edits(
    db_session,
) -> None:
    seeded = _seed_story_setup_session(
        db_session,
        composition_status=JobStatus.IN_PROGRESS,
        audio_status=JobStatus.IN_PROGRESS,
    )
    snapshot = SessionService(db_session).load_session_snapshot(seeded["session_id"])
    assert snapshot.selected_story_outline is not None

    cards = [
        {
            **card.model_dump(mode="json"),
            "summary": (
                "Open on a calmer harbor image, then let Mira follow the first drifting bell."
                if card.card_key == "chapter-1"
                else card.summary
            ),
            "purpose": (
                "Set the moonlit harbor rhythm and launch the first gentle problem."
                if card.card_key == "chapter-1"
                else card.purpose
            ),
        }
        for card in snapshot.selected_story_outline.cards
    ]

    result = StoryWorkflowToolService(db_session).execute(
        tool_name=StoryWorkflowToolName.UPDATE_STORY_OUTLINE,
        session_id=seeded["session_id"],
        arguments={
            "outline_id": snapshot.selected_story_outline.id,
            "cards": cards,
            "origin": "workspace",
        },
    )

    updated_snapshot = SessionService(db_session).load_session_snapshot(seeded["session_id"])
    composition_job = db_session.get(CompositionJob, seeded["composition_job_id"])
    audio_job = db_session.get(AudioJob, seeded["audio_job_id"])

    assert updated_snapshot.selected_story_outline is not None
    assert result.summary == (
        "Updated 1 outline card. Composition, audio, and finalize should refresh before reuse."
    )
    assert updated_snapshot.selected_story_outline.change_impact == "minor"
    assert updated_snapshot.selected_story_outline.last_change_summary == result.summary
    assert updated_snapshot.selected_story_outline.invalidated_stages == [
        WorkflowStage.COMPOSITION,
        WorkflowStage.AUDIO,
        WorkflowStage.FINALIZE,
    ]
    assert updated_snapshot.selected_story_outline.edit_history[0].changed_card_keys == [
        "chapter-1"
    ]
    assert composition_job is not None and composition_job.status == JobStatus.CANCELLED
    assert audio_job is not None and audio_job.status == JobStatus.CANCELLED


def test_story_workflow_tool_service_marks_reordered_outline_as_structural(
    db_session,
) -> None:
    seeded = _seed_story_setup_session(
        db_session,
        composition_status=JobStatus.IN_PROGRESS,
        audio_status=JobStatus.IN_PROGRESS,
    )
    snapshot = SessionService(db_session).load_session_snapshot(seeded["session_id"])
    assert snapshot.selected_story_outline is not None

    reversed_cards = [
        card.model_dump(mode="json") for card in reversed(snapshot.selected_story_outline.cards)
    ]

    result = StoryWorkflowToolService(db_session).execute(
        tool_name=StoryWorkflowToolName.UPDATE_STORY_OUTLINE,
        session_id=seeded["session_id"],
        arguments={
            "outline_id": snapshot.selected_story_outline.id,
            "cards": reversed_cards,
            "regenerate_card_keys": ["chapter-1"],
            "origin": "workspace",
        },
    )

    updated_snapshot = SessionService(db_session).load_session_snapshot(seeded["session_id"])

    assert updated_snapshot.selected_story_outline is not None
    assert result.summary == (
        "Saved a structural outline revision after reordering 2 cards. "
        "Composition, audio, and finalize need regeneration."
    )
    assert updated_snapshot.selected_story_outline.change_impact == "major"
    assert updated_snapshot.selected_story_outline.edit_history[0].reordered is True
    assert updated_snapshot.selected_story_outline.edit_history[0].regenerated_card_keys == [
        "chapter-1"
    ]
    assert updated_snapshot.selected_story_outline.cards[0].card_key == "chapter-3"
    assert updated_snapshot.selected_story_outline.cards[-1].card_key == "chapter-1"
    assert updated_snapshot.selected_story_outline.cards[-1].purpose is not None


def test_story_workflow_tool_service_estimates_audio_length_from_segments(db_session) -> None:
    seeded = _seed_story_setup_session(
        db_session,
        mark_composition_completed=True,
        composition_segment_word_counts=[240, 160],
    )

    result = StoryWorkflowToolService(db_session).execute(
        tool_name=StoryWorkflowToolName.ESTIMATE_AUDIO_LENGTH,
        session_id=seeded["session_id"],
        arguments={
            "playback_speed": 0.8,
        },
    )

    assert result.estimated_word_count == 400
    assert result.estimated_duration_seconds == 215
    assert result.basis_source == "composition_segments"


def test_story_workflow_tool_service_updates_story_outline_and_tracks_revision(
    db_session,
) -> None:
    seeded = _seed_story_setup_session(
        db_session,
        composition_status=JobStatus.IN_PROGRESS,
        audio_status=JobStatus.IN_PROGRESS,
    )
    snapshot = SessionService(db_session).load_session_snapshot(seeded["session_id"])
    assert snapshot.selected_story_outline is not None

    cards = []
    for card in snapshot.selected_story_outline.cards:
        cards.append(
            {
                **card.model_dump(mode="json"),
                "summary": (
                    "Open with a calmer harbor image and let the card land on visible relief."
                    if card.position == 1
                    else card.summary
                ),
            }
        )

    result = StoryWorkflowToolService(db_session).execute(
        tool_name=StoryWorkflowToolName.UPDATE_STORY_OUTLINE,
        session_id=seeded["session_id"],
        arguments={
            "outline_id": snapshot.selected_story_outline.id,
            "summary": snapshot.selected_story_outline.summary,
            "cards": cards,
            "origin": "workspace",
        },
    )

    refreshed = SessionService(db_session).load_session_snapshot(seeded["session_id"])
    composition_job = db_session.get(CompositionJob, seeded["composition_job_id"])
    audio_job = db_session.get(AudioJob, seeded["audio_job_id"])

    assert refreshed.selected_story_outline is not None
    assert result.story_outline_id == refreshed.selected_story_outline.id
    assert refreshed.selected_story_outline.revision_number == 2
    assert refreshed.selected_story_outline.cards[0].summary.startswith("Open with a calmer")
    assert composition_job is not None and composition_job.status == JobStatus.CANCELLED
    assert audio_job is not None and audio_job.status == JobStatus.CANCELLED


def test_story_workflow_tool_service_seeds_composition_segments_from_outline_cards(
    db_session,
) -> None:
    seeded = _seed_story_setup_session(db_session)

    result = StoryWorkflowToolService(db_session).execute(
        tool_name=StoryWorkflowToolName.COMPOSE_NEXT_SEGMENT,
        session_id=seeded["session_id"],
        arguments={},
    )

    job = db_session.get(CompositionJob, result.composition_job_id)
    segment = db_session.get(CompositionSegment, result.segment_id)

    assert job is not None
    assert segment is not None
    assert job.metadata_json["story_outline_id"]
    assert job.metadata_json["outline_card_title"].startswith("Chapter 1:")
    assert job.metadata_json["continuity_bible_id"]
    assert job.metadata_json["continuity_summary"]
    assert job.metadata_json["composition_prompt"]["assembly_version"] == (
        "composition_prompt_assembly.v1"
    )
    assert (
        "Stage focus for composition"
        in job.metadata_json["composition_prompt"]["system_instructions"][
            "bedtime_guidelines_fragment"
        ]
    )
    assert (
        job.metadata_json["composition_prompt"]["dynamic_context"]["genre"]["label"]
        == "Quest Fantasy"
    )
    assert segment.payload["continuity_bible_id"] == job.metadata_json["continuity_bible_id"]
    assert any(fact["category"] == "promise" for fact in segment.payload["continuity_facts"])
    assert segment.payload["composition_prompt"]["debug_context"]["outline_card_key"] == "chapter-1"
    assert segment.planned_summary is not None
    assert "Chapter 1" in job.metadata_json["outline_card_title"]


def test_story_workflow_tool_service_tracks_plan_revision_lineage_for_composition(
    db_session,
) -> None:
    seeded = _seed_story_setup_session(db_session)

    result = StoryWorkflowToolService(db_session).execute(
        tool_name=StoryWorkflowToolName.COMPOSE_NEXT_SEGMENT,
        session_id=seeded["session_id"],
        arguments={},
    )

    snapshot = SessionService(db_session).load_session_snapshot(seeded["session_id"])
    job = db_session.get(CompositionJob, result.composition_job_id)

    assert job is not None
    assert job.plan_revision_id is not None
    assert snapshot.current_plan_revision is not None
    assert snapshot.current_plan_revision.revision_number == 1
    assert snapshot.current_plan_revision.beat_sheet is not None
    assert snapshot.current_plan_revision.beat_sheet.revision_number == 1
    assert snapshot.current_plan_revision.story_setup is not None
    assert snapshot.current_plan_revision.story_setup.revision_number == 1
    assert snapshot.current_plan_revision.story_outline is not None
    assert snapshot.current_plan_revision.story_outline.revision_number == 1
    assert len(snapshot.plan_revisions) == 1
    assert snapshot.latest_composition_job is not None
    assert snapshot.latest_composition_job.id == result.composition_job_id
    assert snapshot.latest_composition_job.plan_revision_id == job.plan_revision_id
    assert snapshot.latest_composition_job.plan_revision_number == 1
    assert snapshot.latest_composition_job.beat_sheet_revision_number == 1
    assert snapshot.latest_composition_job.story_setup_revision_number == 1
    assert snapshot.latest_composition_job.story_outline_revision_number == 1


def test_eval_composition_payload_inherits_outline_metadata_and_drafting_brief(
    db_session,
) -> None:
    seeded = _seed_story_setup_session(db_session)

    result = StoryWorkflowToolService(db_session).execute(
        tool_name=StoryWorkflowToolName.COMPOSE_NEXT_SEGMENT,
        session_id=seeded["session_id"],
        arguments={},
    )

    job = db_session.get(CompositionJob, result.composition_job_id)
    segment = db_session.get(CompositionSegment, result.segment_id)

    assert job is not None
    assert segment is not None
    assert job.metadata_json["story_outline_id"]
    assert job.metadata_json["outline_card_key"] == "chapter-1"
    assert job.metadata_json["outline_card_position"] == 1
    assert job.metadata_json["outline_card_beat_keys"] == [
        "opening_image",
        "catalyst",
    ]
    assert job.metadata_json["continuity_revision_number"] == 1
    assert segment.payload["continuity_revision_number"] == 1
    assert any(
        fact["category"] == "voice_constraint" for fact in segment.payload["continuity_facts"]
    )
    assert (
        job.metadata_json["composition_prompt"]["dynamic_context"]["outline_card"]["card_key"]
        == "chapter-1"
    )
    assert (
        job.metadata_json["composition_prompt"]["dynamic_context"]["segment_goal_summary"]
        == "Chapter 1 should cover Opening Image and Catalyst while staying calm and luminous."
    )
    assert (
        segment.planned_summary
        == "Chapter 1 should cover Opening Image and Catalyst while staying calm and luminous."
    )
    assert (
        segment.payload["outline_card_drafting_brief"]
        == "Chapter 1 should cover Opening Image and Catalyst while staying calm and luminous."
    )


def test_story_workflow_tool_service_persists_rewrite_prompt_package(db_session) -> None:
    seeded = _seed_story_setup_session(db_session)

    result = StoryWorkflowToolService(db_session).execute(
        tool_name=StoryWorkflowToolName.REWRITE_SEGMENTS,
        session_id=seeded["session_id"],
        arguments={
            "instructions": "Soften the midpoint and make the support visible sooner.",
            "rewrite_from_segment_index": 2,
        },
    )

    job = db_session.get(CompositionJob, result.composition_job_id)
    segment = db_session.get(CompositionSegment, result.segment_id)

    assert job is not None
    assert segment is not None
    assert job.metadata_json["composition_prompt"]["dynamic_context"]["job_kind"] == "rewrite"
    assert job.metadata_json["composition_prompt"]["dynamic_context"]["segment_index"] == 2
    assert (
        job.metadata_json["composition_prompt"]["dynamic_context"]["request_instructions"]
        == "Soften the midpoint and make the support visible sooner."
    )
    assert job.metadata_json["outline_card_key"] == "chapter-2"
    assert segment.planned_summary == "Soften the midpoint and make the support visible sooner."


def test_eval_outline_edit_revisions_keep_locked_structure_and_refresh_downstream(
    db_session,
) -> None:
    seeded = _seed_story_setup_session(
        db_session,
        composition_status=JobStatus.IN_PROGRESS,
        audio_status=JobStatus.IN_PROGRESS,
    )
    snapshot = SessionService(db_session).load_session_snapshot(seeded["session_id"])
    assert snapshot.selected_story_outline is not None

    original_cards = snapshot.selected_story_outline.cards
    edited_cards = []
    for card in original_cards:
        edited_cards.append(
            {
                **card.model_dump(mode="json"),
                "title": (
                    "Chapter 1: Lantern Wake and Gentle Departure"
                    if card.card_key == "chapter-1"
                    else card.title
                ),
                "drafting_brief": (
                    "Chapter 1 should move from harbor stillness into a visibly safe departure."
                    if card.card_key == "chapter-1"
                    else card.drafting_brief
                ),
            }
        )

    StoryWorkflowToolService(db_session).execute(
        tool_name=StoryWorkflowToolName.UPDATE_STORY_OUTLINE,
        session_id=seeded["session_id"],
        arguments={
            "outline_id": snapshot.selected_story_outline.id,
            "summary": snapshot.selected_story_outline.summary,
            "cards": edited_cards,
            "origin": "workspace",
        },
    )

    refreshed = SessionService(db_session).load_session_snapshot(seeded["session_id"])
    assert refreshed.selected_story_outline is not None

    edited_card = refreshed.selected_story_outline.cards[0]
    original_card = original_cards[0]

    assert refreshed.selected_story_outline.revision_number == 2
    assert edited_card.title == "Chapter 1: Lantern Wake and Gentle Departure"
    assert (
        edited_card.drafting_brief
        == "Chapter 1 should move from harbor stillness into a visibly safe departure."
    )
    assert edited_card.beat_keys == original_card.beat_keys
    assert edited_card.target_word_count == original_card.target_word_count
    assert edited_card.target_scene_count == original_card.target_scene_count
    assert (
        _stage_status(
            refreshed,
            WorkflowStage.COMPOSITION,
        )
        == WorkflowStageState.NEEDS_REGENERATION
    )
    assert (
        _stage_status(
            refreshed,
            WorkflowStage.AUDIO,
        )
        == WorkflowStageState.NEEDS_REGENERATION
    )


def test_worker_processes_story_tool_job_via_default_registry(tmp_path: Path) -> None:
    session_factory = _build_session_factory(tmp_path)

    with session_factory() as session:
        seeded = _seed_story_setup_session(session)
        queued = StoryWorkflowToolService(session).enqueue(
            tool_name=StoryWorkflowToolName.UPDATE_SETUP_HEURISTICS,
            session_id=seeded["session_id"],
            arguments={
                "target_runtime_minutes": 7,
                "guidance_notes": "Make the read-aloud shorter.",
            },
        )

    worker = JobWorker(
        session_factory=session_factory,
        registry=build_default_job_handler_registry(),
        worker_id="story-tool-worker",
        lease_duration=timedelta(seconds=30),
        poll_interval_seconds=0.01,
    )

    assert worker.run_once() is True

    with session_factory() as session:
        job = BackgroundJobService(session).get_job(queued.id)
        snapshot = SessionService(session).load_session_snapshot(seeded["session_id"])

    assert job.status == JobStatus.COMPLETED
    assert job.result_summary["tool_name"] == "update_setup_heuristics"
    assert snapshot.selected_story_setup is not None
    assert snapshot.selected_story_setup.target_runtime_minutes == 7


def test_story_workflow_tool_service_queues_durable_composition_execution(
    db_session,
) -> None:
    seeded = _seed_story_setup_session(db_session)

    result = StoryWorkflowToolService(db_session).execute(
        tool_name=StoryWorkflowToolName.COMPOSE_NEXT_SEGMENT,
        session_id=seeded["session_id"],
        arguments={},
    )

    job = db_session.get(CompositionJob, result.composition_job_id)
    segments = list(
        db_session.execute(
            select(CompositionSegment)
            .where(CompositionSegment.composition_job_id == result.composition_job_id)
            .order_by(CompositionSegment.segment_index.asc())
        ).scalars()
    )
    queued_runtime_jobs = list(
        db_session.execute(
            select(BackgroundJob)
            .where(BackgroundJob.job_type == COMPOSITION_RUNTIME_JOB_TYPE)
            .order_by(BackgroundJob.created_at.asc())
        ).scalars()
    )

    assert job is not None
    assert job.status == JobStatus.QUEUED
    assert job.current_segment_index == 1
    assert job.metadata_json["total_segments"] == 3
    assert [segment.segment_index for segment in segments] == [1, 2, 3]
    assert all(segment.status == JobStatus.QUEUED for segment in segments)
    assert len(queued_runtime_jobs) == 1
    assert queued_runtime_jobs[0].payload["composition_job_id"] == result.composition_job_id


def test_composition_job_service_resume_does_not_duplicate_runtime_attempts(
    db_session,
) -> None:
    seeded = _seed_story_setup_session(db_session)
    result = StoryWorkflowToolService(db_session).execute(
        tool_name=StoryWorkflowToolName.COMPOSE_NEXT_SEGMENT,
        session_id=seeded["session_id"],
        arguments={},
    )
    service = CompositionJobService(db_session)

    service.pause_job(seeded["session_id"], result.composition_job_id)
    service.resume_job(seeded["session_id"], result.composition_job_id)

    queued_runtime_jobs = list(
        db_session.execute(
            select(BackgroundJob)
            .where(BackgroundJob.job_type == COMPOSITION_RUNTIME_JOB_TYPE)
            .order_by(BackgroundJob.created_at.asc())
        ).scalars()
    )
    pending_for_job = [
        job
        for job in queued_runtime_jobs
        if isinstance(job.payload, dict)
        and job.payload.get("composition_job_id") == result.composition_job_id
        and job.status == JobStatus.QUEUED
    ]
    composition_job = db_session.get(CompositionJob, result.composition_job_id)

    assert composition_job is not None
    assert composition_job.status == JobStatus.QUEUED
    assert len(pending_for_job) == 1


def test_composition_pause_request_is_durable_and_applies_after_checkpoint(
    tmp_path: Path,
) -> None:
    _fake_gcs, client, object_storage = _build_test_object_storage()
    session_factory = _build_session_factory(tmp_path)
    worker_result: dict[str, object] = {}

    try:
        with session_factory() as session:
            seeded = _seed_story_setup_session(session)
            result = StoryWorkflowToolService(session).execute(
                tool_name=StoryWorkflowToolName.COMPOSE_NEXT_SEGMENT,
                session_id=seeded["session_id"],
                arguments={},
            )

        def run_worker() -> None:
            try:
                with session_factory() as session:
                    service = CompositionJobService(
                        session,
                        object_storage=object_storage,
                        writer=SummaryCheckpointCompositionWriter(),
                        chunk_delay_seconds=0.05,
                    )
                    worker_result["result"] = service.run_job(result.composition_job_id)
            except Exception as exc:  # pragma: no cover - surfaced in assertion below
                worker_result["error"] = exc

        worker_thread = Thread(target=run_worker)
        worker_thread.start()

        _wait_for_condition(
            lambda: _job_progress_percent(session_factory, result.composition_job_id) > 0
        )

        with session_factory() as session:
            CompositionJobService(session).pause_job(
                seeded["session_id"],
                result.composition_job_id,
            )

        worker_thread.join(timeout=5)
        assert not worker_thread.is_alive()
        assert "error" not in worker_result, worker_result.get("error")

        with session_factory() as session:
            job = session.get(CompositionJob, result.composition_job_id)
            request = session.execute(
                select(CompositionInterruptionRequest)
                .where(
                    CompositionInterruptionRequest.composition_job_id
                    == result.composition_job_id
                )
                .order_by(CompositionInterruptionRequest.created_at.desc())
            ).scalar_one()
            draft_snapshot_assets = list(
                session.execute(
                    select(SessionAsset).where(
                        SessionAsset.session_id == seeded["session_id"],
                        SessionAsset.asset_kind == AssetKind.DRAFT_TEXT_SNAPSHOT,
                    )
                ).scalars()
            )
            history = SessionEventLogService(session).list_session_history(
                seeded["session_id"]
            )

        assert job is not None
        assert len(draft_snapshot_assets) == 1
        draft_snapshot_asset = draft_snapshot_assets[0]
        draft_snapshot_text = object_storage.download_text(
            StorageObjectLocation(
                bucket=draft_snapshot_asset.storage_bucket,
                key=draft_snapshot_asset.object_path,
            )
        )
        criteria = {
            "worker_paused_after_checkpoint": worker_result["result"]["action"] == "paused",
            "job_status_paused": job.status == JobStatus.PAUSED,
            "request_applied": request.state == CompositionInterruptionState.APPLIED,
            "active_segment_captured": request.requested_segment_index == 1,
            "progress_captured": request.requested_progress_percent is not None
            and request.requested_progress_percent > 0,
            "partial_output_captured": isinstance(request.metadata_json, dict)
            and isinstance(request.metadata_json.get("latest_partial_output"), str)
            and len(str(request.metadata_json.get("latest_partial_output"))) > 0,
            "draft_snapshot_is_rolling": (
                draft_snapshot_asset.object_path
                == f"sessions/{seeded['session_id']}/composition/drafts/latest-stable.md"
            ),
            "draft_snapshot_ready": draft_snapshot_asset.status == AssetStatus.READY,
            "draft_snapshot_points_at_job": draft_snapshot_asset.composition_job_id
            == result.composition_job_id,
            "draft_snapshot_text_saved": len(draft_snapshot_text.strip()) > 0,
            "replay_event_mentions_pause_request": any(
                getattr(getattr(event.payload, "interruption_request", None), "request_kind", None)
                == "pause"
                for event in history.events
                if event.event_type == "composition.progress.recorded"
            ),
        }

        assert all(criteria.values()), criteria
    finally:
        object_storage.close()
        client.close()


def test_composition_redirect_request_is_durable_and_starts_rewrite_after_checkpoint(
    tmp_path: Path,
) -> None:
    _fake_gcs, client, object_storage = _build_test_object_storage()
    session_factory = _build_session_factory(tmp_path)
    worker_result: dict[str, object] = {}

    try:
        with session_factory() as session:
            seeded = _seed_story_setup_session(session)
            result = StoryWorkflowToolService(session).execute(
                tool_name=StoryWorkflowToolName.COMPOSE_NEXT_SEGMENT,
                session_id=seeded["session_id"],
                arguments={},
            )

        def run_worker() -> None:
            try:
                with session_factory() as session:
                    service = CompositionJobService(
                        session,
                        object_storage=object_storage,
                        writer=SummaryCheckpointCompositionWriter(),
                        chunk_delay_seconds=0.05,
                    )
                    worker_result["result"] = service.run_job(result.composition_job_id)
            except Exception as exc:  # pragma: no cover - surfaced in assertion below
                worker_result["error"] = exc

        worker_thread = Thread(target=run_worker)
        worker_thread.start()

        _wait_for_condition(
            lambda: _job_progress_percent(session_factory, result.composition_job_id) > 0
        )

        with session_factory() as session:
            CompositionJobService(session).request_redirect(
                seeded["session_id"],
                result.composition_job_id,
                instructions="Soften the cove reveal and bring Pip in sooner.",
                rewrite_from_segment_index=1,
            )

        worker_thread.join(timeout=5)
        assert not worker_thread.is_alive()
        assert "error" not in worker_result, worker_result.get("error")

        rewrite_job_id = str(worker_result["result"]["composition_job_id"])
        with session_factory() as session:
            original_job = session.get(CompositionJob, result.composition_job_id)
            rewrite_job = session.get(CompositionJob, rewrite_job_id)
            request = session.execute(
                select(CompositionInterruptionRequest)
                .where(
                    CompositionInterruptionRequest.composition_job_id
                    == result.composition_job_id
                )
                .order_by(CompositionInterruptionRequest.created_at.desc())
            ).scalar_one()
            history = SessionEventLogService(session).list_session_history(
                seeded["session_id"]
            )

        assert original_job is not None
        assert rewrite_job is not None
        criteria = {
            "worker_redirected_after_checkpoint": worker_result["result"]["action"]
            == "redirected",
            "original_job_cancelled": original_job.status == JobStatus.CANCELLED,
            "rewrite_job_created": rewrite_job.job_kind == CompositionJobKind.REWRITE,
            "rewrite_job_queued": rewrite_job.status == JobStatus.QUEUED,
            "rewrite_instructions_persisted": (
                isinstance(rewrite_job.metadata_json, dict)
                and rewrite_job.metadata_json.get("request_instructions")
                == "Soften the cove reveal and bring Pip in sooner."
            ),
            "request_applied": request.state == CompositionInterruptionState.APPLIED,
            "request_kept_user_change": request.instructions
            == "Soften the cove reveal and bring Pip in sooner.",
            "request_captured_segment": request.requested_segment_index == 1,
            "replay_event_mentions_redirect": any(
                getattr(getattr(event.payload, "interruption_request", None), "request_kind", None)
                == "redirect"
                for event in history.events
                if event.event_type == "composition.progress.recorded"
            ),
        }

        assert all(criteria.values()), criteria
    finally:
        object_storage.close()
        client.close()


def test_composition_loop_e2e_streams_pause_resume_and_hydrates(
    tmp_path: Path,
) -> None:
    _fake_gcs, client, object_storage = _build_test_object_storage()
    session_factory = _build_session_factory(tmp_path)
    writer = StreamingLoopCompositionWriter()
    worker_result: dict[str, object] = {}

    try:
        with session_factory() as session:
            seeded = _seed_story_setup_session(session)
            result = StoryWorkflowToolService(session).execute(
                tool_name=StoryWorkflowToolName.COMPOSE_NEXT_SEGMENT,
                session_id=seeded["session_id"],
                arguments={},
            )

        with session_factory() as session:
            initial_events, realtime_cursor = SessionRealtimeService(
                session
            ).read_composition_chunk_events(
                seeded["session_id"],
                cursor=CompositionChunkCursor(),
            )

        assert len(initial_events) == 1
        assert initial_events[0].payload.chunk_kind.value == "segment_start"
        assert initial_events[0].payload.segment_index == 1

        def run_worker() -> None:
            try:
                with session_factory() as session:
                    worker_result["result"] = CompositionJobService(
                        session,
                        object_storage=object_storage,
                        writer=writer,
                        chunk_delay_seconds=0.05,
                    ).run_job(result.composition_job_id)
            except Exception as exc:  # pragma: no cover - surfaced in assertion below
                worker_result["error"] = exc

        worker_thread = Thread(target=run_worker)
        worker_thread.start()

        _wait_for_condition(
            lambda: _job_progress_percent(session_factory, result.composition_job_id) > 0
        )

        with session_factory() as session:
            CompositionJobService(session).pause_job(
                seeded["session_id"],
                result.composition_job_id,
            )

        worker_thread.join(timeout=5)
        assert not worker_thread.is_alive()
        assert "error" not in worker_result, worker_result.get("error")
        assert worker_result["result"]["action"] == "paused"

        with session_factory() as session:
            paused_job = session.get(CompositionJob, result.composition_job_id)
            paused_segment = session.execute(
                select(CompositionSegment)
                .where(
                    CompositionSegment.composition_job_id == result.composition_job_id,
                    CompositionSegment.segment_index == 1,
                )
                .limit(1)
            ).scalar_one()
            draft_snapshot_asset = session.execute(
                select(SessionAsset).where(
                    SessionAsset.session_id == seeded["session_id"],
                    SessionAsset.composition_job_id == result.composition_job_id,
                    SessionAsset.asset_kind == AssetKind.DRAFT_TEXT_SNAPSHOT,
                )
            ).scalar_one()
            paused_hydration = SessionHydrationService(
                session,
                object_storage=object_storage,
            ).hydrate_session(seeded["session_id"])
            paused_events, realtime_cursor = SessionRealtimeService(
                session
            ).read_composition_chunk_events(
                seeded["session_id"],
                cursor=realtime_cursor,
            )
            history = SessionEventLogService(session).list_session_history(
                seeded["session_id"]
            )

        paused_story_text = object_storage.download_text(
            StorageObjectLocation(
                bucket=draft_snapshot_asset.storage_bucket,
                key=draft_snapshot_asset.object_path,
            )
        )
        paused_delta_events = [
            event for event in paused_events if event.payload.chunk_kind.value == "delta"
        ]
        paused_progress_events = [
            event
            for event in history.events
            if event.event_type == "composition.progress.recorded"
        ]

        assert paused_job is not None
        assert paused_job.status == JobStatus.PAUSED
        assert paused_job.progress_percent > 0
        assert paused_job.current_segment_index == 1
        assert paused_segment.status == JobStatus.PAUSED
        assert paused_segment.accepted_text == paused_story_text
        assert paused_segment.accepted_text
        assert paused_story_text.strip()
        assert paused_story_text != writer.segment_text(segment_index=1)
        assert "".join(
            event.payload.text or "" for event in paused_delta_events
        ) == paused_story_text
        assert paused_hydration.snapshot.active_composition_job is not None
        assert paused_hydration.snapshot.active_composition_job.status == JobStatus.PAUSED
        assert (
            paused_hydration.snapshot.active_composition_job.accepted_story_so_far
            == paused_story_text
        )
        assert (
            paused_hydration.snapshot.active_composition_job.latest_partial_output
            == paused_story_text
        )
        assert any(
            getattr(getattr(event.payload, "interruption_request", None), "request_kind", None)
            == "pause"
            for event in paused_progress_events
        )

        with session_factory() as session:
            CompositionJobService(session).resume_job(
                seeded["session_id"],
                result.composition_job_id,
            )

        with session_factory() as session:
            resumed_hydration = SessionHydrationService(
                session,
                object_storage=object_storage,
            ).hydrate_session(seeded["session_id"])

        assert resumed_hydration.snapshot.active_composition_job is not None
        assert resumed_hydration.snapshot.active_composition_job.status == JobStatus.QUEUED
        assert resumed_hydration.snapshot.active_composition_job.current_segment_index == 1
        assert (
            resumed_hydration.snapshot.active_composition_job.accepted_story_so_far
            == paused_story_text
        )
        assert (
            resumed_hydration.snapshot.active_composition_job.latest_partial_output
            == paused_story_text
        )

        with session_factory() as session:
            resumed_result = CompositionJobService(
                session,
                object_storage=object_storage,
                writer=writer,
            ).run_job(result.composition_job_id)

        assert resumed_result["action"] == "queued_next_segment"
        assert resumed_result["next_segment_index"] == 2

        expected_segment_one = writer.segment_text(segment_index=1)
        assert expected_segment_one.startswith(paused_story_text)

        with session_factory() as session:
            resumed_session_hydration = SessionHydrationService(
                session,
                object_storage=object_storage,
            ).hydrate_session(seeded["session_id"])
            resumed_events, realtime_cursor = SessionRealtimeService(
                session
            ).read_composition_chunk_events(
                seeded["session_id"],
                cursor=realtime_cursor,
            )

        resumed_delta_events = [
            event for event in resumed_events if event.payload.chunk_kind.value == "delta"
        ]
        resumed_summary_events = [
            event
            for event in resumed_events
            if event.payload.chunk_kind.value == "segment_summary"
        ]
        resumed_segment_start_events = [
            event
            for event in resumed_events
            if event.payload.chunk_kind.value == "segment_start"
        ]

        assert resumed_session_hydration.snapshot.active_composition_job is not None
        assert resumed_session_hydration.snapshot.active_composition_job.status == JobStatus.QUEUED
        assert resumed_session_hydration.snapshot.active_composition_job.current_segment_index == 2
        assert (
            resumed_session_hydration.snapshot.active_composition_job.accepted_story_so_far
            == expected_segment_one
        )
        assert (
            resumed_session_hydration.snapshot.active_composition_job.latest_partial_output
            == expected_segment_one
        )
        assert resumed_segment_start_events
        assert resumed_segment_start_events[0].payload.segment_index == 2
        assert "".join(event.payload.text or "" for event in resumed_delta_events) == (
            expected_segment_one[len(paused_story_text) :]
        )
        assert resumed_summary_events
        assert resumed_summary_events[0].payload.summary.startswith("Segment 1 keeps Mira")

        with session_factory() as session:
            second_result = CompositionJobService(
                session,
                object_storage=object_storage,
                writer=writer,
            ).run_job(result.composition_job_id)

        with session_factory() as session:
            final_result = CompositionJobService(
                session,
                object_storage=object_storage,
                writer=writer,
            ).run_job(result.composition_job_id)

        assert second_result["action"] == "queued_next_segment"
        assert second_result["next_segment_index"] == 3
        assert final_result["action"] == "completed"

        with session_factory() as session:
            final_job = session.get(CompositionJob, result.composition_job_id)
            final_segments = list(
                session.execute(
                    select(CompositionSegment)
                    .where(CompositionSegment.composition_job_id == result.composition_job_id)
                    .order_by(CompositionSegment.segment_index.asc())
                ).scalars()
            )
            final_story_asset = session.execute(
                select(SessionAsset).where(
                    SessionAsset.composition_job_id == result.composition_job_id,
                    SessionAsset.asset_kind == AssetKind.STORY_TEXT,
                )
            ).scalar_one()
            final_hydration = SessionHydrationService(
                session,
                object_storage=object_storage,
            ).hydrate_session(seeded["session_id"])

        final_story_text = object_storage.download_text(
            StorageObjectLocation(
                bucket=final_story_asset.storage_bucket,
                key=final_story_asset.object_path,
            )
        )
        expected_story_text = writer.story_text([1, 2, 3])

        assert final_job is not None
        assert final_job.status == JobStatus.COMPLETED
        assert final_job.progress_percent == 100
        assert [segment.status for segment in final_segments] == [
            JobStatus.COMPLETED,
            JobStatus.COMPLETED,
            JobStatus.COMPLETED,
        ]
        assert [segment.accepted_text for segment in final_segments] == [
            writer.segment_text(segment_index=1),
            writer.segment_text(segment_index=2),
            writer.segment_text(segment_index=3),
        ]
        assert final_story_text == expected_story_text
        assert final_hydration.snapshot.active_composition_job is None
        assert final_hydration.snapshot.latest_composition_job is not None
        assert final_hydration.snapshot.latest_composition_job.status == JobStatus.COMPLETED
        assert (
            final_hydration.snapshot.latest_composition_job.accepted_story_so_far
            == expected_story_text
        )
    finally:
        object_storage.close()
        client.close()


def test_split_text_for_streaming_preserves_exact_story_text() -> None:
    text = (
        "Mira followed the bell through the harbor while the docks stayed soft and silver. "
        "Pip kept close enough to answer every worry before it could grow.\n\n"
        "By the time they reached the quieter cove, the water itself sounded sleepy."
    )

    chunks = split_text_for_streaming("", text)

    assert len(chunks) > 1
    assert "".join(chunks) == text
    assert all(chunk for chunk in chunks)


def test_split_text_for_streaming_targets_readable_live_chunks() -> None:
    text = (
        "Mira stepped carefully between the lantern posts while Otis counted each ripple along "
        "the dock. Every silver reflection carried a small reminder that the harbor was calm, "
        "watched, and already leaning toward sleep. When the drifting bell paused near the last "
        "mooring rope, Mira slowed down enough to hear the water answer in gentle, even taps. "
        "Otis kept beside her so the next step felt guided instead of hurried, and the path home "
        "stayed bright without ever turning loud."
    )

    chunks = split_text_for_streaming("", text)
    non_terminal_counts = [len(chunk.split()) for chunk in chunks[:-1]]

    assert len(chunks) >= 2
    assert "".join(chunks) == text
    assert non_terminal_counts
    assert all(
        STREAMING_MIN_CHUNK_WORDS <= word_count <= STREAMING_MAX_CHUNK_WORDS
        for word_count in non_terminal_counts
    )


def test_composition_summary_checkpoints_follow_meaningful_progress_steps() -> None:
    one_chunk = _plan_composition_summary_checkpoints(1)
    two_chunks = _plan_composition_summary_checkpoints(2)
    six_chunks = _plan_composition_summary_checkpoints(6)

    assert one_chunk == ()
    assert [(checkpoint.key, checkpoint.chunk_index) for checkpoint in two_chunks] == [
        ("progress-34", 1),
    ]
    assert [(checkpoint.key, checkpoint.chunk_index) for checkpoint in six_chunks] == [
        ("progress-34", 3),
        ("progress-67", 5),
    ]


def test_eval_composition_summary_messages_stay_grounded_and_compact() -> None:
    message = _build_composition_summary_message(
        segment_index=2,
        total_segments=4,
        current_text=(
            "Mira followed the bell toward the quieter cove while Pip kept the water calm and "
            "readable. The cove widened into silver water that felt hushed and companioned."
        ),
        segment_payload={
            "outline_card_title": "Chapter 2",
            "outline_card_summary": "Let the cove reveal feel soft and inviting",
            "outline_card_emotional_shift": "keep the wonder gentle and companioned",
            "composition_prompt": {
                "dynamic_context": {
                    "segment_goal_summary": "Reveal the cove without losing the bedtime calm.",
                    "outline_card": {
                        "bedtime_guardrail": "keep the harbor settled",
                    },
                }
            },
        },
        planned_summary="Center the midpoint reveal softly.",
        progress_percent=44,
        checkpoint_key="progress-34",
    )

    assert message is not None
    criteria = {
        "mentions_progress": message.startswith("Writing update 44%"),
        "grounds_excerpt_in_generated_text": "The cove widened" in message,
        "includes_direction": "Direction:" in message,
        "includes_focus": "Focus:" in message,
        "stays_compact_for_history_replay": len(message) <= 160,
    }

    assert all(criteria.values()), criteria


def test_composition_job_service_records_checkpointed_summary_chat_messages(
    tmp_path: Path,
) -> None:
    _fake_gcs, client, object_storage = _build_test_object_storage()
    session_factory = _build_session_factory(tmp_path)

    try:
        with session_factory() as session:
            seeded = _seed_story_setup_session(session)
            result = StoryWorkflowToolService(session).execute(
                tool_name=StoryWorkflowToolName.COMPOSE_NEXT_SEGMENT,
                session_id=seeded["session_id"],
                arguments={},
            )

        with session_factory() as session:
            service = CompositionJobService(
                session,
                object_storage=object_storage,
                writer=SummaryCheckpointCompositionWriter(),
            )
            run_result = service.run_job(result.composition_job_id)
            first_segment = session.execute(
                select(CompositionSegment)
                .where(
                    CompositionSegment.composition_job_id == result.composition_job_id,
                    CompositionSegment.segment_index == 1,
                )
                .order_by(CompositionSegment.revision_number.desc())
            ).scalar_one()
            history = SessionEventLogService(session).list_session_history(
                seeded["session_id"]
            )
            composition_job = session.get(CompositionJob, result.composition_job_id)

        summary_events = [
            event
            for event in history.events
            if event.event_type == "chat.message.recorded"
            and getattr(event.payload, "source", None) == "composition_summary"
        ]
        summary_message_ids = [
            getattr(event.payload, "message_id", None) for event in summary_events
        ]
        criteria = {
            "segment_completed_and_requeued": run_result["action"] == "queued_next_segment",
            "three_checkpoint_messages": len(summary_events) == 3,
            "assistant_role_only": all(
                getattr(event.payload, "message_role", None) == ChatMessageRole.ASSISTANT
                for event in summary_events
            ),
            "composition_stage_only": all(
                event.stage == WorkflowStage.COMPOSITION for event in summary_events
            ),
            "stable_checkpoint_ids": summary_message_ids == [
                f"composition-summary-{result.composition_job_id}-{first_segment.id}-progress-34",
                f"composition-summary-{result.composition_job_id}-{first_segment.id}-progress-67",
                f"composition-summary-{result.composition_job_id}-{first_segment.id}-segment-complete",
            ],
            "checkpoint_state_persisted": composition_job is not None
            and _has_emitted_summary_checkpoint(
                composition_job,
                first_segment.id,
                "progress-34",
            )
            and _has_emitted_summary_checkpoint(
                composition_job,
                first_segment.id,
                "progress-67",
            )
            and _has_emitted_summary_checkpoint(
                composition_job,
                first_segment.id,
                "segment-complete",
            ),
            "messages_include_direction_and_focus": all(
                getattr(event.payload, "content", "").count("Direction:") == 1
                and getattr(event.payload, "content", "").count("Focus:") == 1
                for event in summary_events
            ),
        }

        assert all(criteria.values()), criteria
    finally:
        object_storage.close()
        client.close()


def test_composition_job_service_carries_forward_structured_segment_summaries(
    tmp_path: Path,
) -> None:
    _fake_gcs, client, object_storage = _build_test_object_storage()
    session_factory = _build_session_factory(tmp_path)
    writer = RecordingCompositionWriter(label="Draft")

    try:
        with session_factory() as session:
            seeded = _seed_story_setup_session(session)
            result = StoryWorkflowToolService(session).execute(
                tool_name=StoryWorkflowToolName.COMPOSE_NEXT_SEGMENT,
                session_id=seeded["session_id"],
                arguments={},
            )

        with session_factory() as session:
            service = CompositionJobService(
                session,
                object_storage=object_storage,
                writer=writer,
            )
            first_result = service.run_job(result.composition_job_id)
            second_result = service.run_job(result.composition_job_id)

            segment_one = session.execute(
                select(CompositionSegment)
                .where(
                    CompositionSegment.composition_job_id == result.composition_job_id,
                    CompositionSegment.segment_index == 1,
                )
                .order_by(CompositionSegment.revision_number.desc())
            ).scalar_one()
            segment_two = session.execute(
                select(CompositionSegment)
                .where(
                    CompositionSegment.composition_job_id == result.composition_job_id,
                    CompositionSegment.segment_index == 2,
                )
                .order_by(CompositionSegment.revision_number.desc())
            ).scalar_one()

        assert first_result["action"] == "queued_next_segment"
        assert second_result["action"] == "queued_next_segment"
        assert segment_one.raw_generated_text is not None
        assert segment_one.accepted_text is not None
        assert segment_one.accepted_summary is not None
        assert segment_two.payload["context_carryover"]["prior_segment_count"] == 1
        assert (
            segment_two.payload["context_carryover"]["prior_segments"][0]["accepted_summary"]
            == segment_one.accepted_summary
        )
        assert (
            segment_two.payload["context_carryover"]["latest_accepted_summary"]
            == segment_one.accepted_summary
        )
        assert writer.payloads[0]["context_carryover"]["prior_segment_count"] == 0
        assert writer.payloads[1]["context_carryover"]["prior_segment_count"] == 1
    finally:
        object_storage.close()
        client.close()


def test_run_job_persists_draft_progress_across_sessions(
    tmp_path: Path,
) -> None:
    _fake_gcs, client, object_storage = _build_test_object_storage()
    session_factory = _build_session_factory(tmp_path)
    writer = RecordingCompositionWriter(label="Draft")

    try:
        with session_factory() as session:
            seeded = _seed_story_setup_session(session)
            result = StoryWorkflowToolService(session).execute(
                tool_name=StoryWorkflowToolName.COMPOSE_NEXT_SEGMENT,
                session_id=seeded["session_id"],
                arguments={},
            )

        with session_factory() as session:
            service = CompositionJobService(
                session,
                object_storage=object_storage,
                writer=writer,
            )
            first_result = service.run_job(result.composition_job_id)

        assert first_result["action"] == "queued_next_segment"

        with session_factory() as session:
            snapshot = SessionService(session).load_session_snapshot(seeded["session_id"])

        assert snapshot.latest_composition_job is not None
        assert snapshot.latest_composition_job.status == JobStatus.QUEUED
        assert snapshot.latest_composition_job.current_segment_index == 2

        with session_factory() as session:
            service = CompositionJobService(
                session,
                object_storage=object_storage,
                writer=writer,
            )
            second_result = service.run_job(result.composition_job_id)

        assert second_result["action"] == "queued_next_segment"

        with session_factory() as session:
            snapshot = SessionService(session).load_session_snapshot(seeded["session_id"])

        assert snapshot.latest_composition_job is not None
        assert snapshot.latest_composition_job.status == JobStatus.QUEUED
        assert snapshot.latest_composition_job.current_segment_index == 3

        with session_factory() as session:
            service = CompositionJobService(
                session,
                object_storage=object_storage,
                writer=writer,
            )
            third_result = service.run_job(result.composition_job_id)

        assert third_result["action"] == "completed"

        with session_factory() as session:
            snapshot = SessionService(session).load_session_snapshot(seeded["session_id"])
            story_asset = session.execute(
                select(SessionAsset).where(
                    SessionAsset.composition_job_id == result.composition_job_id,
                    SessionAsset.asset_kind == AssetKind.STORY_TEXT,
                )
            ).scalar_one_or_none()

        assert snapshot.latest_composition_job is not None
        assert snapshot.latest_composition_job.status == JobStatus.COMPLETED
        assert _stage_status(snapshot, WorkflowStage.COMPOSITION) == WorkflowStageState.COMPLETED
        assert story_asset is not None
    finally:
        object_storage.close()
        client.close()


def test_run_job_persists_rewrite_review_state_across_sessions(
    tmp_path: Path,
) -> None:
    _fake_gcs, client, object_storage = _build_test_object_storage()
    session_factory = _build_session_factory(tmp_path)
    initial_writer = RecordingCompositionWriter(label="Draft")
    rewrite_writer = RecordingCompositionWriter(label="Rewrite")

    try:
        with session_factory() as session:
            seeded = _seed_story_setup_session(session)
            draft_result = StoryWorkflowToolService(session).execute(
                tool_name=StoryWorkflowToolName.COMPOSE_NEXT_SEGMENT,
                session_id=seeded["session_id"],
                arguments={},
            )

        with session_factory() as session:
            draft_service = CompositionJobService(
                session,
                object_storage=object_storage,
                writer=initial_writer,
            )
            for _ in range(3):
                draft_service.run_job(draft_result.composition_job_id)

            rewrite_result = StoryWorkflowToolService(session).execute(
                tool_name=StoryWorkflowToolName.REWRITE_SEGMENTS,
                session_id=seeded["session_id"],
                arguments={
                    "instructions": "Rewrite the last two chapters to feel even gentler.",
                    "rewrite_from_segment_index": 2,
                },
            )

        with session_factory() as session:
            rewrite_service = CompositionJobService(
                session,
                object_storage=object_storage,
                writer=rewrite_writer,
            )
            first_rewrite_result = rewrite_service.run_job(rewrite_result.composition_job_id)

        assert first_rewrite_result["action"] == "queued_next_segment"

        with session_factory() as session:
            snapshot = SessionService(session).load_session_snapshot(seeded["session_id"])

        assert snapshot.latest_composition_job is not None
        assert snapshot.latest_composition_job.status == JobStatus.QUEUED
        assert snapshot.latest_composition_job.current_segment_index == 3

        with session_factory() as session:
            rewrite_service = CompositionJobService(
                session,
                object_storage=object_storage,
                writer=rewrite_writer,
            )
            second_rewrite_result = rewrite_service.run_job(rewrite_result.composition_job_id)

        assert second_rewrite_result["action"] == "pending_review"

        with session_factory() as session:
            snapshot = SessionService(session).load_session_snapshot(seeded["session_id"])

        assert snapshot.latest_composition_job is not None
        assert snapshot.latest_composition_job.status == JobStatus.COMPLETED
        assert snapshot.latest_composition_job.pending_review is True
        assert snapshot.latest_composition_job.rewrite_candidate_segment_indexes == [2, 3]
        assert sorted(
            segment.segment_index
            for segment in snapshot.composition_segments or []
            if segment.pending_version_id is not None
        ) == [2, 3]
    finally:
        object_storage.close()
        client.close()


def test_rewrite_job_requires_acceptance_before_promoting_segment_revisions(
    tmp_path: Path,
) -> None:
    _fake_gcs, client, object_storage = _build_test_object_storage()
    session_factory = _build_session_factory(tmp_path)
    initial_writer = RecordingCompositionWriter(label="Draft")
    rewrite_writer = RecordingCompositionWriter(label="Rewrite")

    try:
        with session_factory() as session:
            seeded = _seed_story_setup_session(session)
            draft_result = StoryWorkflowToolService(session).execute(
                tool_name=StoryWorkflowToolName.COMPOSE_NEXT_SEGMENT,
                session_id=seeded["session_id"],
                arguments={},
            )

        with session_factory() as session:
            draft_service = CompositionJobService(
                session,
                object_storage=object_storage,
                writer=initial_writer,
            )
            for _ in range(3):
                draft_service.run_job(draft_result.composition_job_id)

            rewrite_result = StoryWorkflowToolService(session).execute(
                tool_name=StoryWorkflowToolName.REWRITE_SEGMENTS,
                session_id=seeded["session_id"],
                arguments={
                    "instructions": "Rewrite the last two chapters with even gentler support.",
                    "rewrite_from_segment_index": 2,
                },
            )

        with session_factory() as session:
            rewrite_service = CompositionJobService(
                session,
                object_storage=object_storage,
                writer=rewrite_writer,
            )
            for _ in range(2):
                rewrite_service.run_job(rewrite_result.composition_job_id)

            rewritten_job = session.get(CompositionJob, rewrite_result.composition_job_id)
            candidate_story_asset = session.execute(
                select(SessionAsset).where(
                    SessionAsset.composition_job_id == rewrite_result.composition_job_id,
                    SessionAsset.asset_kind == AssetKind.STORY_TEXT,
                )
            ).scalar_one_or_none()
            segment_two_revisions = list(
                session.execute(
                    select(CompositionSegment)
                    .where(
                        CompositionSegment.session_id == seeded["session_id"],
                        CompositionSegment.segment_index == 2,
                    )
                    .order_by(CompositionSegment.revision_number.asc())
                ).scalars()
            )

        assert rewritten_job is not None
        assert rewritten_job.status == JobStatus.COMPLETED
        assert candidate_story_asset is None
        assert segment_two_revisions[0].superseded_by_segment_id is None
        assert segment_two_revisions[1].acceptance_state == "pending"
        assert rewrite_writer.payloads[0]["context_carryover"]["prior_segment_count"] == 1
        assert rewrite_writer.payloads[1]["context_carryover"]["prior_segment_count"] == 2

        with session_factory() as session:
            rewrite_service = CompositionJobService(
                session,
                object_storage=object_storage,
                writer=rewrite_writer,
            )
            rewrite_service.accept_rewrite_job(
                seeded["session_id"],
                rewrite_result.composition_job_id,
            )

            rewritten_asset = session.execute(
                select(SessionAsset).where(
                    SessionAsset.composition_job_id == rewrite_result.composition_job_id,
                    SessionAsset.asset_kind == AssetKind.STORY_TEXT,
                )
            ).scalar_one()
            story_text = object_storage.download_text(
                StorageObjectLocation(
                    bucket=rewritten_asset.storage_bucket,
                    key=rewritten_asset.object_path,
                )
            )
            accepted_segment_two_revisions = list(
                session.execute(
                    select(CompositionSegment)
                    .where(
                        CompositionSegment.session_id == seeded["session_id"],
                        CompositionSegment.segment_index == 2,
                    )
                    .order_by(CompositionSegment.revision_number.asc())
                ).scalars()
            )

        assert "Draft segment 1" in story_text
        assert "Rewrite segment 2" in story_text
        assert "Rewrite segment 3" in story_text
        assert "Draft segment 2" not in story_text
        assert len(accepted_segment_two_revisions) == 2
        assert (
            accepted_segment_two_revisions[0].superseded_by_segment_id
            == accepted_segment_two_revisions[1].id
        )
        assert (
            accepted_segment_two_revisions[1].acceptance_state
            == CompositionSegmentAcceptanceState.ACCEPTED
        )
    finally:
        object_storage.close()
        client.close()


def test_accepting_manual_rewrite_marks_downstream_segments_stale(
    tmp_path: Path,
) -> None:
    _fake_gcs, client, object_storage = _build_test_object_storage()
    session_factory = _build_session_factory(tmp_path)
    initial_writer = RecordingCompositionWriter(label="Draft")
    rewrite_writer = RecordingCompositionWriter(label="Rewrite")

    try:
        with session_factory() as session:
            seeded = _seed_story_setup_session(session)
            draft_result = StoryWorkflowToolService(session).execute(
                tool_name=StoryWorkflowToolName.COMPOSE_NEXT_SEGMENT,
                session_id=seeded["session_id"],
                arguments={},
            )

        with session_factory() as session:
            draft_service = CompositionJobService(
                session,
                object_storage=object_storage,
                writer=initial_writer,
            )
            for _ in range(3):
                draft_service.run_job(draft_result.composition_job_id)

            rewrite_result = StoryWorkflowToolService(session).execute(
                tool_name=StoryWorkflowToolName.REWRITE_SEGMENTS,
                session_id=seeded["session_id"],
                arguments={
                    "instructions": "Rewrite the harbor opening with a calmer promise.",
                    "rewrite_from_segment_index": 1,
                    "rewrite_to_segment_index": 1,
                    "downstream_regeneration_mode": "require_confirmation",
                },
            )

        with session_factory() as session:
            rewrite_service = CompositionJobService(
                session,
                object_storage=object_storage,
                writer=rewrite_writer,
            )
            rewrite_service.run_job(rewrite_result.composition_job_id)
            rewrite_service.accept_rewrite_job(
                seeded["session_id"],
                rewrite_result.composition_job_id,
            )

            snapshot = SessionService(session).load_session_snapshot(seeded["session_id"])
            current_segments = {
                row.segment_index: row
                for row in session.execute(
                    select(CompositionSegment).where(
                        CompositionSegment.session_id == seeded["session_id"],
                        CompositionSegment.acceptance_state
                        == CompositionSegmentAcceptanceState.ACCEPTED,
                        CompositionSegment.superseded_by_segment_id.is_(None),
                    )
                ).scalars()
            }

        assert snapshot.latest_composition_job is not None
        assert snapshot.latest_composition_job.stale_from_segment_index == 2
        assert snapshot.latest_composition_job.stale_to_segment_index == 3
        assert _stage_status(snapshot, WorkflowStage.COMPOSITION) == (
            WorkflowStageState.NEEDS_REGENERATION
        )
        assert current_segments[1].is_stale is False
        assert current_segments[2].is_stale is True
        assert current_segments[3].is_stale is True
    finally:
        object_storage.close()
        client.close()


def test_rejecting_rewrite_keeps_current_manuscript_clean(
    tmp_path: Path,
) -> None:
    _fake_gcs, client, object_storage = _build_test_object_storage()
    session_factory = _build_session_factory(tmp_path)
    initial_writer = RecordingCompositionWriter(label="Draft")
    rewrite_writer = RecordingCompositionWriter(label="Rewrite")

    try:
        with session_factory() as session:
            seeded = _seed_story_setup_session(session)
            draft_result = StoryWorkflowToolService(session).execute(
                tool_name=StoryWorkflowToolName.COMPOSE_NEXT_SEGMENT,
                session_id=seeded["session_id"],
                arguments={},
            )

        with session_factory() as session:
            draft_service = CompositionJobService(
                session,
                object_storage=object_storage,
                writer=initial_writer,
            )
            for _ in range(3):
                draft_service.run_job(draft_result.composition_job_id)

            rewrite_result = StoryWorkflowToolService(session).execute(
                tool_name=StoryWorkflowToolName.REWRITE_SEGMENTS,
                session_id=seeded["session_id"],
                arguments={
                    "instructions": "Soften the middle chapters and add Pip sooner.",
                    "rewrite_from_segment_index": 2,
                },
            )

        with session_factory() as session:
            rewrite_service = CompositionJobService(
                session,
                object_storage=object_storage,
                writer=rewrite_writer,
            )
            for _ in range(2):
                rewrite_service.run_job(rewrite_result.composition_job_id)
            rewrite_service.reject_rewrite_job(
                seeded["session_id"],
                rewrite_result.composition_job_id,
            )

            snapshot = SessionService(session).load_session_snapshot(seeded["session_id"])
            current_segments = {
                row.segment_index: row
                for row in session.execute(
                    select(CompositionSegment).where(
                        CompositionSegment.session_id == seeded["session_id"],
                        CompositionSegment.acceptance_state
                        == CompositionSegmentAcceptanceState.ACCEPTED,
                        CompositionSegment.superseded_by_segment_id.is_(None),
                    )
                ).scalars()
            }
            rejected_segments = list(
                session.execute(
                    select(CompositionSegment).where(
                        CompositionSegment.composition_job_id == rewrite_result.composition_job_id,
                        CompositionSegment.acceptance_state
                        == CompositionSegmentAcceptanceState.REJECTED,
                    )
                ).scalars()
            )
            rewrite_story_asset = session.execute(
                select(SessionAsset).where(
                    SessionAsset.composition_job_id == rewrite_result.composition_job_id,
                    SessionAsset.asset_kind == AssetKind.STORY_TEXT,
                )
            ).scalar_one_or_none()

        assert snapshot.latest_composition_job is not None
        assert snapshot.latest_composition_job.pending_review is False
        assert _stage_status(snapshot, WorkflowStage.COMPOSITION) == (
            WorkflowStageState.COMPLETED
        )
        assert rewrite_story_asset is None
        assert len(rejected_segments) == 2
        assert current_segments[2].text_content is not None
        assert "Draft segment 2" in current_segments[2].text_content
        assert "Rewrite segment 2" not in current_segments[2].text_content
    finally:
        object_storage.close()
        client.close()


def test_restoring_prior_segment_revision_marks_downstream_segments_stale(
    tmp_path: Path,
) -> None:
    _fake_gcs, client, object_storage = _build_test_object_storage()
    session_factory = _build_session_factory(tmp_path)
    initial_writer = RecordingCompositionWriter(label="Draft")
    rewrite_writer = RecordingCompositionWriter(label="Rewrite")

    try:
        with session_factory() as session:
            seeded = _seed_story_setup_session(session)
            draft_result = StoryWorkflowToolService(session).execute(
                tool_name=StoryWorkflowToolName.COMPOSE_NEXT_SEGMENT,
                session_id=seeded["session_id"],
                arguments={},
            )

        with session_factory() as session:
            draft_service = CompositionJobService(
                session,
                object_storage=object_storage,
                writer=initial_writer,
            )
            for _ in range(3):
                draft_service.run_job(draft_result.composition_job_id)

            original_segment = session.execute(
                select(CompositionSegment).where(
                    CompositionSegment.session_id == seeded["session_id"],
                    CompositionSegment.segment_index == 1,
                    CompositionSegment.acceptance_state
                    == CompositionSegmentAcceptanceState.ACCEPTED,
                    CompositionSegment.superseded_by_segment_id.is_(None),
                )
            ).scalar_one()

            rewrite_result = StoryWorkflowToolService(session).execute(
                tool_name=StoryWorkflowToolName.REWRITE_SEGMENTS,
                session_id=seeded["session_id"],
                arguments={
                    "instructions": "Rewrite the harbor opening with an even quieter promise.",
                    "rewrite_from_segment_index": 1,
                    "rewrite_to_segment_index": 1,
                    "downstream_regeneration_mode": "require_confirmation",
                },
            )

        with session_factory() as session:
            rewrite_service = CompositionJobService(
                session,
                object_storage=object_storage,
                writer=rewrite_writer,
            )
            rewrite_service.run_job(rewrite_result.composition_job_id)
            rewrite_service.accept_rewrite_job(
                seeded["session_id"],
                rewrite_result.composition_job_id,
            )
            rewrite_service.select_active_segment_version(
                seeded["session_id"],
                segment_index=1,
                version_id=original_segment.id,
            )

            snapshot = SessionService(session).load_session_snapshot(seeded["session_id"])
            current_segments = {
                row.segment_index: row
                for row in session.execute(
                    select(CompositionSegment).where(
                        CompositionSegment.session_id == seeded["session_id"],
                        CompositionSegment.acceptance_state
                        == CompositionSegmentAcceptanceState.ACCEPTED,
                        CompositionSegment.superseded_by_segment_id.is_(None),
                    )
                ).scalars()
            }
            latest_story_asset = snapshot.latest_story_asset

        assert snapshot.latest_composition_job is not None
        assert _stage_status(snapshot, WorkflowStage.COMPOSITION) == (
            WorkflowStageState.NEEDS_REGENERATION
        )
        assert current_segments[1].id == original_segment.id
        assert current_segments[2].is_stale is True
        assert current_segments[3].is_stale is True
        assert latest_story_asset is not None
        restored_story_text = object_storage.download_text(
            StorageObjectLocation(
                bucket=latest_story_asset.storage_bucket,
                key=latest_story_asset.object_path,
            )
        )
        assert "Draft segment 1" in restored_story_text
        assert "Rewrite segment 1" not in restored_story_text
    finally:
        object_storage.close()
        client.close()


def test_worker_completes_durable_composition_job_and_persists_story_text_asset(
    tmp_path: Path,
) -> None:
    fake_gcs, client, object_storage = _build_test_object_storage()
    session_factory = _build_session_factory(tmp_path)

    try:
        with session_factory() as session:
            seeded = _seed_story_setup_session(session)
            result = StoryWorkflowToolService(session).execute(
                tool_name=StoryWorkflowToolName.COMPOSE_NEXT_SEGMENT,
                session_id=seeded["session_id"],
                arguments={},
            )

        worker = JobWorker(
            session_factory=session_factory,
            registry=build_default_job_handler_registry(object_storage=object_storage),
            worker_id="composition-worker",
            lease_duration=timedelta(seconds=30),
            poll_interval_seconds=0.01,
        )

        processed_jobs = 0
        while worker.run_once():
            processed_jobs += 1
            assert processed_jobs < 10

        with session_factory() as session:
            composition_job = session.get(CompositionJob, result.composition_job_id)
            story_asset = session.execute(
                select(SessionAsset).where(
                    SessionAsset.composition_job_id == result.composition_job_id,
                    SessionAsset.asset_kind == AssetKind.STORY_TEXT,
                )
            ).scalar_one_or_none()
            segment_assets = list(
                session.execute(
                    select(SessionAsset).where(
                        SessionAsset.composition_job_id == result.composition_job_id,
                        SessionAsset.asset_kind == AssetKind.COMPOSITION_SEGMENT,
                    )
                ).scalars()
            )
            segments = list(
                session.execute(
                    select(CompositionSegment)
                    .where(CompositionSegment.composition_job_id == result.composition_job_id)
                    .order_by(CompositionSegment.segment_index.asc())
                ).scalars()
            )

        assert processed_jobs == 3
        assert composition_job is not None
        assert composition_job.status == JobStatus.COMPLETED
        assert composition_job.progress_percent == 100
        assert len(segments) == 3
        assert all(segment.status == JobStatus.COMPLETED for segment in segments)
        assert all(segment.raw_generated_text for segment in segments)
        assert all(segment.accepted_text for segment in segments)
        assert all(segment.accepted_summary for segment in segments)
        assert len(segment_assets) == 3
        assert all(asset.status == AssetStatus.READY for asset in segment_assets)
        assert story_asset is not None
        assert story_asset.status == AssetStatus.READY
        story_text = object_storage.download_text(
            StorageObjectLocation(
                bucket=story_asset.storage_bucket,
                key=story_asset.object_path,
            )
        )
        assert "Mira" in story_text
        assert "The scene landed in visible calm" in story_text
        assert any(key.endswith("/segments/0001.md") for _, key in fake_gcs.objects)
    finally:
        object_storage.close()
        client.close()


def test_eval_prompt_exposes_story_tool_catalog_for_chat_translation() -> None:
    prompt = render_intent_parser_prompt(
        IntentParserPromptContext(
            session_id="session-123",
            display_title="Moonlit Harbor",
            overall_status=WorkflowStageState.IN_PROGRESS,
            resume_stage=WorkflowStage.BEATS,
            stage_context=IntentParserStageContext(
                current_stage=WorkflowStage.BEATS,
                current_stage_label="Beat sheet",
                current_stage_description=(
                    "Store the accepted Save-the-Cat beat sheet for the session."
                ),
                current_stage_status=WorkflowStageState.IN_PROGRESS,
                current_stage_detail="Refining the midpoint tension.",
            ),
            session_summary="Selected tone: Hushed Wonder",
            user_message="make it shorter and gentler",
        )
    )

    assert "Related backend tool registry" in prompt
    assert '"tool_name": "generate_pitches"' in prompt
    assert '"tool_name": "start_audio_generation"' in prompt


def test_eval_registry_alignment_keeps_worker_and_prompt_catalogs_in_sync() -> None:
    registry = get_story_workflow_tool_registry()
    prompt_catalog_names = {item["tool_name"] for item in registry.build_prompt_catalog()}
    worker_job_types = set(build_default_job_handler_registry().registered_job_types())

    assert prompt_catalog_names == {definition.name.value for definition in registry.list_tools()}
    assert worker_job_types >= {definition.job_type for definition in registry.list_tools()}


def test_eval_background_tool_modes_cover_long_running_story_operations() -> None:
    registry = get_story_workflow_tool_registry()
    background_tools = {
        definition.name
        for definition in registry.list_tools()
        if definition.execution_mode == StoryWorkflowToolExecutionMode.BACKGROUND
    }

    assert background_tools >= {
        StoryWorkflowToolName.GENERATE_PITCHES,
        StoryWorkflowToolName.GENERATE_CHARACTER_SHEETS,
        StoryWorkflowToolName.GENERATE_BEAT_SHEET,
        StoryWorkflowToolName.COMPOSE_NEXT_SEGMENT,
        StoryWorkflowToolName.REWRITE_SEGMENTS,
        StoryWorkflowToolName.START_AUDIO_GENERATION,
    }


def _seed_story_setup_session(
    db_session: Session,
    *,
    composition_status: JobStatus | None = None,
    audio_status: JobStatus | None = None,
    mark_composition_completed: bool = False,
    composition_segment_word_counts: list[int] | None = None,
) -> dict[str, str | None]:
    now = datetime.now(timezone.utc)
    service = SessionService(db_session)
    genre = Genre(
        slug="quest-fantasy",
        label="Quest Fantasy",
        description="A gentle harbor adventure.",
    )
    tone = ToneProfile(
        genre=genre,
        slug="hushed-wonder",
        label="Hushed Wonder",
        description="Soft and luminous.",
    )
    db_session.add_all([genre, tone])
    db_session.flush()

    snapshot = service.create_session(working_title="Moonlit Harbor")
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
        raw_brief="A harbor fox follows a silver clue and returns home calm.",
        normalized_summary="A bedtime harbor mystery with a gentle emotional repair.",
        planning_notes="Keep the midpoint safe and sleepy.",
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
        beats=[
            {
                "key": "opening_image",
                "label": "Opening Image",
                "order": 1,
                "summary": "Mira watches the harbor settle under soft moonlight.",
                "emotional_intent": "Begin in stillness and wonder.",
            },
            {
                "key": "catalyst",
                "label": "Catalyst",
                "order": 2,
                "summary": "A bell buoy drifts away from the dock and asks for help.",
                "emotional_intent": "Introduce a gentle problem.",
            },
            {
                "key": "midpoint",
                "label": "Midpoint",
                "order": 3,
                "summary": "Mira finds the hidden cove where the bell belongs.",
                "emotional_intent": "Lift wonder while keeping the surprise soft.",
                "bedtime_softening_note": "Keep the reveal luminous and quickly reassuring.",
            },
            {
                "key": "all_is_lost",
                "label": "All Is Lost",
                "order": 4,
                "summary": "The bell goes quiet and Mira thinks she has failed.",
                "emotional_intent": "Let the low point feel temporary and held.",
                "bedtime_softening_note": "Buffer the low point with visible companionship.",
            },
            {
                "key": "finale",
                "label": "Finale",
                "order": 5,
                "summary": "The bell returns home and the harbor settles together.",
                "emotional_intent": "Deliver repair and visible calm.",
            },
        ],
        is_selected=True,
        accepted_at=now,
    )
    db_session.add(beat_sheet)
    db_session.flush()

    story_setup = StorySetup(
        session_id=snapshot.id,
        beat_sheet_id=beat_sheet.id,
        revision_number=1,
        target_word_count=1600,
        target_runtime_minutes=11,
        chapter_count=3,
        approximate_scene_count=9,
        chapter_style="three gentle chapters",
        guidance_notes="End each chapter with a calmer image than it began.",
        is_selected=True,
        accepted_at=now,
    )
    db_session.add(story_setup)
    db_session.flush()

    story_outline = StoryOutline(
        session_id=snapshot.id,
        beat_sheet_id=beat_sheet.id,
        story_setup_id=story_setup.id,
        revision_number=1,
        outline_kind="chapter",
        summary="Three draftable chapters mapped from the beat sheet.",
        cards=[
            {
                "card_key": "chapter-1",
                "card_type": "chapter",
                "position": 1,
                "title": "Chapter 1: Opening Image to Catalyst",
                "summary": "Set the moonlit harbor mood and launch Mira after the drifting bell.",
                "beat_keys": ["opening_image", "catalyst"],
                "beat_labels": ["Opening Image", "Catalyst"],
                "emotional_shift": "Move from stillness toward gentle motion.",
                "target_word_count": 533,
                "target_runtime_minutes": 4,
                "target_scene_count": 3,
                "tone_direction": (
                    "Stay anchored in the Hushed Wonder tone while advancing "
                    "the Quest Fantasy lane."
                ),
                "bedtime_guardrail": "Keep the problem small, visible, and quickly reassuring.",
                "drafting_brief": (
                    "Chapter 1 should cover Opening Image and Catalyst while "
                    "staying calm and luminous."
                ),
            },
            {
                "card_key": "chapter-2",
                "card_type": "chapter",
                "position": 2,
                "title": "Chapter 2: Midpoint",
                "summary": "Let Mira discover the hidden cove and feel the bell's meaning open up.",
                "beat_keys": ["midpoint"],
                "beat_labels": ["Midpoint"],
                "emotional_shift": "Lift wonder without breaking the bedtime tone.",
                "target_word_count": 533,
                "target_runtime_minutes": 4,
                "target_scene_count": 3,
                "tone_direction": (
                    "Stay anchored in the Hushed Wonder tone while advancing "
                    "the Quest Fantasy lane."
                ),
                "bedtime_guardrail": "Keep the reveal luminous and quickly reassuring.",
                "drafting_brief": (
                    "Chapter 2 should center the midpoint reveal and make it "
                    "feel awe-filled rather than sharp."
                ),
            },
            {
                "card_key": "chapter-3",
                "card_type": "chapter",
                "position": 3,
                "title": "Chapter 3: All Is Lost to Finale",
                "summary": "Move through the brief low point and guide the harbor back into rest.",
                "beat_keys": ["all_is_lost", "finale"],
                "beat_labels": ["All Is Lost", "Finale"],
                "emotional_shift": "Turn temporary doubt into visible relief and belonging.",
                "target_word_count": 534,
                "target_runtime_minutes": 3,
                "target_scene_count": 3,
                "tone_direction": (
                    "Stay anchored in the Hushed Wonder tone while advancing "
                    "the Quest Fantasy lane."
                ),
                "bedtime_guardrail": "Buffer the low point with visible companionship.",
                "drafting_brief": (
                    "Chapter 3 should keep the low point brief, then land in "
                    "repair and sleepy calm."
                ),
            },
        ],
        metadata_json={
            "genre_label": "Quest Fantasy",
            "tone_label": "Hushed Wonder",
            "target_word_count": 1600,
            "target_runtime_minutes": 11,
            "chapter_count": 3,
            "approximate_scene_count": 9,
            "chapter_style": "three gentle chapters",
            "guidance_notes": "End each chapter with a calmer image than it began.",
        },
        is_selected=True,
        accepted_at=now,
    )
    db_session.add(story_outline)
    db_session.flush()

    composition_job_id: str | None = None
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
            progress_percent=42,
            current_segment_index=2,
            started_at=now,
        )
        db_session.add(composition_job)
        db_session.flush()
        composition_job_id = composition_job.id
    elif mark_composition_completed or composition_segment_word_counts:
        service.update_stage_state(
            snapshot.id,
            stage=WorkflowStage.COMPOSITION,
            status=WorkflowStageState.COMPLETED,
        )
        composition_job = CompositionJob(
            session_id=snapshot.id,
            beat_sheet_id=beat_sheet.id,
            story_setup_id=story_setup.id,
            job_kind=CompositionJobKind.DRAFT,
            status=JobStatus.COMPLETED,
            progress_percent=100,
            current_segment_index=(
                len(composition_segment_word_counts or [])
                if composition_segment_word_counts
                else None
            ),
            started_at=now,
            completed_at=now,
        )
        db_session.add(composition_job)
        db_session.flush()
        composition_job_id = composition_job.id

        for index, word_count in enumerate(composition_segment_word_counts or [], start=1):
            db_session.add(
                CompositionSegment(
                    session_id=snapshot.id,
                    composition_job_id=composition_job.id,
                    segment_index=index,
                    revision_number=1,
                    status=JobStatus.COMPLETED,
                    word_count=word_count,
                    text_content="moonlight " * word_count,
                    completed_at=now,
                )
            )
        db_session.flush()

    audio_job_id: str | None = None
    if audio_status is not None:
        if composition_status is not None:
            service.update_stage_state(
                snapshot.id,
                stage=WorkflowStage.COMPOSITION,
                status=WorkflowStageState.COMPLETED,
            )
        service.update_stage_state(
            snapshot.id,
            stage=WorkflowStage.AUDIO,
            status=WorkflowStageState.IN_PROGRESS,
        )
        audio_job = AudioJob(
            session_id=snapshot.id,
            source_composition_job_id=composition_job_id,
            status=audio_status,
            voice_key="gemini-soft-1",
            playback_speed=1.0,
            include_background_music=False,
            started_at=now,
        )
        db_session.add(audio_job)
        db_session.flush()
        audio_job_id = audio_job.id

    db_session.commit()
    return {
        "session_id": snapshot.id,
        "composition_job_id": composition_job_id,
        "audio_job_id": audio_job_id,
    }


def _stage_status(snapshot, stage: WorkflowStage) -> WorkflowStageState:
    return next(item.status for item in snapshot.stage_states if item.stage == stage)

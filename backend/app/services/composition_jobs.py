from __future__ import annotations

import math
import re
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from time import perf_counter, sleep
from typing import Any, Protocol

from sqlalchemy import Select, select
from sqlalchemy.orm import Session

from app.ai import (
    CompositionSegmentGenerationAdapter,
    GeminiCompositionSegmentGenerationAdapter,
    build_composition_segment_generation_invocation,
)
from app.db import (
    AssetKind,
    AssetStatus,
    BackgroundJob,
    CompositionJob,
    CompositionJobKind,
    CompositionSegment,
    JobStatus,
    SessionAsset,
)
from app.db.base import utc_now
from app.models import (
    COMPOSITION_SEGMENT_GENERATION_PROMPT_VERSION,
    ChatMessageRole,
    CompositionPromptAssemblyInput,
    CompositionSegmentCarryoverContext,
    CompositionSegmentCarryoverItem,
    CompositionSegmentGenerationPromptContext,
    ModelCallOutcome,
    ModelUsageBucket,
    SessionEventActor,
    WorkflowStage,
    WorkflowStageState,
)
from app.services.assets import SessionAssetService
from app.services.composition_prompt_assembly import CompositionPromptAssemblyService
from app.services.composition_streaming import (
    build_accepted_story_so_far,
    split_text_for_streaming,
)
from app.services.event_log import (
    DEFAULT_ASSISTANT_ACTOR,
    DEFAULT_SYSTEM_ACTOR,
    SessionEventLogService,
)
from app.services.jobs import BackgroundJobService
from app.services.model_usage import ModelUsageContext, SessionModelUsageService
from app.services.plan_revisions import PlanRevisionService
from app.services.sessions import SessionService
from app.settings import get_settings
from app.storage import ObjectStorageService, build_object_storage_service

COMPOSITION_RUNTIME_JOB_TYPE = "story.run_composition_job"
_SEGMENT_CHUNK_PARAGRAPHS = 3
_COMPLETION_DETAIL = "Writing finished and the latest draft is ready for review."
_COMPOSITION_SUMMARY_PROGRESS_CHECKPOINTS = (0.34, 0.67)
_COMPOSITION_SUMMARY_FINAL_CHECKPOINT = "segment-complete"
_COMPOSITION_SUMMARY_METADATA_KEY = "emitted_summary_checkpoints"
_SENTENCE_PATTERN = re.compile(r"[^.!?]+[.!?]")


class CompositionJobServiceError(Exception):
    """Base error for durable composition orchestration failures."""


class CompositionJobNotFoundError(CompositionJobServiceError):
    """Raised when a composition job cannot be resolved for a session."""


class CompositionJobStateError(CompositionJobServiceError):
    """Raised when a composition job transition is invalid for the current state."""


@dataclass(frozen=True)
class CompositionJobStartResult:
    job: CompositionJob
    first_segment: CompositionSegment
    total_segments: int


@dataclass(frozen=True)
class CompositionSegmentDraftCriterion:
    name: str
    passed: bool
    measured_value: int | str
    detail: str


@dataclass(frozen=True)
class CompositionSegmentDraftEvaluation:
    passed: bool
    criteria: tuple[CompositionSegmentDraftCriterion, ...]


@dataclass(frozen=True)
class GeneratedCompositionSegmentDraft:
    raw_text: str
    accepted_text: str
    carryover_summary: str
    remaining_chunks: tuple[str, ...]
    evaluation: CompositionSegmentDraftEvaluation
    source: str = "heuristic"
    model_id: str | None = None
    prompt_version: str | None = None
    raw_response: dict[str, Any] | list[Any] | str | None = None


@dataclass(frozen=True)
class CompositionSummaryCheckpoint:
    key: str
    chunk_index: int
    progress_ratio: float


class CompositionSegmentWriter(Protocol):
    def compose_segment(
        self,
        *,
        segment_payload: Mapping[str, Any],
        prior_segments: Sequence[str],
        current_partial_text: str | None,
        total_segments: int,
    ) -> GeneratedCompositionSegmentDraft: ...


class HeuristicCompositionSegmentWriter:
    def compose_segment(
        self,
        *,
        segment_payload: Mapping[str, Any],
        prior_segments: Sequence[str],
        current_partial_text: str | None,
        total_segments: int,
    ) -> GeneratedCompositionSegmentDraft:
        dynamic_context = _read_mapping(
            _read_mapping(segment_payload, "composition_prompt"), "dynamic_context"
        )
        carryover_context = _read_mapping(segment_payload, "context_carryover")
        outline_card = _read_mapping(dynamic_context, "outline_card")
        selected_character_sheet = _read_mapping(dynamic_context, "selected_character_sheet")
        protagonist = _read_mapping(selected_character_sheet, "protagonist")
        supporting_cast = _read_list(selected_character_sheet, "supporting_cast")
        beat_sheet = _read_mapping(dynamic_context, "beat_sheet")
        brief = _read_mapping(dynamic_context, "brief")

        protagonist_name = (
            _read_text(protagonist, "name")
            or _read_text(
                selected_character_sheet,
                "protagonist_name",
            )
            or "The young guide"
        )
        companion_name = None
        if supporting_cast:
            first_support = supporting_cast[0]
            if isinstance(first_support, Mapping):
                companion_name = _read_text(first_support, "name")
        outline_title = (
            _read_text(outline_card, "title")
            or f"Segment {segment_payload.get('segment_index', 1)}"
        )
        outline_summary = (
            _read_text(outline_card, "summary")
            or _read_text(
                segment_payload,
                "outline_card_summary",
            )
            or _read_text(dynamic_context, "segment_goal_summary")
            or "Carry the next soft turn forward."
        )
        drafting_brief = _read_text(outline_card, "drafting_brief") or _read_text(
            segment_payload,
            "outline_card_drafting_brief",
        )
        emotional_shift = (
            _read_text(outline_card, "emotional_shift")
            or _read_text(
                segment_payload,
                "outline_card_emotional_shift",
            )
            or "keep the motion calm and readable"
        )
        bedtime_guardrail = _read_text(outline_card, "bedtime_guardrail")
        genre_label = (
            _read_text(_read_mapping(dynamic_context, "genre"), "label") or "Bedtime Story"
        )
        tone_label = _read_text(_read_mapping(dynamic_context, "tone"), "label") or "Calm"
        story_idea = _read_text(brief, "story_idea") or _read_text(brief, "raw_brief") or ""
        beat_entries = _read_list(beat_sheet, "beats")
        beat_labels = [
            _read_text(entry, "label")
            for entry in beat_entries
            if isinstance(entry, Mapping) and _read_text(entry, "label") is not None
        ]
        beat_label_summary = ", ".join(beat_labels[:2]) if beat_labels else "the next bedtime turn"
        continuity_facts = _read_list(segment_payload, "continuity_facts")
        continuity_detail = None
        if continuity_facts:
            first_fact = continuity_facts[0]
            if isinstance(first_fact, Mapping):
                continuity_detail = _read_text(first_fact, "detail")
        carryover_story_summary = _read_text(carryover_context, "story_so_far_summary")
        prior_story_reference = _read_text(carryover_context, "latest_accepted_summary")
        if prior_story_reference is None and prior_segments:
            prior_story_reference = _extract_last_sentence(prior_segments[-1])

        paragraph_one = (
            f"{protagonist_name} stepped into {outline_title.lower()} carrying the hush of "
            f"{genre_label.lower()} and {tone_label.lower()} with them. {outline_summary} "
            f"{story_idea}".strip()
        )
        paragraph_two_parts = [
            f"The segment needed to hold {beat_label_summary} while {emotional_shift}.",
        ]
        if companion_name is not None:
            paragraph_two_parts.append(
                (
                    f"{companion_name} stayed nearby so every new detail "
                    "felt accompanied instead of sharp."
                )
            )
        if drafting_brief is not None:
            paragraph_two_parts.append(drafting_brief)
        paragraph_two = " ".join(
            part.strip() for part in paragraph_two_parts if part and part.strip()
        )

        paragraph_three_parts = []
        if prior_story_reference is not None:
            paragraph_three_parts.append(
                f"The rhythm carried forward from the earlier pages, where {prior_story_reference}."
            )
        if carryover_story_summary is not None:
            paragraph_three_parts.append(f"Story-so-far focus: {carryover_story_summary}")
        if continuity_detail is not None:
            paragraph_three_parts.append(f"A remembered detail stayed steady: {continuity_detail}")
        if bedtime_guardrail is not None:
            paragraph_three_parts.append(
                (
                    "The ending stayed bedtime-safe by following one clear "
                    f"guardrail: {bedtime_guardrail}"
                )
            )
        paragraph_three_parts.append(
            (
                "The scene landed in visible calm, with the next handoff "
                "feeling gentle enough to keep the night settled."
            )
        )
        paragraph_three = " ".join(
            part.strip().rstrip(".") + "."
            for part in paragraph_three_parts
            if part and part.strip()
        )

        accepted_text = "\n\n".join(
            paragraph.strip()
            for paragraph in (paragraph_one, paragraph_two, paragraph_three)
            if paragraph.strip()
        ).strip()
        raw_text = accepted_text
        carryover_summary = _build_carryover_summary(
            protagonist_name=protagonist_name,
            outline_title=outline_title,
            outline_summary=outline_summary,
            emotional_shift=emotional_shift,
            prior_story_reference=prior_story_reference,
            companion_name=companion_name,
        )
        prefix = current_partial_text or ""
        remaining_text = accepted_text
        if prefix and accepted_text.startswith(prefix):
            remaining_text = accepted_text[len(prefix) :]
        remaining_chunks = tuple(
            chunk for chunk in _split_remaining_text(prefix, remaining_text) if chunk.strip()
        )
        evaluation = evaluate_composition_segment_draft(
            accepted_text,
            protagonist_name=protagonist_name,
            supporting_character_name=companion_name,
            carryover_summary=carryover_summary,
        )
        return GeneratedCompositionSegmentDraft(
            raw_text=raw_text,
            accepted_text=accepted_text,
            carryover_summary=carryover_summary,
            remaining_chunks=remaining_chunks,
            evaluation=evaluation,
        )


class GeminiCompositionSegmentWriter:
    def __init__(
        self,
        *,
        adapter: CompositionSegmentGenerationAdapter | None = None,
        fallback_writer: CompositionSegmentWriter | None = None,
    ) -> None:
        self._adapter = adapter
        self._fallback_writer = fallback_writer or HeuristicCompositionSegmentWriter()

    @classmethod
    def from_settings(cls) -> "GeminiCompositionSegmentWriter":
        settings = get_settings()
        return cls(
            adapter=GeminiCompositionSegmentGenerationAdapter(
                credential=settings.gemini.api_key.get_secret_value(),
                model_id=settings.gemini.composition_model,
            )
        )

    def compose_segment(
        self,
        *,
        segment_payload: Mapping[str, Any],
        prior_segments: Sequence[str],
        current_partial_text: str | None,
        total_segments: int,
    ) -> GeneratedCompositionSegmentDraft:
        prompt_payload = _read_mapping(segment_payload, "composition_prompt")
        carryover_payload = _read_mapping(segment_payload, "context_carryover")
        if not prompt_payload or self._adapter is None:
            return self._fallback_writer.compose_segment(
                segment_payload=segment_payload,
                prior_segments=prior_segments,
                current_partial_text=current_partial_text,
                total_segments=total_segments,
            )

        try:
            prompt_context = CompositionSegmentGenerationPromptContext(
                composition_prompt=prompt_payload,
                carryover=carryover_payload,
            )
            invocation = build_composition_segment_generation_invocation(
                prompt_context,
                model_id=self._adapter.model_id,
            )
            result = self._adapter.generate(invocation)
            structured_output = result.structured_output
            evaluation = evaluate_composition_segment_draft(
                structured_output.accepted_text,
                protagonist_name=_resolve_generation_protagonist_name(prompt_payload),
                supporting_character_name=_resolve_generation_support_name(prompt_payload),
                carryover_summary=structured_output.carryover_summary,
            )
            if not evaluation.passed:
                raise CompositionJobServiceError(
                    _build_validation_failure_reason(evaluation),
                )
            prefix = current_partial_text or ""
            remaining_text = structured_output.accepted_text
            if prefix and structured_output.accepted_text.startswith(prefix):
                remaining_text = structured_output.accepted_text[len(prefix) :]
            remaining_chunks = tuple(
                chunk for chunk in _split_remaining_text(prefix, remaining_text) if chunk.strip()
            )
            return GeneratedCompositionSegmentDraft(
                raw_text=structured_output.raw_text,
                accepted_text=structured_output.accepted_text,
                carryover_summary=structured_output.carryover_summary,
                remaining_chunks=remaining_chunks,
                evaluation=evaluation,
                source="gemini",
                model_id=result.invocation.model_id,
                prompt_version=result.invocation.prompt_version,
                raw_response=result.raw_response,
            )
        except Exception as exc:
            fallback = self._fallback_writer.compose_segment(
                segment_payload=segment_payload,
                prior_segments=prior_segments,
                current_partial_text=current_partial_text,
                total_segments=total_segments,
            )
            return GeneratedCompositionSegmentDraft(
                raw_text=fallback.raw_text,
                accepted_text=fallback.accepted_text,
                carryover_summary=fallback.carryover_summary,
                remaining_chunks=fallback.remaining_chunks,
                evaluation=fallback.evaluation,
                source="heuristic",
                model_id=self._adapter.model_id,
                prompt_version=COMPOSITION_SEGMENT_GENERATION_PROMPT_VERSION,
                raw_response={"fallback_reason": str(exc)},
            )


def evaluate_composition_segment_draft(
    full_text: str,
    *,
    protagonist_name: str,
    supporting_character_name: str | None,
    carryover_summary: str | None = None,
) -> CompositionSegmentDraftEvaluation:
    paragraphs = [paragraph for paragraph in full_text.split("\n\n") if paragraph.strip()]
    lower_text = full_text.lower()
    restful_terms = ("calm", "quiet", "settled", "rest", "soft")
    criteria = (
        CompositionSegmentDraftCriterion(
            name="non_empty_output",
            passed=len(full_text.split()) >= 60,
            measured_value=len(full_text.split()),
            detail="A composed segment should be substantial enough to feel like narrative prose.",
        ),
        CompositionSegmentDraftCriterion(
            name="multiple_paragraphs",
            passed=len(paragraphs) >= _SEGMENT_CHUNK_PARAGRAPHS,
            measured_value=len(paragraphs),
            detail="The durable writer should persist more than one paragraph-sized checkpoint.",
        ),
        CompositionSegmentDraftCriterion(
            name="protagonist_named",
            passed=protagonist_name.lower() in lower_text,
            measured_value=protagonist_name,
            detail="The segment should stay grounded in the selected protagonist.",
        ),
        CompositionSegmentDraftCriterion(
            name="support_visible",
            passed=(
                supporting_character_name is None or supporting_character_name.lower() in lower_text
            ),
            measured_value=supporting_character_name or "n/a",
            detail=(
                "Bedtime composition should keep companionship visible when a "
                "support character exists."
            ),
        ),
        CompositionSegmentDraftCriterion(
            name="restful_close",
            passed=any(term in paragraphs[-1].lower() for term in restful_terms)
            if paragraphs
            else False,
            measured_value=paragraphs[-1] if paragraphs else "",
            detail="The closing paragraph should resolve toward visible calm.",
        ),
        CompositionSegmentDraftCriterion(
            name="carryover_summary_present",
            passed=(
                carryover_summary is None
                or len([part for part in carryover_summary.split() if part.strip()]) >= 12
            ),
            measured_value=carryover_summary or "",
            detail="Each segment should leave a concise durable handoff for the next pass.",
        ),
    )
    return CompositionSegmentDraftEvaluation(
        passed=all(criterion.passed for criterion in criteria),
        criteria=criteria,
    )


class CompositionJobService:
    def __init__(
        self,
        session: Session,
        *,
        chunk_delay_seconds: float = 0.0,
        object_storage: ObjectStorageService | None = None,
        writer: CompositionSegmentWriter | None = None,
    ) -> None:
        self._session = session
        self._sessions = SessionService(session)
        self._events = SessionEventLogService(session)
        self._jobs = BackgroundJobService(session)
        self._plan_revisions = PlanRevisionService(session)
        self._prompt_assembly = CompositionPromptAssemblyService(session)
        self._assets = SessionAssetService(session)
        self._chunk_delay_seconds = max(chunk_delay_seconds, 0.0)
        self._object_storage = object_storage
        self._writer = writer or HeuristicCompositionSegmentWriter()

    def start_job(
        self,
        session_id: str,
        *,
        job_kind: CompositionJobKind,
        start_segment_index: int,
        instructions: str | None = None,
        actor: SessionEventActor | None = None,
        cancel_reason: str,
    ) -> CompositionJobStartResult:
        snapshot = self._sessions.load_session_snapshot(session_id)
        if snapshot.selected_story_setup is None:
            raise CompositionJobStateError("save story setup before starting composition")
        if snapshot.selected_beat_sheet is None:
            raise CompositionJobStateError("accept a beat sheet before starting composition")
        if snapshot.selected_story_outline is None or not snapshot.selected_story_outline.cards:
            raise CompositionJobStateError("save a story outline before starting composition")

        total_outline_segments = len(snapshot.selected_story_outline.cards)
        if start_segment_index > total_outline_segments:
            raise CompositionJobStateError(
                f"segment {start_segment_index} is outside the current outline",
            )

        self.cancel_active_jobs(session_id, reason=cancel_reason, actor=actor)

        plan_revision = self._plan_revisions.ensure_current_revision(
            session_id,
            source_stage=WorkflowStage.STORY_SETUP,
            change_summary=(
                "Captured the current plan for a rewrite pass."
                if job_kind == CompositionJobKind.REWRITE
                else "Captured the current plan for composition."
            ),
        )
        if plan_revision is None:
            raise CompositionJobStateError("composition requires a current plan revision")

        prior_completed_segments = self._latest_completed_segments(
            session_id,
            before_segment_index=start_segment_index,
        )
        prior_story_text = build_accepted_story_so_far(
            [row.accepted_text or row.text_content or "" for row in prior_completed_segments]
        )
        prior_segment_summary = (
            _resolve_segment_summary(prior_completed_segments[-1])
            if prior_completed_segments
            else None
        )
        total_segments = total_outline_segments - start_segment_index + 1
        beat_sheet_id = snapshot.selected_beat_sheet.id
        story_setup_id = snapshot.selected_story_setup.id
        job = CompositionJob(
            session_id=session_id,
            beat_sheet_id=beat_sheet_id,
            story_setup_id=story_setup_id,
            plan_revision_id=plan_revision.id,
            job_kind=job_kind,
            status=JobStatus.QUEUED,
            progress_percent=0,
            current_segment_index=start_segment_index,
            metadata_json={
                "orchestration_version": "composition_job.v1",
                "start_segment_index": start_segment_index,
                "total_segments": total_segments,
                "accepted_story_so_far": prior_story_text,
                "latest_segment_summary": prior_segment_summary,
                "latest_partial_output": None,
                "request_instructions": instructions,
            },
        )
        self._session.add(job)
        self._session.flush()

        first_segment: CompositionSegment | None = None
        current_segment_number = start_segment_index
        while current_segment_number <= total_outline_segments:
            assembled_prompt = self._prompt_assembly.assemble_prompt_package(
                CompositionPromptAssemblyInput(
                    session_id=session_id,
                    job_kind=job_kind.value,
                    segment_index=current_segment_number,
                    instructions=instructions,
                    restart_from_segment_index=(
                        start_segment_index if job_kind == CompositionJobKind.DRAFT else None
                    ),
                    rewrite_from_segment_index=(
                        start_segment_index if job_kind == CompositionJobKind.REWRITE else None
                    ),
                )
            )
            segment_payload = {
                "job_kind": job_kind.value,
                "request_instructions": instructions,
                **assembled_prompt.build_storage_payload(),
            }
            segment = CompositionSegment(
                session_id=session_id,
                composition_job_id=job.id,
                segment_index=current_segment_number,
                revision_number=self._next_segment_revision(session_id, current_segment_number),
                status=JobStatus.QUEUED,
                planned_summary=assembled_prompt.dynamic_context.segment_goal_summary,
                payload=segment_payload,
            )
            self._session.add(segment)
            self._session.flush()
            if first_segment is None:
                first_segment = segment
                job.metadata_json = {
                    **_read_metadata(job),
                    **segment_payload,
                    "current_segment_id": first_segment.id,
                }
            current_segment_number += 1

        assert first_segment is not None
        self._events.record_composition_progress(
            session_id,
            job_id=job.id,
            status=JobStatus.QUEUED,
            progress_percent=0,
            current_segment_index=start_segment_index,
            total_segments=total_segments,
            segment_id=first_segment.id,
            actor=actor or DEFAULT_SYSTEM_ACTOR,
        )
        self._enqueue_runtime_job(job.session_id, job.id)
        self._session.refresh(job)
        self._session.refresh(first_segment)
        return CompositionJobStartResult(
            job=job,
            first_segment=first_segment,
            total_segments=total_segments,
        )

    def resolve_continue_start_segment(self, session_id: str) -> int:
        snapshot = self._sessions.load_session_snapshot(session_id)
        if snapshot.selected_story_outline is None or not snapshot.selected_story_outline.cards:
            raise CompositionJobStateError("save a story outline before continuing composition")

        active_job = snapshot.active_composition_job
        if active_job is not None and active_job.current_segment_index is not None:
            return active_job.current_segment_index

        stmt = (
            select(CompositionSegment)
            .where(
                CompositionSegment.session_id == session_id,
                CompositionSegment.status == JobStatus.COMPLETED,
            )
            .order_by(
                CompositionSegment.segment_index.desc(), CompositionSegment.revision_number.desc()
            )
            .limit(1)
        )
        latest_completed = self._session.execute(stmt).scalar_one_or_none()
        if latest_completed is None:
            return 1

        next_index = latest_completed.segment_index + 1
        total_outline_segments = len(snapshot.selected_story_outline.cards)
        return min(next_index, total_outline_segments)

    def pause_job(
        self,
        session_id: str,
        composition_job_id: str,
        *,
        actor: SessionEventActor | None = None,
    ) -> CompositionJob:
        job = self._require_job(session_id, composition_job_id)
        if job.status not in {JobStatus.QUEUED, JobStatus.IN_PROGRESS}:
            raise CompositionJobStateError(
                f"composition job {composition_job_id!r} cannot be paused from {job.status.value}",
            )

        current_segment = self._current_segment(job)
        job.status = JobStatus.PAUSED
        if current_segment is not None and current_segment.status in {
            JobStatus.QUEUED,
            JobStatus.IN_PROGRESS,
        }:
            current_segment.status = JobStatus.PAUSED
        self._events.record_composition_progress(
            session_id,
            job_id=job.id,
            status=JobStatus.PAUSED,
            progress_percent=job.progress_percent,
            current_segment_index=job.current_segment_index,
            total_segments=_read_total_segments(job),
            segment_id=current_segment.id if current_segment is not None else None,
            actor=actor or DEFAULT_SYSTEM_ACTOR,
        )
        self._sessions.update_stage_state(
            session_id,
            stage=WorkflowStage.COMPOSITION,
            status=WorkflowStageState.IN_PROGRESS,
            detail=f"Writing paused at {round(job.progress_percent)}% complete.",
            actor=actor or DEFAULT_SYSTEM_ACTOR,
        )
        self._session.commit()
        return job

    def resume_job(
        self,
        session_id: str,
        composition_job_id: str,
        *,
        actor: SessionEventActor | None = None,
    ) -> CompositionJob:
        job = self._require_job(session_id, composition_job_id)
        if job.status != JobStatus.PAUSED:
            raise CompositionJobStateError(
                f"composition job {composition_job_id!r} can only resume from paused",
            )

        current_segment = self._current_segment(job)
        job.status = JobStatus.QUEUED
        job.stop_reason = None
        if current_segment is not None and current_segment.status == JobStatus.PAUSED:
            current_segment.status = JobStatus.QUEUED
        self._events.record_composition_progress(
            session_id,
            job_id=job.id,
            status=JobStatus.QUEUED,
            progress_percent=job.progress_percent,
            current_segment_index=job.current_segment_index,
            total_segments=_read_total_segments(job),
            segment_id=current_segment.id if current_segment is not None else None,
            actor=actor or DEFAULT_SYSTEM_ACTOR,
        )
        self._sessions.update_stage_state(
            session_id,
            stage=WorkflowStage.COMPOSITION,
            status=WorkflowStageState.IN_PROGRESS,
            detail=(
                f"Queued writing to resume at segment {job.current_segment_index} of "
                f"{_read_total_segments(job)}."
            ),
            actor=actor or DEFAULT_SYSTEM_ACTOR,
        )
        self._enqueue_runtime_job(job.session_id, job.id)
        self._session.refresh(job)
        return job

    def cancel_job(
        self,
        session_id: str,
        composition_job_id: str,
        *,
        reason: str,
        actor: SessionEventActor | None = None,
    ) -> CompositionJob:
        job = self._require_job(session_id, composition_job_id)
        if job.status in {JobStatus.COMPLETED, JobStatus.CANCELLED, JobStatus.FAILED}:
            raise CompositionJobStateError(
                "composition job "
                f"{composition_job_id!r} cannot be cancelled from {job.status.value}",
            )

        self._cancel_job_rows(job, reason=reason)
        current_segment = self._current_segment(job)
        self._events.record_composition_progress(
            session_id,
            job_id=job.id,
            status=JobStatus.CANCELLED,
            progress_percent=job.progress_percent,
            current_segment_index=job.current_segment_index,
            total_segments=_read_total_segments(job),
            segment_id=current_segment.id if current_segment is not None else None,
            actor=actor or DEFAULT_SYSTEM_ACTOR,
        )
        self._sessions.update_stage_state(
            session_id,
            stage=WorkflowStage.COMPOSITION,
            status=WorkflowStageState.NEEDS_REGENERATION,
            detail=reason,
            actor=actor or DEFAULT_SYSTEM_ACTOR,
        )
        self._session.commit()
        return job

    def cancel_active_jobs(
        self,
        session_id: str,
        *,
        reason: str,
        actor: SessionEventActor | None = None,
    ) -> None:
        stmt = select(CompositionJob).where(
            CompositionJob.session_id == session_id,
            CompositionJob.status.in_((JobStatus.QUEUED, JobStatus.IN_PROGRESS, JobStatus.PAUSED)),
        )
        rows = list(self._session.execute(stmt).scalars().all())
        if not rows:
            return

        for row in rows:
            self._cancel_job_rows(row, reason=reason)
            current_segment = self._current_segment(row)
            self._events.record_composition_progress(
                session_id,
                job_id=row.id,
                status=JobStatus.CANCELLED,
                progress_percent=row.progress_percent,
                current_segment_index=row.current_segment_index,
                total_segments=_read_total_segments(row),
                segment_id=current_segment.id if current_segment is not None else None,
                actor=actor or DEFAULT_SYSTEM_ACTOR,
            )
        self._session.flush()

    def run_job(
        self,
        composition_job_id: str,
        *,
        actor: SessionEventActor | None = None,
    ) -> dict[str, Any]:
        job = self._session.get(CompositionJob, composition_job_id)
        if job is None:
            raise CompositionJobNotFoundError(
                f"composition job {composition_job_id!r} was not found",
            )

        total_segments = _read_total_segments(job)
        current_segment = self._current_segment(job)
        if current_segment is None:
            raise CompositionJobStateError(
                f"composition job {composition_job_id!r} does not have a current segment",
            )

        if job.status == JobStatus.CANCELLED:
            return {
                "composition_job_id": job.id,
                "status": job.status.value,
                "action": "noop_cancelled",
            }
        if job.status == JobStatus.PAUSED:
            return {
                "composition_job_id": job.id,
                "status": job.status.value,
                "action": "noop_paused",
            }
        if job.status == JobStatus.COMPLETED:
            return {
                "composition_job_id": job.id,
                "status": job.status.value,
                "action": "noop_completed",
            }

        job.status = JobStatus.IN_PROGRESS
        job.started_at = job.started_at or utc_now()
        current_segment.status = JobStatus.IN_PROGRESS
        job.metadata_json = {
            **_read_metadata(job),
            "current_segment_id": current_segment.id,
        }
        self._events.record_composition_progress(
            job.session_id,
            job_id=job.id,
            status=JobStatus.IN_PROGRESS,
            progress_percent=job.progress_percent,
            current_segment_index=current_segment.segment_index,
            total_segments=total_segments,
            segment_id=current_segment.id,
            actor=actor or DEFAULT_SYSTEM_ACTOR,
        )
        self._sessions.update_stage_state(
            job.session_id,
            stage=WorkflowStage.COMPOSITION,
            status=WorkflowStageState.IN_PROGRESS,
            detail=_build_segment_stage_detail(
                current_segment.segment_index,
                total_segments,
                current_segment.planned_summary,
            ),
            actor=actor or DEFAULT_SYSTEM_ACTOR,
        )

        refreshed_payload = self._refresh_runtime_segment_payload(
            job=job,
            segment=current_segment,
        )
        job.metadata_json = {
            **_read_metadata(job),
            **_read_job_prompt_metadata(refreshed_payload),
            "current_segment_id": current_segment.id,
        }
        completed_segments = self._latest_completed_segment_texts(
            job.session_id,
            before_segment_index=current_segment.segment_index,
        )
        job.metadata_json = {
            **_read_metadata(job),
            "accepted_story_so_far": build_accepted_story_so_far(completed_segments),
        }
        draft_started_at = perf_counter()
        draft = self._writer.compose_segment(
            segment_payload=refreshed_payload,
            prior_segments=completed_segments,
            current_partial_text=current_segment.accepted_text or current_segment.text_content,
            total_segments=total_segments,
        )
        self._record_segment_model_usage(
            session_id=job.session_id,
            draft=draft,
            elapsed_ms=max(round((perf_counter() - draft_started_at) * 1000), 0),
        )
        current_segment.raw_generated_text = draft.raw_text
        current_segment.accepted_summary = draft.carryover_summary
        segment_storage_location = self._storage().paths.partial_draft_segment(
            session_id=job.session_id,
            job_id=job.id,
            segment_index=current_segment.segment_index,
        )

        chunk_count = max(len(draft.remaining_chunks), 1)
        summary_checkpoints = {
            checkpoint.chunk_index: checkpoint
            for checkpoint in _plan_composition_summary_checkpoints(chunk_count)
        }
        current_text = current_segment.accepted_text or current_segment.text_content or ""
        chunk_index = 0
        for chunk in draft.remaining_chunks:
            current_text += chunk
            current_segment.accepted_text = current_text
            current_segment.text_content = current_text
            current_segment.word_count = _count_words(current_text)
            job.progress_percent = _segment_progress_percent(
                job=job,
                total_segments=total_segments,
                chunk_position=chunk_index + 1,
                total_chunks=chunk_count,
            )
            job.metadata_json = {
                **_read_metadata(job),
                "accepted_story_so_far": build_accepted_story_so_far(
                    completed_segments,
                    current_text,
                ),
                "latest_partial_output": current_text,
                "current_segment_id": current_segment.id,
            }
            self._storage().upload_text(
                segment_storage_location,
                current_text,
                content_type="text/markdown; charset=utf-8",
            )
            checkpoint = summary_checkpoints.get(chunk_index + 1)
            if checkpoint is not None:
                self._record_composition_summary_checkpoint(
                    job=job,
                    segment=current_segment,
                    total_segments=total_segments,
                    current_text=current_text,
                    segment_payload=refreshed_payload,
                    progress_percent=job.progress_percent,
                    checkpoint_key=checkpoint.key,
                )
            self._events.record_composition_progress(
                job.session_id,
                job_id=job.id,
                status=JobStatus.IN_PROGRESS,
                progress_percent=job.progress_percent,
                current_segment_index=current_segment.segment_index,
                total_segments=total_segments,
                segment_id=current_segment.id,
                actor=actor or DEFAULT_SYSTEM_ACTOR,
            )
            self._session.commit()
            chunk_index += 1

            self._session.refresh(job)
            self._session.refresh(current_segment)
            if job.status == JobStatus.PAUSED:
                current_segment.status = JobStatus.PAUSED
                self._events.record_composition_progress(
                    job.session_id,
                    job_id=job.id,
                    status=JobStatus.PAUSED,
                    progress_percent=job.progress_percent,
                    current_segment_index=current_segment.segment_index,
                    total_segments=total_segments,
                    segment_id=current_segment.id,
                    actor=actor or DEFAULT_SYSTEM_ACTOR,
                )
                self._sessions.update_stage_state(
                    job.session_id,
                    stage=WorkflowStage.COMPOSITION,
                    status=WorkflowStageState.IN_PROGRESS,
                    detail=f"Writing paused at {round(job.progress_percent)}% complete.",
                    actor=actor or DEFAULT_SYSTEM_ACTOR,
                )
                return {
                    "composition_job_id": job.id,
                    "status": job.status.value,
                    "action": "paused",
                }
            if job.status == JobStatus.CANCELLED:
                current_segment.status = JobStatus.CANCELLED
                self._events.record_composition_progress(
                    job.session_id,
                    job_id=job.id,
                    status=JobStatus.CANCELLED,
                    progress_percent=job.progress_percent,
                    current_segment_index=current_segment.segment_index,
                    total_segments=total_segments,
                    segment_id=current_segment.id,
                    actor=actor or DEFAULT_SYSTEM_ACTOR,
                )
                self._sessions.update_stage_state(
                    job.session_id,
                    stage=WorkflowStage.COMPOSITION,
                    status=WorkflowStageState.NEEDS_REGENERATION,
                    detail=job.stop_reason or "Writing was cancelled before the draft finished.",
                    actor=actor or DEFAULT_SYSTEM_ACTOR,
                )
                return {
                    "composition_job_id": job.id,
                    "status": job.status.value,
                    "action": "cancelled",
                }

            if self._chunk_delay_seconds > 0 and chunk_index < chunk_count:
                sleep(self._chunk_delay_seconds)

        current_segment.accepted_text = draft.accepted_text
        current_segment.text_content = draft.accepted_text
        current_segment.word_count = _count_words(draft.accepted_text)
        current_segment.status = JobStatus.COMPLETED
        current_segment.completed_at = utc_now()
        self._record_composition_summary_checkpoint(
            job=job,
            segment=current_segment,
            total_segments=total_segments,
            current_text=draft.accepted_text,
            segment_payload=refreshed_payload,
            progress_percent=job.progress_percent,
            checkpoint_key=_COMPOSITION_SUMMARY_FINAL_CHECKPOINT,
        )
        self._storage().upload_text(
            segment_storage_location,
            draft.accepted_text,
            content_type="text/markdown; charset=utf-8",
        )
        self._replace_prior_segment_revision(current_segment)
        self._save_segment_asset(
            job=job,
            segment=current_segment,
            storage_location=segment_storage_location,
            draft=draft,
        )

        next_segment = self._next_queued_segment(
            job, after_segment_index=current_segment.segment_index
        )
        if next_segment is None:
            story_text = self._compile_story_text(job.session_id)
            story_location = _story_text_location(
                self._storage(), session_id=job.session_id, job_id=job.id
            )
            story_metadata = self._storage().upload_text(
                story_location,
                story_text,
                content_type="text/markdown; charset=utf-8",
            )
            self._supersede_story_assets(job.session_id)
            self._assets.save_asset_record(
                session_id=job.session_id,
                asset_kind=AssetKind.STORY_TEXT,
                storage_bucket=story_location.bucket,
                object_path=story_location.key,
                mime_type="text/markdown",
                status=AssetStatus.READY,
                composition_job_id=job.id,
                segment_index=current_segment.segment_index,
                byte_size=story_metadata.size_bytes,
                metadata_json={
                    "orchestration_version": "composition_job.v1",
                    "generation_source": draft.source,
                    "final_segment_summary": current_segment.accepted_summary,
                    "evaluation": [
                        {
                            "name": criterion.name,
                            "passed": criterion.passed,
                            "measured_value": criterion.measured_value,
                            "detail": criterion.detail,
                        }
                        for criterion in draft.evaluation.criteria
                    ],
                },
            )
            job.status = JobStatus.COMPLETED
            job.progress_percent = 100
            job.completed_at = utc_now()
            job.metadata_json = {
                **_read_metadata(job),
                "accepted_story_so_far": story_text,
                "latest_segment_summary": current_segment.accepted_summary,
                "latest_partial_output": story_text,
                "current_segment_id": current_segment.id,
            }
            self._events.record_composition_progress(
                job.session_id,
                job_id=job.id,
                status=JobStatus.COMPLETED,
                progress_percent=100,
                current_segment_index=current_segment.segment_index,
                total_segments=total_segments,
                segment_id=current_segment.id,
                actor=actor or DEFAULT_SYSTEM_ACTOR,
            )
            self._sessions.update_stage_state(
                job.session_id,
                stage=WorkflowStage.COMPOSITION,
                status=WorkflowStageState.COMPLETED,
                detail=_COMPLETION_DETAIL,
                actor=actor or DEFAULT_SYSTEM_ACTOR,
            )
            return {
                "composition_job_id": job.id,
                "status": job.status.value,
                "action": "completed",
                "story_asset_path": story_location.key,
            }

        job.status = JobStatus.QUEUED
        job.current_segment_index = next_segment.segment_index
        job.progress_percent = _completed_segment_progress_percent(
            job=job,
            total_segments=total_segments,
            latest_completed_segment_index=current_segment.segment_index,
        )
        job.metadata_json = {
            **_read_metadata(job),
            "accepted_story_so_far": build_accepted_story_so_far(
                completed_segments,
                current_segment.accepted_text,
            ),
            "latest_segment_summary": current_segment.accepted_summary,
            **_read_job_prompt_metadata(_read_mapping(next_segment.payload)),
            "latest_partial_output": current_segment.accepted_text,
            "current_segment_id": next_segment.id,
        }
        self._events.record_composition_progress(
            job.session_id,
            job_id=job.id,
            status=JobStatus.QUEUED,
            progress_percent=job.progress_percent,
            current_segment_index=next_segment.segment_index,
            total_segments=total_segments,
            segment_id=next_segment.id,
            actor=actor or DEFAULT_SYSTEM_ACTOR,
        )
        self._enqueue_runtime_job(job.session_id, job.id)
        return {
            "composition_job_id": job.id,
            "status": job.status.value,
            "action": "queued_next_segment",
            "next_segment_index": next_segment.segment_index,
        }

    def mark_job_failed(
        self,
        composition_job_id: str,
        *,
        error_message: str,
        actor: SessionEventActor | None = None,
    ) -> CompositionJob:
        job = self._session.get(CompositionJob, composition_job_id)
        if job is None:
            raise CompositionJobNotFoundError(
                f"composition job {composition_job_id!r} was not found",
            )

        current_segment = self._current_segment(job)
        job.status = JobStatus.FAILED
        job.error_message = error_message.strip()
        job.completed_at = None
        if current_segment is not None and current_segment.status == JobStatus.IN_PROGRESS:
            current_segment.status = JobStatus.FAILED
        self._events.record_composition_progress(
            job.session_id,
            job_id=job.id,
            status=JobStatus.FAILED,
            progress_percent=job.progress_percent,
            current_segment_index=job.current_segment_index,
            total_segments=_read_total_segments(job),
            segment_id=current_segment.id if current_segment is not None else None,
            actor=actor or DEFAULT_SYSTEM_ACTOR,
        )
        self._sessions.update_stage_state(
            job.session_id,
            stage=WorkflowStage.COMPOSITION,
            status=WorkflowStageState.NEEDS_REGENERATION,
            detail=job.error_message,
            actor=actor or DEFAULT_SYSTEM_ACTOR,
        )
        return job

    def _record_composition_summary_checkpoint(
        self,
        *,
        job: CompositionJob,
        segment: CompositionSegment,
        total_segments: int,
        current_text: str,
        segment_payload: Mapping[str, Any],
        progress_percent: float | None,
        checkpoint_key: str,
    ) -> None:
        if _has_emitted_summary_checkpoint(job, segment.id, checkpoint_key):
            return

        summary_message = _build_composition_summary_message(
            segment_index=segment.segment_index,
            total_segments=total_segments,
            current_text=current_text,
            segment_payload=segment_payload,
            planned_summary=segment.planned_summary,
            progress_percent=progress_percent,
            checkpoint_key=checkpoint_key,
        )
        if summary_message is None:
            return

        self._events.record_chat_message(
            job.session_id,
            message_role=ChatMessageRole.ASSISTANT,
            content=summary_message,
            stage=WorkflowStage.COMPOSITION,
            message_id=_build_composition_summary_message_id(
                job_id=job.id,
                segment_id=segment.id,
                checkpoint_key=checkpoint_key,
            ),
            source="composition_summary",
            actor=DEFAULT_ASSISTANT_ACTOR,
        )
        _mark_summary_checkpoint_emitted(job, segment.id, checkpoint_key)

    def _require_job(self, session_id: str, composition_job_id: str) -> CompositionJob:
        job = self._session.get(CompositionJob, composition_job_id)
        if job is None or job.session_id != session_id:
            raise CompositionJobNotFoundError(
                f"composition job {composition_job_id!r} does not belong to session {session_id!r}",
            )
        return job

    def _current_segment(self, job: CompositionJob) -> CompositionSegment | None:
        if job.current_segment_index is None:
            return None
        stmt: Select[tuple[CompositionSegment]] = (
            select(CompositionSegment)
            .where(
                CompositionSegment.composition_job_id == job.id,
                CompositionSegment.segment_index == job.current_segment_index,
            )
            .order_by(CompositionSegment.revision_number.desc())
            .limit(1)
        )
        return self._session.execute(stmt).scalar_one_or_none()

    def _next_queued_segment(
        self,
        job: CompositionJob,
        *,
        after_segment_index: int,
    ) -> CompositionSegment | None:
        stmt: Select[tuple[CompositionSegment]] = (
            select(CompositionSegment)
            .where(
                CompositionSegment.composition_job_id == job.id,
                CompositionSegment.segment_index > after_segment_index,
                CompositionSegment.status == JobStatus.QUEUED,
            )
            .order_by(CompositionSegment.segment_index.asc())
            .limit(1)
        )
        return self._session.execute(stmt).scalar_one_or_none()

    def _refresh_runtime_segment_payload(
        self,
        *,
        job: CompositionJob,
        segment: CompositionSegment,
    ) -> dict[str, Any]:
        existing_payload = _read_mapping(segment.payload)
        prompt_package = self._prompt_assembly.assemble_prompt_package(
            CompositionPromptAssemblyInput(
                session_id=job.session_id,
                job_kind=job.job_kind.value,
                segment_index=segment.segment_index,
                instructions=_read_optional_prompt_text(
                    _read_metadata(job), "request_instructions"
                ),
                restart_from_segment_index=(
                    _read_start_segment_index(job)
                    if job.job_kind == CompositionJobKind.DRAFT
                    else None
                ),
                rewrite_from_segment_index=(
                    _read_start_segment_index(job)
                    if job.job_kind == CompositionJobKind.REWRITE
                    else None
                ),
            )
        )
        carryover = self._build_context_carryover(
            session_id=job.session_id,
            before_segment_index=segment.segment_index,
        )
        payload = {
            **existing_payload,
            "job_kind": job.job_kind.value,
            "request_instructions": _read_optional_prompt_text(
                _read_metadata(job), "request_instructions"
            ),
            **prompt_package.build_storage_payload(),
            "context_carryover": carryover.model_dump(mode="json"),
        }
        segment.payload = payload
        segment.planned_summary = prompt_package.dynamic_context.segment_goal_summary
        return payload

    def _build_context_carryover(
        self,
        *,
        session_id: str,
        before_segment_index: int,
    ) -> CompositionSegmentCarryoverContext:
        prior_segments = self._latest_completed_segments(
            session_id,
            before_segment_index=before_segment_index,
        )
        carryover_items: list[CompositionSegmentCarryoverItem] = []
        for row in prior_segments:
            summary = _resolve_segment_summary(row)
            if summary is None:
                continue
            payload = _read_mapping(row.payload)
            carryover_items.append(
                CompositionSegmentCarryoverItem(
                    segment_index=row.segment_index,
                    outline_card_title=_read_optional_prompt_text(payload, "outline_card_title"),
                    accepted_summary=summary,
                    accepted_word_count=row.word_count,
                )
            )

        story_so_far_summary = _build_story_so_far_summary(carryover_items)
        latest_summary = carryover_items[-1].accepted_summary if carryover_items else None
        return CompositionSegmentCarryoverContext(
            prior_segment_count=len(carryover_items),
            story_so_far_summary=story_so_far_summary,
            latest_accepted_summary=latest_summary,
            prior_segments=carryover_items,
        )

    def _latest_completed_segment_texts(
        self,
        session_id: str,
        *,
        before_segment_index: int | None = None,
    ) -> list[str]:
        rows = self._latest_completed_segments(
            session_id,
            before_segment_index=before_segment_index,
        )
        return [
            row.accepted_text or row.text_content
            for row in rows
            if row.accepted_text or row.text_content
        ]

    def _latest_completed_segments(
        self,
        session_id: str,
        *,
        before_segment_index: int | None = None,
    ) -> list[CompositionSegment]:
        stmt: Select[tuple[CompositionSegment]] = (
            select(CompositionSegment)
            .where(CompositionSegment.session_id == session_id)
            .order_by(
                CompositionSegment.segment_index.asc(),
                CompositionSegment.revision_number.desc(),
            )
        )
        if before_segment_index is not None:
            stmt = stmt.where(CompositionSegment.segment_index < before_segment_index)
        rows = list(self._session.execute(stmt).scalars().all())
        latest_by_segment: dict[int, CompositionSegment] = {}
        for row in rows:
            if row.segment_index in latest_by_segment:
                continue
            if row.status != JobStatus.COMPLETED and row.completed_at is None:
                continue
            if row.accepted_text is None and row.text_content is None:
                continue
            latest_by_segment[row.segment_index] = row
        return [latest_by_segment[index] for index in sorted(latest_by_segment)]

    def _compile_story_text(self, session_id: str) -> str:
        completed_segments = self._latest_completed_segment_texts(session_id)
        compiled_text = build_accepted_story_so_far(completed_segments)
        if compiled_text is None:
            raise CompositionJobStateError(
                "cannot finalize a composition job without completed text"
            )
        return compiled_text

    def _replace_prior_segment_revision(self, segment: CompositionSegment) -> None:
        stmt = select(CompositionSegment).where(
            CompositionSegment.session_id == segment.session_id,
            CompositionSegment.segment_index == segment.segment_index,
            CompositionSegment.id != segment.id,
            CompositionSegment.superseded_by_segment_id.is_(None),
        )
        for row in self._session.execute(stmt).scalars().all():
            row.superseded_by_segment_id = segment.id

    def _save_segment_asset(
        self,
        *,
        job: CompositionJob,
        segment: CompositionSegment,
        storage_location,
        draft: GeneratedCompositionSegmentDraft,
    ) -> None:
        object_metadata = self._storage().fetch_object_metadata(storage_location)
        self._supersede_segment_assets(job.session_id, segment.segment_index)
        self._assets.save_asset_record(
            session_id=job.session_id,
            asset_kind=AssetKind.COMPOSITION_SEGMENT,
            storage_bucket=storage_location.bucket,
            object_path=storage_location.key,
            mime_type="text/markdown",
            status=AssetStatus.READY,
            composition_job_id=job.id,
            composition_segment_id=segment.id,
            segment_index=segment.segment_index,
            byte_size=object_metadata.size_bytes,
            metadata_json={
                "orchestration_version": "composition_job.v1",
                "generation_source": draft.source,
                "carryover_summary": segment.accepted_summary,
                "evaluation": [
                    {
                        "name": criterion.name,
                        "passed": criterion.passed,
                        "measured_value": criterion.measured_value,
                        "detail": criterion.detail,
                    }
                    for criterion in draft.evaluation.criteria
                ],
            },
        )

    def _record_segment_model_usage(
        self,
        *,
        session_id: str,
        draft: GeneratedCompositionSegmentDraft,
        elapsed_ms: int,
    ) -> None:
        if draft.model_id is None:
            return

        SessionModelUsageService(self._session).record_model_call(
            context=ModelUsageContext(
                session_id=session_id,
                usage_bucket=ModelUsageBucket.COMPOSITION,
                workflow_stage=WorkflowStage.COMPOSITION,
                purpose="segmented_composition_segment",
                model_id=draft.model_id,
                prompt_version=draft.prompt_version,
            ),
            elapsed_ms=elapsed_ms,
            outcome=_resolve_model_usage_outcome(
                source=draft.source,
                raw_response=draft.raw_response,
            ),
            raw_response=draft.raw_response,
            error_message=_extract_model_usage_error_message(draft.raw_response),
        )

    def _supersede_segment_assets(self, session_id: str, segment_index: int) -> None:
        stmt = select(SessionAsset).where(
            SessionAsset.session_id == session_id,
            SessionAsset.asset_kind == AssetKind.COMPOSITION_SEGMENT,
            SessionAsset.segment_index == segment_index,
            SessionAsset.status == AssetStatus.READY,
        )
        for asset in self._session.execute(stmt).scalars().all():
            asset.status = AssetStatus.SUPERSEDED
            asset.superseded_at = utc_now()

    def _next_segment_revision(self, session_id: str, segment_index: int) -> int:
        stmt = (
            select(CompositionSegment)
            .where(
                CompositionSegment.session_id == session_id,
                CompositionSegment.segment_index == segment_index,
            )
            .order_by(CompositionSegment.revision_number.desc())
            .limit(1)
        )
        row = self._session.execute(stmt).scalar_one_or_none()
        return (row.revision_number if row is not None else 0) + 1

    def _cancel_job_rows(self, job: CompositionJob, *, reason: str) -> None:
        normalized_reason = reason.strip()
        if not normalized_reason:
            raise ValueError("cancel reason must not be empty")

        job.status = JobStatus.CANCELLED
        job.stop_reason = normalized_reason
        job.completed_at = job.completed_at or utc_now()
        for segment in job.segments:
            if segment.status in {JobStatus.QUEUED, JobStatus.IN_PROGRESS, JobStatus.PAUSED}:
                segment.status = JobStatus.CANCELLED

    def _supersede_story_assets(self, session_id: str) -> None:
        stmt = select(SessionAsset).where(
            SessionAsset.session_id == session_id,
            SessionAsset.asset_kind == AssetKind.STORY_TEXT,
            SessionAsset.status == AssetStatus.READY,
        )
        for asset in self._session.execute(stmt).scalars().all():
            asset.status = AssetStatus.SUPERSEDED
            asset.superseded_at = utc_now()

    def _enqueue_runtime_job(self, session_id: str, composition_job_id: str) -> None:
        if self._has_pending_runtime_job(composition_job_id):
            return
        self._jobs.enqueue_job(
            job_type=COMPOSITION_RUNTIME_JOB_TYPE,
            payload={"composition_job_id": composition_job_id},
            session_id=session_id,
        )

    def _has_pending_runtime_job(self, composition_job_id: str) -> bool:
        stmt = select(BackgroundJob).where(
            BackgroundJob.job_type == COMPOSITION_RUNTIME_JOB_TYPE,
            BackgroundJob.status == JobStatus.QUEUED,
        )
        for row in self._session.execute(stmt).scalars().all():
            payload = row.payload if isinstance(row.payload, Mapping) else {}
            if payload.get("composition_job_id") == composition_job_id:
                return True
        return False

    def _storage(self) -> ObjectStorageService:
        if self._object_storage is None:
            self._object_storage = build_object_storage_service(get_settings())
        return self._object_storage


def _build_segment_stage_detail(
    segment_index: int,
    total_segments: int,
    planned_summary: str | None,
) -> str:
    summary = planned_summary.strip() if planned_summary else None
    if summary:
        return f"Composing segment {segment_index} of {total_segments}. {summary}"
    return f"Composing segment {segment_index} of {total_segments}."


def _story_text_location(
    storage: ObjectStorageService,
    *,
    session_id: str,
    job_id: str,
):
    return storage.paths.debug_artifact(
        session_id=session_id,
        artifact_group="composition/final",
        artifact_name=f"{job_id}-story",
        extension="md",
    )


def _segment_progress_percent(
    *,
    job: CompositionJob,
    total_segments: int,
    chunk_position: int,
    total_chunks: int,
) -> float:
    start_index = _read_start_segment_index(job)
    completed_segments = max((job.current_segment_index or start_index) - start_index, 0)
    return round(
        ((completed_segments + (chunk_position / max(total_chunks, 1))) / max(total_segments, 1))
        * 100,
        2,
    )


def _completed_segment_progress_percent(
    *,
    job: CompositionJob,
    total_segments: int,
    latest_completed_segment_index: int,
) -> float:
    start_index = _read_start_segment_index(job)
    completed_segments = (latest_completed_segment_index - start_index) + 1
    return round((completed_segments / max(total_segments, 1)) * 100, 2)


def _plan_composition_summary_checkpoints(
    total_chunks: int,
) -> tuple[CompositionSummaryCheckpoint, ...]:
    if total_chunks <= 1:
        return ()

    checkpoints: list[CompositionSummaryCheckpoint] = []
    seen_chunk_indexes: set[int] = set()
    for progress_ratio in _COMPOSITION_SUMMARY_PROGRESS_CHECKPOINTS:
        chunk_index = max(1, math.ceil(total_chunks * progress_ratio))
        if chunk_index >= total_chunks or chunk_index in seen_chunk_indexes:
            continue
        seen_chunk_indexes.add(chunk_index)
        checkpoints.append(
            CompositionSummaryCheckpoint(
                key=f"progress-{int(progress_ratio * 100)}",
                chunk_index=chunk_index,
                progress_ratio=progress_ratio,
            )
        )
    return tuple(checkpoints)


def _build_composition_summary_message(
    *,
    segment_index: int,
    total_segments: int,
    current_text: str,
    segment_payload: Mapping[str, Any],
    planned_summary: str | None,
    progress_percent: float | None,
    checkpoint_key: str,
) -> str | None:
    excerpt = _build_generated_summary_excerpt(current_text, limit=54)
    if excerpt is None:
        return None

    direction = _resolve_summary_direction(segment_payload, planned_summary)
    focus = _resolve_summary_focus(segment_payload, planned_summary)

    prefix = (
        f"Segment {segment_index}/{total_segments} handoff"
        if checkpoint_key == _COMPOSITION_SUMMARY_FINAL_CHECKPOINT
        else (
            f"Writing update {round(progress_percent)}% ({segment_index}/{total_segments})"
            if progress_percent is not None
            else f"Writing update ({segment_index}/{total_segments})"
        )
    )
    parts = [f"{prefix}: {excerpt}"]
    if direction is not None:
        parts.append(f"Direction: {direction}.")
    if focus is not None:
        parts.append(f"Focus: {focus}.")

    return _truncate_text(" ".join(parts), limit=160)


def _build_generated_summary_excerpt(text: str, *, limit: int) -> str | None:
    normalized = " ".join(text.split()).strip()
    if not normalized:
        return None

    completed_sentences = [
        match.group(0).strip() for match in _SENTENCE_PATTERN.finditer(normalized)
    ]
    if completed_sentences:
        excerpt = completed_sentences[-1]
        if len(excerpt) < 56 and len(completed_sentences) >= 2:
            excerpt = f"{completed_sentences[-2]} {excerpt}"
        return _truncate_summary_text(excerpt, limit=limit)

    return _truncate_summary_text(normalized, limit=limit)


def _resolve_summary_direction(
    segment_payload: Mapping[str, Any],
    planned_summary: str | None,
) -> str | None:
    for candidate in (
        _read_optional_prompt_text(segment_payload, "outline_card_summary"),
        _read_text(
            _read_mapping(_read_mapping(segment_payload, "composition_prompt"), "dynamic_context"),
            "segment_goal_summary",
        ),
        planned_summary,
    ):
        normalized = _normalize_summary_fragment(candidate, limit=24)
        if normalized is not None:
            return normalized
    return None


def _resolve_summary_focus(
    segment_payload: Mapping[str, Any],
    planned_summary: str | None,
) -> str | None:
    dynamic_context = _read_mapping(
        _read_mapping(segment_payload, "composition_prompt"),
        "dynamic_context",
    )
    outline_card = _read_mapping(dynamic_context, "outline_card")

    for candidate in (
        _read_optional_prompt_text(segment_payload, "outline_card_emotional_shift"),
        _read_optional_prompt_text(segment_payload, "outline_card_drafting_brief"),
        _read_text(outline_card, "emotional_shift"),
        _read_text(outline_card, "bedtime_guardrail"),
        planned_summary,
    ):
        normalized = _normalize_summary_fragment(candidate, limit=22)
        if normalized is not None:
            return normalized
    return None


def _normalize_summary_fragment(value: str | None, *, limit: int) -> str | None:
    if value is None:
        return None
    normalized = " ".join(value.split()).strip().rstrip(".")
    if not normalized:
        return None
    return _truncate_summary_text(normalized, limit=limit)


def _truncate_summary_text(value: str, *, limit: int) -> str:
    if len(value) <= limit:
        return value
    truncated = value[: limit - 3].rstrip()
    if " " in truncated:
        truncated = truncated.rsplit(" ", 1)[0]
    return f"{truncated.rstrip(' ,;:')}..."


def _build_composition_summary_message_id(
    *,
    job_id: str,
    segment_id: str,
    checkpoint_key: str,
) -> str:
    return f"composition-summary-{job_id}-{segment_id}-{checkpoint_key}"


def _split_remaining_text(prefix: str, remaining_text: str) -> list[str]:
    return split_text_for_streaming(prefix, remaining_text)


def _extract_last_sentence(text: str) -> str | None:
    sentences = [
        sentence.strip() for sentence in text.replace("\n", " ").split(".") if sentence.strip()
    ]
    if not sentences:
        return None
    return sentences[-1]


def _count_words(text: str | None) -> int:
    if text is None:
        return 0
    return len([part for part in text.split() if part.strip()])


def _read_metadata(job: CompositionJob) -> dict[str, Any]:
    if isinstance(job.metadata_json, Mapping):
        return dict(job.metadata_json)
    return {}


def _read_summary_checkpoint_state(job: CompositionJob) -> dict[str, list[str]]:
    raw_state = _read_metadata(job).get(_COMPOSITION_SUMMARY_METADATA_KEY)
    if not isinstance(raw_state, Mapping):
        return {}

    checkpoint_state: dict[str, list[str]] = {}
    for segment_id, raw_values in raw_state.items():
        if not isinstance(segment_id, str) or not isinstance(raw_values, list):
            continue
        values = [
            str(value).strip()
            for value in raw_values
            if isinstance(value, str) and str(value).strip()
        ]
        if values:
            checkpoint_state[segment_id] = values
    return checkpoint_state


def _has_emitted_summary_checkpoint(
    job: CompositionJob,
    segment_id: str,
    checkpoint_key: str,
) -> bool:
    return checkpoint_key in _read_summary_checkpoint_state(job).get(segment_id, [])


def _mark_summary_checkpoint_emitted(
    job: CompositionJob,
    segment_id: str,
    checkpoint_key: str,
) -> None:
    metadata = _read_metadata(job)
    checkpoint_state = _read_summary_checkpoint_state(job)
    segment_state = checkpoint_state.get(segment_id, [])
    if checkpoint_key not in segment_state:
        segment_state = [*segment_state, checkpoint_key]
    checkpoint_state[segment_id] = segment_state
    job.metadata_json = {
        **metadata,
        _COMPOSITION_SUMMARY_METADATA_KEY: checkpoint_state,
    }


def _read_total_segments(job: CompositionJob) -> int:
    metadata = _read_metadata(job)
    total_segments = metadata.get("total_segments")
    if isinstance(total_segments, int) and total_segments >= 1:
        return total_segments
    raise CompositionJobStateError(
        f"composition job {job.id!r} is missing total_segments metadata",
    )


def _read_start_segment_index(job: CompositionJob) -> int:
    metadata = _read_metadata(job)
    start_segment_index = metadata.get("start_segment_index")
    if isinstance(start_segment_index, int) and start_segment_index >= 1:
        return start_segment_index
    raise CompositionJobStateError(
        f"composition job {job.id!r} is missing start_segment_index metadata",
    )


def _resolve_generation_protagonist_name(prompt_payload: Mapping[str, Any]) -> str:
    dynamic_context = _read_mapping(prompt_payload, "dynamic_context")
    selected_character_sheet = _read_mapping(dynamic_context, "selected_character_sheet")
    protagonist = _read_mapping(selected_character_sheet, "protagonist")
    return (
        _read_text(protagonist, "name")
        or _read_text(selected_character_sheet, "protagonist_name")
        or "The young guide"
    )


def _resolve_generation_support_name(prompt_payload: Mapping[str, Any]) -> str | None:
    dynamic_context = _read_mapping(prompt_payload, "dynamic_context")
    selected_character_sheet = _read_mapping(dynamic_context, "selected_character_sheet")
    supporting_cast = _read_list(selected_character_sheet, "supporting_cast")
    if not supporting_cast:
        return None
    first_support = supporting_cast[0]
    if not isinstance(first_support, Mapping):
        return None
    return _read_text(first_support, "name")


def _build_validation_failure_reason(
    evaluation: CompositionSegmentDraftEvaluation,
) -> str:
    failed = [criterion.name for criterion in evaluation.criteria if not criterion.passed]
    if not failed:
        return "composition segment validation failed"
    return "composition segment validation failed: " + ", ".join(failed)


def _build_carryover_summary(
    *,
    protagonist_name: str,
    outline_title: str,
    outline_summary: str,
    emotional_shift: str,
    prior_story_reference: str | None,
    companion_name: str | None,
) -> str:
    parts = [
        (
            f"{protagonist_name} completed {outline_title.lower()} with this durable turn: "
            f"{outline_summary}"
        ),
        f"Emotional handoff: {emotional_shift}.",
    ]
    if prior_story_reference is not None:
        parts.append(f"Keep continuity with the earlier thread: {prior_story_reference}.")
    if companion_name is not None:
        parts.append(f"Keep {companion_name} visibly supportive in the next segment.")
    return _truncate_text(" ".join(parts), limit=320)


def _resolve_segment_summary(segment: CompositionSegment) -> str | None:
    for candidate in (
        segment.accepted_summary,
        segment.planned_summary,
        _extract_last_sentence(segment.accepted_text or segment.text_content or ""),
    ):
        normalized = candidate.strip() if isinstance(candidate, str) else ""
        if normalized:
            return normalized
    return None


def _build_story_so_far_summary(
    items: Sequence[CompositionSegmentCarryoverItem],
) -> str | None:
    if not items:
        return None
    parts = []
    for item in items[-3:]:
        prefix = (
            f"Segment {item.segment_index}"
            if item.outline_card_title is None
            else f"Segment {item.segment_index} ({item.outline_card_title})"
        )
        parts.append(f"{prefix}: {item.accepted_summary}")
    return _truncate_text(" ".join(parts), limit=420)


def _read_job_prompt_metadata(segment_payload: Mapping[str, Any]) -> dict[str, Any]:
    metadata: dict[str, Any] = {}
    for key in (
        "prompt_assembly_version",
        "story_outline_id",
        "story_outline_revision_number",
        "outline_kind",
        "outline_card_key",
        "outline_card_position",
        "outline_card_title",
        "outline_card_summary",
        "outline_card_drafting_brief",
        "outline_card_beat_keys",
        "outline_card_emotional_shift",
        "continuity_bible_id",
        "continuity_revision_number",
        "continuity_summary",
        "continuity_facts",
        "composition_prompt",
        "context_carryover",
    ):
        value = segment_payload.get(key)
        if value is not None:
            metadata[key] = value
    return metadata


def _read_optional_prompt_text(value: object, key: str) -> str | None:
    if not isinstance(value, Mapping):
        return None
    candidate = value.get(key)
    if candidate is None:
        return None
    normalized = str(candidate).strip()
    return normalized or None


def _resolve_model_usage_outcome(
    *,
    source: str,
    raw_response: Any,
) -> ModelCallOutcome:
    if source != "heuristic":
        return ModelCallOutcome.SUCCEEDED

    if isinstance(raw_response, Mapping) and raw_response.get("fallback_reason"):
        return ModelCallOutcome.SUCCEEDED_WITH_FALLBACK

    return ModelCallOutcome.FAILED


def _extract_model_usage_error_message(raw_response: Any) -> str | None:
    if not isinstance(raw_response, Mapping):
        return None
    error = raw_response.get("fallback_reason")
    if error is None:
        return None
    normalized = str(error).strip()
    return normalized or None


def _read_mapping(value: object, key: str | None = None) -> Mapping[str, Any]:
    candidate = value
    if key is not None and isinstance(value, Mapping):
        candidate = value.get(key)
    if isinstance(candidate, Mapping):
        return candidate
    return {}


def _read_list(value: object, key: str) -> list[Any]:
    if not isinstance(value, Mapping):
        return []
    candidate = value.get(key)
    if isinstance(candidate, list):
        return candidate
    return []


def _read_text(value: object, key: str) -> str | None:
    if not isinstance(value, Mapping):
        return None
    candidate = value.get(key)
    if candidate is None:
        return None
    normalized = str(candidate).strip()
    return normalized or None


def _truncate_text(value: str, *, limit: int) -> str:
    if len(value) <= limit:
        return value
    return f"{value[: limit - 3].rstrip()}..."

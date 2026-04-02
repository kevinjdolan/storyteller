from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any, Protocol

from sqlalchemy import Select, select
from sqlalchemy.orm import Session

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
    CompositionPromptAssemblyInput,
    SessionEventActor,
    WorkflowStage,
    WorkflowStageState,
)
from app.services.assets import SessionAssetService
from app.services.composition_prompt_assembly import CompositionPromptAssemblyService
from app.services.event_log import DEFAULT_SYSTEM_ACTOR, SessionEventLogService
from app.services.jobs import BackgroundJobService
from app.services.plan_revisions import PlanRevisionService
from app.services.sessions import SessionService
from app.settings import get_settings
from app.storage import ObjectStorageService, build_object_storage_service

COMPOSITION_RUNTIME_JOB_TYPE = "story.run_composition_job"
_SEGMENT_CHUNK_PARAGRAPHS = 3
_COMPLETION_DETAIL = "Writing finished and the latest draft is ready for review."


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
    full_text: str
    remaining_chunks: tuple[str, ...]
    evaluation: CompositionSegmentDraftEvaluation


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
        prior_story_reference = None
        if prior_segments:
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

        full_text = "\n\n".join(
            paragraph.strip()
            for paragraph in (paragraph_one, paragraph_two, paragraph_three)
            if paragraph.strip()
        ).strip()
        prefix = current_partial_text or ""
        remaining_text = full_text
        if prefix and full_text.startswith(prefix):
            remaining_text = full_text[len(prefix) :]
        remaining_chunks = tuple(
            chunk for chunk in _split_remaining_text(prefix, remaining_text) if chunk.strip()
        )
        evaluation = evaluate_composition_segment_draft(
            full_text,
            protagonist_name=protagonist_name,
            supporting_character_name=companion_name,
        )
        return GeneratedCompositionSegmentDraft(
            full_text=full_text,
            remaining_chunks=remaining_chunks,
            evaluation=evaluation,
        )


def evaluate_composition_segment_draft(
    full_text: str,
    *,
    protagonist_name: str,
    supporting_character_name: str | None,
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

        completed_segments = self._completed_segment_texts(
            job.id, before_segment_index=current_segment.segment_index
        )
        draft = self._writer.compose_segment(
            segment_payload=_read_mapping(current_segment.payload),
            prior_segments=completed_segments,
            current_partial_text=current_segment.text_content,
            total_segments=total_segments,
        )
        segment_storage_location = self._storage().paths.partial_draft_segment(
            session_id=job.session_id,
            job_id=job.id,
            segment_index=current_segment.segment_index,
        )

        chunk_count = max(len(draft.remaining_chunks), 1)
        current_text = current_segment.text_content or ""
        chunk_index = 0
        for chunk in draft.remaining_chunks:
            current_text += chunk
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
                "latest_partial_output": current_text,
                "current_segment_id": current_segment.id,
            }
            self._storage().upload_text(
                segment_storage_location,
                current_text,
                content_type="text/markdown; charset=utf-8",
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

        current_segment.text_content = draft.full_text
        current_segment.word_count = _count_words(draft.full_text)
        current_segment.status = JobStatus.COMPLETED
        current_segment.completed_at = utc_now()
        self._storage().upload_text(
            segment_storage_location,
            draft.full_text,
            content_type="text/markdown; charset=utf-8",
        )

        next_segment = self._next_queued_segment(
            job, after_segment_index=current_segment.segment_index
        )
        if next_segment is None:
            story_text = self._compile_story_text(job.id)
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
            "latest_partial_output": current_segment.text_content,
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

    def _completed_segment_texts(
        self,
        composition_job_id: str,
        *,
        before_segment_index: int | None = None,
    ) -> list[str]:
        stmt: Select[tuple[CompositionSegment]] = (
            select(CompositionSegment)
            .where(
                CompositionSegment.composition_job_id == composition_job_id,
                CompositionSegment.status == JobStatus.COMPLETED,
            )
            .order_by(CompositionSegment.segment_index.asc())
        )
        if before_segment_index is not None:
            stmt = stmt.where(CompositionSegment.segment_index < before_segment_index)
        rows = list(self._session.execute(stmt).scalars().all())
        return [row.text_content for row in rows if row.text_content]

    def _compile_story_text(self, composition_job_id: str) -> str:
        completed_segments = self._completed_segment_texts(composition_job_id)
        if not completed_segments:
            raise CompositionJobStateError(
                "cannot finalize a composition job without completed text"
            )
        return "\n\n".join(
            segment.strip() for segment in completed_segments if segment.strip()
        ).strip()

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


def _split_remaining_text(prefix: str, remaining_text: str) -> list[str]:
    if not remaining_text:
        return []

    paragraphs = [paragraph for paragraph in remaining_text.split("\n\n") if paragraph.strip()]
    chunks: list[str] = []
    for paragraph in paragraphs:
        if chunks:
            chunks.append(f"\n\n{paragraph}")
        else:
            chunks.append(paragraph if not prefix else paragraph)
    return chunks


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

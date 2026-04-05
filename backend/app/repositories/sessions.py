from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy import Select, or_, select
from sqlalchemy.orm import Session, selectinload

from app.db import (
    AssetKind,
    AssetStatus,
    AudioJob,
    BeatSheet,
    CharacterSheet,
    CompositionJob,
    CompositionSegment,
    ContinuityBible,
    Genre,
    JobStatus,
    NarrationSegment,
    Pitch,
    PlanRevision,
    SessionAsset,
    StoryBrief,
    StoryOutline,
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
STORY_MANUSCRIPT_ASSET_KINDS = (AssetKind.STORY_TEXT,)
STORY_EXPORT_ASSET_KINDS = (AssetKind.STORY_DOCX,)


@dataclass(frozen=True)
class SessionAggregate:
    session: StorySession
    active_story_brief: StoryBrief | None
    pitches: list[Pitch]
    selected_pitch: Pitch | None
    character_sheets: list[CharacterSheet]
    selected_character_sheet: CharacterSheet | None
    beat_sheets: list[BeatSheet]
    selected_beat_sheet: BeatSheet | None
    selected_story_setup: StorySetup | None
    story_outlines: list[StoryOutline]
    selected_story_outline: StoryOutline | None
    plan_revisions: list[PlanRevision]
    current_plan_revision: PlanRevision | None
    latest_composition_job: CompositionJob | None
    latest_audio_job: AudioJob | None
    active_composition_job: CompositionJob | None
    active_audio_job: AudioJob | None
    composition_segments: list[CompositionSegment]
    audio_segments: list[NarrationSegment]
    audio_segment_assets: list[SessionAsset]
    latest_draft_snapshot_asset: SessionAsset | None
    latest_story_asset: SessionAsset | None
    latest_story_export_asset: SessionAsset | None
    latest_audio_asset: SessionAsset | None
    selected_continuity_bible: ContinuityBible | None


@dataclass(frozen=True)
class RecentSessionLibraryRecord:
    session: StorySession
    active_story_brief: StoryBrief | None
    selected_pitch: Pitch | None
    selected_story_setup: StorySetup | None
    latest_audio_job: AudioJob | None
    latest_story_asset: SessionAsset | None
    latest_story_export_asset: SessionAsset | None
    latest_audio_asset: SessionAsset | None


class StorySessionRepository:
    def __init__(self, session: Session):
        self._session = session

    def create(
        self,
        *,
        owner_id: str,
        working_title: str | None = None,
    ) -> StorySession:
        story_session = StorySession(owner_id=owner_id, working_title=working_title)
        self._session.add(story_session)
        self._session.flush()
        return story_session

    def get_by_id(
        self,
        session_id: str,
        *,
        owner_id: str | None = None,
    ) -> StorySession | None:
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
        stmt = _filter_for_owner(stmt, owner_id)
        return self._session.execute(stmt).scalar_one_or_none()

    def exists(self, session_id: str, *, owner_id: str | None = None) -> bool:
        stmt = select(StorySession.id).where(StorySession.id == session_id).limit(1)
        stmt = _filter_for_owner(stmt, owner_id)
        return self._session.execute(stmt).scalar_one_or_none() is not None

    def get_for_update(
        self,
        session_id: str,
        *,
        owner_id: str | None = None,
    ) -> StorySession | None:
        stmt: Select[tuple[StorySession]] = (
            select(StorySession)
            .options(selectinload(StorySession.workflow_stage_states))
            .where(StorySession.id == session_id)
        )
        stmt = _filter_for_owner(stmt, owner_id)
        return self._session.execute(stmt).scalar_one_or_none()

    def get_aggregate(
        self,
        session_id: str,
        *,
        owner_id: str | None = None,
    ) -> SessionAggregate | None:
        story_session = self.get_by_id(session_id, owner_id=owner_id)
        if story_session is None:
            return None

        latest_composition_job = self._get_latest_composition_job(session_id)
        latest_audio_job = self._get_latest_audio_job(session_id)
        active_composition_job = self._get_active_composition_job(session_id)
        active_audio_job = self._get_active_audio_job(session_id)
        visible_audio_job = active_audio_job or latest_audio_job

        return SessionAggregate(
            session=story_session,
            active_story_brief=self._get_active_story_brief(session_id),
            pitches=self._list_pitches(session_id),
            selected_pitch=self._get_selected_pitch(session_id),
            character_sheets=self._list_character_sheets(session_id),
            selected_character_sheet=self._get_selected_character_sheet(session_id),
            beat_sheets=self._list_beat_sheets(session_id),
            selected_beat_sheet=self._get_selected_beat_sheet(session_id),
            selected_story_setup=self._get_selected_story_setup(session_id),
            story_outlines=self._list_story_outlines(session_id),
            selected_story_outline=self._get_selected_story_outline(session_id),
            plan_revisions=self._list_plan_revisions(session_id),
            current_plan_revision=self._get_current_plan_revision(session_id),
            latest_composition_job=latest_composition_job,
            latest_audio_job=latest_audio_job,
            active_composition_job=active_composition_job,
            active_audio_job=active_audio_job,
            composition_segments=self._list_composition_segments(session_id),
            audio_segments=self._list_audio_segments(
                visible_audio_job.id if visible_audio_job is not None else None
            ),
            audio_segment_assets=self._list_audio_segment_assets(
                visible_audio_job.id if visible_audio_job is not None else None
            ),
            latest_draft_snapshot_asset=self._get_latest_draft_snapshot_asset(session_id),
            latest_story_asset=self._get_latest_story_asset(session_id),
            latest_story_export_asset=self._get_latest_story_export_asset(session_id),
            latest_audio_asset=self._get_latest_audio_asset(session_id),
            selected_continuity_bible=self._get_selected_continuity_bible(session_id),
        )

    def get_active_story_brief(self, session_id: str) -> StoryBrief | None:
        return self._get_active_story_brief(session_id)

    def get_selected_pitch(self, session_id: str) -> Pitch | None:
        return self._get_selected_pitch(session_id)

    def list_pitches(self, session_id: str) -> list[Pitch]:
        return self._list_pitches(session_id)

    def get_selected_character_sheet(self, session_id: str) -> CharacterSheet | None:
        return self._get_selected_character_sheet(session_id)

    def list_character_sheets(self, session_id: str) -> list[CharacterSheet]:
        return self._list_character_sheets(session_id)

    def get_selected_beat_sheet(self, session_id: str) -> BeatSheet | None:
        return self._get_selected_beat_sheet(session_id)

    def list_beat_sheets(self, session_id: str) -> list[BeatSheet]:
        return self._list_beat_sheets(session_id)

    def get_selected_story_outline(self, session_id: str) -> StoryOutline | None:
        return self._get_selected_story_outline(session_id)

    def list_story_outlines(self, session_id: str) -> list[StoryOutline]:
        return self._list_story_outlines(session_id)

    def get_current_plan_revision(self, session_id: str) -> PlanRevision | None:
        return self._get_current_plan_revision(session_id)

    def list_plan_revisions(self, session_id: str) -> list[PlanRevision]:
        return self._list_plan_revisions(session_id)

    def get_selected_continuity_bible(self, session_id: str) -> ContinuityBible | None:
        return self._get_selected_continuity_bible(session_id)

    def list_recent(
        self,
        *,
        limit: int = 20,
        owner_id: str | None = None,
    ) -> list[StorySession]:
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
        stmt = _filter_for_owner(stmt, owner_id)
        return list(self._session.execute(stmt).scalars().all())

    def list_recent_library_records(
        self,
        *,
        limit: int = 20,
        owner_id: str | None = None,
        query: str | None = None,
        status_filter: str | None = None,
        genre_slug: str | None = None,
    ) -> list[RecentSessionLibraryRecord]:
        stmt: Select[tuple[StorySession]] = (
            select(StorySession)
            .options(
                selectinload(StorySession.selected_genre),
                selectinload(StorySession.selected_tone_profile),
                selectinload(StorySession.workflow_stage_states),
                selectinload(StorySession.story_briefs),
                selectinload(StorySession.pitches),
                selectinload(StorySession.story_setups),
                selectinload(StorySession.audio_jobs),
            )
            .order_by(StorySession.updated_at.desc(), StorySession.created_at.desc())
        )
        stmt = _filter_for_owner(stmt, owner_id)

        if status_filter is not None and status_filter != "all":
            if status_filter == "active":
                stmt = stmt.where(
                    StorySession.overall_status.in_(
                        (
                            WorkflowStageState.DRAFT,
                            WorkflowStageState.IN_PROGRESS,
                            WorkflowStageState.NEEDS_REGENERATION,
                        )
                    )
                )
            else:
                stmt = stmt.where(StorySession.overall_status == WorkflowStageState(status_filter))

        normalized_genre_slug = (genre_slug or "").strip()
        if normalized_genre_slug:
            stmt = stmt.where(StorySession.selected_genre.has(Genre.slug == normalized_genre_slug))

        query_tokens = _tokenize_library_query(query)
        for token in query_tokens:
            pattern = f"%{token}%"
            stmt = stmt.where(
                or_(
                    StorySession.working_title.ilike(pattern),
                    StorySession.story_briefs.any(
                        or_(
                            StoryBrief.story_idea.ilike(pattern),
                            StoryBrief.normalized_summary.ilike(pattern),
                            StoryBrief.raw_brief.ilike(pattern),
                        )
                    ),
                    StorySession.pitches.any(Pitch.title.ilike(pattern)),
                )
            )

        sessions = list(self._session.execute(stmt.limit(limit)).scalars().all())
        if not sessions:
            return []

        asset_map = self._load_library_assets([story_session.id for story_session in sessions])

        return [
            RecentSessionLibraryRecord(
                session=story_session,
                active_story_brief=_select_active_story_brief(story_session.story_briefs),
                selected_pitch=_select_selected_pitch(story_session.pitches),
                selected_story_setup=_select_selected_story_setup(story_session.story_setups),
                latest_audio_job=_select_latest_audio_job(story_session.audio_jobs),
                latest_story_asset=asset_map.get(story_session.id, {}).get(AssetKind.STORY_TEXT),
                latest_story_export_asset=asset_map.get(story_session.id, {}).get(
                    AssetKind.STORY_DOCX
                ),
                latest_audio_asset=asset_map.get(story_session.id, {}).get(AssetKind.FINAL_AUDIO),
            )
            for story_session in sessions
        ]

    def _load_library_assets(
        self,
        session_ids: list[str],
    ) -> dict[str, dict[AssetKind, SessionAsset]]:
        stmt: Select[tuple[SessionAsset]] = (
            select(SessionAsset)
            .where(
                SessionAsset.session_id.in_(session_ids),
                SessionAsset.asset_kind.in_(
                    (
                        AssetKind.STORY_TEXT,
                        AssetKind.STORY_DOCX,
                        AssetKind.FINAL_AUDIO,
                    )
                ),
                SessionAsset.status == AssetStatus.READY,
            )
            .order_by(
                SessionAsset.session_id.asc(),
                SessionAsset.asset_kind.asc(),
                SessionAsset.ready_at.desc(),
                SessionAsset.created_at.desc(),
            )
        )

        asset_map: dict[str, dict[AssetKind, SessionAsset]] = {
            session_id: {} for session_id in session_ids
        }
        for asset in self._session.execute(stmt).scalars().all():
            session_assets = asset_map.setdefault(asset.session_id, {})
            session_assets.setdefault(asset.asset_kind, asset)

        return asset_map

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

    def _list_pitches(self, session_id: str) -> list[Pitch]:
        stmt: Select[tuple[Pitch]] = (
            select(Pitch)
            .where(Pitch.session_id == session_id)
            .order_by(Pitch.created_at.asc(), Pitch.pitch_index.asc())
        )
        return list(self._session.execute(stmt).scalars().all())

    def _get_selected_character_sheet(self, session_id: str) -> CharacterSheet | None:
        stmt: Select[tuple[CharacterSheet]] = (
            select(CharacterSheet)
            .where(CharacterSheet.session_id == session_id, CharacterSheet.is_selected.is_(True))
            .order_by(CharacterSheet.revision_number.desc())
            .limit(1)
        )
        return self._session.execute(stmt).scalar_one_or_none()

    def _list_character_sheets(self, session_id: str) -> list[CharacterSheet]:
        stmt: Select[tuple[CharacterSheet]] = (
            select(CharacterSheet)
            .where(CharacterSheet.session_id == session_id)
            .order_by(CharacterSheet.created_at.asc(), CharacterSheet.revision_number.asc())
        )
        return list(self._session.execute(stmt).scalars().all())

    def _get_selected_beat_sheet(self, session_id: str) -> BeatSheet | None:
        stmt: Select[tuple[BeatSheet]] = (
            select(BeatSheet)
            .where(BeatSheet.session_id == session_id, BeatSheet.is_selected.is_(True))
            .order_by(BeatSheet.revision_number.desc())
            .limit(1)
        )
        return self._session.execute(stmt).scalar_one_or_none()

    def _list_beat_sheets(self, session_id: str) -> list[BeatSheet]:
        stmt: Select[tuple[BeatSheet]] = (
            select(BeatSheet)
            .where(BeatSheet.session_id == session_id)
            .order_by(BeatSheet.created_at.asc(), BeatSheet.revision_number.asc())
        )
        return list(self._session.execute(stmt).scalars().all())

    def _get_selected_story_setup(self, session_id: str) -> StorySetup | None:
        stmt: Select[tuple[StorySetup]] = (
            select(StorySetup)
            .where(StorySetup.session_id == session_id, StorySetup.is_selected.is_(True))
            .order_by(StorySetup.revision_number.desc())
            .limit(1)
        )
        return self._session.execute(stmt).scalar_one_or_none()

    def _get_selected_story_outline(self, session_id: str) -> StoryOutline | None:
        stmt: Select[tuple[StoryOutline]] = (
            select(StoryOutline)
            .where(StoryOutline.session_id == session_id, StoryOutline.is_selected.is_(True))
            .order_by(StoryOutline.revision_number.desc())
            .limit(1)
        )
        return self._session.execute(stmt).scalar_one_or_none()

    def _list_story_outlines(self, session_id: str) -> list[StoryOutline]:
        stmt: Select[tuple[StoryOutline]] = (
            select(StoryOutline)
            .where(StoryOutline.session_id == session_id)
            .order_by(StoryOutline.created_at.asc(), StoryOutline.revision_number.asc())
        )
        return list(self._session.execute(stmt).scalars().all())

    def _get_current_plan_revision(self, session_id: str) -> PlanRevision | None:
        stmt: Select[tuple[PlanRevision]] = (
            select(PlanRevision)
            .options(
                selectinload(PlanRevision.pitch),
                selectinload(PlanRevision.character_sheet),
                selectinload(PlanRevision.beat_sheet),
                selectinload(PlanRevision.story_setup),
                selectinload(PlanRevision.story_outline),
                selectinload(PlanRevision.restored_from_plan_revision),
            )
            .where(PlanRevision.session_id == session_id, PlanRevision.is_current.is_(True))
            .order_by(PlanRevision.revision_number.desc())
            .limit(1)
        )
        return self._session.execute(stmt).scalar_one_or_none()

    def _list_plan_revisions(self, session_id: str) -> list[PlanRevision]:
        stmt: Select[tuple[PlanRevision]] = (
            select(PlanRevision)
            .options(
                selectinload(PlanRevision.pitch),
                selectinload(PlanRevision.character_sheet),
                selectinload(PlanRevision.beat_sheet),
                selectinload(PlanRevision.story_setup),
                selectinload(PlanRevision.story_outline),
                selectinload(PlanRevision.restored_from_plan_revision),
            )
            .where(PlanRevision.session_id == session_id)
            .order_by(PlanRevision.revision_number.asc())
        )
        return list(self._session.execute(stmt).scalars().all())

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

    def _get_latest_composition_job(self, session_id: str) -> CompositionJob | None:
        stmt: Select[tuple[CompositionJob]] = (
            select(CompositionJob)
            .where(CompositionJob.session_id == session_id)
            .order_by(CompositionJob.updated_at.desc(), CompositionJob.created_at.desc())
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

    def _get_latest_audio_job(self, session_id: str) -> AudioJob | None:
        stmt: Select[tuple[AudioJob]] = (
            select(AudioJob)
            .where(AudioJob.session_id == session_id)
            .order_by(AudioJob.updated_at.desc(), AudioJob.created_at.desc())
            .limit(1)
        )
        return self._session.execute(stmt).scalar_one_or_none()

    def _get_latest_story_asset(self, session_id: str) -> SessionAsset | None:
        stmt: Select[tuple[SessionAsset]] = (
            select(SessionAsset)
            .where(
                SessionAsset.session_id == session_id,
                SessionAsset.asset_kind.in_(STORY_MANUSCRIPT_ASSET_KINDS),
                SessionAsset.status == AssetStatus.READY,
            )
            .order_by(SessionAsset.ready_at.desc(), SessionAsset.created_at.desc())
            .limit(1)
        )
        return self._session.execute(stmt).scalar_one_or_none()

    def _get_latest_story_export_asset(self, session_id: str) -> SessionAsset | None:
        stmt: Select[tuple[SessionAsset]] = (
            select(SessionAsset)
            .where(
                SessionAsset.session_id == session_id,
                SessionAsset.asset_kind.in_(STORY_EXPORT_ASSET_KINDS),
                SessionAsset.status == AssetStatus.READY,
            )
            .order_by(SessionAsset.ready_at.desc(), SessionAsset.created_at.desc())
            .limit(1)
        )
        return self._session.execute(stmt).scalar_one_or_none()

    def _get_latest_draft_snapshot_asset(self, session_id: str) -> SessionAsset | None:
        stmt: Select[tuple[SessionAsset]] = (
            select(SessionAsset)
            .where(
                SessionAsset.session_id == session_id,
                SessionAsset.asset_kind == AssetKind.DRAFT_TEXT_SNAPSHOT,
                SessionAsset.status == AssetStatus.READY,
            )
            .order_by(SessionAsset.ready_at.desc(), SessionAsset.updated_at.desc())
            .limit(1)
        )
        return self._session.execute(stmt).scalar_one_or_none()

    def _list_composition_segments(self, session_id: str) -> list[CompositionSegment]:
        stmt: Select[tuple[CompositionSegment]] = (
            select(CompositionSegment)
            .options(selectinload(CompositionSegment.composition_job))
            .where(CompositionSegment.session_id == session_id)
            .order_by(
                CompositionSegment.segment_index.asc(),
                CompositionSegment.revision_number.desc(),
                CompositionSegment.created_at.desc(),
            )
        )
        return list(self._session.execute(stmt).scalars().all())

    def _list_audio_segments(self, audio_job_id: str | None) -> list[NarrationSegment]:
        if audio_job_id is None:
            return []

        stmt: Select[tuple[NarrationSegment]] = (
            select(NarrationSegment)
            .where(NarrationSegment.audio_job_id == audio_job_id)
            .order_by(
                NarrationSegment.segment_index.asc(),
                NarrationSegment.created_at.asc(),
            )
        )
        return list(self._session.execute(stmt).scalars().all())

    def _list_audio_segment_assets(self, audio_job_id: str | None) -> list[SessionAsset]:
        if audio_job_id is None:
            return []

        stmt: Select[tuple[SessionAsset]] = (
            select(SessionAsset)
            .where(
                SessionAsset.audio_job_id == audio_job_id,
                SessionAsset.asset_kind == AssetKind.AUDIO_SEGMENT,
                SessionAsset.status == AssetStatus.READY,
            )
            .order_by(
                SessionAsset.segment_index.asc(),
                SessionAsset.ready_at.desc(),
                SessionAsset.created_at.desc(),
            )
        )
        return list(self._session.execute(stmt).scalars().all())

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

    def _get_selected_continuity_bible(self, session_id: str) -> ContinuityBible | None:
        stmt: Select[tuple[ContinuityBible]] = (
            select(ContinuityBible)
            .where(
                ContinuityBible.session_id == session_id,
                ContinuityBible.is_selected.is_(True),
            )
            .order_by(ContinuityBible.revision_number.desc())
            .limit(1)
        )
        return self._session.execute(stmt).scalar_one_or_none()


def _filter_for_owner(
    stmt: Select,
    owner_id: str | None,
) -> Select:
    if owner_id is None:
        return stmt

    return stmt.where(StorySession.owner_id == owner_id)


def _tokenize_library_query(query: str | None) -> list[str]:
    normalized_query = (query or "").strip()
    if not normalized_query:
        return []
    return [token for token in normalized_query.split() if token]


def _select_active_story_brief(story_briefs: list[StoryBrief]) -> StoryBrief | None:
    active_story_briefs = [row for row in story_briefs if row.is_active]
    if not active_story_briefs:
        return None
    return max(
        active_story_briefs,
        key=lambda row: (row.revision_number, row.updated_at, row.created_at),
    )


def _select_selected_pitch(pitches: list[Pitch]) -> Pitch | None:
    selected_pitches = [row for row in pitches if row.is_selected]
    if not selected_pitches:
        return None
    return max(
        selected_pitches,
        key=lambda row: (row.accepted_at or row.updated_at, row.created_at),
    )


def _select_selected_story_setup(story_setups: list[StorySetup]) -> StorySetup | None:
    selected_story_setups = [row for row in story_setups if row.is_selected]
    if not selected_story_setups:
        return None
    return max(
        selected_story_setups,
        key=lambda row: (row.revision_number, row.accepted_at or row.updated_at, row.created_at),
    )


def _select_latest_audio_job(audio_jobs: list[AudioJob]) -> AudioJob | None:
    if not audio_jobs:
        return None
    return max(audio_jobs, key=lambda row: (row.updated_at, row.created_at))


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

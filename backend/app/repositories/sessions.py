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
    pitches: list[Pitch]
    selected_pitch: Pitch | None
    selected_character_sheet: CharacterSheet | None
    selected_beat_sheet: BeatSheet | None
    selected_story_setup: StorySetup | None
    latest_composition_job: CompositionJob | None
    latest_audio_job: AudioJob | None
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
            pitches=self._list_pitches(session_id),
            selected_pitch=self._get_selected_pitch(session_id),
            selected_character_sheet=self._get_selected_character_sheet(session_id),
            selected_beat_sheet=self._get_selected_beat_sheet(session_id),
            selected_story_setup=self._get_selected_story_setup(session_id),
            latest_composition_job=self._get_latest_composition_job(session_id),
            latest_audio_job=self._get_latest_audio_job(session_id),
            active_composition_job=self._get_active_composition_job(session_id),
            active_audio_job=self._get_active_audio_job(session_id),
            latest_story_asset=self._get_latest_story_asset(session_id),
            latest_audio_asset=self._get_latest_audio_asset(session_id),
        )

    def get_active_story_brief(self, session_id: str) -> StoryBrief | None:
        return self._get_active_story_brief(session_id)

    def get_selected_pitch(self, session_id: str) -> Pitch | None:
        return self._get_selected_pitch(session_id)

    def list_pitches(self, session_id: str) -> list[Pitch]:
        return self._list_pitches(session_id)

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

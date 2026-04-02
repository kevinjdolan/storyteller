from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy import Select, func, select
from sqlalchemy.orm import Session, selectinload

from app.db import PlanRevision, StorySetup
from app.models.workflow import WorkflowStage
from app.repositories.sessions import StorySessionRepository


@dataclass(frozen=True)
class CurrentPlanState:
    pitch_id: str | None
    character_sheet_id: str | None
    beat_sheet_id: str | None
    story_setup_id: str | None
    story_outline_id: str | None

    def has_any_artifact(self) -> bool:
        return any(
            value is not None
            for value in (
                self.pitch_id,
                self.character_sheet_id,
                self.beat_sheet_id,
                self.story_setup_id,
                self.story_outline_id,
            )
        )


class PlanRevisionService:
    def __init__(self, session: Session):
        self._session = session
        self._sessions = StorySessionRepository(session)

    def list_revisions(self, session_id: str) -> list[PlanRevision]:
        stmt = (
            self._base_revision_query()
            .where(PlanRevision.session_id == session_id)
            .order_by(PlanRevision.revision_number.asc())
        )
        return list(self._session.execute(stmt).scalars().all())

    def get_current_revision(self, session_id: str) -> PlanRevision | None:
        stmt = (
            self._base_revision_query()
            .where(PlanRevision.session_id == session_id, PlanRevision.is_current.is_(True))
            .order_by(PlanRevision.revision_number.desc())
            .limit(1)
        )
        return self._session.execute(stmt).scalar_one_or_none()

    def get_revision_by_number(self, session_id: str, revision_number: int) -> PlanRevision | None:
        stmt = (
            self._base_revision_query()
            .where(
                PlanRevision.session_id == session_id,
                PlanRevision.revision_number == revision_number,
            )
            .limit(1)
        )
        return self._session.execute(stmt).scalar_one_or_none()

    def ensure_current_revision(
        self,
        session_id: str,
        *,
        source_stage: WorkflowStage | None = None,
        change_summary: str | None = None,
    ) -> PlanRevision | None:
        current = self.get_current_revision(session_id)
        if current is not None:
            return current

        return self.capture_current_state(
            session_id,
            source_stage=source_stage,
            change_summary=change_summary,
            force=True,
        )

    def capture_current_state(
        self,
        session_id: str,
        *,
        source_stage: WorkflowStage | None = None,
        change_summary: str | None = None,
        restored_from_revision: PlanRevision | None = None,
        force: bool = False,
    ) -> PlanRevision | None:
        state = self._read_current_plan_state(session_id)
        if not state.has_any_artifact():
            return None

        current = self.get_current_revision(session_id)
        if (
            current is not None
            and not force
            and _matches_current_state(current, state)
            and restored_from_revision is None
        ):
            return current

        if current is not None:
            current.is_current = False

        plan_revision = PlanRevision(
            session_id=session_id,
            revision_number=self._next_revision_number(session_id),
            source_stage=source_stage,
            change_summary=change_summary,
            restored_from_plan_revision_id=(
                restored_from_revision.id if restored_from_revision is not None else None
            ),
            pitch_id=state.pitch_id,
            character_sheet_id=state.character_sheet_id,
            beat_sheet_id=state.beat_sheet_id,
            story_setup_id=state.story_setup_id,
            story_outline_id=state.story_outline_id,
            is_current=True,
        )
        self._session.add(plan_revision)
        self._session.flush()
        return self._session.execute(
            self._base_revision_query().where(PlanRevision.id == plan_revision.id)
        ).scalar_one()

    def _base_revision_query(self) -> Select[tuple[PlanRevision]]:
        return select(PlanRevision).options(
            selectinload(PlanRevision.pitch),
            selectinload(PlanRevision.character_sheet),
            selectinload(PlanRevision.beat_sheet),
            selectinload(PlanRevision.story_setup),
            selectinload(PlanRevision.story_outline),
            selectinload(PlanRevision.restored_from_plan_revision),
        )

    def _next_revision_number(self, session_id: str) -> int:
        stmt = select(func.max(PlanRevision.revision_number)).where(
            PlanRevision.session_id == session_id
        )
        current = self._session.execute(stmt).scalar_one_or_none() or 0
        return int(current) + 1

    def _read_current_plan_state(self, session_id: str) -> CurrentPlanState:
        selected_pitch = self._sessions.get_selected_pitch(session_id)
        selected_character_sheet = self._sessions.get_selected_character_sheet(session_id)
        selected_beat_sheet = self._sessions.get_selected_beat_sheet(session_id)
        selected_story_setup = self._get_selected_story_setup(session_id)
        selected_story_outline = self._sessions.get_selected_story_outline(session_id)
        return CurrentPlanState(
            pitch_id=selected_pitch.id if selected_pitch is not None else None,
            character_sheet_id=(
                selected_character_sheet.id if selected_character_sheet is not None else None
            ),
            beat_sheet_id=selected_beat_sheet.id if selected_beat_sheet is not None else None,
            story_setup_id=selected_story_setup.id if selected_story_setup is not None else None,
            story_outline_id=(
                selected_story_outline.id if selected_story_outline is not None else None
            ),
        )

    def _get_selected_story_setup(self, session_id: str) -> StorySetup | None:
        stmt = (
            select(StorySetup)
            .where(StorySetup.session_id == session_id, StorySetup.is_selected.is_(True))
            .order_by(StorySetup.revision_number.desc())
            .limit(1)
        )
        return self._session.execute(stmt).scalar_one_or_none()


def _matches_current_state(plan_revision: PlanRevision, state: CurrentPlanState) -> bool:
    return (
        plan_revision.pitch_id == state.pitch_id
        and plan_revision.character_sheet_id == state.character_sheet_id
        and plan_revision.beat_sheet_id == state.beat_sheet_id
        and plan_revision.story_setup_id == state.story_setup_id
        and plan_revision.story_outline_id == state.story_outline_id
    )

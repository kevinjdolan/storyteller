from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy.orm import Session

from app.ai import (
    BeatSheetGenerationAdapter,
    BriefNormalizationAdapter,
    CharacterGenerationAdapter,
    IntentParserAdapter,
    PitchGenerationAdapter,
)
from app.api.dependencies import (
    get_beat_sheet_generation_adapter,
    get_brief_normalization_adapter,
    get_character_generation_adapter,
    get_db_session,
    get_intent_parser_adapter,
    get_pitch_generation_adapter,
)
from app.db import CompositionDownstreamMode, CompositionJob
from app.models import (
    AcceptRewriteSessionCompositionRequest,
    CreateSessionRequest,
    EditSessionBeatSheetRequest,
    GenerateSessionBeatSheetRequest,
    GenerateSessionCharacterSheetsRequest,
    GenerateSessionPitchesRequest,
    ParseChatIntentRequest,
    ParsedChatIntentResponse,
    RecentSessionSummary,
    RecordSessionUIActionRequest,
    RedirectSessionCompositionRequest,
    RefineSessionBeatSheetRequest,
    RefineSessionCharacterSheetRequest,
    RefineSessionPitchRequest,
    RejectRewriteSessionCompositionRequest,
    RestoreSessionPlanRevisionRequest,
    SaveSessionStoryBriefRequest,
    SaveSessionStoryOutlineRequest,
    SaveSessionStorySetupRequest,
    SelectCompositionSegmentVersionRequest,
    SelectSessionBeatSheetRequest,
    SelectSessionCharacterSheetRequest,
    SelectSessionGenreRequest,
    SelectSessionPitchRequest,
    SelectSessionToneRequest,
    SessionActionPolicyEvaluation,
    SessionActionPolicyEvaluationRequest,
    SessionBeatSheetGenerationResponse,
    SessionBeatSheetUpdateResponse,
    SessionCharacterSheetGenerationResponse,
    SessionCompositionResponse,
    SessionContextUpdateRequest,
    SessionContextUpdateResponse,
    SessionEventView,
    SessionHistoryView,
    SessionHydrationView,
    SessionPitchGenerationResponse,
    SessionSelectionResponse,
    SessionSnapshot,
    SessionStoryBriefResponse,
    SessionStoryOutlineResponse,
    SessionStorySetupResponse,
    SessionUsageDiagnosticsView,
    StartSessionCompositionRequest,
    StoryWorkflowToolName,
    WorkflowStage,
)
from app.services import (
    BeatSheetGenerationService,
    BriefNormalizationService,
    CharacterGenerationService,
    CompositionJobNotFoundError,
    CompositionJobService,
    CompositionJobStateError,
    PitchGenerationService,
    SessionActionPolicyService,
    SessionIntentParserService,
    StoryWorkflowToolService,
)
from app.services.session_hydration import (
    SessionHydrationNotFoundError,
    SessionHydrationService,
    build_composition_job_view,
)
from app.services.sessions import (
    InvalidStageTransitionError,
    SessionBeatSheetEditError,
    SessionBeatSheetGenerationError,
    SessionBeatSheetSelectionError,
    SessionCharacterSheetGenerationError,
    SessionCharacterSheetSelectionError,
    SessionGenreSelectionError,
    SessionNotFoundError,
    SessionPitchGenerationError,
    SessionPitchSelectionError,
    SessionPlanRevisionError,
    SessionService,
    SessionStoryBriefSaveError,
    SessionToneSelectionError,
    UnsupportedSessionContextUpdateError,
)
from app.services.story_tools import StoryWorkflowToolServiceError

router = APIRouter(prefix="/sessions", tags=["sessions"])


@router.get(
    "",
    response_model=list[RecentSessionSummary],
    summary="List recent story sessions",
)
def list_recent_sessions(
    db_session: Annotated[Session, Depends(get_db_session)],
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
) -> list[RecentSessionSummary]:
    return SessionService(db_session).list_recent_sessions(limit=limit)


@router.get(
    "/{session_id}",
    response_model=SessionSnapshot,
    summary="Load a story session snapshot",
)
def get_session_snapshot(
    session_id: str,
    db_session: Annotated[Session, Depends(get_db_session)],
) -> SessionSnapshot:
    try:
        return SessionService(db_session).load_session_snapshot(session_id)
    except SessionNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.get(
    "/{session_id}/hydrate",
    response_model=SessionHydrationView,
    summary="Hydrate a story session workspace snapshot",
)
def hydrate_session_workspace(
    session_id: str,
    db_session: Annotated[Session, Depends(get_db_session)],
    history_limit: Annotated[int, Query(ge=1, le=200)] = 40,
) -> SessionHydrationView:
    try:
        return SessionHydrationService(db_session).hydrate_session(
            session_id,
            history_limit=history_limit,
        )
    except SessionHydrationNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.get(
    "/{session_id}/history",
    response_model=SessionHistoryView,
    summary="Load durable session history",
)
def get_session_history(
    session_id: str,
    db_session: Annotated[Session, Depends(get_db_session)],
    limit: Annotated[int | None, Query(ge=1, le=500)] = None,
    after_sequence_number: Annotated[int | None, Query(ge=0)] = None,
) -> SessionHistoryView:
    try:
        return SessionService(db_session).load_session_history(
            session_id,
            limit=limit,
            after_sequence_number=after_sequence_number,
        )
    except SessionNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.get(
    "/{session_id}/usage",
    response_model=SessionUsageDiagnosticsView,
    summary="Load developer-facing model usage diagnostics for a story session",
)
def get_session_usage_diagnostics(
    session_id: str,
    db_session: Annotated[Session, Depends(get_db_session)],
    recent_limit: Annotated[int, Query(ge=1, le=100)] = 20,
    leaderboard_limit: Annotated[int, Query(ge=1, le=20)] = 5,
) -> SessionUsageDiagnosticsView:
    try:
        return SessionService(db_session).load_session_usage_diagnostics(
            session_id,
            recent_limit=recent_limit,
            leaderboard_limit=leaderboard_limit,
        )
    except SessionNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.post(
    "",
    response_model=SessionSnapshot,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new story session",
)
def create_session(
    db_session: Annotated[Session, Depends(get_db_session)],
    payload: CreateSessionRequest | None = None,
) -> SessionSnapshot:
    return SessionService(db_session).create_session(
        working_title=payload.working_title if payload is not None else None,
    )


@router.post(
    "/{session_id}/selections/genre",
    response_model=SessionSelectionResponse,
    status_code=status.HTTP_200_OK,
    summary="Persist the selected genre for a story session",
)
def select_session_genre(
    session_id: str,
    payload: SelectSessionGenreRequest,
    db_session: Annotated[Session, Depends(get_db_session)],
) -> SessionSelectionResponse:
    try:
        return SessionService(db_session).select_genre(
            session_id,
            genre_id=payload.genre_id,
            genre_slug=payload.genre_slug,
            genre_label=payload.genre_label,
            origin=payload.origin,
        )
    except SessionNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    except SessionGenreSelectionError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc


@router.post(
    "/{session_id}/selections/tone",
    response_model=SessionSelectionResponse,
    status_code=status.HTTP_200_OK,
    summary="Persist the selected tone for a story session",
)
def select_session_tone(
    session_id: str,
    payload: SelectSessionToneRequest,
    db_session: Annotated[Session, Depends(get_db_session)],
) -> SessionSelectionResponse:
    try:
        return SessionService(db_session).select_tone(
            session_id,
            tone_profile_id=payload.tone_profile_id,
            tone_profile_slug=payload.tone_profile_slug,
            tone_profile_label=payload.tone_profile_label,
            origin=payload.origin,
        )
    except SessionNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    except SessionToneSelectionError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc


@router.post(
    "/{session_id}/story-brief",
    response_model=SessionStoryBriefResponse,
    status_code=status.HTTP_200_OK,
    summary="Persist a revisioned story brief for a story session",
)
def save_session_story_brief(
    session_id: str,
    payload: SaveSessionStoryBriefRequest,
    db_session: Annotated[Session, Depends(get_db_session)],
    brief_normalization_adapter: Annotated[
        BriefNormalizationAdapter, Depends(get_brief_normalization_adapter)
    ],
) -> SessionStoryBriefResponse:
    try:
        return SessionService(
            db_session,
            brief_normalization_service=BriefNormalizationService(
                adapter=brief_normalization_adapter
            ),
        ).save_story_brief(
            session_id,
            story_idea=payload.story_idea,
            desired_themes=payload.desired_themes,
            key_images=payload.key_images,
            audience_notes=payload.audience_notes,
            must_have_elements=payload.must_have_elements,
            raw_brief=payload.raw_brief,
            normalized_summary=payload.normalized_summary,
            normalized_preferences=payload.normalized_preferences,
            planning_notes=payload.planning_notes,
            edit_mode=payload.edit_mode,
            origin=payload.origin,
            provided_fields=payload.model_fields_set,
        )
    except SessionNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    except InvalidStageTransitionError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc
    except SessionStoryBriefSaveError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc


@router.post(
    "/{session_id}/story-setup",
    response_model=SessionStorySetupResponse,
    status_code=status.HTTP_200_OK,
    summary="Persist soft story setup targets for a story session",
)
def save_session_story_setup(
    session_id: str,
    payload: SaveSessionStorySetupRequest,
    db_session: Annotated[Session, Depends(get_db_session)],
) -> SessionStorySetupResponse:
    session_service = SessionService(db_session)

    try:
        result = StoryWorkflowToolService(db_session).execute(
            tool_name=StoryWorkflowToolName.UPDATE_SETUP_HEURISTICS,
            session_id=session_id,
            arguments=payload.model_dump(mode="json", exclude_unset=True),
        )
        snapshot = session_service.load_session_snapshot(session_id)
        event = _resolve_story_setup_response_event(
            session_service=session_service,
            session_id=session_id,
            story_setup_id=getattr(result, "story_setup_id", None),
        )
        return SessionStorySetupResponse(snapshot=snapshot, event=event)
    except SessionNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    except InvalidStageTransitionError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc
    except StoryWorkflowToolServiceError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc


@router.post(
    "/{session_id}/story-outline",
    response_model=SessionStoryOutlineResponse,
    status_code=status.HTTP_200_OK,
    summary="Persist an edited chapter or scene outline for a story session",
)
def save_session_story_outline(
    session_id: str,
    payload: SaveSessionStoryOutlineRequest,
    db_session: Annotated[Session, Depends(get_db_session)],
) -> SessionStoryOutlineResponse:
    session_service = SessionService(db_session)

    try:
        result = StoryWorkflowToolService(db_session).execute(
            tool_name=StoryWorkflowToolName.UPDATE_STORY_OUTLINE,
            session_id=session_id,
            arguments=payload.model_dump(mode="json", exclude_unset=True),
        )
        snapshot = session_service.load_session_snapshot(session_id)
        event = _resolve_story_outline_response_event(
            session_service=session_service,
            session_id=session_id,
            story_outline_id=getattr(result, "story_outline_id", None),
        )
        return SessionStoryOutlineResponse(snapshot=snapshot, event=event)
    except SessionNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    except InvalidStageTransitionError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc
    except StoryWorkflowToolServiceError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc


@router.post(
    "/{session_id}/composition/start",
    response_model=SessionCompositionResponse,
    status_code=status.HTTP_200_OK,
    summary="Queue a durable composition job for a story session",
)
def start_session_composition(
    session_id: str,
    payload: StartSessionCompositionRequest,
    db_session: Annotated[Session, Depends(get_db_session)],
) -> SessionCompositionResponse:
    session_service = SessionService(db_session)
    composition_jobs = CompositionJobService(db_session)

    try:
        if payload.mode == "rewrite":
            result = StoryWorkflowToolService(db_session).execute(
                tool_name=StoryWorkflowToolName.REWRITE_SEGMENTS,
                session_id=session_id,
                arguments={
                    "instructions": payload.instructions,
                    "rewrite_from_segment_index": payload.restart_from_segment_index,
                    "rewrite_to_segment_index": payload.rewrite_to_segment_index,
                    "downstream_regeneration_mode": payload.downstream_regeneration_mode,
                    "preserve_completed_segments": False,
                },
            )
        else:
            restart_from_segment_index = (
                payload.restart_from_segment_index
                if payload.mode == "fresh"
                else composition_jobs.resolve_continue_start_segment(session_id)
            )
            result = StoryWorkflowToolService(db_session).execute(
                tool_name=StoryWorkflowToolName.COMPOSE_NEXT_SEGMENT,
                session_id=session_id,
                arguments={
                    "instructions": payload.instructions,
                    "restart_from_segment_index": restart_from_segment_index,
                },
            )

        snapshot = session_service.load_session_snapshot(session_id)
        job_view = _resolve_composition_job_view(
            snapshot=snapshot,
            db_session=db_session,
            composition_job_id=result.composition_job_id,
        )
        event = _resolve_composition_response_event(
            session_service=session_service,
            session_id=session_id,
            composition_job_id=result.composition_job_id,
        )
        return SessionCompositionResponse(snapshot=snapshot, event=event, job=job_view)
    except SessionNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    except (CompositionJobStateError, StoryWorkflowToolServiceError) as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc


@router.post(
    "/{session_id}/composition/{composition_job_id}/pause",
    response_model=SessionCompositionResponse,
    status_code=status.HTTP_200_OK,
    summary="Pause a durable composition job",
)
def pause_session_composition(
    session_id: str,
    composition_job_id: str,
    db_session: Annotated[Session, Depends(get_db_session)],
) -> SessionCompositionResponse:
    session_service = SessionService(db_session)

    try:
        CompositionJobService(db_session).pause_job(session_id, composition_job_id)
        snapshot = session_service.load_session_snapshot(session_id)
        job_view = _resolve_composition_job_view(
            snapshot=snapshot,
            db_session=db_session,
            composition_job_id=composition_job_id,
        )
        event = _resolve_composition_response_event(
            session_service=session_service,
            session_id=session_id,
            composition_job_id=composition_job_id,
        )
        return SessionCompositionResponse(snapshot=snapshot, event=event, job=job_view)
    except SessionNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    except CompositionJobNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    except CompositionJobStateError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc


@router.post(
    "/{session_id}/composition/{composition_job_id}/resume",
    response_model=SessionCompositionResponse,
    status_code=status.HTTP_200_OK,
    summary="Resume a paused durable composition job",
)
def resume_session_composition(
    session_id: str,
    composition_job_id: str,
    db_session: Annotated[Session, Depends(get_db_session)],
) -> SessionCompositionResponse:
    session_service = SessionService(db_session)

    try:
        CompositionJobService(db_session).resume_job(session_id, composition_job_id)
        snapshot = session_service.load_session_snapshot(session_id)
        job_view = _resolve_composition_job_view(
            snapshot=snapshot,
            db_session=db_session,
            composition_job_id=composition_job_id,
        )
        event = _resolve_composition_response_event(
            session_service=session_service,
            session_id=session_id,
            composition_job_id=composition_job_id,
        )
        return SessionCompositionResponse(snapshot=snapshot, event=event, job=job_view)
    except SessionNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    except CompositionJobNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    except CompositionJobStateError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc


@router.post(
    "/{session_id}/composition/{composition_job_id}/cancel",
    response_model=SessionCompositionResponse,
    status_code=status.HTTP_200_OK,
    summary="Cancel a durable composition job",
)
def cancel_session_composition(
    session_id: str,
    composition_job_id: str,
    db_session: Annotated[Session, Depends(get_db_session)],
) -> SessionCompositionResponse:
    session_service = SessionService(db_session)

    try:
        CompositionJobService(db_session).cancel_job(
            session_id,
            composition_job_id,
            reason="Cancelled before the current composition pass finished.",
        )
        snapshot = session_service.load_session_snapshot(session_id)
        job_view = _resolve_composition_job_view(
            snapshot=snapshot,
            db_session=db_session,
            composition_job_id=composition_job_id,
        )
        event = _resolve_composition_response_event(
            session_service=session_service,
            session_id=session_id,
            composition_job_id=composition_job_id,
        )
        return SessionCompositionResponse(snapshot=snapshot, event=event, job=job_view)
    except SessionNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    except CompositionJobNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    except CompositionJobStateError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc


@router.post(
    "/{session_id}/composition/{composition_job_id}/redirect",
    response_model=SessionCompositionResponse,
    status_code=status.HTTP_200_OK,
    summary="Redirect the active composition job into a rewrite pass",
)
def redirect_session_composition(
    session_id: str,
    composition_job_id: str,
    payload: RedirectSessionCompositionRequest,
    db_session: Annotated[Session, Depends(get_db_session)],
) -> SessionCompositionResponse:
    session_service = SessionService(db_session)
    composition_jobs = CompositionJobService(db_session)

    try:
        result = composition_jobs.request_redirect(
            session_id,
            composition_job_id,
            instructions=payload.instructions,
            rewrite_from_segment_index=payload.rewrite_from_segment_index,
            rewrite_to_segment_index=payload.rewrite_to_segment_index,
            downstream_regeneration_mode=(
                CompositionDownstreamMode(payload.downstream_regeneration_mode)
                if payload.downstream_regeneration_mode is not None
                else None
            ),
            origin=payload.origin,
        )
        snapshot = session_service.load_session_snapshot(session_id)
        job_view = _resolve_composition_job_view(
            snapshot=snapshot,
            db_session=db_session,
            composition_job_id=result.response_job_id,
        )
        event = _resolve_composition_response_event(
            session_service=session_service,
            session_id=session_id,
            composition_job_id=result.response_job_id,
        )
        return SessionCompositionResponse(snapshot=snapshot, event=event, job=job_view)
    except SessionNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    except CompositionJobNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    except (CompositionJobStateError, StoryWorkflowToolServiceError) as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc


@router.post(
    "/{session_id}/composition/{composition_job_id}/accept",
    response_model=SessionCompositionResponse,
    status_code=status.HTTP_200_OK,
    summary="Accept a completed rewrite candidate into the manuscript",
)
def accept_session_composition_rewrite(
    session_id: str,
    composition_job_id: str,
    payload: AcceptRewriteSessionCompositionRequest,
    db_session: Annotated[Session, Depends(get_db_session)],
) -> SessionCompositionResponse:
    session_service = SessionService(db_session)

    try:
        job = CompositionJobService(db_session).accept_rewrite_job(
            session_id,
            composition_job_id,
            origin=payload.origin,
        )
        snapshot = session_service.load_session_snapshot(session_id)
        job_view = _resolve_composition_job_view(
            snapshot=snapshot,
            db_session=db_session,
            composition_job_id=job.id,
        )
        event = _resolve_latest_composition_stage_event(
            session_service=session_service,
            session_id=session_id,
        )
        return SessionCompositionResponse(snapshot=snapshot, event=event, job=job_view)
    except SessionNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    except CompositionJobNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    except CompositionJobStateError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc


@router.post(
    "/{session_id}/composition/{composition_job_id}/reject",
    response_model=SessionCompositionResponse,
    status_code=status.HTTP_200_OK,
    summary="Reject a completed rewrite candidate and keep the current manuscript",
)
def reject_session_composition_rewrite(
    session_id: str,
    composition_job_id: str,
    payload: RejectRewriteSessionCompositionRequest,
    db_session: Annotated[Session, Depends(get_db_session)],
) -> SessionCompositionResponse:
    session_service = SessionService(db_session)

    try:
        job = CompositionJobService(db_session).reject_rewrite_job(
            session_id,
            composition_job_id,
            origin=payload.origin,
        )
        snapshot = session_service.load_session_snapshot(session_id)
        job_view = _resolve_composition_job_view(
            snapshot=snapshot,
            db_session=db_session,
            composition_job_id=job.id,
        )
        event = _resolve_latest_composition_stage_event(
            session_service=session_service,
            session_id=session_id,
        )
        return SessionCompositionResponse(snapshot=snapshot, event=event, job=job_view)
    except SessionNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    except CompositionJobNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    except CompositionJobStateError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc


@router.post(
    "/{session_id}/composition/segments/{segment_index}/versions/{version_id}/select",
    response_model=SessionCompositionResponse,
    status_code=status.HTTP_200_OK,
    summary="Select a saved segment revision as the active manuscript text",
)
def select_session_composition_segment_version(
    session_id: str,
    segment_index: int,
    version_id: str,
    payload: SelectCompositionSegmentVersionRequest,
    db_session: Annotated[Session, Depends(get_db_session)],
) -> SessionCompositionResponse:
    session_service = SessionService(db_session)

    try:
        job = CompositionJobService(db_session).select_active_segment_version(
            session_id,
            segment_index=segment_index,
            version_id=version_id,
            origin=payload.origin,
        )
        snapshot = session_service.load_session_snapshot(session_id)
        job_view = _resolve_composition_job_view(
            snapshot=snapshot,
            db_session=db_session,
            composition_job_id=job.id,
        )
        event = _resolve_latest_composition_stage_event(
            session_service=session_service,
            session_id=session_id,
        )
        return SessionCompositionResponse(snapshot=snapshot, event=event, job=job_view)
    except SessionNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    except CompositionJobNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    except CompositionJobStateError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc


@router.post(
    "/{session_id}/plan-revisions/{revision_number}/restore",
    response_model=SessionSelectionResponse,
    status_code=status.HTTP_200_OK,
    summary="Restore a previously captured planning snapshot",
)
def restore_session_plan_revision(
    session_id: str,
    revision_number: int,
    payload: RestoreSessionPlanRevisionRequest,
    db_session: Annotated[Session, Depends(get_db_session)],
) -> SessionSelectionResponse:
    try:
        return SessionService(db_session).restore_plan_revision(
            session_id,
            revision_number=revision_number,
            origin=payload.origin,
        )
    except SessionNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    except SessionPlanRevisionError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc


@router.post(
    "/{session_id}/pitches/generate",
    response_model=SessionPitchGenerationResponse,
    status_code=status.HTTP_200_OK,
    summary="Generate a durable pitch batch for a story session",
)
def generate_session_pitches(
    session_id: str,
    payload: GenerateSessionPitchesRequest,
    db_session: Annotated[Session, Depends(get_db_session)],
    pitch_generation_adapter: Annotated[
        PitchGenerationAdapter,
        Depends(get_pitch_generation_adapter),
    ],
) -> SessionPitchGenerationResponse:
    try:
        return SessionService(db_session).generate_pitches(
            session_id,
            candidate_count=payload.candidate_count,
            guidance=payload.guidance,
            preserve_selected_pitch=payload.preserve_selected_pitch,
            origin=payload.origin,
            pitch_generation_service=PitchGenerationService(
                adapter=pitch_generation_adapter,
            ),
        )
    except SessionNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    except InvalidStageTransitionError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc
    except SessionPitchGenerationError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc


@router.post(
    "/{session_id}/pitches/refine",
    response_model=SessionSelectionResponse,
    status_code=status.HTTP_200_OK,
    summary="Generate and select a refined pitch for a story session",
)
def refine_session_pitch(
    session_id: str,
    payload: RefineSessionPitchRequest,
    db_session: Annotated[Session, Depends(get_db_session)],
    pitch_generation_adapter: Annotated[
        PitchGenerationAdapter,
        Depends(get_pitch_generation_adapter),
    ],
) -> SessionSelectionResponse:
    try:
        return SessionService(db_session).refine_pitch(
            session_id,
            pitch_id=payload.pitch_id,
            generation_key=payload.generation_key,
            pitch_index=payload.pitch_index,
            title=payload.title,
            instructions=payload.instructions,
            origin=payload.origin,
            pitch_generation_service=PitchGenerationService(
                adapter=pitch_generation_adapter,
            ),
        )
    except SessionNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    except InvalidStageTransitionError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc
    except (SessionPitchSelectionError, SessionPitchGenerationError) as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc


@router.post(
    "/{session_id}/selections/pitch",
    response_model=SessionSelectionResponse,
    status_code=status.HTTP_200_OK,
    summary="Persist the selected pitch for a story session",
)
def select_session_pitch(
    session_id: str,
    payload: SelectSessionPitchRequest,
    db_session: Annotated[Session, Depends(get_db_session)],
) -> SessionSelectionResponse:
    try:
        return SessionService(db_session).select_pitch(
            session_id,
            pitch_id=payload.pitch_id,
            generation_key=payload.generation_key,
            pitch_index=payload.pitch_index,
            title=payload.title,
            origin=payload.origin,
        )
    except SessionNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    except InvalidStageTransitionError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc
    except SessionPitchSelectionError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc
    except InvalidStageTransitionError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc


@router.post(
    "/{session_id}/characters/generate",
    response_model=SessionCharacterSheetGenerationResponse,
    status_code=status.HTTP_200_OK,
    summary="Generate a durable character-sheet batch for a story session",
)
def generate_session_character_sheets(
    session_id: str,
    payload: GenerateSessionCharacterSheetsRequest,
    db_session: Annotated[Session, Depends(get_db_session)],
    character_generation_adapter: Annotated[
        CharacterGenerationAdapter,
        Depends(get_character_generation_adapter),
    ],
) -> SessionCharacterSheetGenerationResponse:
    try:
        return SessionService(db_session).generate_character_sheets(
            session_id,
            candidate_count=payload.candidate_count,
            guidance=payload.guidance,
            origin=payload.origin,
            character_generation_service=CharacterGenerationService(
                adapter=character_generation_adapter,
            ),
        )
    except SessionNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    except InvalidStageTransitionError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc
    except SessionCharacterSheetGenerationError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc


@router.post(
    "/{session_id}/characters/refine",
    response_model=SessionSelectionResponse,
    status_code=status.HTTP_200_OK,
    summary="Generate and select a refined character sheet for a story session",
)
def refine_session_character_sheet(
    session_id: str,
    payload: RefineSessionCharacterSheetRequest,
    db_session: Annotated[Session, Depends(get_db_session)],
    character_generation_adapter: Annotated[
        CharacterGenerationAdapter,
        Depends(get_character_generation_adapter),
    ],
) -> SessionSelectionResponse:
    try:
        return SessionService(db_session).refine_character_sheet(
            session_id,
            character_sheet_id=payload.character_sheet_id,
            revision_number=payload.revision_number,
            title=payload.title,
            instructions=payload.instructions,
            focus_character_names=payload.focus_character_names,
            change_summary=payload.change_summary,
            change_impact=payload.change_impact,
            origin=payload.origin,
            character_generation_service=CharacterGenerationService(
                adapter=character_generation_adapter,
            ),
        )
    except SessionNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    except InvalidStageTransitionError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc
    except (SessionCharacterSheetSelectionError, SessionCharacterSheetGenerationError) as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc


@router.post(
    "/{session_id}/selections/character-sheet",
    response_model=SessionSelectionResponse,
    status_code=status.HTTP_200_OK,
    summary="Persist the selected character sheet for a story session",
)
def select_session_character_sheet(
    session_id: str,
    payload: SelectSessionCharacterSheetRequest,
    db_session: Annotated[Session, Depends(get_db_session)],
) -> SessionSelectionResponse:
    try:
        return SessionService(db_session).select_character_sheet(
            session_id,
            character_sheet_id=payload.character_sheet_id,
            revision_number=payload.revision_number,
            title=payload.title,
            origin=payload.origin,
        )
    except SessionNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    except InvalidStageTransitionError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc
    except SessionCharacterSheetSelectionError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc


@router.post(
    "/{session_id}/beats/generate",
    response_model=SessionBeatSheetGenerationResponse,
    status_code=status.HTTP_200_OK,
    summary="Generate a durable beat-sheet revision for a story session",
)
def generate_session_beat_sheet(
    session_id: str,
    payload: GenerateSessionBeatSheetRequest,
    db_session: Annotated[Session, Depends(get_db_session)],
    beat_sheet_generation_adapter: Annotated[
        BeatSheetGenerationAdapter,
        Depends(get_beat_sheet_generation_adapter),
    ],
) -> SessionBeatSheetGenerationResponse:
    try:
        return SessionService(db_session).generate_beat_sheet(
            session_id,
            guidance=payload.guidance,
            focus_beats=payload.focus_beats,
            bedtime_goal=payload.bedtime_goal,
            origin=payload.origin,
            beat_sheet_generation_service=BeatSheetGenerationService(
                adapter=beat_sheet_generation_adapter,
            ),
        )
    except SessionNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    except InvalidStageTransitionError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc
    except SessionBeatSheetGenerationError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc


@router.post(
    "/{session_id}/beats/refine",
    response_model=SessionSelectionResponse,
    status_code=status.HTTP_200_OK,
    summary="Generate and select a refined beat sheet for a story session",
)
def refine_session_beat_sheet(
    session_id: str,
    payload: RefineSessionBeatSheetRequest,
    db_session: Annotated[Session, Depends(get_db_session)],
    beat_sheet_generation_adapter: Annotated[
        BeatSheetGenerationAdapter,
        Depends(get_beat_sheet_generation_adapter),
    ],
) -> SessionSelectionResponse:
    try:
        return SessionService(db_session).refine_beat_sheet(
            session_id,
            beat_sheet_id=payload.beat_sheet_id,
            revision_number=payload.revision_number,
            instructions=payload.instructions,
            beat_names=payload.beat_names,
            bedtime_goal=payload.bedtime_goal,
            origin=payload.origin,
            beat_sheet_generation_service=BeatSheetGenerationService(
                adapter=beat_sheet_generation_adapter,
            ),
        )
    except SessionNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    except InvalidStageTransitionError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc
    except (SessionBeatSheetSelectionError, SessionBeatSheetGenerationError) as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc


@router.post(
    "/{session_id}/beats/edit",
    response_model=SessionBeatSheetUpdateResponse,
    status_code=status.HTTP_200_OK,
    summary="Persist structured edits to a saved beat sheet",
)
def edit_session_beat_sheet(
    session_id: str,
    payload: EditSessionBeatSheetRequest,
    db_session: Annotated[Session, Depends(get_db_session)],
) -> SessionBeatSheetUpdateResponse:
    try:
        return SessionService(db_session).edit_beat_sheet(
            session_id,
            payload=payload,
        )
    except SessionNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    except InvalidStageTransitionError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc
    except (
        SessionBeatSheetEditError,
        SessionBeatSheetSelectionError,
    ) as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc


@router.post(
    "/{session_id}/selections/beat-sheet",
    response_model=SessionSelectionResponse,
    status_code=status.HTTP_200_OK,
    summary="Persist the selected beat sheet for a story session",
)
def select_session_beat_sheet(
    session_id: str,
    payload: SelectSessionBeatSheetRequest,
    db_session: Annotated[Session, Depends(get_db_session)],
) -> SessionSelectionResponse:
    try:
        return SessionService(db_session).select_beat_sheet(
            session_id,
            beat_sheet_id=payload.beat_sheet_id,
            revision_number=payload.revision_number,
            origin=payload.origin,
        )
    except SessionNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    except InvalidStageTransitionError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc
    except SessionBeatSheetSelectionError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc


@router.post(
    "/{session_id}/ui-actions",
    response_model=SessionEventView,
    status_code=status.HTTP_201_CREATED,
    summary="Record a durable UI-originated action",
)
def record_session_ui_action(
    session_id: str,
    payload: RecordSessionUIActionRequest,
    db_session: Annotated[Session, Depends(get_db_session)],
) -> SessionEventView:
    try:
        return SessionService(db_session).record_ui_action(
            session_id,
            action=payload.action,
            stage=payload.stage,
            control_id=payload.control_id,
            value_summary=payload.value_summary,
            origin=payload.origin,
        )
    except SessionNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.post(
    "/{session_id}/context-updates",
    response_model=SessionContextUpdateResponse,
    status_code=status.HTTP_200_OK,
    summary="Apply a durable UI-originated context update",
)
def apply_session_context_update(
    session_id: str,
    payload: SessionContextUpdateRequest,
    db_session: Annotated[Session, Depends(get_db_session)],
) -> SessionContextUpdateResponse:
    try:
        return SessionService(db_session).apply_context_update(
            session_id,
            payload=payload,
        )
    except SessionNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    except UnsupportedSessionContextUpdateError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc
    except InvalidStageTransitionError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc


@router.post(
    "/{session_id}/chat/intents",
    response_model=ParsedChatIntentResponse,
    summary="Parse a chat message into structured UI actions",
)
def parse_chat_intents(
    session_id: str,
    payload: ParseChatIntentRequest,
    request: Request,
    db_session: Annotated[Session, Depends(get_db_session)],
) -> ParsedChatIntentResponse:
    intent_parser: IntentParserAdapter | None = None
    if payload.explicit_command is None:
        intent_parser = get_intent_parser_adapter(request)

    try:
        return SessionIntentParserService(db_session, intent_parser).parse_user_message(
            session_id,
            message=payload.message,
            explicit_command=payload.explicit_command,
        )
    except SessionNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.post(
    "/{session_id}/actions/evaluate",
    response_model=SessionActionPolicyEvaluation,
    summary="Evaluate proposed UI actions against durable session policy",
)
def evaluate_session_actions(
    session_id: str,
    payload: SessionActionPolicyEvaluationRequest,
    db_session: Annotated[Session, Depends(get_db_session)],
) -> SessionActionPolicyEvaluation:
    try:
        return SessionActionPolicyService(db_session).evaluate_request(
            session_id,
            request=payload,
        )
    except SessionNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


def _resolve_story_setup_response_event(
    *,
    session_service: SessionService,
    session_id: str,
    story_setup_id: str | None,
) -> SessionEventView:
    history = session_service.load_session_history(session_id, limit=12)

    if story_setup_id is not None:
        for event in reversed(history.events):
            if event.stage != WorkflowStage.STORY_SETUP:
                continue
            if event.event_type != "selection.recorded":
                continue
            if getattr(event.payload, "selection_id", None) == story_setup_id:
                return event

    for event in reversed(history.events):
        if event.stage == WorkflowStage.STORY_SETUP:
            return event

    raise RuntimeError("story setup save did not produce a replayable event")


def _resolve_story_outline_response_event(
    *,
    session_service: SessionService,
    session_id: str,
    story_outline_id: str | None,
) -> SessionEventView:
    history = session_service.load_session_history(session_id, limit=12)

    if story_outline_id is not None:
        for event in reversed(history.events):
            if event.stage != WorkflowStage.STORY_SETUP:
                continue
            if event.event_type != "content.user_edit.recorded":
                continue
            if getattr(event.payload, "target_id", None) == story_outline_id:
                return event

    for event in reversed(history.events):
        if event.stage == WorkflowStage.STORY_SETUP:
            return event

    raise RuntimeError("story outline save did not produce a replayable event")


def _resolve_composition_response_event(
    *,
    session_service: SessionService,
    session_id: str,
    composition_job_id: str,
) -> SessionEventView:
    history = session_service.load_session_history(session_id, limit=20)

    for event in reversed(history.events):
        if event.stage != WorkflowStage.COMPOSITION:
            continue
        if event.event_type != "composition.progress.recorded":
            continue
        if getattr(event.payload, "job_id", None) == composition_job_id:
            return event

    for event in reversed(history.events):
        if event.stage == WorkflowStage.COMPOSITION:
            return event

    raise RuntimeError("composition operation did not produce a replayable event")


def _resolve_latest_composition_stage_event(
    *,
    session_service: SessionService,
    session_id: str,
) -> SessionEventView:
    history = session_service.load_session_history(session_id, limit=20)

    for event in reversed(history.events):
        if event.stage == WorkflowStage.COMPOSITION:
            return event

    raise RuntimeError("composition operation did not produce a replayable event")


def _resolve_composition_job_view(
    *,
    snapshot: SessionSnapshot,
    db_session: Session,
    composition_job_id: str,
):
    if (
        snapshot.active_composition_job is not None
        and snapshot.active_composition_job.id == composition_job_id
    ):
        return snapshot.active_composition_job
    if (
        snapshot.latest_composition_job is not None
        and snapshot.latest_composition_job.id == composition_job_id
    ):
        return snapshot.latest_composition_job

    job = db_session.get(CompositionJob, composition_job_id)
    if job is None:
        raise CompositionJobNotFoundError(
            f"composition job {composition_job_id!r} was not found",
        )
    job_view = build_composition_job_view(job)
    if job_view is None:
        raise CompositionJobNotFoundError(
            f"composition job {composition_job_id!r} was not found",
        )
    return job_view

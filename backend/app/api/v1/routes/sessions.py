from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy.orm import Session

from app.ai import BriefNormalizationAdapter, IntentParserAdapter, PitchGenerationAdapter
from app.api.dependencies import (
    get_brief_normalization_adapter,
    get_db_session,
    get_intent_parser_adapter,
    get_pitch_generation_adapter,
)
from app.models import (
    CreateSessionRequest,
    GenerateSessionPitchesRequest,
    ParseChatIntentRequest,
    ParsedChatIntentResponse,
    RecentSessionSummary,
    RecordSessionUIActionRequest,
    SaveSessionStoryBriefRequest,
    SelectSessionGenreRequest,
    SelectSessionPitchRequest,
    SelectSessionToneRequest,
    SessionActionPolicyEvaluation,
    SessionActionPolicyEvaluationRequest,
    SessionContextUpdateRequest,
    SessionContextUpdateResponse,
    SessionEventView,
    SessionHistoryView,
    SessionHydrationView,
    SessionPitchGenerationResponse,
    SessionSelectionResponse,
    SessionSnapshot,
    SessionStoryBriefResponse,
)
from app.services import (
    BriefNormalizationService,
    PitchGenerationService,
    SessionActionPolicyService,
    SessionIntentParserService,
)
from app.services.session_hydration import SessionHydrationNotFoundError, SessionHydrationService
from app.services.sessions import (
    InvalidStageTransitionError,
    SessionGenreSelectionError,
    SessionNotFoundError,
    SessionPitchGenerationError,
    SessionPitchSelectionError,
    SessionService,
    SessionStoryBriefSaveError,
    SessionToneSelectionError,
    UnsupportedSessionContextUpdateError,
)

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

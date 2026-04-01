from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.ai import IntentParserAdapter
from app.api.dependencies import get_db_session, get_intent_parser_adapter
from app.models import (
    CreateSessionRequest,
    ParseChatIntentRequest,
    ParsedChatIntentResponse,
    RecentSessionSummary,
    SessionActionPolicyEvaluation,
    SessionActionPolicyEvaluationRequest,
    SessionSnapshot,
)
from app.services import SessionActionPolicyService, SessionIntentParserService
from app.services.sessions import SessionNotFoundError, SessionService

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
    "/{session_id}/chat/intents",
    response_model=ParsedChatIntentResponse,
    summary="Parse a chat message into structured UI actions",
)
def parse_chat_intents(
    session_id: str,
    payload: ParseChatIntentRequest,
    db_session: Annotated[Session, Depends(get_db_session)],
    intent_parser: Annotated[IntentParserAdapter, Depends(get_intent_parser_adapter)],
) -> ParsedChatIntentResponse:
    try:
        return SessionIntentParserService(db_session, intent_parser).parse_user_message(
            session_id,
            message=payload.message,
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

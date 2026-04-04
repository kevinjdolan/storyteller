from __future__ import annotations

import asyncio
from uuid import uuid4

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from pydantic import ValidationError

from app.db.session import get_session_factory
from app.models.events import EventActorType, SessionEventActor
from app.models.identity import LOCAL_DEVELOPMENT_IDENTITY, RequestIdentity
from app.models.realtime import RealtimeDeliveryMode, SessionSubscriptionRequest
from app.services.session_realtime import (
    CompositionChunkCursor,
    SessionRealtimeService,
)
from app.services.sessions import SessionNotFoundError, SessionService

router = APIRouter(prefix="/sessions", tags=["session-events"])

_SESSION_EVENTS_POLL_INTERVAL_SECONDS = 0.08


@router.websocket("/events/ws")
async def session_events_websocket(websocket: WebSocket) -> None:
    await websocket.accept()
    identity = _resolve_websocket_identity(websocket)

    try:
        subscription = SessionSubscriptionRequest.model_validate(
            await websocket.receive_json(),
        )
    except ValidationError as exc:
        await websocket.close(code=1008, reason=str(exc))
        return
    except WebSocketDisconnect:
        return

    session_factory = get_session_factory()
    try:
        with session_factory() as session:
            SessionService(session, owner_id=identity.subject).load_session_snapshot(
                subscription.session_id
            )
            realtime = SessionRealtimeService(
                session,
                local_actor=SessionEventActor(
                    actor_type=EventActorType.USER,
                    actor_id=identity.subject,
                ),
            )
            state = realtime.build_subscription(
                session_id=subscription.session_id,
                connection_id=f"conn-{uuid4()}",
                last_sequence_number=subscription.last_sequence_number,
                request_id=subscription.request_id,
                tab_id=subscription.tab_id,
            )
    except SessionNotFoundError as exc:
        await websocket.close(code=1008, reason=str(exc))
        return

    await websocket.send_json(state.ack.model_dump(mode="json"))
    for event in state.replay_events:
        await websocket.send_json(event.model_dump(mode="json"))

    last_sequence_number = state.latest_sequence_number or subscription.last_sequence_number
    chunk_cursor = CompositionChunkCursor()

    while True:
        try:
            await asyncio.wait_for(
                websocket.receive_text(),
                timeout=_SESSION_EVENTS_POLL_INTERVAL_SECONDS,
            )
            continue
        except asyncio.TimeoutError:
            pass
        except WebSocketDisconnect:
            return

        with session_factory() as session:
            realtime = SessionRealtimeService(
                session,
                local_actor=SessionEventActor(
                    actor_type=EventActorType.USER,
                    actor_id=identity.subject,
                ),
            )
            live_events = realtime.list_realtime_events(
                subscription.session_id,
                after_sequence_number=last_sequence_number,
                delivery=RealtimeDeliveryMode.LIVE,
            )
            chunk_events, chunk_cursor = realtime.read_composition_chunk_events(
                subscription.session_id,
                cursor=chunk_cursor,
            )

        for event in live_events:
            await websocket.send_json(event.model_dump(mode="json"))
            last_sequence_number = event.sequence_number

        for event in chunk_events:
            await websocket.send_json(event.model_dump(mode="json"))


def _resolve_websocket_identity(websocket: WebSocket) -> RequestIdentity:
    identity = getattr(websocket.app.state, "request_identity", None)
    if isinstance(identity, RequestIdentity):
        return identity

    return LOCAL_DEVELOPMENT_IDENTITY

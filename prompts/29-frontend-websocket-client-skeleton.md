# 29 — Frontend WebSocket Client Skeleton

Read `base_prompt.md` first and preserve all prior prompt work.

## Objective

Lay the groundwork for live session updates on the frontend without fully wiring the backend transport yet.

## Build
- Create a WebSocket client abstraction that can connect to a session-specific channel, reconnect, and dispatch typed events into the frontend state layer.
- Add a thin reducer or event handler layer that can merge stage updates, chat events, and progress events into the current session state.
- Expose connection status to the UI so the workspace can show whether live updates are healthy.

## Deliverables

- WebSocket client abstraction
- Event reducer wiring
- Connection status indicator

## Acceptance checks

- The frontend can accept typed live events without each component opening its own socket.
- Reconnect behavior is thought through at least minimally.
- Connection state is visible for debugging and later user trust.

## Notes

Keep transport code isolated from presentation components.

## Suggested commit label

`feat(prompt-29): frontend websocket client skeleton`

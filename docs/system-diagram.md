# System Diagram

This diagram shows the intended runtime shape for Storyteller after the core session, worker, and realtime prompts are built. It documents where session resume, durable event history, realtime delivery, and long-running jobs belong.

```mermaid
flowchart LR
    Browser["Browser UI<br/>React + Vite<br/>sessions home, chat pane, workflow pane"]
    API["FastAPI API<br/>routes, policy checks, session reads/writes"]
    WS["WebSocket session stream<br/>replay recent events + deliver live progress"]
    Worker["Worker process<br/>composition jobs, audio jobs, retries, interruption"]
    Postgres[("PostgreSQL<br/>sessions, workflow state,<br/>durable event history,<br/>job records, asset metadata")]
    GCS[("File-backed GCS emulator<br/>story exports, audio segments,<br/>final artifacts")]
    Gemini["Gemini adapters<br/>planning, composition, narration"]

    Browser -->|"HTTP actions and reads"| API
    API -->|"resume session snapshot"| Browser
    Browser <-->|"subscribe / receive live updates"| WS

    API -->|"read and write durable state"| Postgres
    WS -->|"replay recent events and current job state"| Postgres

    API -->|"store asset metadata and create job records"| Postgres
    Worker -->|"claim jobs, persist partial outputs,<br/>append durable events"| Postgres

    Worker -->|"write and assemble artifacts"| GCS
    API -->|"serve artifact metadata and download links"| GCS

    Worker -->|"planning, composition, TTS calls"| Gemini
    API -. "backend-owned model config and policy" .-> Gemini
```

## Read This Diagram As

- The browser never calls Gemini directly.
- Resume starts from PostgreSQL session state plus durable event history.
- WebSockets deliver progress, but durable state still lives in PostgreSQL and object storage.
- Long-running generation belongs in the worker process, not inside request handlers.
- Artifacts live in object storage while PostgreSQL keeps the references and lifecycle state.

## Soft-Constraint Reminder

Word count, runtime, and chapter count are soft planning hints. They shape prompts and estimates, but the system should favor story quality, bedtime tone, and coherent pacing over exact numeric compliance.

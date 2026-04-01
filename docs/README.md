# Docs

This directory holds product notes, architecture notes, ADRs, diagrams, and other reviewer-oriented documentation.

Current entrypoints:

- `product-brief.md`: product expectations and workflow
- `architecture-overview.md`: target system shape and durable boundaries
- `domain-model.md`: durable session entities, workflow-stage contract, and stage-state rules
- `chat-to-ui-actions.md`: proposed action contract, action catalog, default confirmation policy, and deterministic action-policy evaluator
- `chat-to-ui-actions.schema.json`: machine-readable schema bundle for chat-to-UI proposed actions
- `event-taxonomy.md`: append-only event families, payload versioning rules, and helper usage
- `realtime-events.md`: session-channel contract, live event families, replay rules, and local auth assumptions
- `realtime-events.schema.json`: machine-readable schema bundle for subscription frames and session events
- `genre-tone-catalog.md`: curated catalog provenance, editing rules, and seed command
- `storage-buckets-and-prefixes.md`: bucket roles, stable object-key conventions, and storage usage
- `system-diagram.md`: one-page runtime diagram for browser, API, worker, storage, and Gemini flows
- `contributing.md`: shared quality commands and code-style conventions
- `adr/`: architecture decision records, starting with the core runtime architecture ADR

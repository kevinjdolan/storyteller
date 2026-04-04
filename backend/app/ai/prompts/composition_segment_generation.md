Return JSON only. Do not include markdown, comments, or prose outside the schema.

You are drafting one bedtime-story segment inside a durable segmented writing engine.

Rules:
- Write only the requested segment, never the whole story.
- Use the structured carryover summaries instead of trying to restate the full draft so far.
- Honor the accepted plan, continuity facts, and local outline-card goals.
- Keep the narration calm, clear, and bedtime-safe even when tension is present.
- Let the accepted_text be clean, final prose suitable for durable persistence.
- Let the raw_text capture the model's first-pass segment draft before any light cleanup.
- Let the carryover_summary be a compact handoff for the next segment. It should preserve facts, emotional state, open promises, and anything the next segment must remember.

Output expectations:
- `raw_text`: substantial prose for the current segment only.
- `accepted_text`: final persisted prose for the current segment only.
- `carryover_summary`: 2-4 sentences, concise and durable.

Prompt context JSON:
${composition_segment_context_json}

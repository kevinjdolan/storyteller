# Segmented Writing Context Carryover

The composition runtime now treats each outline card as a durable writing segment and carries
forward a structured summary instead of concatenating the full draft so far into every prompt.

## Strategy

For each segment run, the backend refreshes two context layers:

1. The current plan snapshot
   - Re-assembles the composition prompt package for the active outline card.
   - Pulls the current genre, tone, brief, selected pitch, selected character sheet, beat sheet,
     story setup, outline card, and continuity bible pointers.

2. The session-level carryover context
   - Loads the latest completed segment revision for each earlier segment index.
   - Extracts a durable `accepted_summary` for each prior segment.
   - Builds a compact `story_so_far_summary` from the last few accepted summaries.
   - Preserves the `latest_accepted_summary` as the immediate handoff.

The runtime stores this carryover under `composition_segments.payload.context_carryover` so later
rewrites can inspect the exact structured input that was used when a segment was generated.

## Why This Shape

This keeps the generation context controllable:

- Rewrites do not depend on replaying the entire prior draft verbatim.
- Segment prompts stay bounded even as the story gets longer.
- The carryover summary becomes a durable review surface for later prompts and tooling.
- The session can compile the final story from the latest accepted segment revision at each index.

## Durable Segment Record

Each `composition_segments` row now stores:

- `raw_generated_text`: the first-pass generated segment text
- `accepted_text`: the persisted segment prose used for compilation and later playback/export
- `accepted_summary`: the compact handoff summary for downstream segments
- `text_content`: the streamed accepted draft body kept for backward compatibility
- `payload.context_carryover`: the structured prior-segment context that fed this run

The object-storage side also keeps a `composition_segment` asset per completed segment revision,
with evaluation metadata and the accepted handoff summary.

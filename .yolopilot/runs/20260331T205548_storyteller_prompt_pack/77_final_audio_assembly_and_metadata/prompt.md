# 77 — Final Audio Assembly and Metadata

Read `base_prompt.md` first and preserve all prior prompt work.

## Objective

Assemble the completed audio segments into a final deliverable and record useful metadata about the output.

## Build
- Concatenate or otherwise assemble narration segments in the correct order and apply optional music mixing if enabled.
- Store the final audio asset in object storage and create a durable asset record with runtime, media type, and generation details.
- Mark any superseded final outputs when the user regenerates audio after story changes.

## Deliverables

- Final audio assembly service
- Final asset metadata capture
- Regeneration/update rules for final audio outputs

## Acceptance checks

- The app can produce one coherent final audio file from segmented work.
- The final asset is easy to download and play in the UI.
- Regenerated audio does not silently overwrite history without trace.

## Notes

Treat the final compiled audio as a first-class artifact.

## Suggested commit label

`feat(prompt-77): final audio assembly`

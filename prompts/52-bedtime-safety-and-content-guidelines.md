# 52 — Bedtime Safety and Content Guidelines

Read `base_prompt.md` first and preserve all prior prompt work.

## Objective

Add product rules that keep generated bedtime stories emotionally safe, age-appropriate, and soothing even when they include tension or mystery.

## Build
- Define guidance for maximum scare level, violence avoidance, reassuring resolution, and emotional repair after tension.
- Store these guidelines centrally so pitch, character, beat, composition, and audio prompts can all reuse them.
- Allow future expansion for audience-age presets even if the first version stays simple.

## Deliverables

- `docs/bedtime-guidelines.md`
- Reusable backend prompt fragments or policy constants
- A plan for audience-age defaults

## Acceptance checks

- The product has explicit rules for what makes a story bedtime-safe.
- These rules are reusable across the pipeline instead of copied into random prompts.
- The guidance still leaves room for adventure and wonder.

## Notes

Bedtime-safe does not mean flat or boring.

## Suggested commit label

`feat(prompt-52): bedtime safety and content guidelines`

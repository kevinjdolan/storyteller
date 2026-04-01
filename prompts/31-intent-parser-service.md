# 31 — Gemini-Powered Intent Parser Service

Read `base_prompt.md` first and preserve all prior prompt work.

## Objective

Implement a backend service that uses a fast Gemini model to translate user chat messages into structured UI actions and assistant replies.

## Build
- Create a backend intent-parsing service that sends the current stage context, session summary, and user message to Gemini and requests strict structured output.
- Use a fast, economical model for this translation step and keep model selection configurable from settings.
- Return both the structured actions and a natural-language assistant response or clarification summary.

## Deliverables

- Intent parser service
- Prompt template for action extraction
- Tests with representative chat messages

## Acceptance checks

- A user message like ‘make it a little more mysterious and shorter’ can become structured proposed updates.
- The service is isolated behind a backend API and never exposes API keys to the browser.
- The parser can fail gracefully when the message is too vague.

## Notes

Keep prompts and outputs auditable. Store the structured result in the event log.

## Suggested commit label

`feat(prompt-31): intent parser service`

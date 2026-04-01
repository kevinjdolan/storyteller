---
name: webapp-qa
description: Use when interacting with a local webapp in this repo, taking screenshots, and verifying behavior both visually and functionally through the docker-compose dev stack and the bundled Puppeteer runner.
---

# Webapp QA

Use this skill when the task involves running the local app, exercising it in a browser, taking screenshots, or checking that UI behavior and rendered output match expectations.

## Workflow

1. Start the local stack with `docker compose up -d --build`.
2. Confirm the app is healthy with `docker compose ps`.
3. Run browser checks from the `browser` service with `docker compose run --rm browser npm run check -- --spec <spec-path>`.
4. Review the generated screenshot under `.artifacts/webapp-qa/`.

## App URLs

- From the host machine, the app is available at `http://localhost:8566`.
- From inside the browser container, use `http://frontend:8566`.

## Puppeteer Specs

The reusable runner lives at `tools/webapp-qa/scripts/run-spec.mjs`.

Specs are JSON files with this shape:

```json
{
  "url": "http://frontend:8566",
  "outputPath": "/workspace/.artifacts/webapp-qa/example.png",
  "viewport": { "width": 1440, "height": 960 },
  "steps": [
    { "action": "waitForSelector", "selector": "[data-testid='app-card']" },
    { "action": "assertText", "text": "Hello from FastAPI!" },
    { "action": "screenshot" }
  ]
}
```

Supported actions:

- `goto`
- `waitForSelector`
- `waitForText`
- `click`
- `type`
- `press`
- `hover`
- `assertSelector`
- `assertText`
- `assertUrlIncludes`
- `waitForTimeout`
- `screenshot`

## Example

Use `tools/webapp-qa/examples/homepage.spec.json` for a basic smoke test plus screenshot:

```bash
docker compose run --rm browser npm run check -- --spec ./examples/homepage.spec.json
```

## Verification Guidance

- For functional checks, prefer explicit `assertText`, `assertSelector`, and URL assertions over informal observation.
- For visual checks, capture a screenshot after the page reaches the expected stable state.
- If a page depends on backend data, verify the user-visible result instead of only checking network readiness.

# Developer Debug Inspector

The developer debug inspector is a hidden route for inspecting the backend-owned
truth of a session during long AI-driven runs.

## Enable it

Turn on the backend feature flag in local config:

```yaml
feature_flags:
  enable_debug_inspector: true
```

The same flag can also be set with `STORYTELLER_FEATURE_ENABLE_DEBUG_INSPECTOR=true`.

When running the Docker Compose stack, the backend now accepts that shell
variable directly:

```bash
STORYTELLER_FEATURE_ENABLE_DEBUG_INSPECTOR=true \
  docker compose -f infra/compose/docker-compose.yml up -d backend
```

## Use it

Open the hidden route directly in the frontend:

```text
/sessions/<session-id>/debug
```

Example:

```text
http://127.0.0.1:5173/sessions/moonlit-harbor/debug
```

The inspector shows:

- the current hydrated session snapshot
- the current plan revision
- active or latest composition and audio jobs
- recent durable events
- the current artifact inventory
- model-usage diagnostics

If the feature flag is off, the route stays hidden from normal navigation and the
backend returns a 404 with a message explaining that the inspector is disabled.

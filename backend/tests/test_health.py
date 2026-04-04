import logging

from app.api.dependencies import get_db_session, require_owned_session_access
from app.main import create_app
from app.repositories import StorySessionRepository
from fastapi import Depends
from fastapi.testclient import TestClient


def test_health_endpoint_returns_service_metadata(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    payload = response.json()

    assert payload["status"] == "ok"
    assert payload["service"] == "Storyteller API"
    assert payload["environment"] == "development"
    assert payload["version"] == "0.1.0"
    assert payload["api_version"] is None
    assert payload["dependencies"]["database"] == {
        "status": "configured",
        "detail": "A database URL is configured for the application runtime.",
    }
    assert payload["dependencies"]["object_storage"] == {
        "status": "configured",
        "detail": (
            "A file-backed GCS emulator is configured for buckets "
            "storyteller-sessions, storyteller-audio, storyteller-exports at "
            "http://gcs:4443. Public URL: http://localhost:8568."
        ),
    }
    assert "gemini" not in payload["dependencies"]


def test_versioned_health_endpoint_marks_the_api_version(client: TestClient) -> None:
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    payload = response.json()

    assert payload["status"] == "ok"
    assert payload["api_version"] == "v1"
    assert payload["dependencies"]["database"]["status"] == "configured"
    assert payload["dependencies"]["object_storage"]["status"] == "configured"


def test_legacy_hello_endpoint_remains_available_for_existing_frontend_checks(
    client: TestClient,
) -> None:
    response = client.get("/api/hello")

    assert response.status_code == 200
    assert response.json() == {"message": "Hello from FastAPI!"}


def test_request_logging_echoes_request_id_and_binds_session_context(
    caplog,
    monkeypatch,
) -> None:
    caplog.set_level(logging.INFO)
    session_id = "session-trace-test"

    app = create_app()

    def override_db_session():
        yield object()

    app.dependency_overrides[get_db_session] = override_db_session
    monkeypatch.setattr(StorySessionRepository, "exists", lambda *_args, **_kwargs: True)

    @app.get("/_test/trace/{session_id}", dependencies=[Depends(require_owned_session_access)])
    def trace_session(session_id: str) -> dict[str, str]:
        return {"session_id": session_id}

    with TestClient(app) as client:
        response = client.get(
            f"/_test/trace/{session_id}",
            headers={"X-Request-ID": "req-test-session-trace"},
        )

    assert response.status_code == 200
    assert response.headers["X-Request-ID"] == "req-test-session-trace"

    matching_records = [
        record
        for record in caplog.records
        if getattr(record, "event", None) == "http.request.completed"
        and getattr(record, "log_context_fields", {}).get("path")
        == f"/_test/trace/{session_id}"
    ]

    assert matching_records
    fields = matching_records[-1].log_context_fields
    assert fields["request_id"] == "req-test-session-trace"
    assert fields["session_id"] == session_id
    assert fields["status_code"] == 200

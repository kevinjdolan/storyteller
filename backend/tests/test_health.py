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

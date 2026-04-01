from fastapi.testclient import TestClient


def test_health_endpoint_returns_service_metadata(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "Storyteller API",
        "environment": "development",
        "version": "0.1.0",
        "api_version": None,
        "dependencies": {
            "database": {
                "status": "not-configured",
                "detail": (
                    "Database wiring lands in a later prompt; this scaffold "
                    "only reports configuration state."
                ),
            },
        },
    }


def test_versioned_health_endpoint_marks_the_api_version(client: TestClient) -> None:
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    payload = response.json()

    assert payload["status"] == "ok"
    assert payload["api_version"] == "v1"
    assert payload["dependencies"]["database"]["status"] == "not-configured"


def test_legacy_hello_endpoint_remains_available_for_existing_frontend_checks(
    client: TestClient,
) -> None:
    response = client.get("/api/hello")

    assert response.status_code == 200
    assert response.json() == {"message": "Hello from FastAPI!"}

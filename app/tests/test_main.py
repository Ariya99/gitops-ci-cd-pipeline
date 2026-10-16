import pytest
from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def mock_api_token(monkeypatch):
    """Fixture to set a mock API_TOKEN environment variable for tests."""
    monkeypatch.setenv("API_TOKEN", "test-secret-token")


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_ready() -> None:
    response = client.get("/ready")
    assert response.status_code == 200
    assert response.json()["status"] == "ready"


def test_greeting_authenticated() -> None:
    response = client.get("/api/v1/greeting", headers={"Authorization": "Bearer test-secret-token"})
    assert response.status_code == 200
    assert "message" in response.json()


def test_greeting_unauthenticated_missing_token() -> None:
    response = client.get("/api/v1/greeting")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


def test_greeting_unauthenticated_invalid_token() -> None:
    response = client.get("/api/v1/greeting", headers={"Authorization": "Bearer invalid-token"})
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid authentication token"


def test_greeting_no_api_token_env_var(monkeypatch) -> None:
    monkeypatch.delenv("API_TOKEN", raising=False)
    response = client.get("/api/v1/greeting", headers={"Authorization": "Bearer test-secret-token"})
    assert response.status_code == 500
    assert response.json()["detail"] == "API_TOKEN environment variable not set"


def test_metrics() -> None:
    client.get("/api/v1/greeting", headers={"Authorization": "Bearer test-secret-token"})
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "http_requests_total" in response.text

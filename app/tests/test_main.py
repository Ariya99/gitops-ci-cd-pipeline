import pytest
from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)

# Use a consistent mock token across tests
MOCK_API_TOKEN = "supersecrettoken"


@pytest.fixture(autouse=True)
def mock_api_token(monkeypatch: pytest.MonkeyPatch) -> None:
    """Mock the API_TOKEN environment variable for all tests."""
    monkeypatch.setenv("API_TOKEN", MOCK_API_TOKEN)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_ready() -> None:
    response = client.get("/ready")
    assert response.status_code == 200
    assert response.json()["status"] == "ready"


def test_greeting() -> None:
    response = client.get("/api/v1/greeting", headers={"Authorization": f"Bearer {MOCK_API_TOKEN}"})
    assert response.status_code == 200
    assert "message" in response.json()


def test_greeting_unauthenticated() -> None:
    response = client.get("/api/v1/greeting")
    # HTTPBearer returns 401 when the header is missing
    assert response.status_code == 401


def test_greeting_invalid_token() -> None:
    response = client.get("/api/v1/greeting", headers={"Authorization": "Bearer invalid_token"})
    assert response.status_code == 401


def test_greeting_missing_env_token(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("API_TOKEN", raising=False)
    response = client.get("/api/v1/greeting", headers={"Authorization": f"Bearer {MOCK_API_TOKEN}"})
    assert response.status_code == 500
    assert response.json()["detail"] == "Internal Server Error"


def test_metrics() -> None:
    # Need to pass token to hit the endpoint before metrics
    client.get("/api/v1/greeting", headers={"Authorization": f"Bearer {MOCK_API_TOKEN}"})
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "http_requests_total" in response.text

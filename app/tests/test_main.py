import pytest
from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)

DUMMY_TOKEN = "supersecrettoken"


@pytest.fixture(autouse=True)
def mock_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("API_TOKEN", DUMMY_TOKEN)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_ready() -> None:
    response = client.get("/ready")
    assert response.status_code == 200
    assert response.json()["status"] == "ready"


def test_greeting() -> None:
    response = client.get("/api/v1/greeting", headers={"Authorization": f"Bearer {DUMMY_TOKEN}"})
    assert response.status_code == 200
    assert "message" in response.json()


def test_greeting_unauthorized() -> None:
    response = client.get("/api/v1/greeting")
    assert response.status_code == 401


def test_greeting_invalid_token() -> None:
    response = client.get("/api/v1/greeting", headers={"Authorization": "Bearer wrongtoken"})
    assert response.status_code == 401


def test_greeting_missing_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("API_TOKEN", raising=False)
    response = client.get("/api/v1/greeting", headers={"Authorization": f"Bearer {DUMMY_TOKEN}"})
    assert response.status_code == 500


def test_metrics() -> None:
    client.get("/api/v1/greeting", headers={"Authorization": f"Bearer {DUMMY_TOKEN}"})
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "http_requests_total" in response.text

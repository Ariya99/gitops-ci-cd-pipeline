import pytest
from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def mock_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("API_TOKEN", "test-secret")


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_ready() -> None:
    response = client.get("/ready")
    assert response.status_code == 200
    assert response.json()["status"] == "ready"


def test_greeting_unauthenticated() -> None:
    response = client.get("/api/v1/greeting")
    assert response.status_code == 401


def test_greeting_authenticated() -> None:
    response = client.get("/api/v1/greeting", headers={"Authorization": "Bearer test-secret"})
    assert response.status_code == 200
    assert "message" in response.json()


def test_metrics() -> None:
    client.get("/api/v1/greeting", headers={"Authorization": "Bearer test-secret"})
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "http_requests_total" in response.text

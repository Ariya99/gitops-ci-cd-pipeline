import pytest
from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def set_env(monkeypatch):
    monkeypatch.setenv("API_TOKEN", "supersecret")


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_ready() -> None:
    response = client.get("/ready")
    assert response.status_code == 200
    assert response.json()["status"] == "ready"


def test_greeting_authenticated() -> None:
    response = client.get("/api/v1/greeting", headers={"Authorization": "Bearer supersecret"})
    assert response.status_code == 200
    assert "message" in response.json()


def test_greeting_unauthenticated() -> None:
    response = client.get("/api/v1/greeting")
    assert response.status_code == 401


def test_greeting_invalid_token() -> None:
    response = client.get("/api/v1/greeting", headers={"Authorization": "Bearer invalidtoken"})
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid token"


def test_greeting_missing_env_token(monkeypatch) -> None:
    monkeypatch.delenv("API_TOKEN", raising=False)
    response = client.get("/api/v1/greeting", headers={"Authorization": "Bearer supersecret"})
    assert response.status_code == 500
    assert response.json()["detail"] == "Internal Server Error"


def test_metrics() -> None:
    client.get("/api/v1/greeting", headers={"Authorization": "Bearer supersecret"})
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "http_requests_total" in response.text


import pytest
from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


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
    # We use auto_error=False on HTTPBearer and manually raise 401 when header is missing
    assert response.status_code == 401


def test_greeting_invalid_token(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("API_TOKEN", "default-token")
    response = client.get(
        "/api/v1/greeting",
        headers={"Authorization": "Bearer invalid-token"},
    )
    # Our manual verification logic returns 401 when header is present but token is wrong
    assert response.status_code == 401


def test_greeting_authenticated(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("API_TOKEN", "default-token")
    response = client.get(
        "/api/v1/greeting",
        headers={"Authorization": "Bearer default-token"},
    )
    assert response.status_code == 200
    assert "message" in response.json()


def test_greeting_no_token_configured(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("API_TOKEN", raising=False)
    response = client.get(
        "/api/v1/greeting",
        headers={"Authorization": "Bearer some-token"},
    )
    assert response.status_code == 401


def test_metrics(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("API_TOKEN", "default-token")
    client.get("/api/v1/greeting", headers={"Authorization": "Bearer default-token"})
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "http_requests_total" in response.text

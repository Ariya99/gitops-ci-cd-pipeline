import os
import secrets

from fastapi import Depends, FastAPI, HTTPException, Response, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

from src.metrics import REQUEST_COUNT

app = FastAPI(title="GitOps Demo API", version="1.0.0")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "healthy"}


@app.get("/ready")
def ready() -> dict[str, str]:
    return {"status": "ready"}


security = HTTPBearer(auto_error=True)


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """Verify that the provided bearer token matches the API_TOKEN environment variable."""
    expected_token = os.getenv("API_TOKEN")
    if not expected_token:
        # Secure failure: if no token is configured, fail securely without leaking internal state
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )

    # Use constant-time comparison to prevent timing attacks
    if not secrets.compare_digest(credentials.credentials, expected_token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return credentials.credentials


@app.get("/api/v1/greeting", dependencies=[Depends(verify_token)])
def greeting() -> dict[str, str]:
    REQUEST_COUNT.labels(method="GET", endpoint="/api/v1/greeting").inc()
    return {"message": "Hello from GitOps CI/CD pipeline"}


@app.get("/metrics")
def metrics() -> Response:
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

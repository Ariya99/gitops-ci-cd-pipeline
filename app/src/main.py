from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

from src.metrics import REQUEST_COUNT

app = FastAPI(title="GitOps Demo API", version="1.0.0")


# Optimization: Return JSONResponse directly to avoid serialization overhead
@app.get("/health", response_model=dict[str, str])
def health() -> JSONResponse:
    return JSONResponse(content={"status": "healthy"})


# Optimization: Return JSONResponse directly to avoid serialization overhead
@app.get("/ready", response_model=dict[str, str])
def ready() -> JSONResponse:
    return JSONResponse(content={"status": "ready"})


# Optimization: Return JSONResponse directly to avoid serialization overhead
@app.get("/api/v1/greeting", response_model=dict[str, str])
def greeting() -> JSONResponse:
    REQUEST_COUNT.labels(method="GET", endpoint="/api/v1/greeting").inc()
    return JSONResponse(content={"message": "Hello from GitOps CI/CD pipeline"})


@app.get("/metrics")
def metrics() -> Response:
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

## 2024-05-24 - FastAPI Static Endpoint Optimization
**Learning:** FastAPI serializes dictionary returns using Pydantic, which adds overhead for static JSON responses.
**Action:** Return a new `JSONResponse` directly for static endpoints and use `response_model` in the route decorator to preserve OpenAPI documentation. Avoid global `JSONResponse` objects.

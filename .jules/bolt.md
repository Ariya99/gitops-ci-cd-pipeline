## 2024-03-22 - FastAPI Static Endpoint Optimization
**Learning:** For FastAPI static endpoints, returning a dictionary causes unnecessary Pydantic serialization overhead. Returning a new `JSONResponse` directly avoids this overhead and provides a minor performance improvement (e.g. ~5% faster response time for simple endpoints).
**Action:** When creating static or simple endpoints that just return a hardcoded JSON response, return `JSONResponse(content=...)` directly, and use `response_model` in the route decorator to preserve OpenAPI documentation.

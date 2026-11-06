## 2026-11-06 - FastAPI Static Endpoint Optimization
**Learning:** Returning static dictionaries from FastAPI endpoints incurs a Pydantic serialization overhead, which can be noticeable at high scale.
**Action:** For simple, static responses, return a `JSONResponse` directly while maintaining the `response_model` in the route decorator to preserve OpenAPI documentation. Avoid global JSONResponse instances to prevent bugs from middleware mutations.

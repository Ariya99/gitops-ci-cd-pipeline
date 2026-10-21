## 2026-10-21 - FastAPI Serialization Overhead
**Learning:** Returning a dictionary from a FastAPI route incurs hidden Pydantic serialization and validation overhead, even for simple static responses.
**Action:** Return a new `JSONResponse` directly for static endpoints while keeping `response_model` in the decorator to preserve OpenAPI documentation. Avoid global `JSONResponse` objects to prevent middleware mutation bugs.

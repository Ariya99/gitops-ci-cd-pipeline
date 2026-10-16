
## 2024-05-18 - FastAPI Response Serialization Overhead
**Learning:** Returning Python dictionaries in FastAPI endpoints requires them to be converted to JSON, involving serialization overhead. This serialization via Pydantic is slower than directly returning an already-constructed `JSONResponse`, particularly for fast, high-traffic static responses (e.g., health/readiness checks).
**Action:** Use `JSONResponse` directly from `fastapi.responses` for endpoints with static responses, keeping `response_model` on the decorator to ensure OpenAPI documentation correctly infers the response shape.

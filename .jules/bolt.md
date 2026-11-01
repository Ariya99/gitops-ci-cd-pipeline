## 2023-11-01 - [Avoid Pydantic Serialization Overhead for Static Responses]
**Learning:** [FastAPI's default Pydantic serialization adds overhead to static responses.]
**Action:** [Use `JSONResponse` directly for static endpoints and retain OpenAPI documentation using `response_model`.]

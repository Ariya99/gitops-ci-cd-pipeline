## 2024-05-15 - FastAPI Response Optimization
**Learning:** Returning `JSONResponse` directly instead of a Python dictionary avoids FastAPI's internal serialization overhead for static endpoints.
**Action:** Use `JSONResponse` directly for endpoints returning static or simple dictionary payloads to improve throughput, but ensure `response_model` is set in the route decorator to preserve OpenAPI documentation. Avoid using global `JSONResponse` objects to prevent mutation bugs from middlewares.

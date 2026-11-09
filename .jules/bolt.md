## 2025-02-14 - Optimize FastAPI Static Endpoints
**Learning:** Returning a Python dictionary from a FastAPI endpoint incurs serialization overhead on every request. For static responses, returning a new `JSONResponse` directly avoids this overhead and improves performance.
**Action:** Use `JSONResponse` directly for static endpoints instead of dictionaries, and set `response_model` in the decorator to preserve OpenAPI documentation. Avoid using global `JSONResponse` objects to prevent mutation bugs from middlewares.

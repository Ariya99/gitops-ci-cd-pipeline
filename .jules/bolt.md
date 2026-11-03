
## 2023-11-20 - FastAPI Serialization Overhead
**Learning:** Returning dictionaries from FastAPI endpoints incurs serialization overhead because FastAPI validates and serializes the return value into JSON using its internal Pydantic mechanisms. For static endpoints, returning a `JSONResponse` directly is faster.
**Action:** Always return `JSONResponse(content=...)` directly for static endpoints instead of dictionaries to avoid serialization overhead. Use `response_model` in the route decorator to preserve OpenAPI documentation, and avoid using global `JSONResponse` objects to prevent mutation bugs from middlewares.

## 2024-05-25 - Direct JSONResponse for Static Endpoints
**Learning:** Returning dictionaries from FastAPI endpoints incurs serialization overhead because FastAPI validates and serializes the dictionary before creating the response.
**Action:** For static endpoints, return a new `JSONResponse` directly instead of a dictionary to avoid serialization overhead. Use `response_model` in the route decorator to preserve OpenAPI documentation, and avoid using global `JSONResponse` objects to prevent mutation bugs from middlewares.

## 2024-05-24 - Avoiding FastAPI Serialization Overhead
**Learning:** For static endpoint responses, returning a plain dictionary causes FastAPI to incur Pydantic validation and serialization overhead. Returning a new `JSONResponse` directly avoids this cost.
**Action:** When implementing static endpoints in FastAPI, explicitly return a `JSONResponse` object and define `response_model` in the route decorator to preserve OpenAPI schemas without sacrificing performance.

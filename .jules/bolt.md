## 2024-10-15 - Fast API Dictionary Return Overhead
**Learning:** In FastAPI, returning a dictionary (`dict`) triggers internal response parsing and Pydantic serialization overhead, even for static payloads. Returning `JSONResponse` directly avoids this overhead. However, using `response_model` is necessary to preserve the OpenAPI documentation.
**Action:** When creating simple endpoints returning static JSON payloads, always return `JSONResponse(content=...)` and set `response_model=dict[str, str]` (or the appropriate type) in the route decorator instead of returning dictionaries directly.

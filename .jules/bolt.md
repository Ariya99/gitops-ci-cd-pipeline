## 2024-05-24 - FastAPI static endpoint performance
**Learning:** Returning dictionaries from FastAPI endpoints forces them through Pydantic's serialization pipeline, which adds overhead. Returning `JSONResponse` directly avoids this, but we must be careful to use `response_model` to preserve OpenAPI docs, and avoid global `JSONResponse` instances.
**Action:** Return `JSONResponse` directly from static endpoints in FastAPI and use `response_model` on the decorator.

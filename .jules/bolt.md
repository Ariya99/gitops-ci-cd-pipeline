## 2024-05-24 - Avoid FastAPI dict serialization overhead for static endpoints
**Learning:** For static endpoints returning dictionaries, returning a new `JSONResponse` directly avoids FastAPI's internal serialization overhead. Using `response_model` ensures OpenAPI docs remain accurate.
**Action:** Use `JSONResponse` directly and specify `response_model` in the route decorator for static responses.

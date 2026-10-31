## 2024-10-31 - Fast API JSONResponse overhead
**Learning:** In FastAPI, static endpoints returning dictionaries incur a small Pydantic serialization overhead which is unnecessary when the response is a simple, static dictionary.
**Action:** Always return `JSONResponse` directly for static JSON payloads, and use `response_model` on the `@app.get()` decorator to ensure the OpenAPI documentation isn't lost.

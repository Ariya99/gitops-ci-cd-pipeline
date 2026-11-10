
## 2023-11-10 - Direct JSONResponse for Static Endpoints
**Learning:** Returning dictionaries from FastAPI endpoints incurs a serialization overhead as FastAPI processes the data through Pydantic. For endpoints with static or simple responses, this overhead is noticeable in benchmarks.
**Action:** When creating high-throughput static endpoints (like health checks or simple greetings), return a `JSONResponse` directly, but retain `response_model` in the decorator to preserve OpenAPI documentation.

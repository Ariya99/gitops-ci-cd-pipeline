## 2026-10-23 - [Optimization: FastAPI Static Endpoints]
**Learning:** Returning dictionary responses from static endpoints in FastAPI adds unnecessary serialization overhead. Returning `JSONResponse` directly avoids this overhead, making static endpoints faster. Using `response_model` ensures OpenAPI schema remains correct.
**Action:** When implementing static endpoints in FastAPI (like `/health` or `/ready`), return `JSONResponse` directly and specify `response_model` to avoid serialization penalties while preserving API docs.

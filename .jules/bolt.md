## 2024-10-30 - Optimize FastAPI static dictionary returns
**Learning:** FastAPI uses `jsonable_encoder` to process python dictionaries before sending them to the response class, adding unnecessary serialization overhead for static responses.
**Action:** Return a new `JSONResponse` directly for static endpoints and use `response_model` on the decorator to preserve OpenAPI docs. Avoid returning a global `JSONResponse` object to prevent potential mutation bugs from middlewares.

# from fastapi import FastAPI, Request
# from fastapi.responses import JSONResponse, Response
# from fastapi.openapi.utils import get_openapi
# from fastapi.middleware.cors import CORSMiddleware
# import httpx
# import asyncio
# import json

# app = FastAPI(title="API Gateway", version="1.0.0")


# SERVICE_URLS = {
#     "user": "http://user-service:8001",
#     "cart": "http://cart-service:8002",
#     "product": "http://product-service:8003",
# }


# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# merged_openapi_schema = None



# async def forward_request(service: str, path: str, request: Request):
#     if service not in SERVICE_URLS:
#         return JSONResponse({"error": "Unknown service"}, status_code=400)

#     target_url = f"{SERVICE_URLS[service]}/{path}"
#     method = request.method
#     headers = dict(request.headers)
#     body = await request.body()

#     async with httpx.AsyncClient() as client:
#         resp = await client.request(method, target_url, headers=headers, content=body)

#     return Response(
#         content=resp.content,
#         status_code=resp.status_code,
#         headers={k: v for k, v in resp.headers.items() if k.lower() not in ["content-encoding", "transfer-encoding"]},
#         media_type=resp.headers.get("content-type"),
#     )


# @app.api_route("/{service}/{path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
# async def proxy(service: str, path: str, request: Request):
#     return await forward_request(service, path, request)


# async def fetch_openapi(service_name: str, url: str):
#     try:
#         async with httpx.AsyncClient() as client:
#             r = await client.get(f"{url}/openapi.json", timeout=5.0)
#             r.raise_for_status()
#             data = r.json()
#             # Prefix all paths with /{service}
#             new_paths = {}
#             for path, definition in data.get("paths", {}).items():
#                 new_paths[f"/{service_name}{path}"] = definition
#             data["paths"] = new_paths
#             return data
#     except Exception as e:
#         print(f"Could not load OpenAPI from {service_name}: {e}")
#         return None


# async def merge_openapi_schemas():
#     merged = get_openapi(
#         title="Gateway API",
#         version="1.0.0",
#         routes=app.routes,
#     )
#     merged["paths"] = {}

#     schemas = await asyncio.gather(
#         *[fetch_openapi(name, url) for name, url in SERVICE_URLS.items()]
#     )

#     for schema in schemas:
#         if schema:
#             merged["paths"].update(schema.get("paths", {}))
#             if "components" in schema:
#                 components = merged.setdefault("components", {})
#                 for key, value in schema["components"].items():
#                     components.setdefault(key, {}).update(value)

#     return merged


# @app.on_event("startup")
# async def load_merged_openapi():
#     global merged_openapi_schema
#     merged_openapi_schema = await merge_openapi_schemas()
#     print("Merged OpenAPI schema loaded.")


# @app.get("/openapi.json", include_in_schema=False)
# async def custom_openapi():
#     if merged_openapi_schema is None:
#         return JSONResponse({"error": "OpenAPI schema not ready"}, status_code=503)
#     return JSONResponse(merged_openapi_schema)


# @app.get("/", include_in_schema=False)
# def root():
#     return {"message": "API Gateway is running"}


# def custom_openapi_function():
#     return merged_openapi_schema


# app.openapi = custom_openapi_function
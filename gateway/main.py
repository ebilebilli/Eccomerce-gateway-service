
from fastapi import FastAPI, Request

import requests
from fastapi.responses import JSONResponse, PlainTextResponse


app = FastAPI(title="Gateway API")


# def forward_request(url: str, method: str = "get", data=None):
#     try:
#         if method.lower() == "post":
#             response = requests.post(url, json=data)
#         else:
#             response = requests.get(url)
#         try:
#             return JSONResponse(content=response.json(), status_code=response.status_code)
#         except ValueError:
#             return PlainTextResponse(content=response.text, status_code=response.status_code)
#     except Exception as e:
#         return JSONResponse(content={"error": str(e)}, status_code=500)

# # --------------------------
# # Service 1 — User Service
# # --------------------------
# @app.post("/service1/register")
# def service1_register(body: RegisterRequest):
#     return forward_request(f"{SERVICE_1}/register/", method="post", data=body.dict())

# @app.post("/service1/login")
# def service1_login(body: LoginRequest):
#     return forward_request(f"{SERVICE_1}/login/", method="post", data=body.dict())

# @app.get("/service1/profile")
# def service1_profile():
#     return forward_request(f"{SERVICE_1}/profile/")

# # --------------------------
# # Shop Service Endpoints
# # --------------------------
# @app.get("/service-shop/shops")
# def gateway_shop_list():
#     return forward_request(f"{SERVICE_SHOP}/shops/")

# @app.get("/service-shop/shops/{shop_slug}")
# def gateway_shop_detail(shop_slug: str):
#     return forward_request(f"{SERVICE_SHOP}/shops/{shop_slug}/")

# @app.post("/service-shop/shops/create")
# async def gateway_shop_create(request: Request):
#     body = await request.json()
#     return forward_request(f"{SERVICE_SHOP}/shops/create/", method="post", data=body)

# @app.post("/service-shop/shops/{shop_slug}/management")
# async def gateway_shop_manage(shop_slug: str, request: Request):
#     body = await request.json()
#     return forward_request(f"{SERVICE_SHOP}/shops/{shop_slug}/management/", method="post", data=body)

# # --------------------------
# # Service 3 — Analytics Service
# # --------------------------
# @app.post("/service3/analytics-products")
# def service3_create_analytics(body: AnalyticsRequest):
#     return forward_request(f"{SERVICE_3}/analytics-products/", method="post", data=body.dict())

# @app.get("/service3/analytics-products")
# def service3_list_analytics():
#     return forward_request(f"{SERVICE_3}/analytics-products/")

# @app.get("/service3/shop-views")
# def service3_shop_views():
#     return forward_request(f"{SERVICE_3}/shop-views/")

# @app.get("/service3/product-views")
# def service3_product_views():
#     return forward_request(f"{SERVICE_3}/product-views/")

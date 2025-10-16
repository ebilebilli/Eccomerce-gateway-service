import os
from dotenv import load_dotenv
from fastapi import APIRouter, Request

from gateway.utils import forward_request, load_remote_openapi


load_dotenv()

SHOPCART_SERVICE = os.getenv('SHOPCART_SERVICE')
router = APIRouter(tags=['Shopcart Service'])


async def register_shop_cart_routes():
    openapi = await load_remote_openapi(SHOPCART_SERVICE)
    paths = openapi.get('paths', {})

    for path, methods in paths.items():
        for method, details in methods.items():
            operation_id = details.get('operationId', f'{method}_{path}')
            full_url = f'{SHOPCART_SERVICE}{path}'

            async def handler(request: Request, _url=full_url, _method=method.upper()):
                body = await request.json() if _method in ('POST', 'PUT', 'PATCH') else None
                return await forward_request(_url, method=_method.lower(), data=body)

            clean_path = path.replace('/api/v1', '')

            router.add_api_route(
                path=clean_path,
                endpoint=handler,
                methods=[method.upper()],
                name=operation_id,
                tags=['Shopcart Service']
            )

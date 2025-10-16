import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
import asyncio
from gateway.utils import merge_openapi_docs, load_openapi, forward_request


load_dotenv()


SHOPCART_SERVICE = os.getenv('SHOPCART_SERVICE')
SHOP_SERVICE = os.getenv('SHOP_SERVICE')

app = FastAPI(title='Gateway API', version='0.1')


@app.on_event('startup')
async def on_startup():
    services = [SHOP_SERVICE, SHOPCART_SERVICE]
    app.openapi_schema = await merge_openapi_docs(app, services)

    for service_url in services:
        openapi_data = await load_openapi(service_url)
        if not openapi_data:
            continue

        for path, methods in openapi_data.get('paths', {}).items():
            for method, details in methods.items():
                full_url = f'{service_url}{path}'
                operation_id = details.get('operationId', f'{method}_{path}')

                async def handler(request: Request, _url=full_url, _method=method.upper()):
                    body = await request.json() if _method in ('POST', 'PUT', 'PATCH') else None
                    return await forward_request(_url, method=_method.lower(), data=body)

                clean_path = path.replace('/api/v1', '')
                app.add_api_route(
                    path=path,
                    endpoint=handler,
                    methods=[method.upper()],
                    name=operation_id,
                    tags=[service_url.split('//')[-1]],
                )


@app.get('/openapi.json')
async def openapi():
    return app.openapi_schema
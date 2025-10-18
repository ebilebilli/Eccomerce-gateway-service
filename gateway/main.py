import httpx
import asyncio
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .logging import logger
from .auth import verify_jwt
from .forward import forward_request
from .services import SERVICE_URLS


load_dotenv()

app = FastAPI(title='API Gateway', version='1.0.0')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.middleware('http')
async def log_requests(request: Request, call_next):
    logger.info(f'Incoming request: {request.method} {request.url}')
    try:
        response = await call_next(request)
    except Exception as e:
        logger.error(f'Error handling request: {e}')
        return JSONResponse({'error': str(e)}, status_code=500)
    logger.info(f'Response status: {response.status_code} for {request.method} {request.url}')
    return response


merged_openapi_schema = None

@app.api_route('/{service}/{full_path:path}', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
async def proxy(service: str, full_path: str, request: Request):
    return await forward_request(service, full_path, request)


async def fetch_openapi(service_name: str, url: str):
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            r = await client.get(f'{url}/openapi.json')
            r.raise_for_status()
            data = r.json()
            new_paths = {f'/{service_name}{p}': v for p, v in data.get('paths', {}).items()}
            data['paths'] = new_paths
            return data
    except Exception as e:
        print(f'Could not load OpenAPI from {service_name}: {e}')
        return None


async def merge_openapi_schemas():
    merged = get_openapi(title='Gateway API', version='1.0.0', routes=app.routes)
    merged['paths'] = {}

    schemas = await asyncio.gather(
        *[fetch_openapi(name, url) for name, url in SERVICE_URLS.items()]
    )

    for schema in schemas:
        if schema:
            merged['paths'].update(schema.get('paths', {}))
            if 'components' in schema:
                components = merged.setdefault('components', {})
                for key, value in schema['components'].items():
                    components.setdefault(key, {}).update(value)

    return merged


@app.on_event('startup')
async def load_merged_openapi():
    global merged_openapi_schema
    merged_openapi_schema = await merge_openapi_schemas()
    print('Merged OpenAPI schema loaded.')


@app.get('/openapi.json', include_in_schema=False)
async def custom_openapi():
    if merged_openapi_schema is None:
        return JSONResponse({'error': 'OpenAPI schema not ready'}, status_code=503)
    return JSONResponse(merged_openapi_schema)


@app.get('/', include_in_schema=False)
def root():
    return {'message': 'API Gateway is running'}


app.openapi = lambda: merged_openapi_schema
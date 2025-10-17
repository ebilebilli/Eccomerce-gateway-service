import httpx
from fastapi.openapi.utils import get_openapi


async def load_openapi(service_url: str):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f'{service_url}/openapi.json')
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        print(f'HTTP error occurred: {e}')
    except Exception as e:
        print(f'An error occurred: {e}')
    return {}


async def merge_openapi_docs(app, services):
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    for service_url in services:
        service_openapi = await load_openapi(service_url)  
        if service_openapi:
            openapi_schema['paths'].update(service_openapi.get('paths', {}))
            if 'components' in service_openapi:
                openapi_schema.setdefault('components', {}).update(service_openapi['components'])

    return openapi_schema


async def should_protect(openapi_data: dict, path: str, method: str) -> bool:
    path_info = openapi_data.get('paths', {}).get(path, {})
    method_info = path_info.get(method.lower(), {})
    return 'security' in method_info and method_info['security'] != []
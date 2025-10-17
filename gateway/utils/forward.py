import httpx
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi import Request


async def forward_request(request: Request, url: str, method: str = 'get', data=None):
    headers = {}
    if 'authorization' in request.headers:
        headers['Authorization'] = request.headers['authorization']

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.request(method, url, json=data, headers=headers)
        try:
            return JSONResponse(content=response.json(), status_code=response.status_code)
        except ValueError:
            return PlainTextResponse(content=response.text, status_code=response.status_code)
    except Exception as e:
        return JSONResponse(content={'error': str(e)}, status_code=500)
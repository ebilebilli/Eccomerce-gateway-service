import httpx
from fastapi.responses import JSONResponse, Response
from fastapi import Request
from urllib.parse import urlparse

from .services import SERVICE_URLS
from .logging import logger  

async def forward_request(service: str, path: str, request: Request):
    if service not in SERVICE_URLS:
        return JSONResponse({'error': 'Unknown service'}, status_code=400)

    url = f"{SERVICE_URLS[service].rstrip('/')}/{path.lstrip('/')}"
    method = request.method
    body = await request.body()
    incoming_headers = dict(request.headers)
    excluded = {'host', 'connection', 'content-length', 'accept-encoding', 'cookie', 'referer'}
    headers = {k: v for k, v in incoming_headers.items() if k.lower() not in excluded}
    parsed = urlparse(SERVICE_URLS[service])
    headers['host'] = parsed.netloc
    
    logger.info(f'Forwarding request to {url} | Method: {method} | Headers: {headers}')

    try:
        async with httpx.AsyncClient(timeout=30.0, verify=False) as client:  
            resp = await client.request(method, url, headers=headers, content=body)

        excluded_resp = {'content-encoding', 'transfer-encoding', 'connection'}
        resp_headers = {k: v for k, v in resp.headers.items() if k.lower() not in excluded_resp}

        logger.info(f'Received {resp.status_code} from {url}')

        return Response(
            content=resp.content,
            status_code=resp.status_code,
            headers=resp_headers,
            media_type=resp.headers.get('content-type'),
        )
    except httpx.RequestError as e:
        logger.error(f'RequestError: {e}')
        return JSONResponse({'error': f'Service unreachable: {e}'}, status_code=503)
    except Exception as e:
        logger.error(f'Unexpected error: {e}')
        return JSONResponse({'error': str(e)}, status_code=500)

import httpx
from fastapi.responses import JSONResponse, PlainTextResponse


async def forward_request(url: str, method: str = "get", data=None):
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            if method.lower() == "post":
                response = await client.post(url, json=data)
            elif method.lower() == "put":
                response = await client.put(url, json=data)
            elif method.lower() == "delete":
                response = await client.delete(url)
            else:
                response = await client.get(url)

        try:
            return JSONResponse(content=response.json(), status_code=response.status_code)
        except ValueError:
            return PlainTextResponse(content=response.text, status_code=response.status_code)

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

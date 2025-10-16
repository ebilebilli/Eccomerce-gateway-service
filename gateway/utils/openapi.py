import httpx
from fastapi import FastAPI
import os
from dotenv import load_dotenv
from fastapi import APIRouter, Request

from gateway.utils.forward import forward_request


load_dotenv()

SHOP_SERVICE = os.getenv('SHOP_SERVICE')
app = FastAPI(title="Gateway API")


async def load_remote_openapi(service_url: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{SHOP_SERVICE}/openapi.json")
        response.raise_for_status()
        return response.json()
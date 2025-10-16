from fastapi import FastAPI

from gateway.services import shop_service , shop_cart_service
from contextlib import asynccontextmanager
from gateway.services import (
    register_shop_routes, 
    register_shop_cart_routes
)


app = FastAPI(title='Gateway API', version='0.1')

app.include_router(shop_service.router)
app.include_router(shop_cart_service.router)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await register_shop_routes()
    await register_shop_cart_routes()
    
    yield


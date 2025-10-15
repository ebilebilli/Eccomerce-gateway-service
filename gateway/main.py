from fastapi import FastAPI

from gateway.services import shop_service , shop_cart_service


app = FastAPI(title='Gateway API', version='0.1')


app.include_router(shop_service.router)
app.include_router(shop_cart_service.router)
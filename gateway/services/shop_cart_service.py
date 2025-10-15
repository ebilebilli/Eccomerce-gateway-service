import os
from dotenv import load_dotenv
from fastapi import APIRouter

from gateway.utils.forward import forward_request


load_dotenv()

SHOPCART_SERVICE = os.getenv('SHOPCART_SERVICE')
router = APIRouter(tags=['Shopcart Service'])


@router.post('/shopcart/', tags=['Shopcart Service'])
async def gateway_create_cart(data: dict):
    return await forward_request(f'{SHOPCART_SERVICE}/shopcart/', method='post', data=data)


@router.get('/shopcart/mycart', tags=['Shopcart Service'])
async def gateway_get_mycart():
    return await forward_request(f'{SHOPCART_SERVICE}/shopcart/mycart/')


@router.get('/shopcart/{cart_id}', tags=['Shopcart Service'])
async def gateway_get_cart(cart_id: str):
    return await forward_request(f'{SHOPCART_SERVICE}/shopcart/{cart_id}/')


@router.post('/shopcart/items', tags=['Shopcart Service'])
async def gateway_add_item(data: dict):
    return await forward_request(f'{SHOPCART_SERVICE}/shopcart/items/', method='post', data=data)


@router.put('/shopcart/items/update/{item_id}', tags=['Shopcart Service'])
async def gateway_update_item(item_id: str, data: dict):
    return await forward_request(f'{SHOPCART_SERVICE}/shopcart/items/update/{item_id}/', method='put', data=data)


@router.delete('/shopcart/items/delete/{item_id}', tags=['Shopcart Service'])
async def gateway_delete_item(item_id: str):
    return await forward_request(f'{SHOPCART_SERVICE}/shopcart/items/delete/{item_id}/', method='delete')
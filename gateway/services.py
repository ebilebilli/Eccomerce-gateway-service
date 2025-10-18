import os
from dotenv import load_dotenv


load_dotenv()

SHOP_SERVICE = os.getenv('SHOP_SERVICE')
SHOPCART_SERVICE = os.getenv('SHOPCART_SERVICE')


SERVICE_URLS = {
    'shop': SHOP_SERVICE,
    'cart': SHOPCART_SERVICE,
}

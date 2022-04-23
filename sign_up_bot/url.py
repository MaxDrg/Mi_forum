import json
import hashlib
import requests
import urllib.parse as urlparse
from urllib.parse import urlencode
from cloudipsp import Api, Checkout
from config import Config
cfg = Config()

class Web:
    def __init__(self, user_id: int):
        self.__telegr_id = user_id

    async def forum_url(self, passwd):
        params = {
            'telegr_id': self.__telegr_id,
            'passwd': passwd 
        }
        url_parts = list(urlparse.urlparse(cfg.url))
        query = dict(urlparse.parse_qsl(url_parts[4]))
        query.update(params)
        url_parts[4] = urlencode(query) 
        return urlparse.urlunparse(url_parts)

    async def pay_url(self, order_id: int, amount: int):
        api = Api(merchant_id = cfg.merchant_id,
        secret_key = cfg.payment_key)

        checkout = Checkout(api=api)

        data = f'{cfg.payment_key}|{amount}|USD|{cfg.merchant_id}|M3 Forum subscription payment|{order_id}'

        signature = hashlib.sha1(data.encode('utf-8')).hexdigest()

        params = {
            "order_id": order_id,
            "currency": "USD",
            "amount": amount,
            "order_desc": "M3 Forum subscription payment"
        }

        url = checkout.url(params).get('checkout_url')
        
        return url, signature
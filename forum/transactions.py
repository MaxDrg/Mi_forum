import json
import requests
from django.conf import settings

class Transaction:
    def __init__(self) -> None:
        self.__merchant_id = settings.MERCHANT_ID
        self.__url = settings.PAY_URL

    def check(self, order_id: int, signature: str):
        data = {
            "request": {
              "order_id": order_id,
              "merchant_id": self.__merchant_id,
              "signature": signature
            }
        }
        headers = {'Content-type': 'application/json'}
        response = requests.post(self.__url, data=json.dumps(data), headers=headers).json()

        print(response)
        
        if not response['response_status']:
            if response['order_status'] == 'approved':
                return True
            else: return False
        else: return False

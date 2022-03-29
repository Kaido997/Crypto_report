import requests
from time import sleep
from package.key import KEY

class Apiprep:
    def __init__(self, limit=1000):

        self.url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"

        self.parameters = {
            "start": "1",
            "limit": str(limit),
            "convert": "USD",
        }

        self.headers = {
            "Accepts": "application/json",
            "X-CMC_PRO_API_KEY": KEY,
        }

    def call_api(self):
        '''Function for calling api with error handling'''
        try:
            call = requests.get(
                url=self.url, headers=self.headers, params=self.parameters
            ).json()
            return call["data"]
        except:
            print("Something went wrong")
            sleep(2)
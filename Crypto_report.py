import json
from time import sleep
import requests
from datetime import datetime


class Repo:
    def __init__(self):

        self.api_key = input("Please enter the coinmarketcap API key:")

        self.url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"

        self.parameters = {
            "start": "1",
            "limit": "5000",
            "convert": "USD",
        }

        self.headers = {
            "Accepts": "application/json",
            "X-CMC_PRO_API_KEY": self.api_key,
        }

        self.top20_crypto = {}

        self.best_volume = {}

        self.top10 = {}

        self.worst10 = {}

        self.money = {}

        self.money_best_volume = {}

        self.earn_loss = {}

    # function for the api request and error handling in case of invalid api key
    def call_api(self):

        try:
            call = requests.get(
                url=self.url, headers=self.headers, params=self.parameters
            ).json()
            return call["data"]
        except:
            print("Invalid API key")
            sleep(1)

    def data_crawler(self):
        data = self.call_api()

        # finding the best volume crypto in the last 24h
        # cr is a temp variable
        temp_dict = {}
        for cr in data:
            temp_dict.update({cr["symbol"]: cr["quote"]["USD"]["volume_24h"]})

        max_value = max(temp_dict, key=temp_dict.get)
        self.best_volume.update({max_value: temp_dict[max_value]})

        temp_dict.clear()

        # creating a dictionary for the top 20 cryptos
        # and a dictionary of the money to purchase a unity of the cryptos with volume over 76 000 000$
        money_top_volume = 0
        for crypto in data:
            if crypto["cmc_rank"] <= 20:
                self.top20_crypto.update(
                    {
                        crypto["symbol"]: {
                            "volume_24h": crypto["quote"]["USD"]["volume_24h"],
                            "volume_change_24h": crypto["quote"]["USD"][
                                "volume_change_24h"
                            ],
                            "price": crypto["quote"]["USD"]["price"],
                            "percent_change_24h": crypto["quote"]["USD"][
                                "percent_change_24h"
                            ],
                        }
                    }
                )
            if crypto["quote"]["USD"]["volume_24h"] > 76000000:
                money_top_volume += crypto["quote"]["USD"]["price"]

        self.money_best_volume.update({"money_to_buy_bestvolume": money_top_volume})

        # Createing the best10 and worst10 list
        # t, j, k, are temp variable just for the 'for' loops
        temp_dict_2 = {}
        for t in data:
            temp_dict_2.update({t["symbol"]: t["quote"]["USD"]["percent_change_24h"]})

        for j in sorted(temp_dict_2.items(), key=lambda x: x[1], reverse=True):

            if len(self.top10) < 10:
                self.top10[j[0]] = j[1]

        for k in sorted(temp_dict_2.items(), key=lambda x: x[1]):

            if len(self.worst10) < 10:
                self.worst10[k[0]] = k[1]
        temp_dict_2.clear()

        # money to purchase a unity of the top 20 cryptos
        # and quantify the earn/loss percentage if buy one unity of the top 20 cryptos yesterday
        today_price_top20 = 0
        yesterday_price = 0
        earn_loss_percent = 0

        for s in self.top20_crypto:

            price = self.top20_crypto[s]["price"]
            percent_change_24h = self.top20_crypto[s]["percent_change_24h"]
            today_price_top20 += price

            if percent_change_24h < 0:
                loss = (price * abs(percent_change_24h)) / 100
                yesterday_price += price + loss
            else:
                earn = (price * percent_change_24h) / 100
                yesterday_price += price - earn

        if yesterday_price > today_price_top20:

            earn_loss_percent = -(
                abs(yesterday_price - today_price_top20) / yesterday_price * 100
            )
        else:
            earn_loss_percent = (
                abs(yesterday_price - today_price_top20) / yesterday_price * 100
            )

        self.money.update({"money_to_buy_top20": today_price_top20})
        self.earn_loss.update({"earn_loss_percent": earn_loss_percent, 'money_spent_yesterday':yesterday_price})

    # function for the json output
    def json_dump(self):

        try:
            self.data_crawler()

            time = datetime.now().strftime("%Y-%m-%d %H.%M.%S")

            json_output = {
                "top_20": self.top20_crypto,
                "best_volume_24h": self.best_volume,
                "best_10": self.top10,
                "worst_10": self.worst10,
                "money_to_buy": self.money,
                "earn_loss": self.earn_loss,
            }

            with open(f"{time}.json", "w", encoding="utf-8") as output:
                json.dump(json_output, output, ensure_ascii=False, indent=4)

        except:
            print("Error")

report = Repo()
report.json_dump()
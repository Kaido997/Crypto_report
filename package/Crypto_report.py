from dataclasses import dataclass
from datetime import datetime
from .apiprep import Apiprep
import json


class DataCrawler:

    def sortDatafromAPI(self, symbol: str, need: str, limit: int, *other: str) -> dict:
        '''Function for modifiing the given data from criptomarketcap api or from a file
         returning a dictionary with the needed data'''
        if limit:
            api = Apiprep(limit)
            data = api.call_api()
        else:
            api = Apiprep()
            data = api.call_api()

        temp_dict: dict = {}
        if not other:
            for crypto in data:
                temp_dict.update(
                    {crypto[symbol]: crypto["quote"]["USD"][need]})
        else:
            for crypto in data:
                temp_dict.update(
                    {crypto[symbol]: {need: crypto["quote"]["USD"][need]}})
                for args in other:
                    if args not in crypto.keys():
                        temp_dict[crypto[symbol]
                                  ][args] = crypto['quote']['USD'][args]
                    else:
                        temp_dict[crypto[symbol]][args] = crypto[args]
        return temp_dict

    def get_best_volume_crypto(self) -> dict[str, float]:
        '''This Function is for finding the best volume cryptoccurrences from the api'''
        this_dict = self.sortDatafromAPI("symbol", "volume_24h", 1000)
        max_value = max(this_dict, key=this_dict.get)
        return {max_value: this_dict[max_value]}

    def get_top20_crypto(self) -> dict:
        '''This function will return a dictionary containg the top 20 cryptoccurrences
        and the value of: actual prcice, percentage change 24h and rank'''

        get_dict = self.sortDatafromAPI(
            'symbol', 'price', 20, 'percent_change_24h', 'cmc_rank')
        top20_crypto: dict = {}
        for crypto in get_dict:
            top20_crypto.update({crypto: {
                                "price": get_dict[crypto]["price"], "percent_change_24h": get_dict[crypto]["percent_change_24h"], }})
        return top20_crypto

    def get_top76M_cost(self) -> dict:
        money: float = 0
        get_dict: dict = self.sortDatafromAPI(
            'symbol', 'volume_24h', 1000, 'price')
        for crypto in get_dict:
            if get_dict[crypto]['volume_24h'] > 76000000:
                money += get_dict[crypto]["price"]

        return {"money_top_volume": money}

    def get_top10(self):
        '''this function is for getting the top 10 cryptos by percentage change in 24h'''
        temp_dict: dict = self.sortDatafromAPI(
            'symbol', 'percent_change_24h', 2000)
        top10: dict = {}
        for j in sorted(temp_dict.items(), key=lambda x: x[1], reverse=True):

            if len(top10) < 10:
                top10[j[0]] = j[1]
        return top10

    def get_worst10(self):
        temp_dict: dict = self.sortDatafromAPI(
            'symbol', 'percent_change_24h', 2000)
        worst10: dict = {}

        for k in sorted(temp_dict.items(), key=lambda x: x[1]):

            if len(worst10) < 10:
                worst10[k[0]] = k[1]
        return worst10

    def get_top20_cost(self):
        '''this function return a dictionary with the total unity cost for each top 20 crypto'''
        temp_dict = self.sortDatafromAPI('symbol', 'price', 20,)
        today_price_top20 = 0
        for s in temp_dict:
            today_price_top20 += temp_dict[s]

        return {"money_to_buy_top20": today_price_top20}

    def get_earn_loss(self):
        '''function to return the earn or loss percentage if buy a unity of the top 20 crypto the day before'''
        data = self.sortDatafromAPI('symbol', 'percent_change_24h', 20, 'price')
        temp_dict = self.get_top20_cost()
        percent_change_24h = 0
        yesterday_price = 0
        earn_loss_percent = 0
        price = 0

        for s in data:
            percent_change_24h = data[s]["percent_change_24h"]
            price = data[s]['price']

            yesterday_price += price / (1 + (percent_change_24h / 100))

        earn_loss_percent = (
            (temp_dict['money_to_buy_top20'] - yesterday_price) / yesterday_price) * 100

        return {
            "earn_loss_percent": earn_loss_percent,
            "money_spent_yesterday": yesterday_price,
        }




def json_dump():
    '''simple function for wrapping all data and dump a json file'''
    try:
        data = DataCrawler()
        time = datetime.now().strftime("%Y-%m-%d %H.%M.%S")

        json_output = {
            "top_20": data.get_top20_crypto(),
            "top_20_cost": data.get_top20_cost(),
            "best_volume_24h": data.get_best_volume_crypto(),
            "best_10": data.get_top10(),
            "worst_10": data.get_worst10(),
            "money_to_buy_top_76M": data.get_top76M_cost(),
            "earn_loss": data.get_earn_loss(), 
        }

        with open(f"{time}.json", "w", encoding="utf-8") as output:
            json.dump(json_output, output, ensure_ascii=False, indent=4)
    except:
        print("Error")


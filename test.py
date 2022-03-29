import unittest as ut
from package import Crypto_report as Cr

class UnitTest(ut.TestCase):
    
    def test_best_volume(self):
        instance = Cr.DataCrawler()
        actual : dict = instance.get_best_volume_crypto()
        expected : dict[str, float] = {"USDT" : actual["USDT"]} 
        self.assertDictEqual(actual, expected, 'Expected calling "get_best_volume_crypto()" and return a dictionary with USDT as key')

    def test_top20(self):
        instance = Cr.DataCrawler()
        actual : dict = len(instance.get_top20_crypto().keys())
        expected = 20
        self.assertEqual(actual, expected, 'Expected calling "get_top20_crypto()" and return a dictionray with 20 keys')

    def test_volume_graterThen_76kk(self):
        instance = Cr.DataCrawler()
        actual : dict = instance.get_top76M_cost()
        expected : dict = {'money_top_volume' : actual['money_top_volume']}
        self.assertEqual(actual, expected, 'Expected calling "get_money_qunatiy()" and return a dict with the total money needed')

    def test_top10(self):
        instance = Cr.DataCrawler()
        actual : dict = len(instance.get_top10())
        expected : dict = 10
        self.assertEqual(actual, expected, 'Expected calling "get_top10()" and return a dict with the top 10 best change incremet crypto')

    def test_worst10(self):
        instance = Cr.DataCrawler()
        actual : dict = len(instance.get_worst10())
        expected : dict = 10
        self.assertEqual(actual, expected, 'Expected calling "get_worst10()" and return a dict with the worst 10 change incremet crypto')
        

    def test_money_to_buy_top20(self):
        instance = Cr.DataCrawler()
        actual : dict = instance.get_top20_cost()
        expected : dict = actual
        self.assertEqual(actual, expected, 'Expected calling "get_worst10()" and return a dict with the worst 10 change incremet crypto')
    
    def test_earn_loss(self):
        instance = Cr.DataCrawler()
        temp = instance.get_earn_loss()
        totCost = instance.get_top20_cost()
        actual = temp['earn_loss_percent']
        expected = ((totCost['money_to_buy_top20'] - temp['money_spent_yesterday']) / temp['money_spent_yesterday']) * 100
        self.assertEqual(actual, expected, 'Expected calling "get_worst10()" and return a dict with the worst 10 change incremet crypto')

if __name__ == "__main__":
    ut.main()
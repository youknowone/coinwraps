
from .base import APIBase, CurrencyImplBase


class API(APIBase, name='bithumb'):

    URL_PREFIX = 'https://api.bithumb.com'
    TICKER_URL = (URL_PREFIX + '/public/ticker/{currency}').format

    def ticker(self, currency):
        url = self.TICKER_URL(currency=currency)
        response = self.session.get(url)
        return response.json()


class Currency(CurrencyImplBase, api=API):

    def __init__(self, api, pair):
        c1, c2 = pair
        assert c2 == 'KRW'
        super().__init__(api, pair)

    def last(self):
        r = self.api.ticker(self.pair[0])
        data = r['data']
        p = (float(data['buy_price']) + float(data['sell_price'])) / 2
        return p


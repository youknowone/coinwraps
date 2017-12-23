from .base import APIBase, CurrencyImplBase


class API(APIBase, name='coinone'):

    URL_PREFIX = 'https://api.coinone.co.kr'
    TICKER_URL = f'{URL_PREFIX}/ticker/'

    def ticker(self, currency):
        url = self.TICKER_URL
        response = self.session.get(url, params={'currency': currency})
        return response.json()


class Currency(CurrencyImplBase, api=API):

    def __init__(self, api, pair):
        c1, c2 = pair
        assert c2 == 'KRW'
        super().__init__(api, pair)

    def last(self):
        r = self.api.ticker(self.pair[0])
        return r['last']

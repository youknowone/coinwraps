from .base import APIBase, CurrencyImplBase
import ring


class API(APIBase, name='coinone'):

    URL_PREFIX = 'https://api.coinone.co.kr'
    TICKER_URL = f'{URL_PREFIX}/ticker/'

    def __ring_key__(self):
        return 'coinone'

    @ring.func.dict({}, expire=5)
    def ticker(self, currency):
        url = self.TICKER_URL
        response = self.session.get(url, params={'currency': currency})
        parsed_data = response.json()
        if currency.lower() == 'all':
            for code, row in parsed_data.items():
                self.ticker.set(row, code)
        return parsed_data


class Currency(CurrencyImplBase, api=API):

    def __init__(self, api, pair):
        c1, c2 = pair
        assert c2 == 'KRW'
        super().__init__(api, pair)

    def last(self):
        r = self.api.ticker(self.pair[0].lower())
        return float(r['last'])

from .base import ClientBase, APIBase, CurrencyImplBase
import ring


class Client(ClientBase, name='coinone'):
    pass


class API(APIBase, client=Client):

    URL_PREFIX = 'https://api.coinone.co.kr'
    TICKER_URL = f'{URL_PREFIX}/ticker/'
    ORDERBOOK_URL = f'{URL_PREFIX}/orderbook/'

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

    @ring.func.dict({}, expire=5)
    def orderbook(self, currency):
        url = self.ORDERBOOK_URL
        response = self.session.get(url, params={'currency': currency})
        parsed_data = response.json()
        return parsed_data


class Currency(CurrencyImplBase, client=Client):

    def __init__(self, api, pair):
        c1, c2 = pair
        assert c2 == 'KRW'
        super().__init__(api, pair)

    @property
    def _currency(self):
        return self.pair[0].lower()

    def bid(self):
        r = self.api.orderbook(self._currency)
        return float(r['bid'][0]['price'])

    def ask(self):
        r = self.api.orderbook(self._currency)
        return float(r['ask'][0]['price'])

    def last(self):
        r = self.api.ticker(self.pair[0].lower())
        return float(r['last'])

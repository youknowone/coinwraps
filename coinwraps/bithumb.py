from .base import ClientBase, APIBase, CurrencyImplBase
import ring


class Client(ClientBase, name='bithumb'):
    pass


class API(APIBase, client=Client):

    URL_PREFIX = 'https://api.bithumb.com'
    TICKER_URL = (URL_PREFIX + '/public/ticker/{currency}').format

    def __ring_key__(self):
        return 'bithumb'

    @ring.func.dict({}, expire=5)
    def ticker(self, currency):
        url = self.TICKER_URL(currency=currency)
        response = self.session.get(url)
        parsed_data = response.json()['data']
        if currency == 'ALL':
            for code, row in parsed_data.items():
                self.ticker.set(row, code)
        return parsed_data


class Currency(CurrencyImplBase, client=Client):

    def __init__(self, api, pair):
        c1, c2 = pair
        assert c2 == 'KRW'
        super().__init__(api, pair)

    @property
    def _currency(self):
        return self.pair[0]

    def last(self):
        data = self.api.ticker(self._currency)
        p = (float(data['buy_price']) + float(data['sell_price'])) / 2
        return p

    def bid(self):
        data = self.api.ticker(self._currency)
        return float(data['sell_price'])

    def ask(self):
        data = self.api.ticker(self._currency)
        return float(data['buy_price'])

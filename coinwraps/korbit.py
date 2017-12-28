from .base import ClientBase, APIBase, CurrencyImplBase
import ring


class Client(ClientBase, name='korbit'):
    pass


class API(APIBase, client=Client):

    URL_PREFIX = 'https://api.korbit.co.kr'
    TICKER_URL = f'{URL_PREFIX}/v1/ticker/detailed'

    def __ring_key__(self):
        return 'korbit'

    @ring.func.dict({}, expire=5)
    def ticker(self, currency):
        url = self.TICKER_URL
        response = self.session.get(
            url, params={'currency_pair': f'{currency.lower()}_krw'})
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

    def last(self):
        r = self.api.ticker(self._currency)
        return float(r['last'])

    def ask(self):
        r = self.api.ticker(self._currency)
        return float(r['ask'])

    def bid(self):
        r = self.api.ticker(self._currency)
        return float(r['bid'])

from .base import APIBase, CurrencyImplBase
import ring


class API(APIBase, name='korbit'):

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


class Currency(CurrencyImplBase, api=API):

    def __init__(self, api, pair):
        c1, c2 = pair
        assert c2 == 'KRW'
        super().__init__(api, pair)

    def last(self):
        r = self.api.ticker(self.pair[0].lower())
        return float(r['last'])

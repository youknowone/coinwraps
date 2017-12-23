from .base import APIBase, CurrencyImplBase
import ring


class API(APIBase, name='bithumb'):

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


class Currency(CurrencyImplBase, api=API):

    def __init__(self, api, pair):
        c1, c2 = pair
        assert c2 == 'KRW'
        super().__init__(api, pair)

    def last(self):
        data = self.api.ticker(self.pair[0])
        p = (float(data['buy_price']) + float(data['sell_price'])) / 2
        return p

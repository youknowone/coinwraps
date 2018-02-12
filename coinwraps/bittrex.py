from .base import ClientBase, APIBase, CurrencyImplBase
from .typing import Orderbook, HistoryItem
from decimal import Decimal
import ring


# NOTE: https://bittrex.com/home/api
# We are currently restricting orders to 500 open orders and 200,000 orders a day. We reserve the right to change these settings as we tune the system. If you are affected by these limits as an active trader, please email support@bittrex.com.


class Client(ClientBase, name='bittrex'):
    pass


class API(APIBase, client=Client):

    URL_PREFIX = 'https://bittrex.com/api/v1.1'
    TICKER_URL = f'{URL_PREFIX}/public/getticker'
    ORDERBOOK_URL = f'{URL_PREFIX}/public/getorderbook'
    MARKETHISTORY_URL = f'{URL_PREFIX}/public/getmarkethistory'

    def __ring_key__(self):
        return 'bittrex'

    @ring.func.dict({}, expire=5)
    def getticker(self, market):
        url = self.TICKER_URL
        response = self.session.get(
            url, params={'market': market})
        parsed_data = response.json()
        assert parsed_data['success'] is True, parsed_data
        return parsed_data['result']

    def getorderbook(self, market, type='both'):
        url = self.ORDERBOOK_URL
        response = self.session.original_request(
            'get',
            url, params={'market': market, 'type': type})
        parsed_data = response.json()
        assert parsed_data['success'] is True, parsed_data
        return parsed_data['result']

    def getmarkethistory(self, market, type='both'):
        url = self.MARKETHISTORY_URL
        response = self.session.original_request(
            'get',
            url, params={'market': market})
        parsed_data = response.json()
        assert parsed_data['success'] is True, parsed_data
        return parsed_data['result']


def _flatten_orderbook(item):
    return Decimal(item['Rate']), Decimal(item['Quantity'])


class Currency(CurrencyImplBase, client=Client):

    def __init__(self, api, pair):
        c1, c2 = pair
        super().__init__(api, pair)

    @property
    def _market(self):
        return f'{self.pair[1]}-{self.pair[0]}'

    def last(self):
        data = self.api.getticker(self._market)
        return data['Last']

    def bid(self):
        data = self.api.getticker(self._market)
        return data['Bid']

    def ask(self):
        data = self.api.getticker(self._market)
        return data['Ask']

    def orderbook(self):
        data = self.api.getorderbook(self._market)
        return Orderbook(
            list(map(_flatten_orderbook, data['sell'])),
            list(map(_flatten_orderbook, data['buy'])),
        )

    def history(self):
        data = self.api.getmarkethistory(self._market)
        return [HistoryItem(
            i['Id'], i['TimeStamp'],
            i['FillType'].upper(), i['OrderType'].upper(),
            Decimal(i['Price']), Decimal(i['Quantity']), Decimal(i['Total']),
        ) for i in data]

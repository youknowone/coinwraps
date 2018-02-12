from .base import ClientBase, APIBase, CurrencyImplBase
from .typing import Orderbook, HistoryItem
from decimal import Decimal
import ring


class Client(ClientBase, name='poloniex'):
    pass


class API(APIBase, client=Client):

    PUBLIC_URL = 'https://poloniex.com/public'

    def __ring_key__(self):
        return 'poloniex'

    @ring.func.dict({}, expire=5)
    def return_ticker(self, market):
        url = self.PUBLIC_URL
        response = self.session.get(
            url, params={'command': 'returnTicker'})
        parsed_data = response.json()
        return parsed_data

    def return_order_book(self, currency_pair, depth=10):
        url = self.PUBLIC_URL
        response = self.session.original_request(
            'get',
            url,
            params={
                'command': 'returnOrderBook',
                'currencyPair': currency_pair,
                'depth': depth})
        parsed_data = response.json()
        return parsed_data

    def return_trade_history(self, currency_pair, type='both'):
        url = self.PUBLIC_URL
        response = self.session.original_request(
            'get',
            url,
            params={
                'command': 'returnTradeHistory',
                'currencyPair': currency_pair})
        parsed_data = response.json()
        return parsed_data


class Currency(CurrencyImplBase, client=Client):

    def __init__(self, api, pair):
        c1, c2 = pair
        super().__init__(api, pair)

    @property
    def _currency_pair(self):
        return f'{self.pair[1]}_{self.pair[0]}'

    def last(self):
        data = self.api.return_ticker()
        return data[self._currency_pair]['last']

    def bid(self):
        data = self.api.return_order_book(self._currency_pair)
        return data['bids'][0]

    def ask(self):
        data = self.api.return_order_book(self._currency_pair)
        return data['asks'][0]

    def orderbook(self):
        data = self.api.return_order_book(self._currency_pair)
        return Orderbook(
            [(Decimal(i[0]), Decimal(i[1])) for i in data['asks']],
            [(Decimal(i[0]), Decimal(i[1])) for i in data['bids']])

    def history(self):
        data = self.api.return_trade_history(self._currency_pair)
        return [HistoryItem(
            f"{i['date']}-{i['rate']}-{i['amount']}", i['date'],
            None, i['type'].upper(),
            Decimal(i['rate']), Decimal(i['amount']), Decimal(i['total']),
        ) for i in data]

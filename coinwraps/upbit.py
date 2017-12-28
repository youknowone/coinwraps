import ring
from .base import ClientBase, APIBase, CurrencyImplBase


class Client(ClientBase, name='upbit'):
    pass


class API(APIBase, client=Client):

    URL_PREFIX = 'https://crix-api.upbit.com/v1'
    RECENT_URL = f'{URL_PREFIX}/crix/recent'
    HEADERS = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en',
        'Connection': 'keep-alive',
        'DNT': '1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:57.0) Gecko/20100101 Firefox/57.0'
    }
    FORMAT_CRIX_CODE = 'CRIX.UPBIT.{to_currency}-{from_currency}'.format

    def __ring_key__(self):
        return 'upbit'

    def fetch_recent(self, codes):
        url = self.RECENT_URL
        combined_codes = ','.join(codes)
        params = {'codes': combined_codes}
        response = self.session.get(url, params=params, headers=self.HEADERS)
        data = response.json()
        for row in data:
            self.recent.set(row, row['code'])
        return data

    @ring.func.dict({}, expire=5.0)  # 5 seconds cache
    def recent(self, code):
        full_data = self.fetch_recent([code])
        # logging.warning('fetch full:', full_data)
        data = full_data[0]
        return data


class Currency(CurrencyImplBase, client=Client):

    def last(self):
        code = self.api.FORMAT_CRIX_CODE(
            to_currency=self.pair[1], from_currency=self.pair[0])
        r = self.api.recent(code)
        return r['tradePrice']

    def ask(self):
        # no ask
        return self.last()

    def bid(self):
        # no bid
        return self.last()

from .base import APIBase, CurrencyImplBase


class API(APIBase, name='upbit'):

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

    def recent(self, to_currency, from_currency):
        url = self.RECENT_URL
        params = {'codes': f'CRIX.UPBIT.{to_currency}-{from_currency}'}
        response = self.session.get(url, params=params, headers=self.HEADERS)

        try:
            data = response.json()
        except Exception:
            print(response.text)
            raise
        return data


class Currency(CurrencyImplBase, api=API):

    def last(self):
        r = self.api.recent(self.pair[1], self.pair[0])
        return r[0]['tradePrice']

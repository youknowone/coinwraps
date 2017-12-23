from .base import APIBase, CurrencyImplBase


class API(APIBase, name='upbit'):

    URL_PREFIX = 'https://crix-api.upbit.com/v1'
    RECENT_URL = f'{URL_PREFIX}/crix/recent'

    def recent(self, to_currency, from_currency):
        url = self.RECENT_URL
        params = {'codes': f'CRIX.UPBIT.{to_currency}-{from_currency}'}
        response = self.session.get(url, params=params)

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

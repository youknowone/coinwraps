import json
from .base import APIBase, CurrencyImplBase
import aiohttp
import ring


class API(APIBase, name='korbit'):

    URL_PREFIX = 'https://api.korbit.co.kr'
    TICKER_URL = f'{URL_PREFIX}/v1/ticker/detailed'

    def __ring_key__(self):
        return 'korbit'

    @ring.func_asyncio.dict({}, expire=5)
    async def ticker(self, currency):
        url = self.TICKER_URL
        async with self.aiohttp_session as session:
            response = await session.get(
                url, params={'currency_pair': f'{currency.lower()}_krw'})
        plain_data = await response.text()
        return json.loads(plain_data)


class Currency(CurrencyImplBase, api=API):

    def __init__(self, api, pair):
        c1, c2 = pair
        assert c2 == 'KRW'
        super().__init__(api, pair)

    async def last(self):
        r = await self.api.ticker(self.pair[0].lower())
        return float(r['last'])

import coinwraps

import pytest


@pytest.mark.parametrize('api_name', [
    'bithumb',
    'coinone',
    'korbit',
])
@pytest.mark.asyncio
async def test_ticker(api_name):
    api = getattr(coinwraps, f'{api_name}_api')
    ticker = await api.ticker('eth')
    assert ticker


@pytest.mark.parametrize('api_name', [
    'bithumb',
    'coinone',
    'korbit',
    'upbit',
])
@pytest.mark.asyncio
async def test_last(api_name):
    api = getattr(coinwraps, f'{api_name}_api')
    price = await api.currency(('BTC', 'KRW')).last()
    assert isinstance(price, float)

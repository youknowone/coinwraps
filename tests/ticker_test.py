import coinwraps

import pytest


@pytest.mark.parametrize('api_name', [
    'bithumb',
    'coinone',
    'korbit',
])
def test_krw_ticker(api_name):
    api = getattr(coinwraps, f'{api_name}_api')
    assert api.ticker('eth')


@pytest.mark.parametrize('api_name', [
    'bithumb',
    'coinone',
    'korbit',
    'upbit',
])
def test_last(api_name):
    api = getattr(coinwraps, f'{api_name}_api')
    assert api.currency(('BTC', 'KRW')).last()

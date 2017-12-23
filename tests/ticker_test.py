import coinwraps

import pytest


@pytest.mark.parametrize('api', [
    coinwraps.bithumb.API(),
    coinwraps.coinone.API(),
])
def test_krw_ticker(api):
    assert api.ticker('eth')


@pytest.mark.parametrize('api', [
    coinwraps.bithumb.API(),
    coinwraps.coinone.API(),
    coinwraps.upbit.API(),
])
def test_last(api):
    assert api.currency(('BTC', 'KRW')).last()

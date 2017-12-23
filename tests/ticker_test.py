import coinwraps

import pytest


@pytest.mark.parametrize('api', [
    coinwraps.bithumb.API(),
    coinwraps.coinone.API(),
])
def test_krw_ticker(api):
    assert api.ticker('eth')

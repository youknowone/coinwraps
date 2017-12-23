import coinwraps

import pytest


@pytest.mark.parametrize('client_name', [
    'bithumb',
    'coinone',
    'korbit',
])
def test_krw_ticker(client_name):
    client = coinwraps.clients[client_name]
    assert client.api.ticker('eth')


@pytest.mark.parametrize('client_name', [
    'bithumb',
    'coinone',
    'korbit',
    'upbit',
])
def test_last(client_name):
    client = coinwraps.clients[client_name]
    assert client.currency(('BTC', 'KRW')).last()

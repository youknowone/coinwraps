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
    'upbit',
    'bittrex',
])
def test_btc_last(client_name):
    client = coinwraps.clients[client_name]
    assert client.currency(('ETH', 'BTC')).ask()
    assert client.currency(('ETC', 'BTC')).bid()


@pytest.mark.parametrize('client_name', [
    'bithumb',
    'coinone',
    'korbit',
    'upbit',
])
def test_last(client_name):
    client = coinwraps.clients[client_name]
    assert client.currency(('BTC', 'KRW')).last()
    assert client.currency(('ETH', 'KRW')).ask()
    assert client.currency(('ETC', 'KRW')).bid()


def test_upbit():
    client = coinwraps.clients['upbit']
    assert client.currency(('DOGE', 'BTC')).last()

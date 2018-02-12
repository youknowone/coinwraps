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
    'poloniex',
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
    assert client.currency(('LTC', 'BTC')).last()


@pytest.mark.parametrize('client_name', [
    'poloniex',
    'bittrex',
])
def test_orderbook(client_name):
    client = coinwraps.clients[client_name]
    orderbook = client.currency(('LTC', 'BTC')).orderbook()
    ask = orderbook.asks[0]
    bid = orderbook.bids[0]
    assert ask[0] > bid[0]


@pytest.mark.parametrize('client_name', [
    'poloniex',
    'bittrex',
])
def test_history(client_name):
    client = coinwraps.clients[client_name]
    history = client.currency(('LTC', 'BTC')).history()
    item1 = history[0]
    item2 = history[1]
    assert item1.filled_at > item2.filled_at

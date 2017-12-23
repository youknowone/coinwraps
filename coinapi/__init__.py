from coinapi.base import CurrencyPair
import coinapi.bithumb  # noqa


def create_pair(c1, c2):
    pair = CurrencyPair((c1, c2))
    return pair
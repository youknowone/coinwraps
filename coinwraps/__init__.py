from coinwraps.base import CurrencyPair
import coinwraps.bithumb  # noqa
import coinwraps.coinone  # noqa
import coinwraps.korbit  # noqa
import coinwraps.upbit  # noqa

__all__ = 'CurrencyPair',

bithumb_api = coinwraps.bithumb.API.shared_api
coinone_api = coinwraps.coinone.API.shared_api
korbit_api = coinwraps.korbit.API.shared_api
upbit_api = coinwraps.upbit.API.shared_api

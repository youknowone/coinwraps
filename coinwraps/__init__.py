from coinwraps.base import CurrencyPair, APIBase
import coinwraps.bithumb  # noqa
import coinwraps.coinone  # noqa
import coinwraps.korbit  # noqa
import coinwraps.upbit  # noqa

__all__ = 'CurrencyPair',

bithumb_api: coinwraps.bithumb.API = ...
coinone_api: coinwraps.coinone.API = ...
korbit_api: coinwraps.korbit.API = ...
upbit_api: coinwraps.upbit.API = ...


async def init():
    global bithumb_api, coinone_api, korbit_api, upbit_api
    await APIBase.registry.asyncio_register_all()

    bithumb_api = coinwraps.bithumb.API.shared_api
    coinone_api = coinwraps.coinone.API.shared_api
    korbit_api = coinwraps.korbit.API.shared_api
    upbit_api = coinwraps.upbit.API.shared_api

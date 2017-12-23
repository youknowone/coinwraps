import coinwraps
from coinwraps.base import CurrencyPair
import importlib

__all__ = 'CurrencyPair',


clients = {}
client_names = [
    'korbit', 'bithumb', 'coinone', 'upbit']

for client_name in client_names:
    module = importlib.import_module(f'coinwraps.{client_name}')
    module.client = getattr(coinwraps, client_name).Client.shared
    clients[client_name] = module.client

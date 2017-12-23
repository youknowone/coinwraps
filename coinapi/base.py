from typing import Tuple, Dict
import requests


class RegistryBase:

    registrations: Dict[str, str]

    def __init__(self):
        self.registrations = {}

    def register(self, key, value):
        self.registrations[key] = value

    def get(self, key):
        return self.registrations[key]


class APIBase:
    registry = RegistryBase()
    name: str

    def __init_subclass__(cls, name, **kwargs):
        cls.name = name
        cls.registry.register(name, cls())

    def __init__(self):
        self.session = requests.Session()

    def currency(self, pair):
        return self.currency_impl(self, pair)


class CurrencyImplBase:

    def __init_subclass__(cls, api):
        api.currency_impl = cls

    def __init__(self, api, pair):
        self.api = api
        self.pair = pair


class CurrencyPair:
    pair: Tuple[str, str]

    def __init__(self, pair):
        c1, c2 = [c.upper() for c in pair]
        self.pair = c1, c2

    def exchange(self, name):
        api = APIBase.registry.get(name)
        return api.currency(self.pair)

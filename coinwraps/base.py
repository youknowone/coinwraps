from typing import Tuple, Dict
import time
import requests
import logging


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
        cls.shared_api = cls()
        cls.registry.register(name, cls.shared_api)

    def __init__(self):
        self.session = requests.Session()
        original_request = self.session.request
        last_time = 0.0

        def safe_request(*args, **kwargs):
            nonlocal last_time
            now = time.time()
            if now - last_time < 1.0:
                sleep_time = 1 - (now - last_time)
                logging.warning(f'sleep {sleep_time} to prevent attack')
                time.sleep(sleep_time)
            last_time = time.time()
            response = original_request(*args, **kwargs)
            return response

        self.session.request = safe_request

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

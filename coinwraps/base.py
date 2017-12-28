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


class ClientBase:
    registry = RegistryBase()
    name: str

    def __init_subclass__(cls, name, **kwargs):
        cls.name = name
        cls.shared = cls()
        cls.registry.register(name, cls.shared)

    def __repr__(self):
        return '{self.__class__.__name__}(name={self.name})'

    def currency(self, pair):
        return self.currency_impl(self, pair)


class APIBase:

    def __init_subclass__(cls, client):
        client.api = cls(client)

    def __init__(self, client):
        self.client = client
        self.session = requests.Session()
        original_request = self.session.request
        last_time = 0.0

        def safe_request(*args, **kwargs):
            nonlocal last_time
            now = time.time()
            if now - last_time < 1.0:
                sleep_time = 1 - (now - last_time)
                logging.warning(f'sleep {sleep_time} to prevent attack to {client}')
                time.sleep(sleep_time)
            last_time = time.time()
            response = original_request(*args, **kwargs)
            return response

        self.session.request = safe_request


class CurrencyImplBase:

    def __init_subclass__(cls, client):
        client.currency_impl = cls

    def __init__(self, client, pair):
        self.client = client
        self.pair = pair

    @property
    def api(self):
        return self.client.api


class CurrencyPair:
    pair: Tuple[str, str]

    def __init__(self, pair):
        c1, c2 = [c.upper() for c in pair]
        self.pair = c1, c2

    def exchange(self, name):
        client = ClientBase.registry.get(name)
        return client.currency(self.pair)

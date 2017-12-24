from typing import Tuple, Dict
import time
import asyncio
import aiohttp
import logging


class RegistryBase:

    registrations: Dict[str, str]

    def __init__(self):
        self.registrations = {}
        self.async_registrations = {}

    def register(self, key, value, use_asyncio=False):
        if use_asyncio:
            registrations = self.registrations
        else:
            registrations = self.async_registrations
        registrations[key] = value

    def get(self, key):
        return self.registrations[key]

    async def asyncio_register_all(self):
        assert self.async_registrations
        for name, register in self.async_registrations:
            self.registrations[name] = await register()
        self.async_registrations = None  # finalize


class APIBase:
    registry = RegistryBase()
    name: str

    def __init_subclass__(cls, name, **kwargs):
        cls.name = name

        async def register(registry):
            cls.shared_api = cls()
            await cls.shared_api.init()
            return cls.shared_api

        cls.registry.register(name, register, use_asyncio=True)

    async def init(self):
        self.aiohttp_session = aiohttp.ClientSession()
        last_time = 0.0
        original_request = self.aiohttp_session.request

        async def safe_request(*args, **kwargs):
            nonlocal last_time
            now = time.time()
            if now - last_time < 1.0:
                sleep_time = 1 - (now - last_time)
                logging.warning(f'sleep {sleep_time} to prevent attack')
                asyncio.sleep(sleep_time)
            last_time = time.time()
            response = await original_request(*args, **kwargs)
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

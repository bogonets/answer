# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod
from aiohttp.web import Application


class HttpAppCallback(metaclass=ABCMeta):
    """
    HTTP Application callback methods.
    """

    @abstractmethod
    async def on_startup(self, app: Application):
        raise NotImplementedError

    @abstractmethod
    async def on_shutdown(self, app: Application):
        raise NotImplementedError

    @abstractmethod
    async def on_cleanup(self, app: Application):
        raise NotImplementedError


class EmptyHttpAppCallback(HttpAppCallback):
    async def on_startup(self, app: Application):
        pass

    async def on_shutdown(self, app: Application):
        pass

    async def on_cleanup(self, app: Application):
        pass

# -*- coding: utf-8 -*-

from asyncio import AbstractEventLoop, CancelledError, Event, wait_for
from typing import Final, Optional

from aiohttp.web import Application
from overrides import overrides

from recc.config import Config
from recc.core.context import Context
from recc.http.http_app import HttpApp
from recc.http.http_client import HttpClient
from recc.http.http_interface import EmptyHttpAppCallback
from recc.logging.logging import recc_http_logger as logger
from recc.variables.http import DEFAULT_SCHEME

DEFAULT_ADMIN_USERNAME: Final[str] = "admin"
DEFAULT_ADMIN_PASSWORD: Final[str] = "0000"
DEFAULT_WAIT_STARTUP: Final[float] = 8.0


class HttpAppTester(HttpClient, EmptyHttpAppCallback):
    def __init__(self, loop: Optional[AbstractEventLoop] = None):
        config = Config.test()
        scheme = DEFAULT_SCHEME
        bind = config.http_bind
        port = config.http_port
        timeout = config.http_timeout
        super().__init__(f"{bind}:{port}", timeout=timeout, scheme=scheme)

        self._context = Context(config, loop=loop)
        self._app = HttpApp(context=self._context, callback=self)
        self._startup = Event()

    @property
    def context(self) -> Context:
        return self._context

    @overrides
    async def on_startup(self, app: Application):
        self._startup.set()

    @overrides
    async def on_shutdown(self, app: Application):
        self._startup.clear()

    @overrides
    async def on_request_begin(self):
        await self._startup.wait()

    async def setup(self) -> None:
        await self._app.start()

    async def teardown(self) -> None:
        try:
            self._app.task_cancel()
            await self._app.wait_for_termination()
        except CancelledError:
            pass
        finally:
            self._app.close_socket()

    async def wait_startup(
        self,
        timeout: Optional[float] = DEFAULT_WAIT_STARTUP,
    ) -> None:
        if timeout is not None and timeout > 0:
            logger.debug(f"Waiting for startup ... {timeout}s")
            await wait_for(self._startup.wait(), timeout)
        else:
            logger.debug("Waiting for startup ...")
            await self._startup.wait()

    async def signup(self, username: str, password: str) -> None:
        config_stash = self.context.config.public_signup
        try:
            self.context.config.public_signup = True
            await self.signup_public(username, password)
        finally:
            self.context.config.public_signup = config_stash

    async def signup_default_admin(self):
        await self.signup_admin(DEFAULT_ADMIN_USERNAME, DEFAULT_ADMIN_PASSWORD)

    async def signup_and_in_default_admin(self, save_session=True) -> None:
        await self.signup_and_in(
            username=DEFAULT_ADMIN_USERNAME,
            password=DEFAULT_ADMIN_PASSWORD,
            save_session=save_session,
        )

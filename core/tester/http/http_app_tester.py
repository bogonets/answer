# -*- coding: utf-8 -*-

from typing import Optional, Final
from overrides import overrides
from asyncio import Task, Event, AbstractEventLoop, CancelledError
from tempfile import TemporaryDirectory
from aiohttp.web import Application
from recc.argparse.default_parser import parse_arguments_to_core_config
from recc.http.http_client import HttpClient
from recc.http.http_interface import EmptyHttpAppCallback
from recc.http.http_app import HttpApp
from recc.core.context import Context
from recc.variables.http import DEFAULT_HTTP_TEST_PORT, DEFAULT_SCHEME

DEFAULT_ADMIN_USERNAME: Final[str] = "admin"
DEFAULT_ADMIN_PASSWORD: Final[str] = "0000"


class HttpAppTester(HttpClient, EmptyHttpAppCallback):

    _app: HttpApp
    _task: Task

    def __init__(
        self,
        loop: Optional[AbstractEventLoop] = None,
        storage_root: Optional[str] = None,
    ):
        config = parse_arguments_to_core_config()
        config.developer = True
        config.teardown = True
        config.database_name = "recc.test"
        config.cache_prefix = "recc.test"
        config.http_port = DEFAULT_HTTP_TEST_PORT
        config.public_signup = False
        config.verbose = 0

        if storage_root:
            temp = None
            config.local_storage = storage_root
        else:
            temp = TemporaryDirectory()
            config.local_storage = temp.name

        scheme = DEFAULT_SCHEME
        bind = config.http_bind
        port = config.http_port
        timeout = config.http_timeout
        super().__init__(f"{bind}:{port}", timeout=timeout, scheme=scheme)

        self._temp = temp
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
    async def on_cleanup(self, app: Application):
        if self._temp:
            self._temp.cleanup()

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

    async def wait_startup(self) -> None:
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

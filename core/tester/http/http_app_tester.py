# -*- coding: utf-8 -*-

from hashlib import sha256
from typing import Optional, Final
from overrides import overrides
from http import HTTPStatus
from asyncio import Task, Event, AbstractEventLoop, CancelledError
from tempfile import TemporaryDirectory
from aiohttp.hdrs import AUTHORIZATION
from aiohttp.web import Application
from recc.argparse.default_parser import parse_arguments_to_core_config
from recc.http.header.basic_auth import BasicAuth
from recc.http.v1 import path_v1 as pv1
from recc.http.v1.common import get_v1_path
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
        config.http_port = DEFAULT_HTTP_TEST_PORT
        config.public_signup = False
        config.verbose = 0

        if storage_root:
            temp = None
            config.storage_root = storage_root
        else:
            temp = TemporaryDirectory()
            config.storage_root = temp.name

        scheme = DEFAULT_SCHEME
        bind = config.http_bind
        port = config.http_port
        timeout = config.http_timeout
        super().__init__(f"{bind}:{port}", scheme, timeout)

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

    async def run_v1_admin_login(
        self,
        username=DEFAULT_ADMIN_USERNAME,
        password=DEFAULT_ADMIN_PASSWORD,
    ) -> None:
        if not username:
            raise ValueError("A `username` argument is required.")
        if not password:
            raise ValueError("A `password` argument is required.")

        self.username = username
        self.password = password
        assert self.username
        assert self.password

        hashed_pw = sha256(self.password.encode(encoding="utf-8")).hexdigest()
        signup_response = await self.post(
            path=get_v1_path(pv1.signup_admin),
            data={"id": self.username, "password": hashed_pw},
        )
        if signup_response.status != HTTPStatus.OK:
            raise RuntimeError(f"Signup status error: {signup_response.status}")

        auth = BasicAuth(self.username, hashed_pw)
        login_response = await self.post(
            path=get_v1_path(pv1.login),
            headers={AUTHORIZATION: auth.encode()},
            data={"id": self.username, "password": hashed_pw},
        )
        if login_response.status != HTTPStatus.OK:
            raise RuntimeError(f"Login status error: {login_response.status}")

        assert login_response.data
        assert "result" in login_response.data
        login_data = login_response.data["result"]
        assert "user" in login_data
        assert "id" in login_data["user"]
        assert self.username == login_data["user"]["id"]
        assert "accessToken" in login_data
        assert "refreshToken" in login_data
        self.access_token = login_data["accessToken"]
        self.refresh_token = login_data["refreshToken"]

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

# -*- coding: utf-8 -*-

import json
import hashlib
from copy import deepcopy
from typing import Optional, Any, Union, Final
from multidict import CIMultiDictProxy, CIMultiDict
from http import HTTPStatus
from asyncio import Task, Event, AbstractEventLoop, CancelledError
from aiohttp import ClientSession
from aiohttp.web import Application
from aiohttp.typedefs import LooseHeaders
from aiohttp.hdrs import (
    METH_HEAD,
    METH_GET,
    METH_DELETE,
    METH_OPTIONS,
    METH_PATCH,
    METH_POST,
    METH_PUT,
)
from recc.auth.basic_auth import BasicAuth
from recc.auth.bearer_auth import BearerAuth
from recc.http.v1 import path_v1 as pv1
from recc.http.v1.common import get_v1_path
from recc.http.http_interface import EmptyHttpAppCallback
from recc.http.http_vars import DEFAULT_SCHEME
from recc.argparse.default_parser import parse_arguments_to_core_config
from recc.http.http_app import HttpApp
from recc.core.context import Context

DEFAULT_ADMIN_USERNAME: Final[str] = "admin"
DEFAULT_ADMIN_PASSWORD: Final[str] = "0000"


class RequestData:
    def __init__(
        self,
        method: str,
        path: str,
        *,
        headers: Optional[LooseHeaders] = None,
        data: Optional[Any] = None,
        timeout: Optional[float] = None,
    ):
        self.method = method
        self.path = path
        self.headers = headers
        self.data = data
        self.timeout = timeout


class ResponseData:
    def __init__(
        self,
        *,
        status: Optional[int] = None,
        data: Optional[Any] = None,
        headers: Optional[CIMultiDictProxy] = None,
        exception: Optional[BaseException] = None,
    ):
        self.status = status
        self.data = data
        self.headers = headers
        self.exception = exception


class HttpAppTester(EmptyHttpAppCallback):

    _app: HttpApp
    _task: Task

    def __init__(
        self,
        loop: Optional[AbstractEventLoop] = None,
    ):
        self._config = parse_arguments_to_core_config()
        self._config.developer = True
        self._config.teardown = True
        self._config.database_name = "http_app_tester"
        self._context = Context(self._config, loop=loop)
        self._app = HttpApp(context=self._context, callback=self)

        self._username: Optional[str] = None
        self._password: Optional[str] = None
        self._access_token: Optional[str] = None
        self._refresh_token: Optional[str] = None
        self._startup = Event()

        self._scheme = DEFAULT_SCHEME
        self._bind = self._config.http_bind
        self._port = self._config.http_port
        self._timeout = self._config.http_timeout

    async def on_startup(self, app: Application):
        self._startup.set()

    async def on_shutdown(self, app: Application):
        self._startup.clear()

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

    @staticmethod
    def get_method_caller(method: str, session: ClientSession):
        if method == METH_HEAD:
            return session.head
        elif method == METH_GET:
            return session.get
        elif method == METH_DELETE:
            return session.delete
        elif method == METH_OPTIONS:
            return session.options
        elif method == METH_PATCH:
            return session.patch
        elif method == METH_POST:
            return session.post
        elif method == METH_PUT:
            return session.put
        else:
            raise NotImplementedError

    async def request(
        self,
        method: str,
        path: str,
        headers: Optional[LooseHeaders] = None,
        data: Optional[Any] = None,
    ) -> ResponseData:

        url = f"{self._scheme}://{self._bind}:{self._port}{path}"
        updated_headers = deepcopy(headers) if headers else CIMultiDict()

        if self._access_token is not None:
            keys = headers.keys() if headers else []
            if "authorization" not in keys:
                token = BearerAuth(self._access_token).encode()
                if isinstance(updated_headers, CIMultiDict):
                    updated_headers.add("authorization", token)
                else:
                    updated_headers = CIMultiDict(authorization=token)

        await self._startup.wait()

        async with ClientSession(timeout=self._timeout) as session:
            method_caller = self.get_method_caller(method, session)
            async with method_caller(
                url=url, data=data, headers=updated_headers, timeout=self._timeout
            ) as response:
                response_data: Optional[Union[object, str]] = None
                if response.content_length > 0:
                    if response.content_type == "application/json":
                        response_data = await response.json()
                    else:
                        response_data = await response.text()

                return ResponseData(
                    status=response.status,
                    data=response_data,
                    headers=response.headers,
                )

    async def get_request(
        self,
        path: str,
        headers: Optional[LooseHeaders] = None,
        data: Optional[Any] = None,
    ) -> ResponseData:
        return await self.request(METH_GET, path, headers, data)

    async def post_request(
        self,
        path: str,
        headers: Optional[LooseHeaders] = None,
        data: Optional[Any] = None,
    ) -> ResponseData:
        return await self.request(METH_POST, path, headers, data)

    async def put_request(
        self,
        path: str,
        headers: Optional[LooseHeaders] = None,
        data: Optional[Any] = None,
    ) -> ResponseData:
        return await self.request(METH_PUT, path, headers, data)

    async def delete_request(
        self,
        path: str,
        headers: Optional[LooseHeaders] = None,
        data: Optional[Any] = None,
    ) -> ResponseData:
        return await self.request(METH_DELETE, path, headers, data)

    async def run_v1_admin_login(
        self,
        username=DEFAULT_ADMIN_USERNAME,
        password=DEFAULT_ADMIN_PASSWORD,
    ) -> None:
        if not username:
            raise ValueError("A `username` argument is required.")
        if not password:
            raise ValueError("A `password` argument is required.")

        self._username = username
        self._password = password
        assert self._username
        assert self._password

        hashed_pw = hashlib.sha256(self._password.encode(encoding="utf-8")).hexdigest()
        signup_response = await self.post_request(
            path=get_v1_path(pv1.signup_admin),
            data=json.dumps({"id": self._username, "password": hashed_pw}),
        )
        if signup_response.status != HTTPStatus.OK:
            raise RuntimeError(f"Signup status error: {signup_response.status}")

        auth = BasicAuth(self._username, hashed_pw)
        login_response = await self.post_request(
            path=get_v1_path(pv1.login),
            headers={
                "authorization": auth.encode(),
            },
            data=json.dumps({"id": self._username, "password": hashed_pw}),
        )
        if login_response.status != HTTPStatus.OK:
            raise RuntimeError(f"Login status error: {login_response.status}")

        assert login_response.data
        assert "result" in login_response.data
        login_data = login_response.data["result"]
        assert "user" in login_data
        assert "id" in login_data["user"]
        assert self._username == login_data["user"]["id"]
        assert "accessToken" in login_data
        assert "refreshToken" in login_data
        self._access_token = login_data["accessToken"]
        self._refresh_token = login_data["refreshToken"]

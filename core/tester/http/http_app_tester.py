# -*- coding: utf-8 -*-

from hashlib import sha256
from typing import Optional, Any, Final, Dict, TypeVar, Type
from multidict import CIMultiDictProxy, CIMultiDict
from http import HTTPStatus
from asyncio import Task, Event, AbstractEventLoop, CancelledError
from aiohttp import ClientSession
from aiohttp.hdrs import AUTHORIZATION, CONTENT_TYPE
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
from recc.http.header.basic_auth import BasicAuth
from recc.http.header.bearer_auth import BearerAuth
from recc.argparse.default_parser import parse_arguments_to_core_config
from recc.http.v1 import path_v1 as pv1
from recc.http.v1.common import get_v1_path
from recc.http.http_payload import payload_to_class
from recc.http.http_interface import EmptyHttpAppCallback
from recc.http.http_app import HttpApp
from recc.http.http_utils import v2_public_path
from recc.http import http_urls as u
from recc.serialization.serialize import serialize_default
from recc.serialization.deserialize import deserialize_default
from recc.packet.user import SigninA, SignupQ
from recc.core.context import Context
from recc.driver.json import global_json_encoder
from recc.mime.mime_type import APPLICATION_JSON, MIME_APPLICATION_JSON_UTF8
from recc.variables.http import (
    DEFAULT_HTTP_TEST_PORT,
    DEFAULT_SCHEME,
    URL_PATH_SEPARATOR,
)

_T = TypeVar("_T")

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
        self._config.database_name = "recc.test.http"
        self._config.http_port = DEFAULT_HTTP_TEST_PORT
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

    @property
    def context(self) -> Context:
        return self._context

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
        headers: Optional[Dict[str, str]] = None,
        text: Optional[str] = None,
        data: Optional[Any] = None,
        cls: Optional[Type[_T]] = None,
    ) -> ResponseData:
        prefix = f"{self._scheme}://{self._bind}:{self._port}"
        if path:
            if path[0] == URL_PATH_SEPARATOR:
                url = prefix + path
            else:
                url = prefix + URL_PATH_SEPARATOR + path
        else:
            url = prefix

        updated_headers = CIMultiDict[str]()
        if headers:
            for key, value in headers.items():
                updated_headers.add(key, value)

        if self._access_token and AUTHORIZATION not in updated_headers:
            token = BearerAuth(self._access_token).encode()
            updated_headers.add(AUTHORIZATION, token)

        request_body: str
        if text and data:
            raise ValueError("You must pass only one `text` or `data`")
        elif text:
            request_body = text
        elif data:
            request_body = global_json_encoder(serialize_default(data))
            if CONTENT_TYPE not in updated_headers:
                updated_headers.add(CONTENT_TYPE, str(MIME_APPLICATION_JSON_UTF8))
        else:
            request_body = ""

        await self._startup.wait()

        async with ClientSession(timeout=self._timeout) as session:
            method_caller = self.get_method_caller(method, session)
            async with method_caller(
                url=url,
                data=request_body,
                headers=updated_headers,
                timeout=self._timeout,
            ) as response:
                response_data: Any = None
                if cls is not None:
                    response_data = payload_to_class(
                        response.headers, await response.text(), cls
                    )
                elif response.content_length > 0:
                    if response.content_type == APPLICATION_JSON:
                        response_data = await response.json()
                    else:
                        response_data = await response.text()

                return ResponseData(
                    status=response.status,
                    data=response_data,
                    headers=response.headers,
                )

    async def get(
        self,
        path: str,
        headers: Optional[Dict[str, str]] = None,
        text: Optional[str] = None,
        data: Optional[Any] = None,
        cls: Optional[Type[_T]] = None,
    ) -> ResponseData:
        return await self.request(METH_GET, path, headers, text, data, cls)

    async def post(
        self,
        path: str,
        headers: Optional[Dict[str, str]] = None,
        text: Optional[str] = None,
        data: Optional[Any] = None,
        cls: Optional[Type[_T]] = None,
    ) -> ResponseData:
        return await self.request(METH_POST, path, headers, text, data, cls)

    async def patch(
        self,
        path: str,
        headers: Optional[Dict[str, str]] = None,
        text: Optional[str] = None,
        data: Optional[Any] = None,
        cls: Optional[Type[_T]] = None,
    ) -> ResponseData:
        return await self.request(METH_PATCH, path, headers, text, data, cls)

    async def put(
        self,
        path: str,
        headers: Optional[Dict[str, str]] = None,
        text: Optional[str] = None,
        data: Optional[Any] = None,
        cls: Optional[Type[_T]] = None,
    ) -> ResponseData:
        return await self.request(METH_PUT, path, headers, text, data, cls)

    async def delete(
        self,
        path: str,
        headers: Optional[Dict[str, str]] = None,
        text: Optional[str] = None,
        data: Optional[Any] = None,
        cls: Optional[Type[_T]] = None,
    ) -> ResponseData:
        return await self.request(METH_DELETE, path, headers, text, data, cls)

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

        hashed_pw = sha256(self._password.encode(encoding="utf-8")).hexdigest()
        signup_response = await self.post(
            path=get_v1_path(pv1.signup_admin),
            data={"id": self._username, "password": hashed_pw},
        )
        if signup_response.status != HTTPStatus.OK:
            raise RuntimeError(f"Signup status error: {signup_response.status}")

        auth = BasicAuth(self._username, hashed_pw)
        login_response = await self.post(
            path=get_v1_path(pv1.login),
            headers={AUTHORIZATION: auth.encode()},
            data={"id": self._username, "password": hashed_pw},
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

    async def run_v2_admin_signin(
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

        hashed_pw = SignupQ.encrypt_password(self._password)
        signup = SignupQ(self._username, hashed_pw)
        signup_response = await self.post(v2_public_path(u.signup_admin), data=signup)

        if signup_response.status == HTTPStatus.SERVICE_UNAVAILABLE:
            pass
        elif signup_response.status != HTTPStatus.OK:
            raise RuntimeError(f"Signup status error: {signup_response.status}")

        auth = BasicAuth(self._username, hashed_pw)
        signin_headers = {str(AUTHORIZATION): auth.encode()}
        signin_response = await self.post(v2_public_path(u.signin), signin_headers)
        if signin_response.status != HTTPStatus.OK:
            raise RuntimeError(f"Login status error: {signin_response.status}")

        signin = deserialize_default(signin_response.data, SigninA)
        assert signin.user is not None
        assert isinstance(signin, SigninA)
        assert self._username == signin.user.username
        self._access_token = signin.access
        self._refresh_token = signin.refresh

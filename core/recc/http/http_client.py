# -*- coding: utf-8 -*-

import requests
from http import HTTPStatus
from time import time
from typing import Optional, Tuple, TypeVar, Any, Dict, Type
from aiohttp import ClientSession
from aiohttp.hdrs import (
    METH_HEAD,
    METH_GET,
    METH_DELETE,
    METH_OPTIONS,
    METH_PATCH,
    METH_POST,
    METH_PUT,
    AUTHORIZATION,
    CONTENT_TYPE,
)
from multidict import CIMultiDictProxy, CIMultiDict

from recc.driver.json import global_json_encoder
from recc.mime.mime_type import MIME_APPLICATION_JSON_UTF8, APPLICATION_JSON
from recc.packet.user import SigninA, SignupQ
from recc.serialization.serialize import serialize_default
from recc.http.header.basic_auth import BasicAuth
from recc.http.header.bearer_auth import BearerAuth
from recc.http.http_payload import payload_to_class
from recc.http.http_utils import v2_public_path
from recc.http import http_urls as u
from recc.variables.http import (
    DEFAULT_SCHEME,
    DEFAULT_REQUEST_TIMEOUT_SECONDS,
    URL_PATH_SEPARATOR,
)


def normalize_url_path(path: str) -> str:
    if not path:
        return u.root
    if path[0] != u.root:
        return u.root + path
    return path


def request(
    host: str,
    port: int,
    path=u.root,
    scheme=DEFAULT_SCHEME,
    timeout=DEFAULT_REQUEST_TIMEOUT_SECONDS,
) -> Tuple[int, Optional[str]]:
    response = requests.get(
        f"{scheme}://{host}:{port}{normalize_url_path(path)}", timeout=timeout
    )
    code = response.status_code
    return code, response.text if code == 200 else str()


def request_heartbeat(
    host: str,
    port: int,
    scheme=DEFAULT_SCHEME,
    timeout=DEFAULT_REQUEST_TIMEOUT_SECONDS,
) -> Tuple[int, Optional[str]]:
    return request(
        host=host, port=port, path=u.api_heartbeat, scheme=scheme, timeout=timeout
    )


def wait_heartbeat(
    host: str,
    port: int,
    scheme=DEFAULT_SCHEME,
    timeout=DEFAULT_REQUEST_TIMEOUT_SECONDS,
) -> None:  # nocov
    begin = time()
    last_code = 0
    last_exception = None
    while time() - begin <= timeout:
        try:
            last_code, _ = request_heartbeat(
                host=host, port=port, scheme=scheme, timeout=timeout
            )
            if last_code == 200:
                return
        except Exception as e:  # noqa, nocov
            last_exception = e
    if last_exception:
        raise last_exception
    else:
        raise TimeoutError(
            f"Heartbeat timeout. (url={scheme}://{host}:{port},timeout={timeout}s,code={last_code})"  # noqa
        )


def request_version(
    host: str,
    port: int,
    scheme=DEFAULT_SCHEME,
    timeout=DEFAULT_REQUEST_TIMEOUT_SECONDS,
) -> Tuple[int, Optional[str]]:
    return request(
        host=host,
        port=port,
        path=u.api_version,
        scheme=scheme,
        timeout=timeout,
    )


_T = TypeVar("_T")


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


class HttpClient:
    def __init__(self, scheme: str, address: str, timeout: float):
        self.scheme = scheme
        self.address = address
        self.timeout = timeout

        self.username: Optional[str] = None
        self.password: Optional[str] = None
        self.access_token: Optional[str] = None
        self.refresh_token: Optional[str] = None

    @property
    def origin(self) -> str:
        if self.address[-1] == URL_PATH_SEPARATOR:
            return f"{self.scheme}://{self.address[0:-1]}"
        else:
            return f"{self.scheme}://{self.address}"

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
        if path:
            if path[0] == URL_PATH_SEPARATOR:
                url = self.origin + path
            else:
                url = self.origin + URL_PATH_SEPARATOR + path
        else:
            url = self.origin

        updated_headers = CIMultiDict[str]()
        if headers:
            for key, value in headers.items():
                updated_headers.add(key, value)

        if self.access_token and AUTHORIZATION not in updated_headers:
            token = BearerAuth(self.access_token).encode()
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

        await self.on_request_begin()

        try:
            async with ClientSession(timeout=self.timeout) as session:
                method_caller = self.get_method_caller(method, session)
                async with method_caller(
                    url=url,
                    data=request_body,
                    headers=updated_headers,
                    timeout=self.timeout,
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
        finally:
            await self.on_request_end()

    async def on_request_begin(self):
        pass

    async def on_request_end(self):
        pass

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

    async def signup_public(self, username: str, password: str) -> None:
        if not username:
            raise ValueError("A `username` argument is required.")
        if not password:
            raise ValueError("A `password` argument is required.")
        signup = SignupQ(username, SignupQ.encrypt_password(password))
        response = await self.post(v2_public_path(u.signup), data=signup)
        if response.status != HTTPStatus.OK:
            raise RuntimeError(f"Signup status error: {response.status}")

    async def signup_admin(self, username: str, password: str) -> None:
        signup = SignupQ(username, SignupQ.encrypt_password(password))
        response = await self.post(v2_public_path(u.signup_admin), data=signup)
        if response.status == HTTPStatus.SERVICE_UNAVAILABLE:
            pass
        elif response.status != HTTPStatus.OK:
            raise RuntimeError(f"Signup status error: {response.status}")

    async def signin(self, username: str, password: str, save_session=False) -> SigninA:
        auth = BasicAuth(username, SignupQ.encrypt_password(password))
        headers = {str(AUTHORIZATION): auth.encode()}
        response = await self.post(
            v2_public_path(u.signin), headers=headers, cls=SigninA
        )
        if response.status != HTTPStatus.OK:
            raise RuntimeError(f"Login status error: {response.status}")
        result = response.data
        assert result is not None
        assert result.user is not None
        assert isinstance(result, SigninA)
        if save_session:
            self.username = username
            self.password = password
            self.access_token = result.access
            self.refresh_token = result.refresh
        return result

    async def signup_and_in(
        self, username: str, password: str, save_session=True
    ) -> None:
        if not username:
            raise ValueError("A `username` argument is required.")
        if not password:
            raise ValueError("A `password` argument is required.")
        await self.signup_admin(username, password)
        await self.signin(username, password, save_session=save_session)

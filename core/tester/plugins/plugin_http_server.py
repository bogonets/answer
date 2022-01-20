# -*- coding: utf-8 -*-

from typing import Optional, Any
from asyncio import Task, Event, create_task
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR, SO_REUSEPORT
from functools import partial
from logging import getLogger
from aiohttp.web import Application
from aiohttp.web import _run_app  # noqa
from aiohttp import web
from aiohttp.web_request import Request
from aiohttp.web_response import Response
from recc.http.http_decorator import has_layout_view

DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORT = 39999

logger = getLogger("recc.plugin.http_server")


class Server:

    task: Optional[Task] = None

    def __init__(self, context: Any, **kwargs):
        self.context = context
        self.host = str(kwargs.get("host", DEFAULT_HOST))
        self.port = int(kwargs.get("port", DEFAULT_PORT))
        self.app = Application()
        self.app.add_routes([web.get("/tester", self.on_get_tester)])
        self.app.on_startup.append(self.on_startup)
        self.ready = Event()
        self.body = ""

        self.sock = socket(family=AF_INET, type=SOCK_STREAM)
        self.sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.sock.setsockopt(SOL_SOCKET, SO_REUSEPORT, 1)
        self.sock.bind((self.host, self.port))

    async def on_startup(self, app):
        assert app is not None
        self.ready.set()

    async def on_get_tester(self, request: Request) -> Response:
        self.body = await request.text()
        return Response()

    async def _runner(self) -> None:
        await _run_app(self.app, sock=self.sock)

    async def on_open(self) -> None:
        logger.debug("on_open")
        self.task = create_task(self._runner())
        await self.ready.wait()

    async def on_close(self) -> None:
        logger.debug("on_close")
        assert self.task is not None
        try:
            self.task.cancel()
            await self.task
        except:  # noqa
            pass
        finally:
            assert self.sock is not None
            self.sock.close()

    def get_body(self) -> str:
        return self.body

    def post_server_data(self, data) -> str:
        assert self
        return data


server: Optional[Server] = None


def on_create(context: Any, **kwargs) -> None:
    global server
    server = Server(context, **kwargs)


def on_destroy() -> None:
    global server
    del server


async def on_open() -> None:
    assert server is not None
    await server.on_open()


async def on_close() -> None:
    assert server is not None
    await server.on_close()


async def on_get() -> str:
    assert server is not None
    return server.get_body()


async def on_post(data: str) -> str:
    assert server is not None
    return data


async def on_get_pattern() -> str:
    return "pattern"


@has_layout_view
async def on_get_layout_view() -> str:
    return "aaa"


def on_routes():
    return [
        ("GET", "/", on_get),
        ("POST", "/", on_post),
        ("GET", "/unknown/{pattern}/test", on_get_pattern),
        ("GET", "/layout/view/{data}", on_get_layout_view),
        ("POST", "/server/data", partial(Server.post_server_data, server)),
    ]

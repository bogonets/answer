# -*- coding: utf-8 -*-

from typing import Optional, Any, Dict
from asyncio import Task, Event, create_task
from aiohttp.web import Application
from aiohttp.web import _run_app  # noqa
from aiohttp import web
from aiohttp.web_request import Request
from aiohttp.web_response import Response
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR, SO_REUSEPORT


class Server:

    task: Optional[Task] = None

    def __init__(self, context: Any, **kwargs):
        self.context = context
        self.host = str(kwargs["host"])
        self.port = int(kwargs["port"])
        self.app = Application()
        self.app.add_routes([
            web.get("/tester", self.on_get_tester)
        ])
        self.app.on_startup.append(self.on_startup)
        self.ready = Event()
        self.body = ""

        self.sock = socket(family=AF_INET, type=SOCK_STREAM)
        self.sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.sock.setsockopt(SOL_SOCKET, SO_REUSEPORT, 1)
        self.sock.bind((self.host, self.port))

    async def on_startup(self, app):
        self.ready.set()

    async def on_get_tester(self, request: Request) -> Response:
        self.body = await request.text()
        return Response()

    async def _runner(self) -> None:
        await _run_app(self.app, sock=self.sock)

    async def on_open(self) -> None:
        self.task = create_task(self._runner())
        await self.ready.wait()

    async def on_close(self) -> None:
        assert self.task is not None
        try:
            self.task.cancel()
            await self.task
        except:  # noqa
            pass
        finally:
            assert self.sock is not None
            self.sock.close()

    async def on_request(self, request) -> Response:
        assert self.task is not None
        return Response(text=self.body)


server: Optional[Server] = None


def on_create(context: Any, **kwargs) -> Dict[str, Any]:
    global server
    server = Server(context, **kwargs)
    return {"name": "http_server"}


def on_destroy() -> None:
    global server
    del server


async def on_open() -> None:
    assert server is not None
    await server.on_open()


async def on_close() -> None:
    assert server is not None
    await server.on_close()


async def on_request(request: Request) -> Response:
    assert server is not None
    return await server.on_request(request)

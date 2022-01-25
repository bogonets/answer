# -*- coding: utf-8 -*-

from asyncio import Task, CancelledError
from socket import socket
from typing import Optional, List

from aiohttp import web
from aiohttp.log import access_logger
from aiohttp.web import GracefulExit
from aiohttp.web import _run_app  # noqa
from aiohttp.web_log import AccessLogger
from aiohttp.web_request import Request
from aiohttp.web_response import Response
from aiohttp.web_routedef import AbstractRouteDef

from recc.core.context import Context
from recc.aio.task import all_tasks, cancel_tasks
from recc.network.socket import bind_socket
from recc.http.http_interface import HttpAppCallback, EmptyHttpAppCallback
from recc.http.http_cors import create_cors
from recc.http.v1.router_v1 import RouterV1
from recc.http.v2.router_v2 import RouterV2
from recc.http.http_www import HttpWWW
from recc.http import http_urls as u
from recc.logging.logging import recc_http_logger as logger
from recc.util.version import version_text
from recc.util.python_version import PY_36
from recc.variables.http import DEFAULT_CLIENT_MAX_SIZE


class HttpApp:
    """
    HTTP application.
    """

    _sock: Optional[socket] = None
    """
    You should be able to connect the client socket in the callback.
    Therefore, the socket must be bound before ``loop.create_server()``.
    """

    _task: Optional[Task] = None
    """
    HTTP Application task.
    """

    _app: web.Application
    _context: Context
    _callback: HttpAppCallback

    def __init__(
        self,
        context: Optional[Context] = None,
        callback: Optional[HttpAppCallback] = None,
    ):
        self._context = context if context else Context()
        self._callback = callback if callback else EmptyHttpAppCallback()

        self._routes = list()
        self._routes += self._get_common_routes()
        self._routes += self._get_common_api_routes()

        self._app = web.Application(
            middlewares=[self._global_middleware],
            client_max_size=DEFAULT_CLIENT_MAX_SIZE,
        )

        self._app._set_loop(self._context.loop)  # noqa
        self._app.router.add_routes(self._routes)
        self._app.on_startup.append(self.on_startup)
        self._app.on_shutdown.append(self.on_shutdown)
        self._app.on_cleanup.append(self.on_cleanup)

        self._router_v1 = RouterV1(self._context)
        self._app.add_subapp(u.api_v1, self._router_v1.app)

        self._router_v2 = RouterV2(self._context)
        self._app.add_subapp(u.api_v2, self._router_v2.app)

        self._www = HttpWWW(self._context)
        self._app.add_subapp(u.app, self._www.app)

        self._cors = create_cors(self._app)

    @property
    def context(self):
        return self._context

    @property
    def callback(self):
        return self._callback

    @property
    def app(self):
        return self._app

    @web.middleware
    async def _global_middleware(self, request: Request, handler) -> Response:
        return await handler(request)

    def _get_common_routes(self) -> List[AbstractRouteDef]:
        return [
            web.get(u.root, self.on_get_root),
            web.get(u.index, self.on_get_index),
            web.get(u.favicon, self.on_get_favicon),
        ]

    def _get_common_api_routes(self) -> List[AbstractRouteDef]:
        return [
            web.get(u.api_heartbeat, self.on_heartbeat),
            web.get(u.api_version, self.on_version),
        ]

    def _print(self, *args, **kwargs) -> None:
        if not self._context.config.suppress_print:
            print(*args, **kwargs)

    def _graceful_exit(self):
        raise GracefulExit()

    async def on_get_root(self, request: Request) -> Response:
        raise web.HTTPFound(u.app_root)

    async def on_get_index(self, request: Request) -> Response:
        raise web.HTTPFound(u.app_root)

    async def on_get_favicon(self, request: Request) -> Response:
        raise web.HTTPFound(u.app_favicon)

    async def on_heartbeat(self, _: Request) -> Response:
        assert self._context
        logger.info("http_app.on_heartbeat()")
        return Response()

    async def on_version(self, _: Request) -> Response:
        assert self._context
        logger.info(f"http_app.on_version() -> {version_text}")
        return Response(text=version_text)

    async def call_soon_graceful_exit(self):
        assert self._task
        self._task.get_loop().call_soon_threadsafe(self._graceful_exit)

    async def on_startup(self, app: web.Application):
        logger.info("http_app startup begin ...")
        await self._context.open()
        await self._callback.on_startup(app)
        logger.info("http_app startup done.")

    async def on_shutdown(self, app: web.Application):
        logger.info("http_app shutdown begin ...")
        await self._callback.on_shutdown(app)
        await self._context.close()
        logger.info("http_app shutdown done.")

    async def on_cleanup(self, app: web.Application):
        await self._callback.on_cleanup(app)

    def bind_socket(self) -> bool:
        bind = self._context.config.http_bind
        port = self._context.config.http_port
        dev_mode = self._context.config.developer
        self._sock = bind_socket(bind, port, dev_mode, dev_mode)
        return self._sock is not None

    def exists_socket(self) -> bool:
        return self._sock is not None

    def close_socket(self) -> None:
        if self._sock is not None:
            self._sock.close()
        self._sock = None

    def task_cancel(self) -> None:
        assert self._task
        self._task.cancel()

    async def wait_for_termination(self) -> None:
        assert self._task
        await self._task

    async def _runner(self) -> None:
        await _run_app(
            self._app,
            host=None,
            port=None,
            path=None,
            sock=self._sock,
            shutdown_timeout=60.0,
            ssl_context=None,
            print=self._print,
            backlog=128,
            access_log_class=AccessLogger,
            access_log_format=AccessLogger.LOG_FORMAT,
            access_log=access_logger,
            handle_signals=True,
            reuse_address=None,
            reuse_port=None,
        )

    async def start(self) -> None:
        if not self.exists_socket():
            logger.info("http_app.start() binding socket ...")
            if not self.bind_socket():
                logger.error("http_app.start() socket binding error !!")
                return

        self._task = self._context.loop.create_task(self._runner())
        logger.info(f"http_app.start() created task: {self._task.get_name()}")

    async def run(self) -> None:
        try:
            logger.info("http_app.run() start")
            await self.start()

            logger.info("http_app.run() await task ...")
            await self.wait_for_termination()
            logger.info("http_app.run() await task ...")

        except GracefulExit:
            logger.info("http_app.run() graceful exit !!")
        except KeyboardInterrupt:
            logger.info("http_app.run() keyboard interrupt !!")
        except CancelledError:
            logger.info("http_app.run() asyncio cancelled !!")
        except BaseException as e:
            logger.exception(e)
            raise
        finally:
            self.close_socket()
            logger.info("http_app.run() end")

    def run_until_complete(self, *, finally_clear=False) -> None:
        """
        Start web application.
        """

        loop = self._context.loop
        try:
            self._context.loop.run_until_complete(self.run())
        except GracefulExit:
            logger.info("http_app.run_until_complete() graceful exit !!")
        except KeyboardInterrupt:
            logger.info("http_app.run_until_complete() keyboard interrupt !!")
        finally:
            cancel_tasks(loop, self._task)
            cancel_tasks(loop, *all_tasks(loop))
            if PY_36:  # don't use python3.6 to pass mypy
                loop.run_until_complete(loop.shutdown_asyncgens())
            if finally_clear:
                loop.close()

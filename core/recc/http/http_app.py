# -*- coding: utf-8 -*-

import asyncio
import os
import sys
from asyncio import AbstractEventLoop, Task, CancelledError
from http import HTTPStatus
from ipaddress import ip_address, IPv4Address
from socket import (
    socket,
    AF_INET,
    AF_INET6,
    SOCK_STREAM,
    SOL_SOCKET,
    SO_REUSEADDR,
    SO_REUSEPORT,
)
from typing import Optional, List

import aiohttp_cors
from aiohttp import web
from aiohttp.log import access_logger
from aiohttp.web import HTTPException
from aiohttp.web import GracefulExit
from aiohttp.web import _run_app  # noqa
from aiohttp.web_log import AccessLogger
from aiohttp.web_request import Request
from aiohttp.web_response import Response
from aiohttp.web_routedef import AbstractRouteDef

from recc.argparse.config.core_config import ARG_HTTP_ROOT
from recc.core.context import Context
from recc.http.http_interface import HttpAppCallback, EmptyHttpAppCallback
from recc.http.http_vars import (
    URL_ROOT,
    URL_APP,
    URL_API_VERSION,
    URL_API_HEARTBEAT,
    URL_INDEX,
    URL_APP_INDEX,
    URL_FAVICON,
    URL_APP_FAVICON,
)
from recc.http.v1.router_v1 import RouterV1
from recc.file.permission import is_readable_dir, is_writable_dir
from recc.exception.recc_error import ReccBaseException
from recc.exception.http_status import HttpStatus
from recc.log.logging import recc_http_logger as logger
from recc.util.version import version_text

PY_36 = sys.version_info >= (3, 6)
PY_37 = sys.version_info >= (3, 7)
PY_38 = sys.version_info >= (3, 8)
DEFAULT_HTTP_ROOT = ARG_HTTP_ROOT.inference_default_value()


def _get_ip_family(ip: str) -> int:
    return AF_INET if type(ip_address(ip)) is IPv4Address else AF_INET6


def _create_cors(app: web.Application) -> aiohttp_cors.CorsConfig:
    cors = aiohttp_cors.setup(
        app,
        defaults={
            "*": aiohttp_cors.ResourceOptions(
                allow_credentials=True,
                expose_headers="*",
                allow_headers="*",
                max_age=None,
                allow_methods=None,
            )
        },
    )
    routes = list(app.router.routes())
    for route in routes:
        cors.add(route)
    return cors


def _all_tasks(loop: AbstractEventLoop):
    if PY_37:
        return getattr(asyncio, "all_tasks")(loop)
    else:
        return {t for t in list(asyncio.Task.all_tasks(loop)) if not t.done()}


def _cancel_tasks(to_cancel, loop: AbstractEventLoop) -> None:
    if not to_cancel:
        return

    for task in to_cancel:
        task.cancel()

    loop.run_until_complete(
        asyncio.gather(*to_cancel, loop=loop, return_exceptions=True)
    )

    for task in to_cancel:
        if task.cancelled():
            continue
        if task.exception() is not None:
            loop.call_exception_handler(
                {
                    "message": "unhandled exception during asyncio.run() shutdown",
                    "exception": task.exception(),
                    "task": task,
                }
            )


class HttpApp:
    """
    c2core main application class.
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
        super().__init__()
        self._context = context if context else Context()
        self._callback = callback if callback else EmptyHttpAppCallback()

        self._routes = list()
        self._routes += self._get_http_root_routes()
        self._routes += self._get_common_routes()
        self._routes += self._get_common_api_routes()

        self._app = web.Application(middlewares=[self._global_middleware])
        self._app._set_loop(self._context.loop)  # noqa
        self._app.router.add_routes(self._routes)

        self._router_v1 = RouterV1(self._context)
        self._router_v1.add_parent_app(self._app)
        self._cors = _create_cors(self._app)

        self._app.on_startup.append(self.on_startup)
        self._app.on_shutdown.append(self.on_shutdown)
        self._app.on_cleanup.append(self.on_cleanup)

    def _error_response(
        self, e: BaseException, status: int, code: Optional[int] = None
    ) -> Response:
        dev_mode = self._context.config.developer
        msg = repr(e) if dev_mode else str(e)
        return web.json_response(
            {"code": code if code is not None else status, "msg": msg},
            status=status,
        )

    @web.middleware
    async def _global_middleware(self, request: Request, handler) -> Response:
        # Returns value is 'application/octet-stream' if no Content-Type
        # header present in HTTP headers according to RFC 2616
        try:
            return await handler(request)
        except HTTPException:
            raise
        except HttpStatus as e:
            assert e.is_http_status()
            return self._error_response(e, e.code)
        except ReccBaseException as e:
            logger.exception(e)
            return self._error_response(e, HTTPStatus.INTERNAL_SERVER_ERROR, e.code)
        except NotImplementedError as e:
            logger.exception(e)
            return self._error_response(e, HTTPStatus.NOT_IMPLEMENTED)
        except BaseException as e:
            logger.exception(e)
            return self._error_response(e, HTTPStatus.INTERNAL_SERVER_ERROR)

    def _get_http_root_routes(self) -> List[AbstractRouteDef]:
        http_root = self._context.config.http_root
        if not os.path.isdir(http_root):
            logger.error(f"Not found http root directory: {http_root}")
            return []

        if not is_readable_dir(http_root):
            logger.error(f"Not readable http root directory: {http_root}")
            return []

        if is_writable_dir(http_root):
            logger.warning(
                f"Writable http root directory (There may be a security issue): {http_root}"  # noqa
            )

        return [web.static(URL_APP, http_root if http_root else DEFAULT_HTTP_ROOT)]

    def _get_common_routes(self) -> List[AbstractRouteDef]:
        return [
            web.get(URL_ROOT, self.on_get_root),
            web.get(URL_INDEX, self.on_get_index),
            web.get(URL_FAVICON, self.on_get_favicon),
        ]

    def _get_common_api_routes(self) -> List[AbstractRouteDef]:
        return [
            web.get(URL_API_HEARTBEAT, self.on_heartbeat),
            web.get(URL_API_VERSION, self.on_version),
        ]

    def _print(self, *args, **kwargs) -> None:
        if not self._context.config.suppress_print:
            print(*args, **kwargs)

    def _graceful_exit(self):
        raise GracefulExit()

    async def on_get_root(self, request: Request) -> Response:
        raise web.HTTPFound(URL_APP_INDEX)

    async def on_get_index(self, request: Request) -> Response:
        raise web.HTTPFound(URL_APP_INDEX)

    async def on_get_favicon(self, request: Request) -> Response:
        raise web.HTTPFound(URL_APP_FAVICON)

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
        self._task.get_loop().call_soon(self._graceful_exit)

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

        family: int
        try:
            family = _get_ip_family(bind)
        except ValueError:
            logger.error("The bind argument must be ipv4 or ipv6.")
            return False

        assert family == AF_INET or family == AF_INET6

        try:
            logger.info(f"Socket(bind={bind},port={port}) binding ...")
            self._sock = socket(family=family, type=SOCK_STREAM)
            if dev_mode:
                # This is how to clear the `TIME_WAIT` time
                # when restarting the program to speed up debugging.
                self._sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
                self._sock.setsockopt(SOL_SOCKET, SO_REUSEPORT, 1)
            self._sock.bind((bind, port))
            logger.info("Socket binding success.")
            return True
        except OSError as e:
            logger.error(f"Socket binding failed: {e}")
            if self._sock is not None:
                self._sock.close()
            self._sock = None
            return False

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
            _cancel_tasks({self._task}, loop)
            _cancel_tasks(_all_tasks(loop), loop)
            if sys.version_info >= (3, 6):  # don't use PY_36 to pass mypy
                loop.run_until_complete(loop.shutdown_asyncgens())
            if finally_clear:
                loop.close()

# -*- coding: utf-8 -*-

from typing import List
from aiohttp import web
from recc.core.context import Context
from aiohttp.web_request import Request
from aiohttp.web_routedef import AbstractRouteDef
from recc.logging.logging import recc_http_logger as logger
from recc.http.v1.common import (
    PATH_PREFIX_EXTRA_POSOD,
    no_name,
    at_session,
    response_ok,
)


class PosodV1:
    """
    API version 1.0 - Extra - Posod Router class.
    """

    def __init__(self, context: Context):
        self._context = context
        self._app = web.Application()
        self._app.add_routes(self._get_routers())

    def _get_routers(self) -> List[AbstractRouteDef]:
        # fmt: off
        return [
            web.get("/test", self.on_posod_test),
        ]
        # fmt: on

    @property
    def app(self) -> web.Application:
        return self._app

    def add_parent_app(self, parent_app: web.Application) -> None:
        assert self._app is not None
        assert parent_app is not None
        parent_app.add_subapp(PATH_PREFIX_EXTRA_POSOD, self._app)

    async def on_posod_test(self, request: Request):
        session = request[at_session]
        username = session.audience
        logger.info(f"on_posod_test(session={username})")
        # json: dict = await request.json()
        assert self
        return response_ok(no_name)

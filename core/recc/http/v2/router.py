# -*- coding: utf-8 -*-

import json
from typing import List, Any
from http import HTTPStatus
from aiohttp import web
from aiohttp.web_routedef import AbstractRouteDef
from aiohttp.web_request import Request
from aiohttp.web_response import Response
from recc.auth.bearer_auth import BearerAuth
from recc.core.context import Context
from recc.session.session import Session

PATH_PREFIX_API_V2 = "/api/v2"

CONTENT_TYPE_JSON = "application/json"


def create_v2_packet(data: Any) -> dict:
    return {
        "data": data,
    }


def json_response(
    data: Any,
    *,
    status=HTTPStatus.OK,
    content_type=CONTENT_TYPE_JSON,
) -> Response:
    return Response(text=json.dumps(data), status=status, content_type=content_type)


class Router:
    """
    API version 2.0 - HTTP Router class.
    """

    def __init__(self, context: Context):
        self._context = context
        self._api_v2_app = web.Application(middlewares=[self.middleware])
        self._api_v2_app.add_routes(self._get_routes())

    @property
    def app(self) -> web.Application:
        return self._api_v2_app

    @web.middleware
    async def middleware(self, request: Request, handler):
        result = await handler(request)
        if isinstance(result, Response):
            return result
        else:
            return json_response(result)

    def _get_routes(self) -> List[AbstractRouteDef]:
        # fmt: off
        return [
            web.get("/test", self.on_test),
        ]
        # fmt: on

    async def _get_access_session(self, request: Request) -> Session:
        authorization = request.headers["authorization"]
        auth = BearerAuth.decode_from_authorization_header(authorization)
        return await self._context.get_access_session(auth.token)

    # ---------------
    # API v2 handlers
    # ---------------

    async def on_test(self, _: Request):
        assert self._context
        return json_response({})

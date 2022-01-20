# -*- coding: utf-8 -*-

from typing import List, Any
from multidict import CIMultiDict
from aiohttp import web
from aiohttp.hdrs import (
    METH_OPTIONS,
    ACCESS_CONTROL_ALLOW_CREDENTIALS,
    ACCESS_CONTROL_ALLOW_HEADERS,
    ACCESS_CONTROL_ALLOW_METHODS,
    ACCESS_CONTROL_ALLOW_ORIGIN,
)
from aiohttp.web_routedef import AbstractRouteDef
from aiohttp.web_request import Request
from aiohttp.web_response import Response
from aiohttp.web_exceptions import HTTPNotFound
from recc.core.context import Context
from recc.http.http_parameter import parameter_matcher, parameter_matcher_main
from recc.http import http_urls as u


class RouterV2Plugins:
    """
    API version 2 for plugins.
    """

    def __init__(self, context: Context):
        self._context = context
        self._app = web.Application(middlewares=[self.middleware])
        self._app.add_routes(self._routes())

    @property
    def app(self) -> web.Application:
        return self._app

    @property
    def context(self) -> Context:
        return self._context

    @web.middleware
    async def middleware(self, request: Request, handler) -> Response:
        if request.method == METH_OPTIONS:
            return await self.options_cors(request)
        return await handler(request)  # (CORS) Default `options` handling.

    async def options_cors(self, request: Request) -> Response:
        assert self is not None
        assert request is not None
        headers = CIMultiDict[str]()
        headers.add(ACCESS_CONTROL_ALLOW_CREDENTIALS, "*")
        headers.add(ACCESS_CONTROL_ALLOW_HEADERS, "*")
        headers.add(ACCESS_CONTROL_ALLOW_METHODS, "*")
        headers.add(ACCESS_CONTROL_ALLOW_ORIGIN, "*")
        return Response(headers=headers)

    # noinspection PyTypeChecker
    def _routes(self) -> List[AbstractRouteDef]:
        return [
            web.get(u.empty, self.get_root),
            web.get(u.root, self.get_root),
            web.get(u.pplugin_ptail, self.any_pplugin_ptail),
            web.patch(u.pplugin_ptail, self.any_pplugin_ptail),
            web.post(u.pplugin_ptail, self.any_pplugin_ptail),
            web.delete(u.pplugin_ptail, self.any_pplugin_ptail),
            web.put(u.pplugin_ptail, self.any_pplugin_ptail),
        ]

    # --------
    # Handlers
    # --------

    @parameter_matcher
    async def get_root(self) -> List[str]:
        return self.context.get_plugin_keys()

    @parameter_matcher
    async def any_pplugin_ptail(self, plugin: str, tail: str, request: Request) -> Any:
        module = self.context.plugins.get(plugin, None)
        if module is None:
            raise HTTPNotFound(reason=f"Not found {plugin} plugin")

        method = request.method
        if tail:
            if tail[0] == u.root:
                path = tail
            else:
                path = u.root + tail
        else:
            path = u.root

        try:
            route, match_info = module.get_route(method, path)
        except KeyError:
            msg = f"Not exists router({method},{tail}) function in {plugin} plugin"
            raise HTTPNotFound(reason=msg)

        for key, val in match_info.items():
            request.match_info[key] = val

        assert route is not None

        # [IMPORTANT]
        # Do not use `route.__self__` when `ismethod(route)` is true.
        # This is handled by the Python interpreter.
        return await parameter_matcher_main(
            func=route,
            bound_instance=None,
            request=request,
        )

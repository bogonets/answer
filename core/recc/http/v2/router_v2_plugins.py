# -*- coding: utf-8 -*-

from typing import List, Any
from aiohttp import web
from aiohttp.web_routedef import AbstractRouteDef
from aiohttp.web_request import Request
from aiohttp.web_exceptions import HTTPNotFound
from recc.core.context import Context
from recc.http.http_decorator import parameter_matcher, parameter_matcher_main
from recc.http import http_urls as u


class RouterV2Plugins:
    """
    API version 2 for plugins.
    """

    def __init__(self, context: Context):
        self._context = context
        self._app = web.Application()
        self._app.add_routes(self._routes())

    @property
    def app(self) -> web.Application:
        return self._app

    @property
    def context(self) -> Context:
        return self._context

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

    @parameter_matcher()
    async def get_root(self) -> List[str]:
        return self.context.get_plugin_keys()

    @parameter_matcher()
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
        return await parameter_matcher_main(route, None, request)

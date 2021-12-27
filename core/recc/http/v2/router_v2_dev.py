# -*- coding: utf-8 -*-

from typing import List
from aiohttp import web
from aiohttp.web_routedef import AbstractRouteDef
from aiohttp.web_request import Request
from aiohttp.web_exceptions import (
    HTTPNotFound,
    HTTPBadRequest,
)
from recc.core.context import Context
from recc.http import http_urls as u
from recc.http.http_parameter import parameter_matcher
from recc.packet.config import ConfigA, UpdateConfigValueQ
from recc.packet.environment import EnvironmentA
from recc.packet.info import InfoA, CreateInfoQ, UpdateInfoQ
from recc.packet.plugin import PluginA
from recc.packet.system import VersionsA
from recc.variables.environment import RECC_ENV_PREFIX


class RouterV2Dev:
    """
    API version 2 for developer.
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

    @web.middleware
    async def middleware(self, request: Request, handler):
        return await handler(request)

    # noinspection PyTypeChecker
    def _routes(self) -> List[AbstractRouteDef]:
        # fmt: off
        return [
            # configs
            web.get(u.configs, self.get_configs),
            web.get(u.configs_pkey, self.get_configs_pkey),
            web.patch(u.configs_pkey, self.patch_configs_pkey),

            # infos
            web.get(u.infos, self.get_infos),
            web.post(u.infos, self.post_infos),
            web.get(u.infos_pkey, self.get_infos_pkey),
            web.patch(u.infos_pkey, self.patch_infos_pkey),
            web.delete(u.infos_pkey, self.delete_infos_pkey),

            # system
            web.get(u.system_versions, self.get_versions),

            # plugins
            web.get(u.plugins, self.get_plugins),

            # Environments
            web.get(u.environments, self.get_environments),
        ]
        # fmt: on

    # -------
    # Configs
    # -------

    @parameter_matcher
    async def get_configs(self) -> List[ConfigA]:
        return self.context.get_configs(dev_mode=True)

    @parameter_matcher
    async def get_configs_pkey(self, key: str) -> ConfigA:
        try:
            return self.context.get_config(key, dev_mode=True)
        except KeyError as e:
            raise HTTPBadRequest(reason=str(e))

    @parameter_matcher
    async def patch_configs_pkey(self, key: str, body: UpdateConfigValueQ) -> None:
        try:
            await self.context.set_config(key, body.value, dev_mode=True)
        except KeyError as e:
            raise HTTPBadRequest(reason=str(e))

    # -----
    # Infos
    # -----

    @parameter_matcher
    async def get_infos(self) -> List[InfoA]:
        result = list()
        for info in await self.context.get_infos():
            assert info.key
            item = InfoA(
                key=info.key,
                value=info.value,
                created_at=info.created_at,
                updated_at=info.updated_at,
            )
            result.append(item)
        return result

    @parameter_matcher
    async def post_infos(self, body: CreateInfoQ) -> None:
        try:
            await self.context.create_info(body.key, body.value)
        except KeyError as e:
            raise HTTPBadRequest(reason=str(e))

    @parameter_matcher
    async def get_infos_pkey(self, key: str) -> InfoA:
        try:
            db_info = await self.context.get_info(key)
        except RuntimeError as e:
            raise HTTPNotFound(reason=str(e))
        assert db_info.key
        return InfoA(
            key=db_info.key,
            value=db_info.value,
            created_at=db_info.created_at,
            updated_at=db_info.updated_at,
        )

    @parameter_matcher
    async def patch_infos_pkey(self, key: str, body: UpdateInfoQ) -> None:
        try:
            await self.context.update_info(key, body.value)
        except KeyError as e:
            raise HTTPBadRequest(reason=str(e))

    @parameter_matcher
    async def delete_infos_pkey(self, key: str) -> None:
        await self.context.delete_info(key)

    # ------
    # System
    # ------

    @parameter_matcher
    async def get_versions(self) -> VersionsA:
        return VersionsA(python=self.context.get_python_version_info())

    # -------
    # Plugins
    # -------

    @parameter_matcher
    async def get_plugins(self) -> List[PluginA]:
        return self.context.get_plugins()

    # ------------
    # Environments
    # ------------

    @parameter_matcher
    async def get_environments(self) -> List[EnvironmentA]:
        if self.context.config.developer:
            return self.context.get_environments()
        else:
            return self.context.get_environments(RECC_ENV_PREFIX)

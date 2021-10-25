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
from recc.http.http_decorator import parameter_matcher
from recc.packet.config import ConfigA, UpdateConfigValueQ
from recc.packet.daemon import DaemonA, CreateDaemonQ, UpdateDaemonQ
from recc.packet.environment import EnvironmentA
from recc.packet.info import InfoA, CreateInfoQ, UpdateInfoQ
from recc.packet.plugin import PluginA
from recc.packet.system import VersionsA
from recc.variables.environment import RECC_ENV_PREFIX
from recc.packet.cvt.daemon import daemon_to_answer


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

            # daemon
            web.get(u.daemon_plugins, self.get_daemon_plugins),
            web.get(u.daemons, self.get_daemons),
            web.post(u.daemons, self.post_daemons),
            web.get(u.daemons_pdaemon, self.get_daemons_pdaemon),
            web.patch(u.daemons_pdaemon, self.patch_daemons_pdaemon),
            web.delete(u.daemons_pdaemon, self.delete_daemons_pdaemon),
            web.post(u.daemons_pdaemon_start, self.post_daemons_pdaemon_start),
            web.post(u.daemons_pdaemon_stop, self.post_daemons_pdaemon_stop),
        ]
        # fmt: on

    # -------
    # Configs
    # -------

    @parameter_matcher()
    async def get_configs(self) -> List[ConfigA]:
        return self.context.get_configs(dev_mode=True)

    @parameter_matcher()
    async def get_configs_pkey(self, key: str) -> ConfigA:
        try:
            return self.context.get_config(key, dev_mode=True)
        except KeyError as e:
            raise HTTPBadRequest(reason=str(e))

    @parameter_matcher()
    async def patch_configs_pkey(self, key: str, body: UpdateConfigValueQ) -> None:
        try:
            self.context.set_config(key, body.value, dev_mode=True)
        except KeyError as e:
            raise HTTPBadRequest(reason=str(e))

    # -----
    # Infos
    # -----

    @parameter_matcher()
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

    @parameter_matcher()
    async def post_infos(self, body: CreateInfoQ) -> None:
        try:
            await self.context.create_info(body.key, body.value)
        except KeyError as e:
            raise HTTPBadRequest(reason=str(e))

    @parameter_matcher()
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

    @parameter_matcher()
    async def patch_infos_pkey(self, key: str, body: UpdateInfoQ) -> None:
        try:
            await self.context.update_info(key, body.value)
        except KeyError as e:
            raise HTTPBadRequest(reason=str(e))

    @parameter_matcher()
    async def delete_infos_pkey(self, key: str) -> None:
        await self.context.delete_info(key)

    # ------
    # System
    # ------

    @parameter_matcher()
    async def get_versions(self) -> VersionsA:
        return VersionsA(python=self.context.get_python_version_info())

    # -------
    # Plugins
    # -------

    @parameter_matcher()
    async def get_plugins(self) -> List[PluginA]:
        return self.context.get_plugins()

    # ------------
    # Environments
    # ------------

    @parameter_matcher()
    async def get_environments(self) -> List[EnvironmentA]:
        if self.context.config.developer:
            return self.context.get_environments()
        else:
            return self.context.get_environments(RECC_ENV_PREFIX)

    # ------
    # Daemon
    # ------

    @parameter_matcher()
    async def get_daemon_plugins(self) -> List[str]:
        return self.context.get_daemon_plugins()

    @parameter_matcher()
    async def get_daemons(self) -> List[DaemonA]:
        result = list()
        daemons = await self.context.get_daemons()
        for daemon in daemons:
            if not daemon.slug:
                raise RuntimeError("The `slug` of the daemon must exist.")
            answer = daemon_to_answer(daemon)
            answer.status = self.context.status(daemon.slug)
            answer.exit_code = None
            result.append(answer)
        return result

    @parameter_matcher()
    async def post_daemons(self, body: CreateDaemonQ) -> None:
        await self.context.create_daemon(
            plugin=body.plugin,
            slug=body.slug,
            name=body.name,
            address=body.address,
            requirements_sha256=None,
            description=body.description,
            extra=body.extra,
            enable=body.enable,
        )

    @parameter_matcher()
    async def get_daemons_pdaemon(self, daemon: str) -> DaemonA:
        db_daemon = await self.context.get_daemon_by_slug(daemon)
        if not db_daemon.slug:
            raise RuntimeError("The `slug` of the daemon must exist.")
        answer = daemon_to_answer(db_daemon)
        answer.status = self.context.status(db_daemon.slug)
        answer.exit_code = None
        return answer

    @parameter_matcher()
    async def patch_daemons_pdaemon(self, daemon: str, body: UpdateDaemonQ) -> None:
        uid = await self.context.get_daemon_uid_by_slug(daemon)
        await self.context.update_daemon(
            uid=uid,
            plugin=None,
            slug=body.slug,
            name=body.name,
            address=body.address,
            requirements_sha256=None,
            description=body.description,
            extra=body.extra,
            enable=body.enable,
        )

    @parameter_matcher()
    async def delete_daemons_pdaemon(self, daemon: str) -> None:
        await self.context.delete_daemon_by_slug(daemon)

    @parameter_matcher()
    async def post_daemons_pdaemon_start(self, daemon: str) -> None:
        await self.context.start_daemon(daemon)

    @parameter_matcher()
    async def post_daemons_pdaemon_stop(self, daemon: str) -> None:
        await self.context.stop_daemon(daemon)

# -*- coding: utf-8 -*-

from typing import List

from aiohttp import web
from aiohttp.web_exceptions import HTTPUnauthorized
from aiohttp.web_routedef import AbstractRouteDef

from recc.core.context import Context
from recc.http import http_urls as u
from recc.http.http_decorator import domain_group, domain_project
from recc.http.http_parameter import parameter_matcher
from recc.packet.user import (
    UpdatePasswordQ,
    UpdateUserInfoQ,
    UpdateUserQ,
    UserA,
    UserInfoA,
)
from recc.session.session_ex import SessionEx


class RouterV2Self:
    """
    API version 2 for self.
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
        # fmt: off
        return [
            # User
            web.get(u.empty, self.get_root),
            web.patch(u.empty, self.patch_root),
            web.delete(u.empty, self.delete_root),
            web.get(u.root, self.get_root),
            web.patch(u.root, self.patch_root),
            web.delete(u.root, self.delete_root),

            # User extra information
            web.get(u.extra, self.get_extra),
            web.get(u.extra_pkey, self.get_extra_pkey),
            web.patch(u.extra_pkey, self.patch_extra_pkey),

            # Password
            web.patch(u.password, self.patch_password),

            # Permission
            web.get(u.permissions_pgroup, self.get_permissions_pgroup),
            web.get(u.permissions_pgroup_pproject, self.get_permissions_pgroup_pproject),  # noqa
        ]
        # fmt: on

    # ----
    # User
    # ----

    @parameter_matcher
    async def get_root(self, session: SessionEx) -> UserA:
        db_user = await self.context.get_user(session.uid)
        return UserA.from_database(db_user)

    @parameter_matcher
    async def patch_root(self, session: SessionEx, body: UpdateUserQ) -> None:
        await self.context.update_user(
            uid=session.uid,
            email=body.email,
            phone=body.phone,
            admin=None,
            dark=body.dark,
            lang=body.lang,
            timezone=body.timezone,
        )

    @parameter_matcher
    async def delete_root(self, session: SessionEx) -> None:
        await self.context.remove_user_by_uid(session.uid)

    # ----------------------
    # User extra information
    # ----------------------

    @parameter_matcher
    async def get_extra(self, session: SessionEx) -> List[UserInfoA]:
        return await self.context.get_user_infos(session.uid)

    @parameter_matcher
    async def get_extra_pkey(self, session: SessionEx, key: str) -> UserInfoA:
        return await self.context.get_user_info(session.uid, key)

    @parameter_matcher
    async def patch_extra_pkey(
        self, session: SessionEx, key: str, body: UpdateUserInfoQ
    ) -> None:
        await self.context.set_user_info(session.uid, key, body.value)

    # --------
    # Password
    # --------

    @parameter_matcher
    async def patch_password(self, session: SessionEx, body: UpdatePasswordQ) -> None:
        if await self.context.challenge_password(session.audience, body.before):
            await self.context.change_password(session.audience, body.after)
        else:
            raise HTTPUnauthorized(reason="The password is incorrect.")

    # ----------
    # Permission
    # ----------

    @parameter_matcher
    @domain_group
    async def get_permissions_pgroup(self, session: SessionEx, group: str) -> List[str]:
        roles = await self.context.get_group_permission(session, group)
        return [role.slug for role in roles if role.slug]

    @parameter_matcher
    @domain_project
    async def get_permissions_pgroup_pproject(
        self, session: SessionEx, group: str, project: str
    ) -> List[str]:
        roles = await self.context.get_project_permission(session, group, project)
        return [role.slug for role in roles if role.slug]

# -*- coding: utf-8 -*-

from typing import List, Any, Dict
from aiohttp import web
from aiohttp.web_routedef import AbstractRouteDef
from aiohttp.web_exceptions import HTTPUnauthorized
from recc.core.context import Context
from recc.http.http_parameter import parameter_matcher
from recc.http.http_decorator import domain_group, domain_project
from recc.http import http_urls as u
from recc.session.session_ex import SessionEx
from recc.packet.user import UserA, UpdateUserQ, UpdatePasswordQ


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

            # User extra
            web.get(u.extra, self.get_extra),
            web.patch(u.extra, self.patch_extra),

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
        assert db_user.username is not None
        return UserA(
            username=db_user.username,
            nickname=db_user.nickname,
            email=db_user.email,
            phone1=db_user.phone1,
            phone2=db_user.phone2,
            is_admin=db_user.is_admin,
            extra=db_user.extra,
            created_at=db_user.created_at,
            updated_at=db_user.updated_at,
            last_login=db_user.last_login,
        )

    @parameter_matcher
    async def patch_root(self, session: SessionEx, body: UpdateUserQ) -> None:
        await self.context.update_user(
            uid=session.uid,
            email=body.email,
            phone1=body.phone1,
            phone2=body.phone2,
            is_admin=None,
            extra=body.extra,
        )

    @parameter_matcher
    async def delete_root(self, session: SessionEx) -> None:
        await self.context.remove_user_by_uid(session.uid)

    # ----------
    # User Extra
    # ----------

    @parameter_matcher
    async def get_extra(self, session: SessionEx) -> Any:
        db_user = await self.context.get_user(session.uid)
        return db_user.extra

    @parameter_matcher
    async def patch_extra(self, session: SessionEx, body: Dict[str, Any]) -> None:
        await self.context.update_user_extra(session.audience, body)

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

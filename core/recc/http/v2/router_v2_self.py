# -*- coding: utf-8 -*-

from typing import List, Any, Dict
from aiohttp import web
from aiohttp.web_routedef import AbstractRouteDef
from aiohttp.web_exceptions import HTTPUnauthorized, HTTPBadRequest
from recc.core.context import Context
from recc.http.http_decorator import parameter_matcher
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
        return [
            web.get(u.root, self.get_root),
            web.patch(u.root, self.patch_root),
            web.get(u.extra, self.get_extra),
            web.patch(u.extra, self.patch_extra),
            web.patch(u.password, self.patch_password),
        ]

    # --------
    # Handlers
    # --------

    @parameter_matcher()
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

    @parameter_matcher()
    async def patch_root(self, session: SessionEx, body: UpdateUserQ) -> None:
        await self.context.update_user(
            uid=session.uid,
            email=body.email,
            phone1=body.phone1,
            phone2=body.phone2,
            is_admin=None,
            extra=body.extra,
        )

    @parameter_matcher()
    async def get_extra(self, session: SessionEx) -> Any:
        db_user = await self.context.get_user(session.uid)
        return db_user.extra

    @parameter_matcher()
    async def patch_extra(self, session: SessionEx, body: Dict[str, Any]) -> None:
        await self.context.update_user_extra(session.audience, body)

    @parameter_matcher()
    async def patch_password(self, session: SessionEx, body: UpdatePasswordQ) -> None:
        try:
            if not self.context.challenge_password(session.audience, body.before):
                raise HTTPUnauthorized(reason="The password is incorrect.")
        except ValueError as e:
            raise HTTPBadRequest(reason=str(e))
        await self.context.change_password(session.audience, body.after)

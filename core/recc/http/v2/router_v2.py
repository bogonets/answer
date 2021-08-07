# -*- coding: utf-8 -*-

from typing import List, Any, Dict
from aiohttp import web
from aiohttp.hdrs import METH_OPTIONS, AUTHORIZATION
from aiohttp.web_routedef import AbstractRouteDef
from aiohttp.web_request import Request
from aiohttp.web_response import Response
from aiohttp.web_exceptions import (
    HTTPNotFound,
    HTTPUnauthorized,
    HTTPBadRequest,
    HTTPServiceUnavailable,
)
from recc.log.logging import recc_http_logger as logger
from recc.core.context import Context
from recc.http.v2.router_v2_public import RouterV2Public
from recc.http.header.bearer_auth import BearerAuth
from recc.http.http_response import auto_response
from recc.http.http_decorator import parameter_matcher
from recc.http import http_header_keys as h
from recc.http import http_urls as u
from recc.session.session import Session
from recc.database.struct.info import Info
from recc.database.struct.project import Project
from recc.core.struct.change_password_request import ChangePasswordRequest
from recc.database.struct.user import User
from recc.variables.http import DETAIL_RESPONSE_LOGGING_VERBOSE_LEVEL
from recc.variables.database import ANONYMOUS_GROUP_NAME


class RouterV2:
    """
    API version 2 - HTTP Router class.
    """

    def __init__(self, context: Context):
        self._context = context
        self._app = web.Application(middlewares=[self.middleware])
        self._app.add_routes(self._get_routes())

        self._public = RouterV2Public(context)
        self._app.add_subapp(u.public, self._public.app)

    @property
    def app(self) -> web.Application:
        return self._app

    @property
    def context(self) -> Context:
        return self._context

    async def _assign_session(self, request: Request) -> None:
        try:
            authorization = request.headers[AUTHORIZATION]
            bearer = BearerAuth.decode_from_authorization_header(authorization)
            request[h.session] = await self.context.get_access_session(bearer.token)
        except BaseException as e:
            logger.exception(e)
            error_message = str(e)
            if error_message:
                raise HTTPUnauthorized(reason=error_message)
            else:
                raise HTTPUnauthorized()

    @web.middleware
    async def middleware(self, request: Request, handler):
        if request.method == METH_OPTIONS:
            return await handler(request)

        if not request.path.startswith(u.api_v2_public):
            if not await self.context.exists_admin_user():
                raise HTTPServiceUnavailable(reason="Uninitialized server")
            await self._assign_session(request)

        try:
            return await handler(request)
        except PermissionError as e:
            logger.exception(e)
            error_message = str(e)
            if error_message:
                raise HTTPUnauthorized(reason=error_message)
            else:
                raise HTTPUnauthorized()

    # noinspection PyTypeChecker
    def _get_routes(self) -> List[AbstractRouteDef]:
        # fmt: off
        return [
            # GET: SELECT
            # PATCH: UPDATE
            # DELETE: DELETE
            # POST: INSERT, UPSERT, etc ...

            # self
            web.get(u.self, self.get_self),
            web.get(u.self_extra, self.get_self_extra),
            web.patch(u.self_extra, self.patch_self_extra),
            web.patch(u.self_password, self.patch_self_password),

            # configs
            web.get(u.infos, self.get_infos),
            web.post(u.infos, self.post_infos),
            web.get(u.infos_pkey, self.get_infos_pkey),
            web.delete(u.infos_pkey, self.delete_infos_pkey),

            # users
            web.get(u.users, self.get_users),
            web.post(u.users, self.post_users),
            web.get(u.users_puser, self.get_users_puser),
            web.patch(u.users_puser, self.patch_users_puser),
            web.delete(u.users_puser, self.delete_users_puser),

            # projects
            web.get(u.projects, self.get_projects),

            # # anonymous projects
            # web.get(u.projects_pproject, self.get_projects_pproject),
            # web.patch(u.projects_pproject, self.patch_projects_pproject),
            # web.delete(u.projects_pproject, self.delete_projects_pproject),
        ]
        # fmt: on

    def response(self, request: Request, data: Any = None) -> Response:
        verbose = self.context.config.verbose
        if data is None:
            if verbose >= DETAIL_RESPONSE_LOGGING_VERBOSE_LEVEL:
                logger.debug(f"{request.method} {request.path}")
            return Response()
        else:
            result = auto_response(request, data)
            if verbose >= DETAIL_RESPONSE_LOGGING_VERBOSE_LEVEL:
                logger.debug(f"{request.method} {request.path} -> {data}")
            return result

    # ----
    # Self
    # ----

    @parameter_matcher()
    async def get_self(self, session: Session) -> User:
        return await self.context.get_self(session)

    @parameter_matcher()
    async def get_self_extra(self, session: Session) -> Any:
        return await self.context.get_self_extra(session)

    @parameter_matcher()
    async def patch_self_extra(self, session: Session, extra: Dict[str, Any]) -> None:
        await self.context.update_user_extra(session.audience, extra)

    @parameter_matcher()
    async def patch_self_password(
        self, session: Session, change_password: ChangePasswordRequest
    ) -> None:
        before = change_password.before
        after = change_password.after
        try:
            if not self.context.challenge_password(session.audience, before):
                raise HTTPUnauthorized(reason="The password is incorrect.")
        except ValueError as e:
            raise HTTPBadRequest(reason=str(e))
        await self.context.change_password(session.audience, after)

    # -----
    # Infos
    # -----

    @parameter_matcher()
    async def get_infos(self, session: Session) -> Dict[str, str]:
        session_user = await self.context.get_self(session)
        if not session_user.is_admin:
            raise HTTPUnauthorized(reason="Administrator privileges are required")

        result = dict()
        for info in await self.context.get_infos():
            if not info.key:
                continue
            result[info.key] = info.value if info.value else ""
        return result

    @parameter_matcher()
    async def post_infos(self, session: Session, info: Info) -> None:
        assert info.key is not None
        assert info.value is not None
        session_user = await self.context.get_self(session)
        if not session_user.is_admin:
            raise HTTPUnauthorized(reason="Administrator privileges are required")
        await self.context.set_info(info.key, info.value)

    @parameter_matcher()
    async def get_infos_pkey(self, session: Session, key: str) -> Info:
        session_user = await self.context.get_self(session)
        if not session_user.is_admin:
            raise HTTPUnauthorized(reason="Administrator privileges are required")

        try:
            return await self.context.get_info(key)
        except RuntimeError as e:
            reason = str(e)
            logger.error(e)
            raise HTTPNotFound(reason=reason if reason else None)

    @parameter_matcher()
    async def delete_infos_pkey(self, session: Session, key: str) -> None:
        session_user = await self.context.get_self(session)
        if not session_user.is_admin:
            raise HTTPUnauthorized(reason="Administrator privileges are required")
        await self.context.delete_info(key)

    # -----
    # Users
    # -----

    @parameter_matcher()
    async def get_users(self, session: Session) -> List[User]:
        session_user = await self.context.get_self(session)
        if not session_user.is_admin:
            raise HTTPUnauthorized(reason="Administrator privileges are required")
        return await self.context.get_users()

    @parameter_matcher()
    async def post_users(self, session: Session, user: User) -> None:
        if not user.username:
            raise HTTPBadRequest(reason="Not exists username field")
        if not user.password:
            raise HTTPBadRequest(reason="Not exists password field")

        session_user = await self.context.get_self(session)
        if not session_user.is_admin:
            raise HTTPUnauthorized(reason="Administrator privileges are required")

        await self.context.signup(
            username=user.username,
            hashed_password=user.password,
            nickname=user.nickname,
            email=user.email,
            phone1=user.phone1,
            phone2=user.phone2,
            is_admin=user.is_admin,
            extra=user.extra,
        )

    @parameter_matcher()
    async def get_users_puser(self, session: Session, user: str) -> User:
        session_user = await self.context.get_self(session)
        if session.audience == user:
            return session_user

        if not session_user.is_admin:
            raise HTTPUnauthorized(reason="Administrator privileges are required")
        return await self.context.get_user(user)

    @parameter_matcher()
    async def patch_users_puser(
        self, session: Session, user: str, patch_user_info: User
    ) -> None:
        session_user = await self.context.get_self(session)
        if session.audience != user:
            if not session_user.is_admin:
                raise HTTPUnauthorized(reason="Administrator privileges are required")

        await self.context.update_user(
            user,
            email=patch_user_info.email,
            phone1=patch_user_info.phone1,
            phone2=patch_user_info.phone2,
            is_admin=patch_user_info.is_admin,
            extra=patch_user_info.extra,
        )

    @parameter_matcher()
    async def delete_users_puser(self, session: Session, user: str) -> None:
        session_user = await self.context.get_self(session)
        if not session_user.is_admin:
            raise HTTPUnauthorized(reason="Administrator privileges are required")
        await self.context.remove_user(user)

    # --------
    # Projects
    # --------

    @parameter_matcher()
    async def get_projects(self, session: Session) -> List[Project]:
        projects = await self.context.get_projects(ANONYMOUS_GROUP_NAME)
        for project in projects:
            project.remove_sensitive()
        return projects

    # async def post_projects(self, request: Request) -> Response:
    #     session = request[h.session]
    #     audience = session.audience
    #
    #     data = await read_dict(request, [d.project])
    #     group_name = data.get(d.group, ANONYMOUS_GROUP_NAME)
    #     project_name = data[d.project]
    #
    #     logging_msg = f"{{ {d.group}={group_name}, {d.project}={project_name} }}"
    #     logger.info(f"post_projects(session={audience}) {logging_msg}")
    #
    #     await self.context.create_project(group_name, project_name)
    #     return self.response(request)

    # ------------------
    # Anonymous projects
    # ------------------

    # async def get_projects_pproject(self, request: Request) -> Response:
    #     session = request[h.session]
    #     audience = session.audience
    #     project_name = request.match_info[p.project]
    #     params_msg = f"session={audience},{p.project}={project_name}"
    #     logger.info(f"get_projects_pproject({params_msg})")
    #
    #     group = ANONYMOUS_GROUP_NAME
    #     project = await self.context.get_project(group, project_name)
    #     return self.response(request, serialize_default(project))
    #
    # async def patch_projects_pproject(self, request: Request) -> Response:
    #     session = request[h.session]
    #     audience = session.audience
    #     project_name = request.match_info[p.project]
    #
    #     k = project_keys
    #     data = await read_dict(request)
    #
    #     params_msg = f"session={audience},{p.project}={project_name}"
    #     logger.info(f"patch_projects_pproject({params_msg})")
    #
    #     group = ANONYMOUS_GROUP_NAME
    #     await self.context.update_project(
    #         group,
    #         project_name,
    #         name=data.get(k.name),
    #         description=data.get(k.description),
    #         features=data.get(k.features),
    #         extra=data.get(k.extra),
    #     )
    #     return Response(status=501)
    #
    # async def delete_projects_pproject(self, request: Request) -> Response:
    #     session = request[h.session]
    #     audience = session.audience
    #     project_name = request.match_info[p.project]
    #     params_msg = f"session={audience},{p.project}={project_name}"
    #     logger.info(f"delete_projects_pproject({params_msg})")
    #
    #     group = ANONYMOUS_GROUP_NAME
    #     await self.context.delete_project(group, project_name)
    #     return self.response(request)

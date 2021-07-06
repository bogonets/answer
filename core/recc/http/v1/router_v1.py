# -*- coding: utf-8 -*-

from typing import List
from http import HTTPStatus
from aiohttp import web
from aiohttp.hdrs import METH_OPTIONS
from aiohttp.web_routedef import AbstractRouteDef
from aiohttp.web_request import Request
from aiohttp.web_response import Response
from recc.auth.basic_auth import BasicAuth
from recc.auth.bearer_auth import BearerAuth
from recc.variables.database import ANONYMOUS_GROUP_NAME
from recc.core.context import Context
from recc.http.v1 import path_v1 as pv1
from recc.http.v1.extra.airjoy_v1 import AirjoyV1
from recc.http.v1.extra.posod_v1 import PosodV1
from recc.http.v1.common import (
    PATH_PREFIX_API_V1,
    no_name,
    at_session,
    k_project,
    k_layout,
    k_user,
    k_task,
    k_bucket,
    k_object,
    k_lambda,
    k_output,
    get_v1_path,
    response_ok,
    response_error,
    response_ok_without_detail,
)
from recc.log.logging import recc_http_logger as logger
from recc.session.session import Session
from recc.struct.project import Project
from recc.struct.layout import Layout
from recc.struct.user import User
from recc.driver.json import global_json_encoder, global_json_decoder
from recc.util.version import version_text

GLOBAL_GROUP = ANONYMOUS_GROUP_NAME


class RouterV1:
    """
    API version 1.0 - HTTP Router class.
    """

    def __init__(self, context: Context):
        self._context = context
        self._no_auth_paths = {
            get_v1_path(pv1.initialization),
            get_v1_path(pv1.signup_admin),
            get_v1_path(pv1.login),
            get_v1_path(pv1.refresh_token),
            get_v1_path(pv1.get_core_version),
            get_v1_path(pv1.get_api_version),
        }
        self._app = web.Application(middlewares=[self._middleware])
        self._app.add_routes(self._get_routers())

        self._extra_airjoy = AirjoyV1(self._context)
        self._extra_airjoy.add_parent_app(self._app)

        self._extra_posod = PosodV1(self._context)
        self._extra_posod.add_parent_app(self._app)

    def _get_routers(self) -> List[AbstractRouteDef]:
        # fmt: off
        return [
            # [No authentication]
            web.get(pv1.initialization, self.on_initialization),
            web.post(pv1.signup_admin, self.on_signup_admin),
            web.post(pv1.login, self.on_login),
            web.put(pv1.refresh_token, self.on_refresh_token),
            web.get(pv1.get_core_version, self.on_get_core_version),
            web.get(pv1.get_api_version, self.on_get_api_version),

            # [Authentication]
            web.get(pv1.test_login, self.on_test_login),

            # user
            web.get(pv1.get_users, self.on_get_users),
            web.post(pv1.add_user, self.on_add_user),
            web.delete(pv1.delete_user, self.on_del_user),
            web.put(pv1.set_user, self.on_set_user),
            web.get(pv1.exist_user, self.on_exist_user),
            web.get(pv1.get_user, self.on_get_user),

            # template
            web.get(pv1.get_templates, self.on_get_templates),

            # project
            web.get(pv1.get_projects, self.on_get_projects),
            web.put(pv1.set_project, self.on_set_project),
            web.get(pv1.exist_project, self.on_exist_project),
            web.get(pv1.get_project, self.on_get_project),
            web.post(pv1.create_project, self.on_create_project),
            web.delete(pv1.delete_project, self.on_delete_project),

            # project/layout
            web.post(pv1.create_layout, self.on_create_layout),
            web.get(pv1.get_layouts, self.on_get_layouts),
            web.get(pv1.get_layout, self.on_get_layout),
            web.put(pv1.set_layout_extra, self.on_set_layout_extra),
            web.delete(pv1.delete_layout_extra, self.on_del_layout),
            web.post(pv1.exist_layout, self.on_exist_layout),

            # project/graph
            web.get(pv1.get_proj_graph, self.on_get_graph),
            web.post(pv1.set_proj_graph, self.on_set_graph),
            web.get(pv1.get_proj_graph_status, self.on_get_graph_status),
            web.post(pv1.stop_proj_task, self.on_stop_task),
            web.get(pv1.get_proj_task_prop, self.on_get_task_property_value),
            web.put(pv1.set_proj_task_prop, self.on_set_task_property_value),
            web.put(pv1.send_proj_task_signal, self.on_send_signal_lambda),
            web.get(pv1.get_property_hint, self.on_get_property_hint),

            # project/bucket
            web.get(pv1.get_buckets, self.on_get_buckets),
            web.post(pv1.create_bucket, self.on_create_bucket),
            web.delete(pv1.delete_bucket, self.on_delete_bucket),
            web.get(pv1.get_bucket_objs, self.on_get_buckets_objects),
            web.get(pv1.get_bucket_obj, self.on_get_buckets_object),
            web.post(pv1.set_bucket_obj, self.on_set_buckets_object),
            web.delete(pv1.delete_bucket_obj, self.on_delete_buckets_object),

            # widget/jupyter
            web.get(pv1.get_jupyters, self.on_get_jupyters),
            web.post(pv1.new_jupyter, self.on_new_jupyter),
            web.delete(pv1.delete_jupyter, self.on_delete_jupyter),
            web.get(pv1.get_pips, self.on_get_pips),
            web.get(pv1.get_pip, self.on_get_pip),
            web.post(pv1.add_pips, self.on_add_pips),
            web.delete(pv1.remove_pips, self.on_remove_pips),
            web.delete(pv1.remove_pip, self.on_remove_pip),

            # widget/image_viewer
            web.get(pv1.get_image_by_viewer, self.on_get_image_by_image_viewer_widget),
        ]
        # fmt: on

    @property
    def app(self) -> web.Application:
        return self._app

    @property
    def context(self) -> Context:
        return self._context

    def add_parent_app(self, parent_app: web.Application) -> None:
        assert self._app is not None
        assert parent_app is not None
        parent_app.add_subapp(PATH_PREFIX_API_V1, self._app)

    async def _get_access_session(self, request: Request) -> Session:
        authorization = request.headers["authorization"]
        auth = BearerAuth.decode_from_authorization_header(authorization)
        return await self.context.get_access_session(auth.token)

    async def _auth_middleware(self, request: Request, handler):
        session: Session
        try:
            session = await self._get_access_session(request)
        except Exception as e:
            logger.exception(e)
            return response_error(no_name, str(e), status=HTTPStatus.UNAUTHORIZED)

        request[at_session] = session
        try:
            return await handler(request)
        except Exception as e:
            logger.exception(e)
            return response_error(
                no_name, str(e), status=HTTPStatus.INTERNAL_SERVER_ERROR
            )

    @web.middleware
    async def _middleware(self, request: Request, handler):
        if request.path in self._no_auth_paths:
            return await handler(request)
        if request.method == METH_OPTIONS:
            return await handler(request)
        else:
            return await self._auth_middleware(request, handler)

    # ---------------
    # API v1 handlers
    # ---------------

    async def on_initialization(self, _: Request):
        name = "initialization"
        try:
            if await self.context.exist_admin_user():
                return response_ok(name)
            else:
                return response_error(name, "Not initialized yet.")
        except Exception as e:
            logger.exception(e)
            return response_error(name, str(e))

    async def on_signup_admin(self, request: Request):
        name = "signup_admin"
        try:
            json = await request.json(loads=global_json_decoder)
            user_id = json["id"]
            password = json["password"]  # Perhaps the client encoded it with SHA256.
            logger.info(f"on_signup_admin(id={user_id})")

            if await self.context.exist_admin_user():
                return response_error(name, "Root user already exists.")

            await self.context.signup_admin(user_id=user_id, hashed_user_pw=password)
            return response_ok(name)
        except Exception as e:
            logger.exception(e)
            return response_error(name, str(e))

    async def on_login(self, request: Request):
        name = "login"
        try:
            authorization = request.headers["authorization"]
            auth = BasicAuth.decode_from_authorization_header(authorization)
            logger.info(f"on_login(id={auth.user_id})")

            access_token, refresh_token = await self.context.login(
                auth.user_id, auth.password
            )

            return response_ok_without_detail(
                name,
                {
                    "user": {"id": auth.user_id},
                    "accessToken": access_token,
                    "refreshToken": refresh_token,
                    "t": "login",
                },
            )
        except Exception as e:
            logger.exception(e)
            return response_error(name, str(e), status=HTTPStatus.UNAUTHORIZED)

    async def on_refresh_token(self, request: Request):
        name = "token"
        try:
            authorization = request.headers["authorization"]
            auth = BearerAuth.decode_from_authorization_header(authorization)
            logger.info(f"on_refresh_token(id={auth.user_id})")

            renew_token = await self.context.renew_access_token(auth.token)
            return response_ok_without_detail(
                name, {"t": name, "accessToken": renew_token}
            )
        except Exception as e:
            logger.exception(e)
            return response_error(name, str(e), status=HTTPStatus.UNAUTHORIZED)

    async def on_get_core_version(self, _: Request):
        assert self
        name = "version-core"
        return response_ok_without_detail(
            name, {"t": name, "obj": {"info": version_text}}
        )

    async def on_get_api_version(self, _: Request):
        assert self
        name = "version-api"
        return response_ok_without_detail(
            name, {"t": name, "obj": {"info": version_text}}
        )

    async def on_test_login(self, request: Request):
        name = "test-login"
        session = request[at_session]
        username = session.audience
        logger.info(f"on_test_auth(session={username})")
        assert self
        return response_ok_without_detail(name)

    @staticmethod
    def _user_to_v1_dict(user: User) -> dict:
        created = user.created_at.isoformat() if user.created_at else ""
        modified = user.updated_at.isoformat() if user.updated_at else ""
        last_login = user.last_login.isoformat() if user.last_login else ""
        return {
            "createdAt": created,
            "modifiedAt": modified,
            "lastLogin": last_login,
            "id": user.username,
            "index": user.uid,
            "email": user.email,
            "telephone": user.phone1,
            "password": "",
        }

    async def on_get_users(self, request: Request):
        name = "get-user"
        session = request[at_session]
        username = session.audience
        logger.info(f"on_get_users(session={username})")
        users = await self.context.get_users(session)
        result = [self._user_to_v1_dict(u) for u in users]
        return response_ok_without_detail(name, {"obj": result, "t": "get-user"})

    async def on_add_user(self, request: Request):
        name = "create"
        session = request[at_session]
        username = session.audience
        json: dict = await request.json(loads=global_json_decoder)
        user_id = json["id"]
        password = json["password"]  # Perhaps the client encoded it with SHA256.
        email = json.get("email")
        phone1 = json.get("telephone")
        logger.info(f"on_add_user(session={username},new_user={user_id})")
        await self.context.signup(
            user_id,
            password,
            email=email,
            phone1=phone1,
        )
        return response_ok(name)

    async def on_del_user(self, request: Request):
        name = "delete-user"
        session = request[at_session]
        username = session.audience
        json: dict = await request.json(loads=global_json_decoder)
        user_id = json["id"]
        logger.info(f"on_del_user(session={username},new_user={user_id})")
        await self.context.remove_user(user_id)
        return response_ok(name)

    async def on_set_user(self, request: Request):
        name = "update-user"
        session = request[at_session]
        username = session.audience
        json: dict = await request.json(loads=global_json_decoder)
        user_id = json["id"]
        email = json.get("email")
        phone1 = json.get("telephone")
        logger.info(f"on_set_user(session={username},new_user={user_id})")
        await self.context.update_user(
            user_id,
            email=email,
            phone1=phone1,
        )
        return response_ok(name)

    async def on_exist_user(self, request: Request):
        name = "check-user"
        session = request[at_session]
        username = session.audience
        test_username = request.match_info[k_user]
        logger.info(f"on_exist_user(session={username},test={test_username})")

        result = await self.context.exist_user(session, test_username)
        return response_ok_without_detail(name, {"t": name, "obj": {"findId": result}})

    async def on_get_user(self, request: Request):
        name = "get-user"
        session = request[at_session]
        username = session.audience
        request_username = request.match_info[k_user]
        logger.info(f"on_get_user(session={username},user={request_username})")

        user = await self.context.get_user(session, request_username)
        result = self._user_to_v1_dict(user)
        return response_ok_without_detail(name, {"obj": result, "t": "get-user"})

    async def on_get_templates(self, request: Request):
        name = "graph-template"
        session = request[at_session]
        username = session.audience
        logger.info(f"on_get_templates(session={username})")

        result = await self.context.get_templates_v1(session)
        return response_ok_without_detail(name, {"t": name, "obj": result})

    @staticmethod
    def _project_to_v1_dict(project: Project) -> dict:
        state = False
        created = project.created_at.isoformat() if project.created_at else ""
        modified = project.updated_at.isoformat() if project.updated_at else ""
        return {
            "active": "Active" if state else "Inactive",
            "createdAt": created,
            "modifiedAt": modified,
            "name": project.name,
            "menus": [0, 1, 2, 3, 4],
            "t": "project",
        }

    async def on_get_projects(self, request: Request):
        name = "getAll-project"
        session = request[at_session]
        username = session.audience
        logger.info(f"on_get_projects(session={username})")

        projects = await self.context.get_projects(session, GLOBAL_GROUP)
        result = [self._project_to_v1_dict(project) for project in projects]
        return response_ok_without_detail(name, {"t": name, "obj": result})

    async def on_set_project(self, _: Request):
        assert self
        return response_error("Not implemented")

    async def on_exist_project(self, request: Request):
        name = "exist-project"
        session = request[at_session]
        username = session.audience
        logger.info(f"on_exist_project(session={username})")

        assert self
        return response_error(name, "Not implemented", None, HTTPStatus.NOT_IMPLEMENTED)

    async def on_get_project(self, request: Request):
        name = "project"
        session = request[at_session]
        username = session.audience
        projname = request.match_info[k_project]
        logger.info(f"on_get_project(session={username},project={projname})")

        project = await self.context.get_project(session, GLOBAL_GROUP, projname)
        result = self._project_to_v1_dict(project)
        return response_ok_without_detail(name, result)

    async def on_create_project(self, request: Request):
        name = "create-project"
        session = request[at_session]
        username = session.audience
        projname = request.match_info[k_project]
        logger.info(f"on_create_project(session={username},project={projname})")

        await self.context.create_project(session, GLOBAL_GROUP, projname)
        return response_ok_without_detail(name)

    async def on_delete_project(self, request: Request):
        name = "delete-project"
        session = request[at_session]
        username = session.audience
        projname = request.match_info[k_project]
        logger.info(f"on_delete_project(session={username},project={projname})")

        await self.context.delete_global_project(session, GLOBAL_GROUP, projname)
        return response_ok_without_detail(name)

    async def on_create_layout(self, request: Request):
        name = "project-layout"
        session = request[at_session]
        username = session.audience
        projname = request.match_info[k_project]
        params = f"username={username},project={projname}"
        logger.info(f"on_set_layout_extra({params})")

        request_json = await request.json(loads=global_json_decoder)
        layout_name = request_json["name"]
        layout_panels = global_json_decoder(request_json["panels"])

        await self.context.create_layout(session, projname, layout_name, layout_panels)
        layout = await self.context.get_layout(session, projname, layout_name)
        return response_ok_without_detail(name, self._layout_to_v1_dict(layout))

    async def on_get_layouts(self, request: Request):
        name = "project-layouts"
        session = request[at_session]
        username = session.audience
        projname = request.match_info[k_project]
        logger.info(f"on_get_layouts(session={username},project={projname})")

        layouts = await self.context.get_layouts(session, projname)
        result = [layout.name for layout in layouts]
        return response_ok_without_detail(name, {"layouts": result, "t": "layouts"})

    @staticmethod
    def _layout_to_v1_dict(layout: Layout) -> dict:
        created = layout.created_at.isoformat() if layout.created_at else ""
        modified = layout.updated_at.isoformat() if layout.updated_at else ""
        return {
            "createdAt": created,
            "modifiedAt": modified,
            "name": layout.name,
            "panels": global_json_encoder(layout.extra) if layout.extra else str(),
            "t": "layout",
        }

    async def on_get_layout(self, request: Request):
        name = "project-layout"
        session = request[at_session]
        username = session.audience
        projname = request.match_info[k_project]
        layname = request.match_info[k_layout]
        params = f"username={username},project={projname},layout={layname}"
        logger.info(f"on_get_layout({params})")

        layout = await self.context.get_layout(session, projname, layname)
        return response_ok_without_detail(name, self._layout_to_v1_dict(layout))

    async def on_set_layout_extra(self, request: Request):
        name = "project-layout"
        session = request[at_session]
        username = session.audience
        projname = request.match_info[k_project]
        layname = request.match_info[k_layout]
        params = f"username={username},project={projname},layout={layname}"
        logger.info(f"on_set_layout_extra({params})")

        request_dict = await request.json(loads=global_json_decoder)
        # layout_name = request_json["name"]  # Unused
        panels_json = request_dict["panels"]
        if isinstance(panels_json, str):
            if panels_json:
                panels = global_json_decoder(panels_json)
            else:
                panels = None
        else:
            panels = panels_json

        await self.context.set_layout_extra(session, projname, layname, panels)
        layout = await self.context.get_layout(session, projname, layname)
        return response_ok_without_detail(name, self._layout_to_v1_dict(layout))

    async def on_del_layout(self, request: Request):
        name = "project-layout"
        session = request[at_session]
        username = session.audience
        projname = request.match_info[k_project]
        layname = request.match_info[k_layout]
        params = f"username={username},project={projname},layout={layname}"
        logger.info(f"on_del_layout({params})")

        await self.context.remove_layout(session, projname, layname)
        return response_ok_without_detail(name)

    async def on_exist_layout(self, request: Request):
        name = "project-layouts-check"
        session = request[at_session]
        username = session.audience
        projname = request.match_info[k_project]
        logger.info(f"on_exist_layout(session={username},project={projname})")

        request_json = await request.json(loads=global_json_decoder)
        layout_name = request_json["name"]
        result = await self.context.exists_layout(session, projname, layout_name)
        return response_ok_without_detail(name, {"check": result, "t": "layout-check"})

    @staticmethod
    def _graph_to_v1_dict() -> dict:
        return {
            "links": [],
            "nodes": [],
            "tasks": [],
        }

    async def on_get_graph(self, request: Request):
        name = "graph"
        session = request[at_session]
        username = session.audience
        projname = request.match_info[k_project]
        logger.info(f"on_get_graph(session={username},project={projname})")

        # graph = await self.context.get_tasks(session, projname)
        result = self._graph_to_v1_dict()
        return response_ok_without_detail(name, {"obj": result, "t": name})

    async def on_set_graph(self, request: Request):
        name = "graph-modify"
        session = request[at_session]
        username = session.audience
        projname = request.match_info[k_project]
        logger.info(f"on_set_graph(session={username},project={projname})")

        request_json = await request.json(loads=global_json_decoder)
        group_name = ""
        await self.context.set_graph_with_extra_v1(
            session, group_name, projname, request_json
        )
        result = [
            {
                "msg": "",
                "status": "OK",
                "taskId": 1,
            },
        ]
        return response_ok_without_detail(name, {"t": name, "obj": result})

    async def on_get_graph_status(self, request: Request):
        name = "graph-infos"
        session = request[at_session]
        username = session.audience
        projname = request.match_info[k_project]
        logger.info(f"on_get_graph_status(session={username},project={projname})")

        status = await self.context.get_task_status(session, GLOBAL_GROUP, projname)
        result = [{"name": s.name, "state": str(s.status)} for s in status]
        return response_ok_without_detail(name, {"obj": {"tasks": result}, "t": name})

    async def on_stop_task(self, request: Request):
        name = "postGraphStop"
        session = request[at_session]
        username = session.audience
        projname = request.match_info[k_project]
        taskname = request.match_info[k_task]
        params = f"session={username},project={projname},task={taskname}"
        logger.info(f"on_stop_task({params})")

        # await self.context.stop_task(session, projname, taskname)
        return response_ok_without_detail(name)

    async def on_get_task_property_value(self, request: Request):
        name = "get-lambda-properties"
        session = request[at_session]
        username = session.audience
        projname = request.match_info[k_project]
        taskname = request.match_info[k_task]
        params = f"session={username},project={projname},task={taskname}"
        logger.info(f"on_stop_task({params})")

        # q: {"lambda": "image/manage_rois7", "property": "infos"}
        q_txt = request.url.query.get("q")
        if q_txt is None:
            return response_error(name)

        q_obj = global_json_decoder(q_txt)
        lambda_name = q_obj["lambda"]
        property_name = q_obj["property"]

        result = await self.context.get_lambda_property_value(
            session,
            projname,
            taskname,
            lambda_name,
            property_name,
        )
        return response_ok_without_detail(name, {"obj": result, "t": name})

    async def on_set_task_property_value(self, request: Request):
        name = "set-lambda-properties"
        session = request[at_session]
        username = session.audience
        projname = request.match_info[k_project]
        taskname = request.match_info[k_task]
        params = f"session={username},project={projname},task={taskname}"
        logger.info(f"on_set_task_property_value({params})")

        request_json = await request.json(loads=global_json_decoder)
        lambda_name = request_json["lambda"]
        property_name = request_json["property"]
        property_value = request_json["value"]

        await self.context.set_lambda_property_value(
            session,
            projname,
            taskname,
            lambda_name,
            property_name,
            property_value,
        )
        return response_ok_without_detail(name, {"obj": {"updateDB": True}, "t": name})

    async def on_send_signal_lambda(self, request: Request):
        # name = "send-signal"
        session = request[at_session]
        username = session.audience
        projname = request.match_info[k_project]
        taskname = request.match_info[k_task]
        params = f"session={username},project={projname},task={taskname}"
        logger.info(f"on_send_signal_lambda({params})")

        request_json = await request.json(loads=global_json_decoder)
        signal_name = request_json["name"]
        lambda_name = request_json["lambda_name"]
        input_queries = request_json["input_queries"]
        output_queries = request_json["output_queries"]

        result = await self.context.send_signal_v1(
            session,
            projname,
            taskname,
            signal_name,
            lambda_name,
            input_queries,
            output_queries,
        )
        return Response(body=result)

    async def on_get_property_hint(self, _: Request):
        assert self
        return response_error("Not implemented")

    async def on_get_buckets(self, request: Request):
        name = "get-buckets"
        session = request[at_session]
        username = session.audience
        projname = request.match_info[k_project]
        logger.info(f"on_get_buckets(session={username},project={projname})")

        result = None
        assert self
        return response_ok_without_detail(name, {"obj": result, "t": name})

    async def on_create_bucket(self, request: Request):
        name = "create-bucket"
        session = request[at_session]
        username = session.audience
        projname = request.match_info[k_project]
        logger.info(f"on_create_bucket(session={username},project={projname})")

        result = None
        assert self
        return response_ok_without_detail(name, {"obj": result, "t": name})

    async def on_delete_bucket(self, request: Request):
        name = "delete-bucket"
        session = request[at_session]
        username = session.audience
        projname = request.match_info[k_project]
        bucketname = request.match_info[k_bucket]
        params = f"session={username},project={projname},bucket={bucketname}"
        logger.info(f"on_delete_bucket({params})")

        result = None
        assert self
        return response_ok_without_detail(name, {"obj": result, "t": name})

    async def on_get_buckets_objects(self, request: Request):
        name = "get-bucket-objects"
        session = request[at_session]
        username = session.audience
        projname = request.match_info[k_project]
        bucketname = request.match_info[k_bucket]
        params = f"session={username},project={projname},bucket={bucketname}"
        logger.info(f"on_get_buckets_objects({params})")

        result = None
        assert self
        return response_ok_without_detail(name, {"obj": result, "t": name})

    async def on_get_buckets_object(self, request: Request):
        name = "get-bucket-object"
        session = request[at_session]
        username = session.audience
        projname = request.match_info[k_project]
        bucketname = request.match_info[k_bucket]
        objname = request.match_info[k_object]
        params1 = f"session={username},project={projname}"
        params2 = f"bucket={bucketname},object={objname}"
        logger.info(f"on_get_buckets_object({params1},{params2})")

        result = None
        assert self
        return response_ok_without_detail(name, {"obj": result, "t": name})

    async def on_set_buckets_object(self, request: Request):
        name = "set-bucket-object"
        session = request[at_session]
        username = session.audience
        projname = request.match_info[k_project]
        bucketname = request.match_info[k_bucket]
        params = f"session={username},project={projname},bucket={bucketname}"
        logger.info(f"on_set_buckets_object({params})")

        result = None
        assert self
        return response_ok_without_detail(name, {"obj": result, "t": name})

    async def on_delete_buckets_object(self, request: Request):
        name = "remove-bucket-object"
        session = request[at_session]
        username = session.audience
        projname = request.match_info[k_project]
        bucketname = request.match_info[k_bucket]
        objname = request.match_info[k_object]
        params1 = f"session={username},project={projname}"
        params2 = f"bucket={bucketname},object={objname}"
        logger.info(f"on_delete_buckets_object({params1},{params2})")

        result = None
        assert self
        return response_ok_without_detail(name, {"obj": result, "t": name})

    async def on_get_jupyters(self, _: Request):
        assert self
        return response_error("Not implemented")

    async def on_new_jupyter(self, _: Request):
        assert self
        return response_error("Not implemented")

    async def on_delete_jupyter(self, _: Request):
        assert self
        return response_error("Not implemented")

    async def on_get_pips(self, _: Request):
        assert self
        return response_error("Not implemented")

    async def on_get_pip(self, _: Request):
        assert self
        return response_error("Not implemented")

    async def on_add_pips(self, _: Request):
        assert self
        return response_error("Not implemented")

    async def on_remove_pips(self, _: Request):
        assert self
        return response_error("Not implemented")

    async def on_remove_pip(self, _: Request):
        assert self
        return response_error("Not implemented")

    async def on_get_image_by_image_viewer_widget(self, request: Request):
        name = "get-image-by-image-viewer-widget"
        session = request[at_session]
        username = session.audience
        projname = request.match_info[k_project]
        taskname = request.match_info[k_task]
        lambdaname = request.match_info[k_lambda]
        outname = request.match_info[k_output]
        params1 = f"session={username},project={projname}"
        params2 = f"task={taskname},lambda={lambdaname},output={outname}"
        logger.info(f"on_delete_buckets_object({params1},{params2})")

        result = None
        assert self
        return response_ok_without_detail(name, {"obj": result, "t": name})

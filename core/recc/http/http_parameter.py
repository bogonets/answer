# -*- coding: utf-8 -*-

from typing import Optional, Union, List, Any, get_origin, get_args
from inspect import signature, isclass, iscoroutinefunction
from functools import wraps
from http import HTTPStatus

from aiohttp.hdrs import AUTHORIZATION
from aiohttp.web_request import Request
from aiohttp.web_response import Response
from aiohttp.web_exceptions import (
    HTTPException,
    HTTPBadRequest,
    HTTPUnauthorized,
)

from recc.access_control.acl import AccessControlList
from recc.core.context import Context
from recc.chrono.datetime import today
from recc.session.session import Session
from recc.session.session_ex import SessionEx
from recc.log.logging import recc_http_logger as logger
from recc.serialization.serialize import serialize_default
from recc.http.header.basic_auth import BasicAuth
from recc.http.header.bearer_auth import BearerAuth
from recc.access_control.policy import Policy
from recc.http.http_packet import HttpRequest, HttpResponse
from recc.http.http_payload import payload_to_object, request_payload_to_class
from recc.http.http_response import get_accept_type, get_encoding, create_response
from recc.http.http_status import (
    STATUS_BAD_REQUEST,
    STATUS_UNAUTHORIZED,
    STATUS_INTERNAL_SERVER_ERROR,
)
from recc.http import http_cache_keys as c
from recc.http import http_path_keys as p
from recc.conversion.boolean import str_to_bool
from recc.variables.http import VERY_VERBOSE_DEBUGGING

ERROR_MESSAGE_ONLY_SINGLE_POLICIES = (
    "Group and project permissions cannot be checked at the same time."
)


def _is_serializable_instance(obj: Any) -> bool:
    if isinstance(obj, dict):
        return True
    if isinstance(obj, str):
        return True
    if isinstance(obj, int):
        return True
    if isinstance(obj, list):
        return True
    if isinstance(obj, float):
        return True
    if isinstance(obj, bool):
        return True
    return False


def _is_serializable_class(obj: type) -> bool:
    if issubclass(obj, dict):
        return True
    if issubclass(obj, str):
        return True
    if issubclass(obj, int):
        return True
    if issubclass(obj, list):
        return True
    if issubclass(obj, float):
        return True
    if issubclass(obj, bool):
        return True
    return False


def is_subclass_safe(obj, cls) -> bool:
    if not isinstance(obj, type):
        return False
    return issubclass(obj, cls)


def is_path_class(obj) -> bool:
    if not isinstance(obj, type):
        return False
    if issubclass(obj, str):
        return True
    if issubclass(obj, int):
        return True
    if issubclass(obj, float):
        return True
    if issubclass(obj, bool):
        return True
    return False


def cast_builtin_type_from_string(data: str, cls) -> Any:
    assert isinstance(cls, type)
    if issubclass(cls, str):
        return data
    elif issubclass(cls, int):
        return int(data)
    elif issubclass(cls, float):
        return float(data)
    elif issubclass(cls, bool):
        return str_to_bool(data)
    return cls(data)  # type: ignore[call-arg]


async def _parameter_matcher_main(
    func,
    obj: Any,
    request: Request,
    acl: AccessControlList,
) -> Response:
    accept = get_accept_type(request)
    encoding = get_encoding(request)

    sig = signature(func)
    keys = list(sig.parameters.keys())
    update_arguments: List[Any] = list()
    match_count = len(request.match_info)
    assign_body = False

    group_name: Optional[str] = None
    project_name: Optional[str] = None

    very_verbose_debugging = False
    context = request[c.context] if c.context in request else None
    if context:
        if isinstance(context, Context):
            config = context.config
            if config and config.developer and config.verbose >= VERY_VERBOSE_DEBUGGING:
                very_verbose_debugging = True
        else:
            context = None

    if obj is None:
        argument_keys = keys
    else:
        assert len(keys) >= 1
        update_arguments.append(obj)  # keys[0] is class instance. maybe 'self'
        argument_keys = keys[1:]

    for key in argument_keys:
        param = sig.parameters[key]
        type_origin = get_origin(param.annotation)
        type_args = get_args(param.annotation)
        if type_origin is None:
            if isinstance(param.annotation, type):
                type_origin = param.annotation
            elif isinstance(param.annotation, str):
                if param.annotation == "str":
                    type_origin = str
                elif param.annotation == "int":
                    type_origin = int
                elif param.annotation == "float":
                    type_origin = float
                elif param.annotation == "bytes":
                    type_origin = bytes
                elif param.annotation == "list":
                    type_origin = list
                elif param.annotation == "set":
                    type_origin = set
                elif param.annotation == "dict":
                    type_origin = dict
                else:
                    msg = f"Unknown annotation string: {param.annotation}"
                    raise NotImplementedError(msg)
            else:
                msg = f"Unknown annotation type: {type(param.annotation).__name__}"
                raise NotImplementedError(msg)

        assert type_origin is not None
        assert isinstance(type_origin, type) or type_origin is Union

        optional_parameter: Optional[type]
        if type_origin is Union and len(type_args) == 2 and type(None) in type_args:
            if type_args.index(type(None)) == 0:
                optional_parameter = type_args[1]
            else:
                optional_parameter = type_args[0]
        else:
            optional_parameter = None

        # BasicAuth
        if is_subclass_safe(type_origin, BasicAuth):
            if AUTHORIZATION not in request.headers:
                raise HTTPBadRequest(reason=f"Not exists {AUTHORIZATION} header")
            try:
                authorization = request.headers[AUTHORIZATION]
                basic = BasicAuth.decode_from_authorization_header(authorization)
            except ValueError as e:
                raise HTTPBadRequest(reason=str(e))
            update_arguments.append(basic)
            continue

        # BearerAuth
        if is_subclass_safe(type_origin, BearerAuth):
            if AUTHORIZATION not in request.headers:
                raise HTTPBadRequest(reason=f"Not exists {AUTHORIZATION} header")
            try:
                authorization = request.headers[AUTHORIZATION]
                bearer = BearerAuth.decode_from_authorization_header(authorization)
            except ValueError as e:
                raise HTTPBadRequest(reason=str(e))
            update_arguments.append(bearer)
            continue

        # Request
        if is_subclass_safe(type_origin, Request):
            update_arguments.append(request)
            continue

        # HttpRequest
        if is_subclass_safe(type_origin, HttpRequest):
            update_arguments.append(
                HttpRequest(
                    method=request.method,
                    path=request.path,
                    data=await request.read(),
                    headers=request.headers,
                )
            )
            continue

        # Session
        if is_subclass_safe(type_origin, Session):
            if c.session not in request:
                raise HTTPUnauthorized(reason=f"Not exists {c.session}")
            update_arguments.append(request[c.session])
            continue

        # SessionEx
        if is_subclass_safe(type_origin, SessionEx):
            if c.session not in request:
                raise HTTPUnauthorized(reason=f"Not exists {c.session}")
            update_arguments.append(request[c.session])
            continue

        # Path
        if (
            is_path_class(type_origin)
            and match_count >= 1
            and key in request.match_info
        ):
            path_value = request.match_info[key]

            if key == p.group:
                group_name = path_value
            elif key == p.project:
                project_name = path_value

            try:
                path_arg = cast_builtin_type_from_string(path_value, type_origin)
                update_arguments.append(path_arg)
            except ValueError:
                logger.debug(f"Type casting error for path parameter: {key}")
                update_arguments.append(path_value)

            match_count -= 1
            continue

        # Query
        if optional_parameter is not None:
            if key in request.rel_url.query:
                query_value = request.rel_url.query[key]
                try:
                    query_arg = cast_builtin_type_from_string(
                        query_value, optional_parameter
                    )
                    update_arguments.append(query_arg)
                except ValueError:
                    logger.debug(f"Type casting error for query parameter: {key}")
                    update_arguments.append(query_value)
            else:
                update_arguments.append(None)
            continue

        # Body
        if not assign_body:
            if _is_serializable_class(type_origin):
                body = payload_to_object(request.headers, await request.text())
                assign_body = True
            elif isclass(type_origin):
                body = await request_payload_to_class(request, type_origin)  # noqa
                assign_body = True
            else:
                body = None

            if assign_body:
                assert body is not None
                if very_verbose_debugging:
                    logger.debug(f"Request BODY: {str(body)}")
                update_arguments.append(body)
                continue

        update_arguments.append(None)

    if acl.exists():
        if not context:
            raise RuntimeError("The context does not exist")
        if c.session not in request:
            raise HTTPUnauthorized(reason=f"Not exists session: {c.session}")

        session = request[c.session]
        assert isinstance(session, SessionEx)

        if not session.is_admin:
            if acl.admin:
                raise PermissionError("You do not have administrator privileges")
            if acl.groups and acl.projects:
                raise RuntimeError(ERROR_MESSAGE_ONLY_SINGLE_POLICIES)
            if acl.groups:
                await acl.test_groups(context, session, group_name)
            else:
                assert acl.projects
                await acl.test_projects(context, session, group_name, project_name)

    if iscoroutinefunction(func):
        result = await func(*update_arguments)
    else:
        result = func(*update_arguments)

    if very_verbose_debugging:
        logger.debug(f"RESULT: {str(result)}")

    if result is None:
        return Response()
    elif isinstance(result, Response):
        return result
    elif isinstance(result, HttpResponse):
        return Response(
            body=result.data,
            status=result.status if result.status else HTTPStatus.INTERNAL_SERVER_ERROR,
            reason=result.reason,
            headers=result.headers,
        )
    elif _is_serializable_instance(result):
        return create_response(accept, encoding, result)
    elif isclass(type(result)):
        return create_response(accept, encoding, serialize_default(result))

    raise NotImplementedError


async def parameter_matcher_main(
    func,
    obj: Any,
    request: Request,
    *,
    group_policies: Optional[List[Policy]] = None,
    project_policies: Optional[List[Policy]] = None,
    has_features: Optional[List[str]] = None,
    has_admin=False,
) -> Response:
    now = today()

    # Forwarded
    # X-Forwarded-For
    # X-Forwarded-Host
    # X-Forwarded-Proto
    remote = request.remote
    method = request.method
    path = request.path
    version = request.version
    request_info = f"{remote} {method} {path} HTTP/{version[0]}.{version[1]}"

    try:
        acl = AccessControlList(
            func,
            group_policies,
            project_policies,
            has_features,
            has_admin,
        )
        result = await _parameter_matcher_main(func, obj, request, acl)
    except HTTPException as e:
        logger.error(e)
        result = Response(
            status=e.status,
            reason=e.reason,
            text=e.text,
            headers=e.headers,
        )
    except (ValueError, KeyError) as e:
        logger.exception(e)
        result = Response(status=STATUS_BAD_REQUEST, reason=str(e))
    except PermissionError as e:
        logger.exception(e)
        result = Response(status=STATUS_UNAUTHORIZED, reason=str(e))
    except BaseException as e:
        logger.exception(e)
        result = Response(status=STATUS_INTERNAL_SERVER_ERROR, reason=str(e))

    status = result.status
    reason = result.reason
    duration = (today() - now).total_seconds()
    response_info = f"{status} {reason} ({duration:.3f}s)"
    logger.info(f"{request_info} -> {response_info}")

    return result


def parameter_matcher(
    *,
    group_policies: Optional[List[Policy]] = None,
    project_policies: Optional[List[Policy]] = None,
    has_features: Optional[List[str]] = None,
    has_admin=False,
):
    if group_policies and project_policies:
        raise RuntimeError(ERROR_MESSAGE_ONLY_SINGLE_POLICIES)

    def _wrap(func):
        @wraps(func)
        async def __wrap(obj, request):
            return await parameter_matcher_main(
                func,
                obj,
                request,
                group_policies=group_policies,
                project_policies=project_policies,
                has_features=has_features,
                has_admin=has_admin,
            )

        return __wrap

    return _wrap

# -*- coding: utf-8 -*-

from typing import List, Any, get_origin
from inspect import signature, isclass, iscoroutinefunction
from functools import wraps
from datetime import datetime
from http import HTTPStatus

from aiohttp.hdrs import AUTHORIZATION
from aiohttp.web_request import Request
from aiohttp.web_response import Response
from aiohttp.web_exceptions import (
    HTTPException,
    HTTPBadRequest,
    HTTPUnauthorized,
)
from recc.core.context import Context
from recc.session.session import Session
from recc.log.logging import recc_http_logger as logger
from recc.serialization.serialize import serialize_default
from recc.http.header.basic_auth import BasicAuth
from recc.http.http_packet import HttpRequest, HttpResponse
from recc.http.http_payload import payload_to_object, request_payload_to_class
from recc.http.http_response import get_accept_type, get_encoding, create_response
from recc.session.session_ex import SessionEx
from recc.http.http_status import (
    STATUS_BAD_REQUEST,
    STATUS_UNAUTHORIZED,
    STATUS_INTERNAL_SERVER_ERROR,
)
from recc.http import http_cache_keys as c
from recc.variables.http import VERY_VERBOSE_DEBUGGING

CONTEXT_PROPERTY_NAME = "context"
CONFIG_PROPERTY_NAME = "config"


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
    return False


# def _test_permission(session: SessionEx, acl: Set[aa]) -> None:
#     for ac in acl:
#         if ac == aa.HasAdmin:
#             if not session.is_admin:
#                 raise HTTPForbidden(reason="Administrator privileges are required")
#
#     # if acl:
#     #     if c.session not in request:
#     #         raise HTTPUnauthorized(reason=f"Not exists {c.session}")
#     #     _test_permission(request[c.session], acl if acl else set())


async def _parameter_matcher_main(
    func,
    obj: Any,
    request: Request,
) -> Response:
    accept = get_accept_type(request)
    encoding = get_encoding(request)

    sig = signature(func)
    keys = list(sig.parameters.keys())
    update_arguments: List[Any] = list()
    match_count = len(request.match_info)
    assign_body = False

    very_verbose_debugging = False
    context = getattr(obj, CONTEXT_PROPERTY_NAME, None)
    if context and isinstance(context, Context):
        config = getattr(obj, CONFIG_PROPERTY_NAME, None)
        if config and config.developer and config.verbose >= VERY_VERBOSE_DEBUGGING:
            very_verbose_debugging = True

    if obj is None:
        argument_keys = keys
    else:
        assert len(keys) >= 1
        update_arguments.append(obj)  # keys[0] is class instance. maybe 'self'
        argument_keys = keys[1:]

    for key in argument_keys:
        param = sig.parameters[key]
        type_origin = get_origin(param.annotation)
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
        assert isinstance(type_origin, type)

        # BasicAuth
        if issubclass(type_origin, BasicAuth):
            if AUTHORIZATION not in request.headers:
                raise HTTPBadRequest(reason=f"Not exists {AUTHORIZATION} header")
            try:
                authorization = request.headers[AUTHORIZATION]
                basic = BasicAuth.decode_from_authorization_header(authorization)
            except ValueError as e:
                raise HTTPBadRequest(reason=str(e))
            update_arguments.append(basic)
            continue

        # Request
        if issubclass(type_origin, Request):
            update_arguments.append(request)
            continue

        # HttpRequest
        if issubclass(type_origin, HttpRequest):
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
        if issubclass(type_origin, Session):
            if c.session not in request:
                raise HTTPUnauthorized(reason=f"Not exists {c.session}")
            update_arguments.append(request[c.session])
            continue

        # SessionEx
        if issubclass(type_origin, SessionEx):
            if c.session not in request:
                raise HTTPUnauthorized(reason=f"Not exists {c.session}")
            update_arguments.append(request[c.session])
            continue

        # Path
        if match_count >= 1 and key in request.match_info:
            update_arguments.append(request.match_info[key])
            match_count -= 1
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
                    logger.debug(f"BODY: {str(body)}")
                update_arguments.append(body)
                continue

        update_arguments.append(None)

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
) -> Response:
    now = datetime.utcnow().astimezone()

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
        result = await _parameter_matcher_main(func, obj, request)
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
    duration = (datetime.utcnow().astimezone() - now).total_seconds()
    response_info = f"{status} {reason} ({duration:.3f}s)"
    logger.info(f"{request_info} -> {response_info}")

    return result


def parameter_matcher():
    def _wrap(func):
        @wraps(func)
        async def __wrap(obj, request):
            return await parameter_matcher_main(func, obj, request)

        return __wrap

    return _wrap

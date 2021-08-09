# -*- coding: utf-8 -*-

from typing import List, Any, Optional, Set, get_origin
from inspect import signature, isclass, iscoroutinefunction
from functools import wraps
from datetime import datetime
from aiohttp.hdrs import AUTHORIZATION
from aiohttp.web_request import Request
from aiohttp.web_response import Response
from aiohttp.web_exceptions import (
    HTTPException,
    HTTPBadRequest,
    HTTPUnauthorized,
    HTTPInternalServerError,
)
from recc.session.session import Session
from recc.log.logging import recc_http_logger as logger
from recc.serializable.serialize import serialize_default
from recc.http.header.basic_auth import BasicAuth
from recc.http.http_payload import payload_to_object, request_payload_to_class
from recc.http.http_response import get_accept_type, get_encoding, create_response
from recc.http.http_session import HttpSession
from recc.http import http_cache_keys as c
from recc.access_control.abac.attributes import aa


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


def _test_permission(hs: HttpSession, acl: Set[aa]) -> None:
    for ac in acl:
        if ac == aa.HasAdmin:
            if not hs.user.is_admin:
                raise HTTPUnauthorized(reason="Administrator privileges are required")


async def _parameter_matcher_main(
    func,
    obj: Any,
    request: Request,
    acl: Optional[Set[aa]] = None,
) -> Response:
    accept = get_accept_type(request)
    encoding = get_encoding(request)

    sig = signature(func)
    keys = list(sig.parameters.keys())
    update_arguments: List[Any] = list()
    match_count = len(request.match_info)
    assign_body = False

    if acl:
        if c.http_session not in request:
            raise HTTPUnauthorized(reason=f"Not exists {c.http_session}")
        _test_permission(request[c.http_session], acl if acl else set())

    if len(keys) >= 2:
        for key in keys[1:]:
            param = sig.parameters[key]
            type_origin = get_origin(param.annotation)
            if type_origin is None:
                type_origin = param.annotation
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

            # Session
            if issubclass(type_origin, Session):
                if c.session not in request:
                    raise HTTPUnauthorized(reason=f"Not exists {c.session}")
                update_arguments.append(request[c.session])
                continue

            # HttpSession
            if issubclass(type_origin, HttpSession):
                if c.http_session not in request:
                    raise HTTPUnauthorized(reason=f"Not exists {c.http_session}")
                update_arguments.append(request[c.http_session])
                continue

            # Path
            if match_count >= 1 and key in request.match_info:
                update_arguments.append(request.match_info[key])
                match_count -= 1
                continue

            # Body
            if not assign_body:
                if _is_serializable_class(type_origin):
                    update_arguments.append(
                        payload_to_object(request.headers, await request.text())
                    )
                    assign_body = True
                    continue

                if isclass(type_origin):
                    body = await request_payload_to_class(request, type_origin)  # noqa
                    update_arguments.append(body)
                    assign_body = True
                    continue

            update_arguments.append(None)

    if iscoroutinefunction(func):
        result = await func(obj, *update_arguments)
    else:
        result = func(obj, *update_arguments)

    if result is None:
        return Response()
    elif isinstance(result, Response):
        return result
    elif _is_serializable_instance(result):
        return create_response(accept, encoding, result)
    elif isclass(type(result)):
        return create_response(accept, encoding, serialize_default(result))

    raise NotImplementedError


def parameter_matcher(acl: Optional[Set[aa]] = None):
    def _wrap(func):
        @wraps(func)
        async def __wrap(obj, request: Request) -> Response:
            now = datetime.utcnow()

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
                result = await _parameter_matcher_main(func, obj, request, acl)
            except HTTPException as e:
                logger.exception(e)
                raise e
            except PermissionError as e:
                logger.exception(e)
                reason = str(e)
                raise HTTPUnauthorized(reason=reason if reason else None)
            except BaseException as e:
                logger.exception(e)
                reason = str(e)
                raise HTTPInternalServerError(reason=reason if reason else None)
            else:
                status = result.status
                reason = result.reason
                duration = (datetime.utcnow() - now).total_seconds()
                logger.info(f"{request_info} -> {status} {reason} ({duration:.3f}s)")

            return result

        return __wrap

    return _wrap

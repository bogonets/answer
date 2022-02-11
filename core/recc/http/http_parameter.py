# -*- coding: utf-8 -*-

from pathlib import Path
from typing import Optional, Union, List, Any, get_args
from inspect import signature, isclass, iscoroutinefunction
from functools import wraps
from http import HTTPStatus

from aiohttp.hdrs import AUTHORIZATION
from aiohttp.web_request import Request
from aiohttp.web_response import StreamResponse
from aiohttp.web_response import Response
from aiohttp.web_fileresponse import FileResponse
from aiohttp.web_exceptions import (
    HTTPException,
    HTTPBadRequest,
    HTTPUnauthorized,
)

from recc.core.context import Context
from recc.chrono.datetime import today
from recc.inspect.type_origin import get_type_origin
from recc.session.session import Session
from recc.session.session_ex import SessionEx
from recc.logging.logging import recc_http_logger as logger
from recc.serialization.serialize import serialize_default
from recc.http.header.basic_auth import BasicAuth
from recc.http.header.bearer_auth import BearerAuth
from recc.http.http_decorator import object_to_permissions
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
from recc.variables.http import DEBUGGING_BODY_MSG_MAX_SIZE, VERY_VERBOSE_DEBUGGING
from recc.variables.annotation import ANNOTATION_PERMISSIONS, ANNOTATION_DOMAIN, Domain

_INTERNAL_SERVER_ERROR = HTTPStatus.INTERNAL_SERVER_ERROR


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


class HttpParameterMatcher:
    def __init__(
        self,
        func,
        bound_instance: Any,
        request: Request,
        *,
        group_path_key: Optional[str] = None,
        project_path_key: Optional[str] = None,
    ):
        self.func = func
        self.bound_instance = bound_instance
        self.request = request

        self.accept = get_accept_type(request)
        self.encoding = get_encoding(request)
        self.signature = signature(self.func)

        group_key = group_path_key if group_path_key else p.group
        project_key = project_path_key if project_path_key else p.project
        self.group_name: Optional[str] = request.match_info.get(group_key)
        self.project_name: Optional[str] = request.match_info.get(project_key)

        self.permissions: List[Union[int, str]] = list()
        if hasattr(self.func, ANNOTATION_PERMISSIONS):
            permissions = getattr(self.func, ANNOTATION_PERMISSIONS)
            for perm in object_to_permissions(permissions):
                self.permissions.append(perm)

        self.domain: Domain
        if hasattr(self.func, ANNOTATION_DOMAIN):
            domain = getattr(self.func, ANNOTATION_DOMAIN)
            if isinstance(domain, Domain):
                self.domain = domain
            else:
                raise RuntimeError(f"Unsupported domain type: {type(domain).__name__}")
        else:
            if self.group_name and self.project_name:
                self.domain = Domain.Project
            elif self.group_name and not self.project_name:
                self.domain = Domain.Group
            else:
                self.domain = Domain.Unknown

        self.very_verbose_debugging = False
        context = request[c.context] if c.context in request else None
        if context and isinstance(context, Context):
            config = context.config
            if config and config.developer and config.verbose >= VERY_VERBOSE_DEBUGGING:
                self.very_verbose_debugging = True
        else:
            context = None
        self.context: Optional[Context] = context

        self._assign_body = False

    async def verify_permissions(self):
        if not self.permissions:
            return  # No permissions required.

        if self.domain == Domain.Unknown:
            raise RuntimeError("Unknown domain")

        if not self.context:
            raise RuntimeError("The context does not exist")
        if c.session not in self.request:
            raise HTTPUnauthorized(reason=f"Not exists session: {c.session}")

        session = self.request[c.session]
        if not isinstance(session, SessionEx):
            raise RuntimeError(f"Unsupported session type: {type(session).__name__}")

        if self.domain == Domain.Group:
            await self.context.verify_group_permissions(
                session,
                self.group_name,
                self.permissions,
            )
        else:
            assert self.domain == Domain.Project
            await self.context.verify_project_permissions(
                session,
                self.group_name,
                self.project_name,
                self.permissions,
            )

    async def call(self):
        update_arguments = await self._get_arguments()

        if iscoroutinefunction(self.func):
            result = await self.func(*update_arguments)
        else:
            result = self.func(*update_arguments)

        if self.very_verbose_debugging:
            debugging_body = str(result)
            if len(debugging_body) >= DEBUGGING_BODY_MSG_MAX_SIZE:
                debugging_body = debugging_body[0:DEBUGGING_BODY_MSG_MAX_SIZE] + " ..."
            logger.debug(f"Response BODY: {debugging_body}")

        if result is None:
            return Response()
        elif isinstance(result, StreamResponse):
            return result
        elif isinstance(result, Path):
            return FileResponse(path=result)
        elif isinstance(result, HttpResponse):
            return Response(
                body=result.data,
                status=result.status if result.status else _INTERNAL_SERVER_ERROR,
                reason=result.reason,
                headers=result.headers,
            )
        # elif _is_serializable_instance(result):
        #     return create_response(self.accept, self.encoding, result)
        elif isclass(type(result)):
            return create_response(
                self.accept, self.encoding, serialize_default(result)
            )

        raise NotImplementedError

    async def _get_arguments(self) -> List[Any]:
        result: List[Any] = list()
        keys = list(self.signature.parameters.keys())
        if self.bound_instance is None:
            argument_keys = keys
        else:
            assert len(keys) >= 1
            result.append(self.bound_instance)  # [0] is class instance. maybe 'self'
            argument_keys = keys[1:]

        for key in argument_keys:
            result.append(await self._get_argument(key))

        return result

    async def _get_argument(self, key: str) -> Any:
        param = self.signature.parameters[key]

        type_origin = get_type_origin(param)
        type_args = get_args(param.annotation)

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

        # param.kind
        #  - POSITIONAL_ONLY
        #  - POSITIONAL_OR_KEYWORD
        #  - VAR_POSITIONAL
        #  - KEYWORD_ONLY
        #  - VAR_KEYWORD

        # BasicAuth
        if is_subclass_safe(type_origin, BasicAuth):
            if AUTHORIZATION not in self.request.headers:
                raise HTTPBadRequest(reason=f"Not exists {AUTHORIZATION} header")
            try:
                authorization = self.request.headers[AUTHORIZATION]
                return BasicAuth.decode_from_authorization_header(authorization)
            except ValueError as e:
                raise HTTPBadRequest(reason=str(e))

        # BearerAuth
        if is_subclass_safe(type_origin, BearerAuth):
            if AUTHORIZATION not in self.request.headers:
                raise HTTPBadRequest(reason=f"Not exists {AUTHORIZATION} header")
            try:
                authorization = self.request.headers[AUTHORIZATION]
                return BearerAuth.decode_from_authorization_header(authorization)
            except ValueError as e:
                raise HTTPBadRequest(reason=str(e))

        # Request
        if is_subclass_safe(type_origin, Request):
            return self.request

        # HttpRequest
        if is_subclass_safe(type_origin, HttpRequest):
            return HttpRequest(
                method=self.request.method,
                path=self.request.path,
                data=await self.request.read(),
                headers=self.request.headers,
            )

        # Session
        if is_subclass_safe(type_origin, Session):
            if c.session in self.request:
                return self.request[c.session]
            else:
                raise HTTPUnauthorized(reason=f"Not exists {c.session}")

        # SessionEx
        if is_subclass_safe(type_origin, SessionEx):
            if c.session in self.request:
                return self.request[c.session]
            else:
                raise HTTPUnauthorized(reason=f"Not exists {c.session}")

        # Path
        if is_path_class(type_origin) and key in self.request.match_info:
            path_value = self.request.match_info[key]
            try:
                path_arg = cast_builtin_type_from_string(path_value, type_origin)
                return path_arg
            except ValueError:
                logger.debug(f"Type casting error for path parameter: {key}")
                return path_value

        # Query
        if optional_parameter is not None:
            if key in self.request.rel_url.query:
                query_value = self.request.rel_url.query[key]
                try:
                    query_arg = cast_builtin_type_from_string(
                        query_value, optional_parameter
                    )
                    return query_arg
                except ValueError:
                    logger.debug(f"Type casting error for query parameter: {key}")
                    return query_value
            else:
                return None

        # Body
        if not self._assign_body:
            if _is_serializable_class(type_origin):
                body = payload_to_object(
                    self.request.headers,
                    await self.request.text(),
                )
                self._assign_body = True
            elif isclass(type_origin):
                body = await request_payload_to_class(self.request, type_origin)  # noqa
                self._assign_body = True
            else:
                body = None

            if self._assign_body:
                assert body is not None
                if self.very_verbose_debugging:
                    logger.debug(f"Request BODY: {str(body)}")
                return body

        return None


async def parameter_matcher_main(
    func,
    bound_instance: Any,
    request: Request,
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
        matcher = HttpParameterMatcher(func, bound_instance, request)
        await matcher.verify_permissions()
        result = await matcher.call()
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


def parameter_matcher(func):
    @wraps(func)
    async def _wrap(bound_instance, request):
        return await parameter_matcher_main(func, bound_instance, request)

    return _wrap

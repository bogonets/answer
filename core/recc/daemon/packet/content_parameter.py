# -*- coding: utf-8 -*-

from collections import deque
from inspect import iscoroutinefunction, signature
from multiprocessing.shared_memory import SharedMemory
from typing import (
    Any,
    Deque,
    Dict,
    Iterable,
    List,
    Mapping,
    NamedTuple,
    Optional,
    Union,
)

from numpy import ndarray
from type_serialize import ByteCoding
from type_serialize import decode as byte_decode
from type_serialize import encode as byte_encode
from type_serialize.driver.numpy import ndarray_to_bytes

from recc.conversion.to_boolean import string_to_boolean
from recc.daemon.packet.content_helper import has_array, has_shared_memory
from recc.inspect.type_origin import get_type_origin
from recc.logging.logging import recc_daemon_logger as logger
from recc.proto.daemon.daemon_api_pb2 import ArrayInfo, Content


def _is_path_class(obj) -> bool:
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


def _cast_builtin_type_from_string(data: str, cls) -> Any:
    assert isinstance(cls, type)
    if issubclass(cls, str):
        return data
    elif issubclass(cls, int):
        return int(data)
    elif issubclass(cls, float):
        return float(data)
    elif issubclass(cls, bool):
        return string_to_boolean(data)
    return cls(data)  # type: ignore[call-arg]


class ResultTuple(NamedTuple):
    args: List[Content]
    kwargs: Dict[str, Content]


class ContentParameterMatcher:

    _args: Deque[Content]
    _kwargs: Dict[str, Content]
    _sm_names: Deque[str]

    def __init__(
        self,
        func,
        match_info: Dict[str, str],
        coding: ByteCoding,
        encoding: str,
        compress_level: int,
        args: Iterable[Content],
        kwargs: Mapping[str, Content],
        sm_names: Iterable[str],
    ):
        self._func = func
        self._match_info = match_info
        self._coding = coding
        self._encoding = encoding
        self._compress_level = compress_level
        self._signature = signature(func)
        self._args = deque(args)
        self._kwargs = dict(kwargs)
        self._sm_names = deque(sm_names)

    async def call(self) -> ResultTuple:
        update_arguments = self._get_arguments()

        try:
            if iscoroutinefunction(self._func):
                result = await self._func(*update_arguments)
            else:
                result = self._func(*update_arguments)
        except BaseException as e:
            raise RuntimeError("A runtime error occurred in the route") from e

        result_args: List[Any] = list()
        result_kwargs: Dict[str, Any] = dict()

        if result is None:
            pass
        elif isinstance(result, list):
            result_args = result
        elif isinstance(result, dict):
            result_kwargs = result
        elif isinstance(result, Mapping):
            result_kwargs = {k: v for k, v in result.items()}
        elif isinstance(result, (tuple, set)):
            result_args = list(result)
        else:
            result_args = [result]

        return ResultTuple(
            args=self._args_to_contents(*result_args),
            kwargs=self._kwargs_to_contents(**result_kwargs),
        )

    def _get_arguments(self) -> List[Any]:
        return [self._get_argument(key) for key in self._signature.parameters.keys()]

    def _get_argument(self, key: str) -> Any:
        param = self._signature.parameters[key]

        type_origin = get_type_origin(param)
        assert type_origin is not None
        assert isinstance(type_origin, type) or type_origin is Union

        # param.kind
        #  - POSITIONAL_ONLY
        #  - POSITIONAL_OR_KEYWORD
        #  - VAR_POSITIONAL
        #  - KEYWORD_ONLY
        #  - VAR_KEYWORD

        # Path
        if _is_path_class(type_origin) and key in self._match_info:
            path_value = self._match_info[key]
            try:
                return _cast_builtin_type_from_string(path_value, type_origin)
            except ValueError:
                logger.debug(f"Type casting error for path parameter: {key}")
                return path_value

        # Keyword arguments
        if key in self._kwargs:
            return self._content_to_any(self._kwargs[key], type_origin)

        # Positional arguments
        if self._args:
            return self._content_to_any(self._args.popleft(), type_origin)

        return None

    def _content_to_any(self, content: Content, cls: Optional[Any] = None) -> Any:
        if has_shared_memory(content):
            sm = SharedMemory(name=content.sm_name)
            try:
                size = content.size
                data = bytes(sm.buf[:size])
            finally:
                sm.close()
        else:
            data = content.data

        if has_array(content):
            return ndarray(
                shape=content.array.shape,
                dtype=content.array.dtype,
                buffer=data,
                strides=content.array.strides,
            )
        else:
            return byte_decode(data=data, cls=cls, coding=self._coding)

    def _object_to_content(self, obj: Any) -> Content:
        buffer = byte_encode(data=obj, level=self._compress_level, coding=self._coding)
        size = len(buffer)

        if self._sm_names and buffer:
            data = bytes()
            sm_name = self._sm_names.popleft()
            sm = SharedMemory(name=sm_name)
            try:
                sm.buf[:size] = buffer
            finally:
                sm.close()
        else:
            data = buffer
            sm_name = None

        return Content(size=size, data=data, sm_name=sm_name)

    def _array_to_content(self, array: ndarray) -> Content:
        buffer = ndarray_to_bytes(array)
        size = len(buffer)

        if self._sm_names and buffer:
            data = bytes()
            sm_name = self._sm_names.popleft()
            sm = SharedMemory(name=sm_name)
            try:
                sm.buf[:size] = buffer
            finally:
                sm.close()
        else:
            data = buffer
            sm_name = None

        return Content(
            size=size,
            data=data,
            sm_name=sm_name,
            array=ArrayInfo(
                shape=array.shape,
                dtype=array.dtype.name,
                strides=array.strides,
            ),
        )

    def _any_to_content(self, obj: Any) -> Content:
        if isinstance(obj, ndarray):
            return self._array_to_content(obj)
        else:
            return self._object_to_content(obj)

    def _args_to_contents(self, *args: Any) -> List[Content]:
        return [self._any_to_content(o) for o in args]

    def _kwargs_to_contents(self, **kwargs: Any) -> Dict[str, Content]:
        return {k: self._any_to_content(o) for k, o in kwargs.items()}


async def call_router(
    func,
    match_info: Dict[str, str],
    coding: ByteCoding,
    encoding: str,
    compress_level: int,
    args: Iterable[Content],
    kwargs: Mapping[str, Content],
    sm_names: Iterable[str],
):
    matcher = ContentParameterMatcher(
        func=func,
        match_info=match_info,
        coding=coding,
        encoding=encoding,
        compress_level=compress_level,
        args=args,
        kwargs=kwargs,
        sm_names=sm_names,
    )
    return await matcher.call()

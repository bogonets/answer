# -*- coding: utf-8 -*-

from typing import Optional, Iterable, Mapping, Any, List, Dict, NamedTuple, Set
from numpy import ndarray
from recc.memory.shared_memory_queue import SharedMemoryQueue
from recc.proto.daemon.daemon_api_pb2 import Content, ArrayInfo
from recc.serialization.numpy import ndarray_to_bytes
from recc.serialization.byte_coding import encode as byte_encode
from recc.serialization.byte_coding import ByteCodingType


class PackedTuple(NamedTuple):
    args: List[Content]
    kwargs: Dict[str, Content]


class ContentPacker:

    _coding: ByteCodingType
    _compress_level: int
    _args: List[Any]
    _kwargs: Dict[str, Any]
    _smq: Optional[SharedMemoryQueue]
    _written_sm_names: Set[str]

    def __init__(
        self,
        coding: ByteCodingType,
        compress_level: int,
        args: Optional[Iterable[Any]] = None,
        kwargs: Optional[Mapping[str, Any]] = None,
        smq: Optional[SharedMemoryQueue] = None,
    ):
        self._coding = coding
        self._compress_level = compress_level
        self._args = list(args) if args else list()
        self._kwargs = dict(kwargs) if kwargs else dict()
        self._smq = smq
        self._written_sm_names = set()

    def restore(self) -> None:
        if not self._smq:
            return
        for name in self._written_sm_names:
            self._smq.restore(name)
        self._written_sm_names.clear()

    def object_to_content(self, obj: Any) -> Content:
        buffer = byte_encode(
            data=obj,
            coding=self._coding,
            level=self._compress_level,
        )

        if self._smq and buffer:
            written = self._smq.write(buffer)
            sm_name = written.sm_name
            self._written_sm_names.add(sm_name)
            data = bytes()
            size = written.size
        else:
            sm_name = None
            data = buffer
            size = len(buffer)

        return Content(
            size=size,
            data=data,
            sm_name=sm_name,
        )

    def array_to_content(self, array: ndarray) -> Content:
        buffer = ndarray_to_bytes(array)
        assert isinstance(buffer, bytes)

        if self._smq and buffer:
            written = self._smq.write(buffer)
            sm_name = written.sm_name
            self._written_sm_names.add(sm_name)
            data = bytes()
            size = written.size
        else:
            sm_name = None
            data = buffer
            size = len(buffer)

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

    def any_to_content(self, obj: Any) -> Content:
        if isinstance(obj, ndarray):
            return self.array_to_content(obj)
        else:
            return self.object_to_content(obj)

    def args_to_contents(self) -> List[Content]:
        return [self.any_to_content(o) for o in self._args]

    def kwargs_to_contents(self) -> Dict[str, Content]:
        return {k: self.any_to_content(o) for k, o in self._kwargs.items()}

    def __enter__(self) -> PackedTuple:
        args = self.args_to_contents()
        kwargs = self.kwargs_to_contents()
        return PackedTuple(args=args, kwargs=kwargs)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.restore()

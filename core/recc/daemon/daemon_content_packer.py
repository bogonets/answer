# -*- coding: utf-8 -*-

from typing import Optional, Iterable, Mapping, Any, List, Dict, NamedTuple
from numpy import ndarray
from recc.memory.shared_memory_queue import SharedMemoryQueue
from recc.daemon.daemon_content import DaemonContent
from recc.proto.daemon.daemon_api_pb2 import Content
from recc.serialization.numpy import ndarray_to_bytes
from recc.serialization.byte_coding import encode as byte_encode
from recc.serialization.byte_coding import ByteCodingType


class PackedTuple(NamedTuple):
    args: List[Content]
    kwargs: Dict[str, Content]


class DaemonContentPacker:

    _coding: ByteCodingType
    _compress_level: int

    _args: Iterable[Any]
    _kwargs: Mapping[str, Any]
    _smq: Optional[SharedMemoryQueue]
    _smq_names: List[str]

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
        self._args = args if args else list()
        self._kwargs = kwargs if kwargs else dict()
        self._smq = smq
        self._smq_names = list()

    def restore(self) -> None:
        if not self._smq:
            return

        for name in self._smq_names:
            self._smq.restore(name)
        self._smq_names.clear()

    def object_to_daemon_content(self, obj: Any) -> DaemonContent:
        buffer = byte_encode(
            data=obj,
            coding=self._coding,
            level=self._compress_level,
        )

        if self._smq and buffer:
            written = self._smq.write(buffer)
            sm_name = written.sm_name
            self._smq_names.append(sm_name)
            data = bytes()
            size = written.size
        else:
            sm_name = None
            data = buffer
            size = len(buffer)

        return DaemonContent(size=size, data=data, sm_name=sm_name)

    def array_to_daemon_content(self, array: ndarray) -> DaemonContent:
        buffer = ndarray_to_bytes(array)

        if self._smq and buffer:
            written = self._smq.write(buffer)
            sm_name = written.sm_name
            self._smq_names.append(sm_name)
            data = bytes()
            size = written.size
        else:
            sm_name = None
            data = buffer
            size = len(buffer)

        return DaemonContent(
            size=size,
            data=data,
            sm_name=sm_name,
            shape=array.shape,
            dtype=array.dtype.name,
            strides=array.strides,
        )

    def any_to_daemon_content(self, obj: Any) -> DaemonContent:
        if isinstance(obj, ndarray):
            return self.array_to_daemon_content(obj)
        else:
            return self.object_to_daemon_content(obj)

    def args_to_daemon_contents(self) -> List[DaemonContent]:
        return [self.any_to_daemon_content(o) for o in self._args]

    def kwargs_to_daemon_contents(self) -> Dict[str, DaemonContent]:
        return {k: self.any_to_daemon_content(o) for k, o in self._kwargs.items()}

    def args_to_contents(self) -> List[Content]:
        return [o.to_api() for o in self.args_to_daemon_contents()]

    def kwargs_to_contents(self) -> Dict[str, Content]:
        return {k: o.to_api() for k, o in self.kwargs_to_daemon_contents().items()}

    def __enter__(self) -> PackedTuple:
        return PackedTuple(
            args=self.args_to_contents(),
            kwargs=self.kwargs_to_contents(),
        )

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.restore()

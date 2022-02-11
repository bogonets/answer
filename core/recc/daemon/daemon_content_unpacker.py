# -*- coding: utf-8 -*-

from typing import Optional, Iterable, Mapping, Any, List, Dict
from numpy import ndarray
from multiprocessing.shared_memory import SharedMemory
from recc.daemon.daemon_content import DaemonContent
from recc.daemon.daemon_answer import DaemonAnswer
from recc.proto.daemon.daemon_api_pb2 import Content
from recc.serialization.byte_coding import bytes_to_object
from recc.serialization.byte_coding import ByteCodingType


class DaemonContentUnpacker:

    _coding: ByteCodingType
    _encoding: str

    _args: List[Content]
    _kwargs: Dict[str, Content]
    _sms: Dict[str, SharedMemory]

    def __init__(
        self,
        coding: ByteCodingType,
        encoding: str,
        args: Optional[Iterable[Content]] = None,
        kwargs: Optional[Mapping[str, Content]] = None,
        sms: Optional[Mapping[str, SharedMemory]] = None,
    ):
        self._coding = coding
        self._encoding = encoding

        self._args = list(args) if args else list()
        self._kwargs = dict(kwargs) if kwargs else dict()
        self._sms = dict(sms) if sms else dict()

    def content_to_any(self, content: Content) -> Any:
        daemon_content = DaemonContent.from_api(content)

        if daemon_content.is_sm:
            if not self._sms:
                raise ValueError("The shared-memory-list does not exist")
            if daemon_content.sm_name not in self._sms:
                raise IndexError(
                    f"The shared-memory('{daemon_content.sm_name}') does not exist"
                )
            size = daemon_content.size
            data = bytes(self._sms[daemon_content.sm_name].buf[:size])
        else:
            data = daemon_content.data

        if daemon_content.is_array:
            return ndarray(
                shape=daemon_content.shape,
                dtype=daemon_content.dtype,
                buffer=data,
                strides=daemon_content.strides,
            )
        else:
            return bytes_to_object(
                data=data,
                coding=self._coding,
                encoding=self._encoding,
            )

    def args_to_anys(self) -> List[Any]:
        return [self.content_to_any(arg) for arg in self._args]

    def kwargs_to_anys(self) -> Dict[str, Any]:
        return {key: self.content_to_any(arg) for key, arg in self._kwargs.items()}

    def unpack(self) -> DaemonAnswer:
        args = self.args_to_anys()
        kwargs = self.kwargs_to_anys()
        return DaemonAnswer(*args, **kwargs)


def content_unpack(
    coding: ByteCodingType,
    encoding: str,
    args: Optional[Iterable[Content]] = None,
    kwargs: Optional[Mapping[str, Content]] = None,
    sms: Optional[Mapping[str, SharedMemory]] = None,
) -> DaemonAnswer:
    unpacker = DaemonContentUnpacker(
        coding=coding,
        encoding=encoding,
        args=args,
        kwargs=kwargs,
        sms=sms,
    )
    return unpacker.unpack()

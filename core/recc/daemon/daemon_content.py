# -*- coding: utf-8 -*-

from typing import Optional, List, Iterable
from recc.proto.daemon.daemon_api_pb2 import ArrayInfo, Content


class DaemonContent:

    size: int
    data: bytes
    sm_name: Optional[str]
    shape: Optional[List[int]]
    dtype: Optional[str]
    strides: Optional[List[int]]

    def __init__(
        self,
        size: int,
        data: bytes,
        sm_name: Optional[str] = None,
        shape: Optional[Iterable[int]] = None,
        dtype: Optional[str] = None,
        strides: Optional[Iterable[int]] = None,
    ):
        self.size = size
        self.data = data
        self.sm_name = sm_name

        if shape and dtype and strides:
            self.shape = list(shape)
            self.dtype = dtype
            self.strides = list(strides)
        else:
            self.shape = None
            self.dtype = None
            self.strides = None

    @classmethod
    def from_api(cls, content: Content):
        if content.array:
            shape = content.array.shape
            dtype = content.array.dtype
            strides = content.array.strides
        else:
            shape = None
            dtype = None
            strides = None

        return cls(
            size=content.size,
            data=content.data,
            sm_name=content.sm_name,
            shape=shape,
            dtype=dtype,
            strides=strides,
        )

    @property
    def is_array(self) -> bool:
        return bool(self.shape) and bool(self.dtype) and bool(self.strides)

    @property
    def is_sm(self) -> bool:
        return bool(self.sm_name) and self.size >= 1

    def to_array_info(self) -> Optional[ArrayInfo]:
        if self.is_array:
            return ArrayInfo(
                shape=self.shape,
                dtype=self.dtype if self.dtype else str(),
                strides=self.strides,
            )
        else:
            return None

    def to_api(self) -> Content:
        return Content(
            size=self.size,
            data=self.data,
            sm_name=self.sm_name,
            array=self.to_array_info(),
        )

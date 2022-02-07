# -*- coding: utf-8 -*-

import sys
import numpy as np
from typing import List
from dataclasses import dataclass


def _ndarray_to_bytes_by_darwin(array: np.ndarray) -> bytes:
    return array.tobytes()


def _ndarray_to_bytes(array: np.ndarray) -> bytes:
    """
    .. warning::
        The following error may occur during serialization:
        'multi-dimensional sub-views are not implemented'
    """

    if array.flags["C_CONTIGUOUS"]:
        return array.data
    else:
        return array.tobytes()


if sys.platform == "darwin":
    ndarray_to_bytes = _ndarray_to_bytes_by_darwin
else:
    ndarray_to_bytes = _ndarray_to_bytes


@dataclass
class NumpyProto:

    shape: List[int]
    dtype_name: str
    buffer: bytes
    strides: List[int]

    def to_array(self) -> np.ndarray:
        try:
            dtype = np.dtype(self.dtype_name)
        except:  # noqa
            raise ValueError(f"Unsupported dtype name: {self.dtype_name}")
        return np.ndarray(
            shape=self.shape,
            dtype=dtype,
            buffer=self.buffer,
            strides=self.strides,
        )

    @classmethod
    def from_array(cls, array: np.ndarray):
        try:
            np.dtype(array.dtype.name)
        except:  # noqa
            raise ValueError(f"Unsupported dtype name: {array.dtype.name}")
        return cls(
            shape=list(array.shape),
            dtype_name=array.dtype.name,
            # buffer=ndarray_to_bytes(array),
            buffer=array.tobytes(),
            strides=list(array.strides),
        )

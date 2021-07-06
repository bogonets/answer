# -*- coding: utf-8 -*-
# @see <https://docs.scipy.org/doc/numpy-1.13.0/user/basics.types.html>

import numpy as np


DTYPE_NAME_TO_TYPE = {
    "int8": np.int8,
    "int16": np.int16,
    "int32": np.int32,
    "int64": np.int64,
    "uint8": np.uint8,
    "uint16": np.uint16,
    "uint32": np.uint32,
    "uint64": np.uint64,
    "float32": np.float32,
    "float64": np.float64,
}
DTYPE_TYPE_TO_NAME = {v: k for k, v in DTYPE_NAME_TO_TYPE.items()}

shape = (0,)
dtype = np.int32


def on_set(key, val):
    if key == "shape":
        global shape
        shape = list(map(lambda x: int(x), str(val).split(",")))
    elif key == "dtype":
        global dtype
        dtype = DTYPE_NAME_TO_TYPE[val]


def on_get(key):
    if key == "shape":
        return ",".join(list(map(lambda x: str(x), shape)))
    elif key == "dtype":
        return DTYPE_TYPE_TO_NAME[dtype]


def on_run():
    return {"result": np.zeros(shape, dtype)}


if __name__ == "__main__":
    pass

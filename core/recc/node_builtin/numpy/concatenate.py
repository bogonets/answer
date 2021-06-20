# -*- coding: utf-8 -*-
# @see <https://numpy.org/doc/stable/reference/generated/numpy.concatenate.html>

import numpy as np

axis = 0


def on_set(key, val):
    if key == "axis":
        global axis
        axis = int(val)


def on_get(key):
    if key == "axis":
        return axis


def on_run(array1: np.ndarray, array2: np.ndarray):
    if axis >= 0:
        return {"result": np.concatenate((array1, array2), axis=axis)}
    else:
        return {"result": np.concatenate((array1, array2))}


if __name__ == "__main__":
    pass

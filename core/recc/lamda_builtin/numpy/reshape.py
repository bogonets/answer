# -*- coding: utf-8 -*-
# https://numpy.org/doc/stable/reference/generated/numpy.reshape.html

import numpy as np

ORDER_NAMES = ["K", "A", "C", "F"]

newshape = (0,)
order = "K"


def on_set(key, val):
    if key == "newshape":
        global newshape
        newshape = list(map(lambda x: int(x), str(val).split(",")))
    elif key == "order":
        global order
        order = val
        assert order in ORDER_NAMES


def on_get(key):
    if key == "newshape":
        return ",".join(list(map(lambda x: str(x), newshape)))
    elif key == "order":
        return order


def on_run(array):
    return {"result": np.reshape(array, newshape, order=order)}


if __name__ == "__main__":
    pass

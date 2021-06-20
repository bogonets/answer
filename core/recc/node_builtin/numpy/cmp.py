# -*- coding: utf-8 -*-

import numpy as np

METHOD_EQ = "=="
METHOD_NE = "!="
METHOD_GE = ">="
METHOD_LE = "<="
METHOD_GT = ">"
METHOD_LT = "<"

method = METHOD_EQ


def on_set(key, val):
    if key == "method":
        global method
        method = val


def on_get(key):
    if key == "method":
        return method


def on_run(left: np.ndarray, right: np.ndarray):
    if method == METHOD_EQ:
        return {"result": left == right}
    elif method == METHOD_NE:
        return {"result": left != right}
    elif method == METHOD_GE:
        return {"result": left >= right}
    elif method == METHOD_LE:
        return {"result": left <= right}
    elif method == METHOD_GT:
        return {"result": left > right}
    elif method == METHOD_LT:
        return {"result": left < right}
    else:
        raise ValueError(f"Unknown `method` property: {method}")

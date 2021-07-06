# -*- coding: utf-8 -*-
# @see <https://docs.scipy.org/doc/numpy-1.13.0/user/basics.types.html>

# import numpy as np

slices = list()


def int_or_none(val):
    return int(val) if val else None


def str_to_slice(val):
    result = list()
    for s in str(val).split(":"):
        result.append(int_or_none(s))
    return result


def str_to_slices(val):
    result = list()
    for s in str(val).split(","):
        result.append(str_to_slice(s))
    return result


def slice_to_str(val):
    if len(val) == 0:
        return "::"
    elif len(val) == 1:
        return str(val[0])
    elif len(val) == 2:
        return f"{val[0]}:{val[1]}"
    elif len(val) == 3:
        return ",".join(val)
    else:
        raise IndexError("A slice must have 3 or fewer elements.")


def slices_to_str(val):
    ",".join(list(slice_to_str(x) for x in val))


def on_set(key, val):
    if key == "slices":
        global slices
        slices = str_to_slices(val)


def on_get(key):
    if key == "slices":
        return slices_to_str(slices)


def on_run(array):
    return {"result": array[slices]}


if __name__ == "__main__":
    pass

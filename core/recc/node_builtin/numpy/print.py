# -*- coding: utf-8 -*-

import numpy as np
import sys

FILE_STDOUT = "stdout"
FILE_STDERR = "stderr"
FILES = [FILE_STDOUT, FILE_STDERR]

FILE_NAME_TO_TYPE = {
    "stdout": 1,
    "stderr": 2,
}
FILE_TYPE_TO_NAME = {v: k for k, v in FILE_NAME_TO_TYPE.items()}

file = 1
flush = True
prefix = ""
suffix = ""


def on_set(key, val):
    if key == "file":
        global file
        file = FILE_NAME_TO_TYPE[val]
    elif key == "flush":
        global flush
        flush = str(val).lower() in ["true", "yes", "y"]
    elif key == "prefix":
        global prefix
        prefix = val
    elif key == "suffix":
        global suffix
        suffix = val


def on_get(key):
    if key == "file":
        return FILE_TYPE_TO_NAME[file]
    elif key == "flush":
        return flush
    elif key == "prefix":
        return prefix
    elif key == "suffix":
        return suffix


def on_run(array: np.ndarray):
    if file == 1:
        sys.stdout.write(prefix + str(array) + suffix)
        if flush:
            sys.stdout.flush()
    elif file == 2:
        sys.stderr.write(prefix + str(array) + suffix)
        if flush:
            sys.stderr.flush()


if __name__ == "__main__":
    pass

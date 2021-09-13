# -*- coding: utf-8 -*-

from importlib import import_module


def get_annotations_compiler_flag() -> int:
    future = import_module("__future__")
    assert future is not None
    annotations = getattr(future, "annotations")
    assert annotations is not None
    compiler_flag = getattr(annotations, "compiler_flag")
    assert isinstance(compiler_flag, int)
    return compiler_flag

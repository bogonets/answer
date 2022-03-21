# -*- coding: utf-8 -*-

import os
from functools import lru_cache


@lru_cache
def detect_pydevd() -> bool:
    return "PYDEVD_LOAD_VALUES_ASYNC" in os.environ


@lru_cache
def get_isolate_ensure_pip_flag() -> bool:
    """
    .. warning::
        If pydevd is connected,
        the ``python -Im ensure_pip`` command does not work properly.
    """
    return not detect_pydevd()

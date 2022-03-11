# -*- coding: utf-8 -*-

import sys


def is_debugging_mode() -> bool:
    """
    Return if the debugger is currently active
    """

    get_trace = getattr(sys, "gettrace", lambda: None)
    return get_trace() is not None

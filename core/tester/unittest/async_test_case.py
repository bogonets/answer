# -*- coding: utf-8 -*-

import functools
from asyncio import (
    AbstractEventLoop,
    get_event_loop,
    new_event_loop,
    set_event_loop,
    iscoroutinefunction,
)
from unittest import TestCase
from typing import Callable

COROUTINE_FUNCTION_ALLOWS = ["setUp", "tearDown"]
TEST_FUNCTION_PREFIX = "test_"


def _async_to_sync_decorator(func: Callable, loop: AbstractEventLoop):
    """Sync function for calling async function.

    .. deprecated::
        Returning as `FunctionTypes` causes pytest's unit tests to fail.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return loop.run_until_complete(func(*args, **kwargs))

    return wrapper


def _get_default_loop(debug=True) -> AbstractEventLoop:
    loop: AbstractEventLoop
    try:
        loop = get_event_loop()
    except:  # noqa
        loop = new_event_loop()
        set_event_loop(loop)
    loop.set_debug(debug)
    return loop


class AsyncTestCase(TestCase):

    # We need to pick a loop for entire testing phase,
    # otherwise it will trigger create new loops in new threads,
    # leads to deadlock.
    _test_loop = _get_default_loop()

    def __init__(self, method_name="runTest"):
        super().__init__(method_name)

    @property
    def loop(self) -> AbstractEventLoop:
        return self._test_loop

    def set_debug(self, flag=True) -> None:
        self._test_loop.set_debug(flag)

    def disable_debug(self) -> None:
        self._test_loop.set_debug(False)

    @staticmethod
    def mangling_tester_name(name: str) -> str:
        return "__async_backend_" + name

    def exist_mangled_tester(self, name: str) -> bool:
        mangled_tester_name = self.mangling_tester_name(name)
        try:
            return super().__getattribute__(mangled_tester_name) is not None
        except AttributeError:
            return False

    def __getattribute__(self, name: str):
        """Overrides the loading logic to support coroutine functions."""
        attr = super().__getattribute__(name)

        # If possible, converts the coroutine into a sync function.
        if name.startswith(TEST_FUNCTION_PREFIX) or name in COROUTINE_FUNCTION_ALLOWS:
            if iscoroutinefunction(attr):

                class _Runner:
                    def __init__(self, loop: AbstractEventLoop, func):
                        self.loop = loop
                        self.func = func

                    def _runner(self):
                        self.loop.run_until_complete(self.func())

                # Returning as `FunctionTypes` causes pytest's unit tests to fail.
                return _Runner(self.loop, attr)._runner

        # For other attributes, let them pass.
        return attr

# -*- coding: utf-8 -*-

import os
import builtins
import site
from importlib.machinery import BuiltinImporter
from typing import Optional, Any, Dict
from inspect import iscoroutinefunction
from aiohttp.web_request import Request
from aiohttp.web_response import Response

DEFAULT_MODULE_NAME = "__recc_plugin__"
DEFAULT_FILENAME = "<ReccPlugin>"
COMPILE_MODE_EXEC = "exec"

OPTIMIZE_DEFAULT = -1
OPTIMIZE_LEVEL0 = 0  # no optimization, __debug__ is true
OPTIMIZE_LEVEL1 = 1  # asserts are removed, __debug__ is false
OPTIMIZE_LEVEL2 = 2  # docstrings are removed too

PYTHON_PLUGIN_SOURCE_PREFIX = """# -*- coding: utf-8 -*-
import sys
import os
import signal
if {ignore_interrupt_signal}:
    signal.signal(signal.SIGINT, signal.SIG_IGN)
if "{site_packages}":
    sys.path.insert(0, "{site_packages}")
"""

NAME_ON_SETUP = "on_setup"
NAME_ON_TEARDOWN = "on_teardown"
NAME_ON_REQUEST = "on_request"

PLUGIN_INFORMATION_KEY_NAME = "name"


class Plugin:
    def __init__(self, path: str):
        self._path = path
        with open(path, "r") as f:
            self._source = f.read()
        self._source_ast = compile(self._source, path, COMPILE_MODE_EXEC)
        self._global_variables: Dict[str, Any] = {
            "__name__": DEFAULT_MODULE_NAME,
            "__file__": path,
            "__doc__": "",
            "__loader__": type(BuiltinImporter),
            "__builtins__": builtins,
        }
        local_variables: Dict[str, Any] = dict()

        try:
            site_packages = site.getsitepackages()[0]
        except:  # noqa
            site_packages = str()

        source_prefix = PYTHON_PLUGIN_SOURCE_PREFIX.format(
            ignore_interrupt_signal=True,
            site_packages=site_packages,
        )
        exec(source_prefix, self._global_variables, local_variables)

        exec(self._source_ast, self._global_variables, local_variables)
        self._global_variables.update(local_variables)
        self._name = ""

    @property
    def name(self) -> str:
        return self._name

    def exists_setup(self) -> bool:
        return NAME_ON_SETUP in self._global_variables

    def exists_teardown(self) -> bool:
        return NAME_ON_TEARDOWN in self._global_variables

    def exists_request(self) -> bool:
        return NAME_ON_REQUEST in self._global_variables

    def parse_plugin_name(self, info: Optional[Dict[str, Any]]) -> str:
        if info:
            if isinstance(info, str):
                return info
            elif isinstance(info, dict):
                return str(info.get(PLUGIN_INFORMATION_KEY_NAME))
        return os.path.split(self._path)[1]

    async def call_setup(self, context: Any) -> None:
        on_setup = self._global_variables.get(NAME_ON_SETUP)
        assert on_setup is not None
        if iscoroutinefunction(on_setup):
            result = await on_setup(context)
        else:
            result = on_setup(context)
        self._name = self.parse_plugin_name(result)

    async def call_teardown(self) -> None:
        on_teardown = self._global_variables.get(NAME_ON_TEARDOWN)
        assert on_teardown is not None
        if iscoroutinefunction(on_teardown):
            await on_teardown()
        else:
            on_teardown()

    async def call_request(self, request: Request) -> Response:
        on_request = self._global_variables.get(NAME_ON_REQUEST)
        assert on_request is not None
        if iscoroutinefunction(on_request):
            return await on_request(request)
        else:
            return on_request(request)

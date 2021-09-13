# -*- coding: utf-8 -*-

import os
import builtins
from importlib.machinery import BuiltinImporter
from typing import Optional, Any, Dict
from inspect import iscoroutinefunction
from aiohttp.web_request import Request
from aiohttp.web_response import Response
from recc.compile.future import get_annotations_compiler_flag

DEFAULT_MODULE_NAME = "__recc_plugin__"
DEFAULT_FILENAME = "<ReccPlugin>"
COMPILE_MODE_EXEC = "exec"
COMPILE_FLAGS = get_annotations_compiler_flag()

OPTIMIZE_DEFAULT = -1
OPTIMIZE_LEVEL0 = 0  # no optimization, __debug__ is true
OPTIMIZE_LEVEL1 = 1  # asserts are removed, __debug__ is false
OPTIMIZE_LEVEL2 = 2  # docstrings are removed too

NAME_ON_SETUP = "on_setup"
NAME_ON_TEARDOWN = "on_teardown"
NAME_ON_REQUEST = "on_request"

PLUGIN_INFORMATION_KEY_NAME = "name"


def run_python_plugin(path: str) -> Dict[str, Any]:
    with open(path, "r") as f:
        source = f.read()

    global_variables: Dict[str, Any] = {
        "__name__": DEFAULT_MODULE_NAME,
        "__file__": path,
        "__doc__": "",
        "__loader__": type(BuiltinImporter),
        "__builtins__": builtins,
    }
    local_variables: Dict[str, Any] = dict()

    ast = compile(source, path, COMPILE_MODE_EXEC, COMPILE_FLAGS)
    exec(ast, global_variables, local_variables)
    global_variables.update(local_variables)
    return global_variables


class Plugin:
    def __init__(self, path: str):
        self._path = path
        self._global_variables = run_python_plugin(path)
        self._name = ""

    @property
    def path(self) -> str:
        return self._path

    @property
    def globals(self) -> Dict[str, Any]:
        return self._global_variables

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

    async def call_setup(self, context: Any, **kwargs) -> None:
        on_setup = self._global_variables.get(NAME_ON_SETUP)
        assert on_setup is not None
        if iscoroutinefunction(on_setup):
            result = await on_setup(context, **kwargs)
        else:
            result = on_setup(context, **kwargs)
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

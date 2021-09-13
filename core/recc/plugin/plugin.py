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

NAME_ON_CREATE = "on_create"
NAME_ON_DESTROY = "on_destroy"
NAME_ON_OPEN = "on_open"
NAME_ON_CLOSE = "on_close"
NAME_ON_REQUEST = "on_request"

PLUGIN_INFORMATION_KEY_NAME = "name"


def exec_python_plugin(path: str) -> Dict[str, Any]:
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
        self._name = os.path.split(self._path)[1]
        self._global_variables = exec_python_plugin(path)

    @property
    def path(self) -> str:
        return self._path

    @property
    def name(self) -> str:
        return self._name

    @property
    def globals(self) -> Dict[str, Any]:
        return self._global_variables

    @property
    def exists_create(self) -> bool:
        return NAME_ON_CREATE in self._global_variables

    @property
    def exists_destroy(self) -> bool:
        return NAME_ON_DESTROY in self._global_variables

    @property
    def exists_open(self) -> bool:
        return NAME_ON_OPEN in self._global_variables

    @property
    def exists_close(self) -> bool:
        return NAME_ON_CLOSE in self._global_variables

    @property
    def exists_request(self) -> bool:
        return NAME_ON_REQUEST in self._global_variables

    @staticmethod
    def parse_plugin_name(info: Optional[Dict[str, Any]]) -> str:
        if not isinstance(info, dict):
            raise RuntimeError("The `info` must be `dict` type.")
        return str(info[PLUGIN_INFORMATION_KEY_NAME])

    def call_create(self, context: Any, **kwargs) -> None:
        on_create = self._global_variables.get(NAME_ON_CREATE)
        assert on_create is not None
        if iscoroutinefunction(on_create):
            raise RuntimeError("`on_create` is not a coroutine function")
        result = on_create(context, **kwargs)
        self._name = self.parse_plugin_name(result)

    def call_destroy(self) -> None:
        on_destroy = self._global_variables.get(NAME_ON_DESTROY)
        assert on_destroy is not None
        if iscoroutinefunction(on_destroy):
            raise RuntimeError("`on_destroy` is not a coroutine function")
        on_destroy()

    async def call_open(self) -> None:
        on_open = self._global_variables.get(NAME_ON_OPEN)
        assert on_open is not None
        if not iscoroutinefunction(on_open):
            raise RuntimeError("'on_open' must be a coroutine function")
        await on_open()

    async def call_close(self) -> None:
        on_close = self._global_variables.get(NAME_ON_CLOSE)
        assert on_close is not None
        if not iscoroutinefunction(on_close):
            raise RuntimeError("'on_close' must be a coroutine function")
        await on_close()

    async def call_request(self, request: Request) -> Response:
        on_request = self._global_variables.get(NAME_ON_REQUEST)
        assert on_request is not None
        if not iscoroutinefunction(on_request):
            raise RuntimeError("'on_request' must be a coroutine function")
        return await on_request(request)

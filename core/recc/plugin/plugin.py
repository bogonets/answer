# -*- coding: utf-8 -*-

import builtins
from importlib.machinery import BuiltinImporter
from typing import Any, Dict, Optional
from argparse import Namespace
from aiohttp.web_request import Request
from aiohttp.web_response import Response

DEFAULT_MODULE_NAME = "__recc_plugin__"
DEFAULT_FILENAME = "<ReccPlugin>"
COMPILE_MODE_EXEC = "exec"

OPTIMIZE_DEFAULT = -1
OPTIMIZE_LEVEL0 = 0  # no optimization, __debug__ is true
OPTIMIZE_LEVEL1 = 1  # asserts are removed, __debug__ is false
OPTIMIZE_LEVEL2 = 2  # docstrings are removed too

NAME_ON_SETUP = "on_setup"
NAME_ON_TEARDOWN = "on_teardown"
NAME_ON_REQUEST = "on_request"


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
        exec(self._source_ast, self._global_variables, local_variables)
        self._global_variables.update(local_variables)
        self._config: Dict[str, Any] = dict()

    def exists_setup(self) -> bool:
        return NAME_ON_SETUP in self._global_variables

    def exists_teardown(self) -> bool:
        return NAME_ON_TEARDOWN in self._global_variables

    def exists_request(self) -> bool:
        return NAME_ON_REQUEST in self._global_variables

    async def call_setup(self, config: Namespace, context: Any) -> None:
        on_setup = self._global_variables.get(NAME_ON_SETUP)
        if on_setup:
            config = on_setup(config, context)
            if isinstance(config, dict):
                self._config = config

    async def call_teardown(self) -> None:
        on_teardown = self._global_variables.get(NAME_ON_TEARDOWN)
        if on_teardown:
            on_teardown()

    async def call_request(self, request: Optional[Request] = None) -> Response:
        on_teardown = self._global_variables.get(NAME_ON_REQUEST)
        if on_teardown:
            return on_teardown(request)
        else:
            return Response()

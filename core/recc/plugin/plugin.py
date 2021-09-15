# -*- coding: utf-8 -*-

import os
from typing import Optional, Any, Dict, Tuple, Iterable, List
from inspect import iscoroutinefunction
from aiohttp.web_urldispatcher import DynamicResource
from recc.compile.future import get_annotations_compiler_flag

COMPILE_MODE_EXEC = "exec"
COMPILE_FLAGS = get_annotations_compiler_flag()

NAME_ON_CREATE = "on_create"
NAME_ON_DESTROY = "on_destroy"
NAME_ON_ROUTES = "on_routes"
NAME_ON_OPEN = "on_open"
NAME_ON_CLOSE = "on_close"
NAME_ON_REQUEST = "on_request"


class Route:
    def __init__(self, method: str, path: str, func):
        normalize_method = str(method).strip().upper()
        normalize_path = str(path).strip()

        self.method = normalize_method
        self.path = normalize_path
        self.func = func
        self.dynamic_resource = DynamicResource(normalize_path)

    def match(self, method: str, path: str) -> Optional[Dict[str, str]]:
        normalize_method = str(method).strip().upper()
        normalize_path = str(path).strip()

        if self.method != normalize_method:
            return None

        return self.dynamic_resource._match(normalize_path)  # noqa


def get_python_plugin_name(path: str) -> str:
    name = str(os.path.split(path)[1])
    if name.endswith(".py"):
        return name[:-3]
    else:
        return name


def exec_python_plugin(
    path: str,
    global_variables: Dict[str, Any],
    local_variables: Dict[str, Any],
) -> None:
    with open(path, "r") as f:
        source = f.read()
    ast = compile(source, path, COMPILE_MODE_EXEC, COMPILE_FLAGS)
    exec(ast, global_variables, local_variables)


class Plugin:
    def __init__(self, path: str):
        global_variables: Dict[str, Any] = dict()
        exec_python_plugin(path, global_variables, global_variables)

        self._path = path
        self._name = get_python_plugin_name(path)
        self._global_variables = global_variables
        self._routes: List[Route] = list()

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
    def routes(self) -> List[Route]:
        return self._routes

    @property
    def exists_create(self) -> bool:
        return NAME_ON_CREATE in self._global_variables

    @property
    def exists_destroy(self) -> bool:
        return NAME_ON_DESTROY in self._global_variables

    @property
    def exists_routes(self) -> bool:
        return NAME_ON_ROUTES in self._global_variables

    @property
    def exists_open(self) -> bool:
        return NAME_ON_OPEN in self._global_variables

    @property
    def exists_close(self) -> bool:
        return NAME_ON_CLOSE in self._global_variables

    def get_on_create_func(self) -> Any:
        return self._global_variables.get(NAME_ON_CREATE, None)

    def get_on_destroy_func(self) -> Any:
        return self._global_variables.get(NAME_ON_DESTROY, None)

    def get_on_routes_func(self) -> Any:
        return self._global_variables.get(NAME_ON_ROUTES, None)

    def get_on_open_func(self) -> Any:
        return self._global_variables.get(NAME_ON_OPEN, None)

    def get_on_close_func(self) -> Any:
        return self._global_variables.get(NAME_ON_CLOSE, None)

    def call_create(self, context: Any, **kwargs) -> None:
        on_create = self._global_variables.get(NAME_ON_CREATE)
        assert on_create is not None
        if iscoroutinefunction(on_create):
            raise RuntimeError("`on_create` is not a coroutine function")
        on_create(context, **kwargs)

    def call_destroy(self) -> None:
        on_destroy = self._global_variables.get(NAME_ON_DESTROY)
        assert on_destroy is not None
        if iscoroutinefunction(on_destroy):
            raise RuntimeError("`on_destroy` is not a coroutine function")
        on_destroy()

    def _call_get_routes(self) -> Iterable[Tuple[str, str, Any]]:
        on_routes = self._global_variables.get(NAME_ON_ROUTES)
        assert on_routes is not None
        if iscoroutinefunction(on_routes):
            raise RuntimeError("`on_routes` is not a coroutine function")
        return on_routes()

    def update_routes(self) -> None:
        routes = list()
        for method, path, route in self._call_get_routes():
            routes.append(Route(method, path, route))
        self._routes = routes

    def get_route(self, method: str, path: str) -> Tuple[Any, Dict[str, str]]:
        for route in self._routes:
            match_info = route.match(method, path)
            if match_info is not None:
                return route.func, match_info
        raise KeyError(f"Not found route: method={method}, path={path}")

    async def call_route(self, method: str, path: str, *args, **kwargs) -> Any:
        func, _ = self.get_route(method, path)
        assert func is not None
        if iscoroutinefunction(func):
            return await func(*args, **kwargs)
        else:
            return func(*args, **kwargs)

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

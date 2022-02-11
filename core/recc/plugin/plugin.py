# -*- coding: utf-8 -*-

import os
from typing import Optional, Any, Dict, Tuple, Iterable, List, Mapping, Text
from inspect import iscoroutinefunction
from copy import deepcopy
from aiohttp.web_urldispatcher import DynamicResource
from recc.compile.future import get_annotations_compiler_flag
from recc.typing.annotation import eval_annotations

COMPILE_MODE_EXEC = "exec"
COMPILE_FLAGS = get_annotations_compiler_flag()

NAME_ON_CREATE = "on_create"
NAME_ON_DESTROY = "on_destroy"
NAME_ON_OPEN = "on_open"
NAME_ON_CLOSE = "on_close"

NAME_ON_ROUTES = "on_routes"
NAME_ON_CREATE_GROUP = "on_create_group"
NAME_ON_DELETE_GROUP = "on_delete_group"
NAME_ON_CREATE_PROJECT = "on_create_project"
NAME_ON_DELETE_PROJECT = "on_delete_project"

NAME_ON_REGISTER = "on_register"

PYTHON_PLUGIN_PREFIX = """# -*- coding: utf-8 -*-
import sys
if "{site_packages_dir}":
    sys.path.insert(0, "{site_packages_dir}")
if "{plugin_dir}":
    sys.path.insert(0, "{plugin_dir}")
"""


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


def get_python_plugin_directory(path: str) -> str:
    return os.path.split(path)[0]


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
    site_packages_dir: Optional[str] = None,
) -> None:
    prefix = PYTHON_PLUGIN_PREFIX.format(
        site_packages_dir=site_packages_dir if site_packages_dir else str(),
        plugin_dir=os.path.split(path)[0],
    )
    exec(prefix, global_variables, local_variables)

    with open(path, "r") as f:
        source = f.read()
    ast = compile(source, path, COMPILE_MODE_EXEC, COMPILE_FLAGS)
    exec(ast, global_variables, local_variables)


class Plugin:
    def __init__(self, path: str, site_packages_dir: Optional[str] = None):
        global_variables: Dict[str, Any] = dict()
        exec_python_plugin(path, global_variables, global_variables, site_packages_dir)

        self._path = path
        self._directory = get_python_plugin_directory(path)
        self._name = get_python_plugin_name(path)
        self._global_variables = global_variables
        self._routes: List[Route] = list()

    @property
    def path(self) -> str:
        return self._path

    @property
    def directory(self) -> str:
        return self._directory

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
    def exists_create_group(self) -> bool:
        return NAME_ON_CREATE_GROUP in self._global_variables

    @property
    def exists_delete_group(self) -> bool:
        return NAME_ON_DELETE_GROUP in self._global_variables

    @property
    def exists_create_project(self) -> bool:
        return NAME_ON_CREATE_PROJECT in self._global_variables

    @property
    def exists_delete_project(self) -> bool:
        return NAME_ON_DELETE_PROJECT in self._global_variables

    @property
    def exists_open(self) -> bool:
        return NAME_ON_OPEN in self._global_variables

    @property
    def exists_close(self) -> bool:
        return NAME_ON_CLOSE in self._global_variables

    @property
    def exists_register(self) -> bool:
        return NAME_ON_REGISTER in self._global_variables

    # ----------
    # Get Caller
    # ----------

    def get_on_create_func(self) -> Any:
        return self._global_variables.get(NAME_ON_CREATE, None)

    def get_on_destroy_func(self) -> Any:
        return self._global_variables.get(NAME_ON_DESTROY, None)

    def get_on_routes_func(self) -> Any:
        return self._global_variables.get(NAME_ON_ROUTES, None)

    def get_on_create_group_func(self) -> Any:
        return self._global_variables.get(NAME_ON_CREATE_GROUP, None)

    def get_on_delete_group_func(self) -> Any:
        return self._global_variables.get(NAME_ON_DELETE_GROUP, None)

    def get_on_create_project_func(self) -> Any:
        return self._global_variables.get(NAME_ON_CREATE_PROJECT, None)

    def get_on_delete_project_func(self) -> Any:
        return self._global_variables.get(NAME_ON_DELETE_PROJECT, None)

    def get_on_open_func(self) -> Any:
        return self._global_variables.get(NAME_ON_OPEN, None)

    def get_on_close_func(self) -> Any:
        return self._global_variables.get(NAME_ON_CLOSE, None)

    def get_on_register_func(self) -> Any:
        return self._global_variables.get(NAME_ON_REGISTER, None)

    # ------
    # Caller
    # ------

    def call_create(self, context: Any, **kwargs) -> None:
        func = self._global_variables.get(NAME_ON_CREATE)
        assert func is not None
        if iscoroutinefunction(func):
            raise RuntimeError(f"`{NAME_ON_CREATE}` is not a coroutine function")
        func(context, **kwargs)

    def call_destroy(self) -> None:
        func = self._global_variables.get(NAME_ON_DESTROY)
        assert func is not None
        if iscoroutinefunction(func):
            raise RuntimeError(f"`{NAME_ON_DESTROY}` is not a coroutine function")
        func()

    def _call_get_routes(self) -> Iterable[Tuple[str, str, Any]]:
        func = self._global_variables.get(NAME_ON_ROUTES)
        assert func is not None
        if iscoroutinefunction(func):
            raise RuntimeError(f"`{NAME_ON_ROUTES}` is not a coroutine function")
        return func()

    def update_routes(self, deep_copy=False) -> None:
        routes = list()
        for method, path, guest_route in self._call_get_routes():
            if deep_copy:
                host_route = deepcopy(guest_route)
            else:
                host_route = guest_route
            eval_annotations(host_route, self._global_variables, self._global_variables)
            routes.append(Route(method, path, host_route))
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

    async def call_create_group(self, group: str) -> None:
        func = self._global_variables.get(NAME_ON_CREATE_GROUP)
        assert func is not None
        if iscoroutinefunction(func):
            await func(group)
        else:
            func(group)

    async def call_delete_group(self, group: str) -> None:
        func = self._global_variables.get(NAME_ON_DELETE_GROUP)
        assert func is not None
        if iscoroutinefunction(func):
            await func(group)
        else:
            func(group)

    async def call_create_project(self, group: str, project: str) -> None:
        func = self._global_variables.get(NAME_ON_CREATE_PROJECT)
        assert func is not None
        if iscoroutinefunction(func):
            await func(group, project)
        else:
            func(group, project)

    async def call_delete_project(self, group: str, project: str) -> None:
        func = self._global_variables.get(NAME_ON_DELETE_PROJECT)
        assert func is not None
        if iscoroutinefunction(func):
            await func(group, project)
        else:
            func(group, project)

    async def call_open(self) -> None:
        func = self._global_variables.get(NAME_ON_OPEN)
        assert func is not None
        if iscoroutinefunction(func):
            await func()
        else:
            func()

    async def call_close(self) -> None:
        on_close = self._global_variables.get(NAME_ON_CLOSE)
        assert on_close is not None
        if iscoroutinefunction(on_close):
            await on_close()
        else:
            on_close()

    async def call_register(self, *args, **kwargs) -> Any:
        func = self._global_variables.get(NAME_ON_REGISTER)
        assert func is not None
        if iscoroutinefunction(func):
            return await func(*args, **kwargs)
        else:
            return func(*args, **kwargs)

    @staticmethod
    def object_to_packet_answer(
        obj: Any,
    ) -> Tuple[int, Mapping[Text, Text], Optional[Any]]:
        if obj is None:
            return 0, dict(), None
        if isinstance(obj, int):
            return obj, dict(), None
        if not isinstance(obj, tuple) and not isinstance(obj, list):
            raise TypeError("Only list or tuple types are supported")

        if len(obj) == 0:
            return 0, dict(), None

        if not isinstance(obj[0], int):
            raise TypeError(
                "The first element of the tuple must be a `int` type. "
                f"({type(obj[0]).__name__})"
            )
        if len(obj) == 1:
            return obj[0], dict(), None

        if not isinstance(obj[1], Mapping):
            raise TypeError(
                "The second element of the tuple must be a `Mapping` type. "
                f"({type(obj[1]).__name__})"
            )
        if len(obj) == 2:
            return obj[0], obj[1], None
        return obj[0], obj[1], obj[2]

    # async def call_packet(
    #     self,
    #     method: int,
    #     headers: Optional[Mapping[Text, Text]] = None,
    #     content: Optional[bytes] = None,
    # ) -> Tuple[int, Mapping[Text, Text], Optional[bytes]]:
    #     func = self._global_variables.get(NAME_ON_PACKET)
    #     assert func is not None
    #     if iscoroutinefunction(func):
    #         result = await func(method, headers, content)
    #     else:
    #         result = func(method, headers, content)
    #     updated_result = self.object_to_packet_answer(result)
    #     content = updated_result[2]
    #     if content is not None and not isinstance(content, bytes):
    #         raise TypeError(
    #             "The third element of the tuple must be a `bytes` type. "
    #             f"({type(content).__name__})"
    #         )
    #     return updated_result

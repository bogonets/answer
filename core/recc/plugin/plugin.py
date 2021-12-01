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

# Uses: plugin
NAME_ON_CREATE = "on_create"
NAME_ON_DESTROY = "on_destroy"

# Uses: plugin, daemon
NAME_ON_OPEN = "on_open"
NAME_ON_CLOSE = "on_close"

# Uses: plugin
NAME_ON_ROUTES = "on_routes"
NAME_ON_CREATE_GROUP = "on_create_group"
NAME_ON_DELETE_GROUP = "on_delete_group"
NAME_ON_CREATE_PROJECT = "on_create_project"
NAME_ON_DELETE_PROJECT = "on_delete_project"

# Uses: daemon
NAME_ON_INIT = "on_init"
NAME_ON_PACKET = "on_packet"
NAME_ON_PICKLING = "on_pickling"

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
    def exists_init_func(self) -> bool:
        return NAME_ON_INIT in self._global_variables

    @property
    def exists_packet_func(self) -> bool:
        return NAME_ON_PACKET in self._global_variables

    @property
    def exists_pickling_func(self) -> bool:
        return NAME_ON_PICKLING in self._global_variables

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

    def get_on_init_func(self) -> Any:
        return self._global_variables.get(NAME_ON_INIT, None)

    def get_on_packet_func(self) -> Any:
        return self._global_variables.get(NAME_ON_PACKET, None)

    def get_on_pickling_func(self) -> Any:
        return self._global_variables.get(NAME_ON_PICKLING, None)

    # ------
    # Caller
    # ------

    def call_create(self, context: Any, **kwargs) -> None:
        on_create = self._global_variables.get(NAME_ON_CREATE)
        assert on_create is not None
        if iscoroutinefunction(on_create):
            raise RuntimeError(f"`{NAME_ON_CREATE}` is not a coroutine function")
        on_create(context, **kwargs)

    def call_destroy(self) -> None:
        on_destroy = self._global_variables.get(NAME_ON_DESTROY)
        assert on_destroy is not None
        if iscoroutinefunction(on_destroy):
            raise RuntimeError(f"`{NAME_ON_DESTROY}` is not a coroutine function")
        on_destroy()

    def _call_get_routes(self) -> Iterable[Tuple[str, str, Any]]:
        on_routes = self._global_variables.get(NAME_ON_ROUTES)
        assert on_routes is not None
        if iscoroutinefunction(on_routes):
            raise RuntimeError(f"`{NAME_ON_ROUTES}` is not a coroutine function")
        return on_routes()

    def update_routes(self) -> None:
        routes = list()
        for method, path, guest_route in self._call_get_routes():
            host_route = deepcopy(guest_route)
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
        on_create_group = self._global_variables.get(NAME_ON_CREATE_GROUP)
        assert on_create_group is not None
        if not iscoroutinefunction(on_create_group):
            raise RuntimeError(f"'{NAME_ON_CREATE_GROUP}' must be a coroutine function")
        await on_create_group(group)

    async def call_delete_group(self, group: str) -> None:
        on_delete_group = self._global_variables.get(NAME_ON_DELETE_GROUP)
        assert on_delete_group is not None
        if iscoroutinefunction(on_delete_group):
            raise RuntimeError(f"`{NAME_ON_DELETE_GROUP}` is not a coroutine function")
        return on_delete_group(group)

    async def call_create_project(self, group: str, project: str) -> None:
        on_create_project = self._global_variables.get(NAME_ON_CREATE_PROJECT)
        assert on_create_project is not None
        if not iscoroutinefunction(on_create_project):
            raise RuntimeError(
                f"'{NAME_ON_CREATE_PROJECT}' must be a coroutine function"
            )
        await on_create_project(group, project)

    async def call_delete_project(self, group: str, project: str) -> None:
        on_delete_project = self._global_variables.get(NAME_ON_DELETE_PROJECT)
        assert on_delete_project is not None
        if iscoroutinefunction(on_delete_project):
            raise RuntimeError(
                f"`{NAME_ON_DELETE_PROJECT}` is not a coroutine function"
            )
        return on_delete_project(group, project)

    async def call_open(self) -> None:
        on_open = self._global_variables.get(NAME_ON_OPEN)
        assert on_open is not None
        if not iscoroutinefunction(on_open):
            raise RuntimeError(f"'{NAME_ON_OPEN}' must be a coroutine function")
        await on_open()

    async def call_close(self) -> None:
        on_close = self._global_variables.get(NAME_ON_CLOSE)
        assert on_close is not None
        if not iscoroutinefunction(on_close):
            raise RuntimeError(f"'{NAME_ON_CLOSE}' must be a coroutine function")
        await on_close()

    async def call_init(self, *args, **kwargs) -> None:
        on_init = self._global_variables.get(NAME_ON_INIT)
        assert on_init is not None
        if iscoroutinefunction(on_init):
            await on_init(*args, **kwargs)
        else:
            on_init(*args, **kwargs)

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

    async def call_packet(
        self,
        method: int,
        headers: Optional[Mapping[Text, Text]] = None,
        content: Optional[bytes] = None,
    ) -> Tuple[int, Mapping[Text, Text], Optional[bytes]]:
        func = self._global_variables.get(NAME_ON_PACKET)
        assert func is not None
        if iscoroutinefunction(func):
            result = await func(method, headers, content)
        else:
            result = func(method, headers, content)
        updated_result = self.object_to_packet_answer(result)
        content = updated_result[2]
        if content is not None and not isinstance(content, bytes):
            raise TypeError(
                "The third element of the tuple must be a `bytes` type. "
                f"({type(content).__name__})"
            )
        return updated_result

    async def call_pickling(
        self,
        method: int,
        headers: Optional[Mapping[Text, Text]] = None,
        content: Optional[Any] = None,
    ) -> Tuple[int, Mapping[Text, Text], Optional[Any]]:
        func = self._global_variables.get(NAME_ON_PICKLING)
        assert func is not None
        if iscoroutinefunction(func):
            result = await func(method, headers, content)
        else:
            result = func(method, headers, content)
        return self.object_to_packet_answer(result)

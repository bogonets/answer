# -*- coding: utf-8 -*-

import builtins
from typing import Optional, Any, Dict, List
from importlib.machinery import BuiltinImporter
from recc.exception.recc_error import ReccNotFoundError, ReccInitError
from recc.venv.pyvenv_cfg import read_site_packages_dir
from recc.blueprint.blueprint import BpProperty
from recc.vs.lamda_interface import REQUEST_METHOD_SET, REQUEST_METHOD_GET, Lamda
from recc.template.lamda_template import LamdaTemplate
from recc.template.property import Property

DEFAULT_MODULE_NAME = "__answer__"
DEFAULT_FILENAME = "<PythonLambda>"
COMPILE_MODE_EXEC = "exec"
OPTIMIZE_DEFAULT = -1
OPTIMIZE_LEVEL0 = 0  # no optimization, __debug__ is true
OPTIMIZE_LEVEL1 = 1  # asserts are removed, __debug__ is false
OPTIMIZE_LEVEL2 = 2  # docstrings are removed too

PYTHON_LAMBDA_SOURCE_PREFIX = """# -*- coding: utf-8 -*-
import sys
import os
import signal
if {ignore_interrupt_signal}:
    signal.signal(signal.SIGINT, signal.SIG_IGN)
if "{site_packages}":
    sys.path.insert(0, "{site_packages}")
"""

VAR_NAME_METHOD = "method"
VAR_NAME_KEY = "key"
VAR_NAME_VALUE = "val"
VAR_NAME_OPTIONS = "options"
VAR_NAME_RESULT = "result"
VAR_NAME_KWARGS = "kwargs"

NAME_ON_REQUEST = "on_request"
NAME_ON_GET = "on_get"
NAME_ON_SET = "on_set"
NAME_ON_INIT = "on_init"
NAME_ON_VALID = "on_valid"
NAME_ON_DESTROY = "on_destroy"
NAME_ON_RUN = "on_run"

CALL_SOURCE_ON_REQUEST = "result = on_request(method, key, val, **options)"
CALL_SOURCE_ON_GET = "result = on_get(key)"
CALL_SOURCE_ON_SET = "on_set(key, val)"
CALL_SOURCE_ON_INIT = "result = on_init()"
CALL_SOURCE_ON_VALID = "result = on_valid()"
CALL_SOURCE_ON_DESTROY = "on_destroy()"
CALL_SOURCE_ON_RUN = "result = on_run(**kwargs)"

CALL_FILENAME_ON_REQUEST = "<builtin_on_request_caller>"
CALL_FILENAME_ON_GET = "<builtin_on_get_caller>"
CALL_FILENAME_ON_SET = "<builtin_on_set_caller>"
CALL_FILENAME_ON_INIT = "<builtin_on_init_caller>"
CALL_FILENAME_ON_VALID = "<builtin_on_valid_caller>"
CALL_FILENAME_ON_DESTROY = "<builtin_on_destroy_caller>"
CALL_FILENAME_ON_RUN = "<builtin_on_run_caller>"


class LamdaPython(Lamda):
    """
    Python lambda plugin.
    """

    _template: LamdaTemplate
    _app: Dict[str, Any]
    _global_variables: Dict[str, Any]
    _env_root: str

    _on_get_ast: Any  # legacy
    _on_set_ast: Any  # legacy
    _on_request_ast: Any
    _on_init_ast: Any
    _on_valid_ast: Any
    _on_destroy_ast: Any
    _on_run_ast: Any

    def __init__(self, template: Optional[LamdaTemplate] = None):
        self._template = template if template else LamdaTemplate()
        self._app = {
            # "template_path": TEMPLATE.info.config_path,
            # "workspace_name": parent._shared->workspace,
            # "current_working_directory": cwd,
            "props": dict(),
            "input": dict(),
            "output": dict(),
            "run_results": list(),
        }

        source = self._template.get_script_content()
        script_path = self._template.get_runtime_script_path()
        doc = self._template.get_documentation()
        optimize = self._template.get_optimize()

        self._global_variables = {
            "__name__": DEFAULT_MODULE_NAME,
            "__file__": script_path,
            "__doc__": doc,
            "__loader__": type(BuiltinImporter),
            "__builtins__": builtins,
            "app": self._app,
        }

        env_root = self._template.get_environment_root()
        if env_root and self._template.is_pyenv_environment():
            self._env_root = env_root
        else:
            self._env_root = str()

        try:
            site_packages = read_site_packages_dir(self._env_root)
        except:  # noqa
            site_packages = str()

        local_variables: Dict[str, Any] = dict()
        source_prefix = PYTHON_LAMBDA_SOURCE_PREFIX.format(
            ignore_interrupt_signal=True,
            site_packages=site_packages,
        )
        exec(source_prefix, self._global_variables, local_variables)

        def _compile(src: str, filename: str):
            return compile(src, filename, COMPILE_MODE_EXEC, 0, False, optimize)

        source_ast = _compile(
            source if source is not None else str(),
            script_path if script_path is not None else DEFAULT_FILENAME,
        )

        # This function raises SyntaxError if the compiled source is invalid,
        # and ValueError if the source contains null bytes.
        exec(source_ast, self._global_variables, local_variables)
        self._global_variables.update(local_variables)

        # fmt: off
        self._on_request_ast = _compile(CALL_SOURCE_ON_REQUEST, CALL_FILENAME_ON_REQUEST)  # noqa
        self._on_get_ast = _compile(CALL_SOURCE_ON_GET, CALL_FILENAME_ON_GET)
        self._on_set_ast = _compile(CALL_SOURCE_ON_SET, CALL_FILENAME_ON_SET)
        self._on_init_ast = _compile(CALL_SOURCE_ON_INIT, CALL_FILENAME_ON_INIT)
        self._on_valid_ast = _compile(CALL_SOURCE_ON_VALID, CALL_FILENAME_ON_VALID)
        self._on_destroy_ast = _compile(CALL_SOURCE_ON_DESTROY, CALL_FILENAME_ON_DESTROY)  # noqa
        self._on_run_ast = _compile(CALL_SOURCE_ON_RUN, CALL_FILENAME_ON_RUN)
        # fmt: on

    def _request(self, method: str, key: str, value: Any = None, **options) -> Any:
        if NAME_ON_REQUEST not in self._global_variables:
            raise ReccNotFoundError(f"Not found `{NAME_ON_REQUEST}` function.")

        local_variables: Dict[str, Any] = {
            VAR_NAME_METHOD: method,
            VAR_NAME_KEY: key,
            VAR_NAME_VALUE: value,
            VAR_NAME_OPTIONS: options,
        }
        exec(self._on_request_ast, self._global_variables, local_variables)
        return local_variables[VAR_NAME_RESULT]

    def _get(self, key: str) -> Any:
        if NAME_ON_GET not in self._global_variables:
            raise ReccNotFoundError(f"Not found `{NAME_ON_GET}` function.")

        local_variables = {VAR_NAME_KEY: key}
        exec(self._on_get_ast, self._global_variables, local_variables)

        assert VAR_NAME_RESULT in local_variables
        result = local_variables[VAR_NAME_RESULT]

        if self._template.get_version_tuple() >= (2, 0):
            return result
        else:
            # The "legacy" version can only accept strings.
            return str(result)

    def _set(self, key: str, value: Any = None) -> None:
        if NAME_ON_SET not in self._global_variables:
            raise ReccNotFoundError(f"Not found `{NAME_ON_SET}` function.")

        if self._template.get_version_tuple() >= (2, 0):
            assign_value = value
        else:
            # The "legacy" version can only accept strings.
            assign_value = str(value)

        local_variables = {VAR_NAME_KEY: key, VAR_NAME_VALUE: assign_value}
        exec(self._on_set_ast, self._global_variables, local_variables)

    def request(self, method: str, key: str, value: Any = None, **options) -> Any:
        if self._template.get_version_tuple() < (2, 0):
            if method == REQUEST_METHOD_GET:
                return self._get(key)
            elif method == REQUEST_METHOD_SET:
                self._set(key, value)
                return None

        return self._request(method, key, value, **options)

    def init(self) -> None:
        if NAME_ON_INIT not in self._global_variables:
            return

        local_variables: Dict[str, Any] = dict()
        exec(self._on_init_ast, self._global_variables, local_variables)

        if self._template.get_version_tuple() >= (2, 0):
            return

        assert VAR_NAME_RESULT in local_variables
        if not bool(local_variables[VAR_NAME_RESULT]):
            raise ReccInitError("Initialization failed.")

    def valid(self) -> bool:
        if NAME_ON_VALID not in self._global_variables:
            return True

        try:
            local_variables: Dict[str, Any] = dict()
            exec(self._on_valid_ast, self._global_variables, local_variables)

            assert VAR_NAME_RESULT in local_variables
            return bool(local_variables[VAR_NAME_RESULT])
        except:  # noqa
            return False

    def init_properties(
        self,
        bp_properties: Optional[Dict[str, BpProperty]] = None,
    ) -> None:
        bp_props = bp_properties.copy() if bp_properties else dict()
        temp_props: List[Property]
        if self._template.properties:
            temp_props = self._template.properties
        else:
            temp_props = list()

        for prop in temp_props:
            if not prop.name:
                continue
            name = prop.name
            if name in bp_props.keys():
                value = bp_props.pop(name).value
            else:
                value = prop.value_default
            if value is not None:
                self.request(REQUEST_METHOD_SET, name, value)

        for prop_name, bp_prop in bp_props.items():
            if bp_prop.value is not None:
                self.request(REQUEST_METHOD_SET, prop_name, bp_prop.value)

    def destroy(self) -> None:
        if NAME_ON_DESTROY not in self._global_variables:
            return

        exec(self._on_destroy_ast, self._global_variables)

    def run(self, **kwargs) -> Optional[Dict[str, Any]]:
        if NAME_ON_RUN not in self._global_variables:
            return None

        local_variables: Dict[str, Any] = {VAR_NAME_KWARGS: kwargs}
        exec(self._on_run_ast, self._global_variables, local_variables)
        return local_variables.get(VAR_NAME_RESULT)

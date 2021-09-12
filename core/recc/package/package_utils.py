# -*- coding: utf-8 -*-

import os
from pkgutil import iter_modules, ModuleInfo
from typing import List
from functools import reduce
from importlib import import_module


def get_module_path(module) -> str:
    module_path = getattr(module, "__path__", None)
    if module_path:
        assert isinstance(module_path, list)
        return module_path[0]

    module_file = getattr(module, "__file__", None)
    if module_file:
        assert isinstance(module_file, str)
        return module_file

    raise RuntimeError(f"The '{module.__name__}' module path is unknown")


def get_module_directory(module) -> str:
    module_path = getattr(module, "__path__", None)
    if module_path:
        assert isinstance(module_path, list)
        return module_path[0]

    module_file = getattr(module, "__file__", None)
    if module_file:
        assert isinstance(module_file, str)
        return os.path.dirname(module_file)

    raise RuntimeError(f"The '{module.__name__}' module path is unknown")


def merge_import_path(*modules) -> str:
    return reduce(lambda x, y: f"{x}.{y}", modules)


def list_submodules(module) -> List[ModuleInfo]:
    module_path = getattr(module, "__path__")
    if module_path:
        return [submodule for submodule in iter_modules(module_path)]
    raise RuntimeError(f"'{module.__name__}' does not have attribute `__path__`")


def list_submodule_names(module) -> List[str]:
    return [m.name for m in list_submodules(module)]


def list_submodules_with_import_paths(*import_paths) -> List[ModuleInfo]:
    import_path = merge_import_path(*import_paths)
    module = import_module(import_path)
    return list_submodules(module)


def list_submodule_names_with_import_paths(*import_paths) -> List[str]:
    return [m.name for m in list_submodules(*import_paths)]

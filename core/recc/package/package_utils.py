# -*- coding: utf-8 -*-

import os
from pkgutil import ModuleInfo, iter_modules
from types import ModuleType
from typing import List, Optional, Sequence

from recc.regex.access_filter import UnionPattern, access_filter


def get_module_path(module: ModuleType) -> str:
    module_path = getattr(module, "__path__", None)
    if module_path:
        assert isinstance(module_path, list)
        return module_path[0]

    module_file = getattr(module, "__file__", None)
    if module_file:
        assert isinstance(module_file, str)
        return module_file

    raise RuntimeError(f"The '{module.__name__}' module path is unknown")


def get_module_directory(module: ModuleType) -> str:
    module_path = getattr(module, "__path__", None)
    if module_path:
        assert isinstance(module_path, list)
        return module_path[0]

    module_file = getattr(module, "__file__", None)
    if module_file:
        assert isinstance(module_file, str)
        return os.path.dirname(module_file)

    raise RuntimeError(f"The '{module.__name__}' module path is unknown")


def list_submodules(module: ModuleType) -> List[ModuleInfo]:
    module_path = getattr(module, "__path__")
    if module_path:
        return [submodule for submodule in iter_modules(module_path)]
    raise RuntimeError(f"'{module.__name__}' does not have attribute `__path__`")


def list_submodule_names(module: ModuleType) -> List[str]:
    return [m.name for m in list_submodules(module)]


def all_module_names() -> List[str]:
    return [m.name for m in iter_modules()]


def startswith_module_names(prefix: str) -> List[str]:
    return [m.name for m in iter_modules() if m.name.startswith(prefix)]


def filter_module_names(
    prefix: str,
    denies: Optional[Sequence[UnionPattern]] = None,
    allows: Optional[Sequence[UnionPattern]] = None,
) -> List[str]:
    return access_filter(
        names=startswith_module_names(prefix),
        denies=denies,
        allows=allows,
    )

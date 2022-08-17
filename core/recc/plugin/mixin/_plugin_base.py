# -*- coding: utf-8 -*-

from abc import ABCMeta
from contextlib import contextmanager
from importlib import import_module
from sys import modules as sys_modules
from types import ModuleType
from typing import Any, Optional, TypeVar

from recc.package.package_utils import get_module_directory

_T = TypeVar("_T")


@contextmanager
def module_stash(module_name: str):
    temp: Optional[ModuleType] = None

    if module_name in sys_modules:
        temp = sys_modules.get(module_name)
        del sys_modules[module_name]

    assert module_name not in sys_modules

    yield

    assert module_name in sys_modules
    del sys_modules[module_name]

    if temp is not None:
        sys_modules[module_name] = temp


class PluginBase(metaclass=ABCMeta):

    _module: ModuleType

    @staticmethod
    def import_module(module_name: str, isolate=False) -> ModuleType:
        if isolate:
            with module_stash(module_name):
                return import_module(module_name)
        else:
            return import_module(module_name)

    @property
    def module_directory(self) -> str:
        return get_module_directory(self._module)

    @property
    def module_name(self) -> str:
        assert self._module is not None
        return self._module.__name__

    def has(self, name: str) -> bool:
        assert self._module is not None
        return hasattr(self._module, name)

    def get(self, name: str) -> Any:
        assert self._module is not None
        return getattr(self._module, name, None)

    def opt(self, name: str, default: _T) -> _T:
        assert self._module is not None
        return getattr(self._module, name, default)

    def set(self, name: str, value: Any) -> None:
        assert self._module is not None
        setattr(self._module, name, value)

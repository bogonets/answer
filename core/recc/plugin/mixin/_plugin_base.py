# -*- coding: utf-8 -*-

from abc import ABCMeta
from importlib import import_module
from types import ModuleType
from typing import Any, TypeVar

from recc.package.package_utils import get_module_directory

_T = TypeVar("_T")


class PluginBase(metaclass=ABCMeta):

    _module: ModuleType

    @staticmethod
    def import_module(module_name: str) -> ModuleType:
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

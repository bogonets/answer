# -*- coding: utf-8 -*-

from inspect import iscoroutinefunction
from typing import Any

from recc.plugin.errors import (
    PluginCallbackCoroutineError,
    PluginCallbackNotFoundError,
    PluginCallbackRuntimeError,
)
from recc.plugin.mixin._plugin_base import PluginBase
from recc.variables.plugin import NAME_ON_CREATE, NAME_ON_DESTROY


class PluginCreate(PluginBase):
    @property
    def has_on_create(self) -> bool:
        return hasattr(self._module, NAME_ON_CREATE)

    @property
    def has_on_destroy(self) -> bool:
        return hasattr(self._module, NAME_ON_DESTROY)

    def on_create(self, context: Any) -> None:
        callback = getattr(self._module, NAME_ON_CREATE, None)
        if callback is None:
            raise PluginCallbackNotFoundError(self.module_name, NAME_ON_CREATE)

        if iscoroutinefunction(callback):
            raise PluginCallbackCoroutineError(self.module_name, NAME_ON_CREATE)

        try:
            callback(context)
        except BaseException as e:
            raise PluginCallbackRuntimeError(self.module_name, NAME_ON_CREATE) from e

    def on_destroy(self) -> None:
        callback = getattr(self._module, NAME_ON_DESTROY, None)
        if callback is None:
            raise PluginCallbackNotFoundError(self.module_name, NAME_ON_DESTROY)

        if iscoroutinefunction(callback):
            raise PluginCallbackCoroutineError(self.module_name, NAME_ON_DESTROY)

        try:
            callback()
        except BaseException as e:
            raise PluginCallbackRuntimeError(self.module_name, NAME_ON_DESTROY) from e

# -*- coding: utf-8 -*-

from inspect import iscoroutinefunction

from recc.plugin.errors import (
    PluginCallbackNotCoroutineError,
    PluginCallbackNotFoundError,
    PluginCallbackRuntimeError,
)
from recc.plugin.mixin._plugin_base import PluginBase
from recc.variables.plugin import NAME_ON_CLOSE, NAME_ON_OPEN


class PluginOpen(PluginBase):
    @property
    def has_on_open(self) -> bool:
        return hasattr(self._module, NAME_ON_OPEN)

    @property
    def has_on_close(self) -> bool:
        return hasattr(self._module, NAME_ON_CLOSE)

    async def on_open(self) -> None:
        callback = getattr(self._module, NAME_ON_OPEN, None)
        if callback is None:
            raise PluginCallbackNotFoundError(self.module_name, NAME_ON_OPEN)

        if not iscoroutinefunction(callback):
            raise PluginCallbackNotCoroutineError(self.module_name, NAME_ON_OPEN)

        try:
            await callback()
        except BaseException as e:
            raise PluginCallbackRuntimeError(self.module_name, NAME_ON_OPEN) from e

    async def on_close(self) -> None:
        callback = getattr(self._module, NAME_ON_CLOSE, None)
        if callback is None:
            raise PluginCallbackNotFoundError(self.module_name, NAME_ON_CLOSE)

        if not iscoroutinefunction(callback):
            raise PluginCallbackNotCoroutineError(self.module_name, NAME_ON_CLOSE)

        try:
            await callback()
        except BaseException as e:
            raise PluginCallbackRuntimeError(self.module_name, NAME_ON_CLOSE) from e

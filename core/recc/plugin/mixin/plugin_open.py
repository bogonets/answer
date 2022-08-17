# -*- coding: utf-8 -*-

from inspect import iscoroutinefunction

from recc.plugin.errors import (
    PluginCallbackInvalidStateError,
    PluginCallbackNotCoroutineError,
    PluginCallbackNotFoundError,
    PluginCallbackRuntimeError,
)
from recc.plugin.mixin._plugin_base import PluginBase
from recc.variables.plugin import NAME_ON_CLOSE, NAME_ON_OPEN


class PluginOpen(PluginBase):

    _opened: bool

    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        instance._opened = False
        return instance

    @property
    def opened(self) -> bool:
        assert isinstance(self._opened, bool)
        return self._opened

    @property
    def has_on_open(self) -> bool:
        return self.has(NAME_ON_OPEN)

    @property
    def has_on_close(self) -> bool:
        return self.has(NAME_ON_CLOSE)

    async def on_open(self) -> None:
        if self._opened:
            raise PluginCallbackInvalidStateError(
                self.module_name, NAME_ON_OPEN, "Already opened"
            )

        callback = self.get(NAME_ON_OPEN)
        if callback is None:
            raise PluginCallbackNotFoundError(self.module_name, NAME_ON_OPEN)

        if not iscoroutinefunction(callback):
            raise PluginCallbackNotCoroutineError(self.module_name, NAME_ON_OPEN)

        try:
            await callback()
        except BaseException as e:
            raise PluginCallbackRuntimeError(self.module_name, NAME_ON_OPEN) from e
        else:
            self._opened = True

    async def on_close(self) -> None:
        if not self._opened:
            raise PluginCallbackInvalidStateError(
                self.module_name, NAME_ON_CLOSE, "Not opened"
            )

        callback = self.get(NAME_ON_CLOSE)
        if callback is None:
            raise PluginCallbackNotFoundError(self.module_name, NAME_ON_CLOSE)

        if not iscoroutinefunction(callback):
            raise PluginCallbackNotCoroutineError(self.module_name, NAME_ON_CLOSE)

        try:
            await callback()
        except BaseException as e:
            raise PluginCallbackRuntimeError(self.module_name, NAME_ON_CLOSE) from e
        else:
            self._opened = False

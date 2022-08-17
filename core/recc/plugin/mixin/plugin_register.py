# -*- coding: utf-8 -*-

from inspect import iscoroutinefunction

from recc.plugin.errors import (
    PluginCallbackInvalidReturnValueError,
    PluginCallbackInvalidStateError,
    PluginCallbackNotCoroutineError,
    PluginCallbackNotFoundError,
    PluginCallbackRuntimeError,
)
from recc.plugin.mixin._plugin_base import PluginBase
from recc.variables.plugin import NAME_ON_REGISTER


class PluginRegister(PluginBase):

    _registered = False

    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        instance._registered = False
        return instance

    @property
    def registered(self) -> bool:
        assert isinstance(self._registered, bool)
        return self._registered

    @property
    def has_on_register(self) -> bool:
        return self.has(NAME_ON_REGISTER)

    async def on_register(self, *args, **kwargs) -> int:
        if self._registered:
            raise PluginCallbackInvalidStateError(
                self.module_name, NAME_ON_REGISTER, "Already registered"
            )

        callback = self.get(NAME_ON_REGISTER)
        if callback is None:
            raise PluginCallbackNotFoundError(self.module_name, NAME_ON_REGISTER)

        if not iscoroutinefunction(callback):
            raise PluginCallbackNotCoroutineError(self.module_name, NAME_ON_REGISTER)

        try:
            result = await callback(*args, **kwargs)
        except BaseException as e:
            raise PluginCallbackRuntimeError(self.module_name, NAME_ON_REGISTER) from e

        if not isinstance(result, int):
            raise PluginCallbackInvalidReturnValueError(
                self.module_name,
                NAME_ON_REGISTER,
                "It must be of type `int`",
            )

        self._registered = True
        return result

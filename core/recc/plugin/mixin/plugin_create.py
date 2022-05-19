# -*- coding: utf-8 -*-

from inspect import iscoroutinefunction
from typing import Any

from recc.plugin.errors import (
    PluginCallbackCoroutineError,
    PluginCallbackInvalidStateError,
    PluginCallbackNotFoundError,
    PluginCallbackRuntimeError,
)
from recc.plugin.mixin._plugin_base import PluginBase
from recc.variables.plugin import NAME_ON_CREATE, NAME_ON_DESTROY


class PluginCreate(PluginBase):

    _created = False

    @property
    def created(self) -> bool:
        assert isinstance(self._created, bool)
        return self._created

    @property
    def has_on_create(self) -> bool:
        return hasattr(self._module, NAME_ON_CREATE)

    @property
    def has_on_destroy(self) -> bool:
        return hasattr(self._module, NAME_ON_DESTROY)

    def on_create(self, context: Any) -> None:
        if self._created:
            raise PluginCallbackInvalidStateError(
                self.module_name, NAME_ON_CREATE, "Already created"
            )

        callback = getattr(self._module, NAME_ON_CREATE, None)
        if callback is None:
            raise PluginCallbackNotFoundError(self.module_name, NAME_ON_CREATE)

        if iscoroutinefunction(callback):
            raise PluginCallbackCoroutineError(self.module_name, NAME_ON_CREATE)

        try:
            callback(context)
        except BaseException as e:
            raise PluginCallbackRuntimeError(self.module_name, NAME_ON_CREATE) from e
        else:
            self._created = True

    def on_destroy(self) -> None:
        if not self._created:
            raise PluginCallbackInvalidStateError(
                self.module_name, NAME_ON_DESTROY, "Not created"
            )

        callback = getattr(self._module, NAME_ON_DESTROY, None)
        if callback is None:
            raise PluginCallbackNotFoundError(self.module_name, NAME_ON_DESTROY)

        if iscoroutinefunction(callback):
            raise PluginCallbackCoroutineError(self.module_name, NAME_ON_DESTROY)

        try:
            callback()
        except BaseException as e:
            raise PluginCallbackRuntimeError(self.module_name, NAME_ON_DESTROY) from e
        else:
            self._created = False

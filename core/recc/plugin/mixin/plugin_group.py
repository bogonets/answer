# -*- coding: utf-8 -*-

from inspect import iscoroutinefunction

from recc.plugin.errors import (
    PluginCallbackNotCoroutineError,
    PluginCallbackNotFoundError,
    PluginCallbackRuntimeError,
)
from recc.plugin.mixin._plugin_base import PluginBase
from recc.variables.plugin import NAME_ON_CREATE_GROUP, NAME_ON_DELETE_GROUP


class PluginGroup(PluginBase):
    @property
    def has_on_create_group(self) -> bool:
        return self.has(NAME_ON_CREATE_GROUP)

    @property
    def has_on_delete_group(self) -> bool:
        return self.has(NAME_ON_DELETE_GROUP)

    async def on_create_group(self, uid: int) -> None:
        callback = self.get(NAME_ON_CREATE_GROUP)
        if callback is None:
            raise PluginCallbackNotFoundError(self.module_name, NAME_ON_CREATE_GROUP)

        if not iscoroutinefunction(callback):
            raise PluginCallbackNotCoroutineError(
                self.module_name,
                NAME_ON_CREATE_GROUP,
            )

        try:
            await callback(uid)
        except BaseException as e:
            raise PluginCallbackRuntimeError(
                self.module_name,
                NAME_ON_CREATE_GROUP,
            ) from e

    async def on_delete_group(self, uid: int) -> None:
        callback = self.get(NAME_ON_DELETE_GROUP)
        if callback is None:
            raise PluginCallbackNotFoundError(self.module_name, NAME_ON_DELETE_GROUP)

        if not iscoroutinefunction(callback):
            raise PluginCallbackNotCoroutineError(
                self.module_name,
                NAME_ON_DELETE_GROUP,
            )

        try:
            await callback(uid)
        except BaseException as e:
            raise PluginCallbackRuntimeError(
                self.module_name,
                NAME_ON_DELETE_GROUP,
            ) from e

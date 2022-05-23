# -*- coding: utf-8 -*-

from recc.plugin.errors import (
    PluginAttributeInvalidValueError,
    PluginAttributeNotFoundError,
)
from recc.plugin.mixin._plugin_base import PluginBase
from recc.variables.plugin import NAME_VERSION


class PluginVersion(PluginBase):
    @property
    def version(self) -> str:
        if not self.has(NAME_VERSION):
            raise PluginAttributeNotFoundError(self.module_name, NAME_VERSION)

        value = self.get(NAME_VERSION)

        if value is None:
            raise PluginAttributeInvalidValueError(
                self.module_name,
                NAME_VERSION,
                "It must not be of `None`",
            )

        if not isinstance(value, str):
            raise PluginAttributeInvalidValueError(
                self.module_name,
                NAME_VERSION,
                "The attribute must be of type `str`",
            )

        return value

# -*- coding: utf-8 -*-

from typing import Any, Dict

from recc.plugin.errors import PluginAttributeInvalidValueError
from recc.plugin.mixin._plugin_base import PluginBase
from recc.variables.plugin import NAME_RECC_SPEC


class PluginSpec(PluginBase):
    @property
    def spec(self) -> Dict[str, Any]:
        if not self.has(NAME_RECC_SPEC):
            return dict()

        value = self.get(NAME_RECC_SPEC)

        if value is None:
            return dict()

        if not isinstance(value, dict):
            raise PluginAttributeInvalidValueError(
                self.module_name,
                NAME_RECC_SPEC,
                "The attribute must be of type `dict`",
            )

        return value

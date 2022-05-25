# -*- coding: utf-8 -*-

from typing import List, Optional

from recc.core.mixin.context_base import ContextBase
from recc.packet.plugin import PluginA
from recc.packet.preference import ExtraA
from recc.plugin.core_plugin import CorePlugin


class ContextPlugin(ContextBase):
    def get_plugin_keys(self) -> List[str]:
        return list(self._plugins.keys())

    def get_plugins(self) -> List[PluginA]:
        return list(map(lambda x: PluginA(x), self._plugins.keys()))

    def get_core_plugin(self, key: str) -> Optional[CorePlugin]:
        return self._plugins.get(key)

    def get_plugin_extra(self) -> ExtraA:
        return ExtraA(dict())

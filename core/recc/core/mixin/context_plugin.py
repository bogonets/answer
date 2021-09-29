# -*- coding: utf-8 -*-

from typing import List
from recc.core.mixin.context_base import ContextBase
from recc.packet.plugin import PluginA


class ContextPlugin(ContextBase):
    def get_plugin_keys(self) -> List[str]:
        return list(self.plugins.keys())

    def get_plugins(self) -> List[PluginA]:
        return list(map(lambda x: PluginA(x), self.plugins.keys()))

# -*- coding: utf-8 -*-

from typing import List, Optional

from recc.core.mixin.context_base import ContextBase
from recc.packet.plugin import PluginA
from recc.plugin.core_plugin import CorePlugin


class ContextPlugin(ContextBase):
    def get_plugin_keys(self) -> List[str]:
        return list(self._plugins.keys())

    def get_plugins(self) -> List[PluginA]:
        return self._plugins.as_answer_packet()

    def get_core_plugin(self, key: str) -> Optional[CorePlugin]:
        return self._plugins.get(key)

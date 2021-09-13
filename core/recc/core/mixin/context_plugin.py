# -*- coding: utf-8 -*-

from typing import List
from recc.core.mixin.context_base import ContextBase


class ContextPlugin(ContextBase):
    def get_plugin_keys(self) -> List[str]:
        return list(self.plugins.keys())

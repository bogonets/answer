# -*- coding: utf-8 -*-

from typing import List
from recc.core.mixin.context_base import ContextBase
from recc.packet.template import TemplateA
from recc.template.manager.lamda_template_key import LamdaTemplateKey


class ContextLamda(ContextBase):
    def get_lamda_template_keys(self) -> List[LamdaTemplateKey]:
        return list(self.template_manager.keys())

    def get_template_keys(self) -> List[TemplateA]:
        result = list()
        for k in self.template_manager.keys():
            result.append(TemplateA(k.position.value, k.category, k.name))
        return result

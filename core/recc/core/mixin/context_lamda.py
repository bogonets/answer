# -*- coding: utf-8 -*-

from typing import List
from recc.core.mixin.context_base import ContextBase
from recc.core.struct.template import TemplateKey
from recc.template.manager.lamda_template_key import LamdaTemplateKey


class ContextLamda(ContextBase):
    def get_lamda_template_keys(self) -> List[LamdaTemplateKey]:
        return list(self._templates.keys())

    def get_template_keys(self) -> List[TemplateKey]:
        result = list()
        for k in self._templates.keys():
            result.append(TemplateKey(k.position.value, k.category, k.name))
        return result

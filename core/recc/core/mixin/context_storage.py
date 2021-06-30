# -*- coding: utf-8 -*-

from typing import Dict, List, Any
from recc.core.mixin.context_base import ContextBase
from recc.session.session import Session
from recc.template.v1 import keys as v1k


class ContextStorage(ContextBase):
    async def get_templates_v1(self, _: Session) -> List[Dict[str, Any]]:
        result = list()
        for k, v in self.storage.get_templates().items():
            template_dict = v.serialize_v1()
            if v1k.k_info not in template_dict:
                continue
            template_dict[v1k.k_info][v1k.k_name] = str(k)
            result.append(template_dict)
        return result

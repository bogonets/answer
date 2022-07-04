# -*- coding: utf-8 -*-

from typing import Any, Dict, List

from recc.core.mixin.context_base import ContextBase
from recc.template.v2 import keys


class ContextStorage(ContextBase):
    async def get_templates_v1(self) -> List[Dict[str, Any]]:
        result = list()
        for k, v in self._local_storage.get_templates().items():
            template_dict = v.__serialize__()
            if keys.k_information not in template_dict:
                continue
            template_dict[keys.k_information][keys.k_name] = str(k)
            result.append(template_dict)
        return result

# -*- coding: utf-8 -*-

from typing import Any, Dict, Optional

from type_serialize import Serializable

from recc.serialization.utils import update_dict
from recc.template.v2 import keys as v2k


class Dependency(Serializable):
    category: Optional[str] = None
    source: Optional[str] = None
    destination: Optional[str] = None
    extra: Optional[Any] = None

    def clear(self) -> None:
        self.category = None
        self.source = None
        self.destination = None
        self.extra = None

    def __serialize__(self) -> Any:
        result: Dict[str, Any] = dict()
        update_dict(result, v2k.k_category, self.category)
        update_dict(result, v2k.k_source, self.source)
        update_dict(result, v2k.k_destination, self.destination)
        update_dict(result, v2k.k_extra, self.extra)
        return result

    def __deserialize__(self, data: Any) -> None:
        self.clear()
        if data is None:
            return
        if not isinstance(data, dict):
            raise TypeError
        self.category = data.get(v2k.k_category)
        self.source = data.get(v2k.k_source)
        self.destination = data.get(v2k.k_destination)
        self.extra = data.get(v2k.k_extra)

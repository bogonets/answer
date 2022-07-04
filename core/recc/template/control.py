# -*- coding: utf-8 -*-

from typing import Any, Dict, List, Optional

from type_serialize import Serializable

from recc.serialization.utils import update_dict
from recc.template.v2 import keys as v2k


class Control(Serializable):
    name: Optional[str] = None
    mimes: Optional[List[str]] = None

    def clear(self) -> None:
        self.name = None
        self.mimes = None

    def __serialize__(self) -> Any:
        result: Dict[str, Any] = dict()
        update_dict(result, v2k.k_name, self.name)
        update_dict(result, v2k.k_mimes, self.mimes)
        return result

    def __deserialize__(self, data: Any) -> None:
        self.clear()
        if data is None:
            return
        if not isinstance(data, dict):
            raise TypeError
        self.name = data.get(v2k.k_name)
        self.mimes = data.get(v2k.k_mimes)

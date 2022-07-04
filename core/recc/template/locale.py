# -*- coding: utf-8 -*-

from copy import deepcopy
from typing import Any, Dict

from type_serialize import Serializable


class Locale(Dict[str, str], Serializable):
    def __serialize__(self) -> Any:
        return deepcopy(dict(self))

    def __deserialize__(self, data: Any) -> None:
        self.clear()
        if data is None:
            return
        if not isinstance(data, dict):
            raise TypeError
        self.update(data)

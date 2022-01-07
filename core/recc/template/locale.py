# -*- coding: utf-8 -*-

from typing import Dict, Any
from copy import deepcopy
from recc.serialization.interface import Serializable


class Locale(Dict[str, str], Serializable):
    def serialize(self, version: int) -> Any:
        if version == 1:
            return self.serialize_v1()
        else:
            return self.serialize_v2()

    def deserialize(self, version: int, data: Any) -> None:
        self.clear()
        if data is None:
            return
        if version == 1:
            self.deserialize_v1(data)
        else:
            self.deserialize_v2(data)

    def deserialize_v1(self, data: Any) -> None:
        if not isinstance(data, dict):
            raise TypeError
        self.update(data)

    def serialize_v1(self) -> Dict[str, Any]:
        return deepcopy(dict(self))

    def deserialize_v2(self, data: Any) -> None:
        if not isinstance(data, dict):
            raise TypeError
        self.update(data)

    def serialize_v2(self) -> Dict[str, Any]:
        return deepcopy(dict(self))

# -*- coding: utf-8 -*-

from typing import Dict, Any, Optional, List
from recc.serialization.utils import update_dict, normalize_strings
from recc.serialization.interface import Serializable
from recc.template.v1 import keys as v1k
from recc.template.v2 import keys as v2k


class Control(Serializable):

    name: Optional[str] = None
    mimes: Optional[List[str]] = None

    def clear(self) -> None:
        self.name = None
        self.mimes = None

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
        if isinstance(data, str):
            self.name = data
            return
        if not isinstance(data, dict):
            raise TypeError
        self.name = data.get(v1k.k_name)
        self.mimes = normalize_strings(data.get(v1k.k_mimes))

    def serialize_v1(self) -> Dict[str, Any]:
        result: Dict[str, Any] = dict()
        update_dict(result, v1k.k_name, self.name)
        update_dict(result, v1k.k_mimes, self.mimes)
        return result

    def deserialize_v2(self, data: Any) -> None:
        if not isinstance(data, dict):
            raise TypeError
        self.name = data.get(v2k.k_name)
        self.mimes = data.get(v2k.k_mimes)

    def serialize_v2(self) -> Dict[str, Any]:
        result: Dict[str, Any] = dict()
        update_dict(result, v2k.k_name, self.name)
        update_dict(result, v2k.k_mimes, self.mimes)
        return result

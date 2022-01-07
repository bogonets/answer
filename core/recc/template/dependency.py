# -*- coding: utf-8 -*-

from typing import Optional, Any, Dict
from recc.serialization.utils import update_dict
from recc.serialization.interface import Serializable
from recc.template.v1 import keys as v1k
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
        self.category = data.get(v1k.k_type)
        self.source = data.get(v1k.k_src)
        self.destination = data.get(v1k.k_dest)
        self.extra = data.get(v1k.k_extra)

    def serialize_v1(self) -> Dict[str, Any]:
        result: Dict[str, Any] = dict()
        update_dict(result, v1k.k_type, self.category)
        update_dict(result, v1k.k_src, self.source)
        update_dict(result, v1k.k_dest, self.destination)
        update_dict(result, v1k.k_extra, self.extra)
        return result

    def deserialize_v2(self, data: Any) -> None:
        if not isinstance(data, dict):
            raise TypeError
        self.category = data.get(v2k.k_category)
        self.source = data.get(v2k.k_source)
        self.destination = data.get(v2k.k_destination)
        self.extra = data.get(v2k.k_extra)

    def serialize_v2(self) -> Dict[str, Any]:
        result: Dict[str, Any] = dict()
        update_dict(result, v2k.k_category, self.category)
        update_dict(result, v2k.k_source, self.source)
        update_dict(result, v2k.k_destination, self.destination)
        update_dict(result, v2k.k_extra, self.extra)
        return result

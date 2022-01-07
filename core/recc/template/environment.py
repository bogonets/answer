# -*- coding: utf-8 -*-

from typing import Optional, Any, Dict
from enum import Enum
from recc.serialization.utils import update_dict
from recc.serialization.interface import Serializable
from recc.template.v1 import keys as v1k
from recc.template.v2 import keys as v2k


class EnvironmentCategory(Enum):
    Unknown = 0
    Pyenv = 1
    System = 2

    @classmethod
    def from_str(cls, text: str):
        status_key = text[0].upper() + text[1:].lower()
        statuses = [s for s in dir(cls) if not s.startswith("_")]
        if status_key in statuses:
            return getattr(cls, status_key)
        return EnvironmentCategory.Unknown


class Environment(Serializable):

    category: Optional[str] = None
    name: Optional[str] = None

    def clear(self) -> None:
        self.category = None
        self.name = None

    def get_category(self) -> EnvironmentCategory:
        if not self.category:
            return EnvironmentCategory.Unknown
        return EnvironmentCategory.from_str(self.category.strip())

    def is_unknown(self) -> bool:
        return self.get_category() == EnvironmentCategory.Unknown

    def is_pyenv(self) -> bool:
        return self.get_category() == EnvironmentCategory.Pyenv

    def is_system(self) -> bool:
        return self.get_category() == EnvironmentCategory.System

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
        self.name = data.get(v1k.k_name)

    def serialize_v1(self) -> Dict[str, Any]:
        result: Dict[str, Any] = dict()
        update_dict(result, v1k.k_type, self.category)
        update_dict(result, v1k.k_name, self.name)
        return result

    def deserialize_v2(self, data: Any) -> None:
        if not isinstance(data, dict):
            raise TypeError
        self.category = data.get(v2k.k_category)
        self.name = data.get(v2k.k_name)

    def serialize_v2(self) -> Dict[str, Any]:
        result: Dict[str, Any] = dict()
        update_dict(result, v2k.k_category, self.category)
        update_dict(result, v2k.k_name, self.name)
        return result

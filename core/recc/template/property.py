# -*- coding: utf-8 -*-

from typing import Any, Dict, List, Optional

from type_serialize import deserialize, serialize
from type_serialize.obj.interface import Serializable

from recc.serialization.utils import update_dict
from recc.template.locale import Locale
from recc.template.v2 import keys as v2k

VALUE_TYPE_V1_STR = "str"
VALUE_TYPE_V1_BOOL = "bool"
VALUE_TYPE_V1_INT = "int"
VALUE_TYPE_V1_UNSIGNED = "unsigned"
VALUE_TYPE_V1_SIZE = "size"
VALUE_TYPE_V1_FLOAT = "float"
VALUE_TYPE_V1_DOUBLE = "double"
VALUE_TYPE_V1_JSON = "json"
VALUE_TYPE_V1_CSV = "csv"
VALUE_TYPE_V1_COLOR = "color"
VALUE_TYPE_V1_DURATION = "duration"
VALUE_TYPE_V1_BYTE = "byte"
VALUE_TYPE_V1_TIME = "time"
VALUE_TYPE_V1_BOX_JSON = "box_json"  # Deprecated
VALUE_TYPES_V1 = (
    VALUE_TYPE_V1_STR,
    VALUE_TYPE_V1_BOOL,
    VALUE_TYPE_V1_INT,
    VALUE_TYPE_V1_UNSIGNED,
    VALUE_TYPE_V1_SIZE,
    VALUE_TYPE_V1_FLOAT,
    VALUE_TYPE_V1_DOUBLE,
    VALUE_TYPE_V1_JSON,
    VALUE_TYPE_V1_CSV,
    VALUE_TYPE_V1_COLOR,
    VALUE_TYPE_V1_DURATION,
    VALUE_TYPE_V1_BYTE,
    VALUE_TYPE_V1_TIME,
    VALUE_TYPE_V1_BOX_JSON,
)


class Property(Serializable):
    name: Optional[str] = None
    category: Optional[str] = None
    rule: Optional[str] = None
    value_type: Optional[str] = None
    value_default: Optional[Any] = None
    required: Optional[bool] = None
    choice: Optional[List[str]] = None
    hint: Optional[List[str]] = None
    minimum: Optional[float] = None
    maximum: Optional[float] = None
    password: Optional[bool] = None
    advance: Optional[bool] = None
    hide: Optional[bool] = None
    style: Optional[str] = None
    titles: Optional[Locale] = None
    helps: Optional[Locale] = None

    def clear(self) -> None:
        self.name = None
        self.category = None
        self.rule = None
        self.value_type = None
        self.value_default = None
        self.required = None
        self.choice = None
        self.hint = None
        self.minimum = None
        self.maximum = None
        self.password = None
        self.advance = None
        self.hide = None
        self.style = None
        self.titles = None
        self.helps = None

    def __serialize__(self) -> Any:
        result: Dict[str, Any] = dict()
        update_dict(result, v2k.k_name, self.name)
        update_dict(result, v2k.k_category, self.category)
        update_dict(result, v2k.k_rule, self.rule)
        update_dict(result, v2k.k_value_type, self.value_type)
        update_dict(result, v2k.k_value_default, self.value_default)
        update_dict(result, v2k.k_required, self.required)
        if self.choice is not None:
            result[v2k.k_choice] = serialize(self.choice)
        if self.hint is not None:
            result[v2k.k_hint] = serialize(self.hint)
        update_dict(result, v2k.k_minimum, self.minimum)
        update_dict(result, v2k.k_maximum, self.maximum)
        update_dict(result, v2k.k_password, self.password)
        update_dict(result, v2k.k_advance, self.advance)
        update_dict(result, v2k.k_hide, self.hide)
        update_dict(result, v2k.k_style, self.style)
        if self.titles is not None:
            result[v2k.k_titles] = serialize(self.titles)
        if self.helps is not None:
            result[v2k.k_helps] = serialize(self.helps)
        return result

    def __deserialize__(self, data: Any) -> None:
        self.clear()
        if data is None:
            return
        if not isinstance(data, dict):
            raise TypeError
        self.category = data.get(v2k.k_category)
        self.name = data.get(v2k.k_name)
        self.rule = data.get(v2k.k_rule)
        self.value_type = data.get(v2k.k_value_type)
        self.value_default = data.get(v2k.k_value_default)
        self.required = data.get(v2k.k_required)
        self.choice = data.get(v2k.k_choice)
        self.hint = data.get(v2k.k_hint)
        self.minimum = data.get(v2k.k_minimum)
        self.maximum = data.get(v2k.k_maximum)
        self.password = data.get(v2k.k_password)
        self.advance = data.get(v2k.k_advance)
        self.hide = data.get(v2k.k_hide)
        self.style = data.get(v2k.k_style)

        titles_val = data.get(v2k.k_titles)
        helps_val = data.get(v2k.k_helps)
        self.titles = deserialize(titles_val, Optional[Locale])
        self.helps = deserialize(helps_val, Optional[Locale])

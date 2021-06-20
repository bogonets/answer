# -*- coding: utf-8 -*-

from typing import Dict, Any, Optional, List
from functools import reduce
from recc.serializable.serializable import Serializable, update_dict
from recc.serializable.deserialize import deserialize
from recc.serializable.serialize import serialize
from recc.template.locale import Locale
from recc.template.v1 import keys as v1k
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

        valid = data.get(v1k.k_valid, dict())
        if not isinstance(valid, dict):
            raise TypeError

        choice: Optional[List[str]]
        valid_list = valid.get(v1k.k_list)
        if valid_list is not None:
            if not isinstance(valid_list, str):
                raise TypeError
            choice = valid_list.split(v1k.separator_valid)
        else:
            choice = None

        hint: Optional[List[str]]
        valid_hint = valid.get(v1k.k_hint)
        if valid_hint is not None:
            if not isinstance(valid_hint, str):
                raise TypeError
            hint = valid_hint.split(v1k.separator_valid)
        else:
            hint = None

        self.category = data.get(v1k.k_category)
        self.name = data.get(v1k.k_name)
        self.rule = data.get(v1k.k_rule)
        self.value_type = data.get(v1k.k_type)
        self.value_default = data.get(v1k.k_default_value)
        self.required = data.get(v1k.k_required)
        self.choice = choice
        self.hint = hint
        self.minimum = valid.get(v1k.k_min)
        self.maximum = valid.get(v1k.k_max)
        self.password = valid.get(v1k.k_password)
        self.advance = valid.get(v1k.k_advance)
        self.hide = valid.get(v1k.k_hide)
        self.style = valid.get(v1k.k_style)
        self.helps = data.get(v1k.k_help)

        locale_hint = Optional[Locale]
        titles_val = data.get(v1k.k_title)
        helps_val = data.get(v1k.k_help)
        self.titles = deserialize(1, titles_val, Locale, locale_hint)
        self.helps = deserialize(1, helps_val, Locale, locale_hint)

    def serialize_v1(self) -> Dict[str, Any]:
        result: Dict[str, Any] = dict()
        update_dict(result, v1k.k_type, self.category)
        update_dict(result, v1k.k_name, self.name)
        update_dict(result, v1k.k_name, self.name)
        update_dict(result, v1k.k_category, self.category)
        update_dict(result, v1k.k_rule, self.rule)
        update_dict(result, v1k.k_default_value, self.value_default)
        update_dict(result, v1k.k_type, self.value_type)
        update_dict(result, v1k.k_required, self.required)

        valid_list: Optional[str]
        if self.choice is None:
            valid_list = None
        else:
            valid_list = reduce(lambda x, y: x + v1k.separator_valid + y, self.choice)

        valid_hint: Optional[str]
        if self.hint is None:
            valid_hint = None
        else:
            valid_hint = reduce(lambda x, y: x + v1k.separator_valid + y, self.hint)

        valid: Dict[str, Any] = dict()
        update_dict(valid, v1k.k_list, valid_list)
        update_dict(valid, v1k.k_hint, valid_hint)
        update_dict(valid, v1k.k_min, self.minimum)
        update_dict(valid, v1k.k_max, self.maximum)
        update_dict(valid, v1k.k_password, self.password)
        update_dict(valid, v1k.k_advance, self.advance)
        update_dict(valid, v1k.k_hide, self.hide)
        update_dict(valid, v1k.k_style, self.style)

        # Even if it is an empty `valid`, it must be added.
        update_dict(result, v1k.k_valid, valid)

        if self.titles is not None:
            result[v1k.k_title] = serialize(1, self.titles)
        if self.helps is not None:
            result[v1k.k_help] = serialize(1, self.helps)

        return result

    def deserialize_v2(self, data: Any) -> None:
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

        locale_hint = Optional[Locale]
        titles_val = data.get(v2k.k_titles)
        helps_val = data.get(v2k.k_helps)
        self.titles = deserialize(1, titles_val, Locale, locale_hint)
        self.helps = deserialize(1, helps_val, Locale, locale_hint)

    def serialize_v2(self) -> Dict[str, Any]:
        result: Dict[str, Any] = dict()
        update_dict(result, v2k.k_name, self.name)
        update_dict(result, v2k.k_category, self.category)
        update_dict(result, v2k.k_rule, self.rule)
        update_dict(result, v2k.k_value_type, self.value_type)
        update_dict(result, v2k.k_value_default, self.value_default)
        update_dict(result, v2k.k_required, self.required)
        if self.choice is not None:
            result[v2k.k_choice] = serialize(2, self.choice)
        if self.hint is not None:
            result[v2k.k_hint] = serialize(2, self.hint)
        update_dict(result, v2k.k_minimum, self.minimum)
        update_dict(result, v2k.k_maximum, self.maximum)
        update_dict(result, v2k.k_password, self.password)
        update_dict(result, v2k.k_advance, self.advance)
        update_dict(result, v2k.k_hide, self.hide)
        update_dict(result, v2k.k_style, self.style)
        if self.titles is not None:
            result[v2k.k_titles] = serialize(2, self.titles)
        if self.helps is not None:
            result[v2k.k_helps] = serialize(2, self.helps)
        return result

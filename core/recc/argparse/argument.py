# -*- coding: utf-8 -*-

from typing import List, Any, Dict, Union, Optional, Mapping, Type, Iterable
from re import compile as re_compile
from enum import Enum

ValueType = Optional[Union[str, int, float, bool]]
MapType = Mapping[str, Any]


# def merge_choices(choices: Collection[Any]) -> str:
#     it = iter(choices)
#     result: str
#     first = next(it)
#     if isinstance(first, str):
#         result = f"'{first}'"
#     else:
#         result = str(first)
#     for element in it:
#         if isinstance(element, str):
#             result += f", '{element}'"
#         else:
#             result += f", {element}"
#     return result
#
#
# def make_help(
#     text: str,
#     default_value: Optional[Any] = None,
#     choices: Optional[Collection[Any]] = None,
# ) -> str:
#     default_text: Optional[str] = None
#     if default_value is not None:
#         if isinstance(default_value, str):
#             default_text = f"'{default_value}'"
#         else:
#             default_text = str(default_value)
#
#     if choices and len(choices) >= 2:
#         choose_text = merge_choices(choices)
#         if default_text is not None:
#             return f"{text} (Choose from {choose_text}; default: {default_text})"
#         else:
#             return f"{text} (Choose from {choose_text})"
#
#     if default_text is not None:
#         return f"{text} (default: {default_text})"
#     return text

KEY_NAME_REGEX = re_compile(r"^[0-9A-Za-z_\-]*$")
NORMALIZE_REGEX = re_compile(r"^[0-9a-z_]*$")


def valid_key_name(key: str) -> None:
    if KEY_NAME_REGEX.match(key):
        return

    msg1 = "Invalid key name."
    msg2 = f"A valid regular expression is `{KEY_NAME_REGEX.pattern}`."
    msg3 = f"The verified key name is `{key}`."
    raise KeyError(f"{msg1} {msg2} {msg3}")


def valid_normalize_name(key: str) -> None:
    if NORMALIZE_REGEX.match(key):
        return

    msg1 = "Invalid normalize key name."
    msg2 = f"A valid regular expression is `{NORMALIZE_REGEX.pattern}`"
    msg3 = f"The verified key name is `{key}`."
    raise KeyError(f"{msg1} {msg2} {msg3}")


def remove_start_with_dash(key: str) -> str:
    for i, c in enumerate(key):
        if c == "-":
            continue
        return key[i:]
    raise ValueError(f"Invalid key name: {key}")


class Shortcut(Enum):
    b = "b"  # http-Bind
    c = "c"  # Config
    d = "d"  # Developer (Debug)
    h = "h"  # Help (Don't use this flag)
    k = "k"  # signature Key
    p = "p"  # http-Port
    v = "v"  # Verbose


class Argument:

    _long_key: str
    _normalize_key: str
    _short_key: Optional[str]
    _keys: List[str]
    _last_injection_value: Any
    _kwargs: Dict[str, Any]

    def __init__(
        self,
        *,
        key: str,
        last_injection_value: Any,
        shortcut: Optional[Shortcut] = None,
        **kwargs,
    ):
        valid_key_name(key)
        self._long_key = key

        assert last_injection_value is not None
        self._last_injection_value = last_injection_value

        if "dest" in kwargs:
            normalize_key = kwargs["dest"]
        else:
            normalize_key = remove_start_with_dash(key).replace("-", "_").lower()

        valid_normalize_name(normalize_key)
        self._normalize_key = normalize_key

        if shortcut:
            self._short_key = f"-{shortcut.value}"
        else:
            self._short_key = None

        self._keys = [self._long_key]
        if self._short_key:
            self._keys.append(self._short_key)

        self._kwargs = kwargs

    @property
    def long_key(self) -> str:
        return self._long_key

    @property
    def normalize_key(self) -> str:
        return self._normalize_key

    @property
    def keys(self) -> List[str]:
        return self._keys

    @property
    def last_injection_value(self) -> Any:
        return self._last_injection_value

    @property
    def kwargs(self) -> Dict[str, Any]:
        return self._kwargs

    @property
    def dest(self) -> str:
        return self._kwargs.get("dest", "")

    @property
    def nargs(self) -> str:
        return self._kwargs.get("nargs", "")

    @property
    def default(self) -> Any:
        return self._kwargs.get("default", None)

    @property
    def type(self) -> Type:
        return self._kwargs.get("type", str)

    @property
    def metavar(self) -> str:
        return self._kwargs.get("metavar", "")

    @property
    def action(self) -> str:
        return self._kwargs.get("action", "")

    @property
    def choices(self) -> Iterable[str]:
        return self._kwargs.get("choices", list())

    @property
    def help(self) -> str:
        return self._kwargs.get("help", "")

    def inference_type(self) -> Type:
        if "type" in self._kwargs:
            return self._kwargs["type"]

        if "default" in self._kwargs:
            return type(self._kwargs["default"])

        if self._last_injection_value is not None:
            return type(self._last_injection_value)

        return str

    def inference_default_value(self) -> Any:
        cast_type = self.inference_type()

        if "default" in self._kwargs:
            return cast_type(self._kwargs["default"])

        if self._last_injection_value is not None:
            return cast_type(self._last_injection_value)

        return None

    # def get_env_key(self) -> str:
    #     return convert_environment_key(self._env_prefix, self.get_normalize_key())
    #
    # def get_normalize_value_or_none(self, container: MapType) -> ValueType:
    #     key = self.get_normalize_key()
    #     value_type = type(self.default_value)
    #     return get_value_or_none(container, key, value_type)
    #
    # def get_env_value_or_none(self, container: MapType) -> ValueType:
    #     key = self.get_env_key()
    #     value_type = type(self.default_value)
    #     return get_value_or_none(container, key, value_type)

# -*- coding: utf-8 -*-

from typing import List, Any, Dict, Union, Optional, Mapping, Type
from re import compile as re_compile

from recc.argparse.shortcut import Shortcut

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


class Argument:
    def __init__(
        self,
        *,
        key: str,
        last_injection_value: Any,
        cls: Type,
        shortcut: Optional[Shortcut] = None,
        **kwargs,
    ):
        valid_key_name(key)
        self._long_key = key

        if "default" in kwargs:
            raise ValueError(
                "Do not use `default` arguments. Instead, use `last_injection_value`"
            )
        if "type" in kwargs:
            raise ValueError("Do not use `type` arguments. Instead, use `cls`")

        assert last_injection_value is not None
        self._last_injection_value = last_injection_value

        assert isinstance(cls, type)
        self._cls = cls

        if "dest" in kwargs:
            normalize_key = kwargs["dest"]
        else:
            normalize_key = remove_start_with_dash(key).replace("-", "_").lower()

        valid_normalize_name(normalize_key)
        self._normalize_key = normalize_key
        self._short_key = f"-{shortcut.value}" if shortcut else None
        self._keys = [self._long_key]
        if self._short_key:
            self._keys.append(self._short_key)
        assert len(self._keys) == 1 or len(self._keys) == 2

        self._kwargs = kwargs
        if "action" not in kwargs:
            self._kwargs["type"] = cls
        self._kwargs["default"] = None  # IMPORTANT !!

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
    def cls(self) -> Type:
        return self._cls

    @property
    def kwargs(self) -> Dict[str, Any]:
        return self._kwargs

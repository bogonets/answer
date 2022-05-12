# -*- coding: utf-8 -*-

from argparse import Namespace
from re import compile as re_compile
from typing import Any, Dict, List, Mapping, Optional, Type, Union, get_args, get_origin

from recc.argparse.shortcut import Shortcut
from recc.variables.environment import RECC_ENV_FILE_SUFFIX, RECC_ENV_PREFIX

ValueType = Optional[Union[str, int, float, bool]]
MapType = Mapping[str, Any]

KEY_NAME_REGEX = re_compile(r"^[0-9A-Za-z_\-]*$")
NORMALIZE_REGEX = re_compile(r"^[0-9a-z_]*$")
RECC_ENV_PREFIX_LOWER = RECC_ENV_PREFIX.lower()
RECC_ENV_FILE_SUFFIX_LOWER = RECC_ENV_FILE_SUFFIX.lower()


def valid_key_name(key: str) -> None:
    if KEY_NAME_REGEX.match(key):
        return

    msg1 = "Invalid key name."
    msg2 = f"A valid regular expression is `{KEY_NAME_REGEX.pattern}`."
    msg3 = f"The verified key name is `{key}`."
    raise KeyError(f"{msg1} {msg2} {msg3}")


def valid_normalize_name(key: str) -> None:
    if key.startswith(RECC_ENV_PREFIX_LOWER):
        raise KeyError(
            f"Using the prefix `{RECC_ENV_PREFIX_LOWER}`"
            "will cause problems when reading environment variables"
        )
    if key.endswith(RECC_ENV_FILE_SUFFIX_LOWER):
        raise KeyError(
            f"Using the suffix `{RECC_ENV_FILE_SUFFIX_LOWER}`"
            "will cause problems when reading environment variables"
        )
    if not NORMALIZE_REGEX.match(key):
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
        cls: Any,
        delimiter: Optional[str] = None,
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

        cls_origin = get_origin(cls)
        if cls_origin is None:
            assert isinstance(cls, type)
            if delimiter is not None:
                raise ValueError("Do not use `delimiter` arguments")
        else:
            assert isinstance(cls_origin, type)
            if delimiter is None:
                raise ValueError("Must use the `delimiter` arguments")
            if cls_origin != list:
                raise TypeError(
                    f"The Generic class only supports the List type (Actually `{cls}`)"
                )

        self._cls = cls
        self._delimiter = delimiter

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
    def cls(self) -> Any:
        return self._cls

    @property
    def cls_origin(self) -> Type:
        origin = get_origin(self._cls)
        if origin is None:
            assert isinstance(self._cls, type)
            return self._cls
        else:
            assert isinstance(origin, type)
            return origin

    @property
    def kwargs(self) -> Dict[str, Any]:
        return self._kwargs

    def cast(self, data: Any) -> Any:
        origin = get_origin(self._cls)
        if origin is None:
            if isinstance(data, self._cls):
                return data
            else:
                return self._cls(data)

        assert origin == list, "The Generic class only supports the List type"
        cls_args = get_args(self._cls)
        assert len(cls_args) == 1
        cls_arg0_type = cls_args[0]
        assert isinstance(cls_arg0_type, type)

        if isinstance(data, list):
            return [cls_arg0_type(d) for d in data]
        elif isinstance(data, str):
            assert self._delimiter is not None
            return [cls_arg0_type(d) for d in data.split(self._delimiter)]
        else:
            return [cls_arg0_type(data)]

    def inject_to_namespace(self, namespace: Namespace) -> Namespace:
        key = self.normalize_key
        value = getattr(namespace, key, None)

        if value is None:
            setattr(namespace, key, self.last_injection_value)
        elif not isinstance(value, self.cls_origin):
            setattr(namespace, key, self.cast(value))

        return namespace

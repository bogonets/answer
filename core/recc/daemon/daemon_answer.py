# -*- coding: utf-8 -*-

from functools import reduce
from typing import Any, Dict, List, Type, TypeVar, Union

from type_serialize import deserialize

_T = TypeVar("_T")


class DaemonAnswer:

    args: List[Any]
    kwargs: Dict[str, Any]

    def __init__(self, *args, **kwargs):
        self.args = list(args) if args else list()
        self.kwargs = {k: v for k, v in kwargs.items()} if kwargs else dict()

    @property
    def is_args(self) -> bool:
        return bool(self.args)

    @property
    def is_kwargs(self) -> bool:
        return bool(self.kwargs)

    def to_args_str(self) -> str:
        return reduce(lambda x, y: f"{x},{y}", self.args)

    def to_kwargs_str(self) -> str:
        result = str()
        keys = iter(self.kwargs.keys())
        try:
            k = next(keys)
            result += f"{k}={self.kwargs[k]}"
            while True:
                k = next(keys)
                result += f",{k}={self.kwargs[k]}"
        except StopIteration:
            pass
        return result

    def to_str(self) -> str:
        if self.is_args:
            return f"DaemonAnswer[{self.to_args_str()}]"
        elif self.is_kwargs:
            return f"DaemonAnswer{{{self.to_kwargs_str()}}}"
        else:
            return "DaemonAnswer(-)"

    def __str__(self) -> str:
        return self.to_str()

    def __repr__(self) -> str:
        return self.to_str()

    def size(self) -> int:
        if self.is_args:
            return len(self.args)
        elif self.is_kwargs:
            return len(self.kwargs)
        else:
            return 0

    def __len__(self) -> int:
        return self.size()

    def get(self, key: Union[int, str]) -> Any:
        if isinstance(key, int):
            return self.args[key]
        elif isinstance(key, str):
            return self.kwargs[key]
        else:
            raise KeyError(f"Unsupported key type: {type(key).__name__}")

    def __getitem__(self, item: Union[int, str]) -> Any:
        return self.get(item)

    def cast(self, key: Union[int, str], cls: Type[_T]) -> _T:
        if isinstance(key, int):
            return deserialize(self.args[key], cls)
        elif isinstance(key, str):
            return deserialize(self.kwargs[key], cls)
        else:
            raise KeyError(f"Unsupported key type: {type(key).__name__}")

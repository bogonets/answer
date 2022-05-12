# -*- coding: utf-8 -*-

from inspect import Parameter
from typing import Any, Union, get_origin


def get_type_origin(param: Parameter) -> Any:
    result = get_origin(param.annotation)
    if result is None:
        if isinstance(param.annotation, type):
            result = param.annotation
        elif isinstance(param.annotation, str):
            if param.annotation == "str":
                result = str
            elif param.annotation == "int":
                result = int
            elif param.annotation == "float":
                result = float
            elif param.annotation == "bytes":
                result = bytes
            elif param.annotation == "list":
                result = list
            elif param.annotation == "set":
                result = set
            elif param.annotation == "dict":
                result = dict
            else:
                msg = f"Unknown annotation string: {param.annotation}"
                raise NotImplementedError(msg)
        else:
            msg = f"Unknown annotation type: {type(param.annotation).__name__}"
            raise NotImplementedError(msg)

    assert result is not None
    assert isinstance(result, type) or result is Union

    return result
